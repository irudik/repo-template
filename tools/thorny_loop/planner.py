"""Sparse planner client and parser helpers."""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from typing import Any

from .config import ThornyConfig
from .schemas import PlannerDecision, UsageSummary


PLAN_JSON_BEGIN = "PLAN_JSON_BEGIN"
PLAN_JSON_END = "PLAN_JSON_END"
BACKGROUND_PENDING_STATUSES = {"queued", "in_progress"}
BACKGROUND_FAILURE_STATUSES = {"failed", "cancelled", "incomplete"}


class PlannerParseError(RuntimeError):
    """Raised when planner output cannot be repaired into valid JSON."""

    def __init__(self, message: str, raw_output: str):
        super().__init__(message)
        self.raw_output = raw_output


@dataclass
class PlannerResponse:
    """Bundle the parsed decision together with raw text and usage."""

    decision: PlannerDecision
    raw_output: str
    usage_summary: UsageSummary


def build_planner_instructions() -> str:
    """Return the stable planner system instructions."""

    return (
        "You are the sparse planner for a repo-local thorny-problem escalation loop.\n"
        "Decide only the next minimal reversible increment.\n"
        f"Return JSON only between {PLAN_JSON_BEGIN} and {PLAN_JSON_END}.\n"
        "Do not include prose outside the markers.\n"
        "If blocked, ask only the smallest user decision required.\n"
        "Keep the next increment scoped, evidence-based, and limited to a few files."
    )


def build_planner_prompt(
    task: str,
    context_text: str,
    *,
    why_called: str,
    state_summary: str,
) -> str:
    """Build the planner input from the rolling summary and current evidence bundle."""

    schema_description = {
        "status": "continue | done | blocked",
        "why_called": "initial | stalled | cross_cutting | final_review",
        "diagnosis": "string",
        "risk_flags": ["string"],
        "next_increment": {
            "objective": "string",
            "files_to_touch": ["string"],
            "constraints": ["string"],
            "verification_commands": ["string"],
            "review_requests": [{"skill": "review-r|review-julia|review-tex|review-comments", "target": "string"}],
            "acceptance_criteria": ["string"],
        },
        "questions_for_user": ["string"],
        "stop_if": ["string"],
    }
    return (
        f"Task:\n{task}\n\n"
        f"Planner call reason: {why_called}\n\n"
        f"Rolling summary:\n{state_summary.strip() or 'No prior summary available.'}\n\n"
        f"Schema:\n{json.dumps(schema_description, indent=2)}\n\n"
        f"Evidence bundle:\n{context_text}\n"
    )


def extract_plan_json(raw_output: str) -> str:
    """Extract the JSON payload from planner marker blocks or a repaired fallback."""

    marker_pattern = re.compile(
        rf"{PLAN_JSON_BEGIN}\s*(.*?)\s*{PLAN_JSON_END}",
        re.DOTALL,
    )
    match = marker_pattern.search(raw_output)
    if match:
        return match.group(1).strip()

    cleaned = raw_output.replace("```json", "").replace("```", "").strip()
    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")
    if first_brace == -1 or last_brace == -1 or last_brace <= first_brace:
        raise PlannerParseError("Planner output did not contain a JSON payload.", raw_output)
    return cleaned[first_brace : last_brace + 1].strip()


def parse_planner_decision(raw_output: str) -> PlannerDecision:
    """Validate planner output, performing one local repair pass on failure."""

    try:
        payload = extract_plan_json(raw_output)
        return PlannerDecision.model_validate_json(payload)
    except Exception:
        repaired_output = raw_output.replace("\u201c", '"').replace("\u201d", '"')
        try:
            payload = extract_plan_json(repaired_output)
            return PlannerDecision.model_validate_json(payload)
        except Exception as exc:
            raise PlannerParseError("Planner output could not be repaired into valid JSON.", raw_output) from exc


def _response_text(response: Any) -> str:
    output_text = getattr(response, "output_text", "")
    if output_text:
        return str(output_text)
    output = getattr(response, "output", []) or []
    chunks: list[str] = []
    for item in output:
        for content in getattr(item, "content", []) or []:
            text = getattr(content, "text", None)
            if text:
                chunks.append(text)
    return "\n".join(chunks)


def _usage_summary(response: Any) -> UsageSummary:
    usage = getattr(response, "usage", None)
    if usage is None:
        return UsageSummary()
    input_tokens = int(getattr(usage, "input_tokens", 0) or 0)
    output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
    total_tokens = int(getattr(usage, "total_tokens", input_tokens + output_tokens) or 0)
    input_rate = float(os.getenv("THORNY_COST_PER_1K_INPUT_USD", "0"))
    output_rate = float(os.getenv("THORNY_COST_PER_1K_OUTPUT_USD", "0"))
    estimated_cost = (input_tokens / 1000.0 * input_rate) + (output_tokens / 1000.0 * output_rate)
    return UsageSummary(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        estimated_cost_usd=round(estimated_cost, 6),
    )


def _wait_for_background_response(
    client: Any,
    response: Any,
    *,
    timeout_seconds: int = 300,
    poll_interval_seconds: float = 1.0,
) -> Any:
    """Poll a background planner response until it reaches a terminal status."""

    status = getattr(response, "status", "")
    if status not in BACKGROUND_PENDING_STATUSES:
        return response

    response_id = getattr(response, "id", "")
    if not response_id:
        raise RuntimeError("Background planner response is missing an id for retrieval.")

    deadline = time.monotonic() + timeout_seconds
    while status in BACKGROUND_PENDING_STATUSES:
        if time.monotonic() >= deadline:
            raise RuntimeError(
                f"Background planner response did not complete within {timeout_seconds} seconds."
            )
        time.sleep(poll_interval_seconds)
        response = client.responses.retrieve(response_id)
        status = getattr(response, "status", "")

    if status in BACKGROUND_FAILURE_STATUSES:
        raise RuntimeError(f"Background planner response ended with status={status}.")
    return response


def call_planner(
    config: ThornyConfig,
    *,
    task: str,
    context_text: str,
    why_called: str,
    effort: str,
    state_summary: str,
) -> PlannerResponse:
    """Call the Responses API planner and parse the result."""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for live planner calls.")

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    background = config.background_planner in {"1", "true", "always"} or (
        config.background_planner == "auto" and effort == "high"
    )
    response = client.responses.create(
        model=config.planner_model,
        instructions=build_planner_instructions(),
        input=build_planner_prompt(task, context_text, why_called=why_called, state_summary=state_summary),
        reasoning={"effort": effort},
        text={"verbosity": "low"},
        max_output_tokens=config.planner_max_output_tokens,
        background=background,
    )
    response = _wait_for_background_response(client, response)
    raw_output = _response_text(response)
    decision = parse_planner_decision(raw_output)
    return PlannerResponse(decision=decision, raw_output=raw_output, usage_summary=_usage_summary(response))

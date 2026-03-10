"""Persistent Codex MCP session wrapper."""

from __future__ import annotations

import contextlib
import logging
import shutil
from dataclasses import dataclass
from typing import Any

from .config import ThornyConfig


@dataclass
class CodexTurnResult:
    """Structured output from a Codex MCP tool call."""

    thread_id: str
    content: str


@contextlib.contextmanager
def _suppress_mcp_warnings():
    previous_disable = logging.root.manager.disable
    logging.disable(logging.WARNING)
    try:
        yield
    finally:
        logging.disable(previous_disable)


class CodexSession:
    """Keep one Codex MCP thread alive across multiple increments."""

    def __init__(self, config: ThornyConfig):
        self.config = config
        self.thread_id = ""
        self._server = None
        self._connected = False

    def _primary_params(self) -> dict[str, Any]:
        return {"command": self.config.codex_mcp_command, "args": list(self.config.codex_mcp_args)}

    def _fallback_params(self) -> dict[str, Any]:
        return {"command": "npx", "args": ["-y", self.config.codex_mcp_command, *self.config.codex_mcp_args]}

    async def connect(self) -> None:
        """Start the Codex MCP server using the preferred local command or npx fallback."""

        from agents.mcp import MCPServerStdio, MCPServerStdioParams

        candidates: list[dict[str, Any]] = []
        if shutil.which(self.config.codex_mcp_command):
            candidates.append(self._primary_params())
        if shutil.which("npx") and shutil.which("node"):
            candidates.append(self._fallback_params())

        if not candidates:
            raise RuntimeError("Neither codex nor npx/node are available for MCP startup.")

        last_error: Exception | None = None
        for params_dict in candidates:
            params = MCPServerStdioParams(**params_dict)
            server = MCPServerStdio(
                params=params,
                use_structured_content=True,
                client_session_timeout_seconds=300,
            )
            try:
                with _suppress_mcp_warnings():
                    await server.connect()
                    await server.list_tools()
                self._server = server
                self._connected = True
                return
            except Exception as exc:  # pragma: no cover - exercised in live runs
                last_error = exc
                with contextlib.suppress(Exception):
                    await server.cleanup()
        raise RuntimeError("Unable to start Codex MCP session.") from last_error

    async def close(self) -> None:
        """Clean up the active MCP session."""

        if self._server is not None:
            with contextlib.suppress(Exception):
                with _suppress_mcp_warnings():
                    await self._server.cleanup()
        self._server = None
        self._connected = False

    def _parse_result(self, result: Any) -> CodexTurnResult:
        structured = getattr(result, "structuredContent", None)
        if structured:
            thread_id = structured.get("threadId", self.thread_id)
            content = structured.get("content", "")
            return CodexTurnResult(thread_id=thread_id, content=content)

        content_chunks = []
        for item in getattr(result, "content", []) or []:
            text = getattr(item, "text", None)
            if text:
                content_chunks.append(text)
        return CodexTurnResult(thread_id=self.thread_id, content="\n".join(content_chunks))

    async def send_prompt(self, prompt: str) -> CodexTurnResult:
        """Send an increment to the active Codex thread."""

        if not self._connected or self._server is None:
            await self.connect()

        if self.thread_id:
            tool_name = "codex-reply"
            arguments = {"threadId": self.thread_id, "prompt": prompt}
        else:
            tool_name = "codex"
            arguments = {
                "prompt": prompt,
                "cwd": ".",
                "sandbox": "workspace-write",
                "approval-policy": "never",
            }

        with _suppress_mcp_warnings():
            result = await self._server.call_tool(tool_name, arguments)
        parsed = self._parse_result(result)
        self.thread_id = parsed.thread_id or self.thread_id
        return parsed

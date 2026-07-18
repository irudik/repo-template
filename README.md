# AI-Assisted Academic Research Template (Make + R/Julia/Stata/MATLAB)

> **Work in progress.** This is a summary of how I use AI coding assistants for computational research — running analysis pipelines with Make, writing R, Julia, Stata, and MATLAB scripts, and managing build dependencies. I keep updating these files as I learn new things.

A ready-to-fork starter kit for researchers using [Claude Code](https://code.claude.com/docs/en/overview), [OpenAI Codex CLI](https://github.com/openai/codex), or [Kimi Code CLI](https://www.kimi.com/code/docs/en/) with **Make + R + Julia + Stata + MATLAB** build systems. You describe what you want; the assistant selects the appropriate risk tier, implements and tests routine work directly, and adds plans, independent review, or durable context only when the task warrants them.

**All three tools are supported.** Claude Code uses a `CLAUDE.md` hierarchy plus
`.claude/`; Codex CLI uses an `AGENTS.md` hierarchy plus `.codex/` and
`.agents/`; Kimi Code CLI uses the same `AGENTS.md` hierarchy, scans
`.agents/skills/` natively, and mirrors permissions through
`.kimi-code/config.toml.example`. The same workflow, quality gates, and skills
work with each.

---

## Quick Start: Claude Code (5 minutes)

### 1. Fork & Clone

```bash
# Fork this repo on GitHub (click "Fork" on the repo page), then:
git clone https://github.com/YOUR_USERNAME/repo-template.git my-project
cd my-project
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Start Claude Code and Paste This Prompt

```bash
claude
```

**Using VS Code?** Open the Claude Code panel instead. Everything works the same.

Then paste the following, filling in your project details:

> I am starting to work on **[PROJECT NAME]** in this repo. **[Describe your project in 2–3 sentences — what you're building, what data you use, what your pipeline stages are (e.g., data cleaning, estimation, figures).]**
>
> I want our collaboration to be structured, precise, and rigorous. Code should be reproducible, build-system driven, and written for clarity over cleverness.
>
> I've set up the Claude Code academic workflow (forked from `irudik/repo-template`). The configuration files are already in this repo. Please read them, understand the workflow, and then **update all configuration files to fit my project** — fill in placeholders in `CLAUDE.md`, set up the `code/` directory structure with sub-Makefiles for my pipeline stages, and propose any customizations specific to my use case.
>
> After that, use the risk-based workflow: implement and test routine changes
> directly; use a brief in-conversation plan for substantive single-module
> work; and save a plan before high-risk, cross-cutting, numerical, or
> pre-merge work, then continue automatically unless I explicitly request plan
> approval.
>
> Start adapting the workflow configuration for this project.

**Optional for Claude Code + Codex plugin users:** Add this to the prompt when
you want Claude to plan but Codex to execute and verify:

> During planning, mark the implementation and verification steps that Codex
> should own with `[codex]`. After saving the plan, hand those steps to
> Codex through the Codex plugin
> (`codex:codex-rescue`) in write-capable mode. Codex should implement the
> changes, add or update the tests/checks needed to verify them, run that
> proof-of-correctness itself, self-review the diff and verification design,
> report exact evidence, and address at most one Claude-identified fix pass by
> default. Claude then performs one re-review. Leave changes uncommitted unless
> I explicitly ask for a commit.

**What this does:** Claude reads the root and nested `CLAUDE.md` files plus the
tool-specific `.claude/` configuration, sets up your `code/` directory with
sub-Makefiles for each pipeline stage, fills in your project details, then
applies the risk-based workflow: direct execution for routine work and stronger
planning, verification, or review for consequential changes.

### 3. Configure Hooks (Optional)

Hooks are configured per-user in `.claude/settings.json` (gitignored by default). To enable the bundled hooks, create the file with the format below. The `hooks` key uses nested arrays with optional `matcher` and `timeout` fields. `$CLAUDE_PROJECT_DIR` resolves to the project root at runtime.

```bash
cat > .claude/settings.json << 'EOF'
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/notify.sh",
            "timeout": 5
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh",
            "timeout": 5
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/pre-compact.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
EOF
```

---

## Quick Start: Codex CLI (5 minutes)

### 1. Fork & Clone

Same as above — fork this repo, clone it, and `cd` into it.

### 2. Start Codex CLI and Paste This Prompt

```bash
codex
```

Then paste the same project-description prompt as the Claude Code section above.

**What this does:** Codex reads the root `AGENTS.md`, then uses
`code/AGENTS.md` or `latex/AGENTS.md` to load only the conventions needed for
the files in scope.

### 3. Configuration

Codex project configuration lives in:

- **`AGENTS.md`** (root) — project instructions and workflow rules (loaded every session)
- **`code/AGENTS.md`** — router for shared and file-type-specific conventions under `code/conventions/`
- **`latex/AGENTS.md`** — LaTeX conventions (loaded when working in `latex/`)
- **`protocols/skills/*.md`** — canonical shared skill bodies for all three tools
- **`.codex/config.toml`** — model, sandbox, and approval settings
- **`.codex/rules/default.rules`** — command execution permissions (Starlark format)
- **`.agents/skills/*/SKILL.md`** — thin Codex wrappers around the shared protocols

### Claude Code vs Codex CLI vs Kimi Code CLI: Key Differences

| Aspect | Claude Code | Codex CLI | Kimi Code CLI |
|--------|-------------|-----------|---------------|
| Instructions file | `CLAUDE.md` hierarchy | `AGENTS.md` hierarchy | `AGENTS.md` hierarchy |
| Settings | `.claude/settings.json` (JSON) | `.codex/config.toml` (TOML) | `~/.kimi-code/config.toml` (user-level TOML) |
| Permission rules | Glob patterns in settings.json | `.codex/rules/default.rules` (Starlark) | `.kimi-code/config.toml.example` (merge into user config) |
| Project conventions | `CLAUDE.md` hierarchy plus shared `AGENTS.md` local conventions | `AGENTS.md` hierarchy | `AGENTS.md` hierarchy |
| Shared skill bodies | `protocols/skills/*.md` | `protocols/skills/*.md` | `protocols/skills/*.md` |
| Agent definitions | `.claude/agents/*.md` | Not supported | Built-in subagents; no per-repo agent files |
| Skills | Thin wrappers in `.claude/skills/*/SKILL.md` | Thin wrappers in `.agents/skills/*/SKILL.md` | Reuses `.agents/skills/` natively |
| Hooks | `.claude/hooks/*` | Not supported (use git hooks) | User-level `[[hooks]]` in `~/.kimi-code/config.toml` |

### Known Limitations (Codex)

Codex CLI does not support hooks, so these Claude Code features have no direct equivalent:
- **File protection** (`.claude/hooks/protect-files.sh`) — be careful editing `references.bib` and `settings.json`
- **Context snapshot before compaction** (`.claude/hooks/pre-compact.sh`) — save context to plans/ manually
- **Desktop notifications** (`.claude/hooks/notify.sh`) — not available

---

## Quick Start: Kimi Code CLI (5 minutes)

### 1. Fork & Clone

Same as above — fork this repo, clone it, and `cd` into it.

### 2. Start Kimi Code CLI and Paste This Prompt

```bash
kimi
```

Then paste the same project-description prompt as the Claude Code section above.

**What this does:** Kimi Code reads the root `AGENTS.md`, then uses
`code/AGENTS.md` or `latex/AGENTS.md` to load only the conventions needed for
the files in scope. It also scans `.agents/skills/` natively, so all shared
skills work without extra setup.

### 3. Configuration

Kimi Code project integration lives in:

- **`AGENTS.md` hierarchy** — same instructions and workflow rules as Codex CLI
- **`.agents/skills/*/SKILL.md`** — scanned natively; no Kimi-specific wrappers needed
- **`.kimi-code/config.toml.example`** — permission rules mirroring the Claude and Codex configs

Kimi Code reads permissions, models, and hooks from a single user-level config
(`~/.kimi-code/config.toml`); there is no project-level config file for these
settings. Its project-local `.kimi-code/local.toml` only stores workspace
directories and is gitignored. To mirror the template's command permissions,
merge the `[[permission.rules]]` blocks from `.kimi-code/config.toml.example`
into `~/.kimi-code/config.toml`.

### Known Limitations (Kimi)

- **No project-level config for permissions, models, or hooks** — these
  settings are user-level only; keep them in `~/.kimi-code/config.toml`
  (`.kimi-code/local.toml` only stores workspace directories)
- **No tracked skill wrappers of its own** — by design; it reuses
  `.agents/skills/`

---

## How It Works

### Make as the Backbone

A root Makefile delegates to `code/` (analysis pipeline) and `latex/` (manuscript):

```
my-project/
├── Makefile              # Root — delegates to code/ and latex/
├── code/
│   ├── Makefile          # Delegates to sub-Makefiles
│   ├── data_prep/
│   │   ├── Makefile      # Targets for cleaning raw data
│   │   ├── clean.do
│   │   └── merge.R
│   ├── estimation/
│   │   ├── Makefile      # Targets for running models
│   │   ├── model.R
│   │   └── bootstrap.R
│   ├── simulation/
│   │   ├── Makefile      # Targets for trade model simulation
│   │   ├── simulate_trade.jl
│   │   └── process_results.jl
│   ├── structural_model/
│   │   ├── Makefile      # Targets for numerical optimization
│   │   └── solve_equilibrium.m
│   ├── tables/
│   │   ├── Makefile      # Targets for regression tables
│   │   └── reg_tables.do
│   └── figures/
│       ├── Makefile      # Targets for generating plots
│       └── main_figures.R
└── latex/
    ├── Makefile          # pdflatex 3-pass build
    ├── manuscript.tex    # Main paper
    ├── slides.tex        # Presentation slides
    ├── latex_extras/     # Preamble files
    └── references/       # .bib and .bst files
```

- `make` from project root builds everything (code first, then latex)
- `make -n` shows what would be rebuilt (dry-run)
- `make -C code` rebuilds all code targets
- `make -C code/estimation all` rebuilds one pipeline stage
- `make -C latex` compiles the manuscript
- Scripts never create directories — Makefiles own that via order-only prerequisites

Run these Make commands from the project root. `make -C path` changes Make's
working directory to `path`, so targets, prerequisites, and scripts use paths
relative to that directory. For example, code under `code/estimation/` reaches
the project output directory through `../../output`; it does not treat
`output/` as relative to the project root.

### Risk-Based Workflow

The workflow matches process to the consequences of a wrong result:

1. **Routine or bounded change:** implement, test, and report concisely. No
   saved plan, handoff, score, or reviewer agent by default.
2. **Substantive single-module change:** give a brief in-conversation plan,
   implement, test, and use one targeted review only when independence adds
   material value.
3. **High-risk, cross-cutting, numerical, or pre-merge work:** save a plan,
   continue automatically, implement, verify, run one independent review, and
   allow at most one fix/re-review by default. Pause for plan approval only
   when the user explicitly requests it.
4. **Full multi-agent loop:** use only when explicitly requested or when
   failures remain genuinely ambiguous after normal diagnosis.

Tests remain required at every level. Session logs and handoffs preserve
context and major decisions; they are not mandatory stage paperwork. Plan
approval is opt-in; automatic execution does not authorize a commit, push,
merge, destructive operation, or broader scope.

When a review is useful, choose one reviewer for the main risk: the matching
R, Julia, Stata, MATLAB, Makefile, or LaTeX reviewer; domain review for
identification or code-theory alignment; proofreading for presentation; or
trace for an ambiguous cause. Touching several file types does not by itself
justify several agents.

Make verification is also scoped by risk. Dry-run a changed dependency graph,
run the relevant target directly for an ordinary source change under a stable
Makefile, skip Make for documentation-only changes, and use a full root dry run
for cross-cutting or pre-merge checks when the complete build plan adds value.

### Claude + Codex Handoff

When using Claude Code with the Codex plugin available, you can explicitly ask
Claude to plan and then delegate execution to Codex. Put the request in the
original task or planning prompt with language such as "hand this to Codex",
"delegate execution to Codex", "Codex executes", or by marking plan steps with
`[codex]`.

For those marked steps, Claude records the Codex-owned scope and acceptance
criteria in the saved plan. After saving it, Claude hands the plan to
`codex:codex-rescue`; Codex implements the feature/fix and implements the
verification needed to prove it, such as unit tests, example inputs, Makefile
targets, checksum scripts, or data-property checks.

Codex runs in the same checkout and follows the root and nested `AGENTS.md`
instructions, including the routed code conventions and risk-based verification
policy. The recorded handoff supplies the narrower task scope and acceptance
criteria. Codex then self-reviews its diff and verification design, runs the
tests/builds/checks, fixes obvious gaps, and reports the evidence.

Claude reviews the changed code, the verification design, and the reported
results against the acceptance criteria. In this two-agent workflow, Claude's
review is the independent review required for high-risk work, so Codex does not
launch another reviewer by default. If Claude flags gaps, the task goes back to
Codex for one fix followed by one Claude re-review. A fuller loop requires an
explicit request or genuinely ambiguous failures with stated hypotheses and a
stop condition. Claude does not write the verification code or rerun the full
verification loop unless explicitly asked.

This is intentionally Claude-only and does not live in `AGENTS.md`, so Codex
does not read Claude orchestration instructions as its own operating procedure.

### PR Review (`/review-pr`)

When reviewers leave comments on a pull request, `/review-pr <PR#>` automates the triage-fix-reply loop:

1. **Fetches** all unresolved review threads via GitHub's GraphQL API
2. **Classifies** each thread by confidence:
   - **HIGH** — clear code fix (typo, bug, missing import). Implements, commits, replies with the commit hash, and resolves the thread.
   - **MEDIUM** — ambiguous but likely intent. Implements and stages changes but does *not* commit. Presents the interpretation for your approval.
   - **LOW** — design question or unclear fix. Reports the thread with a suggested approach. No code changes.
3. **Groups** fixes by file so each commit is atomic
4. **Runs the applicable risk-based workflow** on each group, including Make verification and targeted review
5. **Pushes** and prints a summary table of what was addressed, what needs approval, and what needs your input

Outdated threads (code has moved since the comment) are reported but never touched.

### Trace (`/trace`)

When the main question is causal rather than implementational, `/trace` runs a
diagnostic workflow that:

1. Restates the observation
2. Generates competing hypotheses
3. Collects evidence for and against each explanation
4. Ranks the explanations by evidence strength
5. Recommends the single best next probe

This is useful for estimate shifts, merge-key problems, stale build behavior,
solver failures, and code-manuscript mismatches.

### Structured Handoffs and Learning

When context must transfer across a person, agent, branch, session, or major
stage, the workflow can write a short handoff under `quality_reports/handoffs/`.
Durable project-specific lessons are stored in `MEMORY.md` using structured
`[LEARN:category]` entries rather than loose bullets.

### Specialized Agents

Focused agents each check one dimension:

| Agent | What It Checks |
|-------|---------------|
| `r-reviewer` | R code quality, reproducibility, domain correctness |
| `julia-reviewer` | Julia code quality, type stability, performance |
| `stata-reviewer` | Stata code quality, data integrity, and research workflow safety |
| `matlab-reviewer` | MATLAB code quality, solver configuration, derivative correctness |
| `domain-reviewer` | Substantive manuscript/slide review: identification, derivations, citations, code-theory alignment |
| `proofreader` | Grammar, typos, overflow risks, and consistency for academic documents |
| `makefile-reviewer` | Makefile conventions, dependency correctness, script coverage |
| `tracer` | Evidence-driven diagnosis for ambiguous failures and output shifts |

For manuscript or slide tasks, choose at most one **opt-in review pass** based
on the main risk unless the user explicitly requests both:
- `domain-reviewer` for substantive identification and citation checks
- `proofreader` for grammar, overflow, and consistency checks

The selected reviewer runs once on the final state and produces a report only;
fixes require user review.

### Quality Gates

Use a score (0–100) for requested or high-risk review and for commit or merge
decisions when the rubric adds value. Do not score every routine edit. When
scoring applies, scores below threshold block the action:
- **80** — commit threshold
- **90** — PR threshold
- **95** — excellence (aspirational)

Rubrics cover R scripts, Julia scripts, Stata scripts, MATLAB scripts, Makefiles, and LaTeX manuscripts. See `AGENTS.md` for the full deduction table.

---

## What's Included

<details>
<summary><strong>Agents, skills, and guidance</strong> (click to expand)</summary>

### Agents (`.claude/agents/`)

| Agent | What It Does |
|-------|-------------|
| `r-reviewer` | R code quality, reproducibility, and domain correctness |
| `julia-reviewer` | Julia code quality, type stability, and performance |
| `stata-reviewer` | Stata code quality, data integrity, and research workflow safety |
| `matlab-reviewer` | MATLAB code quality, solver configuration, derivative correctness |
| `domain-reviewer` | Substantive review for manuscripts, slides, and teaching materials |
| `proofreader` | Academic proofreading for manuscripts, slides, and notes |
| `tex-reviewer` | LaTeX hardcoded-number review for manuscripts and slides |
| `makefile-reviewer` | Makefile conventions, dependency correctness, script coverage |

### Key Skills (`.claude/skills/`)

| Skill | What It Does |
|-------|-------------|
| `/commit` | Stage, commit, PR, merge on the current non-`main` branch; create a branch only when needed |
| `/data-analysis` | End-to-end R analysis workflow |
| `/refactor [file-or-dir]` | Verify-refactor-verify loop for safe style changes |
| `/verify-outputs [script]` | Checksum outputs, compare to reference |
| `/compare-branches [b1] [b2]` | Cross-branch output comparison via worktrees |
| `/resume-custom` | Recover context after compression/new session |
| `/trace [question]` | Evidence-driven diagnosis for ambiguous failures and result shifts |
| `/learn [insight]` | Save a durable, project-specific lesson to `MEMORY.md` |
| `/setup-makefile [dir]` | Generate Makefile from directory contents |
| `/review-pr [PR#]` | Address PR review comments, commit fixes, resolve threads |
| `/review-r [file]` | R code quality review via r-reviewer agent |
| `/review-julia [file]` | Julia code quality review via julia-reviewer agent |
| `/review-stata [file]` | Stata code quality review via stata-reviewer agent |
| `/review-matlab [file]` | MATLAB code quality review via matlab-reviewer agent |
| `/review-tex [file]` | LaTeX hardcoded-number review for manuscripts and slides via tex-reviewer agent |
| `/review-makefile [file]` | Makefile conventions review via makefile-reviewer agent |
| `/review-domain [file]` | Opt-in substantive domain review via domain-reviewer agent |
| `/proofread [file]` | Opt-in proofreading review via proofreader agent |
| `/review-comments [path]` | Clean up comments, docstrings, dead code |
| `/matlab-optim-derivatives` | Audit MATLAB optimization derivatives |

### Shared Skill Protocols (`protocols/skills/`)

Canonical bodies for all 20 shared skills. Both `.claude/skills/` and `.agents/skills/` point at these files, and Claude review agents execute the same protocol files rather than owning separate copies.

### Shared Guidance Surfaces

| File | What It Covers |
|------|----------------|
| `AGENTS.md` | Risk-based workflow, quality gates, verification, and session logging |
| `code/AGENTS.md` | Router that selects the applicable code convention files |
| `code/conventions/shared.md` | Path and research-code conventions used for all code work |
| `code/conventions/{r,julia,stata,matlab,makefile}.md` | File-type-specific conventions loaded only when applicable |
| `latex/AGENTS.md` | Shared LaTeX build, manuscript, and dynamic-number conventions |
| `CLAUDE.md` | Claude-specific loading model, plan-mode notes, and tool-specific mechanics |
| `code/CLAUDE.md` | Claude entry point that loads the shared code conventions |
| `latex/CLAUDE.md` | Claude entry point that loads the shared LaTeX conventions |

### Claude Code Configuration

| Component | Location | Purpose |
|-----------|----------|---------|
| `CLAUDE.md` (root) | Project root | Core workflow rules and project-wide instructions |
| `code/CLAUDE.md` | `code/` | Claude entry point for shared code conventions |
| `latex/CLAUDE.md` | `latex/` | Claude entry point for shared LaTeX conventions |
| `.claude/agents/*.md` | `.claude/agents/` | Review-oriented Claude execution surfaces |
| `.claude/hooks/*` | `.claude/hooks/` | Optional Claude-only hook scripts |
| `.claude/skills/*/SKILL.md` | `.claude/skills/` | Thin Claude wrappers around shared protocols |

### Codex CLI Configuration

| Component | Location | Purpose |
|-----------|----------|---------|
| `AGENTS.md` (root) | Project root | Core instructions + workflow rules |
| `code/AGENTS.md` | `code/` | Router for shared and file-type-specific conventions |
| `latex/AGENTS.md` | `latex/` | LaTeX conventions |
| `protocols/skills/*.md` | `protocols/skills/` | Canonical shared skill bodies |
| `.codex/config.toml` | `.codex/` | Optional Codex project overrides for sandbox, approval, and model behavior |
| `.codex/rules/default.rules` | `.codex/rules/` | Command execution permissions (Starlark) |
| `.agents/skills/*/SKILL.md` | `.agents/skills/` | 20 thin wrappers around the shared protocols |

### Kimi Code CLI Configuration

| Component | Location | Purpose |
|-----------|----------|---------|
| `AGENTS.md` (root) | Project root | Core instructions + workflow rules (shared with Codex CLI) |
| `.agents/skills/*/SKILL.md` | `.agents/skills/` | Scanned natively; same wrappers Codex uses |
| `.kimi-code/config.toml.example` | `.kimi-code/` | Example permission rules to merge into `~/.kimi-code/config.toml` |

</details>

---

## Prerequisites

| Tool | Required For | Install |
|------|-------------|---------|
| [Claude Code](https://code.claude.com/docs/en/overview), [Codex CLI](https://github.com/openai/codex), or [Kimi Code CLI](https://www.kimi.com/code/docs/en/) | AI assistant | `npm install -g @anthropic-ai/claude-code`, `npm install -g @openai/codex`, or see Kimi Code docs |
| [GNU Make](https://www.gnu.org/software/make/) | Build system | Pre-installed on macOS/Linux |
| R | Data analysis, figures | [r-project.org](https://www.r-project.org/) |
| Julia | Computation, simulation | [julialang.org](https://julialang.org/downloads/) |
| Stata | Replication, cleaning, and panel workflows | Vendor installer; ensure `stata-mp`, `stata-se`, or `stata` is on `PATH` |
| MATLAB | Numerical optimization and structural models | MathWorks installer; ensure `matlab` is on `PATH` |
| pdflatex | Manuscript compilation | Included with TeX Live / MacTeX |
| [gh CLI](https://cli.github.com/) | PR workflow | `brew install gh` (macOS) |
| [jq](https://jqlang.github.io/jq/) | Claude Code hooks and `/review-pr` thread parsing | `brew install jq` (macOS) |

Not all tools are needed — install only what your project uses. One of Claude Code, Codex CLI, or Kimi Code CLI is the only hard requirement.

By default, this template does not pin an AI model for any tool. Codex CLI uses the default model from your local Codex CLI setup (for example `~/.codex/config.toml` or an explicit `codex --model ...` override), Claude Code uses the default model configured in your local Claude Code CLI/app session, and Kimi Code CLI uses the default model from `~/.kimi-code/config.toml` or a `kimi -m` override. Prefer user-level configuration or explicit session/CLI overrides to tracked project model and reasoning-effort pins.

---

## Dynamic Numbers in LaTeX

The pipeline keeps computed results out of your `.tex` source by writing `\newcommand` definitions to `output/numbers/` and resolving them at compile time via `TEXINPUTS`.

### How it works

1. **Code generates a `.txt` file** with a `\newcommand`.
   In the standard `code/[task_group]/` layout, task-group scripts reach the
   repo-root `output/` directory via a working-directory-relative
   `output_root`:

   **R:**
   ```r
   output_root = file.path("..", "..", "output")
   writeLines("\\newcommand{\\revenueEstimate}{4.72}",
              file.path(output_root, "numbers", "revenue_estimate.txt"))
   ```

   **Julia:**
   ```julia
   output_root = joinpath("..", "..", "output")
   open(joinpath(output_root, "numbers", "revenue_estimate.txt"), "w") do io
       println(io, "\\newcommand{\\revenueEstimate}{4.72}")
   end
   ```

   **Stata:**
   ```stata
   local output_root "../../output"
   file open fh using "`output_root'/numbers/revenue_estimate.txt", write text replace
   file write fh "\newcommand{\revenueEstimate}{4.72}" _n
   file close fh
   ```

   **MATLAB:**
   ```matlab
   output_root = fullfile("..", "..", "output");
   fid = fopen(fullfile(output_root, "numbers", "revenue_estimate.txt"), "w");
   fprintf(fid, '\\newcommand{\\revenueEstimate}{4.72}\n');
   fclose(fid);
   ```

2. **The manuscript inputs the file** (plain filename — no path prefix needed):
   ```latex
   \input{revenue_estimate.txt}
   A U.S. carbon tariff raises \$\revenueEstimate\ billion in revenue.
   ```

3. **`TEXINPUTS` resolves the path.** The `latex/Makefile` exports:
   ```make
   export TEXINPUTS := .:./latex_extras/:../output/numbers/:../output/tables/:../output/figures/:
   ```
   So `pdflatex` finds `revenue_estimate.txt` in `../output/numbers/` without your `.tex` files needing `../output/` prefixes.

### Adding a new dynamic number

1. Add the write call to your R, Julia, Stata, or MATLAB script
2. Add the `.txt` file as a prerequisite in the relevant `code/` Makefile
3. Add `\input{filename.txt}` in the manuscript preamble (or wherever the macro is first used)
4. Use the macro (`\revenueEstimate`) in prose
5. Run `make` — the code pipeline writes the file, then `pdflatex` picks it up

The same `TEXINPUTS` mechanism resolves figures (`output/figures/`) and tables (`output/tables/`), so `\includegraphics{plot.pdf}` and `\input{reg_table.tex}` also work without path prefixes.

---

## Maintenance: Keeping Claude, Codex, and Kimi in Sync

This repo now uses a three-layer skill architecture:

- **`protocols/skills/`** — canonical shared skill bodies
- **`.claude/skills/`** — Claude wrappers
- **`.agents/skills/`** — Codex wrappers, also scanned natively by Kimi Code CLI

Claude also has a tool-specific execution layer in **`.claude/agents/`** for review-oriented skills. Those agents execute the same shared protocol files rather than owning separate checklists.

Kimi Code CLI needs no wrapper layer of its own: it loads the `AGENTS.md`
hierarchy and scans `.agents/skills/` out of the box. Its only tracked config
is `.kimi-code/config.toml.example`, which mirrors the command permissions for
merging into the user-level `~/.kimi-code/config.toml`.

### What must stay in sync

| Component | Location | Keep in sync? |
|-----------|----------|---------------|
| Command permissions | `.claude/settings.json.example`, `.codex/rules/default.rules`, and `.kimi-code/config.toml.example` | Yes |
| Shared skill bodies | `protocols/skills/*.md` | Yes |
| Skill wrapper names and descriptions | `.claude/skills/*/SKILL.md` and `.agents/skills/*/SKILL.md` | Yes |
| Project conventions | `CLAUDE.md`, `code/CLAUDE.md`, `latex/CLAUDE.md`, and the `AGENTS.md` hierarchy | Yes |

### What intentionally differs

- **Frontmatter format.** Claude wrappers use Claude frontmatter; Codex wrappers use Codex frontmatter.
- **Agent layer.** Claude has `.claude/agents/` for review-oriented execution surfaces. Codex and Kimi do not.
- **Hooks.** Claude supports `.claude/hooks/`; Codex does not, and Kimi hooks are user-level only.
- **Config scope.** Codex reads tracked project config in `.codex/`; Kimi reads permissions, models, and hooks only from user-level config (its project-local `.kimi-code/local.toml` stores workspace directories only), so `.kimi-code/config.toml.example` is a template to merge, not a live config.

### When adding a new skill or convention

1. Add or update the canonical body in `protocols/skills/<name>.md`
2. Update `.claude/skills/<name>/SKILL.md`
3. Update `.agents/skills/<name>/SKILL.md` (Kimi picks this up automatically)
4. If it is a review-oriented Claude agent surface, update the matching file in `.claude/agents/`
5. If the skill needs new commands, update all three permission config files
6. Run `make check-template`

## Template Consistency Checker

Run `make check-template` to validate:

- permission parity between Claude, Codex, and Kimi configs
- shared protocol and wrapper inventory parity
- wrapper references to `protocols/skills/*.md`
- Claude review-agent references to the same canonical protocol files

## Fresh Main Branch

When maintaining this template repo itself, treat ad hoc files under
`quality_reports/` as branch-local working artifacts rather than permanent
template content. Before merging back to `main`, remove task-specific plans,
handoffs, session logs, merge reports, and scratch directories so the default
branch ships clean. Keep only placeholder `.gitkeep` files and intentional
template assets.

---

## Project Structure

```
my-project/
├── CLAUDE.md                    # Root Claude Code instructions
├── AGENTS.md                    # Codex CLI instructions (loaded every session)
├── MEMORY.md                    # Persistent structured [LEARN] entries
├── Makefile                     # Root — delegates to code/ and latex/
├── protocols/
│   └── skills/                  # Canonical shared skill bodies
├── .claude/                     # Claude Code: rules, wrappers, agents, hooks
├── .codex/                      # Codex CLI: config and permission rules
├── .agents/                     # Codex/Kimi: thin skill wrappers
├── .kimi-code/                  # Kimi Code CLI: example permission config
├── code/
│   ├── CLAUDE.md                # Claude instructions for code/
│   ├── AGENTS.md                # Routes work to applicable conventions
│   ├── conventions/             # Shared, language, and Makefile conventions
│   ├── Makefile                 # Delegates to sub-Makefiles
│   ├── [task_group_a]/          # e.g., data cleaning (R or Stata)
│   │   ├── Makefile
│   │   └── *.R, *.jl, *.do, *.ado, or *.m
│   ├── [task_group_b]/          # e.g., simulation (Julia or MATLAB)
│   │   ├── Makefile
│   │   └── *.R, *.jl, *.do, *.ado, or *.m
│   └── [task_group_c]/          # e.g., figures (R or Stata)
│       ├── Makefile
│       └── *.R, *.jl, *.do, *.ado, or *.m
├── latex/
│   ├── CLAUDE.md                # Claude instructions for latex/
│   ├── Makefile                 # pdflatex 3-pass build
│   ├── manuscript.tex           # Main paper
│   ├── slides.tex               # Presentation slides
│   ├── latex_extras/            # packages.tex, custom_commands.tex, etc.
│   └── references/              # references.bib, econ.bst
├── output/                      # Code pipeline outputs (gitignored)
│   ├── figures/                 # Generated figures
│   ├── tables/                  # Generated tables
│   └── numbers/                 # Inline numbers for manuscript
├── quality_reports/             # Plans, handoffs, session logs, merge reports
└── templates/                   # Session, handoff, learning, and quality templates
```

Each `code/[task_group]/Makefile` follows
`code/conventions/makefile.md`: `all` and `clean` targets, order-only
prerequisites for directories, pattern rules for parametric outputs, and
`.PRECIOUS` for expensive intermediates.

---

## License

MIT License. Use freely for research or any academic purpose.

---

## Acknowledgments

This workflow is heavily based on [Pedro H.C. Sant'Anna's Claude Code workflow](https://github.com/pedrohcgs/claude-code-my-workflow).

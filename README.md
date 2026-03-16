# AI-Assisted Academic Research Template (Make + R/Julia/Stata/MATLAB)

> **Work in progress.** This is a summary of how I use AI coding assistants for computational research — running analysis pipelines with Make, writing R, Julia, Stata, and MATLAB scripts, and managing build dependencies. I keep updating these files as I learn new things.

A ready-to-fork starter kit for researchers using [Claude Code](https://code.claude.com/docs/en/overview) or [OpenAI Codex CLI](https://github.com/openai/codex) with **Make + R + Julia + Stata + MATLAB** build systems. You describe what you want; the assistant plans the approach, implements it, builds via Make, runs specialized review skills, fixes issues, and presents results — like a contractor who handles the entire job.

**Both tools are supported.** Claude Code uses `.claude/` + `CLAUDE.md`; Codex CLI uses `.codex/` + `.agents/` + `AGENTS.md`. The same workflow, quality gates, and skills work with either.

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
> I want our collaboration to be structured, precise, and rigorous. Code should be reproducible and build-system driven.
>
> I've set up the Claude Code academic workflow (forked from `irudik/repo-template`). The configuration files are already in this repo. Please read them, understand the workflow, and then **update all configuration files to fit my project** — fill in placeholders in `CLAUDE.md`, set up the `code/` directory structure with sub-Makefiles for my pipeline stages, and propose any customizations specific to my use case.
>
> After that, use the plan-first workflow for all non-trivial tasks. Once I approve a plan, switch to contractor mode — coordinate everything autonomously and only come back to me when there's ambiguity or a decision to make.
>
> Enter plan mode and start by adapting the workflow configuration for this project.

**What this does:** Claude reads all the configuration files, sets up your `code/` directory with sub-Makefiles for each pipeline stage, fills in your project details, then enters contractor mode — planning, implementing, reviewing, and verifying autonomously.

### 3. Configure Hooks (Optional)

Hooks are configured per-user in `.claude/settings.json` (gitignored by default). To enable the bundled hooks, create the file with the format below. The `hooks` key uses nested arrays with optional `matcher` and `timeout` fields. `$CLAUDE_PROJECT_DIR` resolves to the project root at runtime.

```bash
cat > .claude/settings.json << 'EOF'
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/log-reminder.py",
            "timeout": 10
          }
        ]
      }
    ],
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

**What this does:** Codex reads `AGENTS.md` (root + `code/AGENTS.md` + `latex/AGENTS.md`), understands the full workflow, and configures the project.

### 3. Configuration

Codex project configuration lives in:

- **`AGENTS.md`** (root) — project instructions and workflow rules (loaded every session)
- **`code/AGENTS.md`** — R, Julia, Stata, MATLAB, and Makefile conventions (loaded when working in `code/`)
- **`latex/AGENTS.md`** — LaTeX conventions (loaded when working in `latex/`)
- **`.codex/config.toml`** — model, sandbox, and approval settings
- **`.codex/rules/default.rules`** — command execution permissions (Starlark format)
- **`.agents/skills/*/SKILL.md`** — reusable skill definitions

### Codex vs Claude Code: Key Differences

| Aspect | Claude Code | Codex CLI |
|--------|-------------|-----------|
| Instructions file | `CLAUDE.md` | `AGENTS.md` (hierarchical) |
| Settings | `.claude/settings.json` (JSON) | `.codex/config.toml` (TOML) |
| Permission rules | Glob patterns in settings.json | `.codex/rules/default.rules` (Starlark) |
| Behavioral rules | `.claude/rules/*.md` (separate files) | Inlined into `AGENTS.md` hierarchy |
| Agent definitions | `.claude/agents/*.md` | Inlined into review skills |
| Skills | `.claude/skills/*/SKILL.md` | `.agents/skills/*/SKILL.md` |
| Hooks | `.claude/hooks/*` | Not supported (use git hooks) |

### Known Limitations (Codex)

Codex CLI does not support hooks, so these Claude Code features have no direct equivalent:
- **File protection** (`.claude/hooks/protect-files.sh`) — be careful editing `references.bib` and `settings.json`
- **Session log reminders** (`.claude/hooks/log-reminder.py`) — manually update session logs
- **Context snapshot before compaction** (`.claude/hooks/pre-compact.sh`) — save context to plans/ manually
- **Desktop notifications** (`.claude/hooks/notify.sh`) — not available

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

### Contractor Mode

You describe a task. Claude:
1. **Plans** the approach (enter plan mode, save to disk)
2. **Implements** the code
3. **Verifies** via `make -n` then `make` — builds stale targets (including `make -C latex` for the manuscript), checks exit codes
4. **Reviews** with specialized agents (r-reviewer, julia-reviewer, stata-reviewer, matlab-reviewer, verifier)
5. **Fixes** issues found by reviewers
6. **Scores** against quality gates

If the score meets threshold, Claude presents a summary. Say "just do it" and it auto-commits too.

### PR Review (`/review-pr`)

When reviewers leave comments on a pull request, `/review-pr <PR#>` automates the triage-fix-reply loop:

1. **Fetches** all unresolved review threads via GitHub's GraphQL API
2. **Classifies** each thread by confidence:
   - **HIGH** — clear code fix (typo, bug, missing import). Implements, commits, replies with the commit hash, and resolves the thread.
   - **MEDIUM** — ambiguous but likely intent. Implements and stages changes but does *not* commit. Presents the interpretation for your approval.
   - **LOW** — design question or unclear fix. Reports the thread with a suggested approach. No code changes.
3. **Groups** fixes by file so each commit is atomic
4. **Runs the orchestrator mini-loop** on each group (implement, verify via Make, review, score)
5. **Pushes** and prints a summary table of what was addressed, what needs approval, and what needs your input

Outdated threads (code has moved since the comment) are reported but never touched.

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
| `verifier` | End-to-end build verification, orphaned script detection |

The verifier runs an **orphaned script check**: every `.R`, `.jl`, `.do`, `.ado`, and `.m` file under `code/` must appear as a prerequisite in some Makefile. Scripts with no Makefile target get flagged.

For manuscript or slide tasks, the orchestrator can also run **opt-in review passes** after the review-fix loop completes:
- `domain-reviewer` for substantive identification and citation checks
- `proofreader` for grammar, overflow, and consistency checks

These run once on the final state and produce reports only — fixes require user review.

### Quality Gates

Every file gets a score (0–100). Scores below threshold block the action:
- **80** — commit threshold
- **90** — PR threshold
- **95** — excellence (aspirational)

Rubrics cover R scripts, Julia scripts, Stata scripts, MATLAB scripts, Makefiles, and LaTeX manuscripts. See `.claude/rules/quality-gates.md` for the full deduction table.

---

## What's Included

<details>
<summary><strong>Agents, skills, and rules</strong> (click to expand)</summary>

### Agents (`.claude/agents/`)

| Agent | What It Does |
|-------|-------------|
| `r-reviewer` | R code quality, reproducibility, and domain correctness |
| `julia-reviewer` | Julia code quality, type stability, and performance |
| `stata-reviewer` | Stata code quality, data integrity, and research workflow safety |
| `matlab-reviewer` | MATLAB code quality, solver configuration, derivative correctness |
| `domain-reviewer` | Substantive review for manuscripts, slides, and teaching materials |
| `proofreader` | Academic proofreading for manuscripts, slides, and notes |
| `tex-reviewer` | LaTeX manuscript quality, hardcoded numbers, citation consistency |
| `makefile-reviewer` | Makefile conventions, dependency correctness, script coverage |
| `verifier` | End-to-end build verification with orphaned script check |

### Key Skills (`.claude/skills/`)

| Skill | What It Does |
|-------|-------------|
| `/commit` | Stage, commit, PR, merge (with `make -n` staleness warning) |
| `/data-analysis` | End-to-end R analysis workflow |
| `/refactor [file-or-dir]` | Verify-refactor-verify loop for safe style changes |
| `/verify-outputs [script]` | Checksum outputs, compare to reference |
| `/compare-branches [b1] [b2]` | Cross-branch output comparison via worktrees |
| `/resume` | Recover context after compression/new session |
| `/setup-makefile [dir]` | Generate Makefile from directory contents |
| `/review-pr [PR#]` | Address PR review comments, commit fixes, resolve threads |
| `/review-r [file]` | R code quality review via r-reviewer agent |
| `/review-julia [file]` | Julia code quality review via julia-reviewer agent |
| `/review-stata [file]` | Stata code quality review via stata-reviewer agent |
| `/review-matlab [file]` | MATLAB code quality review via matlab-reviewer agent |
| `/review-tex [file]` | LaTeX manuscript review via tex-reviewer agent |
| `/review-makefile [file]` | Makefile conventions review via makefile-reviewer agent |
| `/review-domain [file]` | Opt-in substantive domain review via domain-reviewer agent |
| `/proofread [file]` | Opt-in proofreading review via proofreader agent |
| `/review-comments [path]` | Clean up comments, docstrings, dead code |
| `/matlab-optim-derivatives` | Audit MATLAB optimization derivatives |

### Key Rules (`.claude/rules/`)

| Rule | What It Enforces |
|------|-----------------|
| `makefile-conventions` | Standard Make patterns: `.PHONY`, order-only prereqs, pattern rules, joint production |
| `r-code-conventions` | R coding standards, Makefile-based directory creation |
| `julia-code-conventions` | Julia coding standards, Makefile-based directory creation |
| `stata-code-conventions` | Stata coding standards, merge safety, and batch workflow discipline |
| `matlab-code-conventions` | MATLAB coding standards, solver configuration, derivative correctness |
| `refactoring-protocol` | Verify-refactor-verify loop, prohibited/approved transformations |
| `solver-debugging-protocol` | Systematic diagnostic checklist for numerical solver failures |
| `verification-formats` | Which output formats are checksum-stable and how to compare each |
| `quality-gates` | 80/90/95 scoring for R, Julia, Stata, MATLAB, Makefiles, and LaTeX |
| `verification-protocol` | Make-first verification, then file-specific checks |
| `orchestrator-protocol` | Contractor mode: implement, verify via Make, review, fix, score |
| `orchestrator-research` | Simplified loop for R/Julia/Stata/MATLAB scripts |
| `plan-first-workflow` | Plan mode for non-trivial tasks |
| `session-logging` | Proactive session logging: post-plan, incremental, end-of-session |
| `bash-conventions` | One command per Bash call for permission glob matching |
| `replication-protocol` | Reproducibility standards for data, code, and output |

### Codex CLI Configuration

| Component | Location | Purpose |
|-----------|----------|---------|
| `AGENTS.md` (root) | Project root | Core instructions + workflow rules |
| `code/AGENTS.md` | `code/` | R, Julia, Stata, MATLAB, and Makefile conventions |
| `latex/AGENTS.md` | `latex/` | LaTeX conventions |
| `.codex/config.toml` | `.codex/` | Optional Codex project overrides for sandbox, approval, and model behavior |
| `.codex/rules/default.rules` | `.codex/rules/` | Command execution permissions (Starlark) |
| `.agents/skills/*/SKILL.md` | `.agents/skills/` | 17 reusable skills (same as Claude) |

</details>

---

## Prerequisites

| Tool | Required For | Install |
|------|-------------|---------|
| [Claude Code](https://code.claude.com/docs/en/overview) or [Codex CLI](https://github.com/openai/codex) | AI assistant | `npm install -g @anthropic-ai/claude-code` or `npm install -g @openai/codex` |
| [GNU Make](https://www.gnu.org/software/make/) | Build system | Pre-installed on macOS/Linux |
| R | Data analysis, figures | [r-project.org](https://www.r-project.org/) |
| Julia | Computation, simulation | [julialang.org](https://julialang.org/downloads/) |
| Stata | Replication, cleaning, and panel workflows | Vendor installer; ensure `stata-mp`, `stata-se`, or `stata` is on `PATH` |
| MATLAB | Numerical optimization and structural models | MathWorks installer; ensure `matlab` is on `PATH` |
| pdflatex | Manuscript compilation | Included with TeX Live / MacTeX |
| [gh CLI](https://cli.github.com/) | PR workflow | `brew install gh` (macOS) |
| [jq](https://jqlang.github.io/jq/) | Claude Code hooks (3 of 4 use it) | `brew install jq` (macOS) |

Not all tools are needed — install only what your project uses. Either Claude Code or Codex CLI is the only hard requirement.

By default, this template does not pin an AI model for either tool. Codex CLI uses the default model from your local Codex CLI setup (for example `~/.codex/config.toml` or an explicit `codex --model ...` override), and Claude Code uses the default model configured in your local Claude Code CLI/app session. If you want a repo-specific model, add that pin yourself.

---

## Dynamic Numbers in LaTeX

The pipeline keeps computed results out of your `.tex` source by writing `\newcommand` definitions to `output/numbers/` and resolving them at compile time via `TEXINPUTS`.

### How it works

1. **Code generates a `.txt` file** with a `\newcommand`:

   **R:**
   ```r
   writeLines("\\newcommand{\\revenueEstimate}{4.72}",
              file.path("output", "numbers", "revenue_estimate.txt"))
   ```

   **Julia:**
   ```julia
   open(joinpath("output", "numbers", "revenue_estimate.txt"), "w") do io
       println(io, "\\newcommand{\\revenueEstimate}{4.72}")
   end
   ```

   **Stata:**
   ```stata
   file open fh using "output/numbers/revenue_estimate.txt", write text replace
   file write fh "\newcommand{\revenueEstimate}{4.72}" _n
   file close fh
   ```

   **MATLAB:**
   ```matlab
   fid = fopen(fullfile("output", "numbers", "revenue_estimate.txt"), "w");
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

## Adapting for Your Field

1. **Add field-specific pitfalls** to `.claude/rules/r-code-conventions.md`, `.claude/rules/julia-code-conventions.md`, `.claude/rules/stata-code-conventions.md`, and `.claude/rules/matlab-code-conventions.md`
2. **Adjust tolerance thresholds** in `.claude/rules/quality-gates.md` for your domain's precision requirements
3. **Set up the `code/` directory** with sub-Makefiles matching your pipeline stages

---

## Project Structure

```
my-project/
├── CLAUDE.md                    # Claude Code instructions (loaded every session)
├── AGENTS.md                    # Codex CLI instructions (loaded every session)
├── Makefile                     # Root — delegates to code/ and latex/
├── .claude/                     # Claude Code: rules, skills, agents, hooks
├── .codex/                      # Codex CLI: config and permission rules
├── .agents/                     # Codex CLI: skill definitions
├── code/
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
│   ├── Makefile                 # pdflatex 3-pass build
│   ├── manuscript.tex           # Main paper
│   ├── slides.tex               # Presentation slides
│   ├── latex_extras/            # packages.tex, custom_commands.tex, etc.
│   └── references/              # references.bib, econ.bst
├── output/                      # Code pipeline outputs (gitignored)
│   ├── figures/                 # Generated figures
│   ├── tables/                  # Generated tables
│   └── numbers/                 # Inline numbers for manuscript
├── quality_reports/             # Plans, session logs, merge reports
└── templates/                   # Session log, quality report templates
```

Each `code/[task_group]/Makefile` follows the conventions in `.claude/rules/makefile-conventions.md`: `all` and `clean` targets, order-only prerequisites for directories, pattern rules for parametric outputs, and `.PRECIOUS` for expensive intermediates.

---

## License

MIT License. Use freely for research or any academic purpose.

---

## Acknowledgments

This workflow is heavily based on [Pedro H.C. Sant'Anna's Claude Code workflow](https://github.com/pedrohcgs/claude-code-my-workflow).

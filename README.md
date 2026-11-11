# AI-Assisted Academic Research Template

A starting point for economics research with Claude Code, Codex, or
Antigravity, using Make and R, Julia, Stata, or MATLAB. The assistant
applies the risk-based workflow in [AGENTS.md](AGENTS.md): it completes the
requested work, checks the result, and adds planning or independent review
when the consequences warrant it.
This template evolves with research practice and the tools it supports.

## Set up a project

Fork this repository on GitHub, then clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/repo-template.git my-project
cd my-project
```

Install an assistant and the tools your project uses:

| Tool | Purpose and setup |
|------|-------------------|
| Claude Code | Follow the [installation guide](https://code.claude.com/docs/en/overview). |
| Codex | Follow the [Codex CLI guide](https://learn.chatgpt.com/docs/cli). |
| Antigravity | Install the `agy` CLI for your Google account. |
| GNU Make | Run the analysis and manuscript builds; install if `make` is unavailable. |
| R, Julia, Stata, MATLAB | Install only the languages used by your analysis; put their command-line executables on `PATH`. |
| TeX Live or MacTeX | Provides `pdflatex` and `bibtex` for the manuscript and slides. |
| Python 3.11 or later | Runs the template checker and update tools. |
| GitHub CLI (`gh`) | Creates and manages pull requests; authenticate with `gh auth login`. |
| `jq` | Used by the Claude hooks and PR review commands. |

Start your assistant from the project directory using one of the quick starts
below, then paste this prompt with your project details:

> I am starting **[PROJECT NAME]** at **[INSTITUTION]**. **[Describe the
> research question, data, and analysis stages in two or three sentences.]**
> Read this repository's instructions and adapt the template to my project.
> Fill in the root `AGENTS.md` placeholders, set up numbered analysis scripts
> and a Makefile for each task group under `code/`, and adapt the manuscript
> setup. Use **[R/Julia/Stata/MATLAB]**. Finish the setup and relevant checks,
> and report any decisions that require my input. Leave changes uncommitted.

After setup, replace this README with your project's purpose, data-access
instructions, required packages, and reproduction commands. Set
`readme_documents_framework = false` in `tools/template_check.toml` so the
checker no longer requires framework examples in your project README.

### Quick Start: Claude Code

```bash
claude
```

The Claude Code panel in VS Code also works. Root `CLAUDE.md` imports the
shared instructions with `@AGENTS.md`; `code/CLAUDE.md` and `latex/CLAUDE.md`
import the `AGENTS.md` beside them.

To enable the supplied permissions and optional hooks, review
[.claude/settings.json.example](.claude/settings.json.example) and copy it to
`.claude/settings.json` if you do not already have that file. If you do,
merge the desired entries. The local file is gitignored. The hooks provide
notifications and protect `settings.json`; `references.bib` is editable.

To have Claude plan and Codex execute, install the Codex plugin for Claude
and explicitly request “hand this to Codex” or mark plan steps `[codex]`.
[protocols/codex-handoff.md](protocols/codex-handoff.md) defines the handoff
and each agent's responsibilities.

### Quick Start: Codex

```bash
codex
```

Codex uses `AGENTS.md`, the applicable nested instructions, and the skills
in `.agents/skills/`. The template's `.codex/config.toml` leaves model and
reasoning effort to your own settings. Project command permissions live in
`.codex/rules/default.rules`.

As verified against official OpenAI documentation on **November 10, 2026**:

- Codex supports subagents and custom agent definitions in
  `.codex/agents/*.toml` or `~/.codex/agents/*.toml`. Delegation follows a
  direct request or applicable project or skill instructions. See
  [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).
- Codex supports lifecycle hooks, configured in `.codex/hooks.json` or
  `[hooks]` in `config.toml`, including user-level equivalents. Non-managed
  hooks require trust review; `/hooks` manages them. See
  [Hooks](https://learn.chatgpt.com/docs/hooks).

This repository supplies shared review skills for Codex, but no custom Codex
agent definitions or hook configuration. The Claude hook files are not
installed as Codex hooks by this template.

### Quick Start: Antigravity

Antigravity (`agy`) replaces Gemini CLI, which Google retired for individual
accounts. Start it from the project directory:

```bash
agy --settings .agents/antigravity-settings.example.json
```

Antigravity finds `AGENTS.md` by walking up from the working directory and
scans `.agents/skills/` itself. It reads no project-level settings file.
Pass the example above for one session, or merge its entries into
`~/.gemini/antigravity-cli/settings.json`. Permissions use entries such as
`command(git)` under `permissions.allow`. Antigravity does not read the
`.gemini/settings.json` that Gemini CLI used.

Choose model and effort through the model name, for example:

```bash
agy --model gemini-4-carbon-high
```

## Where to find the rules

| File or directory | Contents |
|-------------------|----------|
| [AGENTS.md](AGENTS.md) | Shared rules for Claude Code, Codex, and Antigravity. |
| [code/AGENTS.md](code/AGENTS.md) | Selects shared and language-specific conventions from `protocols/conventions/`. |
| [latex/AGENTS.md](latex/AGENTS.md) | Manuscript builds, generated numbers, and TeX prose. |
| [protocols/writing.md](protocols/writing.md) | Writing rules; `Reports and Updates` governs replies and reports. |
| [protocols/solver-debugging.md](protocols/solver-debugging.md) | Numerical failure diagnosis. |
| [protocols/skills/](protocols/skills/) | Shared procedures for all 20 skills. |
| [MEMORY.md](MEMORY.md) | Project lessons with Rule, Reason, Evidence, Date, and Review by fields. |
| [templates/](templates/) | Layouts for records kept under `quality_reports/` when needed. |

`Risk-Based Workflow` in root `AGENTS.md` contains the single ask rule and
the steps that need no further approval. Agents finish authorized work without
pausing for approval of each step. `Defects That Block a Commit or Merge`
replaces numeric scoring; other findings are advisory.

Keep instruction files small. Antigravity cuts an instruction file at
24,000 bytes. Codex's combined `AGENTS.md` allowance is 32,768 bytes, including
global and applicable nested instructions. `make check-template` fails when
root `AGENTS.md` exceeds 20,000 bytes and also checks the repository's nested
instruction totals. Keep personal instructions within the remaining allowance.
Root `CLAUDE.md` should stay under 200 lines.

### Skills and reviewers

Use a skill by name in your request; Claude also offers slash commands.
Read the linked procedure for its scope:

| Task | Skills |
|------|--------|
| Build analysis | `/data-analysis`, `/setup-makefile` |
| Check outputs or reorganize code | `/verify-outputs`, `/compare-branches`, `/refactor` |
| Review research code | `/review-r`, `/review-julia`, `/review-stata`, `/review-matlab`, `/matlab-optim-derivatives` |
| Review dependencies or documentation | `/review-makefile`, `/review-comments`, `/review-tex` |
| Requested academic review | `/review-domain`, `/proofread` |
| Diagnose or recover context | `/trace`, `/resume-custom`, `/learn` |
| Requested GitHub work | `/commit`, `/review-pr` |

`.claude/skills/` and `.agents/skills/` are thin wrappers around those shared
procedures. The latter serves both Codex and Antigravity. Claude reviewer
agents in `.claude/agents/` return findings to the main agent and do not save
report files.

Six mechanical Claude wrappers set `effort: medium`: `commit`,
`compare-branches`, `learn`, `resume-custom`, `setup-makefile`, and
`verify-outputs`. Codex takes effort from the user's settings; Antigravity
uses the selected model name. The template does not pin a project model.

## Build layout and paths

The root Makefile builds `code/` before `latex/`. Each analysis task group
has its own Makefile; outputs go to `output/figures/`, `output/tables/`, and
`output/numbers/`. The manuscript is `latex/manuscript.tex`, with slides in
`latex/slides.tex` and bibliography files in `latex/references/`.

Run these Make commands from the project root.

```bash
make                              # Analysis, then manuscript and slides
make -n                           # Show what would be built
make -C code                      # Analysis only
make -C code/estimation all        # One task group, after creating it
make -C latex                     # Manuscript and slides
make check-template               # Instruction checks and tool tests
```

With `make -C path`, targets, prerequisites, and scripts use paths relative
to `path`. Thus a script in `code/estimation/` uses `../../output` to reach
the project output directory. Makefiles create output directories; scripts
use working-directory-relative paths. See
[the Make conventions](protocols/conventions/makefile.md) for dependency rules.

### Generated numbers: a minimal example

Have your analysis write a value-only macro to `output/numbers/`. These
examples use an illustrative value; replace it with the computed estimate.
Run them from `code/[task_group]/` after Make creates the output directory.

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

The manuscript loads the definition and uses the macro:

```latex
\input{revenue_estimate.txt}
A U.S. carbon tariff raises \$\revenueEstimate\ billion in revenue.
```

Declare the generated `.txt` file as a target of its producing script in
the task-group Makefile, and as a prerequisite of the consuming PDF in
`latex/Makefile`. Its `TEXINPUTS` setting locates numbers, tables, and figures
without path prefixes in the TeX source.

When an agent-driven build can rewrite `output/numbers/`, follow the
before-and-after comparison and prose review in
[latex/AGENTS.md](latex/AGENTS.md#reviewing-updated-values).

## Maintaining the template and updating projects

When adding a skill, write its shared procedure under `protocols/skills/`,
add both wrappers, and update the Claude reviewer definition if needed.
Keep command permissions aligned across `.claude/settings.json.example`,
`.codex/rules/default.rules`, and the Antigravity settings example.
Run `make check-template` after instruction changes. It checks required
references, retired text, size limits, permissions, and skill inventories,
and runs the tests under `tools/tests/`.

Project repositories declare optional parts in `tools/template_check.toml`:
set `has_latex = false` for an external manuscript, `has_code = false` if
there is no code directory, and `readme_documents_framework = false` for a
project-specific README. Omitted declarations default to the full template.

To carry template updates into an existing project, run these from the
template checkout; both default to a dry run:

```bash
python3 tools/sync_template.py --repo ../my-project
python3 tools/merge_template_sections.py --repo ../my-project
```

Inspect the proposed changes, then add `--apply` to apply them. The sync tool
copies shared files and handles retired files. The section merge tool updates
`Core Principles`, `Where Things Are`, `Risk-Based Workflow`,
`Defects That Block a Commit or Merge`, `Changed Numbers in the Manuscript`,
and `Records` in `AGENTS.md`, plus the opening prose of `Commands`. In
`CLAUDE.md` it updates `Shared Instructions` and `Claude Code Notes`. It
removes retired sections while preserving project material outside its owned
sections and the project's manuscript location.

Record deliberate project adaptations in the target's
`tools/template_departures.toml`, for example:

```toml
[[departure]]
path = "protocols/conventions/*.md"
reason = "Adapted to this project's language conventions."
```

The update tools honor matching departures and report their reasons. Use
file paths or patterns; unmatched patterns produce a warning. The template
itself has no departures file. Rules for keeping task-specific records out
of the template's `main` branch are in `AGENTS.md` under `Records`.

## License and acknowledgments

MIT License. This workflow draws on
[Pedro H.C. Sant'Anna's Claude Code workflow](https://github.com/pedrohcgs/claude-code-my-workflow).

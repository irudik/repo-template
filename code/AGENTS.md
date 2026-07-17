# Code Convention Router

These instructions apply to work under `code/`.

Always read [conventions/shared.md](conventions/shared.md). Then read only the
convention files needed for the files in scope:

| Files in scope | Additional convention |
|----------------|-----------------------|
| `.R`, `.Rmd`, `.qmd` analysis files | [conventions/r.md](conventions/r.md) |
| `.jl` | [conventions/julia.md](conventions/julia.md) |
| `.do`, `.ado` | [conventions/stata.md](conventions/stata.md) |
| `.m` | [conventions/matlab.md](conventions/matlab.md) |
| `Makefile`, `*.mk` | [conventions/makefile.md](conventions/makefile.md) |

When a task spans more than one language, read each applicable file. When a
task changes a Makefile and a script, read the Makefile convention and the
script's language convention.

The files under `code/conventions/` are the shared sources of truth for both
Claude and Codex. Do not duplicate their full contents in tool-specific rule
files.

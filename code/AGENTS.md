# Code Convention Router

These instructions apply to work under `code/`.

Always read [../protocols/conventions/shared.md](../protocols/conventions/shared.md).
Then read only the convention files needed for the files in scope:

| Files in scope | Additional convention |
|----------------|-----------------------|
| `.R`, `.Rmd`, `.qmd` analysis files | [../protocols/conventions/r.md](../protocols/conventions/r.md) |
| `.jl` | [../protocols/conventions/julia.md](../protocols/conventions/julia.md) |
| `.do`, `.ado` | [../protocols/conventions/stata.md](../protocols/conventions/stata.md) |
| `.m` | [../protocols/conventions/matlab.md](../protocols/conventions/matlab.md) |
| `Makefile`, `*.mk` | [../protocols/conventions/makefile.md](../protocols/conventions/makefile.md) |

When a task spans more than one language, read each applicable file. When a
task changes a Makefile and a script, read the Makefile convention and the
script's language convention.

The files under `protocols/conventions/` are the shared sources of truth for
both Claude and Codex. Do not duplicate their full contents in tool-specific
rule files.

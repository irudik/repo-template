# R Conventions

Read alongside `protocols/conventions/shared.md`.

## Setup and Estimation

- Load packages at the top with `library()` rather than `require()` in analysis scripts, so missing packages stop the run immediately instead of failing later; use `requireNamespace()` only when checking for an optional package.
- In stochastic scripts, call `set.seed(YYYYMMDD)` once at the top.
- Match estimator implementations, weights, fixed effects, and standard errors to `latex/manuscript.tex`.
- Return named lists or tibbles when a function returns multiple estimates or objects.
- Let the Makefile create output directories.

## Output Paths

Task-group scripts run from the script working directory (usually `code/[task_group]/`). Define `output_root` once and write into the repository-root `output/` subdirectories:

```r
output_root = file.path("..", "..", "output")

ggsave(file.path(output_root, "figures", "my_plot.pdf"), width = 8, height = 8, bg = "transparent")
saveRDS(result, file.path(output_root, "tables", "my_results.rds"))
writeLines("\\newcommand{\\myEstimate}{2.31}",
           file.path(output_root, "numbers", "my_estimate.txt"))
```

Save with `saveRDS()` what later steps, slide rendering, or reproduction need, rather than every intermediate object.

## Visual Identity (Optional)

Use this palette and these themes when the project wants uniform figure
styling. The fonts must already be installed. Do not download them in a
script the build runs: `sysfonts::font_add_google()` fails without a network
connection.

```r
plot_blue = "#4575b4"
plot_mid = "#ffffdf"
plot_red = "#d73027"
plot_purple = "#c51b7d"
plot_green = "#3a7813"

# Regular plots
main_theme =
  theme_classic() +
  theme(
    legend.position = "none",
    title = element_text(size = 24),
    text = element_text(family = font_choice),
    axis.text = element_text(size = 30),
    axis.title = element_text(size = 30),
    panel.grid = element_blank(),
    axis.line = element_line(colour = "black"),
    axis.ticks = element_line(colour = "black"),
    plot.background = element_rect(fill = "#ffffff")
  )

# Maps
map_theme =
  theme_void() +
  theme(
    legend.position = "bottom",
    legend.key.height = unit(.35, "cm"),
    legend.key.width = unit(.6, "cm"),
    legend.text = element_text(size = 8),
    text = element_text(family = font_choice)
  )
```

For the slides template, save figures with `width = 8, height = 8` and maps
with `width = 8, height = 4`, and pass `bg = "transparent"` to `ggsave()` so
figures do not show white boxes on slides.

# Data Figures

Use this only for precise, reproducible plots from CSV, JSON, logs, TensorBoard exports, or explicitly supplied numeric result tables.

## Boundary

- Use Python/Matplotlib/Seaborn for exact experiment data figures.
- Do not use a generative image model for numeric plots, axes, data points, error bars, p-values, trends, or metric labels.
- If the task is a system overview, architecture, pipeline, threat model, workflow, or method intuition with no exact plotted values, use `conceptual-figures.md`.

## Workflow

1. Identify the paper claim the figure supports.
2. Locate source data. If no source data exists, stop at a figure spec or ask for the data.
3. Profile raw tabular data with `scripts/profile_data.py` when available; use `data-profiling.md` to interpret the report.
4. Choose the plot family from the claim and data shape using `chart-selection.md`, `visual-pitfalls.md`, and `plot-patterns.md`.
5. Write or update `figure_spec.yaml` next to outputs; use `figure-contract.md`.
6. Write a deterministic plotting script near the paper or experiment output.
7. Use `scripts/paperfig_style.py` for house plot helpers when it fits the plot.
8. Use a 3x source canvas with explicit source fonts near or above 24pt by
   default; scale strokes and markers consistently and record smaller choices.
9. Export `figure.pdf`; also export `figure.svg` or `figure.png` when useful.
10. Render or place the result at final paper width, complete human visual QA,
    record artifact evidence, and update the caption.

## Source Data Rule

Prefer source-data-driven plotting. Do not hand-copy numbers from prose when CSV/JSON artifacts exist. If the user gives only prose and asks for a plot, ask for data or produce a placeholder spec.

Do not invent:

- exact values
- baselines
- p-values
- confidence intervals
- number of runs
- visual trends
- sample sizes

## Plot Selection

Use `chart-selection.md` as the main advisor when raw data is available.

- Trend over epochs, time, dose, or input size: line plot with uncertainty band.
- Method comparison with few metrics: grouped bar, preferably with raw points or error bars when repeated runs exist.
- Many metrics or exact values: table, not figure.
- Distribution across runs: box plot, violin plot, stripplot, CDF, or histogram.
- Small-n group comparison: show individual points; avoid mean-only bars.
- Tradeoff: scatter or Pareto frontier.
- Matrix relationship: heatmap.
- Attack/defense or privacy/utility boundary: grouped bar, scatter, or heatmap depending on the evidence.

Actively warn before producing a chart that hides distribution, sample size, uncertainty, or comparison boundaries. If the user insists, proceed but show raw points or limitations where possible.

## Implementation Rules

- Do not use in-figure titles. Captions carry titles and interpretation.
- Preserve the intended final aspect ratio on a 3x source canvas. Use one
  controlled placement scale to the target paper width.
- Keep axis labels short and readable.
- Use semantic color roles: proposed method, baseline, boundary or negative result, neutral reference.
- Use hatching, marker shape, or line style when the distinction must survive grayscale print.
- Use a colorblind-safe palette for categorical distinctions. Do not encode the key comparison with color alone.
- Prefer every explicit source text size at or above 24pt. At final placement,
  revise labels or layout first; if smaller source text is retained, record why
  the rendered result remains comfortably readable.
- Include error bars or confidence intervals when the result is averaged over runs and the data supports it.
- Explain error type in the caption: SD, SEM, 95% CI, IQR, or other.
- Keep interpretation out of the plot canvas.
- Prefer vector output for paper inclusion.
- Use one semantic figure file per figure. Build multi-panel figures intentionally, not by dumping unrelated plots into one canvas.

## Visual QA

For venue-ready plots, render a PNG preview before final export and inspect it:

1. Run `layout_tools.finalize_figure(fig)` when appropriate.
2. Render preview with `visual_qa.render_preview`.
3. Run `visual_qa.audit_layout` for glyph, clipping, and overlap issues.
4. Visually inspect the preview for legend occlusion, unreadable labels, grayscale failure, panel misalignment, and cropped data.
5. Fix and rerender until the issues are resolved or explicitly accepted by the user.

Use `visual-qa.md`, `journal-specs.md`, and `publication-checklist.md` for detailed checks.

## Output Layout

Recommended folder:

```text
figures/{slug}/
├── figure_spec.yaml
├── plot_{slug}.py
├── source_data.csv
├── figure.pdf
├── figure.svg
├── figure.png
└── caption.md
```

If the repository has an established figure layout, follow it.

## Placeholder And Simulated Data Boundaries

- If values are simulated, placeholder, or not from a completed experiment, make the evidence boundary clear in paper prose or surrounding artifact notes as appropriate.
- Do not put internal validation labels, local paths, script names, or renderer details in the manuscript caption.
- Do not present placeholder values as real experimental results.

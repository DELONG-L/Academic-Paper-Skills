# Data Figures

Use this for precise, reproducible plots from data artifacts or explicit numerical values supplied in prose or tables.

## Boundary

- Prefer the supplied Python plotting helpers when useful. Other reproducible numeric tools, including R, Julia and static Plotly exports, are valid when they preserve the data and meet output requirements.
- Do not use a generative image model for numeric plots, axes, data points, error bars, p-values, trends, or metric labels.
- If the task is a system overview, architecture, pipeline, threat model, workflow, or method intuition with no exact plotted values, use `conceptual-figures.md`.

## Experimental Figure Placement and Panel Minimums

Apply this skill's default layout requirement to experimental/data figures in
paper placement, independently of the conceptual-figure workflow:

| Placement | Minimum meaningful plot panels in each row |
|---|---|
| Single column | 2 |
| Spanning both columns of a two-column paper | 4 |

These are minimums, not exact counts. Count distinct, meaningful plot panels
arranged horizontally in the final manuscript layout, not separate files,
curves, methods, bars, legends, colorbars, insets, or decorative boxes. Multiple
series within one axes do not satisfy a multi-panel minimum. A composite exported
as one PDF still counts by its constituent plot panels. Apply the minimum to
every row, including the last row; do not average panel counts across rows.

Plan the panel grid before rendering. Record target column span, actual width,
height budget, and panels per row in existing figure notes. For a one-column
paper, do not infer a two-column-spanning placement merely from a wide canvas;
use its actual full text-column width and state the placement interpretation.

Group related datasets, metrics, conditions, or scientifically meaningful views
of supplied data under a coherent question. Shared legends/axes can save space
when their scales and semantics genuinely agree. Four horizontally placed panels
still require readable axes, labels, uncertainty and distinctions at final width.
The minimum count is necessary for this layout requirement, not proof of quality.

Do not manufacture data, launch additional experiments, duplicate views, split a
single comparison artificially, add empty panels, or combine unrelated results
just to reach the count. If the supported panels cannot meet the minimum and stay
readable, first reorganize related available evidence, consider a smaller column
span, or use a table when it serves the same scientific purpose. If no faithful
layout works, report the precise conflict and leave that placement requirement
unmet; do not silently waive the count or claim full compliance. Request a user
exception only if needed to finish a concrete artifact. Explicit later user
instructions and binding venue constraints take precedence; disclose deviations.

## Workflow

1. Identify the paper claim the figure supports.
2. Locate source data. If no source data exists, stop at a figure spec or ask for the data.
3. Profile raw tabular data with `scripts/profile_data.py` when available; use `data-profiling.md` to interpret the report.
4. Choose the plot family from the claim and data shape using `chart-selection.md`, `visual-pitfalls.md`, and `plot-patterns.md`.
5. Plan column span and the per-row panel grid under the experimental placement rule above. Reuse existing source/encoding notes; use `figure-contract.md` for a complex figure when a spec helps.
6. Use or write a reproducible plotting script, notebook or shared-pipeline entrypoint; record its inputs and execution command.
7. Use `scripts/paperfig_style.py` for reusable plot helpers when it fits the plot.
8. Derive canvas dimensions and text sizes from final placement; scale strokes and markers consistently if working on an enlarged source canvas.
9. Prefer PDF/SVG for precise plots; export the format required by the actual delivery and inspect its final-size quality.
10. Export and inspect the actual artifact at final paper width, record the
    actual evaluator and relevant evidence, and update the caption.

## Source Data Rule

Prefer original data artifacts when available. Explicit numerical values supplied in prose or a table are usable sources: transcribe them into a small plot input, retain units and provenance, and verify the transcription. Ask only when the requested plot needs information that was not supplied.

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

- Trend over epochs, time, dose, or input size: line plot; add uncertainty only when the design and supplied data support it.
- Method comparison with few metrics: grouped bar, preferably with raw points or error bars when repeated runs exist.
- Many metrics or exact values: table, not figure.
- Distribution across runs: box plot, violin plot, stripplot, CDF, or histogram.
- Small-n group comparison: show individual points; avoid mean-only bars.
- Tradeoff: scatter or Pareto frontier.
- Matrix relationship: heatmap.
- Attack/defense or privacy/utility boundary: grouped bar, scatter, or heatmap depending on the evidence.

Actively warn before producing a chart that hides distribution, sample size, uncertainty, or comparison boundaries. If the user insists, proceed but show raw points or limitations where possible.

## Implementation Rules

- Avoid redundant in-figure titles. Retain panel headings or annotations that make the comparison clearer.
- Choose aspect ratio from the comparison and target paper width. Track any placement scaling.
- Keep axis labels short and readable.
- Use semantic color roles: proposed method, baseline, boundary or negative result, neutral reference.
- Use hatching, marker shape, or line style when the distinction must survive grayscale print.
- Use a colorblind-safe palette for categorical distinctions. Do not encode the key comparison with color alone.
- Judge text in the exported artifact at actual placement width. Revise labels or layout when dense content impairs reading.
- Include error bars or confidence intervals when the result is averaged over runs and the data supports it.
- Explain error type in the caption: SD, SEM, 95% CI, IQR, or other.
- Keep long interpretation in prose or captions; concise meaning-bearing annotations may belong in the plot.
- Prefer vector output for paper inclusion.
- Keep a clear figure-specific input/output mapping. A focused script, notebook cell or shared pipeline can provide it. Assemble related panels intentionally.

## Visual QA

For venue-ready plots, inspect an exported artifact at final placement; an in-memory preview can help find problems earlier:

1. Run `layout_tools.finalize_figure(fig)` when appropriate.
2. Render preview with `visual_qa.render_preview`.
3. Run `visual_qa.audit_layout` for glyph, clipping, and overlap issues.
4. Check every row against the 2-panel single-column or 4-panel cross-column minimum, then visually inspect for legend occlusion, unreadable labels, grayscale failure, panel misalignment, and cropped data.
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
- Keep irrelevant workflow bookkeeping in artifact or review notes. Retain scientifically necessary implementation identifiers, renderer details and truthful synthetic-data disclosures in the caption or prose where they support interpretation; a venue mandate is not required for relevant scientific content.
- Do not present placeholder values as real experimental results.

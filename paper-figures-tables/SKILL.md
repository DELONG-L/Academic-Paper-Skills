---
name: paper-figures-tables
description: Create, revise, and validate publication-ready academic paper figures and tables. Use for LaTeX tables, related-work comparison tables, result tables, notation/dataset/taxonomy tables, precise source-data-driven experiment plots from CSV/JSON/logs, generated conceptual figures such as system overviews/pipelines/architectures/threat models, captions, artifact specs, source-data traceability, and paper-ready PDF/SVG/PNG/LaTeX exports. Do not use for prose-only paper writing, self-review, reviewer response, rebuttal drafting, or external literature-management workflows.
---

# Paper Figures & Tables

Use this as the single entrypoint for paper artifacts: tables, precise data figures, generated conceptual figures, captions, and artifact QA. It merges house artifact style, data-visualization judgment, security/system plotting contracts, conceptual-figure planning, and experiment artifact checks.

## Priority Model

Always load `references/priority-model.md` first. Load only the task-specific references needed for the current artifact.

Authority order:

1. User-provided data, manuscript facts, target venue, and explicit instructions.
2. Writing handoff specs from `paper-writing`, when present.
3. House artifact style in `references/tables.md`, `references/conceptual-figures.md`, `references/captions.md`, and related figure/table rules.
4. Data-visualization and security/system plotting rules for precise data figures only.

Do not let generic artifact advice override user facts, house style, or route boundaries.

## Task Routing

| Task | Load |
|---|---|
| Decide table vs figure | `artifact-routing.md`, `captions.md` |
| Related Work comparison table | `tables.md`, `captions.md`, optionally `artifact-routing.md` |
| Result table, notation table, taxonomy table, risk matrix | `tables.md`, `captions.md`, `quality-checks.md` |
| Precise experiment/data plot from CSV/JSON/logs | `data-figures.md`, `data-profiling.md`, `chart-selection.md`, `visual-pitfalls.md`, `figure-contract.md`, `plot-patterns.md`, `captions.md`, `quality-checks.md` |
| Journal/venue-specific plot sizing or export | `journal-specs.md`, `visual-qa.md`, `publication-checklist.md`, then the relevant artifact reference |
| Conceptual figure, Figure 1, architecture, pipeline, threat model | `conceptual-figures.md`, `figure-contract.md`, `captions.md`, `quality-checks.md` |
| Statistical summary for artifact creation | `source-data-and-statistics.md`, then `tables.md` or `data-figures.md` |
| Caption-only task | `captions.md` plus the relevant artifact reference |
| Artifact QA or cleanup | `quality-checks.md`, then the relevant artifact reference |

## Hard Artifact Constraints

- Use source data or user-provided values. Do not invent numbers, baselines, methods, p-values, error bars, or visual trends.
- Every artifact must support one explicit paper claim or comparison.
- Every data-driven artifact must identify its source file or state that source data is missing.
- Tables use `booktabs` by default.
- LaTeX tables must use `\resizebox` to align with the target column width unless the natural table already fits cleanly and looks better without resizing. Use `\resizebox{\columnwidth}{!}` for single-column tables and `\resizebox{\textwidth}{!}` or `\resizebox{\linewidth}{!}` for full-width tables.
- Tables should be compact argumentative artifacts, not storage for every available dimension. Prefer single-column tables after pruning to the few dimensions that support the claim; use `table*` only when the argument would become misleading or unreadable in one column.
- Related Work should use an axis-based comparison table when this skill is asked to produce or finalize related-work artifacts, unless the user says prose-only or the venue forbids tables. Default to 3--4 high-signal comparison dimensions and single-column placement; widen only with an explicit reason.
- Precise experiment data figures must be source-data-driven Python/Matplotlib/Seaborn plots. Do not use image generation for numeric plots.
- Non-data conceptual paper images default to a generative image model. Python is not the default renderer for conceptual figures.
- A paper should normally contain at most one or two generated conceptual figures. Prefer Figure 1 plus, at most, one mechanism/threat-model detail figure.
- Conceptual paper figures, especially Figure 1, use a pure white page background by default. Do not use gradient washes, gray canvas fills, paper textures, vignettes, or atmospheric backgrounds.
- Figures must not contain in-figure titles. Put titles and interpretation in captions.
- Prefer vector exports (`.pdf` and/or `.svg`) for precise plots and LaTeX inclusion. PNG is acceptable for review packets and generated conceptual figures.
- Keep one generated plot script per semantic figure unless the task explicitly asks for a multi-panel artifact.
- Preserve house style: exact comparisons often belong in tables; trend shape, flow, geometry, and distribution belong in figures.
- Writing prose belongs to `paper-writing`; this skill may polish captions and short artifact callouts but should not draft full paper sections.

## Output Contracts

For LaTeX tables:

1. Return package or macro requirements when needed.
2. Return compile-ready LaTeX.
3. Include `\caption{}` and `\label{}`.
4. Do not put up/down arrows in table headers by default. If direction is needed, state it briefly in the caption or prose.
5. Define markers such as `\cmark`, `\pmark`, and `\xmark` only when needed for readability, preferably in a short caption phrase rather than a separate note.

For data figures:

1. Create or update a compact `figure_spec.yaml` or equivalent spec.
2. Profile source data before selecting the chart when raw tabular data is available.
3. Recommend the chart type from the paper claim and data shape; actively warn when the requested chart hides distribution, uncertainty, or sample size.
4. Save or describe outputs: `figure.pdf`, optional `figure.svg`, optional `figure.png`, script, source data path, and caption.
5. Validate readability at final paper width and run visual QA when a rendered preview is available.

For conceptual figures:

1. Read enough manuscript context before designing.
2. Produce a `brief.md`, `spec.json` or `figure_spec.yaml`, generation prompt, and caption draft.
3. Use a generative image model by default for system/pipeline/architecture/threat-model/method-intuition figures.
4. For Figure 1, system overview, pipeline, architecture, and threat-model figures, first create or update a precise editable `structure.svg` wireframe and use it as the primary structural reference for image generation.
5. Use Graphviz, Mermaid, TikZ, or final SVG only when strict topology, editable vector output, or venue constraints make them necessary.
6. Preserve the manuscript's structure; do not invent components not supported by the paper.

## Reference Map

- `references/priority-model.md`: source priority and conflict resolution.
- `references/artifact-routing.md`: table vs figure selection.
- `references/tables.md`: LaTeX table style and resizebox rule.
- `references/data-figures.md`: reproducible data-driven plotting workflow.
- `references/data-profiling.md`, `references/chart-selection.md`, `references/visual-pitfalls.md`: data-visualization advisor materials.
- `references/journal-specs.md`, `references/visual-qa.md`, `references/publication-checklist.md`: venue sizing, final-size rendering, and visual QA.
- `references/conceptual-figures.md`: generated conceptual figure planning and rendering.
- `references/captions.md`: self-contained captions and artifact callouts.
- `references/source-data-and-statistics.md`: source data, statistical summaries, and placeholders.
- `references/quality-checks.md`: artifact QA checklist.
- `references/figure-contract.md`, `references/plot-patterns.md`, `references/plot-recipes.md`, `references/data-figure-style-source.md`: detailed plotting resources.

## Script Map

- `scripts/profile_data.py`: profile tabular data before chart selection.
- `scripts/paperfig_style.py`: house helper for paper plots and semantic color roles.
- `scripts/setup_style.py`, `scripts/export_figure.py`, `scripts/layout_tools.py`, `scripts/visual_qa.py`, `scripts/check_figure.py`: final-size styling, export, layout, preview QA, and file audit for precise data figures.

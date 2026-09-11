---
name: paper-figures-tables
description: Create, revise, and validate publication-ready academic paper figures and tables. Use for LaTeX tables, related-work comparison tables, result tables, notation/dataset/taxonomy tables, precise source-data-driven experiment plots from CSV/JSON/logs, generated conceptual figures such as system overviews/pipelines/architectures/threat models, captions, artifact specs, source-data traceability, and paper-ready PDF/SVG/PNG/LaTeX exports. Do not use for prose-only paper writing, self-review, reviewer response, rebuttal drafting, or external literature-management workflows.
---

# Paper Figures & Tables

Use this as the single entrypoint for paper artifacts: tables, precise data figures, generated conceptual figures, captions, and artifact QA. It combines public integrity defaults, adaptable author preferences, data-visualization judgment, conceptual-figure planning, and experiment artifact checks.

Use `paper-policy` for manuscript integrity and applicable project/venue requirements. Select presentation guidance from the artifact’s needs and adaptable author preferences.

For authorization and internal handoffs, follow `../paper-policy/references/authority-model.md` (Task authorization and internal handoffs). Continue authorized local work across skill boundaries without another user invocation; preserve audit-only and explicit approval-before-editing scopes.

## Managed Research Workspace Preflight

Before creating or changing persistent paper artifacts, resolve a valid
`PROJECT-WORKSPACE.md` for the selected project, or the
`.research-workspace.yml` link when operating in its independent paper Git
repository. In a managed workspace, put final lightweight exports only in the
declared paper repository and update its `figure-manifest.yml` with the
experiment ID, run or data snapshot, generator, source path, and code
revision. Keep raw data, logs, checkpoints, and plotting scratch outside the
paper repository.

If no contract resolves, use the normal artifact workflow. Do not initialize a
workspace merely because an artifact is academic. Route repository setup,
asset-provenance repair, or workspace reorganization to
`research-workspace-governance`.

## Priority Model

Always load `references/priority-model.md` first. Load only the task-specific references needed for the current artifact.

Authority order:

1. Core integrity constraints from the sibling `paper-policy` skill.
2. User-provided data, manuscript facts, approved evidence, and explicit instructions.
3. Verified venue requirements.
4. Applicable hard rules from the shared academic workflow.
5. Writing handoff specs within the authorized task; a generated spec cannot override hard rules.
6. Editorial guidance, adaptable author preferences, and precise-plot advice.

Do not let generic artifact advice override user facts, enabled policy rules, or route boundaries. Presentation preferences do not establish academic correctness.

## Task Routing

| Task | Load |
|---|---|
| Decide table vs figure | `artifact-routing.md`, `captions.md` |
| Related Work comparison table | `tables.md`, `captions.md`; add `dense-empirical-tables.md` for a load-bearing multi-axis matrix and `layered-capability-matrix.md` when 8+ dimensions form explicit semantic layers |
| Result table, findings index, sample ledger, taxonomy table, risk matrix | `tables.md`, `captions.md`, `quality-checks.md`; add `dense-empirical-tables.md` when hierarchy or density is high |
| Precise experiment/data plot from supplied values or artifacts | `data-figures.md`, `captions.md`, `quality-checks.md`; add profiling, chart-selection or recipes only when the task needs those decisions |
| Journal/venue-specific plot sizing or export | `journal-specs.md`, `visual-qa.md`, `publication-checklist.md`, then the relevant artifact reference |
| Conceptual figure, Figure 1, architecture, pipeline, threat model | `conceptual-figures.md`, `figure-contract.md`, `captions.md`, `quality-checks.md` |
| Statistical summary for artifact creation | `source-data-and-statistics.md`, then `tables.md` or `data-figures.md` |
| Multi-run result table or plot | `source-data-and-statistics.md` for run validity, comparability and reproducible aggregation, then the relevant artifact reference |
| Caption-only task | `captions.md` plus the relevant artifact reference |
| Artifact QA or cleanup | `quality-checks.md`, then the relevant artifact reference |

For final figures/tables, source-data artifacts, Related Work tables, or any
artifact feeding submission readiness, also load `policy-integration.md`.

## Artifact Constraints And Defaults

- Use source data or user-provided values. Do not invent numbers, baselines, methods, p-values, error bars, or visual trends.
- Every artifact has a clear scientific purpose; related comparisons may share an organized multi-panel figure.
- Every data-driven artifact must identify its source file or state that source data is missing.
- Use `booktabs` as a clean option when compatible with the template. Natural-width tables are valid; verify final readability under `TABLE.FINAL_READABLE`.
- Prefer compact tables after pruning dimensions that add little to the claim. Use wider layouts when needed for a fair, readable comparison.
- Create an axis-based comparison table when useful to the argument or explicitly requested.
- Precise data figures must be derived from source data with reproducible plotting tools. Do not generate numeric trends or error bars with an image model.
- Select the conceptual-figure renderer from topology, editability, explicit requirements, and available tools. Use clean, readable design suited to the figure’s scientific purpose.
- Keep mathematical symbols, components, arrows, and boundaries faithful to the manuscript. Inspect the actual output; prompt wording is not evidence of correctness.
- Follow the active tools' editing constraints. Preserve source and transformation records for generated or edited artifacts; tool choice alone does not pass or fail scientific quality.
- Prefer captions for interpretation and avoid redundant in-figure titles. Panel labels or headings are valid when they improve navigation.
- Derive source dimensions and text size from the actual placement. Final-width visual QA is mandatory for final figures; source-point sizes alone do not establish readability.
- Prefer vector exports (`.pdf` and/or `.svg`) for precise plots and LaTeX inclusion. PNG is acceptable for review packets and generated conceptual figures.
- Keep each data figure traceable to a reproducible script, notebook or shared-pipeline entrypoint; reuse appropriate plotting infrastructure.
- Prefer tables for exact comparisons and figures for trend shape, flow, geometry, and distribution, adapting this heuristic to the artifact and task.
- Writing prose belongs to `paper-writing`; this skill may polish captions and short artifact callouts but should not draft full paper sections.

## Output Contracts

For LaTeX tables:

1. Return package or macro requirements when needed.
2. Return compile-ready LaTeX.
3. Include `\caption{}` and `\label{}`.
4. Make metric directions clear and use consistent, correctly rendered notation.
5. Define markers such as `\cmark`, `\pmark`, and `\xmark` only when needed for readability, preferably in a short caption phrase rather than a separate note.
6. Choose compact, dense or semantically grouped layouts as needed, then inspect at actual placement width.

For data figures:

1. Reuse source and encoding notes; write a compact spec when the figure's
   complexity warrants it. Formal compliance records are needed only for that assessment.
2. Profile unfamiliar raw data when it helps resolve types, grouping or chart selection.
3. Recommend the chart type from the paper claim and data shape; actively warn when the requested chart hides distribution, uncertainty, or sample size.
4. Save or describe outputs: `figure.pdf`, optional `figure.svg`, optional `figure.png`, script, source data path, and caption.
5. Validate source fonts, inspect the actual export at final paper width, and
   record the actual evaluator. Agent visual inspection is not human sign-off.

For conceptual figures:

1. Read enough manuscript context before designing.
2. Capture the supported content, placement and caption in existing notes or a concise spec; add a prompt when using image generation.
3. Select a renderer that suits the figure’s scientific purpose and applicable tool/venue constraints.
4. Add `generated_conceptual_figure` to context features and artifact types whenever an image model produces the final conceptual artifact.
5. For topology-sensitive generation, use an explicit component/connection specification or an editable wireframe when it helps preserve the structure. Reuse an existing accurate structural source.
6. Keep source and editing operations traceable. Code-native diagrams and image-model assets are valid choices when they satisfy the requested output and active tool constraints.
7. Preserve the manuscript's structure; do not invent components not supported by the paper.
8. Inspect final typography and semantics. Correct wrong or unreadable content with the selected tools, and leave unresolved requirements unverified when they cannot be checked.

## Reference Map

- `references/priority-model.md`: source priority and conflict resolution.
- `references/policy-integration.md`: context resolution, artifact evidence, adaptive source fonts, final-width QA, and compliance handoff.
- `references/artifact-routing.md`: table vs figure selection.
- `references/tables.md`: LaTeX table style and resizebox rule.
- `references/dense-empirical-tables.md`: optional design guide for grouped headers, compact empirical matrices, findings-at-a-glance tables, and sample ledgers.
- `references/layered-capability-matrix.md`: design guide for Related Work capability matrices with semantic column layers, conservative family-row evidence, and grounded coverage-delta highlights.
- `references/data-figures.md`: reproducible data-driven plotting workflow.
- `references/data-profiling.md`, `references/chart-selection.md`, `references/visual-pitfalls.md`: data profiling, chart selection, and visual-risk guidance.
- `references/journal-specs.md`, `references/visual-qa.md`, `references/publication-checklist.md`: venue sizing, final-size rendering, and visual QA.
- `references/conceptual-figures.md`: generated conceptual figure planning and rendering.
- `references/captions.md`: self-contained captions and artifact callouts.
- `references/source-data-and-statistics.md`: source data, statistical summaries, and placeholders.
- `references/quality-checks.md`: artifact QA checklist.
- `references/figure-contract.md`, `references/plot-patterns.md`, `references/plot-recipes.md`, `references/data-figure-style-source.md`: detailed plotting resources.

## Script Map

- `scripts/profile_data.py`: profile tabular data before chart selection.
- `scripts/paperfig_style.py`: reusable helper for paper plots and semantic color roles.
- `scripts/setup_style.py`, `scripts/export_figure.py`, `scripts/layout_tools.py`, `scripts/visual_qa.py`, `scripts/check_figure.py`: final-size styling, export, layout, preview QA, and file audit for precise data figures.

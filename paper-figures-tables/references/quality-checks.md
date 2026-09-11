# Quality Checks

Use this before finishing any figure or table task.

## Universal Checks

- The artifact has a clear scientific purpose; related questions may share an intentionally organized multi-panel figure.
- Source data, source notes, manuscript context, or handoff spec is identified.
- Caption is self-contained.
- Label exists and follows local convention.
- Artifact is referenced by the manuscript or has a proposed reference sentence.
- Claims do not exceed the data or manuscript content shown.
- Titles, panel headings and annotations help interpretation without needless repetition of the caption.
- Venue constraints are respected when supplied: page limit, anonymity, allowed formats, color restrictions, and appendix/supplement rules.

## Table Checks

- Uses `booktabs` when the final-table hard rule or venue requires it; otherwise the selected rule style is internally consistent.
- Aligns with `\columnwidth`, `\textwidth`, or `\linewidth`; uses `\resizebox` only when the active rule requires it or structural fitting is insufficient and the scaled text remains readable.
- Uses the smallest readable placement; Related Work and comparison tables are single-column by default after pruning to high-signal dimensions.
- Related Work comparison dimensions and row definitions are clear and supported; layout preferences need no waiver.
- Up/down arrows are not used in headers by default; metric directions, if needed, are stated briefly in caption or prose.
- `\cmark`, `\pmark`, `\xmark`, colors, abbreviations, or ratios are defined.
- Every family-row marker is conservative across all named members; mixed support uses `\pmark`.
- Every uniqueness or coverage-delta highlight has a defined comparison corpus, row-wise evidence, and wording bounded to that corpus.
- Every meaning-bearing color highlight has a non-color cue and remains interpretable in grayscale.
- Notes are omitted unless necessary for interpretation.
- `threeparttable` is used only with actual `tablenotes`; the caption states the claim and scope while notes carry secondary definitions or caveats.
- Semantic emphasis is used sparingly; not every strong-looking cell is bolded or colored.
- Wide matrices use `table*` before becoming unreadable single-column tables.
- Keep irrelevant workflow bookkeeping in artifact or review notes. Retain scientifically necessary implementation identifiers, renderer details and truthful synthetic-data disclosures in the caption or prose where they support interpretation; a venue mandate is not required for relevant scientific content.

## Precise Data Figure Checks

- Source-to-placement scaling is understood, and text remains readable at the actual final width.
- Generated from source data or explicitly supplied values.
- No image-generation model was used to create numeric axes, points, bars, lines, trends, error bars, or p-values.
- Chart choice matches the claim and data shape; bad-chart risks are noted when relevant.
- Axis labels and legends are readable at final paper width.
- Error bars or variability are included when supported by runs and explained in the caption.
- Colors and markers survive grayscale or colorblind viewing.
- Plot text, ticks, legends, and panel labels are legible at the final LaTeX placement.
- Values trace back to source data.
- Script reruns from a documented working directory.
- Exports include PDF or SVG for LaTeX when practical.
- Visual QA was performed for final venue-ready plots when a rendered preview is available.
- Record actual final-width inspection and its evaluator. Agent visual inspection is agent evidence, not human sign-off. Use formal compliance records only when that assessment is in scope; manual rules still require their declared authority.

## Conceptual Figure Checks

- Renderer and format suit the topology, editing needs, and available tools.
- Components, mathematical symbols, labels, and flow match the manuscript.
- Trust boundaries and transformations are clear.
- Any structural reference agrees with the final figure or records intentional changes.
- Fonts, contrast, spacing, and labels remain readable at the actual paper width.
- Presentation supports the figure’s scientific purpose and any verified venue requirements.
- Source and transformations are recorded; a prompt alone does not prove fidelity.
- Caption explains scope and non-obvious visual semantics.

## Stop Conditions

Leave the affected artifact incomplete and state the missing input when
required source data are unavailable, interpretations cannot be resolved from
the manuscript, or producing the artifact would require invented results or
components. After reasonable correction attempts, report unreadable or
incorrect labels, formulas, or topology that remain unresolved. A different
font, background, marker scheme, or renderer is not itself a reason to stop.

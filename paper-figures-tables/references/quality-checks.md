# Quality Checks

Use this before finishing any figure or table task.

## Universal Checks

- The artifact supports one explicit paper claim or comparison.
- Source data, source notes, manuscript context, or handoff spec is identified.
- Caption is self-contained.
- Label exists and follows local convention.
- Artifact is referenced by the manuscript or has a proposed reference sentence.
- Claims do not exceed the data or manuscript content shown.
- No in-artifact title is used for figures.
- Venue constraints are respected when supplied: page limit, anonymity, allowed formats, color restrictions, and appendix/supplement rules.

## Table Checks

- Uses `booktabs` when the final-table hard rule or venue requires it; otherwise the selected rule style is internally consistent.
- Aligns with `\columnwidth`, `\textwidth`, or `\linewidth`; uses `\resizebox` only when the active rule requires it or structural fitting is insufficient and the scaled text remains readable.
- Uses the smallest readable placement; Related Work and comparison tables are single-column by default after pruning to high-signal dimensions.
- Related Work tables use the axis-based comparison-table style unless explicitly waived.
- Up/down arrows are not used in headers by default; metric directions, if needed, are stated briefly in caption or prose.
- `\cmark`, `\pmark`, `\xmark`, colors, abbreviations, or ratios are defined.
- Every family-row marker is conservative across all named members; mixed support uses `\pmark`.
- Every uniqueness or coverage-delta highlight has a defined comparison corpus, row-wise evidence, and wording bounded to that corpus.
- Every meaning-bearing color highlight has a non-color cue and remains interpretable in grayscale.
- Notes are omitted unless necessary for interpretation.
- `threeparttable` is used only with actual `tablenotes`; the caption states the claim and scope while notes carry secondary definitions or caveats.
- Semantic emphasis is used sparingly; not every strong-looking cell is bolded or colored.
- Wide matrices use `table*` before becoming unreadable single-column tables.
- Captions do not include internal source paths, plotting scripts, renderer names, DPI checks, or internal provenance status unless the manuscript explicitly requires an audit section.

## Precise Data Figure Checks

- Source canvas uses the declared scale; below-24pt text is reported as a soft adaptation with final-width evidence.
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
- The final-width human QA result and artifact ID are recorded in
  `compliance-evidence.yaml`; source-level PASS alone is not treated as complete.

## Conceptual Figure Checks

- A generative image model is the default renderer unless strict topology, editability, or venue constraints justify another renderer.
- The paper does not exceed the normal 1-2 generated-conceptual-figure budget without explicit justification.
- Figure 1, system overview, pipeline, architecture, and threat-model figures include a precise `structure.svg` wireframe or an explicit note explaining why it was unnecessary.
- The generated image preserves the `structure.svg` component set, topology, arrow direction, boundaries, and labels, or the deviations are documented and intentional.
- Components match the manuscript.
- Direction of flow is correct.
- Trust boundaries, attacker paths, or data transformations are visually clear.
- Figure 1 and overview-like conceptual figures use a pure white background, with no gradient wash, texture, vignette, or gray canvas.
- When `FIG.CONCEPT_TYPOGRAPHY` is active, every non-mathematical label and annotation is Times New Roman.
- Mathematical variables, operators, Greek symbols, and equations use a dedicated manuscript- or venue-compatible math font rather than Times New Roman imitation.
- Exact font roles are inspected in the accepted model output; prompt wording or silent font fallback is not treated as proof. Uncertain typography triggers regeneration or a stop, never a post-generation repair.
- For `generated_conceptual_figure`, every visible semantic element is present in the accepted model output and the final artifact contains no later text, formula, arrow, icon, component, or boundary overlay.
- Post-generation operations are limited to non-semantic crop, resize, compression, color-profile conversion, or format wrapping.
- Labels are short and readable.
- No title appears inside the generated image.
- Caption explains semantics that are not obvious.

## Stop Conditions

Stop and ask or emit a spec instead of final artifact when:

- required source data is absent for a precise data figure
- multiple incompatible artifact interpretations exist
- the user asks for exact values but only prose is available
- the artifact would require inventing methods, baselines, citations, components, or results
- a generated conceptual figure has wrong or unreadable labels, formulae, font roles, or topology after reasonable model regeneration attempts
- Times New Roman or the required mathematical font is unavailable or cannot be verified and no user/venue waiver exists
- the generative image model repeatedly corrupts the `structure.svg` topology or labels; post-generation semantic repair is not an allowed fallback

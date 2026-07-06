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

- Uses `booktabs`.
- Uses `\resizebox` to align with `\columnwidth`, `\textwidth`, or `\linewidth` unless natural width is visibly better.
- Uses the smallest readable placement; Related Work and comparison tables are single-column by default after pruning to high-signal dimensions.
- Related Work tables use the axis-based comparison-table style unless explicitly waived.
- Up/down arrows are not used in headers by default; metric directions, if needed, are stated briefly in caption or prose.
- `\cmark`, `\pmark`, `\xmark`, colors, abbreviations, or ratios are defined.
- Notes are omitted unless necessary for interpretation.
- Semantic emphasis is used sparingly; not every strong-looking cell is bolded or colored.
- Wide matrices use `table*` before becoming unreadable single-column tables.
- Captions do not include internal source paths, plotting scripts, renderer names, DPI checks, or internal provenance status unless the manuscript explicitly requires an audit section.

## Precise Data Figure Checks

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

## Conceptual Figure Checks

- A generative image model is the default renderer unless strict topology, editability, or venue constraints justify another renderer.
- The paper does not exceed the normal 1-2 generated-conceptual-figure budget without explicit justification.
- Figure 1, system overview, pipeline, architecture, and threat-model figures include a precise `structure.svg` wireframe or an explicit note explaining why it was unnecessary.
- The generated image preserves the `structure.svg` component set, topology, arrow direction, boundaries, and labels, or the deviations are documented and intentional.
- Components match the manuscript.
- Direction of flow is correct.
- Trust boundaries, attacker paths, or data transformations are visually clear.
- Figure 1 and overview-like conceptual figures use a pure white background, with no gradient wash, texture, vignette, or gray canvas.
- Labels are short and readable.
- No title appears inside the generated image.
- Caption explains semantics that are not obvious.

## Stop Conditions

Stop and ask or emit a spec instead of final artifact when:

- required source data is absent for a precise data figure
- multiple incompatible artifact interpretations exist
- the user asks for exact values but only prose is available
- the artifact would require inventing methods, baselines, citations, components, or results
- a generated conceptual figure has wrong/unreadable labels and cannot be corrected without changing renderer
- the generative image model repeatedly corrupts the `structure.svg` topology or labels and no deterministic overlay or editable-renderer fallback is acceptable

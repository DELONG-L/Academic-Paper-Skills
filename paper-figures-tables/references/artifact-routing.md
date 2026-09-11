# Artifact Routing

## Choose the Information Before the Layout

Identify the comparison or explanation the reader needs. Select dimensions from
that purpose and the available evidence, including important counterexamples or
unfavorable comparisons. Remove decorative columns before shrinking type or
expanding width; do not remove dimensions merely because they weaken the proposed
method's apparent advantage. A synthesis table may legitimately need many axes.

For a conceptual figure, establish supported entities, relationships, inputs,
outputs and grouping before visual styling. Split an overloaded overview when it
mixes abstraction levels; do not add an overview or gap teaser solely because it
is Figure 1. For a data figure, match the visual encoding to the question and
preserve uncertainty/distribution when relevant.

For long heatmap labels, consider meaningful abbreviations with an accessible
mapping, wrapping, or a different layout. Select single-column, full-width or
multi-panel form by actual final-size readability. No fixed aspect ratio, panel
count, column budget or source-canvas font size proves that the figure works.

Use this to choose between tables, precise data figures, and conceptual figures.

## Use A Table When

- The reader needs exact values.
- The artifact compares many methods, datasets, settings, papers, systems, or dimensions.
- The artifact is a related-work comparison, taxonomy, lifecycle map, notation list, risk matrix, ablation matrix, or dense result matrix.
- The argument depends on categorical support such as `\cmark`, `\pmark`, and `\xmark`.
- The result has many metrics or baselines where a plot would hide exact comparison.

For Related Work, choose an axis-based table when it adds comparative value or
is explicitly required. Sufficient axis-based prose does not need a redundant table.

Before choosing a wide table, ask whether the table can make its point with fewer columns. Prefer a single-column table when the relevant dimensions fit clearly; choose `table*` only when the additional dimensions are essential and still readable.

## Use A Precise Data Figure When

- The reader needs trend shape, distribution, scaling behavior, Pareto frontier, sensitivity, temporal dynamics, or geometric separation.
- The source is CSV/JSON/log/TensorBoard data and visual encoding reveals structure better than exact cells.
- The artifact is a line plot, grouped bar, heatmap, scatter, CDF, histogram, box/violin plot, error-bar plot, or tradeoff panel.
- The output must be reproducible from source data and a plotting script.

Use data-visualization data profiling and chart-selection references before drawing when raw tabular data is available.

## Use A Conceptual Figure When

- The reader needs to understand architecture, workflow, trust boundary, threat model, data flow, protocol sequence, lifecycle, system overview, or method intuition.
- The artifact should orient the paper before details or explain a mechanism that prose alone cannot keep clear.
- The visual does not encode exact experimental values.

Choose conceptual-figure tools from topology, editability, available capabilities, and venue requirements. Code-native vector diagrams and image generation are both valid when suited to the requested artifact.

## If Both Table And Figure Are Plausible

Use both only when they serve different jobs: a figure for the pattern and a table for exact values. Otherwise pick one and state the reason in the artifact spec.

## Writing Handoff

When `paper-writing` provides a handoff, preserve:

- claim supported
- row/column dimensions
- label
- caption draft
- source data or source notes
- in-text reference sentence

If the handoff implies a missing citation or literature source, return a manual-update note rather than fabricating rows or citations.

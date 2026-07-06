# Artifact Routing

Use this to choose between tables, precise data figures, and conceptual figures.

## Use A Table When

- The reader needs exact values.
- The artifact compares many methods, datasets, settings, papers, systems, or dimensions.
- The artifact is a related-work comparison, taxonomy, lifecycle map, notation list, risk matrix, ablation matrix, or dense result matrix.
- The argument depends on categorical support such as `\cmark`, `\pmark`, and `\xmark`.
- The result has many metrics or baselines where a plot would hide exact comparison.

Related Work artifacts should normally be axis-based comparison tables unless the user says prose-only or the target venue forbids tables.

Before choosing a wide table, ask whether the table can make its point with fewer columns. Prefer a single-column table when 3--4 dimensions carry the claim; choose `table*` only when the additional dimensions are essential and still readable.

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

Conceptual figures default to generation with a generative image model. Use Graphviz, Mermaid, TikZ, or hand-authored SVG only when strict topology, editable vector output, or venue constraints require them.

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

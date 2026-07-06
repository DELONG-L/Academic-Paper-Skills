# Artifact Handoffs

Use this when a writing task identifies a figure or table need.

Writing owns the rhetorical need and content specification. Figures & Tables owns final artifact rendering, visual design, table layout, data plotting, `resizebox`, package choices, compile fixes, and figure export.

## Handoff Principles

- Do not let a writing task silently omit an important table or figure.
- Do not attempt final table/figure rendering inside Writing unless the user explicitly asks for a small prose-adjacent snippet.
- Always connect an artifact to a claim.

## Related Work Table Handoff

```text
Figures & Tables handoff:
- Artifact: related-work comparison table
- Claim supported:
- Label: tab:related-comparison
- Row groups:
- Columns / dimensions: default to 3--4 high-signal dimensions; include an explicit reason for 5+ dimensions
- Placement preference: single-column by default; use full-width only when pruning would weaken the argument
- Marker semantics: \cmark = full support, \pmark = partial support, \xmark = absent, only if symbol markers are needed
- Proposed method row:
- Caption draft: compact paper caption, not internal provenance prose
- In-text reference sentence:
```

## Results Artifact Handoff

```text
Figures & Tables handoff:
- Artifact: result table or plot
- Claim supported:
- Source data:
- Metrics and directions:
- Baselines / variants:
- Expected table/figure label:
- Caption draft: paper-facing interpretation; keep file paths, scripts, renderer names, and validation notes out of the caption unless required
- In-text interpretation paragraph:
```

## Conceptual Figure Handoff

```text
Figures & Tables handoff:
- Artifact: conceptual figure
- Claim or section supported:
- Components:
- Flows / arrows:
- Boundaries:
- What the reader should understand in 5 seconds:
- Caption draft:
```

## Writing Around Missing Artifacts

If an artifact is planned but not yet rendered, write prose with stable labels only when the user wants LaTeX integration. Otherwise, keep labels as placeholders:

```latex
Table~\ref{tab:related-comparison} will summarize this distinction.
```

Do not claim a result that depends on an artifact whose data or content has not been supplied.

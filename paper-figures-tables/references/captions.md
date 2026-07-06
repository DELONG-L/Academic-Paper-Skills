# Captions

Use this for figure and table captions.

## Caption Job

A caption is a miniature interpretation, not a label.

It should state:

1. What artifact reports.
2. The scope: dataset, task count, method family, attack variant, benchmark, or corpus.
3. How to read symbols, colors, markers, axes, or metric directions.
4. The main takeaway or boundary.

In the paper body, captions should read like paper captions, not internal provenance records. Keep internal provenance such as source file paths, plotting scripts, renderer names, DPI checks, placeholder-citation status, and artifact-bundle notes in README, review notes, artifact specs, or supplementary audit files unless the venue explicitly requires that provenance in the manuscript.

## Table Captions

Define markers or metric directions only when the table would otherwise be ambiguous:

```latex
\caption{Comparison of related approaches by boundary mechanism. \cmark{} denotes explicit support and \pmark{} partial support.}
```

For result tables, include metric meanings when needed, but do not use up/down arrows in headers by default:

```latex
\caption{Main results across four task domains. Higher success and plan quality are better; lower leakage and cost are better.}
```

Do not add a separate Notes block unless it is necessary for interpreting symbols, abbreviations, or nonstandard metrics.

## Figure Captions

For conceptual figures, explain component order and arrow/color semantics.

For plots, state the trend and whether error bars, dashed baselines, shared legends, or shaded regions have meaning.

Use `(a)`, `(b)`, etc. in the caption for multi-panel figures even when the LaTeX uses separate `\includegraphics` calls.

For precise data figures, define uncertainty and statistics when present: SD, SEM, 95% CI, IQR, number of runs, statistical test, correction, or significance symbol meanings.

For generated conceptual figures, keep the caption factual: describe manuscript-supported components and flows. Do not claim the generated image proves, measures, or validates anything.

## Avoid

- `Results of our method.`
- `Ablation study.`
- captions that only repeat the figure/table title
- captions that read like internal audit logs
- renderer or script provenance in the paper caption unless required
- verbose marker notes when a short phrase is enough
- unsupported interpretation not visible in the artifact or data
- statistical language that is not backed by source data

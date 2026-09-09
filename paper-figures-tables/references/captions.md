# Captions

Use this for figure and table captions.

## Caption Job

A caption should identify the artifact and supply what the reader needs to
interpret it. Choose its content by artifact type and surrounding context:

- A conceptual diagram needs the components, relationship semantics and intended
  explanation when these are not already clear in the graphic.
- A result figure or table needs the measurement/setting and definitions of
  meaningful encodings, units and uncertainty. Interpretation can remain in the
  Results prose when repeating it in the caption adds nothing.
- Keep essential setup near the artifact; use a note or nearby prose for lengthy
  detail when that is clearer. Do not force all setup into footnotes or all
  conclusions into a caption.

Do not append an unasked defense of what the artifact cannot establish. Retain
actual synthetic-data disclosures and conditions needed to interpret the values.

- Keep irrelevant workflow bookkeeping in artifact or review notes. Retain scientifically necessary implementation identifiers, renderer details and truthful synthetic-data disclosures in the caption or prose where they support interpretation; a venue mandate is not required for relevant scientific content.

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
- renderer or script bookkeeping with no scientific or required disclosure role
- verbose marker notes when a short phrase is enough
- unsupported interpretation not visible in the artifact or data
- statistical language that is not backed by source data

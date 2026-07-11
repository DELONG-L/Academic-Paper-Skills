# Tables

Use this for LaTeX tables, related-work comparison tables, result tables, notation tables, taxonomy tables, and risk matrices.

## Core Style

Prefer clean grouped headers, compact captions, and semantic emphasis over plain
grid tables. Require `booktabs` only when `TABLE.BOOKTABS_FINAL` is active;
otherwise use it as a compatible option. Tables should make one comparison easy
to scan rather than store every available dimension.

Do not use dense grid lines. Prefer spacing, grouped headers, and row order to communicate structure. In a load-bearing high-density matrix, one or two sparse vertical separators may mark true column groups when whitespace and `\cmidrule` are insufficient; do not box individual cells.

Use the compact patterns in this file when compatible with active policy. Load
`dense-empirical-tables.md` only when `TABLE.DENSE_EMPIRICAL_STYLE` is enabled
or the user explicitly requests that profile.

Common packages and macros:

```latex
\usepackage{booktabs}
\usepackage{array}
\usepackage{multirow}
\usepackage{makecell}
\usepackage{graphicx}
\usepackage[table]{xcolor}
\usepackage{pifont}
\usepackage{threeparttable}

\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\definecolor{MethodBlue}{RGB}{232,241,250}
\definecolor{TableSage}{RGB}{165,165,141}
\colorlet{TableHeaderShade}{TableSage!22}
\definecolor{okgreen}{RGB}{31,138,76}
\definecolor{nored}{RGB}{198,55,45}
\definecolor{okamber}{RGB}{214,148,18}
\newcommand{\cmark}{\textcolor{okgreen}{\ding{51}}}
\newcommand{\pmark}{\textcolor{okamber}{\footnotesize\ding{108}}}
\newcommand{\xmark}{\textcolor{nored}{\ding{55}}}
```

Only include package or macro definitions if the target paper does not already define them.

## Resizebox Rule

When `TABLE.FINAL_TARGET_WIDTH` is active, align the table with the target width.
Use `\resizebox` only when scaling is needed and the natural table does not fit
cleanly; prefer structural pruning over unreadable shrinkage.

Use:

```latex
\resizebox{\columnwidth}{!}{...}
```

for single-column tables, and:

```latex
\resizebox{\textwidth}{!}{...}
```

or:

```latex
\resizebox{\linewidth}{!}{...}
```

inside `table*` or width-constrained wrappers.

Only omit `resizebox` when all of these hold:

- the table naturally fits the intended column or page width
- there is no overfull hbox risk
- column spacing and font size are readable
- the rendered table is visually better without scaling

## Placement And Dimension Budget

When the strict placement preferences are enabled, default to the smallest readable placement.

- Prefer single-column `table` for compact comparison tables, notation tables, and most Related Work comparison tables.
- Before using `table*`, prune columns to the minimum set that supports the table's claim.
- A Related Work comparison table should normally use 3--4 high-signal dimensions. Use 5 only when the fifth dimension is essential. Use 6 or more only with an explicit reason in the artifact spec.
- If a table becomes wide because the column names are verbose, shorten the headers before switching to `table*`.
- Do not add a Notes block unless the table cannot be read without it.

## Related Work Comparison Tables

Rows should be paper families, systems, datasets, mechanisms, or approaches. Columns should expose the missing comparison axis from the paper.

When `RELATED.COMPARISON_REQUIRED` is active, produce or preserve an axis-based
comparison table unless an authorized waiver or venue requirement applies. If
the rule is disabled, create one only when requested or argumentatively useful.

When `TABLE.CANONICAL_RELATED_MARKERS` is active, use `\cmark` as a green
check for full support, `\pmark` as an amber filled pifont circle
(`\ding{108}`) for partial support, and `\xmark` as a red cross for absence.
When disabled, choose accessible symbols or text that fit the venue and define
their semantics locally.

Prefer rows that are atomic enough for every marker to be directly defensible. A clearly named literature family is an allowed soft adaptation when its membership is coherent and every marker is assigned conservatively across the entire family. Do not use a naked merged citation row such as `\citep{a,b,c}`. Cite representative works in prose or in the row label, and use `\pmark` whenever support is mixed or only partial across the group.

Represent missing values explicitly. Prefer `N/A`, `Not reported`, or `Not applicable`, and define shortened forms locally. Avoid `---` and unexplained dash glyphs because they obscure whether a value is absent, inapplicable, or merely unreported.

### Table-1-Style Related Work Matrix

Use this compact single-column pattern for paper-positioning tables that compare prior work against the paper's claimed gap. Use 3--4 dimensions by default; use 5 only when the fifth dimension is essential to the argument.

```latex
\begin{table}[t]
\centering
\scriptsize
\setlength{\tabcolsep}{2.2pt}
\renewcommand{\arraystretch}{1.03}
\caption{Positioning against related work. A = ..., B = ..., C = ...; \cmark{} full, \pmark{} partial, \xmark{} absent.}
\label{tab:related-work-positioning}
\resizebox{\columnwidth}{!}{%
\begin{tabular}{@{}L{0.40\columnwidth}ccccc@{}}
\toprule
\textbf{Work} & \textbf{A} & \textbf{B} & \textbf{C} & \textbf{D} & \textbf{E} \\
\midrule
\citep{prior1} & \pmark & \xmark & \xmark & \xmark & \xmark \\
\citep{prior2} & \cmark & \pmark & \xmark & \xmark & \pmark \\
\rowcolor{MethodBlue}
\textbf{Ours} & \cmark & \cmark & \cmark & \cmark & \cmark \\
\bottomrule
\end{tabular}%
}
\end{table}
```

Do not choose dimensions solely to make the proposed method look good. The columns must follow from the paper's stated gap.

Do not fabricate prior-work rows, citation keys, or feature support. If a row or citation is missing, return a manual-update note asking the user to supply the needed BibTeX/source details.

## Result Tables

Use result tables when exact comparisons matter.

Rules:

- When `TABLE.NO_DIRECTION_ARROWS` is enabled, state metric directions in the caption or prose instead of using header arrows.
- If a table has mixed metric directions, put the direction sentence in the caption instead of repeating symbols in every header.
- Bold best values or intended operating points, not every good-looking number.
- Use `\multicolumn` and `\cmidrule(lr){i-j}` for grouped metrics.
- Use a subtle `\rowcolor{TableHeaderShade}` header band when it improves hierarchy and survives grayscale rendering.
- Use `\multirow`, `\makecell`, or italic `\multicolumn` group labels when repeated row labels obscure the table's structure.
- Use `\rowcolor{blue!8}` or a local method macro sparingly for the proposed method.
- Use `threeparttable` when definitions or caveats would make the caption too long.

## Notation And Dataset Tables

Use compact single-column tables when possible. Group symbols or dataset fields by topic.

Notation tables should define only symbols used later. Dataset tables should include units, counts, and filtering boundaries.

## Common Mistakes

- Do not use plain `\hline` grid tables by default.
- Do not color every result cell.
- Do not replace the canonical marker scheme when `TABLE.CANONICAL_RELATED_MARKERS` is active.
- Do not merge multiple unrelated papers into one citation-only row; split rows unless the row is an explicitly named family and the marker values are conservative.
- Do not force a wide matrix into a single-column table with unreadable text.
- Do not write captions that merely restate the table label.
- Do not keep a wide table only because the first draft had many dimensions.
- Do not put internal data paths, script names, renderer names, or internal provenance status in a paper caption.

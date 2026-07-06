# Tables

Use this for LaTeX tables, related-work comparison tables, result tables, notation tables, taxonomy tables, and risk matrices.

## Core Style

Use `booktabs` by default. Prefer clean grouped headers, compact captions, and semantic emphasis over plain grid tables. Tables should make one comparison easy to scan; they should not store every dimension that happened to be available.

Do not use vertical rules or dense grid lines unless the venue template requires them. Prefer spacing, grouped headers, and row order to communicate structure.

Common packages and macros:

```latex
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{makecell}
\usepackage{graphicx}
\usepackage[table]{xcolor}
\usepackage{pifont}
\usepackage{threeparttable}

\newcommand{\cmark}{\textcolor{green!60!black}{\ding{51}}}
\newcommand{\xmark}{\textcolor{red!70!black}{\ding{55}}}
\newcommand{\pmark}{\textcolor{orange!80!black}{$\circ$}}
```

Only include package or macro definitions if the target paper does not already define them.

## Resizebox Rule

LaTeX tables must use `\resizebox` to align with the target column width unless the natural table already fits cleanly and looks better without resizing.

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

Default to the smallest readable placement.

- Prefer single-column `table` for compact comparison tables, notation tables, and most Related Work comparison tables.
- Before using `table*`, prune columns to the minimum set that supports the table's claim.
- A Related Work comparison table should normally use 3--4 high-signal dimensions. Use 5 only when the fifth dimension is essential. Use 6 or more only with an explicit reason in the artifact spec.
- If a table becomes wide because the column names are verbose, shorten the headers before switching to `table*`.
- Do not add a Notes block unless the table cannot be read without it.

## Related Work Comparison Tables

Rows should be paper families, systems, datasets, mechanisms, or approaches. Columns should expose the missing comparison axis from the paper.

When finalizing Related Work artifacts, produce or preserve an axis-based comparison table unless the user explicitly asks for prose-only output or the venue forbids tables. If `paper-writing` provides only a handoff spec, convert it into compile-ready LaTeX rather than re-deciding the rhetorical gap from scratch.

Use `\cmark`, `\pmark`, and `\xmark` for qualitative support when they make the missing axis easier to scan. Keep marker explanations short and local to the caption when necessary.

```latex
\begin{table}[t]
\centering
\caption{Comparison of related approaches by boundary mechanism.}
\label{tab:related-comparison}
\resizebox{\columnwidth}{!}{%
\begin{tabular}{lccc}
\toprule
\textbf{Approach} & \textbf{Boundary} & \textbf{Scoped Memory} & \textbf{Leakage Metric} \\
\midrule
Prior A & \pmark & \xmark & \xmark \\
Prior B & \cmark & \pmark & \xmark \\
\rowcolor{blue!8}
\textbf{Ours} & \cmark & \cmark & \cmark \\
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

- Do not use up/down arrows in metric headers by default. State directions in the caption or prose when needed.
- If a table has mixed metric directions, put the direction sentence in the caption instead of repeating symbols in every header.
- Bold best values or intended operating points, not every good-looking number.
- Use `\multicolumn` and `\cmidrule(lr){i-j}` for grouped metrics.
- Use `\rowcolor{blue!8}` or a local method macro sparingly for the proposed method.
- Use `threeparttable` when definitions or caveats would make the caption too long.

## Notation And Dataset Tables

Use compact single-column tables when possible. Group symbols or dataset fields by topic.

Notation tables should define only symbols used later. Dataset tables should include units, counts, and filtering boundaries.

## Common Mistakes

- Do not use plain `\hline` grid tables by default.
- Do not color every result cell.
- Do not force a wide matrix into a single-column table with unreadable text.
- Do not write captions that merely restate the table label.
- Do not keep a wide table only because the first draft had many dimensions.
- Do not put internal data paths, script names, renderer names, or internal provenance status in a paper caption.

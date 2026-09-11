# Tables

Use this for LaTeX tables, related-work comparison tables, result tables, notation tables, taxonomy tables, and risk matrices.

## Core Style

Prefer clean grouped headers, compact captions, and semantic emphasis over plain
grid tables. Use `booktabs` as a clean option when compatible with the template. Tables should make one comparison easy
to scan rather than store every available dimension.

Do not use dense grid lines. Prefer spacing, grouped headers, and row order to communicate structure. In a load-bearing high-density matrix, one or two sparse vertical separators may mark true column groups when whitespace and `\cmidrule` are insufficient; do not box individual cells.

Use compact patterns when they fit the comparison. Load
`dense-empirical-tables.md` when grouping and numeric density need special care;
load `layered-capability-matrix.md` when the dimensions form meaningful layers.
Choose these guides from the artifact’s needs, without a registered style profile.

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

## Width And Readability

Under `TABLE.FINAL_READABLE`, the table must remain readable and fit within the
available page area. A natural-width table is valid. Use `\resizebox` only when
needed, and prefer structural pruning over unreadable shrinkage.

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

Before finalizing a table, check:

- the table naturally fits the intended column or page width
- there is no overfull hbox risk
- column spacing and font size are readable
- scaling, if used, does not make the final table unreadable

## Placement And Dimension Budget

Prefer the smallest layout that preserves a fair, readable comparison.

- Prefer single-column `table` for compact comparison tables, notation tables, and most Related Work comparison tables.
- Before using `table*`, prune columns to the minimum set that supports the table's claim.
- Retain dimensions that support a fair comparison. Use semantic grouping when it clarifies their relationships; no numerical column budget applies.
- If a table becomes wide because the column names are verbose, shorten the headers before switching to `table*`.
- Do not add a Notes block unless the table cannot be read without it.

## Related Work Comparison Tables

Rows should be paper families, systems, datasets, mechanisms, or approaches. Columns should expose the missing comparison axis from the paper.

Use an axis-based table when it adds argumentative value. Choose prose when a
table would repeat the argument or imply unsupported comparability. An explicit
request or sourced venue requirement still governs the requested artifact.

Choose accessible symbols or text and define their semantics locally. The
`\cmark`/`\pmark`/`\xmark` macros above are an example, not a required scheme.
State full, partial, absent, and unreported support accurately, independently
of the chosen color or glyph.

Prefer rows that are atomic enough for every marker to be directly defensible. A clearly named literature family is useful when its membership is coherent and every marker is assigned conservatively across the entire family. Do not use a naked merged citation row such as `\citep{a,b,c}`. Cite representative works in prose or in the row label, and mark partial support explicitly whenever evidence is mixed across the group.

Do not treat highlighting as proof. A proposed-row background is optional: bold
the row label, use a light whole-row tint, use sparse cell-level coverage-delta
highlights, or omit highlighting according to scanning and accessibility needs. Any
meaning-bearing color needs a non-color cue. A highlighted cell must be supported
against a defined comparison corpus; unless that corpus is exhaustive, describe
the capability as "absent from the compared rows," not universally "unique to
this work."

Represent missing values explicitly. Prefer `N/A`, `Not reported`, or `Not applicable`, and define shortened forms locally. Avoid `---` and unexplained dash glyphs because they obscure whether a value is absent, inapplicable, or merely unreported.

### Table-1-Style Related Work Matrix

Use this compact single-column pattern for paper-positioning tables that compare prior work against the paper's claimed gap. Choose dimensions from the comparison and final readability.

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
\textbf{Ours} & \cmark & \cmark & \cmark & \cmark & \cmark \\
\bottomrule
\end{tabular}%
}
\end{table}
```

Do not choose dimensions solely to make the proposed method look good. The columns must follow from the paper's stated gap.

Do not fabricate prior-work rows, citation keys, or feature support. If source completion is already requested, use the writing skill's citation-integration reference internally to verify primary sources and complete the grounded table. For a closed corpus or inaccessible source, mark the gap and request only the source information that cannot be resolved within scope.

## Result Tables

Use result tables when exact comparisons matter.

Rules:

- Make metric direction clear with words or conventional arrows that render correctly.
- Keep direction notation consistent; define symbols locally when their meaning is not obvious.
- Bold best values or intended operating points, not every good-looking number.
- Use `\multicolumn` and `\cmidrule(lr){i-j}` for grouped metrics.
- Use a subtle `\rowcolor{TableHeaderShade}` header band when it improves hierarchy and survives grayscale rendering.
- Use `\multirow`, `\makecell`, or italic `\multicolumn` group labels when repeated row labels obscure the table's structure.
- Use `\rowcolor{blue!8}` or a local method macro sparingly for the proposed method.
- Use `threeparttable` when definitions or caveats would make the caption too long.
- Keep `threeparttable` only when the table has actual `tablenotes`; otherwise remove the empty wrapper.

## Notation And Dataset Tables

Use compact single-column tables when possible. Group symbols or dataset fields by topic.

Notation tables should define only symbols used later. Dataset tables should include units, counts, and filtering boundaries.

## Common Mistakes

- Do not use plain `\hline` grid tables by default.
- Do not color every result cell.
- Preserve marker meanings when changing symbols, colors, or layout.
- Do not merge multiple unrelated papers into one citation-only row; split rows unless the row is an explicitly named family and the marker values are conservative.
- Do not label or shade a cell as unique without a defined comparison corpus and row-wise evidence.
- Do not use color as the only carrier of a novelty or coverage-delta claim.
- Do not force a wide matrix into a single-column table with unreadable text.
- Do not write captions that merely restate the table label.
- Do not keep a wide table only because the first draft had many dimensions.
- Keep irrelevant workflow bookkeeping in artifact or review notes. Retain scientifically necessary implementation identifiers, renderer details and truthful synthetic-data disclosures in the caption or prose where they support interpretation; a venue mandate is not required for relevant scientific content.

# Dense Empirical Tables

Use this soft style profile for load-bearing empirical tables whose grouping and
scan path matter as much as individual values. It adapts the strongest reusable
patterns identified through reference-paper analysis without reproducing that
paper's text, values, or paper-specific choices.

## Contents

1. Selection
2. Visual Grammar
3. Grouped Empirical Matrix
4. Findings-at-a-Glance Two-Up Layout
5. Grouped Sample Or Validation Ledger
6. Caption And Notes
7. Do Not Generalize

## Selection

Use this profile for:

- multi-axis Related Work matrices;
- findings-at-a-glance or RQ-to-result indexes;
- regression or per-category result matrices;
- sample inventories and validation ledgers;
- wide tables with two or more genuine column groups.

Keep the compact default in `tables.md` when the table has one flat header, few
rows, or no meaningful group hierarchy.

For a Related Work table with eight or more capability dimensions grouped by
the paper's conceptual layers, continue with `layered-capability-matrix.md`.
That profile adds a comparison-corpus and uniqueness-evidence contract that a
generic dense empirical table does not need.

## Visual Grammar

Build hierarchy in this order:

1. `\toprule` and `\bottomrule` establish the outer frame.
2. A subtle header band separates labels from evidence.
3. `\multicolumn` plus `\cmidrule(lr)` names column groups.
4. `\midrule` separates semantic row blocks.
5. Bold marks only load-bearing results, totals, or the proposed row.
6. A light cell or row tint marks one argument-bearing distinction, never every
   positive value.

Use a muted sage-gray header that remains distinct in grayscale:

```latex
\definecolor{TableSage}{RGB}{165,165,141}
\colorlet{TableHeaderShade}{TableSage!22}
```

Use `\footnotesize` as the starting point. For genuinely wide matrices,
`\scriptsize` is an allowed adaptation after final-width inspection. Start with
`\tabcolsep` between `3.5pt` and `4.5pt` and `\arraystretch` between `1.05` and
`1.15`. Adjust content and column structure before shrinking further.

## Grouped Empirical Matrix

Use `@{}` to remove unused outer padding, right-align numeric columns, and add
at most one sparse vertical separator when it carries a real semantic boundary.

```latex
\begin{table*}[t]
\centering
\caption{Outcome rates by repository type and artifact class. Values are
percentages with 95\% confidence intervals.}
\label{tab:grouped-outcomes}
\footnotesize
\setlength{\tabcolsep}{4pt}
\renewcommand{\arraystretch}{1.08}
\begin{tabular}{@{}l rrrrr|rr@{}}
\toprule
& \multicolumn{5}{c}{\textbf{By repository type}}
& \multicolumn{2}{c}{\textbf{By artifact class}} \\
\cmidrule(lr){2-6}\cmidrule(lr){7-8}
\rowcolor{TableHeaderShade}
\textbf{Category} & \textbf{Train} & \textbf{Infer} & \textbf{Toolkit}
& \textbf{Eval} & \textbf{All} & \textbf{Model} & \textbf{Dataset} \\
\midrule
Exact     & 85 (27.2\%) & 54 (26.5\%) & 35 (16.8\%) & 14 (11.3\%) & 188 (22.2\%) & 119 & 69 \\
Card-only & 77 (24.7\%) & 32 (15.7\%) & 104 (50.0\%) & 39 (31.5\%) & 252 (29.7\%) & 111 & 141 \\
Code-only & 139 (44.6\%) & 47 (23.0\%) & 7 (3.4\%) & 1 (0.8\%) & 194 (22.9\%) & 188 & 6 \\
\bottomrule
\end{tabular}
\end{table*}
```

Remove the vertical separator when the `\cmidrule` grouping and whitespace are
already sufficient. Do not add separators between every column.

## Findings-at-a-Glance Two-Up Layout

Use a mirrored two-up layout only when both halves share exactly the same
schema and a one-column list would waste substantial space. Use explicit
inter-group whitespace rather than a central grid.

```latex
\begin{table*}[t]
\centering
\caption{Results at a glance. Each row states one conclusion and its primary
evidence anchor.}
\label{tab:findings-glance}
\footnotesize
\setlength{\tabcolsep}{4pt}
\begin{tabular}{@{}l l r l @{\hspace{1.25em}} l l r l@{}}
\toprule
\rowcolor{TableHeaderShade}
\textbf{RQ} & \textbf{Result} & \textbf{$n$} & \textbf{Value}
& \textbf{RQ} & \textbf{Result} & \textbf{$n$} & \textbf{Value} \\
\midrule
\multirow{2}{*}{RQ1} & Identity vocabulary differs & 803 & 12--25\,pp
& \multirow{2}{*}{RQ3} & Direction changes by type & 848 & 88 / 46\% \\
& Layer ratio inverts & 803 & 55 vs 43\%
& & Result survives sensitivity checks & 805 & 95.6\% \\
\bottomrule
\end{tabular}
\end{table*}
```

Do not use two-up layout when row heights differ substantially or when readers
must compare across the two halves.

## Grouped Sample Or Validation Ledger

Use italic full-width labels and `\midrule` to show a funnel or evidence tier.
Use a `p{}` column for the narrative purpose and `\makecell[l]` only when a row
group label genuinely needs multiple lines.

```latex
\begin{tabular}{@{}l c l p{0.46\textwidth}@{}}
\toprule
\rowcolor{TableHeaderShade}
\textbf{Sample} & \textbf{$n$} & \textbf{Drawn from} & \textbf{Purpose} \\
\midrule
\multicolumn{4}{@{}l}{\itshape Main corpus tiers} \\
Tier A & 2{,}000 & Candidate pool & Breadth estimates. \\
Tier B & 1{,}000 & Tier A & Main inferential analyses. \\
\midrule
\multicolumn{4}{@{}l}{\itshape Validation samples} \\
Tier C & 240 & Tier B outputs & Precision and residual-miss audit. \\
\bottomrule
\end{tabular}
```

## Caption And Notes

Make the first caption sentence identify the table's claim and population.
Define units, uncertainty, abbreviations, and marker semantics locally. Move
secondary sampling details or caveats into `tablenotes` when the caption begins
to dominate the page. Do not copy the reference manuscript's unusually long
captions as a default.

## Do Not Generalize

- Do not copy header direction arrows; follow the active table-direction rule.
- Do not use `---` for missingness; use explicit semantics from
  `TABLE.MISSING_VALUE_LABELS`.
- Do not repeat package imports or keep empty `threeparttable` wrappers.
- Do not use color without grayscale and accessibility checks.
- Do not use `table*`, `\scriptsize`, vertical separators, or `\resizebox`
  merely to preserve first-draft columns.
- Do not reproduce numeric values from this template without source evidence.

# Layered Capability Matrix

Use this optional profile for a load-bearing Related Work table whose capability
dimensions follow the paper's own conceptual layers. It is not the default for
ordinary comparison tables.

## Select This Profile

Select `table_profile: layered_capability_matrix` when all of these hold:

- the table carries a central positioning argument rather than a literature inventory;
- eight or more defensible dimensions remain after pruning;
- the dimensions form two to four named semantic groups;
- the grouping mirrors a model, lifecycle, architecture, or analytical split already explained in the manuscript;
- a double-column layout remains readable at final width.

Use the compact pattern in `tables.md` for three to five flat dimensions. Use
`dense-empirical-tables.md` for dense result or evidence tables that do not make
uniqueness claims about a literature corpus.

## Evidence Contract

- Define the comparison corpus and its exclusions in prose, the caption, or a table note.
- Assign each marker from source-backed row evidence. Do not infer coverage from a title, abstract keyword, or citation proximity alone.
- A named family row receives `\cmark` only when every included member supports the displayed capability. Use `\pmark` for mixed, incomplete, or qualified support.
- A proposed or this-work row must name a manuscript artifact and support every marker from that artifact.
- Shade or label a cell as a coverage delta only when the distinction is supported against every compared row.
- Unless the comparison corpus is exhaustive, say "absent from the compared rows" rather than universally "unique to this work."

The marker rules and the highlight rules are independent. Canonical markers may
be hard under the active house policy, while row or cell highlighting remains a
soft presentation choice.

## Layout Contract

- Start with `table*` at the top of a page and verify the venue's float rules.
- Use `\multicolumn` and `\cmidrule` for semantic column layers.
- Keep a `Type` column when it prevents unlike studies, tools, standards, or datasets from being read as interchangeable.
- Use a fixed-width, ragged-right first column and remove unused outer padding with `@{}`.
- Start at `\footnotesize`; use `\scriptsize` only after final-width QA shows that it remains comfortably readable.
- Start with `\tabcolsep` near 3.5--4.0 pt and `\arraystretch` near 1.05--1.10.
- Prefer whitespace and `\cmidrule` to vertical rules. Use at most one sparse vertical separator when it carries a necessary semantic boundary.
- Use `threeparttable` only when actual `tablenotes` are present.
- Keep the caption focused on the table's claim and scope. Put secondary abbreviations, corpus boundaries, and caveats in notes.
- Pair a meaning-bearing cell tint with a non-color cue such as `\dagger`.

## Generic LaTeX Skeleton

Adapt the group names, row labels, and markers only from manuscript evidence.
Do not copy paper-specific citations or capability assignments from a reference
table.

```latex
% Packages: array, booktabs, makecell, pifont, threeparttable, xcolor[table]
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\definecolor{okgreen}{RGB}{31,138,76}
\definecolor{nored}{RGB}{198,55,45}
\definecolor{okamber}{RGB}{214,148,18}
\newcommand{\cmark}{\textcolor{okgreen}{\ding{51}}}
\newcommand{\pmark}{\textcolor{okamber}{\footnotesize\ding{108}}}
\newcommand{\xmark}{\textcolor{nored}{\ding{55}}}
\newcommand{\deltacell}[1]{\cellcolor{okgreen!18}#1\textsuperscript{\(\dagger\)}}

\begin{table*}[t]
\centering
\begin{threeparttable}
\caption{Capability coverage across the defined comparison corpus.}
\label{tab:layered-capability}
\scriptsize
\setlength{\tabcolsep}{3.6pt}
\renewcommand{\arraystretch}{1.06}
\begin{tabular}{@{}L{0.22\textwidth}c cccc cc ccc@{}}
\toprule
& & \multicolumn{4}{c}{\textbf{Identity layer}}
& \multicolumn{2}{c}{\textbf{Execution context}}
& \multicolumn{3}{c}{\textbf{Method and impact}} \\
\cmidrule(lr){3-6}\cmidrule(lr){7-8}\cmidrule(lr){9-11}
\textbf{Compared work} & \textbf{Type}
& \textbf{Mod} & \textbf{Data} & \textbf{Svc} & \textbf{Card}
& \textbf{Run} & \textbf{WF}
& \makecell{\textbf{Empirical}\\\textbf{validation}}
& \makecell{\textbf{Tool}\\\textbf{benchmark}}
& \makecell{\textbf{Standards}\\\textbf{engagement}} \\
\midrule
Named family A~\cite{family-a} & Measure
& \cmark & \pmark & \xmark & \pmark & \xmark & \xmark
& \cmark & \xmark & \pmark \\
Named system B~\cite{system-b} & Tool
& \cmark & \cmark & \xmark & \pmark & \pmark & \xmark
& \pmark & \cmark & \xmark \\
\midrule
\textbf{This work} & Measure
& \cmark & \cmark & \deltacell{\cmark} & \cmark
& \deltacell{\cmark} & \cmark & \cmark & \cmark & \cmark \\
\bottomrule
\end{tabular}
\begin{tablenotes}[flushleft]\footnotesize
\item[\(\dagger\)] Coverage absent from the compared rows; the claim is bounded to the corpus defined in Section~\ref{sec:related}.
\end{tablenotes}
\end{threeparttable}
\end{table*}
```

## Final QA

Render at the actual `\textwidth` and confirm:

- group labels align with the correct column ranges;
- abbreviations are locally defined and do not force avoidable line breaks;
- every marker and delta cue has a source-evidence entry;
- the table remains intelligible in grayscale and without relying on tint;
- the caption, notes, and Related Work prose state the same comparison boundary;
- no claim expands from the compared corpus to all prior work.

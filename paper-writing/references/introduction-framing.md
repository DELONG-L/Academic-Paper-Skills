# Introduction Framing

Use this for Introduction rewrites, research gap extraction, and RQ-driven framing.

## Default Flow

Rebuild the Introduction as:

1. Problem context and motivation.
2. Explicit research gap.
3. Formal research questions when the paper is measurement, SoK, benchmark, or evaluation-driven.
4. Method, system, dataset, or benchmark overview.
5. Optional conceptual figure handoff when an overview figure would clarify the paper logic.
6. Short RQ-to-evidence mapping.
7. Empirical preview or answer preview.
8. Contributions.

## Gap Standard

The gap must be concrete. State what existing work can explain or support, then state what it cannot interpret, measure, enforce, or compare.

Weak:

```text
Existing methods have limitations.
```

Preferred:

```text
Existing evaluations report aggregate success rates, but they do not separate tool-selection failures from execution failures. This prevents a reviewer from identifying which interface assumption breaks under multi-step tasks.
```

## RQ Formatting

On first mention, write `research questions (RQs)`. After that, use `RQ` or `RQs`.

Use standalone lines when reviewer scanability matters:

```latex
This gap motivates three research questions (RQs).

\noindent\textbf{RQ1:} ...

\noindent\textbf{RQ2:} ...

\noindent\textbf{RQ3:} ...
```

Use bold RQ labels when it helps navigation.

## Response After RQs

Immediately after the RQs, explain the paper's response at a high level:

- what artifact the paper introduces
- what the comparison unit is
- what data, tasks, or dimensions organize the evidence
- what the reader should expect from the evaluation

Do not turn this paragraph into a mini-method section.

## RQ Mapping

Map each RQ to evidence sources in one compact paragraph. The mapping should say where the answer comes from, not restate the contributions.

Example:

```latex
RQ1 is answered by the corpus-level taxonomy in Section~\ref{sec:taxonomy}; RQ2 is addressed by the comparison matrix in Table~\ref{tab:comparison}; RQ3 is evaluated through the benchmark results in Section~\ref{sec:experiments}.
```

## Roadmaps

Delete low-value roadmaps when the Introduction already contains the gap, RQs, method overview, and contributions. Keep a roadmap only when it genuinely reduces navigation cost.

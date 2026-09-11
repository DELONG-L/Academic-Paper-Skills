# Introduction Framing

Use this for Introduction rewrites, research gap extraction, and RQ-driven framing.

## Default Flow

Choose the introduction’s content and order from the contribution and its evidence.
The following functions can help; combine or omit them when already clear:

1. Problem context and motivation.
2. Explicit research gap.
3. Explicit research questions when they help organize distinct evidence or comparisons. Use a claim-to-evidence narrative when RQ labels add no clarity.
4. Method, system, dataset, or benchmark overview.
5. Optional conceptual figure handoff when an overview figure would clarify the paper logic.
6. Short RQ-to-evidence mapping.
7. Empirical preview or answer preview.
8. Contributions.

## Gap Standard

Make the research need concrete. A supported gap may concern a missing comparison, unresolved assumption, replication need or opportunity for synthesis. Describe prior-work limitations only when relevant and evidenced; a deficit narrative is not required for every contribution.

Weak:

```text
Existing methods have limitations.
```

Preferred:

```text
Existing evaluations report aggregate success rates, but they do not separate tool-selection failures from execution failures. This prevents a reviewer from identifying which interface assumption breaks under multi-step tasks.
```

## RQ Formatting

Define `research questions (RQs)` when the abbreviation is unfamiliar or not already introduced in the relevant context.

Use standalone lines when reviewer scanability matters:

```latex
This gap motivates three research questions (RQs).

\noindent\textbf{RQ1:} ...

\noindent\textbf{RQ2:} ...

\noindent\textbf{RQ3:} ...
```

Use bold RQ labels when it helps navigation.

## Response After RQs

Explain the paper’s response near the RQs when it is not already clear:

- what new knowledge or artifact the paper contributes
- what the comparison unit is
- what data, tasks, or dimensions organize the evidence
- what the reader should expect from the evaluation

Do not turn this paragraph into a mini-method section.

## RQ Mapping

Make each RQ’s evidence source easy to locate, using a compact mapping when helpful. The mapping should say where the answer comes from, not restate the contributions.

Example:

```latex
RQ1 is answered by the corpus-level taxonomy in Section~\ref{sec:taxonomy}; RQ2 is addressed by the comparison matrix in Table~\ref{tab:comparison}; RQ3 is evaluated through the benchmark results in Section~\ref{sec:experiments}.
```

## Roadmaps

Delete low-value roadmaps when the Introduction already contains the gap, RQs, method overview, and contributions. Keep a roadmap only when it genuinely reduces navigation cost.

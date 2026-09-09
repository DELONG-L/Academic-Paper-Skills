# Related Work

Use this for Related Work and Background and Related Work prose.

## Core Rule

Related Work should expose the missing comparison axis rather than summarize papers one by one.

Use the comparison that helps explain the research question. A study of existing
phenomena can contribute evidence without claiming that every prior method fails.
When supported by the sources, explain how later work changes an assumption or
addresses an earlier limitation; do not invent a chronological progress story.
Include the strongest relevant comparators, not only convenient contrasts.

For systematic synthesis, record the corpus, search date/strategy, screening and
deduplication decisions, inclusion criteria, and classification rationale. Allow
mixed or uncertain categories and distinguish absent reporting from absent
capability. Derive any research agenda from observed gaps and specify what study
could address them; do not claim exhaustive coverage from a convenient sample.

The soft `RELATED.COMPARISON_REQUIRED` preference favors an axis-based
comparison-table plan when it improves comparison. Use explicit axis-based
prose when a table would duplicate the argument or imply unsupported
comparability. Record material adaptations without a waiver; explicit project
or sourced venue requirements still apply.

## Organization

Organize by intellectual axis:

- assumption boundary
- threat model
- interface layer
- evaluation unit
- dataset/workload scope
- lifecycle phase
- privacy/security guarantee
- capability dimension
- deployment constraint

Avoid chronological lists such as `A did X. B did Y. C proposed Z.`

Preferred paragraph pattern:

```latex
One line of work assumes [axis/value] and therefore evaluates [scope]~\cite{...}. This is effective for [setting], but it leaves [missing boundary] untested. A second line of work studies [adjacent axis]~\cite{...}; however, its comparison unit is [different unit]. Our work differs by treating [your axis] as the primary object of analysis.
```

## Conditional Comparison Table Plan

When a table is selected for its argumentative value or an explicit project or sourced venue instruction requires one, produce a plan with:

1. Table purpose: what gap or axis the table makes visible.
2. Row groups: paper families, systems, datasets, threat models, or approaches.
3. Columns: choose dimensions that carry fair, useful comparisons. Three to four is a compact starting point; use as many as the evidence and readability require. Consider `table_profile: layered_capability_matrix` when semantic grouping helps.
4. Placement preference: single-column by default after pruning; request `table*` only with an explicit reason.
5. Marker semantics: `\cmark` = full support, `\pmark` = partial support, `\xmark` = absent, only when marker symbols are needed.
6. Proposed row: the paper's method or artifact, only if the manuscript has one.
7. Compact caption draft. Do not include internal provenance notes, placeholder-citation status, or long marker notes.
8. In-text reference sentence.
9. Handoff note for Figures & Tables when final LaTeX rendering is needed.

For a proposed-row or cell-level coverage delta, define the compared corpus and
state only what its row evidence supports. Unless the corpus is exhaustive,
write "not covered by the compared work" or "absent from the compared rows"
rather than an unqualified "unique to this work."

Writing may include a compact LaTeX skeleton only when it helps explain content. Final layout, `resizebox`, color, grouped headers, and compile polishing belong to Figures & Tables.

## Table Content Standard

The table should carry an argument. Do not choose columns that all prior work shares, and do not choose dimensions that make only the proposed method look good unless those dimensions follow from the paper's stated gap.

Good columns:

- explicit threat model
- multi-stage workflow support
- artifact-level verification
- cross-dataset evaluation
- privacy boundary
- reproducibility hooks
- lifecycle coverage
- benchmark availability

Weak columns:

- `Uses AI`
- `Good performance`
- `Novel`
- generic `Scalable` without a measurable meaning

## Prose and Table Coupling

When a table is included, introduce it before or near the table reference:

```latex
Table~\ref{tab:related-comparison} summarizes this distinction. Prior work covers either [axis A] or [axis B], but rarely combines [your key dimensions]. This motivates our focus on [paper scope].
```

If the selected table still needs rendering within the current task, output:

```text
Figures & Tables handoff:
- Artifact: related-work comparison table
- Label: tab:related-comparison
- Rows:
- Columns:
- Placement preference: single-column unless the dimensions cannot be pruned further
- Table profile: compact | dense empirical | layered capability matrix
- Semantic column groups: <required for layered capability matrix>
- Comparison-corpus boundary:
- Marker semantics:
- Caption draft:
- In-text reference sentence:
```

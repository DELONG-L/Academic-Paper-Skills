# Related Work

Use this for Related Work and Background and Related Work prose.

## Core Rule

Related Work should expose the missing comparison axis rather than summarize papers one by one.

When `RELATED.COMPARISON_REQUIRED` is active, a full Related Work or Background
and Related Work draft must include an axis-based comparison-table plan unless
an authorized waiver or venue requirement applies. Otherwise propose a table
only when it materially improves comparison.

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

When the comparison requirement is active, produce a plan with:

1. Table purpose: what gap or axis the table makes visible.
2. Row groups: paper families, systems, datasets, threat models, or approaches.
3. Columns: normally 3 to 4 high-signal comparison dimensions; use 5 only if essential. Use 6 to 7 with a justified dense empirical design. When 8 or more dimensions remain after pruning and derive from the paper's conceptual layers, propose `table_profile: layered_capability_matrix` and name the 2--4 column groups.
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

The prose must introduce the table before or near the table reference:

```latex
Table~\ref{tab:related-comparison} summarizes this distinction. Prior work covers either [axis A] or [axis B], but rarely combines [your key dimensions]. This motivates our focus on [paper scope].
```

If the table is not rendered yet, output:

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

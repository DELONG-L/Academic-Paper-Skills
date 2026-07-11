# Section Drafting

Use this for drafting academic prose sections after loading `style-profile.md`.

## Abstract

Use a compact five-move structure:

1. Field pressure or task importance.
2. Specific gap, mismatch, or missing boundary.
3. Proposed artifact and mechanism.
4. Evidence scope and main result.
5. Bounded implication.

Avoid opening with generic statements such as `In this paper, we study ...` when a sharper pressure or mismatch is available.

## Introduction

Use `introduction-framing.md` when RQs or gap structure matter. Otherwise use:

1. Context and pressure.
2. Limitation in existing work.
3. Paper scope and key idea.
4. Evidence preview.
5. Contributions.

Contributions should name artifacts, not paper sections.

## Background

Background should prepare the reader for the paper's boundary. Include definitions, assumptions, notation, and prior mechanisms only when they are needed later.

Avoid turning Background into a paper-by-paper survey. Move comparison and positioning into Related Work.

## Method, System Model, and Approach

Use this order:

1. Define problem setting, actors, inputs, outputs, and threat/workload assumptions.
2. Introduce the main artifact or mechanism.
3. Explain the design choices and why they matter.
4. Give formalization, algorithm, or protocol only after the reader knows the object.
5. Close with implementation or complexity details when needed.

For equations, introduce the left-hand concept, show the equation, then explain the right-hand terms.

### Evidence roles

When the study combines substantive, validation, calibration, control,
case-study, or exploratory evidence, declare the role of every source before
using it. State which claim or RQ it supports and which extrapolation it does
not support. Do not silently use a validation-only or calibration-only sample
as substantive evidence.

Prefer a compact evidence-role ledger with these fields:

```text
source/tier | scale and selection | role | supports | does not support
```

Use prose for at most two simple roles. Keep load-bearing roles and boundaries
in the main text even if the exhaustive inventory moves to an appendix.

When a known measurement, extraction, missingness, or labeling error is
systematic, explain the mechanism and evidence for its direction, name the
affected metrics or claims, and state whether the result is conservative,
anti-conservative, or directionally indeterminate. Do not infer a direction
from intuition alone.

## Results Narrative

Writing handles interpretation, not artifact rendering.

Use the four-sentence result pattern from `style-profile.md`:

```latex
Table~\ref{tab:main} reports [metric] across [scope]. [Main observed value or ranking]. This indicates [bounded interpretation]. The result should be read within [setting or limitation].
```

If exact values should be in a table or figure, state the needed artifact and hand it off using `artifact-handoffs.md`.

Keep provenance and audit details out of the results narrative unless they are part of the scientific method. The paper body can state the evaluation scope and evidence boundary, but local CSV paths, plotting scripts, renderer names, and workflow-validation checks belong in artifact specs, README, or review notes.

For multiple dependent RQs, open Results with a compact dependency map: state
what each RQ establishes and why that evidence is needed by the next RQ. Keep
independent RQs parallel under the common contribution claim. Organize by
argumentative dependency rather than experiment execution chronology when the
two differ.

### RQ Closure

When `RESULTS.RQ_EXPLICIT_ANSWER` is active, close each load-bearing RQ result
block with exactly one explicit answer. Do not add one answer per
experiment subsection. The answer must derive only from evidence already shown
inside that RQ block and must not introduce a new claim, experiment, or result.

When `RESULTS.RQ_ANSWER_BOX` is enabled, prefer this soft presentation for a long, evidence-dense RQ block:

```latex
\takeawaybox[Answer to RQ1 (short thesis)]{[Direct scoped answer].
\textbf{[Load-bearing bounded implication].}}
```

Aim for two sentences and roughly 40--60 English words. Keep exact value lists
in the preceding table, figure, or prose. Under page pressure or venue/template
constraints, replace the visual box with a compact labeled paragraph:

```latex
\noindent\textbf{Answer to RQ1.} [Direct scoped answer and bounded implication.]
```

In either form, use one closure per RQ, not one per experiment; avoid new
citations, repeated findings-table text, decorative icons, bright fills, and
bolding the entire answer.

## Discussion and Limitations

A discussion should:

1. Restate the strongest bounded implication.
2. Explain why it matters for the target community.
3. Identify residual risks, missing validation, or deployment constraints.
4. Translate those limits into future work or usage boundaries.

Do not apologize for limitations. State the boundary and explain why the contribution still matters within it.

For each load-bearing threat or limitation, write:

```text
threat -> affected claim/RQ -> mitigation or no mitigation -> residual boundary
```

Add bias direction only when it is supported. Choose the grouping that matches
the paper: construct/internal/external/statistical for suitable measurement
studies; data/model/evaluation/deployment for ML; or threat-model/
implementation/measurement/generalization for security and systems. These are
options, not required headings.

## Conclusion

Keep the conclusion short and traditional. Do not introduce new claims, new citations, or new experimental numbers.

Preferred conclusion structure:

1. Restate the problem and artifact.
2. Summarize the main evidence.
3. Integrate the key limitation or scope boundary.
4. Close with a bounded implication or future direction.

Write these moves as one substantive paragraph. Do not create a standalone
top-level Limitations section. A separate Threats section does not replace the
conclusion-level boundary.

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

## Results Narrative

Writing handles interpretation, not artifact rendering.

Use the four-sentence result pattern from `style-profile.md`:

```latex
Table~\ref{tab:main} reports [metric] across [scope]. [Main observed value or ranking]. This indicates [bounded interpretation]. The result should be read within [setting or limitation].
```

If exact values should be in a table or figure, state the needed artifact and hand it off using `artifact-handoffs.md`.

Keep provenance and audit details out of the results narrative unless they are part of the scientific method. The paper body can state the evaluation scope and evidence boundary, but local CSV paths, plotting scripts, renderer names, and workflow-validation checks belong in artifact specs, README, or review notes.

## Discussion and Limitations

A discussion should:

1. Restate the strongest bounded implication.
2. Explain why it matters for the target community.
3. Identify residual risks, missing validation, or deployment constraints.
4. Translate those limits into future work or usage boundaries.

Do not apologize for limitations. State the boundary and explain why the contribution still matters within it.

## Conclusion

Keep the conclusion short and traditional. Do not introduce new claims, new citations, or new experimental numbers.

Preferred conclusion structure:

1. Restate the problem and artifact.
2. Summarize the main evidence.
3. Close with a bounded implication or future direction.

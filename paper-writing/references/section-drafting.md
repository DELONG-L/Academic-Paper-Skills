# Section Drafting

Use this for drafting academic prose sections after loading `style-profile.md`.

## Abstract

Use `ABSTRACT.FIVE_MOVES` as an adaptable content guide. The functions below do not prescribe five sentences or a fixed order; combine them as appropriate to the paper type and word limit without inventing evidence:

1. Field pressure or task importance.
2. Specific gap, mismatch, or missing boundary.
3. Proposed artifact and mechanism.
4. Evidence scope and main result.
5. Bounded implication.

Avoid opening with generic statements such as `In this paper, we study ...` when a sharper pressure or mismatch is available.

## Introduction

Use `introduction-framing.md` when RQs or gap structure matter. Otherwise use this starting organization and adapt it to the argument:

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

A useful starting order follows; adapt it to explanatory dependencies and the existing manuscript structure:

1. Define problem setting, actors, inputs, outputs, and threat/workload assumptions.
2. Introduce the main artifact or mechanism.
3. Explain the design choices and why they matter.
4. Give formalization, algorithm, or protocol only after the reader knows the object.
5. Close with implementation or complexity details when needed.

For equations, introduce the left-hand concept, show the equation, then explain the right-hand terms.

For a protocol or formal construction, make the primitives, parameters, actor
interfaces, and input/output conditions explicit when they define correctness.
Use the established notation in pseudocode; abstract standard operations while
retaining the novel steps and choices needed to reproduce the method. Avoid both
implementation transcripts and an algorithm so compressed that it hides the
actual mechanism. A fixed Construction heading or algorithm block is optional.

### Evidence roles

When the study combines substantive, validation, calibration, control,
case-study, or exploratory evidence, declare the role of every source before
using it. State which claim or RQ it supports; keep detailed non-support mappings
in the working evidence record when useful. Do not silently use a validation-only or calibration-only sample
as substantive evidence.

Prefer a compact evidence-role ledger with these fields:

```text
source/tier | scale and selection | role | supports | does not support
```

Use prose or a table according to complexity. Keep load-bearing roles and conditions
in the main text even if the exhaustive inventory moves to an appendix.

When a known measurement, extraction, missingness, or labeling error is
systematic, explain the mechanism and evidence for its direction, name the
affected metrics or claims, and state whether the result is conservative,
anti-conservative, or directionally indeterminate. Do not infer a direction
from intuition alone.

## Results Narrative

Writing handles interpretation, not artifact rendering.

Use the adaptable `RESULTS.FOUR_MOVE` guidance from `style-profile.md`. This example illustrates information relationships, not a required sentence count or fixed paragraph template:

```latex
Table~\ref{tab:main} reports [metric] across [scope]. [Main observed value or ranking].
```

Add interpretation when it contributes information. Include conditions needed
for the claim to hold and report material adverse findings, but do not append
what the result cannot prove in anticipation of an unasked objection.

If exact values should be in a table or figure, state the needed artifact and hand it off using `artifact-handoffs.md`.

Keep provenance and audit details out of the results narrative unless they are part of the scientific method. The paper body can state the evaluation scope and evidence boundary, but local CSV paths, plotting scripts, renderer names, and workflow-validation checks belong in artifact specs, README, or review notes.

For multiple dependent RQs, open Results with a compact dependency map: state
what each RQ establishes and why that evidence is needed by the next RQ. Keep
independent RQs parallel under the common contribution claim. Organize by
argumentative dependency rather than experiment execution chronology when the
two differ.

### RQ Closure

Under `RESULTS.CLAIM_MAPPING`, make each stated RQ answer clear and traceable
to the presented evidence, or explain why it remains unresolved. Avoid adding
new claims or results in a summary. Placement and sentence count are adaptable.

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

Avoid repetitive closures for individual experiments; avoid new
citations, repeated findings-table text, decorative icons, bright fills, and
bolding the entire answer.

## Discussion and Limitations

A discussion should:

1. Restate the strongest bounded implication.
2. Explain why it matters for the target community.
3. Identify residual risks, missing validation, or deployment constraints.
4. Translate those limits into future work or usage boundaries.

Discuss limitations that materially affect the stated contribution. Do not
enumerate every untested setting, apologize, or add a compensating defense of
the paper's value after each limitation.

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

Ground the conclusion in the body. Do not introduce previously unsupported
findings or guarantees. A concise synthesis or relevant citation is valid when
its premises and support are available; do not block it solely because a number
or reference appears here for the first time.

Preferred conclusion structure:

1. Restate the problem and artifact.
2. Summarize the main evidence.
3. Retain conditions needed to understand the conclusion; omit a separate disclaimer when its scope is already clear.
4. Close with a bounded implication or future direction.

Apply `STRUCT.CONCLUSION_SINGLE_PARAGRAPH` and
`STRUCT.CONCLUSION_INTEGRATES_LIMITATIONS` as soft preferences. Prefer one
concise paragraph when the findings and scope fit clearly; use multiple
paragraphs when distinct findings need separation. A standalone Limitations
or Threats section is valid when it supports the argument or is required by
the venue. Keep conclusion claims bounded without duplicating limitations
already clear from the wording. Never remove or hide a material limitation
to satisfy a paragraph-count or placement preference.

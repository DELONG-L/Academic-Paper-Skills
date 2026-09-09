# Style Profile

Use this as adaptable academic writing guidance. It preserves author preferences for precise, concrete prose without creating a separate style-readiness gate.

## Core Identity

The shared default is precise, scoped, and evidence-forward. Table, structure,
and typography guidance is adaptable to the argument and venue.

Default story arc:

1. Start from a field pressure, deployment change, measurement need, or threat-model mismatch.
2. Identify the missing boundary, assumption, interface, taxonomy, or evaluation axis.
3. Define the paper scope before making strong claims.
4. Introduce the new knowledge or artifact: finding, synthesis, system, dataset, taxonomy, mechanism, benchmark, or protocol.
5. Preview evidence with concrete scope: task count, dataset, attack variant, model family, benchmark, or corpus.
6. End with a bounded implication.

## Claim Ladder

Use strong claims only for directly supported contributions:

- `We introduce X` when X is concretely specified.
- `X achieves Y` when Y is measured in the stated setting.
- `X reduces/restores/preserves Y` when the metric directly supports that verb.

Use medium claims for interpretation:

- `The results indicate ...`
- `The comparison reveals ...`
- `This pattern is consistent with ...`

Use scoped framing claims:

- `We treat X as Y.`
- `We formulate X as a systems problem.`
- `We define the analysis boundary as ...`

Avoid unbounded claims such as `solves privacy`, `fully eliminates risk`, `proves generality`, `guarantees robustness`, or `is optimal`.

## Paragraph Pattern

A strong paragraph usually has one job:

1. Topic sentence naming the object or tension.
2. Mechanism or evidence.
3. Consequence for the paper's claim.
4. Scope qualifier or transition.

Use this pattern for related work, method prose, result interpretation, discussion, and limitations.

These are optional functions, not a paragraph template. Do not append a scope
disclaimer or recap when the paragraph is already clear and complete.

## Contribution Lists

Under the soft `CONTRIB.COUNT` preference, start with 3 to 5 distinct contributions; use fewer or more when that better represents the actual work. Never split or inflate contributions to meet a count.

Under `CONTRIB.CONCRETE`, name the new knowledge or artifact in each contribution, including measurement findings, replication, negative results, or systematic synthesis when supported. Avoid activity-only claims. Concrete artifacts may include:

- dataset or benchmark
- formalization, taxonomy, lifecycle, threat model, or specification
- mechanism, protocol, algorithm, or architecture
- evaluation with clear dimensions
- release, tool, or validation harness

Avoid contribution bullets that only say `we propose a method` or `we conduct experiments`.

## Boundary Setting

State supported findings directly, with relevant conditions in the claim itself.
Do not preemptively explain what an accurate result cannot prove merely because
a reader might ask for something broader. Correct an overclaim at its source;
do not surround it with disclaimers. Use `over-defensive-writing.md` for this
distinction, including when revising existing defensive prose.

Keep descriptive observations distinct from causal claims. Report material
limitations and actual adverse findings where they belong; specific reviewer
questions receive direct answers. Neither requires routine self-defense after
each finding.

Ordinary manuscript forms:

```latex
We evaluate [object] on [dataset or workload].
```

```latex
Under [relevant condition], [observed result].
```

```latex
[Method] assumes [condition needed for the stated property].
```

## Typography Discipline

Use ordinary roman text by default.

- Use `\textbf{}` sparingly for RQ labels, contribution cues, or short stage names when it improves scanability.
- Avoid frequent `\textit{}` for method names, variant names, field classes, and error types. Define the term once, then use ordinary text.
- Avoid `\texttt{}` in the main paper body except for code literals, commands, or file names that are genuinely part of the contribution. Internal artifact paths and scripts belong in audit files, not in paper prose.
- Do not use typography as a substitute for structure. If many words need emphasis, rewrite the paragraph.

## Paper Body Versus Audit Trail

Keep the paper-facing narrative separate from internal provenance records.

- Captions explain the artifact and its non-obvious encodings; discuss implications in the caption or surrounding prose where useful.
- Keep internal renderer choices, script paths and DPI checks in task records. A scientific appendix carries details relevant to reproducibility or interpretation, not routine workflow logs.
- Mention simulated or synthetic evidence where it changes the scientific claim, but avoid repeating internal provenance in every caption and paragraph.

## Result Prose

Under the soft `RESULTS.FOUR_MOVE` guidance, cover the information needed to interpret the result. These are functions, not a four-sentence requirement; combine or expand them as needed and avoid repeating a boundary already explicit nearby:

1. Scope: name the table/figure, setting, metric, or workload boundary.
2. Observation: state the main numerical or visual fact.
3. Interpretation: explain how it supports the claim.
4. Boundary, when needed: report a material trade-off or condition of the result;
   do not list unclaimed capabilities or untested settings as anticipatory defense.

Make the result's meaning clear where interpretation is needed. If the scoped
observation is already self-explanatory, do not add a formulaic final interpretation
or disclaimer solely to give the subsection a prescribed ending.

Under `RESULTS.CLAIM_MAPPING`, give clear evidence-grounded answers to the
stated RQs or identify unresolved questions. An answer box is an optional
presentation under `RESULTS.RQ_ANSWER_BOX`; no fixed placement or count is required.

# Style Profile

Use this as the default academic writing profile.

## Core Identity

The house style is precise, scoped, evidence-forward, and table-aware. It overrides generic ML writing style when the two conflict.

Default story arc:

1. Start from a field pressure, deployment change, measurement need, or threat-model mismatch.
2. Identify the missing boundary, assumption, interface, taxonomy, or evaluation axis.
3. Define the paper scope before making strong claims.
4. Introduce the artifact: system, dataset, taxonomy, mechanism, benchmark, or protocol.
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

## Contribution Lists

Use 3 to 5 contribution bullets unless the paper type genuinely requires more.

Each contribution must name an artifact:

- dataset or benchmark
- formalization, taxonomy, lifecycle, threat model, or specification
- mechanism, protocol, algorithm, or architecture
- evaluation with clear dimensions
- release, tool, or validation harness

Avoid contribution bullets that only say `we propose a method` or `we conduct experiments`.

## Boundary Setting

Make scope visible near the claim it supports:

- State what the paper excludes.
- Separate descriptive observations from causal claims.
- Say when a privacy or security property is not cryptographic.
- Treat limitations as part of the design contract.

Useful forms:

```latex
This paper focuses on [scoped subset] rather than [broader category].
```

```latex
The result should be read within [threat model/interface/dataset]; it does not imply [stronger property].
```

```latex
This limitation reflects the [budget/enforcement/data] boundary of the design.
```

## Typography Discipline

Use ordinary roman text by default.

- Use `\textbf{}` sparingly for RQ labels, contribution cues, or short stage names when it improves scanability.
- Avoid frequent `\textit{}` for method names, variant names, field classes, and error types. Define the term once, then use ordinary text.
- Avoid `\texttt{}` in the main paper body except for code literals, commands, or file names that are genuinely part of the contribution. Internal artifact paths and scripts belong in audit files, not in paper prose.
- Do not use typography as a substitute for structure. If many words need emphasis, rewrite the paragraph.

## Paper Body Versus Audit Trail

Keep the paper-facing narrative separate from internal provenance records.

- Paper captions and prose should state what the artifact shows and how it supports the claim.
- README files, review notes, artifact specs, and appendices can record renderer choices, script names, source paths, DPI checks, and placeholder status.
- Mention simulated or synthetic evidence where it changes the scientific claim, but avoid repeating internal provenance in every caption and paragraph.

## Result Prose

Use a four-sentence micro-structure:

1. Scope sentence: name the table/figure, setting, metric, or workload boundary.
2. Reading sentence: state the main numerical or visual fact.
3. Interpretation sentence: explain how it supports the claim.
4. Boundary sentence: mention the trade-off, exception, remaining risk, or scope limit.

Do not end an experiment subsection with a raw number. End with the bounded meaning of the result.

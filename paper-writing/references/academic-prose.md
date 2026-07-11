# Academic Prose

Use this for prose cleanup, AI-pattern removal, and section-level rewriting.

## Goal

Improve academic clarity, density, rhythm, and author voice. Do not optimize for
whether text appears human-generated, and do not make prose casual, chatty, or
personal merely to avoid an AI-associated pattern.

## Hard Boundaries

- Preserve scientific meaning. Do not change claim strength, causal status,
  evidence scope, limitations, terminology, citation attachment, quantitative
  facts, or the author's evidence-bound position to improve style.
- Do not use detector, perplexity, authenticity, or human-likeness scores as a
  compliance, readiness, or authorship gate. Do not rewrite to evade a detector
  or claim that prose is AI-authored from style alone.
- Keep intensifiers and attributions evidence-bound. Delete or ground
  `significantly`, `research shows`, `experts argue`, and equivalent language.
- When `PROSE.EM_DASH_FORBIDDEN` is active, use no em dash in paper prose,
  including Unicode em dash and LaTeX triple hyphen used as an em dash.
  Otherwise treat em-dash frequency as ordinary style judgment. Preserve
  hyphens, numeric ranges, mathematical minus signs, and non-prose table tokens.
- Keep technical terms stable. Do not introduce elegant variation that changes
  the identity of a method, variable, class, threat, or artifact.
- Keep author voice academic. Allow measured judgment tied to evidence or a
  design choice; do not inject casual humanizer language, decorative humor, or
  evidence-free opinion.

## Soft Diagnostics

Treat these as revision candidates, not automatic violations:

- Filler or inflated phrasing such as `It is important to note that`, `plays a
  crucial role`, `pivotal`, or `groundbreaking`.
- Promotional wording such as `vibrant`, `rich landscape`, `showcase`, or
  `breathtaking`.
- Decorative negative parallelism such as `not just X, but Y`.
- Sentence-final `highlighting`, `underscoring`, `ensuring`, or similar clauses
  that append weak analysis.
- Generic colon-led inline lists and repeated rule-of-three structures.
- Rhetorical self-answer forms such as `The result? X.` and dramatic standalone
  fragments.
- Three or more consecutive sentences or bullets with the same opening.
- Gerund-fragment litanies that lack a clear grammatical subject.
- Repeated conjunctive openers or metronomic sentence lengths.

Revise a soft pattern when it repeats, reduces precision, adds no information,
or conflicts with the target section's academic register. Record it as adapted
or skipped when preserving it is the better choice.

## Allowed Exceptions

- Preserve a negative contrast when ruling out the alternative is technically
  important.
- Preserve a participial clause when its grammatical attachment and analytic
  role are clear.
- Preserve parallel list structure when the items are genuinely parallel and
  the list improves auditability.
- Preserve deliberate terminology repetition when synonym substitution would
  blur identity.
- Allow stronger first-person positioning in Introduction, Discussion, and
  Limitations content when it expresses an evidence-bound choice or boundary.
- Allow neutral repetition in Methods and Results when consistency matters more
  than surface variation.

## Replacement Principles

- Replace inflated verbs with precise verbs: `shows`, `measures`, `defines`, `compares`, `evaluates`, `limits`.
- Replace vague attribution with a specific citation or delete it.
- Replace decorative negative parallelism with a direct claim; retain it when the excluded alternative matters.
- Replace decorative examples with scoped technical examples.
- Keep the same technical term throughout the paper.
- Prefer one clear transition over a stack of conjunctive phrases.

## Academic Rhythm

Use compact paragraphs with a clear job. Vary sentence length, but do not insert dramatic short sentences.

Keep paragraph structure direct:

- Start with the object, tension, or claim.
- Use ordinary subject-verb-object sentences when possible.
- Avoid long inline colon lists in prose. Use a sentence, a table, or a short displayed list when the distinction matters.
- Avoid repeated rule-of-three phrasing. Use the number of items the argument actually needs.
- Keep hedging attached to evidence limits, not to every verb.

Avoid:

```text
This is not just a benchmark. It is a new way to understand agents.
```

Prefer:

```text
The benchmark separates tool-selection errors from execution errors, which lets the evaluation identify where the agent interface fails.
```

## LaTeX Preservation

When editing LaTeX:

- Preserve citation commands, labels, references, equations, and macros.
- Do not rewrite display equations into `$$...$$` or `\[...\]`.
- Prefer `\begin{equation}...\end{equation}` for displayed equations that should be referenced.
- If a long descriptive token appears inside math mode, use `\text{...}` instead of treating it as a multi-letter variable.
- Explain displayed equations in nearby prose. Do not leave a formula as an isolated block.
- Do not remove `\textbf{RQ1:}` or contribution-list structure unless asked.
- Keep technical terms consistent even when repetition feels stylistically plain.

## Reference And Number Style

- Introduce abbreviations at first use and use them consistently afterward.
- Keep cross-references woven into sentences: `Table~\ref{...} reports ...`, not `See Table~\ref{...}` as a standalone crutch.
- Use numerals for measured values, dataset sizes, model counts, and section/page references. Spell out small non-technical counts only when it reads more naturally.
- Do not use Unicode arrows in paper prose or table headers. Use prose for directionality unless mathematical notation requires an arrow.

## Typography Cleanup

Flag and reduce unnecessary special fonts:

- Replace repeated `\textit{}` method, variant, class, or error names with ordinary roman text after first definition unless the venue or notation requires italics.
- Keep `\texttt{}` out of normal prose unless the literal command, path, or identifier is scientifically relevant. Move internal filenames, plotting scripts, and internal provenance details to README or review artifacts.
- Prefer `\textbf{}` only for short local anchors such as `RQ1:` or named stages in a dense method paragraph.
- Do not introduce small caps, underlining, or decorative emphasis.

## Audit-Prose Cleanup

If prose sounds like an internal validation report, move that content out of the paper body or rewrite it as a scoped scientific boundary. Paper-facing prose should not repeatedly mention renderer names, script names, local paths, DPI checks, or artifact-bundle mechanics.

## Cleanup Workflow

1. Preserve a source copy and identify the paragraph's job.
2. Mark hard-boundary risks separately from soft style candidates.
3. Delete filler and replace inflated phrases with precise language.
4. Restore direct subject-verb-object claims without forcing surface variation.
5. Add scope or evidence where a claim is too broad.
6. Compare source and revision for claim strength, causality, scope, values,
   citations, terminology, and caveats.
7. Report any soft pattern intentionally preserved and why.

Return rewritten text, not a long diagnosis, unless the user asks for explanation.

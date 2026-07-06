# Academic Prose

Use this for prose cleanup, AI-pattern removal, and section-level rewriting.

## Goal

Remove formulaic AI writing while preserving academic density, technical precision, and the house style. Do not make paper prose casual, chatty, or personal unless the target venue and section already support that voice.

## High-Priority Patterns To Remove

- Inflated significance: `plays a crucial role`, `serves as a testament`, `pivotal`, `groundbreaking`.
- Promotional wording: `vibrant`, `rich landscape`, `showcase`, `breathtaking`, `must-visit`.
- Vague attribution: `experts argue`, `observers note`, `industry reports suggest` without a specific source.
- Negative parallelism: `not just X, but Y`.
- Superficial `-ing` endings: `highlighting`, `underscoring`, `ensuring` when they append weak analysis.
- Overused em-dash parentheticals in prose.
- Colon-led inline lists with three or more generic items.
- Elegant variation that changes technical terms only to avoid repetition.
- Rhetorical self-answer forms such as `The result? X.`
- Standalone punchy fragments.
- Filler openers: `It is important to note that`, `In order to`, `Due to the fact that`, `This paper aims to`.
- Empty intensifiers: `very`, `significantly`, `substantially`, `remarkably`, unless backed by a reported value.
- Anaphora overuse: three or more consecutive sentences or bullets with the same opening phrase.
- Gerund-fragment litanies: sentence fragments that stack `enabling`, `ensuring`, `highlighting`, or `providing` without a clear subject.

## Replacement Principles

- Replace inflated verbs with precise verbs: `shows`, `measures`, `defines`, `compares`, `evaluates`, `limits`.
- Replace vague attribution with a specific citation or delete it.
- Replace negative parallelism with a direct claim.
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

1. Identify the paragraph's job.
2. Delete filler and inflated phrases.
3. Restore direct subject-verb-object claims.
4. Add scope or evidence where a claim is too broad.
5. Preserve house-style boundaries and claim calibration.

Return rewritten text, not a long diagnosis, unless the user asks for explanation.

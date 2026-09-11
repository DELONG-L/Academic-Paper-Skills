# Academic Prose

Use this for prose cleanup, AI-pattern removal, and section-level rewriting.

When the user explicitly asks to reduce AI-associated or formulaic writing
patterns, also load `prose-pattern-audit.md`. Use it to diagnose reader-facing
prose problems, never to infer authorship or optimize a detector score.

## Goal

Improve academic clarity, density, rhythm, and author voice. Do not optimize for
whether text appears human-generated, and do not make prose casual, chatty, or
personal merely to avoid an AI-associated pattern.

## Hard Boundaries

- Preserve scientific meaning during style edits. When correcting an overclaim
  or implementing an authorized substantive revision, make the supported change
  explicitly; do not preserve a known error merely to match the original wording.
  Retain quantitative facts, technical identity, citation support and material conditions.
- Do not use detector, perplexity, authenticity, or human-likeness scores as a
  compliance, readiness, or authorship gate. Do not rewrite to evade a detector
  or claim that prose is AI-authored from style alone.
- Keep intensifiers and attributions evidence-bound. Delete or ground
  `significantly`, `research shows`, `experts argue`, and equivalent language.
- Keep technical terms stable. Do not introduce elegant variation that changes
  the identity of a method, variable, class, threat, or artifact.
- Keep author voice academic. Allow measured judgment tied to evidence or a
  design choice; do not inject casual humanizer language, decorative humor, or
  evidence-free opinion.
- Do not add fabricated specifics, autobiographical detail, intentional errors,
  false starts, self-interruptions, emotional punctuation, or fractured
  discourse as evidence of human authorship.

## Editorial Diagnostics

Treat these as revision candidates, not automatic violations:

- Excessive punctuation or arrows. Retain useful em dashes and correctly rendered symbols; preserve ranges, minus signs, and technical notation.

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
- Repeated openings that make the passage monotonous or obscure the logical relation.
- Gerund-fragment litanies that lack a clear grammatical subject.
- Repeated conjunctive openers or metronomic sentence lengths.

Revise a pattern when it reduces precision, adds no information, or conflicts
with the target section's academic register. Repetition invites contextual review;
it does not establish a defect. Ordinary edits need no per-pattern compliance log.

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

Use paragraphs with a clear job. Judge sentence length by comprehension, grammatical attachment and the placement of conditions. Split an overloaded sentence when it improves clarity; retain a long sentence when splitting would detach a qualifier. Do not use a word-count warning or manufacture rhythmic variation.

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

- Preserve citation attachment, notation meaning and working cross-references.
  During prose-only polish, retain the relevant LaTeX structure. Authorized
  structural, citation or template edits may change commands and labels together
  with their dependent uses; verify the resulting source and affected render.
- Preserve existing display-math delimiters during prose-only edits. If equation formatting is in scope, choose syntax compatible with the document and venue; delimiter choice alone is not a style failure.
- Prefer `\begin{equation}...\end{equation}` for displayed equations that should be referenced.
- If a long descriptive token appears inside math mode, use `\text{...}` instead of treating it as a multi-letter variable.
- Explain displayed equations in nearby prose. Do not leave a formula as an isolated block.
- Preserve RQ anchors and contribution-list structure during local polish; adapt them when an authorized structural revision calls for it, keeping their information and references recoverable.
- Keep technical terms consistent even when repetition feels stylistically plain.

## Reference And Number Style

- Expand abbreviations when the intended reader needs the definition. Common
  disciplinary abbreviations or ones already defined in the relevant context
  can remain; review ambiguity rather than counting first-use expansions.
- Keep cross-references woven into sentences: `Table~\ref{...} reports ...`, not `See Table~\ref{...}` as a standalone crutch.
- Use numerals for measured values, dataset sizes, model counts, and section/page references. Spell out small non-technical counts only when it reads more naturally.
- Use prose or clear, correctly rendered arrows for directionality according to the context. Avoid decorative symbols; preserve useful technical notation when they help the reader.

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
2. Mark hard-boundary risks separately from editorial candidates.
3. Delete filler and replace inflated phrases with precise language.
4. Restore direct subject-verb-object claims without forcing surface variation.
5. Add scope or evidence where a claim is too broad.
   For repeated disclaimers or self-undermining, use `over-defensive-writing.md`;
   do not attach a new caveat to every sentence.
6. Compare source and revision for claim strength, causality, scope, values,
   citations, terminology, and caveats.
7. Explain substantive changes or unresolved facts; do not report every retained
   stylistic choice unless an audit was requested.

Return rewritten text, not a long diagnosis, unless the user asks for explanation.

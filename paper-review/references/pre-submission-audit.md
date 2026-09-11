# Pre-submission Audit

Use this reference for manuscript-quality review before submission or advisor review.

## Severity Levels

- `critical`: likely desk-reject, rejection, or major credibility risk. Fix before submission.
- `major`: likely to lower reviewer score. Strongly prioritize.
- `minor`: likely reviewer comment or polish issue. Fix after critical and major issues.
- `pass`: no meaningful issue found for that dimension.

Always include a one-line required action for `critical` and `major` findings.

## Audit Dimensions

### Logic and Argument

Check whether claims follow from premises and evidence.

For paragraph decisions or cross-section reorganization, use
`argument-structure.md` before line editing. Identify missing inferential links
as well as repeated information; a checklist of section presence is insufficient.

Flag:
- Causal claims without causal evidence.
- Universal claims that exceed the evaluated scope.
- Abstract, contributions, experiments, and conclusion making inconsistent claims.
- Section or RQ order with no recoverable argumentative dependency or common contribution spine.
- "Obviously", "clearly", or similar phrases where a proof or explanation is missing.

### Empirical Rigor

Check whether numbers and experimental claims are traceable.

Flag:
- Numbers inconsistent across abstract, tables, figures, and text.
- "Significant" or "substantial" claims without statistical or numerical support.
- Missing seed count, variance, confidence intervals, or significance tests when needed.
- Baselines with unequal data splits, tuning budgets, training budgets, or evaluation windows.
- Ablations that do not isolate the claimed mechanism.
- Validation, calibration, control, case-study, or exploratory evidence used as substantive support outside its declared role.
- Known systematic measurement or extraction errors without an evidence-backed bias direction, affected claim, or explicit statement that the direction is indeterminate.

### Threats and Limitations

Check every load-bearing threat or limitation as a claim-level argument.

Flag:
- Threats that do not identify the affected claim, RQ, metric, or inference.
- Mitigations named without evidence that they address the stated threat.
- Mitigations presented as eliminating risk when a residual boundary remains.
- A fixed validity taxonomy that hides domain-specific failure modes.
- Missing substantive limitations or unsupported conclusion claims remain evidence problems. Treat paragraph count and limitation placement as editorial choices unless an explicit project or sourced venue requirement applies.

### Contribution and Positioning

Check whether the novelty delta is explicit.

Flag:
- "We are first" or "novel" without a precise, cited comparison.
- Related Work that avoids the closest competitors.
- Contributions that restate implementation details rather than scientific advances.
- Scope too narrow for the stated claim.

Personal comparison preference:
- Use a comparison table when it clarifies the argument; sufficient axis-based prose is equally valid.

### Writing and Structure

Check whether readers can follow the manuscript accurately and efficiently.

Flag:
- Top-level section names that cause a concrete clarity problem or violate a sourced venue requirement; traditional names remain a editorial preference.
- Paragraphs whose function or relation to the argument is unclear; a fixed
  first-sentence formula is not required.
- Overclaims, promotional adjectives, filler, repeated formulaic structures, or other concrete prose defects.
- Excessive lists, bolding, or rhetorical self-answering.
- Excessive `\textit{}`, `\texttt{}`, small caps, underlining, or other special typography in normal prose.
- Paper-body text that reads like internal provenance, including local file paths, script names, renderer names, DPI checks, or artifact-bundle mechanics.
- Detector, perplexity, authenticity, or human-likeness scores used as evidence of manuscript quality, readiness, or authorship.
- Anti-AI rewrites that change claim strength, causality, scope, terminology, citation attachment, values, or required caveats.

Report the observed pattern and its effect on academic clarity. Do not label a
passage AI-generated or infer authorship from style alone.

For rewriting, hand off to `paper-writing`.

For substantial review, finish with `revision-closure.md`. Optional style findings
do not automatically trigger another full rewrite, and partial source coverage
does not justify a whole-manuscript judgment.

### Citations and Attribution

Use only citation and evidence sources declared by the user or project; local
`.bib`, manuscript text, and supplied notes are the default.

Flag:
- `\cite{}` keys missing from local `.bib`.
- Local `.bib` entries unused in the manuscript if cleanup is requested.
- Claims that need a citation but have no local support.
- Self-citation or code-link anonymity leaks in double-blind mode.

Use the source modes in `citation-and-evidence-policy.md`. Ordinary manuscript review stays local; a requested literature or citation check permits scoped public primary-source verification. Request manual input only when necessary support cannot be obtained within scope.

### Math and Notation

Flag:
- Symbols introduced without definitions.
- Same symbol used for multiple meanings.
- Different symbols used for the same quantity.
- Display equations not integrated into prose.
- Broken equation references or ambiguous numbering; an unreferenced numbered equation is not itself a scientific or formatting defect.

### Double-blind and Submission Compliance

Flag:
- Author names, acknowledgments, personal GitHub links, institutional paths, or PDF metadata.
- Non-anonymous supplementary links.
- Page limit, font, margin, or appendix violations when venue rules are provided.
- Missing Limitations, Ethics, Broader Impact, or Reproducibility sections when required by venue.

### Figures and Tables

Diagnose only; route creation/revision to `paper-figures-tables`.

Flag:
- Figure/table not referenced or interpreted.
- In-figure titles that duplicate the caption without helping navigation.
- Captions that omit information needed to interpret the artifact; a separate takeaway is unnecessary when the observation is clear or interpreted in the body.
- Captions containing irrelevant workflow bookkeeping. Retain scientifically necessary implementation identifiers, renderer details and synthetic-data disclosures; their presence alone is not a defect.
- Precise data figures not traceable to source data.
- Tables whose final rendering clips content or makes labels, values, or units unreadable.
- Related Work tables that are wider or denser than their argument requires.
- Related Work family rows whose full-support marker is not defensible for every named member; mixed support should be partial.
- Cells labeled or shaded as unique without a defined comparison corpus, row-wise evidence, or corpus-bounded wording.
- Meaning-bearing color highlights with no non-color cue or grayscale interpretation.
- Unclear optimization-direction markers; arrows are acceptable when their meaning is defined.
- Unnecessary Notes blocks, long marker explanations, or captions that carry too much table metadata.
- Conceptual figures with inconsistent terminology, ambiguous arrows, or unreadable labels.

### Reproducibility

Flag:
- Missing methodological details needed to reproduce or assess the stated claim. Check relevant data handling, parameters and computation; a public code-release commitment is not universal.
- Missing failure cases or limitations for a claim that reviewers can test.

## Output Template

```markdown
## Review Summary
<Concise assessment of the inspected scope; formal readiness only when assessed.>

## Policy Compliance
- Readiness: <READY | BLOCKED | NOT_EVALUATED> (omit for a local critique; only an actual compliance assessment can establish READY)
- Hard results: <PASS n | FAIL n | UNVERIFIED n | NOT_APPLICABLE n | WAIVED n>
- Context blockers: <none or list>

## Critical Findings
- [critical] <issue> [anchor]  
  Why it matters: <reviewer risk>.  
  Required action: <specific fix>.

## Major Findings
- [major] ...

## Minor Findings
- [minor] ...

## Handoffs
- paper-writing: <prose/structure changes>
- paper-figures-tables: <artifact changes>
- Unresolved citation support and required input: <if any>

## Fix Priority
1. <highest impact and feasible>
2. ...
```

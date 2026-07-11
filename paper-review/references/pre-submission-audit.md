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
- If the strict Conclusion rules are active, a missing Conclusion limitation or a Conclusion that violates the configured paragraph shape.

### Contribution and Positioning

Check whether the novelty delta is explicit.

Flag:
- "We are first" or "novel" without a precise, cited comparison.
- Related Work that avoids the closest competitors.
- Contributions that restate implementation details rather than scientific advances.
- Scope too narrow for the stated claim.

Conditional house rule:
- When `RELATED.COMPARISON_REQUIRED` is active, Related Work must include the axis-based comparison table unless an authorized waiver or venue requirement applies.

### Writing and Structure

Check whether the manuscript reads like a traditional academic paper.

Flag:
- Top-level section names that cause a concrete clarity problem; enforce traditional names as a rule only when `STRUCT.TRADITIONAL_HEADINGS` is active.
- Paragraphs without a clear topic sentence.
- Overclaims, promotional adjectives, filler, repeated formulaic structures, or other concrete prose defects.
- Excessive lists, bolding, or rhetorical self-answering.
- Excessive `\textit{}`, `\texttt{}`, small caps, underlining, or other special typography in normal prose.
- Paper-body text that reads like internal provenance, including local file paths, script names, renderer names, DPI checks, or artifact-bundle mechanics.
- Detector, perplexity, authenticity, or human-likeness scores used as evidence of manuscript quality, readiness, or authorship.
- Anti-AI rewrites that change claim strength, causality, scope, terminology, citation attachment, values, or required caveats.

Report the observed pattern and its effect on academic clarity. Do not label a
passage AI-generated or infer authorship from style alone.

For rewriting, hand off to `paper-writing`.

### Citations and Attribution

Use only citation and evidence sources declared by the user or project; local
`.bib`, manuscript text, and supplied notes are the default.

Flag:
- `\cite{}` keys missing from local `.bib`.
- Local `.bib` entries unused in the manuscript if cleanup is requested.
- Claims that need a citation but have no local support.
- Self-citation or code-link anonymity leaks in double-blind mode.

Do not search or verify references by default. Use the manual BibTeX update prompt from `citation-and-evidence-policy.md`.

### Math and Notation

Flag:
- Symbols introduced without definitions.
- Same symbol used for multiple meanings.
- Different symbols used for the same quantity.
- Display equations not integrated into prose.
- Equations numbered but never referenced, or referenced equations unnumbered.

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
- In-figure title text when `FIG.NO_IN_FIGURE_TITLE` is active or when it duplicates the caption.
- Captions that lack what/how/takeaway.
- Captions that read like internal audit logs or include renderer names, local data paths, plotting scripts, DPI checks, or internal-validation notes without a venue reason.
- Precise data figures not traceable to source data.
- Tables lacking `booktabs` when `TABLE.BOOKTABS_FINAL` is active.
- Tables that fail target-width readability; enforce the house `resizebox` pattern only when its rule is enabled.
- Related Work tables that are wider or denser than their argument requires; enforce house placement budgets only when enabled.
- Related Work family rows whose full-support marker is not defensible for every named member; mixed support should be partial.
- Cells labeled or shaded as unique without a defined comparison corpus, row-wise evidence, or corpus-bounded wording.
- Meaning-bearing color highlights with no non-color cue or grayscale interpretation.
- Up/down arrows in table headers when `TABLE.NO_DIRECTION_ARROWS` is enabled.
- Unnecessary Notes blocks, long marker explanations, or captions that carry too much table metadata.
- Conceptual figures that violate `FIG.CONCEPT_HOUSE_STYLE` when that optional rule is active.
- Generated conceptual figures whose non-mathematical text is not Times New Roman, whose mathematics does not use a dedicated math font, or whose font roles cannot be verified when `FIG.CONCEPT_TYPOGRAPHY` is active.
- Generated conceptual figures containing post-generation text, formula, arrow, icon, component, or boundary overlays, redraws, composites, or replacements when `FIG.CONCEPT_MODEL_NATIVE_OUTPUT` is active.

### Reproducibility

Flag:
- Missing dataset split, preprocessing, hyperparameters, hardware, random seeds, code release plan, or compute resources.
- Missing failure cases or limitations for a claim that reviewers can test.

## Output Template

```markdown
## Review Summary
<2-4 sentences on overall readiness.>

## Policy Compliance
- Readiness: <READY | BLOCKED | NOT_EVALUATED>
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
- Manual BibTeX update needed: <if any>

## Fix Priority
1. <highest impact and feasible>
2. ...
```

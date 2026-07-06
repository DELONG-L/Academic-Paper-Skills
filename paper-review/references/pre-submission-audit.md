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
- "Obviously", "clearly", or similar phrases where a proof or explanation is missing.

### Empirical Rigor

Check whether numbers and experimental claims are traceable.

Flag:
- Numbers inconsistent across abstract, tables, figures, and text.
- "Significant" or "substantial" claims without statistical or numerical support.
- Missing seed count, variance, confidence intervals, or significance tests when needed.
- Baselines with unequal data splits, tuning budgets, training budgets, or evaluation windows.
- Ablations that do not isolate the claimed mechanism.

### Contribution and Positioning

Check whether the novelty delta is explicit.

Flag:
- "We are first" or "novel" without a precise, cited comparison.
- Related Work that avoids the closest competitors.
- Contributions that restate implementation details rather than scientific advances.
- Scope too narrow for the stated claim.

Required house rule:
- Related Work must include the axis-based comparison table unless the user explicitly waived it or the venue forbids it.

### Writing and Structure

Check whether the manuscript reads like a traditional academic paper.

Flag:
- Top-level section names that are clever, marketing-like, or overly long.
- Paragraphs without a clear topic sentence.
- Overclaims, promotional adjectives, template phrases, and AI-smell.
- Excessive lists, bolding, or rhetorical self-answering.
- Excessive `\textit{}`, `\texttt{}`, small caps, underlining, or other special typography in normal prose.
- Paper-body text that reads like internal provenance, including local file paths, script names, renderer names, DPI checks, or artifact-bundle mechanics.

For rewriting, hand off to `paper-writing`.

### Citations and Attribution

Use only local `.bib`, local manuscript text, and user notes.

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
- In-figure title text.
- Captions that lack what/how/takeaway.
- Captions that read like internal audit logs or include renderer names, local data paths, plotting scripts, DPI checks, or internal-validation notes without a venue reason.
- Precise data figures not traceable to source data.
- Tables lacking `booktabs`.
- LaTeX tables not using `\resizebox` to align with target width unless natural width is already clean and better.
- Related Work or comparison tables that use `table*` or many dimensions when a pruned single-column table would carry the claim.
- Up/down arrows in table headers unless the user or venue explicitly wants that style.
- Unnecessary Notes blocks, long marker explanations, or captions that carry too much table metadata.
- Figure 1 or overview-style conceptual figures with gray, gradient, textured, or atmospheric backgrounds instead of a pure white page background.

### Reproducibility

Flag:
- Missing dataset split, preprocessing, hyperparameters, hardware, random seeds, code release plan, or compute resources.
- Missing failure cases or limitations for a claim that reviewers can test.

## Output Template

```markdown
## Review Summary
<2-4 sentences on overall readiness.>

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

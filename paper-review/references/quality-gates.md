# Quality Gates

Apply the relevant checks to the requested and actually inspected scope. These are review dimensions, not a mandatory global checklist for a paragraph or response edit. Formal readiness uses the separate policy assessment below.

## Provenance Gate

Every factual statement must map to one of:

- Manuscript source.
- Local PDF or LaTeX artifact.
- Local table, figure, data, or appendix.
- Verified source content within the authorized corpus; a `.bib` entry establishes identity, not specific claim support.
- Reviewer quote.
- User-confirmed fact or result.
- An explicit plan, labeled as a plan rather than evidence that work has been done.

For missing support, identify the affected claim and continue supported work. Retrieve sources when authorized; ask only for an essential input or decision unavailable within scope.

## Coverage Gate

- Claims within the requested scope have been checked against available evidence; a whole-manuscript judgment requires whole-manuscript coverage.
- Every supplied reviewer concern in scope is accounted for in the response or existing notes; an issue-board file is optional.
- Every issue is answered, deferred, or marked needs-user-input.
- No reviewer comment disappears because it is small.

## Evidence-Architecture Gate

- Every evidence source with a distinct role names the claims it may and may not support.
- Validation, calibration, controls, case studies, and exploratory analyses do not silently become substantive evidence.
- Every characterized systematic measurement error names affected claims and an evidence-backed bias direction or explicit indeterminacy.
- Dependent RQs follow a stated logical order; independent RQs remain parallel under a common contribution claim.
- Every load-bearing threat maps to an affected claim or RQ, a mitigation or explicit absence, and a residual boundary.

## Commitment Gate

- Every material promise is traceable to an existing edit or an authorized plan; reuse response notes rather than requiring a separate plan file.
- Every promised result is already provided or explicitly user-approved.
- Every promised citation has verified metadata and appropriate source support; explicitly mark inaccessible or out-of-scope sources as unresolved.
- No "we have done" statement is used unless the edit/result exists.

## Fairness Gate

- Findings avoid unfair rejection reasons from `reviewer-panel.md`.
- Author-side reviews distinguish substantive weaknesses from optional suggestions.
- Severity matches impact; do not inflate minor preferences.
- Positive contributions are acknowledged when real.

## Tone Gate

Flag and revise:

- Aggressive phrasing.
- Reviewer-blaming language.
- Excessive apology that weakens the paper.
- Vague "we will improve" promises.
- Overconfident words without support.

## Anti-AI Revision Gate

- Check concrete prose patterns rather than detector or human-likeness scores.
- Do not infer AI authorship from style alone or recommend detector-evasion edits.
- Compare source and revision for claim strength, causal status, evidence scope,
  terminology, citation attachment, quantitative facts, and caveats.
- Treat negative parallelism, sentence-final ing clauses, rhetorical
  self-answers, repeated openings, fragments, and list rhythm as soft diagnostics
  unless another hard integrity rule is independently violated.
- Preserve measured author judgment; reject casual humanizer language or humor
  that substitutes for analysis.

## Presentation Review

Treat presentation preferences as recommendations. Identify a hard failure only
when accuracy, evidence, final readability, or an explicit applicable requirement
is violated. Check:

- Related Work uses an evidence-supported table or axis-based prose appropriate to its argument; no preference waiver is required.
- Related Work and comparison tables are pruned to the smallest readable placement; wide `table*` usage has an explicit reason.
- Table headers make optimization direction clear; words or defined arrows are acceptable.
- Figure and table captions read like paper captions, not internal audit records.
- Conceptual figures use readable labels, accurate mathematical content, and clear visual grouping; background and font choices follow adaptable guidance or explicit venue requirements.
- Normal prose does not overuse `\textit{}`, `\texttt{}`, small caps, underlining, or other special typography.
- Top-level section headings are concise and informative; descriptive headings are valid.
- Figure/table issues are routed to `paper-figures-tables`.
- Prose drafting issues are routed to `paper-writing`.
- External literature-management workflows are not invoked unless explicitly requested.

## Submission-Compliance Gate

For an explicit compliance or submission-readiness judgment, run
`policy-compliance.md`. Ordinary critique or a scoped revision check need not run
a global audit. Do not return a submission-ready judgment unless the evidence-
backed assessor returns READY for the complete requested submission scope.
Convert every FAIL or UNVERIFIED hard blocker into a traceable issue card.

When venue rules are known, check:

- Page limit, reference/supplement counting rules, and appendix placement.
- Anonymous submission requirements: author names, acknowledgments, personal GitHub links, institution paths, PDF metadata, and non-anonymous URLs.
- Required sections such as Limitations, Ethics, Broader Impact, Reproducibility, Checklist, or LLM-use disclosure.
- Section numbering consistency with the venue template.
- Camera-ready-only metadata is not present in anonymous review drafts.

If venue rules are not supplied, flag these as `unknown` rather than inventing requirements.

## Citation Gate

Check local hygiene and content support within the authorized source mode:

- All `\cite{}` keys exist in local `.bib`.
- Duplicate BibTeX keys are absent when `.bib` files are available.
- First-work, novelty, and closest-prior-work claims are bounded by the sources actually examined; use public primary-source checking when that task is requested and mark remaining coverage gaps.
- Resolve new citation needs within the authorized source mode; request manual input only for gaps that cannot be resolved within scope.
- No automatic external verification is claimed.

## Reproducibility Gate

Check whether the manuscript reports the evidence needed for its claims:

- Dataset/source boundary, splits, preprocessing, and filtering.
- Random seeds or repeated-run counts when variability is reported.
- Hardware or compute resources when runtime, scale, or reproducibility claims depend on them.
- Baseline tuning/evaluation parity.
- Run count, aggregation unit and appropriate uncertainty when the available design and claim require it; missing repeats do not authorize fabricated variation or automatic new runs.
- Ablations isolate the claimed mechanism.

## Final Output Gate

Before finalizing, include material unresolved issues and necessary user inputs if any; do not invent risks or empty blocker sections.
- Exact over-limit status if a rebuttal limit exists.
- Complete authorized writing, figures/tables, and citation work through internal skill routing; list only genuine remaining dependencies or decisions.

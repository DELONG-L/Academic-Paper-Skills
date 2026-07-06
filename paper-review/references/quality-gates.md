# Quality Gates

Run these gates before returning a review report, issue board, rebuttal draft, or revision verification.

## Provenance Gate

Every factual statement must map to one of:

- Manuscript source.
- Local PDF or LaTeX artifact.
- Local table, figure, data, or appendix.
- Local `.bib`.
- Reviewer quote.
- User-confirmed fact or result.
- Explicit future-work or limitation statement.

If no source exists, mark it as blocked or ask the user.

## Coverage Gate

- Every major manuscript claim has been checked against evidence.
- Every external reviewer concern appears in the issue board.
- Every issue is answered, deferred, or marked needs-user-input.
- No reviewer comment disappears because it is small.

## Commitment Gate

- Every promise in a rebuttal appears in the revision plan.
- Every promised result is already provided or explicitly user-approved.
- Every promised citation has local BibTeX or a manual BibTeX update request.
- No "we have done" statement is used unless the edit/result exists.

## Fairness Gate

- Findings avoid unfair rejection reasons from `reviewer-panel.md`.
- Formal reviews distinguish rejection-relevant weaknesses from optional suggestions.
- Severity matches impact; do not inflate minor preferences.
- Positive contributions are acknowledged when real.

## Tone Gate

Flag and revise:

- Aggressive phrasing.
- Reviewer-blaming language.
- Excessive apology that weakens the paper.
- Vague "we will improve" promises.
- Overconfident words without support.

## House-Style Gate

Check:

- Related Work includes the required comparison table or a documented waiver.
- Related Work and comparison tables are pruned to the smallest readable placement; wide `table*` usage has an explicit reason.
- Table headers avoid ML-style up/down arrows unless explicitly requested.
- Figure and table captions read like paper captions, not internal audit records.
- Figure 1 and overview-style conceptual figures use pure white backgrounds unless the manuscript gives a reason otherwise.
- Normal prose does not overuse `\textit{}`, `\texttt{}`, small caps, underlining, or other special typography.
- Top-level section headings are traditional and concise.
- Figure/table issues are routed to `paper-figures-tables`.
- Prose drafting issues are routed to `paper-writing`.
- External literature-management workflows are not invoked unless explicitly requested.

## Submission-Compliance Gate

When venue rules are known, check:

- Page limit, reference/supplement counting rules, and appendix placement.
- Anonymous submission requirements: author names, acknowledgments, personal GitHub links, institution paths, PDF metadata, and non-anonymous URLs.
- Required sections such as Limitations, Ethics, Broader Impact, Reproducibility, Checklist, or LLM-use disclosure.
- Section numbering consistency with the venue template.
- Camera-ready-only metadata is not present in anonymous review drafts.

If venue rules are not supplied, flag these as `unknown` rather than inventing requirements.

## Citation Gate

Check local hygiene only:

- All `\cite{}` keys exist in local `.bib`.
- Duplicate BibTeX keys are absent when `.bib` files are available.
- First-work, novelty, and closest-prior-work claims have local citation support or a manual update request.
- New citation needs are emitted as manual BibTeX update prompts.
- No automatic external verification is claimed.

## Reproducibility Gate

Check whether the manuscript reports the evidence needed for its claims:

- Dataset/source boundary, splits, preprocessing, and filtering.
- Random seeds or repeated-run counts when variability is reported.
- Hardware or compute resources when runtime, scale, or reproducibility claims depend on them.
- Baseline tuning/evaluation parity.
- Error bars or confidence intervals when averaged results are used.
- Ablations isolate the claimed mechanism.

## Final Output Gate

Before finalizing, include:

- Residual risks.
- User-input blockers.
- Exact over-limit status if a rebuttal limit exists.
- Handoffs to writing, figures/tables, experiments, or manual BibTeX.

# Review Modes

Use the mode that matches the user's intent and established role. Do not infer a formal reviewer assignment or manuscript ownership from the word "review" alone. For a general critique, work within the supplied material and requested scope without a submission-readiness claim. If handling a confidential assigned submission depends on the user's role, clarify that role before inspection; formal assigned review is outside this skill and awaits a separate workflow.

Set the machine-readable `task_mode` as follows. These values are controlled;
unknown values are rejected rather than silently disabling policy.

| Human workflow | Canonical `task_mode` |
|---|---|
| Pre-submission audit | `self_review` |
| Reviewer panel for own draft | `self_review` |
| External review analysis | `external_review_analysis` |
| Rebuttal strategy/drafting | `rebuttal` |
| Revision verification | `revision_verification` |
| Paragraph/argument structure review | `architecture_review` |
| Explicit manuscript-only reader test | `cold_reader` |

`pre_submission_audit` and `reviewer_panel` are accepted aliases for
`self_review`. Detector-specific review must use `detector_review` or
`authorship_review`; ordinary self-review does not activate a detector-related
workflow gate.

## Mode A: Pre-submission Audit

For structural problems, use `argument-structure.md`. When formal policy context
is requested, the existing `architecture_review` mode activates its structural
preservation checks; ordinary local structure edits need no context file.

Goal: find evidence, argument, and presentation problems in the requested manuscript scope. A general self-review is not automatically a formal compliance or readiness assessment.

Inputs:
- Manuscript source or PDF.
- Venue and page limit if available.
- Local `.bib`, result tables, figures, and appendix if available.

Output:
- Severity-ranked findings.
- Prioritized fix list.
- Handoffs to `paper-writing` and `paper-figures-tables`.
- Citation verification or completion when already requested; manual-source requests only for remaining inaccessible or closed-corpus gaps.

## Mode B: Reviewer Panel for Own Draft

Goal: simulate likely reviewer objections and produce a fix list.

Use distinct analytic perspectives; additional agents require separate authorization:
- Champion: strongest fair case for the paper.
- Skeptic: soundness, baselines, ablations, statistics, reproducibility.
- Novelty/AC: positioning, contribution delta, related work, likely decision factors.

Output:
- Simulated reviews with evidence anchors.
- Consensus and split risks.
- Indicative scores or outcome only when requested, clearly marked as simulation.
- Fix list sorted by impact and cost.

## Mode C: External Review Analysis

Goal: convert raw reviewer comments into a structured issue board.

Output:
- Atomic issue cards.
- Reviewer quote anchors.
- Merged duplicates.
- Priority and response mode per issue.
- Evidence gaps and user-input blockers.

## Mode D: Rebuttal Strategy and Drafting

Goal: produce a grounded, concise author response.

Output:
- Strategy plan.
- Rebuttal draft in venue shape: single document or per-reviewer thread.
- Exact limits if provided.
- Revision plan covering every promised manuscript edit.

## Mode E: Revision Verification

Goal: verify that the rebuttal and revised manuscript match.

Output:
- Completed, pending, deferred, and unsupported promises.
- Claims that need user-confirmed evidence.
- Local `.bib` and citation hygiene notes.
- Remaining risks for resubmission or camera-ready.

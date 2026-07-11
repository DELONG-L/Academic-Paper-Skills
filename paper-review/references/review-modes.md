# Review Modes

Use the mode that matches the user's intent. If the user gives only a paper and says "review", default to pre-submission audit for the user's own paper unless they say they are reviewing someone else's submission.

Set the machine-readable `task_mode` as follows. These values are controlled;
unknown values are rejected rather than silently disabling policy.

| Human workflow | Canonical `task_mode` |
|---|---|
| Pre-submission audit | `self_review` |
| Reviewer panel for own draft | `self_review` |
| Formal review of another paper | `formal_review` |
| External review analysis | `external_review_analysis` |
| Rebuttal strategy/drafting | `rebuttal` |
| Revision verification | `revision_verification` |

`pre_submission_audit` and `reviewer_panel` are accepted aliases for
`self_review`. Detector-specific review must use `detector_review` or
`authorship_review`; ordinary self-review does not activate a detector-related
workflow gate.

## Mode A: Pre-submission Audit

Goal: find rejection risks before advisor review, collaborator review, or submission.

Inputs:
- Manuscript source or PDF.
- Venue and page limit if available.
- Local `.bib`, result tables, figures, and appendix if available.

Output:
- Severity-ranked findings.
- Prioritized fix list.
- Handoffs to `paper-writing` and `paper-figures-tables`.
- Manual BibTeX update prompts when citation support is locally missing.

## Mode B: Reviewer Panel for Own Draft

Goal: simulate likely reviewer objections and produce a fix list.

Run distinct perspectives:
- Champion: strongest fair case for the paper.
- Skeptic: soundness, baselines, ablations, statistics, reproducibility.
- Novelty/AC: positioning, contribution delta, related work, likely decision factors.

Output:
- Simulated reviews with evidence anchors.
- Consensus and split risks.
- Predicted outcome marked as simulation, never as a promise.
- Fix list sorted by impact and cost.

## Mode C: Formal Review of Someone Else's Paper

Goal: draft a fair, venue-shaped review for user sign-off.

Rules:
- Keep a professional, neutral, constructive tone.
- Anchor every strength and weakness to the paper.
- Do not use unfair rejection reasons from the fairness firewall.
- Remind the user that final scores and submission responsibility are theirs.

Output:
- Paper summary.
- Strengths.
- Weaknesses with severity and anchors.
- Questions for authors.
- Suggestions that are not rejection grounds.
- Venue score recommendation when requested.

## Mode D: External Review Analysis

Goal: convert raw reviewer comments into a structured issue board.

Output:
- Atomic issue cards.
- Reviewer quote anchors.
- Merged duplicates.
- Priority and response mode per issue.
- Evidence gaps and user-input blockers.

## Mode E: Rebuttal Strategy and Drafting

Goal: produce a grounded, concise author response.

Output:
- Strategy plan.
- Rebuttal draft in venue shape: single document or per-reviewer thread.
- Exact limits if provided.
- Revision plan covering every promised manuscript edit.

## Mode F: Revision Verification

Goal: verify that the rebuttal and revised manuscript match.

Output:
- Completed, pending, deferred, and unsupported promises.
- Claims that need user-confirmed evidence.
- Local `.bib` and citation hygiene notes.
- Remaining risks for resubmission or camera-ready.

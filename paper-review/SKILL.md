---
name: paper-review
description: Academic paper review, self-review, red-team review, reviewer-response, rebuttal planning, rebuttal drafting, and revision verification. Use when Codex needs to audit a manuscript before submission, simulate reviewers, prepare a prioritized fix list, analyze external reviewer comments, draft or check author responses, verify promised revisions, check submission readiness, or review paper quality without entering any external literature-management workflow.
---

# Paper Review

## Overview

Use this skill to evaluate a paper as a reviewer would: identify evidence-bound weaknesses, rank fixes by risk and cost, prepare grounded rebuttals, and verify that promised revisions are actually traceable. Keep this skill separate from `paper-writing`, `paper-figures-tables`, and any external literature-management workflow.

## Boundaries

- Do not invoke external literature-management tools or separate review/rebuttal builders by default. Use them only when the user explicitly asks for that separate workflow.
- Do not perform automatic citation retrieval or reference verification. Local `.bib`, local manuscript text, and user-provided notes are the source of truth.
- Do not invent experiments, numbers, p-values, baselines, reviewer comments, citations, links, or revision status.
- Do not rewrite prose as the primary deliverable. Route substantial prose drafting to `paper-writing`.
- Do not redraw or typeset figures/tables as the primary deliverable. Route artifact creation or revision to `paper-figures-tables`.
- Do not submit reviews, rebuttals, or OpenReview/CMT/HotCRP responses for the user. Produce drafts and checks for user sign-off.

## Source Priority

When reviewing or drafting responses, use evidence in this order:

1. User-confirmed facts, experimental results, revision decisions, venue limits, and author intent.
2. The current manuscript, local LaTeX/PDF/source files, local tables/figures, and local `.bib`.
3. Reviewer comments, official venue instructions provided by the user, and local rebuttal drafts.
4. Skill references listed below.

If a likely needed citation is missing locally, use the manual handoff format in `references/citation-and-evidence-policy.md`. Do not search, fetch, or validate references unless the user explicitly asks for that separate task.

## Mode Routing

Read `references/review-modes.md` for mode details, then load only the references needed for the request.

- **Pre-submission audit**: read `pre-submission-audit.md`, `quality-gates.md`, and `citation-and-evidence-policy.md`.
- **Red-team my draft / simulate reviewers**: read `reviewer-panel.md`, `issue-board.md`, and `quality-gates.md`.
- **Formal review of someone else's paper**: read `reviewer-panel.md`, `pre-submission-audit.md`, and `quality-gates.md`; keep tone fair and evidence-bound.
- **Analyze external reviews**: read `issue-board.md`, `rebuttal-strategy.md`, and `citation-and-evidence-policy.md`.
- **Draft or polish rebuttal**: read `rebuttal-strategy.md`, `rebuttal-drafting.md`, `revision-plan.md`, and `quality-gates.md`.
- **Verify revised manuscript after rebuttal**: read `revision-plan.md`, `quality-gates.md`, and the relevant writing or figure/table handoff rules.

## Default Workflow

1. Identify the mode, manuscript stage, venue if known, deadline pressure, and available inputs.
2. Establish an evidence map: manuscript locations, local results, local `.bib`, reviewer comments, user-confirmed constraints.
3. Atomize findings into issue cards instead of free-form critique.
4. Classify each issue by severity, evidence anchor, affected claim, and required action.
5. Apply quality gates: provenance, coverage, commitment, tone, fairness, citation policy, and handoff routing.
6. Return the most actionable artifact for the mode: audit report, reviewer-panel report, issue board, rebuttal strategy, rebuttal draft, or revision checklist.

## Required Review Discipline

- Every criticism must point to a manuscript location, reviewer quote, local artifact, or `MISSING` marker.
- Separate `substance` problems from `misread-risk` problems. Do not recommend new experiments for wording problems that can be fixed by narrowing or clarifying a claim.
- Treat Related Work as a high-risk area. Check whether the paper includes the house-style comparison table required by `paper-writing` and `paper-figures-tables`, unless the user explicitly waived it or the venue forbids it.
- Top-level section headings must remain traditional and concise. Flag marketing-style or overly clever section names.
- For figures and tables, diagnose the issue and hand off to `paper-figures-tables` when creation, redesign, or LaTeX table work is needed.
- For prose rewrites, diagnose the issue and hand off to `paper-writing` when drafting is the main task.
- For rebuttals, answer every reviewer concern or explicitly mark it as deferred with a reason.

## Scripts

- Use `scripts/count_rebuttal_limit.py` when a rebuttal, author response, or per-reviewer reply has a character or word limit.

## Reference Index

- `references/review-modes.md`: mode selection and output shapes.
- `references/pre-submission-audit.md`: manuscript audit dimensions and severity levels.
- `references/reviewer-panel.md`: reviewer personas, fairness firewall, and formal-review mode.
- `references/issue-board.md`: atomic issue schema for audits and external reviews.
- `references/rebuttal-strategy.md`: strategy selection, reviewer intent, and evidence planning.
- `references/rebuttal-drafting.md`: author-response structure, tone, and length discipline.
- `references/revision-plan.md`: mapping rebuttal promises to manuscript edits.
- `references/quality-gates.md`: final gates before returning a review or rebuttal artifact.
- `references/citation-and-evidence-policy.md`: local-only citation and evidence policy.

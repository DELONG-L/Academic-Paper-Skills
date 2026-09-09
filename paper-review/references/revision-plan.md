# Revision Plan

Use this reference for rebuttal follow-through and post-rebuttal manuscript verification.

## Purpose

The revision plan is the source of truth for every manuscript change promised or implied by a rebuttal. It prevents the common failure where the response says "we will add X" but the revised paper never receives X.

## Plan Schema

```markdown
# Revision Plan

## Overall Checklist
- [ ] (<issue_id>) <atomic manuscript edit> - location: <section/table/figure/appendix>; commitment: <already-done|approved-for-rebuttal|future-work-only>; owner: <user|Codex|experiment>; status: <pending|partial|done|blocked|deferred>.

## Grouped by Location
### <Section or artifact>
- <items>

## Grouped by Severity
### Critical
- <items>

## Commitment Summary
- already-done: <n>
- approved-for-rebuttal: <n>
- future-work-only: <n>
- blocked: <n>

## Out-of-Scope Log
- (<issue_id>) <concern> - reason: <why no manuscript edit>.
```

## Rules

- One checklist item equals one paper edit.
- Every checklist item maps to at least one issue id.
- Every rebuttal promise maps to a checklist item.
- Every checklist item must have a status.
- Do not add a promised experiment or result unless the user approved it.
- Add citations only from existing supported sources or primary-source verification within the authorized task. Update the bibliography when requested, preserve existing keys, and record unresolved support instead of promising it.
- Update the same plan in place for follow-up rounds; do not regenerate from scratch if a plan already exists.

## Verification Pass

When checking a revised manuscript:

1. Read the rebuttal draft and revision plan.
2. For each promise, locate the actual manuscript edit.
3. Mark one of:
   - `done`: edit exists and matches the promise.
   - `partial`: edit exists but is weaker, unclear, or in the wrong location.
   - `blocked`: missing user result, missing BibTeX, or unresolved decision.
   - `pending`: no matching edit found.
   - `deferred`: the response explicitly postpones the item and gives the reason.
4. Report any contradictions between rebuttal and manuscript.

## Handoff Rules

- Prose edits: route to `paper-writing`.
- Figure/table edits: route to `paper-figures-tables`.
- Citation additions: use the already authorized source and editing scope in
  `../../paper-writing/references/citation-integration.md`; request manual input
  only for a required inaccessible source or explicit manual-edit constraint.
- Experiment results: inspect available actual numbers/logs/source tables; a
  writing promise does not authorize new experiments. Identify missing evidence
  and continue supported revisions.

## Round and Dependency Tracking

For multi-round responses, keep the comment/round identity and previous decision
with the current verification record. Refresh section/line references after
reorganization. When a result or claim changes, check dependent response text,
abstract, conclusion, captions and supplement. Do not silently mark a previously
completed promise done if its supporting source has changed.

Finish substantial revision with `revision-closure.md`, distinguishing remaining
scientific work from local formatting or optional style advice.

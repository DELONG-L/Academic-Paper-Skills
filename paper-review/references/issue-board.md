# Issue Board

Use issue cards for both manuscript audits and external review analysis. The goal is to prevent vague critique and ensure every concern is traceable.

## Atomicity

Split issues when they require different evidence or different actions:

- Baseline X missing and baseline Y missing are separate if they require different experiments.
- Novelty concern and clarity concern are separate.
- "Slow and less accurate" is two issues: efficiency and performance.

Merge issues when they share the same core objection and same response:

- Multiple reviewers ask why the loss term is needed.
- Multiple reviewers ask for the same missing citation.
- Multiple reviewers are confused by the same method section.

## Issue Schema

```markdown
### <issue_id>: <short title>

- Source: <manuscript audit | R1 | R2 | R3 | AC | user>
- Raw anchor: "<reviewer quote or manuscript quote>" | <section/table/figure> | MISSING
- Paper hook: <section/table/figure/equation/appendix/global>
- Policy rule: <active hard-rule ID | none>
- Compliance status: <FAIL | UNVERIFIED | none>
- Type: <logic | novelty | related-work | empirical-support | baseline | ablation | statistics | theory | clarity | reproducibility | ethics | formatting | citation | figure-table | other>
- Severity: <critical | major | minor>
- Nature: <substance | misread-risk | polish>
- Response mode: <accept | clarify | defend | experiment | narrow-concession | scope-boundary | manual-bibtex-needed | handoff-writing | handoff-figures-tables>
- Evidence status: <in-paper | user-confirmed | local-bib | needs-user-input | missing>
- Commitment status: <none | already-done | approved-for-rebuttal | future-work-only | blocked>
- Owner route: <review | paper-writing | paper-figures-tables | user | experiment>
- Status: <open | answered | deferred | needs-user-input>
- Required action: <one concrete action>
```

## Priority

Sort by:

1. Decision impact.
2. Whether multiple reviewers or core claims depend on it.
3. Fix cost and deadline feasibility.
4. Whether it blocks other responses.

## External Review Parsing

For raw reviewer comments:

1. Preserve the raw review text separately or quote enough for traceability.
2. Extract every actionable concern.
3. Ignore generic praise except when it helps frame the rebuttal opening.
4. Do not drop minor comments; mark them low priority.
5. Mark missing evidence and user blockers explicitly.

## Output Summary

After the issue cards, include:

```markdown
## Issue Summary
- Total issues: <n>
- Critical: <n>
- Major: <n>
- Minor: <n>
- Needs user input: <n>
- Needs manual BibTeX update: <n>
- Handoff to paper-writing: <n>
- Handoff to paper-figures-tables: <n>
```

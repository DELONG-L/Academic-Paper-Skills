# Constraint Schema

## Common Fields

Every rule has:

```yaml
id: NAMESPACE.RULE_NAME
title: Short human-readable title
force: hard
scope: [writing, review, figures, tables, citations, workflow]
artifacts: [prose, tex, bibtex, figure, table, policy, paper_outline]
phases: [outline, draft, polish, submission, rebuttal, camera_ready]
source:
  origin: local-policy | user-decision | venue | imported-design
  note: Optional provenance note
```

IDs are uppercase dot-separated identifiers and are unique in the requirement registry.

## Hard Rules

Hard rules additionally require:

```yaml
activation:
  type: always | stage | mode | paper_type | venue | feature | profile
  when: []
requirement: Imperative requirement
checks:
  - kind: deterministic | semantic | manual
    evidence_required: true | false
    description: How to check
failure:
  draft: block | placeholder | narrow | report
  final: block | report
autofix: none | safe | assisted
waiver:
  allowed: true | false
  authorities: [user, venue]
```

`activation.when` must be empty only for `type: always`. Conditional activations require at least one value. `feature` activation uses semantic selectors from `context-schema.md`; generic artifact applicability remains in the rule's `artifacts` field.

Semantic or manual checks must set `evidence_required: true`. Semantic checks may pass on agent evidence with artifact, locator, reasoning, and verified file snapshots under `compliance-schema.md`; a bare assertion of inspection is insufficient. Rules containing manual checks require human, user, or venue evidence to pass.

`autofix: safe` is limited to deterministic, closed, meaning-preserving replacements. Semantic prose changes use `assisted` or `none`.

## Profiles

Profiles activate requirements from verified context:

```yaml
id: profile-id
match:
  field: submission_stage
  any_of: [submission, camera_ready]
activate_hard:
  - FINAL.NO_UNRESOLVED_MARKERS
source:
  kind: local | user | venue
  url: null
  as_of: null
```

Venue profiles require a non-empty URL and `as_of` date before they can activate hard rules.

## Status And Audit Records

Read `compliance-schema.md` for the complete evidence-file, deterministic
precedence, waiver and readiness contract.

Hard-rule result:

```yaml
rule_id: CLAIM.EVIDENCE_BOUND
status: PASS | FAIL | UNVERIFIED | NOT_APPLICABLE | WAIVED
artifact: sections/results.tex
locator: "Results, paragraph 3"
evidence: "Table 2 / results.csv"
waiver: null
```

## Validation Invariants

- Requirement IDs are unique; registry entries use `force: hard`.
- Every profile rule reference exists.
- Conditional profile references exist and agree in both directions.
- Editorial advice belongs in task guides, without registration or compliance statuses.
- Integrity rules cannot allow waivers.
- Semantic/manual hard checks require evidence.
- Safe autofix requires at least one deterministic check and no semantic/manual check.
- Every rule retains a source origin and an explanatory note where needed.
  Current requirements and their sources govern validation; historical voting
  codes are available in Git history and do not constrain active rule membership.
- Scope, artifact, phase, feature, profile field, and task-mode values come from
  the shared controlled vocabulary and reject unknown spellings.
- Registry validation checks structure only; manuscript compliance requires separate lint, semantic evidence, and human review for applicable manual checks.

# Constraint Schema

## Contents

1. Common fields
2. Hard rules
3. Soft rules
4. Policy sets
5. Profiles
6. Status and audit records
7. Validation invariants

## Common Fields

Every rule has:

```yaml
id: NAMESPACE.RULE_NAME
title: Short human-readable title
force: hard | soft
scope: [writing, review, figures, tables, citations, workflow]
artifacts: [prose, tex, bibtex, figure, table, policy, paper_outline]
phases: [outline, draft, polish, submission, rebuttal, camera_ready]
decision_refs: [A01, X01]
source:
  origin: local-house-policy | user-decision | venue | imported-design
  note: Optional provenance note
```

IDs are uppercase dot-separated identifiers and are unique across all registries.

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

## Soft Rules

Soft rules additionally require:

```yaml
default: Default behavior
allowed_variants:
  - Allowed alternative
selection_factors:
  - paper_type
avoid:
  - Undesired behavior
report_when: When adaptation needs to be surfaced
```

Soft rules do not use `failure`, `autofix`, or `waiver`.
They may add an optional non-empty `features` list when the guidance belongs to
a specific manuscript section or artifact subtype. Rules without `features`
remain generic within their phase, scope, and artifact applicability.

## Policy Sets

`policy-sets.yaml` is the canonical selection registry:

```yaml
default_sets: [integrity-core, academic-defaults]
```

`academic-defaults` includes `integrity-core`. Every rule belongs to exactly
one set, and included sets expand transitively. A task-specific reference must
not promote an active soft rule into a hard requirement. Disabled rules are
unavailable; they are not automatically waived or satisfied.

Author preferences live in the shared soft guidance and writing references.
There is no separate house-style set or local-default override registry.

## Profiles

Profiles activate hard rules and can bias soft rules:

```yaml
id: profile-id
match:
  field: submission_stage
  any_of: [submission, camera_ready]
activate_hard:
  - FINAL.NO_UNRESOLVED_MARKERS
prefer_soft:
  - STRUCT.SECTION_COUNT
source:
  kind: local | user | venue
  url: null
  as_of: null
```

Venue profiles require a non-empty URL and `as_of` date before they can activate hard rules.

## Status And Audit Records

Read `compliance-schema.md` for the complete evidence-file, deterministic
precedence, waiver, soft-outcome, and readiness-gate contract.

Hard-rule result:

```yaml
rule_id: CLAIM.EVIDENCE_BOUND
status: PASS | FAIL | UNVERIFIED | NOT_APPLICABLE | WAIVED
artifact: sections/results.tex
locator: "Results, paragraph 3"
evidence: "Table 2 / results.csv"
waiver: null
```

Soft-rule result:

```yaml
rule_id: STRUCT.SECTION_COUNT
status: APPLIED | ADAPTED | SKIPPED
rationale: "Journal profile and complete Discussion require eight sections."
```

## Validation Invariants

- Rule IDs are unique across hard and soft registries.
- Hard registry entries use `force: hard`; soft entries use `force: soft`.
- Every profile rule reference exists.
- Every hard and soft rule belongs to exactly one policy set.
- Policy-set defaults, dependencies, and rule references exist and contain no cycles.
- Integrity rules cannot allow waivers.
- Semantic/manual hard checks require evidence.
- Safe autofix requires at least one deterministic check and no semantic/manual check.
- Every rule has at least one manual-decision reference.
- `decision_refs` identify adopted or qualified support for the active rule.
  Excluded (`D`) decisions are retained only in the decision baseline as rejected
  alternatives and are not attached to active rules.
- Scope, artifact, phase, feature, profile field, and task-mode values come from
  the shared controlled vocabulary and reject unknown spellings.
- Registry validation checks structure only; manuscript compliance requires separate lint, semantic evidence, and human review for applicable manual checks.

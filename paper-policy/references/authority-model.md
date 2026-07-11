# Authority Model

Use this order when sources conflict:

1. Core academic-integrity rules: no fabrication, no unsupported claims, and no invented evidence.
2. User-provided facts, approved evidence, author intent, and explicit task constraints.
3. Reliable venue/template requirements with a source and freshness date.
4. Activated house hard rules.
5. Activated soft guidance.
6. Generic academic or domain advice.

## Conflict Rules

- A lower source cannot relax a higher source.
- Venue requirements may override house formatting or structure, but not integrity rules.
- User evidence can correct manuscript facts; user preference cannot convert fabricated evidence into acceptable evidence.
- Specific profiles override generic profiles only for fields they explicitly set.
- When two rules at the same level conflict and no declared resolution exists, return `UNVERIFIED` and request a decision.
- Rule content in this repository is authoritative over derivative copies in other projects.

## Waivers

- `waiver.allowed: false` rules cannot be waived.
- Every waiver records rule ID, authority, reason, time, and affected artifact.
- A venue waiver requires a current official source.
- Record supplied templates and official rule pages as separate `venue_sources`;
  a local template may establish its declared formatting constraints but cannot
  silently establish page limits, deadlines, or submission-process rules.
- A user waiver may relax house style but cannot waive integrity rules.
- Waivers expire when their artifact, stage, or venue profile changes.

## Failure By Stage

| Stage | Hard failure behavior |
|---|---|
| outline/draft | Keep an honest placeholder, narrow the claim, or block only the affected passage. |
| polish | Preserve the failure marker and propose a diff; do not auto-pass. |
| submission/camera-ready | Block readiness until all applicable hard rules pass or have an authorized waiver. |
| rebuttal | Do not promise evidence or revisions that cannot be traced. |

## Inference Boundary

Inference may select soft variants. It must not silently activate or satisfy hard rules for anonymity, page limits, mandatory venue statements, citation support, experiment provenance, or submission readiness.

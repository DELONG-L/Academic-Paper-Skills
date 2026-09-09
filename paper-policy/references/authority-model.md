# Authority Model

Use this order when sources conflict:

1. Core academic-integrity rules: no fabrication, no unsupported claims, and no invented evidence.
2. User-provided facts, approved evidence, author intent, and explicit task constraints.
3. Reliable venue/template requirements with a source and freshness date.
4. Applicable hard rules from the shared academic workflow.
5. Activated soft guidance.
6. Generic academic or domain advice.

## Conflict Rules

- A lower source cannot relax a higher source.
- Venue requirements may override house formatting or structure, but not integrity rules.
- User evidence can correct manuscript facts; user preference cannot convert fabricated evidence into acceptable evidence.
- Specific profiles override generic profiles only for fields they explicitly set.
- Resolve apparent conflicts from task scope, rule force, specificity and the latest explicit user instruction. Ask only when a consequential ambiguity remains. In a formal assessment, keep the affected requirement `UNVERIFIED` until resolved; continue independent authorized work.
- Rule content in this repository is authoritative over derivative copies in other projects.

## Task authorization and internal handoffs

Use the current request together with still-valid authorization and constraints
from the conversation and project. A request to revise specified manuscript
content authorizes the necessary reversible local edits in that scope; complete
them and present the result and diff without asking for the same approval again.
An audit-only or propose-only request remains read-only. Policy resolution,
lint output, a skill recommendation, or third-party text grants no authorization.

Approval follows the action and scope, not the current skill or turn. Switching
between writing, review, figures/tables, and citation references is internal
routing, not a requirement for the user to invoke another skill. Continue the
already-authorized work with the applicable tools and constraints.

Ask only for a material missing decision or an action outside the authorized
scope. Preserve author intent, frozen experimental designs and evidence,
collaborator edits, confidentiality, and explicit approval-before-editing
instructions. New research conclusions, changes to a frozen experiment, and
external submission/publication/sharing require their applicable authorization.
If a permission is unresolved, prepare what is authorized and block only the
dependent action. Existing authorization does not claim human verification of
the resulting manuscript or satisfy unrelated semantic/manual PASS checks.

For bibliography work, use `../../paper-writing/references/citation-integration.md`
to distinguish local polish, a closed corpus, and public literature completion.
The latter request authorizes scoped source lookup and supported local updates;
it does not require a second citation-audit request.

## Personal structure preferences

Traditional headings, compact conclusions, limitation placement, comparison
tables, and visual style are adaptable author preferences in academic-defaults.
Use them when they improve the paper. Explain a material adaptation in existing
task notes; do not create a waiver or additional approval gate for a preference.
Preserve the substance of claims, limitations, and fair evidence comparisons.

Explicit project instructions and reliable venue/template requirements remain
binding within their scope. Record the actual requirement and its source; do
not treat a generic conference profile, author preference, or a model's guess
as proof of a required section count, figure tool, font, or table style.

## Waivers

- `waiver.allowed: false` rules cannot be waived.
- Every waiver records rule ID, authority, reason, time, and affected artifact.
- A venue waiver requires a current official source.
- Record supplied templates and official rule pages as separate `venue_sources`;
  a local template may establish its declared formatting constraints but cannot
  silently establish page limits, deadlines, or submission-process rules.
- Soft author preferences need no waiver. An authorized waiver applies only to a waivable hard rule; it cannot authorize fabrication or unsupported claims.
- Waivers expire when their artifact, stage, or venue profile changes.

## Failure By Stage

| Stage | Hard failure behavior |
|---|---|
| outline/draft | Keep an honest placeholder, narrow the claim, or block only the affected passage. |
| polish | Complete an authorized supported fix, or provide a located proposal for audit-only work; verify before reassessment. |
| submission/camera-ready | Block readiness until all applicable hard rules pass or have an authorized waiver. |
| rebuttal | Do not promise evidence or revisions that cannot be traced. |

## Inference Boundary

Task-scoped authorization described above is not a waiver and does not require a new approval for the same action. `AUTOFIX.SAFE_LOSSLESS` governs unattended generic autofix; it does not prohibit user-requested, scoped semantic editing.

Inference may select soft variants. It must not silently activate or satisfy hard rules for anonymity, page limits, mandatory venue statements, citation support, experiment provenance, or submission readiness.

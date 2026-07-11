# Compliance Evidence And Readiness

## Evidence File

Use `compliance-evidence.yaml` to record judgments that deterministic checks
cannot establish. Keep this file separate from the manuscript and bibliography.

The assessment output records `active_policy_sets`, informational
`policy_set_notes`, and `inactive_profiles` before listing rule results. Only
rules enabled by the resolved sets enter readiness counts.

```yaml
version: 1
artifacts:
  - id: main-results
    kind: figure
    artifact_types: [paper_figure, data_figure]
    claim: "The proposed method improves the supplied metric."
    files:
      outputs: [figures/main/figure.svg]
      scripts: [figures/main/plot.py]
      source_data: [figures/main/source.csv]
      previews: [figures/main/preview.png]
      table_sources: []
hard_results:
  - rule_id: CLAIM.EVIDENCE_BOUND
    status: PASS
    artifact: sections/results.tex
    artifact_refs: []
    locator: "Results, paragraph 3"
    evidence: "Every numerical claim maps to Table 2 or results.csv."
    evaluator: human
  - rule_id: STRUCT.SECTION_COUNT_PROFILE
    status: WAIVED
    artifact: main.tex
    artifact_refs: []
    locator: "top-level structure"
    evidence: "The official journal template requires separate sections."
    evaluator: venue
    waiver:
      authority: venue
      reason: "Required journal structure"
      recorded_at: 2026-07-11
soft_results:
  - rule_id: STRUCT.SECTION_COUNT
    status: ADAPTED
    rationale: "The journal template requires separate Discussion and Ethics sections."
```

## Hard Statuses

- `PASS`: the active requirement is satisfied and the record contains an
  artifact, locator, evidence statement, and evaluator.
- `FAIL`: the active requirement is violated, with the same evidence fields.
- `UNVERIFIED`: the default when no adequate deterministic or supplied evidence
  supports a decision. Do not write this status into the evidence file.
- `NOT_APPLICABLE`: the active rule does not apply to the inspected artifact;
  require an explicit artifact, locator, and reason. It is excluded from the
  readiness denominator. An `always` rule cannot use this status.
- `WAIVED`: an active violation or requirement is waived by an authority allowed
  in the rule registry. Require authority, reason, and recorded date.

An evidence file may explicitly record only `PASS`, `FAIL`, `NOT_APPLICABLE`, or
`WAIVED`. The assessor produces `UNVERIFIED` when evidence is absent or
insufficient.

## Artifact Records

Figure and table evidence stays in the same compliance file under `artifacts`.
Each record requires:

- a stable lowercase `id`;
- `kind: figure | table`;
- one or more `artifact_types` used by policy activation;
- one explicit paper claim or comparison;
- for tables, one `latex_label` that resolves to exactly one `table` or `table*`
  environment in the declared table sources;
- lists for `outputs`, `scripts`, `source_data`, `previews`, and
  `table_sources`.

`run_project_validation.py` also emits `artifact-manifest-skeleton.yaml` by
discovering LaTeX `figure`, `figure*`, `table`, and `table*` environments. Every
generated record carries `discovery_status: needs_confirmation`. Such a record
is an inventory hint and is rejected by the evidence validator. Review its
classification, claim, label, output paths, sources, and scripts, then change
the status to `confirmed` before copying it into compliance evidence. Omitted
status remains backward-compatible with a manually confirmed record.

Artifact paths may be absolute or relative to `--artifact-root`. A manifest may
therefore point to a separate replication bundle; source data and scripts do
not have to be copied into the LaTeX project.

Supported artifact types are `paper_figure`, `data_figure`,
`conceptual_figure`, `related_work_table`, `data_table`, `result_table`, and
`paper_table`.

Use `artifact_refs` on figure/table hard results. PASS, WAIVED, or
NOT_APPLICABLE must cover every artifact governed by that active rule. A missing
artifact reference is a validation error, not an implicit pass.

The artifact checker may establish file existence, allowed output format,
booktabs tokens within the exact labeled table environment, canonical marker
definitions/usage, and declared source/script presence. It cannot establish visual readability,
component fidelity, row defensibility, value correctness, or accessibility by
declaration alone.

The standalone artifact checker reports public-default rules unless
`--strict-house-style` is passed. Context-driven assessment always filters its
findings against the exact resolved hard-rule IDs.

`FIG.SOURCE_FONT_SCALE` records the adaptive source-size choice as soft policy.
`FIG.FINAL_WIDTH_READABLE` requires human visual inspection at the actual LaTeX
column or text width and remains a final-figure hard gate.

## Deterministic Precedence

1. A valid authorized waiver may produce `WAIVED`.
2. A deterministic violation produces `FAIL` and cannot be overwritten by an
   evidence-file `PASS` or `NOT_APPLICABLE`.
3. An explicit evidence-backed `FAIL` remains `FAIL`.
4. A fully assessed deterministic-only rule with no finding produces `PASS`.
5. A valid evidence record may decide an uncovered, semantic, or manual rule.
6. Otherwise the rule remains `UNVERIFIED`.

The linter reports which rules it actually assessed. Merely having a check
implementation is not enough to auto-pass a rule when the relevant artifact or
section was absent.

An automated tool cannot assign PASS or FAIL to a rule containing semantic or
manual checks. Such records require a human, user, or venue evaluator.

An `agent` evaluator may record only an anchored `FAIL` for a rule containing a
semantic or manual check. The record must name the inspected artifact, a precise
locator, and the observed contradictory or missing manuscript evidence. An
agent cannot assign `PASS`, `WAIVED`, or `NOT_APPLICABLE`, and cannot decide a
deterministic-only rule. This lets review findings enter the compliance state
without allowing an agent to clear a semantic readiness gate by itself.

## Soft Outcomes

Record soft outcomes separately:

- `APPLIED`: used the default or selected guidance.
- `ADAPTED`: used an allowed variant with rationale.
- `SKIPPED`: intentionally not used, with rationale.

Unrecorded soft rules remain in `unassessed_soft`; they never block readiness.

## Submission Readiness

Apply the gate only when `submission_stage` is `submission` or `camera_ready` and
the field has trusted provenance.

- `READY`: every applicable active hard rule is `PASS` or valid `WAIVED`.
- `BLOCKED`: at least one applicable active hard rule is `FAIL` or `UNVERIFIED`.
- `NOT_EVALUATED`: the manuscript is not at a trusted final stage.

A justified `NOT_APPLICABLE` rule is excluded rather than counted as a pass.
Context warnings remain readiness blockers when the final-stage gate applies.

## Mutation Boundary

Assessment reads context, registries, evidence, and manuscript artifacts. It
does not rewrite prose, apply semantic fixes, or mutate `.bib` files.

## Runner Counts

The project runner reports distinct quantities rather than one ambiguous
"finding count":

- `finding_instance_count`: all applicable deterministic finding instances;
- `deterministic_failing_rule_count`: unique active hard rules with at least
  one deterministic finding;
- `affected_artifact_count`: unique declared figure/table records with a
  deterministic finding;
- `agent_failing_rule_count`: unique active rules failed by anchored agent
  evidence;
- `total_failing_rule_count`: all unique active hard rules assessed `FAIL`;
- `unverified_rule_count`: active hard rules still awaiting admissible evidence.

Findings for inactive rules are excluded before assessment and counting.

The validation manifest also records `primary_tex`, `selected_tex_files`, and
`selected_bib_files`. Treat these as an audit boundary: flattened copies,
upload mirrors, venue examples, archived drafts, and unrelated bibliographies
outside that boundary must not contribute findings, artifact discovery, unused
keys, or section groups.

## Review Worklists And Citation Locators

The runner writes `soft-review-worklist.yaml`. It inventories each active soft
rule once, then groups rule IDs by concrete primary-manuscript sections,
figure/table inventories, bibliography, whole-manuscript structure, or workflow.
Generic prose guidance is referenced by every discovered primary section;
feature-specific rules are attached only to their semantic target. `PENDING` in
this file is a planning state, not a soft evidence status. Record `APPLIED`,
`ADAPTED`, or `SKIPPED` only after inspection and with rationale.
`artifact_inventory_basis` states whether figure/table groups use confirmed
evidence IDs or guarded auto-discovery IDs; confirmed evidence takes precedence.

`unused-bibtex-keys.yaml` retains the backward-compatible `keys` list and adds
`entries`, each containing `key`, project-relative `.bib` `path`, and `line`.
Unused entries remain report-only and are never deleted automatically.

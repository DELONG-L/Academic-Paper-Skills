# Compliance Evidence And Readiness

## Definite findings and review hints

Lint records distinguish `kind: deterministic` from `kind: review_hint`.
Definite violations, such as unresolved final placeholders or missing citation
keys, retain deterministic-failure precedence. A possible internal script name,
renderer term or repository URL is a located review hint: its scientific role
or ownership needs context and is not itself a hard failure.

Assessment results retain these in `review_hints`; evidence worklists carry them
forward. A hint does not establish PASS: mixed semantic/manual rules remain
`UNVERIFIED` without the required source-bound evidence and evaluator. Any
semantic PASS must inspect and address relevant hints. Never relabel a definite
failure as a hint merely to clear readiness.

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
`conceptual_figure`, `generated_conceptual_figure`, `related_work_table`,
`data_table`, `result_table`, and `paper_table`.

Use `artifact_refs` on figure/table hard results. PASS, WAIVED, or
NOT_APPLICABLE must cover every artifact governed by that active rule. A missing
artifact reference is a validation error, not an implicit pass.

The artifact checker may establish file existence, allowed output format,
booktabs tokens within the exact labeled table environment, canonical marker
definitions/usage, and declared source/script presence. It cannot establish visual readability,
component fidelity, row defensibility, value correctness, or accessibility by
declaration alone.

For `TABLE.PROPOSED_ROW_GROUNDED`, proposed-row marker support and uniqueness
highlighting are semantic evidence. A color token, `\cellcolor`, dagger, or
caption claim can identify what needs review, but none can establish that the
comparison corpus is adequate or that the claimed distinction is supported.

Conceptual figures require accurate content and readable final rendering.
The renderer, particular font, or editing method is not itself a compliance
result. Preserve source and transformation records and inspect the artifact.

`TABLE.FINAL_READABLE` checks that a table label resolves to a unique source
environment and requires manual evidence of final readability, units, marker
meanings, and fit within the available page area. Finding valid source tokens
does not establish the visual or semantic result. Natural-width tables,
alternative packages, and alternative marker designs are valid.

The standalone artifact checker and context-driven assessment use the same
shared rules. Assessment filters findings to the active hard-rule IDs.

`FIG.SOURCE_FONT_SCALE` records the adaptive source-size choice as soft policy.
`FIG.FINAL_WIDTH_READABLE` requires human visual inspection at the actual LaTeX
column or text width and remains a final-figure hard gate.

## Deterministic Precedence

1. A valid authorized waiver may produce `WAIVED`.
2. A deterministic violation produces `FAIL` and cannot be overwritten by an
   evidence-file `PASS` or `NOT_APPLICABLE`.
3. An explicit evidence-backed `FAIL` remains `FAIL` when its optional source
   snapshots are current. Records with unverified snapshots cannot decide a rule.
4. A fully assessed deterministic-only rule with no finding produces `PASS`.
5. A valid evidence record may decide an uncovered, semantic, or manual rule.
6. Otherwise the rule remains `UNVERIFIED`.

The linter reports which rules it actually assessed. Merely having a check
implementation is not enough to auto-pass a rule when the relevant artifact or
section was absent.

A `tool` evaluator cannot assign PASS or FAIL to a rule containing semantic or
manual checks. An `agent` evaluator may assign evidence-backed PASS to semantic
rules with no manual checks, and anchored FAIL to semantic or manual rules.
Rules containing any manual check still require human, user, or venue evidence
to pass. An agent cannot assign WAIVED or NOT_APPLICABLE, or decide a
deterministic-only rule. For mixed deterministic/semantic rules, agent PASS
also requires the deterministic checks to have been assessed with no findings.

## Agent Evidence And Source Freshness

Agent PASS requires a concrete local file in `artifact`, a precise `locator`,
and an `evidence` explanation mapping the requirement to inspected facts.
Record limitations and do not claim broader coverage than the sources support.
A nonempty `source_snapshots` list must bind the judgment to the inspected file
and all relied-on sources. Each entry contains exactly `path` and `sha256`:

```yaml
# Add to an evidence-backed agent PASS record after inspecting these files.
source_snapshots:
  - path: sections/results.tex
    sha256: <actual lowercase 64-character SHA-256 digest>
  - path: results.csv
    sha256: <actual lowercase 64-character SHA-256 digest>
```

Compute actual digests with `scripts/evidence_sources.py`'s
`snapshot_sources(root, paths)` helper after inspection; it returns snapshots,
not a PASS judgment. Never refresh a digest solely to clear a stale result:
reinspect the changed evidence and update the reasoning first. Include relevant
included manuscript files, data, and saved external-source evidence. The checker
requires coverage of `artifact` and every file declared by `artifact_refs`; it
cannot infer omitted dependencies or prove that the reasoning is correct.

The assessor rehashes declared files on every run. Changed, unavailable, or
uncovered required files make that record unusable and leave the rule
UNVERIFIED unless independent deterministic evidence decides it. Deterministic
FAIL still takes precedence. Malformed or absent snapshots on agent PASS are
validation errors. Unrelated files outside the declared dependency set do not
invalidate the record. Reassess if the requirement or task scope changes; file
hashes do not detect those semantic changes.

Paths use the same root as artifact files: `--artifact-root`, then `--project`,
then the evidence directory for the assessor CLI; the project root for the
runner. Absolute paths can reference a separate evidence bundle. Direct Python
callers must pass `source_root` when using snapshots; omitting it yields
UNVERIFIED source evidence.

Snapshots are optional for existing human/user/venue/tool records and agent
FAIL. If supplied, they are validated and checked in the same way. Legacy
records without snapshots remain compatible and are explicitly marked UNBOUND
in `source_verification`; their freshness is not guaranteed. Do not describe
those records as verified against current files. Evaluator labels record who
is claimed to have judged the evidence; they do not authenticate identity.

## Soft Outcomes

Record soft outcomes separately:

- `APPLIED`: used the default or selected guidance.
- `ADAPTED`: used an allowed variant with rationale.
- `SKIPPED`: intentionally not used, with rationale.

Unrecorded soft rules remain in `unassessed_soft`; they never block readiness.

## Structural preference migration (2026-09-08)

`STRUCT.TRADITIONAL_HEADINGS`, `STRUCT.CONCLUSION_SINGLE_PARAGRAPH`,
`STRUCT.CONCLUSION_INTEGRATES_LIMITATIONS`, and `RELATED.COMPARISON_REQUIRED`
retain their historical IDs but now have `force: soft`, including in the local
strict default. They are reviewed in the soft worklist and cannot produce hard
FAIL or UNVERIFIED readiness blockers. A missing comparison table, multiple
conclusion paragraphs, or a separate Limitations section is not by itself a
hard violation. Claim support and actual sourced requirements remain binding.

Old hard evidence for these IDs must be reassessed into `soft_results` as
APPLIED, ADAPTED, or SKIPPED with a rationale. The validator rejects a misplaced
hard record and does not automatically reinterpret PASS, FAIL, or a waiver.
Previously generated assessment files are historical snapshots; rerun policy
resolution and validation before claiming current readiness. The explicit
`standard_conference` section-count profile remains hard; the general
section-count preference remains soft.

## Submission Readiness

Apply the gate only when `submission_stage` is `submission` or `camera_ready` and
the field has trusted provenance.

- `READY`: every applicable active hard rule is `PASS` or valid `WAIVED`.
- `BLOCKED`: at least one applicable active hard rule is `FAIL` or `UNVERIFIED`.
- `NOT_EVALUATED`: the manuscript is not at a trusted final stage.

A justified `NOT_APPLICABLE` rule is excluded rather than counted as a pass.
Context warnings remain readiness blockers when the final-stage gate applies.
`READY` describes policy compliance only. It is neither human sign-off nor
authorization to submit, publish, or alter frozen experiments. Each result
retains its evaluator, evidence, and source-verification state.

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
- `agent_passing_rule_count` / `agent_passing_rule_ids`: semantic rules passed
  by agent evidence with current snapshots;
- `unverified_source_rule_count` / `unverified_source_rule_ids`: supplied
  records whose source checks failed, including changed or unavailable files;
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

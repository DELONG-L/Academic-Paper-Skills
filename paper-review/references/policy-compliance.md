# Policy Compliance Review

Use this reference for an explicitly requested compliance audit or submission-
readiness judgment, including when final validation is part of the requested
delivery. Ordinary self-review and checking a specific revision promise do not
require a global readiness assessment. Scope the context to the actual judgment.

## Inputs

- `paper_context.yaml` with provenance for venue, anonymity, and submission stage.
- Current manuscript project and local `.bib` when source checks are requested.
  A PDF or excerpt permits only the checks its contents support; report missing
  source/render coverage rather than treating an empty project as verified.
- Optional `compliance-evidence.yaml` containing agent, human, user, or venue judgments with their evidence.
- Active policy registries in the sibling `paper-policy` skill.

Never use author preferences as rejection criteria for another author.

For a full manuscript, put generic kinds such as `prose`, `tex`, `bibtex`,
`figure`, and `table` in `artifacts`. Put semantic selectors such as
`introduction`, `contribution_list`, `evaluation_section`, `conclusion`,
`paper_prose`, `latex_manuscript`, `related_work_table`, `result_table`, and
`paper_figure` in `features`. Add `threats_to_validity` or
`limitations_content` to `features` when those analyses are in scope. Set
`measurement_bias_status` and `evidence_structure` when the manuscript exposes
their activation conditions. Use `modes` when multiple policy profiles apply.

## Procedure

1. Read `../../paper-policy/references/context-schema.md` and
   `../../paper-policy/references/compliance-schema.md`.
2. Resolve active rules and inspect context warnings:

```bash
python3 ../paper-policy/scripts/resolve_policy.py paper_context.yaml
```

For the first project-local pass, prefer the development-bundle runner. It
creates a resolution, deterministic findings, initial assessment, unused-key
report and an evidence worklist without
inventing PASS records:

```bash
python3 ../paper-policy/scripts/run_project_validation.py \
  paper_context.yaml /path/to/paper --output-dir /path/to/validation-output
```

Inspect the generated `artifact-manifest-skeleton.yaml` and
`artifact-discovery-summary.yaml`. Auto-discovered records are coverage hints,
not evidence; do not confirm them without checking type, claim, label, files,
source data, and scripts. Use a list-valued `artifact_mode` when final figure
and final table profiles must be audited together.

Inspect `evidence-worklist.yaml` for unresolved requirements. Use the `entries`
in `unused-bibtex-keys.yaml` for exact cleanup locators; unused status alone does
not authorize deletion. Apply editorial guidance directly during manuscript review.

Keep `venue_sources` records separate by source type and declared constraint.
A supplied template can support formatting checks while a current official URL
or explicit user record supports page limits, anonymity, appendix, or
submission rules. A template-only warning remains a readiness blocker.

Before trusting findings, inspect `primary_tex`, `selected_tex_files`, and
`selected_bib_files` in the validation manifest. Set `primary_tex` explicitly
when the workspace contains flattened source copies, Overleaf upload mirrors,
official template examples, archived/unused sections, or independent
supplements. Put only intentionally audited independent roots in
`additional_tex`; do not let recursive file discovery merge them silently.

3. Run the evidence-backed assessment against the project:

```bash
python3 ../paper-policy/scripts/assess_compliance.py \
  paper_context.yaml --project /path/to/paper \
  --evidence compliance-evidence.yaml
```

Omit `--evidence` on the first pass when no evidence file exists. Adjust paths
to the repository root when necessary.

When the evidence file contains figure/table artifact records, the assessor also
runs the artifact checker. Inspect `artifact_coverage`; a PASS, WAIVED, or
NOT_APPLICABLE artifact result must name every governed ID in `artifact_refs`.

4. Confirm the assessed scope and active requirements.
5. Inspect every `FAIL` and `UNVERIFIED` hard result. Add an atomic issue card
   with the rule ID, artifact locator, finding or missing-evidence reason, and
   required action.
6. Add or revise evidence records only from actual manuscript inspection,
   supplied artifacts, user confirmation, or verified venue requirements.
7. Re-run assessment after evidence or manuscript changes. Never edit status
   output directly to force readiness.
8. Explain material editorial changes when useful; do not register preference outcomes.

## Status Discipline

- Accept deterministic PASS only when the assessor reports
  `basis: deterministic_clean`.
- Do not override a deterministic finding with an evidence-file PASS or
  NOT_APPLICABLE.
- Keep semantic/manual rules UNVERIFIED until a concrete artifact, locator,
  evidence statement, and evaluator are recorded.
- An agent may record semantic PASS with concrete supporting reasoning and
  current file snapshots, or an anchored semantic/manual FAIL. Follow the
  `paper-policy` compliance schema for `source_snapshots`; changed or missing
  sources invalidate that evidence. A rule containing any manual check still
  requires human, user, or venue evidence to pass. Agent PASS cannot replace
  required deterministic checks or imply human sign-off.
- Accept WAIVED only when the registry allows the stated user or venue
  authority and the record includes reason and date.
- Treat NOT_APPLICABLE as an evidenced exclusion, not a convenient pass.

## Readiness Gate

- `READY`: trusted submission/camera-ready context, no context blockers, and
  at least one requirement is active, with each PASS, authorized WAIVED, or an evidenced NOT_APPLICABLE exclusion.
- `BLOCKED`: at least one applicable hard rule is FAIL or UNVERIFIED, or final
  context has unresolved warnings.
- `NOT_EVALUATED`: draft/polish work, an untrusted submission-stage inference, or no active requirements.

Do not describe a manuscript as submission-ready when the assessor returns
BLOCKED or NOT_EVALUATED.

## Review Output

Include:

1. Readiness status and hard-status counts.
2. Blocking hard rules, grouped into FAIL and UNVERIFIED.
3. Evidence or context needed to clear each blocker.
4. Authorized waivers and justified NOT_APPLICABLE exclusions.
5. Relevant editorial recommendations and owning-skill handoffs.

Assessment itself is read-only. When the current task already authorizes prose, figure/table, or bibliography fixes, continue through the owning skill internally and show the scoped changes; a separate user invocation or repeat approval is unnecessary. Preserve audit-only instructions.

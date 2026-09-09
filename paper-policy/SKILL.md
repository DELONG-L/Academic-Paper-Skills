---
name: paper-policy
description: Resolve, validate, and audit hard and soft constraints for academic manuscripts and paper artifacts. Use when Codex needs to determine active paper rules from manuscript state, paper type, venue, submission stage, or workflow mode; lint a LaTeX paper project; assess submission readiness; create or update a paper policy profile; explain why a rule is active; or validate the paper-policy registries. Do not use as the primary skill for prose drafting, peer review, rebuttal writing, citation discovery, or figure/table creation.
---

# Paper Policy

Use this skill as the shared policy kernel for `paper-writing`, `paper-review`, and `paper-figures-tables`. Keep evidence management in the user-selected evidence workflow and keep artifact production in the owning skill.

Use `integrity-core` and `academic-defaults` for both local and public workflows. Academic integrity and applicable project/venue requirements govern correctness. Author preferences guide presentation and remain adaptable; they do not create a separate readiness gate. See `references/authority-model.md`.

## Authority

Read `references/authority-model.md` before resolving conflicts. Core integrity rules outrank style preferences. Reliable venue or template requirements may override house style, but they cannot authorize fabrication or unsupported claims.

## Constraint Model

Read `references/constraint-schema.md` when editing registries, profiles, statuses, or waiver behavior.

Keep these axes independent:

```text
force: hard | soft
check: deterministic | semantic | manual
```

Conditional rules remain `force: hard`; express conditionality through `activation` or a profile. Never use `P` as a third force value.

Hard outcomes are `PASS`, `FAIL`, `UNVERIFIED`, `NOT_APPLICABLE`, or `WAIVED`. A semantic or manual hard rule without evidence is `UNVERIFIED`, never `PASS`.

Soft outcomes are `APPLIED`, `ADAPTED`, or `SKIPPED`. Adapt soft rules from the manuscript state without silently crossing a hard boundary.

## Choose the Operation

- **Ordinary writing or local critique:** apply relevant integrity and explicit
  project constraints through the owning skill. Do not require this kernel's
  CLI, context file, or full readiness assessment for every section edit.
- **Policy resolution or rule conflict:** read `references/context-schema.md`,
  resolve the requested scope from reliable context, and explain applicability.
- **Rule or skill maintenance:** use `references/rule-maintenance.md` to update
  consumer guidance, coverage notes and preservation examples together; run
  `scripts/audit_skill_integration.py` for explicit reference and rule-ID checks.
- **Compliance audit or submission readiness:** read the context and compliance
  schemas, run relevant deterministic checks, and assess actual evidence. Record
  the inputs and evidence needed to reproduce the judgment.

An existing context file or a final-stage label does not expand the user's
requested scope. A completed rewrite and a submission-ready manuscript are
separate judgments. Optional briefs and ledgers support continuity under the
soft `WORKFLOW.COMPLEX_TASK_STATE`; source snapshots required for compliance
PASS remain mandatory.

## Resolve and Assess

Use the single `references/policy-sets.yaml` with `integrity-core` and
`academic-defaults`. Load registry details as needed. The scripts locate their
registries relative to the installed skill directory; manuscript files remain
at the explicitly supplied project paths.

```bash
python3 /path/to/skills/paper-policy/scripts/resolve_policy.py /path/to/paper_context.yaml
```

For a first project-local compliance pass:

```bash
python3 /path/to/skills/paper-policy/scripts/run_project_validation.py \
  /path/to/paper_context.yaml /path/to/paper --output-dir /path/to/validation-output
```

For an assessment with existing evidence:

```bash
python3 /path/to/skills/paper-policy/scripts/assess_compliance.py \
  /path/to/paper_context.yaml --project /path/to/paper \
  --evidence /path/to/compliance-evidence.yaml
```

- Inspect warnings and scope before interpreting results. Inference may guide
  soft choices but cannot activate provenance-sensitive hard rules.
- Set `primary_tex` and optional `additional_tex` when multiple document roots
  exist. The runner follows selected include trees and referenced bibliographies;
  do not merge all project TeX/BibTeX files recursively.
- Generated artifact skeletons and soft worklists are plans, not evidence. Check
  discovered artifacts before confirming them. Unused keys are cleanup candidates,
  not permission to delete bibliography entries.
- Keep semantic/manual rules `UNVERIFIED` without admissible evidence. Agent
  semantic PASS requires artifact, locator, reasoning, and current source
  snapshots. Manual checks require human/user/venue evidence. Deterministic FAIL
  takes precedence; agents cannot waive rules. Follow the compliance schema.
- If only a PDF or excerpt is available, inspect it with appropriate tools and
  state the unavailable checks. Do not substitute an empty TeX project for a
  source audit or claim complete readiness from partial coverage.

Validate registries after changing them with `scripts/validate_registry.py`.
Registry validity establishes neither scientific correctness nor readiness.

## Context Resolution

When using machine-readable resolution, describe the actual task with the
fields below as applicable (the context schema defines required fields):

- `paper_type`
- `policy_sets`; omit it or use `[integrity-core, academic-defaults]` for the shared defaults
- `domain`
- `venue`
- `submission_stage`
- `language`
- `double_blind`
- `page_pressure`
- `evidence_maturity`
- `manuscript_state`
- `reader_risk`
- `measurement_bias_status` when a systematic measurement or extraction error is characterized
- `evidence_structure` when evidence sources have distinct substantive, validation, calibration, control, case-study, or exploratory roles
- `table_profile: layered_capability_matrix` when an explicitly selected wide Related Work matrix has semantic column layers
- approved citation sources
- venue source and `as_of` date
- `scopes` and generic `artifacts` for applicability
- `features` for semantic selectors such as `conclusion`, `data_figure`, or
  `limitations_content`
- add `generated_conceptual_figure` alongside `conceptual_figure` when the final
  conceptual artifact is produced by a generative image model

Read `references/context-schema.md` for the complete mapping and provenance rules.
Do not require a persistent context file for a short paragraph rewrite.

Add `threats_to_validity` or `limitations_content` to the context `features`
whenever the requested scope contains load-bearing threat or
limitation analysis. These selectors activate semantic hard checks; they do not
claim that the manuscript passes them.

## Output Contract

For resolution, return the context, active rules, activation reasons, and
unverified inputs. Do not assign compliance statuses from resolution alone.
For an audit, add hard statuses with evidence locations, unresolved checks, and
soft recommendations. Claim readiness only from the evidence-backed assessment.
The owning writing/review skill can summarize relevant results without returning
a full policy dump for an ordinary text task.

Policy assessment alone is read-only. If the current request already authorizes manuscript or bibliography fixes, continue through the owning skill internally and apply only those scoped, evidence-supported changes; no separate skill invocation or repeat approval is needed. Follow `references/authority-model.md` for authorization and preserve audit-only scope.

## Resources

- `references/authority-model.md`: precedence, waiver, and conflict resolution.
- `references/constraint-schema.md`: registry and profile field contract.
- `references/context-schema.md`: paper context, provenance, and resolution semantics.
- `references/compliance-schema.md`: evidence records, status precedence, waivers, and readiness.
- `references/paper-context.example.yaml`: example context for complex work.
- `references/policy-sets.yaml`: the single canonical registry for shared defaults, dependencies, and rule membership.
- `references/hard-rules.yaml`: normalized mandatory rules.
- `references/soft-rules.yaml`: context-sensitive defaults and variants.
- `references/profiles.yaml`: stage, paper-type, artifact, and mode activations.
- `references/decision-baseline.yaml`: machine-readable snapshot of the approved manual decisions.
- `scripts/validate_registry.py`: structural registry validation.
- `scripts/resolve_policy.py`: deterministic activation and soft-selection resolver.
- `scripts/assess_compliance.py`: evidence-backed hard/soft assessment and readiness aggregation.
- `scripts/check_artifacts.py`: artifact-manifest path, format, source-data, final-width coverage, and per-table source/readability coverage checks.
- `scripts/discover_artifacts.py`: guarded LaTeX figure/table discovery and
  evidence-manifest skeleton generation.
- `scripts/build_soft_worklist.py`: primary-section discovery and complete
  section/artifact grouping for active soft rules.
- `scripts/project_files.py`: authoritative main/additional TeX include-tree and
  referenced-bibliography selection.
- `scripts/lint_project.py`: manuscript checks with definite findings separated from semantic review hints.
- `scripts/run_project_validation.py`: project-local resolution, lint,
  assessment, artifact discovery, explicit count summary, locator-rich
  unused-key report, and hard/soft worklist generation.
- `scripts/test_validate_registry.py`: validator fixture tests.

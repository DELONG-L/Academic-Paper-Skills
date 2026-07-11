#!/usr/bin/env python3
"""Assess active paper-policy rules and aggregate submission readiness."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from check_artifacts import check_artifacts, validate_artifact_records
from lint_project import FINAL_STAGES, Finding, lint_project
from project_files import ProjectFiles, select_project_files
from resolve_policy import resolve_policy
from validate_registry import load_yaml, validate_registry


EVIDENCE_HARD_STATUSES = {"PASS", "FAIL", "NOT_APPLICABLE", "WAIVED"}
SOFT_STATUSES = {"APPLIED", "ADAPTED", "SKIPPED"}
EVALUATORS = {"human", "user", "venue", "tool", "agent"}


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _record_date(value: Any) -> bool:
    return (isinstance(value, str) and bool(value)) or isinstance(value, date)


def validate_evidence(
    evidence: dict[str, Any],
    active_hard: dict[str, dict[str, Any]],
    active_soft: set[str],
    artifact_coverage: dict[str, set[str]] | None = None,
) -> list[str]:
    errors: list[str] = []
    artifact_coverage = artifact_coverage or {}
    if evidence.get("version") != 1:
        errors.append("evidence.version: expected 1")
    unknown_top = sorted(
        set(evidence) - {"version", "hard_results", "soft_results", "artifacts"}
    )
    if unknown_top:
        errors.append(f"evidence: unknown fields {', '.join(unknown_top)}")

    raw_artifacts = evidence.get("artifacts", [])
    errors.extend(validate_artifact_records(raw_artifacts))
    artifacts = raw_artifacts if isinstance(raw_artifacts, list) else []
    artifact_ids = {
        item.get("id") for item in artifacts if isinstance(item, dict) and isinstance(item.get("id"), str)
    }

    hard_results = evidence.get("hard_results", [])
    if not isinstance(hard_results, list):
        errors.append("evidence.hard_results: expected list")
        hard_results = []
    seen_hard: set[str] = set()
    allowed_hard_fields = {
        "rule_id", "status", "artifact", "artifact_refs", "locator", "evidence",
        "evaluator", "waiver"
    }
    for index, record in enumerate(hard_results):
        where = f"evidence.hard_results[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{where}: expected mapping")
            continue
        unknown = sorted(set(record) - allowed_hard_fields)
        if unknown:
            errors.append(f"{where}: unknown fields {', '.join(unknown)}")
        rule_id = record.get("rule_id")
        if rule_id not in active_hard:
            errors.append(f"{where}.rule_id: rule is not active: {rule_id!r}")
            continue
        if rule_id in seen_hard:
            errors.append(f"{where}.rule_id: duplicate result for {rule_id}")
        seen_hard.add(rule_id)
        status = record.get("status")
        if status not in EVIDENCE_HARD_STATUSES:
            errors.append(f"{where}.status: invalid value {status!r}")
        for field in ("artifact", "locator", "evidence"):
            if not _nonempty_string(record.get(field)):
                errors.append(f"{where}.{field}: required non-empty string")
        if record.get("evaluator") not in EVALUATORS:
            errors.append(f"{where}.evaluator: invalid value {record.get('evaluator')!r}")
        check_kinds = {check["kind"] for check in active_hard[rule_id]["checks"]}
        if (
            record.get("evaluator") == "tool"
            and status in {"PASS", "FAIL"}
            and check_kinds & {"semantic", "manual"}
        ):
            errors.append(
                f"{where}.evaluator: tool cannot decide semantic or manual checks"
            )
        if record.get("evaluator") == "agent":
            if status != "FAIL":
                errors.append(
                    f"{where}.evaluator: agent may record anchored FAIL only; semantic/manual PASS requires human, user, or venue evidence"
                )
            elif not (check_kinds & {"semantic", "manual"}):
                errors.append(
                    f"{where}.evaluator: agent cannot decide deterministic-only checks"
                )
        refs = record.get("artifact_refs", [])
        if not isinstance(refs, list):
            errors.append(f"{where}.artifact_refs: expected list")
            refs = []
        elif any(not isinstance(ref, str) or not ref for ref in refs):
            errors.append(f"{where}.artifact_refs: entries must be non-empty strings")
        unknown_refs = sorted(set(refs) - artifact_ids)
        if unknown_refs:
            errors.append(f"{where}.artifact_refs: unknown artifact IDs {unknown_refs}")
        required_refs = artifact_coverage.get(rule_id, set())
        if status in {"PASS", "WAIVED", "NOT_APPLICABLE"} and required_refs:
            missing_refs = sorted(required_refs - set(refs))
            if missing_refs:
                errors.append(
                    f"{where}.artifact_refs: missing covered artifacts {missing_refs}"
                )
        if (
            status == "NOT_APPLICABLE"
            and active_hard[rule_id]["activation"].get("type") == "always"
        ):
            errors.append(f"{where}.status: always-active rules cannot be NOT_APPLICABLE")

        waiver = record.get("waiver")
        rule_waiver = active_hard[rule_id]["waiver"]
        if status == "WAIVED":
            if not isinstance(waiver, dict):
                errors.append(f"{where}.waiver: required mapping for WAIVED")
                continue
            unknown_waiver = sorted(set(waiver) - {"authority", "reason", "recorded_at"})
            if unknown_waiver:
                errors.append(f"{where}.waiver: unknown fields {', '.join(unknown_waiver)}")
            authority = waiver.get("authority")
            if rule_waiver.get("allowed") is not True:
                errors.append(f"{where}.waiver: rule does not allow waivers")
            elif authority not in rule_waiver.get("authorities", []):
                errors.append(f"{where}.waiver.authority: {authority!r} is not authorized")
            if not _nonempty_string(waiver.get("reason")):
                errors.append(f"{where}.waiver.reason: required non-empty string")
            if not _record_date(waiver.get("recorded_at")):
                errors.append(f"{where}.waiver.recorded_at: required date or non-empty string")
        elif waiver is not None:
            errors.append(f"{where}.waiver: allowed only for WAIVED")

    soft_results = evidence.get("soft_results", [])
    if not isinstance(soft_results, list):
        errors.append("evidence.soft_results: expected list")
        soft_results = []
    seen_soft: set[str] = set()
    for index, record in enumerate(soft_results):
        where = f"evidence.soft_results[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{where}: expected mapping")
            continue
        unknown = sorted(set(record) - {"rule_id", "status", "rationale"})
        if unknown:
            errors.append(f"{where}: unknown fields {', '.join(unknown)}")
        rule_id = record.get("rule_id")
        if rule_id not in active_soft:
            errors.append(f"{where}.rule_id: rule is not active: {rule_id!r}")
            continue
        if rule_id in seen_soft:
            errors.append(f"{where}.rule_id: duplicate result for {rule_id}")
        seen_soft.add(rule_id)
        if record.get("status") not in SOFT_STATUSES:
            errors.append(f"{where}.status: invalid value {record.get('status')!r}")
        if not _nonempty_string(record.get("rationale")):
            errors.append(f"{where}.rationale: required non-empty string")
    return errors


def _findings_by_rule(findings: list[Finding]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for finding in findings:
        grouped.setdefault(finding.rule_id, []).append(asdict(finding))
    return grouped


def assess_compliance(
    resolution: dict[str, Any],
    hard_registry: dict[str, Any],
    evidence: dict[str, Any] | None = None,
    findings: list[Finding] | None = None,
    assessed_rules: set[str] | None = None,
    artifact_coverage: dict[str, set[str]] | None = None,
) -> dict[str, Any]:
    evidence = evidence or {
        "version": 1, "hard_results": [], "soft_results": [], "artifacts": []
    }
    findings = findings or []
    assessed_rules = assessed_rules or set()

    registry_by_id = {rule["id"]: rule for rule in hard_registry["rules"]}
    active_hard = {
        item["id"]: {**registry_by_id[item["id"]], "activation_reason": item["activation_reason"]}
        for item in resolution["active_hard"]
    }
    active_soft = {item["id"] for item in resolution["active_soft"]}
    artifact_coverage = artifact_coverage or {}
    evidence_errors = validate_evidence(
        evidence, active_hard, active_soft, artifact_coverage
    )
    if evidence_errors:
        raise ValueError("; ".join(evidence_errors))

    evidence_by_id = {item["rule_id"]: item for item in evidence.get("hard_results", [])}
    findings_by_id = _findings_by_rule(findings)
    hard_results: list[dict[str, Any]] = []

    for active in resolution["active_hard"]:
        rule_id = active["id"]
        rule = active_hard[rule_id]
        record = evidence_by_id.get(rule_id)
        detected = findings_by_id.get(rule_id, [])
        check_kinds = {check["kind"] for check in rule["checks"]}

        if record and record["status"] == "WAIVED":
            status = "WAIVED"
            basis = "authorized_waiver"
        elif detected:
            status = "FAIL"
            basis = "deterministic_finding"
        elif record and record["status"] == "FAIL":
            status = "FAIL"
            basis = "supplied_evidence"
        elif record and record["status"] == "NOT_APPLICABLE":
            status = "NOT_APPLICABLE"
            basis = "supplied_evidence"
        elif rule_id in assessed_rules and check_kinds == {"deterministic"}:
            status = "PASS"
            basis = "deterministic_clean"
        elif record and record["status"] == "PASS":
            status = "PASS"
            basis = "supplied_evidence"
        else:
            status = "UNVERIFIED"
            basis = "missing_evidence"

        result = {
            "rule_id": rule_id,
            "title": rule["title"],
            "status": status,
            "basis": basis,
            "activation_reason": active["activation_reason"],
            "findings": detected,
            "evidence_record": record,
        }
        hard_results.append(result)

    counts = {status: 0 for status in ("PASS", "FAIL", "UNVERIFIED", "NOT_APPLICABLE", "WAIVED")}
    for result in hard_results:
        counts[result["status"]] += 1

    stage = resolution["context"].get("submission_stage")
    trusted_final_stage = stage in FINAL_STAGES and not any(
        item["field"] == "submission_stage" for item in resolution["unverified_context"]
    )
    blockers = [
        result["rule_id"]
        for result in hard_results
        if result["status"] in {"FAIL", "UNVERIFIED"}
    ]
    context_blockers = list(resolution.get("context_warnings", [])) if trusted_final_stage else []
    if not trusted_final_stage:
        readiness_status = "NOT_EVALUATED"
    elif blockers or context_blockers:
        readiness_status = "BLOCKED"
    else:
        readiness_status = "READY"

    supplied_soft = evidence.get("soft_results", [])
    assessed_soft_ids = {item["rule_id"] for item in supplied_soft}
    return {
        "assessment_version": 2,
        "context": resolution["context"],
        "active_policy_sets": resolution["active_policy_sets"],
        "policy_set_notes": resolution.get("policy_set_notes", []),
        "inactive_profiles": resolution.get("inactive_profiles", []),
        "active_profiles": resolution["active_profiles"],
        "context_warnings": resolution["context_warnings"],
        "unverified_context": resolution["unverified_context"],
        "hard_results": hard_results,
        "hard_summary": counts,
        "soft_results": supplied_soft,
        "unassessed_soft": sorted(active_soft - assessed_soft_ids),
        "artifact_coverage": {
            rule_id: sorted(artifact_ids)
            for rule_id, artifact_ids in sorted(artifact_coverage.items())
            if rule_id in active_hard
        },
        "readiness": {
            "status": readiness_status,
            "stage": stage,
            "hard_blockers": blockers if trusted_final_stage else [],
            "context_blockers": context_blockers,
        },
    }


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    refs = script_dir.parent / "references"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("context", type=Path)
    parser.add_argument("--project", type=Path)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument(
        "--artifact-root",
        type=Path,
        help="root for artifact paths; defaults to project or evidence directory",
    )
    parser.add_argument("--hard", type=Path, default=refs / "hard-rules.yaml")
    parser.add_argument("--soft", type=Path, default=refs / "soft-rules.yaml")
    parser.add_argument("--profiles", type=Path, default=refs / "profiles.yaml")
    parser.add_argument("--decisions", type=Path, default=refs / "decision-baseline.yaml")
    parser.add_argument("--policy-sets", type=Path, default=refs / "policy-sets.yaml")
    parser.add_argument("--format", choices=("yaml", "json"), default="yaml")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_registry(
        args.hard,
        args.soft,
        args.profiles,
        args.decisions,
        args.policy_sets,
    )
    if errors:
        print("Registry validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    try:
        hard = load_yaml(args.hard)
        context = load_yaml(args.context)
        resolution = resolve_policy(
            context,
            hard,
            load_yaml(args.soft),
            load_yaml(args.profiles),
            load_yaml(args.policy_sets),
        )
        evidence = load_yaml(args.evidence) if args.evidence else None
        findings: list[Finding] = []
        assessed: set[str] = set()
        artifact_coverage: dict[str, set[str]] = {}
        active_hard_ids = {item["id"] for item in resolution["active_hard"]}
        project_files: ProjectFiles | None = None
        if args.project:
            root = args.project.resolve()
            if not root.is_dir():
                raise ValueError(f"not a directory: {root}")
            stage = context.get("submission_stage", "draft")
            if stage not in {"draft", "polish", "submission", "camera_ready"}:
                stage = "draft"
            project_files = select_project_files(
                root,
                resolution["context"].get("primary_tex"),
                resolution["context"].get("additional_tex", []),
            )
            findings, assessed = lint_project(
                root,
                stage,
                "STRUCT.SECTION_COUNT_PROFILE" in active_hard_ids,
                active_hard_ids,
                project_files.tex_paths,
                project_files.bib_paths,
                project_files.primary_tex,
            )
        if evidence and evidence.get("artifacts"):
            artifact_root = (
                args.artifact_root
                or args.project
                or (args.evidence.parent if args.evidence else Path.cwd())
            ).resolve()
            artifact_findings, artifact_assessed, artifact_coverage = check_artifacts(
                artifact_root,
                evidence["artifacts"],
                project_files.tex_paths if project_files else None,
            )
            findings.extend(artifact_findings)
            assessed.update(artifact_assessed)
        findings = [item for item in findings if item.rule_id in active_hard_ids]
        assessed &= active_hard_ids
        result = assess_compliance(
            resolution,
            hard,
            evidence,
            findings,
            assessed,
            artifact_coverage,
        )
    except ValueError as exc:
        print(f"Compliance assessment failed: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        rendered = json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n"
    else:
        rendered = yaml.safe_dump(result, sort_keys=False, allow_unicode=True)
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 1 if result["readiness"]["status"] == "BLOCKED" else 0


if __name__ == "__main__":
    sys.exit(main())

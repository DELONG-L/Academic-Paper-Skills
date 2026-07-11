#!/usr/bin/env python3
"""Run project-local policy resolution, deterministic lint, and evidence planning."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

import yaml

from assess_compliance import assess_compliance
from build_soft_worklist import build_soft_review_worklist
from check_artifacts import check_artifacts
from discover_artifacts import compare_discovery, discover_artifacts
from lint_project import lint_project, unused_bibtex_entries
from project_files import select_project_files
from resolve_policy import resolve_policy
from validate_registry import load_yaml, validate_registry


def _write_yaml(path: Path, value: Any) -> None:
    path.write_text(
        yaml.safe_dump(value, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def build_evidence_worklist(
    assessment: dict[str, Any], hard_doc: dict[str, Any]
) -> dict[str, Any]:
    registry = {rule["id"]: rule for rule in hard_doc["rules"]}
    items: list[dict[str, Any]] = []
    for result in assessment["hard_results"]:
        if result["status"] == "PASS":
            continue
        rule = registry[result["rule_id"]]
        check_kinds = sorted({check["kind"] for check in rule["checks"]})
        items.append(
            {
                "rule_id": result["rule_id"],
                "current_status": result["status"],
                "activation_reason": result["activation_reason"],
                "requirement": rule["requirement"],
                "check_kinds": check_kinds,
                "suggested_evaluator": (
                    "human_or_user"
                    if {"semantic", "manual"} & set(check_kinds)
                    else "tool_or_human"
                ),
                "deterministic_findings": result["findings"],
            }
        )
    return {
        "worklist_version": 1,
        "notice": (
            "This is a review worklist, not compliance evidence. Do not convert "
            "items to PASS without inspecting the manuscript and cited artifacts."
        ),
        "items": items,
    }


def run_validation(
    context_path: Path,
    project: Path,
    output_dir: Path,
    evidence_path: Path | None = None,
) -> dict[str, Any]:
    script_dir = Path(__file__).resolve().parent
    policy_dir = script_dir.parent
    refs = policy_dir / "references"
    hard_path = refs / "hard-rules.yaml"
    soft_path = refs / "soft-rules.yaml"
    profiles_path = refs / "profiles.yaml"
    decisions_path = refs / "decision-baseline.yaml"
    policy_sets_path = refs / "policy-sets.yaml"

    errors = validate_registry(
        hard_path, soft_path, profiles_path, decisions_path, policy_sets_path
    )
    if errors:
        raise ValueError("registry validation failed: " + "; ".join(errors))
    if not project.is_dir():
        raise ValueError(f"not a project directory: {project}")

    hard = load_yaml(hard_path)
    context = load_yaml(context_path)
    resolution = resolve_policy(
        context,
        hard,
        load_yaml(soft_path),
        load_yaml(profiles_path),
        load_yaml(policy_sets_path),
    )
    active_hard_ids = {item["id"] for item in resolution["active_hard"]}
    stage = resolution["context"].get("submission_stage", "draft")
    project_files = select_project_files(
        project,
        resolution["context"].get("primary_tex"),
        resolution["context"].get("additional_tex", []),
    )
    findings, assessed = lint_project(
        project,
        stage,
        "STRUCT.SECTION_COUNT_PROFILE" in active_hard_ids,
        active_hard_ids,
        project_files.tex_paths,
        project_files.bib_paths,
        project_files.primary_tex,
    )

    evidence = load_yaml(evidence_path) if evidence_path else None
    artifact_coverage: dict[str, set[str]] = {}
    if evidence and evidence.get("artifacts"):
        artifact_findings, artifact_assessed, artifact_coverage = check_artifacts(
            project, evidence["artifacts"], project_files.tex_paths
        )
        findings.extend(artifact_findings)
        assessed.update(artifact_assessed)

    # Artifact inspection knows about the whole registry. Only active hard rules
    # are applicable in this resolved context and may enter assessment/counts.
    findings = [item for item in findings if item.rule_id in active_hard_ids]
    assessed &= active_hard_ids

    assessment = assess_compliance(
        resolution,
        hard,
        evidence,
        findings,
        assessed,
        artifact_coverage,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    discovery = discover_artifacts(project, project_files.tex_paths)
    _write_yaml(output_dir / "artifact-manifest-skeleton.yaml", discovery)
    _write_yaml(
        output_dir / "artifact-discovery-summary.yaml",
        compare_discovery(
            discovery["artifacts"], evidence.get("artifacts", []) if evidence else []
        ),
    )
    _write_yaml(output_dir / "resolved-policy.yaml", resolution)
    confirmed_artifacts = evidence.get("artifacts", []) if evidence else []
    worklist_artifacts = confirmed_artifacts or discovery["artifacts"]
    soft_worklist = build_soft_review_worklist(
        resolution,
        project,
        worklist_artifacts,
        "confirmed_evidence" if confirmed_artifacts else "auto_discovery",
        project_files.primary_tex_paths,
        project_files.primary_tex,
    )
    _write_yaml(output_dir / "soft-review-worklist.yaml", soft_worklist)
    _write_yaml(output_dir / "initial-assessment.yaml", assessment)
    _write_yaml(output_dir / "evidence-worklist.yaml", build_evidence_worklist(assessment, hard))
    _write_yaml(
        output_dir / "deterministic-findings.yaml",
        {"version": 1, "findings": [asdict(item) for item in findings]},
    )
    unused_entries = (
        unused_bibtex_entries(
            project, list(project_files.tex_paths), list(project_files.bib_paths)
        )
        if "CITE.UNUSED_KEYS_REPORTED" in active_hard_ids
        else []
    )
    _write_yaml(
        output_dir / "unused-bibtex-keys.yaml",
        {
            "version": 1,
            "active": "CITE.UNUSED_KEYS_REPORTED" in active_hard_ids,
            "keys": sorted({str(item["key"]) for item in unused_entries}),
            "entries": unused_entries,
        },
    )
    failing_results = [
        item for item in assessment["hard_results"] if item["status"] == "FAIL"
    ]
    deterministic_rule_ids = sorted({item.rule_id for item in findings})
    agent_rule_ids = sorted(
        {
            item["rule_id"]
            for item in failing_results
            if item.get("basis") == "supplied_evidence"
            and (item.get("evidence_record") or {}).get("evaluator") == "agent"
        }
    )
    affected_artifacts = sorted(
        {
            item.path[len("<artifact:") : -1]
            for item in findings
            if item.path.startswith("<artifact:") and item.path.endswith(">")
        }
    )
    manifest = {
        "validation_runner": str(Path(__file__).resolve()),
        "policy_bundle": str(policy_dir.resolve()),
        "project": str(project.resolve()),
        "context": str(context_path.resolve()),
        "evidence": str(evidence_path.resolve()) if evidence_path else None,
        "active_system_skills_modified": False,
        "primary_tex": project_files.primary_tex.relative_to(project).as_posix(),
        "selected_tex_files": [
            path.relative_to(project).as_posix() for path in project_files.tex_paths
        ],
        "selected_bib_files": [
            path.relative_to(project).as_posix() for path in project_files.bib_paths
        ],
        "finding_instance_count": len(findings),
        "deterministic_failing_rule_count": len(deterministic_rule_ids),
        "deterministic_failing_rule_ids": deterministic_rule_ids,
        "affected_artifact_count": len(affected_artifacts),
        "affected_artifact_ids": affected_artifacts,
        "agent_failing_rule_count": len(agent_rule_ids),
        "agent_failing_rule_ids": agent_rule_ids,
        "total_failing_rule_count": len(failing_results),
        "unverified_rule_count": assessment["hard_summary"]["UNVERIFIED"],
        "unused_bibtex_key_count": len(unused_entries),
        "soft_worklist_active_rule_count": soft_worklist["coverage"][
            "active_soft_rule_count"
        ],
        "soft_worklist_unmapped_rule_count": len(
            soft_worklist["coverage"]["unmapped_rule_ids"]
        ),
        "readiness_status": assessment["readiness"]["status"],
    }
    _write_yaml(output_dir / "validation-manifest.yaml", manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("context", type=Path)
    parser.add_argument("project", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        manifest = run_validation(
            args.context.resolve(),
            args.project.resolve(),
            args.output_dir.resolve(),
            args.evidence.resolve() if args.evidence else None,
        )
    except ValueError as exc:
        print(f"Project validation failed: {exc}", file=sys.stderr)
        return 2
    if args.as_json:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
    else:
        print(f"Validation artifacts written to {args.output_dir.resolve()}")
        print(f"Finding instances: {manifest['finding_instance_count']}")
        print(
            "Deterministic failing rules: "
            f"{manifest['deterministic_failing_rule_count']}"
        )
        print(f"Affected artifacts: {manifest['affected_artifact_count']}")
        print(f"Total failing rules: {manifest['total_failing_rule_count']}")
        print(f"Unverified rules: {manifest['unverified_rule_count']}")
        print(f"Unused BibTeX keys: {manifest['unused_bibtex_key_count']}")
        print(
            "Soft worklist rules: "
            f"{manifest['soft_worklist_active_rule_count']} "
            f"({manifest['soft_worklist_unmapped_rule_count']} unmapped)"
        )
        print(f"Readiness: {manifest['readiness_status']}")
    return 1 if manifest["total_failing_rule_count"] else 0


if __name__ == "__main__":
    sys.exit(main())

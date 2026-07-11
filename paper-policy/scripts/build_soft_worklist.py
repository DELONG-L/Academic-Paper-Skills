#!/usr/bin/env python3
"""Build a section-aware review worklist for active soft paper-policy rules."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from lint_project import iter_tex_lines, primary_manuscript_tex_paths


FEATURE_TARGETS = {
    "abstract": {"abstract"},
    "introduction": {"introduction"},
    "contribution_list": {"introduction"},
    "related_work": {"related_work"},
    "evaluation_section": {"results"},
    "conclusion": {"conclusion"},
    "threats_to_validity": {"conclusion"},
    "limitations_content": {"conclusion"},
    "related_work_table": {"tables"},
    "data_table": {"tables"},
    "result_table": {"tables"},
    "paper_figure": {"figures"},
    "data_figure": {"figures"},
    "conceptual_figure": {"figures"},
    "latex_manuscript": {"whole_manuscript"},
    "paper_prose": {"whole_manuscript"},
}
SPECIAL_TARGET_TITLES = {
    "whole_manuscript": "Whole manuscript and structure",
    "tables": "Tables",
    "figures": "Figures",
    "citations": "Citations and bibliography",
    "workflow": "Review workflow and policy",
}


def _section_target(title: str) -> str:
    lowered = re.sub(r"\\[A-Za-z]+\s*", "", title).lower()
    if "introduction" in lowered:
        return "introduction"
    if "related work" in lowered or "prior work" in lowered:
        return "related_work"
    if any(token in lowered for token in ("experiment", "result", "evaluation")):
        return "results"
    if any(token in lowered for token in ("conclusion", "summary")):
        return "conclusion"
    if any(token in lowered for token in ("threat", "limitation")):
        return "conclusion"
    if any(token in lowered for token in ("method", "formulation", "approach", "design")):
        return "method"
    if "discussion" in lowered:
        return "discussion"
    if "background" in lowered:
        return "background"
    return "other"


def discover_primary_sections(
    root: Path,
    tex_paths: list[Path] | tuple[Path, ...] | None = None,
    primary_tex_path: Path | None = None,
) -> list[dict[str, Any]]:
    """Locate the primary manuscript's abstract and top-level sections."""
    root = root.resolve()
    tex_paths = sorted(root.rglob("*.tex")) if tex_paths is None else sorted(tex_paths)
    sections: list[dict[str, Any]] = []
    for path in primary_manuscript_tex_paths(root, tex_paths, primary_tex_path):
        relative = path.resolve().relative_to(root).as_posix()
        abstract_recorded = False
        for line, text in iter_tex_lines(path):
            if not abstract_recorded and re.search(r"\\begin\{abstract\}", text):
                sections.append(
                    {
                        "id": "abstract",
                        "target": "abstract",
                        "title": "Abstract",
                        "locators": [{"path": relative, "line": line}],
                    }
                )
                abstract_recorded = True
            for match in re.finditer(r"\\section\*?\{([^{}]+)\}", text):
                title = match.group(1).strip()
                base = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "section"
                sections.append(
                    {
                        "id": base,
                        "target": _section_target(title),
                        "title": title,
                        "locators": [{"path": relative, "line": line}],
                    }
                )
    seen: dict[str, int] = {}
    for section in sections:
        base = section["id"]
        seen[base] = seen.get(base, 0) + 1
        if seen[base] > 1:
            section["id"] = f"{base}-{seen[base]}"
    return sections


def _rule_targets(rule: dict[str, Any]) -> set[str]:
    features = set(rule.get("features", []))
    if features:
        targets = {
            target
            for feature in features
            for target in FEATURE_TARGETS.get(feature, {"whole_manuscript"})
        }
        return targets
    rule_id = rule["id"]
    artifacts = set(rule.get("artifacts", []))
    scopes = set(rule.get("scope", []))
    if rule_id.startswith(("PROFILE.", "OUTPUT.", "REVIEW.")):
        return {"workflow"}
    if rule_id.startswith("TABLE."):
        return {"tables"}
    if rule_id.startswith("FIG."):
        return {"figures"}
    if "figure" in artifacts and not (artifacts & {"prose", "tex"}):
        return {"figures"}
    if "table" in artifacts and not (artifacts & {"prose", "tex"}):
        return {"tables"}
    if "bibtex" in artifacts and not (artifacts & {"prose", "tex"}):
        return {"citations"}
    if "paper_outline" in artifacts or artifacts == {"policy"}:
        return {"whole_manuscript"}
    if artifacts & {"prose", "tex"} and scopes & {"writing", "review", "citations"}:
        return {"all_sections"}
    if "workflow" in scopes:
        return {"workflow"}
    return {"whole_manuscript"}


def build_soft_review_worklist(
    resolution: dict[str, Any],
    root: Path,
    artifacts: list[dict[str, Any]] | None = None,
    artifact_inventory_basis: str = "auto_discovery",
    tex_paths: list[Path] | tuple[Path, ...] | None = None,
    primary_tex_path: Path | None = None,
) -> dict[str, Any]:
    """Group every active soft rule by concrete manuscript review target."""
    active_rules = resolution.get("active_soft", [])
    rules_by_id = {rule["id"]: {**rule, "worklist_status": "PENDING"} for rule in active_rules}
    target_rules: dict[str, set[str]] = {}
    global_section_rules: set[str] = set()
    for rule in active_rules:
        for target in _rule_targets(rule):
            if target == "all_sections":
                global_section_rules.add(rule["id"])
            else:
                target_rules.setdefault(target, set()).add(rule["id"])

    groups: list[dict[str, Any]] = []
    sections = discover_primary_sections(root, tex_paths, primary_tex_path)
    present_targets = {section["target"] for section in sections}
    for section in sections:
        targeted = target_rules.get(section["target"], set())
        groups.append(
            {
                "id": section["id"],
                "kind": "section",
                "title": section["title"],
                "locators": section["locators"],
                "global_rule_ids": sorted(global_section_rules),
                "targeted_rule_ids": sorted(targeted),
                "rule_ids": sorted(global_section_rules | targeted),
            }
        )

    logical_targets = {
        target
        for target in target_rules
        if target not in SPECIAL_TARGET_TITLES and target not in present_targets
    }
    for target in sorted(logical_targets):
        groups.append(
            {
                "id": target,
                "kind": "section",
                "title": target.replace("_", " ").title(),
                "locators": [],
                "global_rule_ids": sorted(global_section_rules),
                "targeted_rule_ids": sorted(target_rules[target]),
                "rule_ids": sorted(global_section_rules | target_rules[target]),
            }
        )

    artifacts = artifacts or []
    for target, title in SPECIAL_TARGET_TITLES.items():
        rule_ids = target_rules.get(target, set())
        if not rule_ids:
            continue
        artifact_ids = sorted(
            item["id"]
            for item in artifacts
            if (target == "tables" and item.get("kind") == "table")
            or (target == "figures" and item.get("kind") == "figure")
        )
        groups.append(
            {
                "id": target.replace("_", "-"),
                "kind": "artifact" if target in {"tables", "figures"} else "cross_cutting",
                "title": title,
                "locators": [],
                "artifact_ids": artifact_ids,
                "global_rule_ids": [],
                "targeted_rule_ids": sorted(rule_ids),
                "rule_ids": sorted(rule_ids),
            }
        )

    covered = {rule_id for group in groups for rule_id in group["rule_ids"]}
    missing = sorted(set(rules_by_id) - covered)
    return {
        "version": 1,
        "notice": (
            "This is a section-aware review plan, not soft-rule evidence. Record "
            "APPLIED, ADAPTED, or SKIPPED with rationale in compliance evidence only "
            "after inspecting the named section or artifact."
        ),
        "artifact_inventory_basis": artifact_inventory_basis,
        "rules": [rules_by_id[rule_id] for rule_id in sorted(rules_by_id)],
        "groups": groups,
        "coverage": {
            "active_soft_rule_count": len(rules_by_id),
            "covered_soft_rule_count": len(covered),
            "unmapped_rule_ids": missing,
        },
    }

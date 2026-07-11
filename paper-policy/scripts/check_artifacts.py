#!/usr/bin/env python3
"""Validate figure/table artifact manifests and run reliable source checks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from lint_project import Finding
from validate_registry import load_yaml


ARTIFACT_KINDS = {"figure", "table"}
DISCOVERY_STATUSES = {"confirmed", "needs_confirmation"}
ARTIFACT_TYPES = {
    "paper_figure", "data_figure", "conceptual_figure",
    "related_work_table", "data_table", "result_table", "paper_table",
}
FILE_FIELDS = {"outputs", "scripts", "source_data", "previews", "table_sources"}
VECTOR_FORMATS = {".pdf", ".svg"}
PAPER_FIGURE_FORMATS = VECTOR_FORMATS | {".png", ".tif", ".tiff"}
FILLED_PARTIAL_MARKER_PATTERNS = [
    re.compile(
        r"\\(?:newcommand|renewcommand)\s*\{\\pmark\}"
        r"[\s\S]{0,240}?\\ding\s*\{108\}"
    ),
    re.compile(r"\\def\s*\\pmark[\s\S]{0,240}?\\ding\s*\{108\}"),
]
TABLE_ENV_PATTERN = re.compile(
    r"\\begin\{(?P<env>table\*?)\}(?P<body>[\s\S]*?)\\end\{(?P=env)\}"
)
PUBLIC_DEFAULT_ARTIFACT_RULE_IDS = {
    "FIG.SOURCE_DATA_REQUIRED",
    "FIG.NO_INVENTED_COMPONENTS",
    "FIG.FINAL_WIDTH_READABLE",
    "FIG.FINAL_EXPORT_ACCESSIBILITY",
    "FIG.TRACEABLE_SCRIPT",
    "TABLE.PROPOSED_ROW_GROUNDED",
    "TABLE.VALUES_GROUNDED",
}
STRICT_HOUSE_ARTIFACT_RULE_IDS = {
    "FIG.NO_IN_FIGURE_TITLE",
    "FIG.CONCEPT_HOUSE_STYLE",
    "TABLE.BOOKTABS_FINAL",
    "TABLE.FINAL_TARGET_WIDTH",
    "RELATED.COMPARISON_REQUIRED",
    "TABLE.CANONICAL_RELATED_MARKERS",
}


def validate_artifact_records(records: Any) -> list[str]:
    errors: list[str] = []
    if records is None:
        return errors
    if not isinstance(records, list):
        return ["evidence.artifacts: expected list"]
    seen: set[str] = set()
    for index, record in enumerate(records):
        where = f"evidence.artifacts[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{where}: expected mapping")
            continue
        unknown = sorted(
            set(record)
            - {
                "id", "kind", "artifact_types", "claim", "latex_label",
                "discovery_status", "files",
            }
        )
        if unknown:
            errors.append(f"{where}: unknown fields {', '.join(unknown)}")
        artifact_id = record.get("id")
        if not isinstance(artifact_id, str) or not re.fullmatch(
            r"[a-z0-9]+(?:-[a-z0-9]+)*", artifact_id
        ):
            errors.append(f"{where}.id: invalid artifact ID {artifact_id!r}")
        elif artifact_id in seen:
            errors.append(f"{where}.id: duplicate artifact ID {artifact_id}")
        else:
            seen.add(artifact_id)
        kind = record.get("kind")
        if kind not in ARTIFACT_KINDS:
            errors.append(f"{where}.kind: expected figure or table")
        discovery_status = record.get("discovery_status", "confirmed")
        if discovery_status not in DISCOVERY_STATUSES:
            errors.append(
                f"{where}.discovery_status: invalid value {discovery_status!r}"
            )
        elif discovery_status != "confirmed":
            errors.append(
                f"{where}.discovery_status: auto-discovered record must be reviewed and changed to confirmed before use as evidence"
            )
        latex_label = record.get("latex_label")
        if kind == "table" and (
            not isinstance(latex_label, str) or not latex_label.strip()
        ):
            errors.append(f"{where}.latex_label: required non-empty string for tables")
        if kind == "figure" and latex_label is not None:
            errors.append(f"{where}.latex_label: allowed only for tables")
        artifact_types = record.get("artifact_types")
        if not isinstance(artifact_types, list) or not artifact_types:
            errors.append(f"{where}.artifact_types: expected non-empty list")
        else:
            invalid = sorted(set(artifact_types) - ARTIFACT_TYPES)
            if invalid:
                errors.append(f"{where}.artifact_types: invalid values {invalid}")
        if not isinstance(record.get("claim"), str) or not record.get("claim", "").strip():
            errors.append(f"{where}.claim: required non-empty string")
        files = record.get("files")
        if not isinstance(files, dict):
            errors.append(f"{where}.files: expected mapping")
            continue
        unknown_files = sorted(set(files) - FILE_FIELDS)
        if unknown_files:
            errors.append(f"{where}.files: unknown fields {', '.join(unknown_files)}")
        for field, values in files.items():
            if not isinstance(values, list):
                errors.append(f"{where}.files.{field}: expected list")
            elif any(not isinstance(value, str) or not value for value in values):
                errors.append(f"{where}.files.{field}: entries must be non-empty strings")
    return errors


def _path(root: Path, value: str) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else root / path


def _all_exist(root: Path, values: list[str]) -> tuple[bool, list[str]]:
    missing = [value for value in values if not _path(root, value).is_file()]
    return bool(values) and not missing, missing


def _read_project_tex(
    root: Path, tex_paths: list[Path] | tuple[Path, ...] | None = None
) -> str:
    selected = sorted(root.rglob("*.tex")) if tex_paths is None else sorted(tex_paths)
    return "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in selected
        if path.is_file()
    )


def _table_blocks_by_label(root: Path, values: list[str], label: str) -> list[str]:
    """Return exact table/table* environments containing the requested label."""
    label_pattern = re.compile(rf"\\label\s*\{{\s*{re.escape(label)}\s*\}}")
    blocks: list[str] = []
    for value in values:
        path = _path(root, value)
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in TABLE_ENV_PATTERN.finditer(text):
            block = match.group(0)
            if label_pattern.search(block):
                blocks.append(block)
    return blocks


def _has_filled_partial_marker(text: str) -> bool:
    return any(pattern.search(text) for pattern in FILLED_PARTIAL_MARKER_PATTERNS)


def check_artifacts(
    root: Path,
    records: list[dict[str, Any]],
    project_tex_paths: list[Path] | tuple[Path, ...] | None = None,
) -> tuple[list[Finding], set[str], dict[str, set[str]]]:
    errors = validate_artifact_records(records)
    if errors:
        raise ValueError("; ".join(errors))
    root = root.resolve()
    findings: list[Finding] = []
    candidates: dict[str, set[str]] = {}
    complete: dict[str, set[str]] = {}

    def candidate(rule_id: str, artifact_id: str) -> None:
        candidates.setdefault(rule_id, set()).add(artifact_id)

    def passed(rule_id: str, artifact_id: str) -> None:
        complete.setdefault(rule_id, set()).add(artifact_id)

    def fail(rule_id: str, artifact_id: str, message: str) -> None:
        findings.append(Finding(rule_id, f"<artifact:{artifact_id}>", 0, message))

    for record in records:
        artifact_id = record["id"]
        kind = record["kind"]
        types = set(record["artifact_types"])
        files = {field: record["files"].get(field, []) for field in FILE_FIELDS}

        if kind == "figure":
            if "paper_figure" in types:
                for rule_id in (
                    "FIG.NO_IN_FIGURE_TITLE",
                    "FIG.FINAL_WIDTH_READABLE",
                    "FIG.FINAL_EXPORT_ACCESSIBILITY",
                ):
                    candidate(rule_id, artifact_id)

                outputs_ok, missing_outputs = _all_exist(root, files["outputs"])
                allowed_outputs = [
                    value for value in files["outputs"]
                    if Path(value).suffix.lower() in PAPER_FIGURE_FORMATS
                ]
                if missing_outputs:
                    fail(
                        "FIG.FINAL_EXPORT_ACCESSIBILITY",
                        artifact_id,
                        f"declared output files are missing: {', '.join(missing_outputs)}",
                    )
                elif not allowed_outputs:
                    fail(
                        "FIG.FINAL_EXPORT_ACCESSIBILITY",
                        artifact_id,
                        "no allowed PDF, SVG, PNG, or TIFF output is declared",
                    )
                elif outputs_ok:
                    passed("FIG.FINAL_EXPORT_ACCESSIBILITY", artifact_id)

            if "data_figure" in types:
                for rule_id in ("FIG.SOURCE_DATA_REQUIRED", "FIG.TRACEABLE_SCRIPT"):
                    candidate(rule_id, artifact_id)
                data_ok, missing_data = _all_exist(root, files["source_data"])
                scripts_ok, missing_scripts = _all_exist(root, files["scripts"])
                if missing_data or not files["source_data"]:
                    fail(
                        "FIG.SOURCE_DATA_REQUIRED",
                        artifact_id,
                        "source data are missing or not declared"
                        + (f": {', '.join(missing_data)}" if missing_data else ""),
                    )
                elif data_ok and scripts_ok:
                    passed("FIG.SOURCE_DATA_REQUIRED", artifact_id)
                if missing_scripts or not files["scripts"]:
                    fail(
                        "FIG.TRACEABLE_SCRIPT",
                        artifact_id,
                        "generation scripts are missing or not declared"
                        + (f": {', '.join(missing_scripts)}" if missing_scripts else ""),
                    )
                elif scripts_ok:
                    passed("FIG.TRACEABLE_SCRIPT", artifact_id)

                if files["outputs"] and not any(
                    Path(value).suffix.lower() in VECTOR_FORMATS for value in files["outputs"]
                ):
                    fail(
                        "FIG.FINAL_EXPORT_ACCESSIBILITY",
                        artifact_id,
                        "data figure has no declared PDF or SVG vector output",
                    )

            if "conceptual_figure" in types:
                candidate("FIG.NO_INVENTED_COMPONENTS", artifact_id)
                candidate("FIG.CONCEPT_HOUSE_STYLE", artifact_id)

        if kind == "table":
            candidate("TABLE.BOOKTABS_FINAL", artifact_id)
            candidate("TABLE.FINAL_TARGET_WIDTH", artifact_id)
            sources = files["table_sources"] or [
                value for value in files["outputs"] if Path(value).suffix.lower() == ".tex"
            ]
            latex_label = record["latex_label"]
            table_blocks = _table_blocks_by_label(root, sources, latex_label)
            source_text = table_blocks[0] if len(table_blocks) == 1 else ""
            if len(table_blocks) != 1:
                fail(
                    "TABLE.BOOKTABS_FINAL",
                    artifact_id,
                    f"expected exactly one table/table* environment with label {latex_label!r}; found {len(table_blocks)}",
                )
            else:
                if all(token in source_text for token in ("\\toprule", "\\midrule", "\\bottomrule")):
                    passed("TABLE.BOOKTABS_FINAL", artifact_id)
                else:
                    fail(
                        "TABLE.BOOKTABS_FINAL",
                        artifact_id,
                        "table source does not contain top, mid, and bottom booktabs rules",
                    )

            if "related_work_table" in types:
                for rule_id in (
                    "RELATED.COMPARISON_REQUIRED",
                    "TABLE.PROPOSED_ROW_GROUNDED",
                    "TABLE.CANONICAL_RELATED_MARKERS",
                ):
                    candidate(rule_id, artifact_id)
                if source_text:
                    marker_tokens = ("\\cmark", "\\pmark", "\\xmark")
                    marker_definition_text = source_text + "\n" + _read_project_tex(
                        root, project_tex_paths
                    )
                    if (
                        all(token in source_text for token in marker_tokens)
                        and _has_filled_partial_marker(marker_definition_text)
                    ):
                        passed("TABLE.CANONICAL_RELATED_MARKERS", artifact_id)
                    else:
                        fail(
                            "TABLE.CANONICAL_RELATED_MARKERS",
                            artifact_id,
                            "related-work table must use cmark/pmark/xmark and define pmark as the filled pifont circle \\ding{108}",
                        )
                else:
                    fail(
                        "TABLE.CANONICAL_RELATED_MARKERS",
                        artifact_id,
                        f"cannot inspect related-work markers because label {latex_label!r} did not resolve to exactly one table environment",
                    )

            if types & {"data_table", "result_table"}:
                candidate("TABLE.VALUES_GROUNDED", artifact_id)
                data_ok, missing_data = _all_exist(root, files["source_data"])
                if missing_data or not files["source_data"]:
                    fail(
                        "TABLE.VALUES_GROUNDED",
                        artifact_id,
                        "table source data are missing or not declared"
                        + (f": {', '.join(missing_data)}" if missing_data else ""),
                    )
                elif data_ok:
                    passed("TABLE.VALUES_GROUNDED", artifact_id)

    assessed = {
        rule_id
        for rule_id, artifact_ids in candidates.items()
        if artifact_ids and complete.get(rule_id, set()) == artifact_ids
    }
    return findings, assessed, candidates


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path, help="compliance-evidence.yaml")
    parser.add_argument("--root", type=Path, help="artifact path root; defaults to evidence directory")
    parser.add_argument("--format", choices=("yaml", "json"), default="yaml")
    parser.add_argument(
        "--strict-house-style",
        action="store_true",
        help="include checks owned by the optional strict-house-style set",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        evidence = load_yaml(args.evidence)
        records = evidence.get("artifacts", [])
        root = (args.root or args.evidence.parent).resolve()
        findings, assessed, coverage = check_artifacts(root, records)
    except ValueError as exc:
        print(f"Artifact assessment failed: {exc}", file=sys.stderr)
        return 2
    enabled = set(PUBLIC_DEFAULT_ARTIFACT_RULE_IDS)
    if args.strict_house_style:
        enabled.update(STRICT_HOUSE_ARTIFACT_RULE_IDS)
    findings = [finding for finding in findings if finding.rule_id in enabled]
    assessed &= enabled
    coverage = {key: value for key, value in coverage.items() if key in enabled}
    result = {
        "active_artifact_rule_ids": sorted(enabled),
        "findings": [finding.__dict__ for finding in findings],
        "assessed_rules": sorted(assessed),
        "coverage": {key: sorted(value) for key, value in sorted(coverage.items())},
    }
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(yaml.safe_dump(result, sort_keys=False, allow_unicode=True), end="")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())

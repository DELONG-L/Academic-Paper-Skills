#!/usr/bin/env python3
"""Discover LaTeX figures/tables and emit a guarded evidence-manifest skeleton."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml

from project_files import select_project_files


ENV_PATTERN = re.compile(
    r"\\begin\{(?P<env>figure\*?|table\*?)\}(?P<body>[\s\S]*?)"
    r"\\end\{(?P=env)\}"
)
LABEL_PATTERN = re.compile(r"\\label\s*\{\s*([^{}]+?)\s*\}")
INCLUDE_PATTERN = re.compile(
    r"\\includegraphics(?:\s*\[[^\]]*\])?\s*\{\s*([^{}]+?)\s*\}"
)
CONCEPT_HINTS = {
    "architecture", "framework", "overview", "pipeline", "system", "workflow",
}
RESULT_HINTS = {
    "ablation", "audit", "diagnostic", "evaluation", "evidence", "metric",
    "result", "runtime", "scale", "sensitivity",
}
SETUP_TABLE_HINTS = {
    "condition famil", "dataset", "definition", "evaluation asset", "inventory",
    "metric definition", "setup",
}
GRAPHIC_EXTENSIONS = (".pdf", ".svg", ".png", ".tif", ".tiff", ".eps")


def _strip_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        cut = len(line)
        for index, char in enumerate(line):
            if char == "%" and (index == 0 or line[index - 1] != "\\"):
                cut = index
                break
        lines.append(line[:cut])
    return "\n".join(lines)


def _balanced_argument(text: str, command: str) -> str | None:
    """Return the first brace-balanced mandatory argument for a command."""
    match = re.search(rf"\\{re.escape(command)}(?:\s*\[[^\]]*\])?\s*\{{", text)
    if not match:
        return None
    start = match.end()
    depth = 1
    for index in range(start, len(text)):
        char = text[index]
        if char == "{" and (index == 0 or text[index - 1] != "\\"):
            depth += 1
        elif char == "}" and (index == 0 or text[index - 1] != "\\"):
            depth -= 1
            if depth == 0:
                return text[start:index].strip()
    return None


def _slug(value: str) -> str:
    value = re.sub(r"^(?:fig|tab|table):", "", value.strip(), flags=re.IGNORECASE)
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "unlabeled-artifact"


def _unique_id(base: str, seen: set[str]) -> str:
    candidate = base
    suffix = 2
    while candidate in seen:
        candidate = f"{base}-{suffix}"
        suffix += 1
    seen.add(candidate)
    return candidate


def _relative_tex_path(root: Path, tex_path: Path) -> str:
    return tex_path.resolve().relative_to(root.resolve()).as_posix()


def _graphic_path(root: Path, tex_path: Path, raw: str) -> str:
    """Preserve a usable project-relative graphic path and infer extensions."""
    raw_path = Path(raw)
    candidates = [root / raw_path, tex_path.parent / raw_path]
    expanded: list[Path] = []
    for candidate in candidates:
        expanded.append(candidate)
        if not candidate.suffix:
            expanded.extend(candidate.with_suffix(ext) for ext in GRAPHIC_EXTENSIONS)
    existing = next((item for item in expanded if item.is_file()), None)
    if existing is not None:
        try:
            return existing.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            return str(existing.resolve())
    return raw_path.as_posix()


def _figure_types(label: str, caption: str, outputs: list[str]) -> list[str]:
    haystack = " ".join([label, caption, *outputs]).lower()
    if any(hint in haystack for hint in CONCEPT_HINTS):
        return ["paper_figure", "conceptual_figure"]
    return ["paper_figure", "data_figure"]


def _table_types(label: str, caption: str) -> list[str]:
    haystack = f"{label} {caption}".lower()
    types = ["paper_table"]
    if "related" in haystack or "position" in haystack:
        types.append("related_work_table")
    elif any(hint in haystack for hint in SETUP_TABLE_HINTS):
        types.append("data_table")
    elif any(hint in haystack for hint in RESULT_HINTS):
        types.extend(["data_table", "result_table"])
    return types


def discover_artifacts(
    root: Path, tex_paths: list[Path] | tuple[Path, ...] | None = None
) -> dict[str, Any]:
    """Return evidence-shaped records that require explicit confirmation."""
    root = root.resolve()
    records: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    selected_tex = sorted(root.rglob("*.tex")) if tex_paths is None else sorted(tex_paths)
    for tex_path in selected_tex:
        text = _strip_comments(
            tex_path.read_text(encoding="utf-8", errors="replace")
        )
        for ordinal, match in enumerate(ENV_PATTERN.finditer(text), start=1):
            env = match.group("env")
            body = match.group("body")
            label_match = LABEL_PATTERN.search(body)
            label = label_match.group(1).strip() if label_match else ""
            caption = _balanced_argument(body, "caption") or ""
            fallback = f"{tex_path.stem}-{env.rstrip('*')}-{ordinal}"
            artifact_id = _unique_id(_slug(label or fallback), seen_ids)
            source = _relative_tex_path(root, tex_path)
            if env.startswith("figure"):
                outputs = [
                    _graphic_path(root, tex_path, item.strip())
                    for item in INCLUDE_PATTERN.findall(body)
                ]
                record = {
                    "id": artifact_id,
                    "kind": "figure",
                    "artifact_types": _figure_types(label, caption, outputs),
                    "claim": caption or "Confirm the paper claim supported by this figure.",
                    "discovery_status": "needs_confirmation",
                    "files": {
                        "outputs": outputs,
                        "scripts": [],
                        "source_data": [],
                        "previews": [],
                        "table_sources": [],
                    },
                }
            else:
                record = {
                    "id": artifact_id,
                    "kind": "table",
                    "artifact_types": _table_types(label, caption),
                    "claim": caption or "Confirm the paper claim supported by this table.",
                    "latex_label": label,
                    "discovery_status": "needs_confirmation",
                    "files": {
                        "outputs": [],
                        "scripts": [],
                        "source_data": [],
                        "previews": [],
                        "table_sources": [source],
                    },
                }
            records.append(record)
    return {
        "version": 1,
        "notice": (
            "Auto-discovered records are inventory hints, not compliance evidence. "
            "Review each record, correct its type/claim/files, then change "
            "discovery_status to confirmed before copying it into evidence."
        ),
        "artifacts": records,
        "hard_results": [],
        "soft_results": [],
    }


def compare_discovery(
    discovered: list[dict[str, Any]], confirmed: list[dict[str, Any]]
) -> dict[str, Any]:
    """Compare discovered records with confirmed evidence using stable LaTeX clues."""
    table_labels = {
        item.get("latex_label")
        for item in confirmed
        if item.get("kind") == "table" and item.get("latex_label")
    }
    figure_outputs = {
        value
        for item in confirmed
        if item.get("kind") == "figure"
        for value in item.get("files", {}).get("outputs", [])
    }
    discovered_table_labels = {
        item.get("latex_label")
        for item in discovered
        if item.get("kind") == "table" and item.get("latex_label")
    }
    discovered_figure_outputs = {
        value
        for item in discovered
        if item.get("kind") == "figure"
        for value in item.get("files", {}).get("outputs", [])
    }
    missing: list[dict[str, str]] = []
    for item in discovered:
        if item["kind"] == "table":
            matched = item.get("latex_label") in table_labels
            identity = item.get("latex_label", "")
        else:
            outputs = item.get("files", {}).get("outputs", [])
            matched = bool(set(outputs) & figure_outputs)
            identity = outputs[0] if outputs else item["id"]
        if not matched:
            missing.append({"id": item["id"], "kind": item["kind"], "identity": identity})
    stale_or_external: list[dict[str, str]] = []
    for item in confirmed:
        if item.get("kind") == "table":
            identity = item.get("latex_label", "")
            matched = identity in discovered_table_labels
        else:
            outputs = item.get("files", {}).get("outputs", [])
            identity = outputs[0] if outputs else item.get("id", "")
            matched = bool(set(outputs) & discovered_figure_outputs)
        if not matched:
            stale_or_external.append(
                {"id": item.get("id", ""), "kind": item.get("kind", ""), "identity": identity}
            )
    return {
        "version": 1,
        "discovered_artifact_count": len(discovered),
        "confirmed_evidence_artifact_count": len(confirmed),
        "missing_from_confirmed_evidence_count": len(missing),
        "missing_from_confirmed_evidence": missing,
        "confirmed_not_discovered_count": len(stale_or_external),
        "confirmed_not_discovered": stale_or_external,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--primary-tex")
    parser.add_argument("--additional-tex", action="append", default=[])
    args = parser.parse_args()
    if not args.project.is_dir():
        parser.error(f"not a project directory: {args.project}")
    try:
        selected = select_project_files(
            args.project, args.primary_tex, args.additional_tex
        )
    except ValueError as exc:
        parser.error(str(exc))
    result = discover_artifacts(args.project, selected.tex_paths)
    rendered = yaml.safe_dump(result, sort_keys=False, allow_unicode=True)
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Create and verify file snapshots for evidence; never decide compliance."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any


def source_path(root: Path, value: str) -> Path:
    path = Path(value).expanduser()
    return (path if path.is_absolute() else root / path).resolve()


def file_digest(path: Path) -> str:
    if not path.is_file():
        raise OSError(f"not a readable file: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot_sources(root: Path, paths: list[str]) -> list[dict[str, str]]:
    """Call after inspection; include the manuscript and all relied-on sources."""
    return [
        {"path": path, "sha256": file_digest(source_path(root, path))}
        for path in dict.fromkeys(paths)
    ]


def validate_snapshots(value: Any, where: str) -> list[str]:
    if not isinstance(value, list) or not value:
        return [f"{where}: required non-empty list of path/sha256 snapshots"]
    errors = []
    seen = set()
    for index, item in enumerate(value):
        label = f"{where}[{index}]"
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            errors.append(f"{label}: expected path and sha256 only")
            continue
        path = item["path"]
        if not isinstance(path, str) or not path.strip():
            errors.append(f"{label}.path: required non-empty string")
        elif path in seen:
            errors.append(f"{label}.path: duplicate source {path!r}")
        else:
            seen.add(path)
        if not isinstance(item["sha256"], str) or not re.fullmatch(
            r"[0-9a-f]{64}", item["sha256"]
        ):
            errors.append(f"{label}.sha256: expected lowercase SHA-256 hex digest")
    return errors


def inspect_sources(
    record: dict[str, Any], root: Path | None, artifacts: list[dict[str, Any]]
) -> dict[str, Any]:
    snapshots = record.get("source_snapshots")
    if not snapshots:
        return {"status": "UNBOUND", "issues": []}
    if root is None:
        return {"status": "UNVERIFIED", "issues": ["source root was not supplied"]}
    issues = []
    paths = {source_path(root, item["path"]) for item in snapshots}
    if record["evaluator"] == "agent" and record["status"] == "PASS":
        required = {record["artifact"]}
        for artifact in artifacts:
            if artifact["id"] in record.get("artifact_refs", []):
                for values in artifact["files"].values():
                    required.update(values)
        for value in sorted(required):
            if source_path(root, value) not in paths:
                issues.append(f"missing source snapshot: {value}")
    for item in snapshots:
        try:
            actual = file_digest(source_path(root, item["path"]))
        except OSError:
            issues.append(f"source unavailable: {item['path']}")
            continue
        if actual != item["sha256"]:
            issues.append(f"source changed: {item['path']}")
    return {"status": "UNVERIFIED" if issues else "CURRENT", "issues": issues}

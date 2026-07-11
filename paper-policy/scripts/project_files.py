#!/usr/bin/env python3
"""Resolve the authoritative TeX/BibTeX file set for a paper project."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


INPUT_PATTERN = re.compile(r"\\(?:input|include)\s*\{([^}]+)\}")
BIBLIOGRAPHY_PATTERN = re.compile(r"\\bibliography\s*\{([^}]+)\}")
ADD_BIB_PATTERN = re.compile(r"\\addbibresource(?:\s*\[[^\]]*\])?\s*\{([^}]+)\}")
DOCUMENTCLASS_PATTERN = re.compile(r"\\documentclass(?:\s*\[[^\]]*\])?\s*\{")


@dataclass(frozen=True)
class ProjectFiles:
    primary_tex: Path
    primary_tex_paths: tuple[Path, ...]
    tex_paths: tuple[Path, ...]
    bib_paths: tuple[Path, ...]


def _strip_comments(text: str) -> str:
    output: list[str] = []
    for raw_line in text.splitlines():
        line: list[str] = []
        escaped = False
        for char in raw_line:
            if char == "%" and not escaped:
                break
            line.append(char)
            escaped = char == "\\" and not escaped
            if char != "\\":
                escaped = False
        output.append("".join(line))
    return "\n".join(output)


def _inside_root(root: Path, path: Path, where: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        raise ValueError(f"{where} escapes project root: {path}") from None
    return resolved


def _context_tex_path(root: Path, value: str, where: str) -> Path:
    path = _inside_root(root, root / value, where)
    if path.suffix == "":
        path = path.with_suffix(".tex")
    if not path.is_file():
        raise ValueError(f"{where} does not exist: {value}")
    return path


def _resolve_reference(root: Path, source: Path, value: str, suffix: str) -> Path | None:
    raw = Path(value.strip())
    if raw.suffix == "":
        raw = raw.with_suffix(suffix)
    for candidate in (source.parent / raw, root / raw):
        try:
            resolved = _inside_root(root, candidate, "TeX reference")
        except ValueError:
            continue
        if resolved.is_file():
            return resolved
    return None


def tex_closure(root: Path, entrypoints: list[Path]) -> tuple[Path, ...]:
    """Follow uncommented input/include commands from selected entrypoints."""
    selected: set[Path] = set()
    pending = list(reversed(entrypoints))
    while pending:
        path = pending.pop()
        if path in selected:
            continue
        selected.add(path)
        text = _strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        for value in INPUT_PATTERN.findall(text):
            included = _resolve_reference(root, path, value, ".tex")
            if included is not None and included not in selected:
                pending.append(included)
    return tuple(sorted(selected))


def _auto_primary(root: Path) -> Path:
    conventional = root / "main.tex"
    if conventional.is_file():
        return conventional.resolve()
    document_roots = []
    for path in sorted(root.rglob("*.tex")):
        text = _strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        if DOCUMENTCLASS_PATTERN.search(text):
            document_roots.append(path.resolve())
    if len(document_roots) == 1:
        return document_roots[0]
    choices = ", ".join(path.relative_to(root).as_posix() for path in document_roots)
    raise ValueError(
        "ambiguous manuscript entrypoint; set context.primary_tex"
        + (f" (document roots: {choices})" if choices else "")
    )


def _selected_bibliographies(root: Path, tex_paths: tuple[Path, ...]) -> tuple[Path, ...]:
    selected: set[Path] = set()
    for path in tex_paths:
        text = _strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        values: list[str] = []
        for group in BIBLIOGRAPHY_PATTERN.findall(text):
            values.extend(item.strip() for item in group.split(",") if item.strip())
        values.extend(ADD_BIB_PATTERN.findall(text))
        for value in values:
            bib = _resolve_reference(root, path, value, ".bib")
            if bib is not None:
                selected.add(bib)
    return tuple(sorted(selected))


def select_project_files(
    root: Path,
    primary_tex: str | None = None,
    additional_tex: list[str] | None = None,
) -> ProjectFiles:
    """Select primary/include trees and only their referenced bibliographies."""
    root = root.resolve()
    primary = (
        _context_tex_path(root, primary_tex, "context.primary_tex")
        if primary_tex
        else _auto_primary(root)
    )
    additional = [
        _context_tex_path(root, value, f"context.additional_tex[{index}]")
        for index, value in enumerate(additional_tex or [])
    ]
    primary_paths = tex_closure(root, [primary])
    all_paths = tex_closure(root, [primary, *additional])
    return ProjectFiles(
        primary_tex=primary,
        primary_tex_paths=primary_paths,
        tex_paths=all_paths,
        bib_paths=_selected_bibliographies(root, all_paths),
    )

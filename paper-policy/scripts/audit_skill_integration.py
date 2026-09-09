#!/usr/bin/env python3
"""Check explicit skill-reference paths and build a rule-to-document index.

This is not a Markdown parser, prose-quality test, or manuscript policy assessor.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

SKILLS = ("paper-writing", "paper-review", "paper-policy", "paper-figures-tables")
RULE_ID = re.compile(r"[A-Z][A-Z0-9_]*(?:\.[A-Z][A-Z0-9_]*)+")
INLINE = re.compile(r"`([^`\n]+)`")
LINK = re.compile(r"\[[^\]\n]*\]\(([^)\n]+)\)")
MARKER = re.compile(r"<!--\s*policy:([A-Z0-9_.]+)\s*-->")
EXPLICIT = re.compile(r"^(?:(?:\.\.?/)+|references/|scripts/|assets/)[^\s<>*{}]+$")


def audit(root: Path) -> dict:
    root = root.resolve()
    rules = set()
    for name in ("hard-rules.yaml", "soft-rules.yaml"):
        data = yaml.safe_load((root / "paper-policy/references" / name).read_text())
        rules.update(row["id"] for row in data["rules"])
    errors, references, consumers = [], [], {}
    files = []
    for skill in SKILLS:
        folder = root / skill
        if not (folder / "SKILL.md").is_file():
            errors.append({"file": skill, "kind": "missing_skill", "target": "SKILL.md"})
        files.extend(sorted(folder.rglob("*.md")))
    for path in files:
        fence = None
        for number, line in enumerate(path.read_text().splitlines(), 1):
            stripped = line.lstrip()
            if stripped.startswith(("```", "~~~")):
                marker = stripped[:3]
                if fence is None:
                    fence = marker
                elif fence == marker:
                    fence = None
                continue
            if fence:
                continue
            locator = {"file": str(path.relative_to(root)), "line": number}
            tokens = INLINE.findall(line)
            for rule in sorted({t for t in tokens if RULE_ID.fullmatch(t)} | set(MARKER.findall(line))):
                consumers.setdefault(rule, []).append(locator)
                if rule not in rules:
                    errors.append({**locator, "kind": "unknown_rule", "target": rule})
            paths = {t: "inline" for t in tokens if EXPLICIT.fullmatch(t)}
            for link in LINK.findall(line):
                link = link.strip().strip("<>")
                if not urlsplit(link).scheme and not link.startswith(("#", "/")):
                    paths[unquote(link.split("#", 1)[0])] = "link"
            for value in sorted(paths):
                target = path.parent / value
                if (not target.exists() and paths[value] == "inline"
                        and value.startswith(("references/", "scripts/", "assets/"))):
                    target = root / path.relative_to(root).parts[0] / value
                references.append({**locator, "target": value, "resolved": str(target.resolve())})
                if not target.exists():
                    errors.append({**locator, "kind": "missing_reference", "target": value})
    return {
        "skills_root": str(root), "documents_scanned": len(files),
        "registry_rule_count": len(rules), "errors": errors,
        "references": references, "rule_consumers": dict(sorted(consumers.items())),
        "coverage": {
            "checked": "Markdown outside fences: exact inline rule IDs, policy markers, explicit relative paths, inline Markdown links",
            "not_checked": "Semantic consistency, bare runtime filenames, fenced examples, dynamic paths, reference-style Markdown links, URL availability, manuscript quality or readiness",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills_root", nargs="?", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    try:
        result = audit(args.skills_root)
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        return 2
    print(json.dumps(result, indent=2))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

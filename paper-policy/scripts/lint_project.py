#!/usr/bin/env python3
"""Run deterministic paper-policy checks on a local LaTeX project."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from project_files import select_project_files


FINAL_STAGES = {"submission", "camera_ready"}
TEXT_RULE_IDS = {
    "PROSE.EM_DASH_FORBIDDEN",
    "LATEX.NO_DOLLAR_DISPLAY",
    "LATEX.NO_BRACKET_DISPLAY",
    "PROSE.NO_INTERNAL_PROVENANCE",
    "PROSE.NO_UNICODE_ARROWS",
}
DEFAULT_RULE_IDS = {
    "CITE.APPROVED_SOURCE_ONLY",
    "FINAL.NO_UNRESOLVED_MARKERS",
    "PROSE.NO_INTERNAL_PROVENANCE",
}
STRICT_HOUSE_LINT_RULE_IDS = {
    "PROSE.EM_DASH_FORBIDDEN",
    "LATEX.NO_DOLLAR_DISPLAY",
    "LATEX.NO_BRACKET_DISPLAY",
    "PROSE.NO_UNICODE_ARROWS",
    "STRUCT.CONCLUSION_SINGLE_PARAGRAPH",
}
MARKER_PATTERNS = [
    re.compile(r"\[(?:citation needed|claim not verified|quote not verified)[^\]]*\]", re.I),
    re.compile(r"PLACEHOLDER_[A-Za-z0-9_:-]+"),
    re.compile(r"\b(?:TODO|TBD)\b"),
]
PROVENANCE_PATTERNS = [
    re.compile(r"/(?:Users|home|tmp)/[^\s{}]+"),
    re.compile(r"\b[^\s{}]+\.(?:py|sh|ipynb)\b"),
    re.compile(r"\b(?:renderer|rendering script|DPI check|artifact bundle)\b", re.I),
]
NON_PROSE_ENV_PATTERN = re.compile(
    r"\\(?P<action>begin|end)\{(?:tabular\*?|tabularx|longtable|verbatim\*?|lstlisting|minted)\}"
)
BRACKET_DISPLAY_PATTERN = re.compile(r"(?<!\\)\\[\[\]]")
UNICODE_ARROW_PATTERN = re.compile(r"[←→↔↕↖↗↘↙⇐⇒⇔⟵⟶⟷]")
CONCLUSION_TITLE_PATTERN = (
    r"Conclusion|Conclusions|Concluding\s+Remarks|Summary\s+and\s+Conclusions"
)
BIBTEX_ENTRY_PATTERN = re.compile(
    r"@(?P<entry_type>[A-Za-z]+)\s*\{\s*(?P<key>[^,\s]+)\s*,",
    re.I,
)
BIBTEX_META_TYPES = {"comment", "preamble", "string"}


@dataclass
class Finding:
    rule_id: str
    path: str
    line: int
    message: str


def strip_tex_comment(line: str) -> str:
    output: list[str] = []
    escaped = False
    for char in line:
        if char == "%" and not escaped:
            break
        output.append(char)
        if char == "\\":
            escaped = not escaped
        else:
            escaped = False
    return "".join(output)


def iter_tex_lines(path: Path):
    for number, raw_line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        yield number, strip_tex_comment(raw_line)


def paper_text_outside_nonprose(line: str, excluded_depth: int) -> tuple[str, int]:
    """Return paper-facing text outside tables and verbatim-like environments."""
    parts: list[str] = []
    cursor = 0
    for match in NON_PROSE_ENV_PATTERN.finditer(line):
        if excluded_depth == 0:
            parts.append(line[cursor:match.start()])
        if match.group("action") == "begin":
            excluded_depth += 1
        elif excluded_depth:
            excluded_depth -= 1
        cursor = match.end()
    if excluded_depth == 0:
        parts.append(line[cursor:])
    return "".join(parts), excluded_depth


def prose_projection(paper_text: str) -> str:
    """Project TeX source to prose while excluding code-like command arguments."""
    if re.match(
        r"\s*\\(?:newcommand|renewcommand|providecommand|Declare\w+|def)\b",
        paper_text,
    ):
        return ""
    prose = re.sub(r"\\href\{[^{}]*\}\{([^{}]*)\}", r"\1", paper_text)
    prose = re.sub(r"\\(?:texttt|url|path)\{[^{}]*\}", "", prose)
    prose = re.sub(r"\\lstinline(.).*?\1", "", prose)
    prose = re.sub(r"\\verb(.).*?\1", "", prose)
    return prose


def has_double_dollar_display(line: str, in_inline_math: bool) -> tuple[bool, bool]:
    """Detect $$ only when TeX is outside an existing inline-math span."""
    index = 0
    while index < len(line):
        if line[index] != "$" or (index and line[index - 1] == "\\"):
            index += 1
            continue
        if in_inline_math:
            in_inline_math = False
            index += 1
            continue
        if index + 1 < len(line) and line[index + 1] == "$":
            return True, in_inline_math
        in_inline_math = True
        index += 1
    return False, in_inline_math


def lint_tex_file(
    path: Path,
    root: Path,
    stage: str,
    enforce_standard_section_count: bool = False,
    enabled_rule_ids: set[str] | None = None,
) -> list[Finding]:
    findings: list[Finding] = []
    relative = str(path.relative_to(root))
    lines = list(iter_tex_lines(path))

    enabled = DEFAULT_RULE_IDS if enabled_rule_ids is None else enabled_rule_ids
    excluded_depth = 0
    in_inline_math = False
    for number, line in lines:
        paper_text, excluded_depth = paper_text_outside_nonprose(line, excluded_depth)
        prose = prose_projection(paper_text)
        if "PROSE.EM_DASH_FORBIDDEN" in enabled and ("—" in prose or "---" in prose):
            findings.append(Finding("PROSE.EM_DASH_FORBIDDEN", relative, number, "em dash detected"))
        if "PROSE.NO_UNICODE_ARROWS" in enabled and UNICODE_ARROW_PATTERN.search(prose):
            findings.append(Finding("PROSE.NO_UNICODE_ARROWS", relative, number, "Unicode arrow detected in paper prose"))
        dollar_display, in_inline_math = has_double_dollar_display(paper_text, in_inline_math)
        if "LATEX.NO_DOLLAR_DISPLAY" in enabled and dollar_display:
            findings.append(Finding("LATEX.NO_DOLLAR_DISPLAY", relative, number, "double-dollar display math detected"))
        if "LATEX.NO_BRACKET_DISPLAY" in enabled and BRACKET_DISPLAY_PATTERN.search(paper_text):
            findings.append(Finding("LATEX.NO_BRACKET_DISPLAY", relative, number, "bracket display math detected"))
        if "PROSE.NO_INTERNAL_PROVENANCE" in enabled:
            for pattern in PROVENANCE_PATTERNS:
                if pattern.search(prose):
                    findings.append(Finding("PROSE.NO_INTERNAL_PROVENANCE", relative, number, "possible internal provenance in paper-facing text"))
                    break
        if stage in FINAL_STAGES and "FINAL.NO_UNRESOLVED_MARKERS" in enabled:
            for pattern in MARKER_PATTERNS:
                if pattern.search(prose):
                    findings.append(Finding("FINAL.NO_UNRESOLVED_MARKERS", relative, number, "unresolved final-stage marker"))
                    break
        if "ANON.DOUBLE_BLIND" in enabled:
            author = re.search(r"\\author\s*\{([^{}]*)\}", paper_text, re.I)
            if author and author.group(1).strip() and "anonymous" not in author.group(1).lower():
                findings.append(Finding("ANON.DOUBLE_BLIND", relative, number, "non-anonymous author field detected"))
            elif re.search(r"\\(?:thanks|email|orcid\w*)\b", paper_text, re.I):
                findings.append(Finding("ANON.DOUBLE_BLIND", relative, number, "identity-bearing author metadata command detected"))
            elif re.search(r"\\(?:section\*?\{acknowledg|acknowledg\w*)", paper_text, re.I):
                findings.append(Finding("ANON.DOUBLE_BLIND", relative, number, "acknowledgment content detected"))
            elif re.search(r"https?://(?:www\.)?(?:github|gitlab)\.com/[^\s{}]+", paper_text, re.I):
                findings.append(Finding("ANON.DOUBLE_BLIND", relative, number, "repository URL requires anonymity review"))

    text = "\n".join(line for _, line in lines)
    conclusion = re.search(
        rf"\\section\*?\{{(?:{CONCLUSION_TITLE_PATTERN})\}}(.*?)(?=\\section\*?\{{|\\bibliography|\\printbibliography|\\end\{{document\}})",
        text,
        re.S | re.I,
    )
    if conclusion and "STRUCT.CONCLUSION_SINGLE_PARAGRAPH" in enabled:
        body = conclusion.group(1).strip()
        prose_blocks = [
            block.strip()
            for block in re.split(r"\n\s*\n", body)
            if re.search(r"[A-Za-z]", block)
            and not re.fullmatch(r"\\(?:label|vspace|smallskip|medskip|bigskip)\{?[^\n]*", block)
        ]
        if len(prose_blocks) != 1:
            section_line = text[: conclusion.start()].count("\n") + 1
            findings.append(
                Finding(
                    "STRUCT.CONCLUSION_SINGLE_PARAGRAPH",
                    relative,
                    section_line,
                    f"Conclusion contains {len(prose_blocks)} substantive paragraphs; expected exactly 1",
                )
            )
    if enforce_standard_section_count:
        section_matches = list(re.finditer(r"\\section\s*\{", text))
        section_count = len(section_matches)
        if not 5 <= section_count <= 7:
            section_line = (
                text[: section_matches[0].start()].count("\n") + 1
                if section_matches
                else 1
            )
            findings.append(
                Finding(
                    "STRUCT.SECTION_COUNT_PROFILE",
                    relative,
                    section_line,
                    f"standard conference profile has {section_count} top-level sections; expected 5 to 7",
                )
            )
    return findings


def bibtex_keys(text: str) -> list[str]:
    return [
        match.group("key")
        for match in BIBTEX_ENTRY_PATTERN.finditer(text)
        if match.group("entry_type").lower() not in BIBTEX_META_TYPES
    ]


def bibtex_key_locations(root: Path, bib_paths: list[Path]) -> list[dict[str, object]]:
    """Return every real BibTeX entry key with a source path and line."""
    root = root.resolve()
    locations: list[dict[str, object]] = []
    for path in bib_paths:
        text = "\n".join(line for _, line in iter_tex_lines(path))
        try:
            display_path = path.resolve().relative_to(root).as_posix()
        except ValueError:
            display_path = str(path.resolve())
        for match in BIBTEX_ENTRY_PATTERN.finditer(text):
            if match.group("entry_type").lower() in BIBTEX_META_TYPES:
                continue
            locations.append(
                {
                    "key": match.group("key"),
                    "path": display_path,
                    "line": text[: match.start("key")].count("\n") + 1,
                }
            )
    return locations


def citation_keys(text: str) -> set[str]:
    keys: set[str] = set()
    pattern = re.compile(
        r"\\(?:[A-Za-z]*cite[A-Za-z]*|cite)\*?(?:\[[^\]]*\])*\{([^}]*)\}",
        re.I,
    )
    for match in pattern.finditer(text):
        keys.update(key.strip() for key in match.group(1).split(",") if key.strip())
    return keys


def lint_citations(root: Path, tex_paths: list[Path], bib_paths: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    all_bib_keys: list[str] = []
    for path in bib_paths:
        all_bib_keys.extend(bibtex_keys(path.read_text(encoding="utf-8", errors="replace")))
    seen: set[str] = set()
    for key in all_bib_keys:
        if key in seen:
            findings.append(Finding("CITE.APPROVED_SOURCE_ONLY", "<bibliography>", 0, f"duplicate BibTeX key: {key}"))
        seen.add(key)

    cited: set[str] = set()
    for path in tex_paths:
        cleaned = "\n".join(line for _, line in iter_tex_lines(path))
        cited.update(citation_keys(cleaned))
    for key in sorted(cited - seen):
        findings.append(Finding("CITE.APPROVED_SOURCE_ONLY", "<manuscript>", 0, f"citation key missing from local bibliography: {key}"))
    return findings


def unused_bibtex_keys(tex_paths: list[Path], bib_paths: list[Path]) -> list[str]:
    """Return sorted bibliography keys not cited by supported citation commands."""
    bib_keys: set[str] = set()
    for path in bib_paths:
        bib_keys.update(bibtex_keys(path.read_text(encoding="utf-8", errors="replace")))
    cited: set[str] = set()
    for path in tex_paths:
        cleaned = "\n".join(line for _, line in iter_tex_lines(path))
        cited.update(citation_keys(cleaned))
    return sorted(bib_keys - cited)


def unused_bibtex_entries(
    root: Path, tex_paths: list[Path], bib_paths: list[Path]
) -> list[dict[str, object]]:
    """Return unused BibTeX entries with stable source locators."""
    unused = set(unused_bibtex_keys(tex_paths, bib_paths))
    return sorted(
        [item for item in bibtex_key_locations(root, bib_paths) if item["key"] in unused],
        key=lambda item: (str(item["key"]), str(item["path"]), int(item["line"])),
    )


def lint_referenceable_displays(root: Path, tex_paths: list[Path]) -> list[Finding]:
    """Check that every eqref target is a labelled numbered equation/align block."""
    referenced: set[str] = set()
    numbered_labels: set[str] = set()
    label_locations: dict[str, tuple[str, int]] = {}
    env_pattern = re.compile(
        r"\\begin\{(?P<env>equation|align)\}(?P<body>.*?)\\end\{(?P=env)\}",
        re.S,
    )
    for path in tex_paths:
        cleaned = "\n".join(line for _, line in iter_tex_lines(path))
        referenced.update(re.findall(r"\\eqref\{([^}]+)\}", cleaned))
        for label in re.finditer(r"\\label\{([^}]+)\}", cleaned):
            label_locations.setdefault(
                label.group(1),
                (str(path.relative_to(root)), cleaned[: label.start()].count("\n") + 1),
            )
        for block in env_pattern.finditer(cleaned):
            numbered_labels.update(re.findall(r"\\label\{([^}]+)\}", block.group("body")))
    findings: list[Finding] = []
    for key in sorted(referenced - numbered_labels):
        path, line = label_locations.get(key, ("<manuscript>", 0))
        findings.append(
            Finding(
                "LATEX.REFERENCEABLE_DISPLAY",
                path,
                line,
                f"eqref target {key!r} is missing or is not in a numbered equation/align environment",
            )
        )
    return findings


def primary_manuscript_tex_paths(
    root: Path, tex_paths: list[Path], primary_tex_path: Path | None = None
) -> list[Path]:
    """Select main.tex and its include/input tree, excluding standalone supplements."""
    candidates = {path.resolve() for path in tex_paths}
    explicit_primary = primary_tex_path.resolve() if primary_tex_path else None
    conventional_main = (root / "main.tex").resolve()
    if explicit_primary is not None:
        if explicit_primary not in candidates:
            return []
        primary = explicit_primary
    elif conventional_main in candidates:
        primary = conventional_main
    else:
        document_roots = [
            path
            for path in candidates
            if re.search(
                r"\\documentclass(?:\[[^\]]*\])?\{",
                path.read_text(encoding="utf-8", errors="replace"),
            )
        ]
        if len(document_roots) != 1:
            return tex_paths
        primary = document_roots[0]

    selected: list[Path] = []
    pending = [primary]
    seen: set[Path] = set()
    include_pattern = re.compile(r"\\(?:input|include)\{([^}]+)\}")
    while pending:
        path = pending.pop()
        if path in seen or path not in candidates:
            continue
        seen.add(path)
        selected.append(path)
        text = "\n".join(line for _, line in iter_tex_lines(path))
        for value in include_pattern.findall(text):
            included = Path(value)
            if included.suffix == "":
                included = included.with_suffix(".tex")
            resolved = (path.parent / included).resolve()
            if resolved in candidates and resolved not in seen:
                pending.append(resolved)
    return sorted(selected)


def lint_standalone_limitations(
    root: Path, tex_paths: list[Path], primary_tex_path: Path | None = None
) -> list[Finding]:
    """Reject top-level Limitations headings in the primary manuscript tree."""
    root = root.resolve()
    findings: list[Finding] = []
    pattern = re.compile(r"\\section\*?\{[^}]*\bLimitations?\b[^}]*\}", re.I)
    for path in primary_manuscript_tex_paths(root, tex_paths, primary_tex_path):
        for number, line in iter_tex_lines(path):
            if pattern.search(line):
                findings.append(
                    Finding(
                        "STRUCT.CONCLUSION_INTEGRATES_LIMITATIONS",
                        str(path.relative_to(root)),
                        number,
                        "standalone top-level Limitations section detected; integrate it into Conclusion",
                    )
                )
    return findings


def lint_standard_section_count(
    root: Path, tex_paths: list[Path], primary_tex_path: Path | None = None
) -> list[Finding]:
    tex_paths = primary_manuscript_tex_paths(root, tex_paths, primary_tex_path)
    section_locations: list[tuple[Path, int]] = []
    for path in tex_paths:
        for number, line in iter_tex_lines(path):
            section_locations.extend(
                (path, number) for _ in re.finditer(r"\\section\s*\{", line)
            )
    count = len(section_locations)
    if 5 <= count <= 7:
        return []
    if section_locations:
        path, line = section_locations[0]
        relative = str(path.relative_to(root))
    else:
        relative, line = "<manuscript>", 0
    return [
        Finding(
            "STRUCT.SECTION_COUNT_PROFILE",
            relative,
            line,
            f"standard conference profile has {count} top-level sections; expected 5 to 7",
        )
    ]


def assessed_rule_ids(
    root: Path,
    tex_paths: list[Path],
    bib_paths: list[Path],
    stage: str,
    enforce_standard_section_count: bool = False,
    enabled_rule_ids: set[str] | None = None,
    primary_tex_path: Path | None = None,
) -> set[str]:
    """Return rules for which the linter had enough input to evaluate absence."""
    assessed: set[str] = set()
    enabled = DEFAULT_RULE_IDS if enabled_rule_ids is None else enabled_rule_ids
    if tex_paths:
        assessed.update(TEXT_RULE_IDS & enabled)
        if stage in FINAL_STAGES and "FINAL.NO_UNRESOLVED_MARKERS" in enabled:
            assessed.add("FINAL.NO_UNRESOLVED_MARKERS")
        primary_paths = primary_manuscript_tex_paths(
            root, tex_paths, primary_tex_path
        )
        for path in primary_paths:
            text = "\n".join(line for _, line in iter_tex_lines(path))
            if re.search(
                rf"\\section\*?\{{(?:{CONCLUSION_TITLE_PATTERN})\}}", text, re.I
            ):
                if "STRUCT.CONCLUSION_SINGLE_PARAGRAPH" in enabled:
                    assessed.add("STRUCT.CONCLUSION_SINGLE_PARAGRAPH")
                break
        if enforce_standard_section_count:
            assessed.add("STRUCT.SECTION_COUNT_PROFILE")
        if "LATEX.REFERENCEABLE_DISPLAY" in enabled:
            assessed.add("LATEX.REFERENCEABLE_DISPLAY")
        if "ANON.DOUBLE_BLIND" in enabled:
            assessed.add("ANON.DOUBLE_BLIND")
        if "STRUCT.CONCLUSION_INTEGRATES_LIMITATIONS" in enabled:
            assessed.add("STRUCT.CONCLUSION_INTEGRATES_LIMITATIONS")
    if (tex_paths or bib_paths) and "CITE.APPROVED_SOURCE_ONLY" in enabled:
        assessed.add("CITE.APPROVED_SOURCE_ONLY")
    if tex_paths and bib_paths and "CITE.UNUSED_KEYS_REPORTED" in enabled:
        assessed.add("CITE.UNUSED_KEYS_REPORTED")
    return assessed


def lint_project(
    root: Path,
    stage: str,
    enforce_standard_section_count: bool = False,
    active_rule_ids: set[str] | None = None,
    tex_paths: list[Path] | tuple[Path, ...] | None = None,
    bib_paths: list[Path] | tuple[Path, ...] | None = None,
    primary_tex_path: Path | None = None,
) -> tuple[list[Finding], set[str]]:
    root = root.resolve()
    tex_paths = sorted(root.rglob("*.tex")) if tex_paths is None else sorted(tex_paths)
    bib_paths = sorted(root.rglob("*.bib")) if bib_paths is None else sorted(bib_paths)
    findings: list[Finding] = []
    for path in tex_paths:
        findings.extend(
            lint_tex_file(
                path,
                root,
                stage,
                enabled_rule_ids=active_rule_ids,
            )
        )
    if enforce_standard_section_count:
        findings.extend(
            lint_standard_section_count(root, tex_paths, primary_tex_path)
        )
    if active_rule_ids is None or "CITE.APPROVED_SOURCE_ONLY" in active_rule_ids:
        findings.extend(lint_citations(root, tex_paths, bib_paths))
    if active_rule_ids and "LATEX.REFERENCEABLE_DISPLAY" in active_rule_ids:
        findings.extend(lint_referenceable_displays(root, tex_paths))
    if active_rule_ids and "STRUCT.CONCLUSION_INTEGRATES_LIMITATIONS" in active_rule_ids:
        findings.extend(
            lint_standalone_limitations(root, tex_paths, primary_tex_path)
        )
    return findings, assessed_rule_ids(
        root,
        tex_paths,
        bib_paths,
        stage,
        enforce_standard_section_count,
        active_rule_ids,
        primary_tex_path,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--stage", choices=["draft", "polish", "submission", "camera_ready"], default="draft")
    parser.add_argument(
        "--standard-conference-structure",
        action="store_true",
        help="enforce the profile-specific five-to-seven top-level section rule",
    )
    parser.add_argument(
        "--strict-house-style",
        action="store_true",
        help="enable deterministic checks owned by the optional strict-house-style set",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--primary-tex")
    parser.add_argument("--additional-tex", action="append", default=[])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.project.resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    try:
        selected = select_project_files(
            root, args.primary_tex, args.additional_tex
        )
        active_rule_ids = set(DEFAULT_RULE_IDS)
        if args.strict_house_style:
            active_rule_ids.update(STRICT_HOUSE_LINT_RULE_IDS)
        findings, _ = lint_project(
            root,
            args.stage,
            args.standard_conference_structure,
            active_rule_ids=active_rule_ids,
            tex_paths=selected.tex_paths,
            bib_paths=selected.bib_paths,
            primary_tex_path=selected.primary_tex,
        )
    except ValueError as exc:
        print(f"Project lint failed: {exc}", file=sys.stderr)
        return 2

    if args.as_json:
        print(json.dumps([asdict(finding) for finding in findings], indent=2, ensure_ascii=False))
    elif findings:
        for finding in findings:
            locator = f"{finding.path}:{finding.line}" if finding.line else finding.path
            print(f"{locator}: [{finding.rule_id}] {finding.message}")
        print(f"{len(findings)} deterministic violation(s)")
    else:
        print("No deterministic violations found")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())

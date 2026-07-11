#!/usr/bin/env python3
"""Tests for deterministic project linting."""

from __future__ import annotations

import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from lint_project import (
    DEFAULT_RULE_IDS,
    STRICT_HOUSE_LINT_RULE_IDS,
    assessed_rule_ids,
    citation_keys,
    lint_citations,
    lint_project,
    lint_referenceable_displays,
    lint_standalone_limitations,
    lint_standard_section_count,
    lint_tex_file,
    unused_bibtex_entries,
    unused_bibtex_keys,
)


FIXTURES = Path(__file__).resolve().parent / "fixtures"
STRICT_TEST_RULE_IDS = DEFAULT_RULE_IDS | STRICT_HOUSE_LINT_RULE_IDS


class ProjectLintTests(unittest.TestCase):
    def lint_fixture(self, name: str, stage: str):
        root = FIXTURES / name
        tex_paths = sorted(root.rglob("*.tex"))
        bib_paths = sorted(root.rglob("*.bib"))
        findings = []
        for path in tex_paths:
            findings.extend(
                lint_tex_file(
                    path, root, stage, enabled_rule_ids=STRICT_TEST_RULE_IDS
                )
            )
        findings.extend(lint_citations(root, tex_paths, bib_paths))
        return findings

    def test_clean_project_passes(self) -> None:
        self.assertEqual(self.lint_fixture("project-pass", "submission"), [])

    def test_bad_project_reports_expected_rules(self) -> None:
        findings = self.lint_fixture("project-fail", "submission")
        rule_ids = {finding.rule_id for finding in findings}
        self.assertTrue(
            {
                "PROSE.EM_DASH_FORBIDDEN",
                "LATEX.NO_BRACKET_DISPLAY",
                "PROSE.NO_INTERNAL_PROVENANCE",
                "FINAL.NO_UNRESOLVED_MARKERS",
                "STRUCT.CONCLUSION_SINGLE_PARAGRAPH",
                "CITE.APPROVED_SOURCE_ONLY",
            }.issubset(rule_ids),
            rule_ids,
        )

    def test_public_default_lint_does_not_enforce_house_rules(self) -> None:
        findings, _ = lint_project(FIXTURES / "project-fail", "submission")
        rule_ids = {finding.rule_id for finding in findings}
        self.assertIn("PROSE.NO_INTERNAL_PROVENANCE", rule_ids)
        self.assertNotIn("PROSE.EM_DASH_FORBIDDEN", rule_ids)
        self.assertNotIn("LATEX.NO_BRACKET_DISPLAY", rule_ids)
        self.assertNotIn("STRUCT.CONCLUSION_SINGLE_PARAGRAPH", rule_ids)

    def test_missing_conclusion_is_not_marked_assessed(self) -> None:
        root = FIXTURES / "project-no-conclusion"
        tex_paths = sorted(root.rglob("*.tex"))
        assessed = assessed_rule_ids(
            root,
            tex_paths,
            [],
            "submission",
            enabled_rule_ids=STRICT_TEST_RULE_IDS,
        )
        self.assertNotIn("STRUCT.CONCLUSION_SINGLE_PARAGRAPH", assessed)

    def test_concluding_remarks_alias_is_checked(self) -> None:
        root = FIXTURES / "project-concluding-remarks"
        findings = self.lint_fixture("project-concluding-remarks", "submission")
        self.assertIn(
            "STRUCT.CONCLUSION_SINGLE_PARAGRAPH",
            {finding.rule_id for finding in findings},
        )
        assessed = assessed_rule_ids(
            root,
            sorted(root.rglob("*.tex")),
            [],
            "submission",
            enabled_rule_ids=STRICT_TEST_RULE_IDS,
        )
        self.assertIn("STRUCT.CONCLUSION_SINGLE_PARAGRAPH", assessed)

    def test_spacing_inline_math_and_table_missing_markers_do_not_false_positive(self) -> None:
        findings = self.lint_fixture("project-tex-edge-pass", "submission")
        forbidden = {
            "PROSE.EM_DASH_FORBIDDEN",
            "LATEX.NO_BRACKET_DISPLAY",
            "LATEX.NO_DOLLAR_DISPLAY",
        }
        self.assertTrue(forbidden.isdisjoint({finding.rule_id for finding in findings}))

    def test_standard_conference_section_count_is_profile_scoped(self) -> None:
        root = FIXTURES / "project-pass"
        path = root / "main.tex"
        without_profile = lint_tex_file(
            path, root, "submission", enabled_rule_ids=STRICT_TEST_RULE_IDS
        )
        with_profile = lint_tex_file(
            path,
            root,
            "submission",
            enforce_standard_section_count=True,
            enabled_rule_ids=STRICT_TEST_RULE_IDS,
        )
        self.assertNotIn(
            "STRUCT.SECTION_COUNT_PROFILE", {item.rule_id for item in without_profile}
        )
        self.assertIn(
            "STRUCT.SECTION_COUNT_PROFILE", {item.rule_id for item in with_profile}
        )

    def test_section_count_excludes_standalone_supplement(self) -> None:
        root = FIXTURES / "project-main-with-supplement"
        findings = lint_standard_section_count(root, sorted(root.rglob("*.tex")))
        self.assertEqual([], findings)

    def test_common_biblatex_citation_commands_are_parsed(self) -> None:
        text = (
            r"\parencite{alpha} \textcite{beta,gamma} "
            r"\autocite[see][p. 2]{delta} \footcite{epsilon}"
        )
        self.assertEqual(
            {"alpha", "beta", "gamma", "delta", "epsilon"},
            citation_keys(text),
        )

    def test_unicode_arrow_is_checked_only_when_rule_is_active(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "main.tex"
            path.write_text(
                "\\documentclass{article}\n\\begin{document}\nA → B.\n\\end{document}\n",
                encoding="utf-8",
            )
            inactive = lint_tex_file(path, root, "draft", enabled_rule_ids=set())
            active = lint_tex_file(
                path,
                root,
                "draft",
                enabled_rule_ids={"PROSE.NO_UNICODE_ARROWS"},
            )
            self.assertNotIn("PROSE.NO_UNICODE_ARROWS", {item.rule_id for item in inactive})
            self.assertIn("PROSE.NO_UNICODE_ARROWS", {item.rule_id for item in active})

    def test_referenceable_display_requires_numbered_equation_or_align(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "main.tex"
            path.write_text(
                "\\eqref{eq:good} and \\eqref{eq:bad}.\n"
                "\\begin{equation}x=1\\label{eq:good}\\end{equation}\n"
                "\\begin{equation*}y=2\\label{eq:bad}\\end{equation*}\n",
                encoding="utf-8",
            )
            findings = lint_referenceable_displays(root, [path])
            self.assertEqual(["LATEX.REFERENCEABLE_DISPLAY"], [item.rule_id for item in findings])
            self.assertIn("eq:bad", findings[0].message)

    def test_unused_bibtex_keys_are_reportable_without_becoming_violations(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            tex = root / "main.tex"
            bib = root / "references.bib"
            tex.write_text(r"\parencite{used}" + "\n", encoding="utf-8")
            bib.write_text(
                "@article{used, title={Used}}\n@article{unused, title={Unused}}\n",
                encoding="utf-8",
            )
            self.assertEqual(["unused"], unused_bibtex_keys([tex], [bib]))
            self.assertEqual(
                [{"key": "unused", "path": "references.bib", "line": 2}],
                unused_bibtex_entries(root, [tex], [bib]),
            )
            findings, assessed = lint_project(
                root,
                "submission",
                active_rule_ids={"CITE.UNUSED_KEYS_REPORTED"},
            )
            self.assertEqual([], findings)
            self.assertIn("CITE.UNUSED_KEYS_REPORTED", assessed)

    def test_bibtex_meta_entries_are_not_reported_as_keys(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            bib = root / "references.bib"
            bib.write_text(
                "@string{abbr = {Journal}}\n"
                "@comment{ignored, note={Not an entry}}\n"
                "@article{real, title={Real}}\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [{"key": "real", "path": "references.bib", "line": 3}],
                unused_bibtex_entries(root, [], [bib]),
            )

    def test_double_blind_deterministic_identity_fields_are_detected(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "main.tex"
            path.write_text(
                "\\author{Alice Example}\n\\email{alice@example.org}\n",
                encoding="utf-8",
            )
            findings = lint_tex_file(
                path,
                root,
                "submission",
                enabled_rule_ids={"ANON.DOUBLE_BLIND"},
            )
            self.assertTrue(findings)
            self.assertEqual({"ANON.DOUBLE_BLIND"}, {item.rule_id for item in findings})

    def test_standalone_limitations_section_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "main.tex"
            path.write_text(
                "\\documentclass{article}\n\\begin{document}\n"
                "\\section{Limitations}\nBounded discussion.\n\\end{document}\n",
                encoding="utf-8",
            )
            findings = lint_standalone_limitations(root, [path])
            self.assertEqual(
                ["STRUCT.CONCLUSION_INTEGRATES_LIMITATIONS"],
                [item.rule_id for item in findings],
            )

if __name__ == "__main__":
    unittest.main()

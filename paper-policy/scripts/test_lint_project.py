#!/usr/bin/env python3
"""Tests for deterministic project linting."""

from __future__ import annotations

import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from lint_project import (
    DEFAULT_RULE_IDS,
    Finding,
    assessed_rule_ids,
    citation_keys,
    lint_citations,
    lint_project,
    lint_referenceable_displays,
    lint_tex_file,
    unused_bibtex_entries,
    unused_bibtex_keys,
)


FIXTURES = Path(__file__).resolve().parent / "fixtures"
TEST_RULE_IDS = DEFAULT_RULE_IDS


class ProjectLintTests(unittest.TestCase):
    def test_gather_multline_and_explicit_tags_are_supported(self):
        with TemporaryDirectory() as directory:
            root=Path(directory);path=root/'main.tex'
            path.write_text(r'\eqref{g}\eqref{m}\eqref{t}'+'\n'+
                            r'\begin{gather}x=1\label{g}\end{gather}'+'\n'+
                            r'\begin{multline}x+y\\=1\label{m}\end{multline}'+'\n'+
                            r'\begin{equation*}x=1\tag{A}\label{t}\end{equation*}')
            self.assertEqual([],lint_referenceable_displays(root,[path]))

    def test_suppressed_rows_fail_and_custom_forms_are_only_hints(self):
        with TemporaryDirectory() as directory:
            root=Path(directory);path=root/'main.tex'
            path.write_text(r'\eqref{a}\eqref{b}\eqref{custom}'+'\n'+
                            r'\begin{align}x&=1\label{a}\\y&=2\notag\label{b}\end{align}')
            findings=lint_referenceable_displays(root,[path])
            self.assertEqual(['deterministic','review_hint'],[f.kind for f in findings])
            self.assertIn("'b'",findings[0].message)

    def test_scientific_renderer_and_script_are_not_compliance_items(self):
        with TemporaryDirectory() as directory:
            root=Path(directory)
            path=root/'main.tex'
            path.write_text('The renderer implements the measured operator. We evaluate reference.py.\n')
            findings=lint_tex_file(path,root,'submission',{'PROSE.NO_INTERNAL_PROVENANCE'})
            self.assertEqual([], findings)

    def test_repository_identity_requires_context_but_author_field_is_definite(self):
        with TemporaryDirectory() as directory:
            root=Path(directory)
            path=root/'main.tex'
            path.write_text('We use https://github.com/example/third-party.\n' + r'\author{Named Author}')
            findings=lint_tex_file(path,root,'submission',{'ANON.DOUBLE_BLIND'})
            self.assertEqual(['review_hint','deterministic'],[f.kind for f in findings])

    def test_finding_kind_cannot_silently_disable_failure(self):
        with self.assertRaises(ValueError):
            Finding('FACT.NO_FABRICATION','main.tex',1,'bad kind',kind='ignored')

    def lint_fixture(self, name: str, stage: str):
        root = FIXTURES / name
        tex_paths = sorted(root.rglob("*.tex"))
        bib_paths = sorted(root.rglob("*.bib"))
        findings = []
        for path in tex_paths:
            findings.extend(
                lint_tex_file(
                    path, root, stage, enabled_rule_ids=TEST_RULE_IDS
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
                "FINAL.NO_UNRESOLVED_MARKERS",
                "CITE.APPROVED_SOURCE_ONLY",
            }.issubset(rule_ids),
            rule_ids,
        )

    def test_public_default_lint_does_not_enforce_house_rules(self) -> None:
        findings, _ = lint_project(FIXTURES / "project-fail", "submission")
        rule_ids = {finding.rule_id for finding in findings}
        self.assertNotIn("PROSE.NO_INTERNAL_PROVENANCE", rule_ids)
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
            enabled_rule_ids=TEST_RULE_IDS,
        )
        self.assertNotIn("STRUCT.CONCLUSION_SINGLE_PARAGRAPH", assessed)

    def test_concluding_remarks_paragraph_shape_is_not_a_hard_check(self) -> None:
        root = FIXTURES / "project-concluding-remarks"
        findings = self.lint_fixture("project-concluding-remarks", "submission")
        self.assertNotIn(
            "STRUCT.CONCLUSION_SINGLE_PARAGRAPH",
            {finding.rule_id for finding in findings},
        )
        assessed = assessed_rule_ids(
            root,
            sorted(root.rglob("*.tex")),
            [],
            "submission",
            enabled_rule_ids=TEST_RULE_IDS,
        )
        self.assertNotIn("STRUCT.CONCLUSION_SINGLE_PARAGRAPH", assessed)

    def test_spacing_inline_math_and_table_missing_markers_do_not_false_positive(self) -> None:
        findings = self.lint_fixture("project-tex-edge-pass", "submission")
        forbidden = {
            "PROSE.EM_DASH_FORBIDDEN",
            "LATEX.NO_BRACKET_DISPLAY",
            "LATEX.NO_DOLLAR_DISPLAY",
        }
        self.assertTrue(forbidden.isdisjoint({finding.rule_id for finding in findings}))

    def test_eight_sections_are_not_a_generic_lint_failure(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "main.tex").write_text("\n".join(
                r"\section{Part %d}Content." % i for i in range(8)))
            findings, _ = lint_project(root, "submission")
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

    def test_punctuation_and_display_style_are_not_hard_failures(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "main.tex").write_text(
                "A — B; A → B.\n" + r"\[x=1\] $$y=2$$" + "\n")
            findings, assessed = lint_project(root, "submission")
            self.assertEqual([], findings)
            self.assertTrue({"PROSE.EM_DASH_FORBIDDEN", "LATEX.NO_BRACKET_DISPLAY"}.isdisjoint(assessed))

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
            self.assertNotIn("CITE.UNUSED_KEYS_REPORTED", assessed)

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

    def test_standalone_limitations_section_has_no_hard_finding(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "main.tex"
            path.write_text(
                "\\documentclass{article}\n\\begin{document}\n"
                "\\section{Limitations}\nBounded discussion.\n\\end{document}\n",
                encoding="utf-8",
            )
            findings, assessed = lint_project(root, "submission", active_rule_ids=TEST_RULE_IDS)
            self.assertEqual([], findings)
            self.assertNotIn("STRUCT.CONCLUSION_INTEGRATES_LIMITATIONS", assessed)

if __name__ == "__main__":
    unittest.main()

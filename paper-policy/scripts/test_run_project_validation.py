#!/usr/bin/env python3
"""Tests for the project-local validation entry point."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

from run_project_validation import run_validation


SCRIPT_DIR = Path(__file__).resolve().parent
POLICY_DIR = SCRIPT_DIR.parent
FIXTURES = SCRIPT_DIR / "fixtures"


class ProjectValidationRunnerTests(unittest.TestCase):
    def test_runner_uses_local_bundle_and_writes_review_artifacts(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory) / "validation"
            manifest = run_validation(
                FIXTURES / "context" / "abstract.yaml",
                FIXTURES / "project-pass",
                output,
            )
            self.assertEqual(str(POLICY_DIR.resolve()), manifest["policy_bundle"])
            self.assertFalse(manifest["active_system_skills_modified"])
            for name in (
                "resolved-policy.yaml",
                "initial-assessment.yaml",
                "evidence-worklist.yaml",
                "deterministic-findings.yaml",
                "unused-bibtex-keys.yaml",
                "artifact-manifest-skeleton.yaml",
                "artifact-discovery-summary.yaml",
                "soft-review-worklist.yaml",
                "validation-manifest.yaml",
            ):
                self.assertTrue((output / name).is_file(), name)
            worklist = yaml.safe_load((output / "evidence-worklist.yaml").read_text())
            self.assertIn("not compliance evidence", worklist["notice"])

    def test_clean_submission_has_no_deterministic_findings_but_needs_evidence(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory) / "validation"
            manifest = run_validation(
                FIXTURES / "context" / "submission.yaml",
                FIXTURES / "project-submission-clean",
                output,
            )
            self.assertEqual(0, manifest["finding_instance_count"])
            self.assertEqual(0, manifest["deterministic_failing_rule_count"])
            self.assertEqual(0, manifest["total_failing_rule_count"])
            self.assertEqual(0, manifest["soft_worklist_unmapped_rule_count"])
            self.assertEqual("BLOCKED", manifest["readiness_status"])
            assessment = yaml.safe_load((output / "initial-assessment.yaml").read_text())
            self.assertGreater(assessment["hard_summary"]["UNVERIFIED"], 0)
            self.assertEqual(0, assessment["hard_summary"]["FAIL"])
            unused = yaml.safe_load((output / "unused-bibtex-keys.yaml").read_text())
            self.assertTrue(unused["active"])
            self.assertEqual([], unused["keys"])
            self.assertEqual([], unused["entries"])

    def test_manifest_separates_finding_rule_and_artifact_counts(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory) / "validation"
            manifest = run_validation(
                FIXTURES / "context" / "submission.yaml",
                FIXTURES / "project-fail",
                output,
            )
            self.assertGreaterEqual(manifest["finding_instance_count"], 1)
            self.assertGreaterEqual(manifest["deterministic_failing_rule_count"], 1)
            self.assertGreaterEqual(manifest["total_failing_rule_count"], 1)
            self.assertIn("unverified_rule_count", manifest)

    def test_runner_excludes_artifact_findings_for_inactive_rules(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / "evidence.yaml"
            evidence.write_text(
                yaml.safe_dump(
                    {
                        "version": 1,
                        "artifacts": [
                            {
                                "id": "inactive-table",
                                "kind": "table",
                                "artifact_types": ["paper_table"],
                                "claim": "A table outside the figure-only context.",
                                "latex_label": "tab:inactive",
                                "files": {
                                    "outputs": [], "scripts": [], "source_data": [],
                                    "previews": [], "table_sources": ["main.tex"],
                                },
                            }
                        ],
                        "hard_results": [],
                        "soft_results": [],
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )
            manifest = run_validation(
                FIXTURES / "context" / "final-figure.yaml",
                FIXTURES / "project-pass",
                root / "validation",
                evidence,
            )
            self.assertFalse(
                any(
                    rule_id.startswith("TABLE.")
                    for rule_id in manifest["deterministic_failing_rule_ids"]
                )
            )

    def test_runner_uses_only_selected_manuscript_tree(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "paper.tex").write_text(
                "\\documentclass{article}\n\\author{Anonymous Submission}\n"
                "\\begin{document}\n\\section{Introduction}\nClean~\\cite{used}.\n"
                "\\section{Background}\nB.\n\\section{Method}\nM.\n"
                "\\section{Results}\nR.\n\\section{Discussion}\nD.\n"
                "\\section{Conclusion}\nBounded to this test.\n"
                "\\bibliography{references}\n\\end{document}\n",
                encoding="utf-8",
            )
            (root / "flattened-copy.tex").write_text(
                "\\documentclass{article}\n\\author{Named Author}\nTODO — archive.\n",
                encoding="utf-8",
            )
            (root / "references.bib").write_text(
                "@article{used, title={Used}}\n", encoding="utf-8"
            )
            (root / "archive.bib").write_text(
                "@article{used, title={Duplicate Archive}}\n", encoding="utf-8"
            )
            context = yaml.safe_load(
                (FIXTURES / "context" / "submission.yaml").read_text()
            )
            context["primary_tex"] = "paper.tex"
            context["additional_tex"] = []
            context_path = root / "context.yaml"
            context_path.write_text(yaml.safe_dump(context), encoding="utf-8")
            manifest = run_validation(context_path, root, root / "validation")
            self.assertEqual([], manifest["deterministic_failing_rule_ids"])
            self.assertEqual(["paper.tex"], manifest["selected_tex_files"])
            self.assertEqual(["references.bib"], manifest["selected_bib_files"])


if __name__ == "__main__":
    unittest.main()

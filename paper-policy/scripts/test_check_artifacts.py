#!/usr/bin/env python3
"""Tests for figure/table artifact evidence and policy integration."""

from __future__ import annotations

import unittest
from copy import deepcopy
from tempfile import TemporaryDirectory
from pathlib import Path

from assess_compliance import assess_compliance
from check_artifacts import check_artifacts
from resolve_policy import resolve_policy
from validate_registry import load_yaml


SCRIPT_DIR = Path(__file__).resolve().parent
POLICY_DIR = SCRIPT_DIR.parent
REFS = POLICY_DIR / "references"
FIXTURES = SCRIPT_DIR / "fixtures"
CONTEXTS = FIXTURES / "context"


class ArtifactPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.hard = load_yaml(REFS / "hard-rules.yaml")
        cls.soft = load_yaml(REFS / "soft-rules.yaml")
        cls.profiles = load_yaml(REFS / "profiles.yaml")
        cls.policy_sets = load_yaml(REFS / "policy-sets.yaml")

    def resolution(self, fixture: str) -> dict:
        return resolve_policy(
            load_yaml(CONTEXTS / fixture),
            self.hard,
            self.soft,
            self.profiles,
            self.policy_sets,
        )

    @staticmethod
    def by_id(assessment: dict) -> dict[str, dict]:
        return {item["rule_id"]: item for item in assessment["hard_results"]}

    def test_valid_data_figure_sources_are_deterministically_assessed(self) -> None:
        root = FIXTURES / "artifact-pass"
        evidence = load_yaml(root / "figure-evidence.yaml")
        findings, assessed, coverage = check_artifacts(root, evidence["artifacts"])
        self.assertEqual([], findings)
        self.assertTrue(
            {
                "FIG.SOURCE_DATA_REQUIRED",
                "FIG.TRACEABLE_SCRIPT",
                "FIG.FINAL_EXPORT_ACCESSIBILITY",
            }.issubset(assessed)
        )
        self.assertEqual({"main-results"}, coverage["FIG.FINAL_WIDTH_READABLE"])

    def test_final_width_rule_remains_unverified_without_human_evidence(self) -> None:
        root = FIXTURES / "artifact-pass"
        evidence = load_yaml(root / "figure-evidence.yaml")
        findings, assessed, coverage = check_artifacts(root, evidence["artifacts"])
        result = assess_compliance(
            self.resolution("final-figure.yaml"),
            self.hard,
            evidence,
            findings,
            assessed,
            coverage,
        )
        self.assertEqual(
            "UNVERIFIED", self.by_id(result)["FIG.FINAL_WIDTH_READABLE"]["status"]
        )

    def test_conceptual_figure_content_and_readability_require_evidence(self):
        root = FIXTURES / "artifact-pass"
        evidence = load_yaml(root / "figure-evidence.yaml")
        evidence["artifacts"][0]["artifact_types"] = ["paper_figure", "conceptual_figure", "generated_conceptual_figure"]
        findings, assessed, coverage = check_artifacts(root, evidence["artifacts"])
        self.assertEqual([], findings)
        for rid in ["FIG.NO_INVENTED_COMPONENTS", "FIG.FINAL_WIDTH_READABLE"]:
            self.assertEqual({"main-results"}, coverage[rid])
            self.assertNotIn(rid, assessed)
        self.assertNotIn("FIG.CONCEPT_TYPOGRAPHY", coverage)

    def test_generated_conceptual_artifact_requires_conceptual_type(self) -> None:
        root = FIXTURES / "artifact-pass"
        evidence = load_yaml(root / "figure-evidence.yaml")
        evidence["artifacts"][0]["artifact_types"] = [
            "paper_figure",
            "generated_conceptual_figure",
        ]
        with self.assertRaisesRegex(ValueError, "requires conceptual_figure"):
            check_artifacts(root, evidence["artifacts"])

    def test_human_final_width_evidence_can_complete_readability_rule(self) -> None:
        root = FIXTURES / "artifact-pass"
        evidence = load_yaml(root / "figure-evidence.yaml")
        evidence["hard_results"] = [
            {
                "rule_id": "FIG.FINAL_WIDTH_READABLE",
                "status": "PASS",
                "artifact": "figures/main/figure.svg",
                "artifact_refs": ["main-results"],
                "locator": "single-column rendered preview",
                "evidence": "Human inspection confirmed readable labels at final column width.",
                "evaluator": "human",
            }
        ]
        findings, assessed, coverage = check_artifacts(root, evidence["artifacts"])
        result = assess_compliance(
            self.resolution("final-figure.yaml"),
            self.hard,
            evidence,
            findings,
            assessed,
            coverage,
        )
        self.assertEqual("PASS", self.by_id(result)["FIG.FINAL_WIDTH_READABLE"]["status"])

    def test_incomplete_artifact_refs_are_rejected(self) -> None:
        root = FIXTURES / "artifact-pass"
        evidence = load_yaml(root / "figure-evidence.yaml")
        evidence["hard_results"] = [
            {
                "rule_id": "FIG.FINAL_WIDTH_READABLE",
                "status": "PASS",
                "artifact": "figure set",
                "artifact_refs": [],
                "locator": "final-width QA",
                "evidence": "Only one artifact was inspected.",
                "evaluator": "human",
            }
        ]
        findings, assessed, coverage = check_artifacts(root, evidence["artifacts"])
        with self.assertRaisesRegex(ValueError, "missing covered artifacts"):
            assess_compliance(
                self.resolution("final-figure.yaml"),
                self.hard,
                evidence,
                findings,
                assessed,
                coverage,
            )

    def test_low_source_font_is_soft_but_missing_data_still_fails(self) -> None:
        root = FIXTURES / "artifact-fail"
        evidence = load_yaml(root / "figure-evidence.yaml")
        findings, assessed, coverage = check_artifacts(root, evidence["artifacts"])
        result = assess_compliance(
            self.resolution("final-figure.yaml"),
            self.hard,
            evidence,
            findings,
            assessed,
            coverage,
        )
        records = self.by_id(result)
        self.assertEqual("UNVERIFIED", records["FIG.FINAL_WIDTH_READABLE"]["status"])
        self.assertEqual("FAIL", records["FIG.SOURCE_DATA_REQUIRED"]["status"])

    def test_external_replication_bundle_source_data_is_allowed(self) -> None:
        root = FIXTURES / "artifact-pass"
        evidence = load_yaml(root / "figure-evidence.yaml")
        with TemporaryDirectory() as directory:
            external_data = Path(directory) / "replication-source.csv"
            external_data.write_text("x,y\n1,2\n", encoding="utf-8")
            evidence["artifacts"][0]["files"]["source_data"] = [str(external_data)]
            findings, assessed, _ = check_artifacts(root, evidence["artifacts"])
        self.assertNotIn(
            "FIG.SOURCE_DATA_REQUIRED", {finding.rule_id for finding in findings}
        )
        self.assertIn("FIG.SOURCE_DATA_REQUIRED", assessed)

    def test_table_source_check_cannot_autopass_render_readability(self):
        root = FIXTURES / "artifact-pass"
        evidence = load_yaml(root / "table-evidence.yaml")
        findings, assessed, coverage = check_artifacts(root, evidence["artifacts"])
        result = assess_compliance(self.resolution("final-table.yaml"), self.hard, evidence, findings, assessed, coverage)
        self.assertEqual([], findings)
        self.assertEqual("UNVERIFIED", self.by_id(result)["TABLE.FINAL_READABLE"]["status"])

    def test_missing_table_label_is_checked_per_artifact(self):
        root = FIXTURES / "artifact-table-granularity"
        evidence = load_yaml(root / "evidence.yaml")
        evidence["artifacts"][1]["latex_label"] = "tab:missing"
        findings, assessed, coverage = check_artifacts(root, evidence["artifacts"])
        failures = [x for x in findings if x.rule_id == "TABLE.FINAL_READABLE"]
        self.assertEqual(1, len(failures))
        self.assertEqual("<artifact:bad-table>", failures[0].path)
        self.assertNotIn("TABLE.FINAL_READABLE", assessed)
        self.assertEqual({"good-table", "bad-table"}, coverage["TABLE.FINAL_READABLE"])

    def test_plain_natural_width_table_accepts_human_render_evidence(self):
        evidence = deepcopy(load_yaml(FIXTURES / "artifact-pass" / "table-evidence.yaml"))
        record = evidence["artifacts"][0]
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "plain.tex").write_text(
                r"\begin{table}\begin{tabular}{ll} Method & Support \\ A & Partial \\"
                r"\end{tabular}\caption{Comparison.}\label{tab:plain}\end{table}",
                encoding="utf-8",
            )
            record["latex_label"] = "tab:plain"
            record["files"]["outputs"] = ["plain.tex"]
            record["files"]["table_sources"] = ["plain.tex"]
            evidence["hard_results"] = [{
                "rule_id": "TABLE.FINAL_READABLE", "status": "PASS",
                "artifact": "plain.tex", "artifact_refs": [record["id"]],
                "locator": "Table 1, rendered at its final placement width",
                "evidence": "Synthetic test record: human checked legible labels, units and marker meaning, with no clipping.",
                "evaluator": "human",
            }]
            findings, assessed, coverage = check_artifacts(root, evidence["artifacts"])
            result = assess_compliance(self.resolution("final-table.yaml"), self.hard, evidence, findings, assessed, coverage)
            self.assertEqual([], findings)
            self.assertEqual("PASS", self.by_id(result)["TABLE.FINAL_READABLE"]["status"])
            record["latex_label"] = "tab:missing"
            findings, assessed, coverage = check_artifacts(root, evidence["artifacts"])
            result = assess_compliance(self.resolution("final-table.yaml"), self.hard, evidence, findings, assessed, coverage)
            self.assertEqual("FAIL", self.by_id(result)["TABLE.FINAL_READABLE"]["status"])

    def test_table_label_is_required(self) -> None:
        root = FIXTURES / "artifact-pass"
        evidence = deepcopy(load_yaml(root / "table-evidence.yaml"))
        del evidence["artifacts"][0]["latex_label"]
        with self.assertRaisesRegex(ValueError, "latex_label: required"):
            check_artifacts(root, evidence["artifacts"])

    def test_alternative_partial_marker_is_not_a_mechanical_failure(self) -> None:
        root = FIXTURES / "artifact-pass"
        evidence = deepcopy(load_yaml(root / "table-evidence.yaml"))
        with TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            table_path = temporary_root / "related.tex"
            source = (root / "tables" / "related.tex").read_text(encoding="utf-8")
            table_path.write_text(
                source.replace(
                    r"\textcolor{okamber}{\footnotesize\ding{108}}",
                    r"\textcolor{okamber}{\(\circ\)}",
                ),
                encoding="utf-8",
            )
            record = evidence["artifacts"][0]
            record["files"]["outputs"] = ["related.tex"]
            record["files"]["table_sources"] = ["related.tex"]
            findings, _, _ = check_artifacts(temporary_root, evidence["artifacts"])
        self.assertEqual([], findings)

    def test_marker_style_is_not_a_source_validity_requirement(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            primary = root / "paper.tex"
            primary.write_text(
                "\\newcommand{\\cmark}{\\ding{51}}\n"
                "\\newcommand{\\pmark}{\\(\\circ\\)}\n"
                "\\newcommand{\\xmark}{\\ding{55}}\n"
                "\\begin{table}\n\\begin{tabular}{lll}\\toprule A&B&C\\\\"
                "\\midrule \\cmark&\\pmark&\\xmark\\\\\\bottomrule\\end{tabular}\n"
                "\\caption{Related comparison.}\\label{tab:related}\n\\end{table}\n",
                encoding="utf-8",
            )
            (root / "archived-copy.tex").write_text(
                "\\newcommand{\\pmark}{\\ding{108}}\n", encoding="utf-8"
            )
            records = [
                {
                    "id": "related",
                    "kind": "table",
                    "artifact_types": ["paper_table", "related_work_table"],
                    "claim": "Comparison.",
                    "latex_label": "tab:related",
                    "files": {
                        "outputs": [], "scripts": [], "source_data": [],
                        "previews": [], "table_sources": ["paper.tex"],
                    },
                }
            ]
            findings, _, _ = check_artifacts(
                root, records, project_tex_paths=[primary]
            )
            self.assertEqual([], findings)

    def test_complete_artifact_evidence_can_feed_ready_gate(self) -> None:
        root = FIXTURES / "artifact-pass"
        evidence = load_yaml(root / "figure-evidence.yaml")
        resolution = self.resolution("final-figure.yaml")
        findings, assessed, coverage = check_artifacts(root, evidence["artifacts"])
        hard_results = []
        for active in resolution["active_hard"]:
            record = {
                "rule_id": active["id"],
                "status": "PASS",
                "artifact": "paper project",
                "artifact_refs": sorted(coverage.get(active["id"], set())),
                "locator": "artifact and manuscript audit",
                "evidence": "Human inspection confirmed the active requirement.",
                "evaluator": "human",
            }
            hard_results.append(record)
        evidence["hard_results"] = hard_results
        result = assess_compliance(
            resolution,
            self.hard,
            evidence,
            findings,
            assessed,
            coverage,
        )
        self.assertEqual("READY", result["readiness"]["status"])

    def test_eps_and_raster_exports_need_quality_evidence_not_vector_gate(self):
        for suffix in ("eps", "tiff", "png", "jpg"):
            with self.subTest(suffix=suffix), TemporaryDirectory() as directory:
                root = Path(directory)
                # This checker assesses presence/extension, not image content.
                (root / f"figure.{suffix}").write_bytes(b"synthetic file-presence fixture")
                (root / "data.csv").write_text("x,y\n1,2\n")
                (root / "plot.R").write_text("# synthetic source-presence fixture\n")
                evidence = {"version": 1, "artifacts": [{
                    "id": "plot", "kind": "figure",
                    "artifact_types": ["paper_figure", "data_figure"],
                    "claim": "Synthetic fixture for format handling.",
                    "files": {"outputs": [f"figure.{suffix}"],
                              "scripts": ["plot.R"], "source_data": ["data.csv"]},
                }]}
                findings, assessed, coverage = check_artifacts(root, evidence["artifacts"])
                self.assertEqual([], findings)
                self.assertIn("FIG.FINAL_EXPORT_ACCESSIBILITY", assessed)
                result = assess_compliance(self.resolution("final-figure.yaml"), self.hard,
                                           evidence, findings, assessed, coverage)
                self.assertEqual("UNVERIFIED", self.by_id(result)["FIG.FINAL_EXPORT_ACCESSIBILITY"]["status"])

    def test_unrecognized_existing_export_is_hint_and_missing_file_still_fails(self):
        evidence = deepcopy(load_yaml(FIXTURES / "artifact-pass" / "figure-evidence.yaml"))
        # A conceptual figure isolates format handling from source-data checks.
        record = evidence["artifacts"][0]
        record["artifact_types"] = ["paper_figure", "conceptual_figure"]
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "figure.custom").write_text("synthetic unsupported-format fixture")
            record["files"] = {"outputs": ["figure.custom"]}
            findings, assessed, coverage = check_artifacts(root, evidence["artifacts"])
            self.assertEqual(["review_hint"], [f.kind for f in findings])
            self.assertNotIn("FIG.FINAL_EXPORT_ACCESSIBILITY", assessed)
            result = assess_compliance(self.resolution("final-figure.yaml"), self.hard,
                                       evidence, findings, assessed, coverage)
            self.assertEqual("UNVERIFIED", self.by_id(result)["FIG.FINAL_EXPORT_ACCESSIBILITY"]["status"])
            (root / "figure.custom").unlink()
            findings, _, _ = check_artifacts(root, evidence["artifacts"])
            self.assertEqual(["deterministic"], [f.kind for f in findings])

    def test_shared_notebook_keeps_per_figure_source_mapping(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "plots.ipynb").write_text('{"cells": [], "nbformat": 4}')
            records = []
            for name in ("a", "b"):
                (root / f"{name}.csv").write_text("x,y\n1,2\n")
                (root / f"{name}.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
                records.append({"id": name, "kind": "figure", "artifact_types": ["data_figure"],
                                "claim": "Synthetic source-presence fixture.",
                                "files": {"scripts": ["plots.ipynb"], "source_data": [f"{name}.csv"],
                                          "outputs": [f"{name}.svg"]}})
            findings, assessed, coverage = check_artifacts(root, records)
            self.assertEqual([], findings)
            self.assertEqual({"a", "b"}, coverage["FIG.TRACEABLE_SCRIPT"])
            self.assertIn("FIG.TRACEABLE_SCRIPT", assessed)
            (root / "plots.ipynb").unlink()
            findings, assessed, _ = check_artifacts(root, records)
            failures = [f for f in findings if f.rule_id == "FIG.TRACEABLE_SCRIPT"]
            self.assertEqual(2, len(failures))
            self.assertNotIn("FIG.TRACEABLE_SCRIPT", assessed)


if __name__ == "__main__":
    unittest.main()

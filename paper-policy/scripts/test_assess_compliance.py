#!/usr/bin/env python3
"""Tests for evidence-backed compliance assessment and readiness."""

from __future__ import annotations

import unittest
import json
import subprocess
import sys
from pathlib import Path

from assess_compliance import assess_compliance
from lint_project import lint_project
from resolve_policy import resolve_policy
from validate_registry import load_yaml


SCRIPT_DIR = Path(__file__).resolve().parent
POLICY_DIR = SCRIPT_DIR.parent
REFS = POLICY_DIR / "references"
CONTEXTS = SCRIPT_DIR / "fixtures" / "context"
FIXTURES = SCRIPT_DIR / "fixtures"


class ComplianceAssessmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.hard = load_yaml(REFS / "hard-rules.yaml")
        cls.profiles = load_yaml(REFS / "profiles.yaml")

    def resolution(self, fixture: str) -> dict:
        return resolve_policy(load_yaml(CONTEXTS / fixture), self.hard, self.profiles)

    @staticmethod
    def lint_for_resolution(resolution: dict, project: Path, stage: str):
        active = {item["id"] for item in resolution["active_hard"]}
        return lint_project(
            project,
            stage,
            active_rule_ids=active,
        )

    @staticmethod
    def result_by_id(assessment: dict) -> dict[str, dict]:
        return {item["rule_id"]: item for item in assessment["hard_results"]}

    @staticmethod
    def pass_record(rule_id: str) -> dict:
        return {
            "rule_id": rule_id,
            "status": "PASS",
            "artifact": "paper-project",
            "locator": "policy audit record",
            "evidence": "Human inspection confirmed the active requirement.",
            "evaluator": "human",
        }

    def complete_evidence(self, resolution: dict) -> dict:
        return {
            "version": 1,
            "hard_results": [
                self.pass_record(item["id"]) for item in resolution["active_hard"]
            ],

        }

    def test_optional_workflow_notes_do_not_replace_required_evidence(self) -> None:
        # Synthetic scoped judgment with supplied requirement evidence.
        # No optional brief or workflow ledger is supplied.
        context = {
            "version": 1, "submission_stage": "submission",
            "task_scope": "full_paper", "task_mode": "submission_readiness",
            "scopes": ["workflow", "writing"], "artifacts": ["policy", "prose"],
            "features": ["paper_prose"],
            "provenance": {"submission_stage": "user"},
        }
        resolution = resolve_policy(context, self.hard, self.profiles)
        rule_id = "WORKFLOW.COMPLEX_TASK_STATE"
        self.assertNotIn(rule_id, {x["id"] for x in resolution["active_hard"]})
        evidence = self.complete_evidence(resolution)
        result = assess_compliance(resolution, self.hard, evidence)
        self.assertEqual("READY", result["readiness"]["status"])
        evidence["hard_results"] = [
            x for x in evidence["hard_results"] if x["rule_id"] != "CLAIM.EVIDENCE_BOUND"
        ]
        result = assess_compliance(resolution, self.hard, evidence)
        self.assertEqual("UNVERIFIED", self.result_by_id(result)["CLAIM.EVIDENCE_BOUND"]["status"])
        self.assertEqual("BLOCKED", result["readiness"]["status"])

    def test_draft_readiness_is_not_evaluated(self) -> None:
        resolution = self.resolution("abstract.yaml")
        findings, assessed = self.lint_for_resolution(
            resolution, FIXTURES / "project-pass", "draft"
        )
        result = assess_compliance(resolution, self.hard, findings=findings, assessed_rules=assessed)
        self.assertEqual("NOT_EVALUATED", result["readiness"]["status"])

    def test_submission_without_evidence_is_blocked(self) -> None:
        resolution = self.resolution("submission.yaml")
        findings, assessed = self.lint_for_resolution(
            resolution, FIXTURES / "project-pass", "submission"
        )
        result = assess_compliance(resolution, self.hard, findings=findings, assessed_rules=assessed)
        self.assertEqual("BLOCKED", result["readiness"]["status"])
        self.assertGreater(result["hard_summary"]["UNVERIFIED"], 0)

    def test_deterministic_failure_cannot_be_overwritten_by_pass(self) -> None:
        resolution = self.resolution("submission.yaml")
        findings, assessed = self.lint_for_resolution(
            resolution, FIXTURES / "project-fail", "submission"
        )
        evidence = {
            "version": 1,
            "hard_results": [self.pass_record("FINAL.NO_UNRESOLVED_MARKERS")],

        }
        result = assess_compliance(
            resolution, self.hard, evidence, findings, assessed
        )
        record = self.result_by_id(result)["FINAL.NO_UNRESOLVED_MARKERS"]
        self.assertEqual("FAIL", record["status"])
        self.assertEqual("deterministic_finding", record["basis"])

    def test_missing_conclusion_does_not_auto_pass(self) -> None:
        resolution = self.resolution("conclusion.yaml")
        findings, assessed = self.lint_for_resolution(
            resolution, FIXTURES / "project-no-conclusion", "draft"
        )
        result = assess_compliance(resolution, self.hard, findings=findings, assessed_rules=assessed)
        record = self.result_by_id(result)["STRUCT.CONCLUSION_NO_NEW_CLAIMS"]
        self.assertEqual("UNVERIFIED", record["status"])

    def test_invalid_waiver_is_rejected(self) -> None:
        resolution = self.resolution("conclusion.yaml")
        evidence = {
            "version": 1,
            "hard_results": [
                {
                    "rule_id": "FACT.NO_FABRICATION",
                    "status": "WAIVED",
                    "artifact": "main.tex",
                    "locator": "global",
                    "evidence": "Requested exception.",
                    "evaluator": "user",
                    "waiver": {
                        "authority": "user",
                        "reason": "Style preference",
                        "recorded_at": "2026-07-11",
                    },
                }
            ],

        }
        with self.assertRaisesRegex(ValueError, "does not allow waivers"):
            assess_compliance(resolution, self.hard, evidence)

    def test_authorized_venue_waiver_is_accepted(self) -> None:
        resolution = self.resolution("submission.yaml")
        evidence = {
            "version": 1,
            "hard_results": [
                {
                    "rule_id": "EXPERIMENT.REPRODUCIBILITY",
                    "status": "WAIVED",
                    "artifact": "main.tex",
                    "locator": "top-level structure",
                    "evidence": "The venue exempts this submission type from the compute-resource reporting requirement.",
                    "evaluator": "venue",
                    "waiver": {
                        "authority": "venue",
                        "reason": "Official venue reporting exception",
                        "recorded_at": "2026-07-11",
                    },
                }
            ],

        }
        result = assess_compliance(resolution, self.hard, evidence)
        self.assertEqual(
            "WAIVED",
            self.result_by_id(result)["EXPERIMENT.REPRODUCIBILITY"]["status"],
        )

    def test_complete_evidence_can_make_submission_ready(self) -> None:
        resolution = self.resolution("submission.yaml")
        evidence = self.complete_evidence(resolution)
        result = assess_compliance(resolution, self.hard, evidence)
        self.assertEqual("READY", result["readiness"]["status"])
        self.assertEqual([], result["readiness"]["hard_blockers"])

    def test_not_applicable_is_excluded_from_readiness(self) -> None:
        resolution = self.resolution("submission.yaml")
        evidence = self.complete_evidence(resolution)
        target = next(
            item for item in evidence["hard_results"]
            if item["rule_id"] == "EXPERIMENT.REPRODUCIBILITY"
        )
        target["status"] = "NOT_APPLICABLE"
        target["evidence"] = "No automatic fix operation is in scope for this audit."
        result = assess_compliance(resolution, self.hard, evidence)
        self.assertEqual("READY", result["readiness"]["status"])
        self.assertEqual(1, result["hard_summary"]["NOT_APPLICABLE"])

    def test_tool_cannot_pass_semantic_rule(self) -> None:
        resolution = self.resolution("submission.yaml")
        record = self.pass_record("CLAIM.EVIDENCE_BOUND")
        record["evaluator"] = "tool"
        evidence = {"version": 1, "hard_results": [record]}
        with self.assertRaisesRegex(ValueError, "tool cannot decide semantic"):
            assess_compliance(resolution, self.hard, evidence)

    def test_agent_can_record_anchored_semantic_failure(self) -> None:
        resolution = self.resolution("submission.yaml")
        record = {
            "rule_id": "CLAIM.EVIDENCE_BOUND",
            "status": "FAIL",
            "artifact": "main.tex",
            "locator": "Introduction lines 106-108; Experiments lines 416-418",
            "evidence": "The Introduction claims improvement on five datasets, but the supplied results report only three; the claimed scope exceeds the inspected evidence.",
            "evaluator": "agent",
        }
        evidence = {"version": 1, "hard_results": [record]}
        result = assess_compliance(resolution, self.hard, evidence)
        assessed = self.result_by_id(result)["CLAIM.EVIDENCE_BOUND"]
        self.assertEqual("FAIL", assessed["status"])
        self.assertEqual("supplied_evidence", assessed["basis"])

    def test_agent_cannot_pass_semantic_rule_without_snapshots(self) -> None:
        resolution = self.resolution("submission.yaml")
        record = self.pass_record("CLAIM.EVIDENCE_BOUND")
        record["evaluator"] = "agent"
        evidence = {"version": 1, "hard_results": [record]}
        with self.assertRaisesRegex(ValueError, "source_snapshots: required non-empty list"):
            assess_compliance(resolution, self.hard, evidence)

    def test_agent_cannot_decide_deterministic_only_rule(self) -> None:
        resolution = self.resolution("submission.yaml")
        record = {
            "rule_id": "FINAL.NO_UNRESOLVED_MARKERS",
            "status": "FAIL",
            "artifact": "main.tex",
            "locator": "line 10",
            "evidence": "Agent-reported deterministic issue.",
            "evaluator": "agent",
        }
        evidence = {"version": 1, "hard_results": [record]}
        with self.assertRaisesRegex(ValueError, "agent cannot decide deterministic-only"):
            assess_compliance(resolution, self.hard, evidence)

    def test_always_rule_cannot_be_not_applicable(self) -> None:
        resolution = self.resolution("submission.yaml")
        record = self.pass_record("FACT.NO_FABRICATION")
        record["status"] = "NOT_APPLICABLE"
        evidence = {"version": 1, "hard_results": [record]}
        with self.assertRaisesRegex(ValueError, "always-active"):
            assess_compliance(resolution, self.hard, evidence)

    def test_cli_returns_nonzero_for_blocked_submission(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_DIR / "assess_compliance.py"),
                str(CONTEXTS / "submission.yaml"),
                "--project",
                str(FIXTURES / "project-pass"),
                "--format",
                "json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(1, completed.returncode, completed.stderr)
        self.assertEqual("BLOCKED", json.loads(completed.stdout)["readiness"]["status"])



if __name__ == "__main__":
    unittest.main()

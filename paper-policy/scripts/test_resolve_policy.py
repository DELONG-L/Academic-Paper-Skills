#!/usr/bin/env python3
"""Integration tests for context-driven paper-policy resolution."""

from __future__ import annotations

import unittest
from pathlib import Path

from resolve_policy import resolve_policy
from validate_registry import load_yaml


SCRIPT_DIR = Path(__file__).resolve().parent
POLICY_DIR = SCRIPT_DIR.parent
REFS = POLICY_DIR / "references"
FIXTURES = SCRIPT_DIR / "fixtures" / "context"


class ResolvePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.hard = load_yaml(REFS / "hard-rules.yaml")
        cls.soft = load_yaml(REFS / "soft-rules.yaml")
        cls.profiles = load_yaml(REFS / "profiles.yaml")
        cls.policy_sets = load_yaml(REFS / "policy-sets.yaml")

    def resolve(self, fixture: str) -> dict:
        return resolve_policy(
            load_yaml(FIXTURES / fixture),
            self.hard,
            self.soft,
            self.profiles,
            self.policy_sets,
        )

    @staticmethod
    def ids(result: dict, field: str) -> set[str]:
        return {item["id"] for item in result[field]}

    def test_abstract_selects_abstract_soft_rule(self) -> None:
        result = self.resolve("abstract.yaml")
        soft = self.ids(result, "active_soft")
        hard = self.ids(result, "active_hard")
        self.assertIn("ABSTRACT.FIVE_MOVES", soft)
        self.assertIn("FACT.NO_FABRICATION", hard)
        self.assertIn("PROSE.FORMULAIC_PATTERNS", soft)
        self.assertNotIn("PROSE.FORMULAIC_PATTERN_BAN", hard)
        self.assertNotIn("PROSE.ANTI_AI_MEANING_PRESERVATION", hard)
        self.assertNotIn("WORKFLOW.NO_AI_DETECTOR_GATE", hard)
        self.assertNotIn("RESULTS.FOUR_MOVE", soft)
        self.assertNotIn("RELATED.AXIS_ORGANIZATION", soft)
        self.assertNotIn("TABLE.DENSE_EMPIRICAL_STYLE", soft)

    def test_anti_ai_cleanup_activates_integrity_hard_and_style_soft(self) -> None:
        result = self.resolve("anti-ai-cleanup.yaml")
        hard = self.ids(result, "active_hard")
        soft = self.ids(result, "active_soft")
        self.assertTrue(
            {
                "PROSE.ANTI_AI_MEANING_PRESERVATION",
                "WORKFLOW.NO_AI_DETECTOR_GATE",
            }.issubset(hard)
        )
        self.assertIn("PROSE.FORMULAIC_PATTERNS", soft)
        self.assertNotIn("PROSE.FORMULAIC_PATTERN_BAN", hard)

    def test_introduction_activates_gap_rule(self) -> None:
        result = self.resolve("introduction.yaml")
        self.assertIn("STRUCT.INTRO_CONCRETE_GAP", self.ids(result, "active_hard"))
        self.assertIn("INTRO.RQ_FRAMING", self.ids(result, "active_soft"))

    def test_related_work_activates_profile_and_table_rules(self) -> None:
        result = self.resolve("related-work.yaml")
        self.assertIn("related-work-full", result["active_profiles"])
        hard = self.ids(result, "active_hard")
        self.assertTrue(
            {
                "RELATED.COMPARISON_REQUIRED",
                "TABLE.PROPOSED_ROW_GROUNDED",
                "TABLE.CANONICAL_RELATED_MARKERS",
            }.issubset(hard)
        )
        self.assertIn("TABLE.RELATED_ROW_GRANULARITY", self.ids(result, "active_soft"))

    def test_results_activates_rq_and_stochastic_profiles(self) -> None:
        result = self.resolve("results.yaml")
        self.assertTrue(
            {"rq-driven-evaluation", "stochastic-experiment"}.issubset(
                set(result["active_profiles"])
            )
        )
        hard = self.ids(result, "active_hard")
        self.assertTrue(
            {
                "RESULTS.CLAIM_MAPPING",
                "RESULTS.RQ_EXPLICIT_ANSWER",
                "EXPERIMENT.STOCHASTIC_UNCERTAINTY",
                "TABLE.VALUES_GROUNDED",
            }.issubset(hard)
        )
        self.assertIn("RESULTS.RQ_ANSWER_BOX", self.ids(result, "active_soft"))
        self.assertNotIn("RESULTS.RQ_ANSWER_BOX", hard)

    def test_conceptual_figure_feature_activates_only_supported_component_rules(self) -> None:
        hard = self.ids(self.resolve("conceptual-figure.yaml"), "active_hard")
        self.assertIn("FIG.NO_INVENTED_COMPONENTS", hard)
        self.assertIn("FIG.CONCEPT_HOUSE_STYLE", hard)
        self.assertIn("FIG.CONCEPT_TYPOGRAPHY", hard)
        self.assertIn("FIG.CONCEPT_MODEL_NATIVE_OUTPUT", hard)
        self.assertNotIn("FIG.SOURCE_DATA_REQUIRED", hard)

    def test_public_conceptual_figure_disables_house_typography(self) -> None:
        context = load_yaml(FIXTURES / "conceptual-figure.yaml")
        context.pop("policy_sets")
        result = resolve_policy(
            context, self.hard, self.soft, self.profiles, self.policy_sets
        )
        hard = self.ids(result, "active_hard")
        self.assertIn("FIG.NO_INVENTED_COMPONENTS", hard)
        self.assertNotIn("FIG.CONCEPT_HOUSE_STYLE", hard)
        self.assertNotIn("FIG.CONCEPT_TYPOGRAPHY", hard)
        self.assertNotIn("FIG.CONCEPT_MODEL_NATIVE_OUTPUT", hard)

    def test_non_generated_conceptual_figure_skips_model_native_rules(self) -> None:
        context = load_yaml(FIXTURES / "conceptual-figure.yaml")
        context["features"].remove("generated_conceptual_figure")
        result = resolve_policy(
            context, self.hard, self.soft, self.profiles, self.policy_sets
        )
        hard = self.ids(result, "active_hard")
        self.assertIn("FIG.NO_INVENTED_COMPONENTS", hard)
        self.assertIn("FIG.CONCEPT_HOUSE_STYLE", hard)
        self.assertNotIn("FIG.CONCEPT_TYPOGRAPHY", hard)
        self.assertNotIn("FIG.CONCEPT_MODEL_NATIVE_OUTPUT", hard)

    def test_generated_conceptual_selector_requires_conceptual_selector(self) -> None:
        context = load_yaml(FIXTURES / "conceptual-figure.yaml")
        context["features"].remove("conceptual_figure")
        with self.assertRaisesRegex(ValueError, "requires conceptual_figure"):
            resolve_policy(
                context, self.hard, self.soft, self.profiles, self.policy_sets
            )

    def test_data_table_feature_activates_value_grounding(self) -> None:
        hard = self.ids(self.resolve("data-table.yaml"), "active_hard")
        self.assertIn("TABLE.VALUES_GROUNDED", hard)
        self.assertNotIn("TABLE.PROPOSED_ROW_GROUNDED", hard)

    def test_conclusion_activates_all_conclusion_rules(self) -> None:
        result = self.resolve("conclusion.yaml")
        hard = self.ids(result, "active_hard")
        self.assertTrue(
            {
                "STRUCT.CONCLUSION_SINGLE_PARAGRAPH",
                "STRUCT.CONCLUSION_INTEGRATES_LIMITATIONS",
                "STRUCT.CONCLUSION_NO_NEW_CLAIMS",
                "PROSE.EM_DASH_FORBIDDEN",
                "PROSE.NO_UNICODE_ARROWS",
                "THREATS.CLAIM_MITIGATION_RESIDUAL",
            }.issubset(hard)
        )

    def test_public_default_disables_house_style_rules(self) -> None:
        context = load_yaml(FIXTURES / "conclusion.yaml")
        context.pop("policy_sets")
        result = resolve_policy(
            context, self.hard, self.soft, self.profiles, self.policy_sets
        )
        hard = self.ids(result, "active_hard")
        self.assertEqual(
            ["integrity-core", "academic-defaults"], result["active_policy_sets"]
        )
        self.assertIn("STRUCT.CONCLUSION_NO_NEW_CLAIMS", hard)
        self.assertNotIn("STRUCT.CONCLUSION_SINGLE_PARAGRAPH", hard)
        self.assertNotIn("STRUCT.CONCLUSION_INTEGRATES_LIMITATIONS", hard)
        self.assertNotIn("PROSE.EM_DASH_FORBIDDEN", hard)
        self.assertTrue(any("public default" in item for item in result["policy_set_notes"]))

    def test_strict_house_style_expands_public_policy_sets(self) -> None:
        result = self.resolve("conclusion.yaml")
        self.assertEqual(
            ["integrity-core", "academic-defaults", "strict-house-style"],
            result["active_policy_sets"],
        )
        hard = self.ids(result, "active_hard")
        self.assertIn("FACT.NO_FABRICATION", hard)
        self.assertIn("STRUCT.CONCLUSION_SINGLE_PARAGRAPH", hard)

    def test_house_only_profile_is_inert_under_public_defaults(self) -> None:
        context = load_yaml(FIXTURES / "submission.yaml")
        context.pop("policy_sets")
        result = resolve_policy(
            context, self.hard, self.soft, self.profiles, self.policy_sets
        )
        self.assertNotIn("standard-conference-structure", result["active_profiles"])
        self.assertIn("standard-conference-structure", result["inactive_profiles"])

    def test_unknown_policy_set_is_rejected(self) -> None:
        context = load_yaml(FIXTURES / "abstract.yaml")
        context["policy_sets"] = ["private-typo"]
        with self.assertRaisesRegex(ValueError, "unknown policy set"):
            resolve_policy(
                context, self.hard, self.soft, self.profiles, self.policy_sets
            )

    def test_empty_policy_set_list_is_rejected(self) -> None:
        context = load_yaml(FIXTURES / "abstract.yaml")
        context["policy_sets"] = []
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            resolve_policy(
                context, self.hard, self.soft, self.profiles, self.policy_sets
            )

    def test_final_figure_activates_final_and_source_rules(self) -> None:
        result = self.resolve("final-figure.yaml")
        self.assertIn("final-figure", result["active_profiles"])
        hard = self.ids(result, "active_hard")
        self.assertTrue(
            {
                "FIG.SOURCE_DATA_REQUIRED",
                "FIG.NO_IN_FIGURE_TITLE",
                "FIG.FINAL_WIDTH_READABLE",
                "FIG.FINAL_EXPORT_ACCESSIBILITY",
                "FIG.TRACEABLE_SCRIPT",
            }.issubset(hard)
        )
        self.assertIn("FIG.SOURCE_FONT_SCALE", self.ids(result, "active_soft"))

    def test_submission_activates_trusted_sensitive_profiles(self) -> None:
        result = self.resolve("submission.yaml")
        self.assertTrue(
            {
                "final-manuscript",
                "double-blind",
                "full-paper-workflow",
                "related-work-full",
                "reproducibility",
                "standard-conference-structure",
            }.issubset(set(result["active_profiles"]))
        )
        hard = self.ids(result, "active_hard")
        self.assertTrue(
            {
                "VENUE.CONSTRAINT_PROVENANCE",
                "ANON.DOUBLE_BLIND",
                "FINAL.NO_UNRESOLVED_MARKERS",
                "RELATED.COMPARISON_REQUIRED",
                "STRUCT.CONCLUSION_INTEGRATES_LIMITATIONS",
            }.issubset(hard)
        )
        self.assertEqual([], result["unverified_context"])

    def test_inferred_sensitive_context_does_not_activate_hard_rules(self) -> None:
        context = {
            "version": 1,
            "venue": "GuessedConf",
            "submission_stage": "submission",
            "double_blind": True,
            "scopes": ["writing", "review"],
            "artifacts": ["prose", "tex"],
            "provenance": {
                "venue": "inferred",
                "submission_stage": "inferred",
                "double_blind": "inferred",
            },
        }
        result = resolve_policy(
            context, self.hard, self.soft, self.profiles, self.policy_sets
        )
        profiles = set(result["active_profiles"])
        hard = self.ids(result, "active_hard")
        self.assertNotIn("final-manuscript", profiles)
        self.assertNotIn("double-blind", profiles)
        self.assertNotIn("VENUE.CONSTRAINT_PROVENANCE", hard)
        self.assertNotIn("ANON.DOUBLE_BLIND", hard)
        self.assertEqual(3, len(result["unverified_context"]))

    def test_multiple_venue_source_types_are_preserved(self) -> None:
        context = load_yaml(FIXTURES / "submission.yaml")
        context.pop("venue_source", None)
        context["venue_sources"] = [
            {
                "id": "official-rules",
                "kind": "official",
                "locator": "https://example.org/rules",
                "as_of": "2026-07-11",
                "constraints": ["page_limit", "anonymity"],
            },
            {
                "id": "supplied-template",
                "kind": "template",
                "locator": "templates/example.sty",
                "as_of": "2026-07-11",
                "constraints": ["formatting", "section_numbering"],
            },
        ]
        result = resolve_policy(
            context, self.hard, self.soft, self.profiles, self.policy_sets
        )
        self.assertEqual(2, len(result["context"]["venue_sources"]))
        self.assertFalse(any("template records alone" in item for item in result["context_warnings"]))

    def test_legacy_venue_source_is_normalized(self) -> None:
        result = self.resolve("submission.yaml")
        self.assertNotIn("venue_source", result["context"])
        self.assertEqual(
            "legacy-official-source", result["context"]["venue_sources"][0]["id"]
        )

    def test_official_venue_source_requires_url_and_freshness(self) -> None:
        context = load_yaml(FIXTURES / "submission.yaml")
        context.pop("venue_source", None)
        context["venue_sources"] = [
            {
                "id": "bad-official",
                "kind": "official",
                "locator": "rules.pdf",
                "as_of": None,
                "constraints": ["page_limit"],
            }
        ]
        with self.assertRaisesRegex(ValueError, "official source requires"):
            resolve_policy(
                context, self.hard, self.soft, self.profiles, self.policy_sets
            )

    def test_template_only_source_does_not_clear_authoritative_rule_warning(self) -> None:
        context = load_yaml(FIXTURES / "submission.yaml")
        context.pop("venue_source", None)
        context["venue_sources"] = [
            {
                "id": "supplied-template",
                "kind": "template",
                "locator": "templates/example.sty",
                "as_of": "2026-07-11",
                "constraints": ["formatting"],
            }
        ]
        result = resolve_policy(
            context, self.hard, self.soft, self.profiles, self.policy_sets
        )
        self.assertTrue(
            any("template records alone" in item for item in result["context_warnings"])
        )

    def test_documented_mode_alias_is_normalized(self) -> None:
        context = load_yaml(FIXTURES / "anti-ai-cleanup.yaml")
        context["task_mode"] = "anti-ai-cleanup"
        result = resolve_policy(
            context, self.hard, self.soft, self.profiles, self.policy_sets
        )
        self.assertEqual("anti_ai_cleanup", result["context"]["task_mode"])
        self.assertIn(
            "PROSE.ANTI_AI_MEANING_PRESERVATION",
            self.ids(result, "active_hard"),
        )
        self.assertTrue(any("normalized" in item for item in result["context_warnings"]))

    def test_unknown_mode_is_rejected(self) -> None:
        context = load_yaml(FIXTURES / "abstract.yaml")
        context["task_mode"] = "anti_ai_celanup"
        with self.assertRaisesRegex(ValueError, "unknown task mode"):
            resolve_policy(
                context, self.hard, self.soft, self.profiles, self.policy_sets
            )

    def test_final_figure_excludes_unrelated_prose_and_review_hard_rules(self) -> None:
        hard = self.ids(self.resolve("final-figure.yaml"), "active_hard")
        self.assertNotIn("CLAIM.EVIDENCE_BOUND", hard)
        self.assertNotIn("CITE.NO_MEMORY_BIBTEX", hard)
        self.assertNotIn("STRUCT.CONCLUSION_SINGLE_PARAGRAPH", hard)
        self.assertNotIn("REVIEW.NO_UNNECESSARY_EXPERIMENTS", hard)

    def test_final_table_excludes_figure_and_prose_only_hard_rules(self) -> None:
        hard = self.ids(self.resolve("final-table.yaml"), "active_hard")
        self.assertNotIn("FIG.SOURCE_DATA_REQUIRED", hard)
        self.assertNotIn("CLAIM.EVIDENCE_BOUND", hard)
        self.assertNotIn("STRUCT.CONCLUSION_SINGLE_PARAGRAPH", hard)

    def test_artifact_mode_list_composes_final_figure_and_table_profiles(self) -> None:
        context = load_yaml(FIXTURES / "final-figure.yaml")
        context["artifact_mode"] = ["final_figure", "final_table"]
        context["scopes"] = ["figures", "tables"]
        context["artifacts"] = ["figure", "table"]
        context["features"] = ["paper_figure", "data_figure", "result_table"]
        result = resolve_policy(
            context, self.hard, self.soft, self.profiles, self.policy_sets
        )
        self.assertTrue(
            {"final-figure", "final-table"}.issubset(set(result["active_profiles"]))
        )
        hard = self.ids(result, "active_hard")
        self.assertIn("FIG.FINAL_EXPORT_ACCESSIBILITY", hard)
        self.assertIn("TABLE.BOOKTABS_FINAL", hard)
        self.assertIn("TABLE.VALUES_GROUNDED", hard)

    def test_artifact_mode_list_rejects_unknown_entry(self) -> None:
        context = load_yaml(FIXTURES / "final-figure.yaml")
        context["artifact_mode"] = ["final_figure", "final_tabel"]
        with self.assertRaisesRegex(ValueError, "invalid value"):
            resolve_policy(
                context, self.hard, self.soft, self.profiles, self.policy_sets
            )

    def test_profile_preference_remains_soft(self) -> None:
        result = self.resolve("related-work.yaml")
        rules = {item["id"]: item for item in result["active_soft"]}
        self.assertEqual(
            ["related-work-full"], rules["RELATED.AXIS_ORGANIZATION"]["preferred_by_profiles"]
        )
        self.assertNotIn("RELATED.AXIS_ORGANIZATION", self.ids(result, "active_hard"))

    def test_layered_capability_matrix_prefers_soft_table_guidance(self) -> None:
        context = load_yaml(FIXTURES / "related-work.yaml")
        context["table_profile"] = "layered_capability_matrix"
        result = resolve_policy(
            context, self.hard, self.soft, self.profiles, self.policy_sets
        )
        self.assertIn("layered-capability-matrix", result["active_profiles"])
        rules = {item["id"]: item for item in result["active_soft"]}
        for rule_id in {
            "TABLE.DENSE_EMPIRICAL_STYLE",
            "TABLE.RELATED_ROW_GRANULARITY",
            "TABLE.CAPTION_AND_HIGHLIGHT",
            "TABLE.TARGET_WIDTH",
            "RELATED.DIMENSION_BUDGET",
        }:
            self.assertIn(rule_id, rules)
            self.assertIn(
                "layered-capability-matrix",
                rules[rule_id]["preferred_by_profiles"],
            )
            self.assertNotIn(rule_id, self.ids(result, "active_hard"))

        hard = {item["id"]: item for item in result["active_hard"]}
        self.assertIn("RELATED.COMPARISON_REQUIRED", hard)
        self.assertIn(
            "does not turn the profile's dimension or layout guidance into a hard requirement",
            hard["RELATED.COMPARISON_REQUIRED"]["requirement"],
        )

    def test_public_layered_profile_exposes_its_complete_soft_contract(self) -> None:
        context = load_yaml(FIXTURES / "related-work.yaml")
        context.pop("policy_sets")
        context["table_profile"] = "layered_capability_matrix"
        result = resolve_policy(
            context, self.hard, self.soft, self.profiles, self.policy_sets
        )
        self.assertIn("layered-capability-matrix", result["active_profiles"])
        rules = {item["id"]: item for item in result["active_soft"]}
        for rule_id in {
            "TABLE.DENSE_EMPIRICAL_STYLE",
            "TABLE.RELATED_ROW_GRANULARITY",
            "TABLE.CAPTION_AND_HIGHLIGHT",
            "TABLE.TARGET_WIDTH",
            "RELATED.DIMENSION_BUDGET",
        }:
            self.assertIn(rule_id, rules)
            self.assertIn(
                "layered-capability-matrix",
                rules[rule_id]["preferred_by_profiles"],
            )
            self.assertNotIn(rule_id, self.ids(result, "active_hard"))
        self.assertNotIn(
            "TABLE.CANONICAL_RELATED_MARKERS", self.ids(result, "active_hard")
        )

    def test_unknown_table_profile_is_rejected(self) -> None:
        context = load_yaml(FIXTURES / "related-work.yaml")
        context["table_profile"] = "layered_capabilty_matrix"
        with self.assertRaisesRegex(ValueError, "invalid value"):
            resolve_policy(
                context, self.hard, self.soft, self.profiles, self.policy_sets
            )

    def test_dense_empirical_table_style_remains_soft(self) -> None:
        result = self.resolve("final-table.yaml")
        self.assertIn("TABLE.DENSE_EMPIRICAL_STYLE", self.ids(result, "active_soft"))
        self.assertNotIn(
            "TABLE.DENSE_EMPIRICAL_STYLE", self.ids(result, "active_hard")
        )

    def test_evidence_architecture_profiles_and_threat_artifact(self) -> None:
        result = self.resolve("evidence-architecture.yaml")
        self.assertTrue(
            {
                "known-measurement-bias",
                "multi-role-evidence",
                "rq-driven-evaluation",
            }.issubset(set(result["active_profiles"]))
        )
        hard = self.ids(result, "active_hard")
        self.assertTrue(
            {
                "CLAIM.KNOWN_BIAS_DIRECTION",
                "METHOD.EVIDENCE_ROLE_BOUNDARY",
                "THREATS.CLAIM_MITIGATION_RESIDUAL",
            }.issubset(hard)
        )
        soft = self.ids(result, "active_soft")
        self.assertTrue(
            {
                "STRUCT.ARGUMENTATIVE_SPINE",
                "METHOD.EVIDENCE_ROLE_LEDGER",
                "THREATS.ADAPTIVE_TAXONOMY",
            }.issubset(soft)
        )
        self.assertFalse(
            {
                "STRUCT.ARGUMENTATIVE_SPINE",
                "METHOD.EVIDENCE_ROLE_LEDGER",
                "THREATS.ADAPTIVE_TAXONOMY",
            }
            & hard
        )


if __name__ == "__main__":
    unittest.main()

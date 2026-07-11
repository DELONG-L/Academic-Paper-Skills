#!/usr/bin/env python3
"""Tests for the paper-policy registry validator."""

from __future__ import annotations

import unittest
from copy import deepcopy
from pathlib import Path

from validate_registry import (
    DECISION_RE,
    load_yaml,
    validate_hard_document,
    validate_decision_coverage,
    validate_profiles_document,
    validate_policy_sets_document,
    validate_registry,
    validate_soft_document,
)


FIXTURES = Path(__file__).resolve().parent / "fixtures" / "registry"
REFS = Path(__file__).resolve().parent.parent / "references"


class RegistryValidatorTests(unittest.TestCase):
    def test_latest_decision_group_is_allowed(self) -> None:
        self.assertIsNotNone(DECISION_RE.fullmatch("N01"))

    def test_valid_fixture_passes(self) -> None:
        errors = validate_registry(
            FIXTURES / "valid-hard.yaml",
            FIXTURES / "valid-soft.yaml",
            FIXTURES / "valid-profiles.yaml",
            FIXTURES / "valid-decisions.yaml",
        )
        self.assertEqual(errors, [])

    def test_invalid_hard_force_fails(self) -> None:
        errors = validate_registry(
            FIXTURES / "invalid-hard-force.yaml",
            FIXTURES / "valid-soft.yaml",
            FIXTURES / "valid-profiles.yaml",
        )
        self.assertTrue(any("expected 'hard'" in error for error in errors), errors)

    def test_unknown_profile_reference_fails(self) -> None:
        errors = validate_registry(
            FIXTURES / "valid-hard.yaml",
            FIXTURES / "valid-soft.yaml",
            FIXTURES / "invalid-profile-reference.yaml",
        )
        self.assertTrue(any("unknown hard rule" in error for error in errors), errors)

    def test_decision_force_mismatch_fails(self) -> None:
        errors = validate_registry(
            FIXTURES / "valid-hard.yaml",
            FIXTURES / "valid-soft.yaml",
            FIXTURES / "valid-profiles.yaml",
            FIXTURES / "invalid-decisions.yaml",
        )
        self.assertTrue(any("requires a soft-rule mapping" in error for error in errors), errors)
        self.assertTrue(any("requires a hard-rule mapping" in error for error in errors), errors)

    def test_unknown_check_field_fails(self) -> None:
        errors = validate_registry(
            FIXTURES / "invalid-check-field.yaml",
            FIXTURES / "valid-soft.yaml",
            FIXTURES / "valid-profiles.yaml",
        )
        self.assertTrue(any("unknown fields unintended fragment" in error for error in errors), errors)

    def test_scope_artifact_phase_and_feature_typos_fail(self) -> None:
        base = load_yaml(FIXTURES / "valid-hard.yaml")
        mutations = (
            ("scope", ["writng"], "scope"),
            ("artifacts", ["prosee"], "artifacts"),
            ("phases", ["submisson"], "phases"),
        )
        for field, value, expected in mutations:
            doc = deepcopy(base)
            doc["rules"][0][field] = value
            errors, _ = validate_hard_document(doc)
            self.assertTrue(any(expected in error and "invalid" in error for error in errors), errors)
        doc = deepcopy(base)
        doc["rules"][0]["activation"] = {"type": "feature", "when": ["concluson"]}
        errors, _ = validate_hard_document(doc)
        self.assertTrue(any("invalid feature" in error for error in errors), errors)

    def test_profile_field_and_mode_typos_fail(self) -> None:
        hard = load_yaml(FIXTURES / "valid-hard.yaml")
        soft = load_yaml(FIXTURES / "valid-soft.yaml")
        _, hard_ids = validate_hard_document(hard)
        _, soft_ids = validate_soft_document(soft)
        activation = {hard["rules"][0]["id"]: hard["rules"][0]["activation"]}
        profiles = load_yaml(FIXTURES / "valid-profiles.yaml")
        profiles["profiles"][0]["match"]["field"] = "task_mdoe"
        errors, _ = validate_profiles_document(profiles, hard_ids, soft_ids, activation)
        self.assertTrue(any("match.field: invalid" in error for error in errors), errors)

        profiles = load_yaml(FIXTURES / "valid-profiles.yaml")
        profiles["profiles"][0]["match"]["any_of"] = ["anti_ai_celanup"]
        errors, _ = validate_profiles_document(profiles, hard_ids, soft_ids, activation)
        self.assertTrue(any("unknown task modes" in error for error in errors), errors)

    def test_excluded_decision_cannot_support_active_rule(self) -> None:
        decisions = load_yaml(FIXTURES / "valid-decisions.yaml")
        decisions["rules"]["A01"] = "D"
        errors = validate_decision_coverage(
            decisions,
            load_yaml(FIXTURES / "valid-hard.yaml"),
            load_yaml(FIXTURES / "valid-soft.yaml"),
        )
        self.assertTrue(any("excluded decisions" in error for error in errors), errors)

    def test_canonical_policy_sets_cover_each_rule_once(self) -> None:
        hard = load_yaml(REFS / "hard-rules.yaml")
        soft = load_yaml(REFS / "soft-rules.yaml")
        _, hard_ids = validate_hard_document(hard)
        _, soft_ids = validate_soft_document(soft)
        errors = validate_policy_sets_document(
            load_yaml(REFS / "policy-sets.yaml"), hard_ids, soft_ids
        )
        self.assertEqual([], errors)

    def test_duplicate_policy_set_assignment_is_rejected(self) -> None:
        hard = load_yaml(REFS / "hard-rules.yaml")
        soft = load_yaml(REFS / "soft-rules.yaml")
        _, hard_ids = validate_hard_document(hard)
        _, soft_ids = validate_soft_document(soft)
        policy_sets = load_yaml(REFS / "policy-sets.yaml")
        duplicate = policy_sets["sets"][0]["hard_rules"][0]
        policy_sets["sets"][1]["hard_rules"].append(duplicate)
        errors = validate_policy_sets_document(policy_sets, hard_ids, soft_ids)
        self.assertTrue(any("multiple sets" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()

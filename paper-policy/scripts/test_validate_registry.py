#!/usr/bin/env python3
"""Tests for the paper-policy registry validator."""

from __future__ import annotations

import unittest
from copy import deepcopy
from pathlib import Path

from validate_registry import (
    load_yaml,
    validate_hard_document,
    validate_profiles_document,
    validate_registry,
)


FIXTURES = Path(__file__).resolve().parent / "fixtures" / "registry"
REFS = Path(__file__).resolve().parent.parent / "references"


class RegistryValidatorTests(unittest.TestCase):
    def test_valid_fixture_passes(self) -> None:
        errors = validate_registry(FIXTURES / "valid-hard.yaml", FIXTURES / "valid-profiles.yaml")
        self.assertEqual(errors, [])

    def test_invalid_hard_force_fails(self) -> None:
        errors = validate_registry(FIXTURES / "invalid-hard-force.yaml", FIXTURES / "valid-profiles.yaml")
        self.assertTrue(any("expected 'hard'" in error for error in errors), errors)

    def test_unknown_profile_reference_fails(self) -> None:
        errors = validate_registry(FIXTURES / "valid-hard.yaml", FIXTURES / "invalid-profile-reference.yaml")
        self.assertTrue(any("unknown hard rule" in error for error in errors), errors)

    def test_unknown_check_field_fails(self) -> None:
        errors = validate_registry(FIXTURES / "invalid-check-field.yaml", FIXTURES / "valid-profiles.yaml")
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
        _, hard_ids = validate_hard_document(hard)
        activation = {hard["rules"][0]["id"]: hard["rules"][0]["activation"]}
        profiles = load_yaml(FIXTURES / "valid-profiles.yaml")
        profiles["profiles"][0]["match"]["field"] = "task_mdoe"
        errors, _ = validate_profiles_document(profiles, hard_ids, activation)
        self.assertTrue(any("match.field: invalid" in error for error in errors), errors)

        profiles = load_yaml(FIXTURES / "valid-profiles.yaml")
        profiles["profiles"][0]["match"]["any_of"] = ["anti_ai_celanup"]
        errors, _ = validate_profiles_document(profiles, hard_ids, activation)
        self.assertTrue(any("unknown task modes" in error for error in errors), errors)



    def test_canonical_requirements_and_profiles_validate(self):
        self.assertEqual([], validate_registry(REFS / 'hard-rules.yaml', REFS / 'profiles.yaml'))

    def test_missing_activation_profile_is_rejected(self):
        from tempfile import TemporaryDirectory
        import yaml
        hard = load_yaml(REFS / 'hard-rules.yaml')
        rule = next(r for r in hard['rules'] if r['activation']['type'] == 'profile')
        rule['activation']['when'].append('missing-profile')
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'hard.yaml'
            path.write_text(yaml.safe_dump(hard))
            errors = validate_registry(path, REFS / 'profiles.yaml')
        self.assertTrue(any('unknown activation profile' in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()

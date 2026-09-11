#!/usr/bin/env python3
"""Validate paper-policy requirement and activation-profile registries."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from policy_vocab import (
    ARTIFACT_KINDS,
    CONTEXT_VALUE_VOCABS,
    FEATURES,
    PHASES,
    PROFILE_MATCH_FIELDS,
    SCOPES,
    canonical_task_mode,
    valid_task_mode,
)

ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:\.[A-Z][A-Z0-9_]*)+$")
ACTIVATION_TYPES = {"always", "stage", "mode", "paper_type", "venue", "feature", "profile"}
CHECK_KINDS = {"deterministic", "semantic", "manual"}
HARD_STATUSES = {"block", "placeholder", "narrow", "report"}
FINAL_STATUSES = {"block", "report"}
AUTOFIX_VALUES = {"none", "safe", "assisted"}
WAIVER_AUTHORITIES = {"user", "venue"}
PROFILE_SOURCE_KINDS = {"local", "user", "venue", "imported-design"}


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing file: {path}") from None
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"top level must be a mapping: {path}")
    return data


def require_mapping(value: Any, where: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{where}: expected mapping")
        return {}
    return value


def require_list(value: Any, where: str, errors: list[str], *, nonempty: bool = False) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{where}: expected list")
        return []
    if nonempty and not value:
        errors.append(f"{where}: list must not be empty")
    return value


def validate_common(rule: dict[str, Any], where: str, expected_force: str, errors: list[str]) -> None:
    required = {"id", "title", "force", "scope", "artifacts", "phases", "source"}
    missing = sorted(required - rule.keys())
    if missing:
        errors.append(f"{where}: missing fields {', '.join(missing)}")

    rule_id = rule.get("id")
    if not isinstance(rule_id, str) or not ID_RE.fullmatch(rule_id):
        errors.append(f"{where}.id: invalid rule ID {rule_id!r}")
    if rule.get("force") != expected_force:
        errors.append(f"{where}.force: expected {expected_force!r}")

    controlled_lists = {
        "scope": SCOPES,
        "artifacts": ARTIFACT_KINDS,
        "phases": PHASES,
    }
    for field, allowed in controlled_lists.items():
        values = require_list(rule.get(field), f"{where}.{field}", errors, nonempty=True)
        invalid = sorted(set(values) - allowed) if all(isinstance(item, str) for item in values) else values
        if invalid:
            errors.append(f"{where}.{field}: invalid values {invalid}")

    source = require_mapping(rule.get("source"), f"{where}.source", errors)
    unknown_source = sorted(set(source) - {"origin", "note"})
    if unknown_source:
        errors.append(f"{where}.source: unknown fields {', '.join(unknown_source)}")
    if not isinstance(source.get("origin"), str) or not source.get("origin"):
        errors.append(f"{where}.source.origin: required non-empty string")


def validate_hard_document(doc: dict[str, Any]) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    rules = require_list(doc.get("rules"), "hard.rules", errors, nonempty=True)
    ids: set[str] = set()

    for index, raw_rule in enumerate(rules):
        where = f"hard.rules[{index}]"
        rule = require_mapping(raw_rule, where, errors)
        allowed_rule_fields = {
            "id", "title", "force", "scope", "artifacts", "phases",
            "activation", "requirement", "checks", "failure", "autofix",
            "waiver", "source",
        }
        unknown_rule = sorted(set(rule) - allowed_rule_fields)
        if unknown_rule:
            errors.append(f"{where}: unknown fields {', '.join(unknown_rule)}")
        validate_common(rule, where, "hard", errors)
        rule_id = rule.get("id")
        if isinstance(rule_id, str):
            if rule_id in ids:
                errors.append(f"{where}.id: duplicate ID {rule_id}")
            ids.add(rule_id)

        activation = require_mapping(rule.get("activation"), f"{where}.activation", errors)
        unknown_activation = sorted(set(activation) - {"type", "when"})
        if unknown_activation:
            errors.append(
                f"{where}.activation: unknown fields {', '.join(unknown_activation)}"
            )
        activation_type = activation.get("type")
        when = require_list(activation.get("when"), f"{where}.activation.when", errors)
        if activation_type not in ACTIVATION_TYPES:
            errors.append(f"{where}.activation.type: invalid value {activation_type!r}")
        if activation_type == "always" and when:
            errors.append(f"{where}.activation.when: must be empty for always activation")
        if activation_type in ACTIVATION_TYPES - {"always"} and not when:
            errors.append(f"{where}.activation.when: conditional activation requires values")
        if activation_type == "feature":
            invalid = sorted(set(when) - FEATURES) if all(isinstance(item, str) for item in when) else when
            if invalid:
                errors.append(f"{where}.activation.when: invalid feature values {invalid}")
        elif activation_type == "mode":
            invalid = [item for item in when if not valid_task_mode(item)]
            noncanonical = [item for item in when if valid_task_mode(item) and canonical_task_mode(item) != item]
            if invalid:
                errors.append(f"{where}.activation.when: unknown task modes {invalid}")
            if noncanonical:
                errors.append(f"{where}.activation.when: aliases are not allowed in registries {noncanonical}")
        elif activation_type == "stage":
            invalid = sorted(set(when) - PHASES) if all(isinstance(item, str) for item in when) else when
            if invalid:
                errors.append(f"{where}.activation.when: invalid stage values {invalid}")
        elif activation_type == "paper_type":
            allowed = CONTEXT_VALUE_VOCABS["paper_type"]
            invalid = sorted(set(when) - allowed) if all(isinstance(item, str) for item in when) else when
            if invalid:
                errors.append(f"{where}.activation.when: invalid paper_type values {invalid}")
        elif activation_type == "venue" and set(when) != {"specified"}:
            errors.append(f"{where}.activation.when: venue activation must be ['specified']")

        if not isinstance(rule.get("requirement"), str) or not rule.get("requirement"):
            errors.append(f"{where}.requirement: required non-empty string")

        checks = require_list(rule.get("checks"), f"{where}.checks", errors, nonempty=True)
        check_kinds: set[str] = set()
        for check_index, raw_check in enumerate(checks):
            check_where = f"{where}.checks[{check_index}]"
            check = require_mapping(raw_check, check_where, errors)
            unknown_check = sorted(
                set(check) - {"kind", "evidence_required", "description"}
            )
            if unknown_check:
                errors.append(
                    f"{check_where}: unknown fields {', '.join(unknown_check)}"
                )
            kind = check.get("kind")
            if kind not in CHECK_KINDS:
                errors.append(f"{check_where}.kind: invalid value {kind!r}")
            elif isinstance(kind, str):
                check_kinds.add(kind)
            if kind in {"semantic", "manual"} and check.get("evidence_required") is not True:
                errors.append(f"{check_where}.evidence_required: semantic/manual checks require true")
            if kind == "deterministic" and not isinstance(check.get("evidence_required"), bool):
                errors.append(f"{check_where}.evidence_required: deterministic checks require a boolean")
            if not isinstance(check.get("description"), str) or not check.get("description"):
                errors.append(f"{check_where}.description: required non-empty string")

        failure = require_mapping(rule.get("failure"), f"{where}.failure", errors)
        unknown_failure = sorted(set(failure) - {"draft", "final"})
        if unknown_failure:
            errors.append(f"{where}.failure: unknown fields {', '.join(unknown_failure)}")
        if failure.get("draft") not in HARD_STATUSES:
            errors.append(f"{where}.failure.draft: invalid value {failure.get('draft')!r}")
        if failure.get("final") not in FINAL_STATUSES:
            errors.append(f"{where}.failure.final: invalid value {failure.get('final')!r}")

        autofix = rule.get("autofix")
        if autofix not in AUTOFIX_VALUES:
            errors.append(f"{where}.autofix: invalid value {autofix!r}")
        if autofix == "safe" and ("deterministic" not in check_kinds or check_kinds & {"semantic", "manual"}):
            errors.append(f"{where}.autofix: safe requires deterministic-only checks")

        waiver = require_mapping(rule.get("waiver"), f"{where}.waiver", errors)
        unknown_waiver = sorted(set(waiver) - {"allowed", "authorities"})
        if unknown_waiver:
            errors.append(f"{where}.waiver: unknown fields {', '.join(unknown_waiver)}")
        if not isinstance(waiver.get("allowed"), bool):
            errors.append(f"{where}.waiver.allowed: required boolean")
        authorities = require_list(waiver.get("authorities"), f"{where}.waiver.authorities", errors)
        invalid_authorities = sorted(set(authorities) - WAIVER_AUTHORITIES)
        if invalid_authorities:
            errors.append(f"{where}.waiver.authorities: invalid values {invalid_authorities}")
        if waiver.get("allowed") is False and authorities:
            errors.append(f"{where}.waiver.authorities: must be empty when waiver is disabled")
        if waiver.get("allowed") is True and not authorities:
            errors.append(f"{where}.waiver.authorities: required when waiver is enabled")

    return errors, ids


def validate_profiles_document(
    doc: dict[str, Any],
    hard_ids: set[str],
    hard_activation: dict[str, dict[str, Any]],
) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    profiles = require_list(doc.get("profiles"), "profiles.profiles", errors, nonempty=True)
    ids: set[str] = set()

    for index, raw_profile in enumerate(profiles):
        where = f"profiles.profiles[{index}]"
        profile = require_mapping(raw_profile, where, errors)
        unknown_profile = sorted(
            set(profile) - {"id", "match", "activate_hard", "source"}
        )
        if unknown_profile:
            errors.append(f"{where}: unknown fields {', '.join(unknown_profile)}")
        profile_id = profile.get("id")
        if not isinstance(profile_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", profile_id):
            errors.append(f"{where}.id: invalid profile ID {profile_id!r}")
        elif profile_id in ids:
            errors.append(f"{where}.id: duplicate ID {profile_id}")
        else:
            ids.add(profile_id)

        match = require_mapping(profile.get("match"), f"{where}.match", errors)
        unknown_match = sorted(set(match) - {"field", "any_of"})
        if unknown_match:
            errors.append(f"{where}.match: unknown fields {', '.join(unknown_match)}")
        match_field = match.get("field")
        if match_field not in PROFILE_MATCH_FIELDS:
            errors.append(f"{where}.match.field: invalid value {match_field!r}")
        match_values = require_list(match.get("any_of"), f"{where}.match.any_of", errors, nonempty=True)
        if match_field == "task_mode":
            invalid = [item for item in match_values if not valid_task_mode(item)]
            noncanonical = [
                item
                for item in match_values
                if valid_task_mode(item) and canonical_task_mode(item) != item
            ]
            if invalid:
                errors.append(f"{where}.match.any_of: unknown task modes {invalid}")
            if noncanonical:
                errors.append(f"{where}.match.any_of: aliases are not allowed in registries {noncanonical}")
        elif match_field in CONTEXT_VALUE_VOCABS:
            allowed = CONTEXT_VALUE_VOCABS[match_field]
            invalid = sorted(set(match_values) - allowed) if all(isinstance(item, (str, bool)) for item in match_values) else match_values
            if invalid:
                errors.append(f"{where}.match.any_of: invalid values {invalid}")

        active = require_list(profile.get("activate_hard"), f"{where}.activate_hard", errors)
        for rule_id in active:
            if rule_id not in hard_ids:
                errors.append(f"{where}.activate_hard: unknown hard rule {rule_id!r}")
                continue
            activation = hard_activation.get(rule_id, {})
            if activation.get("type") != "profile":
                errors.append(
                    f"{where}.activate_hard: {rule_id!r} does not declare profile activation"
                )
            elif profile_id not in activation.get("when", []):
                errors.append(
                    f"{where}.activate_hard: {rule_id!r} does not accept profile {profile_id!r}"
                )
        source = require_mapping(profile.get("source"), f"{where}.source", errors)
        unknown_source = sorted(set(source) - {"kind", "url", "as_of"})
        if unknown_source:
            errors.append(f"{where}.source: unknown fields {', '.join(unknown_source)}")
        kind = source.get("kind")
        if kind not in PROFILE_SOURCE_KINDS:
            errors.append(f"{where}.source.kind: invalid value {kind!r}")
        if kind == "venue" and (not source.get("url") or not source.get("as_of")):
            errors.append(f"{where}.source: venue profiles require url and as_of")

    return errors, ids


def validate_registry(hard_path: Path, profiles_path: Path) -> list[str]:
    try:
        hard_doc = load_yaml(hard_path)
        profiles_doc = load_yaml(profiles_path)
    except ValueError as exc:
        return [str(exc)]
    errors, hard_ids = validate_hard_document(hard_doc)
    activation = {
        rule.get("id"): rule.get("activation", {})
        for rule in hard_doc.get("rules", [])
        if isinstance(rule, dict) and isinstance(rule.get("id"), str)
    }
    profile_errors, profile_ids = validate_profiles_document(
        profiles_doc, hard_ids, activation
    )
    errors.extend(profile_errors)
    profiles = {p["id"]: p for p in profiles_doc.get("profiles", [])
                if isinstance(p, dict) and isinstance(p.get("id"), str)}
    for rule_id, selector in activation.items():
        if selector.get("type") != "profile":
            continue
        for profile_id in selector.get("when", []):
            if profile_id not in profile_ids:
                errors.append(f"{rule_id}: unknown activation profile {profile_id!r}")
            elif rule_id not in profiles[profile_id].get("activate_hard", []):
                errors.append(f"{rule_id}: profile {profile_id!r} does not activate this rule")
    return errors


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    default_refs = script_dir.parent / "references"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hard", type=Path, default=default_refs / "hard-rules.yaml")
    parser.add_argument("--profiles", type=Path, default=default_refs / "profiles.yaml")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_registry(args.hard, args.profiles)
    if errors:
        print(f"Registry validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Registry validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

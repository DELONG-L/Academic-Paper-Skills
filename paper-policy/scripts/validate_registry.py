#!/usr/bin/env python3
"""Validate paper-policy hard, soft, and profile registries."""

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
DECISION_RE = re.compile(r"^[A-NX]\d{2}$")
POLICY_SET_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
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
    required = {"id", "title", "force", "scope", "artifacts", "phases", "decision_refs", "source"}
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

    refs = require_list(rule.get("decision_refs"), f"{where}.decision_refs", errors, nonempty=True)
    for ref in refs:
        if not isinstance(ref, str) or not DECISION_RE.fullmatch(ref):
            errors.append(f"{where}.decision_refs: invalid reference {ref!r}")

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
            "waiver", "decision_refs", "source",
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


def validate_soft_document(doc: dict[str, Any]) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    rules = require_list(doc.get("rules"), "soft.rules", errors, nonempty=True)
    ids: set[str] = set()

    for index, raw_rule in enumerate(rules):
        where = f"soft.rules[{index}]"
        rule = require_mapping(raw_rule, where, errors)
        allowed_rule_fields = {
            "id", "title", "force", "scope", "artifacts", "phases",
            "features",
            "default", "allowed_variants", "selection_factors", "avoid",
            "report_when", "decision_refs", "source",
        }
        unknown_rule = sorted(set(rule) - allowed_rule_fields)
        if unknown_rule:
            errors.append(f"{where}: unknown fields {', '.join(unknown_rule)}")
        validate_common(rule, where, "soft", errors)
        if "features" in rule:
            features = require_list(
                rule.get("features"), f"{where}.features", errors, nonempty=True
            )
            invalid_features = (
                sorted(set(features) - FEATURES)
                if all(isinstance(item, str) for item in features)
                else features
            )
            if invalid_features:
                errors.append(f"{where}.features: invalid values {invalid_features}")
        rule_id = rule.get("id")
        if isinstance(rule_id, str):
            if rule_id in ids:
                errors.append(f"{where}.id: duplicate ID {rule_id}")
            ids.add(rule_id)

        if not isinstance(rule.get("default"), str) or not rule.get("default"):
            errors.append(f"{where}.default: required non-empty string")
        require_list(rule.get("allowed_variants"), f"{where}.allowed_variants", errors, nonempty=True)
        require_list(rule.get("selection_factors"), f"{where}.selection_factors", errors, nonempty=True)
        require_list(rule.get("avoid"), f"{where}.avoid", errors)
        if not isinstance(rule.get("report_when"), str) or not rule.get("report_when"):
            errors.append(f"{where}.report_when: required non-empty string")
        for forbidden in ("activation", "failure", "autofix", "waiver"):
            if forbidden in rule:
                errors.append(f"{where}.{forbidden}: not allowed for soft rules")

    return errors, ids


def validate_profiles_document(
    doc: dict[str, Any],
    hard_ids: set[str],
    soft_ids: set[str],
    hard_activation: dict[str, dict[str, Any]],
) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    profiles = require_list(doc.get("profiles"), "profiles.profiles", errors, nonempty=True)
    ids: set[str] = set()

    for index, raw_profile in enumerate(profiles):
        where = f"profiles.profiles[{index}]"
        profile = require_mapping(raw_profile, where, errors)
        unknown_profile = sorted(
            set(profile) - {"id", "match", "activate_hard", "prefer_soft", "source"}
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
        preferred = require_list(profile.get("prefer_soft"), f"{where}.prefer_soft", errors)
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
        for rule_id in preferred:
            if rule_id not in soft_ids:
                errors.append(f"{where}.prefer_soft: unknown soft rule {rule_id!r}")

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


def validate_policy_sets_document(
    doc: dict[str, Any], hard_ids: set[str], soft_ids: set[str]
) -> list[str]:
    """Validate public defaults, opt-in sets, dependencies, and full rule coverage."""
    errors: list[str] = []
    unknown_top = sorted(set(doc) - {"version", "registry", "default_sets", "sets"})
    if unknown_top:
        errors.append(f"policy_sets: unknown fields {', '.join(unknown_top)}")
    if doc.get("version") != 1:
        errors.append("policy_sets.version: expected 1")
    if doc.get("registry") != "paper-policy-sets":
        errors.append("policy_sets.registry: expected 'paper-policy-sets'")

    default_sets = require_list(
        doc.get("default_sets"), "policy_sets.default_sets", errors, nonempty=True
    )
    if any(not isinstance(set_id, str) for set_id in default_sets):
        errors.append("policy_sets.default_sets: entries must be strings")
    elif len(default_sets) != len(set(default_sets)):
        errors.append("policy_sets.default_sets: duplicate set IDs are not allowed")
    raw_sets = require_list(doc.get("sets"), "policy_sets.sets", errors, nonempty=True)
    set_docs: dict[str, dict[str, Any]] = {}
    memberships = {"hard_rules": {}, "soft_rules": {}}

    for index, raw_set in enumerate(raw_sets):
        where = f"policy_sets.sets[{index}]"
        policy_set = require_mapping(raw_set, where, errors)
        unknown = sorted(
            set(policy_set)
            - {"id", "description", "includes", "hard_rules", "soft_rules"}
        )
        if unknown:
            errors.append(f"{where}: unknown fields {', '.join(unknown)}")
        set_id = policy_set.get("id")
        if not isinstance(set_id, str) or not POLICY_SET_RE.fullmatch(set_id):
            errors.append(f"{where}.id: invalid policy-set ID {set_id!r}")
        elif set_id in set_docs:
            errors.append(f"{where}.id: duplicate policy-set ID {set_id}")
        else:
            set_docs[set_id] = policy_set
        if not isinstance(policy_set.get("description"), str) or not policy_set.get(
            "description"
        ):
            errors.append(f"{where}.description: required non-empty string")
        require_list(policy_set.get("includes"), f"{where}.includes", errors)
        for field, known_ids in (("hard_rules", hard_ids), ("soft_rules", soft_ids)):
            rule_ids = require_list(policy_set.get(field), f"{where}.{field}", errors)
            for rule_id in rule_ids:
                if rule_id not in known_ids:
                    errors.append(f"{where}.{field}: unknown rule {rule_id!r}")
                memberships[field].setdefault(rule_id, []).append(set_id)

    known_set_ids = set(set_docs)
    for set_id in default_sets:
        if set_id not in known_set_ids:
            errors.append(f"policy_sets.default_sets: unknown set {set_id!r}")
    for set_id, policy_set in set_docs.items():
        for included in policy_set.get("includes", []):
            if included not in known_set_ids:
                errors.append(
                    f"policy_sets.sets.{set_id}.includes: unknown set {included!r}"
                )

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(set_id: str, trail: list[str]) -> None:
        if set_id in visited or set_id not in set_docs:
            return
        if set_id in visiting:
            errors.append(
                "policy_sets.includes: dependency cycle "
                + " -> ".join(trail + [set_id])
            )
            return
        visiting.add(set_id)
        for included in set_docs[set_id].get("includes", []):
            visit(included, trail + [set_id])
        visiting.remove(set_id)
        visited.add(set_id)

    for set_id in sorted(known_set_ids):
        visit(set_id, [])

    for field, known_ids in (("hard_rules", hard_ids), ("soft_rules", soft_ids)):
        member_map = memberships[field]
        for rule_id in sorted(known_ids - set(member_map)):
            errors.append(f"policy_sets.{field}: unassigned rule {rule_id!r}")
        for rule_id, owners in sorted(member_map.items()):
            if len(owners) > 1:
                errors.append(
                    f"policy_sets.{field}: rule {rule_id!r} assigned to multiple sets {owners}"
                )
    return errors


def validate_decision_coverage(
    doc: dict[str, Any], hard_doc: dict[str, Any], soft_doc: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    rules = require_mapping(doc.get("rules"), "decisions.rules", errors)
    conflicts = require_mapping(doc.get("conflicts"), "decisions.conflicts", errors)
    fusion = require_mapping(doc.get("fusion"), "decisions.fusion", errors)

    force_by_ref: dict[str, set[str]] = {}
    for registry_doc, force in ((hard_doc, "hard"), (soft_doc, "soft")):
        for rule in registry_doc.get("rules", []):
            if not isinstance(rule, dict):
                continue
            for ref in rule.get("decision_refs", []):
                force_by_ref.setdefault(ref, set()).add(force)

    known_refs = set(rules) | set(conflicts) | set(fusion)
    for ref in sorted(force_by_ref):
        if ref not in known_refs:
            errors.append(f"decisions: registry references unknown decision {ref!r}")
        elif ref in rules and rules[ref] == "D":
            errors.append(
                f"decisions.rules.{ref}: excluded decisions cannot support active rules"
            )

    for ref, decision in rules.items():
        if decision not in {"H", "P", "S", "D"}:
            errors.append(f"decisions.rules.{ref}: invalid value {decision!r}")
            continue
        forces = force_by_ref.get(ref, set())
        if decision in {"H", "P"} and "hard" not in forces:
            errors.append(f"decisions.rules.{ref}: {decision} requires a hard-rule mapping")
        if decision == "S" and "soft" not in forces:
            errors.append(f"decisions.rules.{ref}: S requires a soft-rule mapping")

    for ref, decision in conflicts.items():
        if decision not in {"A", "B", "C", "D"}:
            errors.append(f"decisions.conflicts.{ref}: invalid value {decision!r}")
    for ref, decision in fusion.items():
        if decision not in {"Y", "N", "Later"}:
            errors.append(f"decisions.fusion.{ref}: invalid value {decision!r}")
    return errors


def validate_registry(
    hard_path: Path,
    soft_path: Path,
    profiles_path: Path,
    decisions_path: Path | None = None,
    policy_sets_path: Path | None = None,
) -> list[str]:
    try:
        hard_doc = load_yaml(hard_path)
        soft_doc = load_yaml(soft_path)
        profiles_doc = load_yaml(profiles_path)
    except ValueError as exc:
        return [str(exc)]

    errors, hard_ids = validate_hard_document(hard_doc)
    hard_activation = {
        rule.get("id"): rule.get("activation", {})
        for rule in hard_doc.get("rules", [])
        if isinstance(rule, dict) and isinstance(rule.get("id"), str)
    }
    soft_errors, soft_ids = validate_soft_document(soft_doc)
    errors.extend(soft_errors)
    duplicates = sorted(hard_ids & soft_ids)
    for rule_id in duplicates:
        errors.append(f"registry: rule ID appears in hard and soft registries: {rule_id}")
    profile_errors, _ = validate_profiles_document(
        profiles_doc, hard_ids, soft_ids, hard_activation
    )
    errors.extend(profile_errors)
    if policy_sets_path is not None:
        try:
            policy_sets_doc = load_yaml(policy_sets_path)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            errors.extend(
                validate_policy_sets_document(policy_sets_doc, hard_ids, soft_ids)
            )
    if decisions_path is not None:
        try:
            decisions_doc = load_yaml(decisions_path)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            errors.extend(validate_decision_coverage(decisions_doc, hard_doc, soft_doc))
    return errors


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    default_refs = script_dir.parent / "references"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hard", type=Path, default=default_refs / "hard-rules.yaml")
    parser.add_argument("--soft", type=Path, default=default_refs / "soft-rules.yaml")
    parser.add_argument("--profiles", type=Path, default=default_refs / "profiles.yaml")
    parser.add_argument("--decisions", type=Path, default=default_refs / "decision-baseline.yaml")
    parser.add_argument(
        "--policy-sets", type=Path, default=default_refs / "policy-sets.yaml"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_registry(
        args.hard,
        args.soft,
        args.profiles,
        args.decisions,
        args.policy_sets,
    )
    if errors:
        print(f"Registry validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Registry validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Resolve active paper-policy hard and soft rules from paper context."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from policy_vocab import (
    ARTIFACT_KINDS,
    CONTEXT_VALUE_VOCABS,
    FEATURES,
    SCOPES,
    canonical_task_mode,
    valid_task_mode,
)
from validate_registry import load_yaml, validate_registry


CONTEXT_FIELDS = {
    "version",
    "paper_type",
    "domain",
    "venue",
    "submission_stage",
    "language",
    "double_blind",
    "page_pressure",
    "evidence_maturity",
    "manuscript_state",
    "reader_risk",
    "task_scope",
    "task_mode",
    "modes",
    "policy_sets",
    "artifact_mode",
    "structure_profile",
    "evaluation_structure",
    "table_profile",
    "experiment_type",
    "measurement_bias_status",
    "evidence_structure",
    "scopes",
    "artifacts",
    "features",
    "approved_citation_sources",
    "primary_tex",
    "additional_tex",
    "venue_source",
    "venue_sources",
    "provenance",
}
LIST_FIELDS = {
    "modes", "scopes", "artifacts", "features", "approved_citation_sources",
    "additional_tex", "policy_sets",
}
SCALAR_OR_LIST_FIELDS = {"artifact_mode"}
SENSITIVE_FIELDS = {"venue", "double_blind", "submission_stage"}
PROVENANCE_VALUES = {"user", "official", "template", "manuscript", "inferred"}
TRUSTED_PROVENANCE = PROVENANCE_VALUES - {"inferred"}
VENUE_SOURCE_KINDS = {"official", "template", "user"}
VENUE_CONSTRAINTS = {
    "all", "page_limit", "anonymity", "mandatory_statements",
    "section_numbering", "appendix", "formatting", "submission_process",
}


def _values(value: Any) -> set[Any]:
    if value is None:
        return set()
    if isinstance(value, list):
        return set(value)
    return {value}


def validate_context(context: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    unknown = sorted(set(context) - CONTEXT_FIELDS)
    if unknown:
        errors.append(f"context: unknown fields {', '.join(unknown)}")
    if context.get("version") != 1:
        errors.append("context.version: expected 1")

    for required in ("scopes", "artifacts"):
        if required not in context:
            errors.append(f"context.{required}: required for policy applicability")
        elif context.get(required) == []:
            errors.append(f"context.{required}: must not be empty")
    if context.get("task_scope") in {
        "section",
        "artifact",
        "multi_section",
        "full_paper",
        "polish",
        "submission",
        "rebuttal",
    } and not context.get("features"):
        errors.append(
            "context.features: at least one semantic selector is required for section, artifact, or complex work"
        )

    for field in LIST_FIELDS:
        value = context.get(field)
        if value is None:
            continue
        if not isinstance(value, list):
            errors.append(f"context.{field}: expected list")
        elif any(not isinstance(item, str) or not item for item in value):
            errors.append(f"context.{field}: entries must be non-empty strings")
        elif field == "policy_sets" and not value:
            errors.append("context.policy_sets: must not be empty")
        elif field == "policy_sets" and len(value) != len(set(value)):
            errors.append("context.policy_sets: duplicate set names are not allowed")

    for field in SCALAR_OR_LIST_FIELDS:
        value = context.get(field)
        if value is None:
            continue
        values = value if isinstance(value, list) else [value]
        if not values:
            errors.append(f"context.{field}: list must not be empty")
        elif any(not isinstance(item, str) or not item for item in values):
            errors.append(
                f"context.{field}: expected a non-empty string or a non-empty list of strings"
            )

    enum_lists = {
        "scopes": SCOPES,
        "artifacts": ARTIFACT_KINDS,
        "features": FEATURES,
    }
    for field, allowed in enum_lists.items():
        value = context.get(field)
        if isinstance(value, list):
            invalid = sorted(set(value) - allowed)
            if invalid:
                errors.append(f"context.{field}: invalid values {invalid}")

    for field in ("task_mode", "modes"):
        values = context.get(field, [])
        values = values if isinstance(values, list) else [values]
        invalid = [value for value in values if value is not None and not valid_task_mode(value)]
        if invalid:
            errors.append(
                f"context.{field}: unknown task mode(s) {invalid}; use a canonical mode or documented alias"
            )

    for field, allowed in CONTEXT_VALUE_VOCABS.items():
        value = context.get(field)
        values = value if isinstance(value, list) else [value]
        invalid = [
            item
            for item in values
            if item is not None
            and (not isinstance(item, str) or item not in allowed)
        ]
        if invalid:
            errors.append(f"context.{field}: invalid value(s) {invalid!r}")

    for field, value in context.items():
        if field in LIST_FIELDS | SCALAR_OR_LIST_FIELDS | {
            "version", "double_blind", "venue_source", "venue_sources", "provenance"
        }:
            continue
        if value is not None and (not isinstance(value, str) or not value):
            errors.append(f"context.{field}: expected non-empty string or null")

    if "double_blind" in context and not isinstance(context["double_blind"], bool):
        errors.append("context.double_blind: expected boolean")

    provenance = context.get("provenance", {})
    if not isinstance(provenance, dict):
        errors.append("context.provenance: expected mapping")
    else:
        for field, source in provenance.items():
            if field not in CONTEXT_FIELDS - {"version", "provenance"}:
                errors.append(f"context.provenance: unknown field {field!r}")
            if source not in PROVENANCE_VALUES:
                errors.append(f"context.provenance.{field}: invalid source {source!r}")

    venue_source = context.get("venue_source")
    venue_sources = context.get("venue_sources")
    if venue_source is not None and venue_sources is not None:
        errors.append("context: use venue_sources or legacy venue_source, not both")
    if venue_source is not None:
        if not isinstance(venue_source, dict):
            errors.append("context.venue_source: expected mapping")
        else:
            unknown_venue = sorted(set(venue_source) - {"url", "as_of"})
            if unknown_venue:
                errors.append(
                    f"context.venue_source: unknown fields {', '.join(unknown_venue)}"
                )
            for field in ("url", "as_of"):
                value = venue_source.get(field)
                if value is not None and not (
                    (isinstance(value, str) and value) or (field == "as_of" and isinstance(value, date))
                ):
                    errors.append(
                        f"context.venue_source.{field}: expected non-empty string or null"
                    )
    if venue_sources is not None:
        if not isinstance(venue_sources, list) or not venue_sources:
            errors.append("context.venue_sources: expected non-empty list")
        else:
            seen_source_ids: set[str] = set()
            for index, raw_source in enumerate(venue_sources):
                where = f"context.venue_sources[{index}]"
                if not isinstance(raw_source, dict):
                    errors.append(f"{where}: expected mapping")
                    continue
                unknown_source = sorted(
                    set(raw_source) - {"id", "kind", "locator", "as_of", "constraints"}
                )
                if unknown_source:
                    errors.append(
                        f"{where}: unknown fields {', '.join(unknown_source)}"
                    )
                source_id = raw_source.get("id")
                if not isinstance(source_id, str) or not re.fullmatch(
                    r"[a-z0-9]+(?:-[a-z0-9]+)*", source_id
                ):
                    errors.append(f"{where}.id: invalid source ID {source_id!r}")
                elif source_id in seen_source_ids:
                    errors.append(f"{where}.id: duplicate source ID {source_id}")
                else:
                    seen_source_ids.add(source_id)
                kind = raw_source.get("kind")
                if kind not in VENUE_SOURCE_KINDS:
                    errors.append(f"{where}.kind: invalid value {kind!r}")
                locator = raw_source.get("locator")
                if not isinstance(locator, str) or not locator:
                    errors.append(f"{where}.locator: required non-empty string")
                elif kind == "official" and not re.match(r"https?://", locator):
                    errors.append(f"{where}.locator: official source requires HTTP(S) URL")
                as_of = raw_source.get("as_of")
                if not (
                    (isinstance(as_of, str) and as_of) or isinstance(as_of, date)
                ):
                    errors.append(f"{where}.as_of: required date or non-empty string")
                constraints = raw_source.get("constraints")
                if not isinstance(constraints, list) or not constraints:
                    errors.append(f"{where}.constraints: expected non-empty list")
                elif any(not isinstance(item, str) for item in constraints):
                    errors.append(f"{where}.constraints: entries must be strings")
                else:
                    invalid_constraints = sorted(set(constraints) - VENUE_CONSTRAINTS)
                    if invalid_constraints:
                        errors.append(
                            f"{where}.constraints: invalid values {invalid_constraints}"
                        )
    return errors


def normalize_context(context: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Canonicalize accepted aliases while retaining an explicit audit trail."""
    normalized = dict(context)
    notes: list[str] = []
    mode = normalized.get("task_mode")
    canonical = canonical_task_mode(mode)
    if canonical != mode:
        normalized["task_mode"] = canonical
        notes.append(f"task_mode alias {mode!r} normalized to {canonical!r}.")
    if isinstance(normalized.get("modes"), list):
        canonical_modes = [canonical_task_mode(item) for item in normalized["modes"]]
        for original, replacement in zip(normalized["modes"], canonical_modes):
            if original != replacement:
                notes.append(f"modes alias {original!r} normalized to {replacement!r}.")
        normalized["modes"] = canonical_modes
    legacy_venue_source = normalized.get("venue_source")
    if (
        isinstance(legacy_venue_source, dict)
        and legacy_venue_source.get("url")
        and legacy_venue_source.get("as_of")
        and "venue_sources" not in normalized
    ):
        normalized.pop("venue_source")
        normalized["venue_sources"] = [
            {
                "id": "legacy-official-source",
                "kind": "official",
                "locator": legacy_venue_source.get("url"),
                "as_of": legacy_venue_source.get("as_of"),
                "constraints": ["all"],
            }
        ]
    return normalized, notes


def _trusted_for_hard(context: dict[str, Any], field: str) -> bool:
    if field not in SENSITIVE_FIELDS:
        return True
    provenance = context.get("provenance", {})
    return isinstance(provenance, dict) and provenance.get(field) in TRUSTED_PROVENANCE


def _profile_matches(profile: dict[str, Any], context: dict[str, Any]) -> bool:
    match = profile["match"]
    field = match["field"]
    if not _trusted_for_hard(context, field):
        return False
    actual = _values(context.get(field))
    if field == "task_mode":
        actual |= _values(context.get("modes"))
    return bool(actual & _values(match["any_of"]))


def _hard_activation_reason(
    rule: dict[str, Any], context: dict[str, Any], active_profiles: set[str]
) -> str | None:
    activation = rule["activation"]
    kind = activation["type"]
    expected = _values(activation["when"])
    if kind == "always":
        return "always"
    if kind == "profile":
        matched = sorted(expected & active_profiles)
        return f"profile:{','.join(matched)}" if matched else None
    if kind == "feature":
        matched = sorted(expected & _values(context.get("features")))
        return f"feature:{','.join(matched)}" if matched else None
    if kind == "mode":
        actual = _values(context.get("task_mode")) | _values(context.get("modes"))
        matched = sorted(expected & actual)
        return f"mode:{','.join(matched)}" if matched else None
    if kind == "paper_type":
        matched = sorted(expected & _values(context.get("paper_type")))
        return f"paper_type:{','.join(matched)}" if matched else None
    if kind == "stage":
        if not _trusted_for_hard(context, "submission_stage"):
            return None
        matched = sorted(expected & _values(context.get("submission_stage")))
        return f"stage:{','.join(matched)}" if matched else None
    if kind == "venue":
        if "specified" in expected and context.get("venue") and _trusted_for_hard(context, "venue"):
            return "venue:specified"
        return None
    return None


def _rule_applies(rule: dict[str, Any], context: dict[str, Any]) -> bool:
    scopes = _values(context.get("scopes"))
    artifacts = _values(context.get("artifacts"))
    features = _values(context.get("features"))
    phase = context.get("submission_stage")
    if not (scopes & _values(rule.get("scope"))):
        return False
    if not (artifacts & _values(rule.get("artifacts"))):
        return False
    if rule.get("features") and not (features & _values(rule.get("features"))):
        return False
    if phase is not None and phase not in _values(rule.get("phases")):
        return False
    return True


def _resolve_policy_sets(
    context: dict[str, Any], policy_sets_doc: dict[str, Any]
) -> tuple[list[str], set[str], set[str], list[str]]:
    """Expand requested policy sets and return enabled hard/soft rule IDs."""
    set_docs = {item["id"]: item for item in policy_sets_doc["sets"]}
    requested = context.get("policy_sets")
    notes: list[str] = []
    if requested is None:
        requested = list(policy_sets_doc["default_sets"])
        context["policy_sets"] = requested
        notes.append(
            "No policy_sets were supplied; applied the public default policy sets."
        )
    unknown = sorted(set(requested) - set(set_docs))
    if unknown:
        raise ValueError(f"context.policy_sets: unknown policy set(s) {unknown}")

    expanded: list[str] = []
    seen: set[str] = set()

    def add(set_id: str) -> None:
        if set_id in seen:
            return
        for included in set_docs[set_id].get("includes", []):
            add(included)
        seen.add(set_id)
        expanded.append(set_id)

    for set_id in requested:
        add(set_id)

    hard_ids: set[str] = set()
    soft_ids: set[str] = set()
    for set_id in expanded:
        hard_ids.update(set_docs[set_id].get("hard_rules", []))
        soft_ids.update(set_docs[set_id].get("soft_rules", []))
    return expanded, hard_ids, soft_ids, notes


def resolve_policy(
    context: dict[str, Any],
    hard_doc: dict[str, Any],
    soft_doc: dict[str, Any],
    profiles_doc: dict[str, Any],
    policy_sets_doc: dict[str, Any],
) -> dict[str, Any]:
    context_errors = validate_context(context)
    if context_errors:
        raise ValueError("; ".join(context_errors))

    context, normalization_notes = normalize_context(context)

    active_policy_sets, enabled_hard_ids, enabled_soft_ids, policy_set_notes = (
        _resolve_policy_sets(context, policy_sets_doc)
    )

    warnings: list[str] = list(normalization_notes)
    unverified: list[dict[str, str]] = []
    provenance = context.get("provenance", {})
    for field in sorted(SENSITIVE_FIELDS):
        if field not in context:
            continue
        source = provenance.get(field) if isinstance(provenance, dict) else None
        if source not in TRUSTED_PROVENANCE:
            reason = "inferred" if source == "inferred" else "missing provenance"
            unverified.append({"field": field, "reason": reason})
            warnings.append(
                f"{field} did not activate hard rules or profiles because its provenance is {reason}."
            )

    matched_profile_docs = [
        profile for profile in profiles_doc["profiles"] if _profile_matches(profile, context)
    ]
    active_profile_docs = [
        profile
        for profile in matched_profile_docs
        if set(profile.get("activate_hard", [])) & enabled_hard_ids
        or set(profile.get("prefer_soft", [])) & enabled_soft_ids
    ]
    inactive_profile_ids = sorted(
        {profile["id"] for profile in matched_profile_docs}
        - {profile["id"] for profile in active_profile_docs}
    )
    for profile_id in inactive_profile_ids:
        policy_set_notes.append(
            f"Profile {profile_id!r} matched context but has no rules in the active policy sets."
        )
    active_profile_ids = {profile["id"] for profile in active_profile_docs}

    if context.get("venue") and _trusted_for_hard(context, "venue"):
        venue_sources = context.get("venue_sources", [])
        authoritative_sources = [
            source
            for source in venue_sources
            if isinstance(source, dict)
            and source.get("kind") in {"official", "user"}
            and source.get("locator")
            and source.get("as_of")
        ]
        if not authoritative_sources:
            warnings.append(
                "Trusted venue is specified, but no current official or user-provided venue rule source is recorded; template records alone do not establish all venue constraints."
            )

    active_hard: list[dict[str, Any]] = []
    for rule in hard_doc["rules"]:
        if rule["id"] not in enabled_hard_ids:
            continue
        reason = _hard_activation_reason(rule, context, active_profile_ids)
        if reason is None or not _rule_applies(rule, context):
            continue
        active_hard.append(
            {
                "id": rule["id"],
                "title": rule["title"],
                "activation_reason": reason,
                "scope": rule["scope"],
                "artifacts": rule["artifacts"],
                "requirement": rule["requirement"],
                "checks": rule["checks"],
            }
        )

    preferred_by: dict[str, list[str]] = {}
    for profile in active_profile_docs:
        for rule_id in profile.get("prefer_soft", []):
            preferred_by.setdefault(rule_id, []).append(profile["id"])

    active_soft: list[dict[str, Any]] = []
    for rule in soft_doc["rules"]:
        if rule["id"] not in enabled_soft_ids:
            continue
        if not _rule_applies(rule, context):
            continue
        active_soft.append(
            {
                "id": rule["id"],
                "title": rule["title"],
                "scope": rule["scope"],
                "artifacts": rule["artifacts"],
                "features": rule.get("features", []),
                "default": rule["default"],
                "allowed_variants": rule["allowed_variants"],
                "selection_factors": rule["selection_factors"],
                "avoid": rule["avoid"],
                "report_when": rule["report_when"],
                "preferred_by_profiles": sorted(preferred_by.get(rule["id"], [])),
            }
        )

    return {
        "resolver_version": 2,
        "context": context,
        "active_policy_sets": active_policy_sets,
        "policy_set_notes": policy_set_notes,
        "inactive_profiles": inactive_profile_ids,
        "active_profiles": [profile["id"] for profile in active_profile_docs],
        "context_warnings": warnings,
        "unverified_context": unverified,
        "active_hard": active_hard,
        "active_soft": active_soft,
    }


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    refs = script_dir.parent / "references"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("context", type=Path)
    parser.add_argument("--hard", type=Path, default=refs / "hard-rules.yaml")
    parser.add_argument("--soft", type=Path, default=refs / "soft-rules.yaml")
    parser.add_argument("--profiles", type=Path, default=refs / "profiles.yaml")
    parser.add_argument("--decisions", type=Path, default=refs / "decision-baseline.yaml")
    parser.add_argument("--policy-sets", type=Path, default=refs / "policy-sets.yaml")
    parser.add_argument("--format", choices=("yaml", "json"), default="yaml")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    registry_errors = validate_registry(
        args.hard,
        args.soft,
        args.profiles,
        args.decisions,
        args.policy_sets,
    )
    if registry_errors:
        print("Registry validation failed:", file=sys.stderr)
        for error in registry_errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    try:
        context = load_yaml(args.context)
        result = resolve_policy(
            context,
            load_yaml(args.hard),
            load_yaml(args.soft),
            load_yaml(args.profiles),
            load_yaml(args.policy_sets),
        )
    except ValueError as exc:
        print(f"Policy resolution failed: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        rendered = json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n"
    else:
        rendered = yaml.safe_dump(result, sort_keys=False, allow_unicode=True)
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Controlled vocabularies shared by paper-policy validation and resolution."""

from __future__ import annotations

from typing import Any


SCOPES = {"writing", "review", "figures", "tables", "citations", "workflow"}

ARTIFACT_KINDS = {
    "policy",
    "prose",
    "tex",
    "bibtex",
    "figure",
    "table",
    "paper_outline",
}

PHASES = {"outline", "draft", "polish", "submission", "rebuttal", "camera_ready"}

FEATURES = {
    "abstract",
    "introduction",
    "conclusion",
    "contribution_list",
    "evaluation_section",
    "related_work",
    "related_work_table",
    "result_table",
    "data_table",
    "latex_manuscript",
    "paper_prose",
    "paper_figure",
    "data_figure",
    "conceptual_figure",
    "threats_to_validity",
    "limitations_content",
}

TASK_MODES = {
    "writing",
    "figure_creation",
    "related_work_full",
    "background_and_related_work_full",
    "citation_audit",
    "final_citation_check",
    "reproducibility_check",
    "submission_readiness",
    "paper_run_final",
    "architecture_review",
    "cold_reader",
    "comprehension_test",
    "anti_ai_cleanup",
    "prose_cleanup",
    "writing_anti_ai",
    "authorship_review",
    "detector_review",
    "self_review",
    "formal_review",
    "external_review_analysis",
    "rebuttal",
    "revision_verification",
    "synthetic_results",
    "placeholder_results",
    "style_mining",
    "semantic_mutation",
    "bibliography_rewrite",
    "autofix",
}

TASK_MODE_ALIASES = {
    "anti-ai-cleanup": "anti_ai_cleanup",
    "writing-anti-ai": "writing_anti_ai",
    "prose-polish": "prose_cleanup",
    "prose_polish": "prose_cleanup",
    "pre_submission_audit": "self_review",
    "reviewer_panel": "self_review",
    "style-mining": "style_mining",
}

PROFILE_MATCH_FIELDS = {
    "submission_stage",
    "artifact_mode",
    "task_mode",
    "double_blind",
    "paper_type",
    "experiment_type",
    "measurement_bias_status",
    "evidence_structure",
    "structure_profile",
    "evaluation_structure",
    "task_scope",
}

CONTEXT_VALUE_VOCABS = {
    "submission_stage": PHASES,
    "artifact_mode": {"draft", "final", "final_figure", "final_table"},
    "paper_type": {
        "empirical",
        "security",
        "systems",
        "protocol",
        "sok",
        "theoretical",
        "qualitative",
        "mixed_methods",
        "survey",
        "position",
        "experience",
        "benchmark",
        "dataset",
        "tool",
    },
    "experiment_type": {"deterministic", "stochastic", "multi_run"},
    "measurement_bias_status": {
        "none_known",
        "known_systematic",
        "characterized_missingness",
    },
    "evidence_structure": {
        "single_role",
        "multi_role",
        "tiered",
        "validation_and_substantive",
    },
    "structure_profile": {"standard_conference", "venue_defined"},
    "evaluation_structure": {"rq_driven", "claim_driven", "exploratory"},
    "task_scope": {"short", "section", "artifact", "multi_section", "full_paper", "polish", "submission", "rebuttal"},
}


def canonical_task_mode(value: Any) -> Any:
    """Return the canonical mode for a string, preserving non-strings for validation."""
    if not isinstance(value, str):
        return value
    return TASK_MODE_ALIASES.get(value, value)


def valid_task_mode(value: Any) -> bool:
    return isinstance(value, str) and canonical_task_mode(value) in TASK_MODES

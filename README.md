# Academic Paper Skills

English | [简体中文](README.zh-CN.md)

Academic Paper Skills is a compact Codex skill bundle for academic paper workflows. It contains four sibling skills that must stay version-aligned:

- `paper-policy`: shared hard/soft rule resolution, deterministic lint, evidence-backed assessment, and readiness reporting.
- `paper-writing`: prose drafting and revision for abstracts, introductions, RQ framing, related work, methods, results narratives, discussions, limitations, conclusions, claim calibration, citation-aware writing, and academic prose cleanup.
- `paper-figures-tables`: publication-ready LaTeX tables, related-work comparison tables, result tables, source-data-driven plots, conceptual figures, captions, artifact specs, and visual QA.
- `paper-review`: pre-submission audit, reviewer simulation, red-team review, rebuttal planning, rebuttal drafting, revision verification, and submission-readiness checks.

The bundle is intentionally narrow. It does not include literature search, reference verification, experiment execution, or project-management workflows.

The public default is deliberately portable rather than opinionated. It enables
`integrity-core` and `academic-defaults`; optional formatting and structural
preferences live in `strict-house-style`, which is disabled until a project
explicitly selects it.

## Policy Sets

Omit `policy_sets` from `paper_context.yaml` to use the public defaults:

```yaml
policy_sets: [integrity-core, academic-defaults]
```

Opt into the stricter formatting and structure profile explicitly:

```yaml
policy_sets: [strict-house-style]
```

The strict set includes the public sets transitively. Its hard rules remain
hard after opt-in; reliable venue requirements may still override conflicting
house formatting or structure.

## Design Principles

- Keep claims scoped, evidence-forward, and easy to audit.
- Use traditional, concise top-level section names when the optional strict set is active; otherwise adapt headings to the paper and venue.
- Treat user-declared citation and evidence sources as the source of truth.
- Never invent citations, paper claims, venues, years, baselines, metrics, p-values, or experimental results.
- Prompt the user to manually update BibTeX when a needed citation is missing.
- Require a related-work comparison-table plan only when the optional strict rule is active; otherwise propose one when it improves the argument.
- Keep tables compact and argumentative; apply `booktabs`, marker, placement, and resizing house rules only when enabled.
- For an explicitly justified wide Related Work matrix, use `table_profile: layered_capability_matrix` to group capabilities by semantic layer; coverage-delta highlights remain evidence-bound and color is never the sole cue.
- Use source-data-driven Python plots for numeric figures.
- Select conceptual-figure tooling from topology, editability, venue constraints, and enabled policy; generative rendering is an optional house default.
- Keep review work separate from writing and artifact creation: diagnose first, then route substantial rewrites to `paper-writing` or artifact changes to `paper-figures-tables`.

## Installation

Clone the repository and copy all four skill folders into your Codex skills directory as one versioned bundle:

```bash
git clone https://github.com/DELONG-L/Academic-Paper-Skills.git
mkdir -p ~/.codex/skills
cp -R Academic-Paper-Skills/paper-policy ~/.codex/skills/
cp -R Academic-Paper-Skills/paper-writing ~/.codex/skills/
cp -R Academic-Paper-Skills/paper-figures-tables ~/.codex/skills/
cp -R Academic-Paper-Skills/paper-review ~/.codex/skills/
```

Start a new Codex thread after installation so the skills list refreshes.

## Usage Examples

```text
Use $paper-writing to rewrite this introduction with clearer RQs and scoped claims.
```

```text
Use $paper-figures-tables to turn this related-work table spec into compact LaTeX.
```

For a wide, layered capability matrix, add this controlled context value:

```yaml
table_profile: layered_capability_matrix
```

```text
Use $paper-review to audit this manuscript before submission and produce a prioritized issue board.
```

## Folder Layout

```text
Academic-Paper-Skills/
├── paper-policy/
├── paper-writing/
├── paper-figures-tables/
├── paper-review/
├── README.md
├── README.zh-CN.md
├── requirements-policy.txt
├── requirements-figures.txt
├── LICENSE
└── THIRD_PARTY_NOTICES.md
```

Each skill folder is self-contained and includes its own `SKILL.md`, optional `references/`, optional `scripts/`, and UI metadata under `agents/`.

## Requirements

- Codex with local skill support.
- Python 3.10 or newer.
- `PyYAML` for `paper-policy`: `python3 -m pip install -r requirements-policy.txt`.
- Optional figure/table packages: `python3 -m pip install -r requirements-figures.txt`.
- LaTeX tooling only when you want to compile or visually verify a paper project.

## Citation Policy

This bundle does not perform automatic literature verification. Use the citation
and evidence sources declared by the user or project; local `.bib` files and
user-provided notes are the default. When support is unavailable, emit a manual
update request instead of fabricating a reference.

## License

MIT. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

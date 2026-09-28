# Repository structure and naming

English · [简体中文](architecture.zh-CN.md) · [Home](../README.md)

## Stable skill boundaries

The four top-level `paper-*` directories are independently discoverable skills installed together. Their sibling paths are part of the integration contract; moving them into a new wrapper directory would break existing references and installation instructions.

| Directory | Owns | Routes elsewhere |
|---|---|---|
| `paper-writing/` | Manuscript prose, evidence integration, section revision | Finished visual artifacts go to figures/tables; critique and replies go to review. |
| `paper-figures-tables/` | Tables, data plots, conceptual diagrams, captions and artifact QA | Manuscript prose goes to writing; formal requirements resolve through policy. |
| `paper-review/` | Author-side critique, rebuttals, revision verification | Implements prose through writing and final artifacts through figures/tables. |
| `paper-policy/` | Requirement registries, applicability, source checks, evidence assessment | Presentation preferences remain in task guides rather than becoming universal rules. |

A skill uses `SKILL.md` for scope and routing, `references/` for selectively loaded detail, `agents/openai.yaml` for display metadata, and `scripts/` only when executable helpers add value. Tests stay beside the helpers they exercise; fixtures belong to that script suite. A prose-only skill need not have an empty scripts directory.

## Repository-level material

- `README.md` and `README.zh-CN.md`: equivalent user-facing entrypoints.
- `docs/`: installation and architecture guides; brand provenance and resources.
- `docs/assets/`: editable SVGs, the generated design reference and its prompt.
- `scripts/`: repository-wide checks and deterministic brand-source generation.
- `.github/`: CI, issue forms and a pull-request template.
- `requirements-policy.txt` and `requirements-figures.txt`: separate dependency groups; existing filenames remain stable.
- `CONTRIBUTING.md` and its Chinese counterpart: contribution workflow.
- `CHANGELOG.md`, `LICENSE`, `THIRD_PARTY_NOTICES.md`: changes and provenance.

## Naming conventions

| Item | Convention | Example |
|---|---|---|
| Skill directory / frontmatter name | Same lowercase kebab-case identifier | `paper-figures-tables` |
| Reference documents | Descriptive kebab-case | `conceptual-vector-rebuild.md` |
| Python modules and tests | Importable snake_case; tests start with `test_` | `check_artifacts.py`, `test_check_artifacts.py` |
| Paired documentation | English base filename; `.zh-CN.md` Chinese suffix | `getting-started.md`, `getting-started.zh-CN.md` |
| Localized visual assets | Base name plus language code | `hero-en.svg`, `hero-zh-CN.svg` |
| Required/conventional files | Preserve recognized names | `SKILL.md`, `README.md`, `LICENSE`, `openai.yaml` |

Product name: **Academic Paper Skills**. Chinese descriptive name: **学术论文技能集**. Use the existing technical skill identifiers in commands and paths. Keep the repository URL stable rather than renaming it for cosmetic consistency.

## Validation boundaries

`python scripts/check_repository.py` checks public documentation links and anchors, language-pair navigation, skill identity/display metadata, and safe self-contained SVG resources. CI also validates the rule registry, audits cross-skill references, compiles helpers and runs the existing tests.

These checks establish structural consistency and tested behavior. They do not establish visual quality, scientific validity, end-to-end ImageGen reliability or manuscript readiness. Inspect changed visuals and validate the actual manuscript artifacts separately.

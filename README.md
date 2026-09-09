# Academic Paper Skills

English | [简体中文](README.zh-CN.md)

A coordinated set of Codex skills for rigorous academic writing, manuscript review, and publication-ready figures and tables.

| Skill | What it does |
|---|---|
| [paper-writing](paper-writing/SKILL.md) | Draft and revise manuscript prose, strengthen arguments, and integrate citations. |
| [paper-review](paper-review/SKILL.md) | Review the author's manuscript, draft reviewer responses, and verify revisions. |
| [paper-figures-tables](paper-figures-tables/SKILL.md) | Create tables, reproducible data plots, and conceptual figures. |
| [paper-policy](paper-policy/SKILL.md) | Apply manuscript requirements and assess readiness against evidence. |

The workflow keeps claims grounded in evidence while adapting structure and presentation to the paper, author, and venue.

## Installation

Install all four skills together:

```bash
git clone https://github.com/DELONG-L/Academic-Paper-Skills.git
cd Academic-Paper-Skills
mkdir -p ~/.codex/skills
cp -R paper-policy paper-writing paper-review paper-figures-tables ~/.codex/skills/
python3 -m pip install -r requirements-policy.txt
```

Python 3.10+ is recommended. For plotting helpers, also install `requirements-figures.txt`. Compiling manuscripts requires a LaTeX installation.

When upgrading, back up and replace the four existing skill folders. Start a new Codex task after installation.

## Usage

Invoke a skill with your manuscript, data, or reviewer comments:

```text
Use $paper-writing to revise this introduction and sharpen its contribution.
```

```text
Use $paper-review to check the argument structure and suggest specific edits.
```

Each skill's linked guide above contains its detailed workflow and tools.

## License and acknowledgments

MIT. See [LICENSE](LICENSE).

Workflow inspiration and third-party attributions are documented in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), including acknowledgments to [claude-scholar](https://github.com/OniReimu/claude-scholar) and [scipilot-figure-skill](https://github.com/Haojae/scipilot-figure-skill).

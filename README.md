# Academic Paper Skills

English | [简体中文](README.zh-CN.md)

Academic Paper Skills is a compact Codex skill bundle for academic paper workflows. It contains three main skills:

- `paper-writing`: prose drafting and revision for abstracts, introductions, RQ framing, related work, methods, results narratives, discussions, limitations, conclusions, claim calibration, citation-aware writing, and academic prose cleanup.
- `paper-figures-tables`: publication-ready LaTeX tables, related-work comparison tables, result tables, source-data-driven plots, conceptual figures, captions, artifact specs, and visual QA.
- `paper-review`: pre-submission audit, reviewer simulation, red-team review, rebuttal planning, rebuttal drafting, revision verification, and submission-readiness checks.

The bundle is intentionally narrow. It does not include literature search, reference verification, experiment execution, or project-management workflows.

## Design Principles

- Keep claims scoped, evidence-forward, and easy to audit.
- Use traditional, concise top-level section names.
- Treat local `.bib` files and user-provided notes as the citation source of truth.
- Never invent citations, paper claims, venues, years, baselines, metrics, p-values, or experimental results.
- Prompt the user to manually update BibTeX when a needed citation is missing.
- Require a related-work comparison-table plan unless the user explicitly waives it or the venue forbids tables.
- Keep tables compact and argumentative; use `booktabs` and `resizebox` for target column alignment unless the natural table already fits cleanly.
- Use source-data-driven Python plots for numeric figures.
- Use a generative image model for non-data conceptual figures by default, with an editable `structure.svg` as the structural reference for Figure 1, system overviews, pipelines, architectures, and threat models.
- Keep review work separate from writing and artifact creation: diagnose first, then route substantial rewrites to `paper-writing` or artifact changes to `paper-figures-tables`.

## Installation

Clone the repository and copy the three skill folders into your Codex skills directory:

```bash
git clone https://github.com/DELONG-L/Academic-Paper-Skills.git
mkdir -p ~/.codex/skills
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

```text
Use $paper-review to audit this manuscript before submission and produce a prioritized issue board.
```

## Folder Layout

```text
Academic-Paper-Skills/
├── paper-writing/
├── paper-figures-tables/
├── paper-review/
├── README.md
├── README.zh-CN.md
├── LICENSE
└── THIRD_PARTY_NOTICES.md
```

Each skill folder is self-contained and includes its own `SKILL.md`, optional `references/`, optional `scripts/`, and UI metadata under `agents/`.

## Requirements

- Codex with local skill support.
- Python 3 for the figure/table helper scripts.
- Optional Python packages for artifact QA and plotting, depending on the task: `matplotlib`, `numpy`, `pandas`, `seaborn`, `Pillow`, and `pypdf`.
- LaTeX tooling only when you want to compile or visually verify a paper project.

## Citation Policy

This bundle does not perform automatic literature verification. If a draft needs a citation that is not already present in the local `.bib` file or user-provided notes, the workflow should emit a manual BibTeX update request instead of fabricating the reference.

## License

MIT. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

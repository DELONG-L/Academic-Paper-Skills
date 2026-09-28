<p align="center">
  <img src="docs/assets/hero-en.svg" alt="Academic Paper Skills — from evidence to manuscript" width="100%">
</p>

<h1 align="center">Academic Paper Skills</h1>
<p align="center">Four coordinated Codex skills for writing, figures, review, and manuscript requirements.</p>

<p align="center">
  <a href="https://github.com/DELONG-L/Academic-Paper-Skills/actions/workflows/ci.yml"><img src="https://github.com/DELONG-L/Academic-Paper-Skills/actions/workflows/ci.yml/badge.svg" alt="Validation workflow status"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-173F35" alt="License: MIT"></a>
  <a href="docs/getting-started.md"><img src="https://img.shields.io/badge/tested_with-Python_3.11-526A5D" alt="Tested with Python 3.11"></a>
</p>

<p align="center"><strong>English</strong> · <a href="README.zh-CN.md">简体中文</a></p>
<p align="center"><a href="#choose-a-skill">Choose a skill</a> · <a href="#quick-start">Quick start</a> · <a href="#try-it">Examples</a> · <a href="docs/architecture.md">Repository guide</a></p>

Bring a manuscript, research evidence, data, or reviewer comments. These skills help turn them into supported prose, readable artifacts, and revisions you can trace back to the source. Use the skill that matches the current task; install the four together so their shared guidance resolves correctly.

<a id="choose-a-skill"></a>
## Choose a skill

| Your task | Skill | Typical deliverable |
|---|---|---|
| Draft or revise an argument | [paper-writing](paper-writing/SKILL.md) | Evidence-grounded sections, integrated citations, calibrated claims |
| Explain a method or present results | [paper-figures-tables](paper-figures-tables/SKILL.md) | Editable diagrams, reproducible plots, publication-ready tables |
| Inspect a draft or answer reviewers | [paper-review](paper-review/SKILL.md) | Prioritized issues, author responses, verified revision closure |
| Resolve manuscript requirements | [paper-policy](paper-policy/SKILL.md) | Applicable requirements, source checks, evidence-bounded assessment |

Author-side manuscript review is included. Assigned external peer review is outside this bundle.

<a id="quick-start"></a>
## Quick start

For a **fresh installation** on macOS or Linux, clone the repository and copy the four skill folders into Codex's skills directory:

```bash
git clone https://github.com/DELONG-L/Academic-Paper-Skills.git
cd Academic-Paper-Skills
skills_dir="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$skills_dir"
cp -R paper-policy paper-writing paper-review paper-figures-tables "$skills_dir/"
```

If any of these folders already exist, use the [upgrade instructions](docs/getting-started.md#upgrade) to preserve local changes and avoid stale files. Start a new Codex task after installation.

The skill instructions are Markdown. To run the Python checks, create an isolated environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-policy.txt
# Also install this for plotting and figure utilities:
python -m pip install -r requirements-figures.txt
```

Python 3.10+ is recommended; CI tests Python 3.11. ImageGen design requires the available `imagegen` skill and image-generation tool. LaTeX project compilation needs an appropriate compiler. See [setup, upgrades, and troubleshooting](docs/getting-started.md) for details.

<a id="try-it"></a>
## Try it

**Write from evidence**

```text
Use $paper-writing to revise this introduction. Preserve the research question,
ground the contribution in the supplied results, and flag unsupported claims.
```

**Design a figure**

```text
Use $paper-figures-tables to design a two-column method overview from this section.
Define the components and connections, design with ImageGen, then rebuild editable
SVG. Check information density and readability at the manuscript's final width.
```

**Close a revision**

```text
Use $paper-review to compare these reviewer comments with the revised manuscript.
Identify what is resolved, what evidence is missing, and what still needs editing.
```

**Check applicable requirements**

```text
Use $paper-policy to assess this submission against the supplied venue instructions.
Separate verified source checks from judgments that still need human evidence.
```

<a id="how-it-works"></a>
## How it works

| Area | Working approach |
|---|---|
| Writing | Start from the question and evidence; adapt structure to the argument and venue. |
| Conceptual figures | Define content and placement → ImageGen design → editable SVG → semantic, visual, and final-size checks. |
| Experimental plots | Generate from real data; default to **at least 2 panels per row in one column, 4 when spanning both columns**. |
| Experimental tables | No extra density quota for small single-column tables; review information density for cross-column tables. |
| Review and requirements | Trace issues and judgments to sources. Automated checks and agent inspection do not establish scientific validity or human sign-off. |

Layout counts are this skill's defaults, not conference rules. Preserve readability and meaningful comparisons; never invent evidence or duplicate panels to fill a grid. Explicit user choices and applicable venue requirements take precedence. See the [conceptual workflow](paper-figures-tables/references/conceptual-figures.md) and [style guide](paper-figures-tables/references/conceptual-style-reference.md).

<a id="repository-map"></a>
## Repository map

```text
Academic-Paper-Skills/
├── paper-writing/          # Prose and argument
├── paper-figures-tables/   # Diagrams, plots, and tables
├── paper-review/           # Author review and revisions
├── paper-policy/           # Requirements and evidence checks
├── docs/                  # Bilingual guides and brand assets
├── scripts/               # Repository checks and brand generation
└── .github/               # CI and contribution templates
```

Within each skill, `SKILL.md` is the entrypoint, `references/` contains task-specific guidance, `scripts/` contains helpers where needed, and `agents/openai.yaml` supplies display metadata. The [repository guide](docs/architecture.md) explains ownership and naming conventions.

<a id="contributing"></a>
## Contributing

Corrections, reproducible bug reports, and concrete workflow improvements are welcome. Read the [contribution guide](CONTRIBUTING.md); use the issue templates to describe expected behavior and a minimal example. Keep both language editions aligned when changing public guidance.

[Changes](CHANGELOG.md) · [Brand assets and provenance](docs/brand.md) · [Third-party notices](THIRD_PARTY_NOTICES.md)

## License

[MIT](LICENSE). Independently maintained; no affiliation with or endorsement by OpenAI is implied. Reference-paper screenshots are not distributed. Workflow acknowledgments and preserved third-party notices are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

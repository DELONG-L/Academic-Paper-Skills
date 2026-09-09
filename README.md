# Academic Paper Skills

English | [简体中文](README.zh-CN.md)

Four coordinated Codex skills for evidence-grounded academic writing:

| Skill | Responsibility |
|---|---|
| `paper-writing` | Draft and revise prose, integrate verified citations, calibrate claims, remove formulaic or over-defensive writing, prepare review excerpts, and migrate LaTeX templates. |
| `paper-review` | Review the author's argument and paragraph structure, simulate reviewer concerns, draft author responses, and verify revision closure. |
| `paper-figures-tables` | Produce grounded tables, reproducible numeric plots and faithful conceptual figures; inspect final-size output. |
| `paper-policy` | Resolve applicable rules and assess formal compliance using actual evidence. |

Formal assigned peer review, experiment execution and project management belong
to separate workflows. Citation verification and completion are supported within
the authorized writing or review task; this bundle is not a literature manager.

## Shared workflow

Local and public installations use the same two policy sets:

```yaml
policy_sets: [integrity-core, academic-defaults]
```

Omitting `policy_sets` selects these defaults. There is no separate
`strict-house-style` mode. The registry contains 50 hard rules and 49 soft
preferences. Hard rules apply within their declared scope and activation;
they protect integrity, evidence and applicable requirements. Preferences for
headings, paragraph shapes, comparison tables, fonts, source canvas sizes and
renderers can adapt to the paper. Their adaptation does not block readiness.

- Write the supported claim directly. Preserve material adverse findings and
  necessary conditions; remove redundant anticipatory defenses.
- Review argument order and paragraph purpose before polishing sentences when
  structural revision is needed. Do not impose one paragraph template everywhere.
- Diagnose concrete prose problems. Do not infer AI authorship from style or
  optimize detector scores.
- Preserve closed-corpus and confidentiality constraints. A request for public
  citation completion permits scoped primary-source verification and supported
  bibliography updates; missing access remains an unresolved source gap.
- Continue authorized edits across skill boundaries. Ordinary text and artifact
  tasks do not require a full compliance run or empty tracking files.
- Numeric plots use supplied data or explicit supplied values and a reproducible
  generation process. Tools and formats follow content and actual delivery
  requirements. Inspect exports at their final placement size.

## Installation

Keep all four sibling folders at the same revision. For a fresh installation:

```bash
git clone https://github.com/DELONG-L/Academic-Paper-Skills.git
mkdir -p ~/.codex/skills
cp -R Academic-Paper-Skills/paper-policy ~/.codex/skills/
cp -R Academic-Paper-Skills/paper-writing ~/.codex/skills/
cp -R Academic-Paper-Skills/paper-review ~/.codex/skills/
cp -R Academic-Paper-Skills/paper-figures-tables ~/.codex/skills/
```

For an upgrade, back up and replace the four existing folders in full before
copying; merging folders can leave retired rules and references installed.
Preserve intentional local customizations in the backup for inspection.
Start a new Codex task after installation so the skill list refreshes.

Python 3.10+ is recommended. Policy tools require PyYAML; figure helpers use the
optional plotting dependencies. LaTeX and PDF rendering tools are needed for
source builds and visual checks, not for prose-only work.

```bash
python3 -m pip install -r requirements-policy.txt
python3 -m pip install -r requirements-figures.txt
```

## Examples

```text
Use $paper-writing to revise this Results paragraph using the supplied values.
Keep the claim direct and remove repeated anticipatory defenses.
```

```text
Use $paper-review to check paragraph necessity, argument order and repeated
material. Show what should change, what can stay, and exact replacements.
```

```text
Use $paper-figures-tables to plot these measurements and inspect the final export.
```

```text
Use $paper-review to answer these reviewer comments and verify each promised edit.
```

Explicit readiness requests use a project context and evidence records. Missing
semantic/manual evidence remains `UNVERIFIED`. Agent semantic PASS requires
current source snapshots; agent inspection cannot substitute for a manual
evaluator. Definite failures take precedence. A `review_hint` requires inspection
and is neither a failure nor proof of compliance.

See [policy usage](paper-policy/SKILL.md) and the
[evidence contract](paper-policy/references/compliance-schema.md) for commands
and the exact authority model. Editorial completion and submission readiness
are separate judgments.

## Maintenance and validation

```bash
python3 paper-policy/scripts/validate_registry.py
python3 paper-policy/scripts/audit_skill_integration.py .
python3 -m unittest discover -s paper-policy/scripts -p 'test_*.py'
python3 -m unittest discover -s paper-figures-tables/scripts -p 'test_*.py'
```

CI runs these checks and compiles Python helpers. The integration audit checks
explicit references and rule IDs; it does not prove semantic consistency or
manuscript quality. Review registry wording, guidance, examples and checker
behavior together. See [rule maintenance](paper-policy/references/rule-maintenance.md)
and [release notes](CHANGELOG.md).

## Sources and license

The academic workflow incorporates independently written guidance informed by
[OniReimu/claude-scholar](https://github.com/OniReimu/claude-scholar), including
argument architecture, paragraph review, citation verification, revision closure
and prose diagnostics. Source-specific references document the relevant ideas.
Figure helpers retain attribution to `Haojae/scipilot-figure-skill`.

MIT. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

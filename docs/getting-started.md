# Getting started

English · [简体中文](getting-started.zh-CN.md) · [Home](../README.md)

## Install the skill instructions

Install `paper-writing`, `paper-figures-tables`, `paper-review`, and `paper-policy` together. They refer to one another by sibling directory name. Keep those names unchanged.

Follow the [fresh-install commands](../README.md#quick-start). If `CODEX_HOME` is set, use its `skills/` directory; otherwise use `~/.codex/skills/`. Copy only the four skill directories, not the entire repository as a single skill. Start a new Codex task after installation and invoke the relevant skill with your sources.

## Choose the tools you need

| Task | Requirement |
|---|---|
| Read and apply skill guidance | Codex with local skills support |
| Run policy scripts | Python and `requirements-policy.txt` |
| Run plotting/image helpers | Also install `requirements-figures.txt` |
| Design a new conceptual figure | Available `imagegen` skill and built-in image tool; SVG reconstruction follows |
| Compile an existing LaTeX project | A compiler compatible with the manuscript and its packages |

Use a virtual environment for Python dependencies. Python 3.10+ is recommended; automated tests run with 3.11. The Python environment does not supply an image-generation tool or a LaTeX installation. If ImageGen is unavailable, the skill reports the missing stage instead of claiming to have completed it.

<a id="upgrade"></a>
## Upgrade without losing local work

1. Update the repository checkout with `git pull --ff-only`.
2. Compare your installed skill folders with the checkout and preserve any local customizations.
3. Move the four installed folders to a separate backup directory outside the active `skills/` directory.
4. Copy all four new directories using the installation commands, then deliberately reapply compatible customizations.
5. Start a new Codex task.

Replacing complete directories avoids leaving removed references or retired rules behind. Do not use an overlay copy as the upgrade procedure. Repository documentation and branding need not be copied into the skills directory.

## Supply useful context

- **Writing:** current section, research question, source evidence, and the desired scope of editing.
- **Figures/tables:** manuscript context, actual data or exact values, target placement, and any venue restrictions.
- **Review:** manuscript version, reviewer comments, and the revisions or evidence to check.
- **Policy:** paper type, stage, source files, and the applicable venue instructions with their source.

A successful source check is narrower than a scientific judgment. Keep missing evidence explicit rather than filling it with plausible content.

## Troubleshooting

| Symptom | Check |
|---|---|
| Skill is not found | Each installed folder should directly contain `SKILL.md`; check `CODEX_HOME` and start a new task. |
| A sibling reference is missing | Install the four skills together with unchanged names. |
| `ModuleNotFoundError` | Activate the environment used to install the relevant requirements file. |
| Old rules remain after an update | Compare installed files and perform a full-folder replacement after backup. |
| Generated diagram has wrong labels or arrows | Correct from the content brief during SVG reconstruction and inspect the render. |
| Plot panel count conflicts with readable placement | Reorganize supported comparisons, change placement or use a table; report unresolved conflicts. |

For reproducible bugs, open an issue with the skill name, minimal input, expected result, actual result, and relevant tool versions. Remove unpublished or confidential manuscript content from public reports.

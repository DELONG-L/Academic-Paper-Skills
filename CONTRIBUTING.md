# Contributing

English · [简体中文](CONTRIBUTING.zh-CN.md) · [Home](README.md)

Contributions should improve a concrete research-writing task while preserving source traceability and the distinction between automated checks and scientific judgment.

## Propose a focused change

Use a bug report for reproducible failures and a workflow proposal for new behavior. Describe the intended user task, the current limitation, and a small example. Remove confidential material from public reports; synthetic reproductions must be labeled as such.

Keep changes in the owning skill. Add detailed guidance under `references/` and route it from the entrypoint instead of expanding every skill's instructions. Avoid universal requirements inferred from one paper or venue. See the [repository and naming guide](docs/architecture.md).

## Validate locally

From the repository root, activate an environment containing both requirements files, then run:

```bash
python scripts/check_repository.py
python -m unittest discover -s scripts -p 'test_*.py'
python paper-policy/scripts/validate_registry.py
python paper-policy/scripts/audit_skill_integration.py .
python -m py_compile scripts/*.py paper-policy/scripts/*.py paper-figures-tables/scripts/*.py paper-review/scripts/*.py
python -m unittest discover -s paper-policy/scripts -p 'test_*.py'
python -m unittest discover -s paper-figures-tables/scripts -p 'test_*.py'
```

Add behavioral tests when changing executable behavior. For documentation-only changes, check routing, relative links, naming and whether the instructions lead to the intended action. For visual changes, inspect the rendered result; valid XML alone is insufficient. Rebuild owned brand SVGs with `python scripts/build_brand.py` and see [brand provenance](docs/brand.md).

## Keep documentation aligned

Update the English and Chinese README and guide pairs together when public behavior changes. Keep skill identifiers and command paths identical across languages. Shared technical references remain in English unless a translation has a clear maintenance owner; do not create incomplete duplicate skill trees.

Describe the problem, resulting behavior, validation and remaining limitations in the pull request. Add a concise entry under `Unreleased` in `CHANGELOG.md` for user-visible changes. Preserve third-party notices, and do not commit private manuscript material, original reference-paper screenshots, credentials, or local validation output.

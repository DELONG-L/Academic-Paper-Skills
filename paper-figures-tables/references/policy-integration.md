# Artifact Policy Integration

Use the sibling `paper-policy` skill before creating or finalizing a governed
figure or table. Keep creation in this skill and compliance aggregation in
`paper-policy`/`paper-review`.

## Resolve Context

Declare `figure` or `table` in `artifacts`, then declare semantic types in
`features`:

- figures: `paper_figure`, plus `data_figure` or `conceptual_figure`;
- tables: `related_work_table`, `data_table`, or
  `result_table`;
- use `artifact_mode: final_figure` or `final_table` for a single final QA
  profile; use `[final_figure, final_table]` when a full-paper run must compose
  both profiles.

Run:

```bash
python3 ../paper-policy/scripts/resolve_policy.py paper_context.yaml
```

Apply active hard rules before soft artifact preferences.
Confirm `active_policy_sets` first. Omitted `policy_sets` means the public
defaults; add `policy_sets: [strict-house-style]` only when the user or project
explicitly opts into the house table and figure rules.

## Record Artifact Evidence

Add each artifact to the shared `compliance-evidence.yaml` under `artifacts`.
Record a stable ID, kind, types, supported claim, outputs, scripts, source data,
previews, and table sources. For every table, also record the exact
`latex_label`; the checker resolves that label to one `table` or `table*`
environment before inspecting booktabs and marker usage. Paths may be absolute or relative to the selected
`--artifact-root`; they may point to a separate replication bundle rather than
requiring the data and scripts to live inside the LaTeX project. Read
`../../paper-policy/references/compliance-schema.md` for the schema.

For an existing LaTeX manuscript, the policy runner can seed this inventory:

```bash
python3 ../paper-policy/scripts/discover_artifacts.py /path/to/paper \
  --primary-tex paper.tex \
  --output artifact-manifest-skeleton.yaml
```

The skeleton is deliberately guarded with
`discovery_status: needs_confirmation`. It cannot be used as evidence until a
reviewer checks each artifact's type, claim, label, paths, source data, and
scripts and changes the status to `confirmed`.

Run reliable source checks:

```bash
python3 ../paper-policy/scripts/check_artifacts.py \
  compliance-evidence.yaml --root /path/to/paper
```

Then aggregate with manuscript compliance:

```bash
python3 ../paper-policy/scripts/assess_compliance.py \
  paper_context.yaml --project /path/to/paper \
  --evidence compliance-evidence.yaml
```

## Source Font Preference And Final-Width Rule

For paper figures:

1. Use a 3x source canvas by default.
2. Prefer explicit source text at or above 24pt; smaller text is allowed when
   the source scale and final rendering remain comfortably readable.
3. Scale line widths, markers, offsets, and panel labels consistently with the
   source canvas.
4. Export vector output where appropriate.
5. Render or place the artifact at the actual target LaTeX width.
6. Perform human visual QA for clipping, density, label readability, legend
   occlusion, grayscale distinction, and panel alignment.
7. Record the visual judgment as a hard result for
   `FIG.FINAL_WIDTH_READABLE` with all governed `artifact_refs`.

Record a below-24pt choice as `ADAPTED` for `FIG.SOURCE_FONT_SCALE`, with the
source scale and final-width rationale. Source points alone never pass the hard
final-width rule.

## Evidence Boundary

- File existence does not prove that values, rows, components, or arrows are
  correct.
- Canonical marker tokens do not prove that related-work rows are defensible.
- Vector export does not prove color accessibility.
- A declared script does not prove that it produced the inspected output.

Use semantic/manual evidence records for those judgments. Never edit result
status directly to bypass a failing source check.

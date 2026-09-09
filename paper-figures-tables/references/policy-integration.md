# Artifact Policy Integration

Apply relevant sibling `paper-policy` rules to artifact work. Use the structured
context, evidence inventory and CLI below when formal artifact compliance or
submission readiness is requested. An ordinary plot or caption task does not
require a context file, evidence ledger or human sign-off before delivery.
Keep creation in this skill and formal aggregation in `paper-policy`/`paper-review`.

## Resolve Context

Declare `figure` or `table` in `artifacts`, then declare semantic types in
`features`:

- figures: `paper_figure`, plus `data_figure` or `conceptual_figure`; add
  `generated_conceptual_figure` whenever an image model produces the final
  conceptual artifact;
- tables: `related_work_table`, `data_table`, or
  `result_table`;
- use `artifact_mode: final_figure` or `final_table` for a single final QA
  profile; use `[final_figure, final_table]` when a full-paper run must compose
  both profiles.
- set `table_profile: layered_capability_matrix` only when a load-bearing
  Related Work table has eight or more retained dimensions organized into
  explicit semantic layers. This selects soft design guidance; it does not
  turn that guidance into hard policy.

Run:

```bash
python3 ../paper-policy/scripts/resolve_policy.py paper_context.yaml
```

Apply active hard rules before soft artifact preferences.
Confirm `active_policy_sets` first. Omitted `policy_sets` selects
`[integrity-core, academic-defaults]`. Choose renderer, font, and marker
style for accuracy, readability, and explicit venue requirements.

## Record Artifact Evidence

Add each artifact to the shared `compliance-evidence.yaml` under `artifacts`.
Record a stable ID, kind, types, supported claim, outputs, scripts, source data,
previews, and table sources. For every table, also record the exact
`latex_label`; the checker resolves that label to one `table` or `table*`
environment as a deterministic source check. Final-render readability, units,
and marker meaning require separate evidence under `TABLE.FINAL_READABLE`;
booktabs and particular marker glyphs are not mandatory checks. Paths may be
absolute or relative to the selected
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

The `files.scripts` list can contain notebooks or shared pipeline files; locate
the figure-specific function/cell/command in the associated evidence. The format
checker establishes file presence and recognizes common formats; suitability,
resolution and venue acceptance require inspection. An unfamiliar extension is
a `review_hint`, not a definite violation or an automatic PASS.

## Source Font Preference And Final-Width Rule

For paper figures:

1. Use a 3x source canvas by default.
2. Prefer explicit source text at or above 24pt; smaller text is allowed when
   the source scale and final rendering remain comfortably readable.
3. Scale line widths, markers, offsets, and panel labels consistently with the
   source canvas.
4. Export vector output where appropriate.
5. Render or place the artifact at the actual target LaTeX width.
6. Inspect clipping, density, readability, grayscale distinctions and alignment;
   identify the actual evaluator. Agent inspection supports editing and delivery.
7. In a formal assessment, `FIG.FINAL_WIDTH_READABLE` retains its manual evidence
   requirement and all governed `artifact_refs`. Leave it `UNVERIFIED` without
   admissible human/user/venue evidence; never relabel agent inspection as human.

Record a below-24pt choice as `ADAPTED` for `FIG.SOURCE_FONT_SCALE`, with the
source scale and final-width rationale. Source points alone never pass the hard
final-width rule.

## Evidence Boundary

- File existence does not prove that values, rows, components, or arrows are
  correct.
- Marker tokens do not prove that related-work rows are defensible.
- A cell tint or dagger does not prove that a capability is absent from the
  comparison corpus; record the corpus boundary and row-wise evidence.
- A font name or formula in a prompt does not prove accurate or readable
  rendering; inspect the actual artifact.
- Preserve source artifacts and transformation records. Judge the final
  content against the manuscript and follow the selected tools' constraints.
- Vector export does not prove color accessibility.
- A declared script does not prove that it produced the inspected output.

Use semantic/manual evidence records for those judgments. Never edit result
status directly to bypass a failing source check.

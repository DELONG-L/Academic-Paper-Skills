# Figure Contract

For a complex figure, capture the scientific purpose, sources, encodings and target placement in existing notes or a short spec. `figure_spec.yaml` below is optional; a simple supplied plot need not create an extra workflow file.

```yaml
figure:
  slug: semantic-utility-main
  manuscript_target: paper/sections/05_experiments.tex
  placement: main-text
  target_width: double-column
  source_scale: 3.0
  source_font_min_pt: 24
  claim: MethodA preserves more allowed task flow than cost-only cover at matched full privacy cover.
  reader_takeaway: Privacy coverage is matched; the difference is semantic utility preservation.
  structural_reference: figures/semantic-utility-main/structure.svg
  background: pure white

source_data:
  - path: runs/example/test_metrics.json
    role: primary metrics
  - path: runs/example/bootstrap.csv
    role: uncertainty intervals

panels:
  - id: A
    plot_type: grouped_bar
    metrics: [pure_utility_loss, task_flow_preservation, overall_flow_preservation]
    methods: [MethodA, BaselineA, BaselineB]
    message: MethodA has lower loss and higher allowed-flow preservation.
  - id: B
    plot_type: interval_bar
    metrics: [baseline_minus_method_loss_margin]
    message: The paired margin is positive with a non-overlapping CI.

encoding:
  proposed: MethodA
  baselines: [BaselineA, BaselineB]
  color_roles: [method, baseline, neutral]
  uncertainty: paired bootstrap 95% CI

caption:
  draft: >
    Matched full-cover utility comparison. All cover methods satisfy the same privacy-cover constraint;
    MethodA preserves more task-required and overall allowed flow than cost-only cover.

validation:
  - Source font scale is recorded; below-24pt text includes an adaptation rationale.
  - Values match source files.
  - Labels are readable at target width.
  - Caption does not claim deployable online protection unless the data supports it.
```

## Required Decisions

- **Purpose:** the comparison, definition, evidence pattern or mechanism the figure lets the reader inspect.
- **Source data:** exact local paths or generated `source_data.csv`.
- **Panel map:** panel IDs, plot type, metric, method/condition order, and message.
- **Structural reference:** for Figure 1, system overview, pipeline, architecture, and threat-model figures, path to `structure.svg` or a reason it is unnecessary.
- **Typography:** identify text and mathematical roles; verify readable, accurate, manuscript-compatible rendering.
- **Production record:** preserve source files and record transformations; follow the selected tools' constraints.
- **Conditions:** assumptions or settings needed to interpret the figure; do not manufacture a list of unclaimed capabilities.
- **Caption boundary:** what belongs in the paper caption versus artifact audit notes.
- **Source scale:** use 3x by default so 24pt source text maps to approximately
  8pt at final placement; record any smaller-source or venue-specific adaptation.
- **Final-width evidence:** record the preview and actual evaluator; agent inspection must not be labeled human evidence. Formal manual checks remain governed by the compliance schema.

## Conceptual Figure Structure Policy

For topology-sensitive conceptual figures, record the manuscript-supported
components, connections, boundaries, and labels before rendering. A structure.svg
wireframe is useful as a reference for image generation; a code-native diagram
may already serve as the editable structure and final source.

Record the selected renderer, source artifact, typography choices, and any
explicit venue requirements. Inspect the final figure for topology, labels,
mathematical accuracy, contrast, and readability. Correct discrepancies using
the selected tools and keep the transformation record. A clean white background
is a presentation default, not a hard requirement.

## Source Data Policy

- Prefer copying a small plot-ready table to `source_data.csv` when the raw artifact is large or nested.
- Preserve the raw artifact path in `figure_spec.yaml`.
- Put transformations in the plotting script, not in undocumented manual edits.
- Use stable method labels that match the paper text.

## Caption Policy

Use `captions.md` for the artifact type. Explain the setup, encodings and conditions needed to read the figure. Include a result or interpretation when helpful; do not require a takeaway or anticipatory disclaimer in every caption.

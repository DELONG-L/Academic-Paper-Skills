# Figure Contract

Create `figure_spec.yaml` before drawing any nontrivial paper figure. Keep it short enough to review.

```yaml
figure:
  slug: semantic-utility-main
  manuscript_target: paper/sections/05_experiments.tex
  placement: main-text
  target_width: double-column
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
  - Values match source files.
  - Labels are readable at target width.
  - Caption does not claim deployable online protection unless the data supports it.
```

## Required Decisions

- **Claim:** one sentence, falsifiable from the figure.
- **Source data:** exact local paths or generated `source_data.csv`.
- **Panel map:** panel IDs, plot type, metric, method/condition order, and message.
- **Structural reference:** for Figure 1, system overview, pipeline, architecture, and threat-model figures, path to `structure.svg` or a reason it is unnecessary.
- **Boundary:** what the figure does not prove.
- **Caption boundary:** what belongs in the paper caption versus artifact audit notes.

## Conceptual Figure Structure Policy

For overview-like conceptual figures, use `structure.svg` as the editable structural contract before generation with a generative image model. It should encode:

- the 3 to 8 manuscript-supported components
- input/output blocks
- directed arrows and arrow labels where needed
- trust, phase, or module boundaries
- short visible labels that match the paper text

Use the final generated output for visual polish, not for inventing or changing structure. If the generative image model cannot preserve the SVG's topology or labels, regenerate with a stricter prompt, apply deterministic label overlay, or keep an editable SVG/TikZ artifact as the final figure.

For Figure 1 and overview-like conceptual figures, the final paper image should have a pure white background. Avoid background gradients, gray washes, paper textures, vignettes, and atmospheric effects. Use color only for components, arrows, boundaries, and semantic highlights.

## Source Data Policy

- Prefer copying a small plot-ready table to `source_data.csv` when the raw artifact is large or nested.
- Preserve the raw artifact path in `figure_spec.yaml`.
- Put transformations in the plotting script, not in undocumented manual edits.
- Use stable method labels that match the paper text.

## Caption Policy

Write captions as paper claims, not descriptions of visual marks. Include:

- The comparison setup.
- The metric or constraint that makes the comparison fair.
- The main result.
- The boundary if readers could overgeneralize.

# Figure Contract

Create `figure_spec.yaml` before drawing any nontrivial paper figure. Keep it short enough to review.

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

- **Claim:** one sentence, falsifiable from the figure.
- **Source data:** exact local paths or generated `source_data.csv`.
- **Panel map:** panel IDs, plot type, metric, method/condition order, and message.
- **Structural reference:** for Figure 1, system overview, pipeline, architecture, and threat-model figures, path to `structure.svg` or a reason it is unnecessary.
- **Conceptual-figure typography:** when `FIG.CONCEPT_TYPOGRAPHY` is active, identify every text role as non-mathematical or mathematical; require the model output itself to use Times New Roman for the former and a dedicated manuscript- or venue-compatible math font for the latter.
- **Model-native output:** for `generated_conceptual_figure`, preserve the accepted model output as the complete semantic artifact. Record the original generated file and only non-semantic packaging transformations.
- **Boundary:** what the figure does not prove.
- **Caption boundary:** what belongs in the paper caption versus artifact audit notes.
- **Source scale:** use 3x by default so 24pt source text maps to approximately
  8pt at final placement; record any smaller-source or venue-specific adaptation.
- **Final-width evidence:** name the rendered preview and human evaluator in the
  shared compliance evidence.

## Conceptual Figure Structure Policy

For overview-like conceptual figures, use `structure.svg` as the editable structural contract before generation with a generative image model. It should encode:

- the 3 to 8 manuscript-supported components
- input/output blocks
- directed arrows and arrow labels where needed
- trust, phase, or module boundaries
- short visible labels that match the paper text

Record the conceptual-figure font contract in its spec:

```yaml
typography:
  non_math_font: Times New Roman
  math_font: manuscript_or_venue_math_font
  math_rendering: model_native_only
generation:
  artifact_type: generated_conceptual_figure
  semantic_content_source: model_output_only
  allowed_postprocess: [crop, resize, compression, color_profile, format_wrap]
```

Use the final generated output for visual polish, not for inventing or changing structure. If the generative image model cannot preserve the SVG's topology, labels, or formulae, regenerate with a stricter prompt or stop. Do not apply a deterministic label/formula overlay or redraw the generated figure in SVG/TikZ.

Do not infer font compliance from prompt wording alone. Under
`FIG.CONCEPT_TYPOGRAPHY`, inspect the accepted model output for Times New Roman
non-mathematical text and manuscript- or venue-compatible mathematical
typography. If either role is wrong or cannot be verified, regenerate or leave
the rule `UNVERIFIED`; post-generation text or formula repair is forbidden.

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

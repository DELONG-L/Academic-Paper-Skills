# Style Guide

Use restrained, high-contrast scientific plotting suited to the manuscript.

## Sizes

Read the actual column or text width from the manuscript or supplied template.
Choose panel layout and text sizes at that placement. The helper presets are
editable starting examples, not current venue specifications. Change them to fit
the target and verify the exported figure in the manuscript.

## Exports

- Always prefer vector for the paper: `pdf`, and `svg` when later editing is plausible.
- Also export `png` at 300 dpi for quick review.
- Preserve editable vector text with `svg.fonttype = "none"` and TrueType text in PDF with `pdf.fonttype = 42`.

## Palette Roles

Use color by semantic role, not decoration.

| Role | Use |
| --- | --- |
| `method` | Proposed or focal method. |
| `baseline` | Main baseline. |
| `neutral` | Reference, oracle, or background condition. |
| `boundary` | Limitation, ceiling, failure, or stopped route. |
| `allowed` | Safe/allowed flow, utility preserved, benign condition. |
| `forbidden` | Leakage, attack success, unsafe flow, violation. |
| `accent` | One highlighted margin or key callout. |

Use hatch or marker shape when colors may be printed in grayscale.

## Layout

- Remove top and right spines for most quantitative plots.
- Use light y-grid lines only when they improve reading.
- Keep legends outside the data area or in a dedicated panel for multi-panel figures.
- Prefer direct value labels only for a small number of bars; otherwise use axis ticks.
- Avoid dense prose inside panels. Put interpretation in the caption.

## Claim Discipline

- Label offline audit, simulation, replay, and deployment settings explicitly.
- Do not use the same color role for an oracle and a deployable method.
- For security results, separate attack success, detection, prevention, and utility cost; do not merge them into a vague "score."
- For privacy/utility figures, show the matched privacy constraint when utility is the main claim.

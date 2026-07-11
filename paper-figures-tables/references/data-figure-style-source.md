# Style Guide

Use restrained, high-contrast scientific plotting. The default target is a two-column ML, AI, systems, or security conference paper.

## Sizes

- Single column: about 3.25 inches wide.
- Double column: about 6.9 inches wide.
- Main multi-panel figure: double column unless the manuscript clearly needs a compact single-column plot.
- Prefer at least 24pt text on the 3x source canvas. After controlled placement
  at final width, verify the venue's effective 7-9pt target visually and through
  the rendered manuscript. Smaller source text needs an explicit readability
  rationale rather than an automatic hard failure.

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

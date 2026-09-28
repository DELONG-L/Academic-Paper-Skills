# SVG Reconstruction and Acceptance

Use after selecting an ImageGen concept design, or when substantially rebuilding
an existing diagram into editable vectors. Scientific correctness and aesthetic
fidelity are separate acceptance dimensions; success in one cannot substitute
for the other.

## Reconstruct the Design

1. Use the content brief as the source for entities, exact labels/formulas,
   connection endpoints, directions, grouping and boundaries. Use the selected
   image for visual composition, relative area, icon appearance, spacing, color
   roles and emphasis. Resolve disagreements in favor of supported content and
   record material design changes.
2. Build SVG layers/groups for regions, connectors, modules/icons, labels and
   callouts. Use semantic IDs when helpful for later edits. Reconstruct directed
   edges deliberately; do not recover scientific topology by tracing pixels.
3. Rebuild icons as clean paths/basic geometry with their distinctive silhouette,
   semantic features and consistent visual weight. Do not replace every designed
   icon with a generic box, emoji or unrelated stock symbol. Simplify tiny details
   only when needed for final-size readability; note meaningful loss of fidelity.
4. Preserve composition, relative scale, grouping, negative space, visual rhythm,
   and palette roles. Pixel-for-pixel noise, incorrect text, accidental tangencies,
   and generation artifacts are not design features to preserve.
5. Keep text editable where practical. Use exact source strings and precise math
   rendering; retain source formulas if export outlines glyphs. Verify fonts and
   fallback behavior in the exported artifact, not only in the SVG editor.
6. Check every connector's endpoints and arrowhead, crossing, and layer order.
   Neither a pretty arrow nor a valid SVG proves a correct relation.

A raster image embedded in an SVG wrapper is not vector reconstruction. Core
logic, labels, modules, and reconstructable icons must be vector objects. Photos
or complex textures may remain raster where justified; record residual raster
content and avoid claims of full vector editability. Follow active tool rules
for any editing of the generated bitmap; vector reconstruction does not authorize
unrelated raster edits or bypass tool restrictions.

## Acceptance Checks

### Semantic pass: compare with the brief/manuscript

- Required entities and relationships are present; no unsupported additions.
- Edge direction/endpoints, boundary membership, execution order or timing agree.
- Labels, formula symbols, operators, indices and illustrated examples are accurate.
- Color and line types have stable meanings with non-color cues where needed.
- A framework's interfaces are not accidentally depicted as sequential execution.
- Any numeric/data panels come from their documented data-driven renderer.

### Visual pass: compare rendered SVG with the design reference

- Main composition, visual focus, region proportions and reading order survive.
- Meaningful icons retain recognizable features and one consistent visual language.
- Semantic color roles, typography hierarchy, line weights and spacing are coherent.
- Reconstruction does not flatten the design into generic boxes or introduce clutter.
- Differences that correct content or improve final-size readability are explained;
  intentional improvements need not imitate errors in the generated draft.

### Placement pass: inspect actual output at intended size

- Record width, height and any source-to-placement scaling; inspect SVG/PDF render
  at those physical dimensions or a documented faithful placement preview.
- Small labels, legends, math, light boundaries, arrows and icons remain readable.
- Check overlap, clipping, font substitutions, broken glyphs and connector tangencies.
- Content coverage and relationship structure justify the occupied area, especially
  two-column-spanning figures; no stretched sparse layouts or artificial filler.
- Main organization is apparent before details; high density does not require
  tiny text or ambiguous lines. Check grayscale and relevant color distinctions.

Correct material failures and re-render affected outputs. Record actual checks and
remaining limitations in existing notes. Opening a file, parsing XML, or declaring
SVG/PDF output is not evidence of rendered visual quality. Agent review is not
human sign-off; keep any formal policy evidence requirements intact.

## Delivery

Deliver editable SVG, PDF when supported, a review preview, and a caption. Retain
selected generated design, prompt, content/connection source, SVG generator if used,
and concise QA/deviation notes. Keep generation provenance even after full manual
reconstruction. Place materials according to the project's workspace contract.

If an icon cannot be adequately reconstructed, make the best faithful editable
approximation within scope and clearly identify the limitation. If important
content, topology or readability remains wrong, mark the artifact incomplete rather
than claiming publication readiness. Do not impose extra approval gates for normal
local iteration already authorized by the user.

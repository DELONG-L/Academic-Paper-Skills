# Conceptual Figures

Use this for system overviews, architectures, pipelines, threat models,
protocol flows, and method intuition. Exact data plots belong to data-figures.md.

## Scientific Requirements

- Derive components, labels, mathematics, arrows, and trust boundaries from the manuscript.
- Do not invent modules or use image generation to synthesize numerical results.
- Inspect the actual final render at paper width for readable labels and correct meaning.
- Preserve the source artifact and the operations used to produce the final output.
- Apply explicit venue requirements with a source; font names in prompts do not prove compliance.

## Presentation Preferences

Use a clean background, readable manuscript-compatible labels and visual grouping
that explains the figure’s scientific purpose. Choose orientation and aspect ratio
from topology, label space and target placement; wide layouts suit some flows but
are not a general rule. Keep mathematical labels accurate.

Add a conceptual figure when it explains something readers need to see. Combine or
separate views according to their explanatory jobs and readability; there is no
figure-count budget or automatic requirement for an overview figure.

## Renderer Selection

- Use Graphviz, Mermaid, TikZ, or SVG when exact topology, mathematical layout, or editable vector output is useful.
- Use an image-generation tool when the task benefits from a generated visual asset.
- For topology-sensitive image generation, prepare a structure.svg wireframe as a reference when it helps preserve the layout and labels.
- Follow the selected runtime tools' generation and editing instructions. This skill does not authorize bypassing tool constraints.

## Workflow

1. Read enough manuscript and caption context to establish the figure's job.
2. Identify the supported components, connections, grouping, and reader takeaway.
3. Record a compact brief/spec with labels, mathematical content, and source locations.
4. Select a renderer and create the source or generation prompt. Use a structural reference when useful.
5. Produce the artifact and inspect it at its actual paper placement width.
6. Correct corrupted labels, formulas, flow directions, or misleading emphasis with the selected tools; unresolved issues must remain explicit.
7. Write a caption explaining the figure's scope and non-obvious visual semantics.

For an existing small figure edit, reuse its source/spec and perform the relevant
steps only. Do not create a new directory of empty planning documents.

## Generation Prompts

When using image generation, include the figure role, intended takeaway,
layout, exact manuscript labels, flow semantics, and any structural reference.
Request a clear academic design and readable manuscript-compatible typography.
Preserve exact mathematical meaning; do not accept a visually plausible but
incorrect symbol. Include a specific font only when the project or venue asks
for it or it is a suitable design choice, not as a universal requirement.

## Outputs

Return the final artifact, caption, and the source or generation prompt needed
to understand its provenance. Include the brief/spec and structure.svg when
they were used. Prefer PDF/SVG for code-native vector artifacts; PNG and a PDF
wrapper may suit generated images. Record final-width QA in the shared artifact
evidence. Renderer and format choices do not themselves establish correctness.

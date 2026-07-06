# Conceptual Figures

Use this for non-numeric paper images: system overviews, architecture diagrams, pipelines, threat models, protocol flows, comparison figures, lifecycles, method intuition, and Figure 1 planning.

## Boundary

- Conceptual figures default to generation with a generative image model.
- Python is not the default renderer for conceptual paper images.
- Do not use a generative image model for exact experiment data plots, axes, numeric trends, error bars, p-values, or source-data-driven visualizations.
- A paper should normally contain at most one or two generated conceptual figures.
- Figure 1 and other paper conceptual figures default to a pure white page background.

## Workflow

1. Read the relevant manuscript context: abstract, introduction, method/system section, threat model, and existing caption notes.
2. Identify what the reader should understand after five seconds.
3. Count existing generated conceptual figures in the paper if the manuscript is available.
4. Extract 3 to 8 main components.
5. Identify directed flows, trust boundaries, groups, and failure or attack paths.
6. Write a human-readable `brief.md`.
7. Write a structured `spec.json` or `figure_spec.yaml`.
8. For Figure 1, system overview, pipeline, architecture, and threat-model figures, create or update a precise editable `structure.svg` wireframe from the spec.
9. Write a generation prompt from the spec and `structure.svg`.
10. Generate the image with the runtime image-generation tool when available.
11. Draft a caption that explains component order and arrow/color semantics.

## Generated Figure Budget

Default budget:

- 0 to 1 generated conceptual figure for experiment-heavy papers.
- 1 to 2 generated conceptual figures for system, security, or method papers.
- More than 2 only with explicit justification, such as a contribution that needs multiple mechanism views.

Prioritize:

1. Figure 1 system overview, pipeline, architecture, or threat model.
2. One mechanism detail, attack/defense path, or method-intuition figure if Figure 1 cannot carry it.

Avoid using generative image models for decorative filler, repeated workflow variants, or figures whose job is better served by a table.

## Figure 1

Figure 1 should usually orient the paper. Prefer a system overview, workflow, taxonomy, or conceptual comparison over a dense plot unless the paper's primary contribution is a single empirical phenomenon.

Wide layouts are preferred for overview, pipeline, and architecture figures. Keep labels sparse and readable. Use a pure white background; only modules, arrows, and light internal fills may carry color.

For Figure 1 and overview-like conceptual figures, use a structure-first workflow: create a precise `structure.svg` wireframe that fixes components, layout, arrows, group boundaries, and short labels before calling the image-generation tool. Treat this SVG as the structural contract for the generated image, not as the final visual style. The final generation prompt must instruct the model to preserve the SVG's topology, component set, flow direction, and labels while improving visual polish.

## Renderer Selection

Default:

- Use a generative image model for polished conceptual diagrams when exact editability is not required.
- Use an editable `structure.svg` wireframe as the default structural reference for Figure 1, system overview, pipeline, architecture, and threat-model image generation.

Exceptions:

- Use Graphviz or Mermaid for strict graph-like flow, lifecycle, dependency, state, or protocol structure.
- Use TikZ only when the project already uses TikZ or exact LaTeX integration is required.
- Use final SVG when post-generation editing matters or when the generative image model cannot preserve the required topology or labels.
- Use a generated draft plus SVG/TikZ redrawing only when venue or editability constraints require it.

Do not force conceptual diagrams into Matplotlib unless the structure is very simple and not image-like.

## Generation Prompt Requirements

The prompt must include:

- paper role: Figure 1, method overview, threat model, pipeline, etc.
- five-second reader takeaway
- layout direction and main groups
- 3 to 8 labeled components
- arrow/data-flow semantics
- trust boundaries or attacker paths when relevant
- reference to `structure.svg` when available, with instructions to preserve its topology and labels
- visual style: clean academic paper figure, pure white background, sparse labels
- negative constraints: no title inside image, no decorative filler, no unsupported modules, no tiny text, no gradient background, no gray canvas, no vignette, no paper texture

Keep exact technical labels from the manuscript. Do not ask the model to invent components.

When using `structure.svg` as a generation reference, the prompt should say:

- follow the SVG's component layout, arrow directions, boundaries, and label text
- improve spacing, line quality, icons, color hierarchy, and academic polish
- do not add, remove, rename, or reorder core components unless the spec explicitly requests it
- keep labels short and readable; if exact labels cannot be preserved, prefer leaving clean label space for deterministic overlay
- keep the page background pure white; color should appear only inside components, arrows, boundaries, or icons

## Constraints

- No in-image title.
- Pure white background by default for Figure 1 and overview-like paper figures.
- Keep labels short.
- Use captions for interpretation and definitions.
- Do not invent modules that are not supported by the manuscript.
- Preserve trust boundaries, data-flow direction, and threat-model semantics.
- For overview-like figures, preserve the `structure.svg` topology unless the spec is updated first.
- If generated labels are wrong or unreadable, regenerate or switch to an editable renderer.
- If the generative image model preserves the visual style but corrupts labels, use deterministic label overlay on the generated image or keep the SVG/TikZ version as the final artifact.
- If the generative image model introduces a gradient or textured background, regenerate with a stricter prompt or clean the background deterministically before insertion.

## Output Contract

```text
figures/{slug}/
├── brief.md
├── spec.json or figure_spec.yaml
├── structure.svg
├── generator-prompt.txt
├── figure.png
└── caption.md
```

Optional outputs:

- `figure.pdf` wrapper for LaTeX inclusion.
- `figure.svg` for the final vector artifact only when a vector/editor path is actually used; keep `structure.svg` as the editable reference wireframe.

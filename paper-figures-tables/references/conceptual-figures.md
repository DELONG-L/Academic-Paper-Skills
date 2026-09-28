# Conceptual Figures

Use for system overviews, frameworks, pipelines, threat models, protocols,
method mechanisms, and intuition figures. Read `conceptual-style-reference.md`
for design references and `conceptual-vector-rebuild.md` for reconstruction/QA.
Exact data plots and tables retain their data-driven or native workflows.

## Default and Scope

For a new conceptual figure, use:

**Supported content and placement -> ImageGen design -> editable SVG
reconstruction -> independent semantic and visual checks -> final-size QA.**

This is the skill's default production workflow, not a claim that every venue
requires image generation or that generation guarantees beauty. Read the
available `imagegen` skill before the design stage and use its built-in tool by
default. The generated bitmap is a visual design reference; this workflow then requests
an editable vector reconstruction. Follow active tool constraints.

- Small edits to existing SVG/TikZ or another editable source: edit that source
  directly and preserve its established design; do not regenerate the whole image.
- Explicit user choices, applicable venue restrictions, or a source requiring a
  particular renderer take precedence. State a material deviation from the default.
- If ImageGen is unavailable, finish the content/placement brief and any useful
  structural draft, report the missing design stage, and offer the permitted
  alternative. Do not silently claim the default workflow was completed or switch
  to a paid/API fallback without the authorization required by the imagegen skill.
- Numeric panels in a mixed figure must still be rendered from source data.
  ImageGen may design surrounding layout, not invent plotted values or trends.

## 1. Define Content and Figure Type

Read enough manuscript and caption context to identify the takeaway, components,
exact labels/formulas, connection endpoints and direction, boundaries, and sources.
Record these in existing notes or one concise brief. Resolve missing scientific
content rather than asking the image model to supply it. A wireframe is useful
when topology is complex, but is not a separate aesthetic design prerequisite.

Classify the explanatory job independently of page placement:

| Type | Reader's question | Visual semantics |
|---|---|---|
| Flow/process | What happens, and in what order? | Directed execution, transformation, or stage progression |
| Framework/architecture | What are the parts and how do they relate? | Containment, interfaces, dependencies, interaction |
| Hybrid | How does execution traverse the system? | Structural boundaries plus a clearly distinguished main flow |
| Mechanism | How does the key operation work? | Overall position plus local expansion |
| Comparison | What changes across alternatives? | Stable shared skeleton and salient differences |
| Protocol/timing | When or in which round does this happen? | Shared alignment grid, stages, and temporal dependencies |

Do not call every connected-box drawing a flowchart. Arrows in a framework do
not automatically mean execution order; identify their meaning explicitly.

## 2. Define Placement and Effective Density

Record single-column or spanning both columns in a two-column paper, target
width in the actual template, and a height budget or justified aspect ratio.
Distinguish full-width placement in a one-column template when relevant.
If the template is unknown, state a provisional size and defer final-size claims.
Screenshot aspect ratio alone cannot establish original publication placement.

- Single-column: compact but complete explanation of its assigned job; neither
  empty decoration nor an entire system compressed into unreadable labels.
- Spanning both columns: require substantially richer effective information
  content justified by occupied area. Use the space for supported relationships,
  multiple stages, comparisons, meaningful boundaries, mechanism expansions, or
  explanatory input/output examples. Merely stretching a small flow is inadequate.
- Height matters: a shallow cross-column strip and a half-page system figure have
  different information budgets. Do not enforce the same node count for both.
- Plan three reading levels where useful: overall organization and emphasis;
  main relations/path; local operators, labels, and detail. Preserve the semantics
  of necessary connections even when simplifying.
- Evaluate content coverage, organization, and final-size readability together.
  Node counts, ink coverage, and tiny text are not effective-density measures.
- When supported content does not justify the area, shrink or reorganize the
  figure. Never invent components, redundant panels, or decorative icons to fill it.

## 3. Design with ImageGen

Select relevant layout and palette references from `conceptual-style-reference.md`;
when suitable reference images are supplied, inspect only those that support this
figure's job. Provide their role as style references, not scientific content or edit
targets. The written design guide is sufficient when no reference images are supplied. Include in the prompt:

- figure type, takeaway, exact supported entities/labels and connection semantics;
- target placement, width/height or aspect ratio, density plan, and main reading path;
- reference composition, semantic color roles, icon language and text hierarchy;
- vector-friendly shapes, consistent icon strokes/detail, restrained fills, and
  clear separation of background, nodes, connectors, and labels;
- invariants: no extra components/results, no invented relationships, no decorative
  fill used to simulate density. Keep formulas semantically exact.

Inspect the generated design for composition, hierarchy, icons, relationship
clarity, density, and likely readability at the target size. Correct a material
problem with a targeted iteration; do not generate arbitrary variants by default.
Retain the selected draft and prompt. Visual polish must be judged from the actual
image, not inferred from the tool name or prompt. Record any scientific errors
in the draft so reconstruction corrects them instead of tracing them.

## 4. Reconstruct and Verify

Follow `conceptual-vector-rebuild.md`. Build editable SVG geometry and labels,
preserving the selected design's visual character while reconstructing all
scientific content from the brief. Native math tooling may supply precise vector
formula glyphs. Keep source text/formulas even if export requires outlined glyphs.

Render and compare the actual SVG/export with the selected draft, check it against
the supported connection list, and inspect at the planned publication dimensions.
Repair material failures before delivery. No automatic human-approval checkpoint
is added between stages; continue within existing authorization.

## Outputs and Provenance

Keep the brief/source and connection notes, selected generated design, prompt,
editable source, export, preview, and concise QA/deviation notes. These can live
in existing project records; do not create empty planning files. Put only final
lightweight exports in a managed paper repository, following its workspace contract.

Default final outputs: editable `figure.svg`, paper-ready `figure.pdf` when export
is supported, review preview, and caption explaining non-obvious visual semantics.
Keep any generator used to build the SVG. List residual raster elements or reduced
icon fidelity rather than claiming full vectorization. Do not call an unreadable
or topologically incorrect output finished.

ImageGen use remains part of provenance even after full SVG reconstruction.
Use `generated_conceptual_figure` when image-model content is retained in the final
artifact. For a fully reconstructed vector final, record the generated design
reference separately and resolve venue-specific generation/disclosure rules from
the actual workflow; vectorization does not erase that history. Agent inspection
is not human sign-off under formal policy checks.

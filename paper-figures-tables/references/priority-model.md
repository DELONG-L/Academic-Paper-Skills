# Priority Model

Use this file to resolve conflicts among artifact sources and routes.

## Authority Order

1. Core integrity constraints from the sibling `paper-policy` skill.
2. User-provided data, manuscript facts, approved evidence, and explicit instructions.
3. Verified venue requirements with source and freshness date.
4. Applicable hard rules from the shared academic workflow.
5. Writing handoff specs within the authorized task; a generated spec cannot override hard rules.
6. Shared academic defaults, including adaptable author preferences.
7. Data-visualization and security/system plotting advice for precise figures.

## Route Boundaries

- Tables are governed by `tables.md`; chart advice does not override table style.
- Precise experiment plots are governed by `data-figures.md`; image generation must not be used for numeric data figures.
- Conceptual figures are governed by `conceptual-figures.md`; select the renderer from topology, editability, active policy, and available tools.
- Writing prose belongs to `paper-writing`; this skill may emit captions, labels, artifact plans, and short callout sentences.

## Conflict Rules

- Use explicit numerical values in supplied prose, tables or files, retaining their units and conditions. A statement that a result exists without the needed values is insufficient; request the missing data or return a spec when no supported plot can be made.
- Apply verified venue and explicit project requirements; adapt editorial preferences to the artifact and explain material departures briefly.
- If the chart-selection references recommend a different chart from the user request, explain the concern and propose the safer option before proceeding.
- If a venue template imposes stricter layout rules, satisfy the venue while preserving the artifact's claim and readability.
- If the user asks for quick drafting with placeholder values, label placeholders explicitly and do not present them as actual results.
- Choose text size for final placement and inspect the rendered artifact at that width.

## Source of Truth

For numbers and categories, source of truth is:

1. User-provided source data files.
2. User-provided result tables or notes.
3. Existing manuscript artifacts.

Do not infer unstated values or extract exact values from qualitative descriptions. Explicit numerical values in prose are usable after verified transcription. For conceptual figures, components and arrows come from the manuscript rather than model imagination. For literature facts or citation grounding, defer to `paper-writing` or a user-supplied literature workflow; this skill only formats and validates the artifact once content is supplied.

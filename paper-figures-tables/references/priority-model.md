# Priority Model

Use this file to resolve conflicts among artifact sources and routes.

## Authority Order

1. Core integrity constraints from the sibling `paper-policy` skill.
2. User-provided data, manuscript facts, approved evidence, and explicit instructions.
3. Verified venue requirements with source and freshness date.
4. Writing handoff specs from `paper-writing`.
5. Hard rules from explicitly activated policy sets.
6. Enabled public defaults and optional house artifact guidance.
7. Data-visualization and security/system plotting advice for precise figures.

## Route Boundaries

- Tables are governed by `tables.md`; chart advice does not override table style.
- Precise experiment plots are governed by `data-figures.md`; image generation must not be used for numeric data figures.
- Conceptual figures are governed by `conceptual-figures.md`; select the renderer from topology, editability, active policy, and available tools.
- Writing prose belongs to `paper-writing`; this skill may emit captions, labels, artifact plans, and short callout sentences.

## Conflict Rules

- If prose says a result exists but source data is absent, do not plot or tabulate it as a fact. Ask for data or produce a placeholder spec.
- If generic advice conflicts with an enabled house rule, use the enabled rule; otherwise adapt the public default.
- If the chart-selection references recommend a different chart from the user request, explain the concern and propose the safer option before proceeding.
- If a venue template imposes stricter layout rules, satisfy the venue while preserving the artifact's claim and readability.
- If the user asks for quick drafting with placeholder values, label placeholders explicitly and do not present them as actual results.
- Prefer source text at or above 24pt on the 3x source canvas. Below-24pt text is
  a reportable soft adaptation and must still pass the final-width hard gate.

## Source of Truth

For numbers and categories, source of truth is:

1. User-provided source data files.
2. User-provided result tables or notes.
3. Existing manuscript artifacts.

Never infer exact values from prose. For conceptual figures, components and arrows come from the manuscript rather than model imagination. For literature facts or citation grounding, defer to `paper-writing` or a user-supplied literature workflow; this skill only formats and validates the artifact once content is supplied.

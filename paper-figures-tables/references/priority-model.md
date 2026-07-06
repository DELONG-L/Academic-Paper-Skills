# Priority Model

Use this file to resolve conflicts among artifact sources and routes.

## Authority Order

1. User-provided data, manuscript facts, target venue, and explicit instructions.
2. Writing handoff specs from `paper-writing`.
3. House artifact style in this skill's task-specific references.
4. Data-visualization advisor rules for precise data figures only.
5. Security/system figure contracts and plotting helpers for precise paper plots.

## Route Boundaries

- Tables are governed by `tables.md`; chart advice does not override table style.
- Precise experiment plots are governed by `data-figures.md`; image generation must not be used for numeric data figures.
- Conceptual figures are governed by `conceptual-figures.md`; Python is not the default renderer for conceptual paper images.
- Writing prose belongs to `paper-writing`; this skill may emit captions, labels, artifact plans, and short callout sentences.

## Conflict Rules

- If prose says a result exists but source data is absent, do not plot or tabulate it as a fact. Ask for data or produce a placeholder spec.
- If generic advice conflicts with house table/figure style, use house style.
- If the chart-selection references recommend a different chart from the user request, explain the concern and propose the safer option before proceeding.
- If a venue template imposes stricter layout rules, satisfy the venue while preserving the artifact's claim and readability.
- If the user asks for quick drafting with placeholder values, label placeholders explicitly and do not present them as actual results.

## Source of Truth

For numbers and categories, source of truth is:

1. User-provided source data files.
2. User-provided result tables or notes.
3. Existing manuscript artifacts.

Never infer exact values from prose. For conceptual figures, components and arrows come from the manuscript rather than model imagination. For literature facts or citation grounding, defer to `paper-writing` or a user-supplied literature workflow; this skill only formats and validates the artifact once content is supplied.

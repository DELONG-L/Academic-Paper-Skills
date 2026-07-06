---
name: paper-writing
description: Academic paper prose writing and rewriting in the local house style. Use for drafting or revising abstracts, introductions, RQ framing, related work, background, method prose, system-model prose, results narrative, discussion, limitations, conclusions, contribution lists, claim calibration, citation-integrated prose, venue-aware section structure, and academic prose cleanup. Do not use for final figure/table rendering, data plotting, self-review, reviewer response, or rebuttal drafting.
---

# Paper Writing

Use this as the single entrypoint for academic paper prose. It merges a claim-calibrated house style, generic ML paper conventions, introduction/RQ framing, manual-BibTeX citation discipline, and academic prose cleanup.

## Priority Model

Always load `references/priority-model.md` first. For any prose-writing task, also load `references/style-profile.md`.

Authority order:

1. User-provided facts, venue, target section, and manuscript constraints.
2. `references/style-profile.md`, the default house style.
3. Task-specific references in this skill.

When sources conflict, prefer the higher item in this list. Do not let generic ML paper advice override the house style.

## Task Routing

Load only the references needed for the current writing task:

| Task | Load |
|---|---|
| Outline or top-level section structure | `section-architecture.md`, optionally `venue-adaptation.md` |
| Abstract or general section draft | `section-drafting.md`, `academic-prose.md` |
| Introduction, gap, or RQs | `introduction-framing.md`, contribution guidance in `section-drafting.md` |
| Related Work or Background and Related Work | `related-work.md`, `citation-integration.md` |
| Method, System Model, Approach, or technical prose | `section-drafting.md`, `citation-integration.md` if claims cite prior work |
| Results narrative without making plots/tables | `section-drafting.md`, `artifact-handoffs.md` |
| Discussion, limitations, conclusion | `section-drafting.md`, `academic-prose.md` |
| Contribution list or claim calibration | `section-drafting.md`, `style-profile.md` |
| Prose polish, AI-pattern cleanup, or "make this sound less AI" | `academic-prose.md`, `style-profile.md` |
| Citation-aware writing | `citation-integration.md` |
| Need a figure or table artifact | `artifact-handoffs.md`; hand off artifact production to Figures & Tables |

If a task spans multiple sections, load `section-architecture.md` first, then the section-specific reference files.

## Hard Writing Constraints

- Use the house style by default: scoped claims, explicit boundaries, evidence-forward paragraphs, and contribution bullets that name artifacts rather than activities.
- Top-level section names must be traditional and concise. Use `section-architecture.md` before drafting outlines or headings.
- Related Work must include a comparison-table plan unless the user explicitly says the task is prose-only or the target venue forbids tables. Use `related-work.md`.
- Do not produce final figure/table layout in this skill. Writing may produce an artifact plan, caption draft, or table spec, then hand off to Figures & Tables.
- Treat user-maintained `.bib` files and user-provided notes as the citation source of truth. Do not invent citations, BibTeX entries, venues, years, or paper claims. If a needed citation is not present, prompt the user to manually add BibTeX. Use `citation-integration.md`.
- Do not use casual "humanizer" voice. Academic prose cleanup means removing formulaic AI patterns while preserving technical density and house style.
- Do not write meta-text such as "this draft", "this manuscript aims to", or "in xxx-style" in the paper body unless the source paper itself uses that phrase for a substantive reason.
- Keep internal provenance out of the paper body unless the paper is explicitly about audit methods. Internal paths, script names, renderer names, DPI checks, placeholder-citation status, and artifact-bundle notes belong in README, artifact specs, review files, appendices, or comments.
- Use ordinary roman text by default. Use `\textbf{}` sparingly for named paragraph cues such as RQs or stage names. Avoid frequent `\textit{}` and `\texttt{}` in prose unless the text is a mathematical variable, code literal, file path in an audit appendix, or venue-required notation.

## Output Contracts

For drafting or rewriting prose:

1. Prefer concrete rewritten text over advice.
2. Preserve LaTeX commands, labels, citations, math, and macros unless the user asks to refactor them.
3. State any missing factual input as a bracketed placeholder, not as invented content.
4. Keep claims scoped to the available evidence.

For Related Work:

1. Return prose organized by intellectual axes, not paper-by-paper summaries.
2. Include or specify a comparison table with row groups, 3--4 high-signal dimensions by default, marker semantics only if needed, compact caption draft, placement preference, and the sentence that references it.
3. If the final LaTeX table is outside scope, emit a handoff spec for Figures & Tables.

For Results narrative:

1. Interpret supplied values only within the stated experiment scope.
2. Mention the table or figure that should carry exact values.
3. If an artifact is missing, provide a handoff spec instead of pretending the evidence exists.

## Reference Map

- `references/priority-model.md`: source priority and conflict resolution.
- `references/style-profile.md`: default claim-calibrated house style.
- `references/section-architecture.md`: traditional section names and paper structure.
- `references/section-drafting.md`: section-level drafting patterns and claim calibration.
- `references/introduction-framing.md`: gap and RQ-driven introduction flow.
- `references/related-work.md`: related work organization and mandatory comparison-table planning.
- `references/academic-prose.md`: academic anti-AI cleanup and prose guardrails.
- `references/citation-integration.md`: manual-BibTeX citation integration and local citation hygiene.
- `references/venue-adaptation.md`: venue and checklist adaptation.
- `references/artifact-handoffs.md`: handoff specs for Figures & Tables.

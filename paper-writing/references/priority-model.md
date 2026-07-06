# Priority Model

Use this file to resolve conflicts among local writing sources.

## Authority Order

1. User-provided paper facts, target venue, and explicit instructions.
2. The house style in `style-profile.md`.
3. Task-specific writing references in this skill.

The house style is not optional. Generic ML paper advice is a fallback for structure, venue conventions, and missing section scaffolds.

## Conflict Rules

- If generic advice says to maximize reviewer scanability but house style says to narrow claims, narrow the claim first.
- If a venue requires a section or checklist, satisfy the venue but keep the section title traditional.
- If a prose cleanup rule would make text casual, keep academic density and remove only the formulaic pattern.
- If a table or figure style question appears, produce a writing-level spec and hand off artifact rendering.
- Citation source of truth is manual: use only user-maintained `.bib` entries, existing manuscript citation keys, and user-provided notes or matrices. Automatic citation search or verification is out of scope unless the user explicitly requests it as a separate task.

## Default Behavior

When the user asks for writing, produce edited prose. Do not respond with only a plan unless the user asks for planning.

When facts are missing, use bracketed placeholders such as `[dataset]`, `[metric]`, or `[citation needed]`. Do not invent results, citations, venues, baselines, or years.

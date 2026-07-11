# Priority Model

Use this file to resolve conflicts among local writing sources.

## Authority Order

1. Core integrity rules from the sibling `paper-policy` skill.
2. User-provided paper facts, approved evidence, author intent, and explicit task constraints.
3. Verified venue or template requirements with source and freshness date.
4. Hard rules from explicitly activated policy sets.
5. Public academic defaults and enabled optional house guidance in `style-profile.md`.
6. Task-specific writing references in this skill.
7. Generic academic or domain advice.

Apply hard rules before soft guidance. The public academic defaults govern the
remaining freedom unless the context explicitly enables `strict-house-style`.

## Conflict Rules

- Narrow unsupported claims regardless of style profile; claim integrity is not a house preference.
- If a verified venue requires a section or checklist, satisfy the venue. Apply
  Apply traditional section naming only when its strict rule is enabled.
- If a prose cleanup rule would make text casual, keep academic density and remove only the formulaic pattern.
- If a table or figure style question appears, produce a writing-level spec and hand off artifact rendering.
- Citation source of truth is declared by the user or project; local `.bib` entries, manuscript keys, and supplied notes are the default. Automatic search or verification remains out of scope unless explicitly requested as a separate task.
- If venue, anonymity, or submission state is inferred or lacks provenance, do
  not activate its hard rules. Report the unresolved context instead.

## Default Behavior

When the user asks for writing, produce edited prose. Do not respond with only a plan unless the user asks for planning.

When facts are missing, use bracketed placeholders such as `[dataset]`, `[metric]`, or `[citation needed]`. Do not invent results, citations, venues, baselines, or years.

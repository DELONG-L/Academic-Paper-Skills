# Priority Model

Use this file to resolve conflicts among local writing sources.

## Authority Order

1. Core integrity rules from the sibling `paper-policy` skill.
2. User-provided paper facts, approved evidence, author intent, and explicit task constraints.
3. Verified venue or template requirements with source and freshness date.
4. Applicable hard rules from the shared academic workflow.
5. Editorial guidance and adaptable author preferences in `style-profile.md`.
6. Task-specific writing references in this skill.
7. Generic academic or domain advice.

Resolve applicable requirements through `paper-policy`. Select editorial advice
from the task guides; examples do not turn preferences into requirements.

## Conflict Rules

- Narrow unsupported claims regardless of style profile; claim integrity is not a house preference.
- If a verified venue requires a section or checklist, satisfy the venue. Apply
  concise, informative headings suited to the argument otherwise.
- If a prose cleanup rule would make text casual, keep academic density and remove only the formulaic pattern.
- If an artifact is part of the requested deliverable, pass its content and evidence to the owning figure/table skill and complete it within the same task. Return only a spec when that is the requested output.
- Citation scope follows the request: local polish uses existing sources; a closed corpus stays closed; literature completion/verification permits the necessary public primary-source lookup and supported local updates. Follow `citation-integration.md` without requiring another task invocation.
- If venue, anonymity, or submission state is inferred or lacks provenance, do
  not activate its hard rules. Report the unresolved context instead.

## Default Behavior

When the user asks for writing, produce edited prose. Do not respond with only a plan unless the user asks for planning.

When facts are missing, use bracketed placeholders such as `[dataset]`, `[metric]`, or `[citation needed]`. Do not invent results, citations, venues, baselines, or years.

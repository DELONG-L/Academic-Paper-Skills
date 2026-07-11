# Citation Integration

Use this for manual-BibTeX-first citation writing and local citation hygiene.

## Core Rule

Use only citation and evidence sources declared by the user or project. By
default, trust the user-maintained `.bib`, supplied notes, reading lists,
related-work matrices, and manuscript text; add other sources only through an
explicitly authorized verification workflow.

Do not search for, fetch, invent, externally verify, or complete references by default. Do not create BibTeX entries. Do not infer authors, venues, years, DOIs, arXiv IDs, or citation keys from memory.

## What Codex May Do

Codex may:

- Reuse citation keys already present in the manuscript or `.bib` file.
- Check that every `\cite{...}` key in `.tex` exists in the local `.bib`.
- Check for duplicate BibTeX keys.
- Preserve and move existing citation commands while rewriting prose.
- Mark missing citation needs with `[citation needed: ...]`.
- Prompt the user to manually add BibTeX when the writing workflow reveals a needed citation family or specific missing work.
- Help organize user-provided BibTeX entries, notes, and related-work matrices into prose.
- Improve citation placement so claims and citations stay close.
- Flag claims that lack a nearby citation or user-provided note.

Codex may not:

- Add a new citation key that is not already in the `.bib` or explicitly supplied by the user.
- Generate BibTeX from memory.
- Claim that a paper supports a statement unless the user supplied notes, quotes, a sidecar, or nearby manuscript context indicating that support.
- Treat web search, Semantic Scholar, Google Scholar, CrossRef, or arXiv lookup as reliable citation verification unless the user explicitly asks for an exploratory check.

## Writing With Existing Keys

When drafting prose with local citation keys:

- Use keys already present in `.bib` or the manuscript.
- Place citations near the claim they support.
- Avoid dumping many citations at the end of a long paragraph.
- Prefer grouped citations only when all papers support the same sentence.
- Keep uncertain citation needs as placeholders.

Use this placeholder when no approved key exists:

```latex
[citation needed: prior work on X]
```

Use a LaTeX-shaped placeholder only when the user needs compilable shape and accepts a temporary key:

```latex
\cite{PLACEHOLDER_user_to_add_bibtex}
```

## Manual BibTeX Update Prompts

When the workflow indicates that a claim, background statement, or Related Work comparison needs a citation that is not available in the local `.bib`, do not fill it in. Add a concise manual-update prompt for the user.

Use this format:

```text
Manual BibTeX update needed:
- Need: prior work on [topic/claim]
- Why: supports [sentence/paragraph/table axis]
- Suggested search target: [paper family, author if user mentioned one, or keyword]
- Current placeholder: [citation needed: ...]
```

If the user names a specific paper but the key is absent, use:

```text
Manual BibTeX update needed:
- Need: BibTeX for [paper title or author/year supplied by user]
- Why: cited in [section/claim]
- Current placeholder: \cite{PLACEHOLDER_user_to_add_bibtex}
```

Keep these prompts short and actionable. Do not provide invented BibTeX or unverified citation keys.

## Claim-Citation Fit

Codex can check fit only against user-provided evidence.

- If the user supplied notes for a paper, use those notes to decide where the citation belongs.
- If only a `.bib` entry exists, use the citation for broad positioning only when the title/venue/context is sufficient and the user has not asked for claim-level support.
- For specific empirical claims, require user-provided notes, quoted text, a sidecar, or an existing manuscript sentence that already ties the key to the claim.
- For first-work or novelty claims, avoid the claim unless the user supplied a curated comparison or explicit instruction.

Do not cite a paper for a claim merely because the title sounds related.

## Local Hygiene Checks

When asked to check citations in a LaTeX project:

1. Find `.bib` files referenced by the manuscript.
2. Extract BibTeX keys from those `.bib` files.
3. Extract citation keys from `\cite`, `\citet`, `\citep`, `\citealp`, `\citeauthor`, and related commands.
4. Report missing keys, duplicate keys, and unused keys if useful.
5. Do not report that a citation is semantically correct unless user-provided notes support that judgment.

## BibTeX Key Hygiene

When organizing user-supplied BibTeX:

- Preserve existing keys unless the user asks for a key-format migration.
- Prefer stable, readable keys such as `authorYYYYshorttitle` when creating placeholders for the user to replace.
- Do not silently rewrite manuscript citation keys without updating every corresponding `\cite{}`.
- Flag duplicate keys, non-ASCII surprises, broken braces, missing years, and missing titles as local hygiene issues.
- Keep manual-update prompts outside the paper body unless the user explicitly wants draft placeholders.

## Related Work Use

Related Work should synthesize by axis. Citations support the comparison; they should not become a paper-by-paper list.

Preferred:

```latex
Prior defenses usually assume [threat model]~\cite{a,b}, while measurement studies evaluate [different unit]~\cite{c,d}. This leaves [gap] unresolved.
```

Avoid:

```latex
A proposed X~\cite{a}. B studied Y~\cite{b}. C introduced Z~\cite{c}.
```

## If The User Explicitly Requests External Checking

Treat external checking as exploratory assistance until its output is approved
as a project citation source. Return candidates, discrepancies, or unresolved
questions rather than silently converting search output into claim support.

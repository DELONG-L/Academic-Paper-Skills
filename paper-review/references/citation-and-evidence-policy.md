# Citation and Evidence Policy

This skill follows a local-only citation policy.

## Source of Truth

Use:

- Local `.bib` files.
- User-provided BibTeX.
- User notes, related-work matrices, and manuscript text.
- Local PDFs or paper notes only when the user provided them.

Do not by default:

- Search the web for references.
- Fetch BibTeX.
- Verify citation content against APIs.
- Claim that a citation supports a sentence unless the support is evident from local notes or user-provided material.

## Local Citation Hygiene

When requested or relevant, check:

- `\cite{key}` exists in local `.bib`.
- No obvious duplicate BibTeX keys.
- Citation keys follow the local project's style if one is visible.
- Double-blind self-citations are third-person and anonymous where required.

## Missing Citation Handoff

If the review suggests a claim needs citation support and the local `.bib` does not contain an appropriate entry, do not invent a key. Emit:

```text
Manual BibTeX update needed:
- Need: prior work on [topic/claim]
- Why: supports [sentence/paragraph/table axis]
- Suggested search target: [paper family, author if user mentioned one, or keyword]
- Current placeholder: [citation needed: ...]
```

If the user later adds BibTeX, then the review skill may check local key presence and help route prose/table updates.

## Evidence Labels

Use explicit labels in issue boards and rebuttal plans:

- `in-paper`: already present in manuscript.
- `local-bib`: supported by a local citation key or user-provided notes.
- `user-confirmed`: supplied directly by the user.
- `needs-user-input`: cannot be resolved by the agent.
- `missing`: absent from current materials.

## Numerical Evidence

Never invent:

- Accuracy, runtime, memory, p-values, confidence intervals, seed count, or qualitative win/loss status.
- Baseline results.
- Ablation values.
- Dataset sizes unless present in local materials.

If the user asks for a draft before results are ready, use `[TBD: user-provided value]` placeholders and mark them as blockers.

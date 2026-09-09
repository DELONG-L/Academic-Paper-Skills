# Citation and Evidence Policy

Use `../../paper-writing/references/citation-integration.md` as the shared source
workflow. Ordinary manuscript review starts from local evidence; an explicit
closed corpus remains closed. A request to complete literature, verify novelty,
or check citations already authorizes the needed public primary-source lookup.
No separate skill invocation or repeat approval is required. Read-only review
does not authorize editing the manuscript or bibliography.

Never disclose confidential manuscript or review content in external queries.
Verify source identity and read source content before claiming support. A local
BibTeX key alone establishes identifier presence, not semantic correctness.

## Evidence labels

- `in-paper`: reported in the manuscript, with a location.
- `local-bib`: bibliographic entry exists locally; verify claim support separately.
- `source-verified`: primary-source metadata/content actually checked, with URL,
  version, access date, and the relevant locator.
- `user-confirmed`: supplied directly by the user, retaining its stated scope.
- `missing`: absent from available material.
- `needs-user-input`: a consequential gap that cannot be resolved within scope.

For local hygiene, check key presence, duplicates, citation consistency and
applicable anonymity requirements. For an unresolved citation, state the needed
source, affected claim and exact remaining gap. Manual BibTeX input is a fallback
for inaccessible or deliberately closed sources, not the default for a requested
literature-completion task.

## Numerical evidence

Never invent results, p-values, uncertainty, seed counts, baselines, ablations,
or dataset sizes. Distinguish externally reported values from this project's own
measurements. Missing experimental evidence remains missing even when a citation
has been verified. Draft placeholders must not be presented as finished evidence.

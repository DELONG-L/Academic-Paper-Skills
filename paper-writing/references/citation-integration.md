# Citation Integration

Choose the source workflow from the user's request and applicable project
constraints. Reuse existing authorization; do not require a separate
"citation audit" invocation for work already requested.

## Source modes

| Task | Sources and actions |
|---|---|
| Pure prose polish or an ordinary manuscript review | Use existing manuscript keys, `.bib`, supplied papers and notes. Flag unsupported claims; do not expand the bibliography merely to polish wording. |
| Explicit closed-corpus/local-only task | Stay inside the declared corpus. Record missing support rather than searching outside it. |
| Complete Related Work, find missing literature, check novelty, verify or repair citations | Read relevant public primary sources, verify metadata, and produce the requested grounded text or assessment. When local edits are requested, update the relevant bibliography and citations and show the diff. No second authorization is needed for those scoped steps. |

Honor an explicit propose-only, read-only, manual-BibTeX, or approval-before-editing
instruction. If a newer request clearly changes the source scope, use it; ask
only about a material unresolved conflict. A request to find candidates permits
lookup but does not automatically authorize editing an existing manuscript.

## Grounding and metadata

- Never invent authors, titles, years, venues, DOI/arXiv identifiers, or BibTeX
  from memory. Obtain metadata from a primary publication record or the relevant
  registration service and verify that it identifies the intended work/version.
- Read the actual source content before using it to support a specific empirical,
  theoretical, novelty, or comparative claim. Metadata and title similarity alone
  are insufficient; an existing manuscript sentence is a claim to verify, not
  independent evidence that its citation is correct.
- Record the source URL/identifier, version, access date, and relevant page,
  section, table, or quoted span in the project's existing evidence record.
  Distinguish discovery candidates, verified metadata, and verified claim support.
- Keep local references as the default starting point. A requested public-source
  verification workflow can add verified sources to the task's evidence record
  without a separate manual approval ceremony. Where `paper_context.yaml` exists,
  record that source scope in `approved_citation_sources` (for example
  `verified_primary_sources`) with its authorization and locators in the evidence
  record. Do not overwrite an explicitly closed-corpus policy.
- Preserve source-supplied identifiers when a lookup fails; report the unresolved
  check. A 404, timeout, or inaccessible publisher page does not prove fabrication.

## Verify the Level of Support Needed

For a citation audit, distinguish these checks and record their separate results:

| Check | Evidence needed | What it cannot establish |
|---|---|---|
| Key and format | Used keys and actual bibliography records | Whether a paper exists |
| Identity and version | Primary publication/registration record matched to title, authors and identifier | Whether the paper supports a claim |
| Content support | Relevant source passage, table, proof or method plus a locator | Claims outside the inspected content |
| Publication status | Available publisher correction/retraction notice or relevant current metadata | Absence of a notice when no reliable check was possible |

For direct quotes, compare exact wording; for paraphrases, compare meaning,
conditions and strength. A citation merely identifying a work's topic needs
enough verified content to establish that topic, but not an invented result span.
Do not treat citation counts, an API hit, or a similar title as content support.
Do not silently combine a preprint's content with a different version's metadata.

Record `key | manuscript claim | source/version | locator | check result | action`
in an existing evidence note for a substantial audit. Inspect authoritative
corrections when publication status matters; lack of access remains an unresolved
check, not evidence that a paper is fabricated or retracted. If a source fails
to support a statement, repair that association using verified evidence, narrow
the statement, or report the gap. Do not invent which paper the author intended.

## Privacy and action scope

Use public metadata or generic topic queries for public searches. Never upload
unpublished manuscripts, review text, confidential excerpts, or private data to
external services merely because citation checking is requested. Continue with
permitted public information and local material; ask only when a necessary
disclosure falls outside the existing authorization. Do not publish, push, or
submit manuscript changes without the applicable authorization.

## Local edits and hygiene

For authorized citation fixes, preserve existing BibTeX keys and unrelated
entries. Add a new stable, project-consistent key only for a source actually
retrieved and verified. Move or edit citation commands within the requested prose
scope. If a key must change, update all affected references together. Check
missing/duplicate keys and relevant compilation; report unused keys rather than
automatically deleting them.

Place citations beside the claims they support. Group papers only when each
supports the associated statement. For Related Work, synthesize by meaningful
comparison axes and preserve differences in setting and evidence strength.

## Unresolved support

Complete all supported portions first. If a source is unavailable or outside a
closed corpus, explain the exact gap and affected claim. Use a short
`[citation needed: topic/claim]` marker only in a draft; keep process notes outside
paper prose. Request a manual source or BibTeX entry only when it is needed and
cannot be obtained within scope. Do not guess a citation key to make compilation
succeed, and do not claim final citation completeness while support is missing.

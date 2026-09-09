# Standalone Sections for Coauthor Review

Use when asked to compile a section separately or package a focused review copy.
Return the requested excerpt and usable sources. Do not change manuscript prose
to fragments, add a disclaimer, or relocate shared files unless that change is
actually requested or needed for the build.

## Select a Build Strategy

Identify the main document, selected section, its input files, figures, tables,
macros, bibliography, and external references. Build the main source first when
using its reference data. Keep its build products separate from the excerpt's.

- For a local live preview, prefer a driver that inputs the existing section
  sources. Build from the paper root so relative paths retain their meaning, or
  set explicit input/graphics paths in the driver.
- For an existing `include`-based manuscript, `includeonly` can preserve excluded
  sections' reference data after a full build; inspect what remains in the output.
- For a shareable package, make a self-contained snapshot of necessary sources
  and record their source revision. Symlinks to files outside the archive are not
  a portable package. Keep the snapshot separate from the maintained manuscript.

## Resolve References Intentionally

Distinguish labels defined in the excerpt from labels referring to omitted text.
Local labels must resolve to the excerpt's own numbering. External labels should
be identified as references to the full manuscript; do not silently make them
look like local pages or figures.

Where supported by the local TeX setup, use `xr`/`xr-hyper` with an external-label
prefix and a current main `.aux` file. For example, a local-only driver can import
`main.aux` with `\externaldocument[full-]{main}` and explicitly refer to
`\ref{full-sec:method}`. A driver-specific alias may map external labels in shared
text to those prefixed references; do not overwrite labels that are local.
Inspect package support before combining this with `cleveref`, which also needs
reference-type information. Do not hard-code numbers from memory to remove `??`.

If frozen labels or a packaged auxiliary file are used, record the main-source
revision and rebuild or refresh after it changes. Carry the relevant external
label metadata and transitive auxiliary dependencies, not unrelated build state.
If no reference data is available, obtain it or make the unresolved external
reference explicit in a draft; do not claim the excerpt is final.

## Verify Both Use Cases

Compile the excerpt with its actual driver and bibliography. Inspect unresolved
references/citations, missing assets, duplicate labels, overflow, page breaks,
and final-width readability. View the rendered pages; compiler success alone
does not establish readable tables or correct reference numbering.

For a live preview, rebuild the main manuscript if shared source or macros changed.
For a package, extract it into a fresh directory and build there, without relying
on files outside the package. Record the build command, main-source revision and
whether external references use full-manuscript numbering. Keep those notes in
the delivery record rather than adding defensive prose to the paper.

The result is a local preview or a shareable snapshot as requested. Sending it to
coauthors remains a separate external action requiring authorization.

Inspired by claude-scholar's
[coauthor excerpt workflow](https://github.com/OniReimu/claude-scholar/blob/d5eb9fc2e46128fccaf0a198519035c752f358b7/skills/coauthor-excerpt/SKILL.md).

# Paper Policy Integration

Use the sibling `paper-policy` skill as the constraint source for writing. This
integration is read-only: resolve rules before drafting, then write within the
result. Do not use resolution as permission to edit manuscript files or `.bib`
files automatically.

## When To Resolve

Resolve policy for:

- full-paper or multi-section work;
- outlines, structural revision, and prose polish across a manuscript;
- venue-aware, submission, rebuttal, or camera-ready writing;
- citation-aware writing;
- sections or artifacts with conditional rules, including Introduction,
  Related Work, Results, Conclusion, LaTeX manuscripts, and contribution lists.

For a short isolated rewrite, construct a transient context mapping and apply
the same rules without creating a persistent `paper_context.yaml`.

## Procedure

1. Read `../../paper-policy/references/context-schema.md`.
2. Reuse an existing `paper_context.yaml` for complex work, or build context
   from user statements and supplied files. Record provenance for hard-sensitive
   fields. Set `measurement_bias_status` when a characterized systematic error
   exists, set `evidence_structure` when evidence sources have distinct claim
   roles. Put generic file/output kinds in `artifacts`; put semantic selectors
   such as `threats_to_validity` or `limitations_content` in `features` when
   the requested scope analyzes them.
   Omit `policy_sets` for the public defaults. Add
   `policy_sets: [strict-house-style]` only from an explicit user or project
   configuration; the set automatically includes the public defaults.
3. Run the resolver when a context file exists:

```bash
python3 ../paper-policy/scripts/resolve_policy.py paper_context.yaml
```

Adjust the relative path to the repository root when necessary.

4. Inspect `active_policy_sets`; never apply a house rule merely because it
   exists in the registry.
5. Apply `active_hard` requirements before choosing among `active_soft`
   variants. A profile preference remains soft.
6. Treat `context_warnings` and `unverified_context` as unresolved inputs, not
   as passed checks. `policy_set_notes` and `inactive_profiles` are explanatory
   and do not themselves block readiness.
7. Draft or rewrite only the text in the user's requested scope.

## Mutation Boundary

- Never infer that policy resolution authorizes semantic autofixes.
- Never automatically add, remove, or rewrite BibTeX entries.
- Preserve LaTeX commands, labels, citations, math, and macros unless explicitly
  authorized.
- For existing files, present or apply user-requested prose changes only. Do not
  mutate unrelated manuscript state.
- Resolver output says what applies; linting and evidence review determine
  compliance.

## Failure Behavior

- In draft work, narrow unsupported claims or retain an honest placeholder.
- In final-stage work, report blocking hard failures instead of silently
  weakening or deleting requirements.
- Keep semantic and manual hard rules `UNVERIFIED` until evidence or human
  review supports a decision.

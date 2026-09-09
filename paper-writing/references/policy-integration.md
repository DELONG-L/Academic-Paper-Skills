# Paper Policy Integration

Use the sibling `paper-policy` as the shared constraint source. Rule correctness
applies at every task size; the amount of workflow machinery depends on the
requested result. Resolution identifies applicable rules and grants no new
editing, publication, or submission permission.

## Choose the Validation Depth

| Task | Appropriate policy work | Persistence |
|---|---|---|
| Local rewrite, translation, or ordinary section draft | Apply evidence, citation, meaning, and known project constraints to the changed text | No context file or compliance dossier required |
| Outline, multi-section draft, or whole-paper revision | Check relevant manuscript constraints and cross-section claims; resolve policy when applicability is uncertain or the user requests it | Reuse context/notes; persist only when useful for continuity |
| Explicit policy audit or conflict resolution | Read context schema, resolve the actual scope, explain active rules and unresolved facts | Save inputs/results when the requested audit needs a reproducible record |
| Submission-readiness or final compliance judgment | Resolve current context, run relevant checks, and assess admissible evidence | Record context, source-bound evidence, and assessment for the judgment |

A task containing a citation, Introduction, Results, or Conclusion does not by
itself require a full compliance run. An actual citation-verification request
still requires checking sources; an actual final-render request still requires
render inspection. A stage label alone does not expand a local edit into a
whole-paper readiness audit.

## When Using the Resolver

1. Read `../../paper-policy/references/context-schema.md`. Reuse or create context
   from current user statements and supplied materials. Confirm that its scope
   matches the requested judgment and that hard-sensitive fields have provenance.
2. Use shared defaults `[integrity-core, academic-defaults]`. Record applicable
   project/venue requirements with their source. Keep generic artifact kinds in
   `artifacts` and semantic selectors in `features`. Include load-bearing threats,
   limitations, known systematic bias, and distinct evidence roles when present.
3. Run `../../paper-policy/scripts/resolve_policy.py` from the sibling policy skill:

```bash
python3 /path/to/skills/paper-policy/scripts/resolve_policy.py /path/to/paper_context.yaml
```

4. Inspect active rules and unresolved context. Apply hard constraints and adapt
   soft guidance to the manuscript. Resolver warnings do not establish compliance.

For formal readiness assessment, load the policy compliance schema and use
`paper-policy/scripts/run_project_validation.py` for the project-local first
pass, then `assess_compliance.py` with actual evidence. These script names are
relative to the installed policy skill, not the manuscript repository. For
review findings and submission-readiness reporting, use `paper-review`.

## Evidence and Mutation Boundaries

- Apply only the authorized prose, structure, or bibliography changes. Preserve
  unrelated manuscript state and existing citation keys. Source lookup follows
  `citation-integration.md`; an audit is not authorization for a bibliography rewrite.
- Narrow unsupported draft claims or show precise factual placeholders. For a
  final judgment, expose unresolved hard requirements rather than suppress them.
- Formal semantic PASS requires a precise artifact, locator, supporting reasoning,
  and current `source_snapshots`. Manual checks still require human, user, or venue
  evidence. Deterministic failure takes precedence. See the compliance schema.
- A useful prose draft does not need every whole-paper rule to be verified. Report
  completion of the requested edit separately from any unperformed global audit.

# Editing and validation

Use these rules when editing an existing or generated artifact and before reporting completion.

## Handle generated Markdown

Before editing, check whether the target is generated from source comments, schemas, templates, or
a documentation build.

- Prefer changing the canonical input or generator when it is available and within the requested
  scope.
- Do not edit only the generated output when the next build would overwrite the change, except when the user explicitly requests an output-only edit. That exception does not authorize changing the generator.
- Preserve generated markers and regeneration instructions.
- Do not assume a file is generated without repository evidence. If the source or regeneration path
  cannot be found, report the uncertainty instead of inventing one.
- When the user explicitly requests an output-only change, state that regeneration may replace it.

## Edit existing documents

- Make targeted changes and preserve purpose and useful content.
- Remove duplication and place information where readers will look for it.
- Fix headings, terminology, links, and representation choices that obstruct comprehension.
- Do not convert prose into lists, tables, alerts, or diagrams unless doing so reduces cognitive
  effort.
- Do not add sections merely to make a document appear comprehensive.
- Preserve front matter, references, anchors, comments, and custom syntax unless changes are
  required.
- Update summaries, TOCs, and cross-references after structural edits.
- Apply the common source-line policy to newly authored or substantively rewritten explanatory prose. A local link, path, number, or typo correction does not authorize surrounding reflow or whole-file normalization.

## Validate the affected scope

For creation or editing, validate the requested change and directly affected scope; report pre-existing unrelated defects separately.
For review, run only non-mutating checks and report findings rather than repairing files.
Validate in proportion to that scope:

1. Find repository-provided Markdown lint, link-check, documentation-build, and diagram-render
   commands.
2. Run the checks relevant to the changed elements and affected scope.
3. When repository checks do not cover portable structure, run
   `scripts/check-markdown.py <FILE>...` from the installed `markdown-authoring` skill package.
4. Do not install dependencies or alter validation configuration solely to perform the checks.
5. Report each check that ran and its result.
6. Report checks that could not run, why they could not run, and what remains unverified.

The bundled checker validates relative link targets, heading-level jumps, balanced fenced code
blocks, non-portable `path:line` link destinations, and machine-specific home-directory paths. It is
a deterministic baseline, not a replacement for renderer-aware lint, documentation builds, link
fragment validation, or visual diagram review.
Its dependency-free scanner covers a conservative Markdown subset, not a full CommonMark or MDX parser.
It excludes recognized code examples and reports unsupported constructs as advisory coverage limits rather than inventing a broken-link result.
It does not resolve build-generated routes, reference usage, fragments, or arbitrary MDX/HTML semantics.
Assess diagnostics against explicit repository requirements and renderer evidence.
Report the exact evidence for false positives and non-applicable rules without claiming the raw check passed; actual defects and required repository checks remain binding.

## Complete the requested operation

For review, completion means the requested scope was assessed and findings, evidence, and limits were reported.
Neither file changes nor passing checks are required to finish a review.
Use the checklist below as assessment criteria, not as permission to repair findings.

For creation or editing, apply the checklist only to the requested change and directly affected content.
Report unrelated existing problems separately; do not expand the edit to eliminate them.
Before finishing the authorized creation or edit, verify that:

1. Purpose, audience, and outcome are clear.
2. The heading hierarchy forms a logical outline.
3. Each representation matches the information structure.
4. Korean authored prose throughout the changed scope uses `개조식`, including ordinary explanatory paragraphs, list continuations, and table prose; exceptions preserve literal content or explicit narrative requirements.
   Lists remain parallel and use ordering only when order matters; document-wide `개조식` does not force all prose into bullets.
5. Tables contain comparable two-dimensional data and remain readable.
6. Code fences are balanced and language identifiers are accurate.
7. Commands are copyable, placeholders explained, and input separated from output.
8. Links and anchors are descriptive, valid, and updated.
9. Images and diagrams have text alternatives or nearby summaries.
10. Renderer-specific syntax is supported.
11. Required content is not hidden in images, diagrams, footnotes, or collapsed sections.
12. Terminology, punctuation, emphasis, and technical formatting are consistent, and changed prose
    follows the common one-sentence-per-source-line policy.
13. Generated files were changed through an available, in-scope canonical source, or the user explicitly requested output-only editing and was informed that regeneration may replace it.
14. Review findings identify consequential problems before optional improvements and cite locations
    when available.
15. The authorized changes do not introduce secret, personal, stale, duplicated, fabricated, or irrelevant information. Report existing concerns without automatically deleting or rewriting unrelated content.
16. Applicable checks for the affected scope pass. False positives, non-applicable diagnostics, existing unrelated failures, and unavailable checks are identified with evidence and remaining verification limits. Required repository gates are not waived.

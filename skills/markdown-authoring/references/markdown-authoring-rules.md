# Markdown authoring rules

Apply these rules to `.md` files and Markdown content in MDX. Explicit repository instructions and
renderer or build constraints override them. Existing documents do not become writing rules merely
because inconsistent patterns have accumulated in the repository. This document contains the common
contract; read the linked rules only when the artifact uses those elements.

## Priorities

- Optimize for accuracy, readability, scanability, accessibility, portability, and maintainability.
- Prefer the simplest representation that communicates the information correctly.
- Use formatting to expose meaning, not as decoration.
- Preserve correct facts, terminology, examples, and any explicitly required voice when editing.
- Do not invent commands, options, paths, behavior, compatibility, support claims, or metadata.
- Match the requested language or the surrounding documentation. Keep technical identifiers
  canonical.
- Avoid unrelated rewrites and noisy formatting-only diffs. Naming a file does not authorize whole-file style normalization. Local link, path, number, or typo corrections do not require surrounding prose or source reflow. Apply writing defaults to newly authored or substantively rewritten explanatory prose; preserve literal quotations, commands, and identifiers.

## Determine the Markdown environment

Identify the target renderer before using extensions. Use the first available evidence in this
order:

1. Repository instructions such as `AGENTS.md` and explicit task requirements.
2. Documentation framework, build, lint, and renderer configuration.
3. Syntax that nearby maintained documents prove the renderer supports; do not infer prose style,
   list endings, or source wrapping policy from those documents.
4. Portable CommonMark when the renderer remains unknown.

- **Portable baseline:** headings, paragraphs, emphasis, blockquotes, ordered and unordered lists,
  links, images, horizontal rules, inline code, and fenced code blocks.
- **GFM extensions:** tables, task lists, strikethrough, and extended autolinks.
- **Renderer-specific:** alerts, footnotes, Mermaid, math, collapsed sections, front matter,
  directives, MDX components, GeoJSON, TopoJSON, and STL.

When support is unknown, default to portable CommonMark-compatible syntax. Use extensions only when
support is established. Preserve existing front matter, directives, MDX imports, components,
explicit anchors, and HTML unless the task requires changing them.

## Choose the operation

Match the work to the user's requested operation before changing a file.

- **Create:** identify the audience, purpose, renderer, and required outcome; then create the
  smallest complete document that serves them.
- **Edit:** inspect repository instructions, use nearby documents only to verify facts, terminology,
  links, or supported syntax, preserve correct content and stable interfaces, and make a targeted
  diff.
- **Review:** keep the task read-only unless the user also requests a change. Report correctness,
  broken navigation, unsupported syntax, accessibility barriers, and other consequential findings
  before optional improvements. Cite the file and line when available. Use only non-mutating checks.
  A review is complete when the requested scope has been assessed and findings, evidence, and limitations reported; it does not require fixing findings or passing checks.

Reading a document to answer a question is not an authoring review unless the user asks to assess
the document itself.

## Plan around the reader's goal

Identify the document's primary job before restructuring it.

- **Tutorial:** guide learning through a dependable path.
- **How-to:** complete a specific task with prerequisites, ordered actions, verification, and
  relevant recovery.
- **Reference:** support exact lookup with consistent structure and terminology.
- **Explanation:** develop understanding through rationale, examples, trade-offs, and useful
  diagrams.
- **README:** orient quickly; explain what, why, quick start, common use, and where deeper docs
  live.
- **Decision record or proposal:** separate context, constraints, options, decision, rationale,
  consequences, and open questions.

A document can combine modes, but each section should serve one clear reader need.

## Structure and prose

- Use one H1 for a standalone document unless the publishing system generates the title.
- Use short, descriptive headings that form a meaningful outline when read alone. Do not skip
  heading levels downward, use headings for visual size, leave headings empty, or put links in
  headings.
- Use sentence case for English headings and the natural convention of other languages. Prefer
  action-oriented headings for tasks and noun phrases for concepts when useful.
- Avoid manual numbering, trailing punctuation, and unnecessary code literals in headings. Do not
  rename stable headings casually; update links, anchors, and TOCs after structural changes.
- Put the purpose, answer, or outcome before background and history. Start substantial documents
  with a brief orientation covering scope, audience, and expected outcome.
- Put prerequisites before dependent steps and supporting detail after the main path. Use a manual
  table of contents only when a long document needs it and the renderer lacks adequate navigation.
- Use horizontal rules only for a genuine context change; headings should handle ordinary sections.
- Keep one main idea per paragraph. Prefer direct, concrete sentences and active voice when it
  improves clarity.
- Put each complete prose sentence on its own source line. Keep consecutive sentence lines in the
  same rendered paragraph, and use a blank line only for a semantic paragraph break. Do not wrap at
  a fixed column. Apply this policy to newly authored or substantively rewritten explanatory prose; a local literal or typo correction alone does not trigger reflow.
  Normalize the whole document only when that scope is requested.
- Apply Korean `개조식` throughout authored document prose, including ordinary explanatory paragraphs and table cells as well as all list types.
  Use noun phrases or action expressions without sentence-final punctuation; `변경 이력은 Git으로 관리` is the default form rather than `변경 이력은 Git으로 관리한다.`.
  Preserve conditions and causal reasoning, and choose paragraphs or lists according to information structure; this is not a requirement to make every line a bullet.
  Preserve quotations, code, commands, identifiers, and required syntax; honor explicit user requests or controlling requirements for narrative prose.
- Use action-led wording for procedures. Define unfamiliar terms and expand acronyms on first use. Use one term consistently for one concept.
- Put conditions before actions when the condition determines whether the action applies.
- State defaults, limits, consequences, uncertainty, dates, units, and expected results explicitly.
  Use concrete examples when they reduce ambiguity.
- Avoid filler, promotional language, repeated conclusions, and calling tasks easy, simple,
  obvious, or just.
- Do not turn connected reasoning into bullets or every sentence into a list item. Break dense text
  only with meaningful structure.

## Choose the representation

Use each form for the information it represents.

- **Paragraph:** rationale, nuance, cause and effect, concepts, uncertainty, and transitions.
- **Unordered list:** two or more peer items whose order does not matter.
- **Ordered list:** steps, phases, priorities, or rankings where order matters.
- **Task list:** concrete work whose completion state is intentionally tracked.
- **Table:** compact two-dimensional comparison or lookup across shared attributes.
- **Inline code:** commands, flags, paths, identifiers, configuration keys, and literal values.
- **Code block:** code, configuration, commands, data, logs, or output inspected as a unit.
- **Blockquote:** quoted material, not generic indentation.
- **Alert:** an exceptional supplemental fact, prerequisite, or risk when the renderer supports it.
- **Collapsed section:** optional long detail that is not required for the main path.
- **Footnote:** brief, nonessential qualification or source detail when supported.
- **Image:** visual evidence, interface state, or spatial information.
- **Mermaid:** non-trivial relationship, branching flow, interaction sequence, state model, or data
  structure.
- **Math:** a formal relationship that is clearer as an equation.

## Read conditional rules

Read only the references required by the artifact and requested change.

- For lists, procedures, tables, code, commands, emphasis, links, and navigation, read
  [Text and navigation](markdown-authoring/text-and-navigation.md).
- For images, accessibility, alerts, collapsed sections, footnotes, Mermaid, math, front matter,
  HTML, and MDX, read [Media and extensions](markdown-authoring/media-and-extensions.md).
- For generated files, existing-document edits, validation, and the completion checklist, read
  [Editing and validation](markdown-authoring/editing-and-validation.md).

## Finish deliberately

Use repository-provided Markdown lint, link-check, documentation-build, and diagram-render commands
in proportion to the changed content. When no repository checker covers basic portable structure,
use the skill's bundled checker. Do not install dependencies or alter validation configuration
solely to perform documentation checks. Report checks that ran, checks that could not run, and the
remaining unverified scope.
Treat bundled-checker diagnostics as evidence to assess against explicit repository requirements and the target renderer, not an independent authority overriding them.
Record the reason and evidence for a false positive or non-applicable diagnostic; do not change correct content solely to silence it or waive an actual defect or required repository check.

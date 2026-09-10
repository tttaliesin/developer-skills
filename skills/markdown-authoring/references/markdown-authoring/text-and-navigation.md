# Text and navigation

Use these rules when a Markdown artifact contains lists, procedures, tables, code, commands,
emphasis, links, or navigation.

## Lists and procedures

- Introduce a list with a complete sentence when the heading does not provide enough context.
- Keep items grammatically parallel and consistent in capitalization and punctuation.
- Outside the Korean default below, use complete sentences when items explain rationale,
  conditions, consequences, or multiple clauses. Use concise fragments or noun phrases for compact
  inventories, labels, and status summaries. Do not shorten connected reasoning into fragments
  merely to make it look concise.
- Apply the document-wide Korean `개조식` default to unordered, ordered, and task lists, including their explanatory continuation paragraphs.
  Express objects, states, and actions as noun phrases or action expressions without sentence-final punctuation, such as `환경 변수 설정`, `서버 실행`, and `실패 시 로그 확인`.
  Keep peer items parallel and retain rationale, qualifications, and connected reasoning in concise statements within the same item; moving text into a paragraph does not permit narrative `-다.`, `-합니다`, `-습니다`, or mechanical `-함` endings.
  Put only explanations shared by several items outside the list; keep conditions and exceptions attached to their own step.
  Use narrative prose only when the user explicitly requests it or a controlling document requirement needs it.
  These writing defaults do not normalize literal quotations, commands, or identifiers.
- State whether items are required, optional, alternatives, or examples.
- Do not create one-item lists or nest more than two levels when headings would be clearer.
- Use numbering only when sequence, dependency, priority, or ranking matters.
- Keep one primary action per procedural step and place supporting text under that step.
- Label optional and conditional steps explicitly.
- Show how to verify success when the result is not obvious.
- Put warnings before risky actions and add rollback guidance when failure can leave harmful state.
- Use task-list checkboxes only for tracked actions or outcomes, not ordinary instructions or
  feature lists.

## Tables

Use a table when readers need to compare several items across the same properties or repeatedly look
up compact reference data. Do not use a table for procedures, page layout, one-dimensional lists,
long prose, nested lists, code blocks, inconsistent row schemas, or content better expressed as
subsections. Avoid tables inside numbered procedures.

When using a table:

- Introduce its purpose with a complete sentence.
- Use concise headers and put shared units in column headings.
- Format literal values and identifiers with inline code.
- Use explicit values such as “Not applicable” instead of ambiguous empty cells.
- Keep cells short and parallel; split wide or text-heavy tables.
- Sort rows according to reader need: workflow, priority, alphabet, or number.
- Do not encode meaning only through alignment, color, emoji, or symbols.
- Prefer several simple tables over one table with irregular or multi-level headers.
- If GFM cannot express an accessible relationship, restructure the content or use semantic HTML
  only when supported.

## Code and commands

- Use inline code for technical literals, not bold or italics.
- Use fenced code blocks with a lower-case language identifier; use `text` for plain output.
- Put blank lines before and after fenced blocks. Separate commands from output unless a transcript
  is necessary.
- Omit shell prompts from copyable commands; include them only to distinguish users, hosts, or
  interactive contexts.
- State the required directory, shell, permissions, and prerequisites when not obvious.
- Wrap commands only with valid continuation syntax.
- Use consistent placeholders such as `<PROJECT_ID>` and explain them nearby.
- Never include real secrets, tokens, private keys, personal data, or deceptive production values.
- Prefer minimal, complete, executable examples over unexplained fragments.
- Prefer text code samples over screenshots when readers need to copy, search, compare, or maintain
  the example.
- Show output only when needed for verification, understanding, or extracting a value; label it
  exact or representative.
- Use `diff` fences only for small focused changes. Preserve valid syntax over visual alignment.

## Emphasis, links, and navigation

- Use bold sparingly for short scan anchors or UI labels. Use italics sparingly for
  natural-language emphasis or introduced terms.
- Use strikethrough only for a meaningful replacement, deprecation, or status transition. Do not
  rely on emphasis, color, emoji, or icons alone to convey status or risk.
- Use emoji only when it conveys useful meaning and remains understandable without it. Avoid
  decorative emoji and badge walls; keep only stable, useful status badges.
- Use short, descriptive link text that makes sense without surrounding prose. Do not use “click
  here,” “here,” “this page,” “read more,” or raw URLs as ordinary link text.
- Use relative links for repository-local content. Prefer canonical primary sources for technical
  references.
- Do not use identical link text for different destinations in the same document. Explain links
  that download files, open applications, or behave unexpectedly.
- Keep punctuation outside links and do not put links in headings. Use inline links by default; use
  reference-style links only when they improve maintainability.
- Do not guess generated anchors. Confirm renderer behavior or use an explicitly documented,
  renderer-supported anchor syntax.
- Do not use `path:line` as a Markdown link destination. It is an editor convention, not a portable
  CommonMark or GFM source-line link.
- For repository-local concepts, prefer a relative document link and a confirmed stable section
  anchor. When exact source lines are evidence, use the canonical Git host's permalink pinned to an
  immutable revision with an established line fragment such as `#L27-L31`.
- For non-versioned local evidence, use a portable logical locator with the observation date or
  command context instead of a clickable link. Do not put machine-specific home-directory or
  workspace absolute paths in persistent documentation.

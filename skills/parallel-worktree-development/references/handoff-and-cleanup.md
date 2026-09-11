# Handoff and cleanup

Use this phase after local integration, when handing back to the Git owner, or when a parallel path
must stop while preserving all reachable work.

## Return control

Return the exact repository, Issue when applicable, integration branch, integration and worker
commit SHAs, changed paths, validation evidence, final-destination status, and every pending gate to
`github-operations`. That skill retains ownership of push, PR, checks, merge, Issue closure, release,
workflow operations, and local or remote branch cleanup.

Local integration does not authorize publication. For a local diff or review-only endpoint, name
the exact path, base revision, diff, and checks instead of implying that commit or push occurred.
Keep every pending handoff visible with its reason, owner, and resumption condition.

## Preserve work during cleanup

Do not remove a worker worktree or local branch while it contains tracked, untracked, or ignored
files, another process may own it, or its commit is not integrated and verified. Never use
`git branch -D`, unconditional remote deletion, or force removal to make cleanup appear complete.
An idle worker alone is not grounds for deletion.

For Issue or delivery cleanup, follow the exact branch ownership, verified merged SHA, dirty and
ignored file, and process-ownership rules in `github-operations`. This skill never deletes remote
refs or infers cleanup authority from local completion.

## Stop conditions

Stop the affected parallel path and preserve reachable work when:

- slices overlap or depend on unfinished sibling output;
- a base revision, integration branch, worker branch, or worktree path is ambiguous;
- a worktree path is non-empty or contains user-owned state;
- a worker changes files outside its ownership contract;
- integration would change acceptance criteria or require an external interface decision;
- a required test or generated-source owner cannot be identified; or
- exclusive ownership needed for safe cleanup cannot be confirmed.

When serialization or another safe empty local path resolves the blocker within current scope,
continue without requesting approval again. Otherwise report the exact worktrees, branches, commits,
completed slices, conflicting paths, verification state, responsible owner, and resumption condition.

---
name: parallel-worktree-development
description: Coordinate a substantive local implementation across two or more genuinely independent Git worktrees after github-operations has classified any GitHub Issue lifecycle. Use for parallel slice decomposition, agent-to-worktree assignment, file ownership, local integration, conflict handling, and integrated verification. Do not create or resolve Issues, push, create or merge pull requests, publish releases, dispatch workflows, or delete remote refs; route those operations to github-operations.
---

# Parallel worktree development

Use this skill only when a substantive implementation has at least two genuinely independent slices
whose parallel execution is worth the worktree and integration cost. It owns local decomposition,
worktree isolation, worker contracts, integration, and verification. It does not own GitHub Issue
classification or any remote GitHub operation.

Read [the packaged ownership boundary](references/ownership-boundary.md) when establishing authorization and scope.
The complete local workflow is maintained in this entrypoint; no sibling checkout is required.

## Preserve the GitHub lifecycle boundary

Load the installed `github-operations` skill before this skill whenever the task may need
GitHub Issue tracking, an issue-resolution lifecycle, or any remote GitHub operation.
`github-operations` remains the sole owner of:

- deciding whether durable Issue tracking is warranted;
- Issue intake and Issue resolution;
- linked remote branch selection and creation;
- push, pull request, check, merge, release, and workflow operations;
- Issue closure and local or remote branch cleanup.

This skill begins only after that route is known. For an Issue resolution, receive the exact
repository, Issue, base branch, integration branch, acceptance criteria, validation commands, and
remote-mutation boundary from `github-operations`. When local integration and verification finish,
return the integrated commit and evidence to `github-operations`; do not push or continue the
GitHub lifecycle here.

If no GitHub operation is involved, this skill may coordinate local implementation directly, but it
still must not infer authorization for a remote mutation.

## Decide whether parallel worktrees are warranted

Use parallel worktrees only when all of the following are true:

- at least two slices can run without one consuming another's unfinished output;
- each slice has a complete observable result and an explicit file or symbol ownership boundary;
- the integration interface can be fixed before workers start;
- the integration and conflict risk is lower than the expected parallelism benefit; and
- the repository and filesystem can provide isolated, empty worktree paths.

Keep the work serial when slices modify the same file or generated source, share a mutable schema or
migration boundary, require ordered design decisions, or are too small to offset worktree overhead.
Do not manufacture parallel slices merely to use multiple agents.

## Establish the integration contract

Assign one integration owner before creating worker worktrees. Only the integration owner may
modify the integration branch or integration worktree. Record this contract before dispatch:

- exact repository root, verified remote identity when one is relevant, base revision, and
  integration branch and final delivery path/worktree (including any destination beyond the integration worktree);
- exact acceptance criteria and repository validation commands;
- one named slice per worker with owned files, directories, or symbols and explicit non-goals;
- interfaces shared across slices, including signatures, schemas, generated-source ownership, and
  ordering constraints;
- worker branch and worktree path;
- expected worker deliverable: local commit SHA, changed paths, validation performed, and unresolved
  risks;
- integration order when commits are not commutative; and
- the rule that workers never push, merge, rewrite the integration branch, or remove refs.

Name the final integration owner in that contract.
This owner remains accountable across skill transitions until the agreed destination is verified or an explicit pending handoff names its reason, owner, and resumption condition.
A worker's completion does not complete the user's task.

A file or generated artifact may have only one mutation owner. If unavoidable overlap is discovered,
stop the overlapping workers and serialize that boundary under the integration owner. Workers may
read shared files but must not mutate files outside their contract.

## Create isolated worker worktrees

Before mutation, inspect the repository and all current worktrees:

```bash
git rev-parse --show-toplevel
git branch --show-current
git remote -v
git status --short --ignored
git worktree list --porcelain
```

Preserve tracked, untracked, ignored, and user-owned files. Never stash, reset, discard, overwrite,
or carry unrelated changes into a worker branch. Every worker path must be absent or empty, and every
worker branch must be unique. A branch already checked out in another worktree is not reusable.

Create worker worktrees from the exact evidenced base revision using explicit local branches. Do not
use the integration branch in a worker worktree. Verify existing repository paths, remote identity, and the base revision from evidence.
For authorized local worker creation, choose a new unique branch name and an absent or empty worktree path within permitted writable locations, following repository naming rules.
This routine choice does not require another approval; existing files and branches remain protected.
Use the following command shape:

```bash
git worktree add -b <WORKER_BRANCH> <WORKTREE_PATH> <BASE_REVISION>
```

After creation, verify the worker path, branch, HEAD, and clean status independently. A worker must
run commands only with its assigned worktree as the working directory.

## Dispatch workers with complete contracts

Every worker assignment must state:

- exact worktree path and worker branch;
- owned files or symbols and forbidden overlaps;
- required behavior and observable acceptance criteria;
- fixed interfaces consumed or produced;
- relevant repository instructions and existing patterns;
- validation limited to the worker-owned scope; and
- the required local commit and evidence handoff.

Workers must not run project-wide formatters, linters, or full suites concurrently when those tools
can rewrite or contend on shared state. Run shared validation once after integration. A worker may
run a targeted check that is isolated to its contract and does not mutate shared caches or generated
artifacts outside its worktree.

## Integrate under one owner

The integration owner verifies each worker result before applying it:

1. Confirm the reported worker commit exists on the expected worker branch and worktree.
2. Confirm the changed paths match the assigned ownership boundary and contain no unrelated change.
3. Confirm the worker started from the required base or an explicitly approved descendant.
4. Review the diff and targeted validation evidence; do not trust a worker success statement alone.
5. Apply commits to the integration branch in the fixed order using a history-preserving local Git
   operation appropriate to the repository convention.
6. Resolve conflicts only under the integration owner. Re-read the current integrated source and
   preserve both slices' observable contracts; never accept an entire side mechanically.
7. Recheck every changed callsite, duplicate snapshot, generated-source boundary, and shared
   interface after integration.

Workers do not merge one another and do not integrate directly into the Issue branch. If a slice
invalidates the pre-agreed interface, pause dependent integration, update the contract explicitly,
and rerun affected verification rather than hiding the mismatch with a compatibility shim.

## Verify the integrated result

Verification happens from the integration worktree after all selected commits land:

- confirm the integrated diff contains only the authorized task scope;
- run repository formatting only when required and attribute any resulting file to the integration
  owner;
- run the complete relevant test module or test file, not only a single expected-to-change test;
- run applicable lint, type, build, and smoke checks for the integrated behavior;
- search every callsite and duplicate copy for changed interfaces, signatures, or policies;
- confirm worker branches and worktrees did not change remote state; and
- record the integrated commit SHA, commands, results, and remaining unverified boundaries.

A passing worker check is not integrated proof. A merge or cherry-pick success is not behavioral
proof.
Do not report successful integration to `github-operations` until the integration worktree is internally consistent and the task's observable acceptance criteria are verified.
Copying files onto an older or dirty checkout does not establish integration.
Verify the destination's base, preserve unrelated changes, and use the Git owner's safe integration procedure; confirm the integrated revision and relevant checks at the agreed final destination.
If that destination is still pending, return an explicit incomplete handoff rather than claiming integrated delivery.

## Return control and clean safely

Return to `github-operations` with the repository, Issue when applicable, integration branch,
integrated commit SHA, worker commit SHAs, validation evidence, and any pending gate. Only
`github-operations` may push, create or merge a pull request, verify Issue closure, or delete remote
refs.

Local integration does not authorize remote publication.
If the agreed endpoint is a local diff or review-only result, name its exact path, base revision, diff, and checks instead of implying a commit or push occurred; the worker commit contract above applies to this multi-worktree implementation workflow, not to every message or single-worker task.

Do not remove a worker worktree or local branch while it contains tracked, untracked, or ignored
files, while another process may own it, or before its commit is integrated and verified. For
Issue-resolution cleanup, use the safety and merged-SHA rules owned by `github-operations`; never use
`git branch -D`, unconditional remote deletion, or force removal to make cleanup appear complete.
An idle worker alone is not grounds for deletion.
Keep pending cleanup in the task's final status with its reason, owner, and resumption condition, even after implementation or a skill handoff ends.

## Stop conditions

Stop the affected parallel path and preserve all reachable work when:

- slices overlap or depend on an unfinished sibling result;
- the base revision, integration branch, worker branch, or worktree path is ambiguous;
- a worktree path is non-empty or contains user-owned state;
- a worker changes files outside its ownership contract;
- integration would require changing acceptance criteria or an external interface decision;
- a required test or generated-source owner cannot be identified; or
- exclusive ownership needed for safe cleanup cannot be confirmed.

When serialization or another safe empty local path resolves the blocker within existing scope, continue without requesting approval again.
Otherwise continue independent authorized work and report the exact worktrees, branches, commits, completed slices, conflicting paths, verification
state, responsible owner, and resumption condition. Do not turn a coordination blocker into a remote
mutation or destructive cleanup.

# Planning and worker worktrees

Use this phase when deciding whether to parallelize, defining slice ownership, creating worktrees,
or dispatching workers.

## Confirm parallel work is warranted

Parallel worktrees are appropriate only when all of the following hold:

- at least two slices can run without consuming another slice's unfinished output;
- each slice has a complete observable result and explicit ownership boundary;
- shared interfaces can be fixed before workers start;
- integration and conflict risk is lower than the expected throughput benefit; and
- the repository and filesystem provide isolated, absent or empty worktree paths.

Keep work serial when slices touch the same file or generated source, share a mutable schema or
migration, need ordered design decisions, or are too small to offset coordination cost. Do not
manufacture slices to justify multiple agents.

## Establish the integration contract

Record one named integration owner and the following evidence before dispatch:

- exact repository root and verified remote identity when relevant;
- exact base revision, integration branch, integration worktree, and any final destination beyond it;
- observable acceptance criteria and repository validation commands;
- one named slice per worker with owned files or symbols and explicit non-goals;
- shared signatures, schemas, generated-source ownership, and ordering constraints;
- unique worker branch and worktree path;
- required deliverable: local commit SHA, changed paths, validation, and unresolved risks;
- integration order when commits are not commutative; and
- the prohibition on push, merge, integration-branch mutation, ref deletion, or cleanup by workers.

Workers may read shared files but must not mutate outside their contract. If overlap is unavoidable,
stop the affected workers and serialize that boundary under the integration owner.

## Create isolated worker worktrees

Before mutation, inspect the repository and all worktrees:

```bash
git rev-parse --show-toplevel
git branch --show-current
git remote -v
git status --short --ignored
git worktree list --porcelain
```

Verify the exact base revision and repository identity. Each worker path must be absent or empty,
each branch must be new and unique, and no branch may already be checked out elsewhere. Create each
worker from the evidenced base, never from another worker's unfinished state or the integration
branch:

```bash
git worktree add -b <WORKER_BRANCH> <WORKTREE_PATH> <BASE_REVISION>
```

After creation, verify the worker path, branch, HEAD, and clean status independently. This bounded
local setup does not require another approval when it preserves existing state and follows the
already approved contract.

## Dispatch complete worker contracts

Every assignment states the worktree and branch, owned paths or symbols, forbidden overlaps,
required behavior, observable acceptance criteria, fixed interfaces, repository instructions,
targeted validation, and required local commit and evidence handoff.

Workers must not run project-wide formatters, linters, or full suites concurrently when they can
rewrite or contend on shared state. Run shared validation after integration. A worker may run an
isolated targeted check that cannot mutate shared caches or artifacts outside its worktree.

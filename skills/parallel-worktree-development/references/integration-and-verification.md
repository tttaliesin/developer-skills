# Integration and verification

Only the named integration owner performs this phase from the agreed integration worktree.

## Inspect each worker result

Before applying a worker commit:

1. Confirm the commit exists on the expected worker branch and worktree.
2. Confirm changed paths match the ownership contract and contain no unrelated change.
3. Confirm the worker started from the required base or an explicitly accepted descendant.
4. Review the diff and targeted validation evidence rather than trusting the success statement.
5. Reconfirm integration order and the shared interface contract.

## Integrate under one owner

Apply commits in the fixed order with a history-preserving local Git operation that matches the
repository convention. Workers never merge one another or integrate directly into the Issue or
integration branch.

Resolve conflicts only under the integration owner. Re-read the combined source and preserve every
slice's observable contract; do not accept an entire side mechanically. Recheck changed callsites,
duplicate snapshots, generated-source boundaries, and shared interfaces. If a slice invalidates the
agreed interface, pause dependent integration, update the contract explicitly, and rerun affected
verification instead of hiding the mismatch with a compatibility shim.

## Verify the combined result

From the integration worktree:

- confirm the integrated diff contains only authorized scope;
- run repository formatting only when required and attribute its changes to the integration owner;
- run the complete relevant test module or file, not only one expected-to-change test;
- run applicable lint, type, build, and smoke checks;
- search callsites and duplicate copies for changed interfaces, signatures, or policies;
- confirm worker branches and worktrees did not change remote state; and
- record the integrated commit SHA, commands, results, and unverified boundaries.

Verify the result at the agreed final destination, not only in an intermediate worktree. Confirm its
base and revision, preserve unrelated changes, and use the Git owner's safe integration procedure.
Copying files onto an older or dirty checkout does not establish integration. If final-destination
integration is pending, return an explicit incomplete handoff rather than claiming delivery.

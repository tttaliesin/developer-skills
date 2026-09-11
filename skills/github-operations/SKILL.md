---
name: github-operations
description: Establish the delivery endpoint and authorized Git workflow for repository development, independently decide whether GitHub Issue tracking is useful, and safely operate repositories, Issues, pull requests, releases, workflows, pushes, and branches with gh and git. Apply authentication, mutation-scope, retry, and verification rules. Do not use for editing GitHub Actions YAML.
---

# GitHub Operations

Establish the user's delivery endpoint before selecting implementation or tracking steps.
Preserve that outcome and claim completion only from verified GitHub and Git state.

## Read the package policy

Read [the GitHub operations rules](references/github-operations.md) before deciding whether a task
needs issues, running a GitHub command, or deciding that an operation cannot proceed.

Read the endpoint and authorization rules before choosing a route; Issue tracking must not decide where delivery stops.

- **Implementation:** Determine the delivery endpoint from the user's outcome, current session authorization, and verified repository workflow: a local diff/review, pushed branch, PR, or merged target as applicable.
  Complete all authorized stages to that endpoint, with a named integration owner and final-location checks, whether or not an Issue is used.
  A worker result is not final delivery; use the [local completion rules](references/github-operations.md#로컬-통합과-완료를-확인한다).
  A local-only or review-only endpoint does not require a commit or remote mutation; an Issue-free task is not automatically local-only.

- **Task intake:** Decide whether durable issue tracking adds real coordination, review, dependency,
  risk, or resumability value. Keep a small atomic task issue-free. When issues are warranted, make
  each one independently complete and mergeable with scope, acceptance criteria, validation, and
  dependencies. Read [the issue delivery recipes](references/github-issue-delivery-recipes.md)
  before creating them. Stop with the created identifiers only when intake itself is the authorized endpoint.
  When tracking supports an already-authorized implementation, continue to its established endpoint without requiring the user to reissue the work using the new Issue number.
  Issue creation neither expands nor truncates existing authorization; preserve explicit intake-only limits.
- **Issue resolution:** Treat a request to resolve, complete, or handle a specific issue as
  authorization for its normal lifecycle: reuse or create its linked branch, checkout, implement,
  test, commit, push, create a closing PR, satisfy required checks with in-scope fixes, merge under
  repository policy, clean up the issue branch, and verify PR merge and issue closure. Read
  [the issue delivery recipes](references/github-issue-delivery-recipes.md) and the merge sections
  in [the repository and PR recipes](references/github-repository-pr-recipes.md).
- **Explicit GitHub operation:** For repository, push, issue creation only, PR creation only, merge,
  release, or workflow-run requests, read only the matching detailed recipe: issue operations use
  the issue delivery recipes, repository and PR operations use the repository and PR recipes, and
  release or run operations use
  [the release and workflow recipes](references/github-release-workflow-recipes.md). Perform only
  that operation and its normal necessary steps. A PR-only request does not authorize merge.

Before running commands in any route, read
[the common command rules](references/github-operation-recipes.md) for target identification,
dirty-worktree protection, first-class command selection, and retry behavior.
For branch switching, worktree removal, and local or remote branch cleanup, use the bundled
`scripts/git-safety.py` helper. It requires a verified repository remote and expected merged SHA,
refuses ignored-file overwrite and unsafe worktree removal, and uses conditional local and remote ref
deletion. Do not replace it with `git branch -D`, an unconditional remote delete, or
`gh issue develop --checkout`.
The helper does not lock out unrelated local processes, so confirm exclusive ownership of the
repository and worktree before cleanup; if that cannot be confirmed, stop without deleting refs.

## Hand off local parallel implementation

After route selection, hand substantive implementation to
`parallel-worktree-development` only when it has at least
two genuinely independent slices and isolated worktrees materially improve throughput. Pass the
exact repository, Issue when applicable, base revision, final delivery path/worktree, branch or agreed local diff, named integration owner, acceptance criteria, validation commands, and remote-mutation boundary. That skill owns worker worktrees, local commits,
and local integration only; it returns the agreed integrated revision or explicit local diff and final-destination verification evidence here.

Do not ask the parallel skill to decide Issue tracking, create or resolve Issues, push, create or
merge pull requests, publish releases, run workflows, or delete remote refs. Do not create a second
Issue or branch lifecycle for the worker slices. Resume the selected GitHub route only after the
agreed final destination is internally consistent and its observable acceptance criteria are verified.
Then perform any remaining authorized remote delivery stages and verify their result; a local worker handoff does not shrink the parent task's endpoint.
Keep owed integration or cleanup visible with its reason, owner, and resumption condition; an idle worker does not authorize deleting its worktree.

## Preserve the authorization boundary

The issue-resolution lifecycle does not authorize `--admin`, protection or review bypass, material
changes to issue scope or product requirements, production deployment, release publication,
visibility changes, unrelated repository mutations, or deletion of unrelated branches and
resources. Stop at the verified pending state when an external review, check, permission, or policy
gate cannot be satisfied within scope.

Do not carry unrelated uncommitted changes across an issue-branch checkout. Use a safe separate
worktree when its path and ownership are clear; otherwise stop before checkout without stashing,
committing, resetting, or discarding those changes.

Apply these invariants throughout the task:

- Identify the target repository, owner, branch, visibility, and resource from available context.
  Ask only when a wrong choice could materially change another remote resource.
- Do not run `gh auth status` as a routine preflight. Use it when the user requests authentication
  diagnosis or after the targeted command returns an authentication-related failure and the result
  would narrow the cause.
- Do not infer that an untried operation is impossible from a general authentication diagnostic.
  Distinguish authentication, authorization, validation, network, sandbox, and service failures.
- Never expose credentials or switch accounts, credentials, or API clients merely to bypass a
  failure.

## Execute and verify

Use `git` for local history and remote ref transfer and `gh` for GitHub resources. Start with the
narrow command that performs or directly inspects the requested operation. Prefer explicit targets,
non-interactive inputs, and structured `--json` output. Use `gh api` only when a first-class `gh`
command cannot perform the required operation. Preserve the relevant error when a command fails.

Before retrying a create or publish operation, inspect whether the first attempt already created the
resource. Verify each relevant state separately: local and remote commit, PR base and head, actual
merge rather than auto-merge or queue registration, issue closure, and branch cleanup. Report local
completion, remote completion, pending gates, and remaining work separately when the result is
partial.

For cleanup after a verified merge or direct integration, act only on the exact temporary branch owned by that authorized delivery, whether or not it used an Issue.
Preserve a PR-only or branch-delivery endpoint and any branch with an explicit retention purpose.
Confirm the accepted integration and compare local and remote branch SHA with the verified job or PR head immediately before deletion; a changed SHA means the branch advanced and must not be deleted.
Record separate local-ref, remote-ref, and worktree dispositions, and keep any pending cleanup visible with its reason, owner, and resumption condition.

---
name: differential-review
description: Review a PR, commit, or diff for security regressions and blast radius using risk-based history, caller, and test analysis. Use for security-focused differential review, regression checks, or untested changed code; not greenfield audits or ordinary cosmetic review.
allowed-tools: Read Write Grep Glob Bash
---

# Differential security review

Review the changed behavior first, then expand history, dependency, caller, and adversarial analysis when risk evidence justifies it

## Core principles

- Risk first — prioritize trust boundaries, authorization, validation, secrets, crypto, value transfer, external calls, and state changes
- Evidence based — support findings with the current diff, reachable behavior, history, tests, and concrete attack conditions
- Proportionate — scale depth to impact, uncertainty, and reachability rather than repository or diff size alone
- Honest — separate verified behavior, static inference, coverage gaps, and unavailable evidence
- Scoped — review the requested base and head without changing branches, discarding work, or editing reviewed code

## Preserve the output boundary

Use the user's requested output format and location
For a large or resumable review, create a persistent report when repository writes are authorized and persistence materially helps review
For a bounded review or explicit read-only request, report directly without creating a file
Never write to another repository, Desktop, or a skill installation directory to bypass a write restriction
Posting findings to a PR or creating an Issue requires separate authorization

Review priority, vulnerability severity, exploitability, and confidence are separate
Missing tests increase investigation priority but do not by themselves establish a vulnerability or raise severity
Caller counts are search evidence, not a direct measure of affected users, records, tenants, or financial impact

## Triage by changed behavior

| Risk | Evidence in the change | Default depth |
| --- | --- | --- |
| High | Authorization or validation removed, secret or crypto handling, value transfer, privileged state change, new externally reachable call | Focused baseline and caller analysis, relevant history, tests, then adversarial analysis |
| Medium | Business logic, state transitions, parsing, persistence, or a new public interface without a demonstrated high-risk path | Focused diff, relevant dependencies, callers, and tests |
| Low | No meaningful security exposure after checking actual behavior | Surface scan and concise coverage statement |

Repository size can change search batching and sampling but must not lower the depth required by a reachable high-risk change or force all dependencies to be read for a low-risk change

## Choose the route

- Quick triage — inventory and surface-scan every changed file, analyze the risk-bearing changes, and state omitted scope
- Focused review — read [risk-first methodology](methodology.md) for changed behavior, targeted history, test coverage, and blast radius
- High-risk review — after relevant baseline and reachability evidence, read [adversarial analysis](adversarial.md)
- Vulnerability lookup — read [patterns](patterns.md) only for pattern families relevant to the selected changes
- Persistent report — read [reporting](reporting.md) only when producing that artifact

The local adversarial method is sufficient
Delegate only when the host, user request, and review scope authorize it; do not assume a companion agent exists

## Minimum review contract

1. Establish the exact base, head, and changed-file inventory
2. Surface-scan all changed files and classify the behavior and trust boundary of each material change
3. Compare baseline and changed behavior for the selected risk-bearing regions
4. Inspect history when removed or reintroduced code may encode a security invariant or prior fix
5. Trace callers and externally reachable effects when the changed interface or state can propagate impact
6. Inspect relevant tests and distinguish test presence from meaningful assertion coverage and actual execution
7. Build a concrete attack scenario only when the entry point, preconditions, changed behavior, and impact are supported
8. Report analyzed, surface-scanned, and omitted scope with confidence and limitations

## Escalate these signals

- Code removed from a security, CVE, validation, or prior-fix commit
- Access control weakened or an internal boundary made externally reachable
- Validation removed without an equivalent guard at the relevant boundary
- External calls or privileged state changes added without supported failure handling
- A high-risk change with broad reachable effects or unresolved outcome semantics

These signals require deeper investigation, not an automatic vulnerability finding

## Finish the review

- Lead with concrete findings and their file and line locations
- Include the attack path, impact, required conditions, evidence, and confidence for each vulnerability
- Report coverage gaps and missing execution evidence separately from findings
- Do not fabricate history, line numbers, caller counts, test results, or exploitability
- Deliver the requested output and notify the user of material results and unresolved limits

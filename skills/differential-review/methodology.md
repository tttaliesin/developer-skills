# Risk-first differential review methodology

Use this workflow for a focused review after the root skill has selected the material risk-bearing changes
Apply only the sections needed to resolve the current risk and coverage questions

## Establish the exact diff

Read the requested base and head without checking out another revision or altering the working tree

```bash
git diff <base>..<head> --stat
git log <base>..<head> --oneline
git diff <base>..<head> --name-only
```

For a working-tree review, inspect the relevant staged and unstaged diffs separately
Record unavailable commits, shallow history, generated files, submodules, or excluded paths rather than implying complete coverage

Inventory every changed file and surface-scan it for:

- Trust-boundary or privilege changes
- New external input or output
- Authorization, validation, serialization, or error-path changes
- Secret, token, logging, and executable-example exposure
- State transitions, value movement, and irreversible effects

Use repository size only to choose efficient search and sampling tools
Do not classify risk from file count or extension alone

## Compare selected changed behavior

For each risk-bearing region, inspect both versions and record:

```text
Before: relevant behavior and invariant
After: changed behavior
Boundary: caller, input, state, external system, or privilege crossed
Security effect: supported risk or confirmed lack of exposure
Evidence: file, line, revision, and test or caller when available
```

Check nearby code and the dependencies needed to understand that behavior
Do not read every dependency merely because the repository is small
Expand one hop or farther when the changed value, permission, or effect crosses that boundary

### Use history when it can answer a security question

Inspect blame or log evidence when:

- Security, validation, authorization, or error-handling code was removed or weakened
- A change appears to reintroduce a previously removed pattern
- The reason for a non-obvious invariant affects exploitability or compatibility
- A commit message or nearby history names a CVE, incident, audit, or regression

```bash
git log -S "<changed pattern>" --all --oneline
git blame <base> -- <path>
```

Age or commit wording alone does not establish severity
Use history to explain the invariant and regression risk, then confirm the current reachable behavior

## Analyze test coverage

For each selected function, endpoint, parser, or state transition:

- Find tests that exercise the changed branch and its security invariant
- Inspect assertions rather than inferring coverage from a matching test name
- Check boundary cases relevant to the change, such as missing, duplicate, late, unauthorized, malformed, or reordered input
- Record whether tests were executed, inspected statically, unavailable, or absent

An untested change is a verification gap and a reason to investigate further
Rate vulnerability severity only from supported impact, reachability, and exploit conditions

## Trace blast radius

Count direct text matches only as an approximate search aid
Use symbol-aware or call-graph tools when available, then inspect the meaningful callers

```bash
rg "<function or endpoint>" <relevant paths>
```

Assess:

- External entry points and privilege levels
- Transitive callers and downstream consumers
- Records, tenants, assets, or physical effects that can be reached
- Retry, duplication, timeout, and unknown-outcome behavior
- Compatibility with older producers, consumers, clients, or persisted data

A single public caller can have larger impact than many internal callers
Do not turn caller-count thresholds into severity labels

## Build only the needed baseline context

For a high-risk or unresolved change, establish the baseline invariants needed to judge it:

- Entry conditions and access control
- State reads and writes
- Validation and normalization boundaries
- Internal and external calls
- Error, retry, rollback, and unknown-outcome semantics
- Trust assumptions and defense-in-depth layers

Trace only the paths needed to confirm or reject the current risk hypothesis
Record inferred relationships and unsupported gaps explicitly

## Detect cross-cutting regressions

Search for comparable guards, validation patterns, and callsites when a selected change may violate a shared invariant

```bash
rg "<validation or access-control pattern>" <relevant paths>
git diff <base>..<head> -- <relevant paths>
```

Flag a regression only when the current change actually removes, bypasses, or contradicts the supported invariant

## Continue by risk

- For a supported high-risk path, read [adversarial analysis](adversarial.md)
- For a requested persistent artifact, read [reporting](reporting.md)
- Otherwise report the focused findings, coverage, confidence, and remaining uncertainty directly

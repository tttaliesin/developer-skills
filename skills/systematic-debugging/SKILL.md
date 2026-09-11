---
name: systematic-debugging
description: Diagnose bugs, failing tests, build or integration failures, performance regressions, and other unexpected technical behavior before implementing a fix.
---

# Systematic debugging

Find a supported root cause before changing behavior
Scale the investigation and verification to the uncertainty, impact, and evidence already available

## Preserve scope and evidence

- Apply investigation to the requested issue and preserve existing approval, credential, production, and review gates
- A diagnosis-only request does not authorize fixes, instrumentation, test execution with side effects, or file artifacts
- Reuse valid failure and verification evidence for the same code, inputs, and environment
- Preserve tracked, untracked, ignored, and user-owned work
- Never expose credentials, raw environment values, request bodies, or sensitive payloads while gathering evidence

## Choose the shortest sufficient route

| Route | Use when | Read |
| --- | --- | --- |
| Diagnosis only | The user asked for a cause or assessment without a fix | Inspect and report the supported cause, evidence, and remaining uncertainty, then stop before mutation |
| Short investigation | The failure is reliable, the affected boundary is narrow, and direct evidence supports one cause | Use the short path below |
| Deep investigation | The cause is unclear, intermittent, multi-component, security- or production-sensitive, or prior hypotheses failed | Read [deep investigation](references/deep-investigation.md) |

A small diff does not by itself justify the short route
Use it only when the evidence already narrows the cause and affected behavior

## Short investigation

1. Read the exact error, failing assertion, or observed mismatch and the directly relevant code or configuration
2. Check the recent change or input difference most likely to explain it
3. State one causal hypothesis and the evidence that distinguishes it from nearby alternatives
4. If a fix is authorized, apply the smallest change at the source of the behavior without unrelated refactoring
5. Verify the original symptom and the closest affected behavior

An existing failing test, command output, trace, or deterministic configuration check can be the pre-fix evidence
Create a new regression test when it materially protects the repaired behavior and the repository has an appropriate test surface
For configuration, generated files, or behavior without a suitable automated test, use the narrowest repeatable check that demonstrates the defect and fix
Do not ask for a process exception merely because a new test is not the right evidence

Read [failing reproduction](references/failing-test.md) when a new or adapted reproduction is needed

## Deep investigation

Use the detailed evidence and hypothesis workflow in [deep investigation](references/deep-investigation.md)
Load these techniques only when the failure shape requires them:

- Deep call stack or unclear bad-value origin — [root-cause tracing](root-cause-tracing.md)
- Timing, polling, or asynchronous readiness — [condition-based waiting](condition-based-waiting.md)
- Additional validation after the root cause is known — [defense in depth](defense-in-depth.md)

## Handle failed hypotheses

- Change one explanatory variable at a time
- After a failed fix or experiment, inspect what changed and form a new hypothesis before another mutation
- Do not repeat the same attempt without new evidence
- When repeated failures reveal shared state, coupling, or an architectural assumption, stop further mutation and discuss the architectural decision if it would change the requested scope or design
- Continue independent authorized read-only investigation while a decision is pending

## Verify and finish

Read [completion evidence](references/completion-evidence.md) before claiming a fix or passing checks

Verification should cover:

- The original symptom or contract violation
- The changed code and directly affected dependencies
- Relevant regression tests and applicable repository-required checks
- Any risk that remains unresolved after the fix

Broaden or repeat checks only when new changes, failures, invalidated evidence, or an applicable mandatory gate justify it
A passing unit test does not prove production health, and unavailable execution does not justify a success claim
If the evidence supports only an environmental, timing-dependent, or external cause, report that conclusion and its limits rather than inventing an application fix

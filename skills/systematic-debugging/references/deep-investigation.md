# Deep investigation

Use this route when the cause is uncertain, crosses components, appears intermittently, affects a sensitive environment, or remains unresolved after a focused hypothesis
It is an evidence guide, not a requirement to perform every activity for every failure

## Establish the observed failure

- Read the complete relevant error, warning, stack trace, and exit status
- Record the exact input, environment, and steps that produced the failure
- Reproduce when it will materially distinguish causes and the execution is authorized
- If reproduction is unavailable, identify the missing evidence and continue with static or historical evidence without guessing
- Check recent code, dependency, configuration, data, and environment changes that intersect the failure boundary

## Trace the failing boundary

For a multi-component path such as CI to build to signing or API to service to database:

1. Identify each boundary and its expected input and output
2. Compare the observed non-sensitive state at each boundary
3. Find the first boundary where expected and observed behavior diverge
4. Trace the bad value or missing effect back to its originating decision

Use existing logs and read-only diagnostics first
Add temporary instrumentation only when the task authorizes that mutation and existing evidence cannot answer the question
Log allowlisted presence, type, size, identifier class, timestamp, and error-code fields rather than secrets or raw payloads
Review output destinations and remove only task-owned temporary instrumentation after it is no longer needed

Read [root-cause tracing](../root-cause-tracing.md) when the failure appears deep in a call chain

## Compare the relevant pattern

- Find a working example in the same codebase or supported reference implementation
- Read the portions that define the behavior, assumptions, and interface being compared
- List differences that could explain the observed failure and prioritize them by causal relevance
- Confirm required dependencies, settings, environment, and trust assumptions

Do not load an entire unrelated implementation merely because it uses a similar library
Do not dismiss a small difference until the hypothesis explains why it cannot affect the result

## Test one hypothesis

State the hypothesis in a falsifiable form:

```text
Cause: X
Evidence: Y distinguishes X from the nearest alternative
Expected observation: Z if X is correct
```

Choose the smallest authorized observation or change that can confirm or reject it
Keep unrelated variables stable and inspect the result before continuing

- Confirmed hypothesis — proceed to the authorized source fix
- Rejected hypothesis — retain the new evidence and form another hypothesis
- Inconclusive result — narrow the missing observation instead of stacking fixes

## Recognize an architectural decision

Repeated failed fixes warrant architectural review when they reveal evidence such as:

- Shared state or coupling outside the assumed boundary
- A fix that requires changing several unrelated interfaces
- A local change that repeatedly creates a new failure elsewhere
- A platform or lifecycle assumption that the current design cannot satisfy

This evidence does not automatically prove that the architecture is wrong
Pause a scope-changing redesign for the user's decision while continuing safe investigation that may narrow the choice

## Prepare the fix and verification

- Reuse an existing failing case when it already demonstrates the target defect
- Otherwise read [failing reproduction](failing-test.md) and create the narrowest useful reproduction
- Implement one root-cause correction without opportunistic cleanup
- Read [completion evidence](completion-evidence.md) and verify the original symptom plus relevant regressions
- Report what was executed, what was inspected statically, and what remains unverified

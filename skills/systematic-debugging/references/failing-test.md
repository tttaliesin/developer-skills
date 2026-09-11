# Failing reproduction before a fix

Adapted from obra/superpowers test-driven-development and writing-good-tests (MIT).

Before implementing a bug fix, establish meaningful pre-fix evidence for the target defect.
Reuse an existing failing test, command, trace, or deterministic configuration check when it already demonstrates the wrong behavior; do not create a duplicate merely to satisfy a process step.
When durable regression coverage is useful and the repository has an appropriate test surface, add or adapt the simplest failing test.
Otherwise use a bounded reproduction or static contract comparison suited to the artifact and report why an automated test was not applicable or available.
Observe the target defect rather than a syntax error, unavailable service, or broken fixture.
Do not ask for a separate exception when the authorized task and available evidence already establish the appropriate verification route.

Derive expected results from the contract independently of the implementation.
Exercise real behavior and mock only side effects that cannot appropriately run in the test.
Name the wrong branch, missing effect, or contract violation each test catches.
Do not test exact instructional prose or private layout merely to detect change.

Make one root-cause fix and rerun the reproduction or equivalent defect check plus relevant regression checks.
For existing or shared work, never delete or revert user changes to manufacture a red phase.
If the fix already exists and available pre-fix evidence does not resolve the defect, establish the needed baseline in an authorized isolated fixture or temporary checkout while preserving the working tree.
A read-only diagnosis stops before mutations; explain the reproduction and missing execution evidence.

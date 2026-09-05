# Failing reproduction before a fix

Adapted from obra/superpowers test-driven-development and writing-good-tests (MIT).

Before implementing a bug fix, create the simplest meaningful failing reproduction.
Use the repository's test framework when available, or a one-off test script when it has none.
Observe failure for the target defect, not a syntax error, unavailable service, or broken fixture.
Keep this requirement even for an apparently obvious fix.
Exceptions, including throwaway prototypes, generated code, and configuration files, require the human partner's permission; this skill grants no exemption.
Do not ask again if an explicit applicable exception was already approved in this task.

Derive expected results from the contract independently of the implementation.
Exercise real behavior and mock only side effects that cannot appropriately run in the test.
Name the wrong branch, missing effect, or contract violation each test catches.
Do not test exact instructional prose or private layout merely to detect change.

Make one root-cause fix and rerun the reproduction plus relevant regression checks.
For existing or shared work, never delete or revert user changes to manufacture a red phase.
If the fix already exists, establish the failing baseline in an authorized isolated fixture or temporary checkout and preserve the working tree.
A read-only diagnosis stops before mutations; explain the reproduction and missing execution evidence.

# Asynchronous component contracts

## Establish the boundary

Identify the transport, topic or channel ownership, producers, consumers, and canonical schema before proposing changes.
Separate telemetry facts, domain events, and commands with execution side effects.
Document payload types, required/optional fields, nullability, units, timestamp origin and timezone, identifiers, correlation, and schema version.
Use the existing serialization and fixture stack; proposed examples are not an instruction to replace it.

## Delivery and outcomes

Specify duplication and ordering guarantees, acknowledgement meaning, expiry/freshness rules, retries, and error outcomes.
Broker acknowledgement means transport acceptance under that broker's contract; it does not prove physical execution.
For commands distinguish accepted, executed, failed, timed-out, and outcome-unknown.
Define which component owns each transition and what evidence supports it.
A timeout does not establish that execution failed; do not automatically retry a non-idempotent physical action when its outcome is unknown.
Define command identity, deduplication scope and retention, concurrent duplicate handling, and how a caller reconciles an unknown outcome.
Do not invent QoS, expiry, freshness, or operational retry limits: reuse existing decisions or leave explicit unresolved requirements for the project owner.
Designing this contract grants no authority to publish commands or test on live devices.

## Compatibility evidence

Build a producer-consumer table from actual components and schema versions.

| Producer/version | Consumer/version | Accepted payloads | Unknown fields/version | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| Actual producer | Actual consumer | Required/optional fields and units | Existing policy or unresolved | Defined rejection/result | Schema or test location |

Cover valid, invalid, duplicate, late, and out-of-order messages with concrete fixtures.
For Go and NestJS components, check the same serialized fixtures through both sides using their existing test tools.
Check omitted versus null values, numeric ranges/precision, enum additions, timestamp conversion, and forward/backward compatibility.
Record what was executed versus reviewed; schema agreement alone is not an end-to-end or live-device success claim.

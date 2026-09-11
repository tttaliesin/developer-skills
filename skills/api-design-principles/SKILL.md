---
name: api-design-principles
description: Design or review HTTP APIs and asynchronous message contracts between components, including compatibility, validation, idempotency, and command outcomes. Use for interface specifications and contract changes.
---

# API Design Principles

Start from the actual transport, producers, consumers, and existing contract source of truth. Keep
HTTP, GraphQL, and asynchronous message semantics distinct, and load only the reference for the
boundary under review.

## Establish the shared contract first

Before choosing a transport pattern:

- locate the canonical schema, handler, producer, consumer, generated client, and contract tests;
- identify who creates, validates, stores, retries, and observes each request or message;
- distinguish absent, malformed, unauthorized, duplicate, accepted, completed, failed, timed out,
  and outcome-unknown states where they matter;
- state compatibility rules for required and optional fields, defaults, enum growth, deprecation,
  version skew, and unknown fields;
- define validation at the boundary and authoritative business validation separately;
- define idempotency scope, key ownership, retention, concurrent duplicate behavior, replay response,
  and recovery from an unknown outcome when commands can be retried; and
- verify both producer and consumer behavior rather than editing a schema in isolation.

Preserve the repository language, schema format, validation libraries, error model, authentication
boundary, and test stack. Treat existing consumers and stored messages as compatibility evidence,
not merely current implementation detail.

## Route by transport

- **HTTP or REST:** read [REST best practices](references/rest-best-practices.md). Load
  [worked examples](references/details.md) only when concrete endpoint or implementation examples
  are useful. For a structured HTTP review, adapt
  [the API checklist](assets/api-design-checklist.md) to the repository.
- **GraphQL:** read [GraphQL schema design](references/graphql-schema-design.md). Do not import REST
  URL or status-code guidance into a GraphQL-only boundary.
- **Asynchronous event, telemetry, or command:** read
  [message contracts](references/message-contracts.md). Model delivery, ordering, deduplication,
  acknowledgement, observable outcomes, compatibility, and producer-consumer skew explicitly.
- **Mixed boundary:** load only the references for transports that actually cross the boundary and
  describe translation between their success, error, retry, and unknown-outcome semantics.

The [optional Python template](assets/rest-api-template.py) is illustrative. Use it only when Python
and its framework already fit the repository; examples do not authorize a stack change.

## Keep recommendations inside scope

Do not introduce a broker, GraphQL endpoint, schema registry, AsyncAPI dependency, framework, or
versioning scheme solely because a reference demonstrates one. Prefer existing project decisions
and flag unresolved compatibility or operational requirements.

This skill authorizes no live PLC command, broker mutation, deployment, credential access, or
production change. Preserve explicit approvals and production gates, and keep the final design or
review tied to observable producer and consumer behavior.

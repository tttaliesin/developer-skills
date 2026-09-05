---
name: api-design-principles
description: Design or review HTTP APIs and asynchronous message contracts between components, including compatibility, validation, idempotency, and command outcomes. Use for interface specifications and contract changes.
---

# API Design Principles

Start from the actual transport, producers, consumers, and existing contract source of truth.
Use REST rules only for REST interfaces and GraphQL rules only where GraphQL is used.
For asynchronous telemetry, events, and commands, read [message-contracts.md](references/message-contracts.md).
Keep HTTP and message semantics distinct when reviewing a boundary that uses both.

Preserve the repository language, schema format, validation libraries, and test stack.
Python and FastAPI examples are illustrative; do not introduce them into Go or NestJS solely to follow this skill.
Do not introduce a broker, GraphQL endpoint, schema registry, or AsyncAPI dependency solely because an example mentions one.
Use existing project decisions and flag unresolved compatibility or operational requirements.
This skill authorizes no live PLC commands, broker mutations, deployment, credential access, or expansion beyond the user's requested interface work.
Preserve all explicit approval and production gates.

## When to Use This Skill

- Designing HTTP APIs or asynchronous producer-consumer contracts
- Refactoring existing APIs for better usability
- Establishing API design standards for your team
- Reviewing API specifications before implementation
- Migrating between API paradigms (REST to GraphQL, etc.)
- Creating developer-friendly API documentation
- Optimizing APIs for specific use cases (mobile, third-party integrations)

## Core Concepts

### 1. RESTful Design Principles

**Resource-Oriented Architecture**

- Resources are nouns (users, orders, products), not verbs
- Use HTTP methods for actions (GET, POST, PUT, PATCH, DELETE)
- URLs represent resource hierarchies
- Consistent naming conventions

**HTTP Methods Semantics:**

- `GET`: Retrieve resources (idempotent, safe)
- `POST`: Process a resource-specific request, including creation or commands; define retry/idempotency semantics explicitly
- `PUT`: Replace entire resource (idempotent)
- `PATCH`: Partial resource updates
- `DELETE`: Remove resources (idempotent)

### 2. GraphQL Design Principles

**Schema-First Development**

- Types define your domain model
- Queries for reading data
- Mutations for modifying data
- Subscriptions for real-time updates

**Query Structure:**

- Clients request exactly what they need
- Single endpoint, multiple operations
- Strongly typed schema
- Introspection built-in

### 3. API Versioning Strategies

**URL Versioning:**

```
/api/v1/users
/api/v2/users
```

**Header Versioning:**

```
Accept: application/vnd.api+json; version=1
```

**Query Parameter Versioning:**

```
/api/users?version=1
```

## Detailed patterns and worked examples

For HTTP patterns, read [details.md](references/details.md) or [rest-best-practices.md](references/rest-best-practices.md).
For GraphQL schemas, read [graphql-schema-design.md](references/graphql-schema-design.md).
Use [api-design-checklist.md](assets/api-design-checklist.md) for HTTP reviews and adapt the optional Python template only when it matches the repository.

## Best Practices

### REST APIs

1. **Consistent Naming**: Use plural nouns for collections (`/users`, not `/user`)
2. **Stateless**: Each request contains all necessary information
3. **Use HTTP Status Codes Correctly**: 2xx success, 4xx client errors, 5xx server errors
4. **Version Your API**: Plan for breaking changes from day one
5. **Pagination**: Always paginate large collections
6. **Rate Limiting**: Protect your API with rate limits
7. **Documentation**: Use OpenAPI/Swagger for interactive docs

### GraphQL APIs

1. **Schema First**: Design schema before writing resolvers
2. **Avoid N+1**: Use DataLoaders for efficient data fetching
3. **Input Validation**: Validate at schema and resolver levels
4. **Error Handling**: Return structured errors in mutation payloads
5. **Pagination**: Use cursor-based pagination (Relay spec)
6. **Deprecation**: Use `@deprecated` directive for gradual migration
7. **Monitoring**: Track query complexity and execution time

## Common Pitfalls

- **Over-fetching/Under-fetching (REST)**: Fixed in GraphQL but requires DataLoaders
- **Breaking Changes**: Version APIs or use deprecation strategies
- **Inconsistent Error Formats**: Standardize error responses
- **Missing Rate Limits**: APIs without limits are vulnerable to abuse
- **Poor Documentation**: Undocumented APIs frustrate developers
- **Unspecified Retry Semantics**: POST can support an explicit idempotency contract; define key scope, retention, concurrency, duplicate responses, and unknown outcomes rather than redesigning an endpoint solely for idempotence
- **Tight Coupling**: API structure shouldn't mirror database schema

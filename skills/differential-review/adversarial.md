# Adversarial Vulnerability Analysis (Phase 5)

Structured methodology for finding vulnerabilities through attacker modeling.

**When to use:** After completing deep context analysis (Phase 4), apply this to all HIGH RISK changes.

---

## 1. Define Specific Attacker Model

**WHO is the attacker?**
- Unauthenticated external user
- Authenticated regular user
- Malicious administrator
- Compromised contract/service
- Front-runner/MEV bot

**WHAT access/privileges do they have?**
- Public API access only
- Authenticated user role
- Specific permissions/tokens
- Contract call capabilities

**WHERE do they interact with the system?**
- Specific HTTP endpoints
- Smart contract functions
- RPC interfaces
- External APIs

---

## 2. Identify Concrete Attack Vectors

```
ENTRY POINT: [Exact function/endpoint attacker can access]

ATTACK SEQUENCE:
1. [Specific API call/transaction with parameters]
2. [How this reaches the vulnerable code]
3. [What happens in the vulnerable code]
4. [Impact achieved]

PROOF OF ACCESSIBILITY:
- Show the function is public/external
- Demonstrate attacker has required permissions
- Prove attack path exists through actual interfaces
```

---

## 3. Rate Realistic Exploitability

**EASY:** Exploitable via public APIs with no special privileges
- Single transaction/call
- Common user access level
- No complex conditions required

**MEDIUM:** Requires specific conditions or elevated privileges
- Multiple steps or timing requirements
- Elevated but obtainable privileges
- Specific system state needed

**HARD:** Requires privileged access or rare conditions
- Admin/owner privileges needed
- Rare edge case conditions
- Significant resources required

---

## 4. Build Complete Exploit Scenario

```
ATTACKER STARTING POSITION:
[What the attacker has at the beginning]

STEP-BY-STEP EXPLOITATION:
Step 1: [Concrete action through accessible interface]
  - Command: [Exact call/request]
  - Parameters: [Specific values]
  - Expected result: [What happens]

Step 2: [Next action]
  - Command: [Exact call/request]
  - Why this works: [Reference to code change]
  - System state change: [What changed]

Step 3: [Final impact]
  - Result: [Concrete harm achieved]
  - Evidence: [How to verify impact]

CONCRETE IMPACT:
[Specific, measurable impact - not "could cause issues"]
- Exact amount of funds drained
- Specific privileges escalated
- Particular data exposed
```

---

## 5. Cross-Reference with Baseline Context

From baseline analysis (see [methodology.md](methodology.md#pre-analysis-baseline-context-building)), check:
- Does this violate a system-wide invariant?
- Does this break a trust boundary?
- Does this bypass a validation pattern?
- Is this a regression of a previous fix?

---

## Vulnerability Report Template

Generate this for each finding:

````markdown
## [SEVERITY] Vulnerability Title

**Attacker Model:**
- WHO: [Specific attacker type]
- ACCESS: [Exact privileges]
- INTERFACE: [Specific entry point]

**Attack Vector:**
[Step-by-step exploit through accessible interfaces]

**Exploitability:** EASY/MEDIUM/HARD
**Justification:** [Why this rating]

**Concrete Impact:**
[Specific, measurable harm - not theoretical]

**Proof of Concept:**
```code
// Exact code to reproduce
```

**Root Cause:**
[Reference specific code change at file.sol:L123]

**Blast Radius:** [N callers affected]
**Baseline Violation:** [Which invariant/pattern broken]
````

---

## Example: Distinguish changed behavior from demonstrated impact

**Change:** `require(amount > 0)` was removed from `withdraw()`.
Assume the supplied code shows only `withdrawnAmount[user] += amount` and an emitted `Withdraw` event after the check.

A public caller can now request `withdraw(0)` and emit a zero-value event.
Adding zero does not establish accounting corruption or a supply change.
Inspect downstream consumers and the historical reason for the check before claiming a security impact.
If an indexer grants a fixed reward for every event without validating amount, demonstrate that consumer path and its conditions before reporting reward abuse.
Without that evidence, report the changed invariant and unresolved downstream effect, not an invented exploit or financial loss.
Use actual file lines and commits when available; explicitly state unavailable evidence.

---

**Next:** Document all findings in final report (see [reporting.md](reporting.md))

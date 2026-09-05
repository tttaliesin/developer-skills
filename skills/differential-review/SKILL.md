---
name: differential-review
description: "Performs security-focused differential review of code changes. Adapts analysis depth to codebase size, uses git blame for context, calculates blast radius by counting callers, checks test coverage of modified code, and generates a markdown report. Use when reviewing a PR, commit, or diff for security vulnerabilities, checking whether a change re-introduces a previously fixed bug, asking what else a change could break, or finding which modified code has no test covering it."
allowed-tools: Read Write Grep Glob Bash
---

# Differential Security Review

Security-focused code review for PRs, commits, and diffs.

## Core Principles

1. **Risk-First**: Focus on auth, crypto, value transfer, external calls
2. **Evidence-Based**: Every finding backed by git history, line numbers, attack scenarios
3. **Adaptive**: Scale to codebase size (SMALL/MEDIUM/LARGE)
4. **Honest**: Explicitly state coverage limits and confidence level
5. **Output-Driven**: Generate a persistent Markdown report by default, subject to the output boundary below

---

## Scope and output boundary

Review the requested base/head or working-tree diff without changing branches, discarding work, or editing reviewed code.
Use `git show`, `git diff`, and `git blame` for baseline evidence.
Generate a persistent Markdown report in the authorized project location by default.
Honor an explicitly requested chat/other format, read-only scope, or write restriction instead; state when the file artifact was not written.
Do not substitute chat merely by preference when persistence is authorized and no different format was requested.
Never fall back to Desktop, skill installation directories, or another repository to bypass a write boundary.
Review output is repository evidence, not automatically canonical Vault knowledge; apply Second Brain capture separately when applicable.
Skill routing and optional delegation preserve existing scope and approvals; external issue creation or PR posting needs its own authorization.

Record unavailable history, line numbers, commits, execution, and caller evidence with a concrete reason rather than fabricating them or declaring full coverage.
Caller counts are a search aid; assess externally reachable users, records, tenants, and effects as well as code callers.
Review priority, vulnerability severity, and confidence are separate.
Missing tests increase investigation priority and constitute a verification gap; they do not alone establish a vulnerability or increase its severity.
Severity requires evidence of impact, reachability, and exploit conditions.

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "Small PR, quick review" | Heartbleed was 2 lines | Classify by RISK, not size |
| "I know this codebase" | Familiarity breeds blind spots | Build explicit baseline context |
| "Git history takes too long" | History reveals regressions | Never skip Phase 1 |
| "Blast radius is obvious" | You'll miss transitive callers | Calculate quantitatively |
| "No tests = not my problem" | Missing tests leave a verification gap | Flag the gap and prioritize investigation; rate severity from demonstrated impact |
| "Just a refactor, no security impact" | Refactors break invariants | Analyze as HIGH until proven LOW |
| "I'll explain verbally" | Persistent output is the default | Follow the scope and output boundary |

---

## Quick Reference

### Codebase Size Strategy

| Codebase Size | Strategy | Approach |
|---------------|----------|----------|
| SMALL (<20 files) | DEEP | Read all deps, full git blame |
| MEDIUM (20-200) | FOCUSED | 1-hop deps, priority files |
| LARGE (200+) | SURGICAL | Critical paths only |

### Risk Level Triggers

| Risk Level | Triggers |
|------------|----------|
| HIGH | Auth, crypto, external calls, value transfer, validation removal |
| MEDIUM | Business logic, state changes, new public APIs |
| LOW | Changes with no demonstrated security exposure; UI, logging, tests, and comments still require exposure checks for secrets, auth, encoding, and executable examples |

---

## Workflow Overview

```
Pre-Analysis → Phase 0: Triage → Phase 1: Code Analysis → Phase 2: Test Coverage
    ↓              ↓                    ↓                        ↓
Phase 3: Blast Radius → Phase 4: Deep Context → Phase 5: Adversarial → Phase 6: Report
```

---

## Decision Tree

**Starting a review?**

```
├─ Need detailed phase-by-phase methodology?
│  └─ Read: methodology.md
│     (Pre-Analysis + Phases 0-4: triage, code analysis, test coverage, blast radius)
│
├─ Analyzing HIGH RISK change?
│  ├─ Read: adversarial.md
│  │  (Phase 5: Attacker modeling, exploit scenarios, exploitability rating)
│  └─ Perform locally, or delegate only when the host and task permit it
│
├─ Writing the final report?
│  └─ Read: reporting.md
│     (Phase 6: Report structure, templates, formatting guidelines)
│
├─ Looking for specific vulnerability patterns?
│  └─ Read: patterns.md
│     (Regressions, reentrancy, access control, overflow, etc.)
│
└─ Quick triage only?
   └─ Use Quick Reference above, skip detailed docs
```

---

## Optional delegation

The local [adversarial.md](adversarial.md) method is sufficient without an installed companion agent.
When delegation is available and authorized, use the host's actual tool schema and give the agent the requested diff and bounded analysis scope.
Do not assume a `subagent_type` or namespaced agent exists.

---

## Quality Checklist

Before delivering:

- [ ] Changed files inventoried; analyzed, surface-scanned, and omitted scope explicitly identified
- [ ] Git blame on removed security code
- [ ] Blast radius calculated for HIGH risk
- [ ] Attack scenarios are concrete (not generic)
- [ ] Findings reference specific line numbers + commits when available; otherwise state the limitation
- [ ] Output delivered according to the scope and output boundary
- [ ] User notified with summary

---

## Integration

Use the baseline and deep-context procedures in [methodology.md](methodology.md).
An available context-building skill can assist but is not a required CLI executable.
Use [reporting.md](reporting.md) for a self-contained report; do not invoke an assumed issue-writer command or post findings externally without authorization.

---

## Example Usage

### Quick Triage (Small PR)
```
Input: 5 file PR, 2 HIGH RISK files
Strategy: Use Quick Reference
1. Classify risk level per file (2 HIGH, 3 LOW)
2. Focus on 2 HIGH files only
3. Git blame removed code
4. Generate minimal report
Time: ~30 minutes
```

### Standard Review (Medium Codebase)
```
Input: 80 files, 12 HIGH RISK changes
Strategy: FOCUSED (see methodology.md)
1. Full workflow on HIGH RISK files
2. Surface scan on MEDIUM
3. Skip LOW risk files
4. Complete report with all sections
Time: ~3-4 hours
```

### Deep Audit (Large, Critical Change)
```
Input: 450 files, auth system rewrite
Strategy: SURGICAL + local baseline analysis
1. Baseline context using methodology.md
2. Deep analysis on auth changes only
3. Blast radius analysis
4. Adversarial modeling
5. Comprehensive report
Time: ~6-8 hours
```

---

## When NOT to Use This Skill

- **Greenfield code** (no baseline to compare)
- **Documentation-only changes** (no security impact)
- **Formatting/linting** (cosmetic changes)
- **User explicitly requests quick summary only** (they accept risk)

For these cases, use standard code review instead.

---

## Red Flags (Stop and Investigate)

**Immediate escalation triggers:**
- Removed code from "security", "CVE", or "fix" commits
- Access control modifiers removed (onlyOwner, internal → external)
- Validation removed without replacement
- External calls added without checks
- High blast radius (50+ callers) + HIGH risk change

These patterns require adversarial analysis even in quick triage.

---

## Tips for Best Results

**Do:**
- Start with git blame for removed code
- Calculate blast radius early to prioritize
- Generate concrete attack scenarios
- Reference specific line numbers and commits
- Be honest about coverage limitations
- Generate the default report file when authorized; honor explicit output restrictions

**Don't:**
- Skip git history analysis
- Make generic findings without evidence
- Claim full analysis when time-limited
- Forget to check test coverage
- Miss high blast radius changes
- Choose chat-only output without an explicit format request or write restriction

---

## Supporting Documentation

- **[methodology.md](methodology.md)** - Detailed phase-by-phase workflow (Phases 0-4)
- **[adversarial.md](adversarial.md)** - Attacker modeling and exploit scenarios (Phase 5)
- **[reporting.md](reporting.md)** - Report structure and formatting (Phase 6)
- **[patterns.md](patterns.md)** - Common vulnerability patterns reference

---

**For first-time users:** Start with [methodology.md](methodology.md) to understand the complete workflow.

**For experienced users:** Use this page's Quick Reference and Decision Tree to navigate directly to needed content.

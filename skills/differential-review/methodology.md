# Differential Review Methodology

Detailed phase-by-phase workflow for security-focused code review.

## Pre-Analysis: Baseline Context Building

**FIRST ACTION - Build complete baseline understanding:**

Read baseline files with `git show <base>:<path>` and history with `git blame <base> -- <path>`.
Do not checkout the baseline in the user's working tree.
Use the following questions directly; an available context-building skill is optional and is not an assumed shell command.

**Capture from baseline analysis:**
- System-wide invariants (what must ALWAYS be true across all code)
- Trust boundaries and privilege levels (who can do what)
- Validation patterns (what gets checked where - defense-in-depth)
- Complete call graphs for critical functions (who calls what)
- State flow diagrams (how state changes)
- External dependencies and trust assumptions

**Why this matters:**
- Understand what the code was SUPPOSED to do before changes
- Identify implicit security assumptions in baseline
- Detect when changes violate baseline invariants
- Know which patterns are system-wide vs local
- Catch when changes break defense-in-depth

**Store baseline context for reference during differential analysis.**

Read head files with `git show <head>:<path>` or inspect the requested working-tree diff without changing repository state.

---

## Phase 0: Intake & Triage

**Extract changes:**
```bash
# For commit range
git diff <base>..<head> --stat
git log <base>..<head> --oneline

# For PR
gh pr view <number> --json files,additions,deletions

# Get all changed files
git diff <base>..<head> --name-only
```

**Assess codebase size:**
```bash
find . -name "*.sol" -o -name "*.rs" -o -name "*.go" -o -name "*.ts" | wc -l
```

**Classify complexity:**
- **SMALL**: <20 files → Deep analysis (read all deps)
- **MEDIUM**: 20-200 files → Focused analysis (1-hop deps)
- **LARGE**: 200+ files → Surgical (critical paths only)

**Risk score each file:**
- **HIGH**: Auth, crypto, external calls, value transfer, validation removal
- **MEDIUM**: Business logic, state changes, new public APIs
- **LOW**: No security exposure identified after checking actual behavior; UI, logs, tests, and comments are not automatically low risk.

---

## Phase 1: Changed Code Analysis

For each changed file:

1. **Read both versions** (baseline and changed)

2. **Analyze each diff region:**
   ```
   BEFORE: [exact code]
   AFTER: [exact code]
   CHANGE: [behavioral impact]
   SECURITY: [implications]
   ```

3. **Git blame removed code:**
   ```bash
   # When was it added? Why?
   git log -S "removed_code" --all --oneline
   git blame <baseline> -- file.sol | grep "pattern"
   ```

   **Red flags:**
   - Removed code from "fix", "security", "CVE" commits → investigate prior invariant and exploitability urgently
   - Recently added (<1 month) then removed → prioritize regression analysis; age alone is not severity

4. **Check for regressions (re-added code):**
   ```bash
   git log -S "added_code" --all -p
   ```

   Pattern: Code added → removed for security → re-added now = REGRESSION

5. **Micro-adversarial analysis** for each change:
   - What attack did removed code prevent?
   - What new surface does new code expose?
   - Can modified logic be bypassed?
   - Are checks weaker? Edge cases covered?

6. **Generate concrete attack scenarios:**
   ```
   SCENARIO: [attack goal]
   PRECONDITIONS: [required state]
   STEPS:
     1. [specific action]
     2. [expected outcome]
     3. [exploitation]
   WHY IT WORKS: [reference code change]
   IMPACT: [severity + scope]
   ```

---

## Phase 2: Test Coverage Analysis

**Identify coverage gaps:**
```bash
# Production code changes (exclude tests)
git diff <range> --name-only | grep -v "test"

# Test changes
git diff <range> --name-only | grep "test"

# For each changed function, search for tests
grep -r "test.*functionName" test/ --include="*.sol" --include="*.js"
```

**Verification gaps and review priority:**
- New functions without relevant tests warrant more investigation.
- Changed validation with unchanged tests requires checking whether existing cases still cover the invariant.
- Complex untested logic warrants deeper analysis.
These are coverage gaps, not automatic vulnerability severity upgrades.
A matching test name does not prove coverage; inspect assertions and report execution separately.

---

## Phase 3: Blast Radius Analysis

**Calculate impact:**
```bash
# Count callers for each modified function
grep -r "functionName(" --include="*.sol" . | wc -l
```

These counts are review-priority heuristics, not measured affected users or vulnerability severity.
Public endpoint exposure, transitive effects, and tenant/data scope can dominate even with one code caller.
Use symbol-aware tracing where available and label text-match counts as approximate.

**Classify caller-count breadth:**
- 1-5 calls: LOW
- 6-20 calls: MEDIUM
- 21-50 calls: HIGH
- 51+ calls: CRITICAL

**Priority matrix:**

| Change Risk | Blast Radius | Priority | Analysis Depth |
|-------------|--------------|----------|----------------|
| HIGH | CRITICAL | P0 | Deep + all deps |
| HIGH | HIGH/MEDIUM | P1 | Deep |
| HIGH | LOW | P2 | Standard |
| MEDIUM | CRITICAL/HIGH | P1 | Standard + callers |

---

## Phase 4: Deep Context Analysis

Use these questions for each high-priority changed function:

1. **Map complete function flow:**
   - Entry conditions (preconditions, requires, modifiers)
   - State reads (which variables accessed)
   - State writes (which variables modified)
   - External calls (to contracts, APIs, system)
   - Return values and side effects

2. **Trace internal calls:**
   - List all functions called
   - Recursively map their flows
   - Build complete call graph

3. **Trace external calls:**
   - Identify trust boundaries crossed
   - List assumptions about external behavior
   - Check for reentrancy risks

4. **Identify invariants:**
   - What must ALWAYS be true?
   - What must NEVER happen?
   - Are invariants maintained after changes?

5. **Five Whys root cause:**
   - WHY was this code changed?
   - WHY did the original code exist?
   - WHY might this break?
   - WHY is this approach chosen?
   - WHY could this fail in production?

Perform the line-by-line analysis using available read/search tools and code tracing.

**Cross-cutting pattern detection:**
```bash
# Find repeated validation patterns
grep -r "require.*amount > 0" --include="*.sol" .
grep -r "onlyOwner" --include="*.sol" .

# Check if any removed in diff
git diff <range> | grep "^-.*require.*amount > 0"
```

**Flag if removal breaks defense-in-depth.**

---

**Next steps:**
- For HIGH RISK changes, proceed to [adversarial.md](adversarial.md)
- For report generation, see [reporting.md](reporting.md)

# Applied changes — 2026-09-05

The user approved implementing and globally installing the first four researched skills for Codex and Pi.
This local repository records that implementation; no remote repository creation or publication is part of this change.
GitHub Issue tracking has no established remote target for this new local package repository, so the acceptance and validation record stays here.

## Preserved authority and excluded expansions

Explicit user approval, required review, production gates, credential boundaries, and unrelated working state remain protected.
Debugging still requires a meaningful failing reproduction before a fix; exemptions still require user permission.
After three failed fixes, the fourth fix remains paused until architectural discussion with the user.
Differential review still produces a persistent report by default when authorized; chat-only output is reserved for explicit format requests or write restrictions, not agent preference.
Existing differential-review UI metadata and invocation policy were preserved byte-for-byte.
HTTP plus asynchronous-contract activation is broader subject coverage approved in this task, not authority to mutate brokers, PLCs, or deployments.
No optional expansion of agent discretion was applied.

## Package changes

### Systematic debugging

Replace raw environment/credential logging and operational signing examples with allowlisted non-sensitive presence evidence.
Use existing diagnostics before authorized instrumentation and preserve read-only diagnosis.
Bundle failing-test and completion-evidence guidance instead of assuming unavailable Superpowers skill invocations.
Retain upstream test/creation documents only in the snapshot; remove the npm-specific polluter helper from installation because suppressed failures and existing-state handling cannot prove clean tests.
Keep repository runner output and exit status intact and preserve unrelated changes during regression reproduction.
Correct claims that three failures prove architectural failure and the tracing diagram's contradictory symptom-fix branch.

### API design principles

Add actual transport/source-of-truth selection and asynchronous schemas, units, timestamps, identifiers, duplication, ordering, freshness, and explicit command states.
Require compatibility fixtures across actual producers/consumers, using existing language and schema tooling.
Preserve unresolved QoS and operational decisions rather than inventing values.
Distinguish broker acknowledgement from execution and unknown timeout outcome from failure.
Correct POST idempotency and status-code guidance without imposing endpoint or framework redesign.

### Differential review

Keep persistent reports as the default while respecting explicit read-only and output restrictions.
Remove Desktop/global-install fallback paths and working-tree baseline checkouts.
Replace assumed companion-agent/CLI calls with local methodology and host-permitted delegation.
Separate test gaps, review priority, confidence, and demonstrated vulnerability severity.
Inspect UI/logging exposure and report actual analyzed coverage and unavailable evidence.
Correct the zero-withdrawal example's unsupported accounting loss claim and clarify caller counts as heuristics rather than exposed-user counts.

### Web application testing

Use the selected interactive browser and existing repository E2E stack.
Use bounded observable readiness rather than mandatory networkidle, fixed sleeps, Python, or headless Chromium.
Review helpers before first use or after changes; reuse known reviewed helpers without ritual rereading.
The upstream server helper is retained only as evidence: shell-only termination, undrained output pipes, and port-only readiness do not establish safe ownership/cleanup.
Omit its dependent Python examples rather than distributing a second lifecycle implementation.
Preserve existing servers, user browser sessions, login/permission state, and artifact write boundaries.

# Validation — 2026-09-05

## Structural and reproducibility checks

All four skill packages pass skill-creator quick_validate.py.
The local validator verifies every preserved upstream file hash and reconstructs all customized package bytes by applying the recorded patch to an isolated copy of the pinned source.
Negative checks in disposable copies confirmed rejection of both unrecorded package edits and altered upstream snapshots.
The Markdown checker covers maintained package documents and repository documentation; unchanged upstream evidence is not normalized.

## Independent behavioral evaluation

Two independent agents evaluated the staged instructions without the intended customization answers and performed read-only scenario simulations.

| Scenario | Observed outcome |
| --- | --- |
| Read-only security review with removed ownership check and credential logging | Chat findings, no file writes/checkouts, evidence-based impact, test/history limitations stated |
| Signed-in Firefox dashboard with SSE and disabled command button | Existing session retained; bounded visible-state readiness proposed, no new server/framework, permission state distinguished |
| Three failed identity-propagation fixes | Fourth fix paused for user architectural discussion; non-sensitive read-only investigation continued |
| Go/NestJS telemetry units/timestamps and MQTT command acknowledgements | Compatibility correction, acknowledgement/execution separation, unknown-outcome handling, unresolved QoS/freshness preserved |
| Standard authorized report with no format preference | Persistent report selected in the authorized path, without redundant permission request |
| First fix without a test framework | One-off failing reproduction accepted without inventing a failing-test exemption |

Evaluation exposed residual upstream contradictions in the zero-withdrawal example, caller-count heuristics, debugging architecture claims, tracing diagram, and output capture.
These were corrected and the evaluating agents rechecked the affected guidance.
Nested report-template fences were also repaired during structural validation.

## Limits

These are simulated instruction-consumer checks, not live PLC, broker, production, or browser integration tests.
No operational service or credentials were exercised.
Existing illustrative API code and waiting examples were not installed as a new dependency stack or claimed to have passed application tests.
Final installation checks compare all package files and provenance for Codex and Pi; discovery metadata does not prove an actual invocation in a newly loaded host session.

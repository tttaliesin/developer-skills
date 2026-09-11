# Completion evidence

Adapted from obra/superpowers verification-before-completion (MIT).

Before claiming a fix or passing checks, inspect recorded verification evidence for the final relevant code, inputs, and environment, including the command, complete output, and exit status.
Report the result and practical scope it proves.
Reuse that evidence while it remains valid; run affected verification when changes, failures, invalidated evidence, or an applicable mandatory gate require a fresh run.
Missing or incomplete execution evidence requires running the relevant verification; an agent summary alone is not execution evidence.
A lint pass does not prove a build, and a passing test does not prove production health.
Verify the original symptom and relevant regressions.
Preserve recorded failing-then-passing evidence; rerun affected checks when changes invalidate it for the relevant code, inputs, or environment.
Do not revert unrelated work to demonstrate a regression.
If execution is unavailable or prohibited, report that limitation rather than claiming success.

# Completion evidence

Adapted from obra/superpowers verification-before-completion (MIT).

Before claiming a fix or passing checks, identify and run the relevant verification command against the final changed state.
Read its complete output and exit status; report the result and practical scope it proves.
A lint pass does not prove a build, a passing test does not prove production health, and an agent summary is not independent verification.
Verify the original symptom and relevant regressions.
Preserve recorded failing-then-passing evidence; if changed bytes invalidate it, rerun affected checks.
Do not revert unrelated work to demonstrate a regression.
If execution is unavailable or prohibited, report that limitation rather than claiming success.

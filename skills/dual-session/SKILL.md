---
name: dual-session
description: "Coordinate two persistent Codex tasks for planning/review and implementation/execution. Use for 듀얼 세션, 설계와 실행 분리, Astra/Sol role splitting, or continuing an explicitly paired team. Reuse the existing executor and let the user interact with either task. Do not activate merely because a project has other tasks or the user asks about subagents."
---

# Dual session

Use two persistent, user-visible tasks with separate conversation histories and stable roles.
Keep reusable rules in this global skill and team state outside the project; do not create or modify project `AGENTS.md` for this workflow.
Read [the operating rules](references/operation.md) when starting, resuming, or receiving work for a paired team.
Keep a verified pair linked while it is idle: `job: null` means ready for later work, not paused.
Treat stopping a job, disconnecting the pair, and archiving both tasks as separate user actions under the operating rules.

Activate from a natural-language request such as “듀얼 세션으로 하자” or an explicit `$dual-session` invocation.
An incoming team message should name this skill so the receiver can load it independently.
Installation alone does not create tasks or activate a team.
Implicit skill selection is contextual, not an always-running hook.

Keep existing model and reasoning settings when reusing tasks.
When creating a new Sol executor for the Astra/Sol arrangement, use `gpt-5.6-sol` with `xhigh` reasoning unless the user specifies a different model or reasoning level; do not impose these defaults on other teams.
Use the available Codex app task tools, not ephemeral subagents, for this workflow.
For ordinary implementation, continue through executor verification, planner review, authorized local integration, and final-location verification in the same job; prepare the next job from the latest integrated revision.
Follow the operating rules for review/experiment-only exceptions and remote authorization without asking again at routine handoffs.

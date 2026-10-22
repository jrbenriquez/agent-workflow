---
name: orchestrate-work
description: Drive and resume a human-defined software outcome through bounded implementation, verification, and recalibration until complete or blocked.
---

# Orchestrate Work

## Required references
Read [Handoff contracts](references/HANDOFFS.md) for phase result formats and
[Outcome state](references/WORK-STATE.md) for the persistent schema, transition
table, attempt accounting, stopping conditions, and resume rules. The state
policy gates handoff recommendations; a recommendation cannot bypass a limit.

## Inputs
- An authoritative outcome document with acceptance criteria and constraints.
- Existing project-owned outcome state and referenced handoffs/evidence, if any.
- Maximum implementation attempts, default 3 for a new outcome.
- Optional project capabilities registry at `.agents/capabilities/CAPABILITIES.md`.

## Procedure
1. Read the outcome and preserve its criteria. Resolve material ambiguity with
   the human rather than inventing requirements.
2. Validate or initialize project-owned state using the state reference. Check
   outcome identity, workspace, evidence freshness, and saved progress before
   choosing an action. Missing or invalid history never resets the attempt budget.
3. Resume the saved invocation or consume its completed handoff when safe.
   Continue from the next unfinished step; block if recovery cannot be justified.
4. For new implementation, select unmet criteria or a cohesive group, enforce
   the saved attempt limit, and persist the increment before invoking `implement`.
5. Save and validate each handoff, then checkpoint its consumption and next
   action. Use independent `verify` results for criterion verdicts. Reconsider
   prior passes when subsequent changes could invalidate their evidence.
6. Route FAIL or INCONCLUSIVE verification through `recalibrate` before another
   implementation. Follow its scoped adjustment or diagnostic action subject to
   the state rules, budget, and no-progress stopping condition.
7. Stop at `blocked` for exhausted attempts requiring more implementation,
   unresolved impediments, conflicting requirements, or unsafe recovery. Save
   concrete blockers and the action or human decision needed to resume.
8. Complete only when every required criterion has current evidence-backed PASS.
   Save `phase: complete` and provide a concise report linking evidence. On resume,
   retain completion only while its outcome and evidence remain applicable.

## Guardrails
- Keep runtime state and artifacts in the consuming project, suggested
  `.agents/work/<outcome-id>/`, outside reusable skills and capability definitions.
- Never silently change acceptance criteria, reset attempts, or raise the budget.
- Preserve unrelated changes and previously working behavior.
- Treat project capabilities as optional; disclose gaps when using native tools.
- Single-agent execution is the baseline. One orchestrator owns state writes;
  concurrent execution requires coordination beyond this version.

---
name: recalibrate
description: Diagnose failed or inconclusive verification and produce a bounded high-level adjustment plan before retrying implementation.
---

# Recalibrate

## Inputs
- Original outcome and constraints.
- Previous implementation summary.
- Verification evidence and failed/inconclusive criteria.
- Prior attempts and adjustment plans.

## Procedure
1. Identify exactly which criteria failed or remain unverified.
2. Separate observed facts from hypotheses about root cause.
3. Determine whether the issue is implementation, assumption, environment, dependency, or verification coverage.
4. If evidence is insufficient, request targeted diagnostics instead of speculative changes.
5. Propose the smallest high-level adjustment that addresses the likely cause.
6. State what already-working behavior must be preserved and what to reverify.
7. Flag repeated non-progress, conflicting requirements, or risks that warrant human escalation.

## Output
- Failure summary and evidence references.
- Root-cause assessment with uncertainty where relevant.
- Scoped adjustment plan (not code).
- Preservation constraints and reverification plan.
- Decision: `REIMPLEMENT`, `GATHER_EVIDENCE`, or `ESCALATE`.

Never silently change acceptance criteria or implement code during recalibration.

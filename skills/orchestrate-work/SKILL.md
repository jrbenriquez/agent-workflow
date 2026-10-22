---
name: orchestrate-work
description: Drive a human-defined software outcome through implementation, verification, and recalibration until verified or blocked.
---

# Orchestrate Work

## Inputs
- An outcome document with acceptance criteria and constraints.
- Optional project capabilities registry at `.agents/capabilities/CAPABILITIES.md`.

## Contract
1. Read the outcome document and preserve its original acceptance criteria.
2. Resolve material ambiguity with the human rather than inventing requirements.
3. Record the current status of each criterion, attempts, evidence references, and blockers in project-owned work state (suggested `.agents/work/<outcome-id>/`).
4. Select an unmet criterion or cohesive group of criteria and invoke the `implement` skill.
5. Invoke the `verify` skill on the resulting changes. Do not self-certify based on implementation claims.
6. If verification fails or is inconclusive, invoke `recalibrate` before another implementation attempt. If it requests diagnostics, gather them and verify again.
7. Repeat with bounded attempts. Escalate when evidence is unavailable, requirements conflict, or repeated attempts do not make progress.
8. Mark complete only when all required criteria are verified with evidence. Provide a concise report with links or paths to evidence.

## State transitions
`pending → implementing → verifying → verified | recalibrating | blocked`

After recalibration: `recalibrating → implementing | verifying | blocked`.

## Guardrails
- Never rewrite acceptance criteria to manufacture a pass.
- Avoid unrelated changes; preserve previously verified behavior.
- Treat project capabilities as optional. If missing, use available native tools and disclose coverage gaps.
- Single-agent execution is the baseline. For parallel workers, isolate branches/worktrees and run integration verification on the combined state.

---
name: implement
description: Make scoped software changes to satisfy a specific outcome or documented recalibration plan.
---

# Implement

## Inputs
- Assigned outcome and acceptance criteria.
- Constraints and any recalibration plan.
- Current repository state.

## Procedure
1. Inspect relevant code, tests, repository instructions, and optional `.agents/capabilities/CAPABILITIES.md`.
2. Confirm the current branch and repository state; do not discard unrelated changes.
3. Plan the smallest coherent change that satisfies the assigned criteria.
4. Implement and add or update appropriate tests.
5. Run fast, relevant checks available in the environment.
6. Report changed files, rationale, checks run, known gaps, and any assumptions to the orchestrator.

## Boundaries
- Do not alter the outcome's acceptance criteria.
- Do not declare the outcome verified; hand off to `verify`.
- Follow project-specific instructions when present; capabilities are optional.

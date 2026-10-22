# Agent Workflow

A project-agnostic, outcome-driven software development workflow.

**Core loop:** Outcome → Implement → Verify → Recalibrate (if needed) → Repeat until verified or blocked.

## Skills

- `to-outcomes`: Splits a PRD into verifiable outcomes, dependencies, and a coverage index.
- `orchestrate-work`: Owns outcome state, phase transitions, and completion decisions.
- `implement`: Executes a scoped implementation plan.
- `verify`: Assesses acceptance criteria using reproducible evidence.
- `recalibrate`: Diagnoses failed or inconclusive verification and plans the next attempt.

Shared [handoff contracts and examples](docs/HANDOFFS.md) define phase results
and orchestration decisions. [Outcome state and resume rules](docs/WORK-STATE.md)
define project-local checkpoints and a default limit of three implementation attempts.

## Project capabilities

Optional project-owned capabilities live in `.agents/capabilities/CAPABILITIES.md` in consuming repositories. Skills should read the registry if present and proceed with available native tools if absent. A project-specific skill (such as `be-control`) remains owned by that project.

## Installation

Publish this repository to GitHub, tag releases (for example `v0.1.0`), then install the four core skills and optionally `to-outcomes` using an Agent Skills-compatible manager. See [distribution guidance](docs/DISTRIBUTION.md). Check the current CLI documentation for exact commands and flags.

## Project setup

1. Install the core skills in your project's supported skill directory.
2. Optionally copy `templates/CAPABILITIES.md` to `.agents/capabilities/CAPABILITIES.md` and edit it.
3. Create an outcome document from `templates/outcome.md`, or invoke `to-outcomes` with a PRD to generate outcome files and a coverage index inside `outcomes/<general-outcome-name>/`.
4. Invoke `orchestrate-work` with the path to a ready outcome document. For multiple outcomes, follow their dependency order and verify prerequisites before each invocation.

Example: `Use to-outcomes to split docs/product-prd.md. Name the general outcome "Katagawa Website".`
This produces `outcomes/katagawa-website/README.md` and the outcome documents in that folder. Each set has its own folder; the skill asks for the general outcome name when it is missing.
The planning skill writes outcome documents; it does not initialize runtime state or automatically execute the resulting queue.

## Principles

- The human-owned outcome is authoritative; agents cannot silently weaken acceptance criteria.
- Verification is evidence-based; an assertion of success is not proof.
- Failure triggers diagnosis and scoped adjustment, not blind retry.
- Outcome phases are `implement`, `verify`, `recalibrate`, `complete`, or `blocked`.
  Criterion verdicts distinguish PASS, FAIL, and INCONCLUSIVE; missing evidence cannot establish completion.
- Work state and evidence belong to the consuming project, not the upstream skill distribution.
- For multi-agent use, isolate work and reverify after integration. Initial implementation targets one agent.

## Smoke test

See the [CSV export sample](examples/csv-export/README.md) for deterministic
contract/state tests, an agent-driven procedure, and recorded execution results.

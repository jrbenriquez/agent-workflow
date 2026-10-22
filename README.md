# Agent Workflow

A project-agnostic, outcome-driven software development workflow.

**Core loop:** Outcome → Implement → Verify → Recalibrate (if needed) → Repeat until verified or blocked.

## Skills

- `orchestrate-work`: Owns outcome state, phase transitions, and completion decisions.
- `implement`: Executes a scoped implementation plan.
- `verify`: Assesses acceptance criteria using reproducible evidence.
- `recalibrate`: Diagnoses failed or inconclusive verification and plans the next attempt.

## Project capabilities

Optional project-owned capabilities live in `.agents/capabilities/CAPABILITIES.md` in consuming repositories. Skills should read the registry if present and proceed with available native tools if absent. A project-specific skill (such as `be-control`) remains owned by that project.

## Installation

Publish this repository to GitHub, tag releases (for example `v0.1.0`), then install the four skills using an Agent Skills-compatible manager. See [distribution guidance](docs/DISTRIBUTION.md). Check the current CLI documentation for exact commands and flags.

## Project setup

1. Install the core skills in your project's supported skill directory.
2. Optionally copy `templates/CAPABILITIES.md` to `.agents/capabilities/CAPABILITIES.md` and edit it.
3. Create an outcome document from `templates/outcome.md`.
4. Invoke `orchestrate-work` with the path to the outcome document.

## Principles

- The human-owned outcome is authoritative; agents cannot silently weaken acceptance criteria.
- Verification is evidence-based; an assertion of success is not proof.
- Failure triggers diagnosis and scoped adjustment, not blind retry.
- Outcomes can be `verified`, `blocked`, or `inconclusive`; never claim success when necessary evidence is missing.
- Work state and evidence belong to the consuming project, not the upstream skill distribution.
- For multi-agent use, isolate work and reverify after integration. Initial implementation targets one agent.

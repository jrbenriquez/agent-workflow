# Agent Workflow

Turn a software requirement into working, verified software using five reusable
agent skills. Start with a PRD or one outcome; the agent implements it, verifies
its acceptance criteria, and diagnoses failures before trying again.

**PRD → Outcomes → Implement → Verify → Recalibrate → Verified or Blocked**

Progress, evidence and handoffs are saved in your repository so another chat can
resume from the next unfinished phase. Each outcome has a default budget of three
implementation attempts. The workflow never silently weakens acceptance criteria
or resets that budget.

## Get started in your repository

You need Git and an agent supporting Agent Skills. Choose either installer below:
Node.js/npm for `npx skills`, or a GitHub CLI version with `gh skill install`
(currently a preview command). No npm package for Agent Workflow is required.

**Option 1: install with npx.** Run this in your project repository:

```sh
cd /path/to/your-project
npx skills add jrbenriquez/agent-workflow
```

Follow the prompts to select skills and agents. To select every skill for Codex:

```sh
npx skills add jrbenriquez/agent-workflow --skill '*' --agent codex
```

Replace `codex` with `claude-code`, `cursor` or another supported agent. Installation
is project-local by default; add `--global` for user scope. Use `--copy` if you
prefer copies over the installer's default symlinks. See the
[Skills CLI reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)
for available agents and options. These commands follow the upstream source; use
the GitHub CLI release-pinning option below for the documented fixed-release setup.

**Option 2: use the interactive GitHub CLI installer.** Run this in your project repository:

```sh
cd /path/to/your-project
gh skill install jrbenriquez/agent-workflow --agent codex --scope project
```

Follow the prompts to choose skills. Install `to-outcomes`, `orchestrate-work`,
`implement`, `verify` and `recalibrate` for the full workflow. The command opens
skill selection; omitting the skill name does not automatically install all five.
Use the loop below if you want all five installed without selecting each one.

Choose your agent by replacing `codex` with the appropriate value:

| Agent | `--agent` value |
| --- | --- |
| Codex | `codex` |
| Claude Code | `claude-code` |
| GitHub Copilot | `github-copilot` |
| Cursor | `cursor` |
| Gemini CLI | `gemini-cli` |
| Antigravity | `antigravity` |
| Cline | `cline` |
| OpenCode | `opencode` |
| Windsurf | `windsurf` |
| Amp | `amp` |

For example, install for Claude Code with:

```sh
gh skill install jrbenriquez/agent-workflow --agent claude-code --scope project
```

Run `gh skill install --help` for the full list of supported agents. You can also
omit `--agent` to choose it interactively. Project scope keeps the installation in
this repository; `--scope user` makes it available across your projects.
For Codex, project skills are copied into `.agents/skills/`; other agents may use
a different directory. Installing skills does not start implementation.

**Alternative: install all five at a fixed release.** This loop targets Codex;
replace `codex` for another agent:

```sh
for skill in to-outcomes orchestrate-work implement verify recalibrate; do
  gh skill install jrbenriquez/agent-workflow "$skill" \
    --pin v0.1.0 --agent codex --scope project
done
```

This requires the `v0.1.0` tag to have been published. The interactive command can
also take `--pin v0.1.0` when you want skill selection at that fixed release.

Open a new agent chat in that repository and provide your PRD:

```text
Use to-outcomes to split docs/product-prd.md.
Name the general outcome "My Website".
```

The skill writes `outcomes/my-website/README.md` plus one document per outcome in
that folder. The index records dependencies, PRD coverage and unresolved blockers.
Each outcome has observable acceptance criteria and verification requirements.
Different projects or features can have separate folders under `outcomes/`.

Review the generated documents and resolve blockers, then execute the first ready
outcome using its actual file path:

```text
Use orchestrate-work to execute outcomes/my-website/my-website-story.md.
Continue until verified completion or Blocked.
```

Run subsequent outcomes in dependency order. The workflow handles one outcome at
a time; the index does not automatically schedule the whole project. For a small
change, skip PRD splitting and write one outcome using [the template](templates/outcome.md).

To continue in a new chat, provide the saved state path:

```text
Use orchestrate-work to resume from .agents/work/my-website-story/state.yaml.
Validate the outcome, workspace and saved evidence. Preserve the attempt count
and retry limit; continue until verified completion or Blocked.
```

Keep outcome documents and `.agents/work/<outcome-id>/` state, handoffs and evidence
available to the next session. A blocked outcome records what is needed to resume.

## Keep your installed skills updated

Use the same installer you used originally. For skills installed with `npx skills`:

```sh
npx skills check
npx skills update to-outcomes orchestrate-work implement verify recalibrate
```

Review local edits before applying updates. Keep the generated `skills-lock.json`
with your project when present. The commands below apply to GitHub CLI installs.

Upstream changes do not automatically change the copies in your project. A pinned
release stays fixed, and `gh skill update` skips pinned skills.

For a controlled upgrade, review the upstream changes, choose a published release,
and rerun the installation loop above with the new tag (for example, `v0.2.0`).
Review any overwrite prompts and local skill edits, then review and commit the
updated skill files in your project's agent-specific directory. Upgrade all five skills together.
Application code, outcome documents and runtime state remain project-owned;
follow any migration instructions if a release changes the state schema.

If you prefer unpinned updates, from your project run:

```sh
gh skill update to-outcomes orchestrate-work implement verify recalibrate --unpin
```

This removes the release pins and updates the selected skills interactively. For
later checks, use the same command without `--unpin`, adding `--dry-run` to preview
available updates. Unversioned installation resolves the latest tagged release,
or the default branch when there are no releases; it should not be assumed to
follow every commit on `main`. Check `gh skill update --help` for your CLI version.

## The five skills

| Skill | Responsibility |
| --- | --- |
| `to-outcomes` | Split a PRD into scoped outcomes, dependencies and a coverage index. |
| `orchestrate-work` | Own checkpoints, retry limits, phase transitions and completion. |
| `implement` | Make scoped changes and return an implementation handoff. |
| `verify` | Independently assess acceptance criteria with actual evidence. |
| `recalibrate` | Diagnose failed or inconclusive verification and plan the next action. |

Project-specific tools are optional: describe them in
`.agents/capabilities/CAPABILITIES.md` using [the capability template](templates/CAPABILITIES.md).
Without a registry, the agent uses available native tools and reports gaps.

See [handoff contracts](docs/HANDOFFS.md), [state and recovery rules](docs/WORK-STATE.md),
and [distribution and installation checks](docs/DISTRIBUTION.md) for details.

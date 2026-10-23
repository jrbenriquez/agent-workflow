# Distribution and Updates

## Preferred approach
Use an existing Agent Skills-compatible installer rather than creating a custom package manager. Candidates include GitHub CLI skill management (where available) and the open-source Vercel Skills CLI (`npx skills`). Verify current syntax and capabilities against the chosen tool's documentation before publishing installation commands.

## Verified local installation behavior

Tested with `gh version 2.92.0 (2026-04-28)` on macOS, on 2026-10-22.
`gh skill` is a preview feature. The commands inspected were:

```sh
gh --version
gh skill --help
gh skill install --help
```

Each skill was installed independently into a fresh temporary git repository,
with that repository as the working directory. Exact install commands tested
both before and after bundling were:

```sh
git init -q <temporary-consuming-repository>
gh skill install /Users/johnreienriquez/Code/agent-workflow orchestrate-work --from-local --agent codex --scope project
gh skill install /Users/johnreienriquez/Code/agent-workflow implement --from-local --agent codex --scope project
gh skill install /Users/johnreienriquez/Code/agent-workflow verify --from-local --agent codex --scope project
gh skill install /Users/johnreienriquez/Code/agent-workflow recalibrate --from-local --agent codex --scope project
```

The four commands above were run in **four separate consumers**, not together.
The absolute source path is the tested checkout; substitute your checkout path.
All eight installs (four before, four after) exited 0.

Before bundling, each `.agents/skills/<name>/` contained only `SKILL.md`.
No upstream `docs/` directory was copied. Every `../../docs/HANDOFFS.md`
reference failed to resolve. Independent installation did not make files outside
the source skill directory accessible through those references.

After bundling, each installed skill contained `SKILL.md` and
`references/HANDOFFS.md`. All four contract references resolved within their own
skill directory, and the installed contract bytes matched the generated source
copy. Copies were regular files, not symlinks, and no sibling skill was needed.

## Maintaining self-contained skills

`docs/HANDOFFS.md` is the single authoritative handoff contract.
`docs/WORK-STATE.md` is authoritative for orchestration state and is bundled only
in orchestrate-work as `references/WORK-STATE.md`.
`docs/GROUP-ORCHESTRATION.md` is authoritative for group scheduling, checkpoints,
branch handling, local execution and parallel policy; it is bundled there as
`references/GROUP-ORCHESTRATION.md`. After editing these sources, run:

```sh
python3 scripts/sync-handoffs.py
python3 scripts/sync-handoffs.py --check
python3 -m pip install -r scripts/requirements-checks.txt
python3 scripts/check-skill-frontmatter.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/check-skill-install.py
git diff --check
```

Commit the generated `skills/*/references/HANDOFFS.md` files and
`skills/orchestrate-work/references/{WORK-STATE,GROUP-ORCHESTRATION}.md` with their sources.
Do not hand-edit them. The sync script adds a generated-file notice; `--check`
fails if any copy is absent or stale. The installation check repeats the four
independent core installs plus `to-outcomes`, checks all bundled reference contents
and their local links, and removes
its temporary consuming repositories. It requires Python 3.9+, Git, and a `gh`
version supporting `skill install --from-local`.

The installer needs no generator or shared upstream directory at installation
time: each committed skill directory already contains its contract. There is no
new core skill or dependency on project capabilities.

## Continuous integration

`.github/workflows/checks.yml` runs on pull requests, pushes and manual dispatch:

| Check | What fails | How to fix it |
| --- | --- | --- |
| Skill frontmatter | Missing/invalid YAML metadata, empty or non-string name/description, duplicate names | Install `scripts/requirements-checks.txt`, run `python3 scripts/check-skill-frontmatter.py`, then fix the metadata in the files listed by the errors. |
| Generated references | Missing or stale distributed copies of canonical policy | Edit `docs/` sources, run `python3 scripts/sync-handoffs.py`, verify with `--check`, and commit sources plus generated references together. |
| Validation regression tests | Metadata validation, generation, idempotence, drift detection or read-only check behavior changes unexpectedly | Install `scripts/requirements-checks.txt`, run `python3 -m unittest discover -s scripts -p 'test_*.py' -v`, inspect the failing assertion and fix the behavior or intentional compatibility change. |
| Independent local installs | A skill cannot install alone, installed content differs, or an internal link escapes/is missing | Run `python3 scripts/check-skill-install.py` using GitHub CLI 2.92.0; inspect the failing skill/reference, fix its packaging or link, regenerate and commit required files. |

Sync failures include the affected paths, a GitHub error annotation and a job
summary with exact repair steps. CI checks drift without rewriting or committing
files. The install job downloads the tested CLI from the official `cli/cli`
release and verifies its published checksums rather than relying on the runner's
preview-command version. Download/setup failures appear in their own step;
inspect release availability or runner/network errors before changing skill files.
Jobs use read-only repository permissions and do not publish or push anything.

Local verification on 2026-10-23: actionlint 1.7.12 accepted the workflow; the
actual sync-step shell script passed with fresh references and failed against an
intentionally stale copy in a disposable directory. The failure named the affected
file, emitted the annotation and repair summary, and left the stale file unchanged.
The three generator tests and all five local install checks also passed. The
hosted Ubuntu workflow has not run yet; local results do not establish that run.

The frontmatter validator uses PyYAML (pinned in `scripts/requirements-checks.txt`)
so quoted and multiline YAML values work. A subsequent local run passed all five
skill metadata checks and all eight regression tests, including invalid YAML,
missing/empty/non-string fields and duplicate skill names. Metadata failures name
the affected files and required correction; the CI step also emits an annotation.

These are packaging and generator checks. They do not establish runtime
orchestration correctness. Other useful future checks are local documentation
links, parsed state-template schema validation,
and a disposable consuming-repository execution harness when one exists. Prefer
local links in required CI; external-link availability can be checked separately
so transient remote failures do not block ordinary changes.

## Validation limits

These results establish **local-source, Codex, project-scope installation** with
the tested CLI version. Remote GitHub installation of this uncommitted revision,
other agents, user scope, pinned releases, and update behavior were not tested.
Do not infer compatibility for those modes or other installers from this test.
The local installation check validates file availability, not an agent runtime's
execution of the instructions. Re-run it when the CLI or packaging changes.
Generator regression tests exercise generation, idempotence, missing/corrupt copies
and changed canonical sources in disposable directories. They do not simulate an
agent following orchestration prose. See [scenario walkthroughs](ORCHESTRATION-VALIDATION.md)
for policy review coverage and explicit runtime verification limits.

## Release policy
- Tag the entire set of four core skills together (e.g. `v0.1.0`, `v0.2.0`).
- Keep a changelog and note breaking changes.
- Pin consuming repositories to a tested release where the installer supports it.
- Update all four core skills as a compatible unit and review diffs before merging.
- Keep project-specific skills and `.agents/capabilities/` outside upstream-managed skill directories.
- Never force-overwrite local modifications to managed files; inspect conflicts.

## Future checks
- Confirm supported discovery paths for target agents.
- Confirm how installer handles pinning, upgrades, and locally modified skill files.
- Test remote install and update in a disposable consuming repository.

## Optional PRD decomposition

`to-outcomes` is a self-contained planning skill distributed alongside the four
core workflow skills. It has no runtime handoff contract and needs no generated
reference files. Install it independently using the same local-source approach:

```sh
gh skill install /path/to/agent-workflow to-outcomes --from-local --agent codex --scope project
```

Invoke it with a PRD path to write outcome documents and a dependency/coverage
index inside `outcomes/<general-outcome-name>/` in the consuming repository.
The user chooses the general outcome name; multiple sets can coexist in separate
folders. New outcome IDs include the set name to keep runtime state distinct.
Execute a group with `orchestrate-work for outcomes/<general-outcome-name>` or a
single outcome by its document path. The index remains a plan until an execution
request invokes the coordinator; `to-outcomes` does not create runtime state,
launch agents or start implementation. The local
installation checker includes this fifth, optional skill and compares its
installed instruction body to the source (the installer rewrites frontmatter).
Existing per-outcome schema version 1 and phase handoff fields remain compatible;
group checkpoint version 1 is separate and references them. Unknown/legacy state
requires explicit reconciliation, never silent migration or a fresh budget.

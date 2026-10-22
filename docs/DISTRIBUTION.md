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
in orchestrate-work as `references/WORK-STATE.md`. After editing either, run:

```sh
python3 scripts/sync-handoffs.py
python3 scripts/sync-handoffs.py --check
python3 scripts/check-skill-install.py
git diff --check
```

Commit the generated `skills/*/references/HANDOFFS.md` files and
`skills/orchestrate-work/references/WORK-STATE.md` with their sources.
Do not hand-edit them. The sync script adds a generated-file notice; `--check`
fails if any copy is absent or stale. The installation check repeats the four
independent installs above, checks contract contents and local links, and removes
its temporary consuming repositories. It requires Python 3.9+, Git, and a `gh`
version supporting `skill install --from-local`.

The installer needs no generator or shared upstream directory at installation
time: each committed skill directory already contains its contract. There is no
new core skill or dependency on project capabilities.

## Validation limits

These results establish **local-source, Codex, project-scope installation** with
the tested CLI version. Remote GitHub installation of this uncommitted revision,
other agents, user scope, pinned releases, and update behavior were not tested.
Do not infer compatibility for those modes or other installers from this test.
The local installation check validates file availability, not an agent runtime's
execution of the instructions. Re-run it when the CLI or packaging changes.

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
Execute ready outcomes individually with
`orchestrate-work`; the index is a plan, not an automatic scheduler. The local
installation checker includes this fifth, optional skill and compares its
installed instruction body to the source (the installer rewrites frontmatter). The four core contract bundles remain unchanged.

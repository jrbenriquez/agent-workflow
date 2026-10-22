# Distribution and Updates

## Preferred approach
Use an existing Agent Skills-compatible installer rather than creating a custom package manager. Candidates include GitHub CLI skill management (where available) and the open-source Vercel Skills CLI (`npx skills`). Verify current syntax and capabilities against the chosen tool's documentation before publishing installation commands.

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
- Test install and update in a disposable consuming repository.

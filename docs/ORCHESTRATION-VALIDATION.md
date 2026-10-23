# Orchestration validation

## What can be executed here

This repository ships Markdown skills, not a scheduler executable or agent test
harness. Automated checks exercise actual generation and independent local
installation, including all required references and links:

```sh
python3 scripts/sync-handoffs.py
python3 scripts/sync-handoffs.py --check
python3 -m pip install -r scripts/requirements-checks.txt
python3 scripts/check-skill-frontmatter.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/check-skill-install.py
git diff --check
```

The generator tests mutate disposable copies to check missing/corrupt bundles,
changed canonical documents, read-only check behavior, regeneration and idempotence.
The installer check compares installed bodies and every reference byte-for-byte,
and checks local links in the installed documents. No automated test certifies
that a language model will follow scheduling policy. Do not label the walkthroughs
below executed orchestration, browser, accessibility or performance tests.

Local validation on 2026-10-23 used Python 3.12.8, Git 2.39.5 (Apple Git-154),
and GitHub CLI 2.92.0 on macOS, on branch
`codex/outcome-group-orchestration` based on `873b27b` with these working changes:

| Executed check | Observed result |
| --- | --- |
| Canonical generation and `--check` | Exit 0; all six distributed references current. |
| Generator regression suite | 3 tests passed, including missing/corrupt copies and changed sources. |
| Independent `gh skill install --from-local` checks | All 5 skills installed successfully; bodies, every bundled reference and local links passed. |
| `git diff --check` | Exit 0 after correcting changelog whitespace. |

These observations concern local-source, Codex, project-scope packaging of this
revision. Remote installation, other agents/installers and runtime behavior were
not exercised. The unrelated untracked `examples/` directory was not modified or
used as acceptance evidence.

## Policy walkthroughs (design review, not runtime tests)

Use three hypothetical outcomes: A owns stored submissions, B depends on A's
storage criterion and owns notification behavior, C owns independent CSV export.
Each has two required criteria and its own saved three-attempt budget. Suggested
order is B, A, C. These are reasoning fixtures, not shipped executable outcomes or
claims about an application. Review starts from the full definitions, not labels.

| Scenario / starting condition | Derived action and stopping gate |
| --- | --- |
| Single A document, no history | Initialize only A's version 1 state; implement/1 → independent verify both criteria → complete only for two current PASS. No group wrapper or forced branch migration. |
| No input; one group plus standalone C | List group and C once each, excluding group members as standalone entries; wait for selection. One group alone still requires selection. Empty `outcomes/` → report no work, no branch/state/implementation. |
| Context says “make notifications better” | Inspect existing decisions. Without observable acceptance, do not execute invented criteria; clarify or use authorized `to-outcomes`. An embedded outcome with accepted IDs/criteria is saved before execution. |
| B labelled ready; A lacks PASS | Ignore planning label. Eligible A,C; choose A by suggested order among eligible outcomes. After A passes storage, choose B, then C. Inspect all B criteria before completion. |
| Explicit order C,A,B | Execute C,A,B subject to evidence gates. Explicit B,A conflicts with unmet A dependency: record conflict, seek revised order; do not silently execute A first. |
| Duplicate A IDs or A↔B cycle | Reject ambiguous identity/cyclic graph before scheduling. Missing dependency D only for B → exact B blocker; unaffected A,C may proceed. No invented D implementation. |
| A depends on external D | Locate D and required proof; current sufficient evidence can satisfy prerequisite without executing D. Missing/stale proof → A waits on D, B waits on A, C proceeds. Request evidence or authorized scope expansion, preserve D's state. |
| A blocked on missing source asset | Save direct A blocker and resolving asset/action; B is waiting on A, not independently failed. C runs to completion. Group ends blocked with C completed and A/B distinguished. |
| Crash after group dispatch intent, before A's running checkpoint | Read A's state; intent alone does not charge an attempt. If state is ready and no invocation began, start through normal attempt gate; unknown execution evidence requires reconciliation. |
| Crash with A implement running/2, matching saved return artifact | Recover artifact, save returned, consume once, proceed to verify. Keep started=2. If no artifact but invocation identity/progress is clear, safely continue that invocation; uncertain partial work blocks rather than replaying it. |
| A returned result consumed, group still says active | Per-outcome ready/complete and retained handoff establish consumption. Repair group scheduling metadata without replaying implementation or appending recalibration again. Confirm prior coordinator stopped before takeover. |
| Attempt 3 ready for verification | Both criteria PASS → complete with started=3. FAIL → recalibrate; REIMPLEMENT → block/attempt_limit with started=3. Read-only diagnostics/verification may still establish acceptance; a new invocation never grants attempt 4. |
| Browser/visual/a11y/performance check required but unavailable | Early capability inventory records exact missing checks. No observed defect → INCONCLUSIVE, then recalibrate. Unchanged repeated diagnostic request → no_progress; other eligible outcomes continue. CLI unit tests alone cannot fill the gap. |
| B requires real email delivery, only capture available | Capture may demonstrate formatting but cannot pass delivery. Record affected criterion and missing authorization/capability; continue C. If criteria explicitly permit captured delivery, labelled capture is acceptable evidence. No unauthorized send. |
| B implementation changes A's shared storage code | Snapshot dirty inputs/config/fixtures/environment, invalidate potentially affected A PASS before dependent acceptance, queue and run A regression. Retain historical proof. B's scoped PASS does not complete the group while A is stale. |
| C changes only export presentation | Inspect impact rather than assume independence; retain A/B PASS only with explicit applicability assessment. Unbounded shared-config effect invalidates all potentially affected passes. Missing evidence cannot remain PASS. |
| Parallel requested, A and C graph independent but share migration/config | Dependency independence fails edit-safety review; fall back sequentially. No parallel authorization or isolation support also selects sequential mode. Record reason without asking routine permission to continue sequentially. |
| Authorized independent A/C workers in isolated worktrees | Coordinator charges each outcome and owns state; integrate A, verify on coordinator; integrate C, assess impact on A, reverify affected criteria. C worker PASS alone never completes C on assembled code. Freeze relevant inputs during verify or invalidate on integration. |
| Crash during worker integration | Inspect recorded integration intent, actual history/content and worker status. Complete only identifiable remaining integration or block for reconciliation. Do not reapply an already integrated patch or dispatch a duplicate implementer. |
| New group, remote default is `trunk`, current branch has dirty unrelated edits | Resolve configured remote/default, fetch trunk, inspect collisions; create dedicated `codex/outcomes/<id>` in isolated worktree from fetched SHA. Leave dirty checkout intact, record repository/base/branch/worktree. No push/PR/merge. |
| Dedicated branch name already exists without matching state | Inspect local/remote history and worktrees; name alone is not ownership. Block for reconciliation rather than reset it or hide it with a suffix. Existing per-outcome history also forbids fresh budgets. |
| Resume recorded branch after new default-branch commits | Reuse saved branch/worktree after history/content validation, without recreating from new default. Missing branch, rewritten base or conflicting checkout requires conservative reconciliation. Preserve accepted work and attempts. |
| Remote unavailable | Known local default + explicitly permitted offline policy → record local SHA and unknown freshness, disclose fallback. No offline permission/known default → branch-setup blocker. Never claim latest remote. |
| Group checkpoint says complete, B proof missing or workspace changed | Derive truth from current per-outcome evidence, reopen affected verification and pending regressions. Unsupported group summary cannot override missing proof. Unknown schema or changed scope blocks reconciliation; version 1 single-outcome history remains intact. |
| Every A/B/C criterion has current PASS, no active work/regressions | Check authoritative full coverage and accessible evidence, then complete. Report checks actually performed, limitations, evidence, branch/worktree and run instructions. One remaining INCONCLUSIVE criterion forbids completion. |

The review exercises routing, ownership and stopping conditions, with per-outcome
transition walkthroughs retained in `WORK-STATE.md`. Runtime conformance, real
application execution, external delivery and parallel worker integration remain
unverified by this repository's automated checks. A consuming application needs
its own observed evidence for those behaviors.

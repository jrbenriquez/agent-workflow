#!/usr/bin/env python3
"""Bundle the authoritative contract; --check detects missing or stale copies."""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ('orchestrate-work', 'implement', 'verify', 'recalibrate')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    content = (
        b'<!-- Generated from docs/HANDOFFS.md by scripts/sync-handoffs.py. '
        b'Do not edit this copy. -->\n\n'
        + (ROOT / 'docs/HANDOFFS.md').read_bytes()
    )
    stale = []
    for name in SKILLS:
        target = ROOT / 'skills' / name / 'references/HANDOFFS.md'
        if args.check:
            if not target.exists() or target.read_bytes() != content:
                stale.append(str(target.relative_to(ROOT)))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    state_target = ROOT / 'skills/orchestrate-work/references/WORK-STATE.md'
    state_content = (
        b'<!-- Generated from docs/WORK-STATE.md by scripts/sync-handoffs.py. '
        b'Do not edit this copy. -->\n\n'
        + (ROOT / 'docs/WORK-STATE.md').read_bytes()
    )
    if args.check:
        if not state_target.exists() or state_target.read_bytes() != state_content:
            stale.append(str(state_target.relative_to(ROOT)))
    else:
        state_target.parent.mkdir(parents=True, exist_ok=True)
        state_target.write_bytes(state_content)
    if stale:
        parser.exit(1, 'Stale handoff copies; run python3 scripts/sync-handoffs.py:\n'
                    + '\n'.join(stale) + '\n')


if __name__ == '__main__':
    main()

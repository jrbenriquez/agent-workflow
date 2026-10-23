#!/usr/bin/env python3
"""Bundle the authoritative contract; --check detects missing or stale copies."""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ('orchestrate-work', 'implement', 'verify', 'recalibrate')
BUNDLES = [
    ('HANDOFFS.md', name) for name in SKILLS
] + [
    ('WORK-STATE.md', 'orchestrate-work'),
    ('GROUP-ORCHESTRATION.md', 'orchestrate-work'),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    stale = []
    for document, name in BUNDLES:
        content = (
            f'<!-- Generated from docs/{document} by scripts/sync-handoffs.py. '
            'Do not edit this copy. -->\n\n'
        ).encode() + (ROOT / 'docs' / document).read_bytes()
        target = ROOT / 'skills' / name / 'references' / document
        if args.check:
            if not target.exists() or target.read_bytes() != content:
                stale.append(str(target.relative_to(ROOT)))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    if stale:
        parser.exit(1, 'Missing or stale generated references:\n'
                    + '\n'.join(stale)
                    + '\nEdit authoritative docs/ sources, then run '
                    'python3 scripts/sync-handoffs.py.\n'
                    'Commit the source changes and generated skills/*/references/ '
                    'files together; do not hand-edit generated copies.\n')


if __name__ == '__main__':
    main()

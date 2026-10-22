#!/usr/bin/env python3
"""Exercise independent gh skill local installs in disposable git repositories."""
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
subprocess.run(['python3', str(ROOT / 'scripts/sync-handoffs.py'), '--check'], check=True)
with tempfile.TemporaryDirectory(prefix='agent-workflow-install-') as temporary:
    for name in ('orchestrate-work', 'implement', 'verify', 'recalibrate'):
        consumer = Path(temporary) / name
        consumer.mkdir()
        subprocess.run(['git', 'init', '-q', str(consumer)], check=True)
        command = ['gh', 'skill', 'install', str(ROOT), name, '--from-local',
                   '--agent', 'codex', '--scope', 'project']
        print(f'cwd={consumer}: {" ".join(command)}', flush=True)
        subprocess.run(command, cwd=consumer, check=True)
        installed = consumer / '.agents/skills' / name
        assert not installed.is_symlink(), installed
        bundled = installed / 'references/HANDOFFS.md'
        assert bundled.is_file() and not bundled.is_symlink(), bundled
        assert bundled.read_bytes() == (ROOT / 'skills' / name / 'references/HANDOFFS.md').read_bytes()
        for document in (installed / 'SKILL.md', bundled):
            for link in re.findall(r'\]\(([^)]+)\)', document.read_text()):
                if '://' not in link and not link.startswith('#'):
                    resolved = (document.parent / link.split('#')[0]).resolve()
                    assert resolved.is_relative_to(installed.resolve()), resolved
                    assert resolved.exists(), resolved
        assert sorted(p.name for p in installed.parent.iterdir()) == [name]
        print(f'PASS: {name}: bundled contract matches source; local links stay inside skill.')

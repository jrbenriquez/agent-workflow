"""Exercise distribution behavior in disposable copies, without editing source."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='workflow-bundles-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        shutil.copytree(ROOT / 'docs', self.root / 'docs')
        (self.root / 'scripts').mkdir()
        shutil.copy2(ROOT / 'scripts/sync-handoffs.py', self.root / 'scripts')

    def run_sync(self, *args):
        return subprocess.run(
            [sys.executable, str(self.root / 'scripts/sync-handoffs.py'), *args],
            capture_output=True, text=True,
        )

    def test_generation_and_idempotence(self):
        self.assertEqual(self.run_sync().returncode, 0)
        expected = {
            'orchestrate-work': ['HANDOFFS.md', 'WORK-STATE.md', 'GROUP-ORCHESTRATION.md'],
            'implement': ['HANDOFFS.md'],
            'verify': ['HANDOFFS.md'],
            'recalibrate': ['HANDOFFS.md'],
        }
        before = {}
        for skill, documents in expected.items():
            directory = self.root / 'skills' / skill / 'references'
            self.assertEqual(sorted(p.name for p in directory.iterdir()), sorted(documents))
            for name in documents:
                path = directory / name
                content = path.read_bytes()
                self.assertEqual(content.split(b'\n\n', 1)[1],
                                 (self.root / 'docs' / name).read_bytes())
                before[path] = content
        self.assertEqual(self.run_sync('--check').returncode, 0)
        self.assertEqual(self.run_sync().returncode, 0)
        self.assertEqual(before, {path: path.read_bytes() for path in before})

    def test_check_detects_missing_and_corrupt_copies_without_repairing(self):
        self.assertEqual(self.run_sync().returncode, 0)
        missing = self.root / 'skills/orchestrate-work/references/GROUP-ORCHESTRATION.md'
        corrupt = self.root / 'skills/verify/references/HANDOFFS.md'
        missing.unlink()
        corrupt.write_text('corrupt')
        result = self.run_sync('--check')
        self.assertEqual(result.returncode, 1)
        self.assertIn(str(missing.relative_to(self.root)), result.stderr)
        self.assertIn(str(corrupt.relative_to(self.root)), result.stderr)
        self.assertIn('python3 scripts/sync-handoffs.py', result.stderr)
        self.assertIn('do not hand-edit generated copies', result.stderr)
        self.assertFalse(missing.exists())
        self.assertEqual(corrupt.read_text(), 'corrupt')
        self.assertEqual(self.run_sync().returncode, 0)
        self.assertEqual(self.run_sync('--check').returncode, 0)

    def test_source_changes_invalidate_every_corresponding_bundle(self):
        self.assertEqual(self.run_sync().returncode, 0)
        for name in ('HANDOFFS.md', 'WORK-STATE.md', 'GROUP-ORCHESTRATION.md'):
            with self.subTest(source=name):
                with (self.root / 'docs' / name).open('a') as source:
                    source.write('\nChanged canonical policy.\n')
                result = self.run_sync('--check')
                self.assertEqual(result.returncode, 1)
                expected_count = 4 if name == 'HANDOFFS.md' else 1
                self.assertEqual(result.stderr.count(f'/references/{name}'), expected_count)
                self.assertEqual(self.run_sync().returncode, 0)
                self.assertEqual(self.run_sync('--check').returncode, 0)


if __name__ == '__main__':
    unittest.main()

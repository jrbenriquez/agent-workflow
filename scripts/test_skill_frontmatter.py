"""Exercise frontmatter validation against disposable skill directories."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FrontmatterTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='skill-metadata-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / 'scripts').mkdir()
        shutil.copy2(ROOT / 'scripts/check-skill-frontmatter.py', self.root / 'scripts')

    def write_skill(self, directory, content):
        path = self.root / 'skills' / directory / 'SKILL.md'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def check(self):
        return subprocess.run(
            [sys.executable, str(self.root / 'scripts/check-skill-frontmatter.py')],
            capture_output=True, text=True,
        )

    def test_accepts_valid_yaml_including_multiline_and_quoted_fields(self):
        self.write_skill('one', '---\nname: one\ndescription: >\n  First line\n  second line.\n---\n# Body')
        self.write_skill('two', '---\nname: "two"\ndescription: "Includes: punctuation"\n---\n')
        self.assertEqual(self.check().returncode, 0)

    def test_rejects_missing_empty_and_non_string_fields(self):
        for field in ('name', 'description'):
            for value in ('', 'null', 'false', '123', '[]', '"   "'):
                with self.subTest(field=field, value=value):
                    other = 'description: Valid description' if field == 'name' else 'name: one'
                    self.write_skill('one', f'---\n{other}\n{field}: {value}\n---\n')
                    result = self.check()
                    self.assertEqual(result.returncode, 1)
                    self.assertIn(f'skills/one/SKILL.md: set {field}', result.stderr)
            self.write_skill('one', f'---\n{other}\n---\n')
            self.assertEqual(self.check().returncode, 1)

    def test_rejects_duplicate_names_and_identifies_both_files(self):
        for directory in ('one', 'two'):
            self.write_skill(directory, '---\nname: same\ndescription: Valid\n---\n')
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn('duplicate name', result.stderr)
        self.assertIn('skills/one/SKILL.md', result.stderr)
        self.assertIn('skills/two/SKILL.md', result.stderr)

    def test_rejects_missing_delimiters_malformed_yaml_and_non_mapping(self):
        for content in ('# No metadata', '---\nname: one', '---\nname: [\n---', '---\n- one\n---'):
            with self.subTest(content=content):
                path = self.write_skill('one', content)
                result = self.check()
                self.assertEqual(result.returncode, 1)
                self.assertIn('skills/one/SKILL.md', result.stderr)
                self.assertEqual(path.read_text(), content)

    def test_rejects_empty_collection_and_missing_entrypoint(self):
        self.assertEqual(self.check().returncode, 1)
        (self.root / 'skills/one').mkdir(parents=True)
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn('skills/one/SKILL.md', result.stderr)


if __name__ == '__main__':
    unittest.main()

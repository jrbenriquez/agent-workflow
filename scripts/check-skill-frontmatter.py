"""Validate required skill metadata and unique names without changing files."""
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit('Install check dependencies: python3 -m pip install -r scripts/requirements-checks.txt')

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    names = {}
    directories = sorted(path for path in (ROOT / 'skills').glob('*') if path.is_dir())
    if not directories:
        errors.append('skills/: no skill directories found; restore the skills to validate.')
    for directory in directories:
        path = directory / 'SKILL.md'
        label = path.relative_to(ROOT)
        try:
            lines = path.read_text(encoding='utf-8').splitlines()
            if not lines or lines[0] != '---' or '---' not in lines[1:]:
                errors.append(f'{label}: add a YAML metadata block between --- lines at the top.')
                continue
            metadata = yaml.safe_load('\n'.join(lines[1:lines.index('---', 1)]))
        except (OSError, UnicodeError, yaml.YAMLError) as error:
            errors.append(f'{label}: fix unreadable or invalid YAML frontmatter: {error}')
            continue
        if not isinstance(metadata, dict):
            errors.append(f'{label}: frontmatter must be a YAML mapping with name and description.')
            continue
        for field in ('name', 'description'):
            value = metadata.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f'{label}: set {field} to a non-empty string.')
        name = metadata.get('name')
        if isinstance(name, str) and name.strip():
            name = name.strip()
            if name in names:
                errors.append(f'{label}: duplicate name {name!r}, also used in {names[name]}; choose a unique name.')
            else:
                names[name] = label
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'PASS: all {len(directories)} skills have non-empty name/description fields and unique names.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

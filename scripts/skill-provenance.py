#!/usr/bin/env python3
"""Record portable package provenance or check source and installed bytes (Python 3 + Git)."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

VERSION = '2.0.0'
NAME = 'source-provenance.json'


def hashes(package):
    result = {}
    for path in sorted(package.rglob('*')):
        relative = path.relative_to(package)
        if '.git' in relative.parts or '__pycache__' in relative.parts or relative.as_posix() == NAME:
            continue
        if path.is_symlink():
            raise ValueError(f'Package symlink is unsupported: {relative}')
        if path.is_file():
            result[relative.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True, stderr=subprocess.DEVNULL).strip()


def locator(value):
    value = value.strip().rstrip('/')
    if value.startswith('git@github.com:'):
        value = 'https://github.com/' + value.split(':', 1)[1]
    if value.endswith('.git'):
        value = value[:-4]
    # Do not record credentials or machine-specific checkout paths.
    if not re.fullmatch(r'(?:https://[A-Za-z0-9.-]+/[^\s?#@]+|urn:[A-Za-z0-9:._/-]+)', value):
        raise ValueError('Use a credential-free HTTPS repository URL or stable urn: locator')
    return value


def repository(root, override=None):
    if override:
        return locator(override)
    for key in ('skill.provenanceRepository', 'remote.origin.url'):
        try:
            return locator(git(root, 'config', '--get', key))
        except subprocess.CalledProcessError:
            pass
    raise ValueError('No canonical repository locator; pass --repository or set skill.provenanceRepository')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('mode', choices=['write', 'check'])
    parser.add_argument('package', type=Path)
    parser.add_argument('--installed', type=Path)
    parser.add_argument('--repository', help='canonical repository URL/URN; defaults to Git configuration')
    args = parser.parse_args()
    package = args.package.resolve()
    try:
        if not (package / 'SKILL.md').is_file():
            raise ValueError('package must contain SKILL.md')
        root = Path(git(package, 'rev-parse', '--show-toplevel')).resolve()
        source = package.relative_to(root).as_posix()
        if args.mode == 'write':
            if args.installed:
                raise ValueError('--installed is only valid with check')
            repo = repository(root, args.repository)
            revision = git(root, 'rev-parse', 'HEAD')
            dirty = bool(git(root, 'status', '--porcelain', '--untracked-files=all', '--', '.',
                             ':(exclude)**/source-provenance.json', ':(exclude)source-provenance.json'))
            record = {'schema_version': 2, 'tool_version': VERSION, 'repository': repo,
                      'canonical_source': source, 'base_revision': revision,
                      'uncommitted': dirty, 'files': hashes(package)}
            (package / NAME).write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
        else:
            record = json.loads((package / NAME).read_text())
            if record.get('schema_version') == 2:
                repo = repository(root, args.repository)
                if record['repository'] != repo or record['canonical_source'] != source:
                    raise ValueError('Source repository or package locator mismatch')
                if not re.fullmatch(r'[0-9a-f]{40,64}', record['base_revision']) or type(record['uncommitted']) is not bool:
                    raise ValueError('Invalid revision or dirty state')
                subprocess.run(['git', '-C', str(root), 'merge-base', '--is-ancestor', record['base_revision'], 'HEAD'],
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif 'schema_version' not in record:
                if record['canonical_source'] != str(package):
                    raise ValueError('Legacy absolute source changed; review and regenerate with write')
            else:
                raise ValueError('Unsupported provenance schema')
            if record['files'] != hashes(package):
                raise ValueError('Source content mismatch')
            if args.installed:
                installed = args.installed.resolve()
                if not (installed / NAME).is_file() or (installed / NAME).read_bytes() != (package / NAME).read_bytes():
                    raise ValueError('Installed provenance mismatch')
                if hashes(installed) != record['files']:
                    raise ValueError('Installed content mismatch')
        print(f'{args.mode}: {package.name}: OK')
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'Provenance failed: {error}\n')


if __name__ == '__main__':
    main()

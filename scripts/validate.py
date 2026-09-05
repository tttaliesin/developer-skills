#!/usr/bin/env python3
"""Verify pinned snapshots and reconstruct customized package bytes from patches."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def inventory(path):
    return {
        str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(path.rglob('*'))
        if p.is_file() and p.name != 'source-provenance.json'
        and '__pycache__' not in p.relative_to(path).parts
    }


def main():
    lock = json.loads((ROOT / 'upstream-lock.json').read_text())
    for name, meta in lock.items():
        snapshot = ROOT / 'upstream' / name
        if inventory(snapshot) != meta['upstream_files']:
            raise SystemExit(f'{name}: upstream snapshot hash/inventory mismatch')
        with tempfile.TemporaryDirectory(prefix='developer-skills-verify-') as tmp:
            target = Path(tmp) / 'skills' / name
            shutil.copytree(snapshot / meta['source_directory'], target)
            if not (target / 'LICENSE.txt').exists():
                shutil.copyfile(snapshot / 'LICENSE', target / 'LICENSE.txt')
            patch = ROOT / 'patches' / f'{name}.patch'
            for options in [['--check'], []]:
                subprocess.run(['git', 'apply', *options, str(patch)], cwd=tmp, check=True)
            if inventory(target) != inventory(ROOT / 'skills' / name):
                raise SystemExit(f'{name}: patch reconstruction differs from package')
        print(f'{name}: upstream hashes and patch reconstruction OK')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Regenerate one adaptation patch and verify reconstruction before replacing it."""
import argparse
import difflib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from validate import ROOT, inventory


def main():
    lock = json.loads((ROOT / 'upstream-lock.json').read_text())
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', choices=sorted(lock))
    args = parser.parse_args()
    name = args.package
    meta = lock[name]
    snapshot = ROOT / 'upstream' / name
    package = ROOT / 'skills' / name
    if inventory(snapshot) != meta['upstream_files']:
        parser.error('upstream snapshot hash/inventory mismatch; patch was not changed')

    with tempfile.TemporaryDirectory(prefix='developer-skills-patch-') as tmp:
        target = Path(tmp) / 'skills' / name
        shutil.copytree(snapshot / meta['source_directory'], target)
        if not (target / 'LICENSE.txt').exists():
            shutil.copyfile(snapshot / 'LICENSE', target / 'LICENSE.txt')
        old, new = inventory(target), inventory(package)
        chunks = []
        for path in sorted(old.keys() | new.keys()):
            before = (target / path).read_text(encoding='utf-8') if path in old else ''
            after = (package / path).read_text(encoding='utf-8') if path in new else ''
            for line in difflib.unified_diff(
                before.splitlines(keepends=True), after.splitlines(keepends=True),
                fromfile=f'a/skills/{name}/{path}' if path in old else '/dev/null',
                tofile=f'b/skills/{name}/{path}' if path in new else '/dev/null',
            ):
                chunks.append(line if line.endswith('\n') else line + '\n\\ No newline at end of file\n')
        patch = Path(tmp) / 'adaptation.patch'
        patch.write_text(''.join(chunks), encoding='utf-8')
        for options in [['--check'], []]:
            subprocess.run(['git', 'apply', *options, str(patch)], cwd=tmp, check=True)
        if inventory(target) != new:
            parser.error('patch reconstruction differs from package; patch was not changed')
        shutil.copyfile(patch, ROOT / 'patches' / f'{name}.patch')
    print(f'{name}: patch regenerated and reconstruction verified')


if __name__ == '__main__':
    main()

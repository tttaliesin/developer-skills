"""Exercise standalone provenance across relocation and package corruption."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[1] / 'scripts/skill-provenance.py'


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'repo'
        self.root.mkdir()
        self.package = self.root / 'skills/example'
        self.package.mkdir(parents=True)
        (self.package / 'SKILL.md').write_text('---\nname: example\ndescription: Example\n---\n')
        self.git('init', '-q')
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('config', 'user.name', 'Test')
        self.git('config', 'skill.provenanceRepository', 'urn:test:example')
        self.git('add', '.')
        self.git('commit', '-qm', 'initial')

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], text=True).strip()

    def run_tool(self, *args, ok=True):
        result = subprocess.run(['python3', str(TOOL), *map(str, args)], cwd=self.tmp.name,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result

    def write(self):
        self.run_tool('write', self.package)
        return json.loads((self.package / 'source-provenance.json').read_text())

    def test_revision_dirty_and_metadata_commit(self):
        record = self.write()
        self.assertEqual(record['base_revision'], self.git('rev-parse', 'HEAD'))
        self.assertFalse(record['uncommitted'])
        self.assertEqual(record['canonical_source'], 'skills/example')
        self.git('add', '.')
        self.git('commit', '-qm', 'record')
        self.run_tool('check', self.package)
        (self.package / 'new.txt').write_text('new')
        self.assertTrue(self.write()['uncommitted'])
        self.run_tool('check', self.package)

    def test_installed_missing_extra_and_tamper(self):
        self.write()
        installed = Path(self.tmp.name) / 'installed'
        for mutation in ('missing', 'extra', 'tamper', 'provenance'):
            with self.subTest(mutation=mutation):
                shutil.copytree(self.package, installed)
                self.run_tool('check', self.package, '--installed', installed)
                if mutation == 'missing':
                    (installed / 'SKILL.md').unlink()
                elif mutation == 'extra':
                    (installed / 'extra.txt').write_text('unexpected')
                elif mutation == 'tamper':
                    (installed / 'SKILL.md').write_text('changed')
                else:
                    (installed / 'source-provenance.json').write_text('{}')
                self.run_tool('check', self.package, '--installed', installed, ok=False)
                shutil.rmtree(installed)

    def test_relocation_and_repository_mismatch(self):
        self.write()
        moved = Path(self.tmp.name) / 'relocated'
        shutil.move(self.root, moved)
        self.root = moved
        self.package = moved / 'skills/example'
        self.run_tool('check', self.package)
        self.run_tool('check', self.package, '--repository', 'urn:test:other', ok=False)

    def test_source_tamper(self):
        self.write()
        (self.package / 'SKILL.md').write_text('tamper')
        self.run_tool('check', self.package, ok=False)

    def test_unknown_revision_and_dirty_type(self):
        record = self.write()
        for key, value in [('base_revision', '0' * 40), ('uncommitted', 'false')]:
            bad = dict(record, **{key: value})
            (self.package / 'source-provenance.json').write_text(json.dumps(bad))
            self.run_tool('check', self.package, ok=False)

    def test_legacy_check(self):
        record = self.write()
        record.pop('schema_version')
        record['canonical_source'] = str(self.package)
        (self.package / 'source-provenance.json').write_text(json.dumps(record))
        self.run_tool('check', self.package)

    def test_copied_standalone_tool(self):
        self.write()
        copied = Path(self.tmp.name) / 'standalone.py'
        shutil.copyfile(TOOL, copied)
        result = subprocess.run(['python3', str(copied), 'check', str(self.package)],
                                cwd='/', capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_version(self):
        self.assertEqual(self.run_tool('--version').stdout.strip(), '2.0.0')


if __name__ == '__main__':
    unittest.main()

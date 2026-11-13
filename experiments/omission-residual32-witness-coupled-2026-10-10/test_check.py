"""Corruption controls for the exact proof and deletion replay."""
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('coupled_check', BASE/'check.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class ReplayControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for name in ['core13.json','core13.cnf','core13.lrat','deletion-witnesses.json.gz']:
            shutil.copyfile(BASE/name,self.root/name)

    def tearDown(self):
        self.temp.cleanup()

    def update_lrat(self, text):
        path = self.root/'core13.lrat'
        path.write_text(text)
        meta = json.loads((self.root/'core13.json').read_text())
        meta['lrat_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        (self.root/'core13.json').write_text(json.dumps(meta))

    def test_complete_replay(self):
        self.assertEqual(checker.check_rup(self.root),258)
        self.assertEqual(checker.check_deletions(self.root),13)

    def test_fabricated_empty_clause_rejected(self):
        lines = (self.root/'core13.lrat').read_text().splitlines()
        last_id = lines[-1].split()[0]
        self.update_lrat('\n'.join(lines[:-1]+[last_id+' 0 0'])+'\n')
        with self.assertRaises(AssertionError):
            checker.check_rup(self.root)

    def test_missing_final_contradiction_rejected(self):
        lines = (self.root/'core13.lrat').read_text().splitlines()
        self.update_lrat('\n'.join(lines[:-1])+'\n')
        with self.assertRaises(AssertionError):
            checker.check_rup(self.root)

    def test_invalid_deletion_order_rejected(self):
        path = self.root/'deletion-witnesses.json.gz'
        data = json.loads(gzip.decompress(path.read_bytes()))
        pos = data['witnesses'][0]['assignment']['positions']
        pos[0] = pos[1]
        path.write_bytes(gzip.compress(json.dumps(data).encode()))
        with self.assertRaises(AssertionError):
            checker.check_deletions(self.root)

    def test_changed_source_identity_rejected(self):
        path = self.root/'deletion-witnesses.json.gz'
        data = json.loads(gzip.decompress(path.read_bytes()))
        data['source_sha256'] = '0'*64
        path.write_bytes(gzip.compress(json.dumps(data).encode()))
        with self.assertRaisesRegex(AssertionError, 'source identity'):
            checker.check_deletions(self.root)

    def test_changed_core_identity_rejected(self):
        path = self.root/'deletion-witnesses.json.gz'
        data = json.loads(gzip.decompress(path.read_bytes()))
        data['core'].reverse()
        path.write_bytes(gzip.compress(json.dumps(data).encode()))
        with self.assertRaisesRegex(AssertionError, 'core identity'):
            checker.check_deletions(self.root)

    def test_changed_profile_identity_rejected(self):
        path = self.root/'deletion-witnesses.json.gz'
        data = json.loads(gzip.decompress(path.read_bytes()))
        data['profiles'][str(data['core'][0])][0] += 1
        path.write_bytes(gzip.compress(json.dumps(data).encode()))
        with self.assertRaisesRegex(AssertionError, 'profile identity'):
            checker.check_deletions(self.root)


if __name__ == '__main__':
    unittest.main()

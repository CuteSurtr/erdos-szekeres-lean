"""Reject proof corruption even when transport hashes are refreshed."""
import importlib.util
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('rank_certificate_check', HERE / 'check.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class ReplayControls(unittest.TestCase):
    stem = 'core-one'
    expected_steps = 419

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for suffix in ['json', 'cnf', 'lrat']:
            shutil.copyfile(HERE / (self.stem + '.' + suffix), self.root / (self.stem + '.' + suffix))

    def tearDown(self):
        self.temp.cleanup()

    def update_proof(self, lines):
        proof = self.root / (self.stem + '.lrat')
        proof.write_text('\n'.join(lines) + '\n')
        source = self.root / (self.stem + '.json')
        data = json.loads(source.read_text())
        data['lrat_sha256'] = hashlib.sha256(proof.read_bytes()).hexdigest()
        source.write_text(json.dumps(data))

    def test_complete_rup_proof(self):
        self.assertEqual(checker.check_rup(self.root, self.stem)['rup_steps'], self.expected_steps)

    def test_missing_final_empty_clause(self):
        lines = (self.root / (self.stem + '.lrat')).read_text().splitlines()
        self.update_proof(lines[:-1])
        with self.assertRaisesRegex(ValueError, 'Missing final empty clause'):
            checker.check_rup(self.root, self.stem)

    def test_fabricated_contradiction(self):
        lines = (self.root / (self.stem + '.lrat')).read_text().splitlines()
        lines[-1] = lines[-1].split()[0] + ' 0 0'
        self.update_proof(lines)
        with self.assertRaisesRegex(ValueError, 'RUP step has no contradiction'):
            checker.check_rup(self.root, self.stem)


class CoreTwoControls(ReplayControls):
    stem = 'core-two'
    expected_steps = 605


class CoreThreeControls(ReplayControls):
    stem = 'core-three'
    expected_steps = 450


class CoreFourControls(ReplayControls):
    stem = 'core-four'
    expected_steps = 659


if __name__ == '__main__':
    unittest.main()

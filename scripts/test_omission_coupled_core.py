"""Controls for the independently replayed coupled-state proof artifact."""
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from check_omission_coupled_core import check_deletions, check_rup
from check_omission_coupled_second import check_rup as check_second_rup
from check_omission_coupled_third import check_rup as check_third_rup
from check_omission_coupled_fourth import check_rup as check_fourth_rup
from check_omission_coupled_fifth import check_rup as check_fifth_rup

ROOT = Path(__file__).resolve().parents[1]
class CoupledCoreControls:
    def copy_artifact(self, target):
        for name in ('core13.json', 'core13.cnf', 'core13.lrat', 'deletion-witnesses.json.gz'):
            shutil.copyfile(self.artifact / name, target / name)

    def test_complete_rup_and_deletion_models(self):
        self.assertEqual(self.replay(self.artifact), self.steps)
        self.assertEqual(check_deletions(self.artifact), 13)

    def test_changed_formula_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.copy_artifact(root)
            p = root / 'core13.cnf'
            p.write_text(p.read_text().replace('1 0\n', '-1 0\n', 1))
            with self.assertRaises(AssertionError):
                self.replay(root)

    def test_missing_final_derivation_is_rejected_even_with_updated_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.copy_artifact(root)
            p = root / 'core13.lrat'
            lines = p.read_text().splitlines()
            final_id = lines[-1].split()[0]
            lines[-1] = final_id + ' 0 0'
            p.write_text('\n'.join(lines) + '\n')
            meta_path = root / 'core13.json'
            meta = json.loads(meta_path.read_text())
            meta['lrat_sha256'] = hashlib.sha256(p.read_bytes()).hexdigest()
            meta_path.write_text(json.dumps(meta))
            with self.assertRaises(AssertionError):
                self.replay(root)


class CoupledCoreTests(CoupledCoreControls, unittest.TestCase):
    artifact = ROOT / 'experiments/omission-coupled-core-2026-10-10'
    replay = staticmethod(check_rup)
    steps = 343


class CoupledSecondCoreTests(CoupledCoreControls, unittest.TestCase):
    artifact = ROOT / 'experiments/omission-coupled-next-2026-10-10'
    replay = staticmethod(check_second_rup)
    steps = 435


class CoupledThirdCoreTests(CoupledCoreControls, unittest.TestCase):
    artifact = ROOT / 'experiments/omission-coupled-demand-two-2026-10-10'
    replay = staticmethod(check_third_rup)
    steps = 465


class CoupledFourthCoreTests(CoupledCoreControls, unittest.TestCase):
    artifact = ROOT / 'experiments/omission-coupled-fourth-2026-10-10'
    replay = staticmethod(check_fourth_rup)
    steps = 477


class CoupledFifthCoreTests(CoupledCoreControls, unittest.TestCase):
    artifact = ROOT / 'experiments/omission-coupled-fifth-2026-10-10'
    replay = staticmethod(check_fifth_rup)
    steps = 339


if __name__ == '__main__':
    unittest.main()

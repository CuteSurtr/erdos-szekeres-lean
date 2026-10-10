"""Compatibility and kernel rejection controls for source-cup clause exports."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

from export_omission_coupled_rank import LEGACY_EXPORTER_SHA256, export

ROOT = Path(__file__).resolve().parents[1]
RANK = ROOT / 'experiments/omission-residual-rank-attainment-2026-10-10'


def fixture():
    return {
        'support': list(range(8)),
        'variables': [['before', 0, 1], ['cup_ge', 0, 1, 2], ['cup_ge', 0, 1, 3]],
        'clauses': [
            {'kind': 'source_cup', 'detail': [0, 1], 'literals': [-1, -2], 'original_id': 1},
            {'kind': 'source_cup', 'detail': [1, 0], 'literals': [1, -3], 'original_id': 2},
        ],
    }


def emit(directory, data):
    source = directory / 'control.json'
    target = directory / 'Control.lean'
    source.write_text(json.dumps(data))
    export(source, target, 'SourceCupControl', 'rank-control', 'control')
    return target.read_text()


class ExportControls(unittest.TestCase):
    def test_legacy_exporter_bytes_remain_frozen(self):
        source = ROOT / 'scripts/export_omission_coupled_sized.py'
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), LEGACY_EXPORTER_SHA256)

    def test_existing_sixth_export_is_byte_exact(self):
        frozen = ROOT / 'experiments/omission-residual32-witness-coupled-2026-10-10'
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'LeanCore.lean'
            export(frozen / 'core13.json', target, 'CoupledCoreSixth', frozen.name, 'core13')
            emitted = target.read_text().replace('../../experiments/' + frozen.name + '/', '')
            self.assertEqual(emitted, (frozen / 'LeanCore.lean').read_text())
            self.assertNotIn('import CoupledDomain', emitted)

    def test_both_chronological_directions_use_source_cup_lemma(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = emit(Path(tmp), fixture())
        self.assertEqual(text.count('import CoupledDomain\n'), 1)
        self.assertIn('C.source_cup_clause 0 1 (by decide)', text)
        self.assertIn('C.source_cup_clause 1 0 (by decide)', text)
        self.assertIn('Context 8 n states', text)
        self.assertNotIn('Context 13 n states', text)

    def test_invalid_owner_details_are_rejected_before_output(self):
        for details in [[0, 0], [0, 8], [-1, 1], [False, 1], [0], [0, 1, 2], '0 1']:
            with self.subTest(details=details), tempfile.TemporaryDirectory() as tmp:
                data = fixture()
                data['clauses'][0]['detail'] = details
                with self.assertRaisesRegex(ValueError, 'two distinct local owner indices'):
                    emit(Path(tmp), data)
                self.assertFalse((Path(tmp) / 'Control.lean').exists())


@unittest.skipUnless(os.environ.get('ERDOS_LEAN_SOURCE_CUP_TEST') == '1',
                     'optional Lean source-cup controls')
class SourceCupKernelControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.directory = Path(cls.temp.name)
        cls.env = dict(os.environ)
        cls.env['LEAN_PATH'] = str(cls.directory) + os.pathsep + cls.env.get('LEAN_PATH', '')
        cls.env['LEAN_NUM_THREADS'] = '1'
        for module in ['RankAttainment', 'CoupledDomain']:
            proc = subprocess.run(
                ['lean', '-j1', '-s32768', '--root=' + str(RANK),
                 str(RANK / (module + '.lean')), '-o', str(cls.directory / (module + '.olean'))],
                cwd=ROOT, env=cls.env, text=True, capture_output=True)
            if proc.returncode:
                raise AssertionError(proc.stdout + proc.stderr)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def check_clauses(self, data):
        # Keep the exporter-produced atoms, literal clauses, and soundness
        # proofs, but remove the unrelated CNF/LRAT/global contradiction parts.
        raw = emit(self.directory, data)
        raw = re.sub(r'lrat_raw cnf_refutation\n.*?\n\n', '', raw, count=1, flags=re.S)
        raw = re.sub(r'private theorem formula_eq .*?\n\n', '', raw, count=1, flags=re.S)
        raw = raw.split('private theorem all_sound :', 1)[0]
        raw += 'end ErdosSzekeres.Omission.SourceCupControl\n'
        target = self.directory / 'ClauseControl.lean'
        target.write_text(raw)
        return subprocess.run(['lean', '-j1', '-s32768', str(target)],
                              cwd=ROOT, env=self.env, text=True, capture_output=True)

    def test_exported_clauses_pass_kernel(self):
        proc = self.check_clauses(fixture())
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_wrong_direction_literal_is_rejected_by_kernel(self):
        data = fixture()
        data['clauses'][0]['literals'][0] = 1
        proc = self.check_clauses(data)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('error:', proc.stdout + proc.stderr)

    def test_wrong_cup_threshold_is_rejected_by_kernel(self):
        data = fixture()
        data['variables'][1][-1] = 1
        proc = self.check_clauses(data)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('error:', proc.stdout + proc.stderr)


if __name__ == '__main__':
    unittest.main()

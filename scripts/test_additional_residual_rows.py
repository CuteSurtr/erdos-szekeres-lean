"""Literal alignment, separating witnesses, and kernel corruption controls."""
import ast
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

from omission_row_probe import read_rows

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'experiments/omission-additional-rows-2026-10-10.json'
SOURCE = ROOT / 'ErdosSzekeres/Omission/AdditionalResidualRows.lean'


class AdditionalResidualRowsTests(unittest.TestCase):
    def test_literal_data_and_catalog_binding(self):
        data, text = json.loads(DATA.read_text()), SOURCE.read_text()
        body = re.search(r'def cycles.*?:= #\[(.*?)\n\]', text, re.S)[1]
        self.assertEqual(ast.literal_eval('[' + body + ']'), data['cycles'])
        self.assertEqual(len(data['cycles']), 20)
        self.assertEqual(len({tuple(sorted(c)) for c in data['cycles']}), 20)
        for c in data['cycles']:
            self.assertEqual(len(set(c)), 8)
            self.assertTrue(all(type(v) is int and 0 <= v < 154 for v in c))
        for field in ['support', 'thresholds', 'active']:
            body = re.search(field + r' := (\[[^\]]*\])', text)[1]
            self.assertEqual(json.loads(json.dumps(ast.literal_eval(body))), data['block'][field])
        body = re.search(r'def blockSupport.*?:=\s*\{([\d,\s]+)\}', text, re.S)[1]
        self.assertEqual(ast.literal_eval('[' + body + ']'), data['block']['support'])
        raw = gzip.decompress((ROOT / 'experiments/omission-residual-geometry-2026-10-09/row-source.json.gz').read_bytes())
        self.assertEqual(hashlib.sha256(raw).hexdigest(), data['source_catalog_sha256'])

    def test_all_21_separating_witnesses(self):
        data = json.loads(DATA.read_text())
        raw = gzip.decompress((ROOT / 'experiments/omission-residual-geometry-2026-10-09/row-source.json.gz').read_bytes())
        n, old = read_rows(json.loads(raw))
        rows = [(set(c), 1) for c in data['cycles']] + [(set(data['block']['support']), 6)]
        text = (ROOT / 'experiments/omission-additional-rows-2026-10-10/BlockIndependence.lean').read_text()
        body = re.search(r'def blockWitness.*?:=\s*\{([\d,\s]+)\}', text, re.S)[1]
        witnesses = [set(c) for c in data['cycles']] + [set(ast.literal_eval('[' + body + ']'))]
        self.assertEqual(n, 154)
        self.assertEqual(len(old), 1187)
        for i, occupied in enumerate(witnesses):
            self.assertTrue(all(len(set(s)-occupied) >= d for s, d in old))
            self.assertTrue(all(len(s-occupied) >= d for j, (s,d) in enumerate(rows) if i != j))
            self.assertLess(len(rows[i][0]-occupied), rows[i][1])

    @unittest.skipUnless(os.environ.get('ERDOS_LEAN_EXPORT_TEST') == '1', 'Needs lake env and Lean controls')
    def test_kernel_rejects_reversal_and_collapsed_thresholds(self):
        prefix = ('import ErdosSzekeres.Omission.AdditionalResidualRows\n'
                  'open ErdosSzekeres.Omission\n'
                  'open AdditionalResidualRows BlockCompression\n'
                  'set_option maxHeartbeats 100000000\n'
                  'set_option maxRecDepth 100000\n')
        good = ('example : ResidualCycleValid (cycle 0) := (cycles_checked 0).1\n'
                'example : growthOK extraBlock = true := block_checked.2.1\n')
        bad = [
            'example : ResidualCycleValid ((cycle 0).reverse) := by decide +kernel\n',
            'example : growthOK { extraBlock with thresholds := [0,0,0,0,0,0] } = true := by decide +kernel\n']
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'Control.lean'
            for proof in [good, *bad]:
                source.write_text(prefix + proof)
                result = subprocess.run(['lean', str(source)], text=True, capture_output=True)
                if proof == good:
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                else:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn('is false', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()

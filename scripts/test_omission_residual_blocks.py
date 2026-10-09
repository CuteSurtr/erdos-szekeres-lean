"""Residual block coverage, literal parsing, and kernel negative controls."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from check_omission_residual_blocks import verify_sources
from omission_geometry_export import digest
from omission_residual_block_export import parse_blocks

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "experiments/omission-residual-geometry-2026-10-09/block-data.json"


def literal(b):
    return ('{ rowId := ' + str(b['row']) + ', support := ' + str(b['support'])
            + ', thresholds := ' + str(b['thresholds']) + ', active := ['
            + ','.join(f'({x},{y})' for x, y in b['active']) + '] }')


class ResidualBlockTests(unittest.TestCase):
    def test_literal_parser_rejects_code_and_missing_rows(self):
        blocks = json.loads(DATA.read_text())
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "Data.lean"
            text = '\n'.join(literal(b) + ',' for b in blocks)
            source.write_text(text)
            self.assertEqual(parse_blocks(source), blocks)
            source.write_text(text.replace('thresholds := [', 'thresholds := runCode [', 1))
            with self.assertRaises(ValueError):
                parse_blocks(source)
            source.write_text('\n'.join(text.splitlines()[1:]))
            with self.assertRaises(ValueError):
                parse_blocks(source)

    def test_manifest_requires_all_23_blocks_and_matching_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            modules = [{'module': f'ResidualBlock{r:05d}', 'row': r}
                       for r in [973, *range(1165, 1187)]]
            for name in [*(m['module'] for m in modules), 'ResidualAllGeometry']:
                (folder / (name + '.lean')).write_text('-- test fixture\n')
            report = {'block_rows': 23, 'total_rows': 1187, 'modules': modules,
                      'files': {p.name: digest(p) for p in folder.glob('*.lean')}}
            manifest = folder / 'export.json'
            manifest.write_text(json.dumps(report))
            verify_sources(folder)
            report['modules'] = modules[1:]
            manifest.write_text(json.dumps(report))
            with self.assertRaises(ValueError):
                verify_sources(folder)
            report['modules'] = modules
            manifest.write_text(json.dumps(report))
            (folder / 'ResidualBlock00973.lean').write_text('-- changed\n')
            with self.assertRaises(ValueError):
                verify_sources(folder)

    @unittest.skipUnless(os.environ.get('ERDOS_LEAN_EXPORT_TEST') == '1',
                         'Run under lake env with ERDOS_LEAN_EXPORT_TEST=1')
    def test_kernel_rejects_broken_compression(self):
        block = json.loads(DATA.read_text())[0]
        prefix = ('import ErdosSzekeres.Omission.BlockCompression\n'
                  'open ErdosSzekeres.Omission.BlockCompression\n'
                  'set_option maxRecDepth 100000\n'
                  'set_option maxHeartbeats 100000000\n'
                  'def block : Block := ' + literal(block) + '\n')
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'BlockControl.lean'
            source.write_text(prefix + 'example : pairsOK block = true ∧ growthOK block = true := by decide +kernel\n')
            good = subprocess.run(['lean', str(source)], text=True, capture_output=True)
            self.assertEqual(good.returncode, 0, good.stdout + good.stderr)
            source.write_text(prefix + 'example : growthOK { block with thresholds := [0,0,0,0,0,0] } = true := by decide +kernel\n')
            bad = subprocess.run(['lean', str(source)], text=True, capture_output=True)
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn('Tactic `decide` proved that the proposition', bad.stdout + bad.stderr)
            self.assertIn('is false', bad.stdout + bad.stderr)


if __name__ == '__main__':
    unittest.main()

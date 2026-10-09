"""Check literal catalog alignment and reject incomplete/tampered exports."""
import gzip
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

from check_omission_geometry import run as check_geometry, verify_sources
from check_omission_lean import audit_output, run as check_arithmetic
from omission_geometry_export import cycles_from_source, digest, export, occupancy_source
from omission_lean_export import export as export_arithmetic

ROOT = Path(__file__).resolve().parents[1]


class OmissionGeometryTests(unittest.TestCase):
    def test_prefixed_export_and_required_occupancy_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            archive = folder / 'archive'
            (archive / 'certificates').mkdir(parents=True)
            (archive / 'formal/sources').mkdir(parents=True)
            ids = [0, 4, 8, 15, 25, 37, 27, 18]
            (archive / 'certificates/balanced.json').write_text(json.dumps({
                'states': [None] * 252, 'cuts': [ids] * 2685}))
            (archive / 'formal/sources/ES8CycleData.lean').write_text(
                'def cycles := "' + '\\n'.join([' '.join(map(str, ids))] * 2685) + '"')
            out = folder / 'geometry'
            report = export(archive, out, arithmetic_prefix='BalancedProof')
            self.assertEqual(verify_sources(out), report)
            self.assertTrue((out / 'Geometry00000.lean').read_text().startswith(
                'import BalancedProof.Catalog\n'))
            self.assertTrue((out / 'BalancedGeometry.lean').read_text().startswith(
                'import BalancedProof.Root\nimport BalancedOccupancy\n'))
            self.assertEqual((out / 'BalancedOccupancy.lean').read_text(),
                             occupancy_source('BalancedProof.Root'))
            arithmetic = folder / 'arithmetic'
            arithmetic.mkdir()
            (arithmetic / 'export.json').write_text(json.dumps({'module_prefix': 'OtherProof'}))
            with self.assertRaisesRegex(ValueError, 'prefixes differ'):
                check_geometry(out, arithmetic)
            del report['files']['BalancedOccupancy.lean']
            (out / 'export.json').write_text(json.dumps(report))
            with self.assertRaisesRegex(ValueError, 'Incomplete geometry'):
                verify_sources(out)
            for bad in ['../Outside', 'Balanced.Root', 'Bad\nimport Root']:
                with self.assertRaises(ValueError):
                    export(archive, folder / 'invalid', arithmetic_prefix=bad)
                self.assertFalse((folder / 'invalid').exists())

    def test_literal_state_order_matches_arithmetic_source(self):
        source = ROOT / "experiments/omission-balanced-lean-2026-10-09/row-source.json.gz"
        data = json.loads(gzip.decompress(source.read_bytes()))
        lean = (ROOT / "ErdosSzekeres/Omission/BalancedCatalogData.lean").read_text()
        literal = re.search(r"^def catalog : List \(List Nat\) := (.+)$", lean, re.MULTILINE)[1]
        self.assertEqual(json.loads(literal), data["states"])

    def test_cycle_parser_does_not_read_box_data_or_accept_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "cycles.lean"
            p.write_text('def boxes := "9 8 7"\ndef cycles := "0 1 2\\n3 4 5"')
            self.assertEqual(cycles_from_source(p), [[0, 1, 2], [3, 4, 5]])
            p.write_text('def cycles := "0 1; code"')
            with self.assertRaises(ValueError):
                cycles_from_source(p)

    def test_geometry_manifest_rejects_source_tampering_and_gaps(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for name in ["Geometry00000.lean", "BalancedGeometry.lean"]:
                (folder / name).write_text("-- test input\n")
            manifest = {"modules": [{"module": "Geometry00000", "start": 0, "end": 2685}],
                        "files": {p.name: digest(p) for p in folder.glob("*.lean")}}
            path = folder / "export.json"
            path.write_text(json.dumps(manifest))
            verify_sources(folder)
            manifest["modules"][0]["start"] = 1
            path.write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                verify_sources(folder)
            manifest["modules"][0]["start"] = 0
            path.write_text(json.dumps(manifest))
            (folder / "Geometry00000.lean").write_text("-- changed\n")
            with self.assertRaises(ValueError):
                verify_sources(folder)

    @unittest.skipUnless(os.environ.get("ERDOS_LEAN_EXPORT_TEST") == "1",
                         "Run under lake env with ERDOS_LEAN_EXPORT_TEST=1")
    def test_prefixed_occupancy_links_with_unprefixed_tree(self):
        # A small genuine certificate with the same 252-state / 59-hole types
        # exercises the production occupancy bridge, without the large tree.
        from test_omission_lean_export import control
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source, tree = folder / 'balanced.json', folder / 'balanced-tree.json'
            source.write_text(json.dumps({'states': [None] * 252, 'constraints': [
                {'support': list(range(252)), 'rhs': 60}]}))
            tree.write_text(json.dumps({'source_sha256': digest(source), 'hole_budget': 59,
                'nodes': [{'type': 'weighted', 'capacity': 1, 'weights': [[0, 1]]}], 'root': 0}))
            balanced = folder / 'balanced'
            export_arithmetic(source, tree, balanced, namespace='OmissionBalanced',
                              module_prefix='BalancedProof')
            self.assertTrue(check_arithmetic(balanced)['complete'])
            other_source, other_tree, _ = control(folder)
            other = folder / 'other'
            export_arithmetic(other_source, other_tree, other, namespace='OtherControl')
            self.assertTrue(check_arithmetic(other)['complete'])
            env = dict(os.environ)
            env['LEAN_PATH'] = os.pathsep.join([str(balanced), str(other), env.get('LEAN_PATH', '')])
            proof = folder / 'CombinedOccupancy.lean'
            proof.write_text('import Root\n' + occupancy_source('BalancedProof.Root') +
                             '\n#print axioms OtherControl.excludes_budget\n')
            result = subprocess.run(['lean', str(proof)], cwd=ROOT, env=env,
                                    text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            audit_output(result.stdout, 'OmissionBalanced.occupied_card_le')
            audit_output(result.stdout, 'OtherControl.excludes_budget')

    @unittest.skipUnless(os.environ.get("ERDOS_LEAN_EXPORT_TEST") == "1",
                         "Run under lake env with ERDOS_LEAN_EXPORT_TEST=1")
    def test_lean_accepts_cycle_and_rejects_corrupted_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "CycleControl.lean"
            prefix = ("import ErdosSzekeres.Omission.CycleGeometry\n"
                      "open ErdosSzekeres.Omission\n"
                      "set_option maxRecDepth 100000\n")
            p.write_text(prefix + "example : CycleValid [0, 4, 8, 15, 25, 37, 27, 18] := by decide +kernel\n")
            good = subprocess.run(["lean", str(p)], cwd=ROOT, text=True, capture_output=True)
            self.assertEqual(good.returncode, 0, good.stdout + good.stderr)
            p.write_text(prefix + "example : CycleValid [0, 8, 4, 15, 25, 37, 27, 18] := by decide +kernel\n")
            bad = subprocess.run(["lean", str(p)], cwd=ROOT, text=True, capture_output=True)
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn("Tactic `decide` proved that the proposition", bad.stdout + bad.stderr)
            self.assertIn("is false", bad.stdout + bad.stderr)


if __name__ == '__main__':
    unittest.main()

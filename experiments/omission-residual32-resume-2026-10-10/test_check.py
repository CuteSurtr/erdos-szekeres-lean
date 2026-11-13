"""Corruption controls for the independent conditional-tree replay."""
import copy
import gzip
import json
from pathlib import Path
import unittest

from check import replay

BASE = Path(__file__).resolve().parent
SOURCE = json.loads(gzip.decompress((BASE.parent / 'omission-residual32-research-2026-10-10/source.json.gz').read_bytes()))
ROWS = [(r['support'], r['rhs']) for r in SOURCE['constraints']]
CUT = json.loads((BASE.parent / 'omission-residual32-three-row-probe-2026-10-10/diagnostic.json').read_text())['cuts_for_original_source'][0]
CONTEXT = {k: CUT[k] for k in ('missing', 'occupied')}
PROOF = {'missing': CUT['missing'], 'occupied': CUT['occupied'], 'hole_budget': 32,
         'root': 0, 'nodes': [CUT['leaf']]}


class ConditionalReplayTests(unittest.TestCase):
    def test_positive_exact_margin(self):
        self.assertEqual(replay(PROOF, ROWS, len(SOURCE['states']), CONTEXT)['minimum_margin'], 11)

    def test_zero_weights_rejected(self):
        proof = copy.deepcopy(PROOF)
        proof['nodes'][0]['weights'] = []
        with self.assertRaises(ValueError):
            replay(proof, ROWS, len(SOURCE['states']), CONTEXT)

    def test_invalid_row_rejected(self):
        proof = copy.deepcopy(PROOF)
        proof['nodes'][0]['weights'][0][0] = -1
        with self.assertRaises(ValueError):
            replay(proof, ROWS, len(SOURCE['states']), CONTEXT)

    def test_pending_leaf_rejected(self):
        proof = copy.deepcopy(PROOF)
        proof['nodes'][0] = {'type': 'pending'}
        with self.assertRaises(ValueError):
            replay(proof, ROWS, len(SOURCE['states']), CONTEXT)

    def test_changed_context_rejected(self):
        proof = copy.deepcopy(PROOF)
        proof['missing'] = proof['missing'][1:]
        with self.assertRaises(ValueError):
            replay(proof, ROWS, len(SOURCE['states']), CONTEXT)

    def test_shared_branch_child_rejected(self):
        proof = copy.deepcopy(PROOF)
        proof['nodes'] = [{'type': 'branch', 'vertex': 0, 'zero': 1, 'one': 1}, CUT['leaf']]
        with self.assertRaises(ValueError):
            replay(proof, ROWS, len(SOURCE['states']), CONTEXT)


if __name__ == '__main__':
    unittest.main()

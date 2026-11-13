#!/usr/bin/env python3
"""Source-binding and finite-replay rejection controls; no tracked input edits."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = load('normalization_check', HERE / 'check.py')
replayer = load('normalization_example_replay', HERE / 'replay.py')


class RejectionControls(unittest.TestCase):
    def test_changed_bundle_digest_is_rejected(self):
        manifest = copy.deepcopy(checker.preflight())
        manifest['bundle_inputs']['Normalization.lean'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Changed bundle input: Normalization.lean'):
            checker.preflight(manifest)

    def test_changed_external_digest_is_rejected(self):
        manifest = copy.deepcopy(checker.preflight())
        manifest['external_inputs']['lean-toolchain'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Changed external input: lean-toolchain'):
            checker.preflight(manifest)

    def test_old_invalid_domain_is_rejected(self):
        report = json.loads((HERE / 'clipping-example.json').read_text())
        report['old_assignment']['labels'][0][3] = 0
        with self.assertRaisesRegex(ValueError, 'Label bounds'):
            replayer.replay(report)

    def test_incorrect_clipping_is_rejected(self):
        report = json.loads((HERE / 'clipping-example.json').read_text())
        report['clipped_assignment']['labels'][0][3] += 1
        with self.assertRaisesRegex(ValueError, 'Clipped assignment mismatch'):
            replayer.replay(report)

    def test_complete_example(self):
        result = replayer.replay()
        self.assertEqual(result['changed_labels'], 15)
        self.assertEqual(result['eights_checked_per_assignment'], 165)


if __name__ == '__main__':
    unittest.main()

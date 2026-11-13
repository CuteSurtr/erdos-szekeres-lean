#!/usr/bin/env python3
"""Source-binding rejection controls; never changes a tracked input."""
import copy
import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('rank_attainment_check', HERE / 'check.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class SourceBindingControls(unittest.TestCase):
    def test_changed_bundle_digest_is_rejected(self):
        manifest = copy.deepcopy(checker.preflight())
        manifest['bundle_inputs']['RankAttainment.lean'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Changed bundle input: RankAttainment.lean'):
            checker.preflight(manifest)

    def test_changed_external_digest_is_rejected(self):
        manifest = copy.deepcopy(checker.preflight())
        manifest['external_inputs']['lean-toolchain'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Changed external input: lean-toolchain'):
            checker.preflight(manifest)


if __name__ == '__main__':
    unittest.main()

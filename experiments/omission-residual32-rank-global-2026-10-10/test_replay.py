"""Rejection controls for catalog identity and component coverage claims."""
import gzip
import json
from pathlib import Path
import tempfile
import unittest

import replay


class ReplayControls(unittest.TestCase):
    def test_archived_replay(self):
        self.assertEqual(replay.check()['component_survivors'], [306, 16, 16, 16, 0])

    def test_changed_new_row_is_rejected(self):
        data = replay.build()
        data['constraints'][-1]['rhs'] = 0
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'changed.json.gz'
            path.write_bytes(gzip.compress(json.dumps(data).encode(), mtime=0))
            with self.assertRaisesRegex(ValueError, 'Catalog differs'):
                replay.check_catalog(path)

    def test_false_component_elimination_is_rejected(self):
        report = replay.coverage()
        report['survivors_after_each_prefix'][1] = 0
        with self.assertRaisesRegex(ValueError, 'Coverage report differs'):
            replay.check_coverage_report(report)


if __name__ == '__main__':
    unittest.main()

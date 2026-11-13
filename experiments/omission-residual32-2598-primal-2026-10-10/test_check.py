#!/usr/bin/env python3
"""Negative controls for the standalone exact catalog checker."""
import copy
import gzip
import unittest

import check


class CorruptionTests(unittest.TestCase):
    def setUp(self):
        d = check.HERE
        self.base = check.json.loads(gzip.decompress((check.ROOT / "experiments/omission-residual32-research-2026-10-10/source.json.gz").read_bytes()))
        self.middle = check.json.loads(gzip.decompress((d / "source-2471.json.gz").read_bytes()))
        self.source = check.json.loads(gzip.decompress((d / "source-2598.json.gz").read_bytes()))
        self.family = check.read_json(d / "fourth-row-bindings.json")
        self.bindings = check.read_json(d / "family-source-manifest.json")["bindings"]
        self.candidate = check.read_json(d / "candidates.json")["candidates"][2]

    def validate(self):
        check.validate_catalog(self.base, self.middle, self.source, self.family, self.bindings)

    def test_unchanged_bundle(self):
        self.assertTrue(check.check()["complete"])

    def test_modified_prefix_rejected(self):
        self.source["constraints"][0]["rhs"] += 1
        with self.assertRaisesRegex(ValueError, "middle prefix"):
            self.validate()

    def test_wrong_sixth_row_rejected(self):
        self.source["constraints"][2469]["rhs"] = 0
        self.middle["constraints"][2469]["rhs"] = 0
        with self.assertRaisesRegex(ValueError, "Sixth row"):
            self.validate()

    def test_noninjective_mapping_rejected(self):
        self.family["rows"][0]["mapping"][0] = self.family["rows"][0]["mapping"][1]
        with self.assertRaisesRegex(ValueError, "Fourth injection"):
            self.validate()

    def test_changed_mapping_image_rejected(self):
        self.family["rows"][0]["mapping"][0] = 0
        with self.assertRaisesRegex(ValueError, "Fourth mapping image"):
            self.validate()

    def test_reordered_global_binding_rejected(self):
        self.bindings[1]["source_row"] = 2472
        with self.assertRaisesRegex(ValueError, "Fourth manifest mapping"):
            self.validate()

    def test_duplicate_hole_rejected(self):
        self.candidate["holes"][0] = self.candidate["holes"][1]
        with self.assertRaisesRegex(ValueError, "32 distinct holes"):
            check.replay_candidate(self.source["constraints"], self.candidate)

    def test_false_witness_claim_rejected(self):
        self.candidate["expected_violations"] = []
        with self.assertRaisesRegex(ValueError, "candidate violations"):
            check.replay_candidate(self.source["constraints"], self.candidate)

    def test_false_local_repair_count_rejected(self):
        record = copy.deepcopy(check.read_json(check.HERE / "repair-best-final.json"))
        record["two_exchange_trials"] += 1
        with self.assertRaisesRegex(ValueError, "local-repair trial count"):
            check.replay_two_exchange(self.source["constraints"], record)


if __name__ == "__main__":
    unittest.main()

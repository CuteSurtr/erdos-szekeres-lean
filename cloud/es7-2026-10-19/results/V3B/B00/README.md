# V3B B00 (shard 0 of 16)

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`).
- F.cnf sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (regenerated, matches).
- Input commit Z = 066eaa9; verify/v3 at bdf319c.
- Manifest: leaves 35153, cases with leaves 253, problems 0. M.jsonl sha256 22b6f6a782cd2b2e6319c61c7bc7029032d10aa5fd583dcfbba47ec627e1c549; C.jsonl sha256 cd03dd0a81aec5d738a2ef5e6f817a1c151f4b9141b0ca5a3f0546978a7e1fbe.
- VERIFIED keys removed: 10121 (from 21 JSONL files under V3T and V3A; no V3B out.jsonl at Z). Mt.jsonl n = 25032, sha256 605e39d27b8a11c8b8de36b167d1760f91dc3e6c4e49a2e570bf607689e7cfe7 (same as other V3B machines).
- Shard 0 of 16: 1565 leaves. Run: `v3_check.py ... --shard 0 --nshards 16 --skip-covers --jobs 4 --cap 1800`, 11:27 to about 14:00 UTC.

## Results

| verdict | count |
|---|---|
| VERIFIED | 1565 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |

Unchecked leaves in this shard: 0. Every record has `cake_lpr` = `s VERIFIED UNSAT`. No step-5 rechecks were needed (no REJECTED records with an empty cake_lpr field).

Times (seconds, over 1565 leaves):
- solve: sum 29966.9, median 11.06, max 297.98
- check: sum 6573.0, median 3.08, max 21.65

No SAT, REJECTED or TIMEOUT leaves.

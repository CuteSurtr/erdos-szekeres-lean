# V3B B13 (shard 13 of 16)

Second acceptance pass of mirror sub-case (ii), per results/V3B/TASK.md at 066eaa9.

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: s VERIFIED UNSAT). See tools.txt.
- F.cnf regenerated: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit Z = 066eaa9; verify/v3 at bdf319c.
- Manifest: v3_manifest printed leaves 35153, cases with leaves 253, problems 0. M.jsonl sha256 22b6f6a782cd2b2e6319c61c7bc7029032d10aa5fd583dcfbba47ec627e1c549.
- VERIFIED keys from V3T/** and V3A/*/out.jsonl (no V3B out.jsonl at Z): 10121. Mt.jsonl n = 25032, sha256 605e39d27b8a11c8b8de36b167d1760f91dc3e6c4e49a2e570bf607689e7cfe7 (script: mkMt.py).
- Run: v3_check.py --shard 13 --nshards 16 --skip-covers --jobs 4 --cap 1800, from 11:3x to about 13:50 UTC.

## Results (out.jsonl, 1564 records)

| verdict | count |
|---|---|
| VERIFIED | 1564 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |

Unchecked leaves in this shard: 0 of 1564. Every record has cake_lpr = "s VERIFIED UNSAT". No rechecks were needed (step 5).

Times (s): solve sum 27572.7, median 10.67, max 358.97; check sum 6415.8, median 3.01, max 26.47.

Note: one progress push (1152 leaves) was rejected by a concurrent ref update and went to claude/es7-v3b-b13. It was then pushed to es7-cloud after a retry. Everything is on es7-cloud.

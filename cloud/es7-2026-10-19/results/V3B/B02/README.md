# V3B B02: shard 2 of 16, second acceptance pass of mirror sub-case (ii)

- Input commit Z = 066eaa9 (worktree /opt/in); verify/v3 at bdf319c (worktree /opt/v3src).
- Tools (details in tools.txt): CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`).
- F.cnf sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches the expected value).
- Manifest (details in inputs.txt): WAVE1 119 dirs / 30151 leaf lines / 71 skipped records; WAVE2 86 / 5156 / 0; WAVE3 5 / 232 / 0. v3_manifest: 35153 leaves, 253 cases with leaves, 0 problems.
  - M.jsonl sha256 22b6f6a782cd2b2e6319c61c7bc7029032d10aa5fd583dcfbba47ec627e1c549
  - C.jsonl sha256 cd03dd0a81aec5d738a2ef5e6f817a1c151f4b9141b0ca5a3f0546978a7e1fbe (450 lines)
  - Step 3: 21 JSONL files scanned, 10121 distinct VERIFIED keys, so Mt.jsonl has n = 25032 records, sha256 605e39d27b8a11c8b8de36b167d1760f91dc3e6c4e49a2e570bf607689e7cfe7. This is the same as B10's Mt.jsonl.
- Run: `v3_check.py --shard 2 --nshards 16 --skip-covers --jobs 4 --cap 1800`. The log says "shard 2 of 16 leaves 1565 covers 12". Covers were skipped as the task says.

## Results (out.jsonl)

| verdict | count |
|---|---|
| VERIFIED | 1565 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |

- 1565 of 1565 shard leaves were checked, so none are unchecked. They cover 102 distinct cases. Every leaf returned rc 20, and cake_lpr printed `s VERIFIED UNSAT` for each.
- No REJECTED leaf had an empty cake_lpr field, so no step-5 rechecks were needed.
- Solve time: sum 26374.6 s, median 9.95 s, max 267.92 s.
- Check time: sum 6158.9 s, median 2.95 s, max 20.26 s.
- Wall time: 11:32 to 13:48 UTC on 2026-10-20.

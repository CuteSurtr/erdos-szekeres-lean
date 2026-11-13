# V3B B05: shard 5 of 16, second acceptance pass of mirror sub-case (ii)

- Tools (tools.txt): CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`).
- F regenerated, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit Z = 066eaa9; verify/v3 at bdf319c.
- Manifest (inputs.txt): WAVE1 30151 leaf lines (71 skipped records), WAVE2 5156, WAVE3 232; v3_manifest: 35153 leaves, 253 cases, 0 problems.
  M.jsonl sha256 22b6f6a782cd2b2e6319c61c7bc7029032d10aa5fd583dcfbba47ec627e1c549, C.jsonl sha256 cd03dd0a81aec5d738a2ef5e6f817a1c151f4b9141b0ca5a3f0546978a7e1fbe.
- Step 3 (mkmt.py): 21 files, 11308 VERIFIED leaf records, 10121 distinct keys; n = 25032;
  Mt.jsonl sha256 605e39d27b8a11c8b8de36b167d1760f91dc3e6c4e49a2e570bf607689e7cfe7 (same as B00).
- Shard 5 of 16: 1565 leaves (--skip-covers, --jobs 4, --cap 1800).

## Result

| verdict | count |
|---|---|
| VERIFIED | 1565 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |
| unchecked | 0 |

Every record has `cake_lpr` = `s VERIFIED UNSAT`; no step-5 rechecks were needed.

Times over 1565 leaves: solve sum 26701.6 s, median 9.87 s, max 343.91 s; check sum 6094.3 s, median 2.92 s, max 22.62 s.
Wall time of the run: 12:40 to about 15:00 UTC on 2026-10-20.

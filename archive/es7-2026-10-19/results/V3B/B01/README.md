# V3B B01: shard 1 of 16, second acceptance pass of mirror sub-case (ii)

## Setup
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, built from source as /opt/bin/cadical
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`). Its bundled example prints `s VERIFIED UNSAT`
- F.cnf regenerated from source: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches)
- Input commit Z = 066eaa98. verify/v3 commit = bdf319cf
- Machine: 4 cores, 15 GB RAM (env.txt)

## Manifest
- jtree1 (WAVE1): 119 dirs, 30151 leaf lines, 71 records skipped. jtree2 (WAVE2): 86 dirs, 5156 leaf lines. jtree3 (WAVE3): 5 dirs, 232 leaf lines
- v3_manifest: 35153 leaves, 253 cases with leaves, 0 problems. sha256(M.jsonl) = 22b6f6a782cd2b2e6319c61c7bc7029032d10aa5fd583dcfbba47ec627e1c549
- 10121 VERIFIED keys found (V3T/**/*.jsonl and V3A/*/out.jsonl; there was no V3B out.jsonl at Z). All 10121 matched manifest records and were removed
- Mt.jsonl: n = 25032, sha256 605e39d27b8a11c8b8de36b167d1760f91dc3e6c4e49a2e570bf607689e7cfe7 (script: mt.py)

## Results (shard 1: idx % 16 == 1, 1565 leaves)
- VERIFIED 1565, REJECTED 0, SAT 0, TIMEOUT 0. Unchecked: 0
- Every record has cake_lpr = `s VERIFIED UNSAT`. No rechecks were needed (step 5)
- solve_s: sum 26897.4 s, median 10.12 s, max 298.48 s
- check_s: sum 6348.6 s, median 2.99 s, max 23.4 s
- Run: v3_check.py --shard 1 --nshards 16 --skip-covers --jobs 4 --cap 1800, wall time about 2h20m

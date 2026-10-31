# V3B B10 — shard 10 of 16, second acceptance pass of mirror sub-case (ii)

Result: all 1564 leaves in shard 10 were VERIFIED by cake_lpr (`s VERIFIED UNSAT`). None was REJECTED, SAT or TIMEOUT, and none is left unchecked.

## Setup
- Input commit Z = 066eaa9 (worktree /opt/in). verify/v3 is at commit bdf319c (worktree /opt/v3src).
- CaDiCaL 3.0.1 is at commit c60730422e758ef1cebe7aeddf2dda31c996bf04. cake_lpr is at commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, and its bundled example prints `s VERIFIED UNSAT`. Both were built from source (see tools.txt).
- F.cnf sha256 is 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d, which matches the expected value.
- Machine: 4 cores, 15 GB RAM (env.txt).

## Manifest (inputs.txt)
- v3_jsonl_leaves: WAVE1 has 119 dirs and 30151 leaf lines (71 records skipped). WAVE2 has 86 dirs and 5156 lines. WAVE3 has 5 dirs and 232 lines.
- v3_manifest: 35153 leaves in 253 cases, 0 problems.
  - M.jsonl sha256: 22b6f6a782cd2b2e6319c61c7bc7029032d10aa5fd583dcfbba47ec627e1c549
  - C.jsonl sha256: cd03dd0a81aec5d738a2ef5e6f817a1c151f4b9141b0ca5a3f0546978a7e1fbe
- Already-verified keys came from 21 files: results/V3T/**/*.jsonl and results/V3A/*/out.jsonl. At Z there was no V3B out.jsonl yet. These files hold 11308 VERIFIED leaf records, which give 10121 distinct (case, json.dumps(lits)) keys. All 10121 keys were in M and were removed.
- Mt.jsonl: n = 25032, sha256 605e39d27b8a11c8b8de36b167d1760f91dc3e6c4e49a2e570bf607689e7cfe7. The script that built it is mkMt.py.

## Run
- Command: `v3_check.py --shard 10 --nshards 16 --skip-covers --jobs 4 --cap 1800`. It ran from 11:27 to 13:47 UTC and finished on its own.
- Leaves in this shard: 1564, spread over 98 cases.
- Verdicts: 1564 VERIFIED, 0 REJECTED, 0 SAT, 0 TIMEOUT. Unchecked: 0.
- Step 5 rechecks: none were needed, because no REJECTED leaf has an empty cake_lpr field.
- Solve time: sum 27534.4 s, median 10.11 s, max 318.64 s.
- Check time: sum 5951.1 s, median 2.81 s, max 21.84 s.

## Files
- out.jsonl: one record per leaf. It is a copy of /opt/work/out/out.jsonl.
- run.log: the checker's output.

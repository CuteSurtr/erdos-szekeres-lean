# V3B B07 (shard 7 of 16)

Second acceptance pass of mirror sub-case (ii), following `results/V3B/TASK.md` (commit 066eaa9) with V=B07, i=7, N=16, H=3, Z=066eaa9.

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04 (built from source, /opt/bin/cadical)
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`); its bundled example prints `s VERIFIED UNSAT`
- verify/v3 at commit bdf319c; input commit 066eaa98a68e7c4a7f9b7cea24380deef7e8b2e4
- F regenerated (gen_etv.py + mirgen.py --interior --yflip-unit): sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches)
- Leaf lines extracted: WAVE1 30151 (119 dirs, 71 skipped records), WAVE2 5156 (86 dirs), WAVE3 232 (5 dirs)
- M.jsonl: 35153 leaves, 253 cases with leaves, 0 problems, sha256 22b6f6a782cd2b2e6319c61c7bc7029032d10aa5fd583dcfbba47ec627e1c549
- C.jsonl: 450 cases, sha256 cd03dd0a81aec5d738a2ef5e6f817a1c151f4b9141b0ca5a3f0546978a7e1fbe
- VERIFIED keys from V3T and V3A (no V3B out.jsonl existed at Z): 10121, all of them found in M and removed
- Mt.jsonl: n = 25032, sha256 605e39d27b8a11c8b8de36b167d1760f91dc3e6c4e49a2e570bf607689e7cfe7 (script: `mkmt.py`)

## Result
- This shard: 1565 leaves (idx % 16 == 7) across 100 cases. All 1565 were checked; none are left unchecked.
- Verdicts: VERIFIED 1565, REJECTED 0, SAT 0, TIMEOUT 0. Every VERIFIED record has cake_lpr output exactly `s VERIFIED UNSAT`.
- No REJECTED record has an empty cake_lpr field, so step 5 needed no re-checks.
- Solve time: sum 25013.5 s, median 9.55 s, max 312.47 s.
- Check time: sum 5451.0 s, median 2.67 s, max 23.01 s.
- Run: `v3_check.py ... --shard 7 --nshards 16 --skip-covers --jobs 4 --cap 1800`, 11:28 to 13:35 UTC on 2026-10-20, 4 cores, 15 GB RAM.

Files: env.txt, tools.txt, inputs.txt, mkmt.py, out.jsonl (1565 records).

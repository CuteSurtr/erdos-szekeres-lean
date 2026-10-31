# V3B B09 — shard 9 of 16, second acceptance pass of mirror sub-case (ii)

Result: all 1564 leaves of this shard VERIFIED (cake_lpr printed `s VERIFIED UNSAT` for each). No SAT, REJECTED or TIMEOUT. 0 leaves unchecked.

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04 (/opt/bin/cadical)
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`); bundled example prints `s VERIFIED UNSAT`
- verify/v3 from commit bdf319c; input commit Z = 066eaa9
- F = m33k7int.sub.cnf regenerated (gen_etv.py 33 7 7 7 --mirror, then mirgen.py --interior --yflip-unit), sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches)

## Manifest
- v3_jsonl_leaves: WAVE1 dirs 119, leaf lines 30151, skipped records 71; WAVE2 dirs 86, 5156, 0; WAVE3 dirs 5, 232, 0
- v3_manifest: leaves 35153, cases with leaves 253, problems 0
- M.jsonl sha256 22b6f6a782cd2b2e6319c61c7bc7029032d10aa5fd583dcfbba47ec627e1c549
- C.jsonl sha256 cd03dd0a81aec5d738a2ef5e6f817a1c151f4b9141b0ca5a3f0546978a7e1fbe
- VERIFIED keys from V3T and V3A (21 JSONL files; no V3B out.jsonl at Z): 10121, all present in M and removed
- Mt.jsonl: n = 25032, sha256 605e39d27b8a11c8b8de36b167d1760f91dc3e6c4e49a2e570bf607689e7cfe7 (same as B04 and B13)

## Run
`v3_check.py --root $ROOT --base /opt/work/F.cnf --manifest /opt/work/Mt.jsonl --shard 9 --nshards 16 --skip-covers --out /opt/work/out/out.jsonl --work /opt/work/v3w --jobs 4 --cap 1800` (with the default --cadical /opt/bin/cadical --cake /opt/bin/cake_lpr passed explicitly). Started 11:26 UTC, done 13:56 UTC.

- Shard leaves: 1564 (97 cases). Records in out.jsonl: 1564, matching exactly the shard's (case, lits) set.
- Verdicts: VERIFIED 1564, REJECTED 0, SAT 0, TIMEOUT 0. All rc = 20.
- No REJECTED with empty cake_lpr, so no step-5 rechecks.
- Solve time (s): sum 29890.8, median 11.69, max 382.59
- Check time (s): sum 6016.1, median 2.85, max 25.07

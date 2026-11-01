# V3B B11: shard 11 of 16, second acceptance pass of mirror sub-case (ii)

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04 (/opt/bin/cadical)
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`). Its bundled example printed `s VERIFIED UNSAT`.
- F = regenerated `m33k7int.sub.cnf`, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches)
- Input commit Z = 066eaa9; verify/v3 at bdf319c
- v3_jsonl_leaves: WAVE1 dirs 119, leaf lines 30151, skipped 71; WAVE2 dirs 86, leaf lines 5156, skipped 0; WAVE3 dirs 5, leaf lines 232, skipped 0
- v3_manifest: leaves 35153, cases with leaves 253, problems 0. M.jsonl sha256 22b6f6a782cd2b2e6319c61c7bc7029032d10aa5fd583dcfbba47ec627e1c549
- VERIFIED keys from V3T (all *.jsonl, recursive) and V3A/*/out.jsonl (there was no V3B out.jsonl at Z): 21 files, 10121 distinct keys
- Mt.jsonl: n = 25032, sha256 605e39d27b8a11c8b8de36b167d1760f91dc3e6c4e49a2e570bf607689e7cfe7 (made by `mkmt.py`)

## Run
`v3_check.py --shard 11 --nshards 16 --skip-covers --jobs 4 --cap 1800`, from 11:27 to 14:02 UTC.
This shard has 1564 leaves (idx % 16 == 11).

## Results
- VERIFIED 1564, REJECTED 0, SAT 0, TIMEOUT 0. Unchecked: 0.
- Every record has `cake_lpr` = `s VERIFIED UNSAT`, so no step-5 rechecks were needed.
- Solve time: sum 30788.0 s, median 11.2 s, max 392.7 s
- Check time: sum 5678.0 s, median 2.7 s, max 33.0 s

No SAT, REJECTED or TIMEOUT leaves.

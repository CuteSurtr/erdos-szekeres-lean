# V3B B15: shard 15 of 16, second acceptance pass of mirror sub-case (ii)

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (its bundled example prints `s VERIFIED UNSAT`). See tools.txt.
- F (`m33k7int.sub.cnf`, regenerated): sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit 066eaa98a68e7c4a7f9b7cea24380deef7e8b2e4; verify/v3 at bdf319c.
- Manifest: 35153 leaves, 253 cases with leaves, 0 problems; M.jsonl sha256 22b6f6a782cd2b2e6319c61c7bc7029032d10aa5fd583dcfbba47ec627e1c549.
- VERIFIED keys from V3T and V3A (there were no V3B out.jsonl files at the input commit): 10121. Mt.jsonl: n = 25032, sha256 605e39d27b8a11c8b8de36b167d1760f91dc3e6c4e49a2e570bf607689e7cfe7.
- Shard 15 (idx mod 16 = 15): 1564 leaves. Ran with `--skip-covers --jobs 4 --cap 1800`.

## Result
- Leaf verdicts: VERIFIED 1564, REJECTED 0, SAT 0, TIMEOUT 0. Unchecked: 0.
- Every record's cake_lpr line is exactly `s VERIFIED UNSAT`. Each key appears once, and every idx in this shard of Mt.jsonl has a record.
- No REJECTED leaf has an empty cake_lpr field, so there were no step-5 rechecks.
- Solve time: sum 29350.0 s, median 10.91 s, max 326.88 s.
- Check time: sum 6627.7 s, median 3.07 s, max 23.28 s.
- Wall time: 11:31 to about 14:05 UTC on 2026-10-20 (4 cores, 15 GB RAM).

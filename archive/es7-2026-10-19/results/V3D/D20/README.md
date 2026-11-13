# V3D D20 (shard 20 of 24)

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`). See tools.txt.
- F = regenerated `m33k7int.sub.cnf`, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit a71d30d5; verify/v3 at bdf319c.
- Work list `results/V3D/worklist.jsonl`: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (both match).
- Cross-check at 3e4dbaae3: v3_manifest gives 70215 leaves, 0 problems, sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8 (matches); all 22682 work-list (case, lits) occur in it. See inputs.txt.

## Result

Run: `v3_check.py --shard 20 --nshards 24 --skip-covers --jobs 4 --cap 1800`, 16:19 to about 17:31 UTC on 4 cores, completed.

| verdict | count |
|---|---|
| VERIFIED | 945 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |
| unchecked | 0 |

All 945 shard leaves (exactly the work-list records with idx ≡ 20 mod 24) have a record whose cake_lpr line is `s VERIFIED UNSAT`. No REJECTED leaf with an empty cake_lpr field, so no step-4 rechecks.

Times: solve sum 13594.3 s, median 9.10 s, max 186.44 s; check sum 3237.7 s, median 2.62 s, max 19.20 s.

No SAT, REJECTED or TIMEOUT leaves.

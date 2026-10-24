# V3E E07 (shard 7 of 8)

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04, cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`).
- F = m33k7int.sub.cnf regenerated, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit Z = d0456ff; verify/v3 at bdf319c.
- Work list `results/V3E/worklist.jsonl`: sha256 5c10bc043fbacbd397ea5867207b2a3fedebeb0174f98d3590b18c6d564baac9, 3801 lines (match).
- Cross-check at 14447d0d5: manifest Mzd.jsonl 73880 lines, sha256 e01af167266dc044078798355f76f9f8d36c74d1b8843aeab90072b644ea83b5 (matches); every work-list (case, lits) occurs in it (0 of 3801 missing): PASS.
- Run: `v3_check.py --shard 7 --nshards 8 --skip-covers --jobs 4 --cap 1800`, started 2026-10-20 16:39 UTC, finished by 17:30 UTC.

## Results

475 leaves in shard 7 (U3_L 400, U_L7 59, U_L8 10, U_L2 2, U_L6 2, U_L9 2).

| verdict | count |
|---|---|
| VERIFIED | 475 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |

Unchecked: 0. Every record has cake_lpr output `s VERIFIED UNSAT`. No step-4 rechecks were needed.

Times (s): solve sum 7291.98, median 9.70, max 161.39; check sum 2241.51, median 4.05, max 19.80.

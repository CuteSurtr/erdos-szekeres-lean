# V3E E05: shard 5 of 8

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`). See tools.txt.
- F regenerated from source: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit d0456ff; verify/v3 from commit bdf319c.
- Work list `results/V3E/worklist.jsonl`: sha256 5c10bc043fbacbd397ea5867207b2a3fedebeb0174f98d3590b18c6d564baac9, 3801 lines (both match).
- Cross-check at 14447d0d5: Mzd.jsonl sha256 e01af167266dc044078798355f76f9f8d36c74d1b8843aeab90072b644ea83b5, 73880 lines, 0 problems (matches); all 3801 work-list (case, lits) occur in it. See inputs.txt.

## Result

Run: `v3_check.py --shard 5 --nshards 8 --skip-covers --jobs 4 --cap 1800`, 16:39 to 17:19 UTC. The shard has 475 leaves; the run finished.

| verdict | count |
|---|---|
| VERIFIED (cake_lpr `s VERIFIED UNSAT`) | 475 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |

Unchecked leaves in this shard: 0. No REJECTED leaves with an empty cake_lpr field, so step 4 needed no rechecks.

| time (s) | sum | median | max |
|---|---|---|---|
| solve | 7415.5 | 8.65 | 210.99 |
| check | 1955.1 | 3.15 | 22.27 |

No SAT, REJECTED or TIMEOUT leaves. Records are in out.jsonl.

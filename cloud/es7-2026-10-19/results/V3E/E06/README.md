# V3E E06: shard 6 of 8

Fifth acceptance pass of mirror sub-case (ii), task `results/V3E/TASK.md` at d0456ff.

## Setup
- CaDiCaL 3.0.1 at commit c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa. The bundled example printed `s VERIFIED UNSAT`.
- F regenerated from source: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit d0456ff. verify/v3 commit bdf319c.
- Work list `results/V3E/worklist.jsonl`: sha256 5c10bc043fbacbd397ea5867207b2a3fedebeb0174f98d3590b18c6d564baac9, 3801 lines (both match).
- Cross-check at 14447d0d5: rebuilt manifest Mzd.jsonl has sha256 e01af167266dc044078798355f76f9f8d36c74d1b8843aeab90072b644ea83b5 with 73880 lines (match). All 3801 work-list (case, lits) pairs occur in it. PASS. Details are in `inputs.txt` and `tools.txt`.

## Result
The run was `v3_check.py --shard 6 --nshards 8 --skip-covers --jobs 4 --cap 1800` and it finished in about 57 minutes.

| verdict | count |
|---|---|
| VERIFIED | 475 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |

- All 475 leaves of this shard were checked. None are still unchecked.
- Every record has `cake_lpr` = `s VERIFIED UNSAT`. No step-4 rechecks were needed.
- Solve time: sum 9381.9 s, median 10.81 s, max 203.87 s.
- Check time: sum 2273.1 s, median 3.59 s, max 23.46 s.
- There were no SAT, REJECTED or TIMEOUT leaves.

The full records are in `out.jsonl`.

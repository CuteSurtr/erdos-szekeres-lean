# V3E E01: shard 1 of 8 (idx mod 8 == 1), fifth acceptance pass of mirror sub-case (ii)

## Setup
- CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`). See tools.txt.
- F regenerated, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit d0456ff; verify/v3 from commit bdf319c.
- Work list sha256 5c10bc043fbacbd397ea5867207b2a3fedebeb0174f98d3590b18c6d564baac9, 3801 lines (match).
- Cross-check at 14447d0d5: rebuilt manifest sha256 e01af167266dc044078798355f76f9f8d36c74d1b8843aeab90072b644ea83b5, 73880 lines (match); all 3801 work-list (case, lits) occur in it. PASS. See inputs.txt.

## Run
`v3_check.py --shard 1 --nshards 8 --skip-covers --jobs 4 --cap 1800`, 16:39 to about 17:20 UTC.

## Results (out.jsonl)
- 475 leaves in this shard, 475 records, all with `cake_lpr` = `s VERIFIED UNSAT`.
- VERIFIED 475, REJECTED 0, SAT 0, TIMEOUT 0. Unchecked: 0.
- Every record's (case, lits) matches the work-list record of the same idx.
- No rechecks were needed (no REJECTED leaf with an empty cake_lpr field).
- Solve time: sum 6957.42 s, median 9.04 s, max 210.69 s.
- Check time: sum 1889.08 s, median 3.14 s, max 20.87 s.

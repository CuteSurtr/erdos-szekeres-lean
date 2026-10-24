# V3E E04: shard 4 of 8

Machine E04, 4 cores, 15 GB RAM. Run 16:38 to about 17:20 UTC on 2026-10-20 (budget 1.5 h).

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, built from source as /opt/bin/cadical.
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, built with `make cake_lpr`. Its bundled example prints `s VERIFIED UNSAT`.
- F regenerated with gen_etv.py and mirgen.py. sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit d0456ff8d6c066abed068224acd10163c6a4c6bf. verify/v3 at bdf319cfb8b20bfacc951a0d6032ceeda85b8bf5.
- Work list `results/V3E/worklist.jsonl`: sha256 5c10bc043fbacbd397ea5867207b2a3fedebeb0174f98d3590b18c6d564baac9, 3801 lines (both match).
- Cross-check at 14447d0d5: Mzd.jsonl has sha256 e01af167266dc044078798355f76f9f8d36c74d1b8843aeab90072b644ea83b5, 73880 lines and 0 problems (matches). All 3801 work-list (case, lits) pairs occur in it. Details are in inputs.txt and tools.txt.

## Results (out.jsonl)
- Shard 4 of 8 has 475 leaves and all of them were checked. None are left unchecked.
- VERIFIED 475, REJECTED 0, SAT 0, TIMEOUT 0.
- No REJECTED leaf has an empty cake_lpr field, so no step-4 rechecks were needed.
- Leaves per case: U3_L 400, U_L7 59, U_L8 11, U_L2 2, U_L5 1, U_L6 1, U_L9 1.
- Solve time: sum 7501.0 s, median 8.41 s, max 239.52 s.
- Check time: sum 1933.7 s, median 3.03 s, max 19.95 s.
- Largest LRAT proof: 206 MB (deleted after the check).

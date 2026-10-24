# V3E E03: shard 3 of 8 (fifth acceptance pass, mirror sub-case (ii))

Run 2026-10-20, 16:39:42 to about 17:34 UTC, on 4 cores with 15 GB RAM. The shard finished inside the 1.5 h budget.

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, at /opt/bin/cadical
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`). The bundled example prints `s VERIFIED UNSAT`.
- F was regenerated with gen_etv.py and mirgen.py. Its sha256 is 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d, which matches the expected value.
- Input commit Z = d0456ff8d6c066abed068224acd10163c6a4c6bf. verify/v3 is taken from commit bdf319cfb8b20bfacc951a0d6032ceeda85b8bf5.
- Work list `results/V3E/worklist.jsonl`: sha256 5c10bc043fbacbd397ea5867207b2a3fedebeb0174f98d3590b18c6d564baac9, 3801 lines. Both match.
- Cross-check at 14447d0d5: Mzd.jsonl has sha256 e01af167266dc044078798355f76f9f8d36c74d1b8843aeab90072b644ea83b5 and 73880 lines, both matching. All 3801 work-list (case, lits) pairs occur in it, so the check passed. See inputs.txt and tools.txt.

## Results (out.jsonl)
- Leaves in shard: 475. VERIFIED 475, REJECTED 0, SAT 0, TIMEOUT 0. Unchecked: 0.
- No REJECTED leaf had an empty cake_lpr field, so step 4 needed no rechecks.
- Solve time (s): sum 8889.7, median 10.31, max 264.87.
- Check time (s): sum 2115.5, median 3.35, max 22.55.
- Leaves by case: U3_L 401, U_L7 60, U_L8 10, and one each for U_L2, U_L5, U_L6 and U_L9.

Command: `v3_check.py --root /opt/in/cloud/es7-2026-10-19 --base /opt/work/F.cnf --manifest $ROOT/results/V3E/worklist.jsonl --shard 3 --nshards 8 --skip-covers --out /opt/work/out/out.jsonl --work /opt/work/v3w --jobs 4 --cap 1800`

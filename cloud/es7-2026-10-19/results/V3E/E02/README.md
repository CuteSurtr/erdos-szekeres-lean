# V3E E02 (shard 2 of 8)

Fifth acceptance pass of mirror sub-case (ii), following `results/V3E/TASK.md` at d0456ff with V = E02, i = 2, N = 8, H = 1.5.

## Setup
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, as /opt/bin/cadical.
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`); the bundled example prints `s VERIFIED UNSAT`.
- F regenerated with gen_etv.py and mirgen.py: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit Z = d0456ff8; verify/v3 at bdf319c.
- Work list `results/V3E/worklist.jsonl`: sha256 5c10bc043fbacbd397ea5867207b2a3fedebeb0174f98d3590b18c6d564baac9, 3801 lines (both match).
- Cross-check at 14447d0d5: v3_manifest gives 73880 leaves, 278 cases with leaves, 0 problems, sha256 e01af167266dc044078798355f76f9f8d36c74d1b8843aeab90072b644ea83b5 (matches). All 3801 work-list (case, lits) pairs occur in it. Details are in inputs.txt.

## Results (`out.jsonl`)
- This shard has 475 leaves (idx % 8 == 2).
- VERIFIED 475, REJECTED 0, SAT 0, TIMEOUT 0. Unchecked: 0. Every record has rc 20 and cake_lpr `s VERIFIED UNSAT`.
- Solve time: sum 6699.7 s, median 8.10 s, max 175.28 s.
- Check time: sum 1824.0 s, median 2.93 s, max 18.94 s.
- No REJECTED leaves with an empty cake_lpr field, so step 4 had nothing to re-check.
- Run: v3_check.py with --jobs 4 --cap 1800 --skip-covers, from 16:41 to about 17:16 UTC on 2026-10-20.

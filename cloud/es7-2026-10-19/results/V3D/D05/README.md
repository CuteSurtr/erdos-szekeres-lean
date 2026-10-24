# V3D D05 (shard 5 of 24)

Fourth acceptance pass of mirror sub-case (ii), task `results/V3D/TASK.md` at a71d30d.

## Setup
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04 (/opt/bin/cadical)
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`); bundled example prints `s VERIFIED UNSAT`
- F regenerated (gen_etv.py + mirgen.py): sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches)
- Input commit a71d30d; verify/v3 at bdf319c
- Work list `results/V3D/worklist.jsonl`: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (matches)
- Cross-check at 3e4dbaae3: v3_manifest gives 70215 leaves, 278 cases, 0 problems, sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8 (matches); all 22682 work-list (case, lits) pairs occur in it. Details in inputs.txt.

## Run
`v3_check.py --shard 5 --nshards 24 --skip-covers --jobs 4 --cap 1800`, 15:24 to 16:52 UTC.

## Results (out.jsonl)
- Leaves in shard: 945. Checked: 945. Unchecked: 0.
- VERIFIED 945, REJECTED 0, SAT 0, TIMEOUT 0. Every record has `cake_lpr` = `s VERIFIED UNSAT`.
- No REJECTED leaf with an empty cake_lpr field, so no step-4 rechecks were needed.
- By case: U_L2 516, U3_L 177, U_L7 119, U_L6 85, U4_L 32, U_L5 16.
- Solve time: sum 14734.06 s, median 9.91 s, max 203.62 s.
- Check time (cake_lpr): sum 3820.49 s, median 3.08 s, max 22.44 s.

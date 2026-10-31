# V3D D10 (shard 10 of 24)

Fourth acceptance pass of mirror sub-case (ii), task `results/V3D/TASK.md` at a71d30d, run 2026-10-20 15:51-17:22 UTC (budget 2.5 h).

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04 (/opt/bin/cadical).
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`); bundled example prints `s VERIFIED UNSAT`.
- F regenerated (gen_etv.py + mirgen.py --interior --yflip-unit): sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit Z = a71d30d; verify/v3 as of commit bdf319c.
- Work list `results/V3D/worklist.jsonl`: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (matches).
- Cross-check at 3e4dbaae3: manifest of WAVE1-4 has 70215 leaves, sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8 (matches), problems 0; all 22682 work-list (case, lits) records occur in it. PASS.

## Results (`out.jsonl`)
- Leaves in shard: 945 (cases U_L2 516, U3_L 177, U_L7 119, U_L6 85, U4_L 32, U_L5 16).
- VERIFIED 945, REJECTED 0, SAT 0, TIMEOUT 0. Every record has cake_lpr `s VERIFIED UNSAT`.
- Still unchecked: 0.
- Solve time: sum 17023.1 s, median 10.36 s, max 313.88 s.
- Check time: sum 3792.7 s, median 2.77 s, max 22.99 s.
- No REJECTED leaves with an empty cake_lpr field, so step 4 had no rechecks to do.

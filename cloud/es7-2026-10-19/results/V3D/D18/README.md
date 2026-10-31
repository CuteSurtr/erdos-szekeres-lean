# V3D D18: shard 18 of 24

Task: `results/V3D/TASK.md` at commit a71d30d, with V = D18, i = 18, N = 24, H = 2.5.

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, built from source.
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`). Its bundled example prints `s VERIFIED UNSAT`.
- F regenerated with gen_etv.py and mirgen.py: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d. This matches TASK.md.
- Input commit a71d30d. verify/v3 taken from commit bdf319c.
- Work list `results/V3D/worklist.jsonl`: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines. This matches TASK.md.
- Cross-check at 3e4dbaae3: v3_manifest.py produced Mzd.jsonl with sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8 (70215 lines, 0 problems). Every (case, lits) in the work list occurs in Mzd.jsonl (0 of 22682 missing). Result: OK.

## Run
`v3_check.py --shard 18 --nshards 24 --skip-covers --jobs 4 --cap 1800`, run from 16:18 to about 17:45 UTC on 2026-10-20 on 4 cores with 15 GB RAM.

## Results (out.jsonl)
- Leaves in this shard: 945. Checked: 945. Unchecked: 0.
- VERIFIED: 945. REJECTED: 0. SAT: 0. TIMEOUT: 0. Every record has the cake_lpr line `s VERIFIED UNSAT`.
- No record was REJECTED with an empty cake_lpr field, so step 4 needed no rechecks.
- Solve time: sum 16501.9 s, median 9.76 s, max 238.13 s.
- Check time: sum 4085.4 s, median 3.07 s, max 23.77 s.
- There were no SAT, REJECTED or TIMEOUT leaves.

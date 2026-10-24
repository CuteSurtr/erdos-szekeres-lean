# V3D D22: shard 22 of 24 (fourth acceptance pass, mirror sub-case (ii))

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`). See tools.txt.
- F = regenerated `m33k7int.sub.cnf`, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit a71d30d; verify/v3 at bdf319c.
- Work list `results/V3D/worklist.jsonl`: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (matches).
- Cross-check at 3e4dbaae3: Mzd.jsonl sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8, 70215 lines (matches); all 22682 work-list (case, lits) occur in it. See inputs.txt.

## Result

Run: `v3_check.py --shard 22 --nshards 24 --skip-covers --jobs 4 --cap 1800`, 16:21 to 17:38 UTC on 4 cores.

| verdict | leaves |
|---|---|
| VERIFIED (`s VERIFIED UNSAT`) | 945 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |
| unchecked | 0 |

All 945 leaves of shard 22 are checked, with 945 distinct keys. Cases: U_L2 516, U3_L 176, U_L7 120, U_L6 84, U4_L 32, U_L5 17.

Times (seconds): solve sum 15006.8, median 9.65, max 249.68; check sum 3709.7, median 2.97, max 27.74. Largest proof 227.9 MB (not committed).

There were no SAT, REJECTED or TIMEOUT leaves, so no re-checks (step 4) were needed.

Records: out.jsonl.

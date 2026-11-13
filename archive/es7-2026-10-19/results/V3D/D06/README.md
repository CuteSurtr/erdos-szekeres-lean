# V3D D06: shard 6 of 24

- Tools built from source: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04, cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`). See `tools.txt`.
- F regenerated: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Inputs at commit a71d30d; verify/v3 at bdf319c.
- Work list sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (matches).
- Cross-check at 3e4dbaae3: manifest 70215 lines, sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8 (matches), 278 cases, 0 problems; all 22682 work-list (case, lits) occur in it. See `inputs.txt`.

## Result

Shard 6 (idx mod 24 == 6): 945 leaves, all checked.

| verdict | count |
|---|---|
| VERIFIED | 945 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |

Unchecked: 0. No REJECTED leaf with an empty `cake_lpr` field, so no rechecks (step 4) were needed.

By case: U_L2 516, U3_L 177, U_L7 119, U_L6 85, U4_L 32, U_L5 16.

Times (seconds): solve sum 14910.3, median 9.91, max 303.83; check sum 3815.6, median 3.04, max 25.08.

Run: `v3_check.py --shard 6 --nshards 24 --skip-covers --jobs 4 --cap 1800`, 15:46 to 16:43 UTC 2026-10-20 on 4 cores, 15 GB RAM. Output in `out.jsonl`.

# V3D D23 (shard 23 of 24)

- Tools: CaDiCaL 3.0.1 commit c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`).
- F.cnf regenerated: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit a71d30d; verify/v3 from commit bdf319c.
- Work list `results/V3D/worklist.jsonl`: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (match).
- Cross-check at 3e4dbaae3: Mzd.jsonl sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8, 70215 lines (match); all 22682 work-list (case, lits) occur in it. PASS. Details in inputs.txt.

## Run

`v3_check.py --shard 23 --nshards 24 --skip-covers --jobs 4 --cap 1800`, 16:22 to 17:45 UTC.

| verdict | count |
|---|---|
| VERIFIED | 945 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |

Shard leaves: 945; unchecked: 0. No REJECTED leaf with empty cake_lpr, so no rechecks (step 4) were needed.

| time (s) | sum | median | max |
|---|---|---|---|
| solve | 16680.8 | 10.21 | 255.24 |
| check (cake_lpr) | 3847.6 | 2.94 | 23.07 |

No SAT, REJECTED or TIMEOUT leaves.

# V3D D11: shard 11 of 24

Fourth acceptance pass of mirror sub-case (ii), task `results/V3D/TASK.md` at commit a71d30d.

- Tools, built from source: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`).
- F regenerated (gen_etv.py + mirgen.py --interior --yflip-unit): sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit a71d30d, verify/v3 at bdf319c.
- Work list `results/V3D/worklist.jsonl`: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (matches).
- Cross-check at 3e4dbaae3: Mzd.jsonl sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8, 70215 lines, 0 problems (matches); all 22682 work-list (case, lits) occur in it. Details in inputs.txt.

## Result

Run: `v3_check.py --shard 11 --nshards 24 --skip-covers --jobs 4 --cap 1800`, 15:54 to 17:29 UTC, finished.

| verdict | leaves |
|---|---|
| VERIFIED | 945 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |

Shard size 945; unchecked: 0. Every record has cake_lpr output `s VERIFIED UNSAT`. No rechecks were needed (no REJECTED leaf with empty cake_lpr field).

| time (s) | sum | median | max |
|---|---|---|---|
| solve | 18689.1 | 10.82 | 356.42 |
| check | 3903.7 | 2.75 | 26.23 |

No SAT, REJECTED or TIMEOUT leaves. Records: `out.jsonl`.

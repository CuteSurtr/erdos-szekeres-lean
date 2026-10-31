# C2P2 M03: shard j = 3 of N = 42 of C2P2.tsv (H = 2.5 h, TASK at d266d2c3)

Start 2026-10-31 06:47:40 UTC (epoch 1793429260), END = 1793437360 (09:02:40 UTC). One lane (`run.sh`); the lane stopped at 08:49:34 with 785 s left (< 900 s MIN_START).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 vendored files match `MANIFEST.sha256`. It built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc + E2 patch). Nothing was cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…bf472b48`. Both match.
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (8 in the shard: idx 3, 45, 87, 129, 171, 213, 255, 297)
| unit | case | kind | cap s | status | solve s | RSS MB | proof GB | lrat-check s | cake_lpr s | certified |
|---|---|---|---|---|---|---|---|---|---|---|
| P8_1-11 | P8 | Q | 6000 | UNSAT | 4327.4 | 4386 | 8.84 | 132.8 | 680.4 | yes |
| P6_1-2-7 | P6 | H | 1800 | UNSAT | 230.6 | 4390 | 3.20 | 50.2 | 291.3 | yes |
| P6_1-7-11 | P6 | H | 1586 | UNSAT | 445.1 | 4399 | 3.58 | 52.1 | 311.0 | yes |
| P6_1-13-15 | P6 | H | 765 | UNSAT | 231.6 | 4354 | 3.22 | 50.5 | 287.6 | yes |

The caps below the list cap (1586 s and 765 s) come from the lane's END limit. cake_lpr ran with heap 8000 MB for all units.

Counts by case and kind:
- Certified: 4 (P8 Q: 1; P6 H: 3).
- Timed out (UNKNOWN): 0.
- Errors / `certified: false`: 0.
- Not reached: 4 (P6 H: P6_2-8-15, P6_3-7-13, P6_7-10-14, P6_8-13-14).

Certified units, min / median / max:
- solve: 230.6 / 338.4 / 4327.4 s
- lrat-check: 50.2 / 51.3 / 132.8 s
- cake_lpr: 287.6 / 301.2 / 680.4 s
- proof size: 3.20 / 3.40 / 8.84 GB

Largest solver RSS: 4399 MB (P6_1-7-11), as CaDiCaL reported it. cake_lpr peaked at about 8.2 GB RSS.

## SAT, rejections, memory
- No SAT.
- No proof rejection.
- No memory problem.
- Disk: free space fell to 19 GB during P8_1-11, whose proof reached 8.84 GB; there was no shortage.

# C2P5 M75: LIST C2P5B.tsv, shard j = 25 of N = 50, H = 5.25 (TASK commit 81cb025f)

Run 2026-10-31, start 15:24:25Z, END 20:24:25Z (epoch 1793478265); the lane finished all units at 19:30:09Z.

## Tools and checks (details in `tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest of all 196 vendored files matches; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…2b48`, both as expected.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (19 = rows of C2P5B.tsv with idx ≡ 25 mod 50)
- **Certified: 19/19** (all UNSATISFIABLE, lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`).
- Timed out (UNKNOWN): 0. Not reached: 0. Errors / `certified: false`: 0.
- No SAT. No proof rejection. No memory problem: largest solver RSS 4422 MB (P1_3-9); cake_lpr always ran with the 8000 MB heap (no retry needed). Largest proof 5.03 GB; free disk never fell below 23 GB.

| case | kind | certified | other |
|---|---|---|---|
| P1 | H | 5 | 0 |
| P1 | Q | 1 | 0 |
| P2 | H | 6 | 0 |
| P2 | Q | 1 | 0 |
| P3 | H | 5 | 0 |
| P3 | Q | 1 | 0 |

| unit | kind | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|
| P2_4-10 | Q | 1146.91 | 69.7 | 408.6 | 4.37 | 4408 |
| P1_3-9 | Q | 1168.32 | 72.0 | 397.3 | 4.33 | 4422 |
| P2_1-4-5 | H | 245.17 | 55.7 | 302.7 | 3.23 | 4379 |
| P2_3-4-7 | H | 97.64 | 31.1 | 189.1 | 1.46 | 3412 |
| P2_3-7-15 | H | 474.2 | 66.6 | 352.5 | 3.61 | 4369 |
| P2_4-5-12 | H | 204.4 | 50.8 | 292.9 | 3.03 | 4342 |
| P2_4-11-12 | H | 203.26 | 54.4 | 304.7 | 3.14 | 4392 |
| P2_6-7-8 | H | 27.26 | 13.7 | 119.4 | 0.22 | 2650 |
| P1_2-4-14 | H | 349.1 | 56.6 | 314.3 | 3.45 | 4419 |
| P1_2-10-13 | H | 391.28 | 56.2 | 330.8 | 3.35 | 4407 |
| P1_3-7-15 | H | 436.5 | 65.7 | 342.9 | 3.48 | 4379 |
| P1_4-8-11 | H | 80.07 | 25.3 | 172.5 | 1.12 | 3160 |
| P1_6-9-11 | H | 27.73 | 13.9 | 115.2 | 0.22 | 2664 |
| P3_6-12 | Q | 1818.71 | 79.6 | 460.9 | 5.03 | 4405 |
| P3_1-6-12 | H | 610.49 | 61.5 | 357.5 | 3.70 | 4362 |
| P3_1-13-14 | H | 258.24 | 53.4 | 310.2 | 3.24 | 4366 |
| P3_4-9-10 | H | 73.24 | 25.1 | 161.4 | 1.11 | 3159 |
| P3_5-8-13 | H | 230.1 | 52.6 | 311.5 | 3.17 | 4348 |
| P3_6-12-13 | H | 144.55 | 38.4 | 229.3 | 2.05 | 3537 |

- Q (3 units), min / median / max: solve 1146.91 / 1168.32 / 1818.71 s; lrat-check 69.7 / 72 / 79.6 s; cake_lpr 397.3 / 408.6 / 460.9 s; proof 4.33 / 4.37 / 5.03 GB
- H (16 units), min / median / max: solve 27.26 / 217.25 / 610.49 s; lrat-check 13.7 / 53 / 66.6 s; cake_lpr 115.2 / 303.7 / 357.5 s; proof 0.22 / 3.155 / 3.7 GB
- all (19 units), min / median / max: solve 27.26 / 245.17 / 1818.71 s; lrat-check 13.7 / 54.4 / 79.6 s; cake_lpr 115.2 / 310.2 / 460.9 s; proof 0.22 / 3.23 / 5.03 GB
- largest solver RSS: 4422.06 MB (P1_3-9); cake_lpr heap: [8000] MB
- statuses: Counter({'UNSATISFIABLE': 19}); certified 19/19

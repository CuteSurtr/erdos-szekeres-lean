# C2P3 M42

Values: V = M42, LIST = C2P3.tsv, j = 42, N = 50, H = 2.5, Z = 4f653319. Start 09:42:45Z, END 11:57:45Z (1793447865); the lane finished all units at 11:23:06Z.

## Tools and checks (`tools.txt`)

- `C2P/vendor/build_tools.sh` from the vendored sources (manifest: all 196 files match; nothing downloaded): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch).
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf (b0061e90…) and base.json (2476faff…) match.
- Cubes: `l2cubes.py` for P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, `out.jsonl`)

9 units, **9 certified** (UNSAT, lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`), 0 timed out, 0 not reached, 0 errors.

| case | kind | units | certified |
|---|---|---|---|
| P6 | Q | 1 (P6_7-9) | 1 |
| P6 | H | 2 (P6_2-9-10, P6_7-9-13) | 2 |
| P5 | H | 6 (P5_1-2-6, P5_1-7-16, P5_2-3-9, P5_2-11-13, P5_6-10-14, P5_7-13-14) | 6 |

| unit | kind | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|
| P6_7-9 | Q | 580.01 | 57.1 | 351.4 | 3.65 | 4430 |
| P6_2-9-10 | H | 295.11 | 52.7 | 325.3 | 3.26 | 4372 |
| P6_7-9-13 | H | 93.93 | 29.9 | 189.1 | 1.47 | 3401 |
| P5_1-2-6 | H | 223.71 | 49.7 | 303.8 | 3.18 | 4405 |
| P5_1-7-16 | H | 397.20 | 55.8 | 330.6 | 3.56 | 4418 |
| P5_2-3-9 | H | 277.50 | 51.3 | 304.7 | 3.21 | 4392 |
| P5_2-11-13 | H | 318.26 | 53.0 | 320.3 | 3.31 | 4460 |
| P5_6-10-14 | H | 268.97 | 54.0 | 323.9 | 3.19 | 4356 |
| P5_7-13-14 | H | 154.92 | 39.3 | 234.8 | 2.08 | 3610 |

Min / median / max over the 9 certified units: solve 93.9 / 277.5 / 580.0 s; lrat-check 29.9 / 52.7 / 57.1 s; cake_lpr 189.1 / 320.3 / 351.4 s; proof 1.47 / 3.21 / 3.65 GB.

Largest solver RSS: 4460 MB (P5_2-11-13).

No SAT, no proof rejection, no memory or disk problem. The Q unit P6_7-9 (cap 6000) needed only 580 s.

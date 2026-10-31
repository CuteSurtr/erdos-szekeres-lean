# C2P3 M39 (LIST = C2P3.tsv, j = 39, N = 50, H = 2.5, Z = 4f653319)

## Tools and checks
- Built with `C2P/vendor/build_tools.sh` from the vendored `vendor/tools-src.tar.xz` (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch. No code cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers; good LRAT accepted (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…bf472b48`, both as expected.
- Cubes: `l2cubes.py` for a = 1..8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details in `tools.txt`. Lane start 09:45:23Z, END 1793447867 (11:57:47Z); lane finished 11:42:56Z ("stop: 890 s left").

## Units (9 assigned)
| case | kind | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|
| P6 | Q | 1 (P6_2-16) | 0 | 0 | 0 |
| P6 | H | 2 (P6_2-8-13, P6_7-9-10) | 0 | 0 | 0 |
| P5 | Q | 1 (P5_1-2) | 0 | 0 | 0 |
| P5 | H | 3 (P5_1-7-13, P5_2-3-6, P5_2-10-16) | 0 | 2 (P5_6-10-11, P5_7-12-13) | 0 |
| total | | 7 | 0 | 2 | 0 |

All 7 records are UNSATISFIABLE with `"certified": true` (lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT`).

| unit | kind | cap s | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|
| P6_2-16 | Q | 6000 | 1389.35 | 81.5 | 446.9 | 4.87 | 4415.8 |
| P6_2-8-13 | H | 1800 | 662.35 | 64.8 | 365.8 | 3.76 | 4356.0 |
| P6_7-9-10 | H | 1800 | 74.83 | 25.0 | 165.3 | 1.11 | 3152.4 |
| P5_1-2 | Q | 2400 | 861.52 | 66.0 | 359.9 | 4.02 | 4358.7 |
| P5_1-7-13 | H | 1800 | 589.09 | 61.8 | 354.6 | 3.76 | 4367.4 |
| P5_2-3-6 | H | 1693 | 209.47 | 51.8 | 300.0 | 3.13 | 4398.6 |
| P5_2-10-16 | H | 1122 | 413.16 | 61.4 | 344.8 | 3.52 | 4421.0 |

Certified (min / median / max): solve 74.83 / 589.09 / 1389.35 s; lrat-check 25.0 / 61.8 / 81.5 s; cake_lpr 165.3 / 354.6 / 446.9 s; proof 1.11 / 3.76 / 4.87 GB.

Largest solver RSS: 4421.0 MB. No SAT, no proof rejection, no memory problem.

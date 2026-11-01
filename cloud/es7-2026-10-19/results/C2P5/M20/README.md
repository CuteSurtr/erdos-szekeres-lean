# C2P5 M20

Values: V = M20, LIST = C2P5A.tsv, j = 20, N = 37, H = 4.5, Z = 81cb025f. Start 2026-10-31 18:50:24Z (epoch 1793472624); END = 1793487924.

## Tools and checks (details in `tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). No code cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf and base.json match the expected values.
- Cubes P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (5, rows idx ≡ 20 mod 37 of C2P5A.tsv)

| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P4_5-6 | P4 | Q | 8000 | UNSAT, certified | 564.68 | 62.4 | 336.0 | 3593605884 | 4409 |
| P4_2-5-13 | P4 | H | 2400 | UNSAT, certified | 487.55 | 59.0 | 349.8 | 3652144752 | 4374 |
| P4_2-8-13 | P4 | H | 2400 | UNSAT, certified | 517.17 | 59.7 | 335.2 | 3672223950 | 4372 |
| P4_5-10-12 | P4 | H | 2400 | UNSAT, certified | 192.53 | 48.6 | 298.1 | 3114346338 | 4344 |
| P4_6-11-12 | P4 | H | 2400 | UNSAT, certified | 98.39 | 34.0 | 201.9 | 1533329098 | 3411 |

Counts by case and kind: P4 Q: 1 certified; P4 H: 4 certified. Timed out (UNKNOWN): 0. Not reached: 0. Errors: 0.

Certified units (min / median / max): solve 98.39 / 487.55 / 564.68 s; lrat-check 34.0 / 59.0 / 62.4 s; cake_lpr 201.9 / 335.2 / 349.8 s; proof size 1.53 / 3.59 / 3.67 GB.

Largest solver RSS: 4409 MB (P4_5-6).

No SAT, no proof rejection, no memory problem. Every proof was accepted by both lrat-check (`c VERIFIED`) and cake_lpr (`s VERIFIED UNSAT`) and then deleted. The lane finished all units at 19:54:39Z.

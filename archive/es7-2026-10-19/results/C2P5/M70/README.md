# C2P5 M70: LIST = C2P5B.tsv, j = 20, N = 50, H = 5.25 (TASK.md @ 81cb025f)

**Result: all 19 units certified UNSAT (both lrat-check and cake_lpr accepted every proof). No SAT, no timeouts, no errors, no proof rejections, no memory problems.**

## Tools and checks
- `build_tools.sh` from the vendored sources (`vendor/tools-src.tar.xz`, manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc, E2 patch). No code cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…2b48`, both as expected.
- Cubes P1..P8 from `l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details are in `tools.txt`. The lane started 2026-10-31 15:12 UTC with END = 1793477413 (20:10:13 UTC) and finished all units at 18:09:58 UTC.

## Units (idx ≡ 20 mod 50 of C2P5B.tsv: 19 units)
| case | kind | units | certified | UNKNOWN | errors/rejected | not reached |
|---|---|---|---|---|---|---|
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | Q | 1 | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 6 | 0 | 0 | 0 |
| P1 | H | 5 | 5 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |

Q certified (3), min / median / max:
- solve s: 378.07 / 442.3 / 467.82
- lrat-check s: 53.2 / 56.8 / 62.4
- cake_lpr s: 305 / 320.3 / 326.4
- proof GB: 3.31 / 3.31 / 3.33

H certified (16), min / median / max:
- solve s: 26.35 / 232.39 / 511.01
- lrat-check s: 13.4 / 53.95 / 62.4
- cake_lpr s: 114.4 / 308.1 / 373.8
- proof GB: 0.21 / 3.205 / 3.6

all certified (19), min / median / max:
- solve s: 26.35 / 255.19 / 511.01
- lrat-check s: 13.4 / 54.4 / 62.4
- cake_lpr s: 114.4 / 311.2 / 373.8
- proof GB: 0.21 / 3.27 / 3.6

Largest solver RSS: 4426.79 MB (P2_1-3-12)

| unit | case | kind | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|
| P2_4-5 | P2 | Q | UNSATISFIABLE | 442.3 | 56.8 | 326.4 | 3.31 | 4402.54 |
| P1_3-4 | P1 | Q | UNSATISFIABLE | 378.07 | 53.2 | 305.0 | 3.31 | 4417.05 |
| P2_1-3-12 | P2 | H | UNSATISFIABLE | 439.64 | 58.9 | 338.3 | 3.60 | 4426.79 |
| P2_1-8-10 | P2 | H | UNSATISFIABLE | 279.2 | 54.4 | 311.2 | 3.27 | 4368.17 |
| P2_3-7-10 | P2 | H | UNSATISFIABLE | 83.23 | 27.5 | 171.1 | 1.23 | 3209.91 |
| P2_4-5-7 | P2 | H | UNSATISFIABLE | 28.36 | 14.9 | 117.4 | 0.21 | 2654.54 |
| P2_4-9-15 | P2 | H | UNSATISFIABLE | 440.02 | 62.4 | 373.8 | 3.54 | 4373.89 |
| P2_5-10-12 | P2 | H | UNSATISFIABLE | 94.98 | 26.7 | 174.9 | 1.12 | 3119.89 |
| P1_2-4-9 | P1 | H | UNSATISFIABLE | 100.18 | 29.2 | 191.1 | 1.39 | 3408.52 |
| P1_2-9-14 | P1 | H | UNSATISFIABLE | 511.01 | 60.6 | 356.5 | 3.58 | 4414.96 |
| P1_3-7-10 | P1 | H | UNSATISFIABLE | 27.5 | 13.4 | 115.0 | 0.22 | 2650.18 |
| P1_4-7-12 | P1 | H | UNSATISFIABLE | 217.0 | 53.5 | 320.2 | 3.17 | 4350.54 |
| P1_6-8-9 | P1 | H | UNSATISFIABLE | 26.35 | 14.6 | 120.6 | 0.22 | 2676.58 |
| P3_6-7 | P3 | Q | UNSATISFIABLE | 467.82 | 62.4 | 320.3 | 3.33 | 4404.9 |
| P3_1-6-7 | P3 | H | UNSATISFIABLE | 255.19 | 54.4 | 305.0 | 3.24 | 4398.76 |
| P3_1-11-16 | P3 | H | UNSATISFIABLE | 320.87 | 57.5 | 327.3 | 3.36 | 4377.46 |
| P3_4-8-12 | P3 | H | UNSATISFIABLE | 247.78 | 56.0 | 313.2 | 3.27 | 4363.09 |
| P3_5-7-15 | P3 | H | UNSATISFIABLE | 313.73 | 54.8 | 335.8 | 3.33 | 4409.64 |
| P3_6-10-12 | P3 | H | UNSATISFIABLE | 27.95 | 13.6 | 114.4 | 0.22 | 2647.8 |

Not reached: 0. Timed out (UNKNOWN): 0. Errors / certified false: 0. SAT: none (no `/opt/work/SAT_FOUND`).

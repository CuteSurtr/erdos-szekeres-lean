# C2P5 M83

Values: V = M83, LIST = C2P5B.tsv, j = 33, N = 50, H = 5.25, Z = 81cb025f. Start 2026-10-31 15:24:34Z (epoch 1793460274), END = 1793478274 (20:24:34Z). Machine: 4 cores, 15 GB (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch) from the vendored sources; manifest: all 196 files match. Nothing was cloned or downloaded.
- Sanity: both checkers rejected the bad LRAT and accepted the good one; the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…b48`: both match.
- Cubes P1..P8 from `C2C34/l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, 18 rows with idx ≡ 33 mod 50)
All 18 units are **certified** (UNSATISFIABLE; lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`). Timed out (UNKNOWN): 0. Not reached: 0. Errors: 0. The lane finished at 18:51:26Z.

| case | Q certified | H certified |
|---|---|---|
| P2 | 1 (P2_5-8) | 6 |
| P1 | 1 (P1_4-6) | 5 |
| P3 | 1 (P3_7-13) | 4 |
| total | 3 | 15 |

Certified units, min / median / max:
- solve: 24.1 / 315.4 / 1756.8 s (the maximum is P3_7-13, Q, cap 8000)
- lrat-check: 13.3 / 56.8 / 85.4 s
- cake_lpr: 113.7 / 323.9 / 445.8 s
- proof size: 0.22 / 3.34 / 5.04 GB

Largest solver RSS: 4423 MB (P2_3-4-15). The cake_lpr heap was 8000 MB. Per-unit figures are in `out.jsonl`.

There were no SAT answers, no proof rejections and no memory problems.

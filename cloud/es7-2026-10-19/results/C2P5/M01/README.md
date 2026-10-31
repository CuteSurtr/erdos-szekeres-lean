# C2P5 M01 (list C2P5A.tsv, shard j = 1 of N = 37, H = 4.5, TASK commit 81cb025f)

Start 2026-10-31 17:56:23Z (epoch 1793469383), END 1793484683 (22:11:23Z). The lane finished all units at 18:55:56Z.
List used: `lists/C2P5A.tsv` as rewritten in 92a2b58ad (for M01-M36); TASK.md is unchanged since 81cb025f.

## Tools and checks (`tools.txt`)
- Built by `C2P/vendor/build_tools.sh` from the vendored sources (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example prints `s VERIFIED UNSAT`.
- base.cnf header `p cnf 838032 16653336`; sha256 of base.cnf and base.json match the expected values.
- Cubes P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (4: idx 1, 38, 75, 112)
| unit | case | kind | cap | status | solve s | RSS MB | proof bytes | lrat-check s | cake_lpr s | certified |
|---|---|---|---|---|---|---|---|---|---|---|
| P4_1-5 | P4 | Q | 8000 | UNSAT | 1830.27 | 4414.5 | 5542564942 | 85.9 | 470.3 | true |
| P4_5-6-12 | P4 | H | 2400 | UNSAT | 82.33 | 3171.6 | 1263331211 | 26.2 | 169.9 | true |
| P4_5-12-13 | P4 | H | 2400 | UNSAT | 230.70 | 4343.8 | 3071590915 | 52.0 | 293.8 | true |
| P4_7-8-12 | P4 | H | 2400 | UNSAT | 25.72 | 2662.3 | 215488794 | 13.0 | 112.5 | true |

- By case and kind: P4 Q: 1 certified; P4 H: 3 certified. Timed out (UNKNOWN): 0. Not reached: 0. Errors / `certified: false`: 0.
- Certified (4) min / median / max: solve 25.72 / 156.5 / 1830.27 s; lrat-check 13.0 / 39.1 / 85.9 s; cake_lpr 112.5 / 231.9 / 470.3 s; proof 0.22 / 2.17 / 5.54 GB.
- Largest solver RSS: 4414.5 MB (P4_1-5).
- No SAT, no proof rejection, no memory or disk problem (peak disk use about 17 GB of 252 GB, 22 GB still free).

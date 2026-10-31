# C2P3 M31: LIST = C2P3.tsv, shard j = 31 of N = 50, H = 2.5 h, task commit Z = 4f653319

Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 09:42:52Z, END 11:57:52Z (epoch 1793447872); the lane finished all units at 11:43:27Z.

## Tools and checks (`tools.txt`)
- Built by `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz` (manifest: all 196 files match), nothing downloaded: CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity: cake_lpr example `s VERIFIED UNSAT`; bad LRAT rejected by both checkers, good LRAT accepted by both.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1`, base.json `2476faff…bf472b48` (both as required).
- Cubes P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (10 rows with idx ≡ 31 mod 50)
**All 10 certified UNSAT** (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`). Timed out (UNKNOWN): 0. Not reached: 0. Errors / certified=false: 0.

| case | kind | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|
| P6 | Q | 2 | 0 | 0 | 0 |
| P6 | H | 3 | 0 | 0 | 0 |
| P5 | H | 5 | 0 | 0 | 0 |

| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof GB | solver RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P6_2-3 | P6 | Q | 6000 | UNSAT certified | 837.59 | 64.6 | 370.1 | 4.00 | 4405 |
| P6_9-11 | P6 | Q | 4800 | UNSAT certified | 593.13 | 60.4 | 330.0 | 3.61 | 4399 |
| P6_2-7-11 | P6 | H | 1800 | UNSAT certified | 458.66 | 57.7 | 330.4 | 3.57 | 4364 |
| P6_3-11-12 | P6 | H | 1800 | UNSAT certified | 322.28 | 59.4 | 320.0 | 3.26 | 4367 |
| P6_9-10-12 | P6 | H | 1800 | UNSAT certified | 25.96 | 13.3 | 120.7 | 0.22 | 2645 |
| P5_1-6-15 | P5 | H | 1800 | UNSAT certified | 468.32 | 61.8 | 344.9 | 3.58 | 4407 |
| P5_1-13-16 | P5 | H | 1800 | UNSAT certified | 237.65 | 54.5 | 304.9 | 3.21 | 4356 |
| P5_2-9-15 | P5 | H | 1800 | UNSAT certified | 524.75 | 59.4 | 336.8 | 3.63 | 4421 |
| P5_6-9-10 | P5 | H | 914* | UNSAT certified | 75.65 | 24.7 | 163.2 | 1.12 | 3153 |
| P5_7-10-14 | P5 | H | 646* | UNSAT certified | 132.0 | 34.7 | 209.0 | 1.86 | 3476 |

\* cap lowered by lane.py to fit before END (list cap 1800); both solved well within it.

Certified units, min / median / max: solve 25.96 / 390.47 / 837.59 s; lrat-check 13.3 / 58.6 / 64.6 s; cake_lpr 120.7 / 325.0 / 370.1 s; proof 0.22 / 3.41 / 4.00 GB (proofs deleted after checking).

Largest solver RSS: 4421 MB (P5_2-9-15); cake_lpr ran with its 8000 MB heap. No SAT, no proof rejection, no memory problem.

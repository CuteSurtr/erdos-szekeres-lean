# C2P3 M09: shard j = 9 of N = 50 of `lists/C2P3.tsv` (TASK commit 4f653319, H = 2.5 h)

Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 09:42:43Z (epoch 1793439763), END = 1793447863 (11:57:43Z).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest check passed for all 196 files. Built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch) from `vendor/tools-src.tar.xz`. Nothing was cloned or downloaded.
- Sanity: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. Both sha256 values match (base.cnf b0061e90…d8ff1, base.json 2476faff…bf472b48).
- Cubes P1..P8: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (11 rows with idx ≡ 9 mod 50)
| case | kind | units | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|---|
| P7 | Q | 1 | 1 | 0 | 0 | 0 |
| P6 | Q | 1 | 1 | 0 | 0 | 0 |
| P6 | H | 3 | 3 | 0 | 0 | 0 |
| P5 | H | 6 | 4 | 0 | 2 | 0 |
| **total** | | **11** | **9** | **0** | **2** | **0** |

Certified (UNSAT, both checkers accepted): P7_9-11, P6_8-10, P6_1-5-11, P6_2-15-16, P6_7-13-14, P5_1-3-11, P5_1-9-16, P5_2-7-10, P5_2-15-16.
Not reached (the lane stopped at 11:51:33Z with 369 s left before END): P5_6-14-15, P5_8-11-14.

| unit | kind | solve s | lrat-check s | cake_lpr s | proof GB | solver RSS MB |
|---|---|---|---|---|---|---|
| P7_9-11 | Q | 781.6 | 52.7 | 342.7 | 3.73 | 4362 |
| P6_8-10 | Q | 691.1 | 53.4 | 333.3 | 3.60 | 4378 |
| P6_1-5-11 | H | 685.9 | 51.6 | 334.6 | 3.66 | 4406 |
| P6_2-15-16 | H | 251.4 | 46.5 | 297.4 | 3.18 | 4349 |
| P6_7-13-14 | H | 221.3 | 46.0 | 292.6 | 3.09 | 4344 |
| P5_1-3-11 | H | 431.7 | 50.5 | 329.9 | 3.36 | 4396 |
| P5_1-9-16 | H | 487.8 | 50.6 | 317.4 | 3.53 | 4376 |
| P5_2-7-10 | H | 392.8 | 46.6 | 304.4 | 3.40 | 4408 |
| P5_2-15-16 | H | 246.4 | 45.5 | 297.9 | 3.22 | 4355 |

For the 9 certified units (min / median / max):
- solve: 221.3 / 431.7 / 781.6 s
- lrat-check: 45.5 / 50.5 / 53.4 s
- cake_lpr: 292.6 / 317.4 / 342.7 s
- proof size: 3.09 / 3.40 / 3.73 GB

Largest solver RSS: 4408 MB (P5_2-7-10).

## Problems
No SAT, no proof rejections, no ERROR records and no memory problems. Every unit was solved well under its cap, so neither quadrilateral unit came near its 6000 s or 4800 s cap. The proofs were deleted after checking. No CNF or proof files are committed.

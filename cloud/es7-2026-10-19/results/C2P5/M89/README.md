# C2P5 M89 (LIST C2P5B.tsv, shard j=39 of N=50, H=5.25, TASK commit 81cb025f)

## Tools and checks

- Built with `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz` (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch. Nothing cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF `SYMZ/zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`, base.cnf sha256 b0061e90…d8ff1, base.json sha256 2476faff…2b48 (both as required).
- Cubes: `C2C34/l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details in `tools.txt`; the lane command in `run.sh` (start 15:24:35Z, END 20:24:35Z).

## Units

| idx | unit | case | kind | cap | result | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|
| 39 | P2_5-14 | P2 | Q | 8000 | certified | 2592.38 | 96.2 | 608.1 | 5.52 | 4394.04 |
| 89 | P1_4-12 | P1 | Q | 8000 | certified | 2156.81 | 87.0 | 544.0 | 5.17 | 4430.41 |
| 139 | P2_1-5-9 | P2 | H | 2400 | certified | 393.4 | 59.0 | 389.9 | 3.37 | 4384.75 |
| 189 | P2_3-5-10 | P2 | H | 2400 | certified | 155.11 | 42.1 | 237.4 | 2.19 | 3286.0 |
| 239 | P2_3-9-14 | P2 | H | 2400 | certified | 619.78 | 75.4 | 399.3 | 3.65 | 4383.87 |
| 289 | P2_4-7-9 | P2 | H | 2400 | certified | 86.19 | 28.7 | 183.9 | 1.14 | 3154.04 |
| 339 | P2_5-7-8 | P2 | H | 2400 | certified | 32.7 | 15.9 | 123.7 | 0.22 | 2679.31 |
| 389 | P2_6-9-13 | P2 | H | 2400 | certified | 123.82 | 35.2 | 214.3 | 1.71 | 3439.63 |
| 439 | P1_2-6-7 | P1 | H | 2400 | certified | 90.03 | 30.4 | 182.0 | 1.21 | 3195.54 |
| 489 | P1_3-4-6 | P1 | H | 2400 | certified | 29.58 | 14.0 | 111.9 | 0.22 | 2654.03 |
| 539 | P1_3-10-11 | P1 | H | 2400 | certified | 87.84 | 27.6 | 184.3 | 1.11 | 3138.35 |
| 589 | P1_4-12-13 | P1 | H | 2400 | certified | 278.98 | 55.3 | 342.7 | 3.25 | 4360.15 |
| 639 | P3_1-8 | P3 | Q | 8000 (run 6403) | certified | 2380.15 | 93.9 | 533.5 | 5.46 | 4413.57 |
| 689 | P3_9-11 | P3 | Q | 8000 (run 3364) | certified | 476.81 | 62.7 | 350.1 | 3.32 | 4366.69 |

### Counts by case and kind

| case | kind | certified | timed out | not reached | errors / not certified |
|---|---|---|---|---|---|
| P1 | H | 4 | 0 | 0 | 0 |
| P1 | Q | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 0 | 0 | 0 |
| P2 | Q | 1 | 0 | 0 | 0 |
| P3 | Q | 2 | 0 | 0 | 0 |

Total 14 units: 14 certified.

### Certified units (min / median / max)

- kind Q (4): solve s 476.81 / 2268.48 / 2592.38; lrat-check s 62.7 / 90.45 / 96.2; cake_lpr s 350.1 / 538.75 / 608.1; proof GB 3.32 / 5.315 / 5.52
- kind H (10): solve s 29.58 / 106.925 / 619.78; lrat-check s 14 / 32.8 / 75.4; cake_lpr s 111.9 / 199.3 / 399.3; proof GB 0.22 / 1.46 / 3.65
- all (14): solve s 29.58 / 217.045 / 2592.38; lrat-check s 14 / 48.7 / 96.2; cake_lpr s 111.9 / 290.05 / 608.1; proof GB 0.22 / 2.72 / 5.52

## Resources and problems

- Largest solver RSS: 4430 MB (machine: 4 cores, 15 GB RAM, no swap). No memory problem.
- SAT: none. Proof rejections / errors: none.
- The lane finished all units at 19:33:34Z, before END; no unit timed out. Disk use peaked at about 6 GB of proof (deleted after checks).

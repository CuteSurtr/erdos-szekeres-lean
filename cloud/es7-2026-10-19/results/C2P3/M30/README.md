# C2P3 M30

Task `results/C2P3/TASK.md` (commit 4f653319). V = M30, LIST = C2P3.tsv, j = 30, N = 50, H = 2.5. Machine: 4 cores, 15 GB RAM (`env.txt`).
Start 2026-10-31 09:42:55 UTC (epoch 1793439775), END = start + 2.5 h - 15 min = 11:57:55 UTC (1793447875); lane command in `run.sh`.

## Tools and checks (`tools.txt`)

- `C2P/vendor/build_tools.sh`: all 196 vendored files match `MANIFEST.sha256`; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch) built from `vendor/tools-src.tar.xz`. Nothing cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…bf472b48`, both as expected.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`: idx ≡ 30 mod 50, 10 units; records in `out.jsonl`)

| case | kind | units | outcome |
|---|---|---|---|
| P6 | Q | 2 | 2 certified |
| P6 | H | 3 | 3 certified |
| P5 | H | 4 | 3 certified, 1 not reached |
| P5 | Q | 1 | 1 timed out (UNKNOWN) |

Total: 8 certified, 1 timed out (UNKNOWN), 1 not reached of 10 units.

| idx | unit | case | kind | cap s | outcome | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|
| 30 | P6_1-14 | P6 | Q | 6000 | certified | 1344.4 | 72.0 | 412.3 | 4.87 | 4378.37 |
| 80 | P6_9-10 | P6 | Q | 4800 | certified | 524.14 | 53.4 | 324.2 | 3.54 | 4401.41 |
| 130 | P6_2-4-10 | P6 | H | 1800 | certified | 293.98 | 50.4 | 297.6 | 3.29 | 4375.52 |
| 180 | P6_3-10-13 | P6 | H | 1800 | certified | 389.74 | 53.8 | 316.6 | 3.44 | 4368.61 |
| 230 | P6_9-10-11 | P6 | H | 1800 | certified | 22.79 | 12.7 | 110.7 | 0.22 | 2645.51 |
| 280 | P5_1-6-14 | P5 | H | 1800 | certified | 485.77 | 59.1 | 340.6 | 3.67 | 4365.0 |
| 330 | P5_1-13-15 | P5 | H | 1800 | certified | 229.06 | 49.2 | 297.0 | 3.23 | 4406.85 |
| 380 | P5_2-9-14 | P5 | H | 1800 | certified | 526.36 | 56.5 | 328.4 | 3.68 | 4406.83 |
| 430 | P5_6-9 | P5 | Q | 2400 | timed out (UNKNOWN) | 607.9 | - | - | 0.00 | 4408.61 |
| 480 | P5_7-10-13 | P5 | H | 1800 | not reached | | | | | |

Certified units, min / median / max:
- solve s: 22.79 / 437.755 / 1344.4
- lrat-check s: 12.7 / 53.6 / 72
- cake_lpr s: 110.7 / 320.4 / 412.3
- proof GB: 0.22 / 3.49 / 4.87

Largest solver RSS: 4408.61 MB (machine 15 GB).
cake_lpr heap used: [8000] MB.

Notes:
- P5_2-9-14 ran with a cap of 1540 s instead of 1800 s, cut by lane.py so that 10 minutes stay for the checks before END; it was certified at 526 s.
- P5_6-9 (Q, list cap 2400 s) started at 11:37:40 with only 614 s of cap left before END and timed out (UNKNOWN at 607.9 s). That is a time-budget cutoff, not a real 2400 s timeout, so it stays open.
- P5_7-10-13 was not reached: the lane stopped at 11:47:58 with 596 s left (< 15 min).

## SAT, proof rejections, memory

- No SAT (`/opt/work/SAT_FOUND` never appeared).
- No proof rejections and no ERROR records: all 8 UNSAT proofs were accepted by both lrat-check (`c VERIFIED`) and cake_lpr (`s VERIFIED UNSAT`, 8000 MB heap; no 11000 MB retry needed).
- No memory problems: largest solver RSS was 4.4 GB, and free memory never went below about 6 GB available, while cake_lpr was running.
- Disk: the largest proof was 4.9 GB, and at least 23 GB stayed free.

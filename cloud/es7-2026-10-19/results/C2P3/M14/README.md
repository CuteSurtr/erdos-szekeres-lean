# C2P3 M14: third wave on the parallelogram cases, shard 14 of 50 of C2P3.tsv

Task `results/C2P3/TASK.md` at 4f653319, V = M14, LIST = C2P3.tsv, j = 14, N = 50, H = 2.5.
Start 2026-10-31 09:43:03 UTC (epoch 1793439783), END = 1793447883 (11:58:03 UTC). One lane (`run.sh`), 4 cores and 15 GB.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 manifest files match. The build gives CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc + E2 patch). Nothing was cloned or downloaded.
- Sanity checks: the cake_lpr example prints `s VERIFIED UNSAT`. The bad LRAT is rejected by both checkers and the good one is accepted by both.
- Base CNF: header `p cnf 838032 16653336`. Both sha256 match: base.cnf `b0061e90…d8ff1` and base.json `2476faff…bb48`.
- Cubes P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P*_cubes.txt`.

## Units (10 in this shard, `units.tsv`)

| idx | unit | case | kind | cap | result | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|
| 14 | P6_1-10 | P6 | Q | 6000 | **certified UNSAT** | 4527.1 | 129.4 | 673.8 | 8.46 | 4370 |
| 64 | P6_1-9-14 | P6 | H | 1800 | **certified UNSAT** | 491.7 | 58.4 | 331.3 | 3.59 | 4359 |
| 114 | P6_3-7-13 | P6 | H | 1800 (lane cap 1080) | **certified UNSAT** | 555.7 | 56.9 | 348.3 | 3.66 | 4378 |
| 164 | P6_8-9-12 | P6 | H | 1800 | not reached | | | | | |
| 214, 264, 314, 364, 414 | P5_1-3-16, P5_1-10-14, P5_2-7-15, P5_6-7-10, P5_7-8-10 | P5 | H | 1800 | not reached | | | | | |
| 464 | P5_9-10 | P5 | Q | 2400 | not reached | | | | | |

Counts by case and kind:
- P6 Q: 1 certified.
- P6 H: 2 certified, 1 not reached.
- P5 H: 5 not reached.
- P5 Q: 1 not reached.
- Totals: 3 certified, 0 timed out (UNKNOWN), 7 not reached, 0 errors.

For the 3 certified units (minimum / median / maximum):
- solve: 491.7 / 555.7 / 4527.1 s
- lrat-check: 56.9 / 58.4 / 129.4 s
- cake_lpr: 331.3 / 348.3 / 673.8 s
- proof size: 3.59 / 3.66 / 8.46 GB

All proofs were deleted after both checks. The lane stopped at 11:46:18 UTC with 704 s left before END (fewer than 15 minutes, so it started no more units).

## Problems
- Largest solver RSS: 4378 MB. There were no memory problems: available memory never fell below about 7 GB, and peak disk use was about 20 GB of 40.
- No SAT, no proof rejection, no `certified: false` record and no ERROR status.

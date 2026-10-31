# C2P3 M25: shard 25 of 50 of `lists/C2P3.tsv`

Task: `results/C2P3/TASK.md` at commit 4f653319, with V = M25, LIST = C2P3.tsv, j = 25, N = 50, H = 2.5.
Machine: 4 cores, 15 GB, no swap (`env.txt`). Start 2026-10-31T09:42:53Z, lane END 1793447873 (11:57:53Z).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 vendored files match `MANIFEST.sha256`. It built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc + E2 patch) from those sources. Nothing was cloned or downloaded.
- Sanity checks: lrat-check and cake_lpr both rejected the bad LRAT and both accepted the good one. The cake_lpr example gave `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. Both sha256 values match the task: base.cnf `b0061e90…d8ff1` and base.json `2476faff…b48`.
- Cubes: for P1..P8, the `l2cubes.py` output is byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (`units.tsv`, 11 units; records in `out.jsonl`)

| case | kind | certified | timed out (UNKNOWN) | not reached |
|---|---|---|---|---|
| P6 | Q | 2 (P6_1-2, P6_8-11) | 0 | 0 |
| P6 | H | 3 (P6_2-3-11, P6_3-9-12, P6_8-11-14) | 0 | 0 |
| P5 | H | 2 (P5_1-6-9, P5_1-12-14) | 0 | 2 (P5_6-8-12, P5_7-9-14) |
| P5 | Q | 0 | 1 (P5_2-9) | 1 (P5_10-12) |
| total | | **7** | **1** | **3** |

- P5_2-9 (Q, listed cap 2400 s) got only 1511 s, because the lane shortens the cap to fit the time left before END. It returned UNKNOWN after 1498 s. This is a budget-limited timeout, not a timeout at the full cap.
- There were no errors and no `"certified": false` records.

Certified units (7):

| | min | median | max |
|---|---|---|---|
| solve s | 117.4 | 380.6 | 847.7 |
| lrat-check s | 30.3 | 58.1 | 64.7 |
| cake_lpr s | 191.4 | 328.6 | 369.7 |
| proof size | 1.42 GB | 3.39 GB | 3.97 GB |

- cake_lpr needed only the 8000 MB heap on every unit.
- Largest solver RSS was 4423 MB (P5_2-9). The highest RSS seen during the checks was about 8.2 GB, in cake_lpr.

## SAT, rejections, memory
No SAT. No proof was rejected. No memory problem and no OOM.

# C2P3, machine M08

Shard j = 8 of N = 50 of `lists/C2P3.tsv` (task `../TASK.md`, commit 4f653319), budget H = 2.5 h, one lane.
Start 2026-10-31 09:42:37Z (epoch 1793439757); lane END = start + 2 h 15 min = 11:57:37Z (epoch 1793447857).
Machine: 4 cores, 15 GB RAM (`env.txt`).

## Tools and checks (`tools.txt`)

- `C2P/vendor/build_tools.sh`: all 196 files of the vendored sources match `MANIFEST.sha256`; built CaDiCaL 3.0.1
  (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch). Nothing was cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…f2b48`, both as expected.
- Cubes: P1..P8 from `C2C34/l2cubes.py` byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (`units.tsv`, `out.jsonl`)

| idx | unit | case | kind | cap (list) | result |
|---|---|---|---|---|---|
| 8 | P7_8-16 | P7 | Q | 6000 | UNSATISFIABLE, certified, solve 5189.13 s (cap given 6000 s) |
| 58 | P6_1-5-10 | P6 | H | 1800 | UNSATISFIABLE, certified, solve 436.03 s (cap given 1133 s) |
| 108 | P6_2-14-16 | P6 | H | 1800 | UNSATISFIABLE, certified, solve 214.02 s (cap given 319 s) |
| 158 | P6_7-12-15 | P6 | H | 1800 | not reached |
| 208 | P5_1-3-10 | P5 | H | 1800 | not reached |
| 258 | P5_1-9-15 | P5 | H | 1800 | not reached |
| 308 | P5_2-7-9 | P5 | H | 1800 | not reached |
| 358 | P5_2-15 | P5 | Q | 2400 | not reached |
| 408 | P5_6-14 | P5 | Q | 2400 | not reached |
| 458 | P5_8-11-13 | P5 | H | 1800 | not reached |

Totals: **3 certified** (P6 H: 2, P7 Q: 1),
0 timed out (UNKNOWN), 0 errors, 0 uncertified records,
7 not reached (P5 H: 4, P5 Q: 2, P6 H: 1).
The quadrilateral unit P7_8-16 took 5236 s wall to solve, which left time for only two hexagonal P6 units
(the lane gave them caps of 1133 s and 319 s from the time left; both finished well inside).

Certified units, minimum / median / maximum:
- solve: 214.02 / 436.03 / 5189.13 s
- lrat-check: 46.5 / 52.7 / 139.9 s
- cake_lpr (heap 8000 MB, no retry needed): 275.7 / 311.7 / 725 s
- proof size: 3.21 / 3.59 / 9.61 GB (proofs deleted after checking; sizes and sha256 in `out.jsonl`)

Largest solver RSS: 4416 MB (P6_1-5-10). cake_lpr used about 8.2 GB RSS.

## SAT, rejections, memory

No SAT answer (no `SAT_FOUND`). No proof rejected: every proof was accepted by both lrat-check and cake_lpr.
No memory problem. Disk: `/` peaked at about 21.4 GB used (18.9 GB still available) while the 9.6 GB proof of P7_8-16 was on disk.


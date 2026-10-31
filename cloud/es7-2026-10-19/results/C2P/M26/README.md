# C2P M26

Task: `results/C2P/TASK.md` at fb2c59af, with V = M26, LIST = C2P.tsv, j = 26, N = 42, H = 3.5.
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-31 02:57:05 UTC (epoch 1793415425). Lane ran from 03:00:05 to 05:57:28 UTC, END 1793427125 (06:12:05 UTC).

## Tools and checks (`tools.txt`)
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`, example prints `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with `E2/tools/lrat-check-E2.patch`.
- Checker sanity on {1},{-1}: LRAT `3 0 0` rejected by both checkers; `3 0 1 2 0` accepted by both.
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json both match.
- Cubes P1..P8: all 8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- lane.py at fb2c59af, unmodified (`run.sh`).

## Units (53: idx ≡ 26 mod 42; `units.tsv`, records in `out.jsonl`)
- Certified: 10.
- Timed out (UNKNOWN): 2.
- Not reached: 41.
- Errors or `certified: false`: none.

| case | kind | units | certified | UNKNOWN | not reached |
|---|---|---|---|---|---|
| P8 | H | 5 | 5 | 0 | 0 |
| P7 | H | 5 | 5 | 0 | 0 |
| P7 | Q | 2 | 0 | 2 | 0 |
| P6 | H / Q | 6 / 1 | 0 | 0 | 7 |
| P5 | H / Q | 6 / 1 | 0 | 0 | 7 |
| P4 | H / Q | 6 / 1 | 0 | 0 | 7 |
| P3 | H / Q | 5 / 1 | 0 | 0 | 6 |
| P2 | H / Q | 5 / 2 | 0 | 0 | 7 |
| P1 | H / Q | 6 / 1 | 0 | 0 | 7 |

Certified (both lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, heap 8000 MB every time): P8_1-6-14, P8_2-15-16, P8_3-9-11, P8_1-15-16, P8_1-6-9, P7_2-3-10, P7_9-10-12, P7_3-11-15, P7_2-9-12, P7_2-3-4.
Of these, P7_2-3-4 ran with a reduced cap (540 s, time left) and still finished in 76.8 s.

Timed out at the 2400 s cap: P7_8-14 (2382.4 s), P7_8-15 (2382.8 s). Both are Q units.

Certified units (10), min / median / max:
- solve: 24.3 / 284.3 / 442.2 s
- lrat-check: 12.7 / 51.2 / 57.2 s
- cake_lpr: 107.1 / 290.6 / 321.9 s
- proof size: 216,473,382 / 3,265,909,574 / 3,559,249,479 bytes (about 0.22 / 3.27 / 3.56 GB)

Not reached: P6_2-9-15, P6_1-9-15, P6_7-12, P6_1-3-5, P6_1-9-14, P6_3-7-11, P6_1-4-8, P5_1-13-14, P5_2-11-12, P5_2-12-13, P5_1-10-13, P5_6-13, P5_2-11-16, P5_6-13-15, P4_2-7-8, P4_6-9, P4_5-7-16, P4_5-6-14, P4_5-8-13, P4_1-3-8, P4_1-10-15, P3_5-11-13, P3_1-4-7, P3_5-6-13, P3_1-8, P3_1-9-10, P3_5-8-12, P2_3-11-15, P2_3-16, P2_4-6-9, P2_1-5-10, P2_5-11-13, P2_4-10-12, P2_1-7, P1_4-8-10, P1_6-7-11, P1_4-7-11, P1_4-11, P1_2-7-15, P1_3-4-6, P1_2-4-7.

## Resources and incidents
- Largest solver RSS: 4475.2 MB (P7_8-14). cake_lpr never needed the 11000 MB retry.
- No SAT. No proof rejection. No memory problem.
- Operational: the first `git pull` returned HTTP 403 once and the first pushes were rejected by concurrent pushes; a pull/push retry loop then succeeded every time. The first `patch` attempt was given no target file ("Only garbage"); it was re-run as `patch lrat-check.c < patch` (one line added, checked) before the binary was used.

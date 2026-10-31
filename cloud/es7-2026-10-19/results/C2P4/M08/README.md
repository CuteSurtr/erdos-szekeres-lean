# C2P4 M08

Fourth wave on the parallelogram cases, machine M08: LIST = `C2P4.tsv`, shard j = 8 of N = 50, H = 2.5 h, task commit a46b478d (`results/C2P4/TASK.md`). Start 13:01:19 UTC (epoch 1793451679), END = start + 2.5 h − 15 min = 1793459779 (15:16:19 UTC). Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)

- `C2P/vendor/build_tools.sh` from the vendored sources (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing was cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example `s VERIFIED UNSAT`.
- Base CNF `SYMZ/zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…b48`, both as expected.
- Cubes: `l2cubes.py` output for P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, 13 rows with idx ≡ 8 mod 50)

One lane (`run.sh`), records in `out.jsonl`, log tail in `lane.log.tail`.

| unit | case | kind | cap (list) | cap used | status | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|
| P5_1-11 | P5 | Q | 7000 | 7000 | certified UNSAT | 3069.94 | 99.4 | 561.3 | 6,826,127,636 | 4407.66 |
| P4_7-11 | P4 | Q | 6000 | 3581 | certified UNSAT | 921.85 | 60.9 | 369.9 | 4,123,287,570 | 4404.04 |
| P4_1-6-14 | P4 | H | 1800 | 1800 | certified UNSAT | 502.85 | 57.8 | 363.9 | 3,682,981,635 | 4361.64 |
| P4_1-13-16 | P4 | H | 1800 | 1273 | certified UNSAT | 267.46 | 54.5 | 313.3 | 3,247,569,947 | 4362.15 |
| P4_5-6-11 | P4 | H | 1800 | 628 | certified UNSAT | 25.36 | 12.3 | 106.8 | 215,353,659 | 2650.01 |
| P4_5-13-15 | P4 | H | 1800 | 482 | certified UNSAT | 353.34 | 53.2 | 354.6 | 3,361,914,576 | 4392.54 |

(The lane lowered the caps of later units so that 10 minutes remained before END for the checks; every unit it started was solved within its cap.)

Counts:

| | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|
| P5 Q | 1 | 0 | 0 | 0 |
| P4 Q | 1 | 0 | 0 | 0 |
| P4 H | 4 | 0 | 1 (P4_7-10-14) | 0 |
| P3 Q | 0 | 0 | 1 (P3_6-7) | 0 |
| P3 H | 0 | 0 | 5 (P3_1-6-7, P3_1-11-16, P3_4-8-12, P3_5-7-15, P3_6-10-12) | 0 |
| **total** | **6** | **0** | **7** | **0** |

Not reached (the lane stopped at 15:11:09 UTC with 309 s left before END, under the 15-minute start rule): P4_7-10-14 (H), P3_6-7 (Q), P3_1-6-7, P3_1-11-16, P3_4-8-12, P3_5-7-15, P3_6-10-12 (H) — 7 units. With the 6 certified, that accounts for all 13 rows.

Certified units (6): solve s min 25.36 / median 428.10 / max 3069.94; lrat-check s 12.3 / 56.15 / 99.4; cake_lpr s 106.8 / 359.25 / 561.3 (heap 8000 MB every time); proof bytes 215,353,659 / 3,522,448,106 / 6,826,127,636.

## Resources and anomalies

- Largest solver RSS: 4407.66 MB (P5_1-11). cake_lpr reached about 8.2 GB RSS on the largest proof; no memory problem, no heap retry.
- Disk: the largest proof (6.8 GB) left over 20 GB free.
- No SAT, no proof rejection, no `certified: false` record, no ERROR status.

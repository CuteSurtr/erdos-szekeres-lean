# C2P4 M43: LIST = C2P4.tsv, shard j = 43 of N = 50, H = 2.5, task commit Z = a46b478d

## Tools and checks
- `C2P/vendor/build_tools.sh`: all 196 vendored source files match `MANIFEST.sha256`. Built CaDiCaL 3.0.1 (c6073042),
  cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch). Nothing was cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one, and the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. Both sha256 hashes match: base.cnf `b0061e90…d8ff1` and base.json `2476faff…bf472b48`.
- Cubes P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`. Details are in `tools.txt`.
- Lane started at 13:04 UTC with END = 1793459796 (15:16:36 UTC). See `run.sh`.

## Units (19: rows with idx ≡ 43 mod 50)
| case | kind | units | certified | timed out (UNKNOWN) | not reached |
|---|---|---|---|---|---|
| P5 | Q | 1 | 1 (P5_8-9) | 0 | 0 |
| P5 | H | 5 | 5 | 0 | 0 |
| P4 | Q | 1 | 0 | 1 (P4_5-15, solve stopped at 3199.5 s: its cap was cut to 3233 s by END, not the full 6000 s) | 0 |
| P4 | H | 5 | 0 | 0 | 5 |
| P3 | Q | 1 | 0 | 0 | 1 |
| P3 | H | 6 | 0 | 0 | 6 |
| **total** | | 19 | **6** | 1 | 12 |

Not reached: P4_1-5-10, P4_1-10-14, P4_2-7-14, P4_5-10-11, P4_6-11-14, P3_4-7, P3_1-4-8, P3_1-8-14, P3_4-6-9,
P3_4-12-15, P3_5-13-14, P3_9-10-11.

Errors: none. No record has `"certified": false` and no status starts with ERROR.

## Certified units (all are P5; both lrat-check and cake_lpr accepted each one)
| unit | kind | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|
| P5_8-9 | Q | 530.59 | 60.0 | 349.0 | 3.46 | 4358 |
| P5_1-6-12 | H | 614.44 | 64.0 | 358.3 | 3.76 | 4412 |
| P5_2-7-12 | H | 566.97 | 65.8 | 345.6 | 3.68 | 4372 |
| P5_6-7-14 | H | 215.03 | 54.2 | 317.3 | 3.15 | 4368 |
| P5_7-8-13 | H | 122.21 | 33.7 | 201.4 | 1.62 | 3415 |
| P5_9-10-13 | H | 19.81 | 13.6 | 117.9 | 0.22 | 2640 |

min / median / max: solve 19.8 / 372.8 / 614.4 s; lrat-check 13.6 / 57.1 / 65.8 s; cake_lpr 117.9 / 331.5 / 358.3 s;
proof 0.22 / 3.31 / 3.76 GB.

## Resources and anomalies
- Largest solver RSS: 4412 MB (P5_1-6-12). The timed-out P4_5-15 reached 4390 MB. There were no memory problems on the 15 GB / 4-core machine.
- No SAT result, no proof rejections and no errors.

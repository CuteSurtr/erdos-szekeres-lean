# C2P4 M22: shard 22 of 50 of `lists/C2P4.tsv`

Task: `results/C2P4/TASK.md` at a46b478d, with V = M22, LIST = C2P4.tsv, j = 22, N = 50 and H = 2.5. The lane started at 13:04:40Z, and END was 1793459821 (15:17:01Z).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored sources, with nothing downloaded. All 196 files match the manifest. CaDiCaL is 3.0.1 (c6073042), cake_lpr is a36874a8 and lrat-check is 2e3b2dc with the E2 patch.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: the header is `p cnf 838032 16653336` and the sha256 of base.cnf and base.json both match the expected values.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (19 in `units.tsv`)
| case | kind | units | certified | timed out (UNKNOWN) | not reached |
|---|---|---|---|---|---|
| P6 | H | 1 | 1 (P6_3-7-12) | 0 | 0 |
| P5 | Q | 1 | 1 (P5_2-10) | 0 | 0 |
| P5 | H | 4 | 4 (P5_1-10-13, P5_2-9-11, P5_6-9-13, P5_7-11-12) | 0 | 0 |
| P4 | Q | 1 | 0 | 1 (P4_1-11) | 0 |
| P4 | H | 6 | 0 | 0 | 6 |
| P3 | Q | 1 | 0 | 0 | 1 (P3_7-9) |
| P3 | H | 5 | 0 | 0 | 5 |
| **total** | | **19** | **6** | **1** | **12** |

There were no errors and no records with `"certified": false`.

- P4_1-11 is UNKNOWN only because the lane cut it short. Its list cap is 6000 s, but the lane capped the solve at 528 s so that the checks would finish before END; it stopped after 522.84 s. It is still open.
- The 12 units not reached are the P4 H units P4_1-2-6, P4_1-7-14, P4_2-5-11, P4_5-7-11, P4_6-7-15 and P4_8-10-12; the P3 Q unit P3_7-9; and the P3 H units P3_1-6-16, P3_1-14-16, P3_4-9-14, P3_5-9-11 and P3_7-8-12. The lane stopped at 15:07:04Z with 596 s left before END, below the 15-minute start threshold.

## Certified units (both checkers accepted; proofs deleted)
| unit | kind | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|---|
| P5_2-10 | Q | 3276.01 | 88.5 | 558.2 | 6310388310 | 4375 |
| P6_3-7-12 | H | 536.33 | 54.2 | 340.9 | 3523439533 | 4373 |
| P5_1-10-13 | H | 348.22 | 47.3 | 306.7 | 3314926404 | 4368 |
| P5_2-9-11 | H | 344.37 | 44.8 | 298.3 | 3295580576 | 4405 |
| P5_6-9-13 | H | 109.62 | 27.0 | 187.4 | 1479794183 | 3398 |
| P5_7-11-12 | H | 20.71 | 10.7 | 113.4 | 215013766 | 2645 |

Minimum, median and maximum over the six certified units:
- solve: 20.71 s, 346.30 s and 3276.01 s;
- lrat-check: 10.7 s, 46.05 s and 88.5 s;
- cake_lpr: 113.4 s, 302.5 s and 558.2 s;
- proof size: 0.215 GB, 3.31 GB and 6.31 GB.

## Resources and anomalies
- The largest solver RSS was 4416 MB (P4_1-11). cake_lpr used its 8000 MB heap. Free disk never fell below 22 GB.
- There was no SAT (`/opt/work/SAT_FOUND` never appeared), no proof rejection and no memory problem.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (7 records) and `lane.log.tail`.

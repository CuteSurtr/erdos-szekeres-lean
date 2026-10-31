# C2P3 M13 (LIST = C2P3.tsv, j = 13, N = 50, H = 2.5, task commit 4f653319)

Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-31T09:43:02Z; lane END = 1793447882 (11:58:02Z).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest, all 196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch), built from the vendored sources only. Nothing was cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and base.json (2476faff…) match the expected values.
- Cubes: `l2cubes.py` for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, 10 rows with idx ≡ 13 mod 50)
| unit | case | kind | cap | result |
|---|---|---|---|---|
| P6_1-9 | P6 | Q | 6000 | **certified UNSAT** |
| P6_1-9-10 | P6 | H | 1800 (run with 1010) | **certified UNSAT** |
| P6_3-7-12, P6_8-9-11 | P6 | H | 1800 | not reached |
| P5_1-3-15, P5_1-10-13, P5_2-7-14, P5_6-7-9, P5_7-8-9 | P5 | H | 1800 | not reached |
| P5_8-14 | P5 | Q | 2400 | not reached |

By case and kind:
- Certified: P6 Q 1, P6 H 1.
- Timed out (UNKNOWN): 0.
- Errors: 0.
- Not reached: P6 H 2, P5 H 5, P5 Q 1.

The lane stopped at 11:43:59Z with 842 s left, below the 900 s minimum needed to start a unit.

## Certified units
| unit | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|
| P6_1-9 | 5292.13 | 152.1 | 753.1 | 8,728,921,896 | 4404.6 |
| P6_1-9-10 | 358.83 | 57.5 | 337.7 | 3,273,408,160 | 4372.3 |

There are only two units, so the min and max are the two rows (median = mean): solve 358.8 / 2825.5 / 5292.1 s; lrat-check 57.5 / 104.8 / 152.1 s; cake_lpr 337.7 / 545.4 / 753.1 s; proof 3.27 / 6.00 / 8.73 GB. Both proofs were checked with an 8000 MB cake_lpr heap and then deleted.

- Largest solver RSS: 4404.6 MB.
- No SAT, no proof rejection, no memory or disk problem (peak disk use about 20 GB of 252 GB, with 19 GB free).

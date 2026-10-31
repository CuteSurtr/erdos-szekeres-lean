# C2P4 M06 (LIST = C2P4.tsv, j = 6, N = 50, H = 2.5, TASK commit a46b478d)

Started 13:01:37Z (epoch 1793451697); END = 1793459797 (15:16:37Z). One lane (`run.sh`), 4 cores, 15 GB RAM.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 manifest files match; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and
  lrat-check (2e3b2dc + E2 patch) built from `vendor/tools-src.tar.xz`. Nothing was cloned or downloaded.
- Sanity: the bad LRAT was rejected by both checkers, the good one accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); the
  cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf (b0061e90…) and base.json (2476faff…) match.
- Cubes: P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (13 rows with idx ≡ 6 mod 50, `units.tsv`)

| status | P5 Q | P4 Q | P4 H | P3 Q | P3 H | total |
|---|---|---|---|---|---|---|
| certified UNSAT | 1 | 1 | 1 | 0 | 0 | 3 |
| timed out (UNKNOWN) | 0 | 0 | 0 | 0 | 0 | 0 |
| not reached | 0 | 0 | 4 | 1 | 5 | 10 |
| errors / not certified | 0 | 0 | 0 | 0 | 0 | 0 |

Certified:

| unit | kind | cap used (s) | solve (s) | lrat-check (s) | cake_lpr (s) | proof (GB) | RSS (MB) |
|---|---|---|---|---|---|---|---|
| P5_1-8 | Q | 7000 | 4312.35 | 132.6 | 697.0 | 8.15 | 4415 |
| P4_7-9 | Q | 2082 | 545.89 | 66.7 | 359.6 | 3.47 | 4356 |
| P4_1-6-12 | H | 1093 | 670.41 | 73.7 | 380.1 | 3.72 | 4362 |

Min / median / max: solve 545.9 / 670.4 / 4312.4 s; lrat-check 66.7 / 73.7 / 132.6 s; cake_lpr 359.6 / 380.1 / 697.0 s;
proof 3.47 / 3.72 / 8.15 GB. The caps of P4_7-9 and P4_1-6-12 were reduced by lane.py to fit before END; both still
finished within them.

Not reached (lane stopped at 15:07:22Z with 554 s left before END): P4_1-13-14, P4_5-6-9, P4_5-12-15, P4_7-10-12 (P4 H);
P3_5-14 (P3 Q); P3_1-5-15, P3_1-11-14, P3_4-8-10, P3_5-7-13, P3_6-9-14 (P3 H).

## Other
- Largest solver RSS: 4415 MB (P5_1-8).
- No SAT, no proof rejection, no memory problem. Peak disk use was about 20 GB of the allowance, during the 8.15 GB proof.

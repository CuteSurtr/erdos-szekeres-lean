# C2P5 M50: C2P5B.tsv shard j = 0 of N = 50, H = 5.25, TASK commit 81cb025f

Started 2026-10-31 15:10:31 UTC (epoch 1793459431). END = 1793477431 (20:10:31 UTC). The lane finished all units at 18:10:12 UTC, about 2 h before END.

## Tools and checks (`tools.txt`)
- Built by `C2P/vendor/build_tools.sh` from the vendored sources (`vendor/tools-src.tar.xz`, manifest: all 196 files match). These are CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch). Nothing was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and base.json (2476faff…) both match.
- Cubes: l2cubes.py output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (14, rows idx ≡ 0 mod 50)
All 14 were **certified UNSAT**: lrat-check gave `c VERIFIED` and cake_lpr gave `s VERIFIED UNSAT` for every proof. No unit timed out, none went unreached and none ended in an error.

| case | Q certified | H certified |
|---|---|---|
| P1 | 1 (P1_6-7) | 4 (P1_2-7-9, P1_3-5-7, P1_4-5-7, P1_5-7-11) |
| P2 | 2 (P2_1-3, P2_7-11) | 1 (P2_7-10-11) |
| P3 | 1 (P3_4-7) | 5 (P3_1-4-8, P3_1-8-14, P3_4-6-9, P3_4-12-15, P3_5-13-14) |
| total | 4 | 10 |

Seconds and proof sizes, as min / median / max:

| | solve s | lrat-check s | cake_lpr s | proof GB |
|---|---|---|---|---|
| all 14 | 20.9 / 316.3 / 2078.2 | 10.6 / 47.1 / 75.5 | 109.1 / 304.1 / 497.1 | 0.216 / 3.27 / 5.36 |
| Q (4) | 532.1 / 793.0 / 2078.2 | 51.7 / 57.8 / 75.5 | 332.4 / 362.5 / 497.1 | 3.31 / 3.68 / 5.36 |
| H (10) | 20.9 / 124.7 / 603.3 | 10.6 / 28.4 / 55.8 | 109.1 / 202.9 / 343.4 | 0.216 / 1.67 / 3.64 |

The slowest unit was P2_1-3: a 2078 s solve and a 5.36 GB proof.

## Resources and anomalies
- The largest solver RSS was 4425 MB (P1_6-7). Memory was never a problem.
- No SAT was found, no proof was rejected and no memory problem occurred.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (one record per unit), `lane.log.tail`.

# C2P5 M05: C2P5A.tsv shard j = 5 of N = 37, H = 4.5, TASK commit 81cb025f

Started 2026-10-31 18:14:55 UTC (epoch 1793470495). END = 1793485795 (22:29:55 UTC). The lane finished all units at 19:20:09 UTC, about 3 h 10 min before END.

## Tools and checks (`tools.txt`)
- Built by `C2P/vendor/build_tools.sh` from the vendored sources (`vendor/tools-src.tar.xz`, manifest: all 196 files match). These are CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch). Nothing was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and base.json (2476faff…) both match.
- Cubes: l2cubes.py output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (4, rows idx ≡ 5 mod 37)
All 4 were **certified UNSAT**: lrat-check gave `c VERIFIED` and cake_lpr gave `s VERIFIED UNSAT` for every proof. No unit timed out, none went unreached and none ended in an error.

| case | Q certified | H certified |
|---|---|---|
| P4 | 1 (P4_1-11) | 3 (P4_5-7-9, P4_6-7-8, P4_7-9-12) |

Seconds and proof sizes, as min / median / max:

| | solve s | lrat-check s | cake_lpr s | proof GB |
|---|---|---|---|---|
| all 4 | 24.5 / 26.4 / 2782.4 | 12.3 / 13.0 / 100.7 | 109.6 / 112.8 / 533.6 | 0.215 / 0.216 / 6.28 |
| Q (1) | 2782.4 | 100.7 | 533.6 | 6.28 |
| H (3) | 24.5 / 25.7 / 27.0 | 12.3 / 12.7 / 13.2 | 109.6 / 112.7 / 112.8 | 0.215 / 0.216 / 0.216 |

## Resources and anomalies
- The largest solver RSS was 4416 MB (P4_1-11). Memory was never a problem.
- Peak disk use was about 18 GB of the 29 GB available at the start (during the P4_1-11 proof).
- No SAT was found, no proof was rejected and no memory problem occurred.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (one record per unit), `lane.log.tail`.

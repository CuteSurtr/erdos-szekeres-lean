# C2P2 M31 — LIST C2P2.tsv, shard j = 31 of N = 42, H = 2.5 h (TASK commit d266d2c3)

Start 2026-10-31 06:47:31 UTC (epoch 1793429251); END = start + 2.5 h − 15 min = 1793437351 (09:02:31 UTC).
Machine: 4 vCPU, 15 GB RAM, no swap (`env.txt`). One lane only (`run.sh`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest matched all 196 vendored files. It built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8)
  and lrat-check (2e3b2dc + E2 patch) from `vendor/tools-src.tar.xz`. Nothing was cloned or downloaded.
- Sanity checks: the bad LRAT was rejected by both checkers and the good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`).
  The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. base.cnf sha256 `b0061e90…d8ff1` and base.json sha256 `2476faff…b48` both match.
- Cubes: P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (`units.tsv`: idx ≡ 31 mod 42)
| idx | unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|
| 31 | P7_3-13 | P7 | Q | 6000 | certified UNSAT | 3154.2 | 107.8 | 588.3 | 6738112360 | 4382 |
| 73 | P6_1-4-12 | P6 | H | 1800 | certified UNSAT | 445.1 | 58.7 | 326.4 | 3470571047 | 4387 |
| 115 | P6_1-10-16 | P6 | H | 1800 | certified UNSAT | 414.1 | 60.3 | 340.3 | 3500954391 | 4370 |
| 157 | P6_2-7-10 | P6 | H | 1768 (time-limited) | certified UNSAT | 414.5 | 56.8 | 344.6 | 3455776450 | 4406 |
| 199 | P6_2-13-15 | P6 | H | 941 (time-limited) | certified UNSAT | 261.7 | 55.0 | 320.0 | 3211605652 | 4361 |
| 241 | P6_7-8-14 | P6 | H | — | not reached | | | | | |
| 283 | P6_8-10-11 | P6 | H | — | not reached | | | | | |

The lane stopped at 08:47:35 UTC with 895 s left before END, which is under its 15-minute start limit.

Counts by case and kind:
- P7 Q: 1 certified.
- P6 H: 4 certified, 2 not reached.
- Totals: 5 certified, 0 timed out (UNKNOWN), 2 not reached, 0 errors.

Certified units, min / median / max:
- solve: 261.7 / 414.5 / 3154.2 s
- lrat-check: 55.0 / 58.7 / 107.8 s
- cake_lpr: 320.0 / 340.3 / 588.3 s
- proof size: 3.21 / 3.47 / 6.74 GB

Each record holds both checker verdicts (`c VERIFIED` and `s VERIFIED UNSAT`), together with the CNF and proof sha256s.

## Resources and problems
- Largest solver RSS: 4406 MB (P6_2-7-10). cake_lpr ran with an 8000 MB heap (about 8.2 GB RSS). There were no memory problems.
- Peak disk use: about 18 GB of 252 GB (the 6.7 GB proof plus inputs).
- No SAT, no proof rejection, no ERROR records.

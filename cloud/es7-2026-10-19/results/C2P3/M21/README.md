# C2P3 M21: shard j = 21 of N = 50 of `lists/C2P3.tsv`, H = 2.5, task commit Z = 4f653319

Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-31 09:42:59 UTC (epoch 1793439779), END = 1793447879 (11:57:59 UTC). The lane stopped at 11:50:57 UTC because only 421 s were left before END (`lane done`).

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match). These are CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc with the E2 patch). Nothing was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF `SYMZ/zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`. Both sha256 values match: base.cnf `b0061e90…8ff1` and base.json `2476faff…2b48`.
- Cubes P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).
- TASK.md, the lists and `C2P/` are unchanged between Z and the checkout I ran.

## Units (`units.tsv`: 10 rows, idx ≡ 21 mod 50)

| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P6_3-10 | P6 | Q | 6000 | certified UNSAT | 3174.5 | 102.8 | 577.5 | 6.66 | 4415 |
| P6_1-12-15 | P6 | H | 1800 | certified UNSAT | 250.0 | 52.6 | 318.8 | 3.23 | 4358 |
| P6_3-8-13 | P6 | H | 1800 | certified UNSAT | 623.0 | 61.0 | 355.7 | 3.76 | 4403 |
| P6_8-10-14 | P6 | H | 1800 (run with 1739) | certified UNSAT | 113.7 | 33.4 | 199.8 | 1.62 | 3378 |
| P5_1-4-11 | P5 | H | 1800 (run with 1386) | certified UNSAT | 456.8 | 61.5 | 334.3 | 3.46 | 4388 |
| P5_1-11-15 | P5 | H | 1800 (run with 521) | certified UNSAT | 310.3 | 58.5 | 320.7 | 3.32 | 4406 |
| P5_2-8-13 | P5 | H | 1800 | not reached | | | | | |
| P5_6-8 | P5 | Q | 2400 | not reached | | | | | |
| P5_7-9-10 | P5 | H | 1800 | not reached | | | | | |
| P5_9-12 | P5 | Q | 2400 | not reached | | | | | |

Counts:
- Certified: 6. These are P6 Q 1, P6 H 3 and P5 H 2.
- Timed out (UNKNOWN): 0.
- Errors: 0.
- Not reached: 4. These are P5 H 2 and P5 Q 2.

Certified units (min / median / max):
- solve: 113.7 / 383.6 / 3174.5 s
- lrat-check: 33.4 / 59.8 / 102.8 s
- cake_lpr: 199.8 / 327.5 / 577.5 s
- proof size: 1.62 / 3.39 / 6.66 GB

Every certified record has `lrat_check` = `c VERIFIED` and `cake_lpr` = `s VERIFIED UNSAT`.

The largest solver RSS was 4415 MB (P6_3-10). There were no memory problems.

There was no SAT and no proof rejection. Every proof was deleted after its checks, and no CNF or proof files are committed.

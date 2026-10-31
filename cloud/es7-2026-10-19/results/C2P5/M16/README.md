# C2P5 M16

Values: V = M16, LIST = C2P5A.tsv, j = 16, N = 37, H = 4.5, Z = 81cb025f (TASK.md). Start 19:11Z (epoch 1793473868), END 1793489168 (23:26Z). The lane finished all units at 20:58:50Z.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` ran on the vendored sources. All 196 manifest files matched. It built CaDiCaL 3.0.1, cake_lpr and lrat-check (E2 patch). Nothing was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. sha256 b0061e90… (base.cnf) and 2476faff… (base.json), both as expected.
- Cubes: P1..P8 from `l2cubes.py` were byte-identical to `C2P/cubes/P{a}_cubes.txt`, 560 lines each.

## Units (`units.tsv`, rows of C2P5A.tsv with idx ≡ 16 mod 37)
| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P4_1-7 | P4 | Q | 8000 | UNSAT, certified | 2437.2 | 96.5 | 553.7 | 6.11 | 4433 |
| P4_2-5-9 | P4 | H | 2400 | UNSAT, certified | 358.1 | 55.8 | 337.7 | 3.36 | 4372 |
| P4_2-7-13 | P4 | H | 2400 | UNSAT, certified | 632.9 | 64.8 | 369.5 | 3.72 | 4377 |
| P4_5-9-14 | P4 | H | 2400 | UNSAT, certified | 351.5 | 56.8 | 334.5 | 3.37 | 4411 |
| P4_6-10-12 | P4 | H | 2400 | UNSAT, certified | 80.4 | 27.2 | 179.6 | 1.11 | 3162 |
| P3_4-6-7 | P3 | H | 2400 | UNSAT, certified | 80.6 | 25.7 | 167.1 | 1.15 | 3155 |

Counts:
- Certified: 6 of 6. That is P4 Q 1, P4 H 4 and P3 H 1.
- Timed out (UNKNOWN): 0.
- Not reached: 0.
- Errors: 0.

Certified statistics (min / median / max):
- solve: 80.4 / 354.8 / 2437.2 s
- lrat-check: 25.7 / 56.3 / 96.5 s
- cake_lpr: 167.1 / 336.1 / 553.7 s
- proof size: 1.11 / 3.36 / 6.11 GB

Largest solver RSS: 4433 MB.

There was no SAT result, no proof rejection and no memory problem. Every proof was deleted after checking.

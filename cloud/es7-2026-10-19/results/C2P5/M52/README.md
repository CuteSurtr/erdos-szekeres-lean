# C2P5 M52

Task `results/C2P5/TASK.md` (commit 81cb025f), with V = M52, LIST = C2P5B.tsv, j = 2, N = 50, H = 5.25.
The start was 2026-10-31 15:10:22 UTC (epoch 1793459422) and END = 1793477422 (20:10:22 UTC). The lane finished all its units at 18:17:38 UTC.
Machine: 4 vCPU, 15 GB RAM (`env.txt`).

## Tools and checks (`tools.txt`)
- I built the tools with `C2P/vendor/build_tools.sh` from the vendored sources only. All 196 manifest files match.
  - CaDiCaL 3.0.1: c60730422e758ef1cebe7aeddf2dda31c996bf04
  - cake_lpr: a36874a8b750b43fe4b385b8ddbf5b033e46a3fa
  - lrat-check: 2e3b2dc0ecf938addbd779d42877b6ed69d9a985, with the E2 patch
- Sanity checks: both checkers reject the bad LRAT and accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: the header is `p cnf 838032 16653336`. The sha256 of base.cnf and of base.json both match the expected values.
- Cubes: P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`: the 14 rows of C2P5B.tsv with idx ≡ 2 mod 50)
- 14 of 14 are certified UNSAT: both lrat-check (`c VERIFIED`) and cake_lpr (`s VERIFIED UNSAT`) accepted each proof.
- Timed out (UNKNOWN): 0. Not reached: 0. Errors: 0.
- By case and kind:
  - P1: 1 Q and 4 H, all certified.
  - P2: 2 Q and 1 H, all certified.
  - P3: 1 Q and 5 H, all certified.
- For certified units, as min / median / max:
  - Q (n=4):
    - solve: 470.3 / 942.2 / 2179.5 s
    - lrat-check: 49.3 / 58.1 / 83.9 s
    - cake_lpr: 325.1 / 376.7 / 510.5 s
    - proof: 3.27 / 3.89 / 5.23 GB
  - H (n=10):
    - solve: 18.95 / 105.5 / 528.9 s
    - lrat-check: 11.0 / 24.2 / 53.9 s
    - cake_lpr: 117.0 / 184.4 / 342.9 s
    - proof: 0.22 / 1.33 / 3.57 GB
- Largest solver RSS: 4475 MB (P3_1-8-16).
- SAT: none. Proof rejections: none. Memory problems: none.

## Per unit
| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof GB | solver RSS MB | certified |
|---|---|---|---|---|---|---|---|---|---|---|
| P2_1-5 | P2 | Q | 8000 | UNSATISFIABLE | 2179.45 | 83.9 | 510.5 | 5.23 | 4418 | True |
| P2_8-9 | P2 | Q | 8000 | UNSATISFIABLE | 470.3 | 49.6 | 325.1 | 3.27 | 4401 | True |
| P1_6-9 | P1 | Q | 8000 | UNSATISFIABLE | 491.4 | 49.3 | 348.0 | 3.36 | 4382 | True |
| P2_8-9-11 | P2 | H | 2400 | UNSATISFIABLE | 18.95 | 13.0 | 122.7 | 0.22 | 2387 | True |
| P1_2-7-11 | P1 | H | 2400 | UNSATISFIABLE | 322.54 | 46.3 | 324.0 | 3.27 | 4367 | True |
| P1_3-5-9 | P1 | H | 2400 | UNSATISFIABLE | 25.61 | 11.3 | 117.0 | 0.22 | 2665 | True |
| P1_4-5-9 | P1 | H | 2400 | UNSATISFIABLE | 22.04 | 11.2 | 117.8 | 0.22 | 2662 | True |
| P1_5-7-13 | P1 | H | 2400 | UNSATISFIABLE | 127.01 | 26.6 | 197.2 | 1.52 | 3374 | True |
| P3_4-9 | P3 | Q | 8000 | UNSATISFIABLE | 1393.02 | 66.6 | 405.3 | 4.42 | 4374 | True |
| P3_1-4-10 | P3 | H | 2400 | UNSATISFIABLE | 512.51 | 50.8 | 330.6 | 3.53 | 4367 | True |
| P3_1-8-16 | P3 | H | 2400 | UNSATISFIABLE | 528.9 | 51.2 | 342.9 | 3.57 | 4475 | True |
| P3_4-6-11 | P3 | H | 2400 | UNSATISFIABLE | 84.05 | 21.8 | 171.6 | 1.14 | 3173 | True |
| P3_4-13-15 | P3 | H | 2400 | UNSATISFIABLE | 410.66 | 53.9 | 338.4 | 3.40 | 4362 | True |
| P3_6-7-9 | P3 | H | 2400 | UNSATISFIABLE | 26.92 | 11.0 | 118.0 | 0.22 | 2648 | True |

Files: `out.jsonl` (one record per unit), `lane.log.tail` and `run.sh`.

# C2P4 M05

Settings: V = M05, LIST = C2P4.tsv, j = 5, N = 50, H = 2.5, Z = a46b478d. One lane, started 13:05Z. END was 15:16:34Z (epoch 1793459794).
Machine: 4 cores, 15 GB RAM (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built the tools from the vendored sources. All 196 manifest files matched.
  - CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2).
  - Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf and base.json both matched the expected values.
- Cubes: P1..P8 from `l2cubes.py` were byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (13 assigned, `units.tsv`)
| unit | case | kind | cap s | result | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P5_1-6 | P5 | Q | 7000 | certified UNSAT | 3028.4 | 107.9 | 624.8 | 7.23 | 4379 |
| P4_7-8 | P4 | Q | 3462* | certified UNSAT | 481.0 | 57.2 | 316.6 | 3.39 | 4373 |
| P4_1-6-11 | P4 | H | 1800 | certified UNSAT | 523.9 | 61.2 | 349.1 | 3.62 | 4352 |
| P4_1-12-16 | P4 | H | 1644* | certified UNSAT | 271.8 | 55.8 | 323.9 | 3.27 | 4416 |
| P4_5-6-8 | P4 | H | 982* | certified UNSAT | 30.2 | 14.3 | 125.2 | 0.21 | 2651 |
| P4_5-12-14 | P4 | H | 810* | certified UNSAT | 328.2 | 62.0 | 335.4 | 3.30 | 4362 |

\* The lane shortened this cap so that the checks would finish before END.

- Not reached: 7 units, because the lane stopped at 15:05Z with 674 s left.
  - P4: P4_7-10-11 (H).
  - P3: P3_5-13 (Q), P3_1-5-14, P3_1-11-13, P3_4-8-9, P3_5-7-12, P3_6-9-13 (all H).
- By case and kind:
  - P5: 1 Q certified.
  - P4: 1 Q certified; 4 H certified and 1 H not reached.
  - P3: 1 Q and 5 H not reached.
- Timed out (UNKNOWN): 0. Errors: 0. Every record has `"certified": true`.
- Certified units, as min / median / max:
  - solve: 30.2 / 404.6 / 3028.4 s;
  - lrat-check: 14.3 / 59.2 / 107.9 s;
  - cake_lpr: 125.2 / 329.7 / 624.8 s;
  - proof size: 0.21 / 3.34 / 7.23 GB.
- Largest solver RSS: 4416 MB. cake_lpr ran with an 8000 MB heap.
- No SAT, no proof rejection and no memory problem. Disk use peaked at about 19 GB used, with 21 GB free.

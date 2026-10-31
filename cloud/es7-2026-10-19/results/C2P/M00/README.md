# C2P M00: LIST = C2P.tsv, shard j = 0 of N = 42, H = 3.5 h

Task: `results/C2P/TASK.md` at fb2c59af. One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`).
Started 02:48 UTC on 2026-10-31; lane ran 02:51–05:53 UTC (END = 06:03:12 UTC, epoch 1793426592; `run.sh`).

## Tools and checks (`tools.txt`)
- CaDiCaL 3.0.1 c60730422e75; cake_lpr a36874a8b750; drat-trim lrat-check 2e3b2dc0ecf9 + E2 patch.
- cake_lpr example: `s VERIFIED UNSAT`. Sanity on {1},{-1}: LRAT `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `zcnf.py rot 17 7 --m 2 --hull`: `p cnf 838032 16653336`; sha256 of base.cnf and base.json match.
- Cubes P1..P8 from `l2cubes.py`: all 8 byte-identical to `C2P/cubes/`.
- `lane.py` unmodified, one lane, nothing else heavy.

## Units (54 = rows with idx ≡ 0 mod 42; `units.tsv`)
| | certified | UNKNOWN (timed out) | not reached | errors |
|---|---|---|---|---|
| total | 11 | 2 | 41 | 0 |
| P8 H (5) | 5 | 0 | 0 | 0 |
| P8 Q (1) | 1 | 0 | 0 | 0 |
| P7 H (6) | 5 | 1 (P7_3-8-16) | 0 | 0 |
| P7 Q (1) | 0 | 1 (P7_1-10) | 0 | 0 |
| P1–P6 (41: 33 H, 8 Q) | 0 | 0 | 41 | 0 |

Not reached by case/kind: P1 5H+2Q, P2 6H+1Q, P3 5H+2Q, P4 6H+1Q, P5 6H+1Q, P6 5H+1Q.

Certified: P8_1-6-13, P8_4-9-13, P8_1-4-7, P8_1-4-9, P8_2-13-15, P8_3-4 (Q), P7_2-8-13, P7_3-9-16, P7_8-9-13, P7_8-9-11, P7_3-4-12.

Timed out:
- P7_1-10 (Q, cap 2400): UNKNOWN after 2379 s solve.
- P7_3-8-16 (H, list cap 1800): the lane cut its cap to 518 s for the END limit; UNKNOWN after 514 s. It was not given its full cap.

Certified units (11), min / median / max:
- solve: 30.6 / 410.1 / 773.4 s
- lrat-check: 11.3 / 47.2 / 50.6 s
- cake_lpr: 112.1 / 302.2 / 327.8 s (heap 8000 MB every time, no retry)
- proof size: 0.21 / 3.33 / 3.76 GB (213,607,730 / 3,325,674,689 / 3,760,980,572 bytes)

## Memory, SAT, rejections
- Largest solver RSS: 4438 MB (P7_1-10). No memory problem.
- No SAT, no `SAT_FOUND`. No proof rejections: every UNSAT proof was accepted by lrat-check (`c VERIFIED`) and cake_lpr (`s VERIFIED UNSAT`). No `"certified": false` record and no ERROR status.

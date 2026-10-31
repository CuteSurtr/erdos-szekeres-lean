# C2P2 M39 — LIST = C2P2.tsv, shard j = 39 of N = 42, H = 2.5 h, TASK commit Z = d266d2c3

Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 06:46:54Z (epoch 1793429214), lane END = 1793437314 (09:01:54Z).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: built from the vendored sources only (no clone or download); the manifest check passed with all 196 files matching. CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch).
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. Both sha256 values match: base.cnf `b0061e90…d8ff1`, base.json `2476faff…2b48`.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (18 in `units.tsv`; one lane, `run.sh`)
| status | count | units |
|---|---|---|
| certified (UNSAT, both checkers accepted) | 3 | P7_1-2-10 (H), P7_1-5-9 (H), P7_1-6-12 (H) |
| timed out (UNKNOWN) | 2 | P7_1-11 (Q, cap 2400), P7_1-13 (Q, cap reduced by the lane to 2214 because of END) |
| not reached | 13 | P7_2-8-16, P7_2-12, P7_3-8-15, P7_3-11-13, P7_8-13, P7_9-13, P2_cover, P6_1-5-10, P6_1-12-13, P6_2-8-9, P6_3-7, P6_7-9-14, P6_8-11-14 |
| errors / certified false | 0 | — |

By case and kind:
- P7 H: 3 certified, 3 not reached (P7_2-8-16, P7_3-8-15, P7_3-11-13).
- P7 Q: 2 UNKNOWN, 3 not reached (P7_2-12, P7_8-13, P7_9-13).
- P2 cover: 1 not reached.
- P6 H: 5 not reached.
- P6 Q: 1 not reached (P6_3-7).

The lane stopped at 08:52:00Z with 593 s left before END, so it could not start another unit.

## Certified units (3, all H, P7)
| unit | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|
| P7_1-2-10 | 361.51 | 47.7 | 297.8 | 3,270,910,869 | 4365 |
| P7_1-5-9 | 461.66 | 48.8 | 306.6 | 3,476,980,502 | 4407 |
| P7_1-6-12 | 774.94 | 53.2 | 335.7 | 3,828,008,818 | 4370 |

min / median / max:
- solve: 361.5 / 461.7 / 774.9 s
- lrat-check: 47.7 / 48.8 / 53.2 s
- cake_lpr: 297.8 / 306.6 / 335.7 s
- proof size: 3.27 / 3.48 / 3.83 GB

## Other
- Largest solver RSS: 4408 MB (P7_1-13). There were no memory problems.
- SAT: none, and no `SAT_FOUND`.
- Proof rejections: none.
- Files: `out.jsonl` (5 records) and `lane.log.tail`.

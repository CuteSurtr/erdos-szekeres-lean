# C2P / M40 (LIST C2P.tsv, shard 40 of 42, H = 3.5, Z = fb2c59af)

**Result: 12 of 53 units certified UNSAT (all of P8 and P7 in this shard); 41 not reached; no timeout, no error, no SAT.**

## Tools and checks (`tools.txt`)
- CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8, `make cake_lpr`), drat-trim lrat-check (2e3b2dc) with
  `results/E2/tools/lrat-check-E2.patch`. Sanity checks pass: cake_lpr example `s VERIFIED UNSAT`; on {1},{-1} the
  LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` accepted by both.
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json both match.
- Cubes: all 8 `P{a}.txt` byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Lane
Started 03:03:17Z (session start 1793415422, END 1793427122 = 06:12:02Z; `run.sh`). Lane stopped at 05:57:21Z
with 880 s left (< 15 min, so no new unit). Records in `out.jsonl`, log tail in `lane.log.tail`.

## Units (53: `units.tsv`)
| case | kind | units | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|---|
| P8 | H | 3 | 3 | 0 | 0 | 0 |
| P8 | Q | 2 | 2 | 0 | 0 | 0 |
| P7 | H | 6 | 6 | 0 | 0 | 0 |
| P7 | Q | 1 | 1 | 0 | 0 | 0 |
| P6 | H / Q | 4 / 2 | 0 | 0 | 6 | 0 |
| P5 | H / Q / cover | 5 / 1 / 1 | 0 | 0 | 7 | 0 |
| P4 | H / Q | 5 / 2 | 0 | 0 | 7 | 0 |
| P3 | H / Q | 6 / 1 | 0 | 0 | 7 | 0 |
| P2 | H / Q | 6 / 1 | 0 | 0 | 7 | 0 |
| P1 | H / Q | 5 / 2 | 0 | 0 | 7 | 0 |
| total | | 53 | 12 (9 H, 3 Q) | 0 | 41 (31 H, 9 Q, 1 cover: P5_cover) | 0 |

Certified units (both lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, heap 8000 MB every time):
P8_1-9-15, P8_9-13, P8_1-4-5, P8_3-14, P8_2-3-4, P7_3-15-16, P7_1-3-6, P7_2-3-12, P7_1-15, P7_1-4-14,
P7_9-12-13, P7_2-14-15.

| certified (12) | min | median | max |
|---|---|---|---|
| solve s | 25.98 | 255.51 | 1978.65 (P8_3-14, Q) |
| lrat-check s | 12.7 | 53.65 | 92.1 |
| cake_lpr s | 102.2 | 292.8 | 489.1 |
| proof size | 0.22 GB | 3.25 GB | 5.75 GB |

Q units are the slowest (1086–1979 s solve); H units 26–418 s.

## Resources and problems
- Largest solver RSS: 4468.7 MB (P8_9-13). No memory problem (15 GB machine, no swap).
- No SAT, no proof rejection, no cake_lpr heap exhaustion, no `"certified": false` record, no ERROR status.

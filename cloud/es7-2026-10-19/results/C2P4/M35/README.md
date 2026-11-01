# C2P4 M35

Machine M35, list `C2P4.tsv`, shard j = 35 of N = 50, budget H = 2.5 h, task commit Z = a46b478d.
Start 2026-10-31 13:01:41Z (epoch 1793451701); lane END = 1793459801 (15:16:41Z). Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc + E2 patch) from the vendored `vendor/tools-src.tar.xz`. All 196 manifest hashes matched. No code was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF header `p cnf 838032 16653336`. The sha256 of base.cnf and base.json both match the expected values.
- Cubes P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (19 total: idx ≡ 35 mod 50; see `units.tsv`)
| case | kind | units | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|---|---|
| P5 | Q | 1 | 0 | 1 (P5_6-16) | 0 | 0 |
| P5 | H | 5 | 2 (P5_1-2-14, P5_2-6-10) | 0 | 3 | 0 |
| P4 | Q | 1 | 0 | 0 | 1 | 0 |
| P4 | H | 5 | 0 | 0 | 5 | 0 |
| P3 | Q | 1 | 0 | 0 | 1 | 0 |
| P3 | H | 6 | 0 | 0 | 6 | 0 |
| **total** | | 19 | 2 | 1 | 16 | 0 |

- P5_6-16 (Q, cap 6000 s) used its whole cap and returned UNKNOWN after 5942 s. Its partial proof was about 9 GB.
- Because that unit used most of the budget, the next two H units got shortened caps from lane.py (1296 s and 617 s). Both still finished inside those caps.
- Not reached: P5_2-14-15, P5_6-12-15, P5_8-10-13, P4_5-7, P4_1-3-7, P4_1-9-12, P4_2-6-14, P4_5-8-16, P4_6-9-15, P3_1-11, P3_1-2-6, P3_1-7-14, P3_4-5-11, P3_4-10-15, P3_5-10-13, P3_7-10-12.

## Certified units (both checkers accepted)
| unit | solve s | lrat-check s | cake_lpr s | proof bytes |
|---|---|---|---|---|
| P5_1-2-14 | 288.51 | 47.1 | 328.5 | 3,207,344,079 |
| P5_2-6-10 | 540.55 | 52.5 | 340.1 | 3,485,686,979 |

With only two certified units, the minimum and maximum are the two values and the median is their mean:
- solve: 288.5 / 414.5 / 540.6 s
- lrat-check: 47.1 / 49.8 / 52.5 s
- cake_lpr: 328.5 / 334.3 / 340.1 s
- proof: 3.21 / 3.35 / 3.49 GB

## Other
- Largest solver RSS was 4394 MB (P5_1-2-14), so memory was never a problem.
- No SAT result, no proof rejection, no ERROR record and no `certified: false` record.
- Files: `out.jsonl` (all records), `lane.log.tail`, `run.sh`, `units.tsv`, `tools.txt`, `env.txt`.

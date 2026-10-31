# C2P5 M57: list C2P5B.tsv, shard j = 7 of N = 50, H = 5.25 (task commit 81cb025f)

Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Lane started 2026-10-31 15:12:49Z with END = 1793478330 (20:25:30Z, `run.sh`); it finished all 14 units at 18:55:04Z ("lane done").

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored sources only: all 196 manifest files matched. Versions: CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. sha256 of base.cnf `b0061e90…d8ff1` and of base.json `2476faff…b48`, both as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, `out.jsonl`)
14 units: 14 certified, 0 timed out, 0 not reached, 0 errors. Every unit is UNSATISFIABLE with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT` at 8000 MB heap.

| case | kind | units | certified |
|---|---|---|---|
| P2 | Q | 1 (P2_3-4) | 1 |
| P1 | Q | 2 (P1_2-4, P1_7-9) | 2 |
| P1 | H | 5 (P1_2-3-8, P1_2-7-16, P1_3-5-14, P1_4-5-14, P1_5-8-13) | 5 |
| P3 | Q | 1 (P3_4-14) | 1 |
| P3 | H | 5 (P3_1-4-15, P3_1-9-14, P3_4-6-16, P3_5-6-10, P3_6-7-14) | 5 |

Certified units, as min / median / max:

| | solve s | lrat-check s | cake_lpr s | proof GB |
|---|---|---|---|---|
| all 14 | 26.0 / 433.6 / 3308.4 | 12.0 / 50.5 / 93.0 | 116.7 / 334.6 / 591.0 | 0.22 / 3.37 / 6.29 |
| Q (4) | 508.3 / 543.2 / 3308.4 | 49.8 / 51.9 / 93.0 | 319.5 / 331.6 / 591.0 | 3.31 / 3.38 / 6.29 |
| H (10) | 26.0 / 372.0 / 565.2 | 12.0 / 48.7 / 57.2 | 116.7 / 337.4 / 360.8 | 0.22 / 3.32 / 3.62 |

The slowest unit was P3_4-14 (Q), with a 3308 s solve and a 6.29 GB proof.

## Resources and problems
- Largest solver RSS: 4479 MB (P3_1-9-14). No memory problem occurred.
- Lowest free disk observed: about 22 GB.
- No SAT answer, no proof rejection, no ERROR status, and no uncertified record.

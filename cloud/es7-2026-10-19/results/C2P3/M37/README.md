# C2P3 M37 (LIST = C2P3.tsv, shard j = 37 of N = 50, H = 2.5, task commit 4f653319)

Start 2026-10-31 09:42:49Z (epoch 1793439769), lane END 1793447869 (11:57:49Z). Machine: 4 cores, 15 GB RAM (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` from the vendored sources: manifest all 196 files match; CaDiCaL 3.0.1 (c6073042),
  cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). cake_lpr example `s VERIFIED UNSAT`; sanity: bad LRAT
  rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`). No code cloned or downloaded.
- Base CNF `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…2b48`, both as expected.
- Cubes: `l2cubes.py` output for P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (10 rows, `units.tsv`)
| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P6_2-14 | P6 | Q | 6000 | certified UNSAT | 1574.97 | 81.4 | 442.8 | 5.05 | 4365 |
| P6_11-12 | P6 | Q | 4800 | certified UNSAT | 529.17 | 60.1 | 335.1 | 3.55 | 4361 |
| P6_2-8-10 | P6 | H | 1800 | certified UNSAT | 325.96 | 54.5 | 316.6 | 3.31 | 4385 |
| P6_7-8-15 | P6 | H | 1800 | certified UNSAT | 229.63 | 53.5 | 325.0 | 3.14 | 4398 |
| P6_10-11-12 | P6 | H | 1800 | certified UNSAT | 27.57 | 13.7 | 117.2 | 0.22 | 2643 |
| P5_1-7-11 | P5 | H | 1800 | certified UNSAT | 551.06 | 67.3 | 346.1 | 3.60 | 4370 |
| P5_1-16 | P5 | Q | 2400 (lane cap 1754) | certified UNSAT | 1419.52 | 78.7 | 439.0 | 4.92 | 4408 |
| P5_2-10-14 | P5 | H | 1800 | not reached | | | | | |
| P5_6-9-16 | P5 | H | 1800 | not reached | | | | | |
| P5_7-11-15 | P5 | H | 1800 | not reached | | | | | |

Counts by case and kind:
- Certified 7: P6 Q 2, P6 H 3, P5 Q 1, P5 H 1.
- Timed out (UNKNOWN) 0. Errors 0. Certified false 0.
- Not reached 3: P5 H 3 (lane stopped at 11:51:17Z with 391 s left before END).

Certified units (min / median / max): solve 27.57 / 529.17 / 1574.97 s; lrat-check 13.7 / 60.1 / 81.4 s;
cake_lpr 117.2 / 335.1 / 442.8 s; proof size 0.217 / 3.55 / 5.05 GB.

P5_1-16 has list cap 2400 s; lane.py capped its solve at 1754 s to keep 10 minutes for checks before END, and it was
solved within that (1419.52 s).

Largest solver RSS: 4407.6 MB (P5_1-16). No SAT, no proof rejection, no memory or disk problem
(free disk never below about 22.8 GB).

Files: `out.jsonl` (one record per unit), `lane.log.tail`, `units.tsv`, `run.sh`, `tools.txt`, `env.txt`.

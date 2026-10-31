# C2P2 M33

Shard j = 33 of N = 42 of `C2P2/lists/C2P2.tsv`, H = 2.5 h, TASK.md at commit d266d2c3 (unchanged at checkout).
Lane started 06:50:32Z, END = 1793437358 (09:02:38Z); lane stopped at 08:52:16Z with 621 s left.

## Tools and checks (`tools.txt`)
- Built by `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match):
  CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF `zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json as expected.
- Cubes P1..P8 from `l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (7, `units.tsv`)
| unit | case | kind | cap (s) | result | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P7_8-15 | P7 | Q | 6000 | certified | 5043.3 | 141.6 | 726.0 | 8.98 | 4388 |
| P6_1-4-14 | P6 | H | 1800 (lane cap 1348) | certified | 325.2 | 55.0 | 310.8 | 3.34 | 4396 |
| P6_1-11-12 | P6 | H | 1800 (lane cap 646) | certified | 261.2 | 52.4 | 300.0 | 3.20 | 4392 |
| P6_2-7-12 | P6 | H | 1800 | not reached | | | | | |
| P6_2-14 | P6 | Q | 2400 | not reached | | | | | |
| P6_7-8-16 | P6 | H | 1800 | not reached | | | | | |
| P6_8-10-13 | P6 | H | 1800 | not reached | | | | | |

Counts:
- certified 3: P7 Q 1 (P7_8-15), P6 H 2.
- timed out (UNKNOWN) 0; errors 0; certified false 0.
- not reached 4: P6 H 3, P6 Q 1.

Certified units (min / median / max): solve 261.2 / 325.2 / 5043.3 s; lrat-check 52.4 / 55.0 / 141.6 s;
cake_lpr 300.0 / 310.8 / 726.0 s; proof 3.20 / 3.34 / 8.98 GB.

Largest solver RSS: 4396 MB (P6_1-4-14). The largest cake_lpr RSS seen was about 8.2 GB (heap 8000 MB);
memory peaked at about 8 GB used of 15 GB. No memory problem.

No SAT, no proof rejection, no memory or disk problem. Disk peak about 20 GB used of 252 GB (the 9 GB proof was deleted
after its checks).

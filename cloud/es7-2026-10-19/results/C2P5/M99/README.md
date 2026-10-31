# C2P5 M99: LIST = C2P5B.tsv, shard j = 49 of N = 50, H = 5.25, TASK commit 81cb025f

## Tools and checks (`tools.txt`)
- CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch), built by
  `C2P/vendor/build_tools.sh` only from the vendored `vendor/tools-src.tar.xz`. The manifest check passed for all 196 files.
- Sanity checks: both checkers reject the bad LRAT and accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF (`SYMZ/zcnf.py rot 17 7 --m 2 --hull`): its header is `p cnf 838032 16653336`, and the sha256 of base.cnf and base.json both match the expected values.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Run
There was one lane (`run.sh`), started at 15:12:46Z with END = start + 5 h. It finished all units at 18:14:55Z ("lane done").

## Units: 18 of 18 certified (both checkers accepted), 0 timed out, 0 not reached, 0 errors

| case | Q certified | H certified |
|---|---|---|
| P1 | 1 (P1_5-13) | 4 |
| P2 | 1 (P2_7-10) | 6 |
| P3 | 1 (P3_4-6) | 5 |
| total | 3 | 15 |

All 18 units are certified, with seconds and proof sizes as follows (min / median / max):

| | solve s | lrat-check s | cake_lpr s | proof GB |
|---|---|---|---|---|
| all 18 | 17.8 / 241.7 / 1769.4 | 12.5 / 53.7 / 85.7 | 109.0 / 308.7 / 469.5 | 0.21 / 3.19 / 5.16 |
| Q (3) | 453.7 / 491.4 / 1769.4 | 56.1 / 63.0 / 85.7 | 312.2 / 325.5 / 469.5 | 3.39 / 3.44 / 5.16 |
| H (15) | 17.8 / 88.2 / 512.8 | 12.5 / 25.9 / 60.8 | 109.0 / 173.7 / 359.2 | 0.21 / 1.23 / 3.60 |

The hardest unit was P1_5-13 (Q): solve 1769 s, proof 5.16 GB. Every cake_lpr check ran with an 8000 MB heap and none needed the retry.

Largest solver RSS: 4415 MB (P3_1-4-7).

There was no SAT, no proof rejection, no `"certified": false` record, no ERROR status and no memory problem.

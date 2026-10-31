# C2P3 M17: shard j = 17 of C2P3.tsv (N = 50), H = 2.5 h, task commit 4f653319

Start 2026-10-31 09:42:45Z (epoch 1793439765), END = start + 2.5 h - 15 min = 11:57:45Z (1793447865). Lane started 09:46:00Z, finished 11:47:49Z ("stop: 595 s left").

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 files of the vendored sources match MANIFEST.sha256. Built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc, E2 patch). Nothing was cloned or downloaded.
- Sanity: the bad LRAT is rejected by both checkers. The good one is accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`). The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF `zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`, and the sha256 of base.cnf (b0061e90...) and base.json (2476faff...) match.
- Cubes P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (10 rows with idx ≡ 17 mod 50)
| idx | unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof GB | solver RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|
| 17 | P6_2-7 | P6 | Q | 6000 | certified UNSAT | 3183.0 | 95.9 | 550.5 | 6.90 | 4418 |
| 67 | P6_1-11-15 | P6 | H | 1800 | certified UNSAT | 297.9 | 49.4 | 298.8 | 3.33 | 4400 |
| 117 | P6_3-7-16 | P6 | H | 1800 | certified UNSAT | 430.4 | 57.0 | 332.6 | 3.57 | 4425 |
| 167 | P6_8-9-15 | P6 | H | 1800 | certified UNSAT | 120.5 | 33.0 | 201.5 | 1.54 | 3389 |
| 217 | P5_1-4-7 | P5 | H | 1576 (time-limited) | certified UNSAT | 270.0 | 55.3 | 324.1 | 3.24 | 4424 |
| 267 | P5_1-11 | P5 | Q | 915 (time-limited) | UNKNOWN (timeout) | 906.5 | – | – | – | 4408 |
| 317, 367, 417, 467 | P5_2-8-9, P5_6-7-13, P5_7-8-13, P5_9-10-13 | P5 | H | 1800 | not reached | | | | | |

By case and kind:
- P6 Q: 1 certified.
- P6 H: 3 certified.
- P5 H: 1 certified, 4 not reached.
- P5 Q: 1 timed out (cap shortened to 915 s by END; it was not refuted).

Totals: 5 certified, 1 UNKNOWN, 4 not reached, 0 errors.

Certified units (5), as minimum / median / maximum:
- solve: 120.5 / 297.9 / 3183.0 s
- lrat-check: 33.0 / 55.3 / 95.9 s
- cake_lpr: 201.5 / 324.1 / 550.5 s
- proof size: 1.54 / 3.33 / 6.90 GB

## Other
- Largest solver RSS: 4425 MB. cake_lpr ran with an 8000 MB heap (about 8.2 GB RSS seen). There were no memory problems, and disk usage peaked at about 47 %.
- No SAT, no proof rejection, no `certified: false` and no ERROR records.

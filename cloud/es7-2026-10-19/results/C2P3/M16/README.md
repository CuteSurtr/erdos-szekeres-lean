# C2P3 M16: shard j = 16 of N = 50 of C2P3.tsv (H = 2.5 h, task commit 4f653319)

Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 09:42:55Z (epoch 1793439775); lane END = 1793447875 (11:57:55Z).

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match):
  CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch. Nothing was cloned or downloaded.
- Sanity checks: both checkers reject the bad LRAT and accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- Base: `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and base.json (2476faff…) both match.
- Cubes P1..P8 from `l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (10 rows with idx ≡ 16 mod 50)
| unit | case | kind | status | cap s | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P6_1-16 | P6 | Q | certified | 6000 | 1315.6 | 74.6 | 418.3 | 4,850,305,014 | 4422 |
| P6_1-10-12 | P6 | H | certified | 1800 | 294.1 | 52.7 | 309.5 | 3,282,696,847 | 4355 |
| P6_3-7-15 | P6 | H | certified | 1800 | 500.6 | 57.0 | 334.7 | 3,661,747,628 | 4429 |
| P6_8-9-14 | P6 | H | certified | 1800 | 84.5 | 24.7 | 161.4 | 1,114,775,139 | 3124 |
| P5_1-4-6 | P5 | H | certified | 1800 | 262.6 | 54.3 | 303.0 | 3,254,298,511 | 4412 |
| P5_1-10-16 | P5 | H | certified | 1800 | 413.0 | 59.7 | 334.6 | 3,506,594,394 | 4372 |
| P5_2-8 | P5 | Q | UNKNOWN (timed out) | 2108* | 2083.6 | – | – | – | 4417 |
| P5_6-7-12 | P5 | H | not reached | 1800 | | | | | |
| P5_7-8-12 | P5 | H | not reached | 1800 | | | | | |
| P5_9-10-12 | P5 | H | not reached | 1800 | | | | | |

\* The list cap is 2400 s. lane.py lowered it to 2108 s so that 10 minutes would remain before END, so this timeout is not a full-cap result.

Counts by case and kind:
- P6: Q 1/1 certified; H 3/3 certified.
- P5: Q 0/1 (1 timed out); H 2/5 certified, 3 not reached.
- Total: 6 certified, 1 timed out, 3 not reached, 0 errors.

Certified units (6), min / median / max:
- solve s: 84.5 / 353.5 / 1315.6
- lrat-check s: 24.7 / 55.7 / 74.6
- cake_lpr s: 161.4 / 322.1 / 418.3
- proof bytes: 1.11 GB / 3.39 GB / 4.85 GB

Every proof got `c VERIFIED` from lrat-check and `s VERIFIED UNSAT` from cake_lpr, and was then deleted.

Largest solver RSS: 4429 MB (P6_3-7-15). cake_lpr ran with an 8000 MB heap.

There was no SAT, no proof rejection, no ERROR record and no memory problem. The proofs used at most about 5 GB of disk.

Note: the first push (env.txt) lost several races on es7-cloud. It went to the fallback branch `es7-fallback-c2p3-m16`, and was pushed to es7-cloud as well right after. Everything is on es7-cloud.

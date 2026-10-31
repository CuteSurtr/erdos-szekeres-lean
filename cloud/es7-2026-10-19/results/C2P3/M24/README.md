# C2P3 M24 (LIST = C2P3.tsv, j = 24, N = 50, H = 2.5, task commit 4f653319)

Machine: 4 cores, 15 GB RAM (`env.txt`). Start 09:42:40Z (epoch 1793439760), END = 1793447860 (11:57:40Z). The lane finished all units at 11:34:15Z.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest of all 196 vendored files matches; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example `s VERIFIED UNSAT`.
- Base CNF `p cnf 838032 16653336`; sha256 base.cnf b0061e90…d8ff1 and base.json 2476faff…2b48, both as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (10): 10 certified, 0 timed out, 0 not reached, 0 errors

| case | kind | units | certified |
|---|---|---|---|
| P6 | Q (cap 6000) | 1 | 1 |
| P6 | H | 3 | 3 |
| P5 | H | 6 | 6 |

| unit | kind | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|
| P6_9-13 | Q | 1466.63 | 82.7 | 436.2 | 4819346774 | 4355 |
| P6_1-15-16 | H | 216.58 | 53.6 | 299.6 | 3108077230 | 4414 |
| P6_3-9-11 | H | 305.88 | 55.1 | 318.1 | 3296689599 | 4357 |
| P6_8-11-13 | H | 106.48 | 33.4 | 203.1 | 1575382688 | 3400 |
| P5_1-6-8 | H | 356.50 | 55.9 | 319.4 | 3312899239 | 4397 |
| P5_1-12-13 | H | 281.92 | 62.8 | 315.1 | 3205678520 | 4357 |
| P5_2-8-16 | H | 449.06 | 61.7 | 348.3 | 3564808458 | 4415 |
| P5_6-8-11 | H | 28.99 | 14.3 | 115.6 | 216156990 | 2663 |
| P5_7-9-13 | H | 109.64 | 32.4 | 205.1 | 1525370096 | 3399 |
| P5_10-11-12 | H | 20.31 | 13.4 | 115.6 | 214157800 | 2644 |

Certified units (min / median / max): solve 20.3 / 249.3 / 1466.6 s; lrat-check 13.4 / 54.4 / 82.7 s; cake_lpr 115.6 / 307.4 / 436.2 s; proof 0.21 / 3.16 / 4.82 GB.

Largest solver RSS: 4415 MB (P5_2-8-16).

No SAT, no proof rejection, no memory problem. Records: `out.jsonl`; lane log: `lane.log.tail`.

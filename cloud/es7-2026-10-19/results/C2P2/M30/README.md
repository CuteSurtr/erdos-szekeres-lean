# C2P2 M30: shard j = 30 of N = 42 of `C2P2.tsv` (H = 2.5, TASK commit d266d2c3)

Start 2026-10-31 06:47:26 UTC (epoch 1793429246); END = 09:02:26 UTC (epoch 1793437346). One lane (`run.sh`), started 06:49:41, finished 08:50:59 (`stop: 686 s left`, under the 15-minute start limit).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 vendored files match `MANIFEST.sha256`; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…2b48`, both as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 subcases each).

## Units (`units.tsv`, 7 units: idx ≡ 30 mod 42)

| idx | unit | kind | cap s | result | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| 30 | P7_3-11 | Q | 6000 | certified UNSAT | 4167.7 | 122.9 | 658.2 | 7.92 | 4384 |
| 72 | P6_1-4-11 | H | 1800 | certified UNSAT | 433.0 | 55.5 | 321.5 | 3.43 | 4405 |
| 114 | P6_1-10-15 | H | 1800 (run capped 1529) | certified UNSAT | 374.6 | 57.1 | 319.5 | 3.43 | 4369 |
| 156 | P6_2-7-9 | H | 1800 (run capped 765) | certified UNSAT | 301.2 | 55.0 | 311.6 | 3.30 | 4398 |
| 198 | P6_2-13-14 | H | 1800 | not reached | | | | | |
| 240 | P6_7-8-13 | H | 1800 | not reached | | | | | |
| 282 | P6_8-10 | Q | 2400 | not reached | | | | | |

By case and kind:
- P7 Q: 1 certified.
- P6 H: 3 certified, 2 not reached.
- P6 Q: 1 not reached.
- Timed out (UNKNOWN): 0. Errors / `certified: false`: 0.

Certified units (4), min / median / max:
- solve: 301.2 / 403.8 / 4167.7 s
- lrat-check: 55.0 / 56.3 / 122.9 s
- cake_lpr (heap 8000 MB, no retry needed): 311.6 / 320.5 / 658.2 s
- proof size: 3.30 / 3.43 / 7.92 GB (all proofs deleted after checking)

Largest solver RSS: 4405 MB (P6_1-4-11). P7_3-11 (one of the first-wave 6000 s timeouts) is now closed in 4168 s.

No SAT, no proof rejection, no memory or disk problem (lowest free disk ~20 GB, during the 7.9 GB P7_3-11 proof).
Not reached (for a later wave): P6_2-13-14, P6_7-8-13, P6_8-10.

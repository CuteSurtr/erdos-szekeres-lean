# C2P3 M02 (LIST = C2P3.tsv, j = 2, N = 50, H = 2.5, task commit 4f653319)

Start 2026-10-31 09:42:43Z (epoch 1793439763); lane END 11:57:43Z (start + 2.5 h - 15 min). Machine: 4 cores, 15 GB RAM (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 vendored files match `MANIFEST.sha256`; built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing cloned or downloaded.
- Sanity: cake_lpr example `s VERIFIED UNSAT`; bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`).
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…b48`, both as expected.
- Cubes: `l2cubes.py` output for P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (10: idx ≡ 2 mod 50)
| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P7_2-9 | P7 | Q | 6000 | certified | 4225.9 | 120.5 | 674.8 | 8.66 | 4422 |
| P7_3-8-16 | P7 | H | 1800 | certified | 444.6 | 51.2 | 326.4 | 3.61 | 4369 |
| P6_2-11-16 | P6 | H | 1800 (1405) | certified | 342.8 | 49.8 | 306.1 | 3.43 | 4362 |
| P6_7-11-13 | P6 | H | 1800 (695) | certified | 103.2 | 29.9 | 187.7 | 1.69 | 3407 |
| P5_1-2-16 | P5 | H | 1800 (369) | certified | 216.6 | 46.9 | 287.5 | 3.22 | 4403 |
| P5_1-9 | P5 | Q | 2400 | not reached | | | | | |
| P5_2-6-13, P5_2-13-14, P5_6-12-13, P5_8-10-11 | P5 | H | 1800 | not reached | | | | | |

Counts by case and kind:
- Certified 5: P7 Q 1, P7 H 1, P6 H 2, P5 H 1.
- Timed out (UNKNOWN) 0. Errors 0. Proof rejections 0 (all with cake_lpr heap 8000 MB).
- Not reached 5: P5 Q 1 (P5_1-9), P5 H 4 (lane stopped at 11:50:54Z with 408 s left before END).

Certified units (min / median / max): solve 103.2 / 342.8 / 4225.9 s; lrat-check 29.9 / 49.8 / 120.5 s; cake_lpr 187.7 / 306.1 / 674.8 s; proof size 1.69 / 3.43 / 8.66 GB.

Largest solver RSS: 4422 MB (P7_2-9). No SAT, no proof rejection, no memory or disk problem (peak disk use about 21 GB with the 8.66 GB proof).

Files: `out.jsonl` (one record per unit, with CNF and proof sha256), `lane.log.tail`, `units.tsv`, `run.sh`, `tools.txt`, `env.txt`.

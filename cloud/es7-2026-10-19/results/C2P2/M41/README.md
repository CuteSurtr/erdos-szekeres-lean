# C2P2 M41 — LIST C2P2.tsv, shard j = 41 of N = 42, H = 2.5 h, TASK commit d266d2c3

Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 06:47:31Z (epoch 1793429251), END 1793437351 (09:02:31Z).

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz` (manifest: all 196 files match; nothing cloned or downloaded): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF `zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…bb48` — both match.
- Cubes P1..P8 from `l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (18 rows, idx ≡ 41 mod 42; `units.tsv`)
| case | kind | units | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|---|
| P7 | H | 9 | 9 | 0 | 0 | 0 |
| P7 | Q | 2 | 1 | 0 | 1 | 0 |
| P6 | H | 3 | 0 | 0 | 3 | 0 |
| P6 | Q | 4 | 0 | 0 | 4 | 0 |
| **total** | | **18** | **10** | **0** | **8** | **0** |

Certified (all UNSATISFIABLE, lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`): P7_1-4-5, P7_1-5-12, P7_1-8-14, P7_1-11-14, P7_1-14-16, P7_2-9-13, P7_2-13-15, P7_3-9-13, P7_8-9-15 (H), P7_9-10 (Q).

Not reached (lane stopped with 628 s left before END): P7_9-14 (Q), P6_1-2 (Q), P6_1-7 (Q), P6_1-12-15 (H), P6_2-8-11 (H), P6_3-7-9 (H), P6_7-10 (Q), P6_8-12 (Q).

Note: the lane lowered the cap of the last two units to fit END (P7_8-9-15 cap 1349 s, P7_9-10 cap 1026 s); both finished well inside it.

### Certified units: min / median / max
- solve: 87.8 / 396.7 / 578.1 s
- lrat-check: 24.4 / 56.6 / 66.1 s
- cake_lpr: 170.8 / 332.1 / 356.8 s
- proof size: 1.12 / 3.41 / 3.66 GB

| unit | kind | cap s | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|
| P7_1-4-5 | H | 1800 | 87.81 | 24.4 | 170.8 | 1.12 | 3109 |
| P7_1-5-12 | H | 1800 | 525.94 | 59.3 | 343.6 | 3.62 | 4394 |
| P7_1-8-14 | H | 1800 | 543.58 | 66.1 | 356.8 | 3.66 | 4437 |
| P7_1-11-14 | H | 1800 | 295.17 | 54.6 | 320.5 | 3.25 | 4359 |
| P7_1-14-16 | H | 1800 | 232.86 | 53.7 | 311.4 | 3.18 | 4362 |
| P7_2-9-13 | H | 1800 | 498.17 | 61.4 | 348.9 | 3.56 | 4368 |
| P7_2-13-15 | H | 1800 | 240.94 | 52.7 | 314.2 | 3.20 | 4399 |
| P7_3-9-13 | H | 1800 | 519.41 | 59.1 | 350.4 | 3.62 | 4366 |
| P7_8-9-15 | H | 1349 | 105.42 | 28.7 | 184.2 | 1.34 | 3404 |
| P7_9-10 | Q | 1026 | 578.11 | 58.6 | 345.8 | 3.58 | 4369 |

## Largest solver RSS
4437 MB (P7_1-8-14). No memory problems; disk stayed at ≥ 24 GB free.

## SAT, rejections, errors
No SAT (no `SAT_FOUND`), no proof rejected, no `certified: false` record, no ERROR status.

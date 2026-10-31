# C2P5 M00: LIST C2P5A.tsv, shard j = 0 of N = 37, H = 4.5 h (TASK at 81cb025f)

Start 2026-10-31 15:58:48Z (epoch 1793462328), END 1793477628 (20:13:48Z). Lane finished at 19:22:07Z with all units done.

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz` only (nothing cloned or downloaded): manifest all 196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch).
- Sanity: cake_lpr example `s VERIFIED UNSAT`; bad LRAT rejected by both checkers, good LRAT accepted by both.
- Base CNF `SYMZ/zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…bf472b48`, both as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, rows idx ≡ 0 mod 37): 10 units, 10 certified
| case | kind | units | certified | timed out | not reached | errors |
|---|---|---|---|---|---|---|
| P5 | Q (cap 10000) | 1 | 1 | 0 | 0 | 0 |
| P3 | H (cap 2400) | 2 | 2 | 0 | 0 | 0 |
| P2 | H (cap 2400) | 7 | 7 | 0 | 0 | 0 |
| total | | 10 | 10 | 0 | 0 | 0 |

| unit | kind | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|
| P5_6-16 | Q | 6645.1 | 132.7 | 799.6 | 9 047 985 898 | 4389 |
| P3_4-10-14 | H | 581.5 | 52.4 | 346.8 | 3 485 182 570 | 4390 |
| P3_5-9-10 | H | 26.1 | 11.8 | 123.4 | 215 857 034 | 2679 |
| P2_7-8-11 | H | 30.9 | 11.7 | 120.7 | 216 135 568 | 2676 |
| P2_5-8-9 | H | 31.4 | 11.8 | 124.8 | 219 973 996 | 2677 |
| P2_4-8-10 | H | 28.4 | 11.6 | 125.5 | 217 308 623 | 2649 |
| P2_3-11-13 | H | 352.1 | 52.0 | 316.3 | 3 298 049 031 | 4411 |
| P2_3-6-10 | H | 87.0 | 21.6 | 167.4 | 1 130 619 694 | 3130 |
| P2_1-6-12 | H | 673.0 | 53.6 | 349.2 | 3 677 150 219 | 4366 |
| P2_1-3-5 | H | 287.7 | 47.6 | 314.5 | 3 276 925 690 | 4414 |

Certified (all 10), min / median / max:
- solve: 26.1 / 187.3 / 6645.1 s (H only: 26.1 / 87.0 / 673.0 s)
- lrat-check: 11.6 / 34.6 / 132.7 s
- cake_lpr: 120.7 / 241.0 / 799.6 s (all with heap 8000 MB, no retry)
- proof size: 0.216 / 2.20 / 9.05 GB

Largest solver RSS: 4414 MB (P2_1-3-5). Peak disk use during P5_6-16 about 20 GB used / 19 GB free.

No SAT, no proof rejection, no ERROR status, no memory problem. P5_6-16 (a 10000 s unit) was certified at 6645 s.

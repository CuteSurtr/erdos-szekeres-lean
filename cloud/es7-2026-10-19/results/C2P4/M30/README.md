# C2P4 M30: shard j = 30 of N = 50 of `lists/C2P4.tsv` (H = 2.5 h, task commit a46b478d)

Start 13:01:37Z (epoch 1793451697), lane END 15:16:37Z (epoch 1793459797). One lane, `run.sh`.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` from the vendored sources: manifest all 196 files match; CaDiCaL 3.0.1 (c6073042),
  cake_lpr (a36874a8), lrat-check (2e3b2dc) with the E2 patch. Nothing cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`);
  cake_lpr example `s VERIFIED UNSAT`.
- Base CNF `p cnf 838032 16653336`, sha256 base.cnf b0061e90…d8ff1 and base.json 2476faff…72b48: as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (14 in `units.tsv`)
| case | kind | units | certified | timed out | not reached | errors |
|---|---|---|---|---|---|---|
| P5 | Q | 1 | 1 (P5_6-11) | 0 | 0 | 0 |
| P5 | H | 4 | 4 (P5_1-14-15, P5_2-12-14, P5_6-11-14, P5_8-9-12) | 0 | 0 | 0 |
| P6 | H | 1 | 1 (P6_8-9-10) | 0 | 0 | 0 |
| P4 | Q | 1 | 1 (P4_2-7) | 0 | 0 | 0 |
| P4 | H | 5 | 1 (P4_1-2-14) | 0 | 4 (P4_1-8-14, P4_2-6-9, P4_5-8-11, P4_6-9-10) | 0 |
| P3 | Q | 2 | 0 | 0 | 2 (P3_1-6, P3_8-12) | 0 |
| **total** | | 14 | **8** | 0 | 6 | 0 |

All 8 records UNSATISFIABLE with `"certified": true` (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, heap
8000 MB). P4_2-7 ran with a time-limited cap of 2469 s and P4_1-2-14 with 366 s; both finished inside them.

| unit | kind | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|
| P5_6-11 | Q | 2034.6 | 89.1 | 480.4 | 5,450,072,152 | 4379 |
| P6_8-9-10 | H | 24.2 | 13.2 | 110.6 | 217,512,637 | 2649 |
| P5_1-14-15 | H | 223.2 | 54.1 | 304.2 | 3,191,691,530 | 4358 |
| P5_2-12-14 | H | 276.6 | 54.1 | 314.9 | 3,243,685,201 | 4393 |
| P5_6-11-14 | H | 263.0 | 55.6 | 318.6 | 3,201,935,282 | 4349 |
| P5_8-9-12 | H | 25.4 | 13.2 | 111.9 | 216,170,785 | 2645 |
| P4_2-7 | Q | 1535.3 | 82.6 | 460.6 | 5,057,686,230 | 4408 |
| P4_1-2-14 | H | 245.5 | 54.9 | 317.2 | 3,226,446,072 | 4367 |

Min / median / max over the certified units: solve 24.2 / 254.3 / 2034.6 s; lrat-check 13.2 / 54.5 / 89.1 s;
cake_lpr 110.6 / 316.0 / 480.4 s; proof 0.216 / 3.21 / 5.45 GB.

Largest solver RSS: 4408 MB (P4_2-7).

No SAT, no proof rejection, no error record, no memory problem (peak well under the 15 GB of the machine).
The lane stopped at 15:10:58Z with 338 s left before END; the 6 units not reached remain open.

# C2P4 M16 (LIST = C2P4.tsv, j = 16, N = 50, H = 2.5, TASK commit a46b478d)

Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 13:02 UTC, lane END 15:17:29 UTC (epoch 1793459849).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest all 196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8),
  lrat-check (2e3b2dc + E2 patch), built from the vendored sources only, nothing downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`);
  cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf b0061e90...d8ff1 and base.json 2476faff...2b48, both as required.
- Cubes P1..P8 from `C2C34/l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (14 rows, idx ≡ 16 mod 50)
| status | total | P5 Q | P4 Q | P4 H | P3 Q | P3 H |
|---|---|---|---|---|---|---|
| certified UNSAT | 7 | 2 | 1 | 4 | 0 | 0 |
| timed out (UNKNOWN) | 0 | | | | | |
| not reached | 7 | 0 | 0 | 1 | 1 | 5 |
| errors / uncertified | 0 | | | | | |

Certified: P5_1-3, P5_9-12, P4_6-9 (Q); P4_1-5-14, P4_1-11-13, P4_2-8-12, P4_5-10-15 (H).
Not reached (time budget): P4_7-8-9 (H), P3_4-11 (Q), P3_1-4-12, P3_1-9-11, P3_4-6-13, P3_5-6-7, P3_6-7-11 (H).

Certified units (min / median / max):
- solve: 276.7 / 522.2 / 960.7 s
- lrat-check: 61.4 / 62.3 / 79.8 s
- cake_lpr: 327.6 / 362.0 / 392.7 s (heap 8000 MB)
- proof size: 3.23 / 3.65 / 4.11 GB (deleted after checking)

| unit | kind | solve s | lrat-check s | cake_lpr s | proof bytes |
|---|---|---|---|---|---|
| P5_1-3 | Q | 960.66 | 79.8 | 392.7 | 4106272733 |
| P5_9-12 | Q | 697.00 | 61.7 | 359.9 | 3739523458 |
| P4_6-9 | Q | 844.43 | 63.4 | 367.4 | 3715829055 |
| P4_1-5-14 | H | 520.37 | 61.4 | 362.0 | 3648080554 |
| P4_1-11-13 | H | 276.74 | 61.6 | 327.6 | 3232754910 |
| P4_2-8-12 | H | 467.94 | 67.6 | 363.6 | 3520581122 |
| P4_5-10-15 | H | 522.22 | 62.3 | 361.4 | 3533834520 |

Largest solver RSS: 4411 MB (P4_6-9).

No SAT, no proof rejection, no memory problem. Every certified record has both `c VERIFIED` and `s VERIFIED UNSAT`.

# C2P5 M15: C2P5A.tsv, shard j = 15 of N = 37, H = 4.5 h (TASK commit 81cb025f)

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. Nothing cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf `b0061e90…8ff1` and of base.json `2476faff…2b48`, both as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, idx ≡ 15 mod 37): 4 units, 4 certified
Lane started 19:13Z, END 23:26:05Z, lane done at 20:12:44Z.

| case | kind | units | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|---|---|
| P4 | Q | 1 | 1 | 0 | 0 | 0 |
| P4 | H | 3 | 3 | 0 | 0 | 0 |
| total | | 4 | 4 | 0 | 0 | 0 |

| unit | kind | cap s | solve s | RSS MB | proof bytes | lrat-check s | cake_lpr s |
|---|---|---|---|---|---|---|---|
| P4_8-13 | Q | 8000 | 2311.0 | 4471 | 5,304,052,568 | 77.4 | 488.6 |
| P4_5-8-11 | H | 2400 | 26.97 | 2646 | 217,325,036 | 13.5 | 112.0 |
| P4_6-8-13 | H | 2400 | 125.74 | 3403 | 1,663,065,156 | 29.0 | 197.5 |
| P4_8-9-10 | H | 2400 | 25.83 | 2647 | 215,866,340 | 11.5 | 110.0 |

Certified (min / median / max):
- all 4: solve 25.83 / 76.36 / 2311.0 s; lrat-check 11.5 / 21.25 / 77.4 s; cake_lpr 110.0 / 154.75 / 488.6 s; proof 0.216 / 0.940 / 5.30 GB.
- Q (1): solve 2311.0 s, lrat-check 77.4 s, cake_lpr 488.6 s, proof 5.30 GB.
- H (3): solve 25.83 / 26.97 / 125.74 s; lrat-check 11.5 / 13.5 / 29.0 s; cake_lpr 110.0 / 112.0 / 197.5 s; proof 0.216 / 0.217 / 1.66 GB.

Every record has `"certified": true` (lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT`).

## Largest solver RSS
4471 MB (P4_8-13).

## SAT, proof rejections, memory
No SAT. No proof rejection, no ERROR record. No memory or disk problem (at least 23 GB disk free throughout).

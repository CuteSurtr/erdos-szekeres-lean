# C2P5 M53: list C2P5B.tsv, shard j = 3 of N = 50, H = 5.25 (TASK commit 81cb025f)

**Result: all 14 units certified UNSAT (both lrat-check and cake_lpr accepted every proof). No SAT, no timeout, no error, no proof rejection, no memory problem.**

Start 2026-10-31 15:24:11Z (epoch 1793460251), END 1793478251 (20:24:11Z). The lane finished all units at 18:34:03Z.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` from the vendored sources (manifest: all 196 files match; nothing downloaded): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity: the cake_lpr example prints `s VERIFIED UNSAT`; both checkers reject the bad LRAT and accept the good one.
- Base CNF: header `p cnf 838032 16653336`, sha256 b0061e90…d8ff1 (base.cnf) and 2476faff…bb48 (base.json), both as required.
- Cubes P1..P8 from `C2C34/l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, idx ≡ 3 mod 50: 14 units)
| status | count |
|---|---|
| certified (UNSAT, both checkers) | 14 |
| timed out (UNKNOWN) | 0 |
| not reached | 0 |
| errors / certified false | 0 |

Certified by kind and case:

| kind | by case | total |
|---|---|---|
| Q | P2 2, P1 1, P3 1 | 4 |
| H | P1 5, P3 5 | 10 |

No cover units were in this shard.

Certified units (min / median / max):

| quantity | min | median | max |
|---|---|---|---|
| solve s | 23.9 | 318.4 | 1851.0 |
| lrat-check s | 13.9 | 56.6 | 85.3 |
| cake_lpr s | 116.1 | 326.5 | 499.3 |
| proof GB | 0.22 | 3.28 | 5.23 |

Per unit:

| unit | case | kind | cap s | solve s | lrat-check s | cake_lpr s | proof GB | solver RSS MB |
|---|---|---|---|---|---|---|---|---|
| P2_1-6 | P2 | Q | 8000 | 1851.05 | 85.3 | 499.3 | 5.23 | 4426 |
| P2_8-10 | P2 | Q | 8000 | 459.04 | 57.2 | 333.5 | 3.29 | 4410 |
| P1_6-10 | P1 | Q | 8000 | 676.38 | 60.8 | 350.5 | 3.64 | 4417 |
| P1_2-3-4 | P1 | H | 2400 | 29.24 | 13.9 | 118.6 | 0.22 | 2672 |
| P1_2-7-12 | P1 | H | 2400 | 414.43 | 63.2 | 343.8 | 3.47 | 4402 |
| P1_3-5-10 | P1 | H | 2400 | 83.76 | 26.1 | 173.4 | 1.11 | 3165 |
| P1_4-5-10 | P1 | H | 2400 | 23.94 | 15.0 | 120.1 | 0.22 | 2665 |
| P1_5-8-9 | P1 | H | 2400 | 27.02 | 14.8 | 118.4 | 0.23 | 2649 |
| P3_4-10 | P3 | Q | 8000 | 1615.04 | 80.8 | 431.9 | 4.89 | 4415 |
| P3_1-4-11 | P3 | H | 2400 | 444.96 | 61.8 | 347.1 | 3.57 | 4380 |
| P3_1-9-10 | P3 | H | 2400 | 303.98 | 56.3 | 319.5 | 3.26 | 4350 |
| P3_4-6-12 | P3 | H | 2400 | 219.32 | 54.3 | 315.5 | 3.18 | 4414 |
| P3_4-14-15 | P3 | H | 2400 | 332.85 | 56.9 | 335.8 | 3.39 | 4374 |
| P3_6-7-10 | P3 | H | 2400 | 24.38 | 13.9 | 116.1 | 0.22 | 2646 |

Largest solver RSS: 4426 MB (P2_1-6). cake_lpr ran with an 8000 MB heap throughout. Proofs were deleted after checking; their sizes and sha256 are in `out.jsonl`.

## SAT / rejections / memory
None.

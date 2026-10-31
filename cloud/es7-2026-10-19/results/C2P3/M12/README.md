# C2P3 M12 (LIST = C2P3.tsv, j = 12, N = 50, H = 2.5, Z = 4f653319)

Start 2026-10-31 09:42:49 UTC (epoch 1793439769), END = 1793447869 (11:57:49 UTC). Machine: 4 cores, 15 GB RAM (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest all 196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch, built from the vendored sources only.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…bb472b48`, both match.
- Cubes P1..P8: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (10 rows with idx ≡ 12 mod 50)
| case/kind | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|
| P6 Q | 1 (P6_1-8) | 0 | 0 | 0 |
| P6 H | 2 (P6_1-7-14, P6_3-7-11) | 0 | 1 (P6_8-9-10) | 0 |
| P5 H | 0 | 0 | 4 (P5_1-3-14, P5_1-10-12, P5_2-7-13, P5_6-7-8) | 0 |
| P5 Q | 0 | 0 | 2 (P5_7-8, P5_8-13) | 0 |
| total | 3 | 0 | 7 | 0 |

The lane stopped at 11:46:51 with 657 s left before END (under the 15-minute threshold).

Certified units (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT` for all three):

| unit | cap | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|
| P6_1-8 (Q) | 6000 | 4648.1 | 138.9 | 738.5 | 9 211 081 055 | 4366.9 |
| P6_1-7-14 (H) | 1782 | 505.5 | 55.2 | 326.6 | 3 681 972 035 | 4358.5 |
| P6_3-7-11 (H) | 880 | 436.0 | 57.0 | 318.7 | 3 487 321 398 | 4369.3 |

Min / median / max: solve 436.0 / 505.5 / 4648.1 s; lrat-check 55.2 / 57.0 / 138.9 s; cake_lpr 318.7 / 326.6 / 738.5 s; proof 3.49 / 3.68 / 9.21 GB.

(Caps of the H units were reduced by lane.py to fit END.)

## Other
- Largest solver RSS: 4369.3 MB (cake_lpr peaked at about 8.2 GB RSS with heap 8000 MB).
- No SAT, no proof rejection, no ERROR status, no memory or disk problem (the proofs were deleted after the checks).

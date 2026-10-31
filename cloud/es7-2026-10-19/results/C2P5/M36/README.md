# C2P5 M36 (list C2P5A.tsv, shard j = 36 of N = 37, H = 4.5, TASK commit 81cb025f)

## Tools and checks
- Built by `C2P/vendor/build_tools.sh` from the vendored `vendor/tools-src.tar.xz` (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch. No code cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1`, base.json `2476faff…2b48` — both match.
- Cubes: P1..P8 from `C2C34/l2cubes.py` byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details in `tools.txt`; binary hashes there.

## Units (10: idx ≡ 36 mod 37)
| case | kind | units | certified | timed out | not reached | errors |
|---|---|---|---|---|---|---|
| P4 | H | 9 | 9 | 0 | 0 | 0 |
| P3 | H | 1 | 1 | 0 | 0 | 0 |
| **all** | | **10** | **10** | 0 | 0 | 0 |

Certified (all UNSAT, lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`):
P4_1-2-16, P4_1-5-11, P4_1-7-14, P4_1-9-10, P4_1-11-12, P4_1-15-16, P4_2-7-12, P4_5-9-13, P4_6-10-11, P3_1-8-12.

| quantity | min | median | max |
|---|---|---|---|
| solve s | 25.4 | 322.1 | 584.9 |
| lrat-check s | 13.3 | 57.5 | 63.5 |
| cake_lpr s | 119.2 | 334.6 | 367.3 |
| proof size | 0.22 GB | 3.26 GB | 3.66 GB |

Largest solver RSS: 4412.5 MB (P4_1-5-11).

The lane started 19:28Z and finished all units at 21:32Z, well before END.

## Problems
No SAT, no proof rejection, no ERROR records, no memory problem.

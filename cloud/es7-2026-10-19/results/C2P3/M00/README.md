# C2P3 M00 (LIST = C2P3.tsv, j = 0, N = 50, H = 2.5, Z = 4f653319)

Start 2026-10-31 09:42:40Z (epoch 1793439760), END 11:57:40Z (1793447860). Machine: 4 cores, 15 GB RAM (`env.txt`).

## Tools and checks (`tools.txt`)
- Built by `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz` (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch. Nothing cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…2b48`, both as required.
- Cubes P1..P8 from `C2C34/l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (10 assigned: idx ≡ 0 mod 50)
| idx | unit | case | kind | cap (s) | result | solve s | lrat-check s | cake_lpr s | proof |
|---|---|---|---|---|---|---|---|---|---|
| 0 | P7_1-11 | P7 | Q | 6000 | certified UNSAT | 4438.6 | 130.9 | 731.1 | 8.39 GB |
| 50 | P7_2-8-16 | P7 | H | 1800 | certified UNSAT | 444.5 | 59.0 | 338.3 | 3.55 GB |
| 100 | P6_2-11-14 | P6 | H | 1800 (1146 effective) | certified UNSAT | 331.3 | 56.8 | 326.4 | 3.32 GB |
| 150 | P6_7-10-16 | P6 | H | 1800 (420 effective) | certified UNSAT | 335.1 | 54.7 | 318.9 | 3.29 GB |
| 200–450 | P5_1-2-14, P5_1-8-15, P5_2-6-11, P5_2-12-16, P5_6-11-16, P5_8-9-14 | P5 | H | 1800 | not reached | | | | |

Counts by case and kind:
- Certified: 4 — P7 Q 1, P7 H 1, P6 H 2.
- Timed out (UNKNOWN): 0. Errors: 0. Certified false: 0.
- Not reached: 6 — P5 H 6 (lane stopped at 11:52:40Z with 299 s left before END).

Certified units (4), min / median / max:
- solve s: 331.3 / 389.8 / 4438.6
- lrat-check s: 54.7 / 57.9 / 130.9
- cake_lpr s: 318.9 / 332.4 / 731.1 (all at heap 8000 MB)
- proof bytes: 3.29 GB / 3.43 GB / 8.39 GB

Largest solver RSS: 4386 MB (P6_7-10-16). cake_lpr RSS about 8.2 GB.

No SAT, no proof rejection, no memory problem. Disk went down to 20 GB free during the 8.4 GB proof, with no issue.

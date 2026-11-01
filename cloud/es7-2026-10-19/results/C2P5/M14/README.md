# C2P5 M14 — list C2P5A.tsv, shard j = 14 of N = 37, H = 4.5 (task commit 81cb025f)

Started 18:39:44Z (epoch 1793471984); END = 1793487284 (22:54:44Z). The lane finished all units at 20:06:07Z.

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored `vendor/tools-src.tar.xz` (manifest: all 196 files match); nothing cloned or downloaded.
  CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…2b48`, both as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, list at 92a2b58ad, rows with idx ≡ 14 mod 37)

| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P4_6-14 | P4 | Q | 8000 | UNSAT, certified | 3505.49 | 113.9 | 612.8 | 7,404,477,102 | 4379.7 |
| P4_5-8-10 | P4 | H | 2400 | UNSAT, certified | 27.40 | 13.3 | 111.9 | 217,913,470 | 2661.8 |
| P4_6-8-12 | P4 | H | 2400 | UNSAT, certified | 21.67 | 13.3 | 112.6 | 218,950,640 | 2659.6 |
| P4_7-12-13 | P4 | H | 2400 | UNSAT, certified | 153.68 | 43.0 | 261.5 | 2,437,439,836 | 3676.9 |

Counts by case and kind:
- P4 Q: 1 certified, 0 timed out, 0 not reached, 0 errors.
- P4 H: 3 certified, 0 timed out, 0 not reached, 0 errors.
- Total: 4 of 4 certified (both lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`).

Certified units (min / median / max):
- solve: 21.67 / 90.54 / 3505.49 s
- lrat-check: 13.3 / 28.15 / 113.9 s
- cake_lpr: 111.9 / 187.05 / 612.8 s
- proof size: 0.218 / 1.33 / 7.40 GB

Largest solver RSS: 4379.7 MB (P4_6-14). Disk was at most 48% used (about 21 GB free at the peak proof size).

No SAT, no proof rejection, no ERROR status, and no memory problem.

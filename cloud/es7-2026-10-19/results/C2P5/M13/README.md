# C2P5 M13 (LIST = C2P5A.tsv, j = 13, N = 37, H = 4.5, TASK commit 81cb025f)

## Tools and checks
- Built by `C2P/vendor/build_tools.sh` from the vendored `vendor/tools-src.tar.xz` (manifest: all 196 files match; nothing cloned or downloaded):
  CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check (drat-trim 2e3b2dc + E2 patch).
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…b48`, both as required.
- Cubes P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details are in `tools.txt`.

## Units (4, all in case P4): 4 certified, 0 timed out, 0 not reached, 0 errors

| case | kind | units | certified | UNKNOWN | not reached | error |
|---|---|---|---|---|---|---|
| P4 | Q (cap 8000) | 1 | 1 | 0 | 0 | 0 |
| P4 | H (cap 2400) | 3 | 3 | 0 | 0 | 0 |

| unit | kind | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|---|
| P4_6-13 | Q | 2791.95 | 106.3 | 595.0 | 6,468,237,885 | 4386 |
| P4_5-8-9 | H | 76.5 | 26.6 | 173.8 | 1,131,272,449 | 3128 |
| P4_6-8-11 | H | 30.14 | 15.2 | 118.2 | 216,952,561 | 2649 |
| P4_7-11-13 | H | 110.28 | 30.0 | 198.4 | 1,408,363,837 | 3421 |

Over all certified units (min / median / max):
- solve s: 30.14 / 93.39 / 2791.95
- lrat-check s: 15.2 / 28.3 / 106.3
- cake_lpr s: 118.2 / 186.1 / 595.0
- proof bytes: 216,952,561 / 1,269,818,143 / 6,468,237,885

For the H units alone (min / median / max), solve is 30.14 / 76.5 / 110.28 s and proof size is 0.22 / 1.13 / 1.41 GB.

The largest solver RSS was 4386 MB (P4_6-13).

There were no SAT answers, no proof rejections (every proof got `c VERIFIED` and `s VERIFIED UNSAT`) and no memory problems. The lane finished all of its units at 19:53:34Z, well before END (1793487287 = 22:54:47Z).

# checks-20261107: P1 open items 6 and 15 (7 November 2026)

Exact computation, on the Mac (Apple M5 Pro, Python 3.14.10, Apple clang with the MacOSX26 SDK). `run.sh` reruns
everything in about 13 s; the logs in `logs/` are its output.

**Item 6 (programs per sevenfold count).** Before this run, the `ES8SYM` pipeline had checked only the five
sevenfold files that are also in `ES8SYM/sets`. It has now checked the other three files of `PRIMEFOLD/sets/k8`
(`c7_64_own_s1000`, `m7_x2_G9s_centre`, `p7_two_orbit_64`), with the commands of `ES8SYM/tools/run_all.sh` §1 and §5.
- `verify_cfg.py`: 7-fold orbit structure, distinctness, invariance, 0 zero orientations, interval cross-check
  without mismatch (`EXACT-PREP PASS`).
- `cvx2.c` (two dynamic programs), `cvxcheck.c` (depth-first search) and `crosscheck_decimal.py`: all pass.
- The convex k-subset counts for k = 3..8 agree, for all three files, with `PRIMEFOLD/check64/check64.log`, and the
  largest convex subset has 7 points.

| file | SHA-256 | convex 4-subsets | convex 7-subsets | convex 8-subsets |
|---|---|---|---|---|
| `c7_64_own_s1000` | `c9942cc1…` | 392,966 | 3,328,145 | 0 |
| `m7_x2_G9s_centre` | `ac524df7…` | 462,581 | 14,719,287 | 0 |
| `p7_two_orbit_64` | `9a55f245…` | 470,764 | 18,396,499 | 0 |

So every one of the eight sevenfold files has now been checked by both `PRIMEFOLD/check64` (an anchored dynamic
program and a separate C enumerator) and the `ES8SYM` pipeline.

**Item 15 (line-modules of `c7_64_own_s1000`).** Two separately written enumerators agree:
`PRIMEFOLD/check64/modules60` (`otable.py` with a 120-digit decimal cross-check, then `run_modules.py`) and
`ES8SYM/structure/modules.c`. Both find 22 non-trivial line-modules:
- one of size 57, the points inside the convex hull (the complement of the 7 hull vertices);
- seven each of sizes 60, 61 and 62, the complements of 4, 3 and 2 consecutive hull vertices.

None has 2 to 56 points, which is the same pattern as `c7_64pts_9layers_centre_own` (`ES8SYM` §6). Before this run,
only sizes 2 to 20 had been checked for this file (`check64.log`).

The module counts of the two other files also agree with `check64.log`, which covers sizes up to 20:
- `m7_x2_G9s_centre`: 84 = 77 (sizes 2 to 20) + 7 of size 62.
- `p7_two_orbit_64`: 98 = 91 + 7 of size 62.

**Changes to P1.** `p1.tex` §7 and Table 7 now state these results, and `p1.pdf` was rebuilt. The changes are listed
in `../README.md`, section "Checks of 7 November 2026 (open items 6 and 15)". This new text has had no internal
review.

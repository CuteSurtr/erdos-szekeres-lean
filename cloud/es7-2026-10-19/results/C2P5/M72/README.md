# C2P5 M72 — LIST C2P5B.tsv, shard j=22 of N=50, H=5.25, TASK commit 81cb025f

## Tools and checks
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match). CaDiCaL 3.0.1, cake_lpr, lrat-check (E2 patch).
- Sanity: both checkers rejected the bad LRAT and accepted the good one; the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF header `p cnf 838032 16653336`. The sha256 of base.cnf and base.json both match the expected values.
- Cubes P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details are in `tools.txt`.

## Units
19 units (idx ≡ 22 mod 50): 19 certified UNSAT (both lrat-check and cake_lpr accepted), 0 timed out (UNKNOWN), 0 not reached, 0 errors.
The lane finished all units at 18:37Z, well before END.

| case | kind | certified | other |
|---|---|---|---|
| P2 | Q | 1 | 0 |
| P2 | H | 6 | 0 |
| P1 | Q | 1 | 0 |
| P1 | H | 5 | 0 |
| P3 | Q | 1 | 0 |
| P3 | H | 5 | 0 |

Certified-unit statistics (min / median / max):

- solve s: 19.6 / 271.3 / 653.6
- lrat-check s: 12.7 / 51.0 / 57.8
- cake_lpr s: 104.1 / 295.3 / 352.7
- proof GB: 0.2 / 3.3 / 3.7
- largest solver RSS: 4435 MB (P3_1-6-9)

| unit | case | kind | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|
| P2_4-7 | P2 | Q | UNSATISFIABLE certified | 653.59 | 54.3 | 308.1 | 3.51 | 4407 |
| P1_3-6 | P1 | Q | UNSATISFIABLE certified | 416.38 | 51.0 | 295.3 | 3.44 | 4413 |
| P2_1-3-14 | P2 | H | UNSATISFIABLE certified | 328.33 | 55.2 | 322.8 | 3.57 | 4381 |
| P2_1-9-10 | P2 | H | UNSATISFIABLE certified | 271.32 | 47.9 | 285.3 | 3.25 | 4371 |
| P2_3-7-12 | P2 | H | UNSATISFIABLE certified | 300.94 | 55.9 | 303.2 | 3.34 | 4368 |
| P2_4-5-9 | P2 | H | UNSATISFIABLE certified | 27.2 | 14.2 | 117.5 | 0.22 | 2652 |
| P2_4-10-12 | P2 | H | UNSATISFIABLE certified | 219.59 | 49.9 | 285.5 | 3.21 | 4362 |
| P2_5-11-12 | P2 | H | UNSATISFIABLE certified | 79.27 | 25.0 | 160.1 | 1.28 | 3250 |
| P1_2-4-11 | P1 | H | UNSATISFIABLE certified | 248.37 | 51.6 | 302.6 | 3.26 | 4358 |
| P1_2-9-16 | P1 | H | UNSATISFIABLE certified | 497.15 | 57.8 | 352.7 | 3.75 | 4430 |
| P1_3-7-12 | P1 | H | UNSATISFIABLE certified | 249.58 | 49.6 | 291.7 | 3.26 | 4375 |
| P1_4-7-14 | P1 | H | UNSATISFIABLE certified | 273.33 | 49.1 | 288.2 | 3.35 | 4371 |
| P1_6-8-11 | P1 | H | UNSATISFIABLE certified | 19.55 | 12.7 | 104.1 | 0.22 | 2648 |
| P3_6-9 | P3 | Q | UNSATISFIABLE certified | 514.4 | 57.8 | 331.3 | 3.49 | 4409 |
| P3_1-6-9 | P3 | H | UNSATISFIABLE certified | 322.91 | 53.2 | 296.9 | 3.34 | 4435 |
| P3_1-12-14 | P3 | H | UNSATISFIABLE certified | 249.75 | 52.8 | 298.9 | 3.25 | 4371 |
| P3_4-8-14 | P3 | H | UNSATISFIABLE certified | 397.19 | 57.1 | 314.8 | 3.45 | 4371 |
| P3_5-8-10 | P3 | H | UNSATISFIABLE certified | 24.21 | 12.8 | 105.5 | 0.22 | 2678 |
| P3_6-10-14 | P3 | H | UNSATISFIABLE certified | 225.51 | 49.7 | 282.1 | 3.22 | 4390 |

## Problems
- No SAT result, no proof rejections, no `certified: false` records and no ERROR records.
- No memory problems: the largest solver RSS was about 4.4 GB out of 15 GB.

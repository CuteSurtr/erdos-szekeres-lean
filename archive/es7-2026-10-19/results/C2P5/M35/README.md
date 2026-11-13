# C2P5 M35 (LIST C2P5A.tsv, j = 35, N = 37, H = 4.5, TASK commit 81cb025f)

## Tools and checks

- Built with `C2P/vendor/build_tools.sh` from the vendored sources (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json match the expected values.
- Cubes P1..P8 from `C2C34/l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`. Details in `tools.txt`.

## Units

10 units (idx ≡ 35 mod 37): **10 certified**, 0 timed out (UNKNOWN), 0 not reached, 0 errors / uncertified.

| case | kind | certified |
|---|---|---|
| P3 | H | 1 |
| P4 | H | 9 |

| unit | case | kind | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB | certified |
|---|---|---|---|---|---|---|---|---|---|
| P4_1-2-15 | P4 | H | UNSATISFIABLE | 241.45 | 52.8 | 301.1 | 3.20 | 4405 | True |
| P4_1-5-10 | P4 | H | UNSATISFIABLE | 446.72 | 59.6 | 335.1 | 3.59 | 4370 | True |
| P4_1-7-13 | P4 | H | UNSATISFIABLE | 578.65 | 62.3 | 349.3 | 3.74 | 4376 | True |
| P4_1-8-16 | P4 | H | UNSATISFIABLE | 400.26 | 57.3 | 331.6 | 3.55 | 4420 | True |
| P4_1-10-15 | P4 | H | UNSATISFIABLE | 379.32 | 57.9 | 326.9 | 3.45 | 4404 | True |
| P4_1-14-16 | P4 | H | UNSATISFIABLE | 227.11 | 51.5 | 303.3 | 3.24 | 4371 | True |
| P4_2-7-11 | P4 | H | UNSATISFIABLE | 405.57 | 56.6 | 319.9 | 3.51 | 4373 | True |
| P4_5-9-12 | P4 | H | UNSATISFIABLE | 94.47 | 25.4 | 170.0 | 1.22 | 3222 | True |
| P4_6-9-15 | P4 | H | UNSATISFIABLE | 266.15 | 54.1 | 313.6 | 3.22 | 4354 | True |
| P3_1-4-6 | P3 | H | UNSATISFIABLE | 236.6 | 52.2 | 299.6 | 3.26 | 4401 | True |

Certified units, min / median / max:

- solve s: 94.5 / 322.7 / 578.6
- lrat-check s: 25.4 / 55.4 / 62.3
- cake_lpr s: 170.0 / 316.8 / 349.3
- proof size GB: 1.2 / 3.4 / 3.7

Largest solver RSS: 4420 MB.

## Problems

No SAT, no proof rejection, no errors and no memory problem. All 10 units were finished at 21:24Z, well before END (23:40:53Z); every proof was deleted after both checks.

# C2P5 M31 (LIST = C2P5A.tsv, j = 31, N = 37, H = 4.5, TASK commit 81cb025f)

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing cloned or downloaded.
- Sanity checks: cake_lpr example `s VERIFIED UNSAT`; bad LRAT rejected by both checkers, good LRAT accepted by both.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf (b0061e90…) and base.json (2476faff…) match.
- Cubes: `l2cubes.py` output for P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, rows of C2P5A.tsv with idx ≡ 31 mod 37)
10 units, all case P4, kind H (hexagonal), cap 2400 s.

| | certified | timed out (UNKNOWN) | not reached | errors / not certified |
|---|---|---|---|---|
| P4, H | 10 | 0 | 0 | 0 |

The lane started 19:28:20Z and finished all units at 21:02:57Z, well before END (1793490064).

| unit | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB | certified |
|---|---|---|---|---|---|---|---|
| P4_1-2-7 | UNSATISFIABLE | 253.88 | 49.5 | 293.1 | 3.22 | 4412 | True |
| P4_1-5-6 | UNSATISFIABLE | 252.63 | 49.6 | 282.5 | 3.24 | 4404 | True |
| P4_1-6-7 | UNSATISFIABLE | 228.93 | 47.1 | 274.3 | 3.23 | 4362 | True |
| P4_1-8-10 | UNSATISFIABLE | 311.9 | 52.6 | 300.2 | 3.29 | 4395 | True |
| P4_1-10-11 | UNSATISFIABLE | 273.03 | 50.1 | 291.3 | 3.26 | 4395 | True |
| P4_1-12-13 | UNSATISFIABLE | 251.77 | 47.5 | 283.3 | 3.22 | 4394 | True |
| P4_2-6-14 | UNSATISFIABLE | 434.06 | 53.9 | 323.3 | 3.67 | 4370 | True |
| P4_5-8-15 | UNSATISFIABLE | 357.42 | 57.3 | 310.9 | 3.42 | 4372 | True |
| P4_6-9-11 | UNSATISFIABLE | 88.33 | 26.3 | 184.1 | 1.35 | 3406 | True |
| P4_8-10-13 | UNSATISFIABLE | 26.6 | 12.8 | 113.6 | 0.22 | 2659 | True |

Certified: 10 of 10 records.

- solve s (min / median / max): 26.6 / 253.3 / 434.1
- lrat-check s: 12.8 / 49.5 / 57.3
- cake_lpr s: 113.6 / 287.3 / 323.3
- proof size GB: 0.2 / 3.2 / 3.7
- largest solver RSS: 4412 MB

## Problems
No SAT, no proof rejection (both lrat-check and cake_lpr accepted every proof), no ERROR status, no memory problem (largest solver RSS 4.4 GB of 15 GB).

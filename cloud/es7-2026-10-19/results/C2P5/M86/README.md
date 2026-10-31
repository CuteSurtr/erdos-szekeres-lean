# C2P5 M86

Task `results/C2P5/TASK.md` at 81cb025f with V = M86, LIST = C2P5B.tsv, j = 36, N = 50, H = 5.25.
Start 2026-10-31 15:10:21Z (epoch 1793459421), END 1793477421 (20:10:21Z). The lane finished all units at 18:27:58Z.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`, vendored sources only (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). No code was cloned or downloaded.
- Sanity checks: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…f2b48`, both as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (14 rows of C2P5B.tsv with idx ≡ 36 mod 50)
- **Certified (UNSAT, lrat-check and cake_lpr both accepted): 14 of 14.**
  - P1: Q 1, H 4
  - P2: Q 1, H 6
  - P3: Q 2
- Timed out (UNKNOWN): 0. Not reached: 0. Errors or `certified: false`: 0.
- P3_8-11 ran with its cap cut to 6468 s by the END rule, and it finished in 519 s.

Certified units, min / median / max:
- solve: 21.45 / 300.48 / 1535.38 s
- lrat-check: 13.3 / 56.2 / 81.2 s
- cake_lpr: 114.9 / 322.7 / 461.9 s
- proof size: 0.22 / 3.33 / 5.09 GB (216798034 / 3330258358.5 / 5086936476 bytes)

Largest solver RSS: 4418 MB (P1_2-5-14).

No SAT, no proof rejection and no memory problem.

| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof GB | solver RSS MB | certified |
|---|---|---|---|---|---|---|---|---|---|---|
| P2_5-11 | P2 | Q | 8000 | UNSATISFIABLE | 1412.95 | 78.6 | 420.2 | 4.72 | 4391 | True |
| P1_4-9 | P1 | Q | 8000 | UNSATISFIABLE | 847.13 | 68.2 | 364.9 | 4.00 | 4416 | True |
| P2_1-5-6 | P2 | H | 2400 | UNSATISFIABLE | 235.2 | 52.7 | 302.7 | 3.22 | 4361 | True |
| P2_3-5-7 | P2 | H | 2400 | UNSATISFIABLE | 26.34 | 13.3 | 114.9 | 0.22 | 2651 | True |
| P2_3-9-11 | P2 | H | 2400 | UNSATISFIABLE | 218.75 | 54.0 | 298.4 | 3.18 | 4358 | True |
| P2_4-6-14 | P2 | H | 2400 | UNSATISFIABLE | 301.14 | 54.8 | 323.0 | 3.34 | 4379 | True |
| P2_5-6-12 | P2 | H | 2400 | UNSATISFIABLE | 82.49 | 26.8 | 178.0 | 1.22 | 3125 | True |
| P2_6-9-10 | P2 | H | 2400 | UNSATISFIABLE | 21.45 | 14.4 | 117.6 | 0.22 | 2661 | True |
| P1_2-5-14 | P1 | H | 2400 | UNSATISFIABLE | 387.47 | 59.5 | 339.3 | 3.50 | 4418 | True |
| P1_2-13-15 | P1 | H | 2400 | UNSATISFIABLE | 299.82 | 57.6 | 322.4 | 3.32 | 4411 | True |
| P1_3-9-13 | P1 | H | 2400 | UNSATISFIABLE | 340.41 | 60.7 | 339.0 | 3.37 | 4370 | True |
| P1_4-10-13 | P1 | H | 2400 | UNSATISFIABLE | 276.46 | 54.7 | 319.9 | 3.23 | 4374 | True |
| P3_1-5 | P3 | Q | 8000 | UNSATISFIABLE | 1535.38 | 81.2 | 461.9 | 5.09 | 4387 | True |
| P3_8-11 | P3 | Q | 6468 | UNSATISFIABLE | 518.75 | 57.7 | 335.7 | 3.46 | 4361 | True |

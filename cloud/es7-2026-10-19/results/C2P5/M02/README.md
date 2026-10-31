# C2P5 M02

Values used: V = M02, LIST = C2P5A.tsv, j = 2, N = 37, H = 4.5, Z = 81cb025f. Start 1793470351 (2026-10-31 18:12:31Z), END 1793485651. The lane finished at 19:38:18Z, well before END.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built from the vendored sources: CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, and lrat-check 2e3b2dc with the E2 patch. All 196 manifest files match.
- Sanity checks: both checkers reject the bad LRAT and accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF header is `p cnf 838032 16653336`. The sha256 of base.cnf and base.json match the expected values.
- The cubes P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (idx ≡ 2 mod 37 in C2P5A.tsv: 4 units, all P4)

| unit | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|---|---|---|
| P4_1-8 | Q | 8000 | UNSAT, certified | 2687.38 | 102.1 | 564.5 | 6399811605 | 4385 |
| P4_5-6-13 | H | 2400 | UNSAT, certified | 229.98 | 56.6 | 311.5 | 3170633243 | 4356 |
| P4_5-12-15 | H | 2400 | UNSAT, certified | 405.75 | 60.7 | 354.7 | 3422219931 | 4354 |
| P4_7-8-13 | H | 2400 | UNSAT, certified | 24.56 | 14.7 | 129.5 | 215046294 | 2647 |

- Counts: P4 Q 1/1 certified, and P4 H 3/3 certified.
- Timed out (UNKNOWN): 0. Not reached: 0. Errors: 0. Uncertified: 0.
- Certified units, minimum / median / maximum:
  - solve: 24.56 / 317.87 / 2687.38 s
  - lrat-check: 14.7 / 58.65 / 102.1 s
  - cake_lpr: 129.5 / 333.1 / 564.5 s
  - proof size: 0.215 / 3.296 / 6.400 GB
- Largest solver RSS: 4385 MB.

No SAT, no proof rejection, and no memory problem.

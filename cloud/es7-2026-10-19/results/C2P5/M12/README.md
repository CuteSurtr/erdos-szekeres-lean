# C2P5 M12

Task: `results/C2P5/TASK.md` at commit 81cb025f, with V = M12, LIST = C2P5A.tsv, j = 12, N = 37, H = 4.5.
Lane started 2026-10-31 18:42:12Z (start time 18:39:44Z, END 22:54:44Z); it finished all units at 19:49:23Z.

## Tools and checks
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf and base.json match the expected values.
- Cubes P1..P8: byte-identical to `C2P/cubes/P<a>_cubes.txt`.
- Details in `tools.txt`.

## Units (4: idx 12, 49, 86, 123 of C2P5A.tsv)
- Certified: 4 of 4. P4 Q: 1 of 1, P4 H: 3 of 3.
- Timed out (UNKNOWN): 0. Not reached: 0. Errors: 0.

| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof | solve RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P4_6-12 | P4 | Q | 8000 | UNSATISFIABLE | 2198.5 | 89.9 | 497.4 | 5.61 GB | 4377 |
| P4_5-7-16 | P4 | H | 2400 | UNSATISFIABLE | 346.85 | 54.5 | 314.0 | 3.41 GB | 4376 |
| P4_6-8-10 | P4 | H | 2400 | UNSATISFIABLE | 26.32 | 13.0 | 111.8 | 0.23 GB | 2644 |
| P4_7-11-12 | P4 | H | 2400 | UNSATISFIABLE | 103.76 | 29.3 | 191.5 | 1.52 GB | 3401 |

Certified units (min / median / max):
- solve s: 26.32 / 225.305 / 2198.5
- lrat-check s: 13.0 / 41.9 / 89.9
- cake_lpr s: 111.8 / 252.75 / 497.4
- proof bytes: 226702721 / 2465706313.0 / 5612805087

Largest solver RSS: 4377 MB (P4_6-12).

## Problems
No SAT, no proof rejection (every proof accepted by both lrat-check and cake_lpr) and no memory or disk problem.

# C2P5 M11 (LIST = C2P5A.tsv, j = 11, N = 37, H = 4.5, TASK at 81cb025f)

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match):
  CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example gives `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf and base.json match the expected values.
- Cubes: `l2cubes.py` for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, idx ≡ 11 mod 37: 4 units)
Lane started 18:42Z (END 1793487284 = start + 4.5 h − 15 min). It finished all units at 19:45Z.

| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P4_6-11 | P4 | Q | 8000 | UNSAT, certified | 1803.91 | 84.3 | 444.6 | 5,173,648,904 | 4407 |
| P4_5-7-15 | P4 | H | 2400 | UNSAT, certified | 334.03 | 60.2 | 350.0 | 3,358,017,732 | 4377 |
| P4_6-8-9 | P4 | H | 2400 | UNSAT, certified | 78.04 | 23.4 | 168.9 | 1,116,206,216 | 3161 |
| P4_7-10-14 | P4 | H | 2400 | UNSAT, certified | 132.06 | 33.3 | 208.3 | 1,795,302,538 | 3487 |

Counts: by case and kind, P4 Q: 1 certified; P4 H: 3 certified. 0 timed out (UNKNOWN), 0 not reached, 0 errors.

Certified units (4), min / median / max:
- solve: 78.04 / 233.05 / 1803.91 s
- lrat-check: 23.4 / 46.75 / 84.3 s
- cake_lpr: 168.9 / 279.15 / 444.6 s
- proof size: 1.12 / 2.58 / 5.17 GB

Largest solver RSS: 4407 MB (P4_6-11).

There was no SAT, no proof rejection and no memory or disk problem. Every proof was deleted after both checks.

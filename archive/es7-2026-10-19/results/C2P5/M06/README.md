# C2P5 M06 (list C2P5A.tsv, j = 6, N = 37, H = 4.5, TASK commit 81cb025f)

## Tools and checks
- Tools built with `C2P/vendor/build_tools.sh` from the vendored sources (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). No code cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json as required.
- Cubes P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Note: `lists/C2P5A.tsv` is not present at commit 81cb025f; the HEAD version (92a2b58ad, rewritten for residues 1..36 mod 37) was used. Details in `tools.txt`.

## Units (idx ≡ 6 mod 37): 4 units, all certified
- P4 Q: 1 certified (P4_1-13). P4 H: 3 certified (P4_5-7-10, P4_6-7-9, P4_7-9-13).
- Timed out (UNKNOWN): 0. Not reached: 0. Errors / certified false: 0.

| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB | certified |
|---|---|---|---|---|---|---|---|---|---|---|
| P4_1-13 | P4 | Q | 8000 | UNSATISFIABLE | 1715.4 | 76.5 | 428.5 | 5.262 | 4386 | True |
| P4_5-7-10 | P4 | H | 2400 | UNSATISFIABLE | 24.99 | 12.1 | 104.5 | 0.216 | 2649 | True |
| P4_6-7-9 | P4 | H | 2400 | UNSATISFIABLE | 24.94 | 12.2 | 105.3 | 0.216 | 2664 | True |
| P4_7-9-13 | P4 | H | 2400 | UNSATISFIABLE | 94.57 | 28.2 | 180.0 | 1.511 | 3397 | True |

Certified (min / median / max): solve 24.94 / 59.78 / 1715.4 s; lrat-check 12.1 / 20.2 / 76.5 s; cake_lpr 104.5 / 142.65 / 428.5 s; proof 0.216 / 0.8635 / 5.262 GB.

Largest solver RSS: 4386 MB. No SAT, no proof rejection, no memory problem. The lane finished all units at 19:02:12Z, well before END (22:27:33Z).

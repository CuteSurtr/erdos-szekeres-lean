# C2P5 M04 — list C2P5A.tsv, shard j = 4 of N = 37, H = 4.5 h (TASK commit 81cb025f)

Start 2026-10-31 18:12:39 UTC (epoch 1793470359), END 1793485659 (22:27:39 UTC). The lane finished all units at 19:46:00 UTC.

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only. Manifest: all 196 files match. CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. Nothing was cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. sha256 of base.cnf `b0061e90…d8ff1` and of base.json `2476faff…bf472b48`, both as required.
- Cubes P1..P8 from `C2C34/l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (`units.tsv`, `out.jsonl`)
| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P4_1-10 | P4 | Q | 8000 | UNSAT, certified | 3017.94 | 102.5 | 568.6 | 6335612555 | 4401.8 |
| P4_5-6-15 | P4 | H | 2400 | UNSAT, certified | 327.84 | 54.4 | 319.1 | 3340574827 | 4370.2 |
| P4_5-14-15 | P4 | H | 2400 | UNSAT, certified | 319.29 | 59.8 | 326.1 | 3362505817 | 4362.9 |
| P4_7-9-11 | P4 | H | 2400 | UNSAT, certified | 79.95 | 26.9 | 169.7 | 1270045995 | 3224.6 |

- Counts: 4 of 4 certified (P4 Q: 1, P4 H: 3). 0 timed out (UNKNOWN), 0 not reached, 0 errors.
- Certified, over all 4 units (min / median / max):
  - solve 79.95 / 323.57 / 3017.94 s
  - lrat-check 26.9 / 57.1 / 102.5 s
  - cake_lpr 169.7 / 322.6 / 568.6 s
  - proof 1.27 / 3.35 / 6.34 GB
- By kind: Q (1 unit) solve 3017.94 s, lrat-check 102.5 s, cake_lpr 568.6 s, proof 6.34 GB. H (3 units): solve 79.95 / 319.29 / 327.84 s, lrat-check 26.9 / 54.4 / 59.8 s, cake_lpr 169.7 / 319.1 / 326.1 s, proof 1.27 / 3.34 / 3.36 GB.
- Largest solver RSS: 4401.8 MB (P4_1-10). cake_lpr ran with an 8000 MB heap (about 8.2 GB RSS observed).

No SAT, no proof rejection, and no memory or disk problem.

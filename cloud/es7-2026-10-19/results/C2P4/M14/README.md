# C2P4 M14: LIST = C2P4.tsv, j = 14, N = 50, H = 2.5 (TASK commit a46b478d)

Start 2026-10-31 13:02:22Z, lane END 15:17:22Z (epoch 1793459842). The lane finished at 15:03:18Z. It had 843 s left before END, which is under the 15-minute margin, so it started no more units.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: the vendored sources match `MANIFEST.sha256` (all 196 files). Built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch). Nothing was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and base.json (2476faff…) both match.
- Cubes P1..P8: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (13 = rows idx ≡ 14 mod 50)
| case | kind | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|---|
| P5 | Q | 1 (P5_7-13) | 0 | 0 | 0 |
| P4 | Q | 1 (P4_8-11) | 0 | 0 | 0 |
| P4 | H | 5 (P4_1-7-11, P4_2-5-8, P4_5-7-8, P4_6-7-12, P4_8-9-12) | 0 | 0 | 0 |
| P3 | Q | 0 | 0 | 1 (P3_6-13) | 0 |
| P3 | H | 0 | 0 | 5 (P3_1-6-13, P3_1-13-15, P3_4-9-11, P3_5-8-14, P3_7-8-9) | 0 |
| **total** | | **7** | **0** | **6** | **0** |

All 7 records are UNSATISFIABLE with `lrat-check: c VERIFIED` and `cake_lpr: s VERIFIED UNSAT`. That means all of M14's P4 and P5 units are closed. Some caps in `out.jsonl` are below the list cap because the lane shortened them to fit before END. Every solve that ran finished inside its cap.

| unit | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|
| P5_7-13 (Q) | 3023.0 | 107.8 | 596.7 | 6,595,442,394 | 4363 |
| P4_8-11 (Q) | 604.1 | 64.4 | 373.3 | 3,632,900,336 | 4406 |
| P4_1-7-11 (H) | 540.7 | 60.9 | 344.8 | 3,577,775,483 | 4366 |
| P4_2-5-8 (H) | 255.3 | 56.4 | 308.7 | 3,263,682,606 | 4415 |
| P4_5-7-8 (H) | 27.1 | 13.4 | 107.7 | 219,249,138 | 2648 |
| P4_6-7-12 (H) | 86.4 | 27.6 | 185.9 | 1,390,354,653 | 3413 |
| P4_8-9-12 (H) | 77.2 | 25.6 | 168.7 | 1,128,419,167 | 3149 |

Certified units (min / median / max): solve 27.1 / 255.3 / 3023.0 s; lrat-check 13.4 / 56.4 / 107.8 s; cake_lpr 107.7 / 308.7 / 596.7 s; proof 0.22 / 3.26 / 6.60 GB.

Largest solver RSS: 4415 MB (P4_2-5-8).

No SAT, no proof rejections, no errors, and no memory or disk problems: the 15 GB machine had at least about 21 GB of disk free throughout.

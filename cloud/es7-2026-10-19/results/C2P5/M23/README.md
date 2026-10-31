# C2P5 M23

TASK `results/C2P5/TASK.md` at 81cb025f; V = M23, LIST = C2P5A.tsv, j = 23, N = 37, H = 4.5.
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-31T19:11:08Z (epoch 1793473868), END 1793489168
(23:26:08Z). The lane ran from 19:13:30Z to 21:07:08Z and finished every unit well before END.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`, built from the vendored sources only (nothing cloned or downloaded). The manifest
  (196 files) matches: CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity checks: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints
  `s VERIFIED UNSAT`.
- Base CNF: `p cnf 838032 16653336`; sha256 b0061e90… (base.cnf) and 2476faff… (base.json), both as expected.
- Cubes P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, idx ≡ 23 mod 37 of C2P5A.tsv)
| idx | unit | case | kind | cap | status | certified | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 23 | P4_5-14 | P4 | Q | 8000 | UNSAT | yes | 3072.8 | 112.1 | 605.6 | 7 195 319 050 | 4394 |
| 60 | P4_2-5-16 | P4 | H | 2400 | UNSAT | yes | 354.5 | 57.0 | 327.4 | 3 545 804 575 | 4420 |
| 97 | P4_2-9-12 | P4 | H | 2400 | UNSAT | yes | 347.1 | 57.1 | 326.8 | 3 389 634 347 | 4372 |
| 134 | P4_5-10-16 | P4 | H | 2400 | UNSAT | yes | 519.6 | 62.5 | 364.2 | 3 676 292 521 | 4369 |
| 171 | P4_6-12-13 | P4 | H | 2400 | UNSAT | yes | 186.7 | 48.0 | 282.5 | 2 470 255 668 | 3760 |

Counts:
- P4 Q: 1 of 1 certified.
- P4 H: 4 of 4 certified.
- Timed out (UNKNOWN): 0. Not reached: 0. Errors: 0.

Statistics over the 5 certified units (min / median / max):
- solve: 186.7 / 354.5 / 3072.8 s
- lrat-check: 48.0 / 57.1 / 112.1 s
- cake_lpr (all at heap 8000 MB): 282.5 / 327.4 / 605.6 s
- proof size: 2.47 / 3.55 / 7.20 GB

Proofs were deleted after both checks, as lane.py does.

The largest solver RSS was 4420 MB (P4_2-5-16).

There was no SAT answer, no proof rejection and no memory problem.

# C2P4 M12

Fourth wave on the parallelogram cases (TASK.md at commit a46b478d), V = M12, LIST = C2P4.tsv, j = 12, N = 50, H = 2.5.
Start 2026-10-31 13:02:08 UTC (epoch 1793451728), END = 1793459828 (15:17:08 UTC). Lane finished at 15:07:12 UTC.

## Tools and checks (details in `tools.txt`)

- `C2P/vendor/build_tools.sh` built from the vendored sources only: manifest (196 files) matched; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc, E2 patch).
- Sanity: both checkers rejected the bad LRAT and accepted the good one; the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json as required.
- Cubes P1..P8 from `C2C34/l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (13 rows with idx ≡ 12 mod 50)

| outcome | count | units |
|---|---|---|
| certified UNSAT | 4 | P5_2-11 (Q), P4_8-9 (Q), P4_1-7-9 (H), P4_2-5-6 (H) |
| timed out (UNKNOWN) | 1 | P4_5-6-15 (H), at a reduced cap of 328 s because END was near (not a full 1800 s attempt) |
| not reached | 8 | P4_6-7-10, P4_8-9-10 (H); P3_6-11 (Q); P3_1-6-11, P3_1-12-16, P3_4-8-16, P3_5-8-12, P3_6-11-13 (H) |
| errors / certified false | 0 | |

By case and kind:

| case | kind | certified | UNKNOWN | not reached |
|---|---|---|---|---|
| P5 | Q | 1 | 0 | 0 |
| P4 | Q | 1 | 0 | 0 |
| P4 | H | 2 | 1 | 2 |
| P3 | Q | 0 | 0 | 1 |
| P3 | H | 0 | 0 | 5 |

Certified units (cap shown is the effective cap set by lane.py):

| unit | cap s | solve s | lrat-check s | cake_lpr s | proof bytes |
|---|---|---|---|---|---|
| P5_2-11 | 7000 | 3785.52 | 115.9 | 682.3 | 6 393 585 475 |
| P4_8-9 | 2707 | 533.37 | 58.1 | 335.5 | 3 368 994 711 |
| P4_1-7-9 | 1765 | 347.44 | 56.8 | 343.7 | 3 305 348 260 |
| P4_2-5-6 | 1006 | 259.12 | 56.3 | 351.0 | 3 325 663 718 |

Min / median / max: solve 259.12 / 440.41 / 3785.52 s; lrat-check 56.3 / 57.45 / 115.9 s; cake_lpr 335.5 / 347.35 / 682.3 s; proof 3.31 / 3.35 / 6.39 GB.
All four proofs: `c VERIFIED` (lrat-check) and `s VERIFIED UNSAT` (cake_lpr).

## Resources and anomalies

- Largest solver RSS: 4408.71 MB (P4_1-7-9). No memory problems (15 GB machine; cake_lpr heap 8000 MB).
- No SAT, no proof rejection, no errors.
- Note: P4_8-9 was listed with cap 6000 s but ran under a cap of 2707 s set by lane.py's END limit; it finished in 533 s, so the reduced cap made no difference. P4_5-6-15 only had 328 s and remains open.

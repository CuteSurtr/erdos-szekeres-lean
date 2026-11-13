# C2P5 M77: list C2P5B.tsv, shard j = 27 of N = 50, H = 5.25 (TASK commit 81cb025f)

Start 2026-10-31 15:11:48Z, END 1793477508 (20:11:48Z). The lane finished all units at 19:38:29Z.

## Tools and checks (`tools.txt`)
- Built by `C2P/vendor/build_tools.sh` from the vendored sources only (CaDiCaL c6073042 = 3.0.1, cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch); manifest: all 196 files match.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF header `p cnf 838032 16653336`; sha256 of base.cnf and base.json both as expected.
- Cubes P1..P8 from `l2cubes.py` byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (19 = rows with idx ≡ 27 mod 50)
All 19 units are **certified UNSAT** (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`). None timed out, none not reached, no errors.

| case | Q certified | H certified |
|---|---|---|
| P2 | 1 (P2_4-12) | 6 |
| P1 | 1 (P1_3-11) | 5 |
| P3 | 1 (P3_6-14) | 5 |
| total | 3 | 16 |

Certified units, min / median / max:
- solve: 24.5 / 300.7 / 2394.7 s (Q: 1744.9, 1483.7, 2394.7 s)
- lrat-check: 12.6 / 55.4 / 96.8 s
- cake_lpr: 106.8 / 320.2 / 533.9 s
- proof size: 0.22 / 3.27 / 6.06 GB

Note: P3_6-14 ran with cap 7477 s, P3_5-8-15 with 2248 s and P3_7-8-10 with 1544 s (reduced by lane.py for END); all finished well within.

Largest solver RSS: 4429 MB (P1_2-10-15).

No SAT, no proof rejection, no memory problem. Per-unit records in `out.jsonl`.

# C2P4 M26: LIST = C2P4.tsv, j = 26, N = 50, H = 2.5, Z = a46b478d

Start 2026-10-31 13:02:22 UTC (epoch 1793451742), END = 1793459842 (15:17:22 UTC). Machine: 4 cores, 15 GB, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored `vendor/tools-src.tar.xz` (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). No code was cloned or downloaded.
- Sanity checks: the bad LRAT was rejected by both checkers, the good one was accepted by both, and the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. sha256 matches for base.cnf (b0061e90…) and base.json (2476faff…).
- Cubes: P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (19 rows, idx ≡ 26 mod 50)
| | P5 | P6 | P4 | P3 | total |
|---|---|---|---|---|---|
| certified Q | 1 | 0 | 1 | 0 | 2 |
| certified H | 4 | 1 | 1 | 0 | 6 |
| timed out (UNKNOWN) | 0 | 0 | 0 | 0 | 0 |
| not reached Q | 0 | 0 | 0 | 1 | 1 |
| not reached H | 0 | 0 | 5 | 5 | 10 |
| errors / certified false | 0 | 0 | 0 | 0 | 0 |

Certified (all UNSAT; both lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`): P5_2-15 (Q), P6_7-8-11, P5_1-11-16, P5_2-10-12, P5_6-10-11, P5_7-12-13, P4_1-15 (Q), P4_1-2-10.
- The lane cut the solve caps of P4_1-15 (2891 s instead of 6000 s) and P4_1-2-10 (787 s instead of 1800 s) because of END. Both solves finished well within those caps.

Not reached: the lane stopped at 15:06:54 with 627 s left, below its 15-minute threshold. These units were not reached: P4_1-8-10, P4_2-5-15, P4_5-7-15, P4_6-8-12, P4_9-10-12, P3_7-13 (Q), P3_1-7-11, P3_4-5-8, P3_4-10-12, P3_5-9-15, P3_7-9-12.

### Certified units, min / median / max
- solve: 27.4 / 348.5 / 1786.2 s (Q: 1786.2 and 1559.2 s)
- lrat-check: 13.3 / 57.9 / 85.4 s
- cake_lpr: 117.8 / 330.4 / 470.6 s
- proof size: 0.216 / 3.31 / 5.16 GB

Largest solver RSS: 4420 MB (P4_1-15).

No SAT, no proof rejection and no memory problem. Proofs were deleted after checking; no CNF or proof files are committed.

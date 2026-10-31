# C2P M22 (LIST = C2P.tsv, j = 22, N = 42, H = 3.0, Z = 01909a07)

Start 2026-10-31 03:23:23 UTC (epoch 1793417003); END = 1793426903 (06:08:23 UTC). This attempt replaces the earlier
one (TASK at fb2c59af) that stopped at step 1. Lane started 03:25:39, stopped at 05:54:18 ("844 s left", under the
15-minute start limit) after 14 units.

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only: CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8,
  drat-trim 2e3b2dc lrat-check.c with the E2 patch. Manifest: all 196 files match.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf (`b0061e90…`) and base.json (`2476fafff…`) match.
- Cubes P1..P8: all 8 byte-identical to `C2P/cubes/`.

## Units
`units.tsv` holds 53 units (idx ≡ 22 mod 42). Records are in `out.jsonl`, the log tail in `lane.log.tail`.

| case | kind | units | certified | timed out | not reached | error |
|---|---|---|---|---|---|---|
| P1 | H | 5 | 0 | 0 | 5 | 0 |
| P1 | Q | 2 | 0 | 0 | 2 | 0 |
| P2 | H | 5 | 0 | 0 | 5 | 0 |
| P2 | Q | 1 | 0 | 0 | 1 | 0 |
| P2 | cover | 1 | 0 | 0 | 1 | 0 |
| P3 | H | 4 | 0 | 0 | 4 | 0 |
| P3 | Q | 2 | 0 | 0 | 2 | 0 |
| P4 | H | 6 | 0 | 0 | 6 | 0 |
| P4 | Q | 1 | 0 | 0 | 1 | 0 |
| P5 | H | 5 | 0 | 0 | 5 | 0 |
| P5 | Q | 2 | 0 | 0 | 2 | 0 |
| P6 | H | 6 | 2 | 0 | 4 | 0 |
| P6 | Q | 1 | 0 | 0 | 1 | 0 |
| P7 | H | 6 | 6 | 0 | 0 | 0 |
| P7 | Q | 1 | 1 | 0 | 0 | 0 |
| P8 | H | 5 | 5 | 0 | 0 | 0 |
| all | | 53 | 14 | 0 | 39 | 0 |

Certified (14, all UNSATISFIABLE, both lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, cake heap 8000 MB):
P8_3-9-15, P8_4-9-10, P8_2-5-15, P8_4-9-15, P8_1-2-13, P7_2-8-15, P7_10-11-12, P7_10-13, P7_1-12-16, P7_2-14-16, P7_2-10-16, P7_8-11-16, P6_7-9-15, P6_2-7-8.

Certified units, min / median / max:
- solve: 21.1 / 234.4 / 723.3  s
- lrat-check: 11.5 / 47.5 / 54.7  s
- cake_lpr: 107.6 / 271.8 / 313.1  s
- proof size: 0.2 / 3.2 / 4.0 GB (proofs deleted after checking)

Timed out (UNKNOWN): none. Errors / `"certified": false`: none. Not reached: the remaining 39 units (all of P1–P5,
P2_cover included, and 6 of P6), because the 3-hour budget ran out.

## Memory, SAT, rejections
Largest solver RSS: 4469.97 MB (machine 15 GB); no memory problem.
No SAT answer (`/opt/work/SAT_FOUND` never appeared). No proof rejected.

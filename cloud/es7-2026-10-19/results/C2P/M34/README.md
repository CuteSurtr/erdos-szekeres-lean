# C2P / M34 (LIST C2P.tsv, shard 34 of 42, H = 3.0, Z = 01909a07)

Start 03:22:54Z (epoch 1793416974), END 06:07:54Z; lane finished at 05:57:58Z ("stop: 595 s left").
This run replaces the earlier M34 attempt (TASK at fb2c59af), which had stopped at step 1.

**Result: 11 units certified UNSAT, 1 timed out (UNKNOWN), 41 not reached. No SAT, no proof rejection, no error, no memory problem.**

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match):
  CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json match.
- Cubes P1..P8: byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (53; `units.tsv`, `out.jsonl`)

| case | kind | units | certified | UNKNOWN | not reached |
|---|---|---|---|---|---|
| P8 | H | 5 | 5 | 0 | 0 |
| P7 | H | 5 | 5 | 0 | 0 |
| P7 | Q | 2 | 1 (P7_1-4) | 1 (P7_3-12) | 0 |
| P6 | H / Q | 6 / 1 | 0 | 0 | 7 |
| P5 | H / Q | 4 / 2 | 0 | 0 | 6 |
| P4 | H / Q / cover | 5 / 1 / 1 | 0 | 0 | 7 |
| P3 | H / Q | 5 / 2 | 0 | 0 | 7 |
| P2 | H / Q | 6 / 1 | 0 | 0 | 7 |
| P1 | H / Q | 6 / 1 | 0 | 0 | 7 |
| total | | 53 | 11 (10 H, 1 Q) | 1 (Q) | 41 (35 H, 5 Q, 1 cover) |

- Certified (both lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, heap 8000 MB every time):
  P8_2-10-15, P8_3-12-13, P8_3-9-13, P8_3-11-15, P8_9-12-15, P7_3-4-9, P7_1-4, P7_1-5-8, P7_2-3-15, P7_8-11-13, P7_1-4-16.

| certified (11) | min | median | max |
|---|---|---|---|
| solve s | 92.1 | 314.1 | 985.8 (P7_1-4, Q) |
| lrat-check s | 27.7 | 53.3 | 65.9 |
| cake_lpr s | 176.7 | 305.0 | 363.7 |
| proof size | 1.38 GB | 3.27 GB | 4.23 GB |

- Timed out: P7_3-12 (Q), UNKNOWN after 1102 s. Its cap was shortened from the list cap to 1111 s by END,
  so it did not get its full list cap; it is still open.
- Errors / `certified: false`: none.

## Resources
- Largest solver RSS: 4467 MB (P8_3-9-13); no memory problem.
- No SAT_FOUND, no proof rejection.

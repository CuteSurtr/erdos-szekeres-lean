# C2P / M14 (LIST C2P.tsv, shard 14 of 42, H = 3.0, Z = 01909a07)

Start 2026-10-31 03:23:42Z (epoch 1793417022), END 1793426922 (06:08:42Z). One lane (`run.sh`); lane done at 05:58:46Z.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` from the vendored sources (nothing cloned or downloaded): manifest 196/196 files match;
  CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF header `p cnf 838032 16653336`, sha256 of base.cnf and base.json match.
- Cubes P1..P8: byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).
- The earlier attempt (fb2c59af, stopped at step 1) was replaced.

## Units (53: P8 5 H; P7 5 H + 2 Q; P6..P1 as in `units.tsv`; no cover)
| | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|
| P8 H | 5 | 0 | 0 | 0 |
| P7 H | 5 | 0 | 0 | 0 |
| P7 Q | 1 | 1 | 0 | 0 |
| P6 H / Q | 0 | 0 | 6 / 1 | 0 |
| P5 H / Q | 0 | 0 | 5 / 2 | 0 |
| P4 H / Q | 0 | 0 | 6 / 1 | 0 |
| P3 H / Q | 0 | 0 | 6 / 1 | 0 |
| P2 H / Q | 0 | 0 | 6 / 1 | 0 |
| P1 H / Q | 0 | 0 | 5 / 1 | 0 |
| **total** | **11** | **1** | **41** | **0** |

- Certified (11; both lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, heap 8000 MB every time):
  P8_1-5-12, P8_3-10-14, P8_2-3-10, P8_1-6-10, P8_2-11-13, P7_2-12-13, P7_8-10 (Q), P7_1-4-11, P7_3-10-14,
  P7_1-2-12, P7_8-10-11.
  - solve s: min 25.1, median 392.2, max 592.1
  - lrat-check s: min 13.1, median 54.7, max 59.9
  - cake_lpr s: min 110.1, median 309.8, max 331.2
  - proof size: min 0.21 GB, median 3.47 GB, max 3.72 GB
- Timed out: P7_9-14 (Q), UNKNOWN after 1036 s. Its cap was reduced by the END limit to 1045 s (list cap 2400 s),
  so it did not get its full cap.
- Not reached (41): all of P6, P5, P4, P3, P2, P1 in this shard.

## Resources and anomalies
- Largest solver RSS: 4403 MB (P8_2-3-10). No memory problem; no cake_lpr heap retry.
- No SAT, no proof rejection, no `certified: false`, no ERROR record.

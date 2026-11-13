# C2P / M21 (LIST C2P.tsv, shard 21 of 42, H = 3.0, Z = 01909a07)

Restart of M21 (the earlier attempt at fb2c59af stopped at step 1; its files were replaced).

**Result: 10 of 53 units certified UNSAT, 0 timed out, 43 not reached, 0 errors. No SAT.**

## Tools and checks (`tools.txt`)
- `vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1),
  cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch. Sanity: both checkers reject the bad LRAT and accept the good one;
  cake_lpr example `s VERIFIED UNSAT`.
- Base CNF `p cnf 838032 16653336`, sha256 of base.cnf and base.json both match.
- Cubes P1..P8: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Run
One lane (`run.sh`), start 03:23:13Z, END 06:08:13Z. It finished its 10th unit at 05:53:28Z and stopped with
884 s left (< 15 min, no new unit started).

## Units (`units.tsv`, 53: 42 H, 11 Q, no cover)
| case | units (H+Q) | certified | timed out | not reached | errors |
|---|---|---|---|---|---|
| P8 | 3H+2Q | 3H+2Q | 0 | 0 | 0 |
| P7 | 5H+2Q | 4H+1Q | 0 | 1H+1Q (P7_1-13 Q, P7_2-8-16 H) | 0 |
| P6 | 6H+1Q | 0 | 0 | 6H+1Q | 0 |
| P5 | 6H+1Q | 0 | 0 | 6H+1Q | 0 |
| P4 | 6H+1Q | 0 | 0 | 6H+1Q | 0 |
| P3 | 6H+1Q | 0 | 0 | 6H+1Q | 0 |
| P2 | 4H+2Q | 0 | 0 | 4H+2Q | 0 |
| P1 | 6H+1Q | 0 | 0 | 6H+1Q | 0 |
| total | 42H+11Q | 7H+3Q = 10 | 0 | 35H+8Q = 43 | 0 |

Certified units (all `c VERIFIED` by lrat-check and `s VERIFIED UNSAT` by cake_lpr; proofs deleted):
P8_1-4 (Q), P8_3-11-13, P8_1-4-6, P8_1-3-5, P8_10-14 (Q), P7_2-16 (Q), P7_3-4-8, P7_9-11-14, P7_1-6-11, P7_8-14-15.

| | min | median | max |
|---|---|---|---|
| solve s | 63.3 | 241.1 | 1795.9 (P8_10-14, cap 2400) |
| lrat-check s | 22.4 | 50.6 | 81.9 |
| cake_lpr s | 157.4 | 289.7 | 441.3 |
| proof size | 1.11 GB | 3.24 GB | 5.36 GB |

Q units are the slow ones (solve 896, 1162, 1796 s); H units 63–533 s.

- Largest solver RSS: 4416 MB (P7_2-16). No memory problem (cake_lpr heap 8000 MB).
- No SAT, no proof rejection, no `certified: false` record, no ERROR status.

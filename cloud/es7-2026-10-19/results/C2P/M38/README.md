# C2P / M38 (LIST C2P.tsv, shard 38 of 42, H = 3.0, Z = 01909a07)

Restart of an earlier attempt (task at fb2c59af) that stopped at step 1; its files were replaced.
Start 03:22:41Z (epoch 1793416961), END 06:07:41Z (1793426861). Lane finished at 05:53:03Z ("stop: 877 s left").

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: vendored sources, manifest 196/196 files match; nothing cloned or downloaded.
  CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check from drat-trim 2e3b2dc with the E2 patch.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF header `p cnf 838032 16653336`; sha256 of base.cnf and base.json match.
- Cubes P1..P8: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (53: 43 H, 10 Q, no cover)
| | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|
| total | 8 | 2 | 43 | 0 |
| P8 (4H+1Q) | 4 H | 1 Q (P8_1-12) | 0 | 0 |
| P7 (6H+1Q) | 4 H | 1 Q (P7_2-10) | 2 H | 0 |
| P1 (6H+1Q) | 0 | 0 | 6 H + 1 Q | 0 |
| P2 (5H+2Q) | 0 | 0 | 5 H + 2 Q | 0 |
| P3 (6H+1Q) | 0 | 0 | 6 H + 1 Q | 0 |
| P4 (5H+2Q) | 0 | 0 | 5 H + 2 Q | 0 |
| P5 (5H+1Q) | 0 | 0 | 5 H + 1 Q | 0 |
| P6 (6H+1Q) | 0 | 0 | 6 H + 1 Q | 0 |

Certified (all H): P8_1-7-12, P8_10-12-14, P8_1-3-6, P8_1-4-14, P7_2-10-12, P7_1-3-8, P7_8-9-12, P7_2-4-11 —
every one `c VERIFIED` (lrat-check) and `s VERIFIED UNSAT` (cake_lpr, heap 8000 MB).
Timed out at cap 2400 s (both Q): P8_1-12 (2383.7 s), P7_2-10 (2381.0 s).
Not reached (in file order): the remaining 2 P7 H units and all of P6, P5, P4, P3, P2, P1 (see `units.tsv`).

Certified units, min / median / max:
- solve: 23.1 / 267.0 / 582.8 s
- lrat-check: 12.5 / 51.6 / 60.3 s
- cake_lpr: 112.4 / 297.5 / 335.0 s
- proof size: 0.21 / 3.26 / 3.73 GB (214,644,479 / 3,255,621,482 / 3,727,415,783 bytes)

Largest solver RSS: 4414 MB (P8_1-12). Free memory never a problem on 15 GB.

No SAT, no proof rejection, no ERROR record, no memory problem.

# C2P4 M00: shard 0 of 50 of `lists/C2P4.tsv` (H = 2.5 h, task commit a46b478d)

Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-31 13:01:29 UTC (epoch 1793451689), lane END = start + 2.5 h − 15 min = 1793459789 (15:16:29 UTC).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 files of `tools-src.tar.xz` match `MANIFEST.sha256`. It built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch) from the vendored sources only. Nothing was cloned or downloaded.
- Sanity: the cake_lpr example gives `s VERIFIED UNSAT`. Both checkers reject the bad LRAT on {1},{−1}: lrat-check gives `c FAILED`, cake_lpr gives `Checking failed`. Both accept the good one: `c VERIFIED` and `s VERIFIED UNSAT`.
- Base CNF (`SYMZ/zcnf.py rot 17 7 --m 2 --hull`): header `p cnf 838032 16653336`. sha256 is b0061e90…d8ff1 for base.cnf and 2476faff…bf472b48 for base.json, both as expected.
- Cubes: `C2C34/l2cubes.py` for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (`units.tsv`: 13 rows, idx ≡ 0 mod 50)

| unit | case | kind | result | solve s | lrat-check s | cake_lpr s | proof | solver RSS |
|---|---|---|---|---|---|---|---|---|
| P6_1-7 | P6 | Q (cap 7000) | **UNSAT, certified** | 5818.35 | 168.5 | 829.4 | 9.56 GB (9558426451 B) | 4377 MB |
| P4_6-11 | P4 | Q (cap 6000, cut to 476 by END) | UNKNOWN (timeout at 476 s) | 471.47 | – | – | – | 4407 MB |

Not reached, because the lane stopped with 595 s left (11 units):
- P4: one Q (P4_6-11 was reached but cut short) and 5 H: P4_1-5-16, P4_1-11-15, P4_2-9-10, P4_5-11-12, P4_7-9-10.
- P3: one Q (P3_5-8) and 5 H: P3_1-5-9, P3_1-10-13, P3_4-7-12, P3_5-6-15, P3_6-8-13.

Totals by case and kind:
- P6 Q: 1 certified.
- P4 Q: 1 timed out, only at a reduced 476 s cap, not the full 6000 s, so it should be run again at full cap elsewhere.
- P4 H: 5 not reached.
- P3 Q: 1 not reached.
- P3 H: 5 not reached.

Certified unit stats: with only one certified unit, the minimum, median and maximum are all that unit's values: solve 5818 s, lrat-check 168.5 s, cake_lpr 829.4 s, proof 9.56 GB.

Largest solver RSS: 4407 MB (cake_lpr ran with an 8000 MB heap, about 8.2 GB RSS).

No SAT. No proof was rejected, and there are no `certified: false` or `ERROR` records. No memory or disk problem: at the proof's peak, 19 GB of disk was still free.

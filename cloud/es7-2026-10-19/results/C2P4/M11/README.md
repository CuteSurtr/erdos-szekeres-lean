# C2P4 M11

Shard j = 11 of N = 50 of `lists/C2P4.tsv` (task commit a46b478d), budget H = 2.5 h. The lane started at 13:03:42Z.
END was 1793459789 (15:16:29Z). The lane stopped at 15:04:01Z with 747 s left, which is below the 900 s needed to
start a unit.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 files in the manifest matched. Built CaDiCaL 3.0.1 (c6073042), cake_lpr
  (a36874a8) and lrat-check (2e3b2dc + E2 patch) from the vendored sources. Nothing was downloaded.
- Sanity checks: lrat-check and cake_lpr both rejected the bad LRAT and both accepted the good one. The cake_lpr
  example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and of base.json (2476faff…) both
  match the expected values.
- Cubes P1..P8 from `l2cubes.py`: each is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (13 in `units.tsv`)
| unit | case | kind | status | cap s | solve s | RSS MB | proof | lrat-check s | cake_lpr s |
|---|---|---|---|---|---|---|---|---|---|
| P5_2-9 | P5 | Q | UNSAT, certified | 7000 | 2541.3 | 4423 | 6.24 GB | 95.8 | 549.7 |
| P4_7-14 | P4 | Q | UNSAT, certified | 4140 | 2754.3 | 4383 | 6.52 GB | 92.1 | 527.9 |
| P4_1-7-8 | P4 | H | UNSAT, certified | 727 | 236.6 | 4370 | 3.22 GB | 48.4 | 286.2 |

The cap was lowered for P4_7-14 and P4_1-7-8 because less time was left before END. All three units finished
well under their caps.

- Certified: 3 units (P5 Q 1, P4 Q 1, P4 H 1).
  - solve s: min 236.6, median 2541.3, max 2754.3.
  - lrat-check s: min 48.4, median 92.1, max 95.8.
  - cake_lpr s: min 286.2, median 527.9, max 549.7. All ran with an 8000 MB heap.
  - proof size: min 3.22 GB, median 6.24 GB, max 6.52 GB.
- Timed out (UNKNOWN): 0.
- Errors or `certified: false`: 0.
- Not reached: 10 units.
  - P4 H: 4 (P4_1-15-16, P4_5-6-14, P4_6-7-9, P4_7-12-13).
  - P3 Q: 1 (P3_6-10).
  - P3 H: 5 (P3_1-6-10, P3_1-12-15, P3_4-8-15, P3_5-8-11, P3_6-11-12).

## Other
- Largest solver RSS: 4423 MB (P5_2-9). There were no memory problems.
- No SAT result (`SAT_FOUND` was not created).
- No proof was rejected. cake_lpr never needed the 11000 MB retry.

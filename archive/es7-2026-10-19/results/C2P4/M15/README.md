# C2P4 M15: shard 15 of 50 of C2P4.tsv, H = 2.5 h (TASK commit a46b478d)

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only. All 196 manifest files match. The upstream commits are CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8 and lrat-check 2e3b2dc with the E2 patch.
- Sanity checks are as expected: both checkers reject the bad LRAT and accept the good one, and the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and base.json (2476faff…) both match.
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Run
- One lane (`run.sh`), started 13:04:17Z. END = start 1793451724 + 2.5 h − 15 min = 1793459824 (15:17:04Z).
- The lane stopped at 15:07:09Z with 594 s left, which is less than the 900 s needed to start a unit.

## Units (14 in `units.tsv`)
| unit | case | kind | cap | result |
|---|---|---|---|---|
| P6_5-16 | P6 | Q | 6000 | **certified** UNSAT |
| P5_9-11 | P5 | Q | 6000 (given 499 s by the time limit) | UNKNOWN (timed out at the shortened cap) |
| other 12 | | | | not reached |

Counts:
- Certified: 1 (P6 Q: 1).
- Timed out (UNKNOWN): 1 (P5 Q: 1). It is open; the shortened 499 s cap says nothing about its difficulty.
- Not reached: 12.
  - P4: Q 1 (P4_6-8), H 5 (P4_1-5-13, P4_1-11-12, P4_2-8-11, P4_5-10-14, P4_6-13-14).
  - P3: Q 1 (P3_4-10), H 5 (P3_1-4-11, P3_1-9-10, P3_4-6-12, P3_4-14-15, P3_6-7-10).
- Errors: 0.

Certified unit P6_5-16 (with only one certified unit, the minimum, median and maximum are all this one value):
- solve 5883.6 s (5952 s wall)
- lrat-check 131.0 s (`c VERIFIED`)
- cake_lpr 757.3 s (`s VERIFIED UNSAT`, heap 8000 MB)
- proof 9,044,746,159 bytes (sha256 7d060f26…), deleted after the checks

Largest solver RSS: 4370 MB (P6_5-16). P5_9-11 used 4363 MB.

No SAT, no proof rejection, no memory problem. Disk was the tightest resource: the 9.0 GB proof left about 19 GB free.

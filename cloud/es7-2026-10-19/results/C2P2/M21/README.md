# C2P2 M21: LIST = C2P2.tsv, j = 21, N = 42, H = 2.5, TASK commit d266d2c3

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match):
  CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc, E2 patch).
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; base.cnf sha256 `b0061e90…8ff1` and base.json sha256 `2476faff…2b48` both match.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (8 rows, idx ≡ 21 mod 42)
One lane started 06:49:51Z with END = 1793437350 (09:02:30Z); it stopped at 08:52:03Z with 626 s left.

| unit | case | kind | cap (s) | status | solve s | lrat-check s | cake_lpr s | proof | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P7_1-6 | P7 | Q | 6000 | certified | 4310.9 | 134.0 | 705.3 | 8.48 GB | 4360 |
| P6_1-3-13 | P6 | H | 1800 | certified | 297.0 | 54.5 | 315.8 | 3.29 GB | 4366 |
| P6_1-9-13 | P6 | H | 1800 (lane cap 1473) | certified | 431.6 | 58.0 | 327.3 | 3.50 GB | 4359 |
| P6_2-3-15 | P6 | H | 1800 (lane cap 643) | certified | 242.4 | 52.9 | 311.2 | 3.21 GB | 4391 |
| P6_2-11-13 | P6 | H | 1800 | not reached | | | | | |
| P6_3-10-11 | P6 | H | 1800 | not reached | | | | | |
| P6_7-15 | P6 | Q | 2400 | not reached | | | | | |
| P6_10-12 | P6 | Q | 2400 | not reached | | | | | |

Counts by case and kind:
- Certified (4): P7 Q 1 (P7_1-6), P6 H 3.
- Timed out (UNKNOWN): 0.
- Not reached (4): P6 H 2 and P6 Q 2.
- Errors: 0.

Certified units (min / median / max):
- Solve: 242.4 / 364.3 / 4310.9 s.
- lrat-check: 52.9 / 56.3 / 134.0 s.
- cake_lpr: 311.2 / 321.6 / 705.3 s.
- Proof size: 3.21 / 3.39 / 8.48 GB.

The cap column shows the TASK cap; for two units the lane lowered the solve cap to fit before END. Both checkers returned VERIFIED for every proof (`c VERIFIED`, `s VERIFIED UNSAT`); every record has `"certified": true`.

P7_1-6 had timed out at its full cap in the first wave. Here it was solved at the 6000 s cap in 4311 s and certified.

## Resources and anomalies
- Largest solver RSS: 4391 MB (P6_2-3-15). cake_lpr ran with an 8000 MB heap. There was no memory problem.
- The largest proof (8.5 GB) used at most about 20 GB of disk.
- No SAT, no proof rejection, no errors.

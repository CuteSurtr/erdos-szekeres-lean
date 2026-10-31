# C2P2 M29: shard j = 29 of N = 42 of C2P2.tsv, H = 2.5 h, task commit d266d2c3

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built from the vendored sources only. Manifest: all 196 files match. The builds are CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc + E2 patch). Nothing was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example gave `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…d8ff1) and of base.json (2476faff…2b48) both match the expected values.
- Cubes P1..P8: each is byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Commits in this directory: env 9a296bf2 (rebased on push), tools/units/run.sh, progress, and this README.

## Units (`units.tsv`, 7 units: idx ≡ 29 mod 42)
Run by one lane (`run.sh`): start 06:46:53Z, END 09:01:53Z.

| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof bytes |
|---|---|---|---|---|---|---|---|---|
| P7_3-9 | P7 | Q | 6000 | UNSAT, certified | 3200.2 | 112.1 | 606.3 | 7,281,534,886 |
| P6_1-4-10 | P6 | H | 1800 | UNSAT, certified | 397.6 | 56.7 | 325.9 | 3,452,814,573 |
| P6_1-10-14 | P6 | H | 1800 | UNSAT, certified | 367.9 | 56.0 | 319.5 | 3,417,957,500 |
| P6_2-7 | P6 | Q | 2400 → 1814 (lane cut to time left) | UNKNOWN (timeout at 1796.8 s) | – | – | – | – |
| P6_2-13 | P6 | Q | 2400 | not reached | | | | |
| P6_7-8-12 | P6 | H | 1800 | not reached | | | | |
| P6_8-9-15 | P6 | H | 1800 | not reached | | | | |

Counts:
- Certified: 3. P7 Q: 1 (P7_3-9, a first-wave full-cap timeout, now closed at 3200 s). P6 H: 2.
- Timed out: 1, in P6 Q (P6_2-7). It ran only at the reduced cap of 1814 s, not its full 2400 s, so it is not a full-cap timeout.
- Not reached: 3, P6 Q: 1 and P6 H: 2.
- Errors: 0. Uncertified UNSAT records: 0.

Certified units (min / median / max):
- solve s: 367.9 / 397.6 / 3200.2.
- lrat-check s: 56.0 / 56.7 / 112.1.
- cake_lpr s (all at 8000 MB heap): 319.5 / 325.9 / 606.3.
- proof bytes: 3.42 GB / 3.45 GB / 7.28 GB.

## Other
- Largest solver RSS: 4418 MB (P6_2-7). The largest checker RSS seen was about 8.2 GB (cake_lpr). There were no memory problems, and peak disk use was about 21 GB of 29 GB free.
- No SAT and no proof rejection. Every proof was deleted after checking. No CNF or proof files were committed.

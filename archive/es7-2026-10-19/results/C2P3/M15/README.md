# C2P3 M15 (LIST = C2P3.tsv, j = 15, N = 50, H = 2.5, Z = 4f653319)

## Tools and checks
- `C2P/vendor/build_tools.sh` built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch) from the vendored `tools-src.tar.xz`. All 196 files matched the manifest. Nothing was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. Both sha256 values matched: base.cnf `b0061e90…d8ff1` and base.json `2476faff…bf472b48`.
- Cubes P1..P8 from `C2C34/l2cubes.py` were byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details are in `tools.txt`.

## Units (10 rows with idx ≡ 15 mod 50)
Status at a glance: 4 certified, 1 timed out (UNKNOWN), 5 not reached, 0 errors.

| unit | case | kind | status | solve s | proof | lrat-check s | cake_lpr s |
|---|---|---|---|---|---|---|---|
| P6_1-11 | P6 | Q | certified | 3861.36 | 7.66 GB | 110.5 | 595.1 |
| P6_1-9-15 | P6 | H | certified | 409.69 | 3.53 GB | 55.0 | 309.4 |
| P6_3-7-14 | P6 | H | certified | 478.07 | 3.67 GB | 59.5 | 337.1 |
| P6_8-9-13 | P6 | H | certified | 25.73 | 0.22 GB | 12.1 | 109.3 |
| P5_1-4 | P5 | Q | UNKNOWN (cap cut to 842 s by END) | 834.68 | – | – | – |

Five P5 H units were not reached: P5_1-10-15, P5_2-7-16, P5_6-7-11, P5_7-8-11 and P5_9-10-11.

Counts by case and kind:
- P6: Q 1/1 certified, H 3/3 certified.
- P5: Q 1 timed out, H 0 of 5 reached.

Certified units (min / median / max):
- solve: 25.73 / 443.88 / 3861.36 s
- lrat-check: 12.1 / 57.25 / 110.5 s
- cake_lpr: 109.3 / 323.25 / 595.1 s (all with an 8000 MB heap)
- proof: 0.22 / 3.60 / 7.66 GB

## Resources and problems
- Largest solver RSS: 4406 MB (P6_1-11).
- No SAT, no proof rejection and no memory problem.
- Disk stayed at 20 GB free or more. The largest proof was 7.66 GB.

# C2P2 M10

Task `results/C2P2/TASK.md` at commit d266d2c3. V = M10, LIST = C2P2.tsv, j = 10, N = 42, H = 2.5.
Start 2026-10-31 06:46:52Z (epoch 1793429212), lane END = 1793437312 (08:48:32Z). Machine: 4 CPUs, 15 GB RAM (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 vendored files match `MANIFEST.sha256`. It built CaDiCaL 3.0.1 (c6073042),
  cake_lpr (a36874a8) and lrat-check (2e3b2dc with the E2 patch). Nothing was cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The base.cnf sha256 `b0061e90…d8ff1` and base.json sha256 `2476faff…b48` both match.
- Cubes: P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (`units.tsv`, idx ≡ 10 mod 42: 8 units)

| unit | case | kind | cap used (s) | status | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P8_3-11 | P8 | Q | 6000 | certified | 4717.5 | 133.0 | 704.0 | 8,840,401,506 | 4380 |
| P6_1-2-15 | P6 | H | 1758 | certified | 206.3 | 48.7 | 289.9 | 3,179,435,396 | 4375 |
| P6_1-8-10 | P6 | H | 1203 | certified | 319.9 | 54.3 | 295.7 | 3,355,270,028 | 4399 |
| P6_1-16 | P6 | Q | 522 (time left; list cap 2400) | UNKNOWN (timeout) | 515.9 | – | – | – | 4422 |
| P6_2-9-15, P6_3-8-12, P6_7-11-15 | P6 | H | – | not reached | | | | | |
| P6_9-11 | P6 | Q | – | not reached | | | | | |

Counts by case and kind:
- P8 Q: 1 certified.
- P6 H: 2 certified, 3 not reached.
- P6 Q: 1 timed out (UNKNOWN), 1 not reached.

Overall: 3 certified, 1 timed out, 4 not reached, 0 errors.

The P6_1-16 timeout ran under a reduced cap (522 s, the time left before END, against its list cap of 2400 s). It is not a timeout at the full cap.

Certified units, as (minimum / median / maximum):
- solve: 206.3 / 319.9 / 4717.5 s
- lrat-check: 48.7 / 54.3 / 133.0 s
- cake_lpr: 289.9 / 295.7 / 704.0 s (all with an 8000 MB heap, none exhausted)
- proof: 3.18 / 3.36 / 8.84 GB

## Resources and anomalies
- Largest solver RSS: 4421.5 MB (P6_1-16). cake_lpr reached about 8.2 GB RSS. There were no memory problems.
- The disk had at least 19 GB free throughout.
- No SAT, no proof rejection, no `certified: false` record, no ERROR status.
- The lane did 25-minute progress pushes. Some of those pushes first failed on ref-lock races with other machines; each one succeeded on retry. The fallback branch was not needed.

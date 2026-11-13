# C2P2 M06: shard j = 6 of N = 42 of `C2P2.tsv`, budget H = 2.5 h (task commit d266d2c3)

Start 2026-10-31 06:47:50 UTC, lane END 09:02:50 UTC (start + 2.5 h − 15 min). Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest, all 196 files match; CaDiCaL 3.0.1, cake_lpr and lrat-check (E2 patch) built from the vendored sources. Nothing was cloned or downloaded.
- Sanity checks: lrat-check and cake_lpr both reject the bad LRAT and accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. sha256 is b0061e90…d8ff1 for base.cnf and 2476faff…2b48 for base.json. Both match.
- Cubes P1..P8 from `l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`: 8 rows with idx ≡ 6 mod 42)

| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P8_2-10 | P8 | Q | 6000 | UNSAT, certified | 5505.33 | 118.3 | 659.3 | 8.95 GB | 4382 |
| P6_1-2-11 | P6 | H | 1800 (lane cap 1032) | UNSAT, certified | 324.15 | 43.7 | 282.4 | 3.27 GB | 4357 |
| P6_1-7-14 | P6 | H | 1800 (lane cap 371) | UNKNOWN (cut by END) | 367.66 | – | – | – | 4359 |
| P6_1-14-15, P6_2-9-10, P6_3-7-16 | P6 | H | 1800 | not reached | | | | | |
| P6_7-11, P6_9-10 | P6 | Q | 2400 | not reached | | | | | |

Counts:
- P8 Q: 1 certified.
- P6 H: 1 certified, 1 UNKNOWN, 3 not reached.
- P6 Q: 2 not reached.
- Total: 2 certified, 1 UNKNOWN, 5 not reached, 0 errors.

The UNKNOWN for P6_1-7-14 does not mean the unit is hard. The lane cut its cap to 371 s so that it would end before END.

Certified units (2):
- solve: minimum 324.15 s, maximum 5505.33 s.
- lrat-check: minimum 43.7 s, maximum 118.3 s.
- cake_lpr: minimum 282.4 s, maximum 659.3 s.
- proof size: minimum 3.27 GB, maximum 8.95 GB.

With only 2 units, the median is just the midpoint of these values, so it is not given separately.

Largest solver RSS: 4382 MB (P8_2-10).

There was no SAT, no proof rejection, no `certified: false` record, no ERROR and no memory problem. The lowest free disk was about 19 GB, during the 8.9 GB proof.

P8_2-10 is a first-wave quadrilateral subcase that had timed out at its full cap. In this wave it is refuted and certified: solved in 5505 s, under the 6000 s cap.

# C2P3 M23 (LIST C2P3.tsv, shard j = 23 of N = 50, H = 2.5, TASK commit 4f653319)

Machine: 4 cores, 15 GB RAM (`env.txt`). Start 2026-10-31 09:42:48 UTC, END 11:57:48 UTC; the lane finished all units at 11:45:36 UTC.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored sources. No code was cloned or downloaded. All 196 files match the manifest. It built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check with the E2 patch (2e3b2dc).
- Sanity checks: lrat-check and cake_lpr both reject the bad LRAT and both accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and base.json (2476faff…) match the expected values.
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (10: idx ≡ 23 mod 50)
| unit | case | kind | cap s | status | solve s | proof GB | lrat-check s | cake_lpr s | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P6_7-8 | P6 | Q | 6000 | certified UNSAT | 542.4 | 3.62 | 53.5 | 298.4 | 4411 |
| P6_1-14-15 | P6 | H | 1800 | certified UNSAT | 199.4 | 3.18 | 47.6 | 280.5 | 4354 |
| P6_3-9-10 | P6 | H | 1800 | certified UNSAT | 239.9 | 3.21 | 48.3 | 276.5 | 4367 |
| P6_8-11-12 | P6 | H | 1800 | certified UNSAT | 18.6 | 0.22 | 11.8 | 105.4 | 2645 |
| P5_1-6-7 | P5 | H | 1800 | certified UNSAT | 263.6 | 3.29 | 49.3 | 286.6 | 4366 |
| P5_1-12 | P5 | Q | 2400 | **UNKNOWN (timeout)** | 2375.1 | – | – | – | 4406 |
| P5_2-8-15 | P5 | H | 1800 | certified UNSAT | 477.8 | 3.66 | 56.5 | 316.0 | 4416 |
| P5_6-8-10 | P5 | H | 1346* | certified UNSAT | 23.5 | 0.21 | 11.9 | 104.4 | 2647 |
| P5_7-9-12 | P5 | H | 1204* | certified UNSAT | 86.4 | 1.37 | 25.2 | 170.9 | 3414 |
| P5_10-11 | P5 | Q | 918* | certified UNSAT | 419.6 | 3.36 | 50.7 | 304.6 | 4394 |

\* The lane shortened these caps so that 10 minutes would remain for the checks before END. Every unit that ran, ran within its effective cap.

Counts by case and kind:
- P6 Q: 1 certified.
- P6 H: 3 certified.
- P5 H: 4 certified.
- P5 Q: 1 certified (P5_10-11) and 1 timed out (P5_1-12).
- Every unit was reached, and there were no errors.

Certified units (9). Every one has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.
| | min | median | max |
|---|---|---|---|
| solve s | 18.6 | 239.9 | 542.4 |
| lrat-check s | 11.8 | 48.3 | 56.5 |
| cake_lpr s | 104.4 | 280.5 | 316.0 |
| proof bytes | 214,774,943 | 3,206,266,088 | 3,658,366,084 |

Largest solver RSS: 4416 MB (P5_2-8-15).

- No SAT was found.
- No proof was rejected.
- No record has `certified: false` or an `ERROR` status.
- There were no memory problems: peak RSS was about 4.4 GB of 15 GB, and disk peaked at about 17 GB used.

Still open from this shard: P5_1-12 (Q). It timed out at its 2400 s cap.

# C2P2 M18

Values: V = M18, LIST = C2P2.tsv, j = 18, N = 42, H = 2.5, Z = d266d2c3 (`C2P2/TASK.md`).
Machine: 4 cores, 15 GB RAM (`env.txt`). Start 06:47:34Z (epoch 1793429254). END = 1793437354 (09:02:34Z).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored `tools-src.tar.xz`. All 196 files match `MANIFEST.sha256`. The sources are CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch). Nothing was cloned or downloaded.
- Sanity checks: lrat-check and cake_lpr both rejected the bad LRAT and both accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. sha256 `b0061e90…d8ff1` for base.cnf and `2476faff…bf472b48` for base.json, both as expected.
- Cubes: P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (8 = idx ≡ 18 mod 42)
| unit | case | kind | cap | result |
|---|---|---|---|---|
| P8_9-16 | P8 | Q | 6000 | **certified** UNSAT |
| P6_1-3-10 | P6 | H | 1800 (run at 456, the time left) | **certified** UNSAT |
| P6_1-9-10 | P6 | H | 1800 | not reached |
| P6_2-3-12 | P6 | H | 1800 | not reached |
| P6_2-10-16 | P6 | H | 1800 | not reached |
| P6_3-9-13 | P6 | H | 1800 | not reached |
| P6_7-13-15 | P6 | H | 1800 | not reached |
| P6_10-11 | P6 | Q | 2400 | not reached |

Counts by case and kind:
- Certified: 2 (P8 Q: 1, P6 H: 1).
- Timed out (UNKNOWN): 0.
- Errors: 0.
- Not reached: 6 (P6 H: 5, P6 Q: 1). The lane stopped at 08:57:11Z with 322 s left, under the 15-minute floor.

Certified units, min / median / max over the 2 units:
- Solve: 349.02 / 596.3 / 5843.54 s.
- lrat-check: 55.3 / 103.5 / 151.6 s.
- cake_lpr: 318.7 / 555.1 / 791.5 s.
- Proof size: 3.36 / 6.55 / 9.73 GB (3363950113 and 9732341787 bytes).

P8_9-16 is the reflection partner of the hardest first-wave subcase. It finished at 5843.54 s, under its 6000 s cap, with a 9.73 GB proof. Both checkers accepted it: `c VERIFIED` and `s VERIFIED UNSAT`.

## Resources and anomalies
- Largest solver RSS: 4375.29 MB (P8_9-16). There were no memory problems, and peak disk use was about 21 GB of the allowance.
- No SAT result, no proof rejection and no ERROR record.

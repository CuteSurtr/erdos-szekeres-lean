# C2P3 M46

Values: V = M46, LIST = C2P3.tsv, j = 46, N = 50, H = 2.5, Z = 4f653319. Start 09:42:56 UTC (epoch 1793439776), END = 1793447876 (11:57:56 UTC).
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored sources. The manifest check passed (all 196 files match), giving CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch). Nothing was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. Both sha256 values match: base.cnf `b0061e90…d8ff1` and base.json `2476faff…b48`.
- Cubes: for P1..P8, the `l2cubes.py` output is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`: 9 units, idx ≡ 46 mod 50)

| unit | case | kind | status | solve s | RSS MB | proof GB | lrat-check s | cake_lpr s |
|---|---|---|---|---|---|---|---|---|
| P6_7-13 | P6 | Q | certified | 3610.35 | 4367 | 7.08 | 116.0 | 625.0 |
| P6_2-9-16 | P6 | H | certified | 475.63 | 4400 | 3.54 | 60.6 | 347.8 |
| P6_7-10-12 | P6 | H | certified | 80.71 | 3167 | 1.13 | 25.5 | 169.4 |
| P5_1-2-10 | P5 | H | certified | 351.14 | 4358 | 3.36 | 55.2 | 318.0 |
| P5_1-8-11 | P5 | H | certified | 370.91 | 4368 | 3.40 | 55.8 | 323.9 |
| P5_2-6-7 | P5 | H | not reached | | | | | |
| P5_2-12 | P5 | Q | not reached | | | | | |
| P5_6-11-12 | P5 | H | not reached | | | | | |
| P5_8-9-10 | P5 | H | not reached | | | | | |

Counts by case and kind:
- P6: Q 1 certified; H 2 certified.
- P5: H 2 certified and 3 not reached; Q 1 not reached.
- Totals: 5 certified, 0 timed out (UNKNOWN), 4 not reached, 0 errors.

The lane stopped at 11:43:11Z with 884 s left before END, which is under the 15-minute threshold for starting a unit.

Certified units (min / median / max):
- solve: 80.71 / 370.91 / 3610.35 s
- lrat-check: 25.5 / 55.8 / 116.0 s
- cake_lpr: 169.4 / 323.9 / 625.0 s
- proof size: 1.13 / 3.40 / 7.08 GB

All five proofs were accepted by both checkers (`c VERIFIED` and `s VERIFIED UNSAT`) and then deleted.

Largest solver RSS: 4400 MB (P6_2-9-16).

No SAT, no proof rejection and no memory or disk problem.

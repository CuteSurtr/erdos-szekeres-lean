# C2P4 M46 (LIST C2P4.tsv, j = 46, N = 50, H = 2.5, TASK commit a46b478d)

## Tools and checks
- Built with `C2P/vendor/build_tools.sh` from the vendored sources: CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc, E2 patch). No code cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…2b48`, both matching.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details in `tools.txt`.

## Units (14 total, idx ≡ 46 mod 50)
Lane start 13:03 UTC; END = 1793459797 (15:16:37 UTC). The lane stopped at 15:04 UTC with 752 s left, which is under its 15-minute margin.

| status | P5 Q | P5 H | P4 Q | P4 H | P3 Q | P3 H | total |
|---|---|---|---|---|---|---|---|
| certified (UNSAT, both checkers) | 1 | 4 | 2 | 1 | 0 | 0 | 8 |
| timed out (UNKNOWN) | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| not reached | 0 | 0 | 0 | 0 | 1 | 5 | 6 |
| errors / not certified | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

- Certified: P5_8-12, P5_1-8-12, P5_2-7-15, P5_6-8-9, P5_7-9-10, P4_1-2, P4_8-12, P4_7-8-11.
- Not reached: P3_4-15 (Q), P3_1-4-16, P3_1-9-15, P3_4-7-8, P3_5-6-11, P3_6-8-9 (H).
- The lane reduced the caps of the last three units to fit before END: P4_1-2 to 3472 s, P4_8-12 to 2109 s and P4_7-8-11 to 444 s. All three still finished UNSAT within those caps.

## Certified units (min / median / max)
- solve: 25.4 / 481.8 / 1200.4 s
- lrat-check: 13.4 / 60.6 / 75.8 s
- cake_lpr: 108.3 / 371.7 / 444.2 s
- proof size: 0.22 / 3.62 / 4.40 GB

## Other
- Largest solver RSS: 4393 MB (P5_8-12).
- No SAT, no proof rejection, no memory problem.
- Files: `out.jsonl` (all records), `lane.log.tail`, `units.tsv`, `run.sh`, `env.txt`.

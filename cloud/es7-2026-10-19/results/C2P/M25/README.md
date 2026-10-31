# C2P / M25 (LIST C2P.tsv, shard j = 25 of N = 42, H = 3.0, Z = 01909a07)

**Result: 9 units certified UNSAT, 2 timed out, 42 not reached; no SAT, no proof rejection, no error, no memory problem.**

This run replaces an earlier attempt (at fb2c59af) that stopped at step 1; its files were replaced.

## Tools and checks (`tools.txt`)

- Built with `vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json both match.
- Cubes P1..P8: all 8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Run

One lane (`run.sh`), start 03:23:15 UTC, END 06:08:15 UTC (1793426895). The lane ran 03:25:25 to 05:58:17 and stopped with 597 s left (under 15 min before END).

## Units (53: `units.tsv`)

- Certified (9): P7 H: 4, P7 Q: 1, P8 H: 3, P8 Q: 1
  P8_9-10, P8_10-11-12, P8_1-2-5, P8_2-13-14, P7_1-9-16, P7_3-12-13, P7_3-13-16, P7_1-3, P7_3-9-11
- Timed out, status UNKNOWN (2): P8_1-7 (P8 Q, cap 2400 s); P7_3-9-13 (P7 H, cap 386 s, cap shortened by the lane from 1800 s to fit END)
- Not reached (42): P1 H: 5, P1 Q: 2, P2 H: 6, P2 Q: 1, P3 H: 5, P3 Q: 1, P4 H: 6, P4 Q: 1, P5 H: 6, P5 Q: 1, P6 H: 5, P6 Q: 2, P7 H: 1
  P7_1-2-15, P6_7-8, P6_2-8-11, P6_2-7-12, P6_1-11-14, P6_3-8-14, P6_1-10, P6_2-7-13, P5_8-11-12, P5_2-3-9, P5_7-9, P5_2-9-13, P5_1-11-13, P5_6-9-13, P5_7-12-14, P4_1-3-9, P4_9-10-11, P4_2-7-11, P4_1-5-14, P4_5-13, P4_6-11-13, P4_1-10-16, P3_1-5-13, P3_1-15, P3_8-9-12, P3_4-7-10, P3_6-8-11, P3_1-14-15, P2_6-10-12, P2_4-9-12, P2_4-13-14, P2_3-7-14, P2_6-12, P2_3-10-14, P2_3-10-11, P1_6-7-8, P1_5-11, P1_3-5-8, P1_2-8-11, P1_4-8-14, P1_3-6-11, P1_2-12
- Errors / certified false: none

## Certified units: min / median / max

- solve: 25.5 / 340.87 / 941.48 s
- lrat-check: 10.6 / 45.8 / 55.3 s
- cake_lpr: 111.4 / 295.3 / 340.8 s (heap 8000 MB)
- proof size: 0.22 GB / 3.28 GB / 4.06 GB

| unit | case | kind | solve s | lrat-check s | cake_lpr s | proof | RSS MB |
|---|---|---|---|---|---|---|---|
| P8_9-10 | P8 | Q | 723.8 | 50.9 | 324.3 | 3.75 GB | 4409.82 |
| P8_10-11-12 | P8 | H | 25.5 | 10.6 | 111.4 | 0.22 GB | 2647.48 |
| P8_1-2-5 | P8 | H | 74.9 | 20.3 | 151.5 | 1.11 GB | 3155.03 |
| P8_2-13-14 | P8 | H | 247.63 | 44.2 | 290.0 | 3.19 GB | 4356.93 |
| P7_1-9-16 | P7 | H | 454.41 | 46.7 | 302.9 | 3.52 GB | 4404.39 |
| P7_3-12-13 | P7 | H | 313.96 | 45.8 | 293.0 | 3.27 GB | 4364.77 |
| P7_3-13-16 | P7 | H | 376.89 | 46.7 | 300.9 | 3.32 GB | 4362.33 |
| P7_1-3 | P7 | Q | 941.48 | 55.3 | 340.8 | 4.06 GB | 4367.3 |
| P7_3-9-11 | P7 | H | 340.87 | 45.7 | 295.3 | 3.28 GB | 4398.45 |

Largest solver RSS: 4410 MB (P8_9-10).

No SAT (`/opt/work/SAT_FOUND` never appeared), no proof rejection (every UNSAT proof: `c VERIFIED` and `s VERIFIED UNSAT`), no memory problem.

Files: env.txt, tools.txt, units.tsv, run.sh, out.jsonl, lane.log.tail, README.md.

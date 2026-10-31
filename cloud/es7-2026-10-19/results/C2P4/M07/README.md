# C2P4 M07: shard j = 7 of N = 50 of `lists/C2P4.tsv`, H = 2.5 h

Task: `results/C2P4/TASK.md` at commit a46b478d. Start 2026-10-31 13:01:30 UTC (epoch 1793451690), END = 1793459790 (start + 2.5 h − 15 min). Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only: CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (drat-trim 2e3b2dc + E2 patch). Manifest: all 196 files match.
- Sanity checks as expected: both checkers reject the bad LRAT and accept the good one, and the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…bf472b48`, both matching.
- Cubes P1..P8: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (13 rows, idx ≡ 7 mod 50; `units.tsv`)

| unit | case | kind | list cap | cap used | status | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|
| P5_1-10 | P5 | Q | 7000 | 7000 | UNSAT, certified | 4136.5 | 126.0 | 655.1 | 7,425,650,989 | 4414 |
| P4_7-10 | P4 | Q | 6000 | 2336 | UNSAT, certified | 571.3 | 58.8 | 340.8 | 3,592,118,551 | 4361 |
| P4_1-6-13 | P4 | H | 1800 | 1349 | UNSAT, certified | 549.6 | 61.9 | 362.5 | 3,717,795,208 | 4424 |
| P4_1-13-15 | P4 | H | 1800 | 359 | UNSAT, certified | 248.0 | 56.1 | 329.4 | 3,221,093,182 | 4352 |

The lane reduced the caps of the last three units to fit the time left. All three still finished UNSAT well within the reduced caps, so the reduction did not affect any of them.

**Counts**
- Certified: 4. By case and kind: P5 Q 1, P4 Q 1, P4 H 2.
- Timed out (UNKNOWN): 0.
- Errors: 0.
- Not reached: 9. The lane stopped at 15:11:14Z with 315 s left before END. By case and kind:
  - P4 H 3: P4_5-6-10, P4_5-13-14, P4_7-10-13.
  - P3 Q 1: P3_5-15.
  - P3 H 5: P3_1-5-16, P3_1-11-15, P3_4-8-11, P3_5-7-14, P3_6-10-11.

**Certified units, min / median / max**
- Solve: 248.0 / 560.5 / 4136.5 s.
- lrat-check: 56.1 / 60.3 / 126.0 s.
- cake_lpr: 329.4 / 351.7 / 655.1 s, all at heap 8000 MB.
- Proof size: 3.22 / 3.65 / 7.43 GB.

**Largest solver RSS:** 4424 MB (P4_1-6-13). cake_lpr peaked at about 8.2 GB RSS.

**Problems:** no SAT, no proof rejection and no memory or disk problem. Disk use peaked at 19 GB used, with 21 GB free.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (one record per unit), `lane.log.tail`.

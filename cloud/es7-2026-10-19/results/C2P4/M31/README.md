# C2P4 M31: shard j = 31 of N = 50 of `lists/C2P4.tsv`, H = 2.5 h, task commit a46b478d

## Tools and checks (details in `tools.txt`)
- CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch) were built with
  `C2P/vendor/build_tools.sh` from the vendored `vendor/tools-src.tar.xz`. All 196 files match the manifest.
  No code was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example printed
  `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. Both sha256 values match the expected ones
  (base.cnf `b0061e90…`, base.json `2476faff…`).
- Cubes: P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (14 rows, idx ≡ 31 mod 50; see `units.tsv`)
Lane window: 13:04:18Z to END = 1793459796 (15:16:36Z). The lane stopped at 15:06:40Z with 595 s left.

| unit | case | kind | status | cap s | solve s | lrat-check s | cake_lpr s | proof |
|---|---|---|---|---|---|---|---|---|
| P5_6-12 | P5 | Q | certified UNSAT | 6000 | 2853.4 | 102.2 | 571.5 | 6.20 GB |
| P6_8-9-11 | P6 | H | certified UNSAT | 1800 | 79.2 | 27.5 | 173.7 | 1.12 GB |
| P5_1-14-16 | P5 | H | certified UNSAT | 1800 | 252.8 | 60.5 | 315.1 | 3.20 GB |
| P5_2-12-15 | P5 | H | certified UNSAT | 1800 | 332.1 | 56.7 | 323.0 | 3.32 GB |
| P5_6-11-15 | P5 | H | certified UNSAT | 1800 | 356.1 | 56.3 | 333.0 | 3.32 GB |
| P5_8-9-13 | P5 | H | certified UNSAT | 1363 (shortened by END) | 21.9 | 14.8 | 116.8 | 0.21 GB |
| P4_2-8 | P4 | Q | UNKNOWN (timeout) | 1207 (shortened by END) | 1195.8 | – | – | – |

Not reached (7): P4_1-2-15 H, P4_1-8-15 H, P4_2-6-10 H, P4_5-8-12 H, P4_6-9-11 H, P3_1-7 Q, P3_9-10 Q.

Counts by case and kind:
- P5: Q certified 1, H certified 4 (P5 units in this shard all certified).
- P6: H certified 1.
- P4: Q timed out 1 (P4_2-8, only at the shortened cap of 1207 s, not the full 6000 s); H not reached 5.
- P3: Q not reached 2.
- Total: certified 6, timed out 1, not reached 7, errors 0.

Certified units (6), as min / median / max:
- solve: 21.85 / 292.43 / 2853.41 s
- lrat-check: 14.8 / 56.5 / 102.2 s
- cake_lpr: 116.8 / 319.05 / 571.5 s
- proof size: 214.7 MB / 3261.1 MB / 6197.7 MB

Largest solver RSS: 4479.5 MB (P5_6-12).

## Issues
- No SAT answers.
- No proof rejections: every UNSAT proof was accepted by both lrat-check and cake_lpr.
- No `certified: false` records or ERROR statuses.
- No memory or disk problems: peak RSS was 4.5 GB, and the largest proof (6.2 GB) left about 22 GB of disk free.

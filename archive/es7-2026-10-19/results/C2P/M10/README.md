# C2P / M10 (LIST C2P.tsv, shard 10 of 42, H = 3.0, Z = 01909a07)

Start 2026-10-31 03:23:10 UTC (epoch 1793416990). END = start + 3 h − 15 min = 1793426890 (06:08:10 UTC).
This attempt replaces the earlier M10 files (fb2c59af task, stopped at step 1).

**Result: 8 units certified, 1 timed out (UNKNOWN), 44 not reached. No SAT, no proof rejection, no errors.**

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (nothing cloned or downloaded):
  CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch. Manifest: all 196 files match.
- Sanity: cake_lpr example `s VERIFIED UNSAT`; both checkers reject the bad LRAT and accept the good one.
- Base CNF header `p cnf 838032 16653336`; sha256 of base.cnf and base.json match.
- Cubes P1..P8: all 8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (53 = 41 H + 11 Q + 1 cover; `units.tsv`)
| case | certified | UNKNOWN | not reached |
|---|---|---|---|
| P8 | 4 H | 1 Q (P8_1-11, 2380 s at cap 2400) | — |
| P7 | 1 cover, 2 H, 1 Q | — | 3 H |
| P6 | — | — | 5 H, 2 Q |
| P5 | — | — | 6 H, 1 Q |
| P4 | — | — | 6 H, 1 Q |
| P3 | — | — | 5 H, 2 Q |
| P2 | — | — | 6 H, 1 Q |
| P1 | — | — | 4 H, 2 Q |
| total | 8 (6 H, 1 Q, 1 cover) | 1 Q | 44 (35 H, 9 Q) |

Certified: P8_1-5-16, P8_3-9-14, P8_1-2-15, P8_2-9-14 (H); P7_cover; P7_8-9-16, P7_2-3-11 (H); P7_11-13 (Q).
The lane stopped at 05:58:02 UTC with 607 s left before END (under the 15-minute threshold).

Certified units (8), min / median / max:
- solve: 220.0 / 429.5 / 764.6 s (P7_cover slowest)
- lrat-check: 50.0 / 55.2 / 67.1 s
- cake_lpr: 284.5 / 316.0 / 400.8 s (heap 8000 MB)
- proof size: 3.16 / 3.50 / 4.54 GB (3159570487 / 3502058445 / 4541632497 bytes); all proofs deleted after checking.

## Resources and problems
- Largest solver RSS: 4473 MB (P8_3-9-14). No memory problem.
- No SAT (`/opt/work/SAT_FOUND` never appeared), no proof rejection, no `"certified": false` record, no ERROR status.
- Open from this shard: P8_1-11 (UNKNOWN at 2400 s) and the 44 units not reached.

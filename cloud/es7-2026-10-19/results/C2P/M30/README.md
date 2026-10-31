# C2P / M30 (LIST C2P.tsv, shard 30 of 42, H = 3.0, Z = 01909a07)

Restarted at 01909a07; the earlier attempt (fb2c59af) had stopped at step 1, and its files were replaced.

**Result: 10 units certified UNSAT, 1 timed out (UNKNOWN), 42 not reached, 0 errors. No SAT.**

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only. All 196 manifest files match.
  The tools are CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc) with the E2 patch.
- Sanity checks: the cake_lpr example prints `s VERIFIED UNSAT`. Both checkers reject the bad LRAT and accept the good one.
- Base CNF: the header is `p cnf 838032 16653336`, and the sha256 of both base.cnf and base.json match.
- Cubes: all 8 P{a} cube files are byte-identical to `C2P/cubes`.

## Units (53 in `units.tsv`: 43 H, 10 Q, no cover)
The lane started at 03:25:57Z and stopped at 06:01:29Z, with 418 s left before END. It will not start a unit when less than 15 minutes remain.

| case | kind | certified | UNKNOWN | not reached |
|---|---|---|---|---|
| P8 | Q | 1 (P8_11-12) | 0 | 0 |
| P8 | H | 4 | 0 | 0 |
| P7 | Q | 0 | 1 (P7_3-9, 2378.8 s at cap 2400) | 0 |
| P7 | H | 5 | 0 | 1 (P7_2-15-16) |
| P6 | H / Q | 0 | 0 | 5 / 2 |
| P5 | H / Q | 0 | 0 | 6 / 1 |
| P4 | H / Q | 0 | 0 | 5 / 1 |
| P3 | H / Q | 0 | 0 | 6 / 1 |
| P2 | H / Q | 0 | 0 | 6 / 1 |
| P1 | H / Q | 0 | 0 | 5 / 2 |

- **Certified:** P8_11-12, P8_1-4-16, P8_1-11-16, P8_1-10-11, P8_1-10-16, P7_8-10-16, P7_3-4-10, P7_2-4-14, P7_1-2-16 and P7_3-12-15.
  - For every one of them, lrat-check printed `c VERIFIED` and cake_lpr printed `s VERIFIED UNSAT`.
- Statistics over the 10 certified units (min / median / max):

  | measure | min | median | max |
  |---|---|---|---|
  | solve (s) | 211.6 | 288.2 | 655.0 (the Q unit) |
  | lrat-check (s) | 50.4 | 53.3 | 60.4 |
  | cake_lpr (s) | 290.2 | 306.6 | 341.7 |
  | proof size (GB) | 3.16 | 3.28 | 3.79 |

- **Timed out:** P7_3-9 (Q). It was not re-run.
- The two units after it ran with reduced caps, 1104 s and 534 s, because of END. Both were certified.
- **Errors or certified false:** none.

## Resources
- The largest solver RSS was 4476 MB (P8_11-12). There were no memory problems.
- No SAT and no proof rejection.

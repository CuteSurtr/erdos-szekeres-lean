# C2P / M16 (LIST C2P.tsv, shard 16 of 42, H = 3.0, Z = 01909a07)

Run of 2026-10-31, start 03:23:37Z, END 06:08:37Z. This replaces the earlier attempt (Z = fb2c59af), which stopped at step 1.

**Result: 8 units certified, 2 timed out (UNKNOWN), 43 not reached. No SAT, no errors, no proof rejection, no memory problem.**

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` (vendor tree at 01909a07). It built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc + E2 patch) from `tools-src.tar.xz`, and all 196 manifest files matched. Nothing was downloaded.
- Sanity checks: lrat-check and cake_lpr both reject the bad LRAT and both accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: the header is `p cnf 838032 16653336`, and the sha256 of base.cnf and base.json both match.
- Cubes P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (53 = 41 H + 11 Q + 1 cover; `units.tsv`, `out.jsonl`)
| case | certified | UNKNOWN (timed out) | not reached |
|---|---|---|---|
| P8 | 4 H (1-3-16, 1-2-10, 1-2-3, 3-10-15) | 1 Q (P8_1-6, cap 2400) | 0 |
| P7 | 4 H (1-2-14, 10-12-14, 1-2-3, 1-8-16) | 1 Q (P7_1-12, cap 2400) | 1 Q, 1 H |
| P6 | 0 | 0 | 1 Q, 6 H |
| P5 | 0 | 0 | 1 Q, 6 H |
| P4 | 0 | 0 | 2 Q, 5 H |
| P3 | 0 | 0 | 1 Q, 6 H |
| P2 | 0 | 0 | 2 Q, 4 H |
| P1 | 0 | 0 | 1 cover, 1 Q, 5 H |
| total | 8 H | 2 Q | 43 (1 cover, 9 Q, 33 H) |

- Both Q units ran to their full 2400 s cap and timed out. Every H unit that ran was certified.
- Certified units (min / median / max):
  - solve: 23.4 / 218.9 / 539.1 s
  - lrat-check: 12.6 / 50.2 / 57.8 s
  - cake_lpr: 106.9 / 286.0 / 323.9 s (8000 MB heap in every case)
  - proof size: 0.215 / 3.18 / 3.68 GB
- Both checkers accepted every proof (`"certified": true`). Every proof was deleted after the checks.
- The lane stopped at 05:53:59Z with 877 s left before END, under the 900 s minimum for starting a unit.
- Not reached, in file order: P7_1-11, P7_1-4-10, P6_*, P5_*, P4_*, P3_*, P2_*, P1_cover, P1_* (see `units.tsv`).

## Resources
- Largest solver RSS: 4425 MB (P7_1-8-16). Machine: 4 cores, 15 GB RAM.
- No memory problem, no SAT, no record with `"certified": false`, no ERROR status.

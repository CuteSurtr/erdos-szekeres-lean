# C2P / M28 (LIST C2P.tsv, shard 28 of 42, H = 3.0, Z = 01909a07)

This run replaces the earlier M28 attempt (Z = fb2c59af), which stopped at step 1 without running any unit.

**Result: 13 of 53 units were certified UNSAT and 40 were not reached. There was no SAT, no timeout, no error and no proof rejection.**

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built the tools from the vendored sources only:
  - CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04 (3.0.1)
  - cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa
  - drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985, with the E2 patch
- All 196 manifest hashes match.
- Sanity checks:
  - Both checkers reject the bad LRAT and accept the good one.
  - The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF:
  - The header `p cnf 838032 16653336` matches.
  - The sha256 of base.cnf (b0061e90…) and of base.json (2476faff…) both match.
- Cubes: P1..P8 are all byte-identical to `C2P/cubes`.

## Units (`units.tsv`, idx ≡ 28 mod 42)
53 units in all: 41 H, 11 Q and 1 cover.

| | P8 | P7 | P6 | P1–P5 | total |
|---|---|---|---|---|---|
| certified UNSAT | 5 H | 6 H + 1 Q | 1 H | 0 | 13 (12 H, 1 Q) |
| timed out (UNKNOWN) | 0 | 0 | 0 | 0 | 0 |
| not reached | 0 | 0 | 4 H + 2 Q | P1 6H+1Q, P2 5H+2Q, P3 5H+1Q+cover, P4 4H+2Q, P5 6H+1Q | 40 (29 H, 10 Q, 1 cover) |
| errors / certified false | 0 | 0 | 0 | 0 | 0 |

- Certified units: P8_1-5-10, P8_1-9-12, P8_2-4-14, P8_1-10-14, P8_2-3-11, P7_1-6-10, P7_11-12-13,
  P7_9-10-14, P7_10-11-14, P7_11-12 (Q), P7_2-8-11, P7_2-8-10, P6_1-5-7.
  - Each was accepted by both lrat-check (`c VERIFIED`) and cake_lpr (`s VERIFIED UNSAT`, heap 8000 MB). No unit needed the 11000 MB retry.
- Statistics over the 13 certified units (minimum / median / maximum):

  | | min | median | max |
  |---|---|---|---|
  | solve (s) | 25.0 | 328.5 | 558.4 |
  | lrat-check (s) | 13.2 | 54.6 | 58.8 |
  | cake_lpr (s) | 114.0 | 318.4 | 331.7 |
  | proof size (GB) | 0.22 | 3.33 | 3.58 |

- Lane timing:
  - It started at 03:34:48Z, with END = 06:08:17Z.
  - It stopped at 05:53:32Z with 884 s left, which is under the 900 s needed to start a unit.
  - P6_2-14 and the units after it were not reached.

## Resources and anomalies
- The largest solver RSS was 4455 MB (P7_11-12). There was no memory problem.
- There was no SAT and no proof rejection, and no proof or CNF files were kept.

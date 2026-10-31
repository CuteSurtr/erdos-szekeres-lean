# C2P2 M15: shard 15 of 42 of C2P2.tsv, H = 2.5 h (task commit d266d2c3)

## Tools and checks
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only. The manifest check passed for all 196 files. Versions: CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity checks: lrat-check and cake_lpr both rejected the bad LRAT and both accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF header: `p cnf 838032 16653336`. Both sha256 values match: base.cnf b0061e90…d8ff1 and base.json 2476faff…b48.
- Cubes P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details are in `tools.txt`. The lane command is in `run.sh`: start 1793429226, END 1793437326.

## Units (8 rows: idx ≡ 15 mod 42)
| case | kind | units | certified | timed out | not reached | errors |
|---|---|---|---|---|---|---|
| P8 | Q | 1 | 1 | 0 | 0 | 0 |
| P6 | H | 7 | 4 | 0 | 3 | 0 |
| all | | 8 | 5 | 0 | 3 | 0 |

- Certified: P8_4-12 (Q, the reflection partner/hard quadrilateral subcase, cap 6000), P6_1-3-7, P6_1-8-15, P6_2-3-9, P6_2-10-13. All are UNSAT, and both checkers accepted every proof.
- Not reached because the lane stopped at END with 326 s left: P6_3-9-10, P6_7-12-15, P6_9-12-13.

| unit | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|
| P8_4-12 | 3969.98 | 124.2 | 634.6 | 7.71 | 4367 |
| P6_1-3-7 | 229.25 | 51.1 | 308.5 | 3.22 | 4409 |
| P6_1-8-15 | 471.33 | 60.6 | 331.7 | 3.60 | 4361 |
| P6_2-3-9 | 247.05 | 51.3 | 296.7 | 3.21 | 4390 |
| P6_2-10-13 | 377.47 | 58.1 | 317.5 | 3.41 | 4459 |

Over the 5 certified units (minimum / median / maximum):
- solve: 229.25 / 377.47 / 3969.98 s
- lrat-check: 51.1 / 58.1 / 124.2 s
- cake_lpr: 296.7 / 317.5 / 634.6 s
- proof: 3.21 / 3.41 / 7.71 GB

## Problems
- Largest solver RSS: 4459 MB, on P6_2-10-13.
- No SAT, no proof rejections, no errors and no memory problems. Peak disk use was about 20 GB while the 7.7 GB proof of P8_4-12 was being checked.

# C2P2 M32: shard 32 of 42 of C2P2.tsv (H = 2.5 h, TASK.md at d266d2c3)

## Tools and checks
- I built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch) with `C2P/vendor/build_tools.sh`, from the vendored `tools-src.tar.xz`. All 196 files matched the manifest. Nothing was downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example gave `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. Both sha256 values match the task: base.cnf `b0061e90…d8ff1` and base.json `2476faff…b48`.
- Cubes P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details are in `tools.txt`.

## Units (7; idx ≡ 32 mod 42)
| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P7_8-14 | P7 | Q | 6000 | UNSAT, certified | 3438.1 | 106.8 | 565.3 | 7.65 GB | 4475 |
| P6_1-4-13 | P6 | H | 1800 | UNSAT, certified | 355.3 | 52.5 | 301.0 | 3.45 GB | 4366 |
| P6_1-11 | P6 | Q | 2400 | UNKNOWN (timed out at cap) | 2380.6 | – | – | – | 4406 |
| P6_2-7-11 | P6 | H | 1800 | not reached | | | | | |
| P6_2-13-16 | P6 | H | 1800 | not reached | | | | | |
| P6_7-8-15 | P6 | H | 1800 | not reached | | | | | |
| P6_8-10-12 | P6 | H | 1800 | not reached | | | | | |

Counts by case and kind:
- P7 Q: 1 certified.
- P6 H: 1 certified, 4 not reached.
- P6 Q: 1 timed out.
- Errors: 0.

Certified units (n = 2; with two values, the median is their mean):
| measure | min | median | max |
|---|---|---|---|
| solve s | 355.3 | 1896.7 | 3438.1 |
| lrat-check s | 52.5 | 79.7 | 106.8 |
| cake_lpr s | 301.0 | 433.2 | 565.3 |
| proof size | 3.45 GB | 5.55 GB | 7.65 GB |

- The largest solver RSS was 4475 MB (P7_8-14).
- There was no SAT, no proof rejection, no `certified: false` record and no memory problem. Free disk never went below 20 GB.
- The lane stopped at 08:50:59Z with 690 s left before END (1793437350), so it started no further unit. Units not reached: P6_2-7-11, P6_2-13-16, P6_7-8-15 and P6_8-10-12.

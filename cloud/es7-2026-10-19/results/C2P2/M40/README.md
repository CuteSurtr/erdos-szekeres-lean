# C2P2 M40 — shard j = 40 of N = 42 of `C2P2.tsv`, H = 2.5 h, TASK commit d266d2c3

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity: both checkers rejected the bad LRAT and accepted the good one; the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF `p cnf 838032 16653336`, sha256 of base.cnf `b0061e90…d8ff1` and of base.json `2476faff…bf472b48`: both match.
- Cubes P1..P8 from `l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (18 in total, from `units.tsv`; lane started 06:50Z, END 09:02:45Z)
| status | count | by case and kind |
|---|---|---|
| certified (UNSAT, both checkers accepted) | 5 | P7: 4 H + 1 Q |
| timed out (UNKNOWN) | 1 | P7_2-9 (P7 Q), stopped at 2375 s (cap 2400 s, cut slightly by the END limit) |
| not reached | 12 | P7: 2 H + 3 Q; P1: 1 cover; P6: 6 H |
| errors / certified false | 0 | — |

Not reached, exactly: P7_2-13 (Q), P7_3-8-16 (H), P7_3-12 (Q), P7_8-16 (Q), P7_9-13-14 (H), P1_cover (cover), P6_1-5-11, P6_1-12-14, P6_2-8-10, P6_3-7-8, P6_7-9-16, P6_8-11-15 (all H). The lane stopped at 08:51:23Z with 681 s left before END, below the 15-minute start threshold.

Certified units:
| unit | kind | solve s | lrat-check s | cake_lpr s | proof bytes |
|---|---|---|---|---|---|
| P7_1-2-15 | H | 221.76 | 52.4 | 303.0 | 3 166 002 334 |
| P7_1-5-10 | H | 485.98 | 59.3 | 335.8 | 3 593 405 636 |
| P7_1-8-11 | H | 405.12 | 56.2 | 323.5 | 3 459 923 111 |
| P7_1-11-12 | H | 273.86 | 52.8 | 306.4 | 3 198 453 414 |
| P7_1-14 | Q | 1405.17 | 77.5 | 436.0 | 4 782 918 694 |

min / median / max: solve 221.76 / 405.12 / 1405.17 s; lrat-check 52.4 / 56.2 / 77.5 s; cake_lpr 303.0 / 323.5 / 436.0 s; proof 3.17 / 3.46 / 4.78 GB.

## Other
- Largest solver RSS: 4422 MB (P7_2-9); no memory problem (15 GB machine).
- No SAT, no proof rejection, no errors.

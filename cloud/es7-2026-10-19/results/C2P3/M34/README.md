# C2P3 M34: shard j = 34 of N = 50 of `lists/C2P3.tsv`, H = 2.5, task commit 4f653319

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored `vendor/tools-src.tar.xz`. The manifest matched (196 files). The tools are CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc + E2 patch).
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…d8ff1) and of base.json (2476faff…2b48) matched.
- Cubes P1..P8: each byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Run
One lane (`run.sh`), started 09:45:34Z with END = 1793447865 (11:57:45Z). The lane finished at 11:52:34Z ("stop: 310 s left").

## Units (`units.tsv`, 10 rows)
| idx | unit | case | kind | cap | result | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|
| 34 | P6_2-9 | P6 | Q | 6000 | UNSAT, certified | 3948.5 | 103.8 | 628.3 | 7,414,059,903 | 4413 |
| 84 | P6_10-11 | P6 | Q | 4800 (lane cap 2589) | UNSAT, certified | 609.4 | 50.8 | 302.1 | 3,507,686,136 | 4371 |
| 134 | P6_2-7-15 | P6 | H | 1800 (1609) | UNSAT, certified | 563.5 | 53.4 | 323.2 | 3,663,847,890 | 4368 |
| 184 | P6_7-8-12 | P6 | H | 1800 (653) | UNSAT, certified | 25.0 | 12.0 | 108.1 | 214,319,132 | 2647 |
| 234 | P6_9-11-13 | P6 | H | 1800 (506) | UNSAT, certified | 25.4 | 11.5 | 104.0 | 216,743,362 | 2642 |
| 284 | P5_1-7-8 | P5 | H | 1800 (363) | UNSAT, certified | 305.7 | 45.6 | 289.6 | 3,261,623,707 | 4404 |
| 334 | P5_1-14-16 | P5 | H | 1800 | not reached | | | | | |
| 384 | P5_2-10-11 | P5 | H | 1800 | not reached | | | | | |
| 434 | P5_6-9-13 | P5 | H | 1800 | not reached | | | | | |
| 484 | P5_7-11-12 | P5 | H | 1800 | not reached | | | | | |

Counts by case and kind:
- P6 Q: 2 certified.
- P6 H: 3 certified.
- P5 H: 1 certified and 4 not reached.
- Overall: no unit timed out (UNKNOWN) and none ended in an error.

Certified units (6), as min / median / max:
- solve: 25.0 / 434.6 / 3948.5 s
- lrat-check: 11.5 / 48.2 / 103.8 s
- cake_lpr: 104.0 / 295.9 / 628.3 s
- proof size: 0.21 / 3.38 / 7.41 GB

The largest solver RSS was 4413 MB (P6_2-9). There were no SAT answers, no proof rejections and no memory problems: both checkers accepted every proof, and every record has `"certified": true`.

# C2P3 M10: shard j = 10 of N = 50 of `lists/C2P3.tsv`, H = 2.5 h (TASK commit 4f653319)

Lane start 2026-10-31 09:44:48Z. END is 1793447861 (11:57:41Z), which is the start time 09:42:41Z + 2.5 h − 15 min. The lane finished at 11:47:45Z.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 manifest files match. It built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch) from the vendored sources. Nothing was cloned or downloaded.
- Sanity checks: lrat-check and cake_lpr both reject the bad LRAT and both accept the good one. The cake_lpr example gives `s VERIFIED UNSAT`.
- Base CNF: the header is `p cnf 838032 16653336`, and the sha256 of base.cnf (b0061e90…) and base.json (2476faff…) match the expected values.
- Cubes: P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (10 in shard)
| unit | case | kind | status | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|
| P7_9-13 | P7 | Q | UNSAT, certified | 1984.4 | 71.2 | 432.6 | 5087438944 | 4360 |
| P6_1-7-10 | P6 | H | UNSAT, certified | 470.8 | 49.2 | 323.5 | 3452179019 | 4361 |
| P6_3-7-8 | P6 | H | UNSAT, certified | 252.4 | 53.5 | 292.4 | 3216009663 | 4408 |
| P6_7-13-15 | P6 | H | UNSAT, certified | 279.1 | 54.2 | 378.7 | 3166842517 | 4358 |
| P5_1-3-12 | P5 | H | UNSAT, certified | 390.7 | 49.1 | 314.7 | 3367305196 | 4365 |
| P5_1-10 | P5 | Q | UNKNOWN (timed out at cap 1892 s, cut by END) | 1874.5 | – | – | – | 4414 |
| P5_2-7-11, P5_2-16, P5_6-15, P5_8-12 | P5 | H, Q, Q, Q | not reached | | | | | |

Counts by case and kind:
- P7 Q: 1 certified.
- P6 H: 3 certified.
- P5 H: 1 certified, 1 not reached.
- P5 Q: 1 UNKNOWN, 3 not reached.
- Totals: 5 certified, 1 UNKNOWN, 4 not reached, 0 errors.

Certified units (5), as min / median / max:
- solve: 252.4 / 390.7 / 1984.4 s
- lrat-check: 49.1 / 53.5 / 71.2 s
- cake_lpr: 292.4 / 323.5 / 432.6 s (heap 8000 MB every time)
- proof size: 3.17 / 3.37 / 5.09 GB

Largest solver RSS: 4414 MB (P5_1-10).

There were no SAT answers, no proof rejections, no `certified: false` or ERROR records, and no memory or disk problems. The lowest available disk during the run was 23 GB.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl`, `lane.log.tail`.

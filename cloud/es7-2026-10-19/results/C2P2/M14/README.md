# C2P2 M14

Machine M14. TASK `results/C2P2/TASK.md` at commit d266d2c3. Values: LIST = C2P2.tsv, j = 14, N = 42, H = 2.5.
Start time: 2026-10-31 06:47:45Z (epoch 1793429265). END = 1793437365 (09:02:45Z).
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored sources. All 196 manifest files matched.
  - CaDiCaL c6073042 (3.0.1)
  - cake_lpr a36874a8
  - lrat-check 2e3b2dc with the E2 patch
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and of base.json (2476faff…) both match the expected values.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, rows with idx ≡ 14 mod 42): 8 units
| idx | unit | case | kind | cap | result | solve s | RSS MB | proof GB | lrat-check s | cake_lpr s |
|---|---|---|---|---|---|---|---|---|---|---|
| 14 | P8_4-11 | P8 | Q | 6000 | **certified** UNSAT | 3432.6 | 4366 | 7.16 | 117.1 | 612.2 |
| 56 | P6_1-3-5 | P6 | H | 1800 | **certified** UNSAT | 80.1 | 3215 | 1.20 | 26.2 | 171.1 |
| 98 | P6_1-8-14 | P6 | H | 1800 | **certified** UNSAT | 553.0 | 4359 | 3.62 | 59.3 | 343.9 |
| 140 | P6_2-3-8 | P6 | H | 1800 | **certified** UNSAT | 219.6 | 4400 | 3.19 | 52.1 | 304.4 |
| 182 | P6_2-10-12 | P6 | H | 1800 (run with 1298) | **certified** UNSAT | 308.6 | 4371 | 3.29 | 55.7 | 311.2 |
| 224 | P6_3-9 | P6 | Q | 2400 (run with 612) | UNKNOWN (timed out at its END-shortened cap) | 606.2 | 4379 | – | – | – |
| 266 | P6_7-12-14 | P6 | H | 1800 | not reached | | | | | |
| 308 | P6_9-12 | P6 | Q | 2400 | not reached | | | | | |

The lane shortened the caps of P6_2-10-12 and P6_3-9 so that the checks would finish before END. P6_3-9 timed out only at that shortened cap of 612 s. Its full cap is 2400 s.

Counts by case and kind:
- P8 Q: 1 certified.
- P6 H: 4 certified, 1 not reached (P6_7-12-14).
- P6 Q: 1 timed out (P6_3-9, at 612 s), 1 not reached (P6_9-12).
- Total: 5 certified, 1 UNKNOWN, 2 not reached, 0 errors.

Certified units (5), as min / median / max:
- solve: 80.1 / 308.6 / 3432.6 s
- lrat-check: 26.2 / 55.7 / 117.1 s
- cake_lpr: 171.1 / 311.2 / 612.2 s
- proof size: 1.20 / 3.29 / 7.16 GB

P8_4-11 is one of the first-wave quadrilateral timeouts. It is now certified, solved in 3433 s under the 6000 s cap.

## Other
- Largest solver RSS: 4400 MB (P6_2-3-8). cake_lpr ran with an 8000 MB heap, with about 8.2 GB RSS.
- No memory problems.
- No SAT.
- No proof rejections, no `certified: false` records and no ERROR statuses.
- Files: `out.jsonl` (6 records) and `lane.log.tail`.

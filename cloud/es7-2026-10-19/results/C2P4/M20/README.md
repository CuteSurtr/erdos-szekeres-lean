# C2P4 M20

Task `results/C2P4/TASK.md` (commit a46b478d) with V = M20, LIST = C2P4.tsv, j = 20, N = 50, H = 2.5. One lane, started 2026-10-31 13:04 UTC (session start 13:01:32 UTC, epoch 1793451692), END = 1793459792 (15:16:32 UTC). The lane stopped at 15:06:37 UTC ("stop: 594 s left").

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest, all 196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch), all built from the vendored sources. Nothing was cloned or downloaded.
- cake_lpr example: `s VERIFIED UNSAT`. Sanity: both checkers reject the bad LRAT and accept the good one.
- Base CNF: header `p cnf 838032 16653336`. base.cnf sha256 `b0061e90…d8ff1` and base.json sha256 `2476faff…2b48`, both as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (`units.tsv`: 19 rows, idx ≡ 20 mod 50)
| status | count | by case / kind |
|---|---|---|
| certified (UNSAT, both checkers accept) | 6 | P5: 1 Q + 4 H; P6: 1 H |
| timed out (UNKNOWN) | 1 | P4_1-9 (P4, Q). Its cap was cut by the time left: 2124 s, not 6000 s. It ran 2103 s. |
| not reached | 12 | P4: 6 H (P4_1-2-3, P4_1-7-12, P4_2-5-9, P4_5-7-9, P4_6-7-13, P4_8-9-13); P3: 1 Q (P3_6-14) + 5 H (P3_1-6-14, P3_1-13-16, P3_4-9-12, P3_5-8-15, P3_7-8-10) |
| errors / not certified | 0 | |

Certified units:
| unit | kind | solve s | lrat-check s | cake_lpr s | proof bytes |
|---|---|---|---|---|---|
| P5_1-15 | Q | 1458.5 | 78.6 | 456.1 | 4,762,850,175 |
| P6_2-4-8 | H | 270.0 | 53.9 | 317.1 | 3,226,157,810 |
| P5_1-9-15 | H | 443.4 | 62.0 | 360.3 | 3,534,040,370 |
| P5_2-8-14 | H | 630.9 | 66.0 | 383.9 | 3,709,339,151 |
| P5_6-9-11 | H | 28.0 | 13.9 | 123.2 | 216,714,279 |
| P5_7-10-13 | H | 118.4 | 35.1 | 220.4 | 1,592,946,191 |

Min / median / max over the 6 certified units:
- solve: 28.0 / 356.7 / 1458.5 s
- lrat-check: 13.9 / 58.0 / 78.6 s
- cake_lpr: 123.2 / 338.7 / 456.1 s (all at heap 8000 MB)
- proof size: 0.22 / 3.38 / 4.76 GB

## Other
- Largest solver RSS: 4406 MB (P5_1-15). There were no memory problems.
- No SAT, no proof rejections and no ERROR records.
- Files: `out.jsonl` (7 records) and `lane.log.tail`.

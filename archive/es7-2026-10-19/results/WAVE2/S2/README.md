# WAVE2 / S2: hull cases of mirror sub-case (ii) taken from the back of W35's list

Run 2026-10-20, 10:28 to 12:25 UTC, on one 4-core VM (`env.txt`). Tools are in `tools.txt`, and F was regenerated with sha256 69c1dc8f…ffff932d.
Driver: `close_march.py`, a byte-identical copy of F2's. The review against W19 is in `driver.diff`.

## Summary
- **SAT results: none.** No cake_lpr rejection: every UNSAT proof printed `s VERIFIED UNSAT`, so no record has status UNSAT_UNCHECKED.
- **23 of my 29 cases are closed here**: 14 by the whole-case attempt (CaDiCaL with a 120 s cap, LRAT proof checked by cake_lpr) and 9 by `close_march.py --depth 7 --timeout 300 --split-depth 6 --jobs 4`.
- **6 were skipped because W35 had already closed them**: U_L4-8, U_L4-5 and U3-10_L at the start, and U4-10_L, U4-7_L and U3-13_L at 12:12, after W35's final commit at 10:36. The records are in `skipped.jsonl`.
- **Cases started but not closed: none. Cases not reached: none.**
- U4-12_L had been started by W35 (64 leaves, 52 open), so I moved it to the end. I then ran it in full from W35's top file: my own march_cu run gave the same sha, 90cfebac…. It is closed here, independently of W35.
- Each closed case's `leaves.icnf` also passes `Haudit/scripts/mycover.py`, which checks the cover with CaDiCaL and cake_lpr and prints `s COVERED (cake_lpr VERIFIED)`. In every case `open.icnf` is empty.

## Per case
Times are wall-clock seconds summed over leaves: the CaDiCaL solve, then the cake_lpr check. "Prefetched" means the runner (or I, by hand) ran `march_cu CASE.cnf -d 7 -o top.icnf` on the same case CNF ahead of time and passed it with `--top`. Its sha256 is in the `top_sha256` record of leaves.jsonl.

| case | result | method | verified leaves | open | splits | solve s (sum) | check s (sum) | top march s |
|---|---|---|---|---|---|---|---|---|
| U6_L16 | CLOSED | whole case | 1 | 0 | 0 | 52 | 18 |  |
| U6_L10 | CLOSED | whole case | 1 | 0 | 0 | 80 | 17 |  |
| U6_L5 | CLOSED | close_march d7 | 107 | 0 | 0 | 564 | 312 | 227.4 |
| U5_L13 | CLOSED | whole case | 1 | 0 | 0 | 92 | 12 |  |
| U5_L7 | CLOSED | close_march d7 | 112 | 0 | 0 | 609 | 332 | prefetched |
| U4_L16 | CLOSED | whole case | 1 | 0 | 0 | 113 | 23 |  |
| U4_L12 | CLOSED | close_march d7 | 107 | 0 | 0 | 424 | 313 | prefetched |
| U4_L7 | CLOSED | close_march d7 | 112 | 0 | 0 | 1117 | 489 | prefetched |
| U3_L16 | CLOSED | close_march d7 | 113 | 0 | 0 | 1251 | 385 | prefetched |
| U3_L12 | CLOSED | close_march d7 | 119 | 0 | 0 | 1195 | 499 | prefetched |
| U3_L8 | CLOSED | close_march d7 | 127 | 0 | 0 | 2240 | 561 | prefetched |
| U3_L4 | CLOSED | close_march d7 | 254 | 0 | 2 | 5939 | 904 | prefetched |
| U6-14_L | CLOSED | whole case | 1 | 0 | 0 | 16 | 10 |  |
| U6-9_L | CLOSED | whole case | 1 | 0 | 0 | 19 | 8 |  |
| U5-16_L | CLOSED | whole case | 1 | 0 | 0 | 26 | 9 |  |
| U5-14_L | CLOSED | whole case | 1 | 0 | 0 | 27 | 8 |  |
| U5-12_L | CLOSED | whole case | 1 | 0 | 0 | 21 | 7 |  |
| U5-10_L | CLOSED | whole case | 1 | 0 | 0 | 26 | 4 |  |
| U_L5-8 | CLOSED | whole case | 1 | 0 | 0 | 17 | 5 |  |
| U5-7_L | CLOSED | whole case | 1 | 0 | 0 | 29 | 8 |  |
| U_L4-15 | CLOSED | whole case | 1 | 0 | 0 | 29 | 8 |  |
| U4-14_L | CLOSED | whole case | 1 | 0 | 0 | 59 | 13 |  |
| U4-12_L | CLOSED | close_march d7 | 116 | 0 | 0 | 233 | 305 | prefetched |
| U4-10_L | skipped: closed elsewhere (WAVE1/W35/U4-10_L) | | | | | | | |
| U_L4-8 | skipped: closed elsewhere (WAVE1/W35/U_L4-8) | | | | | | | |
| U4-7_L | skipped: closed elsewhere (WAVE1/W35/U4-7_L) | | | | | | | |
| U_L4-5 | skipped: closed elsewhere (WAVE1/W35/U_L4-5) | | | | | | | |
| U3-13_L | skipped: closed elsewhere (WAVE1/W35/U3-13_L) | | | | | | | |
| U3-10_L | skipped: closed elsewhere (WAVE1/W35/U3-10_L) | | | | | | | |

The whole-case attempt timed out at 120 s for the 8 cases that then went to the driver: U6_L5, U5_L7, U4_L12, U4_L7, U3_L16, U3_L12, U3_L8 and U3_L4. All 22 attempts are in `whole_attempts.jsonl`.

## Files
- `<case>/leaves.icnf`: the verified leaves, one per line as `a l1 .. lk 0`. A leaf is the top cube plus any split sub-cubes, relative to the case CNF (F plus the case units). A case closed whole is the single line `a 0`.
- `<case>/open.icnf`: the open cubes. It is empty for every case.
- `<case>/top.icnf`: the top cubes, for driver cases.
- `<case>/leaves.jsonl`: the first record holds `case` and `case_sha256`, and each case sha was checked against `Mii-S/cases.jsonl` before the run.

## Notes
- At 12:12 I stopped my sequential runner so that U4-12_L could use the 3 cores sitting idle while a U3_L4 split ran. The U3_L4 driver kept running. One U3_L4 sub-cube was then left with no record, and `open.icnf` listed it, as it should. I re-ran the driver on U3_L4, which resumes from leaves.jsonl with a frontier of 1, and it closed that cube (20.6 s, `s VERIFIED UNSAT`). The `"resume"` record at 12:19:32 marks this.
- The scratch directories (`tempfile.mkdtemp` under /opt/work/tmp) were removed. No CNF or LRAT file was committed.

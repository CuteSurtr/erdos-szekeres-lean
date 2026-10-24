# WAVE4 H38: U_L7 cubes from tasks/H38.json (commit 4bfd8e7)

- Case: U_L7 (U = "", L = "7"), CASE.cnf sha256 c6d1c840d97921426e0f2d1d34213fb94293cc1783296ec2357d7883b804f099 (matches cases.jsonl).
- Cubes given: 196 (`U_L7/top.icnf`, sha256 d9c82f1f31961f6e016b1d44c6060631651d9da57cf6a00afda2c401c4662784).
- Verified leaves: 369. Each has CaDiCaL exit 20 and cake_lpr printed `s VERIFIED UNSAT` (`U_L7/leaves.icnf`).
- Cubes split: 3 (each reached the 300 s cap). Two were given cubes and one was a sub-cube. march_cu -d 6 gave 55 (7 refuted), 64 (0 refuted) and 57 (5 refuted) sub-cubes.
- Cubes still open: 0 (`U_L7/open.icnf` is empty; the driver printed `open 0`).
- Cover: every one of the 196 given cubes is covered by the verified leaves. The driver's frontier is empty, and a separate check also confirmed it: a recursive split check of each top cube against leaves.icnf, with every line checked to start with `a ` and end in ` 0`.
- Solve time over the 369 verified leaves: sum 7259.4 s, median 8.39 s, max 234.74 s. The 3 split cubes add 3 x 300 s.
- cake_lpr check time: sum 1588.6 s, median 2.76 s, max 23.19 s. No heap retries were needed.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none. TIMEOUT records: none.
- Run: started 13:42:45 UTC with --hours 2.23, finished at about 14:58 UTC with one session and no resume. Tools are in tools.txt and the driver check is in driver.diff.

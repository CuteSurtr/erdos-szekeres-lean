# WAVE4 H06: case U_L2

- Case U_L2 (U = none, L = 2). Case CNF built with hullsplit.py; sha256 1d26b947…aaa53, which matches cases.jsonl. F regenerated with sha256 69c1dc8f…ffff932d.
- Cubes given: 325, from tasks/H06.json at e0f250b. top.icnf has 325 lines in file order, sha256 714450ca…ae1ef5f.
- Driver: close_march.py, a byte-for-byte copy of WAVE2/F2 (see driver.diff). Run with --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.214. It started at 12:53:32 UTC and finished at about 13:38 UTC, printing `open 0`.
- Verified leaves: 388. cake_lpr printed `s VERIFIED UNSAT` for every one. leaves.icnf has 388 distinct lines, all well formed.
  - 324 given cubes were closed directly.
  - 1 given cube timed out at 300 s and was split by march_cu into 64 sub-cubes (0 refuted). All 64 were closed.
- Cubes split: 1. Cubes still open: 0 (open.icnf is empty).
- Every given cube is now covered. I checked this independently: each of the 325 top cubes is either a verified leaf, or a SPLIT record whose sub-cubes are all verified leaves.
- No SAT result. No cake_lpr rejection. No UNSAT_UNCHECKED record. No TIMEOUT records after the deadline.
- Times over the 388 verified leaves:
  - CaDiCaL solve: sum 7096.7 s, median 12.61 s, max 250.09 s.
  - cake_lpr check: sum 2006.1 s, median 4.57 s, max 26.88 s.
  - Child CPU in total: 35664 s.
- Tools: see tools.txt. Environment: see env.txt.

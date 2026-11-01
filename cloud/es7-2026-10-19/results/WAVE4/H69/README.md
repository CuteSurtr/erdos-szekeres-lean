# WAVE4 H69: U_L7 mop-up 4

Case U_L7 (U = [], L = [7]); case CNF sha256 c6d1c840…b804f099 (matches cases.jsonl); F sha256 69c1dc8f…ffff932d.
Task list `results/WAVE4/tasks/H69.json` (commit 1d3a72c): 125 cubes, written in order to `U_L7/top.icnf` (125 lines, sha256 07378d25…cccb379e).
Driver: byte-for-byte copy of `results/WAVE2/F2/close_march.py` (see `driver.diff`), run with
`--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 1.203` from 15:07:50 UTC; it ended at 15:31 UTC with `open 0`.
Tools: see `tools.txt` (CaDiCaL 3.0.1 c6073042, march_cu 705b60c6 with -fcommon, cake_lpr a36874a8; bundled example gives `s VERIFIED UNSAT`).

Result:
- No SAT result. No cake_lpr rejection, no UNSAT_UNCHECKED record.
- Verified leaves: 176 (every one has cake_lpr `s VERIFIED UNSAT`): 124 given cubes closed directly, and 52 sub-cubes of the one split cube.
- Cubes split: 1 (timed out at 300 s; march_cu -d 6 gave 52 cubes, 4 refuted, in 420.9 s; all 52 closed).
- Cubes still open: 0 (`U_L7/open.icnf` is empty).
- Every given cube is covered by the leaves in `U_L7/leaves.icnf`: checked by a branching cover check of each of the 125 top cubes against the 176 leaves (0 uncovered; every line of both files ends in ` 0`).
- Solve time over the 176 UNSAT leaves: sum 2125.6 s, median 4.89 s, max 177.3 s (plus 300.0 s for the split cube's timeout).
- Check time (cake_lpr): sum 737.8 s, median 2.79 s, max 23.6 s.

Files: `U_L7/{top,leaves,open}.icnf`, `U_L7/leaves.jsonl` (first record names case and case_sha256), `env.txt`, `tools.txt`, `driver.diff`, `close_march.py`.

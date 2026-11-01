# WAVE4 H63: case U3_L

Task file `results/WAVE4/tasks/H63.json` (committed at 1d3a72c): case **U3_L** (U=[3], L=[]), 205 open cubes. Time budget: 1.5 h.

- F.cnf was regenerated; its sha256 is 69c1dc8f…ffff932d. The case CNF was built with `hullsplit.py case F.cnf 3 ""`. Its sha256 is 7ab00d97…7f0e01fab79ee0f823, which matches cases.jsonl.
- `U3_L/top.icnf` has 205 lines, one for each cube in the task list, in the same order. Its sha256 is 4471f162…bdf1722698.
- Tools and their commits are listed in `tools.txt`. `close_march.py` is a byte-for-byte copy of `results/WAVE2/F2/close_march.py`; `driver.diff` records the checks made on it.
- The driver ran from 15:02 to about 15:48 UTC with 4 jobs, a 300 s timeout and split depth 6, writing to `/opt/work/out/U3_L` (outside the git checkout). It ended with `open 0`.

## Result
- Cubes given: 205.
- Verified leaves: **261**. Every one printed `s VERIFIED UNSAT` from cake_lpr.
  - 204 top cubes were closed directly.
  - 1 top cube timed out at 300 s and was split by march_cu at depth 6 into 57 sub-cubes (5 of them refuted by march). All 57 were closed.
- Cubes split: 1. Cubes still open: **0**. `open.icnf` is empty.
- Coverage: every given cube is covered by the leaves in `U3_L/leaves.icnf`. I checked this with a separate case-splitting check over the leaves for each of the 205 top cubes: 0 were uncovered. Every line of leaves.icnf ends in ` 0`.
- Solve time over the 261 leaves: sum 5458.3 s, median 19.1 s, max 245.4 s. The split cube also used 300.0 s of solving and 327.3 s of march_cu.
- cake_lpr check time: sum 1325.4 s, median 4.0 s, max 21.0 s.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.

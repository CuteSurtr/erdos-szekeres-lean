# WAVE4 H70: U_L7

- No SAT result. No cake_lpr rejection, no UNSAT_UNCHECKED record.
- Case U_L7 (U = none, L = 7). The case CNF was built with `hullsplit.py case F.cnf "" "7"`. Its sha256 c6d1c840...f099 matches cases.jsonl, and F's sha256 69c1dc8f...932d matches too.
- Cubes given: 125 (`tasks/H70.json`, commit 1d3a72c). `top.icnf` has 125 lines, in the file's order.
- Driver: `close_march.py`, a byte-for-byte copy of WAVE2/F2 (see driver.diff), run with `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 1.226`. It started 15:06:37 UTC and finished all cubes at 15:26 UTC.
- Verified leaves: 188, each with cake_lpr printing `s VERIFIED UNSAT`. 124 are top cubes solved directly, and 64 are the children of the one split.
- Cubes split: 1. That top cube timed out at 300 s, and march_cu split it into 64 subcubes, 0 of them refuted. I checked that the 64 subcubes cover the parent.
- Cubes still open: 0 (`open.icnf` is empty).
- Every given cube is now covered by these leaves: 124 directly (each has a leaf that is a subset of it), and the split cube through its 64 children, each of which has a verified leaf.
- Times over the 188 leaves:

  | | sum | median | max |
  |---|---|---|---|
  | solve | 2252.9 s | 4.93 s | 242.04 s |
  | check | 727.2 s | 2.67 s | 25.71 s |
  | solve + check | 2980.1 s | 8.62 s | 267.75 s |

  The split cube also used 300 s of solving before the timeout, plus 204 s for march.
- Files: `U_L7/{top.icnf, leaves.icnf, open.icnf, leaves.jsonl}`, copied as they were from the driver's output directory (/opt/work/out/U_L7).

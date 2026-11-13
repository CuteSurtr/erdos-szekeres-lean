# WAVE4 H58: case U_L7

Task: `results/WAVE4/tasks/H58.json` (committed at 94cc404), case U_L7 (U = none, L = 7), 95 cubes (lengths 30-31). Time budget 1.5 h. The driver started at 14:43 UTC and finished at about 14:59 UTC.

- Case CNF sha256 c6d1c840d97921426e0f2d1d34213fb94293cc1783296ec2357d7883b804f099 matches cases.jsonl. F sha256 matches 69c1dc8f…932d.
- Driver: byte-for-byte copy of `results/WAVE2/F2/close_march.py` (see `driver.diff`). Tools are listed in `tools.txt`.
- Run: `--top top.icnf --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 1.223`.

Result:
- Cubes given: 95.
- Verified leaves (cake_lpr `s VERIFIED UNSAT`): 149. That is 94 of the given cubes solved directly, plus the 55 sub-cubes of 1 split cube.
- Cubes split: 1 (a length-31 cube timed out at 300 s; march_cu -d 6 gave 55 cubes, including 5 refuted. All 55 are closed as leaves of lengths 35-37).
- Cubes still open: 0 (`U_L7/open.icnf` is empty).
- Every given cube is covered by these leaves. Checked: each top cube has a verified leaf that is a subset of it, or it is the split cube and all of its 55 sub-cubes have one. The split's completeness rests on march_cu and is re-checked by the cover check.
- No SAT result, no cake_lpr rejection, and no UNSAT_UNCHECKED record.
- Solve time over the 149 leaves: sum 1623.5 s, median 3.94 s, max 116.72 s (with the 300 s split cube included: 1923.5 s over 150 runs).
- cake_lpr check time over the 149 leaves: sum 585.1 s, median 2.55 s, max 14.42 s.

Files in `U_L7/`: top.icnf (the 95 given cubes), leaves.icnf, open.icnf and leaves.jsonl, copied from the driver output after it ended.

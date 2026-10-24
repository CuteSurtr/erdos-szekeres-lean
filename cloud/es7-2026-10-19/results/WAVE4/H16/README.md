# WAVE4 H16: case U_L2

Task file `results/WAVE4/tasks/H16.json` (at e0f250b): case **U_L2**, **324** cubes given. The budget was 2.5 h, and the driver started at 12:55:06Z and finished at about 13:45Z.

- The case CNF came from hullsplit.py (`case F.cnf "" "2"`). Its sha256 1d26b947...aaa53 matches cases.jsonl, and F's sha256 69c1dc8f...932d matches too.
- `top.icnf` has 324 lines, one per given cube in the file's order (top_sha256 6930ad71...4fc24).
- The driver is a byte-for-byte copy of WAVE2/F2/close_march.py (see driver.diff). It ran with `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.224`, its output directory was /opt/work/out/U_L2 (outside the checkout) and WORK was /opt/work/tmp. The copy was executed from /opt/work/close_march.py, an identical copy, so that it sat outside the checkout.

## Result
- **No SAT result. No cake_lpr rejection. No UNSAT_UNCHECKED record.**
- **Verified leaves:** 387. Each one has cake_lpr output `s VERIFIED UNSAT`, and `leaves.icnf` has 387 lines.
  - 323 of them are given cubes, solved directly.
  - The other 64 are the sub-cubes of the one split cube.
- **Cubes split:** 1. This is given cube index 303 (0-based). It timed out at 300 s, and march_cu at depth 6 gave 64 cubes, 0 of them refuted, in 93.9 s. All 64 were then verified.
- **Cubes still open:** 0, and `open.icnf` is empty.
- **Coverage:** every given cube is covered by the leaves in `leaves.icnf`. I checked this independently from `leaves.jsonl`: each top cube is either a leaf or a SPLIT whose sub-cubes are all leaves. I also checked that every line ends in ` 0`.
- **Time over the 387 verified leaves (wall seconds):**

| Measure | Sum | Median | Max |
|---|---|---|---|
| CaDiCaL solve | 7443.2 | 12.08 | 155.51 |
| cake_lpr check | 2032.3 | 4.11 | 26.67 |
| Solve + check | 9475.5 | 16.93 | 178.66 |

  The one timed-out solve took 300.02 s and is not counted in these totals.

Files: `U_L2/{top.icnf, leaves.icnf, open.icnf, leaves.jsonl}`, plus env.txt, tools.txt, driver.diff and close_march.py.

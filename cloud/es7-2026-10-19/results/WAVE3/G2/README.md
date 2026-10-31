# WAVE3 G2: open cubes of U_L2

Task: `results/WAVE3/tasks/G2.json` (commit 9a26cc2), with 741 open cubes of case U_L2 only.
Run window: 10:58:24 to about 13:40 UTC on 4 cores (`env.txt`). Tools and hashes are in
`tools.txt`. The driver is F2's `close_march.py`, unchanged; the checks are in `driver.diff`.
Run options: `--name U_L2 --top <741 cubes in file order> --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.68`.
F sha256 69c1dc8f…932d OK. The U_L2 case CNF (`hullsplit.py case F "" "2"`) has sha256
1d26b947…aa53, which equals the cnf_sha256 in cases.jsonl.

| case | cubes given | verified leaves | given cubes fully covered | given cubes not covered | cubes still open (open.icnf) | closed? |
|---|---|---|---|---|---|---|
| U_L2 | 741 | 955 | 707 | 34 | 2115 | **no** |

- Verified leaves: 705 given cubes were closed directly. The other 250 leaves are sub-cubes of
  split cubes. Each leaf line in `leaves.icnf` was counted only after cake_lpr printed exactly
  `s VERIFIED UNSAT` on CaDiCaL's LRAT proof. There are 955 lines, all distinct.
- Splits: 37 cubes timed out at 300 s and were split by march_cu at depth 6, giving 64 sub-cubes
  each. 36 of them are given cubes and 1 is a sub-cube. Two of the split given cubes are now
  fully covered by their sub-leaves. The other 34 given cubes still have open sub-cubes, 2115 in
  total, listed in `open.icnf`.
- `open.icnf` is exactly the frontier of the 741 given cubes. I rebuilt it independently from
  `leaves.jsonl` and it matches. Every line ends in ` 0`.
- SAT results: **none**. cake_lpr rejections: **none** (0 UNSAT_UNCHECKED).
- Time: 28,926 s total CaDiCaL wall time and 3,335 s total cake_lpr wall time, summed over jobs.
- Files: `U_L2/top.icnf` (the 741 given cubes), `U_L2/leaves.icnf`, `U_L2/leaves.jsonl` (the
  first record holds case and case_sha256), `U_L2/open.icnf`.
- Note: one progress push at 12:39 was refused by a ref-lock race and went to `claude/es7-w3-g2`.
  It was then pushed to es7-cloud at once; es7-cloud holds everything.

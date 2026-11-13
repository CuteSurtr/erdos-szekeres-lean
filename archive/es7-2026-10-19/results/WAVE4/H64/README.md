# WAVE4 H64: U3_L

- Case: U3_L (CASE.cnf sha256 7ab00d97d5047e0003bd8d254560dc8464d880d7165c6d7f0e01fab79ee0f823, matches cases.jsonl).
- Cubes given: 204 (`results/WAVE4/tasks/H64.json` at 1d3a72c; `U3_L/top.icnf`, top_sha256 cac04502...).
- Verified leaves: 204. Every leaf has cake_lpr output exactly `s VERIFIED UNSAT`.
- Cubes split: 0. Timeouts: 0. Cubes still open: 0 (`U3_L/open.icnf` is empty).
- Cover: every given cube is covered by a leaf (each leaf equals a given cube; `leaves.icnf` is `top.icnf` in completion order).
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.
- Time (s), over 204 leaves:

| | sum | median | max |
|---|---|---|---|
| CaDiCaL solve | 4708.5 | 17.79 | 272.3 |
| cake_lpr check | 1145.6 | 5.33 | 26.35 |
| solve + check | 5854.0 | 22.93 | 298.65 |

- Driver: `close_march.py` (byte copy of WAVE2/F2, see `driver.diff`), run 15:06:38-15:31 UTC with
  `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 1.2`, output in /opt/work/out/U3_L. Tools in `tools.txt`, environment in `env.txt`.

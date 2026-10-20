# WAVE4 H67: case U3_L (mop-up round 4, task file at 1d3a72c)

- Case: U3_L (U="3", L=""), CNF sha256 7ab00d97d5047e0003bd8d254560dc8464d880d7165c6d7f0e01fab79ee0f823, which matches cases.jsonl.
- Cubes given: 204 (`tasks/H67.json`; top.icnf sha256 3824994bfff683f1547a6762d0f6face42b23c3719cee6b516e30960913de9fd).
- Verified leaves: 330. cake_lpr printed `s VERIFIED UNSAT` for every one.
- Cubes split: 2. Both timed out at 300 s, and march_cu split each into 64 sub-cubes (0 refuted). All 128 sub-cubes are closed.
- Cubes still open: 0 (`open.icnf` is empty).
- Cover: every one of the 204 given cubes is covered by these leaves. I checked this with a script that confirms each given cube is either a leaf or a SPLIT whose sub-cubes form a complete cover, with each sub-cube itself closed.
- Solve time over the 330 leaves: sum 7142.1 s, median 19.95 s, max 105.90 s. This does not count the 2×300 s timeouts that led to the splits.
- Check time (cake_lpr): sum 1529.9 s, median 3.55 s, max 20.09 s.
- Solve plus check per leaf: sum 8672.0 s, median 23.09 s, max 125.99 s.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.
- Driver: run from 15:09:50 to about 16:00 UTC with `--jobs 4 --hours 1.18`. It ended by itself with all cubes closed.

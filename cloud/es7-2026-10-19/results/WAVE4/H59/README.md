# WAVE4 H59: case U_L7

- Task: `results/WAVE4/tasks/H59.json` (committed at 94cc404), case **U_L7** (U = [], L = [7]), case CNF sha256 c6d1c840d97921426e0f2d1d34213fb94293cc1783296ec2357d7883b804f099 (matches cases.jsonl). F.cnf sha256 69c1dc8f…932d (matches).
- Cubes given: **94** (`U_L7/top.icnf`, top_sha256 9e0596b0b444557da4aa015748cdfc59b88c4064ea7e40d00622fd15c8646450).
- Verified leaves: **94**. Every given cube was solved directly by CaDiCaL within the 300 s cap, and cake_lpr printed `s VERIFIED UNSAT` on each LRAT proof (no heap retries needed).
- Cubes split: 0. Cubes still open: 0 (`U_L7/open.icnf` is empty).
- Cover: `leaves.icnf` equals `top.icnf` as a set of cubes, so every given cube is covered by my leaves.
- Solve time (CaDiCaL wall, s): sum 1489.3, median 2.2, max 284.84.
- Check time (cake_lpr wall, s): sum 399.2, median 2.55, max 27.42.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.
- Driver: byte-for-byte copy of `results/WAVE2/F2/close_march.py` (see `driver.diff`). It ran 14:38–14:47 UTC with `--depth 7 --timeout 300 --split-depth 6 --jobs 4`. Tools are listed in `tools.txt`, environment in `env.txt`.

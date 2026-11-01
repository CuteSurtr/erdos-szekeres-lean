# WAVE4 H31: case U4_L (mop-up round 1)

Task: `results/WAVE4/tasks/H31.json` (added at 4bfd8e7), followed per `results/WAVE4/TASK.md` (e0f250b).
Time budget: 2.5 h. The run started at 13:29 UTC and the driver finished at about 14:00 UTC with nothing left open.

- Case: **U4_L** (U = 4, L = empty). The case CNF sha256 is ab7286828ae500e47de8236b6c6953c8ac9a3e776d71991cca253246090ff991 and matches cases.jsonl. F sha256 is 69c1dc8f…ffff932d, as expected.
- Cubes given: **108**. `U4_L/top.icnf` has 108 lines in file order, sha256 f3cffd65f1fb0b0c27f0e2474e5ca65e1b3018c2cb7e7503469c7597a8e23458.
- Verified leaves: **234**. Every one has cake_lpr output exactly `s VERIFIED UNSAT`.
- Cubes split: **2**, top cubes #62 and #63 (0-based). Each timed out at 300 s in CaDiCaL. march_cu at split depth 6 gave 64 sub-cubes each (0 refuted), and all of them closed on the first solve.
- Cubes still open: **0**. `U4_L/open.icnf` is empty.
- Cover: **every given cube is covered by my leaves**. I checked this with my own branching cover check over `leaves.icnf` against each top cube: 0 uncovered. Every line is well formed (`a … 0`). Every leaf extends a given cube, and there are no duplicate leaves.
- SAT results: **none**.
- cake_lpr rejections and UNSAT_UNCHECKED records: **none**.
- Time over the 234 leaves:
  - solve: sum 2550.7 s, median 8.66 s, max 90.90 s.
  - check: sum 916.3 s, median 3.15 s, max 19.41 s.
  - solve and check together: sum 3467.0 s, median 12.71 s, max 110.31 s.
  - The 2 split cubes also spent 300 s each in CaDiCaL before the split. march_cu took 252 s and 650 s to split them.

Driver: `close_march.py` is a byte-for-byte copy of `results/WAVE2/F2/close_march.py` (see `driver.diff`). It ran with `--name U4_L --top top.icnf --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.224`, with its output in /opt/work/out/U4_L, outside the git checkout. Tools and hashes are in `tools.txt`, the environment in `env.txt`.

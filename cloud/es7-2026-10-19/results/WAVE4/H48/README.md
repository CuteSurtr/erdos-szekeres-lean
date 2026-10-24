# WAVE4 H48: case U_L2 (mop-up round 2, list 3/3)

- Case: U_L2 (U = {}, L = {2}); CASE.cnf sha256 1d26b9475d1609388bda1853cc22c1fba0bb73fb1a5f8a28adf9fbd3f15aaa53, matches cases.jsonl.
- Cubes given: 150 (results/WAVE4/tasks/H48.json at 3ed048e); top.icnf has 150 lines, sha256 b47fc29aa6ecc672385d45f768e22e4522d63c5b287656741c1d7e35d3b5831b.
- Verified leaves: 150. Each has CaDiCaL exit 20 and cake_lpr `s VERIFIED UNSAT`.
- Cubes split: 0. Cubes still open: 0 (open.icnf is empty; the driver printed `open 0`).
- Coverage: every given cube is covered. The leaves are exactly the 150 given cubes (leaves.icnf equals top.icnf as a set).
- Solve time (CaDiCaL, wall s): sum 2339.4, median 12.43, max 121.6.
- Check time (cake_lpr, wall s): sum 677.7, median 3.82, max 17.4.
- Solve plus check per cube: sum 3017.2, median 16.82, max 139.0.
- SAT results: none. cake_lpr rejections or UNSAT_UNCHECKED records: none. Heap retries: 0.
- Driver: results/WAVE2/F2/close_march.py copied byte for byte (driver.diff). It ran 14:17:35 to about 14:30 UTC with --jobs 4 --timeout 300 --split-depth 6 --hours 2.2. Output directory /opt/work/out/U_L2 (outside the checkout).
- Tools and hashes: tools.txt. Environment: env.txt.

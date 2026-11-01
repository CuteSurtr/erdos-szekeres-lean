# WAVE4 H15

Case U_L2 (CNF sha256 1d26b9475d1609388bda1853cc22c1fba0bb73fb1a5f8a28adf9fbd3f15aaa53, matches cases.jsonl).
Cubes given: 324 (`tasks/H15.json` at e0f250b; `U_L2/top.icnf`, sha256 6cb61c07...5c4f).

Driver: byte-for-byte copy of `results/WAVE2/F2/close_march.py` (sha256 2e0975aa...c855), run
2026-10-20 12:55:42Z with `--top top.icnf --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.221`.
It ended on its own at about 14:02Z with `open 0`.

Result:
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none. TIMEOUT records: none.
- Verified leaves (cake_lpr `s VERIFIED UNSAT`): 512 (`U_L2/leaves.icnf`).
- Cubes split: 3 (timed out at 300 s; march_cu split depth 6 gave 63, 64 and 64 sub-cubes, all closed).
  321 top cubes closed directly + 191 sub-cubes = 512 leaves.
- Cubes still open: 0 (`U_L2/open.icnf` is empty).
- Cover: every one of the 324 given cubes is covered by the leaves (checked by expanding each top
  cube through the SPLIT records of leaves.jsonl down to leaves in leaves.icnf: 324/324).
- Solve time over the 512 verified leaves (wall, per job): sum 10704.3 s, median 12.15 s, max 278.42 s.
  Check time (cake_lpr): sum 2226.6 s, median 3.19 s, max 29.73 s.
  The 3 split cubes used 300.02 s each of solving plus 553.7 s, 94.5 s and 425.4 s of march_cu.

# WAVE3 / G19

Task `results/WAVE3/tasks/G19.json` (as committed at 9a26cc2): case U9_L, 59 open cubes (each of length 7).

| case | cubes given | verified leaves | cubes still open | every given cube covered | SAT | cake_lpr rejections |
|------|-------------|-----------------|------------------|--------------------------|-----|---------------------|
| U9_L | 59 | 122 | 0 | yes | none | none |

Time:
- Wall time 11:20:25 to 11:40 UTC (about 20 min), 4 jobs.
- CaDiCaL solve time summed over all jobs: 3411 s. cake_lpr check time: 644 s. One march_cu split: 62 s.
- 58 of the given cubes were solved directly; the slowest took 257 s, and the largest LRAT proof was 195 MB.
- The one cube that timed out at 300 s, `-1134 1155 1245 1229 1212 1194 1175`, was split by march_cu at depth 6 into 64 sub-cubes (0 refuted). All 64 were then solved and verified.
- Every one of the 122 leaves has cake_lpr output exactly `s VERIFIED UNSAT`. CaDiCaL reported no SAT result.

Checks:
- F.cnf sha256 69c1dc8f…ffff932d. U9_L.cnf (hullsplit.py case F.cnf 9 "") sha256 379250e6…633922e5, which equals cases.jsonl.
- `U9_L/top.icnf` holds the 59 given cubes in the file's order. It is the driver's `--top`.
- Independent cover check (`/opt/work/cover.py`, not committed; it is a recursive split on the leaf literals): every given cube is covered by the leaves in `U9_L/leaves.icnf`. The leaves are 122 distinct cubes, every line is well formed (`a … 0`), and `U9_L/open.icnf` is empty.
- The driver is `close_march.py`, an unchanged copy of WAVE2/F2's driver. See `driver.diff` for points (a)–(c) and the diff against W19. Tools and commits are listed in `tools.txt`.

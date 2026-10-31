# C2P5 M94: list C2P5B.tsv, shard 44 of 50

TASK `results/C2P5/TASK.md` at commit 81cb025f, run unmodified. V = M94, LIST = C2P5B.tsv, j = 44, N = 50, H = 5.25.
The lane started at 15:16Z (start epoch 1793459590, END 1793477590 = 20:13:10Z). It finished all units at 19:23:03Z, about 50 minutes before END.
The machine had 4 cores, 15 GB RAM and no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored `tools-src.tar.xz` (manifest: all 196 files match). Nothing was cloned or downloaded.
  - CaDiCaL c6073042 (3.0.1)
  - cake_lpr a36874a8
  - lrat-check 2e3b2dc with the E2 patch
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and of base.json (2476faff…) both match.
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, 18 rows with idx ≡ 44 mod 50)

| case | kind | units | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|---|
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 6 | 0 | 0 | 0 |
| P1 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | H | 4 | 4 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |
| **total** | | **18** | **18** | 0 | 0 | 0 |

All 18 records are UNSATISFIABLE with `"certified": true`: lrat-check gave `c VERIFIED` and cake_lpr gave `s VERIFIED UNSAT`, the latter on its first attempt with an 8000 MB heap.

Certified units (min / median / max):
- solve: 26.6 / 365.4 / 2055.1 s
  - Q units: P2_6-11 1241 s, P1_5-8 438 s, P3_1-13 2055 s.
  - H units: 26.6 – 545.6 s.
- lrat-check: 11.6 / 47.5 / 73.1 s
- cake_lpr: 121.8 / 314.9 / 460.3 s
- proof size: 0.22 / 3.37 / 5.21 GB (the proofs were deleted after checking)

Per unit (solve s, lrat-check s, cake_lpr s, proof GB):

| unit | kind | cap | solve | lrat | cake | proof |
|---|---|---|---|---|---|---|
| P2_6-11 | Q | 8000 | 1241.3 | 57.8 | 364.5 | 4.20 |
| P1_5-8 | Q | 8000 | 437.9 | 47.5 | 315.9 | 3.36 |
| P2_1-5-14 | H | 2400 | 545.6 | 53.9 | 345.0 | 3.63 |
| P2_3-5-15 | H | 2400 | 418.7 | 51.3 | 324.5 | 3.50 |
| P2_3-10-13 | H | 2400 | 367.3 | 47.9 | 317.3 | 3.39 |
| P2_4-7-14 | H | 2400 | 363.5 | 53.3 | 326.8 | 3.39 |
| P2_5-7-13 | H | 2400 | 244.6 | 46.0 | 314.8 | 3.15 |
| P2_7-8-10 | H | 2400 | 29.9 | 11.6 | 125.9 | 0.22 |
| P1_2-6-12 | H | 2400 | 424.5 | 47.5 | 314.9 | 3.44 |
| P1_3-4-11 | H | 2400 | 115.9 | 24.9 | 184.9 | 1.39 |
| P1_3-11-13 | H | 2400 | 305.5 | 46.4 | 304.9 | 3.24 |
| P1_5-6-11 | H | 2400 | 26.7 | 12.0 | 121.8 | 0.22 |
| P3_1-13 | Q | 8000 | 2055.1 | 73.1 | 460.3 | 5.21 |
| P3_1-2-8 | H | 2400 | 289.1 | 45.2 | 296.5 | 3.22 |
| P3_1-7-16 | H | 2400 | 476.0 | 49.0 | 325.4 | 3.56 |
| P3_4-5-13 | H | 2400 | 289.4 | 47.6 | 310.7 | 3.27 |
| P3_4-11-12 | H | 2400 | 255.0 | 42.6 | 293.4 | 3.17 |
| P3_5-10-15 | H | 2400 | 517.1 | 51.5 | 313.4 | 3.49 |

## Resources and incidents
- The largest solver RSS was 4421 MB (P2_3-5-15). cake_lpr used up to about 8.2 GB RSS.
- There were no memory problems. The lowest free disk space was about 23 GB.
- No SAT was found (no `SAT_FOUND`), no proof was rejected and no unit gave an error.

Files: `out.jsonl` (18 records), `lane.log.tail`, `units.tsv`, `run.sh`, `tools.txt`, `env.txt`.

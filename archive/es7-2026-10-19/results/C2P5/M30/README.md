# C2P5 M30: list C2P5A.tsv, shard 30 of 37

TASK `results/C2P5/TASK.md` at commit 81cb025f, run unmodified. V = M30, LIST = C2P5A.tsv, j = 30, N = 37, H = 4.5.
The lane started at 19:28Z (start epoch 1793474753 = 19:25:53Z, END 1793490053 = 23:40:53Z). It finished all units at 21:16:21Z, about 2 h 25 min before END.
The machine had 4 cores, 15 GB RAM and no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored `tools-src.tar.xz` (manifest: all 196 files match). Nothing was cloned or downloaded.
  - CaDiCaL c6073042 (3.0.1)
  - cake_lpr a36874a8
  - lrat-check 2e3b2dc with the E2 patch
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and of base.json (2476faff…) both match.
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, 10 rows with idx ≡ 30 mod 37)

| case | kind | units | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|---|
| P4 | H | 10 | 10 | 0 | 0 | 0 |
| **total** | | **10** | **10** | 0 | 0 | 0 |

Certified: P4_1-2-6, P4_1-3-7, P4_1-5-16, P4_1-8-9, P4_1-9-16, P4_1-11-16, P4_2-6-13, P4_5-8-14, P4_6-9-10, P4_8-10-12.

All 10 records are UNSATISFIABLE with `"certified": true`: lrat-check gave `c VERIFIED` and cake_lpr gave `s VERIFIED UNSAT`, the latter on its first attempt with an 8000 MB heap.

Certified units (min / median / max):
- solve: 26.0 / 311.0 / 556.1 s (cap 2400 s)
- lrat-check: 14.1 / 55.7 / 63.0 s
- cake_lpr: 112.8 / 323.0 / 354.2 s
- proof size: 0.22 / 3.31 / 3.65 GB (deleted after checking)

## Resources and anomalies
- Largest solver RSS: 4392 MB (P4_1-3-7).
- No SAT, no proof rejection, no error record, no memory problem.

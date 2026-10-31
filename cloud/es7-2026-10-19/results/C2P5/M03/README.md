# C2P5 M03: LIST C2P5A.tsv, j = 3, N = 37, H = 4.5, Z = 81cb025f

Start 2026-10-31 18:12:44Z (epoch 1793470364), END 1793485664 (22:27:44Z). The lane finished all its units at 19:42:18Z.

## Tools and checks (details in `tools.txt`)

- `C2P/vendor/build_tools.sh`: the vendored sources match all 196 entries of `MANIFEST.sha256`. It built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc with the E2 patch). Nothing was cloned or downloaded.
- Sanity checks: lrat-check and cake_lpr both rejected the bad LRAT and both accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. Both sha256 values match: base.cnf `b0061e90…d8ff1` and base.json `2476faff…2b48`.
- Cubes: for P1..P8, `l2cubes.py` gave files byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (rows of C2P5A.tsv with idx ≡ 3 mod 37; 4 units)

| case | kind | units | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|---|---|
| P4 | Q | 1 | 1 | 0 | 0 | 0 |
| P4 | H | 3 | 3 | 0 | 0 | 0 |
| **total** | | **4** | **4** | 0 | 0 | 0 |

| unit | kind | cap s | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|---|---|
| P4_1-9 | Q | 8000 | 2816.75 | 114.0 | 618.1 | 6349316381 | 4371 |
| P4_5-6-14 | H | 2400 | 332.62 | 66.6 | 361.3 | 3298010031 | 4358 |
| P4_5-13-14 | H | 2400 | 281.88 | 65.1 | 349.9 | 3221175742 | 4398 |
| P4_7-9-10 | H | 2400 | 31.02 | 17.1 | 130.2 | 216724299 | 2662 |

Certified units (min / median / max):
- solve: 31.0 / 307.3 / 2816.8 s
- lrat-check: 17.1 / 65.9 / 114.0 s
- cake_lpr: 130.2 / 355.6 / 618.1 s
- proof size: 0.22 / 3.26 / 6.35 GB

All four records are UNSATISFIABLE with `"certified": true`: lrat-check printed `c VERIFIED` and cake_lpr printed `s VERIFIED UNSAT`.

- The largest solver RSS was 4398 MB (P4_5-13-14).
- There were no SAT answers, no proof rejections, no errors and no memory problems. Disk use peaked with the 6.3 GB proof and stayed within the free space.

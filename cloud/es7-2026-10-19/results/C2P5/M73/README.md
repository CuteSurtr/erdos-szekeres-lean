# C2P5 M73

TASK `results/C2P5/TASK.md` at commit 81cb025f, with V = M73, LIST = C2P5B.tsv, j = 23, N = 50, H = 5.25.
Start 2026-10-31 15:10:29Z (epoch 1793459429), END = 1793477429 (20:10:29Z). The lane started at 15:12:59Z and
finished all units at 18:39:29Z ("lane done").

## Tools and checks (`tools.txt`)

- `C2P/vendor/build_tools.sh` built everything from the vendored `tools-src.tar.xz` (manifest: all 196 files match):
  CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch). Nothing was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example printed
  `s VERIFIED UNSAT`.
- Base CNF from `SYMZ/zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`. The sha256 of base.cnf
  (b0061e90…d8ff1) and base.json (2476faff…b48) both match.
- Cubes: for each a = 1..8, `C2C34/l2cubes.py` output is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, 19 rows of C2P5B.tsv with idx ≡ 23 mod 50)

| case | kind | units | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|---|
| P1 | Q (8000 s) | 1 | 1 | 0 | 0 | 0 |
| P1 | H (2400 s) | 5 | 5 | 0 | 0 | 0 |
| P2 | Q (8000 s) | 1 | 1 | 0 | 0 | 0 |
| P2 | H (2400 s) | 6 | 6 | 0 | 0 | 0 |
| P3 | Q (8000 s) | 1 | 1 | 0 | 0 | 0 |
| P3 | H (2400 s) | 5 | 5 | 0 | 0 | 0 |
| **total** | | **19** | **19** | 0 | 0 | 0 |

All 19 units are UNSATISFIABLE and `"certified": true`. For each one, lrat-check gave `c VERIFIED` and cake_lpr gave `s VERIFIED UNSAT`.

Certified units, as (min / median / max):

| | n | solve s | lrat-check s | cake_lpr s | proof size |
|---|---|---|---|---|---|
| Q | 3 | 774.8 / 802.0 / 855.7 | 65.0 / 65.6 / 73.0 | 376.1 / 377.1 / 379.9 | 3.63 / 3.81 / 3.95 GB |
| H | 16 | 25.3 / 252.0 / 480.2 | 13.8 / 55.2 / 64.1 | 115.8 / 318.4 / 359.5 | 0.22 / 3.22 / 3.57 GB |
| all | 19 | 25.3 / 270.3 / 855.7 | 13.8 / 59.2 / 73.0 | 115.8 / 321.5 / 379.9 | 0.22 / 3.25 / 3.95 GB |

Q units: P2_4-8 802.0 s, P1_3-7 774.8 s, P3_6-10 855.7 s. Each unit's figures are in `out.jsonl`.

## Memory, SAT, rejections

- Largest solver RSS: 4424 MB (P2_1-3-15). cake_lpr ran with an 8000 MB heap. There was no memory problem.
- No SAT. No proof rejection. No ERROR record.

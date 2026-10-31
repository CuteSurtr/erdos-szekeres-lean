# C2P5 M60: LIST = C2P5B.tsv, shard j = 10 of N = 50, H = 5.25 h (TASK.md at 81cb025f)

Ran 2026-10-31 on a 4-core machine with 15 GB RAM (`env.txt`). Lane started at 15:26:59Z. END was 1793478421, which is the start plus 5.25 h minus 15 min (`run.sh`). The lane finished every unit at 17:51:21Z, well before END.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` checked the hashes of all 196 vendored files against the manifest. It then built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch). Nothing was downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: the header is `p cnf 838032 16653336`. The sha256 of base.cnf (`b0061e90…`) and of base.json (`2476faff…`) both match the expected values.
- Cubes: for P1..P8, the output of `l2cubes.py` is byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (`units.tsv`, `out.jsonl`)
14 units: the rows with idx ≡ 10 (mod 50).

| case | kind | units | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|---|
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | Q | 2 | 2 | 0 | 0 | 0 |
| P1 | H | 5 | 5 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |
| **total** | | **14** | **14** | 0 | 0 | 0 |

All 14 units came back UNSATISFIABLE with `"certified": true`: lrat-check printed `c VERIFIED` and cake_lpr printed `s VERIFIED UNSAT`.
- Q: P2_3-7, P1_2-7, P1_8-9, P3_5-6
- H: P1_2-3-11, P1_2-8-11, P1_3-6-8, P1_4-6-9, P1_5-9-12, P3_1-5-7, P3_1-10-11, P3_4-7-10, P3_5-6-13, P3_6-8-11

Seconds and proof sizes for the certified units (min / median / max):

| | solve s | lrat-check s | cake_lpr s | proof GB |
|---|---|---|---|---|
| all 14 | 26.2 / 253.4 / 729.9 | 14.1 / 56.1 / 68.1 | 117.6 / 323.1 / 381.5 | 0.216 / 3.258 / 3.832 |
| Q (4) | 439.5 / 560.2 / 729.9 | 57.4 / 62.8 / 68.1 | 318.3 / 351.0 / 381.5 | 3.285 / 3.548 / 3.832 |
| H (10) | 26.2 / 167.2 / 320.6 | 14.1 / 45.3 / 63.0 | 117.6 / 269.3 / 340.4 | 0.216 / 2.536 / 3.269 |

The largest solver RSS was 4427 MB (P3_1-5-7).

There was no SAT, no proof rejection, no error and no memory or disk problem. At least 24 GB of disk stayed free throughout.

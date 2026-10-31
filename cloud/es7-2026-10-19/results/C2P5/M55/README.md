# C2P5 M55: list C2P5B.tsv, shard 5 of 50, H = 5.25

TASK: `results/C2P5/TASK.md` at 81cb025f. Started 2026-10-31 15:10:24 UTC (epoch 1793459424), END = 1793477424 (20:10:24 UTC). The lane finished all its units at 18:44:22 UTC, well before END.

## Tools and checks (`tools.txt`)
- Built by `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; the sha256 of base.cnf (b0061e90…) and base.json (2476faff…) match the expected values.
- Cubes P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, rows with idx ≡ 5 mod 50: 14 units)

| case | kind | units | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|---|---|
| P2 | Q | 2 | 2 | 0 | 0 | 0 |
| P1 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | H | 5 | 5 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |
| **total** | | **14** | **14** | **0** | **0** | **0** |

Every unit is UNSATISFIABLE with `"certified": true`: lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, all at an 8000 MB heap with no retry.

Certified units (min / median / max):

| | solve s | lrat-check s | cake_lpr s | proof bytes |
|---|---|---|---|---|
| all 14 | 18.6 / 300.6 / 2156.7 | 11.7 / 51.7 / 95.0 | 97.6 / 311.3 / 496.8 | 0.21 / 3.30 / 5.64 GB |
| Q (4) | 380.6 / 1638.3 / 2156.7 | 52.9 / 77.0 / 95.0 | 328.8 / 442.8 / 496.8 | 3.27 / 4.94 / 5.64 GB |
| H (10) | 18.6 / 186.3 / 467.6 | 11.7 / 46.8 / 61.1 | 97.6 / 276.7 / 361.0 | 0.21 / 2.93 / 3.67 GB |

Per unit (solve s): P2_1-8 2060.7, P2_9-10 380.6, P1_6-12 1215.9, P1_2-3-6 81.2, P1_2-7-14 467.6, P1_3-5-12 209.9, P1_4-5-12 162.6, P1_5-8-11 19.0, P3_4-12 2156.7, P3_1-4-13 404.8, P3_1-9-12 321.4, P3_4-6-14 279.9, P3_5-6-8 23.4, P3_6-7-12 18.6.

## Largest solver RSS
4418.6 MB (P1_3-5-12). cake_lpr reached about 8.2 GB RSS at its 8000 MB heap; free memory never fell below about 1 GB.

## SAT, rejections, memory
None. There was no SAT, no proof rejection, no ERROR status and no memory problem. Proofs were deleted after checking, and no CNF or proof file was committed.

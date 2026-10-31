# C2P5 M69: LIST = C2P5B.tsv, j = 19, N = 50, H = 5.25 (task commit 81cb025f)

Start 2026-10-31 15:10:20 UTC (epoch 1793459420); END = 1793477420 (20:10:20 UTC). The lane stopped by itself at 20:04:27 (352 s left before END, so no further unit started).

## Tools and checks (details in `tools.txt`)
- `C2P/vendor/build_tools.sh`: vendored sources, manifest of all 196 files OK. CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch). No code was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf and base.json both match the expected values.
- Cubes: P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (19: rows idx ≡ 19 mod 50 of C2P5B.tsv)
| case | kind | units | certified | timed out | not reached | errors |
|---|---|---|---|---|---|---|
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 6 | 0 | 0 | 0 |
| P1 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | H | 5 | 5 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 0 | 0 | 5 | 0 |
| **total** | | **19** | **14** | **0** | **5** | **0** |

- Certified (UNSATISFIABLE, accepted by lrat-check and by cake_lpr):
  - Q: P2_3-16, P1_2-16 and P3_5-15. P3_5-15 ran with a cap of 4042 s instead of 8000 s, because the lane shortened it to fit before END. It still solved, in 3546 s.
  - H: P2_1-3-11, P2_1-8-9, P2_3-7-9, P2_4-5-6, P2_4-9-14, P2_5-10-11, P1_2-4-8, P1_2-9-13, P1_3-7-9, P1_4-7-11 and P1_6-7-12.
- Not reached (time budget): P3_1-5-16, P3_1-11-15, P3_4-8-11, P3_5-7-14 and P3_6-10-11, all P3 H.
- Timed out (UNKNOWN): none. Errors or `"certified": false`: none.

## Certified units: min / median / max
| | min | median | max |
|---|---|---|---|
| solve s | 28.2 | 213.3 | 3853.7 (P1_2-16) |
| lrat-check s | 11.3 | 35.8 | 106.6 |
| cake_lpr s | 109.2 | 243.3 | 659.4 |
| proof bytes | 215.7 MB | 2.23 GB | 7.09 GB (P1_2-16) |

The three Q units by themselves took 2956, 3854 and 3546 s to solve, and their proofs were 6.5 to 7.1 GB.

## Resources and outcome
- Largest solver RSS: 4452 MB (P2_3-16). cake_lpr ran with an 8000 MB heap and reached about 8.2 GB RSS. The machine has 15 GB of memory, and no memory problem occurred.
- No SAT answer (no `SAT_FOUND`), no proof rejection and no memory problem.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (14 records), `lane.log.tail`.

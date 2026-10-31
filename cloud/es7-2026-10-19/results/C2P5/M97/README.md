# C2P5 M97: shard 47 of 50 of C2P5B.tsv

Task `results/C2P5/TASK.md` (commit 81cb025f, unchanged at the run's HEAD). V = M97, LIST = C2P5B.tsv, j = 47, N = 50, H = 5.25.
Start 2026-10-31 15:10:31 UTC (epoch 1793459431), END = 1793477431; the lane started at 15:12:29Z and finished all units at 18:39:33Z.
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch) from the vendored `tools-src.tar.xz`; all 196 files matched `MANIFEST.sha256`. Nothing was cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf `b0061e90…d8ff1` and base.json `2476faff…72b48`, as required.
- Cubes: `l2cubes.py` for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (`units.tsv`, 18 rows with idx ≡ 47 mod 50)

| case | kind | units | certified | timed out | not reached | errors |
|---|---|---|---|---|---|---|
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 6 | 0 | 0 | 0 |
| P1 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | H | 4 | 4 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |
| **all** | | **18** | **18** | 0 | 0 | 0 |

Every unit was UNSATISFIABLE and certified: lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.

Certified units, min / median / max:

| group | n | solve s | lrat-check s | cake_lpr s | proof size |
|---|---|---|---|---|---|
| Q | 3 | 426.8 / 1161.5 / 1368.4 | 55.4 / 72.5 / 81.8 | 322.3 / 400.7 / 430.5 | 3.30 / 4.40 / 4.96 GB |
| H | 15 | 17.8 / 281.5 / 483.6 | 12.8 / 53.9 / 74.4 | 112.0 / 315.7 / 383.5 | 0.22 / 3.27 / 3.57 GB |
| all | 18 | 17.8 / 294.9 / 1368.4 | 12.8 / 55.5 / 81.8 | 112.0 / 317.4 / 430.5 | 0.22 / 3.29 / 4.96 GB |

Q units: P2_7-8 (427 s), P1_5-11 (1161 s), P3_1-16 (1368 s), all well under the 8000 s cap.

## Memory, SAT, rejections
- Largest solver RSS: 4480.6 MB (P3_1-16). cake_lpr ran with an 8000 MB heap (about 8.2 GB RSS observed). No memory problems.
- No SAT, no proof rejections, no ERROR records, no timeouts.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (18 records), `lane.log.tail`.

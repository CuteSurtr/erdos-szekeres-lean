# C2P5 M95: fifth wave, list C2P5B.tsv, shard j = 45 of N = 50

TASK `results/C2P5/TASK.md` (commit 81cb025f), H = 5.25 h. Start 2026-10-31 15:10:26 UTC (epoch 1793459426),
END = 1793477426 (20:10:26 UTC). Machine: 4 vCPU, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)

- `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz` (nothing cloned or downloaded): manifest all 196 files
  match; CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
  cake_lpr example `s VERIFIED UNSAT`; sanity: both checkers reject the bad LRAT and accept the good one.
- Base CNF `SYMZ/zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json as expected.
- Cubes: `C2C34/l2cubes.py` for P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, rows with idx ≡ 45 mod 50: 18 units)

All 18 units **certified UNSAT** (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`). The lane finished its list at
19:29:53 UTC, before END.

| case | kind | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|---|
| P2 | Q | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 0 | 0 | 0 |
| P1 | Q | 1 | 0 | 0 | 0 |
| P1 | H | 4 | 0 | 0 | 0 |
| P3 | Q | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 0 | 0 | 0 |
| total | | 18 | 0 | 0 | 0 |

(P3_1-14 and P3_5-11-12 ran with caps lowered by lane.py to 7170 s and 2112 s to fit END; both finished well inside them.)

| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P2_6-12 | P2 | Q | 8000 | UNSATISFIABLE | 1715.71 | 73.2 | 411.2 | 4.69 GB | 4429.39 |
| P1_5-9 | P1 | Q | 8000 | UNSATISFIABLE | 807.7 | 58.2 | 360.4 | 3.68 GB | 4405.89 |
| P2_1-6-7 | P2 | H | 2400 | UNSATISFIABLE | 310.88 | 50.8 | 304.8 | 3.24 GB | 4401.61 |
| P2_3-5-16 | P2 | H | 2400 | UNSATISFIABLE | 412.29 | 55.5 | 349.2 | 3.69 GB | 4423.27 |
| P2_3-10-14 | P2 | H | 2400 | UNSATISFIABLE | 513.77 | 53.7 | 340.2 | 3.55 GB | 4412.66 |
| P2_4-7-15 | P2 | H | 2400 | UNSATISFIABLE | 436.49 | 49.2 | 324.1 | 3.46 GB | 4361.5 |
| P2_5-7-14 | P2 | H | 2400 | UNSATISFIABLE | 292.16 | 48.8 | 322.5 | 3.26 GB | 4365.54 |
| P2_7-8-11 | P2 | H | 2400 | UNSATISFIABLE | 28.24 | 13.4 | 123.3 | 0.22 GB | 2676.33 |
| P1_2-6-13 | P1 | H | 2400 | UNSATISFIABLE | 577.13 | 52.7 | 332.5 | 3.59 GB | 4369.69 |
| P1_3-4-12 | P1 | H | 2400 | UNSATISFIABLE | 249.24 | 49.2 | 303.1 | 3.19 GB | 4375.08 |
| P1_3-11-14 | P1 | H | 2400 | UNSATISFIABLE | 382.83 | 48.0 | 313.4 | 3.44 GB | 4409.15 |
| P1_5-6-12 | P1 | H | 2400 | UNSATISFIABLE | 29.94 | 11.6 | 114.7 | 0.24 GB | 2647.54 |
| P3_1-14 | P3 | Q | 7170 | UNSATISFIABLE | 1786.42 | 68.9 | 420.8 | 5.01 GB | 4373.61 |
| P3_1-2-9 | P3 | H | 2400 | UNSATISFIABLE | 345.05 | 47.6 | 309.8 | 3.30 GB | 4363.56 |
| P3_1-8-9 | P3 | H | 2400 | UNSATISFIABLE | 297.89 | 43.1 | 297.2 | 3.22 GB | 4368.52 |
| P3_4-5-14 | P3 | H | 2400 | UNSATISFIABLE | 358.23 | 49.9 | 304.1 | 3.36 GB | 4370.88 |
| P3_4-11-13 | P3 | H | 2400 | UNSATISFIABLE | 292.67 | 47.5 | 304.5 | 3.26 GB | 4373.03 |
| P3_5-11-12 | P3 | H | 2112 | UNSATISFIABLE | 88.31 | 22.7 | 164.0 | 1.12 GB | 3151.06 |

- solve s (min / median / max): 28.24 / 351.64 / 1786.42
- lrat-check s (min / median / max): 11.6 / 49.2 / 73.2
- cake_lpr s (min / median / max): 114.7 / 311.6 / 420.8
- proof size (min / median / max): 0.22 GB / 3.33 GB / 5.01 GB
- largest solver RSS: 4429.39 MB (P2_6-12)
- all records: lrat_check 'c VERIFIED' and cake_lpr 's VERIFIED UNSAT': True

## SAT, rejections, memory

- No SAT (`/opt/work/SAT_FOUND` never appeared).
- No proof rejection, no `"certified": false` record, no ERROR status.
- No memory problem: largest solver RSS 4.43 GB; disk stayed at ≥ 23 GB free; proofs deleted after checking.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (18 records), `lane.log.tail`.

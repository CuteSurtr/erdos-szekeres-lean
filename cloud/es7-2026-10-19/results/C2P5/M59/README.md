# C2P5 M59

TASK `results/C2P5/TASK.md` at commit 81cb025f, with V = M59, LIST = C2P5B.tsv, j = 9, N = 50, H = 5.25. Machine: 4 cores, 15 GB RAM (`env.txt`). Lane started 2026-10-31 15:24:50 UTC (epoch 1793460290), END 1793478290; lane finished all units at 18:19:34 UTC.

**Summary: all 14 units are certified UNSAT.** No timeouts, no units left unreached, no errors, no SAT, no proof rejections and no memory problems.

## Tools and checks (`tools.txt`)

- Built with `C2P/vendor/build_tools.sh` from the vendored `vendor/tools-src.tar.xz`: CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. All 196 manifest hashes match, and nothing was downloaded.
- Sanity checks: lrat-check and cake_lpr both reject the bad LRAT and both accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 values of base.cnf (b0061e90…) and base.json (2476faff…) match.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (idx ≡ 9 mod 50 of C2P5B.tsv; `units.tsv`)

| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof GB | solver RSS MB | certified |
|---|---|---|---|---|---|---|---|---|---|---|
| P2_3-6 | P2 | Q | 8000 | UNSATISFIABLE | 549.41 | 59.4 | 346.7 | 3.53 | 4411.39 | True |
| P1_2-6 | P1 | Q | 8000 | UNSATISFIABLE | 901.78 | 60.4 | 334.3 | 3.61 | 4412.21 | True |
| P1_7-11 | P1 | Q | 8000 | UNSATISFIABLE | 573.09 | 58.6 | 341.6 | 3.57 | 4374.46 | True |
| P1_2-3-10 | P1 | H | 2400 | UNSATISFIABLE | 214.07 | 51.5 | 299.5 | 3.17 | 4365.91 | True |
| P1_2-8-10 | P1 | H | 2400 | UNSATISFIABLE | 235.59 | 52.2 | 296.7 | 3.16 | 4395.79 | True |
| P1_3-6-7 | P1 | H | 2400 | UNSATISFIABLE | 26.03 | 13.9 | 113.3 | 0.22 | 2652.2 | True |
| P1_4-6-8 | P1 | H | 2400 | UNSATISFIABLE | 26.44 | 12.8 | 113.5 | 0.22 | 2665.94 | True |
| P1_5-9-11 | P1 | H | 2400 | UNSATISFIABLE | 21.52 | 14.3 | 116.3 | 0.25 | 2635.26 | True |
| P3_4-16 | P3 | Q | 8000 | UNSATISFIABLE | 2598.91 | 105.0 | 568.9 | 6.58 | 4389.42 | True |
| P3_1-5-6 | P3 | H | 2400 | UNSATISFIABLE | 202.19 | 49.7 | 284.5 | 3.18 | 4405.47 | True |
| P3_1-9-16 | P3 | H | 2400 | UNSATISFIABLE | 406.37 | 56.6 | 332.4 | 3.54 | 4373.25 | True |
| P3_4-7-9 | P3 | H | 2400 | UNSATISFIABLE | 81.82 | 26.1 | 171.9 | 1.11 | 3127.63 | True |
| P3_5-6-12 | P3 | H | 2400 | UNSATISFIABLE | 104.45 | 30.4 | 194.3 | 1.56 | 3419.82 | True |
| P3_6-8-10 | P3 | H | 2400 | UNSATISFIABLE | 27.81 | 14.1 | 110.5 | 0.22 | 2663.71 | True |

Counts by case and kind (certified / timed out / not reached / error):

| case | kind | units | certified | UNKNOWN | not reached | error or not certified |
|---|---|---|---|---|---|---|
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | Q | 2 | 2 | 0 | 0 | 0 |
| P1 | H | 5 | 5 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |

- all certified (14): solve s 21.5 / 208.1 / 2598.9; lrat-check s 12.8 / 50.6 / 105.0; cake_lpr s 110.5 / 290.6 / 568.9; proof GB 0.22 / 3.17 / 6.58 (min / median / max)
- Q certified (4): solve s 549.4 / 737.4 / 2598.9; lrat-check s 58.6 / 59.9 / 105.0; cake_lpr s 334.3 / 344.1 / 568.9; proof GB 3.53 / 3.59 / 6.58 (min / median / max)
- H certified (10): solve s 21.5 / 93.1 / 406.4; lrat-check s 12.8 / 28.2 / 56.6; cake_lpr s 110.5 / 183.1 / 332.4; proof GB 0.22 / 1.33 / 3.54 (min / median / max)

Largest solver RSS: 4412 MB (P1_2-6).


Both checkers accepted every proof (`c VERIFIED` and `s VERIFIED UNSAT`), and each proof was deleted after its check. The peak solver RSS was about 4.4 GB, well within the 15 GB of RAM. The largest proof was 6.58 GB (P3_4-16), and disk use stayed below 50%.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (14 records), `lane.log.tail`.

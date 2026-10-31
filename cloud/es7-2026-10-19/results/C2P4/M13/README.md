# C2P4 M13: shard j = 13 of N = 50 of lists/C2P4.tsv (task commit a46b478d, H = 2.5)

Machine: 4 CPUs, 15 GB RAM (env.txt). Start 13:01:47Z (epoch 1793451707), END 1793459807 (15:16:47Z). One lane (run.sh).

## Tools and checks (tools.txt)
- Built with C2P/vendor/build_tools.sh from the vendored sources only: manifest 196/196 files match; CaDiCaL 3.0.1
  (c6073042), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. cake_lpr example: s VERIFIED UNSAT. Sanity:
  both checkers reject the bad LRAT and accept the good one.
- Base CNF: header p cnf 838032 16653336; sha256 base.cnf b0061e90…d8ff1 and base.json 2476faff…bf472b48, both as required.
- Cubes: l2cubes.py P1..P8 byte-identical to C2P/cubes/P{a}_cubes.txt.

## Units (13: idx ≡ 13 mod 50)
| idx | unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB | certified |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 13 | P5_6-9 | P5 | Q | 6800 | UNSATISFIABLE | 726.09 | 68.5 | 373.2 | 3.71 | 4408.32 | True |
| 63 | P4_8-10 | P4 | Q | 5613 | UNSATISFIABLE | 525.46 | 62.5 | 373.1 | 3.48 | 4362.14 | True |
| 113 | P4_1-7-10 | P4 | H | 1800 | UNSATISFIABLE | 394.13 | 58.8 | 330.7 | 3.38 | 4395.77 | True |
| 163 | P4_2-5-7 | P4 | H | 1800 | UNSATISFIABLE | 254.23 | 57.5 | 318.4 | 3.25 | 4410.5 | True |
| 213 | P4_5-6-16 | P4 | H | 1800 | UNSATISFIABLE | 360.27 | 58.3 | 348.2 | 3.41 | 4375.63 | True |
| 263 | P4_6-7-11 | P4 | H | 1800 | UNSATISFIABLE | 26.84 | 13.8 | 118.3 | 0.22 | 2650.27 | True |
| 313 | P4_8-9-11 | P4 | H | 1800 | UNSATISFIABLE | 28.18 | 14.0 | 118.9 | 0.22 | 2645.96 | True |
| 363 | P3_6-12 | P3 | Q | 2097 | UNSATISFIABLE | 1688.13 | 82.0 | 447.7 | 5.03 | 4405.16 | True |
| 413 | P3_1-6-12 | P3 | H | 1800 | not reached | | | | | | |
| 463 | P3_1-13-14 | P3 | H | 1800 | not reached | | | | | | |
| 513 | P3_4-9-10 | P3 | H | 1800 | not reached | | | | | | |
| 563 | P3_5-8-13 | P3 | H | 1800 | not reached | | | | | | |
| 613 | P3_6-12-13 | P3 | H | 1800 | not reached | | | | | | |

Counts by case/kind/status:
- P3 H not reached: 5
- P3 Q certified: 1
- P4 H certified: 5
- P4 Q certified: 1
- P5 Q certified: 1

Certified 8 (min / median / max): solve s 26.84 / 377.2 / 1688.13; lrat-check s 13.8 / 58.55 / 82; cake_lpr s 118.3 / 339.45 / 447.7; proof GB 0.22 / 3.395 / 5.03 (min / median / max)
Largest solver RSS: 4410.5 MB

Summary: 8 certified (P5 Q 1, P4 Q 1, P4 H 5, P3 Q 1), 0 timed out (UNKNOWN), 5 not reached (P3 H 5:
P3_1-6-12, P3_1-13-14, P3_4-9-10, P3_5-8-13, P3_6-12-13), 0 errors. The lane stopped at 15:09:19Z with 447 s left
before END (less than the 15 min needed to start a unit).

No SAT, no proof rejection (every proof accepted by both lrat-check and cake_lpr at heap 8000 MB), no memory problem
(largest solver RSS about 4.4 GB, under 15 GB). Proofs were deleted after checking; no CNF or proof files committed.

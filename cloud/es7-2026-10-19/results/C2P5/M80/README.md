# C2P5 M80: LIST = C2P5B.tsv, shard j = 30 of N = 50, H = 5.25 h (TASK commit 81cb025f)

## Tools and checks
- Built from the vendored sources with `C2P/vendor/build_tools.sh`: manifest (196 files) matches; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`. Nothing was cloned or downloaded.
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json both as expected.
- Cubes P1..P8 from `l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details in `tools.txt`; run command in `run.sh` (start 15:10:37Z, END 20:10:37Z).

## Units (19 = rows with idx ≡ 30 mod 50)
- **Certified: 19 of 19** (UNSAT, accepted by lrat-check and by cake_lpr). Timed out (UNKNOWN): 0. Not reached: 0. Errors / `certified: false`: 0.
- By case and kind: P1 H: 5, P1 Q: 1, P2 H: 6, P2 Q: 1, P3 H: 5, P3 Q: 1
- The last units got caps reduced by the END limit (P3_7-10 4210 s, P3_4-9-15 1752 s, P3_5-9-12 668 s, P3_7-8-13 387 s); all finished within them.

Certified units, minimum / median / maximum:
- solve: 21.48 / 318.18 / 2757.56 s
- lrat-check: 11.8 / 51.4 / 89.0 s
- cake_lpr: 109.8 / 339.8 / 578.9 s
- proof size: 0.22 GB / 3.27 GB / 5.90 GB

| unit | case | kind | cap s | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|
| P2_4-15 | P2 | Q | 8000 | 2757.56 | 86.9 | 577.2 | 5898151982 | 4383.7 |
| P1_3-14 | P1 | Q | 8000 | 2626.52 | 89.0 | 578.9 | 5680876560 | 4438.77 |
| P2_1-4-10 | P2 | H | 2400 | 577.39 | 54.4 | 360.0 | 3542540802 | 4408.78 |
| P2_3-4-12 | P2 | H | 2400 | 318.18 | 51.3 | 339.8 | 3242921433 | 4414.66 |
| P2_3-8-12 | P2 | H | 2400 | 411.23 | 59.4 | 374.8 | 3342388854 | 4368.95 |
| P2_4-6-8 | P2 | H | 2400 | 30.87 | 12.8 | 123.3 | 218800710 | 2651.74 |
| P2_4-13-14 | P2 | H | 2400 | 385.62 | 54.2 | 362.8 | 3319464955 | 4396.56 |
| P2_6-7-13 | P2 | H | 2400 | 33.49 | 13.5 | 120.5 | 217403164 | 2648.1 |
| P1_2-5-8 | P1 | H | 2400 | 88.61 | 23.4 | 185.7 | 1162506013 | 3186.77 |
| P1_2-11-14 | P1 | H | 2400 | 418.4 | 53.5 | 357.8 | 3461090410 | 4372.04 |
| P1_3-8-13 | P1 | H | 2400 | 443.19 | 51.8 | 349.9 | 3346268822 | 4366.75 |
| P1_4-9-11 | P1 | H | 2400 | 103.65 | 27.6 | 202.2 | 1330753495 | 3406.67 |
| P1_7-8-11 | P1 | H | 2400 | 21.48 | 12.0 | 117.0 | 217108774 | 2647.38 |
| P3_7-10 | P3 | Q | 4210 | 670.19 | 54.4 | 358.7 | 3518618699 | 4405.93 |
| P3_1-7-8 | P3 | H | 2400 | 310.15 | 48.2 | 321.7 | 3220600004 | 4407.09 |
| P3_1-15-16 | P3 | H | 2400 | 281.35 | 51.4 | 325.4 | 3271909654 | 4406.94 |
| P3_4-9-15 | P3 | H | 1752 | 662.16 | 53.8 | 351.7 | 3712502276 | 4375.0 |
| P3_5-9-12 | P3 | H | 668 | 84.19 | 22.2 | 170.2 | 1195698606 | 3186.98 |
| P3_7-8-13 | P3 | H | 387 | 22.07 | 11.8 | 109.8 | 216576376 | 2646.07 |

## Resources and problems
- Largest solver RSS: 4438.77 MB (machine: 4 cores, 15 GB RAM, no swap). No memory problem.
- Largest proof 5.90 GB; free disk never below 22 GB.
- No SAT, no proof rejection, no error. Proofs deleted after checking; no CNF or proof files committed.


# C2P3 M40 (LIST C2P3.tsv, shard j = 40 of N = 50, H = 2.5, TASK commit 4f653319)

Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Lane run from 09:45:55Z to 11:47:55Z, END = 1793447871 (11:57:51Z) (`run.sh`).

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only: all 196 manifest files match. CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity: the cake_lpr example prints `s VERIFIED UNSAT`. The bad LRAT is rejected by both checkers and the good one is accepted by both.
- Base CNF: header `p cnf 838032 16653336`. Both sha256 match (base.cnf b0061e90…, base.json 2476faff…).
- Cubes P1..P8: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (9, idx ≡ 40 mod 50)
| case | kind | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|
| P6 | Q | 1 (P6_3-7) | 0 | 0 | 0 |
| P6 | H | 2 (P6_2-8-14, P6_7-9-11) | 0 | 0 | 0 |
| P5 | H | 3 (P5_1-2-3, P5_1-7-14, P5_2-3-7) | 0 | 2 (P5_6-10-12, P5_7-12-14) | 0 |
| P5 | Q | 0 | 1 (P5_2-11, cap cut to 1301 s by END) | 0 | 0 |
| total | | 6 | 1 | 2 | 0 |

| unit | solve s | lrat-check s | cake_lpr s | proof GB |
|---|---|---|---|---|
| P6_3-7 (Q) | 2022.8 | 76.9 | 472.5 | 5.19 |
| P6_2-8-14 | 757.1 | 57.9 | 362.7 | 3.75 |
| P6_7-9-11 | 27.7 | 11.8 | 122.5 | 0.22 |
| P5_1-2-3 | 89.9 | 22.7 | 175.4 | 1.13 |
| P5_1-7-14 | 673.4 | 58.5 | 369.5 | 3.70 |
| P5_2-3-7 | 268.9 | 46.2 | 304.8 | 3.05 |

For the certified units (min / median / max): solve 27.7 / 471.1 / 2022.8 s, lrat-check 11.8 / 52.1 / 76.9 s, cake_lpr 122.5 / 333.8 / 472.5 s, proof 0.22 / 3.37 / 5.19 GB. Every certified unit was accepted by both checkers (`c VERIFIED`, `s VERIFIED UNSAT`, cake heap 8000 MB).

The largest solver RSS was 4424 MB (P6_3-7).

There was no SAT, no proof rejection, no error record and no memory problem. P5_2-11 is open (UNKNOWN after 1286 s, with the cap shortened by END). P5_6-10-12 and P5_7-12-14 were not reached.

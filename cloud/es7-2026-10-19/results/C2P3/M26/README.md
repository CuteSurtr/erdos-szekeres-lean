# C2P3 M26: shard j = 26 of N = 50 of `lists/C2P3.tsv` (TASK commit 4f653319, H = 2.5)

Start 2026-10-31 09:43:01Z (epoch 1793439781); END = start + 2.5 h - 15 min = 11:58:01Z (1793447881). One lane (`run.sh`), 4 cores and 15 GB.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 files match the manifest. It builds CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch) from the vendored sources. Nothing was cloned or downloaded.
- Sanity checks: lrat-check and cake_lpr both reject the bad LRAT and both accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: `p cnf 838032 16653336`. Both sha256 values match: base.cnf b0061e90…d8ff1 and base.json 2476faff…bf472b48.
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (`units.tsv`, 10 rows)
| unit | case | kind | cap | result | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P6_1-5 | P6 | Q | 6000 | certified UNSAT | 3048.97 | 88.5 | 530.4 | 6315940076 | 4370 |
| P6_8-12 | P6 | Q | 4800 (lane cap 3506) | certified UNSAT | 1599.29 | 68.8 | 415.4 | 4638225410 | 4374 |
| P6_2-3-12 | P6 | H | 1800 (lane cap 1392) | certified UNSAT | 382.84 | 46.7 | 306.1 | 3368513830 | 4364 |
| P6_3-9-13 | P6 | H | 1800 (lane cap 643) | certified UNSAT | 528.95 | 52.3 | 341.7 | 3569154151 | 4372 |
| P6_8-11-15 | P6 | H | 1800 | not reached | | | | | |
| P5_1-6-10, P5_1-12-15, P5_2-9-10, P5_6-8-13, P5_7-9-15 | P5 | H | 1800 | not reached | | | | | |

The lane capped some solves below the listed cap so that time remained for the checks before END. Each of those units still finished within its lane cap.

Counts by case and kind:
- Certified: 4 (P6 Q 2, P6 H 2).
- Timed out (UNKNOWN): 0.
- Errors or `certified: false`: 0.
- Not reached: 6 (P6 H 1, P5 H 5). The lane stopped at 11:52:55Z with 305 s left before END.

Certified units, given as min / median / max:
- solve: 382.84 / 1064.12 / 3048.97 s
- lrat-check: 46.7 / 60.55 / 88.5 s
- cake_lpr: 306.1 / 378.55 / 530.4 s
- proof size: 3.37 / 4.10 / 6.32 GB (the proofs are deleted after checking)

Largest solver RSS: 4374 MB (P6_8-12). cake_lpr used its 8000 MB heap.

No SAT. No proof was rejected. There was no memory problem, and disk stayed at 22 GB or more free.

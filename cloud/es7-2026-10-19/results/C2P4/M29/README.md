# C2P4 M29

Machine M29 of the fourth wave on the parallelogram cases (task `results/C2P4/TASK.md`, commit a46b478d): LIST = `C2P4.tsv`, j = 29, N = 50, H = 2.5. Start 2026-10-31 13:01:33Z, END 15:16:33Z; the lane stopped at 15:01:53Z with 879 s left (under 15 minutes, so no further unit was started).

## Tools and checks (`tools.txt`)

- `C2P/vendor/build_tools.sh` built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch) from the vendored `tools-src.tar.xz`; the manifest check passed (all 196 files match). Nothing was cloned or downloaded.
- Sanity: the bad LRAT was rejected by both checkers, the good one accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf and base.json match the expected values.
- Cubes P1..P8 from `C2C34/l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (14: idx ≡ 29 mod 50)

- Certified UNSAT: **9**
- Timed out (UNKNOWN): 0
- Errors / not certified: 0
- Not reached: 5 (P4_2-6-8, P4_5-8-10, P4_6-8-15, P3_1-5, P3_8-11)

By case and kind:

| case | kind | certified | not reached |
|---|---|---|---|
| P3 | Q | 0 | 2 |
| P4 | H | 2 | 3 |
| P4 | Q | 1 | 0 |
| P5 | H | 4 | 0 |
| P5 | Q | 1 | 0 |
| P6 | H | 1 | 0 |

Per unit:

| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P5_6-8 | P5 | Q | 6000 | UNSATISFIABLE (certified) | 563.26 | 61.5 | 350.8 | 3.54 | 4411 |
| P6_7-12-15 | P6 | H | 1800 | UNSATISFIABLE (certified) | 251.35 | 52.6 | 302.0 | 3.17 | 4347 |
| P5_1-13-14 | P5 | H | 1800 | UNSATISFIABLE (certified) | 224.74 | 51.4 | 307.3 | 3.19 | 4359 |
| P5_2-12-13 | P5 | H | 1800 | UNSATISFIABLE (certified) | 250.26 | 52.8 | 295.9 | 3.21 | 4364 |
| P5_6-11-13 | P5 | H | 1800 | UNSATISFIABLE (certified) | 186.2 | 50.2 | 292.5 | 3.10 | 4386 |
| P5_8-9-11 | P5 | H | 1800 | UNSATISFIABLE (certified) | 27.9 | 13.2 | 116.1 | 0.22 | 2646 |
| P4_2-6 | P4 | Q | 3791 | UNSATISFIABLE (certified) | 1318.34 | 77.0 | 463.8 | 4.86 | 4418 |
| P4_1-2-13 | P4 | H | 1800 | UNSATISFIABLE (certified) | 305.8 | 57.0 | 314.4 | 3.22 | 4357 |
| P4_1-8-13 | P4 | H | 1217 | UNSATISFIABLE (certified) | 501.92 | 61.4 | 360.4 | 3.62 | 4362 |
| P4_2-6-8 | P4 | H | 1800 | not reached | | | | | |
| P4_5-8-10 | P4 | H | 1800 | not reached | | | | | |
| P4_6-8-15 | P4 | H | 1800 | not reached | | | | | |
| P3_1-5 | P3 | Q | 6000 | not reached | | | | | |
| P3_8-11 | P3 | Q | 6000 | not reached | | | | | |

Certified units, minimum / median / maximum:

- solve s: 27.9 / 251.3 / 1318.3
- lrat-check s: 13.2 / 52.8 / 77.0
- cake_lpr s: 116.1 / 307.3 / 463.8
- proof GB: 0.2 / 3.2 / 4.9

## Other

- Largest solver RSS: 4418 MB (P4_2-6).
- No SAT, no proof rejection, no error record, no memory problem. Every proof was accepted by both lrat-check and cake_lpr and then deleted.
- The caps of P4_2-6 (3791 s) and P4_1-8-13 (1217 s) were shortened by lane.py to the time left before END; both finished well within them.

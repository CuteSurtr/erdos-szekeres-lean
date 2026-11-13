# C2P5 M85 — LIST C2P5B.tsv, shard j=35 of N=50, H=5.25 (TASK.md @ 81cb025f)

**Result: all 14 units certified UNSAT (lrat-check and cake_lpr both accepted every proof). No SAT, no timeouts, no units left unreached, no errors, no proof rejections, no memory problems.**

## Tools and checks (details in tools.txt)
- `C2P/vendor/build_tools.sh` built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc + E2 patch) from the vendored `tools-src.tar.xz`. The manifest check passed (all 196 files match). Sanity: both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example printed `s VERIFIED UNSAT`. No code was cloned or downloaded.
- Base CNF: header `p cnf 838032 16653336`; base.cnf sha256 b0061e90…d8ff1 and base.json sha256 2476faff…bf472b48 both match.
- Cubes P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Run
- One lane (run.sh), started at 15:12Z with END = 1793477429 (20:10:29Z). It finished every unit at 18:36:40Z.
- P3_8-10 was the last unit. The lane capped its solve at 5998 s because of END, but it solved in 543 s.

## Units (14)
- Certified: 14. By case and kind: P1 Q 1, P1 H 4; P2 Q 1, P2 H 6; P3 Q 2.
- Timed out (UNKNOWN): 0. Not reached: 0. Errors or `certified: false`: 0.

| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof | RSS MB | certified |
|---|---|---|---|---|---|---|---|---|---|---|
| P2_5-10 | P2 | Q | 8000 | UNSATISFIABLE | 1194.64 | 72.6 | 439.3 | 4.26 GB | 4376 | True |
| P1_4-8 | P1 | Q | 8000 | UNSATISFIABLE | 711.98 | 73.9 | 403.1 | 3.64 GB | 4419 | True |
| P2_1-4-15 | P2 | H | 2400 | UNSATISFIABLE | 472.31 | 64.1 | 376.9 | 3.48 GB | 4421 | True |
| P2_3-5-6 | P2 | H | 2400 | UNSATISFIABLE | 90.95 | 26.4 | 179.7 | 1.19 GB | 3178 | True |
| P2_3-9-10 | P2 | H | 2400 | UNSATISFIABLE | 234.51 | 55.3 | 332.0 | 3.10 GB | 4368 | True |
| P2_4-6-13 | P2 | H | 2400 | UNSATISFIABLE | 313.36 | 62.9 | 340.6 | 3.24 GB | 4376 | True |
| P2_5-6-11 | P2 | H | 2400 | UNSATISFIABLE | 30.26 | 14.0 | 118.0 | 0.22 GB | 2648 | True |
| P2_6-8-13 | P2 | H | 2400 | UNSATISFIABLE | 133.81 | 35.5 | 227.8 | 1.82 GB | 3457 | True |
| P1_2-5-13 | P1 | H | 2400 | UNSATISFIABLE | 431.38 | 66.2 | 369.0 | 3.42 GB | 4381 | True |
| P1_2-13-14 | P1 | H | 2400 | UNSATISFIABLE | 332.05 | 64.4 | 367.7 | 3.41 GB | 4376 | True |
| P1_3-9-12 | P1 | H | 2400 | UNSATISFIABLE | 286.75 | 57.5 | 324.7 | 3.18 GB | 4394 | True |
| P1_4-10-12 | P1 | H | 2400 | UNSATISFIABLE | 143.01 | 34.9 | 213.8 | 1.71 GB | 3439 | True |
| P3_1-4 | P3 | Q | 8000 | UNSATISFIABLE | 1811.77 | 89.0 | 505.8 | 5.28 GB | 4388 | True |
| P3_8-10 | P3 | Q | 5998 | UNSATISFIABLE | 543.48 | 63.8 | 347.9 | 3.35 GB | 4356 | True |

Certified by case/kind: P1 H: 4, P1 Q: 1, P2 H: 6, P2 Q: 1, P3 Q: 2

Certified units (min / median / max):
- solve s: 30.26 / 322.71 / 1811.77
- lrat-check s: 14.0 / 63.35 / 89.0
- cake_lpr s: 118.0 / 344.25 / 505.8
- proof size: 0.22 GB / 3.30 GB / 5.28 GB

Largest solver RSS: 4421 MB (P2_1-4-15).

Disk: each proof was deleted after it was checked. Solver RSS peaked at about 4.4 GB, and the largest cake_lpr heap was 8000 MB, inside the 15 GB machine.

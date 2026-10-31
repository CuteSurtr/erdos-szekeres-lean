# C2P3 M47

TASK `results/C2P3/TASK.md` at 4f653319, V = M47, LIST = C2P3.tsv, j = 47, N = 50, H = 2.5.
Start 2026-10-31 09:42:44 UTC (epoch 1793439764), END = 1793447864 (11:57:44 UTC). Machine: 4 cores, 15 GB RAM (`env.txt`).

## Tools and checks (`tools.txt`)
- Built by `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz` only (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 base.cnf b0061e90…d8ff1 and base.json 2476faff…bb472b48, as required.
- Cubes P1..P8 from `l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (9; `units.tsv`, records in `out.jsonl`)

| unit | case | kind | cap s | result | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P6_7-14 | P6 | Q | 6000 | certified UNSAT | 4996.16 | 114.9 | 658.2 | 7 989 456 924 | 4372 |
| P6_2-10-15 | P6 | H | 1502 (trimmed) | certified UNSAT | 514.20 | 49.8 | 333.4 | 3 565 598 597 | 4366 |
| P6_7-10-13 | P6 | H | 588 (trimmed) | certified UNSAT | 25.77 | 10.7 | 109.7 | 215 997 896 | 2675 |
| P5_1-2-11 | P5 | H | 440 (trimmed) | certified UNSAT | 386.41 | 51.1 | 313.3 | 3 317 661 881 | 4407 |
| P5_1-8-12, P5_2-6-8, P5_2-12-13, P5_6-11-13, P5_8-9-11 | P5 | H | 1800 | not reached | | | | | |

By case and kind:
- P6 Q: 1 certified.
- P6 H: 2 certified.
- P5 H: 1 certified, 5 not reached (lane stopped at 11:53:08Z with 275 s left before END).
- Timed out (UNKNOWN): 0. Errors / `certified: false`: 0.

Certified units (4), min / median / max:
- solve: 25.77 / 450.31 / 4996.16 s
- lrat-check: 10.7 / 50.45 / 114.9 s
- cake_lpr: 109.7 / 323.35 / 658.2 s
- proof size: 0.216 / 3.442 / 7.989 GB

The caps of the 2nd–4th units were reduced by lane.py to fit END; all three still finished UNSAT within them.

## Resources and anomalies
- Largest solver RSS: 4406.63 MB (P5_1-2-11). cake_lpr ran with an 8000 MB heap (about 8.2 GB RSS observed). No memory problem; disk peaked near 20 GB free.
- No SAT, no proof rejection, no errors. All proofs deleted after checking; no CNF or proof files committed.

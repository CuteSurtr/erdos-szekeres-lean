# C2P5 M26: C2P5A.tsv shard 26 of 37

Task: `results/C2P5/TASK.md` at commit 81cb025f, with V = M26, LIST = C2P5A.tsv, j = 26, N = 37, H = 4.5.
Machine: 4 cores, 15 GB RAM (`env.txt`). Start 19:11:08Z, lane END 1793489168 (23:26:08Z); the lane finished all units at 19:58:45Z.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest all 196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8,
  lrat-check 2e3b2dc + E2 patch, all built from `vendor/tools-src.tar.xz`. Nothing was cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf b0061e90…d8ff1 and base.json 2476faff…2b48, both as expected.
- Cubes P1..P8: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, `out.jsonl`)
5 units, all case P4: 1 Q (cap 8000 s), 4 H (cap 2400 s).

| unit | kind | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|
| P4_9-12 | Q | UNSAT, certified | 582.3 | 58.8 | 333.0 | 3.59 | 4400 |
| P4_2-6-9 | H | UNSAT, certified | 271.1 | 54.6 | 327.3 | 3.27 | 4405 |
| P4_5-6-9 | H | UNSAT, certified | 23.4 | 13.4 | 119.5 | 0.22 | 2652 |
| P4_5-11-14 | H | UNSAT, certified | 321.2 | 55.9 | 323.8 | 3.35 | 4362 |
| P4_7-8-9 | H | UNSAT, certified | 26.1 | 13.6 | 117.3 | 0.22 | 2647 |

By case and kind: P4 Q 1/1 certified; P4 H 4/4 certified. Timed out (UNKNOWN): 0. Not reached: 0. Errors: 0.

Certified units (min / median / max):
- solve s: 23.37 / 271.07 / 582.3
- lrat-check s: 13.4 / 54.6 / 58.8
- cake_lpr s: 117.3 / 323.8 / 333.0 (heap 8000 MB each time; no retry)
- proof bytes: 215,623,643 / 3,271,601,642 / 3,591,489,317

Largest solver RSS: 4405 MB (P4_2-6-9).

No SAT, no proof rejection, no memory problem.

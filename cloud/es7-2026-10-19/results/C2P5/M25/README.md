# C2P5 M25: list C2P5A.tsv, shard 25 of 37, H = 4.5, TASK commit 81cb025f

Start 2026-10-31 19:11:12Z (epoch 1793473872); END 1793489172 (23:26:12Z). Machine: 4 cores, 15 GB RAM (`env.txt`).
The lane finished all units at 20:07:37Z, well before END.

## Tools and checks (`tools.txt`)

- CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc, E2 patch), built by `C2P/vendor/build_tools.sh`
  from the vendored sources; manifest: all 196 files match. Nothing was cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…f2b48`, both as required.
- Cubes P1..P8: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, idx ≡ 25 mod 37)

| case | kind | units | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|---|---|
| P4 | H | 4 | 4 | 0 | 0 | 0 |
| P4 | Q | 1 | 1 | 0 | 0 | 0 |
| **all** | | 5 | 5 | 0 | 0 | 0 |

| unit | kind | cap s | solve s | lrat-check s | cake_lpr s | proof GB | solver RSS MB |
|---|---|---|---|---|---|---|---|
| P4_9-10 | Q | 8000 | 484.94 | 58.4 | 339.4 | 3.36 | 4363.57 |
| P4_2-6-8 | H | 2400 | 300.84 | 62.4 | 335.6 | 3.26 | 4367.2 |
| P4_5-6-7 | H | 2400 | 101.72 | 31.7 | 200.7 | 1.43 | 3435.2 |
| P4_5-11-13 | H | 2400 | 272.46 | 56.5 | 326.6 | 3.22 | 4371.03 |
| P4_6-13-14 | H | 2400 | 229.5 | 58.8 | 339.0 | 3.17 | 4352.16 |

Certified units (min / median / max): solve 101.72 / 272.46 / 484.94 s; lrat-check 31.7 / 58.4 / 62.4 s; cake_lpr 200.7 / 335.6 / 339.4 s;
proof size 1.43 / 3.22 / 3.36 GB.

All 5 units are UNSATISFIABLE and certified: `c VERIFIED` from lrat-check and `s VERIFIED UNSAT` from cake_lpr.

- Largest solver RSS: 4371.03 MB.
- No SAT answer, no proof rejection, no error and no memory problem.


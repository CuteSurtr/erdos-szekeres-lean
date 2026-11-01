# C2P5 M24: list C2P5A.tsv, shard j = 24 of N = 37, H = 4.5

TASK.md commit 81cb025f. Start 2026-10-31 19:11:10Z (epoch 1793473870), END 1793489170; the lane finished all units at 20:07:29Z.

## Tools and checks (`tools.txt`)

- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (CaDiCaL c6073042 = 3.0.1, cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch); manifest: all 196 files match.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 b0061e90…d8ff1 (base.cnf) and 2476faff…bf472b48 (base.json), both as required.
- Cubes P1..P8 from `C2C34/l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, idx ≡ 24 mod 37)

| unit | case | kind | cap s | status | certified | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|
| P4_6-8 | P4 | Q | 8000 | UNSATISFIABLE | True | 583.68 | 48.2 | 304.9 | 3.43 | 4406.36 |
| P4_2-6-7 | P4 | H | 2400 | UNSATISFIABLE | True | 233.84 | 43.3 | 281.9 | 3.22 | 4399.98 |
| P4_2-10-11 | P4 | H | 2400 | UNSATISFIABLE | True | 308.29 | 43.3 | 283.5 | 3.25 | 4412.82 |
| P4_5-11-12 | P4 | H | 2400 | UNSATISFIABLE | True | 203.78 | 44.6 | 275.0 | 3.08 | 4346.59 |
| P4_6-12-14 | P4 | H | 2400 | UNSATISFIABLE | True | 237.27 | 45.1 | 286.1 | 3.17 | 4346.31 |

Totals: 5 units, all in case P4: certified 5 (P4 Q: 1, P4 H: 4); timed out (UNKNOWN) 0; not reached 0; errors 0.

Certified units, min / median / max:
- solve seconds: 203.78 / 237.27 / 583.68
- lrat-check seconds: 43.3 / 44.6 / 48.2
- cake_lpr seconds: 275 / 283.5 / 304.9
- proof size GB: 3.08 / 3.22 / 3.43

Largest solver RSS: 4412.82 MB (P4_2-10-11), of 15 GB.

No SAT, no proof rejection, no error, no memory or disk problem (free disk stayed at or above about 24 GB). All proofs were deleted by the lane after checking; no CNF or proof files are committed.

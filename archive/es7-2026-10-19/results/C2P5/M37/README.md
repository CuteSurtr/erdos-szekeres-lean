# C2P5 M37

TASK `results/C2P5/TASK.md` at 81cb025f with V = M37, LIST = C2P5C.tsv, j = 0, N = 13, H = 4.5.
Start 2026-10-31 20:06:35Z (epoch 1793477195), END 1793492495 (2026-11-01 00:21:35Z). Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest, all 196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch) built from `vendor/tools-src.tar.xz`. Nothing was cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…2b48`. Both match.
- Cubes P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (rows of C2P5C.tsv with idx ≡ 0 mod 13)

| idx | unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | P1_5-12 | P1 | Q | 8000 | UNSAT, certified | 1312.67 | 67.5 | 380.1 | 4766208759 | 4403.8 |
| 13 | P3_1-11-15 | P3 | H | 2400 | UNSAT, certified | 279.0 | 48.4 | 298.6 | 3344030568 | 4369.4 |

- Counts: 2 certified (P1 Q: 1, P3 H: 1). None timed out (UNKNOWN), none were left unreached, and there were no errors.
- Certified units, as min / median / max:
  - solve: 279.0 / 795.8 / 1312.7 s
  - lrat-check: 48.4 / 58.0 / 67.5 s
  - cake_lpr: 298.6 / 339.4 / 380.1 s
  - proof size: 3.34 / 4.06 / 4.77 GB
- Largest solver RSS: 4403.8 MB (P1_5-12).
- There was no SAT, no proof rejection and no memory problem. Both proofs were deleted after checking.
- The lane finished at 20:49:22Z, well before END.

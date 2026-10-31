# C2P3 M29

Task `results/C2P3/TASK.md` at commit 4f653319, with V = M29, LIST = C2P3.tsv, j = 29, N = 50, H = 2.5.
Machine: 4 cores, 15 GB RAM (`env.txt`). Start 09:42:46Z, END = 11:57:46Z (1793447866). The lane finished at 11:54:01Z.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored sources: CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). All 196 files match `MANIFEST.sha256`. Nothing was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; the sha256 of base.cnf (b0061e90…) and base.json (2476faff…) match the expected values.
- Cubes P1..P8: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`: 10 rows, idx ≡ 29 mod 50)
| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P6_1-13 | P6 | Q | 6000 | UNSAT, certified | 1833.76 | 85.1 | 484.6 | 5.46 GB | 4370.5 |
| P6_8-15 | P6 | Q | 4800 | UNSAT, certified | 4320.82 | 130.8 | 688.1 | 8.39 GB | 4378.6 |

- Certified: 2. Both are P6 Q.
  - solve: min 1833.76, median 3077.3, max 4320.82 s.
  - lrat-check: min 85.1, median 108.0, max 130.8 s.
  - cake_lpr: min 484.6, median 586.4, max 688.1 s.
  - proof size: min 5,459,997,388, median 6,924,699,834, max 8,389,402,279 bytes.
- Timed out (UNKNOWN): 0.
- Errors / `certified: false`: 0.
- Not reached: 8, because time ran out after the second Q unit (the lane stopped with 224 s left before END):
  - P6 H: P6_2-4-8, P6_3-10-12, P6_8-13-14 (3).
  - P5 H: P5_1-6-13, P5_1-13-14, P5_2-9-13, P5_6-8-16, P5_7-10-12 (5).
- Largest solver RSS: 4378.6 MB. There were no memory problems: the peak system use was about 8 GB of 15, during cake_lpr with its 8000 MB heap. The largest proof (8.4 GB) fit on disk with no trouble.
- No SAT result and no proof rejection.

# C2P5 M22

TASK `results/C2P5/TASK.md` (commit 81cb025f) with V = M22, LIST = C2P5A.tsv (as on branch es7-cloud at the
start, commit 92a2b58ad), j = 22, N = 37, H = 4.5. Start 2026-10-31 18:50:27Z (epoch 1793472627),
END = 1793487927 (start + 4.5 h − 15 min). Lane started 18:52:57Z, finished 20:42:41Z ("lane done").

## Tools and checks (`tools.txt`)

- `C2P/vendor/build_tools.sh`: manifest all 196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8),
  lrat-check (2e3b2dc + E2 patch), built from the vendored sources only.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…2b48`, both match.
- Cubes: `l2cubes.py` output for P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, rows of C2P5A.tsv with idx ≡ 22 mod 37)

| idx | unit | case | kind | cap s | status | certified | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 22 | P4_5-13 | P4 | Q | 8000 | UNSAT | yes | 3008.16 | 104.1 | 585.7 | 6609651656 | 4379.6 |
| 59 | P4_2-5-15 | P4 | H | 2400 | UNSAT | yes | 406.14 | 61.1 | 341.2 | 3556522963 | 4428.1 |
| 96 | P4_2-9-11 | P4 | H | 2400 | UNSAT | yes | 304.51 | 57.0 | 310.5 | 3294476410 | 4395.5 |
| 133 | P4_5-10-14 | P4 | H | 2400 | UNSAT | yes | 345.46 | 59.4 | 322.4 | 3337876281 | 4361.3 |
| 170 | P4_6-11-14 | P4 | H | 2400 | UNSAT | yes | 218.28 | 58.3 | 309.1 | 3155022360 | 4391.5 |

Counts by case and kind:

| case | kind | units | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|---|---|
| P4 | Q | 1 | 1 | 0 | 0 | 0 |
| P4 | H | 4 | 4 | 0 | 0 | 0 |
| total | | 5 | 5 | 0 | 0 | 0 |

Certified units (all 5), min / median / max:
- solve: 218.28 / 345.46 / 3008.16 s
- lrat-check: 57.0 / 59.4 / 104.1 s
- cake_lpr: 309.1 / 322.4 / 585.7 s
- proof size: 3.16 / 3.34 / 6.61 GB (3155022360 / 3337876281 / 6609651656 bytes)

Largest solver RSS: 4428.1 MB (P4_2-5-15). cake_lpr peaked at about 8.2 GB RSS (heap 8000 MB).

No SAT, no proof rejection, no `certified: false` record, no ERROR status and no memory problem.
Every unit has `lrat_check` = `c VERIFIED` and `cake_lpr` = `s VERIFIED UNSAT`; all proofs were deleted by the lane.
The lane finished all its units about 1 h 45 min before END.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl`, `lane.log.tail`.

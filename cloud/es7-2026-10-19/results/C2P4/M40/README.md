# C2P4 M40: shard 40 of 50 of `lists/C2P4.tsv`

Task: `results/C2P4/TASK.md` at a46b478d, with V = M40, LIST = C2P4.tsv, j = 40, N = 50, H = 2.5.
Start 2026-10-31 13:01:37 UTC (1793451697), END = 1793459797 (15:16:37 UTC). One lane (`run.sh`), 4 cores, 15 GB RAM.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built from the vendored sources only (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. Nothing was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one; the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…2b48`, both as expected.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (19 rows with idx ≡ 40 mod 50)

| case | kind | units | certified | timed out | not reached | errors |
|---|---|---|---|---|---|---|
| P5 | Q | 1 | 1 | 0 | 0 | 0 |
| P5 | H | 5 | 5 | 0 | 0 | 0 |
| P4 | Q | 1 | 1 | 0 | 0 | 0 |
| P4 | H | 5 | 0 | 0 | 5 | 0 |
| P3 | Q | 1 | 0 | 0 | 1 | 0 |
| P3 | H | 6 | 0 | 0 | 6 | 0 |
| **total** | | 19 | **7** | 0 | 12 | 0 |

Certified (UNSAT, accepted by both lrat-check and cake_lpr): P5_7-12, P5_1-3-16, P5_2-7-8, P5_6-7-11, P5_7-8-10, P5_8-12-13, P4_5-12.
The lane reduced P4_5-12's cap from 6000 s to 2832 s so that 10 minutes would remain for the checks. It solved the unit in 2428 s.

Not reached: the lane stopped at 15:10:49 UTC with 347 s left before END. These 12 units are P4_1-5-7, P4_1-10-11, P4_2-7-11, P4_5-9-14, P4_6-10-15, P3_1-16, P3_1-4-5, P3_1-8-11, P3_4-5-16, P3_4-11-15, P3_5-11-14 and P3_8-9-12.

| certified (7) | min | median | max |
|---|---|---|---|
| solve s | 20.4 | 245.5 | 2427.8 |
| lrat-check s | 12.2 | 51.6 | 100.2 |
| cake_lpr s | 106.5 | 300.0 | 520.6 |
| proof size | 0.21 GB | 3.22 GB | 6.02 GB |

Per kind: the two Q units took 2079 s and 2428 s to solve, with 5.4 GB and 6.0 GB proofs. The five H units took 20–251 s, with 0.21–3.23 GB proofs.

Largest solver RSS: 4416 MB (P5_2-7-8).

No SAT, no proof rejection, no ERROR record, and no memory or disk problem. Free disk never went below 22 GB.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (7 records), `lane.log.tail`.

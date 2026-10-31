# C2P3 M27 (LIST = C2P3.tsv, j = 27, N = 50, H = 2.5, task commit 4f653319)

Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 09:42:44Z, lane END 11:57:44Z (start + 2.5 h - 15 min); the lane finished at 11:47:50Z.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored `tools-src.tar.xz` (all MANIFEST hashes match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing was cloned or downloaded.
- Sanity checks: lrat-check and cake_lpr both rejected the bad LRAT and both accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF `SYMZ/zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`; sha256 of base.cnf `b0061e90…d8ff1` and of base.json `2476faff…f2b48`. Both match.
- Cubes P1..P8 from `C2C34/l2cubes.py`: each is byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (`units.tsv`: idx ≡ 27 mod 50, 10 units)
| unit | case | kind | cap | result |
|---|---|---|---|---|
| P6_1-7 | P6 | Q | 6000 | UNKNOWN (timed out), solve 5937.9 s, RSS 4377 MB |
| P6_8-13 | P6 | Q | 4800 (lane cap 1328) | UNKNOWN (timed out), solve 1314.0 s, RSS 4472 MB |
| P6_2-3-16, P6_3-9-14, P6_8-12-13 | P6 | H | 1800 | not reached |
| P5_1-6-11, P5_1-12-16, P5_2-9-11, P5_6-8-14 | P5 | H | 1800 | not reached |
| P5_7-10 | P5 | Q | 2400 | not reached |

Counts:
- Certified: 0.
- Timed out: 2, both P6/Q.
- Not reached: 8, namely P6/H 3, P5/H 4 and P5/Q 1.
- Errors: 0.

No unit was certified, so there are no check times or proof sizes to summarize. Both proofs were deleted after the timeouts. The P6_1-7 proof had grown to about 8.3 GB when its cap was hit.

## Resources and anomalies
- Largest solver RSS: 4472 MB (P6_8-13). There were no memory problems, and free disk never fell below 20 GB.
- No SAT answer, no proof rejection, and no record with `"certified": false` or an ERROR status.
- P6_8-13 ran under a reduced cap of 1328 s, not 4800 s, because lane.py leaves room for the checks before END. Its timeout therefore says less than a timeout at the full cap would.

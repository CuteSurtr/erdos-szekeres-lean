# C2P2 M22: shard 22 of 42 of C2P2.tsv

TASK `results/C2P2/TASK.md` at commit d266d2c3. V = M22, LIST = C2P2.tsv, j = 22, N = 42, H = 2.5. Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-31 06:47:02 UTC (epoch 1793429222); END = 1793437322 (09:02:02 UTC). One lane (`run.sh`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch) from the vendored `tools-src.tar.xz`. All 196 files matched `MANIFEST.sha256`, and no code was cloned or downloaded.
- Sanity checks passed. Both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: the header is `p cnf 838032 16653336`, and both sha256 values match (base.cnf `b0061e90…`, base.json `2476fafff…`).
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (8 rows with idx ≡ 22 mod 42)

| idx | unit | kind | list cap | effective cap | result |
|---|---|---|---|---|---|
| 22 | P7_1-8 | Q | 6000 | 6000 | **UNSAT, certified**, solve 5388.9 s |
| 64 | P6_1-3-14 | H | 1800 | 945 | **UNSAT, certified**, solve 230.1 s |
| 106 | P6_1-9-14 | H | 1800 | 366 | UNKNOWN (stopped at a reduced cap of 366 s, not at its full cap) |
| 148 | P6_2-3-16 | H | 1800 | – | not reached |
| 190 | P6_2-11-14 | H | 1800 | – | not reached |
| 232 | P6_3-10-12 | H | 1800 | – | not reached |
| 274 | P6_7-16 | Q | 2400 | – | not reached |
| 316 | P6_10-13 | Q | 2400 | – | not reached |

Counts:
- P7 Q: 1 certified.
- P6 H: 1 certified, 1 UNKNOWN (reduced cap) and 3 not reached.
- P6 Q: 2 not reached.
- Overall: 2 certified, 1 UNKNOWN, 5 not reached, 0 errors.

P7_1-8 timed out at its full cap in the first wave. Here it closed in 5389 s, just under the 6000 s cap. The lane reduced the caps of the later units because the budget was running out (it keeps 10 minutes for the checks).

## Certified units

| unit | solve s | lrat-check s | cake_lpr s | proof bytes |
|---|---|---|---|---|
| P7_1-8 | 5388.9 | 151.6 | 767.1 | 10,130,535,769 |
| P6_1-3-14 | 230.1 | 50.0 | 288.3 | 3,217,341,666 |

Minimum / median / maximum over these two units:
- solve: 230.1 / 2809.5 / 5388.9 s
- lrat-check: 50.0 / 100.8 / 151.6 s
- cake_lpr: 288.3 / 527.7 / 767.1 s
- proof size: 3.22 / 6.67 / 10.13 GB

Both checkers accepted both proofs (`c VERIFIED`, `s VERIFIED UNSAT`). The proofs were deleted after checking.

## Memory, SAT and rejections
- The largest solver RSS was 4370 MB (P7_1-8). cake_lpr peaked at about 8.2 GB RSS (heap 8000 MB). There were no memory problems, and the minimum free disk space was about 18 GB.
- There was no SAT answer, no proof rejection and no ERROR record.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl`, `lane.log.tail`.

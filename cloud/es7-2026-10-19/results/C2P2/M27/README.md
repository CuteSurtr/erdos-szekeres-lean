# C2P2 M27: shard 27 of 42 of C2P2.tsv

Task `results/C2P2/TASK.md` at commit d266d2c3, with V = M27, LIST = C2P2.tsv, j = 27, N = 42 and H = 2.5. Start 2026-10-31 06:46:47Z (epoch 1793429207). END = 1793437307 (09:01:47Z). Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored sources; no code was cloned or downloaded. `vendor/MANIFEST.sha256`: all 196 files match.
  - CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch).
- Sanity checks passed. Both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and of base.json (2476faff…) both match the expected values.
- Cubes P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (`units.tsv`, 7 units: idx ≡ 27 mod 42)
| status | count | by case / kind |
|---|---|---|
| certified (UNSAT, both checkers accepted) | 2 | P7 Q: 1 (P7_2-10); P6 H: 1 (P6_1-4-8) |
| timed out (UNKNOWN) | 0 | — |
| not reached | 5 | P6 H: 5 (P6_1-10-12, P6_2-4-10, P6_2-12-14, P6_7-8-10, P6_8-9-13) |
| errors / certified false | 0 | — |

The lane stopped at 08:51:02Z with 644 s left before END, which is less than the 15-minute minimum to start a unit. P6_1-4-8 ran with its cap reduced from 1800 s to 831 s so that 10 minutes remained for the checks. It finished in 385 s.

### Certified units
| unit | case | kind | cap | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|
| P7_2-10 | P7 | Q | 6000 | 5493.76 | 158.8 | 825.1 | 8,640,035,599 | 4403.68 |
| P6_1-4-8 | P6 | H | 831 | 384.68 | 57.4 | 331.3 | 3,320,793,419 | 4375.5 |

Over the 2 certified units (min / median / max), with the median of two taken as their mean:
- solve: 384.7 / 2939.2 / 5493.8 s;
- lrat-check: 57.4 / 108.1 / 158.8 s;
- cake_lpr: 331.3 / 578.2 / 825.1 s;
- proof size: 3.32 / 5.98 / 8.64 GB.

P7_2-10 is one of the quadrilateral subcases that timed out at its full cap in the first wave. Here it was solved within its 6000 s cap.

## Resources and anomalies
- Largest solver RSS: 4403.68 MB (P7_2-10).
- No SAT, no proof rejections and no memory problems. Peak disk use came from the 8.6 GB proof, with about 22 GB still free; the lane deleted each proof after its checks.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl`, `lane.log.tail`.

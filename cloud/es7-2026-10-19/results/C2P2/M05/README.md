# C2P2 M05 (LIST = C2P2.tsv, j = 5, N = 42, H = 2.5, task commit d266d2c3)

Start 2026-10-31 06:46:56Z (epoch 1793429216); END = start + 2.5 h - 15 min = 1793437316 (09:01:56Z).
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). One lane only (`run.sh`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 vendored files match `MANIFEST.sha256`. It built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch). Nothing was cloned or downloaded.
- Sanity checks: the bad LRAT was rejected by both checkers; the good LRAT was accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`). The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…b48`, both as expected.
- Cubes: P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, idx ≡ 5 mod 42: 8 units)
| unit | case | kind | cap | result |
|---|---|---|---|---|
| P8_2-9 | P8 | Q | 6000 | **certified** UNSAT |
| P6_1-2-10 | P6 | H | 1800 (run at 977, the time left) | **certified** UNSAT |
| P6_1-7-13 | P6 | H | 1800 | not reached |
| P6_1-14 | P6 | Q | 2400 | not reached |
| P6_2-9 | P6 | Q | 2400 | not reached |
| P6_3-7-15 | P6 | H | 1800 | not reached |
| P6_7-10-16 | P6 | H | 1800 | not reached |
| P6_8-15 | P6 | Q | 2400 | not reached |

Counts:
- Certified: 2 (P8 Q: 1, P6 H: 1).
- Timed out (UNKNOWN): 0.
- Errors: 0.
- Not reached: 6 (P6 H: 3, P6 Q: 3). The lane stopped at 08:47:57Z with 838 s left, under the 15-minute rule.

Certified units (min / median / max over 2):
- solve: 362.1 / 1879.0 / 5395.88 s. P8_2-9 was a first-wave full-cap timeout and closed here at 5396 s, under the 6000 s cap.
- lrat-check: 55.3 / 99.1 / 142.8 s.
- cake_lpr: 309.0 / 528.2 / 747.4 s, with an 8000 MB heap.
- proof size: 3.34 / 6.35 / 9.36 GB (3341078333 and 9364440143 bytes). Both proofs were deleted after checking.

## Resources and anomalies
- Largest solver RSS: 4420.87 MB (P8_2-9). cake_lpr used about 8.2 GB RSS. There was no memory problem.
- Disk: the 9.4 GB proof left about 19 GB free.
- No SAT, no proof rejection, no `certified: false` and no ERROR records.

Files: `out.jsonl` (2 records), `lane.log.tail`, `tools.txt`, `units.tsv`, `run.sh`, `env.txt`.

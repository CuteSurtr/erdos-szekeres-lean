# C2P / M39 (LIST C2P.tsv, shard 39 of 42, H = 3.0, Z = 01909a07)

This attempt replaces the earlier M39 files from a run that stopped at step 1.

**Result: 13 units certified, 1 timed out (UNKNOWN), 39 not reached. No SAT. No proof was rejected. No errors.**

## Tools and checks (`tools.txt`)
- The tools were built with `C2P/vendor/build_tools.sh` from the vendored sources. All 196 manifest files match. Nothing was cloned or downloaded.
  - CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, and lrat-check 2e3b2dc with the E2 patch.
- Sanity checks: lrat-check and cake_lpr both rejected the bad LRAT and both accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: the header is `p cnf 838032 16653336`, and the sha256 of base.cnf and of base.json both match.
- Cubes: P1..P8 are all byte-identical to `C2P/cubes`.

## Units (53: P1 6H+1Q, P2 6H+1Q, P3 5H+2Q, P4 6H+1Q, P5 4H+2Q, P6 6H+1Q, P7 6H+1Q, P8 5H; no cover)
The lane started at 03:24:58Z, with END = 06:07:43Z (1793426863). It stopped at 06:01:30Z with 372 s left.

| case | certified | UNKNOWN | not reached |
|---|---|---|---|
| P8 | 5 H | – | – |
| P7 | 6 H | 1 Q (P7_1-8) | – |
| P6 | 2 H (P6_1-2-8, P6_2-9-12) | – | 4 H, 1 Q |
| P5..P1 | – | – | 31 H, 8 Q (all 39) |

- Certified: 13 units, all H. lrat-check gave `c VERIFIED` and cake_lpr gave `s VERIFIED UNSAT` for every one, all at the 8000 MB heap.
  - Solve s: min 23.7 / median 231.7 / max 454.7.
  - lrat-check s: min 11.3 / median 46.2 / max 53.2.
  - cake_lpr s: min 103.3 / median 278.8 / max 305.9.
  - Proof size: min 0.21 GB / median 3.20 GB / max 3.62 GB. Proofs were deleted after checking.
- UNKNOWN: P7_1-8 (Q). It hit its 2400 s cap (2381 s solve). It was not re-run.
- Not reached: in file order, P6_2-9-11, P6_10-13, P6_7-9-16, P6_2-7-10, P6_2-4-11, and every P5, P4, P3, P2 and P1 unit.
- Errors or `"certified": false`: none.

## Resources
- Largest solver RSS: 4423 MB (P8_3-4-9). There was no memory problem. Machine: 4 CPUs, 15 GB RAM.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (14 records) and `lane.log.tail`.

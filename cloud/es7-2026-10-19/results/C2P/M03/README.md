# C2P M03 (LIST = C2P.tsv, j = 3, N = 42, H = 3.0, Z = 01909a07)

Start 03:23:28 UTC on 2026-10-31 (epoch 1793417008). END = start + 3 h − 15 min = 06:08:28 UTC (1793426908). The lane started at 03:35. About 10 of those 12 minutes were lost to a wait loop of mine that hung. The lane stopped itself at 05:58 because only 620 s remained, which is under its 15-minute start limit. This attempt replaces the files of the earlier attempt (Z = fb2c59af), which stopped at step 1.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built the tools from the vendored sources: all 196 manifest hashes matched, and nothing was cloned or downloaded. The tools are CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, and lrat-check from drat-trim 2e3b2dc with the E2 patch.
- Sanity checks: both checkers reject the bad LRAT (lrat-check `c FAILED`, cake_lpr `Checking failed`) and accept the good one (`c VERIFIED`, `s VERIFIED UNSAT`). The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: the header `p cnf 838032 16653336` matches, and so do the sha256 of base.cnf (`b0061e90…`) and of base.json (`2476faff…`).
- Cubes: P1..P8 from `l2cubes.py` are all byte-identical to `C2P/cubes/`.

## Units (54 in `units.tsv`: 45 H, 9 Q)
| case | kind | units | certified | UNKNOWN (timeout) | not reached |
|---|---|---|---|---|---|
| P8 | H | 6 | 6 | 0 | 0 |
| P7 | H | 6 | 6 | 0 | 0 |
| P7 | Q | 1 | 0 | 1 (P7_9-15, cap 2400, solve 2383 s) | 0 |
| P6 | H/Q | 4/2 | 0 | 0 | 6 |
| P5 | H/Q | 6/1 | 0 | 0 | 7 |
| P4 | H/Q | 5/2 | 0 | 0 | 7 |
| P3 | H/Q | 6/1 | 0 | 0 | 7 |
| P2 | H/Q | 6/1 | 0 | 0 | 7 |
| P1 | H/Q | 6/1 | 0 | 0 | 7 |
| **total** | | 54 | **12** | **1** | **41** |

Errors: none. Every finished UNSAT record has `"certified": true`, with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT` (heap 8000 MB, no retry needed).

The 12 certified units are all H units: P8_9-14-15, P8_1-2-12, P8_2-3-13, P8_1-3-11, P8_4-9-11, P8_9-12-16, P7_1-3-10, P7_8-12-14, P7_1-3-13, P7_3-9-10, P7_1-3-14 and P7_8-13-15.

| certified (12) | min | median | max |
|---|---|---|---|
| solve s | 31.7 | 252.6 | 297.2 |
| lrat-check s | 11.4 | 46.8 | 48.9 |
| cake_lpr s | 103.8 | 271.3 | 279.7 |
| proof size | 0.22 GB | 3.25 GB | 3.35 GB |

The units not reached are those after P7_8-13-15 in `units.tsv`, from P6_1-2 onwards.

## SAT, rejection, memory
- No SAT.
- No proof was rejected.
- No memory problem. The largest solver RSS was 4399 MB (P7_1-3-14).

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (13 records) and `lane.log.tail`.

# C2P3 M35: third wave on the parallelogram cases, shard 35 of 50 of C2P3.tsv

Task `results/C2P3/TASK.md` at commit 4f653319, V = M35, LIST = C2P3.tsv, j = 35, N = 50, H = 2.5. One lane (`run.sh`), start 2026-10-31 09:42:56Z, END epoch 1793447876 (11:57:56Z).

## Tools and checks

- Built with `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz` (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. Nothing was cloned or downloaded.
- Sanity: cake_lpr example `s VERIFIED UNSAT`. Both checkers reject the bad LRAT and accept the good one.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and base.json (2476faff…) match.
- Cubes P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`. Details are in `tools.txt`.

## Units

| idx | unit | case | kind | list cap s | lane cap s | result | solve s | lrat-check s | cake_lpr s | proof GB | solver RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 35 | P6_2-12 | P6 | Q | 6000 | 6000 | certified | 4205.9 | 100.9 | 616.5 | 7.08 | 4381 |
| 85 | P6_10-12 | P6 | Q | 4800 | 2356 | certified | 691.7 | 51.6 | 332.7 | 3.60 | 4399 |
| 135 | P6_2-7-16 | P6 | H | 1800 | – | not reached | – | – | – | – | – |
| 185 | P6_7-8-13 | P6 | H | 1800 | – | not reached | – | – | – | – | – |
| 235 | P6_9-11-14 | P6 | H | 1800 | – | not reached | – | – | – | – | – |
| 285 | P5_1-7-9 | P5 | H | 1800 | – | not reached | – | – | – | – | – |
| 335 | P5_1-15 | P5 | Q | 2400 | – | not reached | – | – | – | – | – |
| 385 | P5_2-10-12 | P5 | H | 1800 | – | not reached | – | – | – | – | – |
| 435 | P5_6-9-14 | P5 | H | 1800 | – | not reached | – | – | – | – | – |
| 485 | P5_7-11-13 | P5 | H | 1800 | – | not reached | – | – | – | – | – |

### Counts by case and kind

| case | kind | certified | timed out (UNKNOWN) | not reached | errors / not certified | SAT |
|---|---|---|---|---|---|---|
| P6 | H | 0 | 0 | 3 | 0 | 0 |
| P6 | Q | 2 | 0 | 0 | 0 | 0 |
| P5 | H | 0 | 0 | 4 | 0 | 0 |
| P5 | Q | 0 | 0 | 1 | 0 | 0 |
| all | | 2 | 0 | 8 | 0 | 0 |

### Certified units: minimum / median / maximum

- solve s: 691.74 / 2448.80 / 4205.85
- lrat-check s: 51.60 / 76.25 / 100.90
- cake_lpr s: 332.70 / 474.60 / 616.50
- proof GB: 3.60 / 5.34 / 7.08

## Notes

- Largest solver RSS: 4399 MB (machine: 4 cores, 15 GB).
- SAT: none.
- Proof rejections / records with `certified: false` or ERROR status: none.
- Memory problems: none. Every proof was deleted after its checks. No CNF or proof files are committed.
- Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (the lane records), `lane.log.tail`.

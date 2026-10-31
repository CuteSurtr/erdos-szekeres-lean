# C2P4 M49: fourth wave on the parallelogram cases, one machine

Task `results/C2P4/TASK.md` at commit a46b478d with V = M49, LIST = C2P4.tsv, j = 49, N = 50, H = 2.5. Start 2026-10-31 13:01:37Z (epoch 1793451697), END = 1793459797 (15:16:37Z). Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)

- `C2P/vendor/build_tools.sh`: manifest of all 196 vendored files matches; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch) built from `vendor/tools-src.tar.xz`, no code cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf b0061e90…d8ff1 and base.json 2476faff…2b48, both as expected.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, 14 rows with idx ≡ 49 mod 50)

| idx | unit | case | kind | list cap s | status | lane cap s | solve s | lrat-check s | cake_lpr s | proof | RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 49 | P5_9-10 | P5 | Q | 6000 | certified | 6000 | 475.55 | 54.0 | 313.3 | 3.42 GB | 4366 |
| 99 | P5_1-8-15 | P5 | H | 1800 | certified | 1800 | 477.01 | 57.2 | 336.7 | 3.63 GB | 4367 |
| 149 | P5_2-8-10 | P5 | H | 1800 | certified | 1800 | 276.29 | 49.2 | 290.7 | 3.29 GB | 4402 |
| 199 | P5_6-8-14 | P5 | H | 1800 | certified | 1800 | 200.23 | 49.8 | 289.6 | 3.15 GB | 4364 |
| 249 | P5_7-9-15 | P5 | H | 1800 | certified | 1800 | 201.05 | 46.0 | 275.0 | 3.10 GB | 4390 |
| 299 | P4_1-6 | P4 | Q | 6000 | certified | 3916 | 1979.77 | 83.7 | 482.5 | 5.86 GB | 4383 |
| 349 | P4_9-11 | P4 | Q | 6000 | certified | 1336 | 440.33 | 51.8 | 321.5 | 3.40 GB | 4361 |
| 399 | P4_7-8-14 | P4 | H | 1800 | certified | 510 | 107.17 | 30.2 | 185.5 | 1.44 GB | 3412 |
| 449 | P3_5-7 | P3 | Q | 6000 | not reached | | | | | | |
| 499 | P3_1-5-8 | P3 | H | 1800 | not reached | | | | | | |
| 549 | P3_1-10-12 | P3 | H | 1800 | not reached | | | | | | |
| 599 | P3_4-7-11 | P3 | H | 1800 | not reached | | | | | | |
| 649 | P3_5-6-14 | P3 | H | 1800 | not reached | | | | | | |
| 699 | P3_6-8-12 | P3 | H | 1800 | not reached | | | | | | |

Counts by case and kind:

| case | kind | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|---|
| P5 | Q | 1 | 0 | 0 | 0 |
| P5 | H | 4 | 0 | 0 | 0 |
| P4 | Q | 2 | 0 | 0 | 0 |
| P4 | H | 1 | 0 | 0 | 0 |
| P3 | Q | 0 | 0 | 1 | 0 |
| P3 | H | 0 | 0 | 5 | 0 |
| all | | 8 | 0 | 6 | 0 |

Certified units (8), minimum / median / maximum:

- solve: 107.17 / 358.31 / 1979.77 s
- lrat-check: 30.2 / 50.8 / 83.7 s
- cake_lpr: 185.5 / 302.0 / 482.5 s (all at heap 8000 MB, no retry)
- proof size: 1.44 GB / 3.35 GB / 5.86 GB

Every record has `"certified": true` (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`); proofs were deleted after checking. The lane lowered the solve cap of P4_1-6, P4_9-11 and P4_7-8-14 below the list cap to keep 10 minutes for checks before END; all three still finished UNSAT and certified. After P4_7-8-14 the lane stopped with 782 s left before END (under the 15-minute threshold), so the six P3 units (P3_5-7 Q and five H) were not reached.

## Problems

- SAT: none (`/opt/work/SAT_FOUND` never appeared).
- Proof rejections: none. Errors: none. Timeouts: none.
- Largest solver RSS: 4402 MB (P5_2-8-10); cake_lpr reached about 8.2 GB RSS at heap 8000 MB. No memory problem; disk peak about 6 GB of proof with 22 GB free.
- Pushes to `es7-cloud` occasionally hit ref-lock races / HTTP 403 from concurrent machines and succeeded on retry; the fallback branch was not needed.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl`, `lane.log.tail`.

# C2P4 M41 (LIST C2P4.tsv, j = 41, N = 50, H = 2.5, task commit a46b478d)

## Tools and checks
- `C2P/vendor/build_tools.sh` built CaDiCaL 3.0.1, cake_lpr and lrat-check (E2 patch) from the vendored sources. All 196 manifest hashes matched, and nothing was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: the header is `p cnf 838032 16653336`, and the sha256 of base.cnf (b0061e90…) and base.json (2476faff…) both match the task.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details are in `tools.txt` and `env.txt`. The machine has 4 cores and 15 GB of RAM.

## Units (19 = rows with idx ≡ 41 mod 50)
- Certified UNSAT: 6, all P5: 1 Q (P5_7-14) and 5 H (P5_1-6-10, P5_2-7-9, P5_6-7-12, P5_7-8-11, P5_9-10-11).
- Timed out (UNKNOWN): 0.
- Errors / `certified: false`: 0.
- Not reached: 13, P4: 1 Q + 5 H, P3: 1 Q + 6 H. The lane stopped at 15:02:32Z with 849 s left, below its 15-minute threshold.

By case and kind:

| case | kind | certified | unknown | not reached |
|---|---|---|---|---|
| P5 | Q | 1 | 0 | 0 |
| P5 | H | 5 | 0 | 0 |
| P4 | Q | 0 | 0 | 1 |
| P4 | H | 0 | 0 | 5 |
| P3 | Q | 0 | 0 | 1 |
| P3 | H | 0 | 0 | 6 |

| unit | case | kind | status | cap s | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB | certified |
|---|---|---|---|---|---|---|---|---|---|---|
| P5_7-14 | P5 | Q | UNSATISFIABLE | 6000 | 4139.49 | 124.5 | 675.7 | 7.87 | 4372.18 | True |
| P5_1-6-10 | P5 | H | UNSATISFIABLE | 1800 | 483.85 | 60.7 | 360.2 | 3.54 | 4368.7 | True |
| P5_2-7-9 | P5 | H | UNSATISFIABLE | 1443 | 307.39 | 55.7 | 329.1 | 3.29 | 4410.2 | True |
| P5_6-7-12 | P5 | H | UNSATISFIABLE | 739 | 27.07 | 13.9 | 119.6 | 0.22 | 2646.7 | True |
| P5_7-8-11 | P5 | H | UNSATISFIABLE | 576 | 28.29 | 13.8 | 119.8 | 0.22 | 2647.47 | True |
| P5_9-10-11 | P5 | H | UNSATISFIABLE | 412 | 27.11 | 13.7 | 119.3 | 0.22 | 2644.71 | True |

Certified, solve s (min / median / max): 27.1 / 167.8 / 4139.5  
Certified, lrat-check s: 13.7 / 34.8 / 124.5  
Certified, cake_lpr s: 119.3 / 224.5 / 675.7  
Certified, proof GB: 0.2 / 1.8 / 7.9  
Largest solver RSS: 4410.2 MB

Not reached: P4_5-13 (P4 Q), P4_1-5-8 (P4 H), P4_1-10-12 (P4 H), P4_2-7-12 (P4 H), P4_5-9-15 (P4 H), P4_6-11-12 (P4 H), P3_4-5 (P3 Q), P3_1-4-6 (P3 H), P3_1-8-12 (P3 H), P3_4-6-7 (P3 H), P3_4-12-13 (P3 H), P3_5-12-13 (P3 H), P3_8-10-11 (P3 H)

## Problems
- SAT: none.
- Proof rejections: none.
- Memory problems: none. The peak solver RSS was 4.4 GB of 15 GB.
- With a single lane, P5_7-14 (4139 s solve plus about 13 min of checks) took most of the budget, so the P4 and P3 units of this shard were never started.

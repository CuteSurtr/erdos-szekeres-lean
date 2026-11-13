# C3W7 Q29: nine-bit σ-cubes of the H3/one roots, cap 900 (W7.tsv, shard 29 of 36)

Task: `results/C3W7/TASK.md` at 39bb1bac. Machine: 4 cores, 15 GB RAM (`env.txt`). Start 10:46:36 UTC, END 15:01:36 UTC (H = 4.5).

## Tools and base check (`tools.txt`)
- C3U2 tools at cad4e050 (worktree /opt/c3u2), unmodified; `compose.py` not run.
- CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8 (example: `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch (sanity test passed: `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both).
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).

## Run
53 units (W7.tsv rows ≡ 29 mod 36, `units.tsv`). 3 lanes (`lane0.sh`–`lane2.sh` → `lane.sh`) with `close_tree.py … --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`. No seeding. The lanes' process groups were killed at END.

## Results
- **Certified: 0.**
- **Timed out at 900 s: 48.** All solves ended with `UNKNOWN` at 900.1–900.4 s. Each timed-out unit has its layer-split record (45 children, unsolved; `open_frontier` 45, `unsplittable` 0).
- **Killed at END (still solving): 3.** These are rows 1757, 1793 and 1829 (`0s0_4__1s0-2s1-3s1-5s0-6s1-7s1-8s1-9s0-10s1`, `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0-8s0-9s0-10s1`, `0s0_4__1s1-2s0-3s0-5s1-6s0-7s0-8s1-9s0-10s1`). They have no record.
- **Not reached: 2.** These are rows 1865 and 1901 (`0s0_4__1s1-2s0-3s1-5s0-6s0-7s1-8s0-9s0-10s1`, `0s0_4__1s1-2s0-3s1-5s1-6s0-7s1-8s1-9s0-10s1`).

Per root:

| root | units | certified | timed out | killed at END | not reached |
|---|---|---|---|---|---|
| 0s0_1 | 14 | 0 | 14 | 0 | 0 |
| 0s0_2 | 14 | 0 | 14 | 0 | 0 |
| 0s0_3 | 14 | 0 | 14 | 0 | 0 |
| 0s0_4 | 11 | 0 | 6 | 3 | 2 |

Per parent six-bit cube: each of the 53 units has a different parent, so each parent has one unit on this machine. For the 48 parents in the first 48 rows the unit timed out, for 3 it was killed at END and for 2 it was not reached. No parent had all of its units certified here.

Solve-time distribution of certified units: none were certified, so there is none, and none were certified above 300 s.

## Anomalies
- No SAT, no `PROOF NOT ACCEPTED`, no `recheck.jsonl`, and no certified record with cake_lpr `none`.
- No unit ended early: every finished solve ran its full 900 s cap, none under 72 s. No memory problems were seen.
- This doesn't match `results/C3H1/X1`, where a six-bit cube's nine-bit cubes closed in 450–662 s. Here 48 of 48 timed out at 900 s with 3 solves running in parallel on 4 cores. When I checked mid-run (12:19 UTC), every other C3W7 machine also had 0 UNSAT records.

Files: `out.jsonl` (lanes 0, 1, 2 in order), `driver{0,1,2}.log.tail`, `units.tsv`, `tools.txt`, `env.txt`, lane scripts.

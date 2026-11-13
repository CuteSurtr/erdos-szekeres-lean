# C3W7 Q13: nine-bit σ-cubes of the H3/one roots, shard 13 of 36 of W7.tsv

Task: `results/C3W7/TASK.md` at 39bb1bac, with V = Q13, LIST = W7.tsv, j = 13, N = 36, H = 4.5.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 10:46:34 UTC on 2026-10-25, lanes started 10:49:49, END 15:01:34 (start + 4.5 h − 15 min), when the lanes were killed (whole process groups).

## Tools (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c60730422e75; cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch. Sanity check passed: on {1},{-1}, `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).

## Run

53 units (rows ≡ 13 mod 36 of `lists/W7.tsv`, `units.tsv`). No records were seeded. There were 3 lanes (`lane0.sh` to `lane2.sh`), lane k taking positions ≡ k mod 3, each running `close_tree.py … U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`. Per lane, records are in `out.jsonl` (lane 0, then 1, then 2) and the last 100 driver lines are in `driver{k}.log.tail`.

## Summary

- **Certified: 2 of 53.** Both are in root 0s0_2: row 517 (solve 805.7 s, check 109.4 s) and row 769 (solve 795.3 s, check 114.2 s).
- **Timed out at 900: 45.** Each one's layer-split record (45 children, unsolved) is written, so these units are open.
- **Killed at END: 3** (rows 1741, 1777, 1813). They started at 14:50 and were killed at 15:01 before their solve finished, so they have no record. **Not reached: 2** (rows 1849, 1885).
- No SAT. No proof rejections. No cake_lpr `none`, so no rechecks were needed and there is no `recheck.jsonl`. No memory problem (about 2 GB used). No unit ended early: every solve without a certificate ran the full 900 s.

### Per root

| root | units | certified | timed out | killed at END / not reached |
|---|---|---|---|---|
| 0s0_1 | 14 | 0 | 14 | 0 |
| 0s0_2 | 15 | 2 | 13 | 0 |
| 0s0_3 | 14 | 0 | 14 | 0 |
| 0s0_4 | 10 | 0 | 5 | 3 / 2 |
| total | 53 | 2 | 45 | 3 / 2 |

### Per parent six-bit cube

Each parent has exactly 1 unit on this machine, because 36 ≡ 4 (mod 8): the units are child 5 (`8s1-9s0-10s1`) and child 1 (`8s0-9s0-10s1`), alternating. The parents all of whose units here were certified are:
- `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0` (1/1)
- `0s0_2__1s1-3s0-4s0-5s0-6s0-7s0` (1/1)

The unit table below gives every other parent: its one unit timed out, was killed or was not reached.

### Solve times of certified units

n = 2: min 795.3, quartiles 797.9 / 800.5 / 803.1, p90 804.7, max 805.7 s. Both were certified above 300 s.

On this shard the nine-bit cubes are much harder than the 450–662 s of `results/C3H1/X1`: 45 of the 47 finished solves hit the 900 s cap, with 3 lanes sharing the 4 cores.

## Per unit

| row | unit | lane | result |
|---|---|---|---|
| 13 | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1-8s1-9s0-10s1` | 0 | timed out at 900 |
| 49 | `0s0_1__2s0-3s0-4s0-5s1-6s1-7s0-8s0-9s0-10s1` | 1 | timed out at 900 |
| 85 | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0-8s1-9s0-10s1` | 2 | timed out at 900 |
| 121 | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s1-8s0-9s0-10s1` | 0 | timed out at 900 |
| 157 | `0s0_1__2s0-3s1-4s0-5s0-6s1-7s1-8s1-9s0-10s1` | 1 | timed out at 900 |
| 193 | `0s0_1__2s0-3s1-4s1-5s0-6s0-7s0-8s0-9s0-10s1` | 2 | timed out at 900 |
| 229 | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s0-8s1-9s0-10s1` | 0 | timed out at 900 |
| 265 | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s1-8s0-9s0-10s1` | 1 | timed out at 900 |
| 301 | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s1-8s1-9s0-10s1` | 2 | timed out at 900 |
| 337 | `0s0_1__2s1-3s0-4s1-5s0-6s1-7s0-8s0-9s0-10s1` | 0 | timed out at 900 |
| 373 | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s0-8s1-9s0-10s1` | 1 | timed out at 900 |
| 409 | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s1-8s0-9s0-10s1` | 2 | timed out at 900 |
| 445 | `0s0_1__2s1-3s1-4s0-5s1-6s1-7s1-8s1-9s0-10s1` | 0 | timed out at 900 |
| 481 | `0s0_1__2s1-3s1-4s1-5s1-6s0-7s0-8s0-9s0-10s1` | 1 | timed out at 900 |
| 517 | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0-8s1-9s0-10s1` | 2 | **certified** (solve 805.7 s, check 109.4 s) |
| 553 | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s1-8s0-9s0-10s1` | 0 | timed out at 900 |
| 589 | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s1-8s1-9s0-10s1` | 1 | timed out at 900 |
| 625 | `0s0_2__1s0-3s0-4s1-5s1-6s1-7s0-8s0-9s0-10s1` | 2 | timed out at 900 |
| 661 | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0-8s1-9s0-10s1` | 0 | timed out at 900 |
| 697 | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s1-8s0-9s0-10s1` | 1 | timed out at 900 |
| 733 | `0s0_2__1s0-3s1-4s1-5s0-6s1-7s1-8s1-9s0-10s1` | 2 | timed out at 900 |
| 769 | `0s0_2__1s1-3s0-4s0-5s0-6s0-7s0-8s0-9s0-10s1` | 0 | **certified** (solve 795.3 s, check 114.2 s) |
| 805 | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s0-8s1-9s0-10s1` | 1 | timed out at 900 |
| 841 | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s1-8s0-9s0-10s1` | 2 | timed out at 900 |
| 877 | `0s0_2__1s1-3s0-4s1-5s1-6s0-7s1-8s1-9s0-10s1` | 0 | timed out at 900 |
| 913 | `0s0_2__1s1-3s1-4s0-5s0-6s1-7s0-8s0-9s0-10s1` | 1 | timed out at 900 |
| 949 | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s0-8s1-9s0-10s1` | 2 | timed out at 900 |
| 985 | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s1-8s0-9s0-10s1` | 0 | timed out at 900 |
| 1021 | `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1-8s1-9s0-10s1` | 1 | timed out at 900 |
| 1057 | `0s0_3__1s0-2s0-4s0-5s1-6s0-7s0-8s0-9s0-10s1` | 2 | timed out at 900 |
| 1093 | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0-8s1-9s0-10s1` | 0 | timed out at 900 |
| 1129 | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s1-8s0-9s0-10s1` | 1 | timed out at 900 |
| 1165 | `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1-8s1-9s0-10s1` | 2 | timed out at 900 |
| 1201 | `0s0_3__1s0-2s1-4s0-5s1-6s1-7s0-8s0-9s0-10s1` | 0 | timed out at 900 |
| 1237 | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s0-8s1-9s0-10s1` | 1 | timed out at 900 |
| 1273 | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s1-8s0-9s0-10s1` | 2 | timed out at 900 |
| 1309 | `0s0_3__1s1-2s0-4s0-5s0-6s1-7s1-8s1-9s0-10s1` | 0 | timed out at 900 |
| 1345 | `0s0_3__1s1-2s0-4s1-5s0-6s0-7s0-8s0-9s0-10s1` | 1 | timed out at 900 |
| 1381 | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s0-8s1-9s0-10s1` | 2 | timed out at 900 |
| 1417 | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s1-8s0-9s0-10s1` | 0 | timed out at 900 |
| 1453 | `0s0_3__1s1-2s1-4s0-5s1-6s0-7s1-8s1-9s0-10s1` | 1 | timed out at 900 |
| 1489 | `0s0_3__1s1-2s1-4s1-5s0-6s1-7s0-8s0-9s0-10s1` | 2 | timed out at 900 |
| 1525 | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s0-8s1-9s0-10s1` | 0 | timed out at 900 |
| 1561 | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1-8s0-9s0-10s1` | 1 | timed out at 900 |
| 1597 | `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1-8s1-9s0-10s1` | 2 | timed out at 900 |
| 1633 | `0s0_4__1s0-2s0-3s1-5s1-6s0-7s0-8s0-9s0-10s1` | 0 | timed out at 900 |
| 1669 | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0-8s1-9s0-10s1` | 1 | timed out at 900 |
| 1705 | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s1-8s0-9s0-10s1` | 2 | timed out at 900 |
| 1741 | `0s0_4__1s0-2s1-3s1-5s0-6s0-7s1-8s1-9s0-10s1` | 0 | killed at END (started 14:50, no record) |
| 1777 | `0s0_4__1s0-2s1-3s1-5s1-6s1-7s0-8s0-9s0-10s1` | 1 | killed at END (started 14:50, no record) |
| 1813 | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s0-8s1-9s0-10s1` | 2 | killed at END (started 14:50, no record) |
| 1849 | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s1-8s0-9s0-10s1` | 0 | not reached |
| 1885 | `0s0_4__1s1-2s0-3s1-5s0-6s1-7s1-8s1-9s0-10s1` | 1 | not reached |

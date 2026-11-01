# C3W7 Q03: nine-bit σ-cubes of the H3/one roots, shard 3 of 36 of W7.tsv

Task `results/C3W7/TASK.md` at 39bb1bac, with V = Q03, LIST = W7.tsv, j = 3, N = 36, H = 4.5.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 10:46:23 UTC on 2026-10-25, lanes started 10:49:19, END 15:01:23 (lanes killed 15:01:28).

## Tools and base check (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified. `compose.py` not run.
- CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (example: `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch. Checker sanity test passed: `3 0 0` on {1},{-1} rejected by both, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).

## Run

54 units (rows of W7.tsv with row ≡ 3 mod 36, `units.tsv`, no header), 3 lanes (`lane0.sh`–`lane2.sh`), no seeded records. Each unit ran once with
`close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`.
`out.jsonl` holds the records of lane 0, then 1, then 2. A unit that timed out has its layer-split record (45 children each), and those children are unsolved. That is intended.

## Summary

- **7 certified, 41 timed out at 900 s, 3 killed at END, 3 not reached** (of 54).
- No SAT. No proof rejections: all 7 certified records have lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. No checker was killed at END, so no recheck was needed and there is no `recheck.jsonl`. No memory problem: about 2 GB used, 13 GB available the whole time.
- No unit ended early. The 3 units killed at END (lanes started them at 14:50) were stopped by SIGTERM at 664–680 s, before their 900 s cap. close_tree recorded each one as `UNKNOWN` and then wrote its layer-split record (45 children) before the process group was killed. These are **not** cap timeouts, so they count as not finished. A split record claims nothing.
- All 7 certified units took 789–867 s, close to the cap. This is much slower than the 450–662 s seen in C3H1/X1, probably because 3 solvers shared 4 cores here.
- Each parent six-bit cube has exactly one unit on this machine, so "all units of the parent certified" means that one unit was certified.

| pos | row | unit | lane | result | detail |
|---|---|---|---|---|---|
| 0 | 3 | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s0-8s0-9s1-10s1` | lane 0 | certified | solve 854.3 s, check 98.7 s |
| 1 | 39 | `0s0_1__2s0-3s0-4s0-5s1-6s0-7s0-8s1-9s1-10s1` | lane 1 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 2 | 75 | `0s0_1__2s0-3s0-4s1-5s0-6s0-7s1-8s0-9s1-10s1` | lane 2 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 3 | 111 | `0s0_1__2s0-3s0-4s1-5s1-6s0-7s1-8s1-9s1-10s1` | lane 0 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 4 | 147 | `0s0_1__2s0-3s1-4s0-5s0-6s1-7s0-8s0-9s1-10s1` | lane 1 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 5 | 183 | `0s0_1__2s0-3s1-4s0-5s1-6s1-7s0-8s1-9s1-10s1` | lane 2 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 6 | 219 | `0s0_1__2s0-3s1-4s1-5s0-6s1-7s1-8s0-9s1-10s1` | lane 0 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 7 | 255 | `0s0_1__2s0-3s1-4s1-5s1-6s1-7s1-8s1-9s1-10s1` | lane 1 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 8 | 291 | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s0-8s0-9s1-10s1` | lane 2 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 9 | 327 | `0s0_1__2s1-3s0-4s1-5s0-6s0-7s0-8s1-9s1-10s1` | lane 0 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 10 | 363 | `0s0_1__2s1-3s0-4s1-5s1-6s0-7s1-8s0-9s1-10s1` | lane 1 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 11 | 399 | `0s0_1__2s1-3s1-4s0-5s0-6s0-7s1-8s1-9s1-10s1` | lane 2 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 12 | 435 | `0s0_1__2s1-3s1-4s0-5s1-6s1-7s0-8s0-9s1-10s1` | lane 0 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 13 | 471 | `0s0_1__2s1-3s1-4s1-5s0-6s1-7s0-8s1-9s1-10s1` | lane 1 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 14 | 507 | `0s0_1__2s1-3s1-4s1-5s1-6s1-7s1-8s0-9s1-10s1` | lane 2 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 15 | 543 | `0s0_2__1s0-3s0-4s0-5s0-6s1-7s1-8s1-9s1-10s1` | lane 0 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 16 | 579 | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s0-8s0-9s1-10s1` | lane 1 | certified | solve 789.0 s, check 97.9 s |
| 17 | 615 | `0s0_2__1s0-3s0-4s1-5s1-6s0-7s0-8s1-9s1-10s1` | lane 2 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 18 | 651 | `0s0_2__1s0-3s1-4s0-5s0-6s0-7s1-8s0-9s1-10s1` | lane 0 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 19 | 687 | `0s0_2__1s0-3s1-4s0-5s1-6s0-7s1-8s1-9s1-10s1` | lane 1 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 20 | 723 | `0s0_2__1s0-3s1-4s1-5s0-6s1-7s0-8s0-9s1-10s1` | lane 2 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 21 | 759 | `0s0_2__1s0-3s1-4s1-5s1-6s1-7s0-8s1-9s1-10s1` | lane 0 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 22 | 795 | `0s0_2__1s1-3s0-4s0-5s0-6s1-7s1-8s0-9s1-10s1` | lane 1 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 23 | 831 | `0s0_2__1s1-3s0-4s0-5s1-6s1-7s1-8s1-9s1-10s1` | lane 2 | timed out at 900 | solve 900.2 s; layer split: 45 children, unsolved |
| 24 | 867 | `0s0_2__1s1-3s0-4s1-5s1-6s0-7s0-8s0-9s1-10s1` | lane 0 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 25 | 903 | `0s0_2__1s1-3s1-4s0-5s0-6s0-7s0-8s1-9s1-10s1` | lane 1 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 26 | 939 | `0s0_2__1s1-3s1-4s0-5s1-6s0-7s1-8s0-9s1-10s1` | lane 2 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 27 | 975 | `0s0_2__1s1-3s1-4s1-5s0-6s0-7s1-8s1-9s1-10s1` | lane 0 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 28 | 1011 | `0s0_2__1s1-3s1-4s1-5s1-6s1-7s0-8s0-9s1-10s1` | lane 1 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 29 | 1047 | `0s0_3__1s0-2s0-4s0-5s0-6s1-7s0-8s1-9s1-10s1` | lane 2 | certified | solve 837.1 s, check 94.3 s |
| 30 | 1083 | `0s0_3__1s0-2s0-4s0-5s1-6s1-7s1-8s0-9s1-10s1` | lane 0 | certified | solve 789.1 s, check 96.3 s |
| 31 | 1119 | `0s0_3__1s0-2s0-4s1-5s0-6s1-7s1-8s1-9s1-10s1` | lane 1 | certified | solve 866.9 s, check 89.9 s |
| 32 | 1155 | `0s0_3__1s0-2s1-4s0-5s0-6s0-7s0-8s0-9s1-10s1` | lane 2 | certified | solve 799.5 s, check 96.0 s |
| 33 | 1191 | `0s0_3__1s0-2s1-4s0-5s1-6s0-7s0-8s1-9s1-10s1` | lane 0 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 34 | 1227 | `0s0_3__1s0-2s1-4s1-5s0-6s0-7s1-8s0-9s1-10s1` | lane 1 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 35 | 1263 | `0s0_3__1s0-2s1-4s1-5s1-6s0-7s1-8s1-9s1-10s1` | lane 2 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 36 | 1299 | `0s0_3__1s1-2s0-4s0-5s0-6s1-7s0-8s0-9s1-10s1` | lane 0 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 37 | 1335 | `0s0_3__1s1-2s0-4s0-5s1-6s1-7s0-8s1-9s1-10s1` | lane 1 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 38 | 1371 | `0s0_3__1s1-2s0-4s1-5s0-6s1-7s1-8s0-9s1-10s1` | lane 2 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 39 | 1407 | `0s0_3__1s1-2s0-4s1-5s1-6s1-7s1-8s1-9s1-10s1` | lane 0 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 40 | 1443 | `0s0_3__1s1-2s1-4s0-5s1-6s0-7s0-8s0-9s1-10s1` | lane 1 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 41 | 1479 | `0s0_3__1s1-2s1-4s1-5s0-6s0-7s0-8s1-9s1-10s1` | lane 2 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 42 | 1515 | `0s0_3__1s1-2s1-4s1-5s1-6s0-7s1-8s0-9s1-10s1` | lane 0 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 43 | 1551 | `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1-8s1-9s1-10s1` | lane 1 | certified | solve 795.4 s, check 80.1 s |
| 44 | 1587 | `0s0_4__1s0-2s0-3s0-5s1-6s1-7s0-8s0-9s1-10s1` | lane 2 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 45 | 1623 | `0s0_4__1s0-2s0-3s1-5s0-6s1-7s0-8s1-9s1-10s1` | lane 0 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 46 | 1659 | `0s0_4__1s0-2s0-3s1-5s1-6s1-7s1-8s0-9s1-10s1` | lane 1 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 47 | 1695 | `0s0_4__1s0-2s1-3s0-5s0-6s1-7s1-8s1-9s1-10s1` | lane 2 | timed out at 900 | solve 900.1 s; layer split: 45 children, unsolved |
| 48 | 1731 | `0s0_4__1s0-2s1-3s1-5s0-6s0-7s0-8s0-9s1-10s1` | lane 0 | killed at END | solver killed at 664.1 s (cap 900 not reached); close_tree then wrote a layer-split record (45 children, unsolved) |
| 49 | 1767 | `0s0_4__1s0-2s1-3s1-5s1-6s0-7s0-8s1-9s1-10s1` | lane 1 | killed at END | solver killed at 680.2 s (cap 900 not reached); close_tree then wrote a layer-split record (45 children, unsolved) |
| 50 | 1803 | `0s0_4__1s1-2s0-3s0-5s0-6s0-7s1-8s0-9s1-10s1` | lane 2 | killed at END | solver killed at 671.4 s (cap 900 not reached); close_tree then wrote a layer-split record (45 children, unsolved) |
| 51 | 1839 | `0s0_4__1s1-2s0-3s0-5s1-6s0-7s1-8s1-9s1-10s1` | lane 0 | not reached |  |
| 52 | 1875 | `0s0_4__1s1-2s0-3s1-5s0-6s1-7s0-8s0-9s1-10s1` | lane 1 | not reached |  |
| 53 | 1911 | `0s0_4__1s1-2s0-3s1-5s1-6s1-7s0-8s1-9s1-10s1` | lane 2 | not reached |  |

### Totals per root

| root | units | certified | timed out | not reached or killed at END | other |
|---|---|---|---|---|---|
| `0s0_1` | 15 | 1 | 14 | 0 | 0 |
| `0s0_2` | 14 | 1 | 13 | 0 | 0 |
| `0s0_3` | 14 | 4 | 10 | 0 | 0 |
| `0s0_4` | 11 | 1 | 4 | 6 | 0 |

### Totals per parent six-bit cube

| parent six-bit cube | units | certified | timed out | not reached or killed at END | other |
|---|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s0-3s0-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s1-5s0-6s0-7s0` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s1-5s1-6s0-7s0` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s0-5s0-6s0-7s1` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s0-5s1-6s0-7s1` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s1-5s0-6s1-7s0` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s1-5s1-6s1-7s0` | 1 | 0 | 0 | 1 | 0 |

Parents all of whose units on this machine were certified (7): `0s0_1__2s0-3s0-4s0-5s0-6s0-7s0`, `0s0_2__1s0-3s0-4s1-5s0-6s0-7s0`, `0s0_3__1s0-2s0-4s0-5s0-6s1-7s0`, `0s0_3__1s0-2s0-4s0-5s1-6s1-7s1`, `0s0_3__1s0-2s0-4s1-5s0-6s1-7s1`, `0s0_3__1s0-2s1-4s0-5s0-6s0-7s0`, `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1`

Certified solve times (n=7): min 789.0, Q1 792.2, median 799.5, Q3 845.7, p90 859.3, max 866.9 s; certified above 300 s: 7
Check times: min 80.1, max 98.7 s

Counts: {'certified': 7, 'timed out at 900': 41, 'killed at END': 3, 'not reached': 3}

# C3W4 / H14: wave 4, W4_H3.tsv shard 14 of 30, σ-cube splitting

**Result: root 1 (`0s0_1s0-2s1`) is partial. Roots 2 and 3 were not reached. No SAT, no proof rejection, no memory problem.**
At cap 300 s, all 64 six-bit σ-cubes of the root timed out. 386 of their layer children were certified at cap 600, and none of those timed out.

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:21 UTC, END 16:16:21 UTC (start + 5 h − 15 min).

- Tools: worktree of commit `95cafa93` at `/opt/c3u`, `results/C3U/tools` used unmodified. `compose.py` was not run, per the task.
- CaDiCaL 3.0.1 `c60730422e75…`, cake_lpr `a36874a8b750…` (its example gives `s VERIFIED UNSAT`), and lrat-check `2e3b2dc0ecf9…` with the E2 patch. Sanity check: LRAT `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both. Details are in `tools.txt`.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Roots: rows of `W4_H3.tsv` with row ≡ 14 (mod 30), which gives rows 14, 44 and 74 (`roots.tsv`). All three start fresh, with 0 seeded records.
- Runner (`runner.sh`): `close_tree.py base out R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S`, with S = min(2.0, hours left).

## Per root

| row | root | stratum | status | certified (depth, σ level: count) | timeouts | solve s | check s |
|-----|------|---------|--------|-----------------------------------|----------|---------|---------|
| 14 | 0s0_1s0-2s1 | H3/two | **partial** | d3 σ2: 386 (cap 600) | 1 root (cap 1), 8 σ1 cubes (cap 1), 64 σ2 cubes (cap 300) | 34,859 | 14,458 |
| 44 | 0s0_2s0-5s0 | H3/two | not reached | – | – | – | – |
| 74 | 0s0_3s0-7s1 | H3/two | not reached | – | – | – | – |

Tree of root 14:
- The root and its 8 σ1 cubes timed out at cap 1 as intended and were σ-split: 1 + 8 split records with 8 children each.
- None of the 64 σ2 cubes (6 σ bits) closed in 300 s, so each got a layer split into 51 depth-3 children: 3,264 nodes at cap 600.
- 386 of those 3,264 were certified. Every one has `c VERIFIED` and `s VERIFIED UNSAT`. Solve times are 40 s on average, 168 s at most. The largest proof was 327 MB.
- Coverage by cube: 7 cubes have all 51 children certified, 1 cube has 29 of 51, and the other 56 cubes have no children attempted.
- Open frontier at stop: 2,878 depth-3 nodes, none of them attempted.
- No split record has `"children": 0`.

Solve and check seconds are summed over nodes, with 3 jobs sharing 4 cores.

## Totals (stratum H3/two)

1 root partial, 2 not reached, 0 closed. 532 records: 386 certified, 73 timeouts, 73 splits.

## Notes

- **The 2-hour slice did not bound root 1.** `close_tree.py` checks `--hours` only between generations. The 64-cube generation ended at about 13:25, before the 13:35 deadline, so the next generation of 3,264 nodes was submitted as a whole. It ran until END, when I killed the runner's process group at 16:16:28. This is why roots 44 and 74 were not reached.
- The killed solver and checker jobs wrote no records, so no record has cake_lpr `none` and nothing needed a re-check.
- This differs from C3SIG2, where 6-bit cubes on H3 roots certified in about 100–250 s each. Here all 64 timed out at 300 s with 3 jobs on 4 cores. Their layer children close easily, though: at about 1 min each, finishing this root's remaining 2,878 children would take about 16 machine-hours at 3 jobs.
- **SAT: none. Proof rejections: none. Memory: no problem** (about 2 GB used at peak sample).

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all 532 records, resumable), `driver.log.tail`, `README.md`.

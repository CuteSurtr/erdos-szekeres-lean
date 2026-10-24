# C3W4 / H10: wave 4, list W4_H3.tsv, shard 10 of 30

**Result: 2 of my 3 H3 roots are closed (`0s0_3s1-6s1`, `0s0_2s0-3s0`). The third, `0s0_3s0-5s1`, is partial with 2,737 open nodes. No SAT, no proof rejection, no memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:34 UTC, END 16:16:34 UTC (start + 5 h − 15 min). Details in `tools.txt`.

- Tools: worktree of commit 95cafa93 at `/opt/c3u`, `results/C3U/tools` used unmodified. `compose.py` was not run.
- CaDiCaL c6073042 (3.0.1); cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch. Sanity check: LRAT `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`, which matches.
- Roots: rows of `lists/W4_H3.tsv` with row ≡ 10 (mod 30), which are rows 10, 40 and 70 (`roots.tsv`). Nothing was seeded, so every root started fresh.
- One runner (`runner.sh`) launched with `setsid nohup`, running `close_tree.py … --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S`, with S = min(2.0, hours left).

## Per root

Depth is the number of layers. Level sN means N σ-levels, i.e. 3N σ bits.

| root | stratum | status | certified | timeouts | σ splits | layer splits | solve s | check s | wall |
|------|---------|--------|-----------|----------|----------|--------------|---------|---------|------|
| 0s0_3s1-6s1 | H3/two | **closed** | d2/s2: 64 | d2/s0 @1: 1, d2/s1 @1: 8 | 9 | 0 | 8,405 | 2,381 | 11:33–12:35 |
| 0s0_2s0-3s0 | H3/two | **closed** | d2/s2: 64 | d2/s0 @1: 1, d2/s1 @1: 8 | 9 | 0 | 2,562 | 1,764 | 12:35–13:00 |
| 0s0_3s0-5s1 | H3/two | partial, open frontier 2,737 | d2/s2: 4, d3/s2: 323 | d2/s0 @1: 1, d2/s1 @1: 8, d2/s2 @300: 60 | 9 | 60 (51 children each) | 26,676 | 7,964 | 13:00–16:17 (killed at END) |

The timeouts at cap 1 are the deliberate cap 1 used at the root and at the first σ level.

- On the two closed roots, all 64 6-bit cubes were certified at cap 300. No split record has `"children": 0`.
- On `0s0_3s0-5s1`, 60 of the 64 6-bit cubes timed out at 300 s. Each got the layer split into 51 depth-3 children, 3,060 in all. Of these, 323 were certified at cap 600, none timed out, and 2,737 were never attempted when the run was stopped at END.
  - The `--hours` deadline is only checked between batches, so I killed the run at END. That gave no `cake_lpr: none` records, so nothing needed a re-check.
  - The 4 6-bit cubes that were certified are recorded in `out.jsonl`.

Solve and check times are summed per node. With 3 jobs on 4 cores they are not wall-clock.

## Totals (stratum H3/two)

- 3 roots: 2 closed, 1 partial, 0 not reached.
- 455 certified nodes. Each has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.
- 87 split records: 27 σ, 60 layer.
- 87 timeouts: 27 at cap 1, 60 at cap 300.
- 37,643 solve seconds and 12,109 check seconds.
- `out.jsonl` has 629 records.

## SAT / proof rejections / memory

- SAT: none.
- `PROOF NOT ACCEPTED`: none. No certified-looking record has cake_lpr `none`, so `recheck.jsonl` is absent.
- Memory: the peak seen was about 12 GB used of 15 GB, with 3 GB available. Nothing was killed by OOM.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log.tail`, `summary.jsonl` (per-root breakdown), `README.md`.

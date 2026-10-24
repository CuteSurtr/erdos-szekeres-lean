# C3W4 H07: W4_H3.tsv shard 7 of 30, σ-cube splitting

Task: `results/C3W4/TASK.md` at 3fd8a4d8 with V = H07, LIST = W4_H3.tsv, j = 7, N = 30, SLICE = 2.0, H = 5.0.
One VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:27 UTC on 2026-10-24, END 16:16:27.

## Tools and base CNF (`tools.txt`)

- C3U tools: worktree of 95cafa93 at `/opt/c3u`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c6073042; cake_lpr a36874a8 (example: `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch.
  Sanity check passed: `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).

## Run

There is one runner (`runner.sh`) with `close_tree.py … --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S`, S = min(2.0, hours left).
Roots: rows 7, 37, 67 and 97 of the list (`roots.tsv`). Nothing was seeded, so every record in `out.jsonl` is new (433 lines).

## Per root

Depth means the number of layers (roots are at depth 2). σ level means the number of 3-bit σ splits on the path.

| root | stratum | status | certified (depth, σ level) | timeouts | solve s | check s | wall |
|---|---|---|---|---|---|---|---|
| 0s0_1s0-9s1 | H3/two | **closed** (open frontier 0, no childless node) | 64 at (2, 2) | 9 at cap 1 (root + 8 σ1) | 6717 | 2471 | 11:35–12:28 |
| 0s0_1s1-9s0 | H3/two | **closed** (open frontier 0, no childless node) | 64 at (2, 2) | 9 at cap 1 | 4186 | 2033 | 12:28–13:04 |
| 0s0_3s0-4s0 | H3/two | **closed** (open frontier 0, no childless node) | 64 at (2, 2) | 9 at cap 1 | 2229 | 1708 | 13:04–13:27 |
| 0s0_5 | H3/one | **partial** | 23 at (3, 2) | 9 at cap 1; **all 64 6-bit cubes at cap 300**; 9 depth-3 layer children at cap 600 | 28489 | 926 | 13:27–16:16 (killed at END) |

On the three two-orbit roots, every one of the 64 6-bit cubes was certified directly at cap 300. Each root used 9 σ splits and no layer split.

0s0_5 was different. Every 6-bit cube timed out at 300 s, and each one got the layer split (51, 60 or 72 children; 73 layer splits in all). Of the layer children solved at cap 600, 23 were certified and 9 timed out; the 9 were layer-split again. The open frontier is about 5,089 nodes, counted as split children minus solved nodes. close_tree did not print `open_frontier` because it was killed. Every split record has children > 0.

**Slice overrun:** `close_tree.py` checks `--hours` only between frontier generations. On 0s0_5 it submitted the whole layer-child generation (about 4,600 nodes at cap 600) at 15:27 and kept running past its 2 h slice. Since this was the last root, I let it run until END and then killed it (16:16:38). The jobs killed at that point were in flight and left no records. No certified record has cake_lpr `none`, so nothing needed re-checking (`recheck.jsonl` not created).

## Totals (stratum H3; 4 roots)

- H3/two: 3 roots, 3 closed, 192 certified, solve 13,132 s, check 6,212 s.
- H3/one: 1 root, partial, 23 certified, solve 28,489 s, check 926 s.
- All 215 certified nodes have `lrat_check: c VERIFIED` and `cake_lpr: s VERIFIED UNSAT`. The largest proof was 511 MB (not committed).

No SAT answer, no proof rejection and no memory problem (peak use about 6 GB of 15 GB).

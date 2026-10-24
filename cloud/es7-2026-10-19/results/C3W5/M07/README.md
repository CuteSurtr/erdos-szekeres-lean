# C3W5 / M07: mop-up of the two-orbit roots, shard 7 of 10 of W5_two.tsv

**Result: all 8 of my roots are closed (open frontier 0, no childless timed-out node, no unsplittable node). No SAT. No proof rejection. No memory problem.** The runner finished at 18:16:41 UTC, 41 minutes before END.

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 16:12:31 UTC, END = start + 3 h − 15 min = 18:57:31 UTC. Task `results/C3W5/TASK.md` at 265d8921 with V = M07, LIST = W5_two.tsv, j = 7, N = 10, SLICE = 1.0, H = 3.0.

- Tools: worktree of cad4e050 at `/opt/c3u2`, TOOLS = `/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 (c60730422e758ef1cebe7aeddf2dda31c996bf04); cake_lpr a36874a8 (`make cake_lpr`, its example prints `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc0 with `results/E2/tools/lrat-check-E2.patch`. The patch is in normal-diff format, so `git apply` rejects it; I applied it with `patch`, which adds the single E2 line. Sanity check on {1},{-1}: `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: rows of `lists/W5_two.tsv` with row ≡ 7 (mod 10): 8 roots (`roots.tsv`), all with the note "not reached in C3W4".
- Seeding: I scanned all 48 `results/C3W4/*/out.jsonl` files (there are no `C3W4/*/recheck*.jsonl`) for nodes equal to R or starting with `R_`/`R__`. **0 records were seeded**, so `out.jsonl` holds every record of this run (116 lines).
- Runner: `runner.sh` (`setsid nohup`), `close_tree.py ... --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, S = min(1.0, hours left).

## Per root

All nodes are at layer depth 2, the root depth. No layer split was needed. σ0 is the root, σ1 a cube on 3 σ bits, and σ2 a cube on 6 σ bits. Solve and check seconds are summed per node, not wall-clock time.

| row | root | stratum | status | certified by σ level | timeouts | σ splits | solve s | check s |
|-----|------|---------|--------|----------------------|----------|----------|---------|---------|
| 7 | `0s0-5s1_6s1-7s1` | H6(5,1)/two | closed | σ0: 1 | 0 | 0 | 44 | 48 |
| 17 | `0s0-4s1_1s1-9s1` | H6(4,1)/two | closed | σ1: 4, σ2: 32 | 5 | 5 | 4117 | 1535 |
| 27 | `0s0-5s0_2s0-8s0` | H6(5,0)/two | closed | σ1: 8 | 1 | 1 | 833 | 354 |
| 37 | `0s0-5s1_2s0-10s0` | H6(5,1)/two | closed | σ1: 8 | 1 | 1 | 1180 | 378 |
| 47 | `0s0-5s0_1s0-9s1` | H6(5,0)/two | closed | σ0: 1 | 0 | 0 | 52 | 32 |
| 57 | `0s0-5s1_1s1-3s0` | H6(5,1)/two | closed | σ1: 6, σ2: 16 | 3 | 3 | 3162 | 980 |
| 67 | `0s0-5s1_1s0-8s0` | H6(5,1)/two | closed | σ1: 8 | 1 | 1 | 1111 | 374 |
| 77 | `0s0-5s1_6s1-9s0` | H6(5,1)/two | closed | σ1: 8 | 1 | 1 | 1660 | 378 |

Every timeout was a 300 s UNKNOWN at σ0 or σ1, and every one was σ-split into 8 children. All 48 σ2 cubes were certified at cap 600 s. Two roots, rows 7 and 47, were certified directly at the root.

## Totals per stratum

| stratum | roots | closed | certified | timeouts | σ splits | solve s | check s |
|---------|-------|--------|-----------|----------|----------|---------|---------|
| H6(5,1)/two | 5 | 5 | 47 | 6 | 6 | 7157 | 2156 |
| H6(4,1)/two | 1 | 1 | 36 | 5 | 5 | 4117 | 1535 |
| H6(5,0)/two | 2 | 2 | 9 | 1 | 1 | 885 | 387 |
| **all** | 8 | 8 | 92 | 12 | 12 | 12159 | 4078 |

By cap: 44 UNSAT at 300 s, 48 UNSAT at 600 s, 12 UNKNOWN at 300 s. All 92 UNSAT records have lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.

## SAT / proof rejections / memory

- SAT: none (no SATISFIABLE record and no `SAT FOUND`).
- Proof rejections: none (no `PROOF NOT ACCEPTED` and no cake_lpr `none`), so there is no `recheck.jsonl`.
- Childless split records (`"children": 0`) or `unsplittable` nodes: none.
- Memory: peak use was about 9 of 15 GB, with no problems.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all 116 records, none seeded), `driver.log.tail` (last 100 lines), `README.md`.

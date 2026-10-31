# C3W4 / O12: wave 4, list W4_one.tsv, shard 12 of 16

**Result: both of my 2 roots are closed. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:18 UTC, END 16:16:18 UTC on 2026-10-24
(start + 5 h − 15 min). The runner finished at 13:16:02 UTC, after both roots were closed.

- Tools: worktree of commit `95cafa93` at `/opt/c3u` (`results/C3U/tools`), used unmodified. No `compose.py` was run.
- CaDiCaL 3.0.1 (c60730422e758ef1cebe7aeddf2dda31c996bf04); cake_lpr a36874a8 (`make cake_lpr`, example prints
  `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc with the E2 patch. Sanity check on {1},{-1}: `3 0 0` rejected by
  both checkers, `3 0 1 2 0` accepted by both (`tools.txt`).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: rows of `lists/W4_one.tsv` with row ≡ 12 (mod 16): rows 12 and 28 (`roots.tsv`), started fresh,
  0 seeded records.
- Options (`runner.sh`): `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, slice 2.5 h.

## Per root

All nodes are at layer depth 2 (no layer split was needed); σ level 0 = root, 1 = 3 σ bits, 2 = 6 σ bits.

| row | root | stratum | status | certified (σ level 2, cap 300) | timeouts | splits | max solve s | solve s | check s | wall |
|-----|------|---------|--------|------|----------|--------|------|---------|---------|------|
| 12 | 0s0-4s0_5 | H6(4,0)/one | **closed** (open frontier 0, no childless node) | 64 / 64 | 9 (root + 8 at σ1, all at cap 1, by design) | 9 (8 children each) | 90 | 3,926 | 2,536 | 11:33–12:10 |
| 28 | 0s0-5s0_1 | H6(5,0)/one | **closed** (open frontier 0, no childless node) | 64 / 64 | 9 (root + 8 at σ1, all at cap 1, by design) | 9 (8 children each) | 258 | 8,757 | 2,687 | 12:10–13:16 |

Every 6-bit cube was certified at the 300 s cap on its first attempt; no cube timed out, so the layer split at cap 600
was never used. All 128 certified records have lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. No split
record has `"children": 0`. Solve and check times are summed per node (3 jobs on 4 cores), not wall-clock.

## Totals per stratum

| stratum | roots | closed | certified nodes | solve s | check s |
|---------|-------|--------|-----------------|---------|---------|
| H6(4,0)/one | 1 | 1 | 64 | 3,926 | 2,536 |
| H6(5,0)/one | 1 | 1 | 64 | 8,757 | 2,687 |
| total | 2 | 2 | 128 | 12,683 | 5,223 |

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none; no record with cake_lpr `none`; `recheck.jsonl` not needed.
- Memory: peak used about 9 GB of 15 GB; no failures.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (164 records), `driver.log.tail`, `README.md`.

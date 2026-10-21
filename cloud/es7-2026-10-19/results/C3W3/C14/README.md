# C3W3 / C14: list C_s1two.tsv, shard 14 of 18 (one lane, --jobs 3, slice 2.0 h, 6 h budget)

**Result: 4 roots closed, 1 partial, 27 not reached. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:43:20 UTC, END 10:28:20 UTC (2026-10-21).
- C3-S tools: worktree of 132398c (132398cdc801…; 8dc27c3 before the author rewrite) at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example: `s VERIFIED UNSAT`);
  lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 + E2 patch. Sanity: `3 0 0` on {1},{-1} rejected by both, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches). Details in `tools.txt`.
- Roots: rows of `lists/C_s1two.tsv` with row ≡ 14 (mod 18): 32 roots (`roots.tsv`), one lane (`lane0.sh`).

## Seeding

1543 records seeded at the start of `/opt/work/out0.jsonl` (not in the committed `out.jsonl`, which holds only the 2196 new records):
- `0s0-2s1_1s0-4s1` (row 14): 494 certified + 8 split, from C3WAVE2/K27/out.jsonl
- `0s0-1s1_4s0-10s0` (row 302): 542 certified + 8 split, from C3WAVE2/K06/out.jsonl (root not reached)
- `0s0-2s1_1s1-10s1` (row 320): 483 certified + 8 split, from C3WAVE2/K37/out.jsonl (root not reached)

## Per root (depth = number of layers; roots are at depth 2; times summed per node, in seconds)

| row | root | stratum | list status | status | certified by depth (new) | timeouts | splits | solve s | check s |
|-----|------|---------|-------------|--------|--------------------------|----------|--------|---------|---------|
| 14 | 0s0-2s1_1s0-4s1 | H6(2,1)/two | partial | **closed** | d3: 52 | 0 | 0 (8 seeded) | 2411 | 1507 |
| 32 | 0s0-2s1_1s0-6s1 | H6(2,1)/two | untouched | **closed** | d3: 84, d4: 462 | d2: 1 (300 s) | 8 (1 + 7 pre-split) | 5209 | 8421 |
| 50 | 0s0-2s1_3s1-8s1 | H6(2,1)/two | untouched | **closed** | d3: 84, d4: 462 | d2: 1 | 8 | 5669 | 9043 |
| 68 | 0s0-2s1_5s0-6s1 | H6(2,1)/two | untouched | **closed** | d3: 84, d4: 462 | d2: 1 | 8 | 7196 | 9229 |
| 86 | 0s0-3s1_1s0-5s1 | H6(3,1)/two | untouched | partial | d3: 8, d4: 462 | d2: 1 | 8 | 3353 | 6912 |
| 104–572 | the other 27 roots (`roots.tsv`) | | | not reached | – | – | – | – | – |

Root 86 (0.97 h slice, started 09:30): split into 91 depth-3 children, 7 of them single-orbit and pre-split into 462 depth-4 nodes, all certified;
8 of the 84 two-orbit depth-3 nodes certified, 76 open. The driver checks its time limit only between batches, so it ran past END;
I stopped it by hand at 10:31 UTC (in-flight nodes left no record, so no `cake_lpr: none` records exist and no re-check was needed).

## Totals per stratum

| stratum | roots | closed | partial | not reached | certified (new) | timeouts | solve s | check s |
|---------|-------|--------|---------|-------------|-----------------|----------|---------|---------|
| H6(1,1)/two | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| H6(2,1)/two | 8 | 4 | 0 | 4 | 1690 | 3 | 20485 | 28200 |
| H6(3,1)/two | 8 | 0 | 1 | 7 | 470 | 1 | 3353 | 6912 |
| H6(4,1)/two | 8 | 0 | 0 | 8 | 0 | 0 | 0 | 0 |
| H6(5,1)/two | 7 | 0 | 0 | 7 | 0 | 0 | 0 | 0 |
| total | 32 | 4 | 1 | 27 | 2160 | 4 | 23838 | 35112 |

`out.jsonl`: 2196 new records = 2160 certified (each with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`), 32 split, 4 UNKNOWN (300 s cap).

## compose.py

`compose.py /opt/work/base.cnf out.jsonl` (`compose.txt`): 2160 certified nodes, class not covered (expected for one shard).

## SAT / proof rejections / memory

- SAT: none. PROOF NOT ACCEPTED: none. Memory: peak about 9 GB used of 15 GB, no problem.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `out.jsonl` (new records only), `driver0.log` (last 100 lines), `compose.txt`.

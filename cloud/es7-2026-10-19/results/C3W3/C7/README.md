# C3W3 / C7: list C_s1two.tsv, shard 7 of 18, 1 lane, --jobs 3, slice 2.0 h, H = 6.0 h

**Result: 5 of my 33 roots closed, 1 partial, 27 not reached. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:42:41 UTC on 2026-10-21; END = start + 6 h − 15 min = 10:27:41.
Tools as `tools.txt`, all checks passed:

- C3-S tools: worktree of 132398c at /opt/c3s, unmodified.
- CaDiCaL 3.0.1, c60730422e758ef1cebe7aeddf2dda31c996bf04.
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`), example prints `s VERIFIED UNSAT`.
- lrat-check from drat-trim 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 + E2 patch. Sanity check: `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).

Roots: rows of `lists/C_s1two.tsv` with row ≡ 7 (mod 18), 33 roots (`roots.tsv`). One lane (`lane0.sh`), as the task specifies.

**Seeded records: 663** (certified or split records from C3WAVE1/C3WAVE2/C3S0 out/recheck files) for the three `partial` roots:
0s0-1s1_3s1-7s0: 143, 0s0-3s1_1s0-7s1: 170, 0s0-1s1_6s1-9s0: 350. They are not in `out.jsonl`, which holds only the 2,244 new records.

## Per root (roots are at depth 2; only new records counted)

| row | root | stratum | list status | status | certified by depth | timeouts (300 s) | solve s | check s |
|-----|------|---------|-------------|--------|--------------------|------------------|---------|---------|
| 7 | 0s0-1s1_3s1-7s0 | H6(1,1)/two | partial | **closed** | d3: 84, d4: 327 | 0 | 4033 | 6394 |
| 25 | 0s0-3s1_1s0-7s1 | H6(3,1)/two | partial | **closed** | d3: 84, d4: 300 | 0 | 3030 | 5921 |
| 43 | 0s0-2s1_3s0-9s1 | H6(2,1)/two | untouched | **closed** | d2: 1 | 0 | 99 | 27 |
| 61 | 0s0-2s1_4s1-6s0 | H6(2,1)/two | untouched | **closed** | d3: 84, d4: 462 | 1 (the root) | 7181 | 9175 |
| 79 | 0s0-3s1_1s0-10s0 | H6(3,1)/two | untouched | **closed** | d3: 84, d4: 462 | 1 (the root) | 6124 | 8629 |
| 97 | 0s0-3s1_1s1-5s0 | H6(3,1)/two | untouched | partial | d4: 329 | 1 (the root) | 2276 | 4686 |
| 115–583 | the other 27 rows of `roots.tsv` | | | not reached | – | – | – | – |

Row 313 (0s0-1s1_6s1-9s0, list status partial) was not reached; its 350 seeded records stay as they were.
Solve and check times are summed per node (3 jobs on 4 cores, so not wall clock). Each timed-out root was split (24 split records in all, incl. pre-splits).

## Totals per stratum (new records)

| stratum | roots | closed | partial | not reached | certified | timeouts | solve s | check s |
|---------|-------|--------|---------|-------------|-----------|----------|---------|---------|
| H6(1,1)/two | 2 | 1 | 0 | 1 (row 313, seeded partial) | 411 | 0 | 4033 | 6394 |
| H6(2,1)/two | 6 | 2 | 0 | 4 | 547 | 1 | 7280 | 9202 |
| H6(3,1)/two | 9 | 2 | 1 | 6 | 1259 | 2 | 11430 | 19236 |
| H6(4,1)/two | 8 | 0 | 0 | 8 | 0 | 0 | 0 | 0 |
| H6(5,1)/two | 8 | 0 | 0 | 8 | 0 | 0 | 0 | 0 |
| total | 33 | 5 | 1 | 27 | 2217 | 3 | 22743 | 35532 |

All 2,217 new certified records have `c VERIFIED` (lrat-check) and `s VERIFIED UNSAT` (cake_lpr).

## compose.py

`compose.py /opt/work/base.cnf out.jsonl` (`compose.txt`): `certified_nodes: 2217, class_covered: false`, as expected (new records only, one shard).

## SAT / proof rejections / memory / incidents

- SAT: none. PROOF NOT ACCEPTED: none. No `cake_lpr: none` records. No memory errors (free memory never under ~4 GB).
- Early stop (my error): `close_tree.py` checks its deadline only between batches, so I stopped the lane by hand at END. I computed the END epoch wrong and killed it at **10:21:10 instead of 10:27:41**, 6.5 minutes early, while root 97 was mid-batch. The in-flight nodes had no records written, so nothing incorrect was recorded; root 97 resumes from `out.jsonl`.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `out.jsonl` (new records only), `driver0.log` (last 100 lines), `compose.txt`, `README.md`.

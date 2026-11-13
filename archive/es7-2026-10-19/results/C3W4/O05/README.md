# C3W4 / O05: W4_one.tsv, shard 5 of 16

**Result: all 3 of my roots are closed (open frontier 0, no childless timed-out node). No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:02 UTC on 2026-10-24, END 16:16:02; the runner (`runner.sh`) ran 11:42:31 to 15:01:10 and finished all roots before END.

- C3U tools: worktree of commit 95cafa93 at `/opt/c3u`, unmodified.
- CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (example: `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch. Sanity check passed: on {1},{-1}, `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both (`tools.txt`).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Roots: the rows of `W4_one.tsv` with row ≡ 5 (mod 16): rows 5, 21, 37 (`roots.tsv`). Nothing was seeded; every root started fresh.
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, slice 2.5 h.
- `compose.py` was not run, as the task says.

## Per root

Each root timed out at cap 1 and was σ-split on bits 3 to 5 into 8 nodes. Each of those timed out at cap 1 and was split on 3 more bits, giving 64 cubes with 6 σ bits (σ level 2, 268 units). All 64 cubes of every root were certified at cap 300. No cube timed out, so the layer split (cap 600) was never used.

| row | root | stratum | list status | result | certified (σ level 2, cap 300) | timeouts (cap 1, split into 8) | solve s | check s | max cube solve s | wall |
|-----|------|---------|-------------|--------|------|------|------|------|------|------|
| 5 | 0s0-2s1_1 | H6(2,1)/one | partial | **closed** | 64 | 9 | 12247 | 2893 | 263.6 | 11:42–13:07 |
| 21 | 0s0-4s0_1 | H6(4,0)/one | untouched | **closed** | 64 | 9 | 4716 | 2284 | 130.9 | 13:07–13:48 |
| 37 | 0s0-5s1_8 | H6(5,1)/one | untouched | **closed** | 64 | 9 | 10210 | 2600 | 247.0 | 13:48–15:01 |

All three roots are depth 2 and have no layer-split nodes. Solve and check times are summed over nodes. With 3 jobs on 4 cores they are not wall-clock times.

## Totals

There is one stratum per root (H6(2,1)/one, H6(4,0)/one, H6(5,1)/one), so each stratum total is the row above. Overall: 3 of 3 roots closed; 192 certified nodes, each with `c VERIFIED` (lrat-check) and `s VERIFIED UNSAT` (cake_lpr); 27 timeouts at cap 1, each split into 8 children (no `"children": 0` record); solve 27,173 s, check 7,777 s. `out.jsonl` has 246 records.

## SAT / rejections / incidents

- SAT: none.
- PROOF NOT ACCEPTED: none. No cake_lpr `none`, so `recheck.jsonl` was not needed.
- Memory: at most about 6 GB used of 15 GB.
- Two pushes were rejected (one HTTP 403 and one non-fast-forward). Both went through on retry, so the fallback branch was not used.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records), `driver.log.tail` (last 100 lines of the driver log).

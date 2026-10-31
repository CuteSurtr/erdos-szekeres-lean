# C3W4 / H24: W4_H3.tsv shard 24 of 30, σ-cube splitting, one machine

**Result: root 1 (`0s0_1s1-2s0`) partial; roots 2–3 not reached. No SAT. No proof rejection. No memory problem.**
All 64 six-bit σ-cubes of root 1 timed out at 300 s (none certified). Their layer-split children are easy
(375 certified at cap 600, 0 timeouts, max solve 165 s), but there are 64 × 51 = 3,264 of them.

## Setup
- One VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:29 UTC, END 16:16:29 UTC (start + 5 h − 15 min).
- Tools (`tools.txt`): worktree of 95cafa93 at /opt/c3u, unmodified; CaDiCaL c6073042 (3.0.1); cake_lpr a36874a8
  (example `s VERIFIED UNSAT`); lrat-check 2e3b2dc + E2 patch (sanity check passed: `3 0 0` rejected by both,
  `3 0 1 2 0` accepted by both). Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Roots: rows of `W4_H3.tsv` with row ≡ 24 (mod 30): rows 24, 54, 84, all `H3/two`, untouched (`roots.tsv`). Nothing seeded.
- `runner.sh`: `close_tree.py /opt/work/base.cnf /opt/work/out.jsonl R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S`, S = min(2.0, hours left).
- No `compose.py` was run.

## Per root

| row | root | status | certified (depth 3 layer node under 6 σ bits) | timeouts | splits | solve s | check s |
|-----|------|--------|-----|----------|--------|---------|---------|
| 24 | 0s0_1s1-2s0 | **partial** (open frontier 2,889) | 375 | root and 8 three-bit cubes at cap 1 (by design); 64/64 six-bit cubes at cap 300 | 1 σ (8), 8 σ (8 each), 64 layer (51 each) | 35,849 | 14,488 |
| 54 | 0s0_2s1-3s1 | not reached | – | – | – | – | – |
| 84 | 0s0_3s1-8s0 | not reached | – | – | – | – | – |

Root 1 in detail:
- Cap 1 at the root and the 8 three-bit cubes gave the 64 six-bit cubes at once (11:35). All 64 timed out at
  300 s (11:36–13:27, 19,200 s of solve time) and each was layer-split into 51 children.
- The 3,264 layer children (cap 600) ran in one batch from 13:27. When stopped, 375 had been certified, all with
  lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. None timed out. Certified solve times added up to 16,629 s
  (max 164.8 s), check times to 14,488 s (max 84.7 s). That is about 44 s of solve time per child, so the batch
  would need ~2,900 × 44 / 3 s ≈ 12 more hours.
- Seven six-bit cubes are fully closed (51/51 children certified): `__3s0-4s0-5s0-6s0-7s0-8s0`, `…-7s0-8s1`,
  `…-7s1-8s0`, `…-7s1-8s1`, `__3s0-4s0-5s0-6s1-7s0-8s0`, `…-6s1-7s0-8s1`, `…-6s1-7s1-8s0`. The eighth,
  `__3s0-4s0-5s0-6s1-7s1-8s1`, has 18/51. The other 56 cubes have no children certified yet.
  Open frontier: 56 × 51 + 33 = 2,889 nodes, all never attempted (no childless timed-out node).
- Records by kind: 375 certified (depth 3, 6 σ bits); 73 UNKNOWN (1 root and 8 cubes at cap 1, 64 cubes at cap 300);
  73 split records (1 + 8 σ splits with 8 children, 64 layer splits with 51 children). No record has `"children": 0`.

## Totals (stratum H3/two)
1 root partial, 2 not reached, 0 closed; 375 certified nodes; 64 timeouts at 300 s; solve 35,849 s, check 14,488 s (summed per node, 3 jobs on 4 cores).

## SAT / rejections / memory / incidents
- SAT: none. PROOF NOT ACCEPTED: none. No certified-looking record with cake_lpr `none`, so `recheck.jsonl` is not needed.
- Memory: peak use about 9 GB of 15 GB. No problem.
- Slice: `close_tree.py` checks `--hours` only between batches. The 3,264-node layer batch started at 13:27,
  before root 1's 2 h deadline (13:35), so it ran until END. That is why roots 2 and 3 were never reached.
- Stop: the runner was killed at 16:16:33. My first kill command also killed my own shell (pkill -f matched its
  own command line), so `close_tree.py` and its solvers were killed by PID at 16:22. Killed workers write no record,
  so `out.jsonl` has only complete records (certified ones in this window included).
- Pushes: es7-cloud had heavy push contention; all pushes succeeded with pull --rebase retries (no fallback branch).

## Observation
On this H3/two root the 6-bit σ-cube route did not work: none of 64 cubes closed in 300 s. C3SIG2 had
reported ~100–250 s per cube. The layer split under the cubes works (100% at ≤165 s), but it costs ~51 × 44 s per cube.

## Files
`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all 521 records), `driver.log.tail`, `README.md`.

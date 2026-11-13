# C3WAVE2 K36 (shard 36 of 40, 1.5 h budget)

Start 00:31:25 UTC 2026-10-21; END (start + 1.5 h - 15 min) 01:46:25 UTC. Task: `results/C3WAVE2/TASK.md` at 852bee7.

## Tools and base CNF (`tools.txt`, `env.txt`)
- C3-S tools: worktree of 132398c at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (`example` prints `s VERIFIED UNSAT`), drat-trim lrat-check 2e3b2dc + `lrat-check-E2.patch`.
  Sanity check: `3 0 0` on {1},{-1} rejected by both checkers; `3 0 1 2 0` accepted by both (`c VERIFIED` / `s VERIFIED UNSAT`).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 bf0e502e...cdd6da: matches.
- Machine: 4 cores, 15 GB RAM.

## Roots
33 roots (idx ≡ 36 mod 40, `roots.tsv`). Only the first root was reached.

| root | status | certified nodes (depth 3 / 4) | splits | solve s | check s |
|---|---|---|---|---|---|
| 0s0-1s1_7s0-8s1 (idx 36) | partial | 514 (52 / 462) | 14 (see below) | 4501 | 7968 |
| the other 32 roots | not reached | 0 | 0 | 0 | 0 |

Splits: root `0s0-1s1_7s0-8s1` (91 children) after an UNKNOWN; depth-3 node `0s0-1s1_7s0-8s1_4s1-9s0` (45 children) after a 300 s UNKNOWN; the other 12 are pre-splits from `--split-singles`.

Closed roots: none. Partial roots: `0s0-1s1_7s0-8s1`. Not reached: the other 32 in `roots.tsv`.

Why only one root: `close_tree.py` checks its `--hours` deadline only between layers, and it hands a whole layer to the pool at once. The depth-4 layer of this root (hundreds of nodes, about 10 s solve + 15 to 20 s check each, 3 jobs) did not finish within the 10-minute slice, so the root ran until END. At END I stopped the runner and its workers (in-flight jobs were killed; every finished record is kept in `out.jsonl` for a later wave to resume).

## Proof rejection (caused by my stop, re-checked)
When I killed the in-flight checkers at END, node `0s0-1s1_7s0-8s1_4s0-9s0` had `lrat_check: c VERIFIED` and `cake_lpr: none` (the cake_lpr process was killed), so the driver printed `PROOF NOT ACCEPTED`. It was not a real rejection. I re-ran the node alone (`close_tree.py ... --jobs 1 --caps 300`, `recheck.jsonl`): same CNF sha256 5f53073d...449b, same proof size 87,813,894 bytes, `c VERIFIED` and `s VERIFIED UNSAT`, certified. `out.jsonl` still has the uncertified record; `recheck.jsonl` has the certified one.

## Totals
514 certified nodes in `out.jsonl` (+1 in `recheck.jsonl`), 0 SAT, no real proof rejection, no memory problems (peak about 6 GB used). `compose.txt`: 514 certified nodes, class not covered (as expected), 194 uncovered frontier nodes.

Files: env.txt, tools.txt, roots.tsv, runner.sh, out.jsonl, recheck.jsonl, driver.log.tail, compose.txt.

# C2P M22 (LIST = C2P.tsv, j = 22, N = 42, H = 3.5, Z = fb2c59af): stopped at step 1

Start 2026-10-31 02:57 UTC. The run stopped at step 1 because the tools could not be built, so no lane was started.

## Tools and checks
- Sources cloned at the pinned commits: CaDiCaL c6073042, cake_lpr a36874a8, drat-trim 2e3b2dc.
- **Not built.** This session's execution policy refused to build and run code fetched from outside the
  repository. No cadical, cake_lpr or lrat-check binary exists, and the checker sanity tests were not run.
- Base CNF: header `p cnf 838032 16653336`; both sha256 values (base.cnf `b0061e90…`, base.json `2476fafff…`) match.
- Cubes P1..P8: all 8 byte-identical to `C2P/cubes/`.

## Units
`units.tsv` holds 54 units (idx ≡ 22 mod 42): P1 5H+2Q, P2 5H+1Q+cover, P3 4H+2Q, P4 6H+1Q,
P5 5H+2Q, P6 6H+1Q, P7 6H+1Q, P8 5H (44 H, 9 Q, 1 cover: `P2_cover`). None was reached: no certified
units, timeouts or errors. `run.sh` and `out.jsonl` were not created.

## SAT, rejection, memory
None. Nothing was solved.

## To resume
Run this shard again in an environment where building the three tools is allowed. The base and cube checks above can be reused.

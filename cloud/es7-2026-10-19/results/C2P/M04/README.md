# C2P M04 (LIST = C2P.tsv, j = 4, N = 42, H = 3.5, Z = fb2c59af): stopped at step 1

Start 2026-10-31 02:56 UTC. The run stopped at step 1 because the tools could not be built, so no lane was started.

## Tools and checks
- The sources were cloned at the pinned commits: CaDiCaL c6073042, cake_lpr a36874a8 and drat-trim 2e3b2dc.
- **Not built.** This session's execution policy refused to compile and run code fetched from outside the repository (`./configure && make` for CaDiCaL). So there is no cadical, cake_lpr or lrat-check binary in `/opt/work/bin/`, and the checker sanity tests were not run.
- Base CNF: header `p cnf 838032 16653336`. Both sha256 values (base.cnf `b0061e90…`, base.json `2476fafff…`) match.
- Cubes P1..P8: all 8 are byte-identical to `C2P/cubes/`.

## Units
`units.tsv` holds 54 units (idx ≡ 4 mod 42): 42 H, 11 Q and 1 cover (`P6_cover`), spread over P1..P8. None of them was reached, so there are no certified units, timeouts or errors. `run.sh` and `out.jsonl` were not created.

## SAT, rejection, memory
None. Nothing was solved.

## To resume
Run this shard again in an environment where building the three tools is allowed. The base and cube checks above can be reused.

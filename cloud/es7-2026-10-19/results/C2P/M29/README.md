# C2P M29 (LIST = C2P.tsv, j = 29, N = 42, H = 3.5, Z = fb2c59af): stopped at step 1

Start 2026-10-31 02:57 UTC. The run stopped at step 1 because the tools could not be built, so no lane was started.

## Tools and checks
- Sources cloned at the pinned commits: CaDiCaL c6073042, cake_lpr a36874a8, drat-trim 2e3b2dc.
- **Not built.** This session's permission policy refused to compile and run the cloned external code (CaDiCaL `./configure && make`, cake_lpr, lrat-check). No binaries, no checker sanity tests.
- Base CNF: header `p cnf 838032 16653336`; both sha256 values (base.cnf `b0061e90…`, base.json `2476fafff…`) match.
- Cubes P1..P8: all 8 byte-identical to `C2P/cubes/`.

## Units
`units.tsv`: 53 units (idx ≡ 29 mod 42), 41 H and 12 Q, no cover.
By case (H/Q): P1 6/1, P2 6/1, P3 5/2, P4 5/1, P5 5/2, P6 6/1, P7 5/2, P8 3/2.
All 53 not reached: 0 certified, 0 UNKNOWN, 0 errors. No `run.sh` or `out.jsonl`.

## SAT, rejection, memory
None; nothing was solved.

## To resume
Run this shard in an environment where building the three tools is allowed; the base and cube checks above can be reused.

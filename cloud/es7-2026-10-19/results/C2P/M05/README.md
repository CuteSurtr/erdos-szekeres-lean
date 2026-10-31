# C2P M05 (LIST = C2P.tsv, j = 5, N = 42, H = 3.5, Z = fb2c59af): stopped at step 1

Start 2026-10-31 02:56 UTC. **No unit was run.** Building the tools (CaDiCaL `./configure && make`)
was refused by this session's permission policy as running code fetched from outside the repository,
so cadical, cake_lpr and lrat-check do not exist here and the lane could not be started. This is the
same failure as M01 and M03.

## Tools and checks (`tools.txt`)
- Sources cloned at the pinned commits: CaDiCaL c6073042, cake_lpr a36874a8, drat-trim 2e3b2dc.
- Not built; checker sanity tests not run.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf (`b0061e90…`) and base.json (`2476fafff…`) match.
- Cubes P1..P8: all 8 byte-identical to `C2P/cubes/` (560 lines each).

## Units (`units.tsv`)
54 units (idx ≡ 5 mod 42): P1–P6 7 each, P7 6, P8 6; 44 H and 10 Q, no cover.
Certified 0, timed out 0, errors 0, not reached 54. No `run.sh` or `out.jsonl` (no lane started).

## SAT, rejection, memory
None. Nothing was solved; no solver RSS to report.

## To resume
Run this shard again in a session where building the three tools is allowed. The base and cube checks above can be reused.

# C2P M15 (LIST = C2P.tsv, j = 15, N = 42, H = 3.5, TASK.md at fb2c59af)

Stopped at step 1: the tool build was refused, so no unit was run.

## Tools
- The three sources were cloned into /opt/src at the required commits: CaDiCaL c6073042, cake_lpr a36874a8 and drat-trim 2e3b2dc. They have not been built. In this session the permission classifier refused the command that applies `E2/tools/lrat-check-E2.patch` and compiles CaDiCaL, cake_lpr and lrat-check. So no solver or checker binary exists, and the checker sanity checks were not run.
- Base CNF and cube checks pass (`tools.txt`): the header is `p cnf 838032 16653336`, both sha256 match, and all 8 cube files are byte-identical.

## Units
- 53 units (`units.tsv`; idx ≡ 15 mod 42), none reached.
- By case and kind (H/Q): P1 4/2, P2 6/1, P3 6/1, P4 6/1, P5 6/1, P6 5/2, P7 6/1, P8 3/2.
- Certified 0, UNKNOWN 0, errors 0. No lane was started (no `run.sh`, `out.jsonl` or `lane.log.tail`).
- Largest solver RSS: none, since nothing ran.
- No SAT, no proof rejection and no memory problem.

To run this shard, the build step needs to be allowed in the session's permissions. Then start again from step 1.

# C2P / M08 (LIST C2P.tsv, shard 8 of 42, H = 3.5, Z = fb2c59af)

**Result: stopped at step 1. No unit was run.** Start 2026-10-31 02:56 UTC. The tool build (CaDiCaL, cake_lpr, lrat-check with the E2 patch) was refused by this session's permission policy, so the lane could not be started.

## Tools and checks (`tools.txt`)
- Sources cloned at the pinned commits: CaDiCaL c6073042, cake_lpr a36874a8, drat-trim 2e3b2dc.
- Not built, so no binaries and no checker sanity tests.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf (`b0061e90…`) and base.json (`2476fafff…`) both match.
- Cubes P1..P8: all 8 byte-identical to `C2P/cubes/`.

## Units (`units.tsv`, idx ≡ 8 mod 42)
54 units, 43 H and 11 Q, no cover:

| case | H | Q |
|---|---|---|
| P1 | 6 | 1 |
| P2 | 6 | 1 |
| P3 | 6 | 1 |
| P4 | 5 | 2 |
| P5 | 6 | 1 |
| P6 | 5 | 2 |
| P7 | 5 | 1 |
| P8 | 4 | 2 |

Certified 0, timed out 0, errors 0, not reached 54. `run.sh` and `out.jsonl` were not created. No solver ran, so there is no RSS figure.

## SAT, proof rejection, memory
None. Nothing was solved.

## To resume
Run this shard again in an environment where building the three tools is allowed. The base and cube checks above can be reused.

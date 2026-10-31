# C2P M34 (LIST = C2P.tsv, j = 34, N = 42, H = 3.5, TASK.md at fb2c59af)

Status: **stopped at step 1. No unit was run.**

- Tool sources were cloned at the required commits (CaDiCaL c6073042, cake_lpr a36874a8, drat-trim 2e3b2dc).
  The build command was refused by the session's permission classifier ("Code from External"). That means no
  cadical, cake_lpr or lrat-check binaries, and no checker sanity tests. M01 stopped at the same point.
- Base CNF check passed: header `p cnf 838032 16653336`, and both sha256 values match (base.cnf b0061e90…, base.json 2476faff…).
- Cube check passed: P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).
- Units: 53 rows (idx ≡ 34 mod 42) in `units.tsv`. None reached: P1 6H+1Q, P2 6H+1Q, P3 5H+2Q, P4 5H+1Q+cover,
  P5 4H+2Q, P6 6H+1Q, P7 5H+2Q, P8 5H. Certified 0, UNKNOWN 0, errors 0.
- No SAT, no proof rejection and no memory problem, because nothing was solved.

To redo this shard, run it in a session where the tool build is allowed.

# C2P M06 (LIST=C2P.tsv, j=6, N=42, H=3.5, TASK.md at fb2c59af)

Stopped at step 1: the tool build was refused by the session's permission layer, so no unit was run.

- Tool sources were cloned at the required commits (CaDiCaL c6073042, cake_lpr a36874a8, drat-trim 2e3b2dc),
  but building them (`./configure && make -j4`, `make cake_lpr`) was denied ("Code from External").
  No solver or checker binary exists, so the checker sanity checks were not run.
- Base CNF check: passed (header `p cnf 838032 16653336`, both sha256 match).
- Cube check: passed (P1..P8 byte-identical).
- Units: 54 (`units.tsv`: idx ≡ 6 mod 42): 46 H (cap 1800 s), 8 Q (cap 2400 s), no cover unit;
  by case P1 7, P2 7, P3 7, P4 7, P5 7, P6 7, P7 6, P8 6.
  Certified 0, timed out 0, errors 0, not reached 54.
- No SAT, no proof rejection, no memory problem (nothing ran).

See `tools.txt`. M01 hit the same refusal.

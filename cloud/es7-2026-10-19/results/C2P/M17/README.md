# C2P / M17 (LIST C2P.tsv, shard 17 of 42, H = 3.5, Z = fb2c59af)

**Result: stopped at step 1. No unit was run.** This session's permission policy refused the tool build
(CaDiCaL, cake_lpr, lrat-check with the E2 patch), so the lane could not start. M01 hit the same refusal.

- Done: env.txt; sources cloned at the required commits; base CNF header and both sha256 match;
  all 8 cube files byte-identical (`tools.txt`); 53 units written to `units.tsv`: P1 7, P2 6, P3–P7 7 each, P8 5;
  42 H and 11 Q, no cover.
- Not done: the build and its sanity checks, the lane, and all 53 units (none reached). Certified 0, UNKNOWN 0, errors 0.
- Largest solver RSS: none, since nothing was solved.
- No SAT, no proof rejection, no memory problem.

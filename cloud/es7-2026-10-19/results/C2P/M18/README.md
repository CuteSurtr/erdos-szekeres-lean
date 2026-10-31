# C2P / M18 (LIST C2P.tsv, shard 18 of 42, H = 3.5, Z = fb2c59af)

**Result: stopped at step 1. No unit was run.** The tool build (CaDiCaL, cake_lpr, lrat-check with
the E2 patch) was refused by this session's permission policy, so the lane could not be started.
This is the same thing that happened on M01.

- Done: env.txt; sources cloned at the required commits; base CNF header and both sha256 match;
  all 8 cube files byte-identical (`tools.txt`); 53 units written (`units.tsv`).
- Units by case: P1 7, P2 6, P3 7, P4 7, P5 7, P6 7, P7 7, P8 5; by kind: 44 H, 9 Q, no cover.
- Not done: build and sanity checks, lane, all 53 units (not reached: 0 certified, 0 UNKNOWN, 0 errors).
- No SAT, no proof rejection, no memory problem (nothing was solved).

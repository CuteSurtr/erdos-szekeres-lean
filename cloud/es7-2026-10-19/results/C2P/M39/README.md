# C2P / M39 (LIST C2P.tsv, shard 39 of 42, H = 3.5, Z = fb2c59af)

**Result: stopped at step 1. No unit was run.** This session's permission policy refused the tool build
(CaDiCaL, cake_lpr, lrat-check with the E2 patch), so the lane could not be started. This is the same as M01.

- Done: env.txt. Sources cloned at the required commits. Base CNF header and both sha256 match.
  All 8 cube files are byte-identical (`tools.txt`). 53 units written to `units.tsv`:
  P1 6H+1Q, P2 6H+1Q, P3 5H+2Q, P4 6H+1Q, P5 4H+2Q, P6 6H+1Q, P7 6H+1Q, P8 5H (45 H, 8 Q, no cover).
- Not done: the build and its sanity checks, the lane, and all 53 units (not reached). No run.sh, because the lane was never started.
- No SAT, no proof rejection, no memory problem (nothing was solved).

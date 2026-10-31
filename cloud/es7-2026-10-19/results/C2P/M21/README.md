# C2P / M21 (LIST C2P.tsv, shard 21 of 42, H = 3.5, Z = fb2c59af)

**Result: stopped at step 1. No unit was run.** The tool build (`./configure && make -j4` for
CaDiCaL; cake_lpr and lrat-check were never reached) was refused by this session's permission
policy, so the checkers and the solver do not exist here and the lane could not be started.
This is the same blocker as M01.

- Done: env.txt; sources cloned at the required commits; base CNF header and both sha256 match;
  all 8 cube files byte-identical (`tools.txt`); 53 units written (`units.tsv`: 42 H and 11 Q,
  no cover; P1 6H+1Q, P2 4H+2Q, P3 6H+1Q, P4 6H+1Q, P5 6H+1Q, P6 6H+1Q, P7 5H+2Q, P8 3H+2Q).
- Not done: tool build and checker sanity checks, run.sh, lane, out.jsonl.
- Units: 0 certified, 0 timed out, 53 not reached, 0 errors. No largest RSS (nothing was solved).
- No SAT, no proof rejection, no memory problem.

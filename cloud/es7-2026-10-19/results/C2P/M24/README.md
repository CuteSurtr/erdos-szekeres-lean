# C2P / M24 (LIST C2P.tsv, shard 24 of 42, H = 3.5, Z = fb2c59af)

**Result: stopped at step 1. No unit was run.** The tool build (CaDiCaL, cake_lpr, lrat-check with
the E2 patch) was refused by this session's permission policy, so the lane could not be started
(same outcome as M01).

- Done: env.txt; sources cloned at the required commits; base CNF header and both sha256 match;
  all 8 cube files byte-identical (`tools.txt`); 53 units written (`units.tsv`):
  P1 6H+1Q, P2 6H+1Q, P3 5H+1Q, P4 6H+1Q, P5 5H+2Q, P6 6H+1Q, P7 5H+2Q, P8 4H+1Q;
  43 H and 10 Q, no cover.
- Not done: tool build and checker sanity checks, lane (no run.sh), all 53 units (not reached).
- Certified 0, UNKNOWN 0, errors 0, not reached 53. No solver RSS to report.
- No SAT, no proof rejection, no memory problem (nothing was solved).

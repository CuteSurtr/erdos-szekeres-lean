# C2P / M14 (LIST C2P.tsv, shard 14 of 42, H = 3.5, Z = fb2c59af)

**Result: stopped at step 1. No unit was run.** The tool build (CaDiCaL, cake_lpr, lrat-check with
the E2 patch) was refused by this session's permission policy, so the lane could not be started
(the same outcome as M01).

- Done: env.txt; sources cloned at the required commits; base CNF header and both sha256 match;
  all 8 cube files byte-identical (`tools.txt`); 53 units written (`units.tsv`: P1 6, P2 7, P3 7, P4 7,
  P5 7, P6 7, P7 7, P8 5; 44 H and 9 Q, no cover).
- Not done: build and checker sanity checks, run.sh/lane, all 53 units (not reached).
- Certified 0, timed out 0, errors 0, not reached 53. Largest solver RSS: none (nothing solved).
- No SAT, no proof rejection, no memory problem.

# C2P / M12 (LIST C2P.tsv, shard 12 of 42, H = 3.5, Z = fb2c59af)

**Result: stopped at step 1. No unit was run.** The tool build (CaDiCaL, then cake_lpr and
lrat-check with the E2 patch) was refused by this session's permission policy, so the lane could
not be started.

- Done: env.txt; sources cloned at the required commits; base CNF header and both sha256 match;
  all 8 cube files byte-identical (`tools.txt`); 53 units written (`units.tsv`: P1 6, P2–P7 7 each,
  P8 5; 44 H and 9 Q, no cover).
- Not done: build and sanity checks, lane (no run.sh), all 53 units (not reached).
- No SAT, no proof rejection, no memory problem (nothing was solved).

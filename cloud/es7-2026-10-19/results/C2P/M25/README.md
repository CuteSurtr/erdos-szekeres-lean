# C2P / M25 (LIST C2P.tsv, shard 25 of 42, H = 3.5, Z = fb2c59af)

**Result: stopped at step 1. No unit was run.** The tool build (CaDiCaL, cake_lpr, lrat-check with
the E2 patch) was refused by this session's permission policy, so the lane could not be started (same as M01 and M03).

- Done: env.txt; sources cloned at the required commits; base CNF header and both sha256 match;
  all 8 cube files byte-identical (`tools.txt`); 53 units written (`units.tsv`: P1, P2, P4–P7 7 each, P3 6, P8 5;
  42 H and 11 Q, no cover).
- Not done: build and sanity checks, lane, all 53 units (not reached). No run.sh, out.jsonl or lane.log.tail.
- No SAT, no proof rejection, no memory problem (nothing was solved).

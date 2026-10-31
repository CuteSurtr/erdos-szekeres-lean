# C2P / M09 (LIST C2P.tsv, shard 9 of 42, H = 3.5, Z = fb2c59af)

**Result: stopped at step 1. No unit was run.** The tool build (CaDiCaL, cake_lpr, lrat-check with
the E2 patch) was refused by this session's permission policy, so the lane could not be started
(same outcome as M01 and M03).

- Done: env.txt; sources cloned at the required commits; base CNF header and both sha256 match;
  all 8 cube files byte-identical (`tools.txt`); 54 units written (`units.tsv`: P1–P4 and P6 7 each
  (6 H + 1 Q), P5 7 (5 H + 2 Q), P7 6 (4 H + 2 Q), P8 6 (5 H + 1 Q); 44 H and 10 Q, no cover).
- Not done: build and sanity checks, lane, all 54 units (not reached). No run.sh, out.jsonl or lane log.
- No SAT, no proof rejection, no memory problem (nothing was solved).

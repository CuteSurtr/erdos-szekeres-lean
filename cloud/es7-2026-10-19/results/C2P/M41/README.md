# C2P / M41 (LIST C2P.tsv, shard 41 of 42, H = 3.5, Z = fb2c59af)

**Result: stopped at step 1. No unit was run.** The tool build (CaDiCaL, cake_lpr, lrat-check with
the E2 patch) was refused by this session's permission policy, so the lane could not be started
(same outcome as M01).

- Done: env.txt; sources cloned at the required commits; base CNF header and both sha256 match;
  all 8 cube files byte-identical (`tools.txt`); 53 units written (`units.tsv`).
- Units by case and kind (all not reached): P1 6H+1Q, P2 5H+2Q, P3 6H+1Q, P4 6H+1Q, P5 5H+2Q,
  P6 5H+1Q, P7 5H+2Q, P8 5H; total 43 H and 10 Q, no cover.
- Certified 0, UNKNOWN 0, errors 0, not reached 53. No run.sh, out.jsonl or lane log (lane never started).
- No SAT, no proof rejection, no memory problem (nothing was solved).

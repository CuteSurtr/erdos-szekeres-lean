# C2P / M16 (LIST C2P.tsv, shard 16 of 42, H = 3.5, Z = fb2c59af)

**Result: stopped at step 1. No unit was run.** The tool build (CaDiCaL, cake_lpr, lrat-check with
the E2 patch) was refused by this session's permission policy, so the lane could not be started.

- Done: env.txt; sources cloned at the required commits; base CNF header and both sha256 match;
  all 8 cube files byte-identical (`tools.txt`); 53 units written (`units.tsv`).
  - By case: P1 7 (5 H, 1 Q, 1 cover), P2 6 (4 H, 2 Q), P3 7 (6 H, 1 Q), P4 7 (5 H, 2 Q),
    P5 7 (6 H, 1 Q), P6 7 (6 H, 1 Q), P7 7 (5 H, 2 Q), P8 5 (4 H, 1 Q).
  - Totals: 41 H, 11 Q, 1 cover.
- Not done: build and checker sanity checks, lane (`run.sh` not written), all 53 units (not reached).
- Certified 0, UNKNOWN 0, errors 0. No solver ran, so no RSS figure.
- No SAT, no proof rejection, no memory problem (nothing was solved).

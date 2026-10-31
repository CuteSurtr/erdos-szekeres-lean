# C2P / M33 (LIST C2P.tsv, shard 33 of 42, H = 3.5, Z = fb2c59af)

**Result: stopped at step 1. No unit was run.** The tool build (CaDiCaL, cake_lpr, lrat-check with
the E2 patch) was refused by this session's permission policy, so the lane could not be started
(same outcome as M01).

- Done: env.txt; sources cloned at the required commits (c6073042, a36874a8, 2e3b2dc); base CNF
  header and both sha256 match; all 8 cube files byte-identical (`tools.txt`).
- Units (`units.tsv`): 53 units, 42 H and 11 Q, no cover.
  P1 6H+1Q, P2 5H+2Q, P3 6H+1Q, P4 4H+2Q, P5 6H+1Q, P6 6H+1Q, P7 6H+1Q, P8 3H+2Q.
- Not done: build and sanity checks, lane (no run.sh, out.jsonl or lane.log.tail); all 53 units not reached.
- Certified 0, timed out 0, errors 0; no solver RSS to report.
- No SAT, no proof rejection, no memory problem (nothing was solved).

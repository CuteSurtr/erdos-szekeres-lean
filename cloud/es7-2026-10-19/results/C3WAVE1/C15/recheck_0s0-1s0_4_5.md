# PROOF NOT ACCEPTED 0s0-1s0_4_5 (07:58 UTC, run 1, --jobs 4): cause was memory

- Driver printed `{"node": "0s0-1s0_4_5", "status": "UNSATISFIABLE", "solve_s": 75.8, "certified": false}` then
  `PROOF NOT ACCEPTED 0s0-1s0_4_5` (run1.log). Its out.jsonl record was lost (see README, "file loss").
- dmesg: `Memory cgroup out of memory: Killed process 3427 (cake_lpr) ... anon-rss:4194560kB` at uptime 1305 s (~07:58 UTC),
  with 4 jobs (each cake_lpr reserves a 12 GB heap; 15 GB RAM, no swap).
- Re-run alone at 08:05-08:10 UTC: node CNF 328 units, sha256 5a2cef39f66f6a308125f336dbd6b01bc8c0dc3920b4b1f42b8108c0c36e5b3f;
  `cadical -q --sat --lrat --binary=false`: s UNSATISFIABLE in 75 s, proof 212,228,749 bytes;
  lrat-check (E2): `c VERIFIED` (5.3 s); cake_lpr (CML_HEAP_SIZE=12000, CML_STACK_SIZE=2000): `s VERIFIED UNSAT` (35 s).
- Not a real rejection. Resumed with --jobs 3; the driver re-solves the node and writes its own record.

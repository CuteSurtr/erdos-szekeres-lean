# Terminal n5 closure confirmed

All three formula/map audits PASS and fresh independent cake replays emit
exact `s VERIFIED UNSAT` with stable hashes:

* m7 terminal:204vars/1,143clauses, CNF1d0fb8ff...;
* m8 terminal:471vars/2,440clauses, CNF8729b508...;
* m9 pure base:210vars/2,268clauses, CNF0a2b952d....

The all-size deduction is now confirmed: explicit cup selections for m<=6,
separate certified7,8, and pure-base9 plus geometric heredity for larger
sizes. No selection monotonicity is assumed. The withdrawn m7 shortcut is
excluded, with a concrete real7 countercontrol retained.

See VERIFY_TERMINAL5.md and data/result.json. All jobs used AS300/oneCPU,
cake128/stack32, under20sec; observed maximum22,284KiB RSS. No job or heap
remains reserved. Earlier audit files are unchanged. Continuing only the
newly authorized low_split_audit formula task, without extra proof replay.

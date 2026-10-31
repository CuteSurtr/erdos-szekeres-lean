# C2P M37 (LIST C2P.tsv, j = 37, N = 42, H = 3.5, TASK.md at fb2c59af)

Stopped at step 1: the tool build was blocked. The session's permission layer denied cloning and
building CaDiCaL (c6073042), cake_lpr (a36874a8) and drat-trim lrat-check (2e3b2dc), so TASK.md's
"if any check fails, stop and report" applies. No lane was started.

- Base CNF and cube checks: all pass (header, both sha256, 8/8 cube files byte-identical); see tools.txt.
- Units: 53 (idx ≡ 37 mod 42), in units.tsv: 42 H (cap 1800 s) and 11 Q (cap 2400 s), across P1..P8.
  Certified 0, UNKNOWN 0, errors 0, not reached 53.
- No SAT, no proof rejection, no memory problem (nothing was solved).

These 53 units still need to be run on a machine where the three tools can be built.

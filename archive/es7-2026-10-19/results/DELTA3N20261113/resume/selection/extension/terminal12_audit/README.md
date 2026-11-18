# Terminal n6 minimum audit — PASS; minimum exactly12

**CERTIFIED finite components; PROVED minimum deduction:** the minimum
cardinality of a terminal-safe n6 counterexample is exactly12, among all
real x-ordered GP sets with no five-cap and no convex hexagon. The fixed12
geometry/membership audit and generic10/11 formula audits PASS; all three
fresh cake replays emit exactly `s VERIFIED UNSAT` with stable hashes.

The fixed12 set has14 four-caps,44 bad triples,134 pentagons and maxima
(cap,cup,gon)=(4,5,5). All4096 selections were checked: zero terminal-safe
and945 ordinary weak Deltas, minimum ordinary size4. All192 membership
clauses are byte-identical to our independent exact reconstruction.
Positive twelve-point controls have68,28,2 terminal-safe selections.

Generic10 has1,970vars/9,706rows; generic11 has4,060vars/17,426rows. All
map entries and clauses match the independent checker reused read-only.
Their real controls give34 and10 terminal-safe selectors. The explicit
[through9 dependency](../../boundary/audit/VERIFY_BOUNDARY.md), including
its smaller-size coverage and prior independent replay, completes the
lower bound. No ambient-size monotonicity is assumed.

[VERIFY_TERMINAL12.md](VERIFY_TERMINAL12.md) gives the complete scope,
proof, commands and hashes. Geometry uses exact integers and all-four-subset
triangle containment, not the parent's geometry checker. Only the coordinate
deletion map is used from balanced15; its full audit is not repeated.
The stronger terminal property fails; ordinary weak Delta and ES statements
are not refuted. All jobs used one CPU, AS300, wall20/CPU19, cake64/stack32.
The slowest replay was0.77s; peak RSS68,708KiB. No job or extra heap remains.

Only this directory and scratch
`/home/jay/research/data/delta3-codex-20261113/extension/terminal12-audit/`
are writable for this task. Earlier frozen audit records stay unchanged.

Proofs remain in their original scratch locations; source, dependency,
input/map and tiny fixed-proof snapshots plus commands/logs are retained
under data. Reproduction commands are data/check.command.sh and
data/replays.command.sh; choose fresh output paths for a new replay.

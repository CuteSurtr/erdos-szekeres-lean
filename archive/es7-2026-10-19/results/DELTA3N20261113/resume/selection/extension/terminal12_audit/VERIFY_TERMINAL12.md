# Independent terminal n6 minimum audit — confirmed

**CERTIFIED:** fresh cake_lpr replays accept the fixed12 membership proof
and the new generic n6 size10 and size11 counterexample-formula proofs.
**COMPUTED:** independent integer geometry, complete membership enumeration
and all generic map/row checks pass. **PROVED using these certificates and
the explicitly cited through9 result:** the global minimum cardinality of
a terminal-safe n6 counterexample is exactly12.

Scope: finite real sets in general position with distinct x coordinates,
no five-cap and no convex hexagon. A terminal-safe weak Delta A has no
four-cap, hits every convex pentagon, and every cap triple a<b<c in A has
an ambient four-cap u<v<b<c. This is the minimum for that stronger terminal
property. The example has945 ordinary weak Deltas; it does not refute weak
Delta, uniform-envelope existence, or any numerical ES statement.

## Independent fixed-instance geometry and membership

The locally indexed points are

    (0,0),(37,-35),(38,-248),(84,-270),(472,-427),(653,-757),
    (665,-793),(666,-717),(683,-718),(736,-567),(926,-895),(1000,0).

Their coordinate mapping is checked against balanced15 after removing
original indices4,11,13. Only that coordinate identity is used from the
fifteen-point record; its full geometry/model audit is not repeated.

The new implementation in `tools/check.py` imports no parent geometry or
membership checker. It uses unbounded integer determinants, strict triangle
containment on every four-subset, and the fact that a larger set is convex
iff every four-subset is convex. Caps/cups are tested by all triples.
All4096 subsets are checked. Minimum absolute determinant is45; maximum
absolute determinant895,000. Exact maxima (cap,cup,gon) are(4,5,5).
There are14 four-caps,44 unprotected cap triples and134 pentagons.

The independent membership formula uses twelve variables x_i meaning
point i is selected. A negative row forbids each complete four-cap and
each unprotected cap triple; a positive row meets each whole pentagon.
All192 rows and every byte match the parent CNF and the certificate input:

`25ca75a9eee359ca03ae7f96657128ab03693c03421b1e7e83627f529841890a`.

For every one of4096 assignments, direct clause evaluation agrees with
the independent geometric membership predicate. There are zero terminal
solutions,945 ordinary weak solutions, and minimum ordinary weak size4.
One minimum ordinary witness is A={0,2,3,6}. Ordinary counts by size4–10
are21,138,343,306,116,20,1. All family masks and exact coordinates are in
`data/fixed-case3.json`.

The other three twelve-point complements are positive controls, computed
independently by the same exact method, with terminal counts68,28,2. All
four membership CNFs are independently rebuilt and tested on all4096
assignments each. The older C++ output is only compared as a clause multiset;
its checker and generator are neither imported nor executed.

## New universal size10 and size11 cases

The accepted independent generic row checker `../audit/check.py` is reused
read-only, with bytecode disabled and none of its main/generation/output
routines invoked. Its source hash is
`513c0cb75e6f38c15907425754df9411afb123dcfa3d1651cab5c68e2b4a7990`.
Current terminal and compact source bytes match that generic audit's frozen
sources. The inherited projection proof is
[VERIFY_EXTENSION.md](../audit/VERIFY_EXTENSION.md); every new instance
map entry and clause is reconstructed here, with no fixed signs or new
geometric premise.

| n6 instance | Variables | Clauses | Literals |
|---|---:|---:|---:|
| generic m10 | 1,970 | 9,706 | 30,148 |
| generic m11 | 4,060 | 17,426 | 56,339 |

The original mapped CNFs are byte-identical to their solver inputs.
Exact real controls are the first10 and11 points of the fixed12 example;
they independently have34 and10 terminal-safe selectors. Canonical exact
geometry/containment flags satisfy every non-failure clause, and exactly
34/10 failure rows fail as expected for positive instances.

The generic encoding is sound for real counterexamples at these exact
sizes: exact bad triples and convex-pentagon leaves have their actual
geometric values; canonical containment satisfies the one-way deletion
clauses. Under no-five-cap, a selected four-cap has an unprotected prefix
triple, since protecting that prefix would extend to a five-cap. Therefore
every failed selector has a bad triple or a pentagon in its complement.
All selected sizes0 through m-4 occur. Larger terminal-safe selectors can
be thinned with the ambient set fixed until the blue complement has four
points, so the size bound loses no selector. No extension/deletion
monotonicity of the ambient terminal predicate is invoked.

## Three fresh proof replays

Each replay used cake_lpr heap64/stack32, AS300 MiB, one CPU, outer wall20/
CPU19 seconds and cake wall17/CPU16. Every fresh stdout contains exactly
`s VERIFIED UNSAT`, with successful return and stable pre/post hashes of
CNF, raw proof, compressed proof and checker. Hashing is streamed, releasing
file cache every64MiB and at the remainder. No new solver run occurred.

| Case | CNF SHA-256 |
|---|---|
| generic10 | `982fa0f5f138d3e01c656499c3adef258757919d901a0299735040a226ecab5d` |
| generic11 | `ca1637366185d883d5e78064f17e52680dd7d87516113576ff9861e4256e0c2e` |
| fixed12 | `25ca75a9eee359ca03ae7f96657128ab03693c03421b1e7e83627f529841890a` |

| Case | Binary LRAT SHA-256 | Bytes |
|---|---|---:|
| generic10 | `357fcd0680d2b245c954747b213591f67f5961bb504e68e9471eccebd9a2b208` | 2,269,027 |
| generic11 | `3c7d2c9e0056e2723c6b0bfa760ff2b365f76249b1ca2bdecead5d58ba0730a6` | 31,431,277 |
| fixed12 | `36cc74ed0a141888ed9a23ab90b2b31921025bc03183ccd2aebd18814d02d33c` | 753 |

Checker SHA-256:
`c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54`.
Commands, hashes, exact logs and timing are in `data/replay-m*.json` and
matching files. The original raw and compressed proofs remain retained.

## Through9 dependency and global-minimum deduction

The explicit inherited lower bound is the independently audited
[boundary theorem](../../boundary/audit/VERIFY_BOUNDARY.md), “Consequence”
and “Independent certificate replay”: every admissible n6 set of size at
most9 has a terminal-safe weak Delta. This is not inferred by deleting
points from size10 or11.

Its smaller-size argument can be stated directly. At size at most8, a cup
of size at least4 leaves at most4 blue points and is terminal-safe. If
maxcup is at most3, the endpoints of all pentagons lie in cup-ending rank3:
an upper chain has at most4 points, so a pentagon's lower chain has at
least3. A single rank level is terminal-safe by the reviewed rank lemma.
At size9, a five-cup suffices, while a failure in the remaining case must
have maximum cup4 and convex five-point complement to every four-cup.
The audited boundary CNF covers that localized class and all allowed
selector sizes; its accepted proof excludes it.

That prior independent n6 replay has CNF hash
`1e40345bfedd16d0130a0a00bc6a412d7a0caceb04bcd39879be99d71d9621c3`
and LRAT hash
`f34baddd285f8d0654223edf110c9e2986c43e707ff675a0aae5deedd420f9ce`.
Its exact acceptance log, stable-hash receipt and written audit are read
and copied as explicit dependencies. It is not described as a fresh replay
in this packet.

Thus every admissible real set of size0–9 is covered by that prior theorem,
size10 by its new separate certificate, and size11 by its new separate
certificate. The fixed12 example is a genuine failure. These statements
prove minimum12 across all admissible real sets for terminal n6, rather
than only within the balanced15 fixture. The old minimum18 statement for
subsets of one fixed23-point n7 set is a different scope and is unaffected.

All new exact checks finished in0.21s/23,000KiB peak RSS. Fresh cake times
were about0.05s,0.77s and under0.01s, peak68,708KiB. No job remains active,
no larger heap was reserved, and no prior record, proof or source changed.
The written proof is not a Lean formalization or a literature-priority claim.

# Independent terminal n5 closure — confirmed

**CERTIFIED:** the fresh generic terminal m7,m8 counterexample formulas and
the pure geometric m9 formula each have an independently replayed binary
LRAT accepted by cake_lpr. **COMPUTED:** their complete maps and clauses
match independent reconstruction. **PROVED (written deduction using these
certificates):** every finite real x-ordered GP set with no five-cap and no
convex pentagon admits a terminal-safe weak Delta for n=5.

Here A must contain no four-cap, meet every convex four-subset, and have
an ambient four-cap u<v<b<c for every selected cap triple a<b<c. The
ambient set is fixed throughout this condition. No ambient-size monotonicity
of terminal-safe selection is assumed.

## Formula audit and dependencies

The generic encoder interpretation is inherited from
[VERIFY_EXTENSION.md](../audit/VERIFY_EXTENSION.md). Current sources match
that audit's frozen source bytes:

* `terminal_general.cpp`:
  `7fd10250a1010d0ed18bd6e3bd85ec8c67557b650bc4db43ec06417dd542752d`.
* `resume/compact/compact_cnf.cpp`:
  `1964e17b777fd7b7a973f12b2911c003a050047f13a621f523a9f98c6e31d553`.

As explicitly authorized, `tools/check.py` imports the prior independent
`../audit/check.py` read-only; it does not invoke that file's main function,
producer, solver, generation routines or output paths. Its SHA-256 is
`513c0cb75e6f38c15907425754df9411afb123dcfa3d1651cab5c68e2b4a7990`.
Bytecode writing is disabled. All new results are confined to this packet
and its scratch directory. The pure n5/m9 base is rebuilt separately by
the new checker, including every byte of its padded header, phase comments,
rows and map. Frozen records remain unchanged.

| Formula | Variables | Clauses | Literals | Proof bytes |
|---|---:|---:|---:|---:|
| terminal n5/m7 | 204 | 1,143 | 3,325 | 1,536 |
| terminal n5/m8 | 471 | 2,440 | 7,399 | 48,255 |
| pure base n5/m9 | 210 | 2,268 | 7,056 | 83,139 |

All mapped original CNFs are byte-identical to the corresponding solver
inputs. Complete map allocation and every literal in every phase match the
independent reconstruction. There are no fixed signs or boundary assumptions.
The m9 formula contains only orientations and exact convex-four flags:
1,008 signotope rows,126 no-five-cap rows,1,008 convex-four equivalence rows,
126 no-pentagon rows. It has no selection variables or failure clauses.

For the terminal formulas, exact bad triples are caps whose last pair has
no ambient four-cap. Canonical D(S) records containment of such a triple;
canonical T(S) records containment of a convex four-subset. One-way child
clauses are sufficient for real-counterexample projection: canonical flags
satisfy them, and every forbidden selector satisfies D(A) or T(U\A).
Under no-five-cap, selected four-caps force a bad triple: otherwise protecting
their first three vertices would extend that support to a five-cap. Thus no
separate selected-four-cap failure family is lost. The tested sizes of A are
0 through m-3; larger selectors may be thinned until the blue complement
has three points, preserving terminal safety and ensuring no blue four-gon.

## Independent replay evidence

Each replay ran the current cake_lpr binary with heap128/stack32 under
AS300 MiB and one CPU. The wrapper had wall20/CPU19; cake itself had
wall17/CPU16. Each fresh stdout contains exactly the acceptance line
`s VERIFIED UNSAT`. Each process returned0, and streamed pre/post SHA-256
checks of CNF, raw proof, compressed proof, checker and receipt were stable.
Acceptance is based on the exact line, never exit status alone.

| Input | CNF SHA-256 |
|---|---|
| terminal m7 | `1d0fb8ff80d4754a37ea2eb889737c3c460fffa113314ab8d9b1fe8ca2d452cb` |
| terminal m8 | `8729b5082acd27284bf3c05de69fa079a0613f7fece2ef5d9451d699d3d4b881` |
| base m9 | `0a2b952daba8431cf17d331f63d1f1f634896ab6c65eea5700fcc83dcb614844` |

| Input | Binary LRAT SHA-256 |
|---|---|
| terminal m7 | `8b62ea27834e245a608ea399c6fd235eb8367f619ecd74dbaae8ede4bdee3ec1` |
| terminal m8 | `729b5d56915763d66a34cba39a92cc5cfb71988c6de6168a9ea7a7320ca4a297` |
| base m9 | `c3a92b0d16e5cfbb2c6e90180941f27c1ed7d686326cf3b2dd4e0faf7dda5ff8` |

Checker SHA-256:
`c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54`.
Fresh stdout/stderr, command, timing and hash receipts are in
`data/replay-m{7,8,9}.*`. Raw and compressed parent proofs remain intact;
small compressed copies are retained in this packet as well.

## All-size deduction

Let m=|U|. For m<=3 take A empty. For m=4,5 choose respectively one or two
points, so A has no triple and the blue complement has three points. At
m=6, choose any five points. They cannot have every triple a cap, since
that would be a five-cap. A cup triple therefore exists; take it as A.
It has no cap triple, and again the blue complement has three points.
These choices satisfy all terminal conditions and hit every convex four-set.

At m=7 and m=8 the separately audited and independently replayed terminal
certificates exclude real counterexamples. At m=9 the pure-base certificate
excludes any real set satisfying the geometric premises. Any larger set
would contain an admissible nine-subset because general position, no-five-cap
and no-pentagon are hereditary. Hence no admissible set has m>=9. This uses
heredity of the geometric premises, not of the selection predicate.

Together these cases prove terminal-safe existence at every cardinality.
The result concerns n=5 only; it asserts no new bound or minimality result
for n=7, and no literature novelty claim.

## Positive controls and withdrawn shortcut

The seven- and eight-point controls are prefixes of

    (0,0),(1,-1),(2,-3),(3,-6),(10,500),(11,600),(12,699),(13,797).

Both are integer GP, no-five-cap and no-pentagon. Every selector mask is
evaluated directly (128 and256 masks). Each has44 terminal-safe selections;
38 and40 respectively lie in the encoded size interval. Canonical geometry
and containment flags satisfy every non-failure clause, and exactly the
corresponding38/40 failure clauses fail, as a positive control requires.
The prior checker's hull result is independently cross-checked against
strict triangle containment on all105 four-subsets.

The withdrawn m7 shortcut has an explicit countercontrol on the seven-point
prefix: A={0,1,2,4} contains no four-cap and leaves only three blue points,
so it hits all targets. Nevertheless its cap triple{0,1,2} is unprotected:
an ambient four-cap ending at(1,2) would need two earlier vertices, which
do not exist. Thus four-cap avoidance of a four-set is insufficient for
terminal safety. This incorrect shortcut is not part of the all-size proof.

All new checks completed below0.05s each; observed peak RSS was22,284KiB
for formulas and at most17,540KiB for cake (under20MiB per wrapper). No
re-solve, compilation, long unit or additional memory reservation occurred.
No unresolved formula/replay obligation remains for this stated n5 closure.

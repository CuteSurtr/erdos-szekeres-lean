# Independent verification — confirmed for this fixed 23-point set

**COMPUTED.** All 2,797,674 supplied witnesses pass, with exact coverage
of sizes 13..17. The 18-point coordinate inclusion and obstruction are
independently confirmed. The combined minimum of 18 applies only within
`n7-i076`, using the explicitly inherited through-12 result below.

## Independence and arithmetic

Only point files, witness rows and documentary evidence were read from
the parent computation. Neither `terminal_subsets.cpp` nor any previous
geometry/checker implementation was read, imported, compiled or run.
The independent implementation is [tools/audit.cpp](tools/audit.cpp).
The orchestration imports only Python standard-library modules.

The point reader requires a target-7 header, 1..23 points, exactly the
declared integer coordinates and no trailing tokens. It requires strict
x order and coordinate magnitudes <=2^40. Every subtraction is performed
after conversion to signed 128-bit integers. Coordinate differences have
magnitude <=2^41, their products <=2^82, and their difference <=2^83,
so all determinant arithmetic is exact without signed overflow. Every
triple is tested for zero before strict-sided geometric tests are used.

## Geometric reconstruction

For x-ordered a<b<c, a negative determinant means decreasing secant slopes,
hence a cap triple. A set is a cap precisely when all triple determinants
are negative. Necessity follows from decreasing slopes; sufficiency
includes the consecutive triple tests. The checker enumerates every four-
and five-subset and tests all of its triples.

A point q lies strictly inside triangle abc exactly when its three edge
orientations have one common strict sign. General position excludes
boundary ambiguity. A four-set is nonconvex exactly when one vertex lies
inside the triangle of the other three. This yields all 3,632 ambient
nonconvex four-subsets.

For a finite planar set in general position, failure of convex position
means some point lies in the convex hull of the others. Triangulate that
hull: one triangle of other points contains the point, strictly by general
position. Thus a nonconvex set contains a nonconvex four-set; the converse
is immediate. A six- or seven-set is consequently convex exactly when it
contains no nonconvex four-set. No hull algorithm is needed in the checker.

As an independent control, every ambient 8,855 four-subsets, 100,947
six-subsets and 245,157 seven-subsets was also tested using supporting
edges: an edge is supporting if all other points lie strictly on one side.
Convex position is equivalent to every point having supporting-edge
degree two, with exactly k supporting edges. All **354,959** comparisons
agree. The implementation uses no finder ordering or convexity flags.

## Exact containment tables

For each forbidden family, a byte array over 2^23 masks is seeded at
exactly the family members. For each bit b, entries with b set OR in the
entry with b removed. After processing bits J, entry S is the OR of the
original seeds obtained by deleting any subset of J from S. Induction
over all bits proves that the final flag is true exactly when a forbidden
seed is contained in S.

The first transform handles four-caps, five-caps and nonconvex four-sets.
It is used to enumerate the exact convex-six and convex-seven seeds; a
second transform propagates those seeds. Separate flag bits prevent
cross-contamination. Controls compare these tables with literal seed
scans on all subsets of 272 small general-position fixtures, totaling
17,408 subset checks.

The ambient premises follow directly: all 1,771 triples are noncollinear,
the explicit five-cap list is empty, and the explicit seven-gon list is
empty. These properties are inherited by every W without any claim that
terminal support itself is inherited under deletion.

## Every positive witness

Each row must have W inside the 23-bit universe, m=popcount(W) in 13..17,
result=1 and A contained in W. The checker then verifies:

1. The four-cap flag of A is false.
2. The convex-six flag of W minus A is false. An unhit target is precisely
   a convex six-subset entirely in W minus A, so this is equivalent to
   hitting every convex six-subset of W.
3. For every selected terminal pair b<c occurring in some cap triple
   a<b<c of A, an explicitly enumerated four-cap u<v<b<c has u,v in W.
   The last two vertices are in A and thus W, so the whole four-cap lies
   in W. All cap triples ending at that pair share the same existential
   condition; grouping them loses no obligation.

Support lists are built from the independently enumerated four-caps.
Testing them against W is essential: support from the full ambient set
alone would be unsound under deletion. There were 866,581 pair obligations
covering all 1,485,088 selected cap triples. The finder nodes field is
strictly parsed and reported as metadata; it supplies no evidence.

## Streaming and exact coverage

Rows have exactly five unique known keys and unsigned decimal integers.
Missing, duplicate or unknown keys, signs, noninteger values, overflow,
leading zeroes, trailing data and overlong lines are rejected. A fixed
512-byte line buffer prevents unbounded line allocation. Only geometry
tables, the coverage bitmap and counters are retained.

The bitmap detects duplicate W immediately. At EOF every mask from zero
through 2^23-1 is scanned, and bitmap membership must equal the predicate
13<=popcount(W)<=17. Every size count is also checked against its binomial
value. This establishes completeness and absence of extra rows without
trusting the finder's enumeration order or total. Missing rows cannot be
hidden by duplicates or out-of-range rows. Nonpositive/UNKNOWN results fail.

SHA-256 passes use 1 MiB blocks. Size, modification time and inode are
checked during hashing, and before/after receipts agree exactly. The
145,297,300-byte stream hash is
`972e8f1139de7f9067a77bccd8941ea0bf70a8be19d0064e2816845170519969`.

## Mapped obstruction and minimum claim

Python compares the 23-point input with `n7-i076/input.json` and the frozen
`terminal/data/witness.json` source, then checks the 18-point coordinates
and source indices. Separately, C++ maps each of the 18 coordinate pairs
into the ambient set and checks distinctness. Both obtain W=7339980 and
indices `[2,3,6,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22]`.

C++ enumerates all 2^18 selections of this W. Caps and convexity of a fixed
subset depend only on its own coordinates, so those tables restrict
correctly. Terminal support is re-evaluated inside W. The resulting 8,149
ordinary weak Deltas and zero terminal-safe Deltas provide fresh
**COMPUTED** obstruction evidence, agreeing with the prior certificate.

The complete lower bound through 17 additionally uses:

- [Boundary verification](../../boundary/audit/VERIFY_BOUNDARY.md), sections
  Encoders and coverage and Independent certificate replay: the written
  small-size argument and n7/m11 terminal-boundary certificate cover all
  sizes through 11. For sizes below six, A empty also suffices directly.
- [Extension verification](../audit/VERIFY_EXTENSION.md), Independent
  certificate replay: the general n7/m12 certificate covers size 12.
  Its CNF hash is
  `cebe762c17735b3f811355987acc8912b57b880f341f3ff286097dd98e97d850`
  and LRAT hash is
  `4f770646917f895d5a29934c380b191ee1aceb5bddf0d0f56ee67b23571a15b3`.
- The existing [terminal18 certificate](../../terminal/data/certification/result.json)
  independently supplies the upper-bound fixture. Its core CNF hash is
  `5318a34178cd3aa6acb9f83de54f4e9510b0a968a98fc0c8eb40b20ce135d0dd`.

The three acceptance logs were inspected and hashed and each contains the
exact line `s VERIFIED UNSAT`. **No fresh cake_lpr replay was performed
here.** The through-12 claims retain the prior audits' geometric, encoding
and soundness dependencies.

The argument does not infer smaller sizes by deleting from a size-17
witness: deletion can destroy terminal-pair support. Every size 13..17 is
separately covered, and earlier sizes are separately justified by the
cited results. Therefore the minimum obstruction size is 18 among subsets
of this fixed 23-point set. No enumeration over all order types, other
point sets or integer coordinate realizations was performed.

## Controls and operational outcome

Controls include positive/negative parabola fixtures, arithmetic at
coordinate magnitude 2^40, 272 six-point grid permutations, supporting
edges and 65,280 direct consecutive-slope terminal-support checks. An
actual stream row supplies a positive control. Real four-cap, unhit-hexagon
and unsafe-terminal selections are separately rejected. Ten parser and
seven coverage mutations exercise strict input handling.

The external interface rejects seven point-file mutations and eight
witness-stream mutations. Inputs and failure messages remain under
`data/mutations/` and the corresponding `data/*.stderr` paths. They are
deliberate negative controls, not failed research outcomes. No real input
was rejected, and no run was incomplete or UNKNOWN. Initial compile
formatting warnings and the clean final compile are both preserved; their
cleanup did not change semantics.

The single-CPU unit started at 05:19:00 KST and exited successfully at
05:19:02. Actual limits, command outputs and stopped state are retained.
Main audit: 1.24 seconds and 13,128 KiB RSS; cgroup peak: 168,394,752 bytes,
zero swap. The existing shared guard enforced the requested 500 MiB
threshold. No allocation was raised by this track. The unit is inactive
and the assigned bounded work is complete.

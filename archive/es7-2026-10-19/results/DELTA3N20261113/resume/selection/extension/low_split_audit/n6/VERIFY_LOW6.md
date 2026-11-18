# Independent n6 left10/11 audit — PASS

**CERTIFIED:** both new direct formulas have fresh cake_lpr acceptance.
**COMPUTED:** every row and map entry is independently rebuilt, canonical
exact real controls pass, and all replay input hashes are stable.
**PROVED (written, using cited finite dependencies):** T6(L) holds for all
real x-ordered GP L of size at most11 with no four-cap and no convex six-set.
The capacity step needed to remove the size restriction is separate and
is not independently checked in this subpacket.

## Predicate and specialized projection

T6(L) means one of:

1. A cup B meets every convex five-subset of L; each B vertex after its
   first ends an ambient L three-cap.
2. L partitions into cups B,D with |D|<=4.

The frozen [generic low audit](../VERIFY_LOW_SPLIT.md) proves the exact
classification and encoder projection for n6 as well as n7/n8. For a low
join to a right two-cup, the internal targets are the L pentagons and the
mixed targets are precisely an L cap triple plus both right vertices.
The join has no five-cap or six-gon. A selected L cap triple cannot be
protected, since an ambient four-cap ending inside L would lie entirely
in L. Thus selected B must be a cup. A selected cap a<b<r with two L
vertices is protected exactly when b ends an L three-cap. This gives
alternative1 if a right point is selected. If no right point is selected,
the blue L part must be a cup of size at most4, giving alternative2.
The first selected L point is correctly exempt from the endpoint condition.

For these two instances, cup maximum in L is at most5 because there is
no six-gon. A two-cup partition has total size at most5+4=9. Hence at
left10/11 alternative2 is impossible; zero partition clauses is correct.
Alternative1 need only test |B|<=m_L-4: a larger B can be thinned until its
blue complement has four points, while its cup/endpoint conditions persist.
The ambient set is fixed during thinning; no ambient-size monotonicity is
used. End3 is an exact OR including both directions and false empty ORs
at the first two vertices. The canonical real assignment therefore
satisfies all clauses of the encoded failure whenever T6(L) fails.

No new source family is introduced. The direct source SHA-256 remains
`c7793f8d8a92c5230c38091bf23366e49ec037624085f8752405609c88a335c8`;
the inherited compact geometry source remains
`1964e17b777fd7b7a973f12b2911c003a050047f13a621f523a9f98c6e31d553`.
Our earlier independent rows and exact geometry routines are imported
read-only after comparison with their frozen manifest. Only the row
helper's in-memory scratch destination is redirected; original files
and prior output records are unchanged. No parent checker or producer is
imported or executed, and no compilation is needed.

## Complete reconstruction and fresh replays

| Left size | Variables | Clauses | Literals | End3 clauses | Failure rows |
|---|---:|---:|---:|---:|---:|
| 10 | 592 | 6,522 | 35,845 | 130 | 848 |
| 11 | 968 | 11,298 | 92,730 | 176 | 1,816 |

The10-point map has120 orientations,462 convexity flags and10 End3 flags;
the11-point map has165 orientations,792 convexity flags and11 End3 flags.
Every CNF/map byte, including inherited geometry and empty final phases,
matches the independent reconstruction. Both parent solver inputs have
the identical hash to the corresponding reconstructed source CNF.

For left10, CNF SHA-256 is
`2aac28f4cfbe8b9f99e2ee4959d2efe81f6b4f0ad26805b09f395cd17f24f026`;
the498,365-byte binary LRAT SHA-256 is
`f8ac66d7eba2c854d31a3cb8bc8a390b11de28aeb136faf27e341b8c368338bd`.
For left11, CNF SHA-256 is
`1dcd40d44ed07b7f94d99c450636e0e15fa6eea57f5902cad519177c2f251d37`;
the1,477,972-byte binary LRAT SHA-256 is
`a90cd99d30b32066f97b0312b8dcbc28c7ffd3c6bd99d1275e724daba0c682e0`.

Both fresh checker stdout files contain exactly `s VERIFIED UNSAT` and
both processes exit0. Acceptance is not inferred merely from exit status
or parent receipts. The checker binary is pinned at
`c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54`.
Pre/post streamed hashes, sizes, mtimes and inodes match for original CNFs,
maps, solver input CNFs, raw/compressed proofs, receipts, sources, fixtures,
helpers and checker. Proofs remain at their original paths. Hashing drops
cache every64MiB and at completion; the small proofs need only the final
release. Both cake runs finish before the one-second periodic release.

## Exact positive controls

Only coordinates are taken from the earlier n6 eleven-point fixture. The
first10 and all11 points are recomputed independently using unbounded
integer determinants and triangle containment on all four-subsets. Each
is GP, has no four-cap and no six-gon. They have44 and62 pentagons.
An independently constructed sufficiently low two-cup gives valid joins
of sizes12 and13 with96 and125 pentagons, respectively. These are positive
controls; the existence of other failing12-point sets is unaffected.

The exact End4, bad-triple and target families agree with the classification.
All4,096 and8,192 whole-join membership assignments agree with the two-option
predicate, totaling12,288 checks. Each L has20 Option1 cups, all within
the emitted size bound, zero Option2 partitions, and its join has60 terminal
selectors. One Option1 cup in each is {0,2,5,6}. Assigning canonical flags
to the actual supplied CNF makes every non-failure clause true and exactly
20 failure clauses false, as a positive real control should. These controls
are not order-type exhaustion.

## Explicit lower coverage and the capacity boundary

For nonempty |L|<=9, join L to a low two-cup. Internal L six-gons are
absent; a mixed convex set has at most3+2=5 vertices, and a mixed five-cap
would require an L four-cap. Thus the join is admissible and has at most11
points. Terminal n6 existence through11 follows from the separate
[through9 boundary dependency](../../../boundary/audit/VERIFY_BOUNDARY.md)
and individually audited/replayed generic10/11 formulas in
[terminal12_audit](../../terminal12_audit/VERIFY_TERMINAL12.md).
Applying the exact classification to its selector gives T6(L). Empty L
is immediate. The two fresh proofs here then cover left10 and left11
separately. This establishes the bounded claim without deleting ambient
points from an existing selector or inferring smaller sizes from size11.

To conclude T6 for **all** admissible left sets, it remains to invoke a
separately established capacity theorem:

    no four-cap and no six-gon implies |L|<=11.

The parent identifies this as the Baek M(4,6)<=12 capacity bound and is
preparing `extension/low_split/Capacity11.lean`. Its compilation and
axiom/import checks are not assumed successful and are not performed here.
The all-left conclusion is conditional on that separate capacity evidence;
this packet does not label itself an independent Lean replay.

Even with universal T6, an unconditional all-low-join assertion would be
too strong. In an arbitrary admissible low split let d=maxcup(R)<=4.
For d<=2 use T6's transfer to R. For d=3, L is a cup of size at most5;
one L point plus R's top rank-three level is a terminal selector by the
polygon/rank argument. If |L|>=2, d=4 is impossible because two L points
and an R four-cup make a six-gon. The remaining d=4 branch has singleton
L and requires a terminal selector on R; adding L then preserves it.
Universal T6 alone does not supply that right-block premise.

Accordingly, once the capacity dependency is supplied, valid conclusions
are positivity of low joins with |L|>=2, and absence of any low cut in a
cardinality-minimal counterexample (the singleton case uses minimality on
the proper right block). Without that dependency this packet asserts T6
only through left11 and the corresponding bounded-left transfer. It makes
no unrestricted terminal, ordinary weak-Delta or ES claim.

## Limits and retained evidence

CPU preflight showed11 threads free. Both cases ran sequentially on one
CPU, affinity5,nice10, AS300MiB, wall20/CPU19. Each completed its row/geometry
work before launching cake128/stack32, with a17-second child deadline.
Cake times were0.025s and0.050s; peak child RSS58,500 and134,268KiB.
Total case times were0.070s and0.133s; own peak RSS below24MiB.
No check/compile overlapped cake, no additional allocation or long unit
was used, and no running job remains. No solver, deletion, git, installation,
parent realization or external action occurred.

Commands, stdout/stderr, timing, all formulas, canonical controls, hashes
and receipts are under data/. The driver uses exclusive output files;
reproduction requires new output directories and the same resource bounds.

# Independent compact left15 audit and replay — PASS

**CERTIFIED:** fresh cake_lpr prints exactly `s VERIFIED UNSAT` for the
pinned compact n7/left15 formula. **COMPUTED:** all63,368 map entries and
447,615 clauses match independent reconstruction, and the exact positive
canonical control passes. With the explicit previously certified lower
coverage, **T7(L) now holds through left15**. Left16 and an all-left-size
conclusion remain outside this packet.

## Formula and projection

T7(L), for real x-ordered GP L with no four-cap and no seven-gon, is the
disjunction of a cup transversal of every convex six-subset whose selected
vertices after the first end ambient L three-caps, and a partition into
cups B,D with |D|<=5. At left15 the latter is impossible since a cup has
at most6 points, so the partition would have at most11 points.

The unchanged compact source is SHA-256
`1fb043a5d29fa86047ba05cae86fdfb248e6069bc6731c4ee39c181737319303`.
Its full semantic proof and direct/compact equivalence are inherited from
the frozen [independent low audit](../VERIFY_LOW_SPLIT.md). End3 is an exact
OR of ambient cap triples ending at its vertex. A pair's D value aliases
negative End3 at its later vertex; a triple's exact D is cap3 OR negative
End3 at its second/third vertices. Four deletion children find every bad
witness of size at most3. Target T uses seven exact deletion children to
find each six-point target. All reverse implications are present. The
bounded-selection clauses range over |B|<=15-7+2=10. These definitions
add no geometric premise beyond the audited no4cap/no7gon domain.

The frozen own row checker is reused read-only with only its in-memory
scratch destination redirected. It reconstructs the entire CNF/map,
including inherited geometry, all exact gates, aliases, final failure
clauses, comments and empty partition phase. No producer or parent checker
is imported. No fixed signs or additional assumptions occur.

The map has455 orientations,9,373 convexity flags,15 End3 flags,
30,706 D flags and22,819 T flags. The formula has1,200,138 literals.
Its principal new phase counts are470 End3 clauses,153,075 D clauses,
182,552 T clauses and30,827 selection-failure rows. The complete geometry
and no-four-cap rows are also rebuilt. Source and solver input CNFs have
the same hash as the reconstruction:

`793063f5c7c5208c16ce038c63659878adee4eb049546d775d65c5a18ed60418`.

Map SHA-256:
`851185520efcf6dd6b76c988c645b38272901527559eb8891bed614cf74755a6`.

## Exact positive control

Only15 coordinates are taken from the earlier left16 fixture. Independent
unbounded-integer determinants and triangle containment establish GP,
no-four-cap and no-seven-gon; there are226 convex six-subsets. Enumerating
all32,768 L subsets finds100 Option1 cups. Canonical flags satisfy every
non-failure row of the byte-identical reconstruction, and precisely100
selection-failure rows are false, matching those positive selectors.

An independently constructed low three-cup yields an18-point admissible
join with489 four-caps and389 convex six-subsets. The explicitly checked
terminal-safe selector is {0,3,4,9,11,15}. No parent expected rank or
selector is trusted. This is a positive control, not order-type exhaustion;
it does not modify the earlier fixed23-set minimum18 result or any
unrelated obstruction claim. Full coordinates and counts are in control.json.

## Fresh independent proof replay

The2,526,967,446-byte binary LRAT proof has SHA-256
`f86789033376814b7a36ea4bbc26e5a6007e66168a1fef4e38d09a5f6cca2f7c`.
The retained1,360,518,057-byte compressed proof has SHA-256
`86a3a187245ba67f0f44f00e6f24901008adddcd7edc67cab348d02e26c8366c`.
The pinned checker is
`c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54`.

Our fresh run accepts in73.805 seconds; all pre/post streamed hashes,
sizes, mtimes, inodes and devices match for CNF, raw proof, compressed
proof and checker. Its stdout is exactly `s VERIFIED UNSAT`, independently
of the parent's accepted result. The original heap550 and later heap900
exhaustions remain preserved as rejected runs; neither is relabeled.
Both failure logs and the parent's later accepted receipt/log are retained
as small provenance files here. The original proofs are unchanged.

The unit `nov13c-vfy-delta6-low15-independent` used one CPU, affinity5,
nice10, AS1650MiB, heap1400/stack32, CPUQuota100%, nominal MemoryMax2200M,
MemorySwapMax0 and RuntimeMaxSec780. It also had a clean absolute deadline
07:43:40KST and its own1650MiB cgroup/no-swap guard checked every0.1s.
The shared memory guard was active. Hashing released cache every64MiB
and at completion (122 calls); cake inputs were released73 times at1s
or64MiB read progress. The recorded cgroup peak was1,531,453,440 bytes
(1460.51MiB), with no swap; cake peak RSS was1,436,788KiB. Unit counters
were saved internally before systemd garbage collection omitted them.

Total unit work including all hashes was79.891 seconds, finishing at
07:40:18.796KST, before the requested capacity reservation window. The
unit is inactive, Result=success, ExecMainStatus=0. Its temporary1650MiB
reservation was released immediately upon observing completion. No own
audit check, compilation or capacity work overlapped cake.

## Lower coverage and remaining obligations

The separate [fresh low11–14 packet](../replay/README.md) proves T7 through
left14 with explicit through-left10 coverage via standard low three-cup
joins and the separate full-terminal through11, size12 and exact13
dependencies. The present independent size15 certificate extends that
chain through15. No inference relies on ambient-size monotonicity.

This does not close left16, a universal left-capacity theorem, or every
low join without further hypotheses. The generic low classification and
its transfer apply at the stated left sizes; the larger-right singleton
critical case still requires its own right-block terminal result. No
unrestricted full14, ordinary weak-Delta or ES conclusion follows here.

The instance/control check used AS300, one CPU, wall20/CPU19 and took
1.387s/42,184KiB. The replay's temporary allocation is separately recorded
above. Commands, stdout/stderr, monitor trace, hashes and receipts are in
data/. No solver, compiler, git, deletion, installation or outward action
was used. Earlier frozen packets are rechecked unchanged. A later replay
requires a new exclusive output directory and coordinated allocation.

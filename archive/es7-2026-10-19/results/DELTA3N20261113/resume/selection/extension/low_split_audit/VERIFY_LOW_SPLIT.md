# Independent low-split encoder audit — PASS

**PROVED:** direct/compact projection and the critical low-split two-option
classification are sound. **COMPUTED:** complete streamed map/row rebuilds
and independent Boolean/real controls pass. Parent CERTIFIED artifacts are
pinned separately; no fresh LRAT replay is claimed in this packet. No
unrestricted all-size low-cut theorem follows from these bounded checks.

## Sources and scope

Reviewed direct source SHA-256:
`c7793f8d8a92c5230c38091bf23366e49ec037624085f8752405609c88a335c8`.
Compact source SHA-256:
`1fb043a5d29fa86047ba05cae86fdfb248e6069bc6731c4ee39c181737319303`.
Inherited compact geometry source:
`1964e17b777fd7b7a973f12b2911c003a050047f13a621f523a9f98c6e31d553`.
The common geometric interpretation is inherited from the accepted generic
audit. Both programs accept6<=n<=8, n-1<=m_L<=16, and encode L with no
four-cap and no n-gon. No fixed signs, symmetry or additional cup bound is
inserted. The right(n-4)-cup is eliminated by the proof below.

The new `tools/rows.py` imports no producer or prior checker. It rebuilds
even the inherited geometry, then every new row/map byte. Own compilation
of both native sources supplies ten comparison/small formulas in scratch;
fourteen distinct native instances are checked including the supplied four.

## Independent right-block elimination

Let U=L union R be x-separated with all LLR triples caps and all LRR triples
cups, where R is a cup of size n-4. If L has no four-cap and no n-gon,
U is admissible: a mixed five-cap would require four L cap vertices, and
mixed convex sets are exactly an L cap plus an R cup, of size at most
3+(n-4)=n-1. The mixed-convex criterion follows directly from four-subset
triangle containment. Conversely any nonempty low split in a five-cap-free
U has no four-cap in L, since appending an R point would make a five-cap.

Write End3(b) for existence of an L cap u<v<b. An ambient four-cap ending
in a pair wholly in L would itself lie in L and is impossible. Therefore
the selected L part B must be a cup. An LLR cap a<b<r is protected iff
End3(b): its preceding support vertices must lie in L and form a three-cap
ending at b. No LRR or R-only cap triple exists. Thus, when any R point
is selected, every B vertex after the first must satisfy End3. The first
vertex is exempt; empty/singleton B are permitted.

Targets are exactly internal L(n-1)-gons and L three-caps joined to all R.
Consequently terminal-safe selection is equivalent to either:

1. B is a cup transversal of all internal targets, with End3 at every
   selected vertex after its first. Such B plus any one R point works.
2. L partitions into cups B,D with |D|<=n-2, selecting B and no R point.

For necessity in case2, avoiding mixed targets requires D contain no cap
triple, hence be a cup. A cup avoids internal(n-1)-gons iff its size is at
most n-2. In either construction no selected four-cap occurs: a mixed one
would require a three-cap within the selected cup B; the other cases are
already cups. These observations prove both directions of the classification.

Option1 only needs |B|<=m_L-n+2: thin a larger successful B until its blue
complement has n-2 points. Coverage is then automatic, and cup/End3-after-first
conditions persist under subsets of B. No ambient set is changed. Option2
also has |B|<=n-1, since an n-cup would be an n-gon in L. Thus for n7 its
sizes are bounded by6+5; it is impossible at left size>=12 and at11 only
the6+5 partitions remain. No ambient-selection monotonicity is used.

## Clause families and projection

The no-four-cap row is the OR of all four triple orientations. End3(b)
is exactly the OR of negative triple signs ending at b. Direct emits the
child implications before the parent implication; compact reverses that
order. Both directions are present. At b=0,1 the empty OR forces false.

For every eligible B the direct failure row is the OR of negative triple
signs in B, negative End3 flags after its first point, and positive target
flags in L\B. It is false exactly for an Option1 witness. For each bounded
two-cup partition, the final row contains all negative triple signs from
both parts and is false exactly when both parts are cups. Boundary empty
clauses are retained correctly.

Compact D(S) means that S contains a cap triple or a pair whose later
vertex has false End3. For pairs it aliases the **negative literal**
`-End3(later)`, without a new variable. A triple is exact OR of its negative
orientation and the negative End3 flags at the second/third vertices.
Empty/singleton values are false. Larger sets use four one-vertex-deletion
children, with both implications. Any witness of size at most3 misses at
least one of four deleted vertices, proving the OR equivalence.

Compact T(S) is exact target containment. Size n-1 aliases its convexity
flag; larger sets use n exact children, seven at n7. A six-point witness
misses one of seven deleted vertices. Cardinalities strictly decrease, so
the flags have unique canonical values. Negative pair aliases are negated
correctly in reverse clauses. Thus D(B) OR T(L\B) is exactly the direct
row. The common-geometry projections agree even for abstract assignments
to shared leaves; this Boolean equivalence does not need realizability.
Every real obstruction consequently has canonical flags satisfying the
formula. Extra exact flags impose no new geometric premise.

## Instance reconstruction and controls

| n7 case | Variables | Clauses | Literals |
|---|---:|---:|---:|
| direct left11 | 1,430 | 14,070 | 85,008 |
| direct left12 | 2,443 | 23,829 | 190,191 |
| direct left13 | 4,017 | 40,574 | 536,484 |
| compact left14 | 31,099 | 220,707 | 593,588 |

Full independently rebuilt CNF/map bytes agree, including comments and
empty phases. Direct11 has462 partition rows; the other three have none.
CNF SHA-256 values are:

* left11: `ed5fcfc45282362e443605233aec6caf6521e463e31358fdbfbfe3b7b1c11a1a`;
* left12: `2277a75b6f24d74d7b46876223cc2ad51c0c6270e1777e76198f0359bdebd567`;
* left13: `dde85ef3db6b5aa6cae087b70f45f3a0955ee58512e453fc9753ea254126877f`;
* compact14: `0d8a698c0253d249a6ebbb4d021295ffc06569a34b274ee885cd12fff2931183`.

Boolean controls compare all cap-triple/End3 assignments on five labels
against every subset:1,048,576 D checks. All target families on seven labels
give16,384 T checks. There are2,200 End3 gate cases and22,502 relative
witness-cover checks through size16. Countercontrols expose too-few
children, positive pair aliases, requiring End3 at the first point, and
one-way End3 flags hiding a true cap child.

Exact real controls use unbounded integers and triangle containment, not
a hull algorithm. Seven left coordinate fixtures (n6/7/8 boundaries and n7
left11–14) are independently joined to new low cups using strict rational
secant thresholds. Parent expected ranks/selectors are ignored. Whole
joins are independently GP/no-five-cap/no-n-gon; End4=End3(L) times R,
target families and bad-triple families match exactly. All248,448 full
selector assignments agree with the classification. Small cases exercise
Option2 and67 thinnings. Larger cases have36,58,69,75 Option1 cups and
zero Option2 cups. All fourteen canonical native formulas satisfy every
non-failure clause; direct/compact false-failure counts agree with the
independent predicates. These controls are not exhaustion of order types.

## Certificate provenance and bounded left coverage

Parent direct11–13 and the later compact14 replay have exact
`s VERIFIED UNSAT` logs. `data/parent-certificate-provenance.json` records
fresh streamed hashes of CNF/raw proof/compressed proof, source-to-solver
input identity, receipt hashes and exact logs. Original proofs remain.
This is parent CERTIFIED evidence with an independent formula audit,
**not a fresh LRAT replay by this worker**.

The original compact14 heap128 failure remains UNSAT_UNCERTIFIED with
`CakeML heap space exhausted.` The separate parent low14-replay-a result
is CERTIFIED at heap450/AS700,27.155s, proof hash
`7d67e3161247eb508fc0378a888a3508fb9c36d2b60200d7cd2ece8da916b494`.
No allocation for repeating that replay is used here.

For an n7 size14 reduction, the left predicate is supported through13.
For left<=10, realize a low join to a three-cup (moving that finite cup
sufficiently far down makes all required strict signs hold). The join is
admissible and has at most13 total points. Use separately the
[through11 boundary theorem](../../boundary/audit/VERIFY_BOUNDARY.md),
[exact size12 result](../audit/VERIFY_EXTENSION.md), and independently
[replayed exact size13 result](../exact_audit/replay13/README.md). Its selector
gives one of the two options by the classification. For left11–13 use
their respective parent accepted proofs and this formula/projection audit.
No smaller-size conclusion is inferred from size13 alone.

The predicate transfers to any low right block with maxcup(R)<=3: combine
Option1's B with the top cup-ending-rank level in R. That level is
terminal-safe; mixed protection comes from End3(B); mixed hexagons use a
maximum three-cup in R whose endpoint lies in the level. R has no internal
hexagon because its polygon bound is at most5. Option2 uses B alone, whose
cup complement leaves no mixed target. This is a conditional transfer from
the left predicate, not unrestricted positivity for every L. Larger left
sizes and critical singleton reductions retain their own obligations.

## Limits and retained scope

All checks/provenance use one CPU, AS300 MiB, wall20/CPU19. The slowest
real control was1.62s/33,840KiB; row rebuilds at most0.31s/33,908KiB.
Native compiles used authorized AS500/20s,1.03s each and below150MiB RSS.
The inherited unused renamed-main return warning is retained unchanged.
Large hashes release cache every64MiB and at the remainder. No long job,
new solver, extra cake heap, deletion, git or external action occurred.
No all-size low-cut theorem or unrelated SAT-model realization is claimed.

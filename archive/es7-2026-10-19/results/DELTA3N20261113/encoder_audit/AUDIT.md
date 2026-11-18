# Independent adversarial audit of the Delta C++ encoder

13 November 2026. Scope: `delta_cnf.cpp`, `DESIGN.md`, and `check_model.py`,
against DELTA2N20261113's definitions, especially its §4.2b. No encoder or
old record was modified. No solver, proof checker, optimizer, or long job
was launched. All writes are in the assigned `encoder_audit/` directories.

**Outcome:** no soundness gap was found in the unconditioned encoder. The
all-size weak-gon/4-subset-convexity proof in DESIGN is valid, including
the boundary cases expanded below. The reduced lattices and endpoint
sharing have explicit canonical-assignment proofs, not just finite controls.

**New outcome during this audit:** the n6/m15 SAT candidate is an exact
**real cup-side counterexample**, independently checked from integer
coordinates by direct convex hulls and all 32,768 choices of Delta.
This audit's computational evidence is **COMPUTED**, not an LRAT
certificate. The parent owns the separate small-CNF certification.
There are 353 weak Delta choices on this configuration; weak D(5,6) is
not refuted by it. No Lean or refereed result is claimed here.

**Final parent handoff:** the parent obtained the exact `s VERIFIED UNSAT`
line for its standalone 183-clause hitting-set CNF, with the coordinate
fixture, proof, and hashes retained in `../coordinator/data/cup15/`.
This audit read that success line but did not rerun the checker. That
geometric certificate is independent of the large encoder. The parent
also reports working Delta on all 15 single-point deletions: this
establishes deletion-minimality, **not global minimum size**. Those
deletion runs were the parent's work and were not rerun here.

## 1. The concrete candidate, independently audited

Input coordinates:
`/home/jay/research/data/delta3-codex-20261113/coordinator/cup15/realized.json`.
Original SAT model:
`/home/jay/research/data/delta3-codex-20261113/encoder/scheduled-cup-n6-m15/cadical.log`.
The optimizer's reported status, all reported counts, and the encoder's
auxiliary assignment were unnecessary for the geometric check.

[`coordinate_audit.py`](coordinate_audit.py) imports neither encoder,
`check_model.py`, nor this audit's canonical evaluator. It performs exact
integer determinant calculations; constructs lower and upper convex hulls
on every 5- and 6-subset; independently enumerates homogeneous all-triple
cap/cup chains and disjoint endpoint-matched pairs; then directly scans
every Delta against the resulting families. No subset transform, SAT
solver, or deletion lattice is used in that final scan.

Results, retained with coordinates, signs, full mask families, and input
hashes in [`candidate_geometry.json`](candidate_geometry.json):

| Exact check | Result |
|---|---:|
| Integer points, strictly increasing x | 15 |
| Minimum adjacent x difference | 71 |
| Nonzero orientation determinants, all matching the original SAT signs | 455 |
| Minimum absolute determinant | 70,172,849,827,134 |
| Four-caps, all triples negative | 80 |
| Five-caps | 0 |
| Convex pentagons, by integer hull | 216 |
| Convex hexagons, by integer hull | 0 |
| Distinct lower/cup targets, with both endpoints | 103 |
| Distinct upper/cap targets, with both endpoints | 77 |
| Delta containing a four-cap | 23,586 |
| Four-cap-free Delta, all missing some cup target | 9,182 |
| Working cup-side Delta | **0** |
| Working weak Delta | **353** |
| Working cap-side Delta | **87** |

The independent chain-pair families equal the hull-derived families,
including every target mask, not merely their counts. The direct failure
cover accounts for 23,586 + 9,182 = 32,768 masks. Its ordered witness-stream
hash is recorded in the JSON; that hash is a reproducibility aid, not a
certificate. The run took approximately 0.06 seconds under a 12-second
CPU/18-second external limit and 256 MiB address-space limit.

Independently, [`canonical_eval.py`](canonical_eval.py) assigns all
auxiliary variables their exact semantic values, rather than using the
solver's values. For this candidate it read and satisfied **all 181,556
clauses and 781,297 literals** of the actual unconditioned n6/m15 CNF.
This includes all 32,768 pool clauses, 30,827 cap-lattice clauses, and
32,180 target-lattice clauses. It checked 418 single-source aliases,
49 zero target nodes, and 49 pruned seed candidates against exact subset
containment. There were no canonical-assignment conflicts or false
clauses. See [`candidate_canonical.json`](candidate_canonical.json).

That earlier run reconstructed targets from the candidate signs using
the 4-subset definition, independently of the encoder. The subsequent
coordinate/hull check verifies the same 455 signs and the same target
families geometrically. Thus the realization evidence consists of exact
determinants and hull enumeration, not SLSQP success.

## 2. Precise statement and proof direction

Fix an ordered ground set V=[m], with 5<=n<=8. A signotope assigns + or -
to every increasing triple, with at most one sign change in

    (t(ijk), t(ijl), t(ikl), t(jkl)), i<j<k<l.

Valid means no 5-cap and no convex n-set. Delta works when it contains
no 4-cap and hits all target sets. The targets are whole convex (n-1)-sets
in weak mode, their lower chains in cup mode, or their upper chains in
cap mode. Both endpoints belong to either chain. The cap paired with a
missed cup is a chain of V, not necessarily of V\Delta.

For an UNSAT result to imply the universal m-point assertion, the essential
direction is:

    valid configuration with no working Delta => satisfying CNF assignment.

The reverse implication is also valid here and explains the SAT candidate.
One-way witness definitions do not mean that arbitrary satisfying
assignments have exact auxiliary truth values. They mean a true witness
is genuine, and exact truth values provide a simultaneous satisfying
extension when a counterexample exists.

The source audited is SHA-256
`b953e14fc7d0840712bbf63f502e00c7342cbd1cdb9ef3ed548759e8ae8aa12c`.
Line references below refer to that 321-line `delta_cnf.cpp`.

## 3. Independent all-size chain and convexity proof

### 3.1 Consecutive signs imply all-triple homogeneity; boundary cases

For a packet of four signs with at most one change, agreement of the
first and last forces all four equal. Let p0<...<p(r-1) have every
consecutive triple of sign e. After deleting an internal point pi, the
only possible new consecutive triples are

    (p(i-2), p(i-1), p(i+1)), when i>=2;
    (p(i-1), p(i+1), p(i+2)), when i+2<r.

Each lies in the corresponding four-vertex window of the old chain.
The first and last packet entries on that window are old consecutive
triples and both equal e. The new triple therefore has sign e. Deleting
an endpoint introduces no new triple. Deleting the second or penultimate
vertex requires only the window that actually exists; deleting from a
3-chain leaves a pair with no triple condition. Thus deletion preserves
homogeneity at every boundary. Repeatedly deleting unwanted points proves
that every triple, and every subchain, has sign e.

This argument is on arbitrary selected vertices, not just adjacent
ground-set indices. It uses the signotope axiom, not an unproved geometric
slope or boundary-telescoping rule. DESIGN's current all-size proof uses
this deletion argument and the following chord-sign argument; no
telescoping assumption is needed.

### 3.2 Disjointness and weak gon => every four-subset convex

Let U be a homogeneous cap and L a homogeneous cup with common endpoints
u<v. An interior point x of U has t(u,x,v)=-; an interior point of L has
t(u,x,v)=+. Consequently U and L cannot share an interior point. This
does not require no 5-cap or any assumption about Delta.

For every interior x of G=U union L define c(x)=t(u,x,v). If u<x<y<v:

* When c(x)=c(y), both points belong to the same homogeneous chain, so
  t(u,x,y)=c(x) and t(x,y,v)=c(y).
* When c(x)!=c(y), the packet on u,x,y,v is
  `(?,c(x),c(y),?)`. A change already occurs in the middle, so the
  one-change axiom forces it to be `(c(x),c(x),c(y),c(y))`.

Now let u<x<y<z<v and write T=t(x,y,z). If c(x)!=c(y), the packet on
u,x,y,z is

    (c(x), c(x), c(y), T),

which forces T=c(y). If c(y)!=c(z), the packet on x,y,z,v is

    (T, c(y), c(z), c(z)),

which likewise forces T=c(y). If neither adjacent pair differs, all
three vertices lie on one homogeneous chain, with the same conclusion.
These cases exhaust every triple of chord signs, including +,-,+ and
-,+,-; such alternating chord signs are not themselves forbidden.

Triples (u,x,v) are covered by the definition of c. Triples (u,x,y) and
(x,y,v) were covered in the first step. Thus **every triple of G has
the chord sign of its middle vertex**. The middle vertex is always
strictly between u and v, so c(u) and c(v) are never needed. Hence for
every a<b<c<d in G,

    t(abc)=c(b)=t(abd),   t(acd)=c(c)=t(bcd).

This proves the recorded convexity criterion for all four-subsets, for
every chain length. A 2-chain on either side causes no exception; the
single remaining chain is already homogeneous. The 3-vertex union is
immediate and the 2-vertex case is vacuous if that convention is needed.
All encoder targets have at least four total vertices.

### 3.3 Every four-subset convex => weak gon

For a set G of size at least four, put u=min G and v=max G. Define
c(x)=t(u,x,v) on its interior. The two equalities of the convexity test
on u,x,y,v imply t(u,x,y)=c(x) and t(x,y,v)=c(y).
On u,x,y,z its second equality gives

    t(x,y,z)=t(u,y,z)=c(y).

Endpoint-containing triples are handled as in §3.2. Therefore the
negative interior vertices together with u,v form a homogeneous cap;
the positive vertices together with u,v form a homogeneous cup. They
partition G except for the two common endpoints. This direction does
not even need the signotope axiom once all four-subset equalities hold.

There is no circular use of the desired equivalence in §3.2: same-chain
homogeneity comes from §3.1, and mixed-chain comparisons come directly
from explicit packets. The new DESIGN argument supplies the missing
all-size direction identified in DELTA2N20261113/VERIFY_D1.md §5(2).

### 3.4 Connection to exact real geometry

For x-ordered real points, let a=xj-xi, b=xk-xj, c=xl-xk, all positive,
and let A=Dijk, B=Dijl, C=Dikl, D=Djkl be orientation determinants. Direct
expansion gives

    b B=(b+c) A+a D,       b C=c A+(a+b) D.

The coefficients of D relative to A in B and C are a/(b+c) and
(a+b)/c, in that strict order. If A,D have the same sign, both middle
terms have that sign. If they differ, A+sD crosses zero at most once as
s increases from 0 through those two ratios to infinity. With no
collinearity, the sign sequence A,B,C,D therefore has at most one change.
This explicitly justifies the real-point-to-signotope step with no
floating-point assumption.

For four real points in x order the convexity equalities exclude exactly
the cases in which one of the two middle points lies inside the triangle
of the other three. The x-extreme points cannot be interior. If a larger
set is not in convex position, an interior point is in a triangle of
three other points, so some four-subset fails. Thus the four-subset test
agrees with ordinary convex position. The candidate audit independently
uses integer hulls rather than relying on this conversion.

## 4. Clause-family audit

### 4.1 Base: lines 112–137

**Signotope.** The four variables are ordered as t(ijk),t(ijl),t(ikl),t(jkl).
The `changes` loop counts the three adjacent sign changes. For each bad
4-bit vector b, its clause has literal -q[i] exactly when bit i is true;
it is false exactly on b. Exactly eight of the sixteen vectors are bad.
This is equivalent to the old eight ternary subsequence clauses, not a
requirement that the emitted clauses themselves be identical.

**No five-cap.** For every increasing 5-set the clause is the disjunction
of its three positive consecutive orientation variables. It forbids
precisely an all-negative consecutive chain. By §3.1 this is equivalent
to a homogeneous 5-cap. No cap of length five is inadvertently omitted
because its indices are nonconsecutive in V.

**No n-gon.** For every n-set G, `ends` is its pair of extreme vertices,
and the loop chooses 0,1,2 inner upper vertices. If U is that choice plus
the endpoints and L is its complementary inner choice plus the endpoints,
the emitted clause is

    OR positive consecutive triples of U
      OR negative consecutive triples of L.

It is exactly the negation of “U is a cap AND L is a cup.” The chains
have disjoint interiors by construction and union G. Empty conjunctions
for a 2-chain are correctly represented by no literals from that chain.
By §3, a falsified clause implies a convex n-set. Conversely, a convex
n-set decomposes into U,L; no 5-cap forces |U|<=4, so its split occurs
in precisely this loop. This restriction would be unjustified without
the no5cap base family; the implementation includes that family.

### 4.2 Four-cap leaves and endpoint support: lines 139–177

For |K|=4, A[K] implies the two negative consecutive triples. Thus a true
leaf entails an actual 4-cap; assigning its exact all-triple truth value
satisfies both clauses.

Cup-mode H(u,v,3) implies some negative t(u,x,v). H(u,v,4) implies some
four-cap leaf with endpoints u,v. These support lists include all possible
interior choices. H3 is allocated for intervals with at least three
vertices and H4 for intervals with at least four. There is no fabricated
variable for an impossible endpoint/length combination.

Cap mode first creates positive all-consecutive cup witnesses of lengths
n-3 through n-1 and groups them by endpoints and length. Its endpoint
OR clauses are sound in the same way. At n=5 the enumerated 2-cup has no
triple conditions, correctly; the extra unused endpoint support for
length two is harmless.

### 4.3 Target seeds: lines 178–203

Cup seed size k is in [n-3,n-1]; complementary cap size is r=n+1-k in
{4,3,2}. Its implications require a homogeneous cup and an r-cap with
the same endpoints (or the vacuous endpoint pair for r=2). By §3.2 the
chains are disjoint internally and form a convex (n-1)-set. In particular,
sharing H4 does **not** need a per-seed disjointness filter.

Conversely, every actual lower chain of a convex (n-1)-set has one of
these sizes, because its upper chain has at most four vertices. Its
support exists, and the interval has at least n-1 distinct vertices.
The `v-u+1<n-1` pruning and absent-endpoint pruning therefore cannot
remove a genuine target. They are necessary room checks, not claims that
every retained candidate is geometrically realizable.

For cap seeds, k=2..4 and complementary cup length n+1-k give the same
argument with the chain roles exchanged. For weak mode, each q4 implies
the two equalities via the four clauses `-q4 OR (-a OR b)`,
`-q4 OR (a OR -b)`, and the analogous c,d pair. A whole-set seed implies
every required q4, exactly the convexity definition.

**Delta scope:** endpoint witnesses are in all of V. Requiring the
partner cap to avoid Delta would discard actual missed cup targets.
The source correctly applies complement containment only to the cup seed.

### 4.4 Cap lattice: lines 95–100, 142–148

Let A*(S) mean “some 4-cap K is contained in S.” For |S|>4 the five
selected vertices are distinct. Since |K|=4, some selected vertex is
outside K. Thus a true A*(S) has a true selected-deletion child. Every
child witness is contained in S, so the converse also holds. The
canonical exact assignment satisfies the one-way OR clause.

For an arbitrary CNF assignment, a true internal A forces a true child;
each step decreases cardinality until a true 4-cap leaf is reached.
There is no infinite path and no leaf of size below four. Absent A at
smaller sets is the zero sentinel, not a free variable.

### 4.5 Target lattice, aliases and zero: lines 204–221

Put U=n-1 in weak/cup mode and U=4 in cap mode. Every possible seed has
size at most U and at least `lower`. If a target T is properly contained
in S, then:

* for |S|<=U all vertices are eligible deletions, including some S\T;
* for |S|>U the selected U+1 vertices cannot all belong to T.

Hence at least one selected child contains T. If T=S, its seed is in the
node's right-hand side. This proves the containment recurrence, including
sizes below `upper`; applying just the >U lemma there would be incomplete.

More explicitly, let F(S) be the family of **allocated seed masks**
contained in S, irrespective of which seeds are true. The direct seed
and selected children cover exactly F(S), by the same cardinality
argument. If the constructed right-hand side is empty, F(S) is empty.
If it has one identifier, that identifier has exactly the seed support
F(S). This proves that a canonical truth value is consistent across all
uses of a reused identifier. It is stronger than merely saying that a
true alias has some witness.

Arrays start at zero; sets below `lower` stay zero. Every deletion clears
a set bit, giving a smaller integer mask, so the ascending-mask loop
has already finalized its child. Zero is never emitted as a literal.
Multiple equal child identifiers may make a redundant OR node but do not
affect either proof direction. There is no forward reference or alias cycle.

### 4.6 Every Delta: lines 223–237

The loop visits all masks 0 through full, once each. Lattice mode emits
A[Delta] OR B[full XOR Delta], omitting false sentinels. XOR is the exact
complement because Delta is a submask of full. In flat mode it enumerates
all 4-cap leaves within Delta and all allocated seeds within the complement.
All witnesses enter positively. An empty failure clause must be emitted,
and is emitted; skipping it would change the quantification.

For a genuine counterexample, set all leaves, endpoint indicators,
convexity indicators, seeds, and containment nodes to exact truth. The
previous arguments satisfy every definition and every base clause, and
each failure clause holds. Conversely, any model's true root witnesses
give a genuine reason that each Delta fails. This proves equisatisfiability
for the source's default unconditioned formula.

### 4.7 Explicit flat-pool proof, including cup n8/m14

This branch does **not** depend on either lattice induction. With
`pool=flat`, lines 99–100 allocate A[K] only at |K|=4; `cap_nodes()`
returns after defining those leaves (line 142), and `target_nodes()`
returns immediately (line 205). Endpoint support and target seeds are
unchanged. In particular H4 still refers only to size-four A leaves,
so skipping the larger cap nodes does not break endpoint support.

For each Delta, lines 231–233 emit precisely

    OR { A[K] : K subset Delta, |K|=4 }
      OR { seed[T] : T subset V\Delta, lower<=|T|<=upper,
                                     seed[T] is allocated }.

Under the exact truth assignment, the first disjunction holds iff Delta
contains a 4-cap. By §4.3, every true seed in the second disjunction is
an actual target, and **every actual target has an allocated seed** of
one of the enumerated sizes. Hence that disjunction holds iff Delta
misses some target. Therefore the emitted clause has exactly the
mathematical truth value “Delta fails.” All 2^m masks occur, including
the empty and full masks and any empty failure clauses. Endpoint
variables are still evaluated in V, not in V\Delta.

For a counterexample, the exact leaf/endpoint/seed assignment satisfies
every definition and every one of these clauses. Conversely, a true
literal in a flat pool clause supplies a genuine cap or missed target.
This proves equisatisfiability for flat weak, cup, and cap modes, without
assuming anything about the lattice variables that this branch omits.

For the parent's **cup n8/m14, flat, unconditioned** instance, the target
sizes are 5,6,7, with complementary cap sizes 4,3,2. Thus an accepted
UNSAT proof gives: every 14-point signotope with no 5-cap and no convex
octagon has a 4-cap-free Delta meeting the cup part of every convex
heptagon, including its endpoints. In particular it holds for real point
sets of that size. It is a size-specific result, consistent with the
real n6/m15 counterexample, and does not prove the unrestricted cup-side
octagon conjecture.

The parent supplied these hashes. This audit read its `encode.log`
(cup, flat, sym none, empty cube, no fixed-sign clauses) and the exact
`s VERIFIED UNSAT` line in `cake.log`; the proof was not rerun here:

* CNF: `a0e37105f825fc655ea76faef691c92b3748d99e654fb86cd101545afc1a1dbc`.
* LRAT: `03e6d69917731b55a4fd2d70255668c4caf8a5c52b9343cf99662ac9c2d8344c`.

The n8/m15 flat search is not an accepted theorem merely because it is
running; this audit makes no outcome claim for it.

## 5. Restrictions, output, and model checker

The three first frontier files use `sym=none`, no cube, no fixed signs.
Be careful: scratch files named simply `cup-n6-m14.cnf` etc. were generated
with mirror symmetry; the actual `scheduled-*` directories contain the
unconditioned files audited here. Their parameters and CNF hashes are
recorded in `source_manifest.json`.

The optional mirror map reverses labels without complementing signs.
It reverses each four-sign packet, preserves cap/cup types, and permutes
Delta. The source compares the smaller index of each two-element reversal
orbit in increasing order. With prefix flag true, its clauses forbid
x=1,y=0 and force the next flag true at equality; after x=0,y=1 remaining
flags may be false. Thus some member of every orbit survives. A cube or
fixed sign string alone, however, proves only a restricted instance;
all prefixes must be covered for an unrestricted cubed theorem.

The bitmask range m<=20 stays inside uint32_t; a deleted bit always
decreases the mask. Triple indexing is allocated in the lexicographic
combination order used by the checker. The DIMACS writer preserves empty
clauses, counts every emitted clause, checks output errors and header
length, and rewrites the reserved header. A partial/failed output must
not be passed off as successful generation. The runner checks generation
success before launching the solver.

`check_model.py` does not trust the encoder's auxiliary variables. It
extracts all orientation literals, checks all packets, all-triple caps,
all four-subset convexity conditions, and the full subset transforms.
Its plus chord sign selects the lower chain: for u<x<v,
D(u,x,v)>0 means x is below the chord uv. The working-Delta test uses
containment of a four-cap in Delta and containment of a target in its
complement, with endpoints included. Its current `P is not None` check
handles abstract fixtures. A successful run with `--mode cup` requires
both validity and zero working cup Delta; omitting `--mode` only analyzes.

For general coordinate inputs the checker does not enforce integer JSON
types, and several validation checks are Python `assert` statements.
Consequently its “exact integer” description requires actual integer
inputs and running without Python optimization. Those conditions hold
for the present invocation and fixture. This audit's coordinate checker
explicitly rejects non-integer coordinates and uses unconditional error
checks. This is an input-contract caveat, not an encoder soundness gap.

A certificate claim requires the **exact line** `s VERIFIED UNSAT` for
the retained matching CNF/proof pair. A solver UNSAT line alone is
COMPUTED. SAT plus the independent exact coordinate/family check above
is evidence of a real counterexample; no certificate or realization
claim follows merely from SAT or an optimizer status.

## 6. Adversarial checks and outstanding obligations

The hand-sized checks are reproducible with
[`bounded_checks.py`](bounded_checks.py); output is
[`bounded_checks.json`](bounded_checks.json). They were subsecond and
used no solver. They include the exact packet implications in §3 and a
smoke evaluation of an existing 4-point CNF, plus two concrete pitfalls:

1. **Four cap deletions would fail.** The five points
   `(0,0),(1,3),(2,4),(3,3),(4,100)` have exactly one 4-cap, indices
   `{0,1,2,3}`, and no 5-cap. For S={0,...,4}, deleting any of its first
   four vertices destroys that sole witness. The fifth deletion retains
   it. This is a genuine geometric counterexample to the stronger,
   incorrect four-deletion recurrence, not to the implemented five-deletion
   recurrence.
2. **The partner cap may meet Delta.** For n=6, the convex five points
   `(0,0),(1,3),(2,-2),(3,3),(4,0)` have upper chain `{0,1,3,4}` and lower
   chain `{0,2,4}`. Delta={1} is cap-free but misses the lower chain.
   The correct H4 witness meets Delta. A restriction of its support to
   V\Delta would lose this genuine obstruction. The source does not make
   that restriction.

A third sharpness check uses a singleton target family T={0,...,U-1}
inside S={0,...,U}. Keeping only the first U deletions loses T; U+1
retains it. This is a set-family argument, not a claim that that entire
singleton family arises from a particular point configuration.

The author's 501,024 zero-mismatch comparisons are useful additional
implementation evidence. They were not rerun or used as the proof of
the all-size lemmas. The present candidate's integer-hull and direct-Delta
checks are independent of those controls.

Remaining operational obligations for any future UNSAT frontier claim
are binding the executed binary to this source revision, retaining the
actual CNF/proof hashes, and obtaining the exact cake success line. No
finite fixture check replaces the written canonical-assignment argument.
Conversely, the realized cup-side counterexample no longer depends on the
large encoder once the coordinate/family enumeration is independently
verified; the parent's 183-clause hitting-set certificate is a separate
way to certify its finite obstruction.

No additional mathematical gap was left open in the clause families
audited here. Optional parent-only commands and bounded resource estimates
are in [`PARENT_RUNS.md`](PARENT_RUNS.md).

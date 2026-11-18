# Exact one-old-blue repair: criterion, positive range and obstructions

**PROVED** means the written implications below. The concrete real-coordinate
predicates are **COMPUTED**, checked with two independently implemented integer
geometry routines. No claim here is Lean-checked, refereed or novel. SAT
certification of the frozen formulas is assigned to the parent.

## 1. Definitions and exact scope

S is a finite real set in general position, with distinct x-coordinates.
A cap has decreasing consecutive slopes in x order. Put k=n-1. A full
weak Delta is a four-cap-free B subset S meeting every convex k-gon in S.
Fix r in S and a weak Delta A of U=S minus {r}. An old-blue point is a point
of V=S minus (A union {r}); its color in A is unselected. Define

    rho(A,r;S) = min { |B intersect V| : B is a full weak Delta in S }.

The minimum is infinity if there is no full Delta. Deletions from A are
unrestricted, and r may have either color. This is exactly the condition
in the request, |B minus (A union {r})|<=1. It is not a cardinality bound
on B, a requirement to retain A, or a requirement to select r.

The two frozen counterexamples satisfy the stronger geometric condition
that r is rightmost. Both ordinary and r-selected full Deltas do exist.
Consequently they refute the universal one-old-blue repair rule even for
rightmost deletion, but do not refute weak D(5,7), weak D(5,8), or the
existence of some more favorably chosen old Delta.

## 2. Exact deletion-and-addition criterion (PROVED)

Choose Q from the sets E, E union {r}, where E is empty or a singleton
contained in V. For R subset A put B=(A minus R) union Q. Then B is a
full weak Delta if and only if both conditions hold:

1. For every four-cap K contained in A union Q, R intersects K intersect A.
2. For every convex k-gon H disjoint from Q, H intersect A is not contained
   in R.

**Proof.** A cap can occur in B precisely when it is contained in A union Q
and none of its A-vertices was deleted. This is the negation of condition 1.
A polygon intersecting Q is automatically hit. For any other polygon, the
surviving hits are precisely (H intersect A) minus R, giving condition 2.
In particular an empty trace H intersect A makes condition 2 impossible.
Conversely these conditions exclude every cap and hit every target. Every
repair of cost at most one has exactly this form by taking Q=B minus A and
R=A minus B. This proves necessity and sufficiency. QED.

The criterion allows blockers involving both r and the new old-blue point;
ignoring such four-caps would make the criterion unsound. A itself is
four-cap-free, so all active caps involve at least one point of Q.

## 3. A universal positive small-size lemma (PROVED)

**Theorem.** Let n>=5. Suppose S has no five-cap, |S|<=n+2, and A is a weak
Delta in S minus {r}. Then rho(A,r;S)<=1. Neither r being extreme nor S
being convex-n-gon-free is needed. If |S|<=n+1, in fact rho=0.

**Proof.** If A already hits every target in S, take B=A. Otherwise choose
a convex k-gon H disjoint from A. It contains r, because all old targets
are hit. Hence |A|<=|S|-k<=3.

If A union {r} has no four-cap, take that set: it retains every old hit and
hits every new target at r. A failure of this step requires |A|=3 and
T=A union {r} to be a four-cap. Combining |A|=3, H disjoint A and |H|=k
forces |S|=k+3=n+2. This already proves the rho=0 assertion for |S|<=n+1.

Choose any p in S minus T; this is possible since |S minus T|=n-2>=3.
Some four-element subset D of T union {p} is not a four-cap. Indeed, if
every four-element subset were a cap, every consecutive triple in the
x-ordered five-element set would be a cap triple (extend it to a
four-subset). Thus its four consecutive slopes would be strictly
decreasing, making a forbidden five-cap. Since D has only four points and
is not a four-cap, it is four-cap-free. Also

    |S minus D| = (n+2)-4 = n-2 < k,

so D hits every k-element subset, in particular every target polygon.
Finally D is contained in A union {r,p}, giving cost at most one. QED.

This theorem does not assert a repair selecting r. The noncap four-subset
D can omit r. The finite obstructions below have n+7 and n+8 points,
respectively, and therefore do not contradict it. No universal assertion
for the intervening sizes is made here.

The old deletion-only fixtures at n7/m9 and n8/m10 give exact controls:
their chosen old Deltas require one old-blue selection, while the singleton
{0} is a full Delta in each. Thus the small-size theorem's allowance of
one old-blue selection cannot be reduced to zero at |S|=n+2.

## 4. Robust private-polygon obstruction (PROVED)

Let T be a four-cap in S. For each t in T suppose there is a nonempty
family of convex k-gons H with H intersect T={t}, and suppose

    intersection { H minus {t} : H in this family } = empty.

Then every full weak Delta B selects at least two points outside T.

**Proof.** B cannot contain T, so choose t in T minus B. Each listed private
polygon for t must be hit outside T. If B selects no point outside T it
misses all of them. If its only outside point is q, that same q must belong
to every H minus {t}, contrary to the empty intersection. QED.

More generally, if every such private-support family has transversal
number at least b+1, every full Delta selects at least b+1 points outside
T. This is a sufficient obstruction, not a necessary characterization.

In the frozen examples A=T minus {r}; exact geometry confirms A is an old
weak Delta. The short lists in PRIVATE_POLYGONS.md establish the empty
intersections using 12 hexagons for n7 and 13 heptagons for n8. Thus the
lower bound two has this direct combinatorial proof in addition to the
full subset enumeration. An ordinary full Delta with cost two supplies the
matching upper bound. r-selected cost-two positives are recorded separately.

## 5. Exact min-plus subset transform (PROVED)

Let F be the family of all full weak Deltas. Initialize f(B)=0 for B in F
and f(B)=infinity otherwise, for all subsets of S. Process each point once.
For paired masks X without this point and Y=X union {point}, update from
the two *old* values simultaneously:

    new_f(X) = min(old_f(X), old_f(Y)+1)
    new_f(Y) = min(old_f(X), old_f(Y)).

After every coordinate is processed,

    f(T) = min_{B in F} |B minus T|.

**Proof.** On one coordinate the input bit represents membership in B and
the output bit membership in T. The only positive cost is input=1,
output=0, and it equals one. The displayed recurrence applies precisely
this two-by-two min-plus matrix. After processing a set of coordinates,
the invariant is the minimum over those input bits of the initialized
cost plus their individual costs, with the unprocessed bits still fixed.
Induct on the processed coordinates. At completion the individual costs
sum to |B minus T|; only B in F has finite initialized cost. QED.

Evaluate f(A union {r}) to obtain the exact repair cost, simultaneously
for every old Delta and every root. The transform uses O(m 2^m) time and
O(2^m) memory, not a pairwise enumeration of A and B. The old-Delta test
is four-cap-freeness of A together with absence of any target wholly in
S minus (A union {r}). The latter set is exactly the old complement.

`repair.cpp` computes cap/gon containment flags by Boolean subset zeta
transforms. `verify.py` instead enumerates every B once for each frozen
chosen A and uses different geometry predicates. The supplemental 0-1 BFS
check starts from all full Deltas, adds a point for cost zero and deletes
a point for cost one; its distance to T is the same minimum and serves
as a distinct transform control. None of these calculations is an LRAT
certificate or an omission-method EXACT TREE.

## 6. Coloring CNF soundness and positive controls (PROVED)

Variable x_i selects point i (DIMACS variable i+1). Include:

- For every four-cap K: the clause OR_{i in K} not x_i.
- For every target k-gon H: the clause OR_{i in H} x_i.
- For every distinct u,v in V=S minus (A union {r}): not x_u OR not x_v.

The first clauses are exactly four-cap-freeness, the second exactly target
coverage, and the third exactly selection of at most one point from V.
There are no unit clauses fixing A or r. Therefore the models are in
bijective correspondence with the allowed full repairs. The complete
formulas have 14/213 and 16/277 variables/clauses for n7 and n8.

For positive controls the `*-two.cnf` variants replace negative pairs by
all negative triples on V, enforcing cost at most two. Explicit full
assignments are supplied. Separate one-blue positive controls use the
small deletion-only fixtures. Core formulas keep only the four-cap T,
the listed private polygons and the negative pairs. Every core clause is
checked to occur verbatim in the full one-blue formula. Their unsatisfiability
also follows directly from Section 4, conditional on the checked geometry.

No finder UNSAT verdict is a certification. The parent independently audited
coordinates and clauses and freshly certified both full frozen CNFs with
cake_lpr. This track checked the literal verification lines and hashes, but
did not replay those proofs itself. See data/PARENT_CERTIFICATES.json.

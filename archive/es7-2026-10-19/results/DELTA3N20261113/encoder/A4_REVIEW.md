# Independent bounded audit of a4/theory.md

**PROVED (written audit):** Section 1's terminal polygon lemma and
extreme-point theorem, and Section 2's shared-endpoint fact and stated
boundary localization, are sound for the stated real-point hypotheses.
I found no missing case or unsupported symmetry step. This is an audit
of those statements, not a theorem extension or a Lean verification.

Audited source: `../a4/theory.md`. The initial read had SHA-256
`5aebbbe99ca0e00856c0d90bd5ed65e44dc2ca23365e2bf533e261cb99365ca1`.
The author subsequently added a conditional Q_S observation and bounded
controls. I reread Sections 1 and 2 at SHA-256
`41a1ef7d192fe0ab0c2521c85f43601f62861e74577e074aebcea5b2be72af68`;
the verdict also covers that version, including the Q_S observation below.
The source was read without modification. No search, enumeration, solver,
or coordinate computation was used for this audit. Section 3's separate
seven-point obstruction is outside this requested review.

## Quantifiers and conventions

The extreme-point theorem fixes any integer k>=3 and any nonempty finite
real point set S in general position, with distinct x coordinates and no
4-cap. The existence of a named rightmost point r implicitly requires
nonemptiness. U=S minus {r} must contain **no k-cup anywhere**, not just
no maximal cup of length exactly k: a longer cup contains a k-cup.
For the empty ground set the desired transversal assertion is vacuous,
but r itself is undefined; this is a harmless convention, not a missing
nonempty case of the proof.

As used in the source, saying a set is a cup includes the vacuous sets
of size 0,1,2. This convention is needed when E is empty or a singleton
and in the explicit one-point extension facts. For larger sets, absence
of a 3-cap means every increasing triple is positive and hence the
x-ordered set is a cup. All edge labels in Section 2 are on **every
ordered pair x<y**; they are not restricted to consecutive points or to
edges of a particular polygon.

No no-(k+1)-gon hypothesis is used in Section 1. Section 2 does require
no convex n-gon with n=k+1, in addition to no 4-cap; it uses that
hypothesis to bound beta by k and to rule out the shared-endpoint
conclusions. The proofs do not interchange these scopes.

## The two extension facts

Suppose (p,q,z) is a cap and a cup C ends at p. If |C|>=2, let a be its
penultimate vertex. All four vertices satisfy a<p<q<z. If (a,p,q) were
a cap, its decreasing slope followed by the decreasing slope of
(p,q,z) would make (a,p,q,z) a 4-cap. Therefore (a,p,q) is a cup, and
appending q to C preserves its last consecutive turn. Earlier turns of
C are unchanged. Also q is new because q>p. If |C|=1, appending q
gives a two-point cup without needing a triple.

The left extension is equally valid but should not be silently confused
with appending: if (a,b,p) is a cap and a cup C starts at p, its next
vertex q satisfies a<b<p<q. A cap (b,p,q) would give the 4-cap
(a,b,p,q). Thus b can be **prepended** to C, and b is outside C. Again
the one-point case simply produces two points. No hidden convex-polygon
assumption is used in either extension.

## Terminal polygon lemma, including k=3

In a no-4-cap set U, a convex k-gon's upper chain has c<=3 vertices.
Because both endpoints belong to each chain, c+d-2=k. If c=2, its lower
chain is a k-cup, excluded by the hypothesis. Thus every target has
exactly a 3-cap upper chain and a (k-1)-cup lower chain. In particular,
**each** e in E is the endpoint of both witnesses inside U; the two
witnesses come from a target ending at that e. No common polygon or
common cup for different elements of E is assumed.

If e1<e2<e3 in E form a cap, append e2 to a (k-1)-cup ending at e1.
This is legal by the first extension fact, and e2 is not already on
the cup because it lies to the right of e1. The new cup has k vertices
all in U, a contradiction. Hence E is a cup.

If E has at least k-1 vertices, take its first k-1 as a cup C with
first vertex e. A 3-cap (a,b,e) exists inside U by the preceding
endpoint observation. The second extension fact prepends b to C.
The new b is strictly before every vertex of C, so bC has exactly k
distinct vertices and lies in U. This contradiction proves |E|<=k-2.
Every target's own right endpoint lies on its lower chain and in E,
which proves the required hitting property.

For k=3 the target is a triangle. In U it cannot be a 3-cup, so it is
a 3-cap; its lower chain has two endpoints. A purported cap among
three E vertices would extend a two-point cup to a three-point cup.
The size argument, if |E|>=2, prepends b to the two-point C, again
producing a three-point cup. Therefore the conclusion |E|<=1 holds
with no invocation of a nonexistent earlier vertex or of k>=4.

## Extreme-point theorem and its reflection

The terminal lemma applies to U by heredity of no 4-cap. To test
Delta=E union {r}, consider any cap x<y<z among its vertices. Since r
is strictly rightmost, x and y are in E even when z=r. A (k-1)-cup in
U ends at x. Appending y uses the cap (x,y,z) in S, where no 4-cap
holds. The resulting k-cup lies wholly in U: it contains the old cup
and y, **not z**. This is the crucial quantifier check; z may be r
without spoiling the contradiction in U.

Consequently Delta is a cup. Since r is not in E,
|Delta|=|E|+1<=k-1. Each target k-gon H either contains r, in which
case r is its right endpoint and belongs to its lower chain, or is
contained in U, in which case its right endpoint lies in E. This
covers all target polygons, not just pure cups. A cup has no 3-cap,
and its cardinality below k excludes a convex k-gon inside Delta,
so the claimed strong restrictions follow.

For k=3, Delta has at most two vertices; the same argument and the
two-point-cup convention handle every case. The reflected leftmost
theorem is sound: horizontal reflection reverses x order, and a
second reversal comes from relabelling each triple increasingly.
Cup/cap signs are consequently preserved. A lower chain remains a
lower chain, with left and right exchanged. There is no vertical
reflection and no exchange of cups with caps.

The equivalence of the additional hypothesis with “r belongs to every
k-cup” is exact: a k-cup avoiding r is precisely a k-cup contained
in U. The condition is vacuous when there are no k-cups. These facts
justify the source's necessary condition for a counterexample after
deleting each extreme point, without asserting that the two surviving
cups must be different.

The author's added conditional Q_S localization is also correct within
the same theorem. If e in E starts a cap (e,x,z) in S, then x cannot be
r because z>x and r is rightmost. Hence x is in U. The (k-1)-cup ending
at e extends by x entirely inside U, a contradiction. Thus e starts no
3-cap in S, and r trivially starts none, giving Delta contained in Q_S.
This does not justify an unconditional Q_S rule: the absent-k-cup
hypothesis is still used in that contradiction.

## Valid two-label assignments and concatenation

For the canonical rule, a cap (x,y,z) gives s(xy)=2. If s(yz)=2,
there is a w>z with (y,z,w) a cap, yielding the 4-cap (x,y,z,w).
Thus s(yz)=1. This proves that the canonical assignment exists and
satisfies the defining validity condition.

Now discard canonicity and keep only this condition for **every cap**:
its successive edge labels are (2,1). If s(xy)=1, no triple (x,y,z)
with z>y can be a cap, so x prepends to any cup starting at y. If
s(xy)=2, no triple (w,x,y) with w<x can be a cap, so y appends to
any cup ending at x. These are contrapositives of the condition,
not claims that an arbitrary label 2 must have a future cap witness.
They work for two-point cups and by vacuity for singletons.

For the alpha inequalities, a cup T ending at ci with a last edge
labelled 1 can be joined to the suffix ci,...,cL. If the suffix has
another vertex, the joining turn is positive by that label-1 rule;
the other turns were already positive. T's earlier vertices are
strictly before ci and the suffix's other vertices strictly after,
so the only overlap is ci. If i=L there is no joining turn: T
itself gives the necessary long cup. Thus length at least i+1 makes
the combined length at least k when L=k-1. Since no n-cup implies
beta<=k, its endpoint belongs to R. For a missed lower chain this
is a contradiction, establishing alpha(ci)<=i and alpha(c1)=1.
The default alpha=1 never provides an imaginary edge: in the
contradiction alpha>=i+1>=2, so an actual last-edge witness exists.

The other localization statements also follow with their stated
hypotheses: a k-cup ends in R; a target's lower chain has length
k or k-1; a missed one cannot have length k, and its endpoint has
beta exactly k-1. If a cap starts at a point in R, the first
extension gives an n-cup, forbidden by no convex n-gon. Hence R
itself contains no 3-cap.

## Shared-endpoint fact and noncanonical reflected labels

Let Pz and zQ be k-cups, with a the last vertex of P and b the first
of Q. Since each cup is x-increasing, all vertices of P are left of
z and all of Q are right of z; the two cups intersect only at z.
For k>=3 both a and b exist and Q has at least two vertices.
Let c be its last, so a<z<b<=c, in fact b<c here.

If a 4-cap already exists, the first conclusion of the fact holds.
Otherwise use any valid assignment, whose existence follows from
the canonical one. When s(ab)=2, horizontally reflect the points,
reverse their x-order, and assign each reversed edge the label
3 minus its old label. A cap remains a cap under this operation.
Its old consecutive labels (2,1) reverse to (1,2) and complement
back to (2,1), so the new assignment is valid for **every** cap.
The old right cup becomes the new left cup, and vice versa. The
new connecting edge is the reversed old ab and has label 1.

This is a valid WLOG step even though the new assignment need not
be canonical. The subsequent argument uses only validity's two
extension rules, never the interpretation “there is a future cap.”
The resulting forbidden configuration reflects back to one of the
same three geometric kinds. No unproved symmetry of alpha or of
canonical labels is invoked.

With s(ab)=1, prepend a to the cup Q. This gives a k-cup aQ.
General position leaves exactly two cases for (a,z,c):

- If it is a cup, append c to Pz. Its last turn is exactly (a,z,c),
  and c is new; Pzc is a (k+1)-cup.
- If it is a cap, take the upper chain (a,z,c) and lower chain aQ.
  Their common endpoints are a,c and their interiors are disjoint:
  z<b, whereas all interior vertices of aQ are in Q. The cap's
  interior vertex is above the endpoint chord; all cup interior
  vertices are below it. Each chain is convex on its respective
  side, so their union is a convex (k+1)-gon. Its size is
  3+k-2=k+1. Other vertices of P or S are irrelevant: the statement
  concerns convex position, not an empty polygon.

For k=3, Q=(b,c) and aQ is a three-point cup. The first branch gives
a four-point cup Pzc; the second gives the four distinct vertices
a,z,b,c in convex position. Neither branch assumes k>=4.

Finally, if R had k vertices, its first k would form a k-cup whose
first vertex also ends a k-cup by beta=k. They meet only at that
vertex, so the shared-endpoint fact applies. No 4-cap and no convex
n-gon exclude all its alternatives, including the n-cup. Thus
|R|<=k-1. This establishes the source's size bound without a
numerical Baek theorem or an unproved decomposition statement.

## Verdict and limits

The absent-k-cup hypothesis is used exactly where the source says:
it rules out c=2 upper chains in U and supplies the contradiction
after each extension inside U. The no-n-gon hypothesis enters only
the general boundary argument of Section 2. The extreme-point
reflection preserves cups/caps, while the shared-endpoint WLOG
additionally complements the auxiliary edge labels; the source
correctly distinguishes these operations.

No substantive correction is requested. For eventual formalization,
make the nonempty-S and small-cup conventions explicit. Nothing in
this audit extends the unrestricted a=4 theorem, repairs the missed
chains, changes an a=5 statement, or establishes Euclidean
realizability of the encoder's separate abstract counterexample.

# The all-cap cut

**PROVED (written), n>=5.** Let U=L disjoint-union R be a real GP set,
x-separated with both blocks nonempty. Suppose every crossing triple
(LLR or LRR) is a cap. Assume U has no five-cap and no convex n-gon.

If |L|,|R|>=2, U has a terminal-safe weak Delta. In fact, for **every**
l in L, the set

    A={l} union R

is such a selector. No smaller-size theorem, capacity bound, T_n premise,
or condition on the maximum cup is needed in this case.

## Proof for two non-singleton blocks

Both L and R are cups. If three points in L formed a cap, adding any two
points of R would give a five-cap: the one internal triple is a cap and
every crossing triple is a cap. The same argument with the blocks reversed
excludes every cap triple of R. General position then makes all their
triples cups. Consequently |L|,|R|<=n-1, since a cup is a convex polygon.

Every selected cap triple is of the form l<b<c with b,c in R; triples
inside R are cups. Choose any two ambient points u<v in L. The quadruple
u,v,b,c is a four-cap, since all four of its triples cross the cut.
It has the same terminal pair b,c and therefore protects the selected
triple l,b,c. The witness need not use l as one of its first two points.

The selected set has no four-cap. Four selected R points are a cup;
one selected L point and three R points include a cup triple in R.
There cannot be two selected L points.

Every target intersecting R is hit. Any remaining (n-1)-gon lies in L;
since |L|<=n-1 it must be all of L and hence contains l. This proves
target coverage and completes terminal-safe selection. QED.

In particular the proposed mixed-polygon bound is unnecessary for the
proof. It is nevertheless consistent: a mixed convex set can use at
most two points from each cup block. If a<b<c lie in one block and d in
the other, the middle vertex b lies inside the triangle on the other
three, by the internal cup sign and the three crossing cap signs.
The selector proof does not depend on this optional observation.

## Singleton-left case is directly positive

Let L={l}. An R four-cap together with l would be a five-cap, so R has
no four-cap. Select A=R. Each selected R cap a<b<c is protected by the
ambient four-cap l,a,b,c. Every target has at least4 points because
n>=5, so cannot lie in the one-point complement {l}. Thus A is terminal-safe.

This is the noncritical small-left case of the high-split theorem,
but the preceding direct proof avoids any induction dependency.

## Singleton-right case uses T_n(L)

Let R={r}. This is a low split with right cup maximum1. A four-cap in
L together with r would make a five-cap, so L has no four-cap. It also
has no n-gon. Since 1<=n-4, the proved arbitrary-right-block transfer
applies whenever T_n(L) holds.

Explicitly, an Option1 cup B in L gives A=B union {r}. Its mixed selected
cap a<b<r is protected by an L three-cap ending at b, followed by r;
all old selected triples are cups. Every new target contains r and old
targets meet B. An Option2 partition L=B disjoint-union D into cups,
|D|<=n-2, gives A=B: the complement D union {r} has at most n-1 points,
and any mixed convex subset has at most3 points because D is a cup.
Thus it has no (n-1)-gon for n>=5. The same terminal/cap conditions hold
because B is a cup.

The singleton-right case is not unconditional for arbitrary n unless
the relevant T_n premise is supplied. This is the only such premise
for an all-cap cut; it is not the low-split critical d=n-2 branch.

## Exact cut consequences

* For any n>=5, every all-cap cut with |R|>=2 is directly positive,
  including singleton-left cuts. The two-point set is trivial as well.
* Universal T6 is now closed by the finite audits and checked capacity11.
  Therefore **every admissible n6 set admitting any all-cap cut has a
  terminal-safe weak Delta**, without a cardinality or minimality premise.
* T7 is independently closed through left15. Therefore **every admissible
  n7 set of full size at most16 admitting any all-cap cut is positive**.
  In particular all all-cap cut rows may exclude terminal counterexamples
  in a full14 search, without a full13 theorem for the singleton case.
* Once universal T7 has completed its remaining certificate verification,
  the same all-size all-cap conclusion follows for n7. That conclusion
  remains conditional here until the independent proof closure is read.

All these constructions are terminal-safe and therefore also satisfy
each weaker protection rule that accepts terminal witnesses. No CNF is
created or changed in this packet. A new cut encoder still needs its
own semantic and implementation audit.

Exact positive controls are in `data/all_cap_controls.json`; their driver
is `tools/all_cap_controls.py`. The recorded absence of these cuts in
specific obstructions is not used as a theorem premise.

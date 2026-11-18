# A selection theorem for a separated n=7 subclass

This n=7 proof and its original fixtures are retained as an instance of
the general n>=5 theorem in [separated_general.md](separated_general.md).

**PROVED (written).** Suppose U is a finite real point set in general
position, with distinct x coordinates, no five-cap, no six-cup and no
convex seven-gon. Suppose it has a nonempty split U=L union R such that
every L point precedes every R point in x order and

    every LLR triple is a cup; every LRR triple is a cap.       (S)

Then one global cup-ending rank level is a terminal-safe weak Delta, hence
a uniform-envelope Delta. In particular this settles the subclass with
maximum cup exactly five. The restriction (S) is a geometric hypothesis;
it is not asserted for arbitrary sets in the rank-five class.

Let c be the maximum cup length in L, and let beta_U be longest cup length
ending at a vertex of U. The explicit selection is

    A = {v: beta_U(v)=5}       if c<=2,
    A = {v: beta_U(v)=4}       if c=3 or c=4.                 (A)

The hypotheses imply c<=4. No size bound on U occurs in this theorem.
It does not contradict the 18-point terminal-safe obstruction, which
cannot satisfy (S). This is a written theorem only; exact controls and
verification scopes are separate. No novelty or numerical ES claim is made.

## 1. Consequences of the split

A cup meeting both blocks contains at most one point of R, because an LRR
triple is a cap. Conversely any cup in L followed by any one R point is a
cup, by the LLR condition. Similarly a cap meeting both blocks contains
at most one point of L, and any one L point followed by a cap in R is a cap.
Consequently

    maxcup(U) = max(maxcup(L)+1, maxcup(R)),
    maxcap(U) = max(maxcap(L), maxcap(R)+1).                 (1)

In particular c<=4 and R has no four-cap. For v in R, the same argument
applied to cups ending at v gives the exact rank identity

    beta_U(v) = max(c+1, beta_R(v)).                        (2)

Ranks of L vertices are unchanged by adding points to their right.

## 2. Mixed convex polygons

**Split-polygon lemma.** A subset meeting both blocks is convex if and
only if its L part is a cup and its R part is a cap. Singleton and pair
parts are allowed with their usual vacuous triple conditions.

For necessity, if x<y<z in its L part form a cap, then for any r in its R
part, y is strictly inside triangle x,z,r: the three determinants relative
to that triangle are positive by (S) and the negative turn xyz. Likewise,
if a<b<d in its R part form a cup, then for any l in its L part, b lies
strictly inside triangle l,a,d, by the LRR signs. Such a subset cannot be
convex. This proves both necessary chain conditions.

For sufficiency, its lower hull is the L cup followed by the last R point,
and its upper hull is the first L point followed by the R cap. The chain
turns and all cross-edge supporting inequalities follow from (S). These
two chains contain every selected point and intersect only at the first
L point and last R point. Thus all points are strict hull vertices.

It follows that the maximum size of a mixed convex polygon is

    maxcup(L)+maxcap(R).                                   (3)

For any point set, an upper cap of size at most a and a lower cup of size
at most b bound its convex polygon sizes by a+b-2.

## 3. Why the indicated rank level hits every hexagon

**Case c=4.** If R had a three-cap, (3) would produce a convex seven-gon.
Thus R has no three-cap and is itself a cup, of size at most five. There
are no internal hexagons in R. A mixed hexagon must have four L vertices
forming a cup and two R vertices; its last L vertex has rank four in L
and in U. An internal hexagon in L has an upper cap of size at most four,
so its lower cup has size at least four; since c=4, its right endpoint has
rank four. Thus the global level four hits all hexagons.

**Case c=3.** R has no four-cap by (1). Its vertices have global rank four
or five by (2). Let Q be its global rank-five vertices; equivalently Q is
the beta_R=5 level. **Q is a cup.** Indeed if a<b<d in Q formed a cap,
choose a longest cup ending ...p,a. If p,a,b were a cup it would extend to
a six-cup at b. Hence p,a,b is a cap, and p,a,b,d would be a forbidden
four-cap in R. This proves the assertion.

There is no internal hexagon in L, because its cap and cup maxima are at
most four and three, giving polygon bound five. A mixed hexagon has three
L cup vertices and three R cap vertices by (3); that R cap cannot lie in
the cup Q, so it contains a global rank-four point. An internal hexagon
in R cannot lie in Q either: Q is a cup of size at most five. Every such
hexagon therefore also contains a global rank-four point. Level four hits
all targets.

**Case c<=2.** No hexagon lies in L, and by (3) no mixed hexagon exists,
since maxcap(R)<=3. An internal hexagon in R has upper chain at most three
and hence lower cup at least five. Its right endpoint has beta_R=5, since
there is no six-cup, and consequently beta_U=5 by (2). Thus level five hits
all targets. If there are no targets, an empty chosen level is harmless.

These cases exhaust (1), proving the hitting claim for (A).

## 4. Terminal and uniform safety

The earlier rank lemma applies to a single global beta level: if a<b<d
is a cap triple with beta_U(a)=beta_U(b), then a penultimate vertex p of
a longest cup ending at a satisfies p,a,b cap, so p,a,b,d is an ambient
four-cap ending in b,d. Every cap triple of the selected level therefore
has its terminal pair realized by an ambient four-cap.

There is no four-cap in that level: the first three vertices of such a
four-cap have an ambient four-cap on their terminal pair, and appending
the fourth selected point would create a five-cap. Thus A is a terminal-
safe weak Delta. Its triple lines are themselves ambient four-cap lines,
so it is uniform-envelope safe. For every rightmost r preserving absence
of five-caps, A+r is a weak Delta, with no no-seven-gon assumption on the
extension needed.

## 5. Nontrivial exact controls

The recursive separated cup-cap construction E(a,b) has maximum cup a,
maximum cap b and binomial(a+b-2,a-1) points. Start with a b-point cap for
a=2 and an a-point cup for b=2, and form

    E(a,b) = high_split(E(a-1,b), E(a,b-1)).

Here high_split translates the second block sufficiently far up and to
the right to enforce (S). Formula (1) proves the chain maxima and the
binomial recurrence proves the size. All coordinates can be integral.

Use the following controls, none of which assumes the selection result:

* L=E(3,4), R=E(5,3): 10+15=25 points, case c=3.
* L=E(4,4), R=E(5,2): 20+5=25 points, case c=4.
* L=E(2,4), R=E(5,3): 4+15=19 points, case c=2.

Their full maxima are (cap,cup,gon)=(4,5,6). For the last two cases the
maximal polygon size follows from the internal bounds and (3); existence
of a six-gon is checked directly. All three controls passed exact checks
of split signs, general position, ranks, every target hit and terminal
certificates, with no seven-gon. The 25-point controls each have 7,126
hexagons; the 19-point control has 410. Each selected complement has maximum
gon five in the separate chain-based replay. The two 25-point examples
have the same labeled hexagon family but different four-cap counts (1,501
and 501), so these are correlated controls, not coverage statistics.

The known terminal18 and boundary three-block fixtures admit no split (S),
as checked at every x cut. They remain outside the proved subclass.

## 6. Scope

This proves a specified geometric subclass of maximum-cup-five sets. The
single-common-rank-four-representative candidate is separately refuted by
terminal18. No implication from maximum cup five to the split hypothesis
is proposed. The full next cup-rank subclass remains unresolved here.

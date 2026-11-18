# Favorable selection from cup ranks and small complements

**PROVED** means written arguments below, not Lean proofs. Weak D(5,7) and
D(5,8) remain open in general. The seven-point cap-only strengthening in
Section 6 is **refuted by an explicit real example**. Finite checks are
reported separately as COMPUTED. No certificate or literature-priority claim
is made.

All point sets are finite, in general position, with distinct x-coordinates.
Caps and cups are listed in increasing x-order. A weak Delta meets every
whole convex (n-1)-gon and contains no four-cap. A rooted weak Delta must
also contain the prescribed point r. Write k=n-1 and U=S minus {r}.

## 1. Rank-three blockers force a cup-rank increase

Let beta(v) be the longest cup length ending at v in U, allowing singleton
cups. Let h(b,c) be the longest cap length ending in the pair b<c.

**Lemma 1.** If a<b<c is a three-cap and beta(a)>=beta(b), then h(b,c)>=4.
Equivalently, a three-cap of terminal rank exactly three has beta(a)<beta(b).

**Proof.** beta(a)>=2, since b has a two-point cup ending at it. Choose a
longest cup ending ...p,a. If p,a,b were a cup, appending b would give
beta(b)>=beta(a)+1, a contradiction. Thus p,a,b is a cap. Together with
the cap a,b,c it gives the four-cap p,a,b,c. QED.

Call A *terminal-safe in U* if it has no four-cap and every three-cap of A
ends in a pair of cap rank at least four in U. In a five-cap-free U, any set
whose beta-values are nonincreasing in x-order is terminal-safe. Lemma 1
proves the terminal-pair condition. A hypothetical four-cap a,b,c,d in A
would extend the ambient four-cap ending b,c by d to a five-cap. In
particular, **each individual beta-level is terminal-safe**.

As already established in resume/weak_theory, if r is rightmost and S is
five-cap-free, adding r to a terminal-safe old weak Delta is safe. Indeed,
an alleged cap a,b,c,r would extend an ambient four-cap ending b,c to a
five-cap. The new content here is a way to obtain the terminal-pair property
from cup ranks, rather than assuming that property as an exact criterion.

This does not show that one beta-level, or a set with nonincreasing beta,
always meets all targets. Nor does it license combining arbitrary levels.

## 2. A favorable choice when the longer cups are absent

**Theorem 2.** Let n>=6. Suppose U has no five-cap and no (n-2)-cup. Let E
be the right endpoints of all convex (n-1)-gons in U. Then E is a weak
Delta, and it is terminal-safe in U. Consequently E+{r} is a rooted weak
Delta for every rightmost r for which S=U+{r} has no five-cap.

**Proof.** If there are no target polygons, E is empty. Otherwise every
target H has an upper cap of at most four vertices. Its lower cup therefore
has at least (n-1)+2-4=n-3 vertices. The missing (n-2)-cup forces equality.
For the endpoint e of H, beta(e)>=n-3, while beta(e)<=n-3 throughout U.
Thus E lies in the single beta-level n-3. Lemma 1 and five-cap-freeness make
E terminal-safe. It meets every old target at its right endpoint. Adding r
is cap-safe and hits every new target. QED.

No no-n-gon hypothesis or restriction on |U| was used. The chosen E also
hits old lower chains, but no general cup-side claim is inferred.

This extends the *method* of the earlier a4 terminal-polygon lemma to an
a5 subclass; it is a selection theorem for this subclass, not a repetition
of the previous envelope sufficient condition. It also shows that a
minimal failing selection cannot live entirely in the short-cup subclass.

## 3. Bounded rooted existence by a cup/endpoint dichotomy

**Lemma 3 (cup complement).** Suppose U has a cup C with
|U minus C|<=n-2. Then C is an old weak Delta and C+{r} is a rooted weak
Delta, for **any position of r**.

**Proof.** A target polygon has n-1 vertices, so cannot be disjoint from C.
A four-cap in C+{r} would contain at least three vertices of C; those three
are a cup, whereas every triple of a cap is a cap. Thus no such four-cap
exists. Old targets are hit by C and new targets by r. QED.

**Theorem 4 (PROVED).** For n>=6, any five-cap-free S with a prescribed
rightmost point r and |S|<=2n-3 has a rooted weak Delta. In fact U has a
terminal-safe weak Delta. No no-n-gon premise is needed.

**Proof.** If U has an (n-2)-cup, choose n-2 of its vertices as C. Then
|U minus C| <= (2n-4)-(n-2)=n-2, so Lemma 3 applies; a cup is trivially
terminal-safe. Otherwise Theorem 2 applies. QED.

The leftmost version follows by horizontal reflection. This gives written
bounds **11 points for n=7 and 13 points for n=8**, not a new numerical ES
bound and not a larger frontier than the parent's finite certifications
(through 13 and 14 points respectively, subject to their separate audits).
Omitting the no-n-gon assumption gives **weaker premises and a stronger
theorem** than proving just the corresponding valid-instance cases.

For a root in arbitrary position, a simpler version yields |S|<=2n-4:
if U has no target, {r} works; otherwise a target contains an (n-3)-cup C,
and |U minus C| <= (2n-5)-(n-3)=n-2. Apply Lemma 3. This gives 10 and 12
points at n=7,8 without an extreme-root or no-n-gon assumption.

## 4. Localization of the first possible failure

The following isolates a genuinely narrower next case; it does not close it.

**Corollary 5.** Suppose S is five-cap-free, r is rightmost, |S|=2n-2,
and there is no terminal-safe old weak Delta (in particular this conclusion
applies if there is no rooted weak Delta). Then:

1. the longest cup in U has length exactly n-2;
2. for **every** (n-2)-cup C in U, U minus C is a convex (n-1)-gon;
3. each of these complementary polygons has upper/lower chain sizes
   (3,n-2) or (4,n-3).

**Proof.** If U has no (n-2)-cup, use Theorem 2. If it has an (n-1)-cup,
its complement has at most (2n-3)-(n-1)=n-2 points, and Lemma 3 supplies
a terminal-safe solution. Thus the maximum is n-2. A cup C of that size
is cap-free and terminal-safe; its only possible disjoint target is its
entire complement, of size n-1. If that complement were nonconvex, C would
work. Finally, no five-cap bounds the upper side by four, and no (n-1)-cup
excludes upper side two. QED.

At n=7 the first case is |S|=12, |U|=11, maximum cup length five; every
five-cup would have to leave a convex hexagon. At n=8 it is |S|=14,
|U|=13, maximum cup length six; every six-cup would leave a convex heptagon.

The no-n-gon premise has still not been needed. In a valid instance it
additionally forbids extending any of these complementary polygons by any
point of C. Deriving a contradiction from this simultaneous condition, or
finding a favorable exchange between the complementary cups/polygons,
is an explicit open gap. A single private-hit star does not establish it.

## 5. Review of the parent's nonconvex-four argument

The parent supplied the following different result, which this track
reviewed; it should not be attributed to this track as a new derivation.

**Parent lemma (PROVED, argument checked).** If n>=6, S has no five-cap
and no convex n-gon, and |S|<=n+3, then every prescribed root r belongs
to a weak Delta, even if r is not extreme.

For |S|<=n+1, choose a set A containing r with at most three points and
|S minus A|<=n-2. For |S|=n+2 or n+3, U has at least n vertices and
therefore is not in convex position. It contains a nonconvex four-set W:
a point inside the hull of the others is inside a triangle of other points
(triangulate the hull), and general position makes the containment strict.

If |S|=n+2, choose A of size three containing r outside W. Its complement
has n-1 points and contains W, so is not convex. If |S|=n+3, the set
S minus W has n-1>=5 points and contains r. Choose five of them including r.
Some four-subset containing r is not a cap: otherwise every triple of
those five lies in one of the four-subsets containing r, making all
triples negative and hence all five a cap. Choose this four-subset as A.
Again S minus A has n-1 points and contains W. A is cap-free and its
complement is not a target, so it hits every target. QED.

The nonconvex-four step is where the no-n-gon assumption is used. For n=7
this arbitrary-root bound is 10, and for n=8 it is 11; Section 3 independently
improves the n=8 arbitrary-root bound to 12 without using no-n-gon.

## 6. Seven points refute a proposed pure-cap extension

**Refuted claim:** every seven-point five-cap-free set has a five-point
four-cap-free subset containing its rightmost point.

Use these exact coordinates in x-order:

```
0=(0,0)  1=(1,1)  2=(2,0)
3=(3,100)  4=(4,99)  5=(5,100)  r=6=(6,-10).
```

The first block L={0,1,2} is a three-cap, the second H={3,4,5} a
three-cup. Every slope between the blocks is at least 20, while within
either block every slope lies between -1 and 1. Hence any triple with
two points in L and one in H is a cup, and any triple with one in L and
two in H is a cap. These descriptions also show no collinear triples
among the first six points.

There is neither a four-cap nor a four-cup among the first six points:
every 3+1 or 1+3 distribution has opposite orientations from the pure
triple and a mixed triple, and every 2+2 distribution has both mixed
orientations. Every secant through the first six points has height at
least -4 at x=6, whereas y(r)=-10. Thus every old three-cap extends by r
to a four-cap, and no old pair is collinear with r. No five-cap can occur:
one avoiding r would contain an old four-cap; one using r would also
have an old four-cap after deleting r.

Any five-set containing r contains four old points. They are not a cup,
so some triple is a cap. That triple extends by r to a four-cap. All 15
candidate five-sets therefore fail. The four-set {0,1,3,r} is cap-free,
so the maximum rooted cap-free subset size is exactly four. There is
also a cap-free five-set avoiding r, e.g. {0,1,2,3,4}.

The first six points have no convex five-gon (both chain lengths are at
most three), so the seven-point set has no convex six-gon. Thus the
example is compatible with the no-n-gon hypothesis for every n>=6.
It does **not** refute rooted weak Delta: it refutes a cardinality tool
for enlarging the parent's nonconvex-four construction. Section 3 reaches
larger bounded cases using a different argument.

## 7. The projective normal form, checked algebraically

This suggestion came from the parent. Translate y and x so that the
rightmost root is r=(1,0), with every old x<1. Set

    T(x,y)=(x/(1-x), y/(1-x)).

The homogeneous matrix has determinant one and sends [1:0:1] to [1:0:0],
the horizontal point at infinity. For old points p,q,s,

    det(Tp,Tq,Ts) = det(p,q,s) / ((1-x_p)(1-x_q)(1-x_s)).

All denominator factors are positive. Also x/(1-x) is strictly increasing
on x<1. Thus old x-order and triple signs, in particular caps, cups and
convexity, are preserved. For p<q,

    det(p,q,r) = y_q*(x_p-1) + y_p*(1-x_q),
    y'_q-y'_p = -det(p,q,r)/((1-x_p)(1-x_q)).

Therefore **a cap turn p,q,r corresponds to a POSITIVE transformed slope**,
not a negative one, under this displayed transformation. For example
p=(0,0), q=(1/2,1), r=(1,0) is a cap; its images are (0,0),(1,2), an
increasing edge. Reversing the sign of transformed y would change the
slope sign but would also interchange the old cup and cap conventions.

With the displayed T and the repository's negative-determinant cap
convention, the corrected normal form is: every old four-cap has
**negative** last-edge slope (otherwise it extends to a forbidden five-cap),
and an old weak Delta extends at r iff none of its three-caps has a
**positive** last-edge slope. General position excludes zero last slopes.
Old four-cap-freeness remains an independent requirement; the slope
condition alone does not imply it. This is a reformulation, not an
existence proof, and no convex polygon containing infinity is assumed.

## 8. Selection failures and the remaining gap

The old nine/ten-point private-hit stars already refute the implication
"a private polygon for each point of a rank-three blocker forces a
five-cap or an n-gon." Their selected triples are inclusion-minimal old
solutions, but need not have minimum cardinality or minimum envelope.
The current rank lemma adds beta(a)<beta(b) to such a blocker; it supplies
no coverage-preserving recoloring by itself.

The tiny probe retains failures of lexicographically first old solutions
at fixed **larger** cardinalities. They already hit every full target;
only forcing the root red fails. They are not failures of a minimum-size
rule, a minimum-envelope rule, or unrooted extension. All six controls
admit a common beta-level hitting their targets, so they cannot establish
that this stronger selection always exists. Five of the six have
singleton old solutions, making their minimum-size checks especially weak.

No argument here proves favorable selection in the remaining long-cup
cases of general size. No global minimum-envelope exchange theorem, no
universal antichain transversal, and no proof that a minimal failing
exchange forces a forbidden polygon or cap is claimed.

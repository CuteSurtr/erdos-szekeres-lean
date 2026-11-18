# Cup paths and the endpoint-sign criterion

**PROVED** here means written proof, not Lean formalization. Finite controls
and enumerations remain COMPUTED. No universal selector existence is claimed.

## 1. Endpoint-sign protection

For query pair p=(b,c) and support q=(u,v), let d(X)=ell_q(X)-ell_p(X).
At an endpoint z of p only, sign d(x_z) is -chi(u,v,z); at an endpoint of q
only it is chi(b,c,z); at a shared endpoint it is zero. The positive secant
denominators justify these signs even when the indices in chi are unsorted.

If the final endpoint value is nonnegative and some earlier endpoint value
is nonpositive, with at least one strict, the slope of d is positive.
Consequently d(X)>0 beyond the last endpoint. Identical pairs give d=0.
An ambient four-cap with terminal pair q therefore protects p under these
conditions. This rule depends only on ordered orientations.

For disjoint pairs, the general-position endpoint values are all nonzero.
An affine difference can change sign at most once among four increasing
abscissae. These eight sign patterns correspond to the eight possible
four-point orientation patterns. There are six ways to choose which pair
is the query, giving48 cases. The predicate is positive in18 cases. The
direct componentwise cup-union rule accepts only2 of these disjoint cases.
The table and exact opposite-realization controls were frozen in the main
cup record; this subrecord checks the stated predicate against all48 rows.

## 2. Cup paths flatten to two steps

Write p -> q when q has componentwise later endpoints and the distinct
endpoint union is a cup. Equal pairs may be omitted. The endpoints increase
along every edge, so this is a DAG.

**Theorem.** For p=(b,c), q=(u,v), with u>=b,v>=c, the following are equivalent:

1. q is reachable from p through cup edges, including a path of length zero.
2. The endpoint-sign protection predicate holds for p,q, or p=q.
3. The following two triples are cups whenever nondegenerate:
   (b,c,v) if v>c, and (b,u,v) if u>b.
4. There is a cup path through the single intermediate pair(b,v), deleting
   repeated pairs. In particular, every reachable pair has a path of length<=2.

**Proof.** One cup edge has positive slope difference and nonpositive line
difference at its source's left endpoint, and nonnegative difference at its
target's right endpoint. At an earlier abscissa the difference remains
nonpositive; at a later abscissa it remains nonnegative. Along a path all
left endpoints move right and all right endpoints move right. Evaluate each
edge at the original x_b and final x_v, then add. The total has positive
slope, nonpositive value at x_b and nonnegative value at x_v; at least one
endpoint inequality is strict for distinct pairs. This proves1=>2.

For forward endpoints, x_b and x_v are the extreme endpoint abscissae.
Predicate2 implies d(x_b)<=0<=d(x_v). If u>b, general position makes the
first inequality strict, equivalent to chi(b,u,v)>0. If v>c, the second
is strict, equivalent to chi(b,c,v)>0. This is3. These are exactly the two
three-point cup unions for p -> (b,v) -> q, ignoring equal pairs, so3=>4.
The implication4=>1 is immediate. QED.

This theorem uses neither a four-cap nor the no-five-cap premise. When the
last pair actually ends a four-cap, it provides a uniform envelope support.
The intermediate pair need not terminate any cap triple: the closure must
range over **all ordered pairs**, as in the implementation and theorem.

Thus a generic closure encoder need not introduce recursive reachability
depth: a support flag for(u,v) and at most two ordinary three-cup flags
suffice. This is a mathematical observation; the parent's running generic
direct-cup encoder was not changed.

## 3. Which additional patterns survive no-five-cap?

If q=(u,v) ends an ambient four-cap and c>v, endpoint-forced domination
puts point c strictly below ell_uv at x_c. Appending c to that ambient
four-cap creates a five-cap. Therefore **v>=c** for every endpoint-forced
support in a no-five-cap set. This rules out9 of the18 disjoint forced cases.

The condition u>=b need not hold. Hence the endpoint rule can be stronger
than cup-path closure even under no-five-cap. The retained data give32 such
additional cap-terminal pairs, all requiring a support with u<b. An exact
small subset witness is retained separately. The remaining orientation
patterns are not all forbidden: the known18 q(5,6), supported by(12,13)
ending four-cap(0,9,12,13), already supplies a valid non-cup forced pattern.

## 4. Strict hierarchy on real valid data

The six-point fixture extracted from old18 has a cap triple(0,1,2), an
ambient four-cap(0,3,4,5), and cup path

    (1,2) -> (2,5) -> (4,5).

The source pair has **no direct ambient cup support**. The fixture is in
general position and has no five-cap; all four-caps are enumerated in its
packet. Thus presence of an actual terminal four-cap does not collapse cup
closure to one step. A separate at-most-seven-point fixture shows that the
broader endpoint rule can also exceed closure under the same premise.

All witnesses are finite exact controls. No theorem says one of these
selectors exists for every valid point set, and no counterexample to
ordinary weak Delta or full uniform-envelope selection is claimed.

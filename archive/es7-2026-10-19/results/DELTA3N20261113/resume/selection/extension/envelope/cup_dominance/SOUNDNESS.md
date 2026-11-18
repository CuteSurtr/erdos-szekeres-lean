# Orientation-only cup protection

## Sufficient line domination

Let b<c and u<v in increasing x-order. Suppose u>=b,v>=c and the distinct
union of the pairs is a cup: all its sorted triples have positive determinant.
If the pairs coincide, their lines coincide. Otherwise there are three or
four distinct points. Increasing cup secants imply

    slope(u,v) > slope(b,c).

For disjoint consecutive pairs this follows from the consecutive cup slopes.
For interleaved pairs b<u<c<v, compare(b,c) to(u,c), then(u,c) to(u,v).
For a common endpoint or u=c the corresponding single triple gives the same
comparison. These exhaust the componentwise endpoint order.

At x_v, the ambient line has height y_v. If v>c, the cup triple(b,c,v) puts
y_v strictly above line(b,c); if v=c their heights agree. The slope inequality
therefore implies line(u,v)>=line(b,c) for every X>=x_v, and in particular
for every X>max_x(U). When(u,v) ends an ambient four-cap, its line is part
of the ambient maximum. This proves the stated sufficient protection rule.

The rule depends only on x-order and triple orientations. It is weaker than
requiring the pair(b,c) itself to end an ambient four-cap, but it need not
be necessary for actual line-envelope safety. The geometric seven-point
control has a cap triple(0,1,2) protected by the cup union(1,2,5,6) and the
ambient four-cap(3,4,5,6), although(1,2) cannot end any four-cap.

## Membership formula

Enumerate the full exact target polygons and four-caps of a validated set U.
For each cap triple(a,b,c), enumerate all ambient terminal pairs and mark it
bad iff none satisfies the preceding rule (including equal pairs).
The CNF has one variable per point. Positive clauses hit every whole
(n-1)-gon, negative four-cap clauses enforce old weak Delta, and negative
bad-triple clauses enforce cup protection for every selected cap triple.
Thus SAT is equivalent to existence of this specific sufficient selector.
It is not equivalent to arbitrary uniform-envelope selection.

Every positive model is checked against all clauses. Each selected cap
triple receives an actual ambient four-cap witness and its cup union, which
are checked with integer determinants. The ambient line's slope and height
at M are also checked directly by integer cross-products. The separate
positive geometry/certificate replay then verifies ordinary weak Delta and
uniform envelope safety. A negative formula, after independent certification,
would refute only universal existence of this cup-protected selector.

## General four-point orientation classification

For two disjoint pairs define d(X)=line(ambient)(X)-line(query)(X). At each
of the four endpoint abscissae, the sign of d is determined by one triple
orientation: at an ambient endpoint it is the query orientation; at a query
endpoint it is the negative ambient orientation. Let L,R be the leftmost and
rightmost of the four endpoints. General position makes these values nonzero.

- d(L)<0<d(R) forces positive slope and domination for every X>=R.
- d(R)<0 rules out domination of the entire ray X>=R.
- d(L)>0 and d(R)>0 does not determine the slope sign. With the query line
  normalized to y=0, choose the ambient line positive at all four endpoints.
  Its slope can be slightly negative, zero, or positive without changing
  any triple orientation. Therefore this sign pattern alone cannot force
  domination on the whole ray.

These statements classify all four-point order/sign patterns without LP.
The rule concerns the ray beginning at R. Failure at R does not by itself
exclude domination after a later ambient maximum abscissa M>R.
Additional points can impose further orientation constraints; this analysis
does not classify the full18-point cell.

For the known A={0,5,6,7,8}, the actual supporting pair(14,17) gives++-- on
each sorted quadruple(5,6,14,17),(5,7,14,17). Equivalently d is positive at
all four endpoints. The actual coordinates have a positive slope difference,
but that fact is not forced by those four-point signs. The full structural
packet checks all ambient support pairs, rather than just this chosen one.

# Projection for the cup and endpoint-sign protection formulas

**PROVED (written projection argument), implementation audit pending.**
These formulas test sufficient selection rules, not exact uniform-envelope
selection. An accepted generic UNSAT proof can establish a finite theorem
only after the implementation and this projection are independently checked.
SAT requires exact coordinates before it can refute a real selection rule.
Nothing here claims general Delta existence, Lean checking of the encoding,
or a numerical ES improvement.

## Geometry and the two sufficient predicates

Use the reviewed compact geometry with positive orientation meaning cup.
The universe has m x-ordered points in general position, no five-cap and no
convex n-gon. End4(u,v) means that some ambient four-cap ends in u,v. The
flags for every four-cap and End4 pair are exact equivalences. End4 is false
if fewer than two vertices precede u.

For q=(b,c), the **cup rule** allows its identical End4 pair, or an End4 pair
(u,v) with u>=b, v>=c such that the distinct union of the two pairs is a cup.
For nonidentical pairs this union has three or four vertices. The source
uses an existing positive orientation variable in the three-point case,
and an exact four-cup flag in the four-point case.

For q=(b,c), the **endpoint-sign rule** allows the identical End4 pair or
an End4 pair (u,v) with v>=c and the following applicable tests:

    if v>c: (b,c,v) is a cup;
    if u>b: (b,u,v) is a cup;
    if u<b: (u,b,c) is a cap.

When u=b, the last two tests are absent. When v=c, the first is absent.
These are sufficient signs, not a claim that every numerically dominating
line must satisfy them. In particular, a line may dominate only after a
later crossing, or several ambient lines may jointly protect a triple.

## Why either predicate gives rightward protection

For the cup rule, monotonicity of secant slopes along a cup gives
slope(u,v)>=slope(b,c) when both endpoint indices move rightward. At x_v,
the support line equals y_v, while the target line is at most y_v: this is
the cup turn (b,c,v), or equality if v=c. The affine difference is therefore
nonnegative for every X>=x_v. This includes every X>max_x(U).

For the endpoint-sign rule, put d(X)=ell_uv(X)-ell_bc(X). If u>=b, the
tests give d(x_b)<=0 and d(x_v)>=0. If u<b, they give d(x_u)<0 and
d(x_v)>=0. Shared endpoint equalities are allowed. In every nonidentity
case at least one inequality is strict, so d has positive slope and is
nonnegative beyond x_v. The identical pair gives d=0. This proves the
same protection conclusion. For u>=b this predicate is exactly the
two-step cup-comparison closure, with intermediate pair (b,v); the
backward-left cases u<b add further possible supports.

Suppose A has no old four-cap, meets every old convex (n-1)-set, and each
of its cap triples has one of these supports. Let r be any general-position
rightmost insertion preserving no-five-cap. A new four-cap abc r in A+r
would put y_r below ell_bc(x_r). Its ambient supporting four-cap would
then extend with r to a five-cap, because

    y_r < ell_bc(x_r) <= ell_uv(x_r).

This is impossible. Old targets are hit by A, and every new target using r
is hit by r. Thus A+r is a weak Delta. The enlarged set need not remain
free of convex n-gons. The choice of A precedes every such insertion.

## Exact support flags and containment flags

Each support flag is equivalent to End4(u,v) AND its required cup/cap
orientation conditions. Covered(b,c) is equivalent to the OR of all
eligible supports, including End4(b,c). Bad(a,b,c) is equivalent to
Cap(a,b,c) AND NOT Covered(b,c). Exactness matters because these flags
occur with negative signs. The cup implementation caches literally
identical support conjunctions; the endpoint-sign implementation allocates
a named support for each comparison.

Let D(S) mean that S contains a bad triple OR an old four-cap. At size
three, D aliases Bad. At size four, an asserted D(S) implies the disjunction
of its four Bad children and its exact four-cap flag. Above size four, an
asserted D(S) implies the OR of the five children deleting one of the five
least vertices. A true node descends to a genuine bad triple or four-cap.
Conversely, any witness of size at most four misses at least one of five
chosen deletion vertices. Therefore canonical exact containment values
satisfy every row. These internal flags deliberately need only one-way
implications.

The selected-four-cap condition cannot be dropped. Consider

    (0,0),(1,-1),(2,-3),(3,-6),
    (10,500),(11,600),(12,699),(13,797).

Both four-point blocks are caps; every mixed triple is a cup. There is no
five-cap, and the maximum convex subset has size four. Every cap triple
in A={0,1,2,3} is cup-protected by the ambient four-cap {4,5,6,7}, yet A
itself is a four-cap. For n=7 its complement has only four points and
target coverage is automatic. For n=5, A={0,1,2,3,4} gives the same warning
with a three-point complement. Exact checks are retained in
`data/cup_protected_fourcap_control.json`.

Target containment T(S) uses exact convex (n-1)-subset leaves and the
reviewed one-way recurrence with n children at larger sizes. A true node
descends to an actual target, and canonical containment assignments satisfy
the recurrence because an (n-1)-witness misses one of n deletion vertices.

## Complete failure range and counterexample projection

Set k=m-n+2. The formula includes

    D(A) OR T(U minus A)

for EVERY A of size zero through k. If a larger protected weak Delta
exists, any k-subset remains four-cap-free and protected, and its complement
has size n-2, so it hits every target automatically. Thus this range loses
no working selection. It does not justify growing a smaller selection:
sizes zero, one and two must be retained. The supported source domain is
5<=n<=8 and n-1<=m<=20, hence k>=1.

Every real counterexample to the chosen sufficient rule gives the source
a canonical assignment: its orientation signs, exact geometric and support
flags, and exact D/T containment values. It satisfies every clause. Conversely
the exact flags and descending containment implications interpret a model
as failure of all selections in the encoded abstract geometry. The real
projection is enough for an UNSAT implication even if an abstract SAT model
has no realization. No symmetry, cup-maximum or boundary-complement premise
is added. Optional fixed-sign units are controls only and restrict any claim
to those signs.

## Current validation boundary

The endpoint-sign support predicate separately matches direct exact line
tests in all 9,347,628 comparisons on 317 retained geometries. This does not
by itself audit the full generic CNF. The cup-rule fixed witnesses were
independently checked on 322 fixtures/controls. The n7/m13 endpoint-sign
180-second run ended UNKNOWN. The generic cup n7/m15 run is still active
as of this note. Neither status is a finite theorem.

# Controlled lifts of the 15-point cup-side counterexample

13 November 2026. Bounded follow-up to the completed hypergraph track.
The earlier `theory.md`, witnesses, scripts, and `SHA256SUMS` are unchanged.

**PROVED:** the projection-transfer lemma, an eight-chain obstruction to
constant-weight duplication, and the geometric model-to-CNF implication below.
**CERTIFIED:** the two stated finite cluster CNFs are unsatisfiable; both
cake_lpr outputs are exactly `s VERIFIED UNSAT`.
**COMPUTED:** the exact input geometry, encoder controls, and coordinate audits.

No lift to (5,7) or (5,8) was obtained. The certificates rule out the precise
generic infinitesimal cluster families in Section 3, including coverage by
new polygons projecting to smaller original polygons. They do **not** rule
out arbitrary duplication, aligned tangent limits, general three-point
clusters, or nonlocal point insertions. No claim about either main weak
Delta conjecture follows.

## 1. Input and projection transfer

Input: coordinator's
`/home/jay/research/data/delta3-codex-20261113/coordinator/cup15/realized.json`.
SHA-256:
`1e8b43136d096abb2deaea14743ed62a52ff622a991dd2fbbcb7140a15593b04`.

The input hash, frozen coordinates, and all lower-chain/carrier pairs
are recorded in `lift_probe.json`. The exact audit recovers 80 four-caps,
216 pentagons, 103 distinct lower chains, no five-cap, and no hexagon.
The parent's 183-clause coloring CNF has a cake_lpr certificate; its saved
`cup15_coloring.cake.out` was read and contains `s VERIFIED UNSAT`.
The parent's counts of zero cup-side Delta and 353 weak Delta were not
re-enumerated by this task.

**Lemma 1 (projection transfer).** Let pi:Q -> S map new points to old points.
Suppose:

1. For every four-cap K of S, every choice of one representative from each
   fiber above K is a four-cap of Q.
2. For every old pentagon lower chain C, Q has a convex (N−1)-gon whose lower
   chain L satisfies pi(L) subset C, with endpoints included.

If Q has a four-cap-free red set meeting all its (N−1)-gon lower chains, its
image is a four-cap-free red set meeting all the old chains C.

*Proof.* If the image contained an old four-cap, choose red representatives
over its four distinct vertices and use condition 1. For condition 2, a red
point of L projects to a red point in C. ∎

Thus a (5,N)-valid Q with these properties would lift the old counterexample.
This uses no restriction on how many red clones one fiber contains.

## 2. The exact-one proposal is impossible, even with real weights

The following six triples are actual pentagon lower chains of S:

    018, 068, 268, 169, 269, 189.

Here, for example, `018` denotes {0,1,8}. If all six equations
sum_{p in C} x_p = d hold, subtraction gives

    x0 = x1 = x2 = x6 = t,
    x8 = x9 = d−2t,
    t + 2(d−2t) = d,

so t=d/3. Therefore d=1 already precludes a zero-one set T meeting each
of these six chains exactly once. All six equations are needed in the
displayed zero-one core; deletion witnesses are in `lift_probe.json`.

The chains {1,2,7} and {0,1,2,7} are also actual old lower chains. Giving
both sum d forces x0=0. Together with t=d/3, this forces **d=0**.

**Corollary 1.** There are no real point weights with the same nonzero sum
on every old lower chain. In particular, there is no exact-one transversal,
and no scheme assigning a fixed pointwise multiplicity increment whose
sum on every old lower chain is exactly one or exactly two.

This is a written linear contradiction supported by exact geometric data.
`lift_probe.json` additionally supplies an eight-row rational combination
giving 0=1; `lift_audit.py` checks its coefficients exactly.
It is not a SAT-UNSAT certificate claim.

A related necessary-direction check is COMPUTED: only points 0,11,14 have
a nonempty interval of tangent slopes that duplicates the point on **every**
old lower chain containing it. They miss {1,2,7}. Requiring a selected
point to remain visible on all its old lower chains therefore also fails.
This does not exclude directions whose visibility depends on the chain;
the CNFs below allow that dependence.

## 3. Precisely specified cluster families

For target N=7 set r=2; for target N=8 set r=3. Independently at each original
point p=(x_p,y_p), keep one point, or replace it by r points

    q_(p,a) = (x_p + epsilon*a,
               y_p + epsilon*t_p*a + epsilon^2*a^2),
    a = 0,...,r−1,

for sufficiently small positive epsilon. The slope t_p is **generic**:
it differs from every original secant slope s(p,q). Only its open cell
between those secant slopes matters. The finite model includes all cells,
including the two unbounded cells, and the option not to duplicate p.

For binary clusters this describes generic first-order pair directions.
For ternary clusters it describes thin cups with one common generic limiting
tangent; it does not describe every small three-point cup. Any construction
with the same limiting signs has the same finite model.

The three-point orientation rules follow by expanding the determinant:

- triples from three different fibers have the original sign;
- a pair in one fiber and a third point elsewhere has the sign determined
  by t_p relative to the relevant old secant;
- a triple within a ternary fiber is a cup.

All these signs stabilize for sufficiently small epsilon. The model is
realizable over rational coordinates: use rational cell representatives
and then sufficiently small rational epsilon. In particular, Lemma 1's
four-cap representative condition holds automatically.

### Visibility and exact capacities (PROVED)

For an ordered old chain A containing p, let s_in and s_out be its incident
secant slopes, omitting a bound at an endpoint. A duplicated fiber can
contribute extra points to that chain precisely in these open intervals:

    cup: s_in < t_p < s_out;
    cap: s_in > t_p > s_out.

Let ell_H(p), u_H(p) be these visibility indicators on the lower and upper
chains of an old convex set H; an unduplicated point has both indicators
zero. For endpoints, the lower and upper intervals are disjoint. Other
vertices belong to only one of the two chains.

For an old convex H of size at least three, the convex hull of all its
clusters has exactly

    M(H) = |H| + (r−1) * sum_p ell_H(p) + sum_p u_H(p)                 (1)

vertices, and the projection of its lower chain is exactly the old lower
chain of H. An exposed lower cup cluster contributes all r points. An
exposed upper cluster contributes its two end points: its internal third
point, when present, is below their chord. An unexposed cluster contributes
one vertex. The interval tests are exactly the adjacent slope tests for
these insertions. Genericity makes each comparison strict, so small
perturbations cannot change these conclusions.

**Upper bound for arbitrary convex subsets.** Let Q' be any convex polygon
chosen from the clusters, with projection exactly this H. It need not be
the full cluster hull. For a non-endpoint p of H, the signs with the two
extreme fibers fix every selected clone's lower/upper assignment to that
of p. The projected neighbors on that chain are the old chain neighbors.
If at least two clones of p are selected, the adjacent slope tests force
the corresponding visibility interval above. Thus an invisible lower or
upper fiber contributes at most one point; a visible lower fiber contributes
at most r; and a visible upper fiber contributes at most two, since three
clones in one fiber form a cup and cannot lie on a cap.

The endpoint count is a **total across both chains**, not a separate bound
to be added twice. At the left endpoint p, the leftmost selected clone is
shared by the upper and lower chains. An additional lower clone requires
t_p below the outgoing lower secant; an additional upper clone requires
t_p above the outgoing upper secant. The latter secant is strictly larger
than the former. These requirements are incompatible. Consequently all
additional endpoint clones, if any, lie on just one chain. Their total
contribution, including the shared extreme point, is at most r in the
lower-visible case, at most two in the upper-visible case, and at most one
otherwise. The right endpoint has the mirrored inequalities and the same
total bound. These arguments apply to any selected clones, even if other
clones of the endpoint fiber were omitted.

Every fiber therefore contributes at most
1+(r−1)*ell_H(p)+u_H(p), and summing gives **|Q'| <= M(H)**. This per-fiber
argument is essential: the size of a full convex hull is not, in general,
an upper bound on the size of its convex subsets.

For an old cap K, the maximum cap length using every fiber of K is

    |K| + sum_p v_K(p),                                             (2)

where v_K is cap visibility. A cup fiber contributes at most two points to
a cap. The upper bound follows from the adjacent slope tests; choosing
the two extreme clones at visible fibers attains it.

Every new cap projects to an old cap. Every new convex polygon projects to
an old convex set: an original point strictly inside a triangle of three
other original points remains inside the triangle of any sufficiently
close representatives. Consequently, it cannot occur in a new polygon
containing those fibers. The fixed original general-position set makes
this stability uniform over all the finitely many subsets.

The source has no five-cap and no hexagon. Thus no new five-cap is equivalent
in this model to:

- no visible duplication on any original four-cap;
- at most one visible duplication on any original three-cap.

Projections of size two cannot give a five-cap, because each cup cluster
contributes at most two points. Similarly, no new N-gon is equivalent to

    M(H) <= N−1 for every old convex H with 3 <= |H| <= 5.            (3)

Projections of size at most two contain at most 2r points, which is less
than N−1 for both models. No omitted projection size can supply a target
polygon or violate (3).

### Coverage includes smaller carriers

For each old target chain C, require some original convex H, 3<=|H|<=5,
whose lower chain is a subset of C, and for which M(H)>=N−1. Under (3),
this means equality. Its full cluster hull is the required new target
polygon. Conversely, any target polygon permitted by Lemma 1's coverage
condition projects to such an H. Its lower-chain projection is the old
lower chain of H by the same fixed chain assignments. The per-fiber bound
just proved gives N−1 <= M(H), and (3) then gives equality. This converse
uses the bound for arbitrary convex subsets, not full-hull size alone.

This test permits a completely different carrier, including old triangles
and quadrilaterals. It does not merely try to inflate each original
pentagon. It also permits extra upper-chain vertices; lower-chain growth
is not required if a suitable larger carrier exists.

## 4. CNFs, soundness, and certified answers

`lift_cluster_cnf.py` creates one-hot choices of slope cell or singleton at
each point. Visibility variables are equivalent to the disjunction of the
corresponding cell choices. It adds the cap restrictions from (2) and the
polygon bounds (3).

For each H, an indicator Z_H implies M(H)>=N−1. For each old C there is one
clause OR{Z_H: lower(H) subset C}. The implication is deliberately one-way:
a geometric lift assigns true to each adequate H, while any satisfying
assignment's true Z_H is sufficient for coverage.

Weighted cardinalities use repeated literals: an r=3 lower visibility
indicator occurs twice in (1). At-most-b is encoded by forbidding every
(b+1)-element submultiset of the list of literal occurrences; at-least-b
uses the dual clauses. Collapsing duplicate literals within a clause does
not change its meaning. Every geometric lift in Section 3 therefore gives
a model of the CNF. **Its certified unsatisfiability excludes that family.**

| model | variables | clauses | LRAT bytes | checker output |
|---|---|---|---|---|
| N=7, singleton/binary clusters | 4,221 | 44,133 | 215,323 | `s VERIFIED UNSAT` |
| N=8, singleton/ternary thin cups | 4,221 | 68,386 | 133,436 | `s VERIFIED UNSAT` |

Both use 80 old four-caps, 211 old three-caps, all 103 lower targets, and
1,308 convex projection sets of sizes 3–5. CNF SHA-256 values:

    binary:  d3831f0ba65ff302008b6dca24f413616e372cfae68ed76b0bb36c752136bf8b
    ternary: d82e5e18cf66499c6bbd92f22461d509b062c3ba090ddd56789eecfa9e20d8bd

CaDiCaL was limited to five seconds per instance and finished immediately.
The checker invocations had ten-second external limits, 256 MB CakeML heap,
32 MB stack, and 512 MiB process address-space limits. Both finished well
inside those limits. Verdicts were read from the literal checker lines,
not inferred from exit codes. Plain and zstd LRAT files are retained.

## 5. Final validation and its limits

`lift_audit.py` is a separate audit driver. It uses the earlier independent
point-in-triangle geometry checker to recover the source caps and gons,
rather than the encoder's hull routine. It checks every saved carrier and
the rational linear contradiction.

For the encoder controls it imports the **formula under test**. It is not
a second independent CNF encoder, and byte-identical regeneration by itself
is not an independent encoding proof. The additional controls are:

- Both formulas accept an explicit real lift of the five parabola points
  (i,i^2), i=0,...,4, duplicating point 2 at tangent slope 4. The results
  are a six-cup and a seven-cup, respectively. Every CNF clause is checked
  under the assignment obtained from exact coordinates, with no SAT call.
- On the actual source, the all-singleton assignment violates precisely
  the 103 coverage clauses and satisfies every other clause.
- Two fixed coordinate configurations per target (all singletons and one
  predetermined mixed assignment) check formula (1) on every one of the
  1,308 projection sets: 5,232 hull-capacity comparisons. All lower-chain
  projections also agree. The two mixed configurations are controls, not
  valid lift candidates and not sampling evidence for nonexistence.
- Coordinates use epsilon=2^−256 and are scaled to integers. All triple
  determinants are nonzero; every choice of representatives of an old
  triple preserves its orientation. Visibility truth values are computed
  from these actual chain determinants.
- Both original CNFs regenerate byte-for-byte. The audit verifies that
  the saved cake outputs each contain exactly the required line; it does
  not claim a second LRAT replay by an independent verifier.

Result: `lift_audit.json`; about 0.72 seconds, 43,904 KiB maximum RSS.
All research and validation calls used one thread and bounded timeouts.
The new repository house rules were read when announced; the resource
helper reported five free threads before the final audit. No long job or
systemd unit was started.

## 6. Scope, files, and handoff

The exact-one/constant-weight route is refuted independently of the cluster
CNFs. The broader **generic binary** and **thin generic ternary cup** models
are excluded by the certified formulas and the written implication above.
Remaining possibilities include directions aligned with old secants, where
second-order positions decide otherwise unresolved signs; ternary clusters
with different first-order edge directions; different cluster sizes or
types; changes to the original order type; and other nonlocal constructions.
No feasibility or promise is asserted for those possibilities.

No additional search or long computation is proposed or pending. All new
paths are under `R/DELTA3N20261113/hypergraph/`:

- `LIFT.md`;
- `lift_probe.py`, `lift_probe.json`;
- `lift_cluster_cnf.py`;
- `lift_audit.py`, `lift_audit.json`;
- `lift_binary.cnf`, `.json`, `.lrat`, `.lrat.zst`, `.solver.out`, `.cake.out`;
- `lift_ternary.cnf`, `.json`, `.lrat`, `.lrat.zst`, `.solver.out`, `.cake.out`;
- `lift_SHA256SUMS`.

The last manifest hashes this delivered snapshot and excludes itself.
The earlier `SHA256SUMS` is deliberately preserved. No scratch file,
old research record, git branch, commit, or remote was changed by this task.

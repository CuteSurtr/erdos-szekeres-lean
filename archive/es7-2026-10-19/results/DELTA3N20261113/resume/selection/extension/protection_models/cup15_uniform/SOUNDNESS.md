# Fixed-coordinate membership and line certificates

The mathematical implications here are written arguments. Coordinate and
membership enumerations are COMPUTED; only the identified cup-membership
CNF with an accepted LRAT replay is CERTIFIED. No universal selector theorem
or counterexample to ordinary or uniform Delta existence is claimed.

Let the 15 points be indexed in increasing x-order. A selected set A is an
ordinary weak Delta when it contains no four-cap and meets every convex
six-subset. We check all four-caps and all six-subsets directly. A cap is
recognized by all its triple orientations being negative. The replay uses
decreasing consecutive secant slopes instead: weighted averages of those
slopes imply every nonconsecutive triple is negative. Convexity is checked
by a monotone hull in the finder and by supporting edges in the replay.
In general position a k-subset is convex exactly when it has k supporting
edges. Both independently reconstruct the entire target family.

For an ordered pair b<c, write its secant at X=M+t as
`q(t)=s*t+z`, where `M=max_x(U)` and `t>0`. Let L contain the secants of all
ambient four-cap terminal pairs. The uniform condition requires every cap
triple in A to have its terminal line below `max(L)` for all t>0.

For a candidate pair, exact intersection of all inequalities
`q(t)>ell(t)` gives either an empty interval or an open exposure interval.
Safe pairs retain a convex combination of at most two ambient lines whose
combined slope and height at M dominate q. Its value cannot exceed the
ambient upper envelope, so it proves safety on the full ray. All safe
pairs in these two realizations happen to admit a single-line certificate.
Each exposed pair retains the exact interval and a rational t strictly
inside it, with q above every ambient line there.

The replay does not call the interval finder. It tests q at zero and all
positive pairwise ambient-line intersections, then compares the final
slope with the largest ambient slope. This contains every upper-envelope
breakpoint. On each intervening segment the envelope minus q is affine;
its endpoint values and final slope therefore completely characterize
safety. It separately verifies all stored convex-combination certificates,
exposure witnesses, and interval bounds using exact rational arithmetic.

Three orientation-only protection predicates are inspected:

- Terminal protection: `(b,c)` itself ends an ambient four-cap.
- Cup protection: an ambient tail `(u,v)` is identical, or `u>=b`, `v>=c`
  and its distinct endpoint union with `(b,c)` is a cup.
- Forced protection: an ambient tail satisfies `v>=c`, with positive
  `chi(b,c,v)` when `v>c`, positive `chi(b,u,v)` when `u>b`, and negative
  `chi(u,b,c)` when `u<b`.

The independent forced check evaluates the exact line difference at all
ordered endpoints. Identical pairs are safe. Otherwise it requires a
nonnegative final value and a nonpositive earlier value, with one strict.
The affine difference then has positive slope and stays positive beyond
the final endpoint. These checks agree with the orientation predicate for
all 840 query/support combinations in each realization. The cup check is
independently repeated using consecutive increasing slopes. The existing
written endpoint and cup arguments are in
`../../envelope/cup_dominance/comparison/SOUNDNESS.md`.

For any of these predicates, let B be the cap triples whose terminal pair
is unprotected. With variable z_i meaning i belongs to A, the exact
membership formula consists of:

1. A positive clause over each convex six-subset, requiring a hit.
2. A negative clause over each four-cap, forbidding its selection.
3. A negative clause over each triple in B, forbidding that obstruction.

For uniform membership, B is the coordinate-dependent exposure family.
For cup membership it is the orientation-defined cup-unprotected family.
No auxiliary variables or extra constraints occur. Both reconstructions
give the parent's complete 211-clause cup multiset: 70 target clauses,
47 four-cap clauses and 94 cup-unprotected triple clauses, with multiplicity
preserved. The proof is replayed against the parent's exact clause order,
whose bytes match its certificate input, because LRAT references depend on
that order.

All 32,768 assignments are also enumerated independently. The finder tests
each clause family directly; the replay uses upward-closure transforms to
mark supersets of forbidden subsets and complements containing a target.
Equality is checked for every mask in every family, not just aggregate
counts. Positive uniform models are checked against the reconstructed
geometry, every relevant line certificate, and every uniform CNF clause.

The 26-member difference between the two uniform families establishes
dependence of the uniform family and its count on coordinates within this
orientation type. It does not exhibit a change of minimum size or an
existence reversal: both minima are four and both families are nonempty.

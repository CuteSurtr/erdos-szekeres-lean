# Verification scope: weak extreme-point continuation

**CONFIRMED by a separate exact implementation** at the finite scopes below.
This is not a second human review, a Lean proof, or a CERTIFIED SAT result.
The written universal statements are in theory.md and were not inferred from
the finite enumeration.

## Coordinate obstruction checks

`independent_check.py` imports no finder, encoder, or existing research code.
The finder uses monotone hulls and all-triple homogeneous caps; the audit uses
point-in-triangle tests on all four-subsets and consecutive cap turns. Every
point is tested for strict x-order and every triple for a nonzero determinant.
General position makes convexity equivalent to having no nonconvex four-subset.

Both retained source hashes and all source-index coordinate selections match.
The nine-point n=7 set has 9 four-caps, 9 hexagons, no five-cap, and no heptagon.
The ten-point n=8 set has 7 four-caps, 11 heptagons, no five-cap, and no octagon.
Minimum absolute determinants are respectively 19,308,240 and 21,135,254.

For each obstruction the audit checks the four-cap T, all four polygons B+t,
the old Delta A=T-r, and the full weak Delta {0}. It independently evaluates
all 16 possible C or C+r, C subset A, and saves a violating cap or missed
polygon for each. The size-minimality conclusion uses the separate written
bound |S|<=n+1, not a claim of exhaustive order-type enumeration.

The rational leftmost insertion is realized on both bases. The resulting
n=8 and n=9 configurations pass all coordinate predicates, including new
general position, no five-cap, no forbidden polygon, and all four enlarged
private/missed polygons. Their integer-scaled coordinates are retained.

## Threshold and exact-removal checks

On four valid configurations, every old weak Delta is enumerated. Exact
rational line heights agree with direct four-cap enumeration for every
actual red extension. The identical-terminal-pair condition implies envelope
domination, which implies a valid red extension. All blocking triples have
terminal rank three in the ambient deletion. Both sufficient implications
are strict on these controls.

For each old Delta every subset removal is independently tested directly
and against the blocker/support criterion: 22,892 comparisons, zero differences.
There are 863 old Deltas total. The checks include non-cup selected sets and
selected sets that miss a polygon's entire lower chain, preserving the weak
scope of the statements.

## Retained failures

The first synthetic-control audit stopped on collinearity of (0,0),(6,0),(8,0).
Those controls were rejected, recorded in failed_audit_01.json, and retained
in scratch with their original statistics. Moving the synthetic extreme point
to (8,1) gives valid controls; the finder now asserts general position too.
The final complete audit passes.

The proposed common-cup construction with (-1,-20) followed by
(0,0),(1,10),(2,18),(3,24) fails five-cap-freeness. The audit confirms that
five-cap and the failed attempt remains in findings.json.

## Limits

No theorem of unrestricted D(5,7) or D(5,8), no cup-side theorem, no solver
certificate, and no change to an ES bound follows. In particular the tests
do not show that some threshold-safe Delta exists on every valid deletion.
No hidden assumption from the parent's separate maximal-red-set work is used.
All files and retained scratch artifacts are covered by SHA256SUMS.

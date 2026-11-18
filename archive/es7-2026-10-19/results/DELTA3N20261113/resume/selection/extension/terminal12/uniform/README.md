# The twelve-point example still has uniform selections

**COMPUTED exact fixed-coordinate analysis:**848 uniform-envelope Deltas,
out of945 ordinary weak Deltas. The minimum size is4, with21 minimum
witnesses. All21 minimum ordinary witnesses are uniform. There are298
cup-support selections and848 endpoint-sign selections in these exact
coordinates. Terminal-safe selections remain absent.

A particularly simple positive witness is A={0,2,3,6}, using the local
indices in the parent record. Exact enumeration checks that it has no
four-cap and meets every convex pentagon. Its only cap triple is(2,3,6).
The ambient four-cap(5,7,8,10) supplies a dominating terminal line.
Writing l_ab for the line through points a,b, at X=1000+t one has

    l_8,10(X) - l_3,6(X) = (8084 t + 6854737) / 47061 > 0  (t>=0).

Thus this same A is safe over the whole rightward half-line. This explicit
certificate explains why failure of terminal membership does not imply
failure of uniform extension. The rational identity is separately checked
in [simple-certificate.json](simple-certificate.json).

The parent [fixed_uniform.py](../../fixed_uniform.py) reconstructs all
integer caps and polygons, builds the exact exposure intervals, and
independently checks pair safety at every ambient-line intersection,
at the right boundary, and at the eventual slope. Every safe pair's
one/two-line rational certificate and every exposed pair's rational
counterpoint are replayed. All4096 memberships are enumerated. Only two
cap triples are exposed in this realization.

[result.json](result.json) pins inputs, sources and the complete CNF;
[exposure.json](exposure.json) retains the pair certificates;
[families.json](families.json) retains every ordinary/uniform membership;
[protection-counts.json](protection-counts.json) gives the separate
orientation-predicate counts. This is a parent computation with an
independent arithmetic formulation, not a new independent-worker audit
or a universal existence theorem. No LP or solver status is used.

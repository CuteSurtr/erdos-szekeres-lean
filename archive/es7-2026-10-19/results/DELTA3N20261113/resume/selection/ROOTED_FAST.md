# Specialized rooted formula — written soundness

**Written soundness independently reviewed; exact controls COMPUTED.** Both
m16 real controls and 2,907 small auxiliary-projection queries passed the
separate audit. This is an alternative encoding of the same rooted statement,
with the audited compact geometric base included unchanged. Its completed
searches ended UNKNOWN and supply no new certificate.

Let r be the rightmost point and U=S−r. A rooted Delta is A∪{r}, A⊂U.
It is four-cap-free exactly when A contains neither an old four-cap nor an
old three-set which together with r is a four-cap. For a<b<c<r the latter
condition is the two negative consecutive signs abc and bcr. The signotope
axioms make these equivalent to all four signs of that cap being negative.

`root_bad_contains(A)` is a one-way witness of one of these forbidden
subsets. At size three it implies those two negative signs. At size four it
implies either an old-four-cap witness (the two consecutive negative signs)
or a bad size-three child, using all four deletions. At larger sizes it
implies one of five one-vertex-deletion children. Every forbidden set has
size at most four, so avoids one of those five vertices. Descending yields
an actual forbidden subset; assigning flags to actual forbidden containment
gives a canonical assignment in the converse direction. Four-cap witnesses
do not have reverse implications, which are unnecessary for this projection.

Targets containing r are already hit. Only old (n−1)-gons need hit clauses.
Their containment flags alias exact compact Q flags at size n−1; at larger
sizes they imply one of n deletion children. The children cover every
(n−1)-subset, so the same descent/canonical proof applies.

The reduced size interval from ROOTED.md becomes 2≤|A|≤m−n+1. For each such
A, a clause requires forbidden containment in A or a target in U−A. Missing
small-size flags are literal false constants. This is precisely failure of
every rooted Delta in the interval. The root-preserving growth/shrink
argument covers all other sizes. No symmetry, cube, coordinates, or fixed
orientation are imposed. Thus certified UNSAT of
this formula establishes the same finite rooted theorem as the filtered
formula. SAT still requires independent semantic checks and, for a real
counterexample, exact realization.

## Completed searches

Both longer trials ended **COMPUTED UNKNOWN**: n7/m14 and n8/m15, each
after 300 seconds. The initial n7/m14 ten-second probe also ended UNKNOWN.
No universal conclusion is inferred from these attempts. Large traces
(1,388,682,091 and 1,317,520,169 bytes) are retained, with roundtrip-checked
zstd copies and hashes in `data/fast14-7/solve/result.json` and
`data/fast15-8/solve/result.json`.

The n7/m14 specialized formula has 18,174 variables, 71,370 clauses and
241,085 literals. It substantially reduces the auxiliary lattice while
preserving the geometric base. Neither that reduction nor a favorable
runtime estimate constitutes evidence for the mathematical statement.
Source/controls review is recorded separately in
`audit/VERIFY_ROOTED_FAST.md`. The accepted finite certificates in ROOTED.md
use the earlier filtered formula, so none depends on this alternative
implementation or its UNKNOWN results.

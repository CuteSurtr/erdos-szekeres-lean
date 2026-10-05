# Suk's real-point upper bound: dependency ledger

Completed result: Theorem 1.1 of [Suk, arXiv:1604.08657v2](https://arxiv.org/pdf/1604.08657v2).
`Suk.theorem2016 : Suk.Theorem2016` proves the eventual upper bound with
coefficient 6 and the paper's floor convention for arbitrary real point sets
in general position. The full build and current 201-theorem axiom audit pass; only
`propext`, `Classical.choice`, and `Quot.sound` occur. There are no proof
placeholders or additional axioms.

## Checked prerequisites

- `Suk/FourPoint.lean`: convex independence follows from checking subsets of size
  at most four, using Mathlib's Carathéodory theorem. For a set with at least four
  elements, testing exactly four suffices. This is the substance of Lemma 2.1.
- `Suk/CupsCaps.lean`: geometric cups-caps upper bound and the classical binomial
  bound for arbitrary real point sets. A linear equivalence connects the vendored
  pair-coordinate geometry to our `Fin 2 → ℝ` definitions. The lower-bound equality
  in Theorem 2.2 is not needed for the upper-bound argument and is not claimed.
- `Suk/ChainAntichain.lean`: if |S| > (a−1)(b−1), then S has a chain of at least a
  elements or an antichain of at least b elements. Derived from the adapted
  Dilworth theorem for any finite subset of a partial order.
- `Suk/TriangleOrder.lean`: a partial order on points above a normalized base
  segment, equivalent to triangle containment. Incomparable pairs put the base
  endpoints strictly on the same side of their line; no point of the base
  segment is collinear with the pair.
- `Suk/BaseChart.lean` and `Suk/BaseOrder.lean`: concrete affine normalization
  for every nondegenerate base; the triangle order, antichain/base
  nonintersection, and chain/base intersection for arbitrary base segments.
- `Suk/TransitiveColoring.lean`: the upper-bound direction of Theorem 2.3 for
  abstract transitive two-colorings, with actual distinct-vertex cliques. The
  consecutive-path to clique bridge is proved separately from Baek's path theorem.
- `Suk/ChainColoring.lean`: proves both colors transitive for the actual
  orientation coloring along a triangle-order chain, then extracts cliques.
  `BaseOrientation.lean` transports this to every base segment.
- `Suk/SupportingLines.lean`: strict support lines imply convex independence;
  positively oriented quadruples are in convex position.
- `Suk/TriangleMembership.lean`: barycentric/halfplane membership equivalence,
  including both triangle orientations, and the separated-pair quadrilateral test.
- `Suk/Quadrilateral.lean`: all sixteen triple-sign assignments are checked in
  Lean to characterize convex quadrilaterals. Moving the fourth point inside
  the same open cell of the other three pair-lines preserves convex position.
  This proves the local replacement step used in gluing.
- `Suk/OrientationClique.lean`: orientation cliques form actual convex polygons;
  an anchor on the appropriate side of every pair-line can be included.
- `Suk/SpikeGeometry.lean`: a support spike is defined by three strict
  halfplanes of four clockwise anchors. Determinant identities prove its other
  orientation signs and show that the outer-base triangle order implies the
  middle-edge triangle order.
- `Suk/ChainCaps.lean`: the chain cups-caps bound produces geometric caps using
  Suk's middle-edge anchors, although the input order uses the outer base.
  This extraction currently requires both target cap sizes to be at least three.
- `Suk/AdjacentSpikes.lean`: ordered pairs leave the entire neighboring spike
  on one weak side, proved in both directions from the five anchors.
- `Suk/GlueOrientation.lean` and `Suk/AdjacentCaps.lean`: facing caps from two
  adjacent chains have a convex union when their total size is at least four.
  General position is assumed for the selected vertices and shared anchor.
  Cross-region separation is derived, not assumed. This is the geometric
  content of Suk's Observation 3.1 in that size range.
- `Suk/ChainEnumeration.lean` and `Suk/SpikeChain.lean`: finite chains in the
  actual outer-base order admit strictly increasing enumerations, with exactly
  the same vertices and cardinality. Adjacent spike point sets are disjoint;
  gluing caps whose sizes sum to at least n gives an actual n-gon in P.
- `Suk/CapGrowth.lean`, `Suk/ChainCase.lean`, and `Suk/SupportSequence.lean`:
  the finite geometric chain case. For n ≥ 4 and K ≥ 3, r consecutive support
  spikes, each containing a chain of more than 2^(n+K−4) points, force a convex
  n-gon whenever n ≤ rK. A clockwise sequence of r+3 anchors supplies all local
  frames and their adjacency. General position and membership in P are explicit.
  The induction requests sizes min(n,c+K) and max(3,n−c); their sum is at most
  n+K, so it handles the terminal step without a cap of size one or two.
  This is a formalized component of Suk's proof, not a new asymptotic bound.
- `Suk/SpikeSeparation.lean`: the global support sequence implies that a line
  through an incomparable pair in one spike misses every nonadjacent spike.
  More precisely, every point of those other spikes lies on the same strict
  side as the first outer-base endpoint. The proof works on either side of the
  selected index; it also proves nonadjacent spikes disjoint.
- `Suk/PairSupports.lean` and `Suk/AntichainCaps.lean`: a local supporting edge
  at every selected antichain vertex extends to the entire union of nonadjacent
  parts. The resulting union is convex, its cardinality is the sum of the local
  cardinalities, and it gives an n-gon once that sum reaches n. The local support
  condition is explicit: for every p there is q in its own selected part, with
  p ≠ q, and every other local z lies on the same strict side of pq as the
  outer-base anchor. The extraction bridge below derives this condition.
- `Suk/HorizontalSpike.lean`: each support spike of a horizontal cap lies
  strictly between its two middle anchors in x-coordinate. Incomparable pairs
  have distinct x-coordinates, and their pair-lines put the outer anchor below
  the line when the pair is ordered from left to right.
- `Suk/CapSupports.lean` and `Suk/AntichainExtraction.lean`: negative cap triples
  give local supporting edges. Classical cups-caps extraction in an actual
  spike antichain either gives an n-gon immediately or a b-point cap with
  those supports. No local support condition is assumed by the extraction theorem.
- `Suk/AntichainCase.lean`: the finite geometric antichain case. Pairwise
  nonadjacent parts Q_i in a horizontal clockwise support sequence give an
  n-gon if each is a triangle-order antichain with
  |Q_i| > C(n+b−4,n−2), n ≥ 3, b ≥ 3, and the number of parts times b reaches n.
- `Suk/SpikeDichotomy.lean` and `Suk/FiniteSupport.lean`: both cases are now
  assembled. Given n ≥ 4, K,b ≥ 3, n ≤ rK, n ≤ tb, and t(r+1) ≤ k, a horizontal
  clockwise sequence of k+3 anchors in a general-position ambient set P forces
  an n-gon whenever each of its k interior spikes contains more than
  2^(n+K−4) C(n+b−4,n−2) points of P. Dilworth supplies the geometric chains
  and antichains; region selection chooses the applicable case. The statement
  assumes the populated support configuration, not an n-gon or a gluing result.
- `Suk/RegionSelection.lean`: if k ≥ t(r+1), either r consecutive indices have
  a chosen property, or there are t pairwise nonadjacent indices without it.
- `Suk/ExtractionCounting.lean`: double counting gives an unconditional density
  bound for convex subsets using the classical theorem. In particular,
  C(N,k) ≤ (# convex k-subsets) C(4^k,k) when N ≥ 4^k and k ≥ 3.
- `Suk/MonochromaticCounting.lean`, `Suk/HorizontalCounting.lean`, and
  `Suk/OrderedCounting.lean`: the same double count supplies genuine cups and
  caps of an x-ordered point set. Increasing enumeration preserves the exact
  number of subsets, connecting this count to finite families of point sequences.
- `Suk/AlternatingAnchors.lean` and `Suk/SupportFiber.lean`: the odd interior
  vertices of a cap lie in support spikes of its even anchors. A fixed anchor
  sequence supports at most N³ times the product of the interior spike sizes;
  the N³ factor accounts for three endpoint vertices. Anchor sequences are
  counted conservatively by N to the number of anchors.
- `Suk/ProductSelection.lean`, `Suk/SupportCoarsening.lean`, and
  `Suk/DenseCapExtraction.lean`: a large product forces sufficiently many rich
  regions. Selecting fewer anchors preserves the required spike inclusions.
  From a sufficiently dense cap family, the proof extracts k populated interior
  support regions and k+3 anchors, without an assumed partition theorem.
- `Suk/Reflection.lean` and `Suk/CoordinateNormalization.lean`: reflection
  exchanges cups and caps while preserving x-order; rotation gives distinct
  x-coordinates. Invertible linear maps preserve actual convex n-gons.
- `Suk/FiniteDensityBound.lean` and `Suk/FiniteBound.lean`: the complete finite
  proof for arbitrary real point sets in general position. The assumptions are
  integer inequalities, not a supplied geometric support configuration.
- `Suk/ExtractionEstimates.lean`, `Suk/ExponentialBound.lean`, and
  `Suk/IntegerParameters.lean`: integer estimates yield the bound below. The
  coarse extraction loss is 64(k+5) in the exponent. This is a horizontal
  cup/cap variant of the Pór–Valtr argument; the literal 32k constant in Suk's
  Theorem 2.4 has not been formalized.
- `Suk/Asymptotic.lean`: takes a=ceil(n^(1/3)) and H=ceil(log₂(n+a²)),
  bounds the integer exponent by n+6 n^(2/3) log₂(n), transfers the power bound
  through natural floor, and proves that the necessary cutoffs hold eventually.
  The final `theorem2016` has no hypotheses.
- `OrientationGeometry.lean`: determinants versus collinearity; exact rational
  general position transfers to real geometry.

The cups-caps and Dilworth prerequisites reuse attributed CC0 source. See
`THIRD_PARTY.md`; this work does not claim their proofs as original research.

## Checked finite bound and asymptotic assembly

`cubic_log_bound` proves that, for n ≥ 4, a ≥ 2, and n ≤ a³,

```text
2 ^ (n + a² + a² ceil(log₂(n+a²)) + 64(a(a+1)+5))
```

points in general position suffice for a convex n-gon. The integer logarithm
is Lean's `Nat.clog 2 (n+a²)`. This statement has no unproved geometric premises.
The proof uses k=a(a+1), r=t=a, K=b=a², and an alternating cap of 4k+14 vertices.
The counting and coarsening approach is based on
[Pór–Valtr (2002), §2](https://link.springer.com/content/pdf/10.1007/s00454-002-2894-1.pdf),
with endpoint losses and horizontal symmetry checked explicitly.

The final comparison is checked in `integer_parameters_fit_exponent` whenever
n ≥ 4, n^(1/3) ≥ 4, and log₂(n) ≥ 100. With a=ceil(n^(1/3)), the proof uses
a² ≤ 2 n^(2/3), a² ≤ n, H ≤ log₂(n)+2, and a(a+1)+5 ≤ 3a². These estimates
absorb the coarse extraction constant within Suk's coefficient 6. The
`coefficient_six_bound` theorem handles the exact natural floor, and divergence
of the cube root and logarithm gives the eventual statement `theorem2016`.

This completes Suk's upper-bound result, not every intermediate statement in
his paper with its original constants. The final HMPT 2020 upper bound is also
proved for ordinary real point sets; see [HMPT.md](HMPT.md). A strict
improvement remains unproved. The [paper mapping](PAPER_MAP.md) records the
precise scope of both formalizations; [VALIDATION.md](VALIDATION.md) links the
current axiom output. Research is stopped at the user's request. The numerical
experiments in `COUNTING.md` are separate from these completed proofs.

## Recent computational evidence

The 32-point heptagon-avoiding CNF is satisfiable. Its model is not automatically
a realizable point set. Joint Boolean/linear-arithmetic searches found and exactly
verified 8-point pentagon-avoiding and 16-point hexagon-avoiding configurations.
Five-minute uniform-x-grid searches for 32 and 33 points returned UNKNOWN, not
UNSAT. The first unrestricted 33-point SAT run ended UNKNOWN after 30 minutes. The two
additional SAT-focused and UNSAT-focused runs also ended UNKNOWN at 30 minutes.
A 20-round integer-mutation campaign found 21 orientation signatures and no
33-point extension. A verified 33-point configuration with exactly one convex
heptagon reproduces a known benchmark. All seven fixed-coordinate single-vertex
repairs returned UNSAT. These experiments do not replace the missing geometric
proofs or exclude coordinated point moves. A subsequent fixed-x search ruled
out all 21 two-vertex vertical repairs within the unique heptagon; moving all
seven y coordinates together ended UNKNOWN after 300 seconds.

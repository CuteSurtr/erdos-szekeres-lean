# Full Suk formalization: dependency ledger

Target: Theorem 1.1 of [Suk, arXiv:1604.08657v2](https://arxiv.org/pdf/1604.08657).
`Suk.Theorem2016` defines the eventual upper bound with coefficient 6 and the
paper's floor convention. **It is not yet proved.** No missing dependency is
represented by an axiom, `sorry`, or a theorem whose name disguises assumptions.

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
  for every nondegenerate base; the triangle order and the antichain/base
  nonintersection property for arbitrary base segments.
- `Suk/TransitiveColoring.lean`: the upper-bound direction of Theorem 2.3 for
  abstract transitive two-colorings, with actual distinct-vertex cliques. The
  consecutive-path to clique bridge is proved separately from Baek's path theorem.
- `Suk/RegionSelection.lean`: if k ≥ t(r+1), either r consecutive indices have
  a chosen property, or there are t pairwise nonadjacent indices without it.
- `Suk/ExtractionCounting.lean`: double counting gives an unconditional density
  bound for convex subsets using the classical theorem. In particular,
  C(N,k) ≤ (# convex k-subsets) C(4^k,k) when N ≥ 4^k and k ≥ 3.
- `OrientationGeometry.lean`: determinants versus collinearity; exact rational
  general position transfers to real geometry.

The cups-caps and Dilworth prerequisites reuse attributed CC0 source. See
`THIRD_PARTY.md`; this work does not claim their proofs as original research.

## Required work still outstanding

1. Positive-fraction extraction with explicit exponential constants (Theorem 2.4),
   especially alternating-anchor selection and support-region geometry. The
   initial convex-subset counting step is proved; the geometric extraction is not.
   Source: [Pór–Valtr (2002)](https://link.springer.com/content/pdf/10.1007/s00454-002-2894-1.pdf).
2. The remaining chain separation and cross-region geometry. The base order and
   antichain/base nonintersection are proved, but this does not yet establish the
   needed relations between different support regions.
3. The nonadjacent antichain case: compatible union of the extracted caps.
4. The adjacent chain case: orientation transitivity for the actual chain coloring,
   Observation 3.1, and the iterative growth argument.
5. Integer ceilings, floors and all eventual numerical inequalities; assemble the
   unconditional geometric conclusion `Suk.Theorem2016`.

The numerical HMPT experiments in `COUNTING.md` do not discharge these geometric
obligations. Full Suk is the primary milestone; a claimed new bound must also be
compared against HMPT v3 and more recent literature, not only the 2016 exponent.

## Recent computational evidence

The 32-point heptagon-avoiding CNF is satisfiable. Its model is not automatically
a realizable point set. Joint Boolean/linear-arithmetic searches found and exactly
verified 8-point pentagon-avoiding and 16-point hexagon-avoiding configurations.
Five-minute uniform-x-grid searches for 32 and 33 points returned UNKNOWN, not
UNSAT. The first unrestricted 33-point SAT run ended UNKNOWN after 30 minutes. Two
additional runs use SAT-focused and UNSAT-focused solver configurations. A separate
mutation campaign explores realizable 32-point configurations and full-plane
extensions; these experiments do not replace the missing geometric proofs.

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
- `OrientationGeometry.lean`: determinants versus collinearity; exact rational
  general position transfers to real geometry.

The cups-caps and Dilworth prerequisites reuse attributed CC0 source. See
`THIRD_PARTY.md`; this work does not claim their proofs as original research.

## Required work still outstanding

1. Combinatorial transitive-coloring formulation of cups-caps, or a fully proved
   geometric substitute for its use on the ordered chains in Section 3.
2. Positive-fraction extraction with explicit exponential constants (Theorem 2.4),
   including geometric definitions of support regions and consecutive-region
   selection. Its source is the proof of Theorem 4 in
   [Pór–Valtr (2002)](https://link.springer.com/content/pdf/10.1007/s00454-002-2894-1.pdf).
3. Transport the normalized triangle order to each support segment, and prove
   the remaining chain and antichain separation properties across regions.
4. The nonadjacent antichain case: cups-caps extraction and compatible union.
5. The adjacent chain case: Observation 3.1 and the iterative growth argument.
6. Integer ceilings, floors and all eventual numerical inequalities; assemble the
   unconditional geometric conclusion `Suk.Theorem2016`.

The numerical HMPT experiments in `COUNTING.md` do not discharge these geometric
obligations. Full Suk is the primary milestone; a claimed new bound must also be
compared against HMPT v3 and more recent literature, not only the 2016 exponent.

## Recent computational evidence

The 32-point heptagon-avoiding CNF is satisfiable. Its model is not automatically
a realizable point set. Joint Boolean/linear-arithmetic searches found and exactly
verified 8-point pentagon-avoiding and 16-point hexagon-avoiding configurations.
Five-minute uniform-x-grid searches for 32 and 33 points returned UNKNOWN, not
UNSAT. The separate unrestricted 33-point SAT search has its own manifest and
continues independently of these restricted realization experiments.

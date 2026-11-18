# Written real-geometry connection; not part of the kernel-checked finite claim

The current main theorem is explicitly about the integer predicates in
`FiniteModel.lean`. The following steps describe how those predicates relate to
the intended real geometry and what a separate Lean bridge must still establish.
Existing repository lemmas are source references here, not imported dependencies
of the finite packet.

1. **Coordinate embedding and cardinality.** Turn each integer pair into a function
   `Fin 2 → ℤ` and apply `ErdosSzekeres.integerToReal`. The cast preserves determinant
   arithmetic and order. `IntegerCertificates.lean` provides `integerToReal_injective`
   and `orient_integerToReal`. Strict horizontal order makes the fifteen indexed
   points distinct; their real image consequently has cardinality fifteen.

2. **General position.** Every increasing triple has nonzero integer determinant.
   Alternation and cyclic invariance extend this to every triple of distinct
   indices. After casting, `generalPosition_iff_orient_ne_zero` in
   `OrientationGeometry.lean` identifies nonzero orientations with the repository's
   affine general-position definition. `OrientationObstructions.lean` also supplies
   the corresponding distinct-index argument for an `Omission.Configuration`.

3. **Caps.** For strictly increasing horizontal coordinates, negative consecutive
   orientation determinants mean strictly decreasing adjacent slopes. This implies
   every increasing triple has negative determinant. Conversely the all-triples
   condition includes consecutive triples. The repository's vendor convex-polygon
   development proves `isCap_orientationDet_neg`. Thus the finite five-cap exclusion
   corresponds to absence of an ordinary five-cap, once the index/list/cast adapters
   are formally connected. That connection was not compiled here.

4. **Four points and larger convex sets.** Our `quadConvex` body is precisely
   `QuadConvexSigns` evaluated on the signs of the four integer determinants.
   `OrientationConvexity.lean` proves `convexPosition_four_iff_signs` for nondegenerate
   real quadruples. `OrientationObstructions.lean` proves
   `convexPosition_image_of_increasing_quadruples`, and `Basic.lean` provides
   `ConvexPosition.mono`. These give the two directions between the all-four-point
   criterion and real convex position for the finite images in question. The
   underlying planar argument is that a nonvertex lies in a triangle of other
   points, producing a nonconvex quadruple. For the no-seven direction specifically,
   convex-position heredity already suffices: any real convex seven-set would have
   all quadruples convex and would contradict the finite seven-subsequence theorem.

5. **Terminal selection.** `terminalPair_iff` is already compiled: the finite test
   means that some earlier ordered pair forms an ambient four-cap ending in the
   specified pair. To interpret the final obstruction geometrically, map a selected
   subset of the real image back to its unique indices. The real terminal condition
   must imply `TerminalSafe`; hitting every real convex six-set must imply `HitsSix`.
   The second implication needs the positive direction of the four-point-to-convex-
   image theorem. The finite contradiction then applies. This transfer has not been
   compiled, so no full real terminal-selection counterexample is claimed here.

An alternative no-seven bridge can use integer point-in-triangle certificates:
`IntegerCertificates.lean` supplies `IntegerInterior.mem_triangle` and
`IntegerInterior.not_convexPosition`. Such witnesses are not needed by the current
finite orientation proof and were not added to this packet.

Read-only inspection found cached `.olean` files for `IntegerCertificates`,
`OrientationObstructions`, `OrientationGeometry`, and `Basic` under
`.lake/build/lib/lean/ErdosSzekeres/`. This removes one possible build obstacle,
but does not establish that their import closure fits the current resident budget.
No real-geometry import probe was run. A new resource allocation, if needed, must
be coordinated before probing; existing nominal/global/track caps stay unchanged.

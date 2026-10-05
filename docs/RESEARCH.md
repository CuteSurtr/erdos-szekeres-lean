# Research and library map

Initial assessment: 2026-10-04.

## Mathematical target and status

The [supplied UCSD page](https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/Convex.html)
states the conjectured threshold 2^(n−2)+1. Its prose definition of g(n) has a
typo: it should quantify over g(n) input points, rather than n input points.
The formal statement also explicitly restricts n ≥ 3, avoiding natural-number
subtraction edge cases. We formalize the upper-bound claim directly, without
defining a minimum that would first need an existence theorem.

The page's known-case list is dated. Szekeres and Peters established the
17-point/6-gon result computationally in
[Computer solution to the 17-point Erdős–Szekeres problem](https://www.cambridge.org/core/journals/anziam-journal/article/computer-solution-to-the-17point-erdosszekeres-problem/0EC7876789232266D60439A4C00D86D9).
The December 2025 preprint
[Notes on the 33-point Erdős–Szekeres problem](https://arxiv.org/abs/2512.24061)
identifies n = 7 as the first open case and reports SAT results on restricted
subfamilies, not a complete resolution. The 2026 paper
[The Erdős–Szekeres conjecture revisited](https://www.sciencedirect.com/science/article/pii/S0097316526000385)
also describes the general conjecture as open. Thus the first open computational
target is 33 points forcing a convex heptagon.

Formalization milestone: `Suk.theorem2016` now proves Suk's 2016 eventual
upper bound with coefficient 6, including the complete real geometry and
floor convention. See `SUK.md`. `HMPT.theorem2020` now also proves the final
HMPT coefficient 8√2/3, with arbitrary positive epsilon, for ordinary real
point sets. These reproduce known theorems; a strict improvement remains a
research goal.

On 2026-10-05, `HMPT.integer_product_bound` completed a finite product-method
bound for every n ≥ 4 and positive region count. This includes actual geometric
maxima, adjacent-cap and parity budgets, extraction, and a computable exponent.
The subsequent projective construction closes the one-scale general convex-subset
bridge and yields `HMPT.suk_bootstrap_bound`. The genuine convex-subset ratio,
its two-scale composition, the factorial-sensitive entropy bound, and the exact
natural-floor bridge are now checked. `HMPT.suk_entropy_two_scale_bound` supplies
a closed exponent. The subsequent rounded-parameter limits and exact normalized
budget argument complete the final eventual theorem. The dependency ledger and
precise scope are recorded in [`HMPT.md`](HMPT.md).

## Installed mathematical dependencies

Mathlib is the only direct Lake dependency. Its transitive packages are locked
in `lake-manifest.json`. The plane is `Fin 2 → ℝ`; no metric structure is needed
for the initial affine and convex statements.

| Component | Mathlib module / declarations | Role |
| --- | --- | --- |
| Finite subsets | `Data.Finset.Card`: `exists_subset_card_eq`, `card_eq_three` | Select exact-size configurations |
| General position | `LinearAlgebra.AffineSpace.FiniteDimensional`: `Collinear`, `affineIndependent_iff_not_collinear_set` | No three distinct points on a line |
| Convex position | `Analysis.Convex.Independent`: `ConvexIndependent`, `convexIndependent_set_iff_notMem_convexHull_diff` | Every selected point is a hull vertex |
| Hull reasoning | `Analysis.Convex.Hull`: `convexHull_subset_affineSpan` | Affine independence implies convex independence |
| Small witnesses, next phase | `Analysis.Convex.Caratheodory`: `convexHull_eq_union` | Reduce hull membership to affinely independent finite subsets |
| Subset enumeration, next phase | `Data.Finset.Powerset`: `powersetCard`, `card_powersetCard` | Finite exhaustive certificates |
| Determinants, next phase | `LinearAlgebra.Matrix.Determinant.Basic` | Relate signed area to standard linear algebra |
| Arithmetic proofs | `Tactic.Ring`, `Tactic.NormNum` | Kernel-checked algebra and exact constants |

The needed definitions are present. A search of the pinned Mathlib file paths
did not reveal a dedicated convex-polygon Erdős–Szekeres development; this is
not a claim that all relevant external formalizations have been exhausted.

## Existing Lean development worth reusing

[EmptyHexagonLean](https://github.com/bsubercaseaux/EmptyHexagonLean) was inspected
at commit `3073981d2aa5aa1e399b382e605c0ed12a0b69af`. Despite its name, it includes
ordinary convex polygons as well as empty polygons. Relevant files under `Lean/`:

- `Geo/Definitions/Point.lean`: determinant and general-position APIs.
- `Geo/Definitions/PtInTriangle.lean`: orientation versus hull membership.
- `Geo/Definitions/Structures.lean`: convexity via triangles.
- `Geo/Canonicalization/`: geometric justification of symmetry reductions.
- `Geo/Gon/Encoding.lean`, `Assn.lean`, `TheMainTheorem.lean`: ordinary-polygon SAT reduction.

Its `gon_theorem` assumes UNSAT of the generated CNF and derives a geometric
upper bound, but **the inspected revision also depends on `mathlibSorry`**, a
placeholder axiom. A subsequent `#print axioms` audit found it in
`LeanSAT.PropForm.toICnf_sat`; the geometric `symmetry_breaking` and
`CanonicalPoints.satisfies_gonEncoding` theorems have only the three standard
axioms. The placeholder cannot be imported into a fully verified result. Besides
checking an UNSAT certificate, the conversion lemmas must be repaired or replaced.
The inspected
project pins Lean 4.7.0 and LeanSAT v4.7.0, so it is a porting candidate rather
than a drop-in dependency for our 4.24 project. No upstream source has been
copied into our tracked files; check licensing and preserve attribution before
porting. A local ignored inspection clone is in `.cache/EmptyHexagonLean`.

The associated [ITP 2024 paper](https://www.cs.cmu.edu/~mheule/publications/ITP24.pdf)
explains the geometry-to-SAT proof architecture. Its central empty-hexagon result
concerns 30 points, which is distinct from the ordinary 17-point result.

## What brute force can establish

1. **Bounded coordinate search:** exactly inspect subsets of an integer grid.
   Failure to find a counterexample proves only the bounded statement. A candidate
   at or above the conjectured threshold must be checked against the real geometric
   definitions before it counts as a formal counterexample.
2. **Order-type search:** for N labeled points in general position, record the sign
   of each triple determinant. There are at most 2^(choose(N,3)) sign assignments.
   At N = 33 this is 2^5456, before imposing consistency or exploiting symmetry.
   Direct enumeration is not realistic.
3. **SAT with a sound reduction:** prove in Lean that every geometric counterexample
   produces a satisfying assignment. Then a verified UNSAT certificate excludes
   all geometric counterexamples for that N. Every symmetry restriction needs a
   coverage proof. UNSAT of selected subfamilies alone is insufficient.
4. **SAT models:** an abstract orientation assignment may not be realizable by
   real points. A SAT result is not automatically a geometric counterexample.
5. **Full conjecture:** a single certified counterexample disproves it. Finitely
   many successful values of n do not prove the universal statement; that needs
   an argument uniform in n, or a proved reduction to finitely many cases.

Rational witness search is mathematically well motivated: strict nonzero
determinant signs persist under sufficiently small perturbations, and rational
points are dense. Together with orientation invariance of convex position this
would let a real counterexample be represented rationally. Those continuity and
invariance bridges are **not yet proved in this repository**, and do not provide
a fixed grid bound.

## Next proof obligations

1. **Done:** `OrientationGeometry.lean` proves
   `orient a b c = 0 ↔ Collinear ℝ {a,b,c}`, including degenerate triples.
2. **Geometric bridges done:** exact triangle membership and the four-point
   Carathéodory reduction are proved. `IntegerCertificates.lean` now also checks
   integer interior and supporting-edge certificates against real convexity.
   A general rational convex-subset decision procedure remains unfinished.
3. Certify the four-point lower-bound witness and the universal five-point theorem.
4. Audit and port the ordinary-polygon SAT reduction and certificate-checking path.
5. Reproduce n = 5 and n = 6 before budgeting a 33-point search.

The current Python hull algorithm has independent small-instance tests, but no
Lean soundness theorem. The subsequent research checkpoint installed local
CaDiCaL and drat-trim, reproduced UNSAT for the 9-point pentagon and 17-point
hexagon CNFs with independently checked DRAT certificates, and launched the
unrestricted 33-point heptagon CNF. See the JSON manifests in `experiments/`
and `docs/COUNTING.md`. These computational results do not close the conversion
axiom gap described above.

## Frontier computational comparison (checked 2026-10-04)

[Georgiev–Gómez-Serrano–Tao–Wagner, arXiv:2511.02864v3, §6.38](https://arxiv.org/html/2511.02864v3#S6.SS38)
reports searches through k=8. They recovered configurations of 2^(k−2) points
with zero convex k-gons and configurations of 2^(k−2)+1 points with exactly one.
They explicitly report no improved lower bound on this problem. Thus a 33-point
configuration with one heptagon would be a reproduced benchmark, not a new result.
A useful next search objective is to reach that near-counterexample and try
coordinated point moves to eliminate the remaining polygon, with exact validation.

Our current search has two complementary representations: unrestricted abstract
orientation CNFs, whose SAT models still need realization; and realizable coordinate
mutations followed by full-plane single-point extension. Failed fixed-configuration
extensions do not exhaust the configuration space.

## Checked mixed-cap obstruction (2026-10-05)

The Suk and final HMPT upper bounds are fully proved for ordinary real point
sets. Research toward a stricter bound tested whether vertical and horizontal
cap sizes admit an additional unconditional additive budget. They do not under
the tested geometric hypotheses: a Lean-checked 22-point example has two
nonadjacent eight-point caps and all six support anchors, but its largest convex
subset has size 15. [`MIXED_CAPS.md`](MIXED_CAPS.md) records the exact statement
and proof. The example isolates a failed route; it does not improve the
published coefficient. The remaining research must establish additional
compatibility conditions or strengthen another part of the counting argument.

## September 2026 finite-bound preprint

[Michael Schroeder, *Erdős–Szekeres: Upper Bounds for Convex Heptagons and
Octagons*, version 1, 19 September 2026](https://doi.org/10.5281/zenodo.22842891)
claims ES(7) ≤ 81, ES(8) ≤ 319, and the sharp restricted ETV value
M₇(5,6)=25. Its [companion page](https://michaelschroeder.ai/research/ErdosSzekeres/companion)
discloses native-evaluation dependencies and no external peer review. These
finite thresholds do not improve the leading coefficient in HMPT's eventual
bound.

On 2026-10-05 we downloaded the release, matched its published archive SHA-256,
and verified all 322 manifest entries. We inspected the final real-plane
statements, the Mathlib convex-independence adapter, and selected cyclic-sign
and capacity proofs. The release's separate Python octagon checker passed
locally: 3,849 cyclic families, 23 block maps, and both complete omission trees,
including rejection controls. This is reproduction of the author's checker,
not a new independent implementation or a Lean rebuild.

The package pins Lean 4.32.0-rc1 and a different Mathlib revision. We have not
rebuilt its 208 proof modules or independently replayed its heptagon certificates.
Nothing from that proof package is imported into our Lean dependency graph.
The audit record and bounded row experiments are in
`experiments/schroeder-2026-10-05.json`.

`scripts/omission_row_probe.py` tests the published octagon row systems at one
additional allowed hole: 59 holes among 252 balanced states, or 30 among 154
residual states. Excluding either budget would sharpen the corresponding
finite occupancy bound by one. A successful exclusion would still need its
own certificate and the full geometric connection; a satisfying row assignment
need not be geometrically realizable. Thus neither solver output alone proves
a new ordinary-polygon theorem.

Both budgets were tested with seeds 0 and 1 for 180 seconds each. All four
attempts returned UNKNOWN. No satisfying hole assignment or exclusion was
obtained. To reproduce a bounded probe after extracting the verified archive:

```sh
.cache/solver-venv/bin/python scripts/omission_row_probe.py \
  .cache/schroeder-release/es7_es8_bounds_81_319_v1/certificates/balanced.json \
  --output fresh-balanced-probe.json --holes 59 --seconds 180 --seed 1
```

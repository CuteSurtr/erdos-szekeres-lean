# Mathematical explanation

**Current result: ES(8) ≤ 314. The next target, ES(8) ≤ 313, is not proved.**
This note explains the statements, the finite reduction, and what the latest
certificates establish. The [README](../README.md) is the theorem index;
[VALIDATION.md](VALIDATION.md) records the checks.

## 1. The original problem

Let ES(n) be the least integer N such that every set of at least N points in
the real plane, with no three points on a line, contains n points in convex
position. Convex position means that all n selected points are vertices of
their convex hull. Other points may lie inside the polygon.

The Erdős–Szekeres conjecture is

$$
\operatorname{ES}(n)=2^{n-2}+1 \qquad(n\geq3).
$$

The classical lower-bound construction explains why this proposed threshold
cannot be smaller. The difficult direction is the universal upper bound.
This is the claim on the [original problem page](https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/Convex.html).
For octagons, the conjectured value is **65**, since 2⁶ + 1 = 65.
Our proved threshold of 314 is a partial upper bound; it does not settle the
conjecture. The lower-bound construction is background here, not an additional
formalization claimed by this note.

## 2. What Suk and HMPT contribute

The repository proves the following ordinary real-point upper bounds. Write
log for log₂. Floors below are natural-number floors.

| Result | Sufficient number of points | Quantifiers |
| --- | --- | --- |
| Suk 2016 | ⌊2^(n + 6 n^(2/3) log n)⌋ | All sufficiently large n |
| HMPT 2020 specialization | ⌊2^(n + (8√2/3 + ε)√(n log n))⌋ | Every ε > 0, then all sufficiently large n |

Both make the exponent n plus a smaller-order error. They are asymptotic
statements: substituting n = 8 does not give a certified finite threshold
without also satisfying the eventual hypotheses.

The main Lean declarations are `ErdosSzekeres.Suk.theorem2016` in
[Suk/Asymptotic.lean](../ErdosSzekeres/Suk/Asymptotic.lean) and
`ErdosSzekeres.HMPT.theorem2020` in
[HMPT/Asymptotic.lean](../ErdosSzekeres/HMPT/Asymptotic.lean).
The [paper map](PAPER_MAP.md) identifies replacement arguments and scope
restrictions. In particular, the full HMPT pseudo-configuration and convex-body
extensions are not claimed. The finite octagon work does not improve HMPT's
asymptotic coefficient 8√2/3.

## 3. How real points become a finite counting problem

Assume that a general-position point set has no convex octagon. A proved
projective change of chart removes one distinguished point and arranges the
remaining points for a minimum-slope partition. The partition separates them
into two actual configurations, H and R:

- H has no seven-point cup, seven-point cap, or convex octagon.
- R has no six-point cap or convex octagon, and no junction consisting of an
  incoming six-point cup and an outgoing five-point cap at the same point.

A cup or cap is an x-ordered chain bending consistently upward or downward.
Its ranks record lengths of chains that actually occur. Rank growth assigns
distinct points distinct finite states. The balanced catalog has 252 states;
the residual catalog has 154. These states are combinatorial rank profiles,
not coordinates in a grid and not a list of possible point locations.

For the residual configuration let O be its occupied states and let
M = {0,…,153} ∖ O be its missing states, or **holes**. Injectivity gives

$$
|R|+|M|=154.
$$

Each proved geometric row consists of a support Sᵣ and a demand dᵣ, asserting

$$
|S_r\cap M|\geq d_r.
$$

Equivalently, with hᵢ = 1 for a missing state and hᵢ = 0 otherwise,
the row says ∑ᵢ∈Sᵣ hᵢ ≥ dᵣ. A demand-one row forbids all of its states
being occupied simultaneously. Every actual avoiding configuration satisfies
these inequalities. The converse is not asserted: an assignment satisfying
the rows need not come from real points.

The method and original catalogs are adapted from Michael Schroeder's pinned
version-1 archive; see [attribution](THIRD_PARTY.md). The geometric interfaces
are described in [OMISSION_GEOMETRY.md](OMISSION_GEOMETRY.md),
[OMISSION_PROJECTIVE.md](OMISSION_PROJECTIVE.md),
[OMISSION_PARTITION.md](OMISSION_PARTITION.md), and
[OMISSION_RESIDUAL.md](OMISSION_RESIDUAL.md). Historical status paragraphs in
those frozen proof notes precede the completed assembly.

## 4. Why the completed theorem gives 314

The finished arithmetic certificates prove at least 62 balanced holes and
at least 32 residual holes. Therefore

$$
|H|\leq252-62=190,\qquad |R|\leq154-32=122.
$$

Adding back the distinguished point, an avoiding set has at most

$$
190+122+1=313
$$

points. Hence every set of 314 points forces an octagon.
The closed theorem is `ErdosSzekeres.Omission.forces_convex_octagon_314` in
[FinalCover314B61FusedR31Fused.lean](../experiments/omission-global-assembly-2026-10-10/FinalCover314B61FusedR31Fused.lean).
Its explicit real-point form is `convex_octagon_of_card_ge_314` in the same
file. No unproved arithmetic or geometric premise remains in those theorems.

To obtain 313 by the current residual route, it would suffice to prove
|M| ≥ 33, giving |R| ≤ 121. The same assembly would then bound an avoiding
set by 190 + 121 + 1 = 312 points. An alternative is to lower the balanced
population from 190 to 189. Neither improvement is currently proved.

## 5. What happened in the three remaining cases

The old 2,469-row search branched on whether particular states were occupied.
Three conditional contexts remained unresolved. Continuing them found a
**32-hole assignment satisfying every old row**, in case 4:

```text
7,12,33,39,44,47,50,51,52,54,55,56,69,71,73,75,
76,77,78,90,97,99,101,109,115,117,118,119,124,127,132,133
```

Lean checks its cardinality, every one of the 2,469 inequalities, the case-4
branch assumptions, and occupation of state zero. In particular,
`OmissionResidual32Case4.no_universal_thirty_three_hole_bound` proves that these
old inequalities cannot imply a 33-hole minimum. See
[Witness.lean](../experiments/omission-residual32-case4-2026-10-10/Witness.lean).
Cases 2 and 7 have partial, integer-checked search records; they were not
closed. Closing them could not remove this case-4 witness.

This is an obstruction to the chosen finite relaxation, not a counterexample
to ES(8) ≤ 313. In fact, the new geometric theorem below proves that this
assignment cannot be realized by an actual avoiding residual configuration.

## 6. The new geometric progress

Take the thirteen states

$$
S=\{25,43,53,65,74,85,89,91,96,107,110,111,125\}.
$$

The new theorem proves |S ∩ M| ≥ 1 for every actual residual configuration
with the restrictions in Section 3. The old witness occupies all thirteen,
so this inequality is strictly stronger than the old row system.

The proof selects the alleged owners of these states in one real
configuration. Their chronological order, chain ranks, and orientation signs
must obey a common collection of constraints. These include rank growth,
orientation relations on four points, and exclusions of convex octagons.
The constraints imply a particular unsatisfiable Boolean formula.

The retained formula has **337 variables and 376 clauses**, with a
**258-step RUP/LRAT refutation**. A RUP step asserts a clause whose negation,
together with earlier clauses, causes a contradiction by unit propagation.
Lean checks both the refutation and the geometric justification of its
clauses. The solver is a discovery tool, not a trusted proof oracle.

The declarations `CoupledCoreSixth.hole_bound`, `strict_strengthening`, and
`countermodel_not_realizable` live under `ErdosSzekeres.Omission` in
[Geometry.lean](../experiments/omission-residual32-witness-coupled-2026-10-10/Geometry.lean).
The last theorem rules out the complement of the displayed missing-state list
as the occupied set of an actual configuration; it does not rule out every
32-hole assignment.

An additional search found **128 distinct new supports** for a previously
proved thirteen-owner template. Every resulting row is proved by
`ErdosSzekeres.Omission.CoupledFourthGlobalVariants.all_rows` in
[Root.lean](../experiments/omission-residual32-fourth-global-variants-2026-10-10/FourthGlobalProof/Root.lean).
The first three exclude the displayed witness. Distinct supports do not by
themselves mean logically independent inequalities. None is implied by a
single old row through the checked support-difference test; combinations of
old rows could still imply them. A generic version of the
Sixth template is also proved; its 29 further discovered supports add no
strength because individual old rows already imply them.

## 7. What is still missing for 313

The strengthened search catalog has 2,598 rows: the old 2,469, the new Sixth
core, and the 128 Fourth-template rows. The current bounded searches have
not established its required 33-hole minimum. A failed witness search or a
solver timeout is not a proof of infeasibility.

The exact ordered 129-row addition is bound to its geometric theorems by
`ErdosSzekeres.Omission.Residual32AddedRows.all_rows` in
[AddedRows.lean](../experiments/omission-residual32-added-rows-2026-10-10/AddedRows.lean).
Together with the unchanged old catalog's transfer, the present search rows
have their necessary geometric proofs. The best recorded 32-hole near-model
still violates original row 205, which requires a hole in
{24,31,34,40,61,68,73,100}.

To finish the residual route we need a complete exclusion of at most 32
holes, a Lean-checked arithmetic certificate, an exact match between its
literal rows and the already established geometric interfaces, and final composition with the
existing partition. If the strengthened relaxation has another 32-hole
witness, further necessary geometry or a different counting argument will be
required. There is no reliable completion-time or proof-size estimate.

One possible source of additional constraints is attainment: positive chain
ranks have actual incoming witnesses. Such a witness can lie outside a small
selected support, so requiring it inside a sampled thirteen-state subset
would be unsound. No such extra attainment constraint is claimed here.

All finished Lean conclusions use only `propext`, `Classical.choice`, and
`Quot.sound`; no `sorry`, custom axiom, or native-evaluation oracle is used.
Local audits and hosted CI are recorded separately in
[VALIDATION.md](VALIDATION.md). The 314 result remains the completed global
bound, with no claim that it is the best bound in the literature.

import D3Encoding.Geometry

/-!
# The remaining target for a verified D3 exclusion

`dimacsSatisfiable_of_labelled` covers configurations that are already in the labelling
normal form of `results/E` (centre in general position, representatives sorted by angle in
the sector). What is not proved here is that every D3-symmetric 33-point set can be put in
that form. `results/E` argues it informally: the only D3 orbit type at 33 points in general
position is five 6-orbits and one 3-orbit; label orbit 0 as the 3-orbit and sort the
6-orbit representatives by angle; if the centre is collinear with two points of the set,
move each 6-orbit representative slightly (keeping the symmetry), which keeps all
orientations of the set and so keeps it heptagon-free.

The target is stated as a proposition and is not proved.
-/

open ErdosSzekeres

namespace D3

/-- `S` is invariant under the rotation by 120° about `c` and the reflection in the line
through `c` with unit direction `u`, i.e. under a dihedral group of order 6. -/
def D3Symmetric (S : Finset Point) : Prop :=
  ∃ c u : Point, u 0 ^ 2 + u 1 ^ 2 = 1 ∧ (∀ p ∈ S, rotC c p ∈ S) ∧ (∀ p ∈ S, reflC c u p ∈ S)

/-- **Open target.** Every heptagon-free D3-symmetric 33-point set in general position
yields a heptagon-free labelled configuration. -/
def D3LabellingTarget : Prop :=
  ∀ S : Finset Point, S.card = 33 → GeneralPosition S → D3Symmetric S →
    ¬HasConvexNGon 7 S → ∃ L : LabelledD3 11, ¬HasConvexNGon 7 L.pts

/-- The statement a verified D3 exclusion would give. -/
def D3Exclusion : Prop :=
  ∀ S : Finset Point, S.card = 33 → GeneralPosition S → D3Symmetric S → HasConvexNGon 7 S

/-- The target and the UNSAT fact for `d3cnf.py 33 7` give the exclusion. -/
theorem d3Exclusion_of_unsat (hT : D3LabellingTarget)
    (h : ¬ETV.DimacsSatisfiable (d3Cnf 33 7).2.2) : D3Exclusion := by
  intro S hcard hgp hsym
  by_contra hno
  obtain ⟨L, hL⟩ := hT S hcard hgp hsym hno
  exact hL (hasConvexNGon_of_unsat_d3 h L)

end D3

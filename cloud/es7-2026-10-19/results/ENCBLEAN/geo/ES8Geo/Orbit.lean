import ES8Geo.Capstone2
import ES8Geo.OrbitConsistency

/-! # M4: `orient` is invariant under `LayerLemma.rotAbout`

`OrbitConsistency` proves `orient_rotAbout_inv` for its own copy of `rotAbout` (OrbitConsistency.lean:93,117).
The two definitions are verbatim copies, so they agree by `rfl` (DESIGN.md §3.5, "Two further mismatches"); this
file restates the lemma for the `rotAbout` of `LayerLemma`, the one in `Sixfold66` and in `Invariant`. -/

namespace EncB.Geo
open ErdosSzekeres

theorem rotAbout_eq_orbitConsistency (c : Point) (θ : ℝ) :
    LayerLemma.rotAbout c θ = OrbitConsistency.rotAbout c θ := rfl

theorem orient_rotAbout_inv (c : Point) (θ : ℝ) (a b d : Point) :
    orient (LayerLemma.rotAbout c θ a) (LayerLemma.rotAbout c θ b) (LayerLemma.rotAbout c θ d) =
      orient a b d :=
  OrbitConsistency.orient_rotAbout_inv c θ a b d

end EncB.Geo

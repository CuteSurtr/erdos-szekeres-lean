import ErdosSzekeres.Suk.BaseOrder
import ErdosSzekeres.Suk.TransitiveColoring

namespace ErdosSzekeres.Suk

private theorem orient_identity₀ (a b c d : Point) :
    orient a b d * (b 1 - c 1) =
      orient a b c * (b 1 - d 1) + orient b c d * (a 1 - b 1) := by
  simp only [orient]
  ring

private theorem orient_identity₁ (a b c d : Point) :
    orient a c d * (b 1 - c 1) =
      orient a b c * (c 1 - d 1) + orient b c d * (a 1 - c 1) := by
  simp only [orient]
  ring

/-- For decreasing heights, positive adjacent triples force the two other
triples to be positive. This is a geometric transitivity proof, not a hypothesis. -/
theorem orient_positive_transitive (a b c d : Point)
    (hab : b 1 < a 1) (hbc : c 1 < b 1) (hcd : d 1 < c 1)
    (h₀ : 0 < orient a b c) (h₁ : 0 < orient b c d) :
    0 < orient a b d ∧ 0 < orient a c d := by
  have hden := sub_pos.mpr hbc
  constructor
  · apply pos_of_mul_pos_left (b := b 1 - c 1) ?_ hden.le
    rw [orient_identity₀]
    exact add_pos (mul_pos h₀ (sub_pos.mpr (hcd.trans hbc)))
      (mul_pos h₁ (sub_pos.mpr hab))
  · apply pos_of_mul_pos_left (b := b 1 - c 1) ?_ hden.le
    rw [orient_identity₁]
    exact add_pos (mul_pos h₀ (sub_pos.mpr hcd))
      (mul_pos h₁ (sub_pos.mpr (hbc.trans hab)))

theorem orient_nonpositive_transitive (a b c d : Point)
    (hab : b 1 < a 1) (hbc : c 1 < b 1) (hcd : d 1 < c 1)
    (h₀ : orient a b c ≤ 0) (h₁ : orient b c d ≤ 0) :
    orient a b d ≤ 0 ∧ orient a c d ≤ 0 := by
  have hden := sub_pos.mpr hbc
  have habd : orient a b d * (b 1 - c 1) ≤ 0 := by
    rw [orient_identity₀]
    exact add_nonpos (mul_nonpos_of_nonpos_of_nonneg h₀ (sub_pos.mpr (hcd.trans hbc)).le)
      (mul_nonpos_of_nonpos_of_nonneg h₁ (sub_pos.mpr hab).le)
  have hacd : orient a c d * (b 1 - c 1) ≤ 0 := by
    rw [orient_identity₁]
    exact add_nonpos (mul_nonpos_of_nonpos_of_nonneg h₀ (sub_pos.mpr hcd).le)
      (mul_nonpos_of_nonpos_of_nonneg h₁ (sub_pos.mpr (hbc.trans hab)).le)
  constructor
  · by_contra! h
    exact (mul_pos h hden).not_ge habd
  · by_contra! h
    exact (mul_pos h hden).not_ge hacd

theorem upperPoint_positive_transitive : TripleTransitive
    (fun p q r : UpperPoint => 0 < orient p.val q.val r.val) := by
  intro a b c d hab hbc hcd h₀ h₁
  exact orient_positive_transitive _ _ _ _
    (triangleOrder_height_strict a b hab) (triangleOrder_height_strict b c hbc)
    (triangleOrder_height_strict c d hcd) h₀ h₁

theorem upperPoint_nonpositive_transitive : TripleTransitive
    (fun p q r : UpperPoint => ¬ 0 < orient p.val q.val r.val) := by
  intro a b c d hab hbc hcd h₀ h₁
  simpa only [not_lt] using orient_nonpositive_transitive _ _ _ _
    (triangleOrder_height_strict a b hab) (triangleOrder_height_strict b c hbc)
    (triangleOrder_height_strict c d hcd) (le_of_not_gt h₀) (le_of_not_gt h₁)

/-- Every chain in the actual triangle order inherits a transitive orientation
coloring. The conclusion is an orientation clique; its interpretation as a
left-cap or right-cap relative to support anchors is a separate geometric step. -/
theorem chain_orientation_clique {ι : Type*} [LinearOrder ι]
    (p : ι → UpperPoint) (hp : StrictMono p) (s : Finset ι)
    (a b : ℕ) (hcard : (a + b).choose a < s.card) :
    HasTripleClique (fun i j k => 0 < orient (p i).val (p j).val (p k).val) (a + 2) s ∨
    HasTripleClique (fun i j k => ¬ 0 < orient (p i).val (p j).val (p k).val) (b + 2) s := by
  apply transitive_cups_caps _ ?_ ?_ a b s hcard
  · intro i j k l hij hjk hkl
    exact upperPoint_positive_transitive _ _ _ _ (hp hij) (hp hjk) (hp hkl)
  · intro i j k l hij hjk hkl
    exact upperPoint_nonpositive_transitive _ _ _ _ (hp hij) (hp hjk) (hp hkl)

end ErdosSzekeres.Suk

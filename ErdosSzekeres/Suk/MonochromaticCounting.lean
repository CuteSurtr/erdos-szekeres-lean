import ErdosSzekeres.Suk.ExtractionCounting
import ErdosSzekeres.Suk.TransitiveColoring

namespace ErdosSzekeres.Suk

noncomputable def cliqueSubsets {α : Type*} [LinearOrder α]
    (R : α → α → α → Prop) (s : Finset α) (k : ℕ) : Finset (Finset α) := by
  classical
  exact (s.powersetCard k).filter
    (fun t => ∀ a ∈ t, ∀ b ∈ t, ∀ c ∈ t, a < b → b < c → R a b c)

@[simp] theorem mem_cliqueSubsets {α : Type*} [LinearOrder α]
    {R : α → α → α → Prop} {s u : Finset α} {k : ℕ} :
    u ∈ cliqueSubsets R s k ↔ u ⊆ s ∧ u.card = k ∧
      ∀ a ∈ u, ∀ b ∈ u, ∀ c ∈ u, a < b → b < c → R a b c := by
  classical
  simp [cliqueSubsets, and_assoc]

/-- A division-free density estimate for monochromatic k-subsets of any
transitive two-coloring. It retains the two color classes separately. -/
theorem monochromatic_subsets_density {α : Type*} [LinearOrder α]
    (R : α → α → α → Prop) (hR : TripleTransitive R)
    (hnotR : TripleTransitive (fun a b c => ¬ R a b c))
    (s : Finset α) (k : ℕ) (hk : 3 ≤ k) (hs : 4 ^ k ≤ s.card) :
    s.card.choose k ≤
      ((cliqueSubsets R s k).card + (cliqueSubsets (fun a b c => ¬ R a b c) s k).card) *
        (4 ^ k).choose k := by
  classical
  let F := cliqueSubsets R s k ∪ cliqueSubsets (fun a b c => ¬ R a b c) s k
  have hF : ∀ u ∈ F, u ⊆ s ∧ u.card = k := by
    intro u hu
    rcases Finset.mem_union.mp hu with hu | hu
    all_goals exact ⟨(mem_cliqueSubsets.mp hu).1, (mem_cliqueSubsets.mp hu).2.1⟩
  have hcover : ∀ v ∈ s.powersetCard (4 ^ k), ∃ u ∈ F, u ⊆ v := by
    intro v hv
    obtain ⟨hvs, hvc⟩ := Finset.mem_powersetCard.mp hv
    have hbin : ((k - 2) + (k - 2)).choose (k - 2) < v.card := by
      calc
        _ < 2 ^ ((k - 2) + (k - 2)) := Nat.choose_lt_two_pow _ _ (by omega)
        _ ≤ 2 ^ (2 * k) := Nat.pow_le_pow_right (by decide) (by omega)
        _ = 4 ^ k := by rw [pow_mul]; norm_num
        _ = v.card := hvc.symm
    rcases transitive_cups_caps R hR hnotR (k - 2) (k - 2) v hbin with
      ⟨u, huv, huc, hc⟩ | ⟨u, huv, huc, hc⟩
    · refine ⟨u, Finset.mem_union_left _ ?_, huv⟩
      exact mem_cliqueSubsets.mpr ⟨huv.trans hvs, by omega, hc⟩
    · refine ⟨u, Finset.mem_union_right _ ?_, huv⟩
      exact mem_cliqueSubsets.mpr ⟨huv.trans hvs, by omega, hc⟩
  have hkpow : k ≤ 4 ^ k := (Nat.lt_pow_self (n := k) (a := 4) (by decide)).le
  exact (uniform_family_density s F k (4 ^ k) hkpow hs hF hcover).trans
    (Nat.mul_le_mul_right _ (Finset.card_union_le _ _))

end ErdosSzekeres.Suk

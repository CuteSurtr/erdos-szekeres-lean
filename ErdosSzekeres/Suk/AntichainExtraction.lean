import ErdosSzekeres.Suk.HorizontalSpike
import ErdosSzekeres.Suk.CapSupports
import ErdosSzekeres.Suk.CupsCaps

namespace ErdosSzekeres.Suk

/-- Cups-caps extraction in a geometric antichain. Either the n-gon is
already present, or a b-point cap has the exact local supporting edges
needed to glue nonadjacent antichain parts. -/
theorem CapFrame.antichain_cup_cap (F : CapFrame) (hx : F.Horizontal)
    {s : Finset Point} {n b : ℕ} (hn : 3 ≤ n) (hb : 3 ≤ b)
    (hgp : GeneralPosition s) (hspike : ∀ p ∈ s, p ∈ F.spike)
    (hanti : ∀ p ∈ s, ∀ q ∈ s, p ≠ q →
      q ∉ convexHull ℝ ({F.a, F.d, p} : Set Point))
    (hsize : (n + b - 4).choose (n - 2) < s.card) :
    HasConvexNGon n s ∨ ∃ t ⊆ s, t.card = b ∧
      ∀ p ∈ t, ∃ q ∈ t, p ≠ q ∧ ∀ z ∈ t, z ≠ p → z ≠ q →
        0 < orient p q F.a * orient p q z := by
  classical
  have hincomp (p : Point) (hp : p ∈ s) (q : Point) (hq : q ∈ s) (hpq : p ≠ q) :
      ¬ F.toOuter ⟨p, hspike p hp⟩ ≤ F.toOuter ⟨q, hspike q hq⟩ := by
    rw [AboveBase.le_iff]
    exact hanti p hp q hq hpq
  have hdist : HasDistinctX (s.image pointEquiv) := by
    intro p q hp hq hpq
    obtain ⟨p', hp', rfl⟩ := Finset.mem_image.mp hp
    obtain ⟨q', hq', rfl⟩ := Finset.mem_image.mp hq
    have hne : p' ≠ q' := fun he => hpq (congrArg pointEquiv he)
    exact F.incomparable_distinct_x hx ⟨p', hspike p' hp'⟩ ⟨q', hspike q' hq'⟩
      (hincomp p' hp' q' hq' hne) (hincomp q' hq' p' hp' hne.symm)
  rcases cups_caps n b hn hb hgp hdist (by omega) with ⟨cup, hc, hsub⟩ | ⟨cap, hc, hsub⟩
  · exact Or.inl (hasConvexNGon_of_pair (formsConvexPolygon_of_isCup _ cup n hn hc hsub))
  · right
    let p : Fin cap.length → Point := fun i => pointEquiv.symm (cap.get i)
    have hmono : StrictMono (fun i => p i 0) := by
      intro i j hij
      exact isXMonotone_get_lt cap hc.2.1 i.val j.val i.isLt j.isLt hij
    have hinj : Function.Injective p := by
      intro i j he
      exact hmono.injective (congrArg (fun x : Point => x 0) he)
    have hmem (i : Fin cap.length) : p i ∈ s := by
      obtain ⟨q, hq, he⟩ := Finset.mem_image.mp (hsub (cap.get i) (List.get_mem cap i))
      change pointEquiv.symm (cap.get i) ∈ s
      rw [← he, LinearEquiv.symm_apply_apply]
      exact hq
    have hanchor : ∀ i j, i < j → orient (p i) (p j) F.a < 0 := by
      intro i j hij
      have hne := hinj.ne hij.ne
      exact F.incomparable_anchor_negative hx ⟨p i, hspike _ (hmem i)⟩
        ⟨p j, hspike _ (hmem j)⟩ (hincomp _ (hmem i) _ (hmem j) hne)
        (hincomp _ (hmem j) _ (hmem i) hne.symm) (hmono hij)
    have hcap : ∀ i j k, i < j → j < k → orient (p i) (p j) (p k) < 0 := by
      intro i j k hij hjk
      exact isCap_orientationDet_neg cap b hc i.val j.val k.val i.isLt j.isLt k.isLt hij hjk
    refine ⟨Finset.univ.image p, ?_, ?_, ?_⟩
    · intro q hq
      obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hq
      exact hmem i
    · simpa [Finset.card_image_of_injective _ hinj] using hc.1
    · exact pair_supports_of_negative_cap p F.a (by have := hc.1; omega) hinj hanchor hcap

end ErdosSzekeres.Suk

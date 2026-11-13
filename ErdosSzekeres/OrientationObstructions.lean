import ErdosSzekeres.Suk.OrientationClique
import ErdosSzekeres.Omission.Realization

/-! Generic geometric semantics for finite no-octagon clauses. -/

namespace ErdosSzekeres

/-- Convexity of every increasing quadruple implies convexity of the whole
image. The index order need not agree with the horizontal coordinate order. -/
theorem convexPosition_image_of_increasing_quadruples {ι : Type*} [LinearOrder ι]
    (p : ι → Point) (hp : Function.Injective p) (s : Finset ι) (hs : 4 ≤ s.card)
    (h : ∀ i ∈ s, ∀ j ∈ s, ∀ k ∈ s, ∀ l ∈ s,
      i < j → j < k → k < l → ConvexPosition ({p i, p j, p k, p l} : Finset Point)) :
    ConvexPosition (s.image p) := by
  classical
  apply Suk.convexPosition_of_four_subsets
    (by simpa only [Finset.card_image_of_injective s hp] using hs)
  intro t hts ht
  obtain ⟨u, hus, hut⟩ := Finset.subset_image_iff.mp hts
  have hu : u.card = 4 := by simpa [← hut, Finset.card_image_of_injective u hp] using ht
  let e := u.orderEmbOfFin hu
  have hem (i : Fin 4) : e i ∈ s := hus (Finset.orderEmbOfFin_mem u hu i)
  have ht' : t = {p (e 0), p (e 1), p (e 2), p (e 3)} := by
    rw [← hut, ← Finset.image_orderEmbOfFin_univ u hu, Finset.image_image]
    have hf : (Finset.univ : Finset (Fin 4)) = {0, 1, 2, 3} := by decide
    rw [hf]
    simp [e]
  rw [ht']
  exact h _ (hem 0) _ (hem 1) _ (hem 2) _ (hem 3)
    (e.strictMono (by decide)) (e.strictMono (by decide)) (e.strictMono (by decide))

/-- Any eight distinct indexed points in an octagon-free ambient set contain
an increasing nonconvex quadruple. No general-position hypothesis is needed. -/
theorem exists_nonconvex_quadruple_of_no_octagon {ι : Type*} [LinearOrder ι]
    (p : ι → Point) (hp : Function.Injective p) (s : Finset ι) (hs : s.card = 8)
    (P : Finset Point) (hsub : s.image p ⊆ P) (havoid : ¬ HasConvexNGon 8 P) :
    ∃ i ∈ s, ∃ j ∈ s, ∃ k ∈ s, ∃ l ∈ s,
      i < j ∧ j < k ∧ k < l ∧ ¬ConvexPosition ({p i, p j, p k, p l} : Finset Point) := by
  classical
  by_contra! h
  apply havoid
  refine ⟨s.image p, hsub, ?_, ?_⟩
  · simpa only [Finset.card_image_of_injective s hp] using hs
  · apply convexPosition_image_of_increasing_quadruples p hp s (by omega)
    intro i hi j hj k hk l hl hij hjk hkl
    exact h i hi j hj k hk l hl hij hjk hkl

namespace Omission.Configuration

theorem point_injective {n : ℕ} (c : Omission.Configuration n) :
    Function.Injective c.point :=
  fun _ _ h => c.xOrder.injective (congrArg (fun p : Point => p 0) h)

/-- Ordered general position implies nonzero orientation in every index order. -/
theorem orient_ne_of_distinct {n : ℕ} (c : Omission.Configuration n)
    (u v w : Fin n) (huv : u ≠ v) (huw : u ≠ w) (hvw : v ≠ w) :
    orient (c.point u) (c.point v) (c.point w) ≠ 0 := by
  by_cases h₁ : u < v
  · by_cases h₂ : v < w
    · exact c.generalPosition u v w h₁ h₂
    · have hwv : w < v := by omega
      by_cases h₃ : u < w
      · have h := c.generalPosition u w v h₃ hwv
        rw [orient_swap (c.point u) (c.point v) (c.point w)] at h
        simpa only [neg_ne_zero] using h
      · have hwu : w < u := by omega
        have h := c.generalPosition w u v hwu h₁
        rwa [orient_cycle (c.point w) (c.point u) (c.point v)]
  · have hvu : v < u := by omega
    by_cases h₂ : u < w
    · have h := c.generalPosition v u w hvu h₂
      have he : orient (c.point v) (c.point u) (c.point w) =
          -orient (c.point u) (c.point v) (c.point w) := by simp only [orient]; ring
      simpa only [he, neg_ne_zero] using h
    · have hwu : w < u := by omega
      by_cases h₃ : v < w
      · have h := c.generalPosition v w u h₃ hwu
        simpa only [orient_cycle] using h
      · have hwv : w < v := by omega
        have h := c.generalPosition w v u hwv hvu
        have he : orient (c.point w) (c.point v) (c.point u) =
            -orient (c.point u) (c.point v) (c.point w) := by simp only [orient]; ring
        simpa only [he, neg_ne_zero] using h

end Omission.Configuration
end ErdosSzekeres

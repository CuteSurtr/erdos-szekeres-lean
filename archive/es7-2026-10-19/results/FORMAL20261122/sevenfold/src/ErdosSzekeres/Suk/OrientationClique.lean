import ErdosSzekeres.Suk.FourPoint
import ErdosSzekeres.Suk.SupportingLines
import Mathlib.Data.Finset.Sort

namespace ErdosSzekeres.Suk

/-- Four-point reduction turns an ordered orientation clique into a polygon.
This statement uses an arbitrary index order, not horizontal coordinates. -/
theorem convexPosition_of_positive_triples {ι : Type*} [LinearOrder ι]
    (p : ι → Point) (hp : Function.Injective p) (s : Finset ι) (hs : 4 ≤ s.card)
    (h : ∀ i ∈ s, ∀ j ∈ s, ∀ k ∈ s, i < j → j < k → 0 < orient (p i) (p j) (p k)) :
    ConvexPosition (s.image p) := by
  classical
  apply convexPosition_of_four_subsets
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
  apply convexPosition_four_of_positive
  · exact h _ (hem 0) _ (hem 1) _ (hem 2) (e.strictMono (by decide)) (e.strictMono (by decide))
  · exact h _ (hem 0) _ (hem 1) _ (hem 3) (e.strictMono (by decide)) (e.strictMono (by decide))
  · exact h _ (hem 0) _ (hem 2) _ (hem 3) (e.strictMono (by decide)) (e.strictMono (by decide))
  · exact h _ (hem 1) _ (hem 2) _ (hem 3) (e.strictMono (by decide)) (e.strictMono (by decide))

theorem convexPosition_of_negative_triples {ι : Type*} [LinearOrder ι]
    (p : ι → Point) (hp : Function.Injective p) (s : Finset ι) (hs : 4 ≤ s.card)
    (h : ∀ i ∈ s, ∀ j ∈ s, ∀ k ∈ s, i < j → j < k → orient (p i) (p j) (p k) < 0) :
    ConvexPosition (s.image p) := by
  apply convexPosition_of_positive_triples (ι := ιᵒᵈ) p hp s hs
  intro i hi j hj k hk hij hjk
  have hn := h k hk j hj i hi hjk hij
  have he : orient (p i) (p j) (p k) = -orient (p k) (p j) (p i) := by
    simp only [orient]
    ring
  rw [he]
  exact neg_pos.mpr hn

/-- A positive orientation clique remains convex after adding an anchor that
lies to the left of every ordered pair-line. -/
theorem convexPosition_insert_of_positive_triples {ι : Type*} [LinearOrder ι]
    (p : ι → Point) (hp : Function.Injective p) (s : Finset ι) (hs : 3 ≤ s.card)
    (a : Point) (ha : ∀ i, a ≠ p i)
    (h : ∀ i ∈ s, ∀ j ∈ s, ∀ k ∈ s, i < j → j < k → 0 < orient (p i) (p j) (p k))
    (hpair : ∀ i ∈ s, ∀ j ∈ s, i < j → 0 < orient (p i) (p j) a) :
    ConvexPosition (insert a (s.image p)) := by
  classical
  let q : WithTop ι → Point := WithTop.recTopCoe a p
  let t : Finset (WithTop ι) := insert ⊤ (s.image (fun i : ι => (i : WithTop ι)))
  have hq : Function.Injective q := by
    intro i j he
    cases i using WithTop.recTopCoe <;> cases j using WithTop.recTopCoe
    · rfl
    · exact (ha _ he).elim
    · exact (ha _ he.symm).elim
    · exact congrArg (fun i : ι => (i : WithTop ι)) (hp he)
  have hcard : 4 ≤ t.card := by
    have he : t.card = s.card + 1 := by
      simp [t, Finset.card_image_of_injective s WithTop.coe_injective]
    omega
  have hmem (i : ι) : (i : WithTop ι) ∈ t ↔ i ∈ s := by simp [t]
  have ht := convexPosition_of_positive_triples q hq t hcard (by
    intro i hi j hj k hk hij hjk
    cases i using WithTop.recTopCoe
    · exact (not_top_lt hij).elim
    · rename_i i
      cases j using WithTop.recTopCoe
      · exact (not_top_lt hjk).elim
      · rename_i j
        cases k using WithTop.recTopCoe
        · exact hpair i (hmem i |>.mp hi) j (hmem j |>.mp hj) (WithTop.coe_lt_coe.mp hij)
        · rename_i k
          exact h i (hmem i |>.mp hi) j (hmem j |>.mp hj) k (hmem k |>.mp hk)
            (WithTop.coe_lt_coe.mp hij) (WithTop.coe_lt_coe.mp hjk))
  simpa [t, q, Finset.image_image, Function.comp_def] using ht

theorem convexPosition_insert_of_negative_triples {ι : Type*} [LinearOrder ι]
    (p : ι → Point) (hp : Function.Injective p) (s : Finset ι) (hs : 3 ≤ s.card)
    (a : Point) (ha : ∀ i, a ≠ p i)
    (h : ∀ i ∈ s, ∀ j ∈ s, ∀ k ∈ s, i < j → j < k → orient (p i) (p j) (p k) < 0)
    (hpair : ∀ i ∈ s, ∀ j ∈ s, i < j → orient (p i) (p j) a < 0) :
    ConvexPosition (insert a (s.image p)) := by
  apply convexPosition_insert_of_positive_triples (ι := ιᵒᵈ) p hp s hs a ha
  · intro i hi j hj k hk hij hjk
    have hn := h k hk j hj i hi hjk hij
    have he : orient (p i) (p j) (p k) = -orient (p k) (p j) (p i) := by
      simp only [orient]
      ring
    rw [he]
    exact neg_pos.mpr hn
  · intro i hi j hj hij
    have hn := hpair j hj i hi hij
    have he : orient (p i) (p j) a = -orient (p j) (p i) a := by
      simp only [orient]
      ring
    rw [he]
    exact neg_pos.mpr hn

end ErdosSzekeres.Suk

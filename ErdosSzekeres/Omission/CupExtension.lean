/-
The chord identity and upper/lower arc argument follow Michael Schroeder's
version-1 archive, DOI 10.5281/zenodo.22842891, ES8BoundaryGeometry.lean.
Code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Changes: a direct all-triples proof for adding one point to an arbitrary cup,
using this project's finite-set convex-position theorem.
-/
import ErdosSzekeres.Omission.ListGeometry

namespace ErdosSzekeres.Omission.CupExtension
open ActualRanks ListGeometry

/-- A point above the endpoint chord of a cup, within its horizontal span,
forms a convex polygon with the entire cup. -/
theorem cup_above_chord {k : ℕ} (hk : 1 ≤ k) (p : Fin (k + 2) → Point)
    (hx : StrictMono (fun i => p i 0))
    (positive : ∀ i j l, i < j → j < l → 0 < orient (p i) (p j) (p l))
    (q : Point) (left : p 0 0 ≤ q 0) (right : q 0 ≤ p (Fin.last (k + 1)) 0)
    (above : 0 < orient (p 0) (p (Fin.last (k + 1))) q)
    (S : Finset Point) (inside : ∀ i, p i ∈ S) (hq : q ∈ S) :
    HasConvexNGon (k + 3) S := by
  classical
  let last : Fin (k + 2) := Fin.last (k + 1)
  have pair : ∀ i j, i < j → 0 < orient (p i) (p j) q := by
    intro i j hij
    have hs : 0 ≤ orient (p i) (p j) (p 0) := by
      by_cases hi : i = 0
      · simp [hi, orient]
      · rw [orient_cycle]
        exact (positive 0 i j (Fin.pos_iff_ne_zero.mpr hi) hij).le
    have ht : 0 ≤ orient (p i) (p j) (p last) := by
      by_cases hj : j = last
      · simp [hj, orient, mul_comm]
      · exact (positive i j last hij (lt_of_le_of_ne (Fin.le_last j) hj)).le
    have identity : (p last 0 - p 0 0) * orient (p i) (p j) q =
        (p last 0 - q 0) * orient (p i) (p j) (p 0) +
        (q 0 - p 0 0) * orient (p i) (p j) (p last) +
        (p j 0 - p i 0) * orient (p 0) (p last) q := by unfold orient; ring
    have st : 0 < p last 0 - p 0 0 := sub_pos.mpr (hx (by change 0 < k + 1; omega))
    apply (mul_pos_iff_of_pos_left st).mp
    rw [identity]
    exact add_pos_of_nonneg_of_pos
      (add_nonneg (mul_nonneg (sub_nonneg.mpr right) hs)
        (mul_nonneg (sub_nonneg.mpr left) ht))
      (mul_pos (sub_pos.mpr (hx hij)) above)
  have distinct : ∀ i, q ≠ p i := by
    intro i eq
    by_cases hi : i = 0
    · have h := pair 0 ⟨1, by omega⟩ (by simp)
      rw [eq, hi] at h
      simp [orient, mul_comm] at h
    · have h := pair 0 i (Fin.pos_iff_ne_zero.mpr hi)
      rw [eq] at h
      simp [orient, mul_comm] at h
  have injective : Function.Injective p := fun _ _ eq => hx.injective (congrArg (· 0) eq)
  refine ⟨insert q (Finset.univ.image p), ?_, ?_, ?_⟩
  · intro x h
    rcases Finset.mem_insert.mp h with rfl | h
    · exact hq
    · obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp h
      exact inside i
  · have notMem : q ∉ Finset.univ.image p := by
      rintro h
      obtain ⟨i, _, eq⟩ := Finset.mem_image.mp h
      exact distinct i eq.symm
    simp [Finset.card_insert_of_notMem notMem, Finset.card_image_of_injective _ injective]
  · exact Suk.convexPosition_insert_of_positive_triples p injective Finset.univ
      (by simp; omega) q distinct (fun i _ j _ l _ => positive i j l)
      (fun i _ j _ => pair i j)

/-- A seven-cup and a three-cap sharing their endpoints form an actual octagon.
Their interiors need not be assumed disjoint. -/
theorem cup7_cap3 {n} (c : Configuration n) (s a b d v u t q : Nat)
    (cup : (colorConfig c.cup true).Cup [s,a,b,d,v,u,t])
    (sq : s < q) (qt : q < t) (cap : c.cup s q t = false)
    (tn : t < n) : HasConvexNGon 8 (Finset.univ.image c.point) := by
  let xs := [s,a,b,d,v,u,t]
  have inside : xs.In (Finset.range n) := by
    have order := cup.1
    simp only [List.isChain_cons_cons] at order
    intro z hz
    simp only [xs, List.mem_cons, List.not_mem_nil, or_false] at hz
    apply Finset.mem_range.mpr
    omega
  let p : Fin 7 → Point := fun i => pointAt c (xs.get i)
  have hx : StrictMono (fun i => p i 0) := by
    intro i j hij
    exact pointAt_order c (Finset.mem_range.mp (inside _ (xs.get_mem i)))
      (Finset.mem_range.mp (inside _ (xs.get_mem j))) (List.Sorted.rel_get_of_lt cup.1.pairwise hij)
  have all := cup_list_all c xs inside cup
  have positive : ∀ i j l : Fin 7, i < j → j < l → 0 < orient (p i) (p j) (p l) := by
    intro i j l hij hjl
    exact all _ (xs.get_mem i) _ (xs.get_mem j) _ (xs.get_mem l)
      (List.Sorted.rel_get_of_lt cup.1.pairwise hij) (List.Sorted.rel_get_of_lt cup.1.pairwise hjl)
  have sn : s < n := by omega
  have qn : q < n := by omega
  apply cup_above_chord (k := 5) (by omega) p hx positive (pointAt c q) ?_ ?_ ?_
    (Finset.univ.image c.point) ?_ ?_
  · exact (pointAt_order c sn qn sq).le
  · exact (pointAt_order c qn tn qt).le
  · change 0 < orient (pointAt c s) (pointAt c t) (pointAt c q)
    rw [orient_swap]
    exact neg_pos.mpr ((cap_sign c s q t sn qn tn sq qt).mp (by simp [cap]))
  · intro i
    rw [show p i = pointAt c (xs.get i) from rfl,
      pointAt_eq c _ (Finset.mem_range.mp (inside _ (xs.get_mem i)))]
    exact Finset.mem_image_of_mem c.point (Finset.mem_univ _)
  · rw [pointAt_eq c q qn]
    exact Finset.mem_image_of_mem c.point (Finset.mem_univ _)

end ErdosSzekeres.Omission.CupExtension


/-! ===== Appended by verify_odd_k_C12: m(5,9) ≤ 113 and N_mirror(9) ≤ 226 ===== -/

/-! Independent check for claim C12: m(5,9) ≤ 113 in Lean.

Abstract part (`config_capacity113`): in any `Config` (an arbitrary ternary relation `Cup3` on a linear
order), a finite set with no 5-cap and no 9-"gon" (cap and cup with common ends, lengths summing to 11)
has at most 113 elements.  Proof = one Erdős–Szekeres split: `T` = first points of 4-caps.
* `S \ T` has no 4-cap, so by Baek's theorem (vendored `main 6`) it has at most `C(8,2)+1 = 29` elements;
* `T` has no 8-cup (an 8-cup ending at a first point of a 4-cap extends to a 9-cup, which is a 9-gon,
  or to a 5-cap), so by the vendored cups–caps theorem `cap_cup 3 6` it has at most `C(9,3) = 84` elements.
The join step is adapted from the vendored proof of `Config.cap_cup`.

Geometric part (`capacity113`): the same for x-sorted geometric configurations, via the repository's
`colorConfig`/`hasCap_of_list`/`boundary_polygon` bridge (n = 9 analogue of `hasNGon_heptagon`). -/

open scoped Classical

namespace C12Check
open ErdosSzekeres
open ErdosSzekeres.Omission ErdosSzekeres.Omission.BoundaryGeometry
open ErdosSzekeres.Omission.BaekGeometry ErdosSzekeres.Omission.ActualRanks

theorem config_capacity113 {α : Type _} [LinearOrder α] (C : Config α) (S : Finset α)
    (noCap : ¬ C.HasNCap 5 S) (noGon : ¬ C.HasNGon 9 S) : S.card ≤ 113 := by
  set is_start_of_cap : α → Prop := fun p =>
    ∃ c, C.Cap c ∧ c.In S ∧ c.length = 4 ∧ p ∈ c.head? with def_is_start_of_cap
  set T := Finset.filter is_start_of_cap S with def_T
  have eq_card : (S \ T).card + T.card = S.card := by
    apply Finset.card_sdiff_add_card_eq_card
    rw [def_T]; exact S.filter_subset is_start_of_cap
  -- S \ T: no 4-cap, no 9-gon, so at most 29 points (Baek)
  have h1 : (S \ T).card ≤ 29 := by
    by_contra hlt
    have h28 : Nat.choose (6 + 2) 2 = 28 := by decide
    have hs : Nat.choose (6 + 2) 2 + 2 ≤ (S \ T).card := by rw [h28]; omega
    rcases main 6 C (S \ T) hs with hcap | hgon
    · rcases hcap with ⟨c, ⟨c_cap, c_length⟩, c_in⟩
      have c_nnil : c ≠ [] := by
        intro eq_c
        subst eq_c
        simp at c_length
      rcases List.takeHead c_nnil with ⟨ch, ct, eq_c⟩
      have h : ch ∈ S \ T := by apply c_in; rw [eq_c]; simp
      rw [def_T] at h; simp at h; cases' h with c_in_S h
      have f := h c_in_S ⟨c, c_cap, ?_, ?_, ?_⟩
      · exact f
      · intros a ha
        apply Finset.sdiff_subset
        apply c_in a ha
      · exact c_length
      · rw [eq_c]
        simp
    · exact noGon (hasNGon_supset Finset.sdiff_subset hgon)
  -- T: no 5-cap, no 8-cup, so at most 84 points (cups-caps)
  have h2 : T.card ≤ 84 := by
    by_contra hlt
    have h84 : Nat.choose (3 + 6) 3 = 84 := by decide
    have hs : Nat.choose (3 + 6) 3 < T.card := by rw [h84]; omega
    rcases C.cap_cup 3 6 T hs with hcap | hcup
    · exact noCap (hasNCap_supset (by rw [def_T]; simp) hcap)
    · rcases hcup with ⟨cl, ⟨cl_cup, cl_length⟩, cl_in_T⟩
      have cl_sz2 : 2 ≤ cl.length := by rw [cl_length] <;> simp
      rcases List.takeLast2 cl_sz2 with ⟨p, q, cl', eq_cl⟩; clear cl_sz2
      have q_in_T : q ∈ T := by refine' cl_in_T q _ <;> rw [eq_cl] <;> simp
      rw [def_T] at q_in_T <;> simp at q_in_T
      cases' q_in_T with q_in_S q_st; simp [def_is_start_of_cap] at q_st
      rcases q_st with ⟨cr, cr_cap, cr_in_S, cr_length, cr_head⟩
      have cr_sz2 : 2 ≤ cr.length := by rw [cr_length] <;> simp
      rcases List.takeHead2 cr_sz2 with ⟨q, r, cr', eq_cr⟩; clear cr_sz2
      rw [eq_cr] at cr_head; simp at cr_head; subst cr_head
      by_cases hpqr : C.Cup3 p q r
      · -- the 8-cup extends to a 9-cup, which is a 9-gon
        apply noGon
        apply ncup_is_ngon (by norm_num)
        use cl ++ [r]; refine' ⟨⟨_, _⟩, _⟩
        · rw [eq_cl]; simp; rw [← eq_cl]
          rw [eq_cr] at cr_cap; simp [Config.Cap] at cr_cap; tauto
        · simp; rw [cl_length]
        · simp; constructor
          refine' List.in_superset _ cl_in_T; rw [def_T]; simp
          rw [eq_cr] at cr_in_S; simp at cr_in_S; tauto
      · -- the 4-cap extends to a 5-cap
        apply noCap
        use p::cr; refine' ⟨⟨_, _⟩, _⟩
        · rw [eq_cr]; simp; rw [← eq_cr]
          rw [eq_cl] at cl_cup; simp [Config.Cup] at cl_cup; tauto
        · simp; rw [cr_length]
        · rw [List.cons_in]
          constructor
          · apply Finset.filter_subset is_start_of_cap
            rw [← def_T]
            simp_rw [eq_cl, List.In] at cl_in_T
            apply cl_in_T
            simp
          · assumption
  omega

theorem hasNGon_nonagon {n} (c : Configuration n)
    (gon : (colorConfig c.cup true).HasNGon 9 (Finset.range n)) :
    HasConvexNGon 9 (Finset.univ.image c.point) := by
  obtain ⟨xs,ys,hgon,xi,yi⟩ := gon
  let k := xs.length-2
  let l := ys.length-2
  have hx : xs.length=k+2 := by have := hgon.1.1; dsimp [k]; omega
  have hy : ys.length=l+2 := by have := hgon.1.2.2.1; dsimp [l]; omega
  have nine : l+k+2=9 := by have := hgon.2; omega
  have h := boundary_polygon (boundaryOfGon c xs ys k l hx hy xi yi hgon.1)
    (Finset.univ.image c.point) (by
      simpa only [Finset.coe_image, Finset.coe_univ, Set.image_univ] using
        boundaryOfGon_inside c xs ys k l hx hy xi yi hgon.1)
  simpa only [nine] using h

/-- m(5,9) ≤ 113 in geometric form: an x-sorted configuration with no geometric 5-cap and no convex
9-gon has at most 113 points. -/
theorem capacity113 {n} (c : Configuration n) (noCap : ¬ c.HasCap 5)
    (noNon : ¬ HasConvexNGon 9 (Finset.univ.image c.point)) : n ≤ 113 := by
  have h := config_capacity113 (colorConfig c.cup true) (Finset.range n)
    (fun cap => noCap (ListGeometry.hasCap_of_list c cap))
    (fun gon => noNon (hasNGon_nonagon c gon))
  simpa using h

end C12Check


namespace C12Check
open ErdosSzekeres

/-- **k = 9.** A finite set in general position that is symmetric under the reflection in the x-axis and
contains no 9 points in convex position has at most 226 points. -/
theorem mirror_nine (S : Finset Point) (gp : GeneralPosition S) (sym : ∀ p ∈ S, MirrorOdd.mir p ∈ S)
    (noGon : ¬ HasConvexNGon 9 S) : S.card ≤ 226 :=
  MirrorOdd.mirror_odd_general 4 113 (by norm_num) (fun _ c h1 h2 => capacity113 c h1 h2) S gp sym noGon

/-- **k = 9**, reflection in an arbitrary line `n0 x + n1 y = c` with `n0^2 + n1^2 = 1`. -/
theorem mirror_nine_line {n0 n1 c : ℝ} (hn : n0 ^ 2 + n1 ^ 2 = 1) (S : Finset Point)
    (gp : GeneralPosition S) (sym : ∀ p ∈ S, MirrorOdd.lineRefl n0 n1 c p ∈ S)
    (noGon : ¬ HasConvexNGon 9 S) : S.card ≤ 226 :=
  MirrorOdd.mirror_odd_general_line 4 113 (by norm_num) (fun _ c h1 h2 => capacity113 c h1 h2) hn S gp
    sym noGon

end C12Check

#print axioms C12Check.config_capacity113
#print axioms C12Check.capacity113
#print axioms C12Check.mirror_nine
#print axioms C12Check.mirror_nine_line

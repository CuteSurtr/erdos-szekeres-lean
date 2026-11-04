
/-! ## Review: non-vacuity tests (appended to a verbatim copy of `LayerLemma.lean`)

A concrete fourfold instance with two layers: the square `(±2,0),(0,±2)` and the inner square
`(±1/2,±1/2)`, about the origin, `m = 4`, `K = 8 = 2m`.  Every hypothesis of `strict_nesting`,
`layers_are_orbits`, `hullVerts_eq_orbitFS_rotAbout` and `chain_clauses_sound` is discharged. -/

namespace ErdosSzekeres.LayerLemma.Review

open ErdosSzekeres ErdosSzekeres.LayerLemma

noncomputable def L4 : List Point :=
  [![2, 0], ![0, 2], ![-2, 0], ![0, -2], ![1/2, 1/2], ![-1/2, 1/2], ![-1/2, -1/2], ![1/2, -1/2]]

noncomputable def S4 : Finset Point := L4.toFinset

theorem mem_S4 {x : Point} : x ∈ S4 ↔ x = ![2, 0] ∨ x = ![0, 2] ∨ x = ![-2, 0] ∨ x = ![0, -2] ∨
    x = ![1/2, 1/2] ∨ x = ![-1/2, 1/2] ∨ x = ![-1/2, -1/2] ∨ x = ![1/2, -1/2] := by
  simp [S4, L4]

theorem card_S4 : S4.card ≤ 8 := (List.toFinset_card_le _).trans (by simp [L4])

theorem angle4 : 2 * Real.pi / ((4 : ℕ) : ℝ) = Real.pi / 2 := by push_cast; ring

theorem rot4 (p : Point) : rotAbout 0 (2 * Real.pi / ((4 : ℕ) : ℝ)) p = ![-(p 1), p 0] := by
  rw [angle4]
  funext i
  fin_cases i <;> simp [rotAbout, Real.cos_pi_div_two, Real.sin_pi_div_two]

theorem hc4 : (0 : Point) ∉ S4 := by
  intro h
  rcases mem_S4.1 h with h | h | h | h | h | h | h | h <;>
    (rw [funext_iff, Fin.forall_fin_two] at h; norm_num at h)

theorem inv4 : Invariant (rotAbout 0 (2 * Real.pi / ((4 : ℕ) : ℝ))) S4 := by
  intro p hp
  rw [rot4, mem_S4]
  rcases mem_S4.1 hp with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> norm_num

set_option maxHeartbeats 20000000 in
theorem gp4 : GeneralPosition S4 := by
  rw [generalPosition_iff_orient_ne_zero]
  intro a ha b hb d hd h1 h2 h3
  rcases mem_S4.1 ha with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
  rcases mem_S4.1 hb with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
  rcases mem_S4.1 hd with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
  first
  | exact absurd rfl h1
  | exact absurd rfl h2
  | exact absurd rfl h3
  | norm_num [orient]

/-- The inner point `(1/2,1/2)` is the centroid of `(2,0), (0,2), (-1/2,-1/2)`. -/
theorem inner4 : (![1/2, 1/2] : Point) ∈ convexHull ℝ ((S4 : Set Point) \ {![1/2, 1/2]}) := by
  have mem : ∀ q : Point, q ∈ S4 → q ≠ ![1/2, 1/2] →
      q ∈ convexHull ℝ ((S4 : Set Point) \ {![1/2, 1/2]}) :=
    fun q hq hne => subset_convexHull ℝ _ ⟨hq, hne⟩
  have ha := mem ![2, 0] (mem_S4.2 (by simp)) (by norm_num)
  have hb := mem ![0, 2] (mem_S4.2 (by simp)) (by norm_num)
  have hd := mem ![-1/2, -1/2] (mem_S4.2 (by simp)) (by norm_num)
  have hab := convex_convexHull ℝ _ ha hb (by norm_num : (0 : ℝ) ≤ 1/2) (by norm_num : (0 : ℝ) ≤ 1/2)
    (by norm_num : (1/2 : ℝ) + 1/2 = 1)
  have h2 := convex_convexHull ℝ _ hab hd (by norm_num : (0 : ℝ) ≤ 2/3) (by norm_num : (0 : ℝ) ≤ 1/3)
    (by norm_num : (2/3 : ℝ) + 1/3 = 1)
  convert h2 using 1
  funext i
  fin_cases i <;> norm_num

theorem hno4 : ¬ HasConvexNGon 8 S4 := by
  rintro ⟨t, ht, htc, hconv⟩
  have heq : t = S4 := Finset.eq_of_subset_of_card_le ht (by have := card_S4; omega)
  subst heq
  unfold ConvexPosition at hconv
  rw [convexIndependent_set_iff_notMem_convexHull_diff] at hconv
  exact hconv _ (Finset.mem_coe.2 (mem_S4.2 (by simp))) inner4

theorem hv4 : (![2, 0] : Point) ∈ hullVerts S4 := by
  rw [mem_hullVerts]
  refine ⟨mem_S4.2 (by simp), fun hmem => ?_⟩
  have hsub : ((S4 : Set Point) \ {![2, 0]}) ⊆ {q : Point | 0 ≤ orient ![1/2, 0] ![1/2, 1] q} := by
    rintro q ⟨hq, hq2⟩
    simp only [Set.mem_singleton_iff] at hq2
    simp only [Set.mem_setOf_eq]
    rcases mem_S4.1 (Finset.mem_coe.1 hq) with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
      first
      | exact absurd rfl hq2
      | norm_num [orient]
  have := convexHull_min hsub (convex_orient_nonneg _ _) hmem
  norm_num [orient] at this

theorem peel1_4 : (![1/2, 1/2] : Point) ∈ peel S4 1 := by
  rw [peel_succ]
  exact Finset.mem_sdiff.2 ⟨mem_S4.2 (by simp), fun h => (mem_hullVerts.1 h).2 inner4⟩

/-- `strict_nesting` applies to the instance (all hypotheses discharged). -/
theorem nest4 : 0 < orient (![2, 0] : Point) (rotAbout 0 (2 * Real.pi / ((4 : ℕ) : ℝ)) ![2, 0])
    ![1/2, 1/2] :=
  strict_nesting (m := 4) (K := 8) (by norm_num) (by norm_num) hc4 inv4 hno4 gp4
    (n := 0) (n' := 1) (by norm_num) hv4 peel1_4

/-- `hullVerts_eq_orbitFS_rotAbout` applies: the outer layer is the orbit of `(2,0)`. -/
theorem orbit4 : hullVerts S4 = orbitFS (rotAbout 0 (2 * Real.pi / ((4 : ℕ) : ℝ))) 4 ![2, 0] :=
  hullVerts_eq_orbitFS_rotAbout (m := 4) (K := 8) (by norm_num) (by norm_num) hc4 inv4 hno4 hv4

/-- `layers_are_orbits` applies, at layers 0 and 1 (both nonempty). -/
theorem layers4 (n : ℕ) (hn : n ≤ 1) :
    ∃ x ∈ peel S4 n, hullVerts (peel S4 n) = orbitFS (rotAbout 0 (2 * Real.pi / ((4 : ℕ) : ℝ))) 4 x ∧
      (orbitFS (rotAbout 0 (2 * Real.pi / ((4 : ℕ) : ℝ))) 4 x).card = 4 ∧
      (peel S4 (n + 1) : Set Point) ⊆
        convexHull ℝ (hullVerts (peel S4 n) : Set Point) := by
  refine layers_are_orbits (m := 4) (K := 8) (by norm_num) (by norm_num) hc4 inv4 hno4 n ?_
  interval_cases n
  · exact ⟨_, hullVerts_subset _ hv4⟩
  · exact ⟨_, peel1_4⟩

/-- `chain_clauses_sound` applies with `m = 4`, `K = 8`: no 7-point chain around `(2,0)`. -/
theorem chain4 (q : ℕ → Point) (hq : ∀ s < 7, q s ∈ peel S4 0) (hqp : ∀ s < 7, q s ≠ ![2, 0])
    (hfan : ∀ s, s + 1 < 7 → 0 < orient ![2, 0] (q s) (q (s + 1)))
    (hturn : ∀ s, s + 2 < 7 → 0 < orient (q s) (q (s + 1)) (q (s + 2))) : False :=
  chain_clauses_sound (m := 4) (K := 8) (by norm_num) (by norm_num) (by norm_num) hc4 inv4 hno4 gp4
    (i := 0) hv4 hq hqp hfan hturn

/-- Sixfold single layer: the rotation by `2π/6` maps the regular hexagon to itself. -/
noncomputable def H6 : Finset Point :=
  [![1, 0], ![1/2, Real.sqrt 3 / 2], ![-1/2, Real.sqrt 3 / 2], ![-1, 0], ![-1/2, -(Real.sqrt 3 / 2)],
    ![1/2, -(Real.sqrt 3 / 2)]].toFinset

theorem inv6 : Invariant (rotAbout 0 (2 * Real.pi / ((6 : ℕ) : ℝ))) H6 := by
  have hang : 2 * Real.pi / ((6 : ℕ) : ℝ) = Real.pi / 3 := by push_cast; ring
  have h3 : Real.sqrt 3 * Real.sqrt 3 = 3 := Real.mul_self_sqrt (by norm_num)
  intro p hp
  simp only [H6, List.mem_toFinset, List.mem_cons, List.not_mem_nil,
    or_false] at hp ⊢
  rw [hang]
  rcases hp with rfl | rfl | rfl | rfl | rfl | rfl <;>
    simp [rotAbout, Real.cos_pi_div_three, Real.sin_pi_div_three] <;> ring_nf <;>
    norm_num

end ErdosSzekeres.LayerLemma.Review

#print axioms ErdosSzekeres.LayerLemma.Review.nest4
#print axioms ErdosSzekeres.LayerLemma.Review.orbit4
#print axioms ErdosSzekeres.LayerLemma.Review.layers4
#print axioms ErdosSzekeres.LayerLemma.Review.chain4
#print axioms ErdosSzekeres.LayerLemma.Review.inv6
#check @ErdosSzekeres.LayerLemma.sixfold_octagon
#check @ErdosSzekeres.LayerLemma.sevenfold_octagon
#print ErdosSzekeres.LayerLemma.Sixfold66
#print ErdosSzekeres.LayerLemma.Sevenfold70

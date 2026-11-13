import ErdosSzekeres.OrientationGeometry
import ErdosSzekeres.Basic
import ErdosSzekeres.Vendor.ErdosSzekeresConvex.ConvexPolygon

namespace ErdosSzekeres.Suk

/-- Coordinate equivalence used to connect the independently developed APIs. -/
def pointEquiv : Point ≃ₗ[ℝ] Point2D where
  toFun p := (p 0, p 1)
  invFun p := ![p.1, p.2]
  left_inv p := by ext i; fin_cases i <;> rfl
  right_inv p := by rfl
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

theorem pair_generalPosition {s : Finset Point} (h : GeneralPosition s) :
    InGeneralPosition (s.image pointEquiv) := by
  classical
  intro a b c ha hb hc hab hbc hac
  obtain ⟨a', ha', rfl⟩ := Finset.mem_image.mp ha
  obtain ⟨b', hb', rfl⟩ := Finset.mem_image.mp hb
  obtain ⟨c', hc', rfl⟩ := Finset.mem_image.mp hc
  exact (generalPosition_iff_orient_ne_zero s).mp h a' ha' b' hb' c' hc'
    (fun e => hab (congrArg pointEquiv e))
    (fun e => hac (congrArg pointEquiv e))
    (fun e => hbc (congrArg pointEquiv e))

theorem hasConvexNGon_of_pair {s : Finset Point} {n : ℕ}
    (h : FormsConvexPolygon (s.image pointEquiv) n) : HasConvexNGon n s := by
  classical
  obtain ⟨t, hts, htcard, htconvex⟩ := h
  let u := t.image pointEquiv.symm
  refine ⟨u, ?_, ?_, ?_⟩
  · intro p hp
    obtain ⟨q, hq, rfl⟩ := Finset.mem_image.mp hp
    obtain ⟨r, hr, rfl⟩ := Finset.mem_image.mp (hts hq)
    simpa using hr
  · rw [Finset.card_image_of_injective t pointEquiv.symm.injective]
    exact htcard
  · rw [convexPosition_iff]
    intro p hp hmem
    obtain ⟨q, hq, rfl⟩ := Finset.mem_image.mp hp
    apply htconvex q hq
    have hm : pointEquiv (pointEquiv.symm q) ∈
        pointEquiv '' convexHull ℝ ((u : Set Point) \ {pointEquiv.symm q}) :=
      Set.mem_image_of_mem pointEquiv hmem
    change pointEquiv (pointEquiv.symm q) ∈
      pointEquiv.toLinearMap '' convexHull ℝ ((u : Set Point) \ {pointEquiv.symm q}) at hm
    rw [pointEquiv.toLinearMap.image_convexHull] at hm
    change pointEquiv (pointEquiv.symm q) ∈
      convexHull ℝ (pointEquiv '' ((u : Set Point) \ {pointEquiv.symm q})) at hm
    have himage : pointEquiv '' ((u : Set Point) \ {pointEquiv.symm q}) =
        (t : Set Point2D) \ {q} := by
      rw [Set.image_diff pointEquiv.injective, Set.image_singleton,
        LinearEquiv.apply_symm_apply]
      congr 1
      simp [u, Finset.coe_image, ← Set.image_comp]
    simpa [himage] using hm

/-- Suk's geometric cups-caps prerequisite, stated using this project's points. -/
theorem cups_caps {s : Finset Point} (a b : ℕ) (ha : 3 ≤ a) (hb : 3 ≤ b)
    (hgp : GeneralPosition s)
    (hx : HasDistinctX (s.image pointEquiv))
    (hcard : (a + b - 4).choose (a - 2) + 1 ≤ s.card) :
    (∃ cup : List Point2D, IsCup cup a ∧ ∀ p ∈ cup, p ∈ s.image pointEquiv) ∨
    (∃ cap : List Point2D, IsCap cap b ∧ ∀ p ∈ cap, p ∈ s.image pointEquiv) := by
  classical
  exact cup_cap_lemma a b ha hb _ hx
    (by simpa [Finset.card_image_of_injective s pointEquiv.injective] using hcard)
    (pair_generalPosition hgp)

/-- The classical binomial upper bound, using the bridged real geometric definition.
This is a prerequisite for, and much weaker than, Suk's asymptotic theorem. -/
theorem classical_upper_bound (n : ℕ) (hn : 3 ≤ n) :
    ForcesConvexNGon ((2 * n - 4).choose (n - 2) + 1) n := by
  classical
  intro s hgp hcard
  let S := s.image pointEquiv
  obtain ⟨c, d, hunit, hdist⟩ := exists_rotation_hasDistinctX S
  have hgen := inGeneralPosition_rotate2D S c d hunit (pair_generalPosition hgp)
  have hsize : (n + n - 4).choose (n - 2) + 1 ≤ (S.image (rotate2D c d)).card := by
    rw [Finset.card_image_of_injective S (rotate2D_injective c d hunit)]
    simpa [S, Finset.card_image_of_injective s pointEquiv.injective, two_mul] using hcard
  have hpoly : FormsConvexPolygon (S.image (rotate2D c d)) n := by
    rcases cup_cap_lemma n n hn hn _ hdist hsize hgen with ⟨C, hC, hsub⟩ | ⟨C, hC, hsub⟩
    · exact formsConvexPolygon_of_isCup _ C n hn hC hsub
    · exact formsConvexPolygon_of_isCap _ C n hn hC hsub
  exact hasConvexNGon_of_pair (formsConvexPolygon_of_rotate2D S n c d hunit hpoly)

end ErdosSzekeres.Suk

import ErdosSzekeres.HMPT.Maxima

namespace ErdosSzekeres.HMPT

open Suk

/-- Attained maxima of the two facing cap sizes in a geometric chain. -/
structure ChainCapacities {F : CapFrame} (C : SpikeChain F) where
  left : ℕ
  right : ℕ
  left_cap : C.LeftCap left
  right_cap : C.RightCap right
  left_max : ∀ m, C.LeftCap m → m ≤ left
  right_max : ∀ m, C.RightCap m → m ≤ right

theorem exists_chainCapacities {F : CapFrame} (C : SpikeChain F) :
    Nonempty (ChainCapacities C) := by
  classical
  have hzero (a : Point) : ConvexPosition (insert a ((∅ : Finset (Fin C.length)).image C.vertex)) := by
    simp [convexPosition_iff]
  obtain ⟨l, hl, hlmax⟩ := exists_max_bounded (N := C.length) (P := C.LeftCap)
    ⟨0, ∅, rfl, hzero F.c⟩ (by
      rintro m ⟨s, rfl, _⟩
      exact (Finset.card_le_univ s).trans_eq (Fintype.card_fin _))
  obtain ⟨r, hr, hrmax⟩ := exists_max_bounded (N := C.length) (P := C.RightCap)
    ⟨0, ∅, rfl, hzero F.b⟩ (by
      rintro m ⟨s, rfl, _⟩
      exact (Finset.card_le_univ s).trans_eq (Fintype.card_fin _))
  exact ⟨⟨l, r, hl, hr, hlmax, hrmax⟩⟩

/-- Padding the capacities to two handles empty and singleton chains while
keeping the geometric maxima as actual witnesses. -/
theorem ChainCapacities.length_le_binomial {F : CapFrame} {C : SpikeChain F}
    (B : ChainCapacities C)
    (hgp : GeneralPosition (insert F.b (insert F.c C.points))) :
    C.length ≤ ((max 2 B.left - 1) + (max 2 B.right - 1)).choose (max 2 B.left - 1) := by
  classical
  by_contra! hsize
  rcases F.chain_caps C.point C.increasing Finset.univ hgp
      (max 2 B.left - 1) (max 2 B.right - 1) (by omega) (by omega)
      (by simpa using hsize) with ⟨s, _, hs, hc⟩ | ⟨s, _, hs, hc⟩
  · have := B.left_max _ ⟨s, hs, hc⟩
    omega
  · have := B.right_max _ ⟨s, hs, hc⟩
    omega

theorem ChainCapacities.left_lt {F : CapFrame} {C : SpikeChain F}
    (B : ChainCapacities C) {n : ℕ} (havoid : ¬ HasConvexNGon n C.points) : B.left < n := by
  by_contra! h
  exact havoid (C.leftCap_hasConvexNGon B.left_cap h)

theorem ChainCapacities.right_lt {F : CapFrame} {C : SpikeChain F}
    (B : ChainCapacities C) {n : ℕ} (havoid : ¬ HasConvexNGon n C.points) : B.right < n := by
  by_contra! h
  exact havoid (C.rightCap_hasConvexNGon B.right_cap h)

/-- The adjacent-region budget is derived from convex gluing of the attained
maxima. It is not an assumed numerical constraint. -/
theorem adjacent_cap_budget (F : AdjacentCapFrames)
    (C : SpikeChain F.left) (D : SpikeChain F.right)
    (B : ChainCapacities C) (E : ChainCapacities D) {P : Finset Point} {n : ℕ}
    (hn : 4 ≤ n) (hgp : GeneralPosition P) (hanchor : F.left.c ∈ P)
    (hC : C.points ⊆ P) (hD : D.points ⊆ P) (havoid : ¬ HasConvexNGon n P) :
    B.left + E.right < n := by
  by_contra! hsize
  exact havoid (F.glue_chain_caps C D hgp hanchor hC hD hn hsize B.left_cap E.right_cap)

end ErdosSzekeres.HMPT

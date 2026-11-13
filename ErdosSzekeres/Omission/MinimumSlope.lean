/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891, ES8MinimumSlope.lean.
Code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Changes: real points as Fin 2 → ℝ, local geometry and namespaces, Lean 4.24.
-/
import ErdosSzekeres.Omission.Realization

namespace ErdosSzekeres.Omission.MinimumSlope
open ErdosSzekeres

noncomputable def slope (a b : Point) : ℝ := (b 1-a 1)/(b 0-a 0)

theorem slope_symm (a b : Point) : slope a b=slope b a := by
  unfold slope
  calc
    _ = -(b 1-a 1)/ -(b 0-a 0) := (neg_div_neg_eq _ _).symm
    _ = _ := by congr 1 <;> ring

theorem orientation_left (a b c : Point) (ab : a 0<b 0) (ac : a 0<c 0) :
    orient a b c=(b 0-a 0)*(c 0-a 0)*(slope a c-slope a b) := by
  unfold orient slope
  field_simp [ne_of_gt (sub_pos.mpr ab),ne_of_gt (sub_pos.mpr ac)]

theorem orientation_middle (a b c : Point) (ab : a 0<b 0) (bc : b 0<c 0) :
    orient a b c=(b 0-a 0)*(c 0-b 0)*(slope b c-slope a b) := by
  unfold orient slope
  field_simp [ne_of_gt (sub_pos.mpr ab),ne_of_gt (sub_pos.mpr bc)]
  ring

theorem orientation_right (a b c : Point) (ac : a 0<c 0) (bc : b 0<c 0) :
    orient a b c=(c 0-a 0)*(c 0-b 0)*(slope b c-slope a c) := by
  unfold orient slope
  field_simp [ne_of_gt (sub_pos.mpr ac),ne_of_gt (sub_pos.mpr bc)]
  ring

/-- A chosen attaining minimum slope at every point. General position will
supply strict geometric consequences; no global distinct-slope assumption is used. -/
structure MinNeighbors {n} (c : Configuration n) where
  neighbor : Fin n→Fin n
  different : ∀ u, neighbor u≠u
  minimum : ∀ u v, v≠u → slope (c.point u) (c.point (neighbor u))≤slope (c.point u) (c.point v)

theorem exists_min_neighbors {n} (c : Configuration n) (hn : 2≤n) : Nonempty (MinNeighbors c) := by
  classical
  have exists_min (u : Fin n) : ∃ v : Fin n, v≠u ∧
      ∀ w : Fin n, w≠u → slope (c.point u) (c.point v)≤slope (c.point u) (c.point w) := by
    have nonempty : (Finset.univ.erase u).Nonempty := by
      by_cases hz : u.val=0
      · refine ⟨⟨1,by omega⟩,Finset.mem_erase.mpr ⟨?_,by simp⟩⟩
        intro he; have := congrArg Fin.val he; simp at this; omega
      · refine ⟨⟨0,by omega⟩,Finset.mem_erase.mpr ⟨?_,by simp⟩⟩
        intro he; have := congrArg Fin.val he; simp at this; omega
    obtain ⟨v,hv,hmin⟩ := Finset.exists_min_image (Finset.univ.erase u) (fun v=>slope (c.point u) (c.point v)) nonempty
    exact ⟨v,(Finset.mem_erase.mp hv).1,fun w hw=>hmin w (Finset.mem_erase.mpr ⟨hw,by simp⟩)⟩
  choose f different minimum using exists_min
  exact ⟨⟨f,different,minimum⟩⟩

theorem cap_to_right {n} {c : Configuration n} (m : MinNeighbors c) (u v : Fin n)
    (uv : u<v) (right : v<m.neighbor v) : orient (c.point u) (c.point v) (c.point (m.neighbor v))<0 := by
  have h := m.minimum v u (ne_of_lt uv)
  rw [slope_symm (c.point v) (c.point u)] at h
  have nonpos : orient (c.point u) (c.point v) (c.point (m.neighbor v))≤0 := by
    rw [orientation_middle _ _ _ (c.xOrder uv) (c.xOrder right)]
    exact mul_nonpos_of_nonneg_of_nonpos
      (le_of_lt (mul_pos (sub_pos.mpr (c.xOrder uv)) (sub_pos.mpr (c.xOrder right)))) (sub_nonpos.mpr h)
  exact lt_of_le_of_ne nonpos (c.generalPosition u v _ uv right)

theorem cup_from_left {n} {c : Configuration n} (m : MinNeighbors c) (u v : Fin n)
    (uv : u<v) (left : m.neighbor u<u) : 0<orient (c.point (m.neighbor u)) (c.point u) (c.point v) := by
  have h := m.minimum u v (ne_of_gt uv)
  rw [slope_symm (c.point u) (c.point (m.neighbor u))] at h
  have nonneg : 0≤orient (c.point (m.neighbor u)) (c.point u) (c.point v) := by
    rw [orientation_middle _ _ _ (c.xOrder left) (c.xOrder uv)]
    exact mul_nonneg
      (le_of_lt (mul_pos (sub_pos.mpr (c.xOrder left)) (sub_pos.mpr (c.xOrder uv)))) (sub_nonneg.mpr h)
  exact lt_of_le_of_ne nonneg (Ne.symm (c.generalPosition _ u v left uv))

theorem right_neighbor_points_left {n} {c : Configuration n} (m : MinNeighbors c) (u : Fin n)
    (right : u<m.neighbor u) : m.neighbor (m.neighbor u)<m.neighbor u := by
  by_contra hn
  have rr : m.neighbor u<m.neighbor (m.neighbor u) :=
    lt_of_le_of_ne (le_of_not_gt hn) (Ne.symm (m.different _))
  have negative := cap_to_right m u (m.neighbor u) right rr
  have minimum := m.minimum u (m.neighbor (m.neighbor u)) (ne_of_gt (lt_trans right rr))
  have nonneg : 0≤orient (c.point u) (c.point (m.neighbor u)) (c.point (m.neighbor (m.neighbor u))) := by
    rw [orientation_left _ _ _ (c.xOrder right) (c.xOrder (lt_trans right rr))]
    exact mul_nonneg (le_of_lt (mul_pos (sub_pos.mpr (c.xOrder right))
      (sub_pos.mpr (c.xOrder (lt_trans right rr))))) (sub_nonneg.mpr minimum)
  linarith

theorem left_neighbor_points_right {n} {c : Configuration n} (m : MinNeighbors c) (u : Fin n)
    (left : m.neighbor u<u) : m.neighbor u<m.neighbor (m.neighbor u) := by
  by_contra hn
  have ll : m.neighbor (m.neighbor u)<m.neighbor u :=
    lt_of_le_of_ne (le_of_not_gt hn) (m.different _)
  have positive := cup_from_left m (m.neighbor u) u left ll
  have minimum := m.minimum u (m.neighbor (m.neighbor u)) (ne_of_lt (lt_trans ll left))
  rw [slope_symm (c.point u) (c.point (m.neighbor u)),
    slope_symm (c.point u) (c.point (m.neighbor (m.neighbor u)))] at minimum
  have nonpos : orient (c.point (m.neighbor (m.neighbor u))) (c.point (m.neighbor u)) (c.point u)≤0 := by
    rw [orientation_right _ _ _ (c.xOrder (lt_trans ll left)) (c.xOrder left)]
    exact mul_nonpos_of_nonneg_of_nonpos
      (le_of_lt (mul_pos (sub_pos.mpr (c.xOrder (lt_trans ll left))) (sub_pos.mpr (c.xOrder left))))
      (sub_nonpos.mpr minimum)
  linarith

end ErdosSzekeres.Omission.MinimumSlope

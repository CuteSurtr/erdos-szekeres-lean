import ErdosSzekeres.Suk.Reflection

namespace ErdosSzekeres.Suk

/-- The existing geometric rotation, transported to the project's point type. -/
def rotation (c s : ℝ) (hunit : c ^ 2 + s ^ 2 = 1) : Point ≃ₗ[ℝ] Point :=
  { pointEquiv.symm.toLinearMap.comp ((rotate2D_lm c s).comp pointEquiv.toLinearMap) with
    invFun := fun p => pointEquiv.symm (rotate2D c (-s) (pointEquiv p))
    left_inv := by
      intro p
      change pointEquiv.symm (rotate2D c (-s)
        (pointEquiv (pointEquiv.symm (rotate2D c s (pointEquiv p))))) = p
      rw [LinearEquiv.apply_symm_apply, rotate2D_inv c s hunit,
        LinearEquiv.symm_apply_apply]
    right_inv := by
      intro p
      change pointEquiv.symm (rotate2D c s
        (pointEquiv (pointEquiv.symm (rotate2D c (-s) (pointEquiv p))))) = p
      rw [LinearEquiv.apply_symm_apply, rotate2D_inv' c s hunit,
        LinearEquiv.symm_apply_apply] }

theorem orient_rotation (c s : ℝ) (hunit : c ^ 2 + s ^ 2 = 1) (a b d : Point) :
    orient (rotation c s hunit a) (rotation c s hunit b) (rotation c s hunit d) =
      orient a b d :=
  orientationDet_rotate2D c s hunit (pointEquiv a) (pointEquiv b) (pointEquiv d)

/-- Every finite point set has an invertible linear image with distinct
x-coordinates. General position and the number of points are retained. -/
theorem exists_horizontal_image (S : Finset Point) (hgp : GeneralPosition S) :
    ∃ e : Point ≃ₗ[ℝ] Point,
      GeneralPosition (S.image e) ∧
      ∀ a ∈ S.image e, ∀ b ∈ S.image e, a 0 = b 0 → a = b := by
  classical
  obtain ⟨c, s, hu, hd⟩ := exists_rotation_hasDistinctX (S.image pointEquiv)
  refine ⟨rotation c s hu, ?_, ?_⟩
  · rw [generalPosition_iff_orient_ne_zero] at hgp ⊢
    intro a ha b hb d hd hab had hbd
    obtain ⟨a', ha', rfl⟩ := Finset.mem_image.mp ha
    obtain ⟨b', hb', rfl⟩ := Finset.mem_image.mp hb
    obtain ⟨d', hd', rfl⟩ := Finset.mem_image.mp hd
    rw [orient_rotation]
    exact hgp a' ha' b' hb' d' hd'
      (fun he => hab (congrArg _ he)) (fun he => had (congrArg _ he))
      (fun he => hbd (congrArg _ he))
  · intro a ha b hb he
    obtain ⟨a', ha', rfl⟩ := Finset.mem_image.mp ha
    obtain ⟨b', hb', rfl⟩ := Finset.mem_image.mp hb
    by_contra hn
    apply hd (rotate2D c s (pointEquiv a')) (rotate2D c s (pointEquiv b'))
      (Finset.mem_image_of_mem (rotate2D c s) (Finset.mem_image_of_mem pointEquiv ha'))
      (Finset.mem_image_of_mem (rotate2D c s) (Finset.mem_image_of_mem pointEquiv hb'))
      (fun h => hn (congrArg pointEquiv.symm h))
    exact he

end ErdosSzekeres.Suk

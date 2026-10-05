import ErdosSzekeres.OrientationGeometry
import ErdosSzekeres.Suk.TriangleMembership
import ErdosSzekeres.Suk.PairSupports

namespace ErdosSzekeres

/-- Exact integer coordinates, interpreted in the real plane. -/
def integerToReal (p : Fin 2 → ℤ) : Point := fun i => p i

theorem integerToReal_injective : Function.Injective integerToReal := by
  intro p q h
  funext i
  exact Int.cast_injective (congrFun h i)

@[simp] theorem orient_integerToReal (a b c : Fin 2 → ℤ) :
    orient (integerToReal a) (integerToReal b) (integerToReal c) =
      (orient a b c : ℤ) := by
  simp [orient, integerToReal]

/-- A strict interior certificate. The three products also certify that the
triangle is nondegenerate. All certificate arithmetic is over integers. -/
def IntegerInterior (p a b c : Fin 2 → ℤ) : Prop :=
  0 < orient a b c * orient a b p ∧
  0 < orient a b c * orient b c p ∧
  0 < orient a b c * orient c a p

instance (p a b c : Fin 2 → ℤ) : Decidable (IntegerInterior p a b c) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _))

theorem IntegerInterior.mem_triangle {p a b c : Fin 2 → ℤ}
    (h : IntegerInterior p a b c) :
    integerToReal p ∈ convexHull ℝ
      ({integerToReal a, integerToReal b, integerToReal c} : Set Point) := by
  have hz : orient a b c ≠ 0 := left_ne_zero_of_mul (ne_of_gt h.1)
  apply (Suk.mem_triangle_iff_orient_products _ _ _ _ ?_).mpr
  · simp only [orient_integerToReal]
    exact_mod_cast (show 0 ≤ orient a b c * orient a b p ∧
      0 ≤ orient a b c * orient b c p ∧ 0 ≤ orient a b c * orient c a p from
      ⟨h.1.le, h.2.1.le, h.2.2.le⟩)
  · simpa only [orient_integerToReal, ne_eq, Int.cast_eq_zero] using hz

/-- A checked interior point excludes convex position in every containing set.
This is the soundness bridge used by finite obstruction certificates. -/
theorem IntegerInterior.not_convexPosition {p a b c : Fin 2 → ℤ}
    (h : IntegerInterior p a b c) {s : Finset Point}
    (hp : integerToReal p ∈ s) (ha : integerToReal a ∈ s)
    (hb : integerToReal b ∈ s) (hc : integerToReal c ∈ s) : ¬ ConvexPosition s := by
  intro hs
  have hpa : p ≠ a := by intro he; subst p; simpa [orient] using h.1
  have hpb : p ≠ b := by intro he; subst p; simpa [orient, mul_comm] using h.1
  have hpc : p ≠ c := by intro he; subst p; simpa [orient, mul_comm] using h.2.1
  apply (convexPosition_iff s).mp hs _ hp
  apply convexHull_mono (s := ({integerToReal a, integerToReal b,
    integerToReal c} : Set Point)) ?_ h.mem_triangle
  intro x hx
  rcases hx with rfl | rfl | rfl
  · exact ⟨ha, fun he => hpa (integerToReal_injective he).symm⟩
  · exact ⟨hb, fun he => hpb (integerToReal_injective he).symm⟩
  · exact ⟨hc, fun he => hpc (integerToReal_injective he).symm⟩

/-- Finite supporting-edge certificates prove convex position of their real
image. The sign may be chosen separately for each vertex. -/
theorem convexPosition_integer_image_of_supports {ι : Type*} [Fintype ι]
    (p : ι → Fin 2 → ℤ)
    (h : ∀ i, ∃ j, p i ≠ p j ∧ ∃ sign : ℤ,
      ∀ k, p k ≠ p i → p k ≠ p j → 0 < sign * orient (p i) (p j) (p k)) :
    ConvexPosition (Finset.univ.image (fun i => integerToReal (p i))) := by
  classical
  apply Suk.convexPosition_of_pair_supports
  rintro x hx
  obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hx
  obtain ⟨j, hij, sign, hsign⟩ := h i
  refine ⟨integerToReal (p j), (sign : ℝ), fun he => hij (integerToReal_injective he), ?_⟩
  rintro z hz hzi
  obtain ⟨k, _, rfl⟩ := Finset.mem_image.mp hz
  by_cases hkj : p k = p j
  · exact Or.inl (congrArg integerToReal hkj)
  · right
    have hki : p k ≠ p i := fun he => hzi (congrArg integerToReal he)
    simp only [orient_integerToReal]
    exact_mod_cast hsign k hki hkj

end ErdosSzekeres

/-
The root-and-chart argument follows Michael Schroeder's version-1 archive,
19 September 2026, DOI 10.5281/zenodo.22842891, ES8ProjectiveTransfer / ES8Final.
Adapted code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Changes: use this project's finite real sets, existing HMPT projective theorems,
and a general polygon-size statement. Finite capacity hypotheses remain explicit
parameters of the conditional transfer theorems.
-/
import ErdosSzekeres.Omission.Realization
import ErdosSzekeres.ConvexCycleCuts
import ErdosSzekeres.HMPT.ProjectedCaps
import ErdosSzekeres.Suk.CoordinateNormalization

namespace ErdosSzekeres.Omission

open HMPT

/-- A cap in the positive projective chart, together with its retained root,
is a convex polygon in the original real plane. This statement is uniform in
the cap size, and requires no general-position assumption beyond the strict
signs and ordering explicitly given. -/
theorem root_cap_polygon {k : ℕ} (hk : 3 ≤ k) (a : Point) (p : Fin k → Point)
    (right : ∀ i, a 0 < p i 0)
    (ordered : StrictMono (fun i => projectFrom a (p i) 0))
    (caps : ∀ i j l : Fin k, i < j → j < l →
      orient (projectFrom a (p i)) (projectFrom a (p j)) (projectFrom a (p l)) < 0)
    {S : Finset Point} (root : a ∈ S) (inside : ∀ i, p i ∈ S) :
    HasConvexNGon (k + 1) S := by
  have hinj : Function.Injective p := fun i j h =>
    ordered.injective (congrArg (fun z => projectFrom a z 0) h)
  have hroot : a ∉ Set.range p := by
    rintro ⟨i, hi⟩
    have h := right i
    rw [hi] at h
    exact (lt_irrefl _ h)
  let q : Fin (k + 1) → Point := Fin.cons a p
  have hq : Function.Injective q := Fin.cons_injective_of_injective hroot hinj
  apply hasConvexNGon_of_positive_cycle (by omega) q hq (Function.Embedding.refl _) ?_ ?_
  · intro i
    cases i using Fin.cases with
    | zero => exact root
    | succ i => exact inside i
  · intro i j l hij hjl
    change 0 < orient (q i) (q j) (q l)
    cases i using Fin.cases <;> cases j using Fin.cases <;> cases l using Fin.cases
    all_goals simp only [Fin.succ_lt_succ_iff, Fin.not_lt_zero] at hij hjl
    · exact (projectFrom_x_lt_iff a _ _ (right _) (right _)).mp
        (ordered (by simpa using hjl))
    · exact (orient_projectFrom_neg_iff a _ _ _ (right _) (right _) (right _)).mp
        (caps _ _ _ (by simpa using hij) (by simpa using hjl))

/-- Enumerate every point of a finite general-position set with distinct
abscissae, retaining the exact cardinality and the full point set. -/
theorem exists_configuration (S : Finset Point) (gp : GeneralPosition S)
    (distinctX : ∀ a ∈ S, ∀ b ∈ S, a 0 = b 0 → a = b) :
    ∃ c : Configuration S.card, Finset.univ.image c.point = S := by
  classical
  let X := S.image (fun p => p 0)
  have hinj : Set.InjOn (fun p : Point => p 0) (S : Set Point) := distinctX
  have hc : X.card = S.card := Finset.card_image_of_injOn hinj
  let e := X.orderEmbOfFin hc
  have hget (i : Fin S.card) : ∃ p ∈ S, p 0 = e i :=
    Finset.mem_image.mp (Finset.orderEmbOfFin_mem X hc i)
  choose p hmem he using hget
  have hx : StrictMono (fun i => p i 0) := by
    intro i j hij
    change p i 0 < p j 0
    rw [he i, he j]
    exact e.strictMono hij
  have hp : Function.Injective p := fun i j h => hx.injective (congrArg (· 0) h)
  have image : Finset.univ.image p = S := by
    apply Finset.eq_of_subset_of_card_le
    · rintro q hq
      obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hq
      exact hmem i
    · simp [Finset.card_image_of_injective _ hp]
  exact ⟨Configuration.ofGeneralPosition p hx (by rwa [image]), image⟩

/-- If every chart point comes from the right of a retained root, an avoided
polygon in the original set rules out the corresponding cap in the chart. -/
theorem Configuration.no_cap_of_projected_image {n k : ℕ} (hk : 3 ≤ k)
    (c : Configuration n) (a : Point) (R S : Finset Point)
    (root : a ∈ S) (subset : R ⊆ S) (right : ∀ p ∈ R, a 0 < p 0)
    (chart : ∀ i, c.point i ∈ R.image (projectFrom a))
    (avoid : ¬ HasConvexNGon (k + 1) S) : ¬ c.HasCap k := by
  classical
  rintro ⟨f, hf, cap⟩
  have preimage (i : Fin k) : ∃ p ∈ R, projectFrom a p = c.point (f i) :=
    Finset.mem_image.mp (chart (f i))
  choose p hp he using preimage
  apply avoid
  apply root_cap_polygon hk a p (fun i => right _ (hp i)) ?_ ?_ root
    (fun i => subset (hp i))
  · intro i j hij
    change projectFrom a (p i) 0 < projectFrom a (p j) 0
    rw [he i, he j]
    exact c.xOrder (hf hij)
  · intro i j l hij hjl
    rw [he i, he j, he l]
    exact cap i j l hij hjl

/-- Normalize all non-root points into an ordered chart, with cardinality
unchanged. Octagon avoidance in the original set implies both octagon and
7-cap avoidance in this chart; no partition or population bound is used. -/
theorem exists_projective_chart (a : Point) (R : Finset Point)
    (gp : GeneralPosition (insert a R)) (right : ∀ p ∈ R, a 0 < p 0)
    (avoid : ¬ HasConvexNGon 8 (insert a R)) :
    ∃ n : ℕ, ∃ c : Configuration n, n = R.card ∧
      Finset.univ.image c.point = R.image (projectFrom a) ∧
      ¬ c.HasCap 7 ∧ ¬ HasConvexNGon 8 (Finset.univ.image c.point) := by
  classical
  have gpR : GeneralPosition R := gp.mono (Finset.subset_insert _ _)
  have gpChart := generalPosition_projectFrom a gpR right
  have distinctX : ∀ p ∈ R.image (projectFrom a), ∀ q ∈ R.image (projectFrom a),
      p 0 = q 0 → p = q := by
    intro p hp q hq he
    obtain ⟨u, hu, rfl⟩ := Finset.mem_image.mp hp
    obtain ⟨v, hv, rfl⟩ := Finset.mem_image.mp hq
    by_cases huv : u = v
    · rw [huv]
    · exact False.elim (projectFrom_distinct_x a gp right hu hv huv he)
  obtain ⟨c, image⟩ := exists_configuration _ gpChart distinctX
  have hcard : (R.image (projectFrom a)).card = R.card :=
    Finset.card_image_of_injOn ((projectFrom_injOn a).mono (fun p hp => right p hp))
  refine ⟨_, c, hcard, image, ?_, ?_⟩
  · exact c.no_cap_of_projected_image (by omega : 3 ≤ 7) a R (insert a R)
      (Finset.mem_insert_self _ _) (Finset.subset_insert _ _) right
      (fun i => image.le (Finset.mem_image_of_mem c.point (Finset.mem_univ i))) avoid
  · intro octagon
    rw [image] at octagon
    exact avoid ((hasConvexNGon_of_projectFrom a (by omega) gpR right octagon).mono
      (Finset.subset_insert _ _))

/-- The configuration is the actual image obtained by an invertible linear
normalization, deletion of a leftmost root, and projection from that root.
This retains the relation to the original set, not just its cardinality. -/
def IsRootDeletionChart {n : ℕ} (S : Finset Point) (c : Configuration n) : Prop :=
  ∃ e : Point ≃ₗ[ℝ] Point, ∃ a : Point, a ∈ S.image e ∧
    (∀ p ∈ (S.image e).erase a, a 0 < p 0) ∧
    Finset.univ.image c.point = ((S.image e).erase a).image (projectFrom a)

/-- Every nonempty octagon-free real set in general position has a chart with
exactly one fewer point, no 7-cap, and no convex octagon. Coordinates are first
normalized by the existing invertible linear map; no x-order hypothesis is
imposed on the original set. -/
theorem exists_cap_free_chart (S : Finset Point) (gp : GeneralPosition S)
    (nonempty : S.Nonempty) (avoid : ¬ HasConvexNGon 8 S) :
    ∃ n : ℕ, ∃ c : Configuration n, S.card = n + 1 ∧ IsRootDeletionChart S c ∧
      ¬ c.HasCap 7 ∧ ¬ HasConvexNGon 8 (Finset.univ.image c.point) := by
  classical
  obtain ⟨e, gpT, distinct⟩ := Suk.exists_horizontal_image S gp
  let T := S.image e
  have avoidT : ¬ HasConvexNGon 8 T := by
    intro h
    apply avoid
    simpa [T, Finset.image_image, Function.comp_def] using h.linearEquiv e.symm
  obtain ⟨a, ha, least⟩ := T.exists_min_image (fun p : Point => p 0) (nonempty.image e)
  let R := T.erase a
  have insert_eq : insert a R = T := Finset.insert_erase ha
  have right : ∀ p ∈ R, a 0 < p 0 := by
    intro p hp
    have hmem := Finset.mem_erase.mp hp
    apply lt_of_le_of_ne (least p hmem.2)
    intro he
    exact hmem.1 (distinct a ha p hmem.2 he).symm
  obtain ⟨n, c, count, image, noCap, noOctagon⟩ := exists_projective_chart a R
    (by rwa [insert_eq]) right (by rwa [insert_eq])
  refine ⟨n, c, ?_, ⟨e, a, ha, right, image⟩, noCap, noOctagon⟩
  have hT : T.card = S.card := Finset.card_image_of_injective _ e.injective
  have hR : R.card + 1 = T.card := Finset.card_erase_add_one ha
  omega

/-- The only population hypothesis needed by the global transfer: a bound
for ordered real configurations avoiding 7-caps and convex octagons. This is
a proposition parameter, not an axiom or an asserted finite bound. -/
def AsymmetricBound (B : ℕ) : Prop :=
  ∀ n : ℕ, ∀ c : Configuration n, ¬ c.HasCap 7 →
    ¬ HasConvexNGon 8 (Finset.univ.image c.point) → n ≤ B

theorem avoiding_card_le_of_asymmetric_bound {B : ℕ} (bound : AsymmetricBound B)
    (S : Finset Point) (gp : GeneralPosition S) (avoid : ¬ HasConvexNGon 8 S) :
    S.card ≤ B + 1 := by
  rcases S.eq_empty_or_nonempty with rfl | nonempty
  · simp
  · obtain ⟨n, c, count, _, noCap, noOctagon⟩ := exists_cap_free_chart S gp nonempty avoid
    have h := bound n c noCap noOctagon
    omega

/-- Exact global threshold bookkeeping: the deleted root and the strict
forcing threshold contribute one point each. -/
theorem forces_of_asymmetric_bound {B : ℕ} (bound : AsymmetricBound B) :
    ForcesConvexNGon (B + 2) 8 := by
  intro S gp size
  by_contra avoid
  have h := avoiding_card_le_of_asymmetric_bound bound S gp avoid
  omega

/-- Conditional target reduction. The hypothesis `AsymmetricBound 315` is
still unproved; this theorem discharges the entire projective/root transfer. -/
theorem forces_317_of_asymmetric_315 (bound : AsymmetricBound 315) :
    ForcesConvexNGon 317 8 := forces_of_asymmetric_bound bound

end ErdosSzekeres.Omission

import N66Geo.MirrorA
import ErdosSzekeres.Suk.Reflection

/-!
# N66Geo.MirrorB: G4, the mirror image (x, y) ↦ (x, −y)

* `profOf_swap`, `idxOf_swap`: under negated colors every point's state is the transposed state, whose index is
  `τ` of the old one (`N66Enc.tauList_spec`).
* `reflectConf`: the reflected configuration; its triple colors are negated (`Suk.orient_reflectY`), it stays in the
  class (caps and cups exchange; `Suk.hasConvexNGon_of_reflectY`).
* `mirror_holds`: the field `mirror` of `Gaps5`.
-/

namespace N66Geo
open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks N66Enc

/-! ## The τ tables (kernel checks on 70 entries) -/

def tauChecks : Bool :=
  (List.range 70).all fun k =>
    decide (tauList.getD k 0 < 70) && decide (tauList.getD (tauList.getD k 0) 0 = k) &&
      decide (stateList.idxOf (stateList.getD k (0, 0, 0, 0)) = k)

theorem tauChecks_true : tauChecks = true := by decide +kernel

theorem tau_facts {k : ℕ} (hk : k < 70) : tauList.getD k 0 < 70 ∧ tauList.getD (tauList.getD k 0) 0 = k ∧
    stateList.idxOf (stateList.getD k (0, 0, 0, 0)) = k := by
  have h := List.all_eq_true.1 tauChecks_true k (List.mem_range.2 hk)
  simp only [Bool.and_eq_true, decide_eq_true_eq] at h
  exact ⟨h.1.1, h.1.2, h.2⟩

theorem tau_val (s : Fin 70) : (tau s).val = tauList.getD s.val 0 := by
  unfold tau
  exact Nat.mod_eq_of_lt (tau_facts s.isLt).1

theorem tau_tau (s : Fin 70) : tau (tau s) = s := by
  apply Fin.ext
  rw [tau_val, tau_val]
  exact (tau_facts s.isLt).2.1

/-! ## Transposed states -/

variable {n : ℕ} {cup cup' : ℕ → ℕ → ℕ → Bool}

theorem filter4_length (c0 c1 c2 c3 x : ℕ) (f : ℕ → ℕ) (h0 : f 0 = c0) (h1 : f 1 = c1) (h2 : f 2 = c2) (h3 : f 3 = c3) :
    ((List.range 4).filter (fun a => decide (x ≤ f a))).length =
      (if x ≤ c0 then 1 else 0) + (if x ≤ c1 then 1 else 0) + (if x ≤ c2 then 1 else 0) +
        (if x ≤ c3 then 1 else 0) := by
  rw [show List.range 4 = [0, 1, 2, 3] from rfl]
  simp only [List.filter_cons, List.filter_nil, h0, h1, h2, h3]
  by_cases a : x ≤ c0 <;> by_cases b : x ≤ c1 <;> by_cases c : x ≤ c2 <;> by_cases d : x ≤ c3 <;>
    simp [a, b, c, d]

theorem profOf_swap (hneg : ∀ i j k, i < j → j < k → k < n → cup' i j k = !cup i j k) {v : ℕ} (hv : v < n)
    (hb : ∀ u < v, (labels cup u v).1 ≤ 4) : profOf cup' v = (profOf cup v).transpose := by
  have hc := fun i => column_swap hneg hv hb i
  unfold profOf Prof.transpose
  simp only [hc]
  refine Prod.ext ?_ (Prod.ext ?_ (Prod.ext ?_ ?_)) <;>
    exact filter4_length _ _ _ _ _ (column cup v) rfl rfl rfl rfl

/-- **The index of the transposed state is τ of the index.** -/
theorem idxOf_swap (hneg : ∀ i j k, i < j → j < k → k < n → cup' i j k = !cup i j k) {v : ℕ} (hv : v < n)
    (hb : ∀ u < v, (labels cup u v).1 ≤ 4) (hmem : profOf cup v ∈ stateList) :
    idxOf cup' v = tauList.getD (idxOf cup v) 0 := by
  have ht : idxOf cup v < 70 := by
    have := List.idxOf_lt_length_of_mem hmem
    rwa [stateList_length] at this
  have hget : stateList.getD (idxOf cup v) (0, 0, 0, 0) = profOf cup v := by
    rw [List.getD_eq_getElem _ _ (by rw [stateList_length]; exact ht)]
    exact EncB.getElem_idxOf _
  have hspec := tauList_spec (idxOf cup v) ht
  rw [hget] at hspec
  unfold idxOf
  rw [profOf_swap hneg hv hb, ← hspec]
  exact (tau_facts (tau_facts ht).1).2.2

/-! ## The reflected configuration -/

/-- The mirror image `(x, y) ↦ (x, −y)` of a configuration. -/
noncomputable def reflectConf (c : Configuration n) : Configuration n where
  point := fun i => Suk.reflectY (c.point i)
  xOrder := fun i j h => by simpa using c.xOrder h
  generalPosition := fun i j k hij hjk => by
    rw [Suk.orient_reflectY]
    exact neg_ne_zero.2 (c.generalPosition i j k hij hjk)

theorem reflect_cup (c : Configuration n) : ∀ i j k, i < j → j < k → k < n →
    (reflectConf c).cup i j k = !c.cup i j k := by
  intro i j k hij hjk hk
  have hi : i < n := by omega
  have hj : j < n := by omega
  have e1 : (reflectConf c).cup i j k = (reflectConf c).cup (⟨i, hi⟩ : Fin n) (⟨j, hj⟩ : Fin n) (⟨k, hk⟩ : Fin n) := rfl
  have e2 : c.cup i j k = c.cup (⟨i, hi⟩ : Fin n) (⟨j, hj⟩ : Fin n) (⟨k, hk⟩ : Fin n) := rfl
  rw [e1, e2]
  have hgp := c.generalPosition ⟨i, hi⟩ ⟨j, hj⟩ ⟨k, hk⟩ (by simpa using hij) (by simpa using hjk)
  apply Bool.eq_iff_iff.2
  rw [Configuration.cup_true_iff]
  change 0 < orient (Suk.reflectY _) (Suk.reflectY _) (Suk.reflectY _) ↔ _
  rw [Suk.orient_reflectY]
  cases h : c.cup (⟨i, hi⟩ : Fin n) (⟨j, hj⟩ : Fin n) (⟨k, hk⟩ : Fin n)
  · have := (Configuration.cup_false_iff c _ _ _ (by simpa using hij) (by simpa using hjk)).1 h
    simp only [Bool.not_false, iff_true]
    linarith
  · have := (Configuration.cup_true_iff c _ _ _).1 h
    simp only [Bool.not_true, Bool.false_eq_true, iff_false, not_lt]
    linarith

theorem reflect_noCap {c : Configuration n} (h : ¬ c.HasCup 6) : ¬ (reflectConf c).HasCap 6 := by
  rintro ⟨f, hf, hcap⟩
  apply h
  refine ⟨f, hf, fun i j l hij hjl => ?_⟩
  have := hcap i j l hij hjl
  change orient (Suk.reflectY _) (Suk.reflectY _) (Suk.reflectY _) < 0 at this
  rw [Suk.orient_reflectY] at this
  linarith

theorem reflect_noCup {c : Configuration n} (h : ¬ c.HasCap 6) : ¬ (reflectConf c).HasCup 6 := by
  rintro ⟨f, hf, hcup⟩
  apply h
  refine ⟨f, hf, fun i j l hij hjl => ?_⟩
  have := hcup i j l hij hjl
  change 0 < orient (Suk.reflectY _) (Suk.reflectY _) (Suk.reflectY _) at this
  rw [Suk.orient_reflectY] at this
  linarith

theorem reflect_noOct {c : Configuration n} (h : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) :
    ¬ HasConvexNGon 8 (Finset.univ.image (reflectConf c).point) := by
  intro hc
  apply h
  apply Suk.hasConvexNGon_of_reflectY
  have : Finset.univ.image (reflectConf c).point = (Finset.univ.image c.point).image Suk.reflectY := by
    rw [Finset.image_image]; rfl
  rwa [← this]

theorem labels_le_four_of_class {c : Configuration n} (hc : InClass c) {u v : ℕ} (huv : u < v) (hv : v < n) :
    (labels c.cup u v).1 ≤ 4 := by
  have := rank_lt_of_avoids n c.cup false 6 (by omega) (c.avoids_of_noCap hc.1) u v huv hv
  simp only [labels]
  omega

/-- Every point's profile is a state, from the two Avoids facts alone (no `Model` needed). -/
theorem profOf_mem_of_avoids {cup : ℕ → ℕ → ℕ → Bool} (h1 : Avoids n cup false 6) (h2 : Avoids n cup true 6)
    {v : ℕ} (hv : v < n) : profOf cup v ∈ stateList := by
  have hcol : ∀ i, column cup v i ≤ 4 := by
    intro i
    unfold column
    apply Finset.sup_le
    intro u hu
    have hu' := Finset.mem_range.1 hu
    have c1 := rank_lt_of_avoids n cup false 6 (by omega) h1 u v hu' hv
    have c2 := rank_lt_of_avoids n cup true 6 (by omega) h2 u v hu' hv
    simp only [labels]
    split_ifs <;> omega
  have anti := column_antitone cup v
  exact mem_stateList_of_bounds _ (by have := hcol 0; omega) _ (by have := hcol 1; omega) _
    (by have := hcol 2; omega) _ (by have := hcol 3; omega) (anti (show 0 ≤ 1 by omega))
    (anti (show 1 ≤ 2 by omega)) (anti (show 2 ≤ 3 by omega))

/-- **G4.** -/
theorem mirror_holds : ∀ n (c : Configuration n), InClass c → ∃ c' : Configuration n, InClass c' ∧
    ∀ s, n66Occ c'.cup n s ↔ n66Occ c.cup n (tau s) := by
  intro n c hc
  refine ⟨reflectConf c, ⟨reflect_noCap hc.2.1, reflect_noCup hc.1, reflect_noOct hc.2.2⟩, fun s => ?_⟩
  have hidx : ∀ v < n, idxOf (reflectConf c).cup v = tauList.getD (idxOf c.cup v) 0 := fun v hv =>
    idxOf_swap (reflect_cup c) hv (fun u hu => labels_le_four_of_class hc hu hv)
      (profOf_mem_of_avoids (c.avoids_of_noCap hc.1) (c.avoids_of_noCup hc.2.1) hv)
  have hlt : ∀ v < n, idxOf c.cup v < 70 := fun v hv => by
    have := List.idxOf_lt_length_of_mem
      (profOf_mem_of_avoids (c.avoids_of_noCap hc.1) (c.avoids_of_noCup hc.2.1) hv)
    rwa [stateList_length] at this
  constructor
  · rintro ⟨v, hv, he⟩
    refine ⟨v, hv, ?_⟩
    rw [hidx v hv] at he
    rw [tau_val, ← he]
    exact ((tau_facts (hlt v hv)).2.1).symm
  · rintro ⟨v, hv, he⟩
    refine ⟨v, hv, ?_⟩
    rw [hidx v hv, he, tau_val]
    exact (tau_facts s.isLt).2.1

end N66Geo

#print axioms N66Geo.idxOf_swap
#print axioms N66Geo.mirror_holds

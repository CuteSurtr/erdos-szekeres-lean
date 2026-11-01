import Mathlib

/-!
# Theorem A (mirror reduction), formal check

Mirror axis = x-axis, reflection `mu (x,y) = (x,-y)`.  Points are `ℝ × ℝ`.

* `ConvexPos T`  : every point of the finite set `T` lies outside the convex hull of the others.
* `HasGon n S`   : `S` has `n` points in convex position.
* `IsCapSeq m c` : `c 0, …, c (m-1)` have strictly increasing x and every consecutive triple is clockwise.
* `InClass n a b X` : `X` is x-distinct, in general position, with no `n` points in convex position,
                      no `a`-cap and no `b`-cup  (the class whose maximum size is `N(n,a,b)`).
-/

namespace MirrorA

open Set Finset

noncomputable section

/-- twice the signed area of `(p,q,r)` -/
def orient (p q r : ℝ × ℝ) : ℝ := (q.1 - p.1) * (r.2 - p.2) - (q.2 - p.2) * (r.1 - p.1)

/-- the reflection in the x-axis -/
def mu (p : ℝ × ℝ) : ℝ × ℝ := (p.1, -p.2)

@[simp] lemma mu_fst (p : ℝ × ℝ) : (mu p).1 = p.1 := rfl
@[simp] lemma mu_snd (p : ℝ × ℝ) : (mu p).2 = -p.2 := rfl
@[simp] lemma mu_mu (p : ℝ × ℝ) : mu (mu p) = p := by simp [mu]

lemma mu_injective : Function.Injective mu := fun p q h => by
  have := congrArg mu h; simpa using this

/-- `mu` as a linear map -/
def muL : (ℝ × ℝ) →ₗ[ℝ] (ℝ × ℝ) := LinearMap.prod (LinearMap.fst ℝ ℝ ℝ) (-(LinearMap.snd ℝ ℝ ℝ))

lemma muL_apply (p : ℝ × ℝ) : muL p = mu p := by
  simp [muL, mu]

/-! ## orientation identities -/

lemma orient_cyc (p q r : ℝ × ℝ) : orient p q r = orient q r p := by
  simp only [orient]; ring

lemma orient_mu3 (p q r : ℝ × ℝ) : orient p q (mu r) = orient p q r - 2 * r.2 * (q.1 - p.1) := by
  simp only [orient, mu]; ring

lemma orient_mu_all (p q r : ℝ × ℝ) : orient (mu p) (mu q) (mu r) = - orient p q r := by
  simp only [orient, mu]; ring

lemma orient_self2 (p q : ℝ × ℝ) : orient p q q = 0 := by
  simp only [orient]; ring

lemma orient_self1 (p q : ℝ × ℝ) : orient p q p = 0 := by
  simp only [orient]; ring

/-- four-point identity (I1) -/
lemma I1 (a b c d : ℝ × ℝ) :
    orient a b d * (c.1 - b.1) = orient a b c * (d.1 - b.1) + orient b c d * (b.1 - a.1) := by
  simp only [orient]; ring

/-- four-point identity (I2) -/
lemma I2 (a b c d : ℝ × ℝ) :
    orient a c d * (c.1 - b.1) = orient a b c * (d.1 - c.1) + orient b c d * (c.1 - a.1) := by
  simp only [orient]; ring

lemma orient_affine (p q x y : ℝ × ℝ) (a b : ℝ) (hab : a + b = 1) :
    orient p q (a • x + b • y) = a * orient p q x + b * orient p q y := by
  simp only [orient, Prod.fst_add, Prod.snd_add, Prod.smul_fst, Prod.smul_snd, smul_eq_mul]
  linear_combination ((q.1 - p.1) * p.2 - (q.2 - p.2) * p.1) * hab

/-! ## convex position and a lexicographic separation lemma -/

/-- `T` is in convex position: no point lies in the convex hull of the others. -/
def ConvexPos (T : Finset (ℝ × ℝ)) : Prop :=
  ∀ p ∈ T, p ∉ convexHull ℝ (↑(T.erase p) : Set (ℝ × ℝ))

lemma ConvexPos.mono {T U : Finset (ℝ × ℝ)} (hU : ConvexPos U) (hTU : T ⊆ U) : ConvexPos T := by
  intro p hp hcon
  apply hU p (hTU hp)
  refine convexHull_mono ?_ hcon
  intro z hz
  simp only [Finset.coe_erase, Set.mem_diff, Finset.mem_coe, Set.mem_singleton_iff] at hz ⊢
  exact ⟨hTU hz.1, hz.2⟩

/-- If two affine functions `φ, ψ` vanish at `v` and every point of `T` is lexicographically negative
for `(φ, ψ)`, then `v` is not in the convex hull of `T`. -/
lemma not_mem_convexHull_lex (T : Set (ℝ × ℝ)) (v : ℝ × ℝ) (φ ψ : ℝ × ℝ → ℝ)
    (hφ : ∀ x y : ℝ × ℝ, ∀ a b : ℝ, a + b = 1 → φ (a • x + b • y) = a * φ x + b * φ y)
    (hψ : ∀ x y : ℝ × ℝ, ∀ a b : ℝ, a + b = 1 → ψ (a • x + b • y) = a * ψ x + b * ψ y)
    (hv1 : φ v = 0) (hv2 : ψ v = 0)
    (hT : ∀ z ∈ T, φ z < 0 ∨ (φ z = 0 ∧ ψ z < 0)) : v ∉ convexHull ℝ T := by
  intro hv
  have hK : Convex ℝ {z : ℝ × ℝ | φ z < 0 ∨ (φ z = 0 ∧ ψ z < 0)} := by
    intro x hx y hy a b ha hb hab
    simp only [Set.mem_setOf_eq] at hx hy ⊢
    rw [hφ x y a b hab, hψ x y a b hab]
    have hx' : φ x ≤ 0 := by rcases hx with h | ⟨h, _⟩ <;> linarith
    have hy' : φ y ≤ 0 := by rcases hy with h | ⟨h, _⟩ <;> linarith
    have hax : a * φ x ≤ 0 := mul_nonpos_of_nonneg_of_nonpos ha hx'
    have hby : b * φ y ≤ 0 := mul_nonpos_of_nonneg_of_nonpos hb hy'
    rcases lt_or_eq_of_le (add_nonpos hax hby) with h | h
    · exact Or.inl h
    · right
      refine ⟨h, ?_⟩
      have h1 : a * φ x = 0 := by linarith
      have h2 : b * φ y = 0 := by linarith
      -- each weighted ψ-term is ≤ 0, and the one with positive weight is < 0
      have tx : a * ψ x ≤ 0 ∧ (0 < a → a * ψ x < 0) := by
        rcases eq_or_lt_of_le ha with ha0 | ha0
        · subst ha0; simp
        · have hφx : φ x = 0 := by
            rcases mul_eq_zero.mp h1 with h | h
            · linarith
            · exact h
          have hψx : ψ x < 0 := by
            rcases hx with h' | ⟨_, h'⟩
            · linarith
            · exact h'
          exact ⟨le_of_lt (mul_neg_of_pos_of_neg ha0 hψx), fun _ => mul_neg_of_pos_of_neg ha0 hψx⟩
      have ty : b * ψ y ≤ 0 ∧ (0 < b → b * ψ y < 0) := by
        rcases eq_or_lt_of_le hb with hb0 | hb0
        · subst hb0; simp
        · have hφy : φ y = 0 := by
            rcases mul_eq_zero.mp h2 with h | h
            · linarith
            · exact h
          have hψy : ψ y < 0 := by
            rcases hy with h' | ⟨_, h'⟩
            · linarith
            · exact h'
          exact ⟨le_of_lt (mul_neg_of_pos_of_neg hb0 hψy), fun _ => mul_neg_of_pos_of_neg hb0 hψy⟩
      rcases eq_or_lt_of_le ha with ha0 | ha0
      · have hb1 : 0 < b := by linarith
        linarith [ty.2 hb1, tx.1]
      · linarith [tx.2 ha0, ty.1]
  have hmem := convexHull_min (fun z hz => hT z hz) hK hv
  rcases hmem with h | ⟨_, h⟩ <;> linarith

lemma affine_fst_sub (x0 : ℝ) : ∀ x y : ℝ × ℝ, ∀ a b : ℝ, a + b = 1 →
    (a • x + b • y).1 - x0 = a * (x.1 - x0) + b * (y.1 - x0) := by
  intro x y a b hab
  simp only [Prod.fst_add, Prod.smul_fst, smul_eq_mul]
  linear_combination x0 * hab

lemma affine_snd_sub (y0 : ℝ) : ∀ x y : ℝ × ℝ, ∀ a b : ℝ, a + b = 1 →
    (a • x + b • y).2 - y0 = a * (x.2 - y0) + b * (y.2 - y0) := by
  intro x y a b hab
  simp only [Prod.snd_add, Prod.smul_snd, smul_eq_mul]
  linear_combination y0 * hab

lemma affine_sub_fst (x0 : ℝ) : ∀ x y : ℝ × ℝ, ∀ a b : ℝ, a + b = 1 →
    x0 - (a • x + b • y).1 = a * (x0 - x.1) + b * (x0 - y.1) := by
  intro x y a b hab
  simp only [Prod.fst_add, Prod.smul_fst, smul_eq_mul]
  linear_combination (-x0) * hab

/-! ## caps -/

/-- `c 0, …, c (m-1)` is a cap: strictly increasing x, consecutive triples clockwise. -/
def IsCapSeq (m : ℕ) (c : ℕ → ℝ × ℝ) : Prop :=
  (∀ i, i + 1 < m → (c i).1 < (c (i + 1)).1) ∧
  (∀ i, i + 2 < m → orient (c i) (c (i + 1)) (c (i + 2)) < 0)

/-- `c 0, …, c (m-1)` is a cup: strictly increasing x, consecutive triples counter-clockwise. -/
def IsCupSeq (m : ℕ) (c : ℕ → ℝ × ℝ) : Prop :=
  (∀ i, i + 1 < m → (c i).1 < (c (i + 1)).1) ∧
  (∀ i, i + 2 < m → 0 < orient (c i) (c (i + 1)) (c (i + 2)))

lemma xmono {m : ℕ} {c : ℕ → ℝ × ℝ} (h : ∀ i, i + 1 < m → (c i).1 < (c (i + 1)).1) :
    ∀ i j, i < j → j < m → (c i).1 < (c j).1 := by
  intro i j hij hjm
  induction j with
  | zero => omega
  | succ k ih =>
    rcases Nat.lt_succ_iff_lt_or_eq.mp hij with hik | hik
    · exact lt_trans (ih hik (by omega)) (h k (by omega))
    · subst hik; exact h i (by omega)

lemma injOn_of_xmono {m : ℕ} {c : ℕ → ℝ × ℝ} (h : ∀ i, i + 1 < m → (c i).1 < (c (i + 1)).1) :
    Set.InjOn c ↑(Finset.range m) := by
  intro i hi l hl hil
  simp only [Finset.coe_range, Set.mem_Iio] at hi hl
  by_contra hne
  rcases Nat.lt_or_gt_of_ne hne with h1 | h1
  · have := xmono h i l h1 hl; rw [hil] at this; exact lt_irrefl _ this
  · have := xmono h l i h1 hi; rw [hil] at this; exact lt_irrefl _ this

/-- every triple of a cap is clockwise (Lemma 2.1(b)). -/
lemma cap_all {m : ℕ} {c : ℕ → ℝ × ℝ} (hc : IsCapSeq m c) :
    ∀ i j l, i < j → j < l → l < m → orient (c i) (c j) (c l) < 0 := by
  have hx := xmono hc.1
  have key : ∀ d, ∀ i j l, l = i + d → i < j → j < l → l < m → orient (c i) (c j) (c l) < 0 := by
    intro d
    induction d using Nat.strong_induction_on with
    | _ d ih =>
      intro i j l hl hij hjl hlm
      by_cases hj : j = i + 1
      · subst hj
        by_cases hl2 : l = i + 2
        · subst hl2; exact hc.2 i hlm
        · -- l > i+2 : use I1 with a=c i, b=c(i+1), c=c(l-1), d=c l
          obtain ⟨l', rfl⟩ : ∃ l', l = l' + 1 := ⟨l - 1, by omega⟩
          have h1 : orient (c i) (c (i + 1)) (c l') < 0 :=
            ih (l' - i) (by omega) i (i + 1) l' (by omega) (by omega) (by omega) (by omega)
          have h2 : orient (c (i + 1)) (c l') (c (l' + 1)) < 0 :=
            ih (l' + 1 - (i + 1)) (by omega) (i + 1) l' (l' + 1) (by omega) (by omega) (by omega) hlm
          have e := I1 (c i) (c (i + 1)) (c l') (c (l' + 1))
          have p1 : 0 < (c l').1 - (c (i + 1)).1 := by linarith [hx (i + 1) l' (by omega) (by omega)]
          have p2 : 0 < (c (l' + 1)).1 - (c (i + 1)).1 := by linarith [hx (i + 1) (l' + 1) (by omega) hlm]
          have p3 : 0 < (c (i + 1)).1 - (c i).1 := by linarith [hx i (i + 1) (by omega) (by omega)]
          by_contra hneg
          push_neg at hneg
          nlinarith [mul_nonneg hneg (le_of_lt p1), mul_pos_of_neg_of_neg h1 (neg_neg_of_pos p2),
            mul_neg_of_neg_of_pos h2 p3, mul_neg_of_neg_of_pos h1 p2]
      · -- j > i+1 : use I2 with a=c i, b=c(i+1), c=c j, d=c l
        have h1 : orient (c i) (c (i + 1)) (c j) < 0 :=
          ih (j - i) (by omega) i (i + 1) j (by omega) (by omega) (by omega) (by omega)
        have h2 : orient (c (i + 1)) (c j) (c l) < 0 :=
          ih (l - (i + 1)) (by omega) (i + 1) j l (by omega) (by omega) hjl hlm
        have e := I2 (c i) (c (i + 1)) (c j) (c l)
        have p1 : 0 < (c j).1 - (c (i + 1)).1 := by linarith [hx (i + 1) j (by omega) (by omega)]
        have p2 : 0 < (c l).1 - (c j).1 := by linarith [hx j l hjl hlm]
        have p3 : 0 < (c j).1 - (c i).1 := by linarith [hx i j hij (by omega)]
        by_contra hneg
        push_neg at hneg
        nlinarith [mul_nonneg hneg (le_of_lt p1), mul_neg_of_neg_of_pos h1 p2, mul_neg_of_neg_of_pos h2 p3]
  intro i j l hij hjl hlm
  exact key (l - i) i j l (by omega) hij hjl hlm

/-! ## Lemma 3.1: a cap in the closed upper half-plane together with its mirror image -/

/-- the set `C ∪ mu(C)` for `C = {c 0, …, c (m-1)}` -/
def V (m : ℕ) (c : ℕ → ℝ × ℝ) : Finset (ℝ × ℝ) :=
  (Finset.range m).image c ∪ (Finset.range m).image (fun i => mu (c i))

lemma mem_V {m : ℕ} {c : ℕ → ℝ × ℝ} {z : ℝ × ℝ} :
    z ∈ V m c ↔ (∃ i, i < m ∧ c i = z) ∨ (∃ i, i < m ∧ mu (c i) = z) := by
  simp [V]

lemma V_mu_mem {m : ℕ} {c : ℕ → ℝ × ℝ} {z : ℝ × ℝ} (hz : z ∈ V m c) : mu z ∈ V m c := by
  rcases mem_V.mp hz with ⟨i, hi, rfl⟩ | ⟨i, hi, rfl⟩
  · exact mem_V.mpr (Or.inr ⟨i, hi, rfl⟩)
  · exact mem_V.mpr (Or.inl ⟨i, hi, by simp⟩)

/-- edge fact: every point of `V` other than `c i, c (i+1)` is strictly right of the directed line
`c i → c (i+1)` (only `y ≥ 0` is assumed). -/
lemma edge_fact {m : ℕ} {c : ℕ → ℝ × ℝ} (hc : IsCapSeq m c) (hy : ∀ i, i < m → 0 ≤ (c i).2)
    (i : ℕ) (hi : i + 1 < m) (z : ℝ × ℝ) (hz : z ∈ V m c) (h1 : z ≠ c i) (h2 : z ≠ c (i + 1)) :
    orient (c i) (c (i + 1)) z < 0 := by
  have hdx : 0 < (c (i + 1)).1 - (c i).1 := by linarith [hc.1 i hi]
  have upper : ∀ l, l < m → l ≠ i → l ≠ i + 1 → orient (c i) (c (i + 1)) (c l) < 0 := by
    intro l hl hli hli1
    rcases Nat.lt_or_gt_of_ne hli with hlt | hgt
    · rw [orient_cyc, orient_cyc]
      exact cap_all hc l i (i + 1) hlt (by omega) hi
    · exact cap_all hc i (i + 1) l (by omega) (by omega) hl
  rcases mem_V.mp hz with ⟨l, hl, rfl⟩ | ⟨l, hl, rfl⟩
  · exact upper l hl (fun h => h1 (by rw [h])) (fun h => h2 (by rw [h]))
  · rw [orient_mu3]
    by_cases hli : l = i
    · subst hli
      rw [orient_self1]
      have hpos : 0 < (c l).2 := by
        rcases lt_or_eq_of_le (hy l hl) with h | h
        · exact h
        · exfalso; apply h1; ext <;> simp [mu, ← h]
      nlinarith
    · by_cases hli1 : l = i + 1
      · subst hli1
        rw [orient_self2]
        have hpos : 0 < (c (i + 1)).2 := by
          rcases lt_or_eq_of_le (hy (i + 1) hl) with h | h
          · exact h
          · exfalso; apply h2; ext <;> simp [mu, ← h]
        nlinarith
      · have h3 := upper l hl hli hli1
        have h4 := hy l hl
        nlinarith

/-- **Lemma 3.1.** If `c` is a cap with all heights `≥ 0`, then `C ∪ mu(C)` is in convex position. -/
theorem lemma31 {m : ℕ} {c : ℕ → ℝ × ℝ} (hc : IsCapSeq m c) (hy : ∀ i, i < m → 0 ≤ (c i).2) :
    ConvexPos (V m c) := by
  have hx := xmono hc.1
  have hup : ∀ i, i < m → c i ∉ convexHull ℝ (↑((V m c).erase (c i)) : Set (ℝ × ℝ)) := by
    intro i hi
    by_cases hlast : i + 1 < m
    · apply not_mem_convexHull_lex _ (c i) (fun z => orient (c i) (c (i + 1)) z)
        (fun z => (c i).1 - z.1)
      · intro x y a b hab; exact orient_affine _ _ x y a b hab
      · exact affine_sub_fst (c i).1
      · exact orient_self1 _ _
      · simp
      · intro z hz
        simp only [Finset.coe_erase, Set.mem_diff, Finset.mem_coe, Set.mem_singleton_iff] at hz
        by_cases hz2 : z = c (i + 1)
        · right
          subst hz2
          refine ⟨orient_self2 _ _, ?_⟩
          show (c i).1 - (c (i + 1)).1 < 0
          linarith [hc.1 i hlast]
        · left
          exact edge_fact hc hy i hlast z hz.1 hz.2 hz2
    · apply not_mem_convexHull_lex _ (c i) (fun z => z.1 - (c i).1) (fun z => z.2 - (c i).2)
      · exact affine_fst_sub (c i).1
      · exact affine_snd_sub (c i).2
      · simp
      · simp
      · intro z hz
        simp only [Finset.coe_erase, Set.mem_diff, Finset.mem_coe, Set.mem_singleton_iff] at hz
        rcases mem_V.mp hz.1 with ⟨l, hl, rfl⟩ | ⟨l, hl, rfl⟩
        · left
          have hli : l ≠ i := fun h => hz.2 (by rw [h])
          have hlt : l < i := by omega
          show (c l).1 - (c i).1 < 0
          linarith [hx l i hlt hi]
        · by_cases hli : l = i
          · subst hli
            right
            have hpos : 0 < (c l).2 := by
              rcases lt_or_eq_of_le (hy l hl) with h | h
              · exact h
              · exfalso; apply hz.2; ext <;> simp [mu, ← h]
            constructor
            · show (mu (c l)).1 - (c l).1 = 0
              simp
            · show (mu (c l)).2 - (c l).2 < 0
              simp only [mu_snd]
              linarith
          · left
            have hlt : l < i := by omega
            show (mu (c l)).1 - (c i).1 < 0
            simp only [mu_fst]
            linarith [hx l i hlt hi]
  intro p hp
  rcases mem_V.mp hp with ⟨i, hi, rfl⟩ | ⟨i, hi, rfl⟩
  · exact hup i hi
  · intro hcon
    apply hup i hi
    have h1 := Set.mem_image_of_mem muL hcon
    rw [LinearMap.image_convexHull, muL_apply, mu_mu] at h1
    refine convexHull_mono ?_ h1
    rintro w ⟨u, hu, rfl⟩
    simp only [Finset.coe_erase, Set.mem_diff, Finset.mem_coe, Set.mem_singleton_iff] at hu ⊢
    rw [muL_apply]
    refine ⟨V_mu_mem hu.1, ?_⟩
    intro h
    apply hu.2
    rw [← h, mu_mu]

/-- the points of a cap alone are in convex position -/
theorem cap_convexPos {m : ℕ} {c : ℕ → ℝ × ℝ} (hc : IsCapSeq m c) :
    ConvexPos ((Finset.range m).image c) := by
  have hx := xmono hc.1
  intro p hp
  obtain ⟨i, hi, rfl⟩ := Finset.mem_image.mp hp
  rw [Finset.mem_range] at hi
  by_cases hlast : i + 1 < m
  · apply not_mem_convexHull_lex _ (c i) (fun z => orient (c i) (c (i + 1)) z) (fun z => (c i).1 - z.1)
    · intro x y a b hab; exact orient_affine _ _ x y a b hab
    · exact affine_sub_fst (c i).1
    · exact orient_self1 _ _
    · simp
    · intro z hz
      simp only [Finset.coe_erase, Set.mem_diff, Finset.mem_coe, Set.mem_singleton_iff,
        Finset.mem_image, Finset.mem_range] at hz
      obtain ⟨⟨l, hl, rfl⟩, hne⟩ := hz
      by_cases hl1 : l = i + 1
      · subst hl1
        right
        refine ⟨orient_self2 _ _, ?_⟩
        show (c i).1 - (c (i + 1)).1 < 0
        linarith [hc.1 i hlast]
      · left
        have hli : l ≠ i := fun h => hne (by rw [h])
        show orient (c i) (c (i + 1)) (c l) < 0
        rcases Nat.lt_or_gt_of_ne hli with hlt | hgt
        · rw [orient_cyc, orient_cyc]; exact cap_all hc l i (i + 1) hlt (by omega) hlast
        · exact cap_all hc i (i + 1) l (by omega) (by omega) hl
  · apply not_mem_convexHull_lex _ (c i) (fun z => z.1 - (c i).1) (fun z => z.2 - (c i).2)
    · exact affine_fst_sub (c i).1
    · exact affine_snd_sub (c i).2
    · simp
    · simp
    · intro z hz
      simp only [Finset.coe_erase, Set.mem_diff, Finset.mem_coe, Set.mem_singleton_iff,
        Finset.mem_image, Finset.mem_range] at hz
      obtain ⟨⟨l, hl, rfl⟩, hne⟩ := hz
      left
      have hli : l ≠ i := fun h => hne (by rw [h])
      have hlt : l < i := by omega
      show (c l).1 - (c i).1 < 0
      linarith [hx l i hlt hi]

/-- convex position is preserved by the reflection -/
lemma convexPos_image_mu {T : Finset (ℝ × ℝ)} (hT : ConvexPos T) : ConvexPos (T.image mu) := by
  intro p hp hcon
  obtain ⟨q, hq, rfl⟩ := Finset.mem_image.mp hp
  apply hT q hq
  have h1 := Set.mem_image_of_mem muL hcon
  rw [LinearMap.image_convexHull, muL_apply, mu_mu] at h1
  refine convexHull_mono ?_ h1
  rintro w ⟨u, hu, rfl⟩
  simp only [Finset.coe_erase, Set.mem_diff, Finset.mem_coe, Set.mem_singleton_iff,
    Finset.mem_image] at hu ⊢
  obtain ⟨⟨u', hu', rfl⟩, hne⟩ := hu
  rw [muL_apply, mu_mu]
  exact ⟨hu', fun h => hne (by rw [h])⟩

lemma cap_of_cup {m : ℕ} {c : ℕ → ℝ × ℝ} (hc : IsCupSeq m c) : IsCapSeq m (fun i => mu (c i)) := by
  refine ⟨fun i hi => by simpa using hc.1 i hi, fun i hi => ?_⟩
  show orient (mu (c i)) (mu (c (i + 1))) (mu (c (i + 2))) < 0
  rw [orient_mu_all]
  linarith [hc.2 i hi]

/-- the points of a cup are in convex position -/
theorem cup_convexPos {m : ℕ} {c : ℕ → ℝ × ℝ} (hc : IsCupSeq m c) :
    ConvexPos ((Finset.range m).image c) := by
  have h := convexPos_image_mu (cap_convexPos (cap_of_cup hc))
  rw [Finset.image_image] at h
  have e : (mu ∘ fun i => mu (c i)) = c := by funext i; simp
  rwa [e] at h

/-! ## Theorem A -/

/-- no three points collinear -/
def GenPos (S : Finset (ℝ × ℝ)) : Prop :=
  ∀ p ∈ S, ∀ q ∈ S, ∀ r ∈ S, p ≠ q → p ≠ r → q ≠ r → orient p q r ≠ 0

/-- distinct x-coordinates -/
def XDistinct (S : Finset (ℝ × ℝ)) : Prop := ∀ p ∈ S, ∀ q ∈ S, p.1 = q.1 → p = q

/-- `S` contains `n` points in convex position -/
def HasGon (n : ℕ) (S : Finset (ℝ × ℝ)) : Prop := ∃ T ⊆ S, T.card = n ∧ ConvexPos T

/-- `S` contains an `a`-cap -/
def HasCap (a : ℕ) (S : Finset (ℝ × ℝ)) : Prop :=
  ∃ c : ℕ → ℝ × ℝ, (∀ i, i < a → c i ∈ S) ∧ IsCapSeq a c

/-- `S` contains a `b`-cup -/
def HasCup (b : ℕ) (S : Finset (ℝ × ℝ)) : Prop :=
  ∃ c : ℕ → ℝ × ℝ, (∀ i, i < b → c i ∈ S) ∧ IsCupSeq b c

/-- the class whose largest size is `N(n,a,b)` -/
def InClass (n a b : ℕ) (X : Finset (ℝ × ℝ)) : Prop :=
  XDistinct X ∧ GenPos X ∧ ¬ HasGon n X ∧ ¬ HasCap a X ∧ ¬ HasCup b X

/-- invariant under the reflection in the x-axis -/
def MirrorSym (S : Finset (ℝ × ℝ)) : Prop := ∀ p ∈ S, mu p ∈ S

lemma GenPos.mono {S T : Finset (ℝ × ℝ)} (h : GenPos S) (hTS : T ⊆ S) : GenPos T :=
  fun p hp q hq r hr h1 h2 h3 => h p (hTS hp) q (hTS hq) r (hTS hr) h1 h2 h3

lemma XDistinct.mono {S T : Finset (ℝ × ℝ)} (h : XDistinct S) (hTS : T ⊆ S) : XDistinct T :=
  fun p hp q hq e => h p (hTS hp) q (hTS hq) e

lemma HasGon.mono {n : ℕ} {S T : Finset (ℝ × ℝ)} (h : HasGon n T) (hTS : T ⊆ S) : HasGon n S := by
  obtain ⟨U, hU, hc, hcp⟩ := h
  exact ⟨U, hU.trans hTS, hc, hcp⟩

lemma hasGon_of_card {n : ℕ} {S U : Finset (ℝ × ℝ)} (hU : U ⊆ S) (hcp : ConvexPos U)
    (hn : n ≤ U.card) : HasGon n S := by
  obtain ⟨T, hT, hTc⟩ := Finset.exists_subset_card_eq hn
  exact ⟨T, hT.trans hU, hTc, hcp.mono hT⟩

/-- a `b`-cup is a convex `b`-gon, so "no `b`-gon" implies "no `b`-cup" -/
lemma not_hasCup_of_not_hasGon {n : ℕ} {X : Finset (ℝ × ℝ)} (h : ¬ HasGon n X) : ¬ HasCup n X := by
  rintro ⟨c, hmem, hc⟩
  apply h
  refine hasGon_of_card (U := (Finset.range n).image c) ?_ (cup_convexPos hc) ?_
  · intro z hz
    obtain ⟨i, hi, rfl⟩ := Finset.mem_image.mp hz
    exact hmem i (Finset.mem_range.mp hi)
  · rw [Finset.card_image_of_injOn (injOn_of_xmono hc.1), Finset.card_range]

lemma V_subset {m : ℕ} {c : ℕ → ℝ × ℝ} {S : Finset (ℝ × ℝ)} (hsym : MirrorSym S)
    (hmem : ∀ i, i < m → c i ∈ S) : V m c ⊆ S := by
  intro z hz
  rcases mem_V.mp hz with ⟨i, hi, rfl⟩ | ⟨i, hi, rfl⟩
  · exact hmem i hi
  · exact hsym _ (hmem i hi)

/-- `|C ∪ mu(C)| ≥ m + #{i : height of c i > 0}` -/
lemma card_V_ge {m : ℕ} {c : ℕ → ℝ × ℝ} (hc : IsCapSeq m c) (hy : ∀ i, i < m → 0 ≤ (c i).2)
    (s : Finset ℕ) (hs : s ⊆ Finset.range m) (hpos : ∀ i ∈ s, 0 < (c i).2) :
    m + s.card ≤ (V m c).card := by
  have hinj := injOn_of_xmono hc.1
  have d : Disjoint ((Finset.range m).image c) (s.image (fun i => mu (c i))) := by
    rw [Finset.disjoint_left]
    intro z hz1 hz2
    obtain ⟨i, hi, rfl⟩ := Finset.mem_image.mp hz1
    obtain ⟨l, hl, hl'⟩ := Finset.mem_image.mp hz2
    have h2 := congrArg Prod.snd hl'
    simp only [mu_snd] at h2
    have h3 := hy i (Finset.mem_range.mp hi)
    have h4 := hpos l hl
    linarith
  have hsub : (Finset.range m).image c ∪ s.image (fun i => mu (c i)) ⊆ V m c := by
    intro z hz
    rcases Finset.mem_union.mp hz with h | h
    · exact Finset.mem_union_left _ h
    · apply Finset.mem_union_right
      obtain ⟨l, hl, rfl⟩ := Finset.mem_image.mp h
      exact Finset.mem_image.mpr ⟨l, hs hl, rfl⟩
  have hinj2 : Set.InjOn (fun i => mu (c i)) ↑s := by
    intro i hi l hl h
    exact hinj (hs hi) (hs hl) (mu_injective h)
  calc m + s.card
      = ((Finset.range m).image c).card + (s.image (fun i => mu (c i))).card := by
        rw [Finset.card_image_of_injOn hinj, Finset.card_image_of_injOn hinj2, Finset.card_range]
    _ = ((Finset.range m).image c ∪ s.image (fun i => mu (c i))).card :=
        (Finset.card_union_of_disjoint d).symm
    _ ≤ (V m c).card := Finset.card_le_card hsub

/-- (F2) the closed upper half of a mirror set in general position is x-distinct -/
lemma xdistinct_nonneg (S : Finset (ℝ × ℝ)) (hsym : MirrorSym S) (hgp : GenPos S) :
    XDistinct (S.filter (fun p => 0 ≤ p.2)) := by
  have col : ∀ p q : ℝ × ℝ, p.1 = q.1 → orient p q (mu p) = 0 := by
    intro p q e
    simp only [orient, mu, e]; ring
  -- a point with positive height and another point of the closed upper half with the same x
  have key : ∀ p ∈ S, ∀ q ∈ S, 0 < p.2 → 0 ≤ q.2 → p.1 = q.1 → p = q := by
    intro p hp q hq hp2 hq2 e
    by_contra hne
    apply hgp p hp q hq (mu p) (hsym p hp) hne
    · intro h; have := congrArg Prod.snd h; simp only [mu_snd] at this; linarith
    · intro h; have := congrArg Prod.snd h; simp only [mu_snd] at this; linarith
    · exact col p q e
  intro p hp q hq e
  simp only [Finset.mem_filter] at hp hq
  rcases lt_or_eq_of_le hp.2 with hp2 | hp2
  · exact key p hp.1 q hq.1 hp2 hq.2 e
  · rcases lt_or_eq_of_le hq.2 with hq2 | hq2
    · exact (key q hq.1 p hp.1 hq2 hp.2 e.symm).symm
    · exact Prod.ext e (by rw [← hp2, ← hq2])

/-- (F1) and the count `|S| ≤ 2|R| + |A|`, `|A| ≤ 2` -/
lemma card_mirror_le (S : Finset (ℝ × ℝ)) (hsym : MirrorSym S) (hgp : GenPos S) :
    S.card ≤ 2 * (S.filter (fun p => 0 < p.2)).card + (S.filter (fun p => p.2 = 0)).card ∧
    (S.filter (fun p => p.2 = 0)).card ≤ 2 := by
  constructor
  · have e1 : (S.filter (fun p => 0 < p.2)).card + (S.filter (fun p => ¬ 0 < p.2)).card = S.card :=
      Finset.filter_card_add_filter_neg_card_eq_card _
    have e2 : ((S.filter (fun p => ¬ 0 < p.2)).filter (fun p => p.2 = 0)).card +
        ((S.filter (fun p => ¬ 0 < p.2)).filter (fun p => ¬ p.2 = 0)).card =
        (S.filter (fun p => ¬ 0 < p.2)).card :=
      Finset.filter_card_add_filter_neg_card_eq_card _
    have i1 : ((S.filter (fun p => ¬ 0 < p.2)).filter (fun p => p.2 = 0)).card ≤
        (S.filter (fun p => p.2 = 0)).card := by
      apply Finset.card_le_card
      intro z hz
      simp only [Finset.mem_filter] at hz ⊢
      exact ⟨hz.1.1, hz.2⟩
    have i2 : ((S.filter (fun p => ¬ 0 < p.2)).filter (fun p => ¬ p.2 = 0)).card ≤
        (S.filter (fun p => 0 < p.2)).card := by
      apply Finset.card_le_card_of_injOn mu
      · intro z hz
        rw [Finset.mem_coe, Finset.mem_filter, Finset.mem_filter] at hz
        rw [Finset.mem_coe, Finset.mem_filter]
        refine ⟨hsym z hz.1.1, ?_⟩
        rw [mu_snd]
        have h1 := hz.1.2
        have h2 := hz.2
        push_neg at h1
        have : z.2 < 0 := lt_of_le_of_ne h1 h2
        linarith
      · intro x _ y _ h
        exact mu_injective h
    omega
  · by_contra hlt
    push_neg at hlt
    obtain ⟨p, hp, q, hq, r, hr, hpq, hpr, hqr⟩ := Finset.two_lt_card.mp hlt
    simp only [Finset.mem_filter] at hp hq hr
    apply hgp p hp.1 q hq.1 r hr.1 hpq hpr hqr
    simp only [orient, hp.2, hq.2, hr.2]; ring

/-- (F4) a `j`-cap in the closed upper half (at most one point on the axis) yields `2j - 1` points of
`S` in convex position, and `2j` points if no point of the cap is on the axis. -/
lemma cap_upper_gon {S : Finset (ℝ × ℝ)} (hsym : MirrorSym S) {j : ℕ} {c : ℕ → ℝ × ℝ}
    (hc : IsCapSeq j c) (hmem : ∀ i, i < j → c i ∈ S) (hy : ∀ i, i < j → 0 ≤ (c i).2)
    (k : ℕ) (hk : k + ((Finset.range j).filter (fun i => ¬ 0 < (c i).2)).card ≤ 2 * j) :
    HasGon k S := by
  refine hasGon_of_card (V_subset hsym hmem) (lemma31 hc hy) ?_
  have h1 := card_V_ge hc hy ((Finset.range j).filter (fun i => 0 < (c i).2))
    (Finset.filter_subset _ _) (fun i hi => (Finset.mem_filter.mp hi).2)
  have h3 : ((Finset.range j).filter (fun i => 0 < (c i).2)).card +
      ((Finset.range j).filter (fun i => ¬ 0 < (c i).2)).card = (Finset.range j).card :=
    Finset.filter_card_add_filter_neg_card_eq_card _
  rw [Finset.card_range] at h3
  omega

/-- **Theorem A (i)**, even case `k = 2j`.  (The hypothesis `2 ≤ j` is not needed in this case.) -/
theorem theoremA_even (j : ℕ) (_hj : 2 ≤ j) (S : Finset (ℝ × ℝ)) (hsym : MirrorSym S)
    (hgp : GenPos S) (hno : ¬ HasGon (2 * j) S) :
    ∃ X : Finset (ℝ × ℝ), InClass (2 * j) j (2 * j) X ∧ S.card ≤ 2 * X.card + 2 := by
  have hRS : S.filter (fun p => 0 < p.2) ⊆ S := Finset.filter_subset _ _
  obtain ⟨hcard, hA⟩ := card_mirror_le S hsym hgp
  refine ⟨S.filter (fun p => 0 < p.2), ⟨?_, hgp.mono hRS, fun h => hno (h.mono hRS), ?_, ?_⟩, by omega⟩
  · refine (xdistinct_nonneg S hsym hgp).mono ?_
    intro z hz
    simp only [Finset.mem_filter] at hz ⊢
    exact ⟨hz.1, le_of_lt hz.2⟩
  · rintro ⟨c, hmem, hc⟩
    apply hno
    have hpos : ∀ i, i < j → 0 < (c i).2 := fun i hi => (Finset.mem_filter.mp (hmem i hi)).2
    have h0 : ((Finset.range j).filter (fun i => ¬ 0 < (c i).2)).card = 0 := by
      rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
      intro i hi
      exact not_not.mpr (hpos i (Finset.mem_range.mp hi))
    exact cap_upper_gon hsym hc (fun i hi => hRS (hmem i hi)) (fun i hi => le_of_lt (hpos i hi))
      (2 * j) (by omega)
  · exact not_hasCup_of_not_hasGon (fun h => hno (h.mono hRS))

/-- **Theorem A (ii)**, odd case `k = 2j - 1`. -/
theorem theoremA_odd (j : ℕ) (hj : 2 ≤ j) (S : Finset (ℝ × ℝ)) (hsym : MirrorSym S)
    (hgp : GenPos S) (hno : ¬ HasGon (2 * j - 1) S) :
    ∃ X : Finset (ℝ × ℝ), InClass (2 * j - 1) j (2 * j - 1) X ∧ S.card ≤ 2 * X.card := by
  have hRS : S.filter (fun p => 0 < p.2) ⊆ S := Finset.filter_subset _ _
  obtain ⟨hcard, hA⟩ := card_mirror_le S hsym hgp
  by_cases hax : ∃ a ∈ S, a.2 = 0
  · obtain ⟨a, haS, ha0⟩ := hax
    have hXS : insert a (S.filter (fun p => 0 < p.2)) ⊆ S := Finset.insert_subset haS hRS
    have hX0 : ∀ p ∈ insert a (S.filter (fun p => 0 < p.2)), 0 ≤ p.2 := by
      intro p hp
      rcases Finset.mem_insert.mp hp with h | h
      · rw [h, ha0]
      · exact le_of_lt (Finset.mem_filter.mp h).2
    have hXpos : ∀ p ∈ insert a (S.filter (fun p => 0 < p.2)), p ≠ a → 0 < p.2 := by
      intro p hp hne
      rcases Finset.mem_insert.mp hp with h | h
      · exact absurd h hne
      · exact (Finset.mem_filter.mp h).2
    have haR : a ∉ S.filter (fun p => 0 < p.2) := by
      intro h
      have := (Finset.mem_filter.mp h).2
      linarith
    refine ⟨insert a (S.filter (fun p => 0 < p.2)),
      ⟨?_, hgp.mono hXS, fun h => hno (h.mono hXS), ?_, ?_⟩, ?_⟩
    · refine (xdistinct_nonneg S hsym hgp).mono ?_
      intro z hz
      rw [Finset.mem_filter]
      exact ⟨hXS hz, hX0 z hz⟩
    · rintro ⟨c, hmem, hc⟩
      apply hno
      have h2 : ((Finset.range j).filter (fun i => ¬ 0 < (c i).2)).card ≤ 1 := by
        rw [Finset.card_le_one]
        intro i hi l hl
        simp only [Finset.mem_filter, Finset.mem_range] at hi hl
        have ei : c i = a := by
          by_contra hne
          exact hi.2 (hXpos _ (hmem i hi.1) hne)
        have el : c l = a := by
          by_contra hne
          exact hl.2 (hXpos _ (hmem l hl.1) hne)
        exact injOn_of_xmono hc.1 (Finset.mem_range.mpr hi.1) (Finset.mem_range.mpr hl.1)
          (ei.trans el.symm)
      exact cap_upper_gon hsym hc (fun i hi => hXS (hmem i hi)) (fun i hi => hX0 _ (hmem i hi))
        (2 * j - 1) (by omega)
    · exact not_hasCup_of_not_hasGon (fun h => hno (h.mono hXS))
    · rw [Finset.card_insert_of_notMem haR]
      omega
  · push_neg at hax
    have hA0 : (S.filter (fun p => p.2 = 0)).card = 0 := by
      rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
      intro p hp
      exact hax p hp
    refine ⟨S.filter (fun p => 0 < p.2), ⟨?_, hgp.mono hRS, fun h => hno (h.mono hRS), ?_, ?_⟩, by omega⟩
    · refine (xdistinct_nonneg S hsym hgp).mono ?_
      intro z hz
      simp only [Finset.mem_filter] at hz ⊢
      exact ⟨hz.1, le_of_lt hz.2⟩
    · rintro ⟨c, hmem, hc⟩
      apply hno
      have hpos : ∀ i, i < j → 0 < (c i).2 := fun i hi => (Finset.mem_filter.mp (hmem i hi)).2
      have h0 : ((Finset.range j).filter (fun i => ¬ 0 < (c i).2)).card = 0 := by
        rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
        intro i hi
        exact not_not.mpr (hpos i (Finset.mem_range.mp hi))
      exact cap_upper_gon hsym hc (fun i hi => hRS (hmem i hi)) (fun i hi => le_of_lt (hpos i hi))
        (2 * j - 1) (by omega)
    · exact not_hasCup_of_not_hasGon (fun h => hno (h.mono hRS))

/-- Theorem A as stated in the claim: any upper bound `Nb` for the class `(2j, j, 2j)`
(in particular `Nb = N(2j,j,2j)`) gives `|S| ≤ 2 Nb + 2` for mirror sets without `2j`-gons. -/
theorem theoremA_even_bound (j : ℕ) (hj : 2 ≤ j) (Nb : ℕ)
    (hN : ∀ X : Finset (ℝ × ℝ), InClass (2 * j) j (2 * j) X → X.card ≤ Nb)
    (S : Finset (ℝ × ℝ)) (hsym : MirrorSym S) (hgp : GenPos S) (hno : ¬ HasGon (2 * j) S) :
    S.card ≤ 2 * Nb + 2 := by
  obtain ⟨X, hX, hc⟩ := theoremA_even j hj S hsym hgp hno
  have := hN X hX
  omega

/-- odd case: any upper bound `Nb` for the class `(2j-1, j, 2j-1)` gives `|S| ≤ 2 Nb`. -/
theorem theoremA_odd_bound (j : ℕ) (hj : 2 ≤ j) (Nb : ℕ)
    (hN : ∀ X : Finset (ℝ × ℝ), InClass (2 * j - 1) j (2 * j - 1) X → X.card ≤ Nb)
    (S : Finset (ℝ × ℝ)) (hsym : MirrorSym S) (hgp : GenPos S) (hno : ¬ HasGon (2 * j - 1) S) :
    S.card ≤ 2 * Nb := by
  obtain ⟨X, hX, hc⟩ := theoremA_odd j hj S hsym hgp hno
  have := hN X hX
  omega


/-! ## Arbitrary mirror line: reduction to the x-axis by an isometry -/

/-- reflection in the line through `p0` with unit direction `u` -/
def refl (p0 u : ℝ × ℝ) (p : ℝ × ℝ) : ℝ × ℝ :=
  (p0.1 + 2 * ((p.1 - p0.1) * u.1 + (p.2 - p0.2) * u.2) * u.1 - (p.1 - p0.1),
   p0.2 + 2 * ((p.1 - p0.1) * u.1 + (p.2 - p0.2) * u.2) * u.2 - (p.2 - p0.2))

/-- the rigid motion taking the line `p0 + ℝ u` to the x-axis -/
def isoT (p0 u : ℝ × ℝ) (p : ℝ × ℝ) : ℝ × ℝ :=
  (u.1 * (p.1 - p0.1) + u.2 * (p.2 - p0.2), -u.2 * (p.1 - p0.1) + u.1 * (p.2 - p0.2))

lemma isoT_refl {p0 u : ℝ × ℝ} (hu : u.1 ^ 2 + u.2 ^ 2 = 1) (p : ℝ × ℝ) :
    isoT p0 u (refl p0 u p) = mu (isoT p0 u p) := by
  ext
  · simp only [isoT, refl, mu]
    linear_combination (2 * ((p.1 - p0.1) * u.1 + (p.2 - p0.2) * u.2)) * hu
  · simp only [isoT, refl, mu]
    ring

lemma isoT_orient {p0 u : ℝ × ℝ} (hu : u.1 ^ 2 + u.2 ^ 2 = 1) (p q r : ℝ × ℝ) :
    orient (isoT p0 u p) (isoT p0 u q) (isoT p0 u r) = orient p q r := by
  simp only [orient, isoT]
  linear_combination ((q.1 - p.1) * (r.2 - p.2) - (q.2 - p.2) * (r.1 - p.1)) * hu

lemma isoT_injective {p0 u : ℝ × ℝ} (hu : u.1 ^ 2 + u.2 ^ 2 = 1) : Function.Injective (isoT p0 u) := by
  intro p q h
  have h1 := congrArg Prod.fst h
  have h2 := congrArg Prod.snd h
  simp only [isoT] at h1 h2
  ext
  · linear_combination u.1 * h1 - u.2 * h2 + (q.1 - p.1) * hu
  · linear_combination u.2 * h1 + u.1 * h2 + (q.2 - p.2) * hu

lemma isoT_affine (p0 u : ℝ × ℝ) : ∀ x y : ℝ × ℝ, ∀ a b : ℝ, a + b = 1 →
    isoT p0 u (a • x + b • y) = a • isoT p0 u x + b • isoT p0 u y := by
  intro x y a b hab
  ext
  · simp only [isoT, Prod.fst_add, Prod.snd_add, Prod.smul_fst, Prod.smul_snd, smul_eq_mul]
    linear_combination (u.1 * p0.1 + u.2 * p0.2) * hab
  · simp only [isoT, Prod.fst_add, Prod.snd_add, Prod.smul_fst, Prod.smul_snd, smul_eq_mul]
    linear_combination (u.1 * p0.2 - u.2 * p0.1) * hab

/-- an affine map sends the convex hull into the convex hull of the image -/
lemma image_hull_subset (T : ℝ × ℝ → ℝ × ℝ)
    (hT : ∀ x y : ℝ × ℝ, ∀ a b : ℝ, a + b = 1 → T (a • x + b • y) = a • T x + b • T y)
    (s : Set (ℝ × ℝ)) : T '' convexHull ℝ s ⊆ convexHull ℝ (T '' s) := by
  rintro _ ⟨x, hx, rfl⟩
  have hconv : Convex ℝ (T ⁻¹' convexHull ℝ (T '' s)) := by
    intro x hx y hy a b ha hb hab
    simp only [Set.mem_preimage] at hx hy ⊢
    rw [hT x y a b hab]
    exact convex_convexHull ℝ _ hx hy ha hb hab
  have hsub : s ⊆ T ⁻¹' convexHull ℝ (T '' s) :=
    fun z hz => subset_convexHull ℝ _ (Set.mem_image_of_mem T hz)
  exact convexHull_min hsub hconv hx

lemma convexPos_of_image (T : ℝ × ℝ → ℝ × ℝ)
    (hT : ∀ x y : ℝ × ℝ, ∀ a b : ℝ, a + b = 1 → T (a • x + b • y) = a • T x + b • T y)
    (hinj : Function.Injective T) (U : Finset (ℝ × ℝ)) (h : ConvexPos (U.image T)) : ConvexPos U := by
  intro p hp hcon
  apply h (T p) (Finset.mem_image_of_mem T hp)
  have h1 := image_hull_subset T hT _ (Set.mem_image_of_mem T hcon)
  refine convexHull_mono ?_ h1
  rintro _ ⟨z, hz, rfl⟩
  simp only [Finset.coe_erase, Set.mem_diff, Finset.mem_coe, Set.mem_singleton_iff] at hz ⊢
  exact ⟨Finset.mem_image_of_mem T hz.1, fun e => hz.2 (hinj e)⟩

/-- transport of the hypotheses of Theorem A along the rigid motion -/
lemma transport {p0 u : ℝ × ℝ} (hu : u.1 ^ 2 + u.2 ^ 2 = 1) {S : Finset (ℝ × ℝ)}
    (hsym : ∀ p ∈ S, refl p0 u p ∈ S) (hgp : GenPos S) (n : ℕ) (hno : ¬ HasGon n S) :
    MirrorSym (S.image (isoT p0 u)) ∧ GenPos (S.image (isoT p0 u)) ∧
    ¬ HasGon n (S.image (isoT p0 u)) ∧ (S.image (isoT p0 u)).card = S.card := by
  have hinj := isoT_injective (p0 := p0) hu
  refine ⟨?_, ?_, ?_, Finset.card_image_of_injective _ hinj⟩
  · intro q hq
    obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp hq
    rw [← isoT_refl hu]
    exact Finset.mem_image_of_mem _ (hsym p hp)
  · intro a ha b hb c hc hab hac hbc
    obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp ha
    obtain ⟨q, hq, rfl⟩ := Finset.mem_image.mp hb
    obtain ⟨r, hr, rfl⟩ := Finset.mem_image.mp hc
    rw [isoT_orient hu]
    exact hgp p hp q hq r hr (fun e => hab (by rw [e])) (fun e => hac (by rw [e]))
      (fun e => hbc (by rw [e]))
  · rintro ⟨U, hU, hUc, hUcp⟩
    apply hno
    have himg : (S.filter (fun p => isoT p0 u p ∈ U)).image (isoT p0 u) = U := by
      ext q
      simp only [Finset.mem_image, Finset.mem_filter]
      constructor
      · rintro ⟨p, ⟨_, hpU⟩, rfl⟩
        exact hpU
      · intro hq
        obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp (hU hq)
        exact ⟨p, ⟨hp, hq⟩, rfl⟩
    refine ⟨S.filter (fun p => isoT p0 u p ∈ U), Finset.filter_subset _ _, ?_, ?_⟩
    · have hc := Finset.card_image_of_injective (S.filter (fun p => isoT p0 u p ∈ U)) hinj
      rw [himg] at hc
      omega
    · apply convexPos_of_image (isoT p0 u) (isoT_affine p0 u) hinj
      rw [himg]
      exact hUcp

/-- **Theorem A (i), as stated in the claim**: a set symmetric under the reflection in an arbitrary line,
in general position, with no `2j` points in convex position, has at most `2 Nb + 2` points, where `Nb` is
any upper bound for the class `(2j, j, 2j)` (e.g. `Nb = N(2j,j,2j)`). -/
theorem theoremA_even_line (j : ℕ) (hj : 2 ≤ j) (Nb : ℕ)
    (hN : ∀ X : Finset (ℝ × ℝ), InClass (2 * j) j (2 * j) X → X.card ≤ Nb)
    (p0 u : ℝ × ℝ) (hu : u.1 ^ 2 + u.2 ^ 2 = 1) (S : Finset (ℝ × ℝ))
    (hsym : ∀ p ∈ S, refl p0 u p ∈ S) (hgp : GenPos S) (hno : ¬ HasGon (2 * j) S) :
    S.card ≤ 2 * Nb + 2 := by
  obtain ⟨h1, h2, h3, h4⟩ := transport hu hsym hgp (2 * j) hno
  obtain ⟨X, hX, hc⟩ := theoremA_even j hj _ h1 h2 h3
  have := hN X hX
  omega

/-- **Theorem A (ii), as stated in the claim**, odd case `k = 2j - 1`, `j ≥ 2`. -/
theorem theoremA_odd_line (j : ℕ) (hj : 2 ≤ j) (Nb : ℕ)
    (hN : ∀ X : Finset (ℝ × ℝ), InClass (2 * j - 1) j (2 * j - 1) X → X.card ≤ Nb)
    (p0 u : ℝ × ℝ) (hu : u.1 ^ 2 + u.2 ^ 2 = 1) (S : Finset (ℝ × ℝ))
    (hsym : ∀ p ∈ S, refl p0 u p ∈ S) (hgp : GenPos S) (hno : ¬ HasGon (2 * j - 1) S) :
    S.card ≤ 2 * Nb := by
  obtain ⟨h1, h2, h3, h4⟩ := transport hu hsym hgp (2 * j - 1) hno
  obtain ⟨X, hX, hc⟩ := theoremA_odd j hj _ h1 h2 h3
  have := hN X hX
  omega

/-- `refl` is a reflection: an involution fixing the line pointwise (sanity check of the definition). -/
lemma refl_refl {p0 u : ℝ × ℝ} (hu : u.1 ^ 2 + u.2 ^ 2 = 1) (p : ℝ × ℝ) :
    refl p0 u (refl p0 u p) = p := by
  apply isoT_injective (p0 := p0) hu
  rw [isoT_refl hu, isoT_refl hu, mu_mu]

lemma refl_fix_line (p0 u : ℝ × ℝ) (hu : u.1 ^ 2 + u.2 ^ 2 = 1) (t : ℝ) :
    refl p0 u (p0.1 + t * u.1, p0.2 + t * u.2) = (p0.1 + t * u.1, p0.2 + t * u.2) := by
  ext
  · simp only [refl]; linear_combination (2 * t * u.1) * hu
  · simp only [refl]; linear_combination (2 * t * u.2) * hu

/-- `refl` negates the normal direction `(-u.2, u.1)`: together with `refl_fix_line` this identifies
`refl p0 u` as the orthogonal reflection in the line `p0 + ℝ u`. -/
lemma refl_normal (p0 u : ℝ × ℝ) (s : ℝ) :
    refl p0 u (p0.1 - s * u.2, p0.2 + s * u.1) = (p0.1 + s * u.2, p0.2 - s * u.1) := by
  ext
  · simp only [refl]; ring
  · simp only [refl]; ring

/-- sanity check: `ConvexPos` is not vacuous (a point inside a triangle). -/
example : ¬ ConvexPos ({(0, 0), (4, 0), (0, 4), (1, 1)} : Finset (ℝ × ℝ)) := by
  intro h
  apply h (1, 1) (by simp)
  have hs : ((({(0, 0), (4, 0), (0, 4), (1, 1)} : Finset (ℝ × ℝ)).erase (1, 1) : Finset (ℝ × ℝ)) :
      Set (ℝ × ℝ)) = {(0, 0), (4, 0), (0, 4)} := by
    ext z
    simp only [Finset.coe_erase, Finset.coe_insert, Finset.coe_singleton, Set.mem_diff,
      Set.mem_insert_iff, Set.mem_singleton_iff]
    constructor
    · rintro ⟨h1 | h1 | h1 | h1, h2⟩
      · exact Or.inl h1
      · exact Or.inr (Or.inl h1)
      · exact Or.inr (Or.inr h1)
      · exact absurd h1 h2
    · rintro (h1 | h1 | h1) <;> subst h1 <;> norm_num
  rw [hs]
  have h22 : ((2 : ℝ), (2 : ℝ)) ∈ convexHull ℝ ({(0, 0), (4, 0), (0, 4)} : Set (ℝ × ℝ)) := by
    have hseg := segment_subset_convexHull (𝕜 := ℝ) (s := ({(0, 0), (4, 0), (0, 4)} : Set (ℝ × ℝ)))
      (x := ((4 : ℝ), (0 : ℝ))) (y := ((0 : ℝ), (4 : ℝ))) (by simp) (by simp)
    apply hseg
    refine ⟨1 / 2, 1 / 2, by norm_num, by norm_num, by norm_num, ?_⟩
    ext <;> norm_num
  have h00 : ((0 : ℝ), (0 : ℝ)) ∈ convexHull ℝ ({(0, 0), (4, 0), (0, 4)} : Set (ℝ × ℝ)) :=
    subset_convexHull ℝ _ (by simp)
  apply (convex_convexHull ℝ _).segment_subset h00 h22
  refine ⟨1 / 2, 1 / 2, by norm_num, by norm_num, by norm_num, ?_⟩
  ext <;> norm_num

end

end MirrorA

#print axioms MirrorA.theoremA_even_bound
#print axioms MirrorA.theoremA_odd_bound
#print axioms MirrorA.theoremA_even
#print axioms MirrorA.theoremA_odd
#print axioms MirrorA.lemma31
#print axioms MirrorA.cup_convexPos
#print axioms MirrorA.theoremA_even_line
#print axioms MirrorA.theoremA_odd_line

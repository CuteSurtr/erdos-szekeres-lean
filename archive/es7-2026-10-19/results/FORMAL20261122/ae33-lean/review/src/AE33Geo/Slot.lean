import ErdosSzekeres.OrientationGeometry
import ErdosSzekeres.Suk.OrientationClique

/-!
# AE33Geo.Slot: positive chains, the slot lemma, rotation and insertion (DESIGN.md §3)

* `PosChain X m`: all increasing index triples below `m` are positively oriented (a ccw convex polygon when m ≥ 3).
* `gp3`: the 3-term Grassmann–Plücker identity at a pivot (`ring`).
* `slot`: x₀..x_k positive, and T left of (x₀,x₁), of (x_{k−1},x_k) and of (x₀,x_k) ⇒ (x₀..x_k, T) positive.
  Three GP steps (pivots x₀, x_k, x_a), replacing the normal-cone argument of ABSAT8 §3.
* `posChain_rot`: invariance under cyclic rotation of the index.
* `insert_pos`: a point that sees exactly the edge (c_j, c_{j+1}) of a positive cyclic list, and neither neighbour,
  can be inserted after position j (l2enc's `Q1 = Q[0..i] ++ [p] ++ Q[i+1..]`).
* `posChain_card_convex`: a positive chain of m ≥ 4 points is m distinct points in convex position.
-/

namespace AE33Geo
open ErdosSzekeres

/-- All increasing index triples below `m` are positively oriented. -/
def PosChain (X : ℕ → Point) (m : ℕ) : Prop :=
  ∀ a b c, a < b → b < c → c < m → 0 < orient (X a) (X b) (X c)

theorem posChain_congr {X Y : ℕ → Point} {m : ℕ} (h : ∀ r, r < m → X r = Y r) (hX : PosChain X m) :
    PosChain Y m := by
  intro a b c hab hbc hcm
  rw [← h a (by omega), ← h b (by omega), ← h c hcm]
  exact hX a b c hab hbc hcm

theorem gp3 (o x y z t : Point) :
    orient o x z * orient o y t = orient o y z * orient o x t + orient o x y * orient o z t := by
  simp only [orient]; ring

theorem or12 (a b c : Point) : orient b a c = -orient a b c := by simp only [orient]; ring
theorem or23 (a b c : Point) : orient a c b = -orient a b c := by simp only [orient]; ring
theorem or13 (a b c : Point) : orient c b a = -orient a b c := by simp only [orient]; ring
theorem orcyc (a b c : Point) : orient b c a = orient a b c := by simp only [orient]; ring
theorem orcyc2 (a b c : Point) : orient c a b = orient a b c := by simp only [orient]; ring

theorem pos_of_mul_eq {A v R : ℝ} (hA : 0 < A) (h : A * v = R) (hR : 0 < R) : 0 < v := by
  by_contra hv
  push_neg at hv
  nlinarith

theorem neg_of_mul_eq {A v R : ℝ} (hA : 0 < A) (h : A * v = R) (hR : R < 0) : v < 0 := by
  by_contra hv
  push_neg at hv
  nlinarith

/-- **Slot lemma.** -/
theorem slot {X : ℕ → Point} {k : ℕ} (hk : 2 ≤ k) (hX : PosChain X (k + 1)) {T : Point}
    (h01 : 0 < orient (X 0) (X 1) T) (hk1 : 0 < orient (X (k - 1)) (X k) T)
    (h0k : 0 < orient (X 0) (X k) T) :
    ∀ a b, a < b → b ≤ k → 0 < orient (X a) (X b) T := by
  -- step 1: pivot x₀
  have s1 : ∀ b, 1 ≤ b → b ≤ k → 0 < orient (X 0) (X b) T := by
    intro b hb1 hbk
    rcases Nat.eq_or_lt_of_le hb1 with rfl | hb1
    · exact h01
    rcases Nat.eq_or_lt_of_le hbk with rfl | hbk
    · exact h0k
    exact pos_of_mul_eq (hX 0 1 k (by omega) (by omega) (by omega)) (gp3 (X 0) (X 1) (X b) (X k) T)
      (add_pos (mul_pos (hX 0 b k (by omega) hbk (by omega)) h01)
        (mul_pos (hX 0 1 b (by omega) hb1 (by omega)) h0k))
  -- step 2: pivot x_k
  have s2 : ∀ a, a + 1 ≤ k → 0 < orient (X a) (X k) T := by
    intro a ha
    rcases Nat.eq_zero_or_pos a with rfl | ha0
    · exact h0k
    rcases Nat.eq_or_lt_of_le ha with hak | hak
    · have : a = k - 1 := by omega
      subst this
      exact hk1
    have hA : 0 < orient (X k) (X 0) (X (k - 1)) := by
      rw [orcyc2]; exact hX 0 (k - 1) k (by omega) (by omega) (by omega)
    have hB : 0 < orient (X k) (X a) (X (k - 1)) := by
      rw [orcyc2]; exact hX a (k - 1) k (by omega) (by omega) (by omega)
    have hC : 0 < orient (X k) (X 0) (X a) := by
      rw [orcyc2]; exact hX 0 a k ha0 (by omega) (by omega)
    have hD : orient (X k) (X 0) T < 0 := by rw [or12]; linarith
    have hE : orient (X k) (X (k - 1)) T < 0 := by rw [or12]; linarith
    have hv := neg_of_mul_eq hA (gp3 (X k) (X 0) (X a) (X (k - 1)) T)
      (by nlinarith [mul_pos hB (neg_pos.2 hD), mul_pos hC (neg_pos.2 hE)])
    rw [or12] at hv
    linarith
  -- step 3: pivot x_a
  intro a b hab hbk
  rcases Nat.eq_zero_or_pos a with rfl | ha0
  · exact s1 b (by omega) hbk
  rcases Nat.eq_or_lt_of_le hbk with rfl | hbk'
  · exact s2 a (by omega)
  have hA : 0 < orient (X a) (X k) (X 0) := by
    rw [orcyc]; exact hX 0 a k ha0 (by omega) (by omega)
  have hB : 0 < orient (X a) (X b) (X 0) := by
    rw [orcyc]; exact hX 0 a b ha0 hab (by omega)
  have hC : 0 < orient (X a) (X b) (X k) := hX a b k hab hbk' (by omega)
  have hD : orient (X a) (X 0) T < 0 := by have := s1 a (by omega) (by omega); rw [or12]; linarith
  have hE : 0 < orient (X a) (X k) T := s2 a (by omega)
  have key := gp3 (X a) (X b) (X k) (X 0) T
  exact pos_of_mul_eq hA (by linarith [key] : orient (X a) (X k) (X 0) * orient (X a) (X b) T =
      orient (X a) (X b) (X 0) * orient (X a) (X k) T - orient (X a) (X b) (X k) * orient (X a) (X 0) T)
    (by nlinarith [mul_pos hB hE, mul_pos hC (neg_pos.2 hD)])

/-- The extended chain (x₀..x_k, T) is positive. -/
theorem slot_chain {X : ℕ → Point} {k : ℕ} (hk : 2 ≤ k) (hX : PosChain X (k + 1)) {T : Point}
    (h01 : 0 < orient (X 0) (X 1) T) (hk1 : 0 < orient (X (k - 1)) (X k) T)
    (h0k : 0 < orient (X 0) (X k) T) :
    PosChain (fun r => if r < k + 1 then X r else T) (k + 2) := by
  intro a b c hab hbc hck
  simp only
  rw [if_pos (by omega : a < k + 1), if_pos (by omega : b < k + 1)]
  by_cases hc : c < k + 1
  · rw [if_pos hc]; exact hX a b c hab hbc hc
  · rw [if_neg hc]; exact slot hk hX h01 hk1 h0k a b hab (by omega)

theorem mod_wrap {x m : ℕ} (h1 : m ≤ x) (h2 : x < 2 * m) : x % m = x - m := by
  rw [Nat.mod_eq_sub_mod h1, Nat.mod_eq_of_lt (by omega)]

/-- **Rotation invariance.** -/
theorem posChain_rot {X : ℕ → Point} {m : ℕ} (hX : PosChain X m) (s : ℕ) (hs : s < m) :
    PosChain (fun r => X ((r + s) % m)) m := by
  intro a b c hab hbc hcm
  simp only
  rcases Nat.lt_or_ge (c + s) m with hc | hc
  · rw [Nat.mod_eq_of_lt (by omega : a + s < m), Nat.mod_eq_of_lt (by omega : b + s < m), Nat.mod_eq_of_lt hc]
    exact hX _ _ _ (by omega) (by omega) hc
  rw [mod_wrap hc (by omega)]
  rcases Nat.lt_or_ge (b + s) m with hb | hb
  · rw [Nat.mod_eq_of_lt (by omega : a + s < m), Nat.mod_eq_of_lt hb, ← orcyc2]
    exact hX _ _ _ (by omega) (by omega) (by omega)
  rw [mod_wrap hb (by omega)]
  rcases Nat.lt_or_ge (a + s) m with ha | ha
  · rw [Nat.mod_eq_of_lt ha, ← orcyc]
    exact hX _ _ _ (by omega) (by omega) (by omega)
  rw [mod_wrap ha (by omega)]
  exact hX _ _ _ (by omega) (by omega) (by omega)

theorem getD_insert {c : List ℕ} {m j t r : ℕ} (hm : c.length = m) (hj : j < m) :
    (c.take (j + 1) ++ [t] ++ c.drop (j + 1)).getD r 0 =
      if r < j + 1 then c.getD r 0 else if r = j + 1 then t else c.getD (r - 1) 0 := by
  have htl : (c.take (j + 1)).length = j + 1 := by simp [List.length_take]; omega
  simp only [List.getD_eq_getElem?_getD]
  split_ifs with h1 h2
  · rw [List.append_assoc, List.getElem?_append_left (by omega), List.getElem?_take_of_lt h1]
  · subst h2
    rw [List.append_assoc, List.getElem?_append_right (by omega), htl]
    simp
  · rw [List.append_assoc, List.getElem?_append_right (by omega), htl, List.singleton_append]
    obtain ⟨k, rfl⟩ : ∃ k, r = j + 2 + k := ⟨r - (j + 2), by omega⟩
    rw [show j + 2 + k - (j + 1) = k + 1 by omega, List.getElem?_cons_succ, List.getElem?_drop]
    congr 2
    omega

/-- **Insertion of a point into the slot after position `j` of a positive cyclic list.** -/
theorem insert_pos {P : ℕ → Point} {c : List ℕ} {m : ℕ} (hm : c.length = m) (hm3 : 3 ≤ m)
    (hc : PosChain (fun r => P (c.getD r 0)) m) {j : ℕ} (hj : j < m) {t : ℕ}
    (h1 : 0 < orient (P (c.getD ((j + m - 1) % m) 0)) (P (c.getD j 0)) (P t))
    (h2 : orient (P (c.getD j 0)) (P (c.getD ((j + 1) % m) 0)) (P t) < 0)
    (h3 : 0 < orient (P (c.getD ((j + 1) % m) 0)) (P (c.getD ((j + 2) % m) 0)) (P t)) :
    PosChain (fun r => P ((c.take (j + 1) ++ [t] ++ c.drop (j + 1)).getD r 0)) (m + 1) := by
  have hrot := posChain_rot hc ((j + 1) % m) (Nat.mod_lt _ (by omega))
  have em : ∀ r, (r + (j + 1) % m) % m = (r + j + 1) % m := by
    intro r; rw [Nat.add_mod_mod]; congr 1
  have hrot' : PosChain (fun r => P (c.getD ((r + j + 1) % m) 0)) (m - 1 + 1) := by
    have : m - 1 + 1 = m := by omega
    rw [this]
    exact posChain_congr (fun r _ => by simp only [em]) hrot
  have e0 : (0 + j + 1) % m = (j + 1) % m := by congr 1; omega
  have e1 : (1 + j + 1) % m = (j + 2) % m := by congr 1; omega
  have e2 : (m - 1 - 1 + j + 1) % m = (j + m - 1) % m := by congr 1; omega
  have e3 : (m - 1 + j + 1) % m = j := by
    rw [show m - 1 + j + 1 = j + m by omega, Nat.add_mod_right, Nat.mod_eq_of_lt hj]
  have hch := slot_chain (X := fun r => P (c.getD ((r + j + 1) % m) 0)) (k := m - 1) (by omega) hrot'
    (T := P t) (by simp only [e0, e1]; exact h3) (by simp only [e2, e3]; exact h1)
    (by simp only [e0, e3]; rw [or12]; linarith)
  have hm' : m - 1 + 2 = m + 1 := by omega
  rw [hm'] at hch
  have hfin := posChain_rot hch (m - 1 - j) (by omega)
  refine posChain_congr (fun r hr => ?_) hfin
  simp only
  rw [getD_insert hm hj]
  by_cases hb : r < j + 1
  · have hlt : r + (m - 1 - j) < m + 1 := by omega
    rw [Nat.mod_eq_of_lt hlt, if_pos (by omega), if_pos hb]
    congr 2
    rw [show r + (m - 1 - j) + j + 1 = r + m by omega, Nat.add_mod_right, Nat.mod_eq_of_lt (by omega)]
  · by_cases hc' : r = j + 1
    · subst hc'
      rw [Nat.mod_eq_of_lt (by omega : j + 1 + (m - 1 - j) < m + 1), if_neg (by omega), if_neg hb, if_pos rfl]
    · rw [mod_wrap (by omega : m + 1 ≤ r + (m - 1 - j)) (by omega), if_pos (by omega), if_neg hb, if_neg hc']
      congr 2
      rw [show r + (m - 1 - j) - (m + 1) + j + 1 = r - 1 by omega, Nat.mod_eq_of_lt (by omega)]

theorem posChain_ne {X : ℕ → Point} {m : ℕ} (hX : PosChain X m) {a b c : ℕ} (ha : a < m) (hb : b < m)
    (hc : c < m) (hab : a ≠ b) (hbc : b ≠ c) (hac : a ≠ c) : orient (X a) (X b) (X c) ≠ 0 := by
  rcases Nat.lt_or_gt_of_ne hab with h1 | h1
  · rcases Nat.lt_or_gt_of_ne hbc with h2 | h2
    · exact (hX a b c h1 h2 hc).ne'
    rcases Nat.lt_or_gt_of_ne hac with h3 | h3
    · rw [or23 (X a) (X c) (X b)]; exact neg_ne_zero.2 (hX a c b h3 h2 hb).ne'
    · rw [orcyc (X c) (X a) (X b)]; exact (hX c a b h3 h1 hb).ne'
  · rcases Nat.lt_or_gt_of_ne hac with h3 | h3
    · rw [or12 (X b) (X a) (X c)]; exact neg_ne_zero.2 (hX b a c h1 h3 hc).ne'
    rcases Nat.lt_or_gt_of_ne hbc with h2 | h2
    · rw [orcyc2 (X b) (X c) (X a)]; exact (hX b c a h2 h3 ha).ne'
    · rw [or13 (X c) (X b) (X a)]; exact neg_ne_zero.2 (hX c b a h2 h1 ha).ne'

/-- **A positive chain of m ≥ 4 points is m distinct points in convex position.** -/
theorem posChain_card_convex {X : ℕ → Point} {m : ℕ} (hm : 4 ≤ m) (hX : PosChain X m) :
    (Finset.univ.image (fun i : Fin m => X i)).card = m ∧
      ConvexPosition (Finset.univ.image (fun i : Fin m => X i)) := by
  classical
  have hinj : Function.Injective (fun i : Fin m => X i) := by
    intro i j hij
    by_contra hne
    have hne' : (i : ℕ) ≠ j := fun h => hne (Fin.ext h)
    obtain ⟨c, hc, hci, hcj⟩ : ∃ c, c < m ∧ c ≠ i ∧ c ≠ j := by
      by_cases h0 : (0 : ℕ) ≠ i ∧ (0 : ℕ) ≠ j
      · exact ⟨0, by omega, h0.1, h0.2⟩
      by_cases h1 : (1 : ℕ) ≠ i ∧ (1 : ℕ) ≠ j
      · exact ⟨1, by omega, h1.1, h1.2⟩
      exact ⟨2, by omega, by omega, by omega⟩
    have := posChain_ne hX i.2 j.2 hc hne' (Ne.symm hcj) (Ne.symm hci)
    apply this
    simp only at hij
    rw [hij]
    simp only [orient]; ring
  refine ⟨by rw [Finset.card_image_of_injective _ hinj]; simp, ?_⟩
  exact Suk.convexPosition_of_positive_triples (fun i : Fin m => X i) hinj Finset.univ (by simpa using hm)
    (fun i _ j _ k _ hij hjk => hX i j k hij hjk k.2)

end AE33Geo

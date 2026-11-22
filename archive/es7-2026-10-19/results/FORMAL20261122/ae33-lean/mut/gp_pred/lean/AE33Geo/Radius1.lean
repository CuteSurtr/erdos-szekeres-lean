import AE33Geo.Pair

/-!
# AE33Geo.Radius1: radius 1 around AE33 is empty at the order-type level (REC §1 Corollary)

No 33-point set in general position without a convex 7-gon contains a 31-point subset with the labelled order type
(or mirror order type) of AE33 − {u, v}: the 203 pairs meeting H by `ae33_pair`; the other 325 because H itself
is mapped onto a convex heptagon (kernel check `hept_ccw` on the AE33 integers).
-/

namespace AE33Geo
open ErdosSzekeres AE33

/-- `φ` maps the labels of AE33 − {u, v} preserving all orientation signs. -/
def OTEmb (φ : ℕ → Point) (u v : ℕ) : Prop :=
  ∀ a b c, a < 33 → b < 33 → c < 33 → a ≠ u → a ≠ v → b ≠ u → b ≠ v → c ≠ u → c ≠ v →
    (0 < orient (φ a) (φ b) (φ c) ↔
      0 < iorient (ae33.getD a (0, 0)) (ae33.getD b (0, 0)) (ae33.getD c (0, 0)))

/-- `φ` maps the labels of AE33 − {u, v} reversing all orientation signs (mirror order type). -/
def OTEmbMirror (φ : ℕ → Point) (u v : ℕ) : Prop :=
  ∀ a b c, a < 33 → b < 33 → c < 33 → a ≠ u → a ≠ v → b ≠ u → b ≠ v → c ≠ u → c ≠ v →
    (0 < orient (φ a) (φ b) (φ c) ↔
      iorient (ae33.getD a (0, 0)) (ae33.getD b (0, 0)) (ae33.getD c (0, 0)) < 0)

/-! ## Kernel checks on the data (DESIGN.md D8) -/

/-- H's 35 increasing triples in ccw order (14, 15, 17, 20, 23, 32, 25) are positive on the AE33 integers. -/
theorem hept_ccw : ∀ c, c < 7 → ∀ b, b < c → ∀ a, a < b →
    0 < iorient (ae33.getD (hept.getD a 0) (0, 0)) (ae33.getD (hept.getD b 0) (0, 0))
      (ae33.getD (hept.getD c 0) (0, 0)) := by
  decide +kernel

/-- Each pair u < v < 33 is one of the 203 or misses H. -/
theorem pairs_cover : ∀ v, v < 33 → ∀ u, u < v →
    pairs203.toList.any (fun pr => pr.1 == u && pr.2 == v) = true ∨ (u ∉ hept ∧ v ∉ hept) := by
  decide +kernel

theorem mem_of_any {u v : ℕ} (h : pairs203.toList.any (fun pr => pr.1 == u && pr.2 == v) = true) :
    (u, v) ∈ pairs203.toList := by
  obtain ⟨pr, hpr, he⟩ := List.any_eq_true.1 h
  simp only [Bool.and_eq_true, beq_iff_eq] at he
  obtain ⟨rfl, rfl⟩ := he
  exact hpr

theorem pairs203_len : pairs203.toList.length = 203 := by decide +kernel

theorem keepIdx_len : ∀ i, i < 203 → (keepIdx (pairOfIdx i).1 (pairOfIdx i).2).length = 31 := by
  decide +kernel

theorem hept_lt : ∀ x ∈ hept, x < 33 := by decide

theorem hept_len : hept.length = 7 := rfl

theorem pairOfIdx_of_mem {u v : ℕ} (h : (u, v) ∈ pairs203.toList) : ∃ i, i < 203 ∧ pairOfIdx i = (u, v) := by
  obtain ⟨i, hi, hiv⟩ := List.mem_iff_getElem.1 h
  have hi' : i < 203 := by rw [pairs203_len] at hi; exact hi
  refine ⟨i, hi', ?_⟩
  have hs : i < pairs203.size := by rw [← Array.length_toList]; exact hi
  simp only [pairOfIdx, Array.getD_eq_getD_getElem?, Array.getElem?_eq_getElem hs, Option.getD_some]
  rw [← hiv, Array.getElem_toList]

theorem mem_keepIdx {u v x : ℕ} : x ∈ keepIdx u v ↔ x < 33 ∧ x ≠ u ∧ x ≠ v := by
  simp [keepIdx, List.mem_filter, List.mem_range]

theorem keepIdx_nodup (u v : ℕ) : (keepIdx u v).Nodup := List.nodup_range.filter _

theorem base_getD (u v a : ℕ) (ha : a < (keepIdx u v).length) :
    (base u v).getD a (0, 0) = ae33.getD ((keepIdx u v).getD a 0) (0, 0) := by
  have ha' : a < ((keepIdx u v).map fun i => ae33.getD i (0, 0)).length := by simpa using ha
  simp only [base, Array.getD_eq_getD_getElem?, List.getElem?_toArray, List.getD_eq_getElem?_getD,
    List.getElem?_map, List.getElem?_eq_getElem ha, Option.map_some, Option.getD_some]

/-! ## The corollary -/

theorem radius1_lt (h : TextsUnsat203) (S : Finset Point) (hgp : GeneralPosition S) (hcard : S.card = 33)
    (u v : ℕ) (hv : v < 33) (huv : u < v) (φ : ℕ → Point)
    (hS : ∀ w, w < 33 → w ≠ u → w ≠ v → φ w ∈ S)
    (hinj : ∀ a b, a < 33 → b < 33 → a ≠ u → a ≠ v → b ≠ u → b ≠ v → φ a = φ b → a = b)
    (hφ : OTEmb φ u v ∨ OTEmbMirror φ u v) : HasConvexNGon 7 S := by
  classical
  rcases pairs_cover v hv u huv with hany | ⟨hu', hv'⟩
  · obtain ⟨i, hi, hpair⟩ := pairOfIdx_of_mem (mem_of_any hany)
    have hK : (keepIdx u v).length = 31 := by have := keepIdx_len i hi; rwa [hpair] at this
    have hKm : ∀ a, a < 31 → (keepIdx u v).getD a 0 < 33 ∧ (keepIdx u v).getD a 0 ≠ u ∧
        (keepIdx u v).getD a 0 ≠ v := fun a ha => mem_keepIdx.1 (getD_mem_of_lt (by omega))
    let P : Fin 31 → Point := fun a => φ ((keepIdx u v).getD a 0)
    have hPinj : Function.Injective P := by
      intro a b hab
      have hm1 := hKm a a.2
      have hm2 := hKm b b.2
      have := hinj _ _ hm1.1 hm2.1 hm1.2.1 hm1.2.2 hm2.2.1 hm2.2.2 hab
      by_contra hne
      exact getD_ne_of_nodup (keepIdx_nodup u v) (by omega) (by omega)
        (fun e => hne (Fin.ext e)) this
    have hT : Finset.univ.image P ⊆ S := by
      intro y hy
      obtain ⟨a, -, rfl⟩ := Finset.mem_image.1 hy
      have hm := hKm a a.2
      exact hS _ hm.1 hm.2.1 hm.2.2
    have hTcard : (Finset.univ.image P).card = 31 := by
      rw [Finset.card_image_of_injective _ hPinj]; simp
    have h2 : (S \ Finset.univ.image P).card = 2 := by
      rw [Finset.card_sdiff, Finset.inter_eq_left.2 hT]; omega
    obtain ⟨p, q, hpq, hpqS⟩ := Finset.card_eq_two.1 h2
    have hSeq : S = insert p (insert q (Finset.univ.image P)) := by
      ext x
      constructor
      · intro hx
        by_cases hxT : x ∈ Finset.univ.image P
        · exact Finset.mem_insert_of_mem (Finset.mem_insert_of_mem hxT)
        · have : x ∈ S \ Finset.univ.image P := Finset.mem_sdiff.2 ⟨hx, hxT⟩
          rw [hpqS] at this
          simp only [Finset.mem_insert, Finset.mem_singleton] at this
          rcases this with rfl | rfl
          · exact Finset.mem_insert_self _ _
          · exact Finset.mem_insert_of_mem (Finset.mem_insert_self _ _)
      · intro hx
        simp only [Finset.mem_insert] at hx
        rcases hx with rfl | rfl | hx
        · exact (Finset.mem_sdiff.1 (by rw [hpqS]; simp : x ∈ S \ Finset.univ.image P)).1
        · exact (Finset.mem_sdiff.1 (by rw [hpqS]; simp : x ∈ S \ Finset.univ.image P)).1
        · exact hT hx
    have hb : baseOf i = base u v := by simp only [baseOf, hpair]
    have hreal : Realizes (baseOf i) P ∨ RealizesMirror (baseOf i) P := by
      rw [hb]
      rcases hφ with hφ | hφ
      · left
        intro a b c
        rw [base_getD u v a (by omega), base_getD u v b (by omega), base_getD u v c (by omega)]
        have ha := hKm a a.2
        have hb' := hKm b b.2
        have hc := hKm c c.2
        exact hφ _ _ _ ha.1 hb'.1 hc.1 ha.2.1 ha.2.2 hb'.2.1 hb'.2.2 hc.2.1 hc.2.2
      · right
        intro a b c
        rw [base_getD u v a (by omega), base_getD u v b (by omega), base_getD u v c (by omega)]
        have ha := hKm a a.2
        have hb' := hKm b b.2
        have hc := hKm c c.2
        exact hφ _ _ _ ha.1 hb'.1 hc.1 ha.2.1 ha.2.2 hb'.2.1 hb'.2.2 hc.2.1 hc.2.2
    have hgp' : GeneralPosition (insert p (insert q (Finset.univ.image P))) := hSeq ▸ hgp
    have hcard' : (insert p (insert q (Finset.univ.image P))).card = 33 := hSeq ▸ hcard
    rcases ae33_pair h ⟨i, hi⟩ P hreal p q hgp' hcard' with ⟨t, ht, htc, htconv, -⟩ | ⟨t, ht, htc, htconv, -⟩
    · exact ⟨t, hSeq ▸ ht, htc, htconv⟩
    · exact ⟨t, hSeq ▸ ht, htc, htconv⟩
  · -- H misses {u, v}: φ(H) is a convex heptagon
    have hX : ∀ r, r < 7 → hept.getD r 0 < 33 ∧ hept.getD r 0 ≠ u ∧ hept.getD r 0 ≠ v := by
      intro r hr
      have hm := getD_mem_of_lt (L := hept) (r := r) (by rw [hept_len]; exact hr)
      exact ⟨hept_lt _ hm, fun e => hu' (e ▸ hm), fun e => hv' (e ▸ hm)⟩
    have key : ∃ Y : ℕ → Point, PosChain Y 7 ∧ ∀ r, r < 7 → Y r ∈ S := by
      rcases hφ with hφ | hφ
      · refine ⟨fun r => φ (hept.getD r 0), fun a b c hab hbc hc => ?_, fun r hr => ?_⟩
        · have ha := hX a (by omega)
          have hb := hX b (by omega)
          have hc' := hX c hc
          exact (hφ _ _ _ ha.1 hb.1 hc'.1 ha.2.1 ha.2.2 hb.2.1 hb.2.2 hc'.2.1 hc'.2.2).2
            (hept_ccw c hc b hbc a hab)
        · have := hX r hr; exact hS _ this.1 this.2.1 this.2.2
      · refine ⟨fun r => φ (hept.getD (6 - r) 0), fun a b c hab hbc hc => ?_, fun r hr => ?_⟩
        · have ha := hX (6 - a) (by omega)
          have hb := hX (6 - b) (by omega)
          have hc' := hX (6 - c) (by omega)
          refine (hφ _ _ _ ha.1 hb.1 hc'.1 ha.2.1 ha.2.2 hb.2.1 hb.2.2 hc'.2.1 hc'.2.2).2 ?_
          have := hept_ccw (6 - a) (by omega) (6 - b) (by omega) (6 - c) (by omega)
          have e : ∀ x y z : Pt, iorient z y x = -iorient x y z := by
            intro x y z; simp only [iorient]; ring
          rw [e]; omega
        · have := hX (6 - r) (by omega); exact hS _ this.1 this.2.1 this.2.2
    obtain ⟨Y, hY, hYS⟩ := key
    obtain ⟨hc7, hconv⟩ := posChain_card_convex (by norm_num) hY
    refine ⟨_, fun y hy => ?_, hc7, hconv⟩
    obtain ⟨r, -, rfl⟩ := Finset.mem_image.1 hy
    exact hYS r r.2

/-- **The record's corollary (REC §1), Lean-checked modulo `TextsUnsat203`**: let S be 33 points in general
position, u ≠ v two labels of AE33, and φ an injective map of the other 31 labels into S that preserves (or
reverses) every orientation sign of AE33. Then S contains a convex 7-gon. Equivalently: no 33-point set in general
position without a convex 7-gon contains a 31-point subset with the order type (or mirror order type) of any
31-point subset of AE33 (radius 1 around AE33 is empty at the order-type level). -/
theorem ae33_radius1 (h : TextsUnsat203) (S : Finset Point) (hgp : GeneralPosition S) (hcard : S.card = 33)
    (u v : ℕ) (hu : u < 33) (hv : v < 33) (huv : u ≠ v) (φ : ℕ → Point)
    (hS : ∀ w, w < 33 → w ≠ u → w ≠ v → φ w ∈ S)
    (hinj : ∀ a b, a < 33 → b < 33 → a ≠ u → a ≠ v → b ≠ u → b ≠ v → φ a = φ b → a = b)
    (hφ : OTEmb φ u v ∨ OTEmbMirror φ u v) : HasConvexNGon 7 S := by
  rcases Nat.lt_or_gt_of_ne huv with hlt | hgt
  · exact radius1_lt h S hgp hcard u v hv hlt φ hS hinj hφ
  · refine radius1_lt h S hgp hcard v u hu hgt φ (fun w hw h1 h2 => hS w hw h2 h1)
      (fun a b ha hb h1 h2 h3 h4 => hinj a b ha hb h2 h1 h4 h3) ?_
    rcases hφ with hφ | hφ
    · exact Or.inl fun a b c ha hb hc h1 h2 h3 h4 h5 h6 => hφ a b c ha hb hc h2 h1 h4 h3 h6 h5
    · exact Or.inr fun a b c ha hb hc h1 h2 h3 h4 h5 h6 => hφ a b c ha hb hc h2 h1 h4 h3 h6 h5

/-- **Radius 0** (REC §1, "Radius 0 follows"): a 32-point subset with the order type (or mirror order type) of
AE33 − {w} also forces a convex 7-gon; it contains the 31-point subset AE33 − {w, t} for t = (w + 1) % 33. -/
theorem ae33_radius0 (h : TextsUnsat203) (S : Finset Point) (hgp : GeneralPosition S) (hcard : S.card = 33)
    (w : ℕ) (hw : w < 33) (φ : ℕ → Point) (hS : ∀ x, x < 33 → x ≠ w → φ x ∈ S)
    (hinj : ∀ a b, a < 33 → b < 33 → a ≠ w → b ≠ w → φ a = φ b → a = b)
    (hφ : OTEmb φ w w ∨ OTEmbMirror φ w w) : HasConvexNGon 7 S := by
  have ht : (w + 1) % 33 < 33 := Nat.mod_lt _ (by norm_num)
  have hwt : w ≠ (w + 1) % 33 := by
    rcases Nat.lt_or_ge (w + 1) 33 with h1 | h1
    · rw [Nat.mod_eq_of_lt h1]; omega
    · rw [show w = 32 by omega]; norm_num
  refine ae33_radius1 h S hgp hcard w ((w + 1) % 33) hw ht hwt φ (fun x hx h1 _ => hS x hx h1)
    (fun a b ha hb h1 _ h3 _ => hinj a b ha hb h1 h3) ?_
  rcases hφ with hφ | hφ
  · exact Or.inl fun a b c ha hb hc h1 _ h3 _ h5 _ => hφ a b c ha hb hc h1 h1 h3 h3 h5 h5
  · exact Or.inr fun a b c ha hb hc h1 _ h3 _ h5 _ => hφ a b c ha hb hc h1 h1 h3 h3 h5 h5

end AE33Geo

#print axioms AE33Geo.ae33_radius1
#print axioms AE33Geo.ae33_radius0

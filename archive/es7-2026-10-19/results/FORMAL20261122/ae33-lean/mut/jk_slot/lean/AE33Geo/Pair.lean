import AE33Geo.Sound
import ErdosSzekeres.Suk.Reflection

/-!
# AE33Geo.Pair: the pair theorem of the record (REC §1 Theorem), modulo the 203 verdicts

`core`: if `cnf B` is unsatisfiable, every realization of B's labelled order type with two new points in general
position has a positive 7-chain through p or q. `core_mirror`: the same for the mirror order type (reflection).
`pair_of_unsat`: the statement with `GeneralPosition`, `ConvexPosition`. `ae33_pair`: the 203 pairs, from
`TextsUnsat203`.
-/

namespace AE33Geo
open ErdosSzekeres AE33

def RealizesMirror31 (B : Array Pt) (pt : ℕ → Point) : Prop :=
  ∀ i j k, i < 31 → j < 31 → k < 31 →
    (0 < orient (pt i) (pt j) (pt k) ↔ iorient (B.getD i (0, 0)) (B.getD j (0, 0)) (B.getD k (0, 0)) < 0)

/-- A positive 7-chain of indices below 33 that contains 31 (p) or 32 (q). -/
def Chain7 (pt : ℕ → Point) : Prop :=
  ∃ L : List ℕ, L.length = 7 ∧ (∀ x ∈ L, x < 33) ∧ PosChain (fun r => pt (L.getD r 0)) 7 ∧ (31 ∈ L ∨ 32 ∈ L)

theorem core {B : Array Pt} (hB : B.size = 31) (hU : ¬ EncB.DimacsSatisfiable (cnf B)) {pt : ℕ → Point}
    (hreal : Realizes31 B pt)
    (hgp : ∀ i j k, i < 33 → j < 33 → k < 33 → i ≠ j → j ≠ k → i ≠ k → orient (pt i) (pt j) (pt k) ≠ 0) :
    Chain7 pt := by
  by_contra hno
  apply hU
  refine cnf_sat ⟨hB, hreal, hgp, fun L h1 h2 h3 => ?_⟩
  by_contra h4
  apply hno
  refine ⟨L, h1, h2, h3, ?_⟩
  by_contra h5
  push_neg at h5
  exact h4 h5

theorem core_mirror {B : Array Pt} (hB : B.size = 31) (hU : ¬ EncB.DimacsSatisfiable (cnf B))
    {pt : ℕ → Point} (hreal : RealizesMirror31 B pt)
    (hgp : ∀ i j k, i < 33 → j < 33 → k < 33 → i ≠ j → j ≠ k → i ≠ k → orient (pt i) (pt j) (pt k) ≠ 0) :
    Chain7 pt := by
  have hreal' : Realizes31 B (fun i => Suk.reflectY (pt i)) := by
    intro i j k hi hj hk
    simp only [Suk.orient_reflectY]
    rw [show -orient (pt i) (pt j) (pt k) = orient (pt i) (pt k) (pt j) from (or23 _ _ _).symm,
      hreal i k j hi hk hj, iorient_swap23]
    omega
  have hgp' : ∀ i j k, i < 33 → j < 33 → k < 33 → i ≠ j → j ≠ k → i ≠ k →
      orient (Suk.reflectY (pt i)) (Suk.reflectY (pt j)) (Suk.reflectY (pt k)) ≠ 0 := by
    intro i j k hi hj hk hij hjk hik
    simp only [Suk.orient_reflectY, neg_ne_zero]
    exact hgp i j k hi hj hk hij hjk hik
  obtain ⟨L, h1, h2, h3, h4⟩ := core hB hU hreal' hgp'
  refine ⟨L.reverse, by simp [h1], fun x hx => h2 x (List.mem_reverse.1 hx), ?_, by simpa using h4⟩
  have hr : ∀ r, r < 7 → L.reverse.getD r 0 = L.getD (6 - r) 0 := by
    intro r hr
    simp only [List.getD_eq_getElem?_getD]
    rw [List.getElem?_reverse (by rw [h1]; exact hr), h1]
  intro a b c hab hbc hc
  simp only
  rw [hr a (by omega), hr b (by omega), hr c hc]
  have := h3 (6 - c) (6 - b) (6 - a) (by omega) (by omega) (by omega)
  simp only [Suk.orient_reflectY] at this
  rw [or13 (pt (L.getD (6 - c) 0)) (pt (L.getD (6 - b) 0)) (pt (L.getD (6 - a) 0))]
  exact this

/-- A convex `m`-gon of `S` with `x` among its vertices. -/
def ConvexNGonThrough (m : ℕ) (S : Finset Point) (x : Point) : Prop :=
  ∃ t ⊆ S, t.card = m ∧ ConvexPosition t ∧ x ∈ t

theorem through_of_chain7 {pt : ℕ → Point} {S : Finset Point} (hS : ∀ i, i < 33 → pt i ∈ S)
    (h : Chain7 pt) : ConvexNGonThrough 7 S (pt 31) ∨ ConvexNGonThrough 7 S (pt 32) := by
  classical
  obtain ⟨L, h1, h2, h3, h4⟩ := h
  obtain ⟨hcard, hconv⟩ := posChain_card_convex (by norm_num) h3
  have hsub : Finset.univ.image (fun r : Fin 7 => pt (L.getD r 0)) ⊆ S := by
    intro y hy
    obtain ⟨r, -, rfl⟩ := Finset.mem_image.1 hy
    exact hS _ (h2 _ (getD_mem_of_lt (by rw [h1]; exact r.2)))
  have hmem : ∀ x ∈ L, pt x ∈ Finset.univ.image (fun r : Fin 7 => pt (L.getD r 0)) := by
    intro x hx
    obtain ⟨r, hr, hrx⟩ := List.mem_iff_getElem.1 hx
    refine Finset.mem_image.2 ⟨⟨r, by omega⟩, Finset.mem_univ _, ?_⟩
    simp only [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hr, Option.getD_some, hrx]
  rcases h4 with h | h
  · exact Or.inl ⟨_, hsub, hcard, hconv, hmem _ h⟩
  · exact Or.inr ⟨_, hsub, hcard, hconv, hmem _ h⟩

/-! ## The statement with `Fin 31`, `GeneralPosition` and `ConvexPosition` -/

/-- `P` realizes the labelled order type of `B` (all orientation signs agree). -/
def Realizes (B : Array Pt) (P : Fin 31 → Point) : Prop :=
  ∀ i j k : Fin 31, (0 < orient (P i) (P j) (P k) ↔
    0 < iorient (B.getD i (0, 0)) (B.getD j (0, 0)) (B.getD k (0, 0)))

/-- `P` realizes the labelled order type of the mirror image of `B` (all orientation signs reversed). -/
def RealizesMirror (B : Array Pt) (P : Fin 31 → Point) : Prop :=
  ∀ i j k : Fin 31, (0 < orient (P i) (P j) (P k) ↔
    iorient (B.getD i (0, 0)) (B.getD j (0, 0)) (B.getD k (0, 0)) < 0)

noncomputable def ptOf (P : Fin 31 → Point) (p q : Point) (i : ℕ) : Point :=
  if h : i < 31 then P ⟨i, h⟩ else if i = 31 then p else q

theorem card33_facts {P : Fin 31 → Point} {p q : Point}
    (h : (insert p (insert q (Finset.univ.image P))).card = 33) :
    Function.Injective P ∧ p ∉ Finset.univ.image P ∧ q ∉ Finset.univ.image P ∧ p ≠ q := by
  classical
  have hT : (Finset.univ.image P).card ≤ 31 := by
    simpa using Finset.card_image_le (s := (Finset.univ : Finset (Fin 31))) (f := P)
  have h1 := Finset.card_insert_le q (Finset.univ.image P)
  have hp : p ∉ insert q (Finset.univ.image P) := by
    intro hp; rw [Finset.insert_eq_of_mem hp] at h; omega
  rw [Finset.card_insert_of_notMem hp] at h
  have hq : q ∉ Finset.univ.image P := by
    intro hq; rw [Finset.insert_eq_of_mem hq] at h; omega
  rw [Finset.card_insert_of_notMem hq] at h
  have hinj : Set.InjOn P (Finset.univ : Finset (Fin 31)) :=
    Finset.card_image_iff.1 (by simp; omega)
  refine ⟨fun a b hab => hinj (by simp) (by simp) hab, fun h' => hp (Finset.mem_insert_of_mem h'), hq,
    fun h' => hp (by rw [h']; exact Finset.mem_insert_self _ _)⟩

theorem pair_of_unsat {B : Array Pt} (hB : B.size = 31) (hU : ¬ EncB.DimacsSatisfiable (cnf B))
    (P : Fin 31 → Point) (hP : Realizes B P ∨ RealizesMirror B P) (p q : Point)
    (hgp : GeneralPosition (insert p (insert q (Finset.univ.image P))))
    (hcard : (insert p (insert q (Finset.univ.image P))).card = 33) :
    ConvexNGonThrough 7 (insert p (insert q (Finset.univ.image P))) p ∨
      ConvexNGonThrough 7 (insert p (insert q (Finset.univ.image P))) q := by
  classical
  obtain ⟨hinj, hpT, hqT, hpq⟩ := card33_facts hcard
  set S := insert p (insert q (Finset.univ.image P))
  set pt := ptOf P p q
  have pt_lt : ∀ i (h : i < 31), pt i = P ⟨i, h⟩ := fun i h => by simp [pt, ptOf, h]
  have pt31 : pt 31 = p := by simp [pt, ptOf]
  have pt32 : pt 32 = q := by simp [pt, ptOf]
  have pt_mem : ∀ i, i < 33 → pt i ∈ S := by
    intro i hi
    by_cases h : i < 31
    · rw [pt_lt i h]; exact Finset.mem_insert_of_mem (Finset.mem_insert_of_mem (by simp))
    · by_cases h' : i = 31
      · subst h'; rw [pt31]; exact Finset.mem_insert_self _ _
      · have : i = 32 := by omega
        subst this; rw [pt32]; exact Finset.mem_insert_of_mem (Finset.mem_insert_self _ _)
  have pt_ne : ∀ i j, i < 33 → j < 33 → i ≠ j → pt i ≠ pt j := by
    intro i j hi hj hij
    have key : ∀ a b, a < 31 → b = 31 ∨ b = 32 → b < 33 → pt a ≠ pt b := by
      intro a b ha hb _
      rw [pt_lt a ha]
      rcases hb with rfl | rfl
      · rw [pt31]; intro e; exact hpT (by rw [← e]; simp)
      · rw [pt32]; intro e; exact hqT (by rw [← e]; simp)
    by_cases hi' : i < 31 <;> by_cases hj' : j < 31
    · rw [pt_lt i hi', pt_lt j hj']; intro e; exact hij (congrArg Fin.val (hinj e))
    · exact key i j hi' (by omega) hj
    · exact fun e => key j i hj' (by omega) hi e.symm
    · have : (i = 31 ∧ j = 32) ∨ (i = 32 ∧ j = 31) := by omega
      rcases this with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
      · rw [pt31, pt32]; exact hpq
      · rw [pt31, pt32]; exact hpq.symm
  have hgp' : ∀ i j k, i < 33 → j < 33 → k < 33 → i ≠ j → j ≠ k → i ≠ k → orient (pt i) (pt j) (pt k) ≠ 0 := by
    intro i j k hi hj hk hij hjk hik
    rw [generalPosition_iff_orient_ne_zero] at hgp
    exact hgp _ (pt_mem i hi) _ (pt_mem j hj) _ (pt_mem k hk) (pt_ne i j hi hj hij) (pt_ne i k hi hk hik)
      (pt_ne j k hj hk hjk)
  have hch : Chain7 pt := by
    rcases hP with hP | hP
    · refine core hB hU (fun i j k hi hj hk => ?_) hgp'
      rw [pt_lt i hi, pt_lt j hj, pt_lt k hk]
      exact hP ⟨i, hi⟩ ⟨j, hj⟩ ⟨k, hk⟩
    · refine core_mirror hB hU (fun i j k hi hj hk => ?_) hgp'
      rw [pt_lt i hi, pt_lt j hj, pt_lt k hk]
      exact hP ⟨i, hi⟩ ⟨j, hj⟩ ⟨k, hk⟩
  have := through_of_chain7 pt_mem hch
  rwa [pt31, pt32] at this

/-! ## The 203 pairs -/

/-- Kernel check: every base has 31 points. -/
theorem baseOf_size : ∀ i, i < 203 → (baseOf i).size = 31 := by
  decide +kernel

/-- **The record's theorem (REC §1), Lean-checked modulo `TextsUnsat203`**: for each of the 203 pairs, any
realization `P` of the labelled order type of `B = AE33 − {u, v}` (or of its mirror) and any two further points
`p, q` with the 33 points in general position give a convex 7-gon through `p` or through `q`. -/
theorem ae33_pair (h : TextsUnsat203) (i : Fin 203) (P : Fin 31 → Point)
    (hP : Realizes (baseOf i) P ∨ RealizesMirror (baseOf i) P) (p q : Point)
    (hgp : GeneralPosition (insert p (insert q (Finset.univ.image P))))
    (hcard : (insert p (insert q (Finset.univ.image P))).card = 33) :
    ConvexNGonThrough 7 (insert p (insert q (Finset.univ.image P))) p ∨
      ConvexNGonThrough 7 (insert p (insert q (Finset.univ.image P))) q :=
  pair_of_unsat (baseOf_size i i.2) (texts_iff_cnfs.1 h i i.2) P hP p q hgp hcard

end AE33Geo

#print axioms AE33Geo.cnf_sat
#print axioms AE33Geo.ae33_pair

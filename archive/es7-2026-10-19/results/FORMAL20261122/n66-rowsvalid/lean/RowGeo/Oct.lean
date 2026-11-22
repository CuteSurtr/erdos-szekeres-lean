import RowGeo.Eight
import Mathlib.Data.Finset.Sort

/-!
# RowGeo.Oct: the no-octagon clauses (S6)

`sat_oct`: for eight positions `e` (strictly increasing, below `n`), some 4-subset of their owners is not convex
under the intended assignment. Proof: otherwise every 4-subset satisfies `convexFrom` of its position-order
orientations; that value does not depend on the order of the four points (`cf_arr`), so every x-sorted quadruple
of the eight owners satisfies `convexFrom` of its four triple colors, which under the signotope condition means
`cup abc = cup abd ∧ cup acd = cup bcd` (`convex_sorted`); `no_eight` (RowGeo.Eight) excludes that.
-/

namespace RowGeo
open RowEnc N66Geo ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks

/-- The convexity formula of four points in the given order (`meaning` of `cvx`). -/
def CF (cup : ℕ → ℕ → ℕ → Bool) (w x y z : ℕ) : Bool :=
  convexFrom (ori3 cup w x y) (ori3 cup w x z) (ori3 cup w y z) (ori3 cup x y z)

theorem meaning_cvx (M : Model) (o : ℕ → ℕ) (i j k l : ℕ) :
    meaning M o (.cvx i j k l) = CF M.cup (o i) (o j) (o k) (o l) := rfl

/-- **The formula does not depend on the order of the four points.** -/
theorem cf_arr (cup : ℕ → ℕ → ℕ → Bool) {a b c d : ℕ} (h1 : a < b) (h2 : b < c) (h3 : c < d) {w x y z : ℕ}
    (hw : w = a ∨ w = b ∨ w = c ∨ w = d) (hx : x = a ∨ x = b ∨ x = c ∨ x = d)
    (hy : y = a ∨ y = b ∨ y = c ∨ y = d) (hz : z = a ∨ z = b ∨ z = c ∨ z = d)
    (hd : w ≠ x ∧ w ≠ y ∧ w ≠ z ∧ x ≠ y ∧ x ≠ z ∧ y ≠ z) :
    CF cup w x y z = convexFrom (cup a b c) (cup a b d) (cup a c d) (cup b c d) := by
  have h4 : a < c := Nat.lt_trans h1 h2
  have h5 : a < d := Nat.lt_trans h4 h3
  have h6 : b < d := Nat.lt_trans h2 h3
  have n1 : ¬ b < a := Nat.lt_asymm h1
  have n2 : ¬ c < b := Nat.lt_asymm h2
  have n3 : ¬ d < c := Nat.lt_asymm h3
  have n4 : ¬ c < a := Nat.lt_asymm h4
  have n5 : ¬ d < a := Nat.lt_asymm h5
  have n6 : ¬ d < b := Nat.lt_asymm h6
  obtain ⟨d1, d2, d3, d4, d5, d6⟩ := hd
  rcases hw with hw | hw | hw | hw <;> rcases hx with hx | hx | hx | hx <;>
    rcases hy with hy | hy | hy | hy <;> rcases hz with hz | hz | hz | hz <;>
    (subst w; subst x; subst y; subst z) <;>
    first
    | exact absurd rfl d1 | exact absurd rfl d2 | exact absurd rfl d3
    | exact absurd rfl d4 | exact absurd rfl d5 | exact absurd rfl d6
    | (simp only [CF, ori3, h1, h2, h3, h4, h5, h6, n1, n2, n3, n4, n5, n6, if_true, if_false,
          Nat.lt_irrefl] <;>
       cases cup a b c <;> cases cup a b d <;> cases cup a c d <;> cases cup b c d <;> rfl)

/-- An x-sorted quadruple satisfying the signotope condition is convex iff `abc = abd` and `acd = bcd`. -/
theorem convex_sorted {p0 p1 p2 p3 : Bool} (hp : PacketValid p0 p1 p2 p3)
    (hc : convexFrom p0 p1 p2 p3 = true) : p0 = p1 ∧ p2 = p3 := by
  revert hp hc
  cases p0 <;> cases p1 <;> cases p2 <;> cases p3 <;> decide

theorem pairwise_lt_sublist {e s : List ℕ} (he : e.Pairwise (· < ·)) (hs : s.Pairwise (· < ·)) (hsub : s ⊆ e) :
    s.Sublist e :=
  List.sublist_of_subperm_of_sorted (r := (· ≤ ·)) (List.subperm_of_subset (hs.imp fun h => Nat.ne_of_lt h) hsub)
    (hs.imp fun h => Nat.le_of_lt h) (he.imp fun h => Nat.le_of_lt h)

/-- **S6.** -/
theorem sat_oct {M : Model} {n : ℕ} {o : ℕ → ℕ} (ho : Owners M n o) {e : List ℕ} (he : octOk n e = true) :
    ∃ l ∈ octClause e, l.eval (meaning M o) = true := by
  simp only [octOk, Bool.and_eq_true, beq_iff_eq, List.all_eq_true, decide_eq_true_eq] at he
  obtain ⟨⟨hlen, hup⟩, hbd⟩ := he
  have hpw := strictUp_pairwise hup
  by_contra hall
  push_neg at hall
  -- every 4-subset of positions is convex
  have hcv : ∀ s ∈ combs 4 e, ∀ a b c d, s = [a, b, c, d] → CF M.cup (o a) (o b) (o c) (o d) = true := by
    intro s hs a b c d hsd
    have hl : (cvxL a b c d).neg ∈ octClause e := by
      unfold octClause; exact List.mem_map.2 ⟨s, hs, by rw [hsd]⟩
    have hsub := ((mem_combs_iff 4 e s).1 hs).1
    have hsp : s.Pairwise (· < ·) := hpw.sublist hsub
    rw [hsd] at hsp
    simp at hsp
    have := hall _ hl
    rw [L3.eval_neg, eval_cvxL (by omega) (by omega) (by omega), meaning_cvx] at this
    simpa using this
  -- the eight owners, x-sorted
  have hnd : e.Nodup := hpw.imp fun h => Nat.ne_of_lt h
  have hinjE : ∀ x ∈ e, ∀ y ∈ e, o x = o y → x = y := fun x hx y hy h =>
    ho.inj x y (hbd x hx) (hbd y hy) h
  set P := (e.map o).toFinset with hP
  have hPcard : P.card = 8 := by
    rw [hP, List.toFinset_card_of_nodup ((List.nodup_map_iff_inj_on hnd).2 hinjE), List.length_map, hlen]
  set qs := P.sort (· ≤ ·) with hqs
  have hqlen : qs.length = 8 := by rw [hqs, Finset.length_sort, hPcard]
  have hqsorted : qs.Pairwise (· < ·) := Finset.sort_sorted_lt P
  let q : Fin 8 → ℕ := fun i => qs.get ⟨i.val, by rw [hqlen]; exact i.isLt⟩
  have hqmono : StrictMono q := by
    intro i j hij
    exact List.pairwise_iff_get.1 hqsorted ⟨i.val, by rw [hqlen]; exact i.isLt⟩
      ⟨j.val, by rw [hqlen]; exact j.isLt⟩ hij
  have hqmem : ∀ i, q i ∈ P := fun i => (Finset.mem_sort _).1 (List.get_mem _ _)
  have hpos : ∀ i, ∃ p ∈ e, o p = q i := fun i => by
    have := hqmem i
    rw [hP, List.mem_toFinset, List.mem_map] at this
    exact this
  choose pf hpfe hpfo using hpos
  have hq7 : q 7 < M.n := by rw [← hpfo 7]; exact ho.lt _ (hbd _ (hpfe 7))
  apply no_eight M q hqmono hq7
  intro i j k l hij hjk hkl
  have qij := hqmono hij; have qjk := hqmono hjk; have qkl := hqmono hkl
  -- the four positions, sorted
  set S4 : Finset ℕ := {pf i, pf j, pf k, pf l} with hS4
  have dpf : ∀ x y : Fin 8, x < y → pf x ≠ pf y := fun x y hxy h => by
    have := congrArg o h; rw [hpfo, hpfo] at this; exact absurd this (Nat.ne_of_lt (hqmono hxy))
  have dij := dpf i j hij; have djk := dpf j k hjk; have dkl := dpf k l hkl
  have dik := dpf i k (lt_trans hij hjk); have dil := dpf i l (lt_trans (lt_trans hij hjk) hkl)
  have djl := dpf j l (lt_trans hjk hkl)
  have hS4card : S4.card = 4 := by
    rw [hS4, Finset.card_insert_of_not_mem (by simp [dij, dik, dil]),
      Finset.card_insert_of_not_mem (by simp [djk, djl]), Finset.card_insert_of_not_mem (by simp [dkl]),
      Finset.card_singleton]
  set s := S4.sort (· ≤ ·) with hs
  have hslen : s.length = 4 := by rw [hs, Finset.length_sort, hS4card]
  have hssorted : s.Pairwise (· < ·) := Finset.sort_sorted_lt S4
  have hsmem : ∀ x, x ∈ s ↔ x = pf i ∨ x = pf j ∨ x = pf k ∨ x = pf l := fun x => by
    rw [hs, Finset.mem_sort, hS4]; simp
  have hscomb : s ∈ combs 4 e := by
    rw [mem_combs_iff]
    refine ⟨pairwise_lt_sublist hpw hssorted (fun x hx => ?_), hslen⟩
    rcases (hsmem x).1 hx with rfl | rfl | rfl | rfl <;> exact hpfe _
  match s, hslen, hsmem, hscomb, hssorted with
  | [s0, s1, s2, s3], _, hsm, hsc, hso =>
    have hcf := hcv _ hsc s0 s1 s2 s3 rfl
    simp at hso
    have own : ∀ x, x = pf i ∨ x = pf j ∨ x = pf k ∨ x = pf l →
        o x = q i ∨ o x = q j ∨ o x = q k ∨ o x = q l := by
      rintro x (rfl | rfl | rfl | rfl) <;> simp [hpfo]
    have m0 := own s0 ((hsm s0).1 (by simp)); have m1 := own s1 ((hsm s1).1 (by simp))
    have m2 := own s2 ((hsm s2).1 (by simp)); have m3 := own s3 ((hsm s3).1 (by simp))
    have ein : ∀ x, x = pf i ∨ x = pf j ∨ x = pf k ∨ x = pf l → x < n := by
      rintro x (rfl | rfl | rfl | rfl) <;> exact hbd _ (hpfe _)
    have b0 := ein s0 ((hsm s0).1 (by simp)); have b1 := ein s1 ((hsm s1).1 (by simp))
    have b2 := ein s2 ((hsm s2).1 (by simp)); have b3 := ein s3 ((hsm s3).1 (by simp))
    have hd : o s0 ≠ o s1 ∧ o s0 ≠ o s2 ∧ o s0 ≠ o s3 ∧ o s1 ≠ o s2 ∧ o s1 ≠ o s3 ∧ o s2 ≠ o s3 :=
      ⟨ho.ne b0 b1 (by omega), ho.ne b0 b2 (by omega), ho.ne b0 b3 (by omega), ho.ne b1 b2 (by omega),
        ho.ne b1 b3 (by omega), ho.ne b2 b3 (by omega)⟩
    rw [cf_arr M.cup qij qjk qkl m0 m1 m2 m3 hd] at hcf
    have hn : q l < M.n := by rw [← hpfo l]; exact ho.lt _ (hbd _ (hpfe l))
    exact convex_sorted (M.signotope _ _ _ _ qij qjk qkl hn) hcf

end RowGeo

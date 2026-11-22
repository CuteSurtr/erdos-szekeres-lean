import EncB.Compose
import RowGeo.Decode
import RowGeo.Members

/-!
# RowGeo.Text: the printed text parses back to `rowCnf` (core + ENCBLEAN, no Mathlib)

* `litsOk_of_wf`: every literal of `rowCnf S` is nonzero with `|l| ≤ rowNv S` (every atom a clause uses is
  allocated: `code ∈ allocCodes`), for every support. Generic in `S`.
* `parseDimacs_rowText`: `EncB.parseDimacs (rowText S) = some (rowNv S, rowCnf S)` (ENCBLEAN `parseDimacs_render`).
* `parseDimacsBytes_rowText`: the same on the UTF-8 bytes the exe writes (`EncB.render_ascii`; the bytes of an
  ASCII text are its characters' codes), read by ENCBLEAN's `parseDimacsBytes`.
So a cake_lpr verdict on the certified file (E2), whose bytes are those of `rowText S` (E1, `tools/hash_binding.py`),
read as `parseDimacsBytes` reads it (E3), is `¬ DimacsSatisfiable (rowCnf S)`.
-/

namespace RowGeo
open RowEnc

/-! ## Every atom a clause uses is allocated -/

def LOk (k : Nat) : Lit → Prop
  | .const _ => True
  | .atom a _ => a.code ∈ allocCodes k

theorem sub_of_lt2 {k i j : Nat} (hij : i < j) (hj : j < k) : [i, j].Sublist (List.range k) :=
  sublist_of_sorted List.pairwise_lt_range (by simp [hij])
    (by intro x hx; simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
        rcases hx with rfl | rfl <;> simp <;> omega)

theorem sub_of_lt3 {k i j l : Nat} (hij : i < j) (hjl : j < l) (hl : l < k) :
    [i, j, l].Sublist (List.range k) :=
  sublist_of_sorted List.pairwise_lt_range (by simp; omega)
    (by intro x hx; simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
        rcases hx with rfl | rfl | rfl <;> simp <;> omega)

theorem sub_of_lt4 {k a b c d : Nat} (hab : a < b) (hbc : b < c) (hcd : c < d) (hd : d < k) :
    [a, b, c, d].Sublist (List.range k) :=
  sublist_of_sorted List.pairwise_lt_range (by simp; omega)
    (by intro x hx; simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
        rcases hx with rfl | rfl | rfl | rfl <;> simp <;> omega)

theorem pair_alloc {k i j : Nat} (hij : i < j) (hj : j < k) {a : Atm}
    (ha : a ∈ [Atm.bef i j, .cap i j 2, .cap i j 3, .cap i j 4, .cup i j 2, .cup i j 3, .cup i j 4, .cup i j 5,
      .cup i j 6]) : a.code ∈ allocCodes k := by
  unfold allocCodes
  refine List.mem_map_of_mem (List.mem_append.2 (Or.inl (List.mem_append.2 (Or.inl ?_))))
  exact List.mem_flatMap.2 ⟨[i, j], combs_of_sublist (sub_of_lt2 hij hj) rfl, ha⟩

theorem ori_alloc {k i j l : Nat} (hij : i < j) (hjl : j < l) (hl : l < k) :
    (Atm.ori i j l).code ∈ allocCodes k := by
  unfold allocCodes
  refine List.mem_map_of_mem (List.mem_append.2 (Or.inl (List.mem_append.2 (Or.inr ?_))))
  exact List.mem_filterMap.2 ⟨[i, j, l], combs_of_sublist (sub_of_lt3 hij hjl hl) rfl, rfl⟩

theorem cvx_alloc {k a b c d : Nat} (hab : a < b) (hbc : b < c) (hcd : c < d) (hd : d < k) :
    (Atm.cvx a b c d).code ∈ allocCodes k := by
  unfold allocCodes
  refine List.mem_map_of_mem (List.mem_append.2 (Or.inr ?_))
  exact List.mem_filterMap.2 ⟨[a, b, c, d], combs_of_sublist (sub_of_lt4 hab hbc hcd hd) rfl, rfl⟩

theorem neg_ok {k : Nat} {e : Lit} (h : LOk k e) : LOk k e.neg := by cases e <;> exact h

theorem disagreeL_ok {k : Nat} {e : Lit} (h : LOk k e) (b : Bool) : LOk k (disagreeL e b) := by
  cases b
  · exact h
  · exact neg_ok h

theorem befL_ok {k i j : Nat} (hi : i < k) (hj : j < k) (hij : i ≠ j) : LOk k (befL i j) := by
  unfold befL
  by_cases h : i < j
  · rw [if_pos h]; exact pair_alloc (a := .bef i j) h hj (by simp)
  · rw [if_neg h]; exact pair_alloc (i := j) (j := i) (a := .bef j i) (by omega) hi (by simp)

theorem geL_ok {k i j : Nat} (hi : i < k) (hj : j < k) (hij : i ≠ j) (cup : Bool) (t : Nat) :
    LOk k (geL cup i j t) := by
  have h1 : min i j < max i j := by omega
  have h2 : max i j < k := by omega
  cases cup
  · unfold geL
    simp only [Bool.false_eq_true, if_false]
    by_cases ht1 : t ≤ 1
    · rw [if_pos ht1]; trivial
    rw [if_neg ht1]
    by_cases ht4 : 4 < t
    · rw [if_pos ht4]; trivial
    rw [if_neg ht4]
    exact pair_alloc (a := .cap (min i j) (max i j) t) h1 h2 (by simp; omega)
  · unfold geL
    simp only [if_true]
    by_cases ht1 : t ≤ 1
    · rw [if_pos ht1]; trivial
    rw [if_neg ht1]
    by_cases ht6 : 6 < t
    · rw [if_pos ht6]; trivial
    rw [if_neg ht6]
    exact pair_alloc (a := .cup (min i j) (max i j) t) h1 h2 (by simp; omega)

theorem posL_ok {k i j l : Nat} (hi : i < k) (hj : j < k) (hl : l < k) (hij : i ≠ j) (hil : i ≠ l)
    (hjl : j ≠ l) : LOk k (posL i j l) := by
  unfold posL
  split <;> split <;> (try split) <;> simp only [LOk] <;> apply ori_alloc <;> omega

theorem dir_ok {S : List Nat} {u v : Nat} (hu : u < S.length) (hv : v < S.length) (huv : u ≠ v) :
    ∀ cl ∈ dirPart S u v, ∀ e ∈ cl, LOk S.length e := by
  intro cl hcl
  unfold dirPart at hcl
  rcases List.mem_cons.1 hcl with rfl | hcl
  · simp only [sourceClause, List.mem_cons, List.not_mem_nil, or_false]
    rintro e (rfl | rfl)
    · exact neg_ok (befL_ok hu hv huv)
    · exact neg_ok (geL_ok hu hv huv _ _)
  · split at hcl
    · rw [List.mem_singleton] at hcl; subst hcl
      simp only [emptyClause, List.mem_cons, List.not_mem_nil, or_false]
      rintro e rfl; exact neg_ok (befL_ok hu hv huv)
    · obtain ⟨z, -, rfl⟩ := List.mem_map.1 hcl
      simp only [domainClause, List.mem_cons, List.not_mem_nil, or_false]
      rintro e (rfl | rfl | rfl | rfl | rfl)
      · exact neg_ok (befL_ok hu hv huv)
      · exact neg_ok (geL_ok hu hv huv _ _)
      · exact geL_ok hu hv huv _ _
      · exact neg_ok (geL_ok hu hv huv _ _)
      · exact geL_ok hu hv huv _ _

theorem raw_ok (S : List Nat) : ∀ cl ∈ rawClauses S, ∀ e ∈ cl, LOk S.length e := by
  intro cl hcl
  simp only [rawClauses, List.mem_append] at hcl
  rcases hcl with (((h | h) | h) | h) | h
  · obtain ⟨p, hp, hcl⟩ := List.mem_flatMap.1 h
    rcases p with _ | ⟨i, _ | ⟨j, _ | ⟨x, t⟩⟩⟩ <;> simp only [List.not_mem_nil] at hcl
    obtain ⟨hij, hjk⟩ := pair_facts hp
    have hik : i < S.length := Nat.lt_trans hij hjk
    simp only [pairClauses, List.mem_append, List.mem_cons, List.not_mem_nil, or_false] at hcl
    rcases hcl with ((rfl | rfl | rfl | rfl | rfl | rfl) | h) | h
    all_goals first
      | (simp only [threshClause, List.mem_cons, List.not_mem_nil, or_false]
         rintro e (rfl | rfl)
         · exact neg_ok (geL_ok hik hjk (Nat.ne_of_lt hij) _ _)
         · exact geL_ok hik hjk (Nat.ne_of_lt hij) _ _)
      | exact dir_ok hik hjk (Nat.ne_of_lt hij) _ h
      | exact dir_ok hjk hik (Nat.ne_of_lt hij).symm _ h
  · obtain ⟨⟨a, b, c⟩, ht, hcl⟩ := List.mem_flatMap.1 h
    obtain ⟨ha, hb, hc, hab, hac, hbc⟩ := perm3_facts ht
    simp only [tripleClauses, List.mem_cons, List.mem_append, List.mem_map, List.not_mem_nil, or_false] at hcl
    rcases hcl with rfl | ⟨t, -, rfl⟩ | ⟨t, -, rfl⟩
    · simp only [transClause, List.mem_cons, List.not_mem_nil, or_false]
      rintro e (rfl | rfl | rfl)
      · exact neg_ok (befL_ok ha hb hab)
      · exact neg_ok (befL_ok hb hc hbc)
      · exact befL_ok ha hc hac
    all_goals
      simp only [growthClause, List.mem_cons, List.not_mem_nil, or_false]
      rintro e (rfl | rfl | rfl | rfl | rfl)
      · exact neg_ok (befL_ok ha hb hab)
      · exact neg_ok (befL_ok hb hc hbc)
      · first
          | exact neg_ok (posL_ok ha hb hc hab hac hbc)
          | exact posL_ok ha hb hc hab hac hbc
          | (simp only [Bool.false_eq_true, if_false, if_true]
             first | exact neg_ok (posL_ok ha hb hc hab hac hbc) | exact posL_ok ha hb hc hab hac hbc)
      · exact neg_ok (geL_ok ha hb hab _ _)
      · exact geL_ok hb hc hbc _ _
  · obtain ⟨q, hq, hcl⟩ := List.mem_flatMap.1 h
    rcases q with _ | ⟨i, _ | ⟨j, _ | ⟨l, _ | ⟨x, t⟩⟩⟩⟩ <;> simp only [List.not_mem_nil] at hcl
    obtain ⟨hij, hjl, hlk⟩ := triple_facts hq
    have hjk : j < S.length := Nat.lt_trans hjl hlk
    have hik : i < S.length := Nat.lt_trans hij hjk
    have hp := posL_ok hik hjk hlk (Nat.ne_of_lt hij) (Nat.ne_of_lt (Nat.lt_trans hij hjl)) (Nat.ne_of_lt hjl)
    unfold fixedClauses at hcl
    split at hcl
    · rw [List.mem_singleton] at hcl; subst hcl
      intro e he; rw [List.mem_singleton] at he; subst he; exact hp
    · split at hcl
      · rw [List.mem_singleton] at hcl; subst hcl
        intro e he; rw [List.mem_singleton] at he; subst he; exact neg_ok hp
      · simp at hcl
  · obtain ⟨q, hq, hcl⟩ := List.mem_flatMap.1 h
    rcases q with _ | ⟨a, _ | ⟨b, _ | ⟨c, _ | ⟨d, _ | ⟨x, t⟩⟩⟩⟩⟩ <;> simp only [List.not_mem_nil] at hcl
    obtain ⟨hab, hbc, hcd, hdk⟩ := quad_facts hq
    unfold quadClauses at hcl
    rcases List.mem_append.1 hcl with hcl | hcl
    · obtain ⟨⟨q0, q1, q2, q3⟩, hp, hcl⟩ := List.mem_flatMap.1 hcl
      obtain ⟨⟨x, y, z, w⟩, -, rfl⟩ := List.mem_map.1 hcl
      obtain ⟨d01, d02, d03, d12, d13, d23, l0, l1, l2, l3⟩ := perm4_facts hab hbc hcd hp
      simp only at d01 d02 d03 d12 d13 d23 l0 l1 l2 l3
      have k0 : q0 < S.length := by omega
      have k1 : q1 < S.length := by omega
      have k2 : q2 < S.length := by omega
      have k3 : q3 < S.length := by omega
      simp only [packetClause, List.mem_cons, List.not_mem_nil, or_false]
      rintro e (rfl | rfl | rfl | rfl | rfl | rfl | rfl)
      · exact neg_ok (befL_ok k0 k1 d01)
      · exact neg_ok (befL_ok k1 k2 d12)
      · exact neg_ok (befL_ok k2 k3 d23)
      · exact disagreeL_ok (posL_ok k0 k1 k2 d01 d02 d12) _
      · exact disagreeL_ok (posL_ok k0 k1 k3 d01 d03 d13) _
      · exact disagreeL_ok (posL_ok k0 k2 k3 d02 d03 d23) _
      · exact disagreeL_ok (posL_ok k1 k2 k3 d12 d13 d23) _
    · obtain ⟨⟨x, y, z, w⟩, -, rfl⟩ := List.mem_map.1 hcl
      have hck : c < S.length := Nat.lt_trans hcd hdk
      have hbk : b < S.length := Nat.lt_trans hbc hck
      have hak : a < S.length := Nat.lt_trans hab hbk
      simp only [convexClause, List.mem_cons, List.not_mem_nil, or_false]
      rintro e (rfl | rfl | rfl | rfl | rfl)
      · exact disagreeL_ok (posL_ok hak hbk hck (by omega) (by omega) (by omega)) _
      · exact disagreeL_ok (posL_ok hak hbk hdk (by omega) (by omega) (by omega)) _
      · exact disagreeL_ok (posL_ok hak hck hdk (by omega) (by omega) (by omega)) _
      · exact disagreeL_ok (posL_ok hbk hck hdk (by omega) (by omega) (by omega)) _
      · exact cvx_alloc hab hbc hcd hdk
  · obtain ⟨eight, h8, rfl⟩ := List.mem_map.1 h
    obtain ⟨hp8, hm8, -⟩ := range_facts h8
    intro e he
    obtain ⟨q, hq, rfl⟩ := List.mem_map.1 he
    obtain ⟨hsub, hlen⟩ := mem_combs hq
    have hpq : q.Pairwise (· < ·) := List.Pairwise.sublist hsub hp8
    rcases q with _ | ⟨i, _ | ⟨j, _ | ⟨l, _ | ⟨m, _ | ⟨x, t⟩⟩⟩⟩⟩ <;> simp at hlen
    simp only [List.pairwise_cons, List.mem_cons, List.not_mem_nil, or_false, forall_eq_or_imp, forall_eq,
      List.Pairwise.nil, and_true, false_implies, implies_true] at hpq
    exact cvx_alloc hpq.1.1 hpq.2.1.1 hpq.2.2 (hm8 m (hsub.subset (by simp)))

/-! ## The literal bound and the round trip -/

theorem numWith_le {L : List Nat} {a : Atm} (h : a.code ∈ L) :
    1 ≤ numWith (EncB.numberMap L) L.length a ∧ numWith (EncB.numberMap L) L.length a ≤ L.length := by
  have hm := EncB.numberMap_getD_le h
  have hnum : numWith (EncB.numberMap L) L.length a = (EncB.numberMap L).getD a.code 0 := by
    unfold numWith
    rw [if_neg (by omega)]
  rw [hnum]; exact hm

theorem mem_dedupAdj' : ∀ {l : List Int} {x : Int}, x ∈ dedupAdj l → x ∈ l
  | [], _, h => h
  | [_], _, h => h
  | a :: b :: t, x, h => by
    have ih : x ∈ dedupAdj (b :: t) → x ∈ b :: t := fun hx => mem_dedupAdj' hx
    by_cases hab : a = b
    · simp only [dedupAdj, if_pos hab] at h
      exact List.mem_cons_of_mem _ (ih h)
    · simp only [dedupAdj, if_neg hab] at h
      rcases List.mem_cons.1 h with rfl | h
      · exact List.mem_cons_self
      · exact List.mem_cons_of_mem _ (ih h)

theorem finish_ok {k : Nat} {cl : List Lit} {xs : List Int} (hok : ∀ e ∈ cl, LOk k e)
    (hf : finish (EncB.numberMap (allocCodes k)) (allocCodes k).length cl = some xs) :
    ∀ l ∈ xs, l ≠ 0 ∧ l.natAbs ≤ (allocCodes k).length := by
  intro l hl
  unfold finish at hf
  split at hf
  · exact absurd hf (by simp)
  simp only at hf
  split at hf
  · exact absurd hf (by simp)
  simp only [Option.some.injEq] at hf
  subst hf
  have hl' := List.mem_mergeSort.1 (mem_dedupAdj' hl)
  obtain ⟨e, he, hx⟩ := List.mem_filterMap.1 hl'
  cases e with
  | const b => simp [Lit.toInt] at hx
  | atom a b =>
    have hb := numWith_le (hok _ he)
    simp only [Lit.toInt, Option.some.injEq] at hx
    subst hx
    cases b <;> simp only [Bool.false_eq_true, if_false, if_true] <;> omega

/-- **The literal bound**, for every support (no hypothesis needed). -/
theorem litsOk_of_wf (S : List Nat) : ∀ cl ∈ rowCnf S, ∀ l ∈ cl, l ≠ 0 ∧ l.natAbs ≤ rowNv S := by
  intro cl hcl
  unfold rowCnf at hcl
  obtain ⟨c, hc, hfin⟩ := List.mem_filterMap.1 hcl
  exact finish_ok (raw_ok S c hc) hfin

theorem parseDimacs_rowText (S : List Nat) : EncB.parseDimacs (rowText S) = some (rowNv S, rowCnf S) :=
  EncB.parseDimacs_render (rowNv S) (rowCnf S) (litsOk_of_wf S)

/-- The UTF-8 bytes of the text are its characters' codes (it is ASCII), read by `parseDimacsBytes`. -/
theorem parseDimacsBytes_rowText (S : List Nat) :
    EncB.parseDimacsBytes (rowText S).toUTF8.data.toList = some (rowNv S, rowCnf S) := by
  have hb : (rowText S).toUTF8.data.toList = (rowText S).data.map fun c => c.val.toUInt8 := by
    have := EncB.renderCube_bytes (rowNv S) (rowCnf S) (EncB.bodyR (rowCnf S)) [] rfl
    rwa [EncB.renderCube_eq, EncB.cubeCnf_nil] at this
  rw [EncB.parseDimacsBytes, hb, List.map_map, ← parseDimacs_rowText, EncB.parseDimacs]
  congr 1
  conv => rhs; rw [← List.map_id (rowText S).data]
  apply List.map_congr_left
  intro c hc
  exact EncB.ofNat_toUInt8_ascii c (EncB.render_ascii _ _ c hc)

/-- **A verdict on the bytes is a verdict on `rowCnf`.** If every `parseDimacsBytes` parse of the bytes the exe
writes is unsatisfiable, `rowCnf S` is. -/
theorem rowUnsat_of_bytes (S : List Nat)
    (hv : ∀ nv F, EncB.parseDimacsBytes (rowText S).toUTF8.data.toList = some (nv, F) →
      ¬ EncB.DimacsSatisfiable F) : ¬ EncB.DimacsSatisfiable (rowCnf S) :=
  hv _ _ (parseDimacsBytes_rowText S)

end RowGeo

import ErdosSzekeres.OmissionPacking

/-!
# Compact reflective checker for omission certificate subtrees

A row catalog is a binary trie of `(support list, demand)` pairs, indexed by the
bits of the row number. A certificate subtree is a `PTree` whose weighted leaves
carry one list of small natural numbers (`row * K + weight` per entry). The Bool
checker `checkPacked` recomputes all column loads with one packed big-integer
sum per leaf and decodes its base-`base` digits, so a leaf carries no load
vector and no large literal. `checkPacked_sound` concludes exactly the
proposition of `CertificateTree.check_sound` for the catalog's support and
demand functions and the missing/occupied sets encoded by the mask.
-/

namespace CompactChecker

open ErdosSzekeres.OmissionCertificates
open scoped BigOperators

/-- Row catalog as a binary trie; `get k` follows the bits of `k`. -/
inductive Cat where
  | empty
  | row (supp : List ℕ) (dem : ℕ)
  | node (l r : Cat)

def Cat.get : Cat → ℕ → List ℕ × ℕ
  | .empty, _ => ([], 0)
  | .row s d, _ => (s, d)
  | .node l r, k => bif Nat.beq (k % 2) 0 then l.get (k / 2) else r.get (k / 2)

/-- One-time well-formedness check of the catalog: duplicate-free supports below `n`. -/
def Cat.wf (n : ℕ) : Cat → Bool
  | .empty => true
  | .row s _ => decide s.Nodup && s.all (fun i => decide (i < n))
  | .node l r => l.wf n && r.wf n

theorem Cat.get_wf {n : ℕ} (c : Cat) (h : c.wf n = true) (k : ℕ) :
    (c.get k).1.Nodup ∧ ∀ i ∈ (c.get k).1, i < n := by
  induction c generalizing k with
  | empty => simp [Cat.get]
  | row s d =>
      simp only [Cat.wf, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true] at h
      exact ⟨h.1, h.2⟩
  | node l r ihl ihr =>
      simp only [Cat.wf, Bool.and_eq_true] at h
      simp only [Cat.get]
      cases Nat.beq (k % 2) 0
      · exact ihr h.2 _
      · exact ihl h.1 _

/-- Semantic support of row `r` over `n` states. -/
def supp (c : Cat) (n r : ℕ) : Finset (Fin n) :=
  Finset.univ.filter (fun i : Fin n => i.val ∈ (c.get r).1)

/-- Semantic demand of row `r`. -/
def dem (c : Cat) (r : ℕ) : ℕ := (c.get r).2

/-- Packed row code computed from the support list. -/
def codeL (base : ℕ) (s : List ℕ) : ℕ := (s.map (fun i => base ^ i)).sum

theorem codeL_eq_rowCode {n : ℕ} (c : Cat) (hwf : c.wf n = true) (base r : ℕ) :
    codeL base (c.get r).1 = rowCode base (supp c n r) := by
  classical
  obtain ⟨hnd, hlt⟩ := c.get_wf hwf r
  have himg : (supp c n r).map Fin.valEmbedding = (c.get r).1.toFinset := by
    ext x
    simp only [supp, Finset.mem_map, Finset.mem_filter, Finset.mem_univ, true_and,
      Fin.valEmbedding_apply, List.mem_toFinset]
    constructor
    · rintro ⟨i, hi, rfl⟩
      exact hi
    · intro hx
      exact ⟨⟨x, hlt x hx⟩, hx, rfl⟩
  have h1 : rowCode base (supp c n r) = ∑ x ∈ (c.get r).1.toFinset, base ^ x := by
    rw [← himg, Finset.sum_map]
    rfl
  rw [h1, List.sum_toFinset _ hnd]
  rfl

/-- Base-`base` digits, least significant first. -/
def digits (base : ℕ) : ℕ → ℕ → List ℕ
  | 0, _ => []
  | n + 1, p => p % base :: digits base n (p / base)

theorem digits_length (base n p : ℕ) : (digits base n p).length = n := by
  induction n generalizing p with
  | zero => rfl
  | succ n ih => simp [digits, ih]

/-- Sum of `f c v` over the digits `c` paired with the mask values `v`
(missing positions in the mask default to `0`). -/
def zipSum (f : ℕ → ℕ → ℕ) : List ℕ → List ℕ → ℕ
  | [], _ => 0
  | c :: cs, m => f c (m.headD 0) + zipSum f cs m.tail

theorem zipSum_eq (f : ℕ → ℕ → ℕ) (cs mask : List ℕ) :
    zipSum f cs mask = ∑ i : Fin cs.length, f (cs.get i) (mask.getD i.val 0) := by
  induction cs generalizing mask with
  | nil => simp [zipSum]
  | cons c cs ih =>
      rw [zipSum, ih]
      rw [show (∑ i : Fin (c :: cs).length, f ((c :: cs).get i) (mask.getD i.val 0)) =
          ∑ i : Fin (cs.length + 1), f ((c :: cs).get i) (mask.getD i.val 0) from rfl,
        Fin.sum_univ_succ]
      congr 1
      · cases mask <;> simp
      · apply Finset.sum_congr rfl
        intro i _
        cases mask <;> simp

/-- The states with mask value `v` (1 = missing, 2 = occupied, else unassigned). -/
def mset (n : ℕ) (mask : List ℕ) (v : ℕ) : Finset (Fin n) :=
  Finset.univ.filter (fun i : Fin n => mask.getD i.val 0 = v)

theorem getD_set (mask : List ℕ) (v x i : ℕ) (hi : i ≠ v) :
    (mask.set v x).getD i 0 = mask.getD i 0 := by
  simp [List.getD_eq_getElem?_getD, Ne.symm hi]

theorem getD_set_self (mask : List ℕ) (v x : ℕ) :
    (mask.set v x).getD v 0 = x ∨ (mask.set v x).getD v 0 = mask.getD v 0 := by
  by_cases h : v < mask.length
  · left
    simp [List.getD_eq_getElem?_getD, h]
  · right
    rw [List.set_eq_of_length_le (by omega)]

theorem getD_set_cases (mask : List ℕ) (v x i : ℕ) :
    (mask.set v x).getD i 0 = mask.getD i 0 ∨ (i = v ∧ (mask.set v x).getD i 0 = x) := by
  by_cases hiv : i = v
  · subst hiv
    rcases getD_set_self mask i x with h | h
    · exact Or.inr ⟨rfl, h⟩
    · exact Or.inl h
  · exact Or.inl (getD_set mask v x i hiv)

theorem mem_mset {n : ℕ} (mask : List ℕ) (v : ℕ) (i : Fin n) :
    i ∈ mset n mask v ↔ mask.getD i.val 0 = v := by
  simp only [mset, Finset.mem_filter, Finset.mem_univ, true_and]

/-- Setting one mask entry keeps a compatible assignment compatible. -/
theorem feas_set {n : ℕ} (mask : List ℕ) (v x : ℕ) (holes : Fin n → ℕ)
    (hm : ∀ i ∈ mset n mask 1, holes i = 1) (hz : ∀ i ∈ mset n mask 2, holes i = 0)
    (hv : ∀ i : Fin n, i.val = v → (x = 1 → holes i = 1) ∧ (x = 2 → holes i = 0)) :
    (∀ i ∈ mset n (mask.set v x) 1, holes i = 1) ∧
      (∀ i ∈ mset n (mask.set v x) 2, holes i = 0) := by
  constructor
  · intro i hi
    rw [mem_mset] at hi
    rcases getD_set_cases mask v x i.val with h | ⟨hiv, h⟩
    · rw [h] at hi
      exact hm i ((mem_mset mask 1 i).mpr hi)
    · rw [h] at hi
      exact (hv i hiv).1 hi
  · intro i hi
    rw [mem_mset] at hi
    rcases getD_set_cases mask v x i.val with h | ⟨hiv, h⟩
    · rw [h] at hi
      exact hz i ((mem_mset mask 2 i).mpr hi)
    · rw [h] at hi
      exact (hv i hiv).2 hi

/-- A packed certificate subtree. A weighted leaf stores `row * K + weight`
for each row multiplier; a split branches on state `v` (zero child first). -/
inductive PTree where
  | overBudget
  | leaf (capacity : ℕ) (entries : List ℕ)
  | split (v : ℕ) (zero one : PTree)

def decode (K : ℕ) (es : List ℕ) : List (ℕ × ℕ) := es.map (fun e => (e / K, e % K))

/-- Count of missing states (mask value 1) among the digits. -/
def oneOf (_ v : ℕ) : ℕ := if v = 1 then 1 else 0

/-- Per-column left-hand contribution of the full-load leaf test. -/
def colOf (cap c v : ℕ) : ℕ := if v = 1 then c else if v = 2 then 0 else c - cap

/-- The arithmetic part of a leaf, given the decoded entries and the digits. -/
def leafArith (c : Cat) (m budget base cap : ℕ) (mask : List ℕ)
    (ent : List (ℕ × ℕ)) (cs : List ℕ) (P : ℕ) : Bool :=
  ent.all (fun e => Nat.blt e.1 m) &&
  Nat.blt 1 base &&
  Nat.blt (sparseSum (fun _ => 1) ent) base &&
  cs.all (fun x => decide (x < base)) &&
  Nat.beq (packList base cs) P &&
  Nat.blt (cap * (budget - zipSum oneOf cs mask) + zipSum (colOf cap) cs mask)
    (sparseSum (fun r => (c.get r).2) ent)

def leafOK (c : Cat) (m n budget base K cap : ℕ) (mask entries : List ℕ) : Bool :=
  let ent := decode K entries
  let P := sparseSum (fun r => codeL base (c.get r).1) ent
  leafArith c m budget base cap mask ent (digits base n P) P

/-- The compact Bool checker. -/
def checkPacked (c : Cat) (m n budget base K : ℕ) : List ℕ → PTree → Bool
  | mask, .overBudget => decide (budget < (mset n mask 1).card)
  | mask, .leaf cap es => leafOK c m n budget base K cap mask es
  | mask, .split v z o =>
      checkPacked c m n budget base K (mask.set v 2) z &&
      checkPacked c m n budget base K (mask.set v 1) o

/-- The proposition excluded at a node: exactly the conclusion of
`CertificateTree.check_sound` for the catalog rows `Fin m`. -/
def Feas (c : Cat) (m n budget : ℕ) (mask : List ℕ) (holes : Fin n → ℕ) : Prop :=
  (∀ i, holes i ≤ 1) ∧
    (∀ r : Fin m, dem c r.val ≤ ∑ i ∈ supp c n r.val, holes i) ∧
    (∑ i, holes i) ≤ budget ∧
    (∀ i ∈ mset n mask 1, holes i = 1) ∧ (∀ i ∈ mset n mask 2, holes i = 0)

theorem leaf_core (c : Cat) (m budget base cap : ℕ) (mask : List ℕ)
    (ent : List (ℕ × ℕ)) (cs : List ℕ) (n : ℕ) (hlen : cs.length = n)
    (hwf : c.wf n = true) (P : ℕ)
    (hP : P = sparseSum (fun r => codeL base (c.get r).1) ent)
    (h : leafArith c m budget base cap mask ent cs P = true) :
    ¬ ∃ holes : Fin n → ℕ, Feas c m n budget mask holes := by
  classical
  subst hlen
  subst hP
  simp only [leafArith, Bool.and_eq_true, List.all_eq_true, Nat.blt_eq] at h
  obtain ⟨⟨⟨⟨⟨hrowlt, hb⟩, hw⟩, hc⟩, heq⟩, hm⟩ := h
  have hcode : ∀ r, codeL base (c.get r).1 = rowCode base (supp c cs.length r) :=
    fun r => codeL_eq_rowCode c hwf base r
  have hc' : cs.all (fun x => decide (x < base)) = true := List.all_eq_true.mpr hc
  have hloads := load_eq_of_sparse_packed base cs (supp c cs.length)
    (fun r => codeL base (c.get r).1) ent hcode hb hw hc' (Nat.eq_of_beq_eq_true heq)
  set M := mset cs.length mask 1 with hM
  set O := mset cs.length mask 2 with hO
  have hcard : M.card = zipSum oneOf cs mask := by
    rw [zipSum_eq, hM, mset, Finset.card_filter]
    rfl
  have hcols : (∑ i, (if i ∈ M ∪ O then 0 else cs.get i - cap)) + ∑ i ∈ M, cs.get i =
      zipSum (colOf cap) cs mask := by
    rw [zipSum_eq, hM, mset, Finset.sum_filter, ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro i _
    simp only [hO, mset, Finset.mem_union, Finset.mem_filter, Finset.mem_univ, true_and,
      colOf]
    generalize mask.getD i.val 0 = v
    by_cases h1 : v = 1
    · subst h1; simp
    · by_cases h2 : v = 2
      · subst h2; simp
      · simp [h1, h2]
  have key := conditioned_excludes_of_full_load
    (fun i : Fin ent.length => supp c cs.length (ent.get i).1)
    (fun i => (c.get (ent.get i).1).2) (fun i => (ent.get i).2) M O cap budget (by
      rw [← hloads]
      have hs : sparseSum (fun r => (c.get r).2) ent =
          ∑ i : Fin ent.length, (ent.get i).2 * (c.get (ent.get i).1).2 :=
        sparseSum_eq_sum _ ent
      show cap * (budget - M.card) + (∑ i, if i ∈ M ∪ O then 0 else cs.get i - cap) +
          ∑ i ∈ M, cs.get i < ∑ i : Fin ent.length, (ent.get i).2 * (c.get (ent.get i).1).2
      rw [← hs, hcard, add_assoc, hcols]
      exact hm)
  rintro ⟨holes, hbool, hrows, hbud, hmiss, hocc⟩
  apply key
  refine ⟨holes, hbool, ?_, hbud, hmiss, hocc⟩
  intro i
  exact hrows ⟨(ent.get i).1, hrowlt _ (List.get_mem ent i)⟩

theorem leaf_sound (c : Cat) (m n budget base K cap : ℕ) (mask es : List ℕ)
    (hwf : c.wf n = true) (h : leafOK c m n budget base K cap mask es = true) :
    ¬ ∃ holes : Fin n → ℕ, Feas c m n budget mask holes :=
  leaf_core c m budget base cap mask (decode K es) _ n (digits_length _ _ _) hwf _ rfl h

/-- Soundness of the compact checker, by induction over the packed subtree. -/
theorem checkPacked_feas (c : Cat) (m n budget base K : ℕ) (hwf : c.wf n = true)
    (t : PTree) (mask : List ℕ)
    (h : checkPacked c m n budget base K mask t = true) :
    ¬ ∃ holes : Fin n → ℕ, Feas c m n budget mask holes := by
  classical
  induction t generalizing mask with
  | overBudget =>
      simp only [checkPacked, decide_eq_true_eq] at h
      rintro ⟨holes, _, _, hb, hm, _⟩
      have hle : (mset n mask 1).card ≤ ∑ i, holes i := by
        calc (mset n mask 1).card = ∑ i ∈ mset n mask 1, holes i := by
              rw [Finset.card_eq_sum_ones]
              exact Finset.sum_congr rfl (fun i hi => (hm i hi).symm)
          _ ≤ ∑ i, holes i := Finset.sum_le_sum_of_subset (Finset.subset_univ _)
      omega
  | leaf cap es => exact leaf_sound c m n budget base K cap mask es hwf h
  | split v z o ihz iho =>
      simp only [checkPacked, Bool.and_eq_true] at h
      rintro ⟨holes, hbool, hrows, hb, hm, hz⟩
      by_cases hvn : v < n
      · have hcases : holes ⟨v, hvn⟩ = 0 ∨ holes ⟨v, hvn⟩ = 1 := by
          have := hbool ⟨v, hvn⟩
          omega
        rcases hcases with h0 | h1
        · obtain ⟨hm', hz'⟩ := feas_set mask v 2 holes hm hz (fun i hiv => by
            have hi' : i = ⟨v, hvn⟩ := Fin.ext hiv
            subst hi'
            exact ⟨fun h => absurd h (by decide), fun _ => h0⟩)
          exact ihz (mask.set v 2) h.1 ⟨holes, hbool, hrows, hb, hm', hz'⟩
        · obtain ⟨hm', hz'⟩ := feas_set mask v 1 holes hm hz (fun i hiv => by
            have hi' : i = ⟨v, hvn⟩ := Fin.ext hiv
            subst hi'
            exact ⟨fun _ => h1, fun h => absurd h (by decide)⟩)
          exact iho (mask.set v 1) h.2 ⟨holes, hbool, hrows, hb, hm', hz'⟩
      · obtain ⟨hm', hz'⟩ := feas_set mask v 2 holes hm hz (fun i hiv =>
          absurd (hiv ▸ i.isLt) hvn)
        exact ihz (mask.set v 2) h.1 ⟨holes, hbool, hrows, hb, hm', hz'⟩

/-- Main soundness theorem, stated in the exact shape of
`CertificateTree.check_sound`: support and demand are the catalog's, and the
missing/occupied finsets are the mask's value-1 and value-2 states. -/
theorem checkPacked_sound (c : Cat) (m n budget base K : ℕ) (hwf : c.wf n = true)
    (t : PTree) (mask : List ℕ)
    (h : checkPacked c m n budget base K mask t = true) :
    ¬ ∃ holes : Fin n → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r : Fin m, dem c r.val ≤ ∑ i ∈ supp c n r.val, holes i) ∧
      (∑ i, holes i) ≤ budget ∧
      (∀ i ∈ mset n mask 1, holes i = 1) ∧ (∀ i ∈ mset n mask 2, holes i = 0) :=
  checkPacked_feas c m n budget base K hwf t mask h

end CompactChecker

import CompactChecker.Packed

/-!
# Kernel-optimized variant of the compact checker

Same certificate format as `Packed.lean` (`PTree`, entries `row * K + weight`),
but every recursive function the kernel evaluates is written with the plain
recursor (`List.rec`, `Nat.rec`, `FCat.rec`, `PTree.rec`) instead of compiled
structural recursion, the catalog stores each row's packed code (checked once
by `FCat.wf`), and the redundant digit-range check is replaced by a lemma.
`checkF_sound` concludes the `CertificateTree.check_sound` proposition.
-/

namespace CompactChecker

open ErdosSzekeres.OmissionCertificates
open scoped BigOperators

noncomputable section

/-- Catalog trie whose rows also carry their packed code `∑ base ^ i`. -/
inductive FCat where
  | empty
  | row (supp : List ℕ) (dem code : ℕ)
  | node (l r : FCat)

def FCat.get (c : FCat) : ℕ → List ℕ × ℕ × ℕ :=
  FCat.rec (motive := fun _ => ℕ → List ℕ × ℕ × ℕ) (fun _ => ([], 0, 0))
    (fun s d k _ => (s, d, k))
    (fun _ _ gl gr k => bif Nat.beq (k % 2) 0 then gl (k / 2) else gr (k / 2)) c

def FCat.wf (n base : ℕ) : FCat → Bool
  | .empty => true
  | .row s _ k => decide s.Nodup && s.all (fun i => decide (i < n)) && Nat.beq k (codeL base s)
  | .node l r => l.wf n base && r.wf n base

theorem FCat.get_wf {n base : ℕ} (c : FCat) (h : c.wf n base = true) (k : ℕ) :
    (c.get k).1.Nodup ∧ (∀ i ∈ (c.get k).1, i < n) ∧
      (c.get k).2.2 = codeL base (c.get k).1 := by
  induction c generalizing k with
  | empty =>
      show ([] : List ℕ).Nodup ∧ (∀ i ∈ ([] : List ℕ), i < n) ∧ 0 = codeL base []
      simp [codeL]
  | row s d code =>
      simp only [FCat.wf, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true] at h
      exact ⟨h.1.1, h.1.2, Nat.eq_of_beq_eq_true h.2⟩
  | node l r ihl ihr =>
      simp only [FCat.wf, Bool.and_eq_true] at h
      have e : FCat.get (.node l r) k =
          bif Nat.beq (k % 2) 0 then l.get (k / 2) else r.get (k / 2) := rfl
      rw [e]
      cases Nat.beq (k % 2) 0
      · exact ihr h.2 _
      · exact ihl h.1 _

/-- Semantic support and demand of row `r`. -/
def fsupp (c : FCat) (n r : ℕ) : Finset (Fin n) :=
  Finset.univ.filter (fun i : Fin n => i.val ∈ (c.get r).1)

def FCat.dem (c : FCat) (r : ℕ) : ℕ := (c.get r).2.1
def FCat.code (c : FCat) (r : ℕ) : ℕ := (c.get r).2.2

theorem FCat.code_eq_rowCode {n base : ℕ} (c : FCat) (hwf : c.wf n base = true) (r : ℕ) :
    c.code r = rowCode base (fsupp c n r) := by
  classical
  obtain ⟨hnd, hlt, hk⟩ := c.get_wf hwf r
  have himg : (fsupp c n r).map Fin.valEmbedding = (c.get r).1.toFinset := by
    ext x
    simp only [fsupp, Finset.mem_map, Finset.mem_filter, Finset.mem_univ, true_and,
      Fin.valEmbedding_apply, List.mem_toFinset]
    constructor
    · rintro ⟨i, hi, rfl⟩
      exact hi
    · intro hx
      exact ⟨⟨x, hlt x hx⟩, hx, rfl⟩
  have h1 : rowCode base (fsupp c n r) = ∑ x ∈ (c.get r).1.toFinset, base ^ x := by
    rw [← himg, Finset.sum_map]
    rfl
  rw [h1, List.sum_toFinset _ hnd, FCat.code, hk]
  rfl

/-! Recursor-based list functions and their agreement with the reference ones. -/

def sumF (value : ℕ → ℕ) (K : ℕ) (es : List ℕ) : ℕ :=
  List.rec (motive := fun _ => ℕ) 0 (fun e _ acc => (e % K) * value (e / K) + acc) es

theorem sumF_eq (value : ℕ → ℕ) (K : ℕ) (es : List ℕ) :
    sumF value K es = sparseSum value (decode K es) := by
  induction es with
  | nil => rfl
  | cons e es ih =>
      show (e % K) * value (e / K) + sumF value K es = _
      rw [ih]
      rfl

def allLtF (m K : ℕ) (es : List ℕ) : Bool :=
  List.rec (motive := fun _ => Bool) true (fun e _ acc => Nat.blt (e / K) m && acc) es

theorem allLtF_sound (m K : ℕ) (es : List ℕ) (h : allLtF m K es = true) :
    ∀ x ∈ decode K es, x.1 < m := by
  induction es with
  | nil => simp [decode]
  | cons e es ih =>
      have h' : (Nat.blt (e / K) m && allLtF m K es) = true := h
      simp only [Bool.and_eq_true, Nat.blt_eq] at h'
      intro x hx
      simp only [decode, List.map_cons, List.mem_cons] at hx
      rcases hx with rfl | hx
      · exact h'.1
      · exact ih h'.2 x hx

def packF (base : ℕ) (cs : List ℕ) : ℕ :=
  List.rec (motive := fun _ => ℕ) 0 (fun c _ acc => c + base * acc) cs

theorem packF_eq (base : ℕ) (cs : List ℕ) : packF base cs = packList base cs := by
  induction cs with
  | nil => rfl
  | cons c cs ih =>
      show c + base * packF base cs = _
      rw [ih]
      rfl

def digitsF (base n p : ℕ) : List ℕ :=
  Nat.rec (motive := fun _ => ℕ → List ℕ) (fun _ => [])
    (fun _ ih p => p % base :: ih (p / base)) n p

theorem digitsF_eq (base n p : ℕ) : digitsF base n p = digits base n p := by
  induction n generalizing p with
  | zero => rfl
  | succ n ih =>
      show p % base :: digitsF base n (p / base) = _
      rw [ih]
      rfl

theorem digits_lt (base n p : ℕ) (hb : 0 < base) : ∀ x ∈ digits base n p, x < base := by
  induction n generalizing p with
  | zero => simp [digits]
  | succ n ih =>
      intro x hx
      simp only [digits, List.mem_cons] at hx
      rcases hx with rfl | hx
      · exact Nat.mod_lt _ hb
      · exact ih _ x hx

def zipF (f : ℕ → ℕ → ℕ) (cs mask : List ℕ) : ℕ :=
  List.rec (motive := fun _ => List ℕ → ℕ) (fun _ => 0)
    (fun c _ ih m => f c (m.headD 0) + ih m.tail) cs mask

theorem zipF_eq (f : ℕ → ℕ → ℕ) (cs mask : List ℕ) : zipF f cs mask = zipSum f cs mask := by
  induction cs generalizing mask with
  | nil => rfl
  | cons c cs ih =>
      show f c (mask.headD 0) + zipF f cs mask.tail = _
      rw [ih]
      rfl

/-- Arithmetic part of a leaf, given the packed sum `P`. -/
def leafTailF (c : FCat) (n budget base K cap : ℕ) (mask es : List ℕ) (P : ℕ)
    (cs : List ℕ) : Bool :=
  Nat.beq (packF base cs) P &&
  Nat.blt (cap * (budget - zipF oneOf cs mask) + zipF (colOf cap) cs mask)
    (sumF c.dem K es)

def leafF (c : FCat) (m n budget base K cap : ℕ) (mask es : List ℕ) : Bool :=
  allLtF m K es && Nat.blt 1 base && Nat.blt (sumF (fun _ => 1) K es) base &&
  leafTailF c n budget base K cap mask es (sumF c.code K es)
    (digitsF base n (sumF c.code K es))

/-- The optimized checker. -/
def checkF (c : FCat) (m n budget base K : ℕ) (t : PTree) : List ℕ → Bool :=
  PTree.rec (motive := fun _ => List ℕ → Bool)
    (fun mask => decide (budget < (mset n mask 1).card))
    (fun cap es mask => leafF c m n budget base K cap mask es)
    (fun v _ _ ihz iho mask => ihz (mask.set v 2) && iho (mask.set v 1)) t

/-- The excluded proposition, as in `CertificateTree.check_sound`. -/
def FFeas (c : FCat) (m n budget : ℕ) (mask : List ℕ) (holes : Fin n → ℕ) : Prop :=
  (∀ i, holes i ≤ 1) ∧
    (∀ r : Fin m, c.dem r.val ≤ ∑ i ∈ fsupp c n r.val, holes i) ∧
    (∑ i, holes i) ≤ budget ∧
    (∀ i ∈ mset n mask 1, holes i = 1) ∧ (∀ i ∈ mset n mask 2, holes i = 0)

theorem leafF_core (c : FCat) (m budget base cap : ℕ) (mask : List ℕ)
    (ent : List (ℕ × ℕ)) (cs : List ℕ) (n : ℕ) (hlen : cs.length = n)
    (hwf : c.wf n base = true)
    (hrowlt : ∀ x ∈ ent, x.1 < m) (hb : 1 < base)
    (hw : sparseSum (fun _ => 1) ent < base)
    (hc : ∀ x ∈ cs, x < base)
    (heq : packList base cs = sparseSum c.code ent)
    (hm : cap * (budget - zipSum oneOf cs mask) + zipSum (colOf cap) cs mask <
      sparseSum c.dem ent) :
    ¬ ∃ holes : Fin n → ℕ, FFeas c m n budget mask holes := by
  classical
  subst hlen
  have hcode : ∀ r, c.code r = rowCode base (fsupp c cs.length r) :=
    fun r => c.code_eq_rowCode hwf r
  have hc' : cs.all (fun x => decide (x < base)) = true :=
    List.all_eq_true.mpr (fun x hx => decide_eq_true (hc x hx))
  have hloads := load_eq_of_sparse_packed base cs (fsupp c cs.length)
    c.code ent hcode hb hw hc' heq
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
    (fun i : Fin ent.length => fsupp c cs.length (ent.get i).1)
    (fun i => c.dem (ent.get i).1) (fun i => (ent.get i).2) M O cap budget (by
      rw [← hloads]
      have hs : sparseSum c.dem ent =
          ∑ i : Fin ent.length, (ent.get i).2 * c.dem (ent.get i).1 :=
        sparseSum_eq_sum _ ent
      show cap * (budget - M.card) + (∑ i, if i ∈ M ∪ O then 0 else cs.get i - cap) +
          ∑ i ∈ M, cs.get i < ∑ i : Fin ent.length, (ent.get i).2 * c.dem (ent.get i).1
      rw [← hs, hcard, add_assoc, hcols]
      exact hm)
  rintro ⟨holes, hbool, hrows, hbud, hmiss, hocc⟩
  apply key
  refine ⟨holes, hbool, ?_, hbud, hmiss, hocc⟩
  intro i
  exact hrows ⟨(ent.get i).1, hrowlt _ (List.get_mem ent i)⟩

theorem leafF_sound (c : FCat) (m n budget base K cap : ℕ) (mask es : List ℕ)
    (hwf : c.wf n base = true) (h : leafF c m n budget base K cap mask es = true) :
    ¬ ∃ holes : Fin n → ℕ, FFeas c m n budget mask holes := by
  simp only [leafF, leafTailF, Bool.and_eq_true, Nat.blt_eq] at h
  obtain ⟨⟨⟨hlt, hb⟩, hw⟩, heq, hm⟩ := h
  rw [sumF_eq] at hw
  rw [digitsF_eq, sumF_eq, sumF_eq, zipF_eq, zipF_eq] at hm
  rw [digitsF_eq, packF_eq, sumF_eq] at heq
  exact leafF_core c m budget base cap mask (decode K es) _ n (digits_length _ _ _) hwf
    (allLtF_sound m K es hlt) hb hw (digits_lt _ _ _ (by omega))
    (Nat.eq_of_beq_eq_true heq) hm

theorem checkF_feas (c : FCat) (m n budget base K : ℕ) (hwf : c.wf n base = true)
    (t : PTree) (mask : List ℕ)
    (h : checkF c m n budget base K t mask = true) :
    ¬ ∃ holes : Fin n → ℕ, FFeas c m n budget mask holes := by
  classical
  induction t generalizing mask with
  | overBudget =>
      have h' : decide (budget < (mset n mask 1).card) = true := h
      simp only [decide_eq_true_eq] at h'
      rintro ⟨holes, _, _, hb, hm, _⟩
      have hle : (mset n mask 1).card ≤ ∑ i, holes i := by
        calc (mset n mask 1).card = ∑ i ∈ mset n mask 1, holes i := by
              rw [Finset.card_eq_sum_ones]
              exact Finset.sum_congr rfl (fun i hi => (hm i hi).symm)
          _ ≤ ∑ i, holes i := Finset.sum_le_sum_of_subset (Finset.subset_univ _)
      omega
  | leaf cap es => exact leafF_sound c m n budget base K cap mask es hwf h
  | split v z o ihz iho =>
      have h' : (checkF c m n budget base K z (mask.set v 2) &&
          checkF c m n budget base K o (mask.set v 1)) = true := h
      rw [Bool.and_eq_true] at h'
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
          exact ihz (mask.set v 2) h'.1 ⟨holes, hbool, hrows, hb, hm', hz'⟩
        · obtain ⟨hm', hz'⟩ := feas_set mask v 1 holes hm hz (fun i hiv => by
            have hi' : i = ⟨v, hvn⟩ := Fin.ext hiv
            subst hi'
            exact ⟨fun _ => h1, fun h => absurd h (by decide)⟩)
          exact iho (mask.set v 1) h'.2 ⟨holes, hbool, hrows, hb, hm', hz'⟩
      · obtain ⟨hm', hz'⟩ := feas_set mask v 2 holes hm hz (fun i hiv =>
          absurd (hiv ▸ i.isLt) hvn)
        exact ihz (mask.set v 2) h'.1 ⟨holes, hbool, hrows, hb, hm', hz'⟩

/-- Soundness of the optimized checker, in the shape of `CertificateTree.check_sound`. -/
theorem checkF_sound (c : FCat) (m n budget base K : ℕ) (hwf : c.wf n base = true)
    (t : PTree) (mask : List ℕ)
    (h : checkF c m n budget base K t mask = true) :
    ¬ ∃ holes : Fin n → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r : Fin m, c.dem r.val ≤ ∑ i ∈ fsupp c n r.val, holes i) ∧
      (∑ i, holes i) ≤ budget ∧
      (∀ i ∈ mset n mask 1, holes i = 1) ∧ (∀ i ∈ mset n mask 2, holes i = 0) :=
  checkF_feas c m n budget base K hwf t mask h

end

end CompactChecker

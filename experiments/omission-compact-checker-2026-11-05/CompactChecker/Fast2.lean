import CompactChecker.Fast
import CompactChecker.WordPack
import CompactChecker.Split

/-!
# Fused, row-cached variant of the compact checker (6 November 2026)

Same certificate shape as `Fast.lean` (`PTree`, the `FCat` catalog, the `FFeas`
proposition), with four kernel-level changes:

* **Cached row lookups.** An entry `row * K + weight` is decoded by a `Nat.rec` on
  the row. The kernel turns the computed row into a literal before it calls the
  row function, so `rowVal … (Nat.succ j)` is the same term for every entry of that
  row and the kernel's `whnf` cache does each trie descent once per block, not
  once per entry.
* **One pass over the entries.** The row value is `code + base ^ n * demand`, so
  one weighted sum `Q` carries the column loads (its low `n` digits) and the
  demand sum (`Q / base ^ n`). The no-carry bound needs no separate weight sum:
  every kept row has demand `≥ 1`, so the weight sum is at most the demand sum,
  and the checker tests `Q / base ^ n < base`. Rows `≥ m` and rows of demand `0`
  contribute `0` (the leaf is then judged on the remaining entries, which is
  sound).
* **One pass over the digits.** Digit extraction, the mask and the count of
  missing states are fused into `colLoop`, a recursion over the mask list itself
  (its length `n` is checked once per call of `checkF2`); the count sits above the
  column sum in the same number (`colF`), and no `packList` comparison is
  evaluated (it follows from the bound above, `packList_digits`).
* **Only `Nat` primitives and recursors** in evaluated code (`Nat.div`, `Nat.mod`,
  `Nat.beq`, …), so the kernel never unfolds `HDiv`/`HMod`/`OfNat` instances
  inside loops. Row codes are recomputed from the support (`codeR`), so the leaf
  base may differ from the catalog's.

`checkF2_sound` concludes the `CertificateTree.check_sound` proposition, exactly
as `checkF_sound`.
-/

namespace CompactChecker

open ErdosSzekeres.OmissionCertificates
open scoped BigOperators

open Lean Elab Term Meta in
/-- `natlits% [a, b, …]` is the `List ℕ` of the raw literals `a, b, …`. It skips
`OfNat` instance synthesis in the elaborator and `OfNat.ofNat` unfolding in the
kernel. It only builds data; soundness never depends on it. -/
elab "natlits% " "[" xs:num,* "]" : term => do
  let nat := Lean.mkConst ``Nat
  let mut e := mkApp (Lean.mkConst ``List.nil [levelZero]) nat
  for x in xs.getElems.reverse do
    e := mkApp3 (Lean.mkConst ``List.cons [levelZero]) nat (mkRawNatLit x.getNat) e
  return e

noncomputable section

/-! ## Functions evaluated by the kernel -/

/-- One trie descent; applies `f` to the support and demand of the row found
(`0` at an empty slot). -/
def FCat.getWith (f : List ℕ → ℕ → ℕ) (c : FCat) : ℕ → ℕ :=
  FCat.rec (motive := fun _ => ℕ → ℕ) (fun _ => 0) (fun s d _ _ => f s d)
    (fun _ _ gl gr k =>
      Bool.rec (gr (Nat.div k 2)) (gl (Nat.div k 2)) (Nat.beq (Nat.mod k 2) 0)) c

/-- Packed code `∑ base ^ i` of a support list. -/
def codeR (base : ℕ) (s : List ℕ) : ℕ :=
  List.rec (motive := fun _ => ℕ) 0 (fun i _ acc => Nat.add (Nat.pow base i) acc) s

/-- Value of row `r` in the fused sum: `code + BN * demand`, or `0` when `r ≥ m`
or the demand is `0`. -/
def rowVal (c : FCat) (m base BN r : ℕ) : ℕ :=
  Bool.rec 0
    (c.getWith (fun s d => Bool.rec 0 (Nat.add (codeR base s) (Nat.mul BN d)) (Nat.blt 0 d)) r)
    (Nat.blt r m)

/-- `weight * rv row` for the entry `e = row * K + weight`. The `Nat.rec` hands
`rv` a literal row, which makes the call cacheable across entries. -/
def entQ (rv : ℕ → ℕ) (K e : ℕ) : ℕ :=
  Nat.rec (motive := fun _ => ℕ) (Nat.mul (Nat.mod e K) (rv 0))
    (fun j _ => Nat.mul (Nat.mod e K) (rv (Nat.succ j))) (Nat.div e K)

/-- Sum of `entQ` over the `k` base-`J` digits of a word. -/
def wordQ (rv : ℕ → ℕ) (K J k : ℕ) : ℕ → ℕ :=
  Nat.rec (motive := fun _ => ℕ → ℕ) (fun _ => 0)
    (fun _ ih y => Nat.add (entQ rv K (Nat.mod y J)) (ih (Nat.div y J))) k

/-- The fused weighted sum of a leaf, over its words. -/
def leafQ (rv : ℕ → ℕ) (K J k : ℕ) (ws : List ℕ) : ℕ :=
  List.rec (motive := fun _ => ℕ) 0 (fun y _ acc => Nat.add (wordQ rv K J k y) acc) ws

/-- Column term plus `BIG` for each missing state (mask value 1). -/
def colF (cap BIG v c : ℕ) : ℕ :=
  Bool.rec (Bool.rec (Nat.sub c cap) 0 (Nat.beq v 2)) (Nat.add c BIG) (Nat.beq v 1)

/-- Digits of `p`, mask and column terms in one pass over the mask. -/
def colLoop (base cap BIG : ℕ) (mask : List ℕ) : ℕ → ℕ :=
  List.rec (motive := fun _ => ℕ → ℕ) (fun _ => 0)
    (fun v _ ih p => Nat.add (colF cap BIG v (Nat.mod p base)) (ih (Nat.div p base))) mask

/-- Separates the column sum (`< (n + 1) * base`) from the missing count. -/
def bigF (n base : ℕ) : ℕ := Nat.mul (Nat.succ n) base

/-- `1 < base`, `Q / BN < base`, and the full-load test with `X` from `colLoop`. -/
def leafTest (budget base BN BIG cap Q X : ℕ) : Bool :=
  Bool.rec false
    (Bool.rec false
      (Nat.blt (Nat.add (Nat.mul cap (Nat.sub budget (Nat.div X BIG))) (Nat.mod X BIG))
        (Nat.div Q BN))
      (Nat.blt (Nat.div Q BN) base))
    (Nat.blt 1 base)

def leafF2 (c : FCat) (m n budget base K J k cap : ℕ) (mask ws : List ℕ) : Bool :=
  leafTest budget base (Nat.pow base n) (bigF n base) cap
    (leafQ (rowVal c m base (Nat.pow base n)) K J k ws)
    (colLoop base cap (bigF n base) mask (leafQ (rowVal c m base (Nat.pow base n)) K J k ws))

/-- More missing states than the budget. -/
def overF (n budget base : ℕ) (mask : List ℕ) : Bool :=
  Nat.blt budget (Nat.div (colLoop base 0 (bigF n base) mask 0) (bigF n base))

/-- `List.set` by recursors. -/
def setF (x : ℕ) : List ℕ → ℕ → List ℕ :=
  List.rec (motive := fun _ => ℕ → List ℕ) (fun _ => [])
    (fun a as ih k => Nat.rec (motive := fun _ => List ℕ) (x :: as) (fun j _ => a :: ih j) k)

def treeF2 (c : FCat) (m n budget base K J k : ℕ) (t : PTree) : List ℕ → Bool :=
  PTree.rec (motive := fun _ => List ℕ → Bool)
    (fun mask => overF n budget base mask)
    (fun cap ws mask => leafF2 c m n budget base K J k cap mask ws)
    (fun v _ _ ihz iho mask => Bool.rec false (iho (setF 1 mask v)) (ihz (setF 2 mask v))) t

def lenF (l : List ℕ) : ℕ := List.rec (motive := fun _ => ℕ) 0 (fun _ _ acc => Nat.succ acc) l

/-- The fused checker. Leaf entries are words of `k` base-`J` digits, each digit
`row * K + weight`; `base` is the leaf base (independent of the catalog's). The
mask must have length `n`; `setF` keeps that length. -/
def checkF2 (c : FCat) (m n budget base K J k : ℕ) (t : PTree) (mask : List ℕ) : Bool :=
  Bool.rec false (treeF2 c m n budget base K J k t mask) (Nat.beq (lenF mask) n)

/-! ## Agreement with the reference functions -/

theorem FCat.getWith_eq (f : List ℕ → ℕ → ℕ) (hf : f [] 0 = 0) (c : FCat) (k : ℕ) :
    c.getWith f k = f (c.get k).1 (c.get k).2.1 := by
  induction c generalizing k with
  | empty => exact hf.symm
  | row s d code => rfl
  | node l r ihl ihr =>
      have e1 : FCat.getWith f (.node l r) k =
          Bool.rec (r.getWith f (k / 2)) (l.getWith f (k / 2)) (Nat.beq (k % 2) 0) := rfl
      have e2 : FCat.get (.node l r) k =
          bif Nat.beq (k % 2) 0 then l.get (k / 2) else r.get (k / 2) := rfl
      rw [e1, e2]
      cases Nat.beq (k % 2) 0
      · exact ihr _
      · exact ihl _

theorem codeR_eq (base : ℕ) (s : List ℕ) : codeR base s = codeL base s := by
  induction s with
  | nil => rfl
  | cons i s ih =>
      show base ^ i + codeR base s = _
      rw [ih]
      simp [codeL]

theorem entQ_eq (rv : ℕ → ℕ) (K e : ℕ) : entQ rv K e = (e % K) * rv (e / K) := by
  show Nat.rec (motive := fun _ => ℕ) (Nat.mul (Nat.mod e K) (rv 0))
    (fun j _ => Nat.mul (Nat.mod e K) (rv (Nat.succ j))) (e / K) = _
  generalize e / K = r
  cases r <;> rfl

theorem sparseSum_append (value : ℕ → ℕ) (a b : List (ℕ × ℕ)) :
    sparseSum value (a ++ b) = sparseSum value a + sparseSum value b := by
  induction a with
  | nil => simp [sparseSum]
  | cons x a ih =>
      obtain ⟨r, w⟩ := x
      simp only [List.cons_append, sparseSum, ih]
      omega

theorem wordQ_eq (rv : ℕ → ℕ) (K J k y : ℕ) (acc : List ℕ) :
    wordQ rv K J k y + sparseSum rv (decode K acc) =
      sparseSum rv (decode K (pushDigits J k y acc)) := by
  induction k generalizing y with
  | zero => show 0 + _ = _; rw [Nat.zero_add]; rfl
  | succ k ih =>
      show entQ rv K (y % J) + wordQ rv K J k (y / J) + sparseSum rv (decode K acc) =
        sparseSum rv (decode K (y % J :: pushDigits J k (y / J) acc))
      rw [Nat.add_assoc, ih, entQ_eq]
      rfl

theorem leafQ_eq (rv : ℕ → ℕ) (K J k : ℕ) (ws : List ℕ) :
    leafQ rv K J k ws = sparseSum rv (decode K (expandW J k ws)) := by
  induction ws with
  | nil => rfl
  | cons y ws ih =>
      show wordQ rv K J k y + leafQ rv K J k ws = _
      rw [ih, wordQ_eq]
      rfl

theorem lenF_eq (l : List ℕ) : lenF l = l.length := by
  induction l with
  | nil => rfl
  | cons a l ih => show Nat.succ (lenF l) = _; rw [ih]; rfl

theorem beq_false_of_ne {a b : ℕ} (h : a ≠ b) : Nat.beq a b = false := by
  cases hb : Nat.beq a b
  · rfl
  · exact absurd (Nat.eq_of_beq_eq_true hb) h

theorem blt_false_of_not_lt {a b : ℕ} (h : ¬ a < b) : Nat.blt a b = false := by
  cases hb : Nat.blt a b
  · rfl
  · exact absurd (Nat.blt_eq.mp hb) h

theorem colF_eq (cap BIG v c : ℕ) :
    colF cap BIG v c = colOf cap c v + BIG * oneOf c v := by
  unfold colF colOf oneOf
  by_cases h1 : v = 1
  · subst h1; simp
  · by_cases h2 : v = 2
    · subst h2; simp; rfl
    · rw [beq_false_of_ne h1, beq_false_of_ne h2]
      simp [h1, h2]

theorem colLoop_eq (base cap BIG : ℕ) (mask : List ℕ) (p : ℕ) :
    colLoop base cap BIG mask p =
      zipSum (fun c v => colF cap BIG v c) (digits base mask.length p) mask := by
  induction mask generalizing p with
  | nil => rfl
  | cons v mask ih =>
      show colF cap BIG v (p % base) + colLoop base cap BIG mask (p / base) = _
      rw [ih]
      rfl

theorem setF_eq (x : ℕ) (l : List ℕ) (v : ℕ) : setF x l v = l.set v x := by
  induction l generalizing v with
  | nil => cases v <;> rfl
  | cons a as ih =>
      cases v with
      | zero => rfl
      | succ v =>
          show a :: setF x as v = _
          rw [ih]
          rfl

/-! ## Arithmetic lemmas -/

theorem packList_digits (base n p : ℕ) : packList base (digits base n p) = p % base ^ n := by
  induction n generalizing p with
  | zero => simp [digits, packList, Nat.mod_one]
  | succ n ih =>
      show p % base + base * packList base (digits base n (p / base)) = _
      rw [ih, pow_succ, Nat.mul_comm (base ^ n) base, Nat.mod_mul]

theorem pack_lt {n base : ℕ} (f : Fin n → ℕ) (hf : ∀ i, f i < base) : pack base f < base ^ n := by
  induction n with
  | zero => simp [pack]
  | succ n ih =>
      rw [pack_succ, pow_succ]
      have h1 := ih (fun i => f i.succ) (fun i => hf _)
      have h0 := hf 0
      have h2 : base * (pack base (fun i => f i.succ) + 1) ≤ base * base ^ n :=
        Nat.mul_le_mul_left _ h1
      rw [Nat.mul_add, Nat.mul_one, Nat.mul_comm base (base ^ n)] at h2
      rw [Nat.mul_comm (base ^ n) base] at h2 ⊢
      omega

theorem zipSum_colOf_lt (cap base : ℕ) (cs mask : List ℕ) (hc : ∀ x ∈ cs, x < base) :
    zipSum (colOf cap) cs mask + base ≤ (cs.length + 1) * base := by
  induction cs generalizing mask with
  | nil => simp [zipSum]
  | cons c cs ih =>
      have hc0 : c < base := hc c (by simp)
      have hrest := ih mask.tail (fun x hx => hc x (by simp [hx]))
      have hle : colOf cap c (mask.headD 0) ≤ c := by
        unfold colOf; split_ifs <;> omega
      show colOf cap c (mask.headD 0) + zipSum (colOf cap) cs mask.tail + base ≤
        (cs.length + 1 + 1) * base
      rw [Nat.add_mul (cs.length + 1) 1 base, Nat.one_mul]
      omega

theorem zipSum_add (f g : ℕ → ℕ → ℕ) (cs mask : List ℕ) :
    zipSum (fun c v => f c v + g c v) cs mask = zipSum f cs mask + zipSum g cs mask := by
  induction cs generalizing mask with
  | nil => rfl
  | cons c cs ih =>
      show (f c (mask.headD 0) + g c (mask.headD 0)) +
          zipSum (fun c v => f c v + g c v) cs mask.tail =
        (f c (mask.headD 0) + zipSum f cs mask.tail) + (g c (mask.headD 0) + zipSum g cs mask.tail)
      rw [ih]
      omega

theorem zipSum_mul (B : ℕ) (g : ℕ → ℕ → ℕ) (cs mask : List ℕ) :
    zipSum (fun c v => B * g c v) cs mask = B * zipSum g cs mask := by
  induction cs generalizing mask with
  | nil => rfl
  | cons c cs ih =>
      show B * g c (mask.headD 0) + zipSum (fun c v => B * g c v) cs mask.tail =
        B * (g c (mask.headD 0) + zipSum g cs mask.tail)
      rw [ih, Nat.mul_add]

/-- The two halves of a `colLoop` value. -/
theorem colLoop_split (base cap n p : ℕ) (mask : List ℕ) (hlen : mask.length = n)
    (hb : 0 < base) :
    colLoop base cap (bigF n base) mask p % bigF n base =
        zipSum (colOf cap) (digits base n p) mask ∧
      colLoop base cap (bigF n base) mask p / bigF n base =
        zipSum oneOf (digits base n p) mask := by
  have hX : colLoop base cap (bigF n base) mask p =
      zipSum (colOf cap) (digits base n p) mask +
        bigF n base * zipSum oneOf (digits base n p) mask := by
    rw [colLoop_eq, hlen, ← zipSum_mul, ← zipSum_add]
    simp only [colF_eq]
  have hlt : zipSum (colOf cap) (digits base n p) mask < bigF n base := by
    have := zipSum_colOf_lt cap base (digits base n p) mask (digits_lt base n p hb)
    rw [digits_length] at this
    show _ < (n + 1) * base
    omega
  have hpos : 0 < bigF n base := by
    show 0 < (n + 1) * base
    exact Nat.mul_pos (Nat.succ_pos n) hb
  rw [hX]
  constructor
  · rw [Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hlt]
  · rw [Nat.add_mul_div_left _ _ hpos, Nat.div_eq_of_lt hlt, Nat.zero_add]

theorem card_mset_eq (n : ℕ) (mask cs : List ℕ) (hlen : cs.length = n) :
    (mset n mask 1).card = zipSum oneOf cs mask := by
  subst hlen
  rw [zipSum_eq, mset, Finset.card_filter]
  rfl

/-! ## The fused leaf -/

/-- Entries that `rowVal` keeps. -/
def keep (c : FCat) (m : ℕ) (es : List (ℕ × ℕ)) : List (ℕ × ℕ) :=
  es.filter (fun x => decide (x.1 < m ∧ 0 < c.dem x.1))

theorem rowVal_eq (c : FCat) (m base BN r : ℕ) :
    rowVal c m base BN r =
      if r < m ∧ 0 < c.dem r then codeL base (c.get r).1 + BN * c.dem r else 0 := by
  unfold rowVal
  rw [FCat.getWith_eq _ rfl]
  rw [show (c.get r).2.1 = c.dem r from rfl]
  by_cases hr : r < m
  · have : Nat.blt r m = true := Nat.blt_eq.mpr hr
    rw [this]
    by_cases hd : 0 < c.dem r
    · have : Nat.blt 0 (c.dem r) = true := Nat.blt_eq.mpr hd
      rw [this, if_pos ⟨hr, hd⟩, ← codeR_eq]
      rfl
    · rw [blt_false_of_not_lt hd, if_neg (fun h => hd h.2)]
  · rw [blt_false_of_not_lt hr, if_neg (fun h => hr h.1)]

theorem sparseSum_rowVal (c : FCat) (m base BN : ℕ) (es : List (ℕ × ℕ)) :
    sparseSum (rowVal c m base BN) es =
      sparseSum (fun r => codeL base (c.get r).1) (keep c m es) +
        BN * sparseSum c.dem (keep c m es) := by
  induction es with
  | nil => rfl
  | cons x es ih =>
      obtain ⟨r, w⟩ := x
      rw [sparseSum, rowVal_eq, ih]
      by_cases h : r < m ∧ 0 < c.dem r
      · rw [if_pos h]
        have hk : keep c m ((r, w) :: es) = (r, w) :: keep c m es := by
          simp [keep, h.1, h.2]
        rw [hk, sparseSum, sparseSum, Nat.mul_add, Nat.mul_add, Nat.mul_left_comm w BN]
        omega
      · rw [if_neg h]
        have hk : keep c m ((r, w) :: es) = keep c m es := by
          simp only [keep, List.filter_cons]
          rw [if_neg (by simpa using h)]
        rw [hk]
        omega

theorem keep_spec (c : FCat) (m : ℕ) (es : List (ℕ × ℕ)) :
    ∀ x ∈ keep c m es, x.1 < m ∧ 0 < c.dem x.1 := by
  intro x hx
  simpa [keep] using (List.mem_filter.mp hx).2

theorem weight_le_dem (c : FCat) (ent : List (ℕ × ℕ)) (h : ∀ x ∈ ent, 0 < c.dem x.1) :
    sparseSum (fun _ => 1) ent ≤ sparseSum c.dem ent := by
  induction ent with
  | nil => exact le_refl _
  | cons x ent ih =>
      obtain ⟨r, w⟩ := x
      have h0 : 0 < c.dem r := h (r, w) (by simp)
      have h1 := ih (fun y hy => h y (by simp [hy]))
      show w * 1 + _ ≤ w * c.dem r + _
      have : w * 1 ≤ w * c.dem r := Nat.mul_le_mul_left _ h0
      omega

theorem codeL_get_eq_rowCode {n base0 : ℕ} (c : FCat) (hwf : c.wf n base0 = true)
    (base r : ℕ) : codeL base (c.get r).1 = rowCode base (fsupp c n r) := by
  classical
  obtain ⟨hnd, hlt, -⟩ := c.get_wf hwf r
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
  rw [h1, List.sum_toFinset _ hnd]
  rfl

/-- `leafF_core` with the row code given as a function. -/
theorem leaf_core2 (c : FCat) (m budget base cap : ℕ) (mask : List ℕ)
    (ent : List (ℕ × ℕ)) (cs : List ℕ) (n : ℕ) (hlen : cs.length = n)
    (code : ℕ → ℕ) (hcode : ∀ r, code r = rowCode base (fsupp c n r))
    (hrowlt : ∀ x ∈ ent, x.1 < m) (hb : 1 < base)
    (hw : sparseSum (fun _ => 1) ent < base)
    (hc : ∀ x ∈ cs, x < base)
    (heq : packList base cs = sparseSum code ent)
    (hm : cap * (budget - zipSum oneOf cs mask) + zipSum (colOf cap) cs mask <
      sparseSum c.dem ent) :
    ¬ ∃ holes : Fin n → ℕ, FFeas c m n budget mask holes := by
  classical
  subst hlen
  have hc' : cs.all (fun x => decide (x < base)) = true :=
    List.all_eq_true.mpr (fun x hx => decide_eq_true (hc x hx))
  have hloads := load_eq_of_sparse_packed base cs (fsupp c cs.length)
    code ent hcode hb hw hc' heq
  set M := mset cs.length mask 1 with hM
  set O := mset cs.length mask 2 with hO
  have hcard : M.card = zipSum oneOf cs mask := card_mset_eq _ mask cs rfl
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

/-- The packed loads of kept entries stay below `base ^ n` once the weight sum is below `base`. -/
theorem packed_lt (c : FCat) (n base : ℕ) (code : ℕ → ℕ)
    (hcode : ∀ r, code r = rowCode base (fsupp c n r)) (ent : List (ℕ × ℕ))
    (hw : sparseSum (fun _ => 1) ent < base) :
    sparseSum code ent < base ^ n := by
  classical
  have hP : sparseSum code ent =
      pack base (load (fun i : Fin ent.length => fsupp c n (ent.get i).1)
        (fun i => (ent.get i).2)) := by
    rw [pack_load, sparseSum_eq_sum]
    simp only [hcode]
  rw [hP]
  apply pack_lt
  intro i
  apply lt_of_le_of_lt ?_ hw
  rw [sparseSum_eq_sum]
  unfold load
  simp only [Nat.mul_one]
  apply Finset.sum_le_sum
  intro r _
  split_ifs <;> omega

theorem leafF2_sound (c : FCat) (m n budget base0 base K J k cap : ℕ) (mask ws : List ℕ)
    (hwf : c.wf n base0 = true) (hlen : mask.length = n)
    (h : leafF2 c m n budget base K J k cap mask ws = true) :
    ¬ ∃ holes : Fin n → ℕ, FFeas c m n budget mask holes := by
  set BN := base ^ n with hBN
  set Q := leafQ (rowVal c m base BN) K J k ws with hQ
  set X := colLoop base cap (bigF n base) mask Q with hX
  have h' : leafTest budget base BN (bigF n base) cap Q X = true := h
  unfold leafTest at h'
  have hb : 1 < base := by
    cases hb' : Nat.blt 1 base
    · rw [hb'] at h'; exact (Bool.false_ne_true h').elim
    · exact Nat.blt_eq.mp hb'
  rw [Nat.blt_eq.mpr hb] at h'
  have hT : Q / BN < base := by
    cases hT' : Nat.blt (Q / BN) base
    · rw [show Nat.div Q BN = Q / BN from rfl, hT'] at h'
      exact (Bool.false_ne_true h').elim
    · exact Nat.blt_eq.mp hT'
  rw [show Nat.div Q BN = Q / BN from rfl, Nat.blt_eq.mpr hT] at h'
  have htest : cap * (budget - X / bigF n base) + X % bigF n base < Q / BN := Nat.blt_eq.mp h'
  -- the kept entries and the decomposition of `Q`
  set ent := keep c m (decode K (expandW J k ws)) with hent
  set code : ℕ → ℕ := fun r => codeL base (c.get r).1 with hcodedef
  have hcode : ∀ r, code r = rowCode base (fsupp c n r) :=
    fun r => codeL_get_eq_rowCode c hwf base r
  have hQeq : Q = sparseSum code ent + BN * sparseSum c.dem ent := by
    rw [hQ, leafQ_eq, sparseSum_rowVal]
  have hBNpos : 0 < BN := by rw [hBN]; exact Nat.pow_pos (by omega)
  have hD : sparseSum c.dem ent ≤ Q / BN := by
    rw [Nat.le_div_iff_mul_le hBNpos, hQeq]
    rw [Nat.mul_comm]
    omega
  have hspec := keep_spec c m (decode K (expandW J k ws))
  have hw : sparseSum (fun _ => 1) ent < base :=
    lt_of_le_of_lt (weight_le_dem c ent (fun x hx => (hspec x hx).2)) (lt_of_le_of_lt hD hT)
  have hPlt : sparseSum code ent < BN := packed_lt c n base code hcode ent hw
  have hmod : Q % BN = sparseSum code ent := by
    rw [hQeq, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hPlt]
  have hdiv : Q / BN = sparseSum c.dem ent := by
    rw [hQeq, Nat.add_mul_div_left _ _ hBNpos, Nat.div_eq_of_lt hPlt, Nat.zero_add]
  obtain ⟨hXmod, hXdiv⟩ := colLoop_split base cap n Q mask hlen (by omega)
  rw [← hX] at hXmod hXdiv
  rw [hXmod, hXdiv, hdiv] at htest
  exact leaf_core2 c m budget base cap mask ent (digits base n Q) n (digits_length _ _ _)
    code hcode (fun x hx => (hspec x hx).1) hb hw (digits_lt _ _ _ (by omega))
    (by rw [packList_digits, ← hBN, hmod]) htest

theorem overF_sound (n budget base : ℕ) (mask : List ℕ) (hlen : mask.length = n)
    (h : overF n budget base mask = true) :
    budget < (mset n mask 1).card := by
  have h' : budget < colLoop base 0 (bigF n base) mask 0 / bigF n base := Nat.blt_eq.mp h
  rcases Nat.eq_zero_or_pos base with h0 | hb
  · subst h0
    have : bigF n 0 = 0 := Nat.mul_zero _
    rw [this, Nat.div_zero] at h'
    omega
  · rw [(colLoop_split base 0 n 0 mask hlen hb).2,
      ← card_mset_eq n mask (digits base n 0) (digits_length _ _ _)] at h'
    exact h'

theorem treeF2_feas (c : FCat) (m n budget base0 base K J k : ℕ) (hwf : c.wf n base0 = true)
    (t : PTree) (mask : List ℕ) (hlen : mask.length = n)
    (h : treeF2 c m n budget base K J k t mask = true) :
    ¬ ∃ holes : Fin n → ℕ, FFeas c m n budget mask holes := by
  classical
  induction t generalizing mask with
  | overBudget =>
      have h' := overF_sound n budget base mask hlen h
      rintro ⟨holes, _, _, hb, hm, _⟩
      have hle : (mset n mask 1).card ≤ ∑ i, holes i := by
        calc (mset n mask 1).card = ∑ i ∈ mset n mask 1, holes i := by
              rw [Finset.card_eq_sum_ones]
              exact Finset.sum_congr rfl (fun i hi => (hm i hi).symm)
          _ ≤ ∑ i, holes i := Finset.sum_le_sum_of_subset (Finset.subset_univ _)
      omega
  | leaf cap ws => exact leafF2_sound c m n budget base0 base K J k cap mask ws hwf hlen h
  | split v z o ihz iho =>
      have h' : (treeF2 c m n budget base K J k z (setF 2 mask v) &&
          treeF2 c m n budget base K J k o (setF 1 mask v)) = true := by
        have e : treeF2 c m n budget base K J k (.split v z o) mask =
            Bool.rec false (treeF2 c m n budget base K J k o (setF 1 mask v))
              (treeF2 c m n budget base K J k z (setF 2 mask v)) := rfl
        rw [e] at h
        revert h
        cases treeF2 c m n budget base K J k z (setF 2 mask v) <;> simp
      rw [Bool.and_eq_true, setF_eq, setF_eq] at h'
      exact split_feas c m n budget mask v (ihz _ (by rw [List.length_set, hlen]) h'.1)
        (iho _ (by rw [List.length_set, hlen]) h'.2)

theorem checkF2_feas (c : FCat) (m n budget base0 base K J k : ℕ) (hwf : c.wf n base0 = true)
    (t : PTree) (mask : List ℕ)
    (h : checkF2 c m n budget base K J k t mask = true) :
    ¬ ∃ holes : Fin n → ℕ, FFeas c m n budget mask holes := by
  have h' : Bool.rec false (treeF2 c m n budget base K J k t mask)
      (Nat.beq (lenF mask) n) = true := h
  cases hb : Nat.beq (lenF mask) n
  · rw [hb] at h'
    exact (Bool.false_ne_true h').elim
  · rw [hb] at h'
    have hlen : mask.length = n := by
      rw [← lenF_eq]
      exact Nat.eq_of_beq_eq_true hb
    exact treeF2_feas c m n budget base0 base K J k hwf t mask hlen h'

/-- Soundness of the fused checker, in the shape of `CertificateTree.check_sound`
(and of `checkF_sound`). `base0` is the catalog's base, `base` the leaf base. -/
theorem checkF2_sound (c : FCat) (m n budget base0 base K J k : ℕ)
    (hwf : c.wf n base0 = true) (t : PTree) (mask : List ℕ)
    (h : checkF2 c m n budget base K J k t mask = true) :
    ¬ ∃ holes : Fin n → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r : Fin m, c.dem r.val ≤ ∑ i ∈ fsupp c n r.val, holes i) ∧
      (∑ i, holes i) ≤ budget ∧
      (∀ i ∈ mset n mask 1, holes i = 1) ∧ (∀ i ∈ mset n mask 2, holes i = 0) :=
  checkF2_feas c m n budget base0 base K J k hwf t mask h

end

end CompactChecker

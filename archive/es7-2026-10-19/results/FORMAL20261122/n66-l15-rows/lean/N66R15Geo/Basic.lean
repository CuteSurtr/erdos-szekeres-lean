import Mathlib.Data.List.Sort
import Batteries.Data.List.Perm
import N66R15Enc.Gen

/-!
# N66R15Geo.Basic: data validity, the numbering, and the DIMACS transfer (theorem side)

* `mem_combs_iff`: `combs k l` lists exactly the length-`k` sublists of `l`; `sublist_range_iff`.
* `Atom.Ok n`: the atom's positions are increasing and below `n` (and `2 ≤ k ≤ 4` for thresholds); `mem_alloc`,
  `ok_of_mem_alloc`, `code_inj` (positions below 32).
* `certOk`: the data of a certificate is well formed (a Bool, kernel-checked for the 629 certificates).
* `finClause_sat`, `finClause_atoms`: the constant folding keeps a true literal and creates no atom.
* `dimacsSat_of_meaning`: if every structured clause has a literal that `meaning` makes true and all atoms are
  `Ok`, the DIMACS CNF `certCnf t` is satisfiable (ν v := meaning of the `v`-th allocated atom).
-/

namespace N66R15Enc

/-! ## Sublists -/

theorem mem_combs_iff : ∀ (k : Nat) (l s : List Nat), s ∈ combs k l ↔ s.Sublist l ∧ s.length = k
  | 0, l, s => by
    have e : combs 0 l = [[]] := by cases l <;> rfl
    rw [e, List.mem_singleton]
    constructor
    · rintro rfl; exact ⟨List.nil_sublist _, rfl⟩
    · rintro ⟨-, h⟩; exact List.length_eq_zero_iff.1 h
  | k + 1, [], s => by
    simp only [combs, List.not_mem_nil, false_iff, not_and, List.sublist_nil]
    rintro rfl; simp
  | k + 1, x :: xs, s => by
    simp only [combs, List.mem_append, List.mem_map, mem_combs_iff k xs, mem_combs_iff (k + 1) xs,
      List.sublist_cons_iff]
    constructor
    · rintro (⟨t, ⟨ht, hl⟩, rfl⟩ | ⟨h1, h2⟩)
      · exact ⟨Or.inr ⟨t, rfl, ht⟩, by simp [hl]⟩
      · exact ⟨Or.inl h1, h2⟩
    · rintro ⟨h | ⟨r, rfl, hr⟩, hl⟩
      · exact Or.inr ⟨h, hl⟩
      · exact Or.inl ⟨r, ⟨hr, by simpa using hl⟩, rfl⟩

theorem sublist_range_iff {s : List Nat} {n : Nat} :
    s.Sublist (List.range n) ↔ s.Pairwise (· < ·) ∧ ∀ x ∈ s, x < n := by
  constructor
  · intro h
    exact ⟨List.pairwise_lt_range.sublist h, fun x hx => List.mem_range.1 (h.subset hx)⟩
  · rintro ⟨hp, hb⟩
    have hnd : s.Nodup := hp.imp (fun h => Nat.ne_of_lt h)
    have hsub : s ⊆ List.range n := fun x hx => List.mem_range.2 (hb x hx)
    exact List.sublist_of_subperm_of_sorted (r := (· ≤ ·)) (List.subperm_of_subset hnd hsub)
      (hp.imp (fun h => Nat.le_of_lt h)) (List.pairwise_lt_range.imp (fun h => Nat.le_of_lt h))

theorem mem_combs_range {k n : Nat} {s : List Nat} :
    s ∈ combs k (List.range n) ↔ s.Pairwise (· < ·) ∧ (∀ x ∈ s, x < n) ∧ s.length = k := by
  rw [mem_combs_iff, sublist_range_iff, and_assoc]

theorem pair_mem {n i j : Nat} (h1 : i < j) (h2 : j < n) : [i, j] ∈ combs 2 (List.range n) := by
  rw [mem_combs_range]; simp [h1, h2]; omega

theorem triple_mem {n i j k : Nat} (h1 : i < j) (h2 : j < k) (h3 : k < n) :
    [i, j, k] ∈ combs 3 (List.range n) := by
  rw [mem_combs_range]; simp; omega

theorem quad_mem {n i j k l : Nat} (h1 : i < j) (h2 : j < k) (h3 : k < l) (h4 : l < n) :
    [i, j, k, l] ∈ combs 4 (List.range n) := by
  rw [mem_combs_range]; simp; omega

theorem combs2_shape {n : Nat} {s : List Nat} (h : s ∈ combs 2 (List.range n)) :
    ∃ i j, s = [i, j] ∧ i < j ∧ j < n := by
  rw [mem_combs_range] at h
  obtain ⟨hp, hb, hl⟩ := h
  match s, hl with
  | [i, j], _ => exact ⟨i, j, rfl, by simpa using hp, hb j (by simp)⟩

theorem combs3_shape {n : Nat} {s : List Nat} (h : s ∈ combs 3 (List.range n)) :
    ∃ i j k, s = [i, j, k] ∧ i < j ∧ j < k ∧ k < n := by
  rw [mem_combs_range] at h
  obtain ⟨hp, hb, hl⟩ := h
  match s, hl with
  | [i, j, k], _ =>
    exact ⟨i, j, k, rfl, List.rel_of_pairwise_cons hp List.mem_cons_self,
      List.rel_of_pairwise_cons hp.of_cons List.mem_cons_self, hb k (by simp)⟩

theorem combs4_shape {n : Nat} {s : List Nat} (h : s ∈ combs 4 (List.range n)) :
    ∃ i j k l, s = [i, j, k, l] ∧ i < j ∧ j < k ∧ k < l ∧ l < n := by
  rw [mem_combs_range] at h
  obtain ⟨hp, hb, hl⟩ := h
  match s, hl with
  | [i, j, k, l], _ =>
    exact ⟨i, j, k, l, rfl, List.rel_of_pairwise_cons hp List.mem_cons_self,
      List.rel_of_pairwise_cons hp.of_cons List.mem_cons_self,
      List.rel_of_pairwise_cons hp.of_cons.of_cons List.mem_cons_self, hb l (by simp)⟩

/-! ## Atoms -/

def Atom.Ok (n : Nat) : Atom → Prop
  | .bef i j => i < j ∧ j < n
  | .ge _ i j k => i < j ∧ j < n ∧ 2 ≤ k ∧ k ≤ 4
  | .ori i j k => i < j ∧ j < k ∧ k < n
  | .cvx i j k l => i < j ∧ j < k ∧ k < l ∧ l < n

theorem mem_alloc {n : Nat} : ∀ {a : Atom}, a.Ok n → a ∈ alloc n
  | .bef i j, ⟨h1, h2⟩ => by
    unfold alloc
    refine List.mem_append_left _ (List.mem_append_left _ (List.mem_flatMap.2 ⟨[i, j], pair_mem h1 h2, ?_⟩))
    simp [allocPair]
  | .ge c i j k, ⟨h1, h2, h3, h4⟩ => by
    unfold alloc
    refine List.mem_append_left _ (List.mem_append_left _ (List.mem_flatMap.2 ⟨[i, j], pair_mem h1 h2, ?_⟩))
    have : k = 2 ∨ k = 3 ∨ k = 4 := by omega
    rcases this with rfl | rfl | rfl <;> cases c <;> simp [allocPair]
  | .ori i j k, ⟨h1, h2, h3⟩ => by
    unfold alloc
    refine List.mem_append_left _ (List.mem_append_right _ (List.mem_filterMap.2 ⟨[i, j, k], triple_mem h1 h2 h3, ?_⟩))
    rfl
  | .cvx i j k l, ⟨h1, h2, h3, h4⟩ => by
    unfold alloc
    exact List.mem_append_right _ (List.mem_filterMap.2 ⟨[i, j, k, l], quad_mem h1 h2 h3 h4, rfl⟩)

theorem ok_of_mem_alloc {n : Nat} {a : Atom} (h : a ∈ alloc n) : a.Ok n := by
  unfold alloc at h
  simp only [List.mem_append, List.mem_flatMap, List.mem_filterMap] at h
  rcases h with (⟨p, hp, ha⟩ | ⟨p, hp, ha⟩) | ⟨p, hp, ha⟩
  · obtain ⟨i, j, rfl, h1, h2⟩ := combs2_shape hp
    simp only [allocPair, List.mem_cons, List.not_mem_nil, or_false] at ha
    rcases ha with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> simp [Atom.Ok] <;> omega
  · obtain ⟨i, j, k, rfl, h1, h2, h3⟩ := combs3_shape hp
    simp only [Option.some.injEq] at ha
    subst ha; exact ⟨h1, h2, h3⟩
  · obtain ⟨i, j, k, l, rfl, h1, h2, h3, h4⟩ := combs4_shape hp
    simp only [Option.some.injEq] at ha
    subst ha; exact ⟨h1, h2, h3, h4⟩

theorem digit32 {a b a' b' : ℕ} (ha : a < 32) (ha' : a' < 32) (h : a + 32 * b = a' + 32 * b') :
    a = a' ∧ b = b' := by
  have h1 : (a + 32 * b) % 32 = (a' + 32 * b') % 32 := by rw [h]
  have h2 : (a + 32 * b) / 32 = (a' + 32 * b') / 32 := by rw [h]
  rw [Nat.add_mul_mod_self_left, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt ha, Nat.mod_eq_of_lt ha'] at h1
  rw [Nat.add_mul_div_left _ _ (by omega), Nat.add_mul_div_left _ _ (by omega), Nat.div_eq_of_lt ha,
    Nat.div_eq_of_lt ha'] at h2
  exact ⟨h1, by omega⟩

theorem code_inj {n : Nat} (hn : n ≤ 32) : ∀ {a b : Atom}, a.Ok n → b.Ok n → code a = code b → a = b := by
  intro a b ha hb h
  cases a with
  | bef i j =>
    cases b with
    | bef i' j' => simp only [Atom.Ok, code] at ha hb h; simp only [Atom.bef.injEq]; exact ⟨by omega, by omega⟩
    | ge c i' j' k' => exfalso; simp only [code] at h; omega
    | ori i' j' k' => exfalso; simp only [code] at h; omega
    | cvx i' j' k' l' => exfalso; simp only [code] at h; omega
  | ge c i j k =>
    cases b with
    | bef i' j' => exfalso; simp only [code] at h; omega
    | ge c' i' j' k' =>
      simp only [Atom.Ok, code] at ha hb h
      simp only [Atom.ge.injEq]
      cases c <;> cases c' <;> simp at h ⊢ <;> omega
    | ori i' j' k' => exfalso; simp only [code] at h; omega
    | cvx i' j' k' l' => exfalso; simp only [code] at h; omega
  | ori i j k =>
    cases b with
    | bef i' j' => exfalso; simp only [code] at h; omega
    | ge c i' j' k' => exfalso; simp only [code] at h; omega
    | ori i' j' k' =>
      simp only [Atom.Ok, code] at ha hb h; simp only [Atom.ori.injEq]
      have h0 : i + 32 * (j + 32 * k) = i' + 32 * (j' + 32 * k') := by omega
      obtain ⟨e1, h1⟩ := digit32 (by omega) (by omega) h0
      obtain ⟨e2, e3⟩ := digit32 (by omega) (by omega) h1
      exact ⟨e1, e2, e3⟩
    | cvx i' j' k' l' => exfalso; simp only [code] at h; omega
  | cvx i j k l =>
    cases b with
    | bef i' j' => exfalso; simp only [code] at h; omega
    | ge c i' j' k' => exfalso; simp only [code] at h; omega
    | ori i' j' k' => exfalso; simp only [code] at h; omega
    | cvx i' j' k' l' =>
      simp only [Atom.Ok, code] at ha hb h; simp only [Atom.cvx.injEq]
      have h0 : i + 32 * (j + 32 * (k + 32 * l)) = i' + 32 * (j' + 32 * (k' + 32 * l')) := by omega
      obtain ⟨e1, h1⟩ := digit32 (by omega) (by omega) h0
      obtain ⟨e2, h2⟩ := digit32 (by omega) (by omega) h1
      obtain ⟨e3, e4⟩ := digit32 (by omega) (by omega) h2
      exact ⟨e1, e2, e3, e4⟩

/-! ## Data validity -/

def strictUp : List Nat → Bool
  | a :: b :: rest => decide (a < b) && strictUp (b :: rest)
  | _ => true

def octOk (n : Nat) (e : List Nat) : Bool := e.length == 8 && strictUp e && e.all (· < n)

def testOk (n : Nat) : Test → Bool
  | .E u v => decide (u < n) && decide (v < n) && u != v
  | .D u v _ _ => decide (u < n) && decide (v < n) && u != v
  | .P p q r => decide (p < n) && decide (q < n) && decide (r < n) && p != q && q != r && p != r

def octsOk (n : Nat) : Option (List (List Nat)) → Bool
  | none => true
  | some es => es.all (octOk n)

/-- **Well-formed data** (kernel-checked for the 629 certificates). For a core the tests are generated
(`allTests`), so only the size and the octagon list are checked. -/
def certOk : Cert → Bool
  | .tmpl n ts o => decide (n ≤ 32) && ts.all (testOk n) && octsOk n o
  | .core S o => decide (S.length ≤ 32) && octsOk S.length o

theorem strictUp_pairwise : ∀ {e : List Nat}, strictUp e = true → e.Pairwise (· < ·)
  | [], _ => List.Pairwise.nil
  | [a], _ => by simp
  | a :: b :: rest, h => by
    simp only [strictUp, Bool.and_eq_true, decide_eq_true_eq] at h
    have ih := strictUp_pairwise h.2
    refine List.Pairwise.cons ?_ ih
    intro x hx
    rcases List.mem_cons.1 hx with rfl | hx
    · exact h.1
    · exact Nat.lt_trans h.1 (List.rel_of_pairwise_cons ih hx)

/-! ## Constant folding -/

def L3.eval (m : Atom → Bool) : L3 → Bool
  | .t => true
  | .f => false
  | .lit p a => m a == p

theorem L3.eval_neg (m : Atom → Bool) (l : L3) : l.neg.eval m = !l.eval m := by
  cases l with
  | t => rfl
  | f => rfl
  | lit p a => simp only [L3.neg, L3.eval]; cases m a <;> cases p <;> rfl

theorem finClause_mem : ∀ {L : List L3} {cl : List (Bool × Atom)}, finClause L = some cl →
    ∀ x ∈ cl, L3.lit x.1 x.2 ∈ L
  | [], cl, h => by simp [finClause] at h; subst h; simp
  | .t :: _, _, h => by simp [finClause] at h
  | .f :: ls, cl, h => by
    simp only [finClause] at h
    intro x hx; exact List.mem_cons_of_mem _ (finClause_mem h x hx)
  | .lit p a :: ls, cl, h => by
    simp only [finClause] at h
    obtain ⟨cl', h', rfl⟩ := Option.map_eq_some_iff.1 h
    intro x hx
    rcases List.mem_cons.1 hx with rfl | hx
    · exact List.mem_cons_self
    · exact List.mem_cons_of_mem _ (finClause_mem h' x hx)

theorem finClause_sat (m : Atom → Bool) : ∀ {L : List L3} {cl : List (Bool × Atom)}, finClause L = some cl →
    (∃ l ∈ L, l.eval m = true) → ∃ x ∈ cl, m x.2 = x.1
  | [], _, _, ⟨l, hl, _⟩ => absurd hl List.not_mem_nil
  | .t :: _, _, h, _ => by simp [finClause] at h
  | .f :: ls, cl, h, ⟨l, hl, he⟩ => by
    simp only [finClause] at h
    rcases List.mem_cons.1 hl with rfl | hl
    · simp [L3.eval] at he
    · exact finClause_sat m h ⟨l, hl, he⟩
  | .lit p a :: ls, cl, h, ⟨l, hl, he⟩ => by
    simp only [finClause] at h
    obtain ⟨cl', h', rfl⟩ := Option.map_eq_some_iff.1 h
    rcases List.mem_cons.1 hl with rfl | hl
    · refine ⟨(p, a), List.mem_cons_self, ?_⟩
      simpa [L3.eval] using he
    · obtain ⟨x, hx, hxe⟩ := finClause_sat m h' ⟨l, hl, he⟩
      exact ⟨x, List.mem_cons_of_mem _ hx, hxe⟩

/-! ## DIMACS transfer -/

theorem litSat_pos' (ν : Nat → Bool) (k : Nat) (hk : 0 < k) : EncB.LitSat ν (k : Int) ↔ ν k = true := by
  simp only [EncB.LitSat, Int.natAbs_natCast]
  constructor
  · rintro (⟨_, h⟩ | ⟨h, _⟩)
    · exact h
    · omega
  · intro h; exact Or.inl ⟨by omega, h⟩

theorem litSat_neg'' (ν : Nat → Bool) (k : Nat) (hk : 0 < k) : EncB.LitSat ν (-(k : Int)) ↔ ν k = false := by
  simp only [EncB.LitSat, Int.natAbs_neg, Int.natAbs_natCast]
  constructor
  · rintro (⟨h, _⟩ | ⟨_, h⟩)
    · omega
    · exact h
  · intro h; exact Or.inr ⟨by omega, h⟩

/-- The assignment of variable numbers induced by an assignment of atoms. -/
def nuOf (n : Nat) (meaning : Atom → Bool) (v : Nat) : Bool := meaning ((alloc n).getD (v - 1) (.bef 0 0))

theorem numberMap_alloc {n : Nat} (hn : n ≤ 32) {a : Atom} (ha : a.Ok n) :
    0 < (EncB.numberMap (allocCodes n)).getD (code a) 0 ∧
      (alloc n).getD ((EncB.numberMap (allocCodes n)).getD (code a) 0 - 1) (.bef 0 0) = a := by
  have hmem : code a ∈ allocCodes n := List.mem_map_of_mem (mem_alloc ha)
  have hle := EncB.numberMap_getD_le hmem
  have hdec := EncB.decode_numberMap hmem
  refine ⟨by omega, ?_⟩
  set N := (EncB.numberMap (allocCodes n)).getD (code a) 0
  have hlenC : (allocCodes n).length = (alloc n).length := List.length_map _
  have hlen : N - 1 < (alloc n).length := by omega
  have hlen' : N - 1 < (allocCodes n).length := by omega
  unfold EncB.decode at hdec
  rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hlen', Option.getD_some] at hdec
  unfold allocCodes at hdec
  rw [List.getElem_map] at hdec
  rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hlen, Option.getD_some]
  exact code_inj hn (ok_of_mem_alloc (List.getElem_mem hlen)) ha hdec

/-- **Model transfer.** -/
theorem dimacsSat_of_meaning {t : Cert} (hn : t.n ≤ 32) (meaning : Atom → Bool)
    (hok : ∀ cl ∈ clsS t, ∀ x ∈ cl, x.2.Ok t.n)
    (hsat : ∀ cl ∈ clsS t, ∃ x ∈ cl, meaning x.2 = x.1) : EncB.DimacsSatisfiable (certCnf t) := by
  refine ⟨nuOf t.n meaning, ?_⟩
  intro cl hcl
  unfold certCnf at hcl
  obtain ⟨cl', hcl', rfl⟩ := List.mem_map.1 hcl
  obtain ⟨x, hx, hxe⟩ := hsat cl' hcl'
  refine ⟨toLit _ x, List.mem_map_of_mem hx, ?_⟩
  obtain ⟨hpos, hget⟩ := numberMap_alloc hn (hok cl' hcl' x hx)
  have hnu : nuOf t.n meaning ((EncB.numberMap (allocCodes t.n)).getD (code x.2) 0) = meaning x.2 := by
    unfold nuOf; rw [hget]
  obtain ⟨p, a⟩ := x
  simp only at hxe hnu hpos ⊢
  unfold toLit
  cases p with
  | true =>
    simp only [if_true]
    exact Or.inl ⟨by exact_mod_cast hpos, by rw [Int.natAbs_natCast, hnu, hxe]⟩
  | false =>
    simp only [Bool.false_eq_true, if_false]
    exact Or.inr ⟨by omega, by rw [Int.natAbs_neg, Int.natAbs_natCast, hnu, hxe]⟩

end N66R15Enc

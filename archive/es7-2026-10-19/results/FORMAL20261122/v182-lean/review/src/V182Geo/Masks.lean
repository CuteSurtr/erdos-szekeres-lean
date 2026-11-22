import V182Geo.Defs
import V182Enc.Gen

/-!
# V182Geo.Masks: masks, the numbered edges and the structural 4-cycles (DESIGN.md §3.1)

* `ofMask m`: the subset of `{0..7}` with mask `m`; `vtx m`: the vertex (`X0` if `m` is not a vertex mask);
  `edgeOfIdx e = s(vtx (eT e), vtx (eO e))`: the edge with number `e` of the CNF numbering (V182Enc.Gen).
* `cyc_bridge`: for every structural 4-cycle `cyc X p q` of `V182Enc.cycles` the four vertices
  `X, X+p, X+p+q, X+q` form a 4-cycle subgraph of `G`, and the edges of `cyc X p q` are its four edges in order.
* `conflict_ne`: a rainbow colouring gives conflicting edges (`V182Enc.conflict`) different colours.
-/

namespace V182Geo
open V182Enc

/-- The subset of `{0, …, 7}` with mask `m`. -/
def ofMask (m : ℕ) : Finset (Fin 8) := Finset.univ.filter fun i => m.testBit i = true

@[simp] theorem mem_ofMask {m : ℕ} {i : Fin 8} : i ∈ ofMask m ↔ m.testBit i = true := by
  simp [ofMask]

/-- The vertex `{0,1,2}`. -/
def X0 : V := ⟨{0, 1, 2}, by decide⟩

/-- The vertex with mask `m` (`X0` when `m` has fewer than 3 or more than 5 of the bits 0..7). -/
def vtx (m : ℕ) : V := if h : 3 ≤ (ofMask m).card ∧ (ofMask m).card ≤ 5 then ⟨ofMask m, h⟩ else X0

theorem vtx_eq {m : ℕ} {s : Finset (Fin 8)} (hs : ofMask m = s) (h : 3 ≤ s.card ∧ s.card ≤ 5) :
    vtx m = ⟨s, h⟩ := by
  subst hs
  unfold vtx
  rw [dif_pos h]

/-- **The edge with number `e`** (CNF numbering): between the 4-set `eT e` and `eO e = eT e ^^^ 2^(e % 8)`. -/
def edgeOfIdx (e : ℕ) : Sym2 V := s(vtx (eT e), vtx (eO e))

/-! ## Bits -/

theorem ofMask_xor_insert {m p : ℕ} (hp : p < 8) (h : m.testBit p = false) :
    ofMask (m ^^^ 1 <<< p) = insert ⟨p, hp⟩ (ofMask m) := by
  ext i
  rw [mem_ofMask, Finset.mem_insert, mem_ofMask, Nat.testBit_xor, Nat.one_shiftLeft, Nat.testBit_two_pow]
  rcases eq_or_ne (i : ℕ) p with hi | hi
  · have hi' : i = ⟨p, hp⟩ := Fin.ext hi
    subst hi'
    simp [h]
  · have hi' : i ≠ ⟨p, hp⟩ := fun e => hi (by rw [e])
    have hpi : ¬ p = (i : ℕ) := fun e => hi e.symm
    simp [hi', hpi]

theorem ofMask_xor_erase {m p : ℕ} (hp : p < 8) (h : m.testBit p = true) :
    ofMask (m ^^^ 1 <<< p) = (ofMask m).erase ⟨p, hp⟩ := by
  ext i
  rw [mem_ofMask, Finset.mem_erase, mem_ofMask, Nat.testBit_xor, Nat.one_shiftLeft, Nat.testBit_two_pow]
  rcases eq_or_ne (i : ℕ) p with hi | hi
  · have hi' : i = ⟨p, hp⟩ := Fin.ext hi
    subst hi'
    simp [h]
  · have hi' : i ≠ ⟨p, hp⟩ := fun e => hi (by rw [e])
    have hpi : ¬ p = (i : ℕ) := fun e => hi e.symm
    simp [hi', hpi]

theorem or_eq_xor {m p : ℕ} (h : m.testBit p = false) : m ||| 1 <<< p = m ^^^ 1 <<< p := by
  apply Nat.eq_of_testBit_eq
  intro i
  rw [Nat.testBit_or, Nat.testBit_xor, Nat.one_shiftLeft, Nat.testBit_two_pow]
  rcases eq_or_ne p i with hi | hi
  · subst hi
    simp [h]
  · simp [hi]

theorem xor_xor_cancel (m x : ℕ) : m ^^^ x ^^^ x = m := by
  rw [Nat.xor_assoc, Nat.xor_self, Nat.xor_zero]

theorem testBit_or_two_pow {m p q : ℕ} (hpq : p ≠ q) (h : m.testBit q = false) :
    (m ||| 1 <<< p).testBit q = false := by
  rw [Nat.testBit_or, Nat.one_shiftLeft, Nat.testBit_two_pow, h]
  simp [hpq]

theorem lt256_or {m p : ℕ} (hm : m < 256) (hp : p < 8) : m ||| 1 <<< p < 256 := by
  have h1 : m < 2 ^ 8 := hm
  have h2 : 1 <<< p < 2 ^ 8 := by
    rw [Nat.one_shiftLeft]
    exact Nat.pow_lt_pow_right (by omega) hp
  exact Nat.or_lt_two_pow h1 h2

theorem lt256_xor {m p : ℕ} (hm : m < 256) (hp : p < 8) : m ^^^ 1 <<< p < 256 := by
  have h1 : m < 2 ^ 8 := hm
  have h2 : 1 <<< p < 2 ^ 8 := by
    rw [Nat.one_shiftLeft]
    exact Nat.pow_lt_pow_right (by omega) hp
  exact Nat.xor_lt_two_pow h1 h2

theorem ofMask_inj {m m' : ℕ} (hm : m < 256) (hm' : m' < 256) (h : ofMask m = ofMask m') : m = m' := by
  apply Nat.eq_of_testBit_eq
  intro i
  by_cases hi : i < 8
  · have e := congrArg (fun s => (⟨i, hi⟩ : Fin 8) ∈ s) h
    simp only [mem_ofMask] at e
    cases h1 : m.testBit i <;> cases h2 : m'.testBit i <;> simp_all
  · have h8 : 2 ^ 8 ≤ 2 ^ i := Nat.pow_le_pow_right (by omega) (by omega)
    rw [Nat.testBit_lt_two_pow (lt_of_lt_of_le (show m < 2 ^ 8 from hm) h8),
      Nat.testBit_lt_two_pow (lt_of_lt_of_le (show m' < 2 ^ 8 from hm') h8)]

/-- The size of a mask's subset is its bit count `pc` (kernel check over the 256 masks). -/
theorem card_ofMask_eq_pc : ∀ m, m < 256 → (ofMask m).card = pc m := by decide +kernel

theorem mem_fourMasks {T : ℕ} : T ∈ fourMasks ↔ T < 256 ∧ pc T = 4 := by
  simp [fourMasks, List.mem_filter, List.mem_range]

theorem mem_threeMasks {X : ℕ} : X ∈ threeMasks ↔ X < 256 ∧ pc X = 3 := by
  simp [threeMasks, List.mem_filter, List.mem_range]

theorem mem_bitPairs {X p q : ℕ} (h : (p, q) ∈ bitPairs X) :
    p < 8 ∧ q < 8 ∧ p < q ∧ X.testBit p = false ∧ X.testBit q = false := by
  unfold bitPairs at h
  obtain ⟨h1, h2⟩ := List.mem_filter.1 h
  obtain ⟨p', hp', h3⟩ := List.mem_flatMap.1 h1
  obtain ⟨q', hq', h4⟩ := List.mem_map.1 h3
  simp only [Prod.mk.injEq] at h4
  obtain ⟨rfl, rfl⟩ := h4
  simp only [Bool.and_eq_true, decide_eq_true_eq, Bool.not_eq_true'] at h2
  exact ⟨List.mem_range.1 hp', List.mem_range.1 hq', h2.1.1, h2.1.2, h2.2⟩

/-! ## The numbered edges -/

theorem eT_eidx {T x : ℕ} (hT : T ∈ fourMasks) (hx : x < 8) : eT (eidx T x) = T := by
  unfold eT eidx
  have h1 : (8 * fourMasks.idxOf T + x) / 8 = fourMasks.idxOf T := by omega
  rw [h1, List.getD_eq_getElem?_getD, List.getElem?_eq_getElem (List.idxOf_lt_length_of_mem hT),
    Option.getD_some]
  exact EncB.getElem_idxOf _

theorem eO_eidx {T x : ℕ} (hT : T ∈ fourMasks) (hx : x < 8) : eO (eidx T x) = T ^^^ 1 <<< x := by
  unfold eO
  rw [eT_eidx hT hx]
  have h2 : eidx T x % 8 = x := by unfold eidx; omega
  rw [h2]

theorem edgeOfIdx_eidx {T x : ℕ} (hT : T ∈ fourMasks) (hx : x < 8) :
    edgeOfIdx (eidx T x) = s(vtx T, vtx (T ^^^ 1 <<< x)) := by
  unfold edgeOfIdx
  rw [eT_eidx hT hx, eO_eidx hT hx]

/-! ## Structural 4-cycles are 4-cycle subgraphs -/

theorem ne_of_card_ne {u v : V} (h : u.1.card ≠ v.1.card) : u ≠ v := fun e => h (by rw [e])

/-- `(S, S+P, S+P+Q, S+Q)` is a 4-cycle subgraph for a 3-set `S` and distinct `P, Q ∉ S`. -/
theorem fourCycle_std {S : Finset (Fin 8)} {P Q : Fin 8} (hS : S.card = 3) (hP : P ∉ S) (hQ : Q ∉ S)
    (hPQ : P ≠ Q) (h1 : 3 ≤ S.card ∧ S.card ≤ 5) (h2 : 3 ≤ (insert P S).card ∧ (insert P S).card ≤ 5)
    (h3 : 3 ≤ (insert Q (insert P S)).card ∧ (insert Q (insert P S)).card ≤ 5)
    (h4 : 3 ≤ (insert Q S).card ∧ (insert Q S).card ≤ 5) :
    IsFourCycle ⟨S, h1⟩ ⟨insert P S, h2⟩ ⟨insert Q (insert P S), h3⟩ ⟨insert Q S, h4⟩ := by
  have cP : (insert P S).card = 4 := by rw [Finset.card_insert_of_notMem hP, hS]
  have hQP : Q ∉ insert P S := by
    rw [Finset.mem_insert, not_or]
    exact ⟨fun e => hPQ e.symm, hQ⟩
  have cPQ : (insert Q (insert P S)).card = 5 := by rw [Finset.card_insert_of_notMem hQP, cP]
  have cQ : (insert Q S).card = 4 := by rw [Finset.card_insert_of_notMem hQ, hS]
  have hbd : (⟨insert P S, h2⟩ : V) ≠ ⟨insert Q S, h4⟩ := by
    intro e
    have e' : insert P S = insert Q S := congrArg Subtype.val e
    have hm : P ∈ insert Q S := e' ▸ Finset.mem_insert_self P S
    rw [Finset.mem_insert] at hm
    rcases hm with hm | hm
    · exact hPQ hm
    · exact hP hm
  refine ⟨ne_of_card_ne ?_, ne_of_card_ne ?_, ne_of_card_ne ?_, ne_of_card_ne ?_, hbd, ne_of_card_ne ?_,
    Or.inl ⟨Finset.subset_insert P S, ?_⟩, Or.inl ⟨Finset.subset_insert Q (insert P S), ?_⟩,
    Or.inr ⟨Finset.insert_subset_insert Q (Finset.subset_insert P S), ?_⟩,
    Or.inr ⟨Finset.subset_insert Q S, ?_⟩⟩
  · show S.card ≠ (insert P S).card
    omega
  · show S.card ≠ (insert Q (insert P S)).card
    omega
  · show S.card ≠ (insert Q S).card
    omega
  · show (insert P S).card ≠ (insert Q (insert P S)).card
    omega
  · show (insert Q (insert P S)).card ≠ (insert Q S).card
    omega
  · show (insert P S).card = S.card + 1
    omega
  · show (insert Q (insert P S)).card = (insert P S).card + 1
    omega
  · show (insert Q (insert P S)).card = (insert Q S).card + 1
    omega
  · show (insert Q S).card = S.card + 1
    omega

/-- **Bridge.** Every structural 4-cycle `cyc X p q` of the CNF is a 4-cycle subgraph of `G`, edge by edge. -/
theorem cyc_bridge {X p q : ℕ} (hX : X ∈ threeMasks) (hpq : (p, q) ∈ bitPairs X) :
    IsFourCycle (vtx X) (vtx (X ||| 1 <<< p)) (vtx (X ||| 1 <<< p ||| 1 <<< q)) (vtx (X ||| 1 <<< q)) ∧
      (cyc X p q).map edgeOfIdx =
        [s(vtx X, vtx (X ||| 1 <<< p)), s(vtx (X ||| 1 <<< p), vtx (X ||| 1 <<< p ||| 1 <<< q)),
          s(vtx (X ||| 1 <<< p ||| 1 <<< q), vtx (X ||| 1 <<< q)), s(vtx (X ||| 1 <<< q), vtx X)] := by
  obtain ⟨hX256, hX3⟩ := mem_threeMasks.1 hX
  obtain ⟨hp8, hq8, hpq', hXp, hXq⟩ := mem_bitPairs hpq
  have hne : p ≠ q := by omega
  set S := ofMask X with hSdef
  set P : Fin 8 := ⟨p, hp8⟩
  set Q : Fin 8 := ⟨q, hq8⟩
  have hS : S.card = 3 := by rw [hSdef, card_ofMask_eq_pc X hX256, hX3]
  have hPS : P ∉ S := by rw [hSdef, mem_ofMask]; simp [P, hXp]
  have hQS : Q ∉ S := by rw [hSdef, mem_ofMask]; simp [Q, hXq]
  have hPQ : P ≠ Q := fun e => hne (congrArg Fin.val e)
  -- the masks
  have hA : X ||| 1 <<< p = X ^^^ 1 <<< p := or_eq_xor hXp
  have hB : X ||| 1 <<< q = X ^^^ 1 <<< q := or_eq_xor hXq
  have hAq : (X ||| 1 <<< p).testBit q = false := testBit_or_two_pow hne hXq
  have hC : X ||| 1 <<< p ||| 1 <<< q = (X ||| 1 <<< p) ^^^ 1 <<< q := or_eq_xor hAq
  have oA : ofMask (X ||| 1 <<< p) = insert P S := by rw [hA, ofMask_xor_insert hp8 hXp]
  have oB : ofMask (X ||| 1 <<< q) = insert Q S := by rw [hB, ofMask_xor_insert hq8 hXq]
  have oC : ofMask (X ||| 1 <<< p ||| 1 <<< q) = insert Q (insert P S) := by
    rw [hC, ofMask_xor_insert hq8 hAq, oA]
  have hQP : Q ∉ insert P S := by
    rw [Finset.mem_insert, not_or]
    exact ⟨fun e => hPQ e.symm, hQS⟩
  have cA : (insert P S).card = 4 := by rw [Finset.card_insert_of_notMem hPS, hS]
  have cB : (insert Q S).card = 4 := by rw [Finset.card_insert_of_notMem hQS, hS]
  have cC : (insert Q (insert P S)).card = 5 := by rw [Finset.card_insert_of_notMem hQP, cA]
  have h1 : 3 ≤ S.card ∧ S.card ≤ 5 := by omega
  have h2 : 3 ≤ (insert P S).card ∧ (insert P S).card ≤ 5 := by omega
  have h3 : 3 ≤ (insert Q (insert P S)).card ∧ (insert Q (insert P S)).card ≤ 5 := by omega
  have h4 : 3 ≤ (insert Q S).card ∧ (insert Q S).card ≤ 5 := by omega
  have va : vtx X = ⟨S, h1⟩ := vtx_eq hSdef.symm h1
  have vb : vtx (X ||| 1 <<< p) = ⟨insert P S, h2⟩ := vtx_eq oA h2
  have vc : vtx (X ||| 1 <<< p ||| 1 <<< q) = ⟨insert Q (insert P S), h3⟩ := vtx_eq oC h3
  have vd : vtx (X ||| 1 <<< q) = ⟨insert Q S, h4⟩ := vtx_eq oB h4
  -- membership in fourMasks
  have hA256 : X ||| 1 <<< p < 256 := lt256_or hX256 hp8
  have hB256 : X ||| 1 <<< q < 256 := lt256_or hX256 hq8
  have fA : X ||| 1 <<< p ∈ fourMasks := by
    rw [mem_fourMasks, ← card_ofMask_eq_pc _ hA256, oA, cA]
    exact ⟨hA256, rfl⟩
  have fB : X ||| 1 <<< q ∈ fourMasks := by
    rw [mem_fourMasks, ← card_ofMask_eq_pc _ hB256, oB, cB]
    exact ⟨hB256, rfl⟩
  refine ⟨?_, ?_⟩
  · rw [va, vb, vc, vd]
    exact fourCycle_std hS hPS hQS hPQ h1 h2 h3 h4
  · simp only [cyc, List.map_cons, List.map_nil]
    rw [edgeOfIdx_eidx fA hp8, edgeOfIdx_eidx fA hq8, edgeOfIdx_eidx fB hp8, edgeOfIdx_eidx fB hq8]
    have e1 : (X ||| 1 <<< p) ^^^ 1 <<< p = X := by rw [hA, xor_xor_cancel]
    have e2 : (X ||| 1 <<< p) ^^^ 1 <<< q = X ||| 1 <<< p ||| 1 <<< q := hC.symm
    have e3 : (X ||| 1 <<< q) ^^^ 1 <<< p = X ||| 1 <<< p ||| 1 <<< q := by
      rw [hC, hA, hB, Nat.xor_assoc, Nat.xor_assoc, Nat.xor_comm (1 <<< q) (1 <<< p)]
    have e4 : (X ||| 1 <<< q) ^^^ 1 <<< q = X := by rw [hB, xor_xor_cancel]
    rw [e1, e2, e3, e4, Sym2.eq_swap (a := vtx (X ||| 1 <<< p)) (b := vtx X),
      Sym2.eq_swap (a := vtx (X ||| 1 <<< q)) (b := vtx (X ||| 1 <<< p ||| 1 <<< q))]

/-- A rainbow colouring is injective on every structural 4-cycle. -/
theorem rainbow_cyc {α : Type*} {ψ : Sym2 V → α} (hψ : IsRainbowS ψ) {X p q : ℕ} (hX : X ∈ threeMasks)
    (hpq : (p, q) ∈ bitPairs X) : ((cyc X p q).map fun e => ψ (edgeOfIdx e)).Nodup := by
  obtain ⟨h4, hmap⟩ := cyc_bridge hX hpq
  have h := hψ _ _ _ _ h4
  have e : ((cyc X p q).map fun e => ψ (edgeOfIdx e)) = ((cyc X p q).map edgeOfIdx).map ψ := by
    rw [List.map_map]
    rfl
  rw [e, hmap]
  simpa using h

/-- **Conflicting edges get different colours** under a rainbow colouring. -/
theorem conflict_ne {α : Type*} {ψ : Sym2 V → α} (hψ : IsRainbowS ψ) {e f : ℕ} (h : conflict e f = true) :
    ψ (edgeOfIdx e) ≠ ψ (edgeOfIdx f) := by
  unfold conflict at h
  rw [Bool.and_eq_true, bne_iff_ne, List.any_eq_true] at h
  obtain ⟨hne, z, hz, hez⟩ := h
  rw [Bool.and_eq_true, List.contains_iff_mem, List.contains_iff_mem] at hez
  unfold cycles at hz
  obtain ⟨X, hX, hz'⟩ := List.mem_flatMap.1 hz
  obtain ⟨pq, hpq, rfl⟩ := List.mem_map.1 hz'
  have hnd := rainbow_cyc hψ hX (p := pq.1) (q := pq.2) hpq
  exact fun heq => hne (List.inj_on_of_nodup_map hnd hez.1 hez.2 heq)

end V182Geo

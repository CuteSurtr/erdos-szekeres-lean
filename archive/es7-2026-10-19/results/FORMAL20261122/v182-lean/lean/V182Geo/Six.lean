import V182Geo.Masks
import V182Chk.Walk

/-!
# V182Geo.Six: a rainbow 6-colouring of G (M5; Lean-checked outright)

The colouring is the notes' six-colour table (wave 1's decoding `verify/a2/col6_mine.json`, sha256 22cee12c…1578;
equal to an own decoding of `notes_src/diamond-colors.txt`, `tools/gen_six.py`), packed into `col6Big` by edge
(4-set mask `T`, bit `x`). The natural colouring `col6 : Sym2 V → Fin 6` reads the table at the masks of the two
ends (`toMask`, by choice from `exists_mask`).

Proof that `col6` is rainbow: adjacent vertices have masks differing in one bit (`toMask_adj`), so the masks of a
4-cycle subgraph `a-b-c-d` are a closed walk `m, m⊕2^i, m⊕2^i⊕2^j, m⊕2^i⊕2^j⊕2^k` of vertex masks with
`m ≠ m⊕2^i⊕2^j`, `m⊕2^i ≠ m⊕2^i⊕2^j⊕2^k` and `(last) ⊕ m` a single bit; `walk_all` checks all 256 × 8³ such walks in
the kernel (4,480 qualify) for four distinct colours, in 23 chunks (`V182Chk.Walk`).
-/

namespace V182Geo
open V182Enc

-- `popT`, `isV`, `col6At`, `onebit`, `rainbow4`, `walkBody`, the chunked kernel check `walk_all`, `walk_spec` and
-- `onebit_shl` are in the Std-only module `V182Chk.Walk` (kept out of the Mathlib environment for memory).

/-- Every vertex mask `< 256` passes `isV` (kernel check). -/
theorem isV_spec : ∀ m, m < 256 → 3 ≤ (ofMask m).card → (ofMask m).card ≤ 5 → isV m = true := by decide +kernel

/-! ## Masks of vertices -/

theorem exists_mask (s : Finset (Fin 8)) : ∃ m, m < 256 ∧ ofMask m = s := by
  induction s using Finset.induction_on with
  | empty =>
    refine ⟨0, by decide, ?_⟩
    ext i
    simp [ofMask]
  | insert a s ha ih =>
    obtain ⟨m, hm, rfl⟩ := ih
    have hbit : m.testBit a.val = false := by
      cases hb : m.testBit a.val with
      | false => rfl
      | true => exact absurd (mem_ofMask.2 hb) ha
    exact ⟨m ^^^ 1 <<< a.val, lt256_xor hm a.2, by rw [ofMask_xor_insert a.2 hbit]⟩

/-- A mask of a subset (by choice). -/
noncomputable def toMask (s : Finset (Fin 8)) : ℕ := Classical.choose (exists_mask s)

theorem toMask_lt (s : Finset (Fin 8)) : toMask s < 256 := (Classical.choose_spec (exists_mask s)).1

theorem ofMask_toMask (s : Finset (Fin 8)) : ofMask (toMask s) = s := (Classical.choose_spec (exists_mask s)).2

/-- **Adjacent vertices have masks differing in one bit.** -/
theorem toMask_adj {u v : V} (h : G.Adj u v) : ∃ i, i < 8 ∧ toMask v.1 = toMask u.1 ^^^ 1 <<< i := by
  have key : ∀ {s t : Finset (Fin 8)}, s ⊆ t → t.card = s.card + 1 →
      ∃ i, i < 8 ∧ toMask t = toMask s ^^^ 1 <<< i := by
    intro s t hst hc
    obtain ⟨a, ha, rfl⟩ := Finset.exists_eq_insert_iff.2 ⟨hst, hc.symm⟩
    refine ⟨a.val, a.2, ?_⟩
    have hbit : (toMask s).testBit a.val = false := by
      cases hb : (toMask s).testBit a.val with
      | false => rfl
      | true =>
        have : a ∈ ofMask (toMask s) := mem_ofMask.2 hb
        rw [ofMask_toMask] at this
        exact absurd this ha
    apply ofMask_inj (toMask_lt _) (lt256_xor (toMask_lt _) a.2)
    rw [ofMask_toMask, ofMask_xor_insert a.2 hbit, ofMask_toMask]
  rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩
  · exact key h1 h2
  · obtain ⟨i, hi, he⟩ := key h1 h2
    exact ⟨i, hi, by rw [he, xor_xor_cancel]⟩

theorem isV_of_vertex (u : V) : isV (toMask u.1) = true := by
  have h := isV_spec (toMask u.1) (toMask_lt _)
  rw [ofMask_toMask] at h
  exact h u.2.1 u.2.2

theorem toMask_inj {u v : V} (e : toMask u.1 = toMask v.1) : u = v :=
  Subtype.ext (by rw [← ofMask_toMask u.1, e, ofMask_toMask])

/-! ## The colouring -/

theorem col6At_comm (m m' : ℕ) : col6At m m' = col6At m' m := by
  unfold col6At
  rw [Nat.or_comm, Nat.and_comm, Nat.xor_comm]

theorem col6At_lt (m m' : ℕ) : col6At m m' < 6 := by
  unfold col6At
  exact Nat.mod_lt _ (by decide)

/-- **The six-colouring** of all pairs (only edges matter). -/
noncomputable def col6 : Sym2 V → Fin 6 :=
  Sym2.lift ⟨fun u v => ⟨col6At (toMask u.1) (toMask v.1), col6At_lt _ _⟩,
    fun u v => Fin.ext (col6At_comm _ _)⟩

theorem col6_rainbow : IsRainbowS col6 := by
  intro a b c d h
  obtain ⟨i, hi, hb⟩ := toMask_adj h.ab
  obtain ⟨j, hj, hc⟩ := toMask_adj h.bc
  obtain ⟨k, hk, hd⟩ := toMask_adj h.cd
  obtain ⟨l, hl, ha⟩ := toMask_adj h.da
  have hac : toMask a.1 ≠ toMask c.1 := fun e => h.ne_ac (toMask_inj e)
  have hbd : toMask b.1 ≠ toMask d.1 := fun e => h.ne_bd (toMask_inj e)
  have h1 : onebit (toMask d.1 ^^^ toMask a.1) = true := by
    rw [ha, ← Nat.xor_assoc, Nat.xor_self, Nat.zero_xor]
    exact onebit_shl l hl
  have hw := walk_spec (toMask_lt a.1) hi hj hk hb hc hd (isV_of_vertex a) (isV_of_vertex b) (isV_of_vertex c)
    (isV_of_vertex d) hac hbd h1
  apply List.Nodup.of_map Fin.val
  simp only [col6, Sym2.lift_mk, List.map_cons, List.map_nil]
  exact of_decide_eq_true hw

/-- **G has a rainbow edge colouring with 6 colours** (Lean-checked outright). -/
theorem rainbowColorable_six : RainbowColorable 6 := rainbowColorable_of_S col6_rainbow

end V182Geo

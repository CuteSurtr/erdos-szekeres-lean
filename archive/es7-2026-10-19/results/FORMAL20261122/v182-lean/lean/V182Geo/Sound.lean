import V182Geo.Masks
import EncB.Render

/-!
# V182Geo.Sound: every clause of B holds for the indicator of a normalised rainbow 5-colouring (M2)

`ind ψ` is the indicator assignment of `ψ : Sym2 V → Fin 5`: variable `5e + c + 1` is true iff the numbered edge
`e` has colour `c`. Families (DESIGN.md §2): ALO, CONF (`conflict_ne`), AMO, STAR (pigeonhole on 5 pairwise
conflicting edges), UNITS (the hypothesis `UnitsHold`). Also the literal bounds of `baseCnf` and of every piece, and
the transfer of the verdict hypothesis through `EncB.parseDimacs_renderCube`.
-/

namespace V182Geo
open V182Enc

/-- The indicator assignment of a colouring. -/
def ind (ψ : Sym2 V → Fin 5) (v : ℕ) : Bool := decide (((ψ (edgeOfIdx ((v - 1) / 5)) : Fin 5) : ℕ) = (v - 1) % 5)

theorem lit_natAbs (e c : ℕ) : (lit e c).natAbs = 5 * e + c + 1 := by
  unfold lit
  exact Int.natAbs_natCast _

theorem lit_pos (e c : ℕ) : (0 : ℤ) < lit e c := by
  unfold lit
  omega

theorem ind_lit (ψ : Sym2 V → Fin 5) {e c : ℕ} (hc : c < 5) :
    ind ψ (lit e c).natAbs = decide (((ψ (edgeOfIdx e)) : ℕ) = c) := by
  rw [lit_natAbs]
  unfold ind
  have h1 : (5 * e + c + 1 - 1) / 5 = e := by omega
  have h2 : (5 * e + c + 1 - 1) % 5 = c := by omega
  rw [h1, h2]

theorem litSat_lit (ψ : Sym2 V → Fin 5) {e c : ℕ} (hc : c < 5) :
    EncB.LitSat (ind ψ) (lit e c) ↔ ((ψ (edgeOfIdx e)) : ℕ) = c := by
  unfold EncB.LitSat
  have hp := lit_pos e c
  rw [ind_lit ψ hc]
  constructor
  · rintro (⟨-, h⟩ | ⟨h, -⟩)
    · exact of_decide_eq_true h
    · omega
  · intro h
    exact Or.inl ⟨hp, decide_eq_true h⟩

theorem litSat_neg_lit (ψ : Sym2 V → Fin 5) {e c : ℕ} (hc : c < 5) :
    EncB.LitSat (ind ψ) (-lit e c) ↔ ((ψ (edgeOfIdx e)) : ℕ) ≠ c := by
  unfold EncB.LitSat
  have hp := lit_pos e c
  rw [Int.natAbs_neg, ind_lit ψ hc]
  constructor
  · rintro (⟨h, -⟩ | ⟨-, h⟩)
    · omega
    · intro h'
      rw [decide_eq_true h'] at h
      exact absurd h (by decide)
  · intro h
    refine Or.inr ⟨by omega, ?_⟩
    simp [h]

/-- The 10 unit clauses hold: the normal form of DESIGN.md §3.3. -/
def UnitsHold (ψ : Sym2 V → Fin 5) : Prop := ∀ ec ∈ unitPairs, ((ψ (edgeOfIdx ec.1)) : ℕ) = ec.2

/-- Five distinct values below 5 take every value below 5. -/
theorem five_complete {L : List ℕ} (hnd : L.Nodup) (hlen : L.length = 5) (hlt : ∀ x ∈ L, x < 5) {c : ℕ}
    (hc : c < 5) : c ∈ L := by
  have h1 : L.toFinset ⊆ Finset.range 5 := fun x hx => Finset.mem_range.2 (hlt x (List.mem_toFinset.1 hx))
  have h2 : L.toFinset.card = 5 := by rw [List.toFinset_card_of_nodup hnd, hlen]
  have h3 : L.toFinset = Finset.range 5 := Finset.eq_of_subset_of_card_le h1 (by rw [h2, Finset.card_range])
  have h4 : c ∈ L.toFinset := by rw [h3]; exact Finset.mem_range.2 hc
  exact List.mem_toFinset.1 h4

/-- The colours on a list of pairwise conflicting distinct edges are pairwise distinct. -/
theorem nodup_colours {ψ : Sym2 V → Fin 5} (hψ : IsRainbowS ψ) {L : List ℕ} (hnd : L.Nodup)
    (hconf : ∀ e ∈ L, ∀ f ∈ L, e = f ∨ conflict e f = true) :
    (L.map fun e => ((ψ (edgeOfIdx e)) : ℕ)).Nodup := by
  refine List.Nodup.map_on ?_ hnd
  intro e he f hf h
  rcases hconf e he f hf with h' | h'
  · exact h'
  · exact absurd (Fin.ext h) (conflict_ne hψ h')

theorem allConf_spec {L : List ℕ} (h : allConf L = true) : ∀ e ∈ L, ∀ f ∈ L, e = f ∨ conflict e f = true := by
  intro e he f hf
  unfold allConf at h
  rw [List.all_eq_true] at h
  have h1 := h e he
  rw [List.all_eq_true] at h1
  have h2 := h1 f hf
  rw [Bool.or_eq_true, beq_iff_eq] at h2
  exact h2

/-- **M2.** The indicator of a rainbow colouring satisfying the units satisfies B. -/
theorem baseCnf_sat {ψ : Sym2 V → Fin 5} (hψ : IsRainbowS ψ) (hu : UnitsHold ψ) :
    EncB.DimacsSat baseCnf (ind ψ) := by
  intro cl hcl
  unfold baseCnf at hcl
  rcases List.mem_append.1 hcl with h | h5
  · rcases List.mem_append.1 h with h | h4
    · rcases List.mem_append.1 h with h | h3
      · rcases List.mem_append.1 h with h1 | h2
        · -- ALO
          unfold aloCls at h1
          obtain ⟨e, -, rfl⟩ := List.mem_map.1 h1
          refine ⟨lit e (ψ (edgeOfIdx e)), List.mem_map.2 ⟨_, List.mem_range.2 (ψ (edgeOfIdx e)).2, rfl⟩, ?_⟩
          exact (litSat_lit ψ (ψ (edgeOfIdx e)).2).2 rfl
        · -- CONF
          unfold confCls at h2
          obtain ⟨e, -, h2⟩ := List.mem_flatMap.1 h2
          obtain ⟨c, hc, h2⟩ := List.mem_flatMap.1 h2
          obtain ⟨f, hf, rfl⟩ := List.mem_map.1 h2
          have hc5 : c < 5 := List.mem_range.1 (List.mem_reverse.1 hc)
          unfold partnersDesc at hf
          have hf' := (List.mem_filter.1 (List.mem_reverse.1 hf)).2
          rw [Bool.and_eq_true] at hf'
          have hne := conflict_ne hψ hf'.2
          by_cases hec : ((ψ (edgeOfIdx e)) : ℕ) = c
          · refine ⟨-lit f c, List.mem_cons_of_mem _ (List.mem_singleton.2 rfl), ?_⟩
            exact (litSat_neg_lit ψ hc5).2 (fun hfc => hne (Fin.ext (hec.trans hfc.symm)))
          · exact ⟨-lit e c, List.mem_cons_self, (litSat_neg_lit ψ hc5).2 hec⟩
      · -- AMO
        unfold amoCls at h3
        obtain ⟨e, -, h3⟩ := List.mem_flatMap.1 h3
        obtain ⟨c1, hc1, h3⟩ := List.mem_flatMap.1 h3
        obtain ⟨c2, hc2, rfl⟩ := List.mem_map.1 h3
        have hc1' : c1 < 5 := List.mem_range.1 hc1
        have hc2' := List.mem_filter.1 hc2
        have hc2'' : c2 < 5 := List.mem_range.1 hc2'.1
        have hlt : c1 < c2 := of_decide_eq_true hc2'.2
        by_cases hec : ((ψ (edgeOfIdx e)) : ℕ) = c1
        · refine ⟨-lit e c2, List.mem_cons_of_mem _ (List.mem_singleton.2 rfl), ?_⟩
          exact (litSat_neg_lit ψ hc2'').2 (by omega)
        · exact ⟨-lit e c1, List.mem_cons_self, (litSat_neg_lit ψ hc1').2 hec⟩
    · -- STAR
      unfold surjCls at h4
      obtain ⟨v, -, h4⟩ := List.mem_flatMap.1 h4
      split at h4
      · next hif =>
        rw [Bool.and_eq_true, beq_iff_eq] at hif
        obtain ⟨c, hc, rfl⟩ := List.mem_map.1 h4
        have hc5 : c < 5 := List.mem_range.1 hc
        have hnd : (star v).Nodup := List.Nodup.filter _ List.nodup_range
        have hcol := nodup_colours hψ hnd (allConf_spec hif.2)
        have hlt : ∀ x ∈ (star v).map fun e => ((ψ (edgeOfIdx e)) : ℕ), x < 5 := by
          intro x hx
          obtain ⟨e, -, rfl⟩ := List.mem_map.1 hx
          exact (ψ (edgeOfIdx e)).2
        have hmem := five_complete hcol (by rw [List.length_map, hif.1]) hlt hc5
        obtain ⟨e, he, hec⟩ := List.mem_map.1 hmem
        exact ⟨lit e c, List.mem_map.2 ⟨e, he, rfl⟩, (litSat_lit ψ hc5).2 hec⟩
      · exact absurd h4 List.not_mem_nil
  · -- UNITS
    unfold unitCls at h5
    obtain ⟨ec, hec, rfl⟩ := List.mem_map.1 h5
    have hc : ec.2 < 5 := by
      have : ∀ x ∈ unitPairs, x.2 < 5 := by decide
      exact this ec hec
    exact ⟨lit ec.1 ec.2, List.mem_singleton.2 rfl, (litSat_lit ψ hc).2 (hu ec hec)⟩

/-! ## Literal bounds and the verdict transfer -/

theorem lit_wf {e c : ℕ} (he : e < 560) (hc : c < 5) : lit e c ≠ 0 ∧ (lit e c).natAbs ≤ nVars := by
  refine ⟨ne_of_gt (lit_pos e c), ?_⟩
  rw [lit_natAbs]
  unfold nVars
  omega

theorem neg_lit_wf {e c : ℕ} (he : e < 560) (hc : c < 5) : -lit e c ≠ 0 ∧ (-lit e c).natAbs ≤ nVars := by
  rw [Int.natAbs_neg]
  exact ⟨neg_ne_zero.2 (lit_wf he hc).1, (lit_wf he hc).2⟩

/-- Every literal of B is nonzero with `natAbs ≤ 2800` (the shape `EncB.parseDimacs_render` needs). -/
theorem baseCnf_wf : ∀ cl ∈ baseCnf, ∀ l ∈ cl, l ≠ 0 ∧ l.natAbs ≤ nVars := by
  intro cl hcl l hl
  unfold baseCnf at hcl
  rcases List.mem_append.1 hcl with h | h5
  · rcases List.mem_append.1 h with h | h4
    · rcases List.mem_append.1 h with h | h3
      · rcases List.mem_append.1 h with h1 | h2
        · unfold aloCls numE at h1
          obtain ⟨e, he, rfl⟩ := List.mem_map.1 h1
          obtain ⟨c, hc, rfl⟩ := List.mem_map.1 hl
          exact lit_wf (List.mem_range.1 he) (List.mem_range.1 hc)
        · unfold confCls at h2
          obtain ⟨e, he, h2⟩ := List.mem_flatMap.1 h2
          obtain ⟨c, hc, h2⟩ := List.mem_flatMap.1 h2
          obtain ⟨f, hf, rfl⟩ := List.mem_map.1 h2
          have he' : e < 560 := List.mem_range.1 (List.mem_reverse.1 he)
          have hc' : c < 5 := List.mem_range.1 (List.mem_reverse.1 hc)
          unfold partnersDesc at hf
          have hf' : f < 560 := List.mem_range.1 (List.mem_filter.1 (List.mem_reverse.1 hf)).1
          rcases List.mem_cons.1 hl with rfl | hl
          · exact neg_lit_wf he' hc'
          · rw [List.mem_singleton.1 hl]
            exact neg_lit_wf hf' hc'
      · unfold amoCls at h3
        obtain ⟨e, he, h3⟩ := List.mem_flatMap.1 h3
        obtain ⟨c1, hc1, h3⟩ := List.mem_flatMap.1 h3
        obtain ⟨c2, hc2, rfl⟩ := List.mem_map.1 h3
        have he' : e < 560 := List.mem_range.1 he
        rcases List.mem_cons.1 hl with rfl | hl
        · exact neg_lit_wf he' (List.mem_range.1 hc1)
        · rw [List.mem_singleton.1 hl]
          exact neg_lit_wf he' (List.mem_range.1 (List.mem_filter.1 hc2).1)
    · unfold surjCls at h4
      obtain ⟨v, -, h4⟩ := List.mem_flatMap.1 h4
      split at h4
      · obtain ⟨c, hc, rfl⟩ := List.mem_map.1 h4
        obtain ⟨e, he, rfl⟩ := List.mem_map.1 hl
        unfold V182Enc.star at he
        exact lit_wf (List.mem_range.1 (List.mem_filter.1 he).1) (List.mem_range.1 hc)
      · exact absurd h4 List.not_mem_nil
  · unfold unitCls at h5
    obtain ⟨ec, hec, rfl⟩ := List.mem_map.1 h5
    rw [List.mem_singleton.1 hl]
    have : ∀ x ∈ unitPairs, x.1 < 560 ∧ x.2 < 5 := by decide
    exact lit_wf (this ec hec).1 (this ec hec).2

theorem mem_permsOf_sub : ∀ (k : ℕ) (l p : List ℕ), p ∈ permsOf k l → ∀ x ∈ p, x ∈ l
  | 0, l, p, h, x, hx => by
    simp only [permsOf, List.mem_singleton] at h
    subst h
    exact absurd hx List.not_mem_nil
  | k + 1, l, p, h, x, hx => by
    simp only [permsOf] at h
    obtain ⟨a, ha, h⟩ := List.mem_flatMap.1 h
    obtain ⟨p', hp', rfl⟩ := List.mem_map.1 h
    rcases List.mem_cons.1 hx with rfl | hx
    · exact ha
    · exact List.mem_of_mem_erase (mem_permsOf_sub k _ p' hp' x hx)

theorem perms5_lt {p : List ℕ} (hp : p ∈ perms5) : ∀ x ∈ p, x < 5 := fun x hx =>
  List.mem_range.1 (mem_permsOf_sub 5 _ p hp x hx)

theorem getD_perms5_lt (n : ℕ) : ∀ x ∈ perms5.getD n [], x < 5 := by
  intro x hx
  rw [List.getD_eq_getElem?_getD] at hx
  cases h : perms5[n]? with
  | none => rw [h] at hx; exact absurd hx List.not_mem_nil
  | some p => rw [h] at hx; exact perms5_lt (List.mem_of_getElem? h) x hx

theorem mem_zipWith_lit : ∀ {S L : List ℕ} {l : ℤ}, l ∈ List.zipWith lit S L → ∃ e ∈ S, ∃ c ∈ L, l = lit e c
  | [], _, _, h => absurd h List.not_mem_nil
  | _ :: _, [], _, h => absurd h List.not_mem_nil
  | e :: S, c :: L, l, h => by
    rw [List.zipWith_cons_cons, List.mem_cons] at h
    rcases h with rfl | h
    · exact ⟨e, List.mem_cons_self, c, List.mem_cons_self, rfl⟩
    · obtain ⟨e', he', c', hc', rfl⟩ := mem_zipWith_lit h
      exact ⟨e', List.mem_cons_of_mem _ he', c', List.mem_cons_of_mem _ hc', rfl⟩

theorem starUnits_wf {S : List ℕ} (hS : ∀ e ∈ S, e < 560) (n : ℕ) :
    ∀ l ∈ starUnits S n, l ≠ 0 ∧ l.natAbs ≤ nVars := by
  intro l hl
  obtain ⟨e, he, c, hc, rfl⟩ := mem_zipWith_lit hl
  exact lit_wf (hS e he) (getD_perms5_lt n c hc)

theorem y1Star_lt : ∀ e ∈ y1Star, e < 560 := by decide
theorem y2Star_lt : ∀ e ∈ y2Star, e < 560 := by decide

theorem pieceCube_wf (q : ℕ × Option ℕ) : ∀ l ∈ pieceCube q, l ≠ 0 ∧ l.natAbs ≤ nVars := by
  rcases q with ⟨n, _ | m⟩
  · exact starUnits_wf y1Star_lt n
  · intro l hl
    rcases List.mem_append.1 hl with h | h
    · exact starUnits_wf y1Star_lt n l h
    · exact starUnits_wf y2Star_lt m l h

/-- **The verdict hypothesis**: for each of the 4,404 pieces, the text `pieceText q` (exactly what `v182print`
writes for piece `q`, hash-bound in M9) parses to an unsatisfiable clause list. Carried by the cake_lpr verdicts
`s VERIFIED UNSAT` under trust items E1-E6 (DESIGN.md §4). -/
def PieceVerdicts : Prop :=
  ∀ q ∈ pieces, ∀ (nv : ℕ) (F : List (List ℤ)), EncB.parseDimacs (pieceText q) = some (nv, F) →
    ¬ EncB.DimacsSatisfiable F

theorem piece_unsat (h : PieceVerdicts) {q : ℕ × Option ℕ} (hq : q ∈ pieces) :
    ¬ EncB.DimacsSatisfiable (EncB.cubeCnf baseCnf (pieceCube q)) :=
  h q hq _ _ (EncB.parseDimacs_renderCube nVars baseCnf (pieceCube q) baseCnf_wf (pieceCube_wf q))

end V182Geo

import N66G15.End

/-!
# N66R15Geo.Bound: `N66Bound 54` for any row list whose cube CNFs are refuted and whose rows are valid

n66-level15's end theorem `N66G15.n66_bound_54_of_cubes` is stated for its row list `R0_15` (an `include_str` parse).
Its proof uses `R0_15` only through `no_model_of_cubes`; everything else is generic. `n66_bound_54_of_rows` is the same
proof (`N66G15.n66_bound_54_of_gaps`, copied) with a row list `R` as a parameter, `N66E15.no_base_model` (generic in
`R`) in place of `no_model_of_cubes`, and the `Gaps` facts taken from n66-level15's proved chain
(`gaps_of_gaps2 ∘ … ∘ gaps4_of_gaps5`, with `capCup55_holds` and `mirror_holds`).
-/

namespace N66R15Geo
open ErdosSzekeres ErdosSzekeres.Omission N66E15 N66G15

/-- Every field of `N66G15.Gaps` (n66-level15's list of the facts the encoder needs), from its proved lemmas. -/
theorem gaps_proved : Gaps :=
  gaps_of_gaps2 (gaps2_of_gaps3 (gaps3_of_gaps4 (gaps4_of_gaps5 ⟨capCup55_holds, mirror_holds⟩)))

/-- **`N66Bound 54` from any row list `R`** such that the level-15 relaxation `fullCnf R c` is refuted for each of
the 105 leaf cubes and every row of `R` is valid. -/
theorem n66_bound_54_of_rows {R : List (List (Fin 70))}
    (h : ∀ c ∈ leaves105, ¬ EncB.DimacsSatisfiable (fullCnf R c)) (hR : RowsValid R) :
    OmissionZRow.N66Bound 54 := by
  have g : Gaps := gaps_proved
  intro n c hcap hcup hoct
  by_contra hn
  have hn55 : 55 ≤ n := by omega
  have hc : InClass c := ⟨hcap, hcup, hoct⟩
  obtain ⟨c', hc', hlex⟩ : ∃ c' : Configuration n, InClass c' ∧ LexOcc (n66Occ c'.cup n) := by
    rcases g.lexChoice (n66Occ c.cup n) with hl | hl
    · exact ⟨c, hc, hl⟩
    · obtain ⟨c', hc', hocc⟩ := g.mirror n c hc
      refine ⟨c', hc', ?_⟩
      have heq : n66Occ c'.cup n = fun s => n66Occ c.cup n (tau s) := funext fun s => propext (hocc s)
      rw [heq]
      exact hl
  let M := modelOf c' hc' (g.capCup55 n c' hc'.2.2)
  have hMn : M.n = n := rfl
  have hM : M.Holds (baseS R) := by
    refine holds_baseS (g.eager M) (g.quad M) (g.fixed M (by rw [hMn]; omega)) ?_
      (holds_card M (g.holes M (by rw [hMn]; exact hn55)))
      (holds_sb M (fun j p hp hb h1 => hlex j p hp hb h1))
    intro cl hcl
    obtain ⟨T, hT, rfl⟩ := List.mem_map.1 hcl
    obtain ⟨s, hs, hno⟩ := hR T hT n c' hc'
    refine ⟨(false, Atom.sel s), List.mem_map_of_mem hs, ?_⟩
    simp only [meaning_sel, decide_eq_false_iff_not]
    exact hno
  exact no_base_model h ⟨_, dimacsSat_of_holds M.meaning (baseS R) hM⟩

end N66R15Geo

/-- info: 'N66R15Geo.n66_bound_54_of_rows' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms N66R15Geo.n66_bound_54_of_rows

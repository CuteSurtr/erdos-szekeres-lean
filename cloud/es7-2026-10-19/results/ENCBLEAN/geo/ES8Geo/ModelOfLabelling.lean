import ES8Geo.Labelling
import ES8Geo.ModelBasic
import ES8Geo.ArcBridge

/-! # M6 assembly: the intended `EncB.Model` of a polar labelling (DESIGN.md §2.4, §3.4)

`modelOfLabelling` packs the field theorems of the M6 units (`ES8Geo.ModelBasic`: G1–G7 and the
`psiLt`/`chi`/`nest`/`noChain` fields; `ES8Geo.ArcBridge`: G8–G9 and rules A/B) into a
`EncB.Model m K t` whose orientation table is `L.chi` and whose phase order is `L.psiLt`. -/

namespace EncB.Geo
open ErdosSzekeres ErdosSzekeres.LayerLemma

/-- **M6.** The intended model of a counterexample's polar labelling: `chi a b d` iff
    `orient (P a) (P b) (P d) > 0`, and `psiLt i j` iff `ψ i < ψ j`. -/
noncomputable def modelOfLabelling {m K t : ℕ} (hm : 3 ≤ m) (heven : Even m) (hK4 : 4 ≤ K)
    (hK : K ≤ 2 * m) {T : Finset Point} {c : Point} (hgp : GeneralPosition T) (hc : c ∉ T)
    (hinv : Invariant (rotAbout c (2 * Real.pi / m)) T) (hno : ¬ HasConvexNGon K T)
    (L : PolarLabelling m t T c) : EncB.Model m K t where
  chi := L.chi
  psiLt := L.psiLt
  psiLt_irrefl := labelling_psiLt_irrefl L
  psiLt_trans := labelling_psiLt_trans L
  psiLt_total := labelling_psiLt_total L
  psiLt_zero := labelling_psiLt_zero L
  chi_rot := labelling_chi_rot hm L
  chi_cycle := labelling_chi_cycle L
  chi_swap := labelling_chi_swap hm hgp hc L
  ruleA := labelling_ruleA hm heven L
  ruleB := labelling_ruleB hm heven L
  nest := labelling_nest hm hK hgp hc hinv hno L
  noChain := labelling_noChain hm hK4 hK hgp hc hinv hno L

/-- The model's orientation table is the intended one. -/
theorem modelOfLabelling_chi {m K t : ℕ} (hm : 3 ≤ m) (heven : Even m) (hK4 : 4 ≤ K)
    (hK : K ≤ 2 * m) {T : Finset Point} {c : Point} (hgp : GeneralPosition T) (hc : c ∉ T)
    (hinv : Invariant (rotAbout c (2 * Real.pi / m)) T) (hno : ¬ HasConvexNGon K T)
    (L : PolarLabelling m t T c) :
    (modelOfLabelling hm heven hK4 hK hgp hc hinv hno L).chi = L.chi := rfl

/-- The model's phase order is the intended one. -/
theorem modelOfLabelling_psiLt {m K t : ℕ} (hm : 3 ≤ m) (heven : Even m) (hK4 : 4 ≤ K)
    (hK : K ≤ 2 * m) {T : Finset Point} {c : Point} (hgp : GeneralPosition T) (hc : c ∉ T)
    (hinv : Invariant (rotAbout c (2 * Real.pi / m)) T) (hno : ¬ HasConvexNGon K T)
    (L : PolarLabelling m t T c) :
    (modelOfLabelling hm heven hK4 hK hgp hc hinv hno L).psiLt = L.psiLt := rfl

end EncB.Geo

#print axioms EncB.Geo.modelOfLabelling
#print axioms EncB.Geo.modelOfLabelling_chi
#print axioms EncB.Geo.modelOfLabelling_psiLt

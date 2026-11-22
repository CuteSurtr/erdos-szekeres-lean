import RowGeo.Oct
import N66Geo.End
import ErdosSzekeres.ConvexCycleCuts
import ErdosSzekeres.Omission.CycleSigns

/-!
# RowGeo.Row: from a certificate to a valid row (transport, core, mirror, cycle)

* `cls3_sat`, `clsS_ok`, `certCnf_sat`: for a well-formed certificate `t`, owners of positions `0..n-1` whose
  states `σ` make every test of `t` good, the intended assignment satisfies every clause, so `certCnf t` is
  satisfiable.
* `rowValid_of_cert` (**transport**, N66 README §2.9): if `certCnf t` is unsatisfiable, `σ` (length `n`,
  distinct states) makes every test good, then no configuration of the class occupies every state of `σ`.
* `allTests_ok`, `allTests_good`: the tests of a core are good for its own states (**core** = transport by the
  identity).
* `rowValid_tau` (**mirror**, §2.8): from n66enc's `mirror_holds`.
* `rowValid_cycle` (**cycle**, §2.6): eight states whose list-order triples pass the six-order test.
-/

namespace RowGeo
open RowEnc N66Geo ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks

/-! ## Atoms of the clauses are well formed -/

def LOk (n : ℕ) (l : L3) : Prop := ∀ p a, l = .lit p a → a.Ok n

theorem lok_t (n : ℕ) : LOk n .t := fun _ _ h => by cases h
theorem lok_f (n : ℕ) : LOk n .f := fun _ _ h => by cases h

theorem lok_neg {n : ℕ} {l : L3} (h : LOk n l) : LOk n l.neg := by
  intro p a hl
  cases l with
  | t => cases hl
  | f => cases hl
  | lit q b => simp only [L3.neg, L3.lit.injEq] at hl; obtain ⟨-, rfl⟩ := hl; exact h q b rfl

theorem lok_flipIf {n : ℕ} (b : Bool) {l : L3} (h : LOk n l) : LOk n (flipIf b l) := by
  unfold flipIf; split
  · exact lok_neg h
  · exact h

theorem lok_befL {n u v : ℕ} (hu : u < n) (hv : v < n) (huv : u ≠ v) : LOk n (befL u v) := by
  intro p a h
  unfold befL at h
  split at h <;> simp only [L3.lit.injEq] at h <;> obtain ⟨-, rfl⟩ := h <;> simp only [Atom.Ok] <;> omega

theorem lok_geL {n u v : ℕ} (c : Bool) (hu : u < n) (hv : v < n) (huv : u ≠ v) (k : ℕ) : LOk n (geL c u v k) := by
  intro p a h
  unfold geL at h
  split at h
  · cases h
  · split at h
    · cases h
    · simp only [L3.lit.injEq] at h; obtain ⟨-, rfl⟩ := h
      simp only [Atom.Ok]
      refine ⟨?_, ?_, ?_, ?_⟩ <;> omega

theorem lok_oriL {n a b c : ℕ} (ha : a < n) (hb : b < n) (hc : c < n) (hab : a ≠ b) (hbc : b ≠ c) (hac : a ≠ c) :
    LOk n (oriL a b c) := by
  intro p x h
  unfold oriL at h
  simp only [L3.lit.injEq] at h
  obtain ⟨-, rfl⟩ := h
  unfold sort3
  split_ifs <;> simp only [Atom.Ok] <;> omega

theorem lok_cvxL {n a b c d : ℕ} (h1 : a < b) (h2 : b < c) (h3 : c < d) (h4 : d < n) : LOk n (cvxL a b c d) := by
  intro p x h
  unfold cvxL at h
  rw [sortAsc_four h1 h2 h3] at h
  simp only [L3.lit.injEq] at h
  obtain ⟨-, rfl⟩ := h
  exact ⟨h1, h2, h3, h4⟩

theorem lok_thresh {n : ℕ} : ∀ L ∈ threshCls n, ∀ l ∈ L, LOk n l := by
  intro L hL l hl
  unfold threshCls at hL
  obtain ⟨s, hs, hL⟩ := List.mem_flatMap.1 hL
  obtain ⟨i, j, rfl, hij, hjn⟩ := combs2_shape hs
  simp only [List.mem_flatMap, List.mem_cons, List.mem_map, List.not_mem_nil, or_false] at hL
  obtain ⟨cup, -, k, -, rfl⟩ := hL
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hl
  rcases hl with rfl | rfl
  · exact lok_neg (lok_geL cup (by omega) hjn (by omega) _)
  · exact lok_geL cup (by omega) hjn (by omega) _

theorem lok_trip {n : ℕ} : ∀ L ∈ tripCls n, ∀ l ∈ L, LOk n l := by
  intro L hL l hl
  unfold tripCls at hL
  simp only [List.mem_flatMap, List.mem_range] at hL
  obtain ⟨a, ha, b, hb, c, hc, hL⟩ := hL
  split at hL
  · simp at hL
  · rename_i hd
    have hab : a ≠ b := by tauto
    have hbc : b ≠ c := by tauto
    have hac : a ≠ c := by tauto
    unfold tripleCls at hL
    rcases List.mem_cons.1 hL with rfl | hL
    · simp only [List.mem_cons, List.not_mem_nil, or_false] at hl
      rcases hl with rfl | rfl | rfl
      · exact lok_neg (lok_befL ha hb hab)
      · exact lok_neg (lok_befL hb hc hbc)
      · exact lok_befL ha hc hac
    · simp only [List.mem_flatMap, List.mem_cons, List.mem_map, List.not_mem_nil, or_false] at hL
      obtain ⟨cup, -, k, -, rfl⟩ := hL
      simp only [List.mem_cons, List.not_mem_nil, or_false] at hl
      rcases hl with rfl | rfl | rfl | rfl | rfl
      · exact lok_neg (lok_befL ha hb hab)
      · exact lok_neg (lok_befL hb hc hbc)
      · split
        · exact lok_neg (lok_oriL ha hb hc hab hbc hac)
        · exact lok_oriL ha hb hc hab hbc hac
      · exact lok_neg (lok_geL cup ha hb hab k)
      · exact lok_geL cup hb hc hbc (k + 1)

theorem lok_packet {n q0 q1 q2 q3 : ℕ} (h0 : q0 < n) (h1 : q1 < n) (h2 : q2 < n) (h3 : q3 < n)
    (d01 : q0 ≠ q1) (d02 : q0 ≠ q2) (d03 : q0 ≠ q3) (d12 : q1 ≠ q2) (d13 : q1 ≠ q3) (d23 : q2 ≠ q3) :
    ∀ L ∈ packetCls [q0, q1, q2, q3], ∀ l ∈ L, LOk n l := by
  intro L hL l hl
  unfold packetCls at hL
  obtain ⟨bb, -, rfl⟩ := List.mem_map.1 hL
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hl
  rcases hl with rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact lok_neg (lok_befL h0 h1 d01)
  · exact lok_neg (lok_befL h1 h2 d12)
  · exact lok_neg (lok_befL h2 h3 d23)
  · exact lok_flipIf _ (lok_oriL h0 h1 h2 d01 d12 d02)
  · exact lok_flipIf _ (lok_oriL h0 h1 h3 d01 d13 d03)
  · exact lok_flipIf _ (lok_oriL h0 h2 h3 d02 d23 d03)
  · exact lok_flipIf _ (lok_oriL h1 h2 h3 d12 d23 d13)

theorem lok_quad {n : ℕ} : ∀ L ∈ quadCls n, ∀ l ∈ L, LOk n l := by
  intro L hL l hl
  unfold quadCls at hL
  obtain ⟨s, hs, hL⟩ := List.mem_flatMap.1 hL
  obtain ⟨a, b, c, d, rfl, h1, h2, h3, h4⟩ := combs4_shape hs
  simp only [List.mem_append, List.mem_flatMap] at hL
  rcases hL with ⟨ix, hix, hL⟩ | hL
  · obtain ⟨q0, q1, q2, q3, hq, hset⟩ := perm4_shape hix a b c d
    rw [hq] at hL
    have hm : ∀ x, x ∈ ({q0, q1, q2, q3} : Finset ℕ) ↔ x ∈ ({a, b, c, d} : Finset ℕ) := fun x => by rw [hset]
    have m0 := (hm q0).1 (by simp); have m1 := (hm q1).1 (by simp)
    have m2 := (hm q2).1 (by simp); have m3 := (hm q3).1 (by simp)
    have ma := (hm a).2 (by simp); have mb := (hm b).2 (by simp)
    have mc := (hm c).2 (by simp); have md := (hm d).2 (by simp)
    simp only [Finset.mem_insert, Finset.mem_singleton] at m0 m1 m2 m3 ma mb mc md
    exact lok_packet (by omega) (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)
      (by omega) (by omega) (by omega) L hL l hl
  · unfold cvxDefCls at hL
    obtain ⟨m, -, rfl⟩ := List.mem_map.1 hL
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hl
    rcases hl with rfl | rfl | rfl | rfl | rfl
    · exact lok_flipIf _ (lok_oriL (by omega) (by omega) (by omega) (by omega) (by omega) (by omega))
    · exact lok_flipIf _ (lok_oriL (by omega) (by omega) (by omega) (by omega) (by omega) (by omega))
    · exact lok_flipIf _ (lok_oriL (by omega) (by omega) (by omega) (by omega) (by omega) (by omega))
    · exact lok_flipIf _ (lok_oriL (by omega) (by omega) (by omega) (by omega) (by omega) (by omega))
    · split
      · exact lok_cvxL h1 h2 h3 h4
      · exact lok_neg (lok_cvxL h1 h2 h3 h4)

theorem lok_octClause {n : ℕ} {e : List ℕ} (hp : e.Pairwise (· < ·)) (hb : ∀ x ∈ e, x < n) :
    ∀ l ∈ octClause e, LOk n l := by
  intro l hl
  unfold octClause at hl
  obtain ⟨s, hs, rfl⟩ := List.mem_map.1 hl
  have hsub := ((mem_combs_iff 4 e s).1 hs)
  have hsp : s.Pairwise (· < ·) := hp.sublist hsub.1
  match s, hsub.2, hsp, hsub.1 with
  | [a, b, c, d], _, hsp, hsl =>
    simp at hsp
    exact lok_neg (lok_cvxL (by omega) (by omega) (by omega) (hb d (hsl.subset (by simp))))

theorem strictUp_of_pairwise : ∀ {e : List ℕ}, e.Pairwise (· < ·) → strictUp e = true
  | [], _ => rfl
  | [_], _ => rfl
  | a :: b :: rest, h => by
    simp only [strictUp, Bool.and_eq_true, decide_eq_true_eq]
    exact ⟨List.rel_of_pairwise_cons h List.mem_cons_self, strictUp_of_pairwise h.of_cons⟩

theorem octs_lists {n : ℕ} {octs : Option (List (List ℕ))} (h : octsOk n octs = true) :
    ∀ e ∈ (match octs with | some es => es | none => combs 8 (List.range n)), octOk n e = true := by
  cases octs with
  | none =>
    intro e he
    rw [mem_combs_range] at he
    obtain ⟨hp, hb, hl⟩ := he
    simp only [octOk, Bool.and_eq_true, beq_iff_eq, List.all_eq_true, decide_eq_true_eq]
    exact ⟨⟨hl, strictUp_of_pairwise hp⟩, hb⟩
  | some es =>
    simp only [octsOk, List.all_eq_true] at h
    exact h

theorem octCls_eq (n : ℕ) (octs : Option (List (List ℕ))) :
    octCls n octs = (match octs with | some es => es | none => combs 8 (List.range n)).map octClause := by
  cases octs <;> rfl

/-! ## The whole clause list -/

section
variable {M : Model} {n : ℕ} {o : ℕ → ℕ}

theorem cls3_sat (ho : Owners M n o) (σ : ℕ → Fin 70) (hσ : ∀ i, i < n → idxOf M.cup (o i) = (σ i).val)
    {tests : List Test} {octs : Option (List (List ℕ))} (htok : ∀ x ∈ tests, testOk n x = true)
    (hoct : octsOk n octs = true) (hgood : ∀ x ∈ tests, Good σ x) :
    ∀ L ∈ cls3 n tests octs, ∃ l ∈ L, l.eval (meaning M o) = true := by
  intro L hL
  unfold cls3 at hL
  simp only [List.mem_append] at hL
  rcases hL with (((hL | hL) | hL) | hL) | hL
  · exact sat_thresh ho L hL
  · exact sat_trip ho L hL
  · exact sat_quad ho L hL
  · rw [octCls_eq] at hL
    obtain ⟨e, he, rfl⟩ := List.mem_map.1 hL
    exact sat_oct ho (octs_lists hoct e he)
  · obtain ⟨x, hx, rfl⟩ := List.mem_map.1 hL
    exact sat_test ho σ hσ (htok x hx) (hgood x hx)

theorem cls3_ok {tests : List Test} {octs : Option (List (List ℕ))} (htok : ∀ x ∈ tests, testOk n x = true)
    (hoct : octsOk n octs = true) : ∀ L ∈ cls3 n tests octs, ∀ l ∈ L, LOk n l := by
  intro L hL
  unfold cls3 at hL
  simp only [List.mem_append] at hL
  rcases hL with (((hL | hL) | hL) | hL) | hL
  · exact lok_thresh L hL
  · exact lok_trip L hL
  · exact lok_quad L hL
  · rw [octCls_eq] at hL
    obtain ⟨e, he, rfl⟩ := List.mem_map.1 hL
    have h := octs_lists hoct e he
    simp only [octOk, Bool.and_eq_true, beq_iff_eq, List.all_eq_true, decide_eq_true_eq] at h
    exact lok_octClause (strictUp_pairwise h.1.2) h.2
  · obtain ⟨x, hx, rfl⟩ := List.mem_map.1 hL
    have h := htok x hx
    intro l hl
    cases x with
    | E u v =>
      simp only [testOk, Bool.and_eq_true, decide_eq_true_eq, bne_iff_ne, ne_eq] at h
      simp only [testCl, List.mem_cons, List.not_mem_nil, or_false] at hl
      subst hl; exact lok_neg (lok_befL h.1.1 h.1.2 h.2)
    | D u v a b =>
      simp only [testOk, Bool.and_eq_true, decide_eq_true_eq, bne_iff_ne, ne_eq] at h
      obtain ⟨⟨hu, hv⟩, huv⟩ := h
      have hmn : min u v < n := by omega
      have hmx : max u v < n := by omega
      have hne : min u v ≠ max u v := by omega
      simp only [testCl, List.mem_cons, List.not_mem_nil, or_false] at hl
      rcases hl with rfl | rfl | rfl | rfl | rfl
      · exact lok_neg (lok_befL hu hv huv)
      · exact lok_neg (lok_geL false hmn hmx hne _)
      · exact lok_geL false hmn hmx hne _
      · exact lok_neg (lok_geL true hmn hmx hne _)
      · exact lok_geL true hmn hmx hne _
    | P p q r =>
      simp only [testOk, Bool.and_eq_true, decide_eq_true_eq, bne_iff_ne, ne_eq] at h
      obtain ⟨⟨⟨⟨⟨hp, hq⟩, hr⟩, hpq⟩, hqr⟩, hpr⟩ := h
      simp only [testCl, List.mem_cons, List.not_mem_nil, or_false] at hl
      subst hl; exact lok_oriL hp hq hr hpq hqr hpr

end

/-! ## Certificates -/

/-- The tests of a well-formed certificate are well formed (generated tests of a core: `allTests_ok`). -/
def TestsOk (t : Cert) : Prop := ∀ x ∈ t.tests, testOk t.n x = true

theorem certCnf_sat {t : Cert} (hn : t.n ≤ 32) (htok : TestsOk t) (hoct : octsOk t.n t.octs = true)
    {M : Model} {o : ℕ → ℕ} (ho : Owners M t.n o)
    (σ : ℕ → Fin 70) (hσ : ∀ i, i < t.n → idxOf M.cup (o i) = (σ i).val)
    (hgood : ∀ x ∈ t.tests, Good σ x) : EncB.DimacsSatisfiable (certCnf t) := by
  apply dimacsSat_of_meaning hn (meaning M o)
  · intro cl hcl x hx
    unfold clsS at hcl
    obtain ⟨L, hL, hfin⟩ := List.mem_filterMap.1 hcl
    exact cls3_ok htok hoct L hL _ (finClause_mem hfin x hx) x.1 x.2 rfl
  · intro cl hcl
    unfold clsS at hcl
    obtain ⟨L, hL, hfin⟩ := List.mem_filterMap.1 hcl
    exact finClause_sat _ hfin (cls3_sat ho σ hσ htok hoct hgood L hL)

/-- Owners of the states of a list, in a configuration of the class that occupies all of them. -/
theorem owners_of_occ {N : ℕ} (c : Configuration N) (hc : InClass c) (σ : List (Fin 70)) (hnd : σ.Nodup)
    (hocc : ∀ s ∈ σ, n66Occ c.cup N s) :
    ∃ o : ℕ → ℕ, Owners (modelOf c hc (capCup55_holds N c hc.2.2)) σ.length o ∧
      ∀ i, i < σ.length → idxOf c.cup (o i) = (σ.getD i 0).val := by
  classical
  have hex : ∀ i, i < σ.length → ∃ v < N, idxOf c.cup v = (σ.getD i 0).val := fun i hi => by
    have : σ.getD i 0 ∈ σ := by
      rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi, Option.getD_some]; exact List.getElem_mem hi
    exact hocc _ this
  let o : ℕ → ℕ := fun i => if h : i < σ.length then Classical.choose (hex i h) else 0
  have hoi : ∀ i (h : i < σ.length), o i = Classical.choose (hex i h) := fun i h => by simp [o, h]
  refine ⟨o, ⟨fun i hi => ?_, fun i j hi hj hij => ?_⟩, fun i hi => ?_⟩
  · rw [hoi i hi]; exact (Classical.choose_spec (hex i hi)).1
  · have e1 := (Classical.choose_spec (hex i hi)).2
    have e2 := (Classical.choose_spec (hex j hj)).2
    rw [← hoi i hi] at e1; rw [← hoi j hj] at e2
    rw [hij] at e1
    have : σ.getD i 0 = σ.getD j 0 := Fin.ext (e1.symm.trans e2)
    rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi, Option.getD_some,
      List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hj, Option.getD_some] at this
    exact (List.Nodup.getElem_inj_iff hnd).1 this
  · rw [hoi i hi]; exact (Classical.choose_spec (hex i hi)).2

/-- **Transport** (a template certificate refutes every σ that passes its tests). -/
theorem rowValid_of_cert {t : Cert} (hn : t.n ≤ 32) (htok : TestsOk t) (hoct : octsOk t.n t.octs = true)
    (σ : List (Fin 70)) (hlen : σ.length = t.n) (hnd : σ.Nodup)
    (hgood : ∀ x ∈ t.tests, Good (fun i => σ.getD i 0) x)
    (hunsat : ¬ EncB.DimacsSatisfiable (certCnf t)) : RowValid σ := by
  intro N c hc
  by_contra hno
  push_neg at hno
  obtain ⟨o, ho, hσ⟩ := owners_of_occ c hc σ hnd hno
  rw [hlen] at ho hσ
  exact hunsat (certCnf_sat hn htok hoct ho (fun i => σ.getD i 0) hσ hgood)

end RowGeo

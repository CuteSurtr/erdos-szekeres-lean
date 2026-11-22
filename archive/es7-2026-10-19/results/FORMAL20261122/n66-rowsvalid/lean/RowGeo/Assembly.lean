import RowGeo.Kinds
import RowChk.RowsAll
import RowChk.TabPs
import RowChk.TabTt
import RowChk.TabDr
import RowChk.TabCan
import RowChk.CertsOk
import RowChk.IsCore

/-!
# RowGeo.Assembly: `RowsValid R1` modulo the 629 row-certificate verdicts

* Table soundness (`ttB_sound`, `drB_sound`, `canB_sound`) from the kernel checks `RowChk.Tab*` and n66enc's
  `tt_eq`, `can_eq`; `ttQ_eq : ttQ = ttF` from the plain-domain statistics table.
* `chkRow_sound`: a row whose certificate passes `chkRow` is valid, given `RowCertsUnsat` (transport
  `rowValid_of_cert`, cores `allTests_good`, mirror `rowValid_tau`, cycles `rowValid_cycle`).
* **`rowsValid_R1 : RowCertsUnsat → RowsValid R1`**, where `R1` is the list of the 11,884 rows of `N66Enc.R0`
  (same order) and every row's check is evaluated by the kernel (`RowChk.chkAll`).
-/

namespace RowGeo
open RowEnc RowChk N66Geo

def toFin70 (x : ℕ) : Fin 70 := ⟨x % 70, Nat.mod_lt _ (by decide)⟩

theorem toFin70_val {x : ℕ} (h : x < 70) : (toFin70 x).val = x := Nat.mod_eq_of_lt h

/-! ## Tables -/

theorem psChk_all (u : Fin 70) : psChk u = true := by
  have h := List.all_eq_true.1 ps_all u.val (List.mem_range.2 u.isLt)
  simpa [psChkN, u.isLt] using h

theorem ps_facts (u v : Fin 70) :
    neQ u v = N66Enc.nePlain u v ∧ mnQ false u v = N66Enc.mnPlain false u v ∧
      mxQ false u v = N66Enc.mxPlain false u v ∧ mnQ true u v = N66Enc.mnPlain true u v ∧
      mxQ true u v = N66Enc.mxPlain true u v := by
  have h := List.all_eq_true.1 (psChk_all u) v (List.mem_finRange v)
  simp only [Bool.and_eq_true, beq_iff_eq] at h
  exact ⟨h.1.1.1.1, h.1.1.1.2, h.1.1.2, h.1.2, h.2⟩

theorem neQ_eq (u v : Fin 70) : neQ u v = N66Enc.nePlain u v := (ps_facts u v).1

theorem mnQ_eq (coord : Bool) (u v : Fin 70) : mnQ coord u v = N66Enc.mnPlain coord u v := by
  cases coord
  · exact (ps_facts u v).2.1
  · exact (ps_facts u v).2.2.2.1

theorem mxQ_eq (coord : Bool) (u v : Fin 70) : mxQ coord u v = N66Enc.mxPlain coord u v := by
  cases coord
  · exact (ps_facts u v).2.2.1
  · exact (ps_facts u v).2.2.2.2

theorem ttQ_eq (a b c : Fin 70) : ttQ a b c = N66Enc.ttF a b c := by
  unfold ttQ N66Enc.ttF
  simp only [neQ_eq, mnQ_eq, mxQ_eq]

theorem ttB_sound {a b c : ℕ} (ha : a < 70) (hb : b < 70) (hc : c < 70) (h : ttB a b c = true) :
    N66Enc.tt (toFin70 a) (toFin70 b) (toFin70 c) = true := by
  have hrow := List.all_eq_true.1 tt_all a (List.mem_range.2 ha)
  unfold ttChk at hrow
  have hi := List.all_eq_true.1 hrow (b * 70 + c) (List.mem_range.2 (by omega))
  unfold ttB at h
  rw [h] at hi
  have e1 : (b * 70 + c) / 70 = b := by omega
  have e2 : (b * 70 + c) % 70 = c := by omega
  simp only [Bool.not_true, Bool.false_or, e1, e2] at hi
  unfold ttQN at hi
  rw [dif_pos ⟨ha, hb, hc⟩, ttQ_eq] at hi
  rw [tt_eq]
  have ea : toFin70 a = ⟨a, ha⟩ := Fin.ext (toFin70_val ha)
  have eb : toFin70 b = ⟨b, hb⟩ := Fin.ext (toFin70_val hb)
  have ec : toFin70 c = ⟨c, hc⟩ := Fin.ext (toFin70_val hc)
  rw [ea, eb, ec]; exact hi

theorem drB_sound {u v a b : ℕ} (hu : u < 70) (hv : v < 70) (hr : 1 ≤ a ∧ a ≤ 4 ∧ 1 ≤ b ∧ b ≤ 4)
    (h : drB u v a b = false) :
    N66Enc.domRef (N66Enc.prof (toFin70 u)) (N66Enc.prof (toFin70 v)) (a, b) = false := by
  have hrow := List.all_eq_true.1 dr_all u (List.mem_range.2 hu)
  simp only [drChkN, dif_pos hu] at hrow
  have hv' := List.all_eq_true.1 hrow ⟨v, hv⟩ (List.mem_finRange _)
  have hz := List.all_eq_true.1 hv' (a, b) (mem_grid' hr.1 hr.2.1 hr.2.2.1 hr.2.2.2)
  simp only [beq_iff_eq] at hz
  have ea : toFin70 u = ⟨u, hu⟩ := Fin.ext (toFin70_val hu)
  have eb : toFin70 v = ⟨v, hv⟩ := Fin.ext (toFin70_val hv)
  rw [ea, eb, ← hz]; exact h

theorem canB_sound {u v : ℕ} (hu : u < 70) (hv : v < 70) (h : canB u v = false) :
    N66Enc.can (toFin70 u) (toFin70 v) = false := by
  have hrow := List.all_eq_true.1 can_all u (List.mem_range.2 hu)
  simp only [canChkN, dif_pos hu] at hrow
  have hv' := List.all_eq_true.1 hrow ⟨v, hv⟩ (List.mem_finRange _)
  simp only [beq_iff_eq] at hv'
  have ea : toFin70 u = ⟨u, hu⟩ := Fin.ext (toFin70_val hu)
  have eb : toFin70 v = ⟨v, hv⟩ := Fin.ext (toFin70_val hv)
  rw [can_eq, ea, eb, ← hv']; exact h

/-! ## Lists -/

theorem nodupB_sound : ∀ {l : List ℕ}, nodupB l = true → l.Nodup
  | [], _ => List.nodup_nil
  | x :: xs, h => by
    simp only [nodupB, Bool.and_eq_true, Bool.not_eq_true'] at h
    refine List.nodup_cons.2 ⟨fun hm => ?_, nodupB_sound h.2⟩
    have := List.contains_iff_mem.2 hm
    rw [h.1] at this; exact Bool.false_ne_true this

theorem map_toFin70_nodup {l : List ℕ} (h : l.Nodup) (hb : ∀ x ∈ l, x < 70) : (l.map toFin70).Nodup :=
  List.Nodup.map_on (fun x hx y hy e => by
    have := congrArg Fin.val e; rwa [toFin70_val (hb x hx), toFin70_val (hb y hy)] at this) h

theorem getD_map_toFin70 (σ : List ℕ) (i : ℕ) : (σ.map toFin70).getD i 0 = toFin70 (σ.getD i 0) := by
  rw [List.getD_eq_getElem?_getD, List.getD_eq_getElem?_getD, List.getElem?_map]
  cases σ[i]? <;> rfl

theorem getD_lt {σ : List ℕ} (hb : ∀ x ∈ σ, x < 70) (i : ℕ) : σ.getD i 0 < 70 := by
  rw [List.getD_eq_getElem?_getD]
  cases hσ : σ[i]? with
  | none => decide
  | some x => exact hb x (List.mem_of_getElem? hσ)

theorem goodN_sound {σ : List ℕ} (hb : ∀ x ∈ σ, x < 70) {x : Test} (h : goodN σ x = true) :
    Good (fun i => (σ.map toFin70).getD i 0) x := by
  cases x with
  | E u v =>
    simp only [goodN, Bool.not_eq_true'] at h
    simp only [Good, getD_map_toFin70]
    exact canB_sound (getD_lt hb u) (getD_lt hb v) h
  | D u v a b =>
    simp only [goodN, Bool.and_eq_true, decide_eq_true_eq, Bool.not_eq_true'] at h
    simp only [Good, getD_map_toFin70]
    exact drB_sound (getD_lt hb u) (getD_lt hb v) h.1 h.2
  | P p q r =>
    simp only [goodN] at h
    simp only [Good, getD_map_toFin70]
    exact ttB_sound (getD_lt hb p) (getD_lt hb q) (getD_lt hb r) h

/-! ## Certificates -/

/-- **The 629 verdicts** (421 template CNFs, 208 core CNFs), as one proposition. Discharged outside the kernel:
printed text = VB's certified CNF (M9) and VB's cake_lpr verdict, under E1-E6 (`certUnsat_of_text`). -/
def RowCertsUnsat : Prop :=
  (∀ t ∈ templates, ¬ EncB.DimacsSatisfiable (certCnf t)) ∧ (∀ k ∈ cores, ¬ EncB.DimacsSatisfiable (certCnf k))

theorem certOk_parts {c : Cert} (h : certOk c = true) :
    c.n ≤ 32 ∧ TestsOk c ∧ octsOk c.n c.octs = true := by
  cases c with
  | tmpl n ts o =>
    simp only [certOk, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true] at h
    exact ⟨h.1.1, h.1.2, h.2⟩
  | core S o =>
    simp only [certOk, Bool.and_eq_true, decide_eq_true_eq] at h
    exact ⟨h.1, allTests_ok S, h.2⟩

theorem tau_toFin70 {x : ℕ} (hx : x < 70) : tau (toFin70 x) = toFin70 (tauN x) := by
  apply Fin.ext
  simp only [tau, toFin70, tauN, Nat.mod_eq_of_lt hx]

theorem rowValid_sig {c : Cert} (hU : ¬ EncB.DimacsSatisfiable (certCnf c)) (hc : certOk c = true)
    {σ : List ℕ} (h : sigOk c σ = true) : RowValid (σ.map toFin70) := by
  simp only [sigOk, Bool.and_eq_true, beq_iff_eq, List.all_eq_true, decide_eq_true_eq] at h
  obtain ⟨⟨⟨hlen, hb⟩, hnd⟩, hg⟩ := h
  obtain ⟨hn, htok, hoct⟩ := certOk_parts hc
  exact rowValid_of_cert hn htok hoct (σ.map toFin70) (by rw [List.length_map, hlen])
    (map_toFin70_nodup (nodupB_sound hnd) hb) (fun x hx => goodN_sound hb (hg x hx)) hU

theorem rowValid_core {k : Cert} (hU : ¬ EncB.DimacsSatisfiable (certCnf k)) (hk : coreOk k = true)
    {T : List ℕ} (hT : ∀ x ∈ T, x < 70) (hsub : (coreStates k).all (fun x => T.contains x) = true) :
    ∃ S : List (Fin 70), RowValid S ∧ ∀ s ∈ S, s.val ∈ T := by
  simp only [coreOk, Bool.and_eq_true] at hk
  cases k with
  | tmpl n ts o =>
    simp only [coreStates, List.all_cons, List.all_nil, Bool.and_true, List.contains_iff_mem] at hsub
    exact absurd (hT 70 hsub) (by decide)
  | core S o =>
    obtain ⟨hn, htok, hoct⟩ := certOk_parts hk.1
    have hnd : S.Nodup := by
      have := (strictUp_pairwise hk.2).imp (fun h => Nat.ne_of_lt h)
      exact List.Nodup.of_map Fin.val this
    refine ⟨S, rowValid_of_cert hn htok hoct S rfl hnd (fun x hx => allTests_good S x hx) hU, fun s hs => ?_⟩
    simp only [coreStates, List.all_map, List.all_eq_true, Function.comp, List.contains_iff_mem] at hsub
    exact hsub s hs

theorem mem_tri8 {i j k : ℕ} (h1 : i < j) (h2 : j < k) (h3 : k < 8) : (i, j, k) ∈ tri8 := by
  unfold tri8
  simp only [List.mem_flatMap, List.mem_filterMap, List.mem_range, Option.ite_none_right_eq_some,
    Option.some.injEq]
  exact ⟨i, by omega, j, by omega, k, h3, ⟨h1, h2⟩, rfl⟩

/-- **One row.** -/
theorem chkRow_sound (hU : RowCertsUnsat) {T : List ℕ} (hT : ∀ x ∈ T, x < 70) {rc : RC}
    (h : chkRow T rc = true) : RowValid (T.map toFin70) := by
  have memT : ∀ x, T.contains x = true → toFin70 x ∈ T.map toFin70 := fun x hx =>
    List.mem_map_of_mem (List.contains_iff_mem.1 hx)
  cases rc with
  | tr t σ =>
    simp only [chkRow] at h
    split at h
    · rename_i c hc
      simp only [Bool.and_eq_true, List.all_eq_true] at h
      have hmem := List.mem_of_getElem? hc
      have hok := List.all_eq_true.1 certsOkT c hmem
      refine rowValid_mono (rowValid_sig (hU.1 c hmem) hok h.1) ?_
      intro s hs
      obtain ⟨x, hx, rfl⟩ := List.mem_map.1 hs
      exact memT x (h.2 x hx)
    · cases h
  | mt t σ =>
    simp only [chkRow] at h
    split at h
    · rename_i c hc
      simp only [Bool.and_eq_true, List.all_eq_true] at h
      have hmem := List.mem_of_getElem? hc
      have hok := List.all_eq_true.1 certsOkT c hmem
      have hσ : ∀ x ∈ σ, x < 70 := by
        have := h.1; simp only [sigOk, Bool.and_eq_true, List.all_eq_true, decide_eq_true_eq] at this
        exact this.1.1.2
      refine rowValid_mono (rowValid_tau (rowValid_sig (hU.1 c hmem) hok h.1)) ?_
      intro s hs
      obtain ⟨y, hy, rfl⟩ := List.mem_map.1 hs
      obtain ⟨x, hx, rfl⟩ := List.mem_map.1 hy
      rw [tau_toFin70 (hσ x hx)]
      exact memT _ (h.2 x hx)
    · cases h
  | co c =>
    simp only [chkRow] at h
    split at h
    · rename_i k hk
      have hmem := List.mem_of_getElem? hk
      obtain ⟨S, hS, hST⟩ := rowValid_core (hU.2 k hmem) (List.all_eq_true.1 certsOkC k hmem) hT h
      refine rowValid_mono hS fun s hs => ?_
      have : toFin70 s.val = s := Fin.ext (toFin70_val s.isLt)
      rw [← this]; exact List.mem_map_of_mem (hST s hs)
    · cases h
  | mc c =>
    simp only [chkRow] at h
    split at h
    · rename_i k hk
      have hmem := List.mem_of_getElem? hk
      have hok := List.all_eq_true.1 certsOkC k hmem
      -- the mirror images of the core's states lie in T
      have hcore := List.all_eq_true.1 cores_isCore k hmem
      cases k with
      | tmpl n ts o => simp [isCore] at hcore
      | core S o =>
        have hsubS : (coreStates (.core S o)).all (fun x => (S.map Fin.val).contains x) = true := by
          simp only [coreStates, List.all_eq_true, List.contains_iff_mem]; exact fun x hx => hx
        obtain ⟨S', hS', hS'S⟩ := rowValid_core (hU.2 _ hmem) hok
          (fun x hx => by obtain ⟨s, -, rfl⟩ := List.mem_map.1 hx; exact s.isLt) hsubS
        refine rowValid_mono (rowValid_tau hS') fun s hs => ?_
        obtain ⟨y, hy, rfl⟩ := List.mem_map.1 hs
        have hyS := hS'S y hy
        obtain ⟨z, hz, hzy⟩ := List.mem_map.1 hyS
        simp only [coreStates, List.all_map, List.all_eq_true, Function.comp, List.contains_iff_mem] at h
        have h1 := h z hz
        rw [hzy] at h1
        have : tau y = toFin70 (tauN y.val) := by
          rw [← tau_toFin70 y.isLt]; congr 1; exact (Fin.ext (toFin70_val y.isLt)).symm
        rw [this]; exact List.mem_map_of_mem h1
    · cases h
  | cy L =>
    simp only [chkRow, cycOk, Bool.and_eq_true, beq_iff_eq, List.all_eq_true, decide_eq_true_eq] at h
    obtain ⟨⟨⟨⟨hlen, hb⟩, hnd⟩, htri⟩, hsub⟩ := h
    have hcyc := rowValid_cycle (L.map toFin70) (by rw [List.length_map, hlen])
      (map_toFin70_nodup (nodupB_sound hnd) hb) (fun i j k h1 h2 h3 => by
        rw [getD_map_toFin70, getD_map_toFin70, getD_map_toFin70]
        exact ttB_sound (getD_lt hb i) (getD_lt hb j) (getD_lt hb k) (htri (i, j, k) (mem_tri8 h1 h2 h3)))
    refine rowValid_mono hcyc fun s hs => ?_
    obtain ⟨x, hx, rfl⟩ := List.mem_map.1 hs
    exact memT x (hsub x hx)

theorem chkRows_mem : ∀ {Ts : List (List ℕ)} {rs : List RC}, chkRows Ts rs = true → ∀ T ∈ Ts,
    (∀ x ∈ T, x < 70) ∧ ∃ rc, chkRow T rc = true
  | [], [], _, T, hT => absurd hT List.not_mem_nil
  | T0 :: Ts, r :: rs, h, T, hT => by
    simp only [chkRows, Bool.and_eq_true, List.all_eq_true, decide_eq_true_eq] at h
    rcases List.mem_cons.1 hT with rfl | hT
    · exact ⟨h.1.1, r, h.1.2⟩
    · exact chkRows_mem h.2 T hT
  | [], _ :: _, h, _, _ => by simp [chkRows] at h
  | _ :: _, [], h, _, _ => by simp [chkRows] at h

/-- The 11,884 rows of `N66Enc.R0`, in its order, as kernel-friendly data. -/
def R1 : List (List (Fin 70)) := R1nat.map (·.map toFin70)

/-- **`RowsValid R1`, Lean-checked modulo the 629 row-certificate verdicts.** -/
theorem rowsValid_R1 (hU : RowCertsUnsat) : RowsValid R1 := by
  intro T hT
  obtain ⟨Tn, hTn, rfl⟩ := List.mem_map.1 hT
  unfold R1nat at hTn
  obtain ⟨p, hp, hTp⟩ := List.mem_flatMap.1 hTn
  obtain ⟨hb, rc, hrc⟩ := chkRows_mem (chkAll p hp) Tn hTp
  exact chkRow_sound hU hb hrc

end RowGeo

import ETVEncoding.Dimacs

/-!
# A small verified LRAT (RUP-only) checker that the kernel can run

Lean's own LRAT checker (`Std.Tactic.BVDecide.LRAT.check`) is verified but does not reduce
in the kernel (it gets stuck), so without `native_decide` it cannot discharge even tiny
instances. This file gives a deliberately simple checker over lists, by structural
recursion, with a soundness proof: `checkUnsat cnf proof = true → ¬DimacsSatisfiable cnf`.
It handles RUP additions with hints (the steps CaDiCaL writes with `--lrat`) and ignores
deletions, which is sound. It is quadratic and only meant for small instances.
-/

namespace ETV.Rup

/-- One LRAT step: add clause `c` with id `id` justified by unit propagation on the hint
clauses in order, or delete clauses (ignored by the checker). -/
inductive Step where
  | add (id : ℕ) (c : List ℤ) (hints : List ℕ)
  | del (ids : List ℕ)

/-- Unit propagation along the hints, from the literals `A` assumed true. Succeeds when a
hint clause becomes falsified. -/
def propagate (getC : ℕ → Option (List ℤ)) : List ℤ → List ℕ → Bool
  | _, [] => false
  | A, h :: hs =>
    match getC h with
    | none => false
    | some c =>
      match c.filter (fun l => !A.contains (-l)) with
      | [] => true
      | [l] => propagate getC (l :: A) hs
      | _ :: _ :: _ => false

def lookup (F : List (ℕ × List ℤ)) (h : ℕ) : Option (List ℤ) :=
  (F.find? (fun p => p.1 == h)).map (·.2)

/-- Run the proof; `true` once the empty clause has been derived. -/
def run : List (ℕ × List ℤ) → List Step → Bool
  | _, [] => false
  | F, .add id c hints :: rest =>
    if c.all (· != 0) && propagate (lookup F) (c.map (- ·)) hints then
      if c.isEmpty then true else run ((id, c) :: F) rest
    else false
  | F, .del _ :: rest => run F rest

/-- Original clauses get the ids `1, 2, …` in file order. -/
def checkUnsat (cnf : List (List ℤ)) (proof : List Step) : Bool :=
  run ((List.range cnf.length).map (· + 1) |>.zip cnf) proof

/-! ### Soundness -/

/-- The DIMACS meaning of a literal. -/
def LitSat (ν : ℕ → Bool) (l : ℤ) : Prop := (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)

def ClauseSat (ν : ℕ → Bool) (c : List ℤ) : Prop := ∃ l ∈ c, LitSat ν l

theorem litSat_neg {ν : ℕ → Bool} {l : ℤ} (hl : l ≠ 0) : LitSat ν (-l) ↔ ¬LitSat ν l := by
  unfold LitSat
  rw [Int.natAbs_neg]
  rcases lt_trichotomy l 0 with h | h | h
  · cases hv : ν l.natAbs <;> simp [h, not_lt.2 h.le]
  · exact absurd h hl
  · cases hv : ν l.natAbs <;> simp [h, not_lt.2 h.le]

theorem not_litSat_zero {ν : ℕ → Bool} : ¬LitSat ν 0 := by
  simp [LitSat]

theorem not_litSat_of_neg_mem {ν : ℕ → Bool} {A : List ℤ} (hA : ∀ a ∈ A, LitSat ν a)
    {l : ℤ} (h : A.contains (-l) = true) : ¬LitSat ν l := by
  have hm : -l ∈ A := by simpa using h
  by_cases hl : l = 0
  · subst hl
    exact not_litSat_zero
  · exact (litSat_neg hl).1 (hA _ hm)

theorem propagate_sound {ν : ℕ → Bool} {getC : ℕ → Option (List ℤ)}
    (hF : ∀ h c, getC h = some c → ClauseSat ν c) :
    ∀ (A : List ℤ) (hs : List ℕ), propagate getC A hs = true → (∀ a ∈ A, LitSat ν a) → False
  | _, [], h, _ => by simp [propagate] at h
  | A, h :: hs, hp, hA => by
    unfold propagate at hp
    cases hc : getC h with
    | none => simp [hc] at hp
    | some c =>
      simp only [hc] at hp
      obtain ⟨l, hlc, hlsat⟩ := hF h c hc
      have hl : l ∈ c.filter (fun l => !A.contains (-l)) := by
        rw [List.mem_filter]
        refine ⟨hlc, ?_⟩
        cases hcon : A.contains (-l)
        · rfl
        · exact absurd hlsat (not_litSat_of_neg_mem hA hcon)
      split at hp
      · rename_i heq
        rw [heq] at hl
        simp at hl
      · rename_i l' heq
        rw [heq, List.mem_singleton] at hl
        subst hl
        exact propagate_sound hF (l :: A) hs hp (by
          intro a ha
          rcases List.mem_cons.1 ha with rfl | ha
          · exact hlsat
          · exact hA a ha)
      · simp at hp

theorem lookup_sat {ν : ℕ → Bool} {F : List (ℕ × List ℤ)} (hF : ∀ p ∈ F, ClauseSat ν p.2) :
    ∀ h c, lookup F h = some c → ClauseSat ν c := by
  intro h c hc
  simp only [lookup, Option.map_eq_some_iff] at hc
  obtain ⟨p, hp, rfl⟩ := hc
  exact hF p (List.mem_of_find?_eq_some hp)

theorem run_sound {ν : ℕ → Bool} :
    ∀ (F : List (ℕ × List ℤ)) (proof : List Step), (∀ p ∈ F, ClauseSat ν p.2) →
      run F proof = true → False
  | _, [], _, h => by simp [run] at h
  | F, .del _ :: rest, hF, h => run_sound (ν := ν) F rest hF (by simpa [run] using h)
  | F, .add id c hints :: rest, hF, h => by
    unfold run at h
    split_ifs at h with hchk hemp
    · simp only [Bool.and_eq_true, List.all_eq_true, bne_iff_ne, ne_eq] at hchk
      obtain ⟨hnz, hprop⟩ := hchk
      have hsat : ClauseSat ν c := by
        by_contra hns
        apply propagate_sound (lookup_sat hF) _ _ hprop
        intro a ha
        obtain ⟨l, hl, rfl⟩ := List.mem_map.1 ha
        rw [litSat_neg (hnz l hl)]
        exact fun hls => hns ⟨l, hl, hls⟩
      obtain ⟨l, hl, -⟩ := hsat
      simp only [List.isEmpty_iff] at hemp
      subst hemp
      simp at hl
    · simp only [Bool.and_eq_true, List.all_eq_true, bne_iff_ne, ne_eq] at hchk
      obtain ⟨hnz, hprop⟩ := hchk
      have hsat : ClauseSat ν c := by
        by_contra hns
        apply propagate_sound (lookup_sat hF) _ _ hprop
        intro a ha
        obtain ⟨l, hl, rfl⟩ := List.mem_map.1 ha
        rw [litSat_neg (hnz l hl)]
        exact fun hls => hns ⟨l, hl, hls⟩
      refine run_sound (ν := ν) ((id, c) :: F) rest ?_ h
      intro p hp
      rcases List.mem_cons.1 hp with rfl | hp
      · exact hsat
      · exact hF p hp

/-- **Soundness of the checker.** -/
theorem not_dimacsSatisfiable_of_checkUnsat {cnf : List (List ℤ)} {proof : List Step}
    (h : checkUnsat cnf proof = true) : ¬DimacsSatisfiable cnf := by
  rintro ⟨ν, hν⟩
  refine run_sound (ν := ν) _ proof ?_ h
  intro p hp
  have := List.of_mem_zip hp
  obtain ⟨l, hl, hsat⟩ := hν p.2 this.2
  exact ⟨l, hl, hsat⟩

/-- Soundness with an explicit starting formula: any clauses of `cnf`, with any ids (typically
only the original clauses that the proof uses). -/
theorem not_dimacsSatisfiable_of_run {cnf : List (List ℤ)} {F : List (ℕ × List ℤ)}
    {proof : List Step} (hF : ∀ p ∈ F, p.2 ∈ cnf) (h : run F proof = true) :
    ¬DimacsSatisfiable cnf := by
  rintro ⟨ν, hν⟩
  refine run_sound (ν := ν) F proof ?_ h
  intro p hp
  obtain ⟨l, hl, hsat⟩ := hν p.2 (hF p hp)
  exact ⟨l, hl, hsat⟩

end ETV.Rup

import MirrorEncoding.Sound
import MirrorEncoding.CoverCore

/-!
# Cube covers and the composition of per-cube UNSAT results

A cube-and-conquer run (march_cu, or the adaptive splitter `results/C/scripts/cnc2.py`)
refutes `F ∧ cube` for every cube of a list. Together these prove `F` unsatisfiable exactly
when the cubes cover every assignment. This file gives

* `coverCheck cubes`, a decision-tree check that every Boolean assignment satisfies some
  cube, with soundness theorem `covers_of_coverCheck`. It is linear-ish on tree-shaped
  cube sets (each split on the first literal of the first cube), and it rejects the literal
  `0`;
* `cubeCnf F cube = F ++ (cube as unit clauses)`, the file given to the solver and to the
  proof checker for one cube;
* `not_dimacsSatisfiable_of_cover`: if the cubes cover and every `cubeCnf F cube` is UNSAT,
  then `F` is UNSAT.

`lake exe cover_check` runs `coverCheck` on a cube file (compiled code; see
`CoverMain.lean`).
-/

namespace Mir

open ETV

/-- A cube (a conjunction of DIMACS literals) holds under `ν`. -/
def CubeSat (ν : ℕ → Bool) (cube : List ℤ) : Prop := ∀ z ∈ cube, LitSat ν z

/-- The cubes cover the whole space. -/
def Covers (cubes : List (List ℤ)) : Prop := ∀ ν : ℕ → Bool, ∃ c ∈ cubes, CubeSat ν c

theorem litSat_neg {ν : ℕ → Bool} {z : ℤ} (hz : z ≠ 0) (h : ¬LitSat ν z) : LitSat ν (-z) := by
  unfold LitSat at h ⊢
  rw [Int.natAbs_neg]
  rcases lt_trichotomy z 0 with hlt | heq | hgt
  · left
    refine ⟨by omega, ?_⟩
    cases e : ν z.natAbs
    · exact absurd (Or.inr ⟨hlt, e⟩) h
    · rfl
  · exact absurd heq hz
  · right
    refine ⟨by omega, ?_⟩
    cases e : ν z.natAbs
    · rfl
    · exact absurd (Or.inl ⟨hgt, e⟩) h

theorem cubeSat_of_restrict {ν : ℕ → Bool} {z : ℤ} {cubes : List (List ℤ)} (hz : LitSat ν z)
    {c' : List ℤ} (hc' : c' ∈ restrict z cubes) (hs : CubeSat ν c') :
    ∃ c ∈ cubes, CubeSat ν c := by
  simp only [restrict, List.mem_filterMap] at hc'
  obtain ⟨c, hc, he⟩ := hc'
  split at he
  · exact absurd he (by simp)
  · simp only [Option.some.injEq] at he
    subst he
    refine ⟨c, hc, fun w hw => ?_⟩
    by_cases hwz : w = z
    · exact hwz ▸ hz
    · exact hs w (List.mem_filter.2 ⟨hw, by simpa using hwz⟩)

theorem covers_of_coverAux : ∀ (fuel : ℕ) (cubes : List (List ℤ)),
    coverAux fuel cubes = true → Covers cubes
  | 0, _, h => by simp [coverAux] at h
  | fuel + 1, cubes, h => by
    intro ν
    by_cases he : cubes.any List.isEmpty = true
    · obtain ⟨c, hc, hce⟩ := List.any_eq_true.1 he
      refine ⟨c, hc, ?_⟩
      have : c = [] := List.isEmpty_iff.1 hce
      subst this
      intro w hw
      simp at hw
    · rcases cubes with _ | ⟨_ | ⟨z, rest⟩, more⟩
      · simp [coverAux] at h
      · exact ⟨[], List.mem_cons_self, fun w hw => by simp at hw⟩
      · unfold coverAux at h
        rw [if_neg he] at h
        simp only [Bool.and_eq_true, bne_iff_ne, ne_eq] at h
        obtain ⟨⟨hz, h1⟩, h2⟩ := h
        by_cases hs : LitSat ν z
        · obtain ⟨c', hc', hsc'⟩ := covers_of_coverAux fuel _ h1 ν
          exact cubeSat_of_restrict hs hc' hsc'
        · obtain ⟨c', hc', hsc'⟩ := covers_of_coverAux fuel _ h2 ν
          exact cubeSat_of_restrict (litSat_neg hz hs) hc' hsc'

/-- **Soundness of the cover check.** -/
theorem covers_of_coverCheck {cubes : List (List ℤ)} (h : coverCheck cubes = true) :
    Covers cubes :=
  covers_of_coverAux _ _ h

/-- The CNF of one cube: `F` and the cube literals as unit clauses. -/
def cubeCnf (F : List (List ℤ)) (cube : List ℤ) : List (List ℤ) := F ++ cube.map fun z => [z]

/-- **Composition.** A cover whose cubes are all refuted refutes `F`. -/
theorem not_dimacsSatisfiable_of_cover {F : List (List ℤ)} {cubes : List (List ℤ)}
    (hcov : Covers cubes) (hcube : ∀ c ∈ cubes, ¬DimacsSatisfiable (cubeCnf F c)) :
    ¬DimacsSatisfiable F := by
  rintro ⟨ν, hν⟩
  obtain ⟨c, hc, hsat⟩ := hcov ν
  apply hcube c hc
  refine ⟨ν, fun cl hcl => ?_⟩
  simp only [cubeCnf, List.mem_append, List.mem_map] at hcl
  rcases hcl with hcl | ⟨z, hz, rfl⟩
  · exact hν cl hcl
  · exact ⟨z, List.mem_singleton_self _, hsat z hz⟩

/-- The same with the cover given by a successful run of `coverCheck`. -/
theorem not_dimacsSatisfiable_of_coverCheck {F : List (List ℤ)} {cubes : List (List ℤ)}
    (hcov : coverCheck cubes = true)
    (hcube : ∀ c ∈ cubes, ¬DimacsSatisfiable (cubeCnf F c)) : ¬DimacsSatisfiable F :=
  not_dimacsSatisfiable_of_cover (covers_of_coverCheck hcov) hcube

end Mir

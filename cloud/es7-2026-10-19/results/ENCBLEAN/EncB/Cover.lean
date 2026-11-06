import EncB.Dimacs
import EncB.Coded

/-!
# Cube covers and the 64 cubes of B(6,8,11) (Std-only)

`cubeCnf`, `CubeSat`, `Covers`, `litSat_neg` and `not_dimacsSatisfiable_of_cover` are copied from H3
`MirrorEncoding/Cover.lean:29-48,95-108` (namespace `Mir` there). H3's cover *check* (`coverCheck`,
`CoverCore.lean`) is not needed: the cover of the sign patterns is proved structurally (`covers_signPatterns`), for
any list of nonzero literals, so nothing here depends on what the cube variables mean or on evaluating `encB`.

`cubes64 = signPatterns [1, 2, 3, 10, 11, 18]` lists the 64 cubes in mkcubes order: the 32 cubes with unit `+1`
first, then the 32 with `−1`; inside each half `itertools.product((1, 0), repeat=5)` over the last five
(`C6UPPER/tools/mkcubes.py:17-20`, noty12.py:76-78). In the numbering `encB 6 8 11` produces, these six variables
are Y(1,2), Y(1,3), Y(1,4), Y(2,3), Y(2,4), Y(3,4); that is checked by compiled code when the cube files are written
(`encb_dimacs twin-cubes64`, see the README), never by the kernel.
-/

namespace EncB

/-- A cube (a conjunction of DIMACS literals) holds under `ν` (H3 `Cover.lean:29`). -/
def CubeSat (ν : Nat → Bool) (cube : List Int) : Prop := ∀ z ∈ cube, LitSat ν z

/-- The cubes cover the whole space (H3 `Cover.lean:32`). -/
def Covers (cubes : List (List Int)) : Prop := ∀ ν : Nat → Bool, ∃ c ∈ cubes, CubeSat ν c

/-- H3 `Cover.lean:34`. -/
theorem litSat_neg {ν : Nat → Bool} {z : Int} (hz : z ≠ 0) (h : ¬LitSat ν z) : LitSat ν (-z) := by
  unfold LitSat at h ⊢
  rw [Int.natAbs_neg]
  rcases Int.lt_trichotomy z 0 with hlt | heq | hgt
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

/-- All `2 ^ n` sign patterns of `vs`, in `itertools.product((1, 0), repeat=n)` order (positive first, last
coordinate fastest). -/
def signPatterns : List Int → List (List Int)
  | [] => [[]]
  | v :: vs => (signPatterns vs).map (v :: ·) ++ (signPatterns vs).map ((-v) :: ·)

theorem length_signPatterns : ∀ vs : List Int, (signPatterns vs).length = 2 ^ vs.length
  | [] => rfl
  | v :: vs => by
    simp only [signPatterns, List.length_append, List.length_map, length_signPatterns vs,
      List.length_cons, Nat.pow_succ]
    omega

/-- **The sign patterns of nonzero literals cover every assignment.** -/
theorem covers_signPatterns : ∀ {vs : List Int}, (∀ v ∈ vs, v ≠ 0) → Covers (signPatterns vs)
  | [], _ => fun _ => ⟨[], List.mem_singleton_self _, fun _ hz => absurd hz List.not_mem_nil⟩
  | v :: vs, h => by
    intro ν
    obtain ⟨c, hc, hsat⟩ := covers_signPatterns (fun w hw => h w (List.mem_cons_of_mem v hw)) ν
    have hv : v ≠ 0 := h v List.mem_cons_self
    by_cases hs : LitSat ν v
    · refine ⟨v :: c, ?_, ?_⟩
      · exact List.mem_append_left _ (List.mem_map_of_mem hc)
      · intro z hz
        rcases List.mem_cons.1 hz with rfl | hz
        · exact hs
        · exact hsat z hz
    · refine ⟨(-v) :: c, ?_, ?_⟩
      · exact List.mem_append_right _ (List.mem_map_of_mem hc)
      · intro z hz
        rcases List.mem_cons.1 hz with rfl | hz
        · exact litSat_neg hv hs
        · exact hsat z hz

/-- The CNF of one cube: `F` and the cube literals as unit clauses (H3 `Cover.lean:95`). -/
def cubeCnf (F : List (List Int)) (cube : List Int) : List (List Int) := F ++ cube.map fun z => [z]

/-- **Composition** (H3 `Cover.lean:98`): a cover whose cubes are all refuted refutes `F`. -/
theorem not_dimacsSatisfiable_of_cover {F : List (List Int)} {cubes : List (List Int)}
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

/-! ## The 64 cubes of B(6,8,11) (variant A of `DESIGN.md` §1.1) -/

/-- The DIMACS numbers of Y(1,2), Y(1,3), Y(1,4), Y(2,3), Y(2,4), Y(3,4) in `encB 6 8 11` (checked by compiled
code against the twin's own numbering and against gen_b2.py's map file; see the README). -/
def cubeVars64 : List Int := [1, 2, 3, 10, 11, 18]

/-- The 64 sign patterns of `cubeVars64`, in mkcubes order (`c`-cubes, then `n`-cubes). -/
def cubes64 : List (List Int) := signPatterns cubeVars64

theorem cubeVars64_ne_zero : ∀ v ∈ cubeVars64, v ≠ 0 := by decide

theorem length_cubes64 : cubes64.length = 64 := by
  rw [cubes64, length_signPatterns]
  rfl

/-- The only external input of variant A: one cake_lpr verdict per cube file. -/
def CubesUnsat64 : Prop := ∀ c ∈ cubes64, ¬DimacsSatisfiable (cubeCnf (encB 6 8 11) c)

/-- **The 64 cube refutations refute `encB 6 8 11`.** The proof never evaluates `encB 6 8 11`: the cover is
structural, and the only `decide` is `cubeVars64_ne_zero` (six numerals). -/
theorem encB_unsat_of_cubes64 (h : ∀ c ∈ cubes64, ¬DimacsSatisfiable (cubeCnf (encB 6 8 11) c)) :
    ¬DimacsSatisfiable (encB 6 8 11) :=
  not_dimacsSatisfiable_of_cover (covers_signPatterns cubeVars64_ne_zero) h

theorem encB_unsat_of_cubesUnsat64 (h : CubesUnsat64) : ¬DimacsSatisfiable (encB 6 8 11) :=
  encB_unsat_of_cubes64 h

end EncB

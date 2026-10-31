import MirrorEncoding.Cover
import V2L.Defs

/-!
# Clause covers: composing UNSAT results through blocking clauses

H3's `Mir.not_dimacsSatisfiable_of_cover` composes per-cube refutations when the cubes cover
every assignment. Here the cover is itself certified by a SAT solver: `F` together with the
*blocking clauses* `negClause c` of a list of cubes is UNSAT, so every model of `F` satisfies
one of the cubes. This is the argument of `results/Mii-S/soundness.md` ("certificate
argument").

* `negClause c` (`V2L.Defs`) is the clause of the negated literals of the cube `c`.
* `not_dimacsSatisfiable_of_clauseCover` (one level): `F ++ blocking clauses` UNSAT and every
  `cubeCnf F c` UNSAT.
* `not_dimacsSatisfiable_of_clauseCover₂` (two levels, as in `cover.py`): `F ++ {¬UP(u)}`
  UNSAT; for each `u`, `cubeCnf F (UP u) ++ {¬c : c ∈ casesOf u}` UNSAT; every case UNSAT.
  The form with `Us : List (List ℤ)` and `casesOf : List ℤ → List (List ℤ)` is
  `not_dimacsSatisfiable_of_clauseCover₂'`.
* `not_dimacsSatisfiable_of_clauseCover₂_leaves`: the same with each case refuted by leaf
  cubes accepted by `coverCheck`, each leaf CNF being `cubeCnf (cubeCnf F c) l`.

All literals of the blocked cubes must be nonzero: the literal `0` is never satisfied, so
`negClause` of a cube containing `0` would not block it.
-/

namespace V2L

open ETV Mir

theorem withUnits_eq : withUnits = cubeCnf := rfl

theorem cubeSat_of_not_negClause {ν : ℕ → Bool} {c : List ℤ} (hc : ∀ z ∈ c, z ≠ 0)
    (h : ¬∃ z ∈ negClause c, LitSat ν z) : CubeSat ν c := by
  intro z hz
  by_contra hn
  exact h ⟨-z, List.mem_map.2 ⟨z, hz, rfl⟩, litSat_neg (hc z hz) hn⟩

/-- A model of `F` that cannot be extended past the blocking clauses satisfies some cube. -/
theorem exists_cubeSat_of_block {F cubes : List (List ℤ)} {ν : ℕ → Bool}
    (hnz : ∀ c ∈ cubes, ∀ z ∈ c, z ≠ 0) (hF : DimacsSat F ν)
    (h : ¬DimacsSatisfiable (F ++ cubes.map negClause)) : ∃ c ∈ cubes, CubeSat ν c := by
  by_contra hno
  apply h
  refine ⟨ν, fun cl hcl => ?_⟩
  rcases List.mem_append.1 hcl with hcl | hcl
  · exact hF cl hcl
  · obtain ⟨c, hc, rfl⟩ := List.mem_map.1 hcl
    by_contra hns
    exact hno ⟨c, hc, cubeSat_of_not_negClause (hnz c hc) hns⟩

theorem dimacsSat_cubeCnf {F : List (List ℤ)} {c : List ℤ} {ν : ℕ → Bool}
    (hF : DimacsSat F ν) (hc : CubeSat ν c) : DimacsSat (cubeCnf F c) ν := by
  intro cl hcl
  simp only [cubeCnf, List.mem_append, List.mem_map] at hcl
  rcases hcl with hcl | ⟨z, hz, rfl⟩
  · exact hF cl hcl
  · exact ⟨z, List.mem_singleton_self _, hc z hz⟩

/-- **One-level clause cover.** -/
theorem not_dimacsSatisfiable_of_clauseCover {F cubes : List (List ℤ)}
    (hnz : ∀ c ∈ cubes, ∀ z ∈ c, z ≠ 0)
    (hroot : ¬DimacsSatisfiable (F ++ cubes.map negClause))
    (hcase : ∀ c ∈ cubes, ¬DimacsSatisfiable (cubeCnf F c)) : ¬DimacsSatisfiable F := by
  rintro ⟨ν, hν⟩
  obtain ⟨c, hc, hs⟩ := exists_cubeSat_of_block hnz hν hroot
  exact hcase c hc ⟨ν, dimacsSat_cubeCnf hν hs⟩

/-- **Two-level clause cover**, with an index type: the first level blocks the cubes `up u`
(`u ∈ Us`); below `up u`, the second level blocks the cubes `casesOf u`. -/
theorem not_dimacsSatisfiable_of_clauseCover₂ {α : Type*} {F : List (List ℤ)} {Us : List α}
    {up : α → List ℤ} {casesOf : α → List (List ℤ)}
    (hnzU : ∀ u ∈ Us, ∀ z ∈ up u, z ≠ 0)
    (hnzC : ∀ u ∈ Us, ∀ c ∈ casesOf u, ∀ z ∈ c, z ≠ 0)
    (hroot : ¬DimacsSatisfiable (F ++ (Us.map up).map negClause))
    (hup : ∀ u ∈ Us, ¬DimacsSatisfiable (cubeCnf F (up u) ++ (casesOf u).map negClause))
    (hcase : ∀ u ∈ Us, ∀ c ∈ casesOf u, ¬DimacsSatisfiable (cubeCnf F c)) :
    ¬DimacsSatisfiable F := by
  rintro ⟨ν, hν⟩
  have hnz : ∀ c ∈ Us.map up, ∀ z ∈ c, z ≠ 0 := by
    intro c hc
    obtain ⟨u, hu, rfl⟩ := List.mem_map.1 hc
    exact hnzU u hu
  obtain ⟨c, hc, hs⟩ := exists_cubeSat_of_block hnz hν hroot
  obtain ⟨u, hu, rfl⟩ := List.mem_map.1 hc
  obtain ⟨c', hc', hs'⟩ :=
    exists_cubeSat_of_block (hnzC u hu) (dimacsSat_cubeCnf hν hs) (hup u hu)
  exact hcase u hu c' hc' ⟨ν, dimacsSat_cubeCnf hν hs'⟩

/-- **Two-level clause cover**, with the first-level cubes as the index list. -/
theorem not_dimacsSatisfiable_of_clauseCover₂' {F Us : List (List ℤ)}
    {casesOf : List ℤ → List (List ℤ)}
    (hnzU : ∀ u ∈ Us, ∀ z ∈ u, z ≠ 0)
    (hnzC : ∀ u ∈ Us, ∀ c ∈ casesOf u, ∀ z ∈ c, z ≠ 0)
    (hroot : ¬DimacsSatisfiable (F ++ Us.map negClause))
    (hup : ∀ u ∈ Us, ¬DimacsSatisfiable (cubeCnf F u ++ (casesOf u).map negClause))
    (hcase : ∀ u ∈ Us, ∀ c ∈ casesOf u, ¬DimacsSatisfiable (cubeCnf F c)) :
    ¬DimacsSatisfiable F :=
  not_dimacsSatisfiable_of_clauseCover₂ (up := id) hnzU hnzC (by simpa using hroot) hup hcase

/-- **Leaf form of one case**: leaves accepted by `coverCheck`, each leaf CNF
`cubeCnf (cubeCnf F c) l` (the case CNF with the leaf's units appended) UNSAT. -/
theorem not_dimacsSatisfiable_case_of_leaves {F : List (List ℤ)} {c : List ℤ}
    {leaves : List (List ℤ)} (hcov : coverCheck leaves = true)
    (h : ∀ l ∈ leaves, ¬DimacsSatisfiable (cubeCnf (cubeCnf F c) l)) :
    ¬DimacsSatisfiable (cubeCnf F c) :=
  not_dimacsSatisfiable_of_coverCheck hcov h

/-- **One-level clause cover, leaf form.** -/
theorem not_dimacsSatisfiable_of_clauseCover_leaves {F cubes : List (List ℤ)}
    {leaves : List ℤ → List (List ℤ)}
    (hnz : ∀ c ∈ cubes, ∀ z ∈ c, z ≠ 0)
    (hroot : ¬DimacsSatisfiable (F ++ cubes.map negClause))
    (hcov : ∀ c ∈ cubes, coverCheck (leaves c) = true)
    (hleaf : ∀ c ∈ cubes, ∀ l ∈ leaves c, ¬DimacsSatisfiable (cubeCnf (cubeCnf F c) l)) :
    ¬DimacsSatisfiable F :=
  not_dimacsSatisfiable_of_clauseCover hnz hroot fun c hc =>
    not_dimacsSatisfiable_case_of_leaves (hcov c hc) (hleaf c hc)

/-- **Two-level clause cover, leaf form.** -/
theorem not_dimacsSatisfiable_of_clauseCover₂_leaves {F Us : List (List ℤ)}
    {casesOf : List ℤ → List (List ℤ)} {leaves : List ℤ → List (List ℤ)}
    (hnzU : ∀ u ∈ Us, ∀ z ∈ u, z ≠ 0)
    (hnzC : ∀ u ∈ Us, ∀ c ∈ casesOf u, ∀ z ∈ c, z ≠ 0)
    (hroot : ¬DimacsSatisfiable (F ++ Us.map negClause))
    (hup : ∀ u ∈ Us, ¬DimacsSatisfiable (cubeCnf F u ++ (casesOf u).map negClause))
    (hcov : ∀ u ∈ Us, ∀ c ∈ casesOf u, coverCheck (leaves c) = true)
    (hleaf : ∀ u ∈ Us, ∀ c ∈ casesOf u, ∀ l ∈ leaves c,
      ¬DimacsSatisfiable (cubeCnf (cubeCnf F c) l)) :
    ¬DimacsSatisfiable F :=
  not_dimacsSatisfiable_of_clauseCover₂' hnzU hnzC hroot hup fun u hu c hc =>
    not_dimacsSatisfiable_case_of_leaves (hcov u hu c hc) (hleaf u hu c hc)

end V2L

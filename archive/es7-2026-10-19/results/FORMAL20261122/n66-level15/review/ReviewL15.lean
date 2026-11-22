import N66G15.End

/-!
Independent statement-fidelity review of item n66-level15 (slot lrv3). One compile, bare `lean` against the worker's
oleans with a read-only LEAN_PATH, no `-o` (writes no olean). It prints axioms (first), the compiled statement and
the definitions in it, checks the level-15 scalar constants by `rfl`, re-checks the worker's unfolded statement, adds
the reviewer's own restatement and a contrapositive corollary, and dumps data terms (leaves, rows, embedded rows text,
state list, SB pairs) into review/ for comparison with the record by the reviewer's own code. Nothing here evaluates
`num`, `toDimacs`, `pyMap`, `eagerStream` or `fullCnf`.
-/

open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks

/-! ## 1. Axioms: the end theorem, every theorem of the worker's list, and the closure lemmas -/
#print axioms N66G15.n66_bound_54_of_cubes
#print axioms N66E15.fullUnsat_of_text
#print axioms N66E15.base_unsat_of_cubes
#print axioms N66G15.holds_card
#print axioms N66G15.holes_le
#print axioms N66G15.leaves105_length
#print axioms N66E15.printClause_mem
#print axioms N66E15.printClauses_mem
#print axioms N66E15.no_base_model
#print axioms N66E15.covers_leaves
#print axioms N66E15.unsat_of_sub
#print axioms N66E15.dimacsSat_of_holds
#print axioms N66E15.stateListOk_true
#print axioms N66G15.no_model_of_cubes
#print axioms N66G15.holds_baseS
#print axioms N66G15.holds_sb
#print axioms N66G15.holds_fixed
#print axioms N66G15.lexChoice
#print axioms N66G15.holds_pair
#print axioms N66G15.holds_pos
#print axioms N66G15.holds_thresh
#print axioms N66G15.holds_triple
#print axioms N66G15.holds_ceue
#print axioms N66G15.holds_quad
#print axioms N66G15.holds_eager_of_parts
#print axioms N66G15.mirror_holds
#print axioms N66G15.capCup55_holds
#print axioms N66G15.signotope_of_config
#print axioms N66G15.n66Bound_unfold
#print axioms N66G15.n66_bound_54_of_gaps
#print axioms N66G15.n66_bound_54_of_gaps2
#print axioms N66G15.n66_bound_54_of_gaps3
#print axioms N66G15.n66_bound_54_of_gaps4
#print axioms N66G15.n66_bound_54_of_gaps5
#print axioms N66G15.n66_bound_54_of_capCup55
#print axioms EncB.parseDimacs_render

/-! ## 2. The statement as compiled -/
#check @N66G15.n66_bound_54_of_cubes
#check @N66E15.fullUnsat_of_text
#check @N66E15.base_unsat_of_cubes
#check @N66G15.holds_card
#check @N66G15.holes_le
#check @N66G15.leaves105_length

/-! ## 3. Definitions in the statement (and below it) -/
#print OmissionZRow.N66Bound
#print N66E15.CubesUnsat105
#print N66E15.fullCnf
#print N66E15.fullS
#print N66E15.baseS
#print N66E15.leaves105
#print N66E15.SplitTree.leaves
#print N66E15.SplitTree.leavesFrom
#print N66E15.R0_15
#print N66E15.parseRows
#print N66E15.toDimacs
#print N66E15.litInt
#print N66E15.cubeUnit
#print N66E15.rowClause
#print N66E15.fixedUnits
#print N66E15.cardClauses
#print N66E15.kBound
#print N66E15.nLits
#print N66E15.nvHeader
#print N66E15.printClause
#print N66E15.printClauses
#print N66E15.litsBounded
#print N66G15.RowsValid
#print N66G15.RowValid
#print N66G15.InClass
#print N66G15.n66Occ
#print N66G15.idxOf
#print N66G15.profOf
#print N66G15.Model.holes
#print N66G15.Model.holesUpTo
#print ErdosSzekeres.Omission.ActualRanks.column
#print ErdosSzekeres.Omission.ActualRanks.labels
#print ErdosSzekeres.Omission.ActualRanks.rank
#print ErdosSzekeres.Omission.ActualRanks.EndingPath
#print ErdosSzekeres.Omission.Configuration
#print ErdosSzekeres.Omission.Configuration.cup
#print ErdosSzekeres.Omission.Configuration.HasCap
#print ErdosSzekeres.Omission.Configuration.HasCup
#print ErdosSzekeres.HasConvexNGon
#print ErdosSzekeres.ConvexPosition
#print ErdosSzekeres.orient
#print EncB.DimacsSatisfiable
#print EncB.DimacsSat
#print EncB.LitSat
#print EncB.render

/-! ## 4. Level-15 scalar constants (definitional) -/
example : N66E15.kBound = 15 := rfl
example : N66E15.nLits = 68 := rfl
example : N66E15.nvHeader = 1647847 := rfl
example : N66E15.leaves105.length = 105 := N66G15.leaves105_length
example : ∀ M : N66G15.Model, 55 ≤ M.n → M.holes ≤ 15 := N66G15.holes_le
example : ∀ M : N66G15.Model, M.holes ≤ 15 → M.Holds N66E15.cardClauses := N66G15.holds_card

/-! ## 5a. The worker's unfolded statement (`check/Check15.lean`, text copied verbatim), re-checked here -/
theorem check15_unfolded_recheck :
    (∀ c ∈ N66E15.leaves105, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ N66E15.fullCnf N66E15.R0_15 c, ∃ l ∈ cl,
        (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)) →
    (∀ T ∈ N66E15.R0_15, ∀ n (c : Configuration n),
        (¬ c.HasCap 6 ∧ ¬ c.HasCup 6 ∧ ¬ HasConvexNGon 8 (Finset.univ.image c.point)) →
        ∃ s ∈ T, ¬ ∃ v < n, N66E15.stateList.idxOf
          (ErdosSzekeres.Omission.ActualRanks.column c.cup v 0,
           ErdosSzekeres.Omission.ActualRanks.column c.cup v 1,
           ErdosSzekeres.Omission.ActualRanks.column c.cup v 2,
           ErdosSzekeres.Omission.ActualRanks.column c.cup v 3) = s.val) →
    ∀ n (c : Configuration n), ¬ c.HasCap 6 → ¬ c.HasCup 6 →
      ¬ HasConvexNGon 8 (Finset.univ.image c.point) → n ≤ 54 :=
  N66G15.n66_bound_54_of_cubes

/-! ## 5b. The reviewer's own restatement: hypotheses named, `DimacsSatisfiable` and `LitSat` spelled through
`DimacsSat`'s body, `RowsValid`/`RowValid`/`InClass`/`n66Occ`/`idxOf`/`profOf` unfolded, conclusion through
`N66Bound`'s body. Accepted iff definitionally equal to the compiled statement. -/
theorem review15_unfolded
    (hcubes : ∀ c ∈ N66E15.tree15.leaves, ∀ ν : ℕ → Bool,
      ¬ ∀ cl ∈ N66E15.fullCnf N66E15.R0_15 c, ∃ l ∈ cl, (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false))
    (hrows : ∀ T ∈ N66E15.R0_15, ∀ (n : ℕ) (c : Configuration n),
      (¬ c.HasCap 6 ∧ ¬ c.HasCup 6 ∧ ¬ HasConvexNGon 8 (Finset.univ.image c.point)) →
      ∃ s ∈ T, ¬ ∃ v, v < n ∧ N66E15.stateList.idxOf
          (column c.cup v 0, column c.cup v 1, column c.cup v 2, column c.cup v 3) = s.val) :
    ∀ (n : ℕ) (c : Configuration n), ¬ c.HasCap 6 → ¬ c.HasCup 6 →
      ¬ HasConvexNGon 8 (Finset.univ.image c.point) → n ≤ 54 :=
  N66G15.n66_bound_54_of_cubes (fun c hc ⟨ν, hν⟩ => hcubes c hc ν hν) hrows

/-! ## 5c. Contrapositive corollary: 55 points of the configuration force a 6-cap, a 6-cup or a convex octagon -/
theorem review15_contra (h : N66E15.CubesUnsat105) (hR : N66G15.RowsValid N66E15.R0_15)
    (n : ℕ) (c : Configuration n) (hn : 55 ≤ n) :
    c.HasCap 6 ∨ c.HasCup 6 ∨ HasConvexNGon 8 (Finset.univ.image c.point) := by
  by_contra hc
  have h1 : ¬ c.HasCap 6 := fun x => hc (Or.inl x)
  have h2 : ¬ c.HasCup 6 := fun x => hc (Or.inr (Or.inl x))
  have h3 : ¬ HasConvexNGon 8 (Finset.univ.image c.point) := fun x => hc (Or.inr (Or.inr x))
  have hb : ∀ (m : ℕ) (d : Configuration m), ¬ d.HasCap 6 → ¬ d.HasCup 6 →
      ¬ HasConvexNGon 8 (Finset.univ.image d.point) → m ≤ 54 := N66G15.n66_bound_54_of_cubes h hR
  have := hb n c h1 h2 h3
  omega

#print axioms check15_unfolded_recheck
#print axioms review15_unfolded
#print axioms review15_contra

/-! ## 6. Data dumps (interpreter; compared with the record by the reviewer's own Python) -/
def reviewOut : String := "/home/jay/research/data/formalize-20261122/n66-level15/review/"

#eval show IO Unit from do
  IO.FS.writeFile (reviewOut ++ "dump_leaves105.txt") <|
    String.intercalate "\n" (N66E15.leaves105.map fun c =>
      " ".intercalate (c.map fun z => s!"{z.1.val}:{if z.2 then 1 else 0}")) ++ "\n"
  IO.FS.writeFile (reviewOut ++ "dump_R0_15.txt") <|
    String.intercalate "\n" (N66E15.R0_15.map fun T => " ".intercalate (T.map fun s => toString s.val)) ++ "\n"
  IO.FS.writeFile (reviewOut ++ "dump_rowsText.txt") N66E15.rowsText
  IO.FS.writeFile (reviewOut ++ "dump_stateList.txt") <|
    String.intercalate "\n" (N66E15.stateList.map fun p => s!"{p.1} {p.2.1} {p.2.2.1} {p.2.2.2}") ++ "\n"
  IO.FS.writeFile (reviewOut ++ "dump_sbPairs.txt") <|
    String.intercalate "\n" (N66E15.sbPairs.map fun p => s!"{p.1.val} {p.2.val}") ++ "\n"
  IO.println s!"leaves105 {N66E15.leaves105.length} R0_15 {N66E15.R0_15.length} rowsText bytes {N66E15.rowsText.utf8ByteSize} stateList {N66E15.stateList.length} sbPairs {N66E15.sbPairs.length}"

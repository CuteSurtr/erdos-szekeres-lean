import N66Geo.End

/-!
Independent statement-fidelity review of item n66-encoder (slot lrv2). Loads the worker's oleans read-only, prints
axioms and definitions, restates the end theorem fully unfolded (checked by the elaborator/kernel against the
compiled theorem), and dumps data terms (leaves, rows, embedded rows text, state list) for comparison with the
record by the reviewer's own Python.
-/

open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks

/-! ## 1. Axioms -/
#print axioms N66Geo.n66_bound_55_of_cubes
#print axioms N66Enc.fullUnsat_of_text
#print axioms N66Enc.printClause_mem
#print axioms N66Enc.printClauses_mem
#print axioms N66Enc.base_unsat_of_cubes
#print axioms N66Geo.no_model_of_cubes
#print axioms N66Geo.capCup55_holds
#print axioms N66Geo.mirror_holds
#print axioms N66Geo.lexChoice
#print axioms N66Geo.holes_le
#print axioms N66Geo.leaves132_length
#print axioms N66Geo.n66Bound_unfold

/-! ## 2. The statement as compiled -/
#check @N66Geo.n66_bound_55_of_cubes

/-! ## 3. Definitions in the statement -/
#print OmissionZRow.N66Bound
#print N66Enc.CubesUnsat132
#print N66Enc.fullCnf
#print N66Enc.fullS
#print N66Enc.leaves132
#print N66Enc.R0
#print N66Geo.RowsValid
#print N66Geo.RowValid
#print N66Geo.InClass
#print N66Geo.n66Occ
#print N66Geo.idxOf
#print N66Geo.profOf
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

/-! ## 4. The end theorem, restated with every non-data definition unfolded by hand.
Only the data terms `N66Enc.leaves132`, `N66Enc.fullCnf`, `N66Enc.R0`, `N66Enc.stateList` and the library's
`column` / `Configuration` / `HasCap` / `HasCup` / `HasConvexNGon` remain. Accepted iff the hand-written type is
definitionally the compiled one. -/
theorem review_unfolded :
    (∀ c ∈ N66Enc.leaves132, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ N66Enc.fullCnf N66Enc.R0 c, ∃ l ∈ cl,
        (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)) →
    (∀ T ∈ N66Enc.R0, ∀ n (c : Configuration n),
        (¬ c.HasCap 6 ∧ ¬ c.HasCup 6 ∧ ¬ HasConvexNGon 8 (Finset.univ.image c.point)) →
        ∃ s ∈ T, ¬ ∃ v < n, N66Enc.stateList.idxOf
          (ErdosSzekeres.Omission.ActualRanks.column c.cup v 0,
           ErdosSzekeres.Omission.ActualRanks.column c.cup v 1,
           ErdosSzekeres.Omission.ActualRanks.column c.cup v 2,
           ErdosSzekeres.Omission.ActualRanks.column c.cup v 3) = s.val) →
    ∀ n (c : Configuration n), ¬ c.HasCap 6 → ¬ c.HasCup 6 →
      ¬ HasConvexNGon 8 (Finset.univ.image c.point) → n ≤ 55 :=
  N66Geo.n66_bound_55_of_cubes

#print axioms review_unfolded

/-! ## 5. Data dumps (interpreter; not evidence by themselves, compared with the record by own Python) -/
def reviewOut : String := "/home/jay/research/data/formalize-20261122/n66enc/review/"

#eval show IO Unit from do
  IO.FS.writeFile (reviewOut ++ "dump_leaves132.txt") <|
    String.intercalate "\n" (N66Enc.leaves132.map fun c =>
      " ".intercalate (c.map fun z => s!"{z.1.val}:{if z.2 then 1 else 0}")) ++ "\n"
  IO.FS.writeFile (reviewOut ++ "dump_R0.txt") <|
    String.intercalate "\n" (N66Enc.R0.map fun T => " ".intercalate (T.map fun s => toString s.val)) ++ "\n"
  IO.FS.writeFile (reviewOut ++ "dump_rowsText.txt") N66Enc.rowsText
  IO.FS.writeFile (reviewOut ++ "dump_stateList.txt") <|
    String.intercalate "\n" (N66Enc.stateList.map fun p => s!"{p.1} {p.2.1} {p.2.2.1} {p.2.2.2}") ++ "\n"
  IO.println s!"leaves132 {N66Enc.leaves132.length} R0 {N66Enc.R0.length} rowsText bytes {N66Enc.rowsText.utf8ByteSize} stateList {N66Enc.stateList.length}"

-- fv304-audit independent review (slot rv4, 22 Nov 2026): the ONE compile of this review. No -o: no olean written.
-- LEAN_PATH = /home/jay/research/data/fv304-20261120/lean_path.txt + fv304-audit/olean (both read only).
-- Plain #check / #print / #print axioms lines, my own re-derivation of the combined theorem (kernel-checked here),
-- and soft meta checks (#eval with try/catch: a slip in my transcription prints RV-ERROR and cannot change lean_rc).
import E304Z.Final
import FV4A.Combined
import E304Z.C260801
import E304Z.C311801
import E304Z.C325201
import E304Z.C634501
import ErdosSzekeres.LowerBound.Construction

set_option format.width 100000
set_option Elab.async false

/-! ## Own re-derivation of the combined theorem (checked by the kernel in this compile) -/
namespace RV

theorem forces_304
    (n66 : OmissionZRow.N66Bound 55)
    (vP : Res118.BlockValid Res118.rowsP) (vQ : Res118.BlockValid Res118.rowsQ)
    (vU : Res118.BlockValid Res118.rowsU) (vA : Res118.BlockValid Res118.rowsA)
    (s33_18 : Res118.ResSliceExcludes [] 33 18)
    (s34_18 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 34 18)
    (s34_19 : Res118.ResSliceExcludes Res118.rowsP 34 19)
    (s35_18 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 35 18)
    (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 304 8 :=
  Res118.forces_304_of_slices E304Z.Final.excludes_67 n66 vP vQ vU vA s33_18 s34_18 s34_19 s35_18 s35_19 s35_20

/-- Second route: FV304's own final theorem fed with Res118's residual bound. -/
theorem forces_304_alt
    (n66 : OmissionZRow.N66Bound 55)
    (vP : Res118.BlockValid Res118.rowsP) (vQ : Res118.BlockValid Res118.rowsQ)
    (vU : Res118.BlockValid Res118.rowsU) (vA : Res118.BlockValid Res118.rowsA)
    (s33_18 : Res118.ResSliceExcludes [] 33 18)
    (s34_18 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 34 18)
    (s34_19 : Res118.ResSliceExcludes Res118.rowsP 34 19)
    (s35_18 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 35 18)
    (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 304 8 :=
  E304Z.Final.forces_304_of_n66_res n66
    (Res118.residual_bound_118_of_slices n66 vP vQ vU vA s33_18 s34_18 s34_19 s35_18 s35_19 s35_20)

end RV

/-! ## Meta helpers (own code) -/
open Lean Meta Elab Term in
def RVTool.elabStr (s : String) : TermElabM Expr := do
  match Parser.runParserCategory (← getEnv) `term s with
  | .error e => throwError "parse error: {e}"
  | .ok stx => withoutErrToSorry do
      let e ← elabTerm stx none
      synthesizeSyntheticMVarsNoPostponing
      let e ← instantiateMVars e
      if e.hasMVar then throwError "unassigned metavariables"
      return e

open Lean Meta Elab Term in
/-- The constant's type against my own transcription: alpha-equivalence (`==`) and defeq. -/
def RVTool.checkType (n : Name) (s : String) : TermElabM Unit := do
  try
    let e ← RVTool.elabStr s
    let ci ← getConstInfo n
    let dq ← isDefEq ci.type e
    let al := ci.type == e
    IO.println s!"RV-TYPE {n} alpha={al} defeq={dq}"
  catch ex =>
    let msg ← ex.toMessageData.toString
    IO.println s!"RV-ERROR type {n}: {msg}"

open Lean Meta Elab Term in
/-- Two constants have alpha-equivalent types. -/
def RVTool.sameType (a b : Name) : TermElabM Unit := do
  try
    let ta := (← getConstInfo a).type
    let tb := (← getConstInfo b).type
    let dq ← isDefEq ta tb
    let al := ta == tb
    IO.println s!"RV-SAMETYPE {a} {b} alpha={al} defeq={dq}"
  catch ex =>
    let msg ← ex.toMessageData.toString
    IO.println s!"RV-ERROR sametype {a} {b}: {msg}"

open Lean Meta Elab Term in
/-- Definitional unfolding: two terms (strings) are defeq at default transparency. -/
def RVTool.checkDefEq (tag a b : String) : TermElabM Unit := do
  try
    let ea ← RVTool.elabStr a
    let eb ← RVTool.elabStr b
    let dq ← isDefEq ea eb
    IO.println s!"RV-DEFEQ {tag} {dq}"
  catch ex =>
    let msg ← ex.toMessageData.toString
    IO.println s!"RV-ERROR defeq {tag}: {msg}"

open Lean in
/-- Module that provides each constant. -/
def RVTool.origin (ns : List Name) : CoreM Unit := do
  let env ← getEnv
  for n in ns do
    match env.getModuleIdxFor? n with
    | some i => IO.println s!"RV-ORIGIN {n} {env.header.moduleNames[i.toNat]!}"
    | none => IO.println s!"RV-ORIGIN {n} <not-imported>"

open Lean in
/-- Constants that fix the meaning of the statements `roots` (types, definition bodies, inductive types and
constructors; proofs are skipped), and the modules that provide them. -/
def RVTool.stmtDeps (tag : String) (roots : List Name) : CoreM Unit := do
  let env ← getEnv
  let mut seen : Std.HashSet Name := {}
  let mut todo : Array Name := #[]
  let mut opaques : Array Name := #[]
  let mut axs : Array Name := #[]
  for r in roots do
    match env.find? r with
    | some ci => todo := todo ++ ci.type.getUsedConstants
    | none => IO.println s!"RV-DEPS {tag} missing root {r}"
  while !todo.isEmpty do
    let c := todo.back!
    todo := todo.pop
    unless seen.contains c do
      seen := seen.insert c
      match env.find? c with
      | some (.defnInfo v) => todo := todo ++ v.type.getUsedConstants ++ v.value.getUsedConstants
      | some (.opaqueInfo v) =>
        opaques := opaques.push c
        todo := todo ++ v.type.getUsedConstants ++ v.value.getUsedConstants
      | some (.axiomInfo v) =>
        axs := axs.push c
        todo := todo ++ v.type.getUsedConstants
      | some (.inductInfo v) => todo := todo ++ v.type.getUsedConstants ++ v.ctors.toArray
      | some (.ctorInfo v) => todo := todo ++ v.type.getUsedConstants
      | some (.recInfo v) => todo := todo ++ v.type.getUsedConstants
      | some (.quotInfo v) => todo := todo ++ v.type.getUsedConstants
      | some (.thmInfo _) => pure ()
      | none => IO.println s!"RV-DEPS {tag} unknown {c}"
  let mut mods : Std.HashMap Name Nat := {}
  for c in seen.toList do
    let m : Name := match env.getModuleIdxFor? c with
      | some i => env.header.moduleNames[i.toNat]!
      | none => `_this_file
    mods := mods.insert m (mods.getD m 0 + 1)
  IO.println s!"RV-DEPS {tag} constants={seen.size} modules={mods.size} opaque={opaques.size} axioms={axs.toList}"
  for o in opaques do IO.println s!"RV-DEPOPAQUE {tag} {o}"
  for (m, k) in mods.toArray.qsort (fun a b => a.1.toString < b.1.toString) do
    IO.println s!"RV-DEPMOD {tag} {m} {k}"

open Lean in
partial def RVTool.natOf? (e : Expr) : Option Nat :=
  match e with
  | .lit (.natVal n) => some n
  | .mdata _ b => RVTool.natOf? b
  | _ => if e.isAppOfArity ``OfNat.ofNat 3 then RVTool.natOf? (e.getArg! 1) else none

open Lean in
/-- A list literal as elaborated (cons chains; long literals are nested `let`s, zeta-expanded here). -/
partial def RVTool.listOf? (e : Expr) : Option (List Expr) :=
  match e with
  | .mdata _ b => RVTool.listOf? b
  | .letE _ _ v b _ => RVTool.listOf? (b.instantiate1 v)
  | _ =>
    if e.isAppOfArity ``List.nil 1 then some []
    else if e.isAppOfArity ``List.cons 3 then (RVTool.listOf? (e.getArg! 2)).map (e.getArg! 1 :: ·)
    else none

open Lean in
partial def RVTool.appendParts (e : Expr) : List Expr :=
  if e.isAppOfArity ``HAppend.hAppend 6 then RVTool.appendParts (e.getArg! 4) ++ RVTool.appendParts (e.getArg! 5)
  else [e]

open Lean in
/-- The body of a constant reference (a definition), else the term itself. -/
def RVTool.constBody (env : Environment) (p : Expr) : Expr :=
  ((p.constName?).bind (fun c => (env.find? c).bind (·.value?))).getD p

open Lean in
def RVTool.natList? (e : Expr) : Option (List Nat) :=
  (RVTool.listOf? e).bind (fun xs => xs.mapM RVTool.natOf?)

open Lean in
/-- The rows of a block as stored in the kernel term (`rowsX_00 ++ … ++ rowsX_NN`, each a literal). -/
def RVTool.dumpRows (n : Name) : CoreM Unit := do
  let env ← getEnv
  let some v := (env.find? n).bind (·.value?) | IO.println s!"RV-ERROR rows {n}: no value"
  let parts := RVTool.appendParts v
  let mut rows : Array (List Nat) := #[]
  let mut bad := 0
  for p in parts do
    let es := (RVTool.listOf? (RVTool.constBody env p)).getD []
    if es.isEmpty then bad := bad + 1
    for r in es do
      if let some ns := RVTool.natList? r then rows := rows.push ns else bad := bad + 1
  IO.println s!"RV-ROWS {n} parts={parts.length} rows={rows.size} undecoded={bad}"
  for r in rows do IO.println s!"RV-ROW {n} {r}"

open Lean in
def RVTool.dumpNatList (n : Name) : CoreM Unit := do
  let env ← getEnv
  let some v := (env.find? n).bind (·.value?) | IO.println s!"RV-ERROR natlist {n}: no value"
  let some ns := RVTool.natList? v | IO.println s!"RV-ERROR natlist {n}: not a literal"
  IO.println s!"RV-NATLIST {n} {ns.length} {ns}"

/-! ## 1. Statements as printed (same commands as the audit) -/
#eval IO.println "=== CHECK"
#check E304Z.Final.excludes_67
#check E304Z.Final.forces_304_of_n66_res
#check E304Z.root
#check FV4A.forces_304_of_slices_rows_n66
#check RV.forces_304
#check RV.forces_304_alt
#check Res118.forces_304_of_slices
#check OmissionBalancedZ.composition_304_z
#check ErdosSzekeres.not_forcesConvexNGon_64_8

/-! ## 2. Axioms -/
#eval IO.println "=== AXIOMS"
#print axioms E304Z.Final.excludes_67
#print axioms E304Z.Final.forces_304_of_n66_res
#print axioms E304Z.root
#print axioms E304Z.C260801.ex0
#print axioms E304Z.C311801.ex0
#print axioms E304Z.C325201.ex0
#print axioms E304Z.C634501.ex0
#print axioms FV4A.forces_304_of_slices_rows_n66
#print axioms RV.forces_304
#print axioms RV.forces_304_alt
#print axioms Res118.forces_304_of_slices
#print axioms Res118.residual_bound_118_of_slices
#print axioms OmissionBalancedZ.composition_304_z
#print axioms CompactChecker.BridgeZ.balanced_z_of_root
#print axioms Res118.F_eq
#print axioms Res118.Lo_eq
#print axioms Res118.rows_lengths
#print axioms ErdosSzekeres.not_forcesConvexNGon_64_8

/-! ## 3. Types against my own transcription of the claimed signatures -/
#eval IO.println "=== TYPES"
#eval RVTool.checkType ``E304Z.Final.excludes_67 "OmissionBalancedZ.ExcludesHoleBudgetZ 67"
#eval RVTool.checkType ``E304Z.Final.forces_304_of_n66_res
  "OmissionZRow.N66Bound 55 → ErdosSzekeres.Omission.Partition.ResidualBound 118 → ErdosSzekeres.ForcesConvexNGon 304 8"
#eval RVTool.checkType ``E304Z.root
  "¬ ∃ holes : Fin 252 → ℕ, CompactChecker.FFeas CompactChecker.fcatZ 3132 252 67 (CompactChecker.pmask (CompactChecker.zerosF 252) []) holes"
#eval RVTool.checkType ``FV4A.forces_304_of_slices_rows_n66
  "OmissionZRow.N66Bound 55 → Res118.BlockValid Res118.rowsP → Res118.BlockValid Res118.rowsQ → Res118.BlockValid Res118.rowsU → Res118.BlockValid Res118.rowsA → Res118.ResSliceExcludes [] 33 18 → Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 34 18 → Res118.ResSliceExcludes Res118.rowsP 34 19 → Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 35 18 → Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19 → Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20 → ErdosSzekeres.ForcesConvexNGon 304 8"
#eval RVTool.checkType ``Res118.forces_304_of_slices
  "OmissionBalancedZ.ExcludesHoleBudgetZ 67 → OmissionZRow.N66Bound 55 → Res118.BlockValid Res118.rowsP → Res118.BlockValid Res118.rowsQ → Res118.BlockValid Res118.rowsU → Res118.BlockValid Res118.rowsA → Res118.ResSliceExcludes [] 33 18 → Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 34 18 → Res118.ResSliceExcludes Res118.rowsP 34 19 → Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 35 18 → Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19 → Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20 → ErdosSzekeres.ForcesConvexNGon 304 8"
#eval RVTool.checkType ``OmissionBalancedZ.composition_304_z
  "OmissionBalancedZ.ExcludesHoleBudgetZ 67 → OmissionZRow.N66Bound 55 → ErdosSzekeres.Omission.Partition.ResidualBound 118 → ErdosSzekeres.ForcesConvexNGon 304 8"
#eval RVTool.checkType ``Res118.F_eq "∀ i : Fin 154, i ∈ Res118.F ↔ i.val ∈ Res118.fIndices"
#eval RVTool.checkType ``Res118.Lo_eq "∀ i : Fin 154, i ∈ Res118.Lo ↔ i.val ∈ Res118.loIndices"
#eval RVTool.checkType ``Res118.rows_lengths
  "Res118.rowsP.length = 812 ∧ Res118.rowsQ.length = 208 ∧ Res118.rowsU.length = 35 ∧ Res118.rowsA.length = 970"
#eval RVTool.checkType ``ErdosSzekeres.not_forcesConvexNGon_64_8 "¬ ErdosSzekeres.ForcesConvexNGon 64 8"
#eval RVTool.sameType ``RV.forces_304 ``FV4A.forces_304_of_slices_rows_n66
#eval RVTool.sameType ``RV.forces_304_alt ``FV4A.forces_304_of_slices_rows_n66

/-! ## 4. Definitional unfolding to explicit statements (own transcription) -/
#eval IO.println "=== UNFOLD"
#eval RVTool.checkDefEq "ForcesConvexNGon-304-8"
  "ErdosSzekeres.ForcesConvexNGon 304 8"
  "∀ s : Finset (Fin 2 → ℝ), (∀ a ∈ s, ∀ b ∈ s, ∀ c ∈ s, a ≠ b → a ≠ c → b ≠ c → ¬ Collinear ℝ ({a, b, c} : Set (Fin 2 → ℝ))) → 304 ≤ s.card → ∃ t : Finset (Fin 2 → ℝ), t ⊆ s ∧ t.card = 8 ∧ ConvexIndependent ℝ (fun p : (t : Set (Fin 2 → ℝ)) => (p : Fin 2 → ℝ))"
#eval RVTool.checkDefEq "N66Bound-55"
  "OmissionZRow.N66Bound 55"
  "∀ (n : ℕ) (c : ErdosSzekeres.Omission.Configuration n), ¬ c.HasCap 6 → ¬ c.HasCup 6 → ¬ ErdosSzekeres.HasConvexNGon 8 (Finset.univ.image c.point) → n ≤ 55"
#eval RVTool.checkDefEq "HasCap"
  "fun (n : ℕ) (c : ErdosSzekeres.Omission.Configuration n) (k : ℕ) => c.HasCap k"
  "fun (n : ℕ) (c : ErdosSzekeres.Omission.Configuration n) (k : ℕ) => ∃ f : Fin k → Fin n, StrictMono f ∧ ∀ i j l, i < j → j < l → ErdosSzekeres.orient (c.point (f i)) (c.point (f j)) (c.point (f l)) < 0"
#eval RVTool.checkDefEq "HasCup"
  "fun (n : ℕ) (c : ErdosSzekeres.Omission.Configuration n) (k : ℕ) => c.HasCup k"
  "fun (n : ℕ) (c : ErdosSzekeres.Omission.Configuration n) (k : ℕ) => ∃ f : Fin k → Fin n, StrictMono f ∧ ∀ i j l, i < j → j < l → 0 < ErdosSzekeres.orient (c.point (f i)) (c.point (f j)) (c.point (f l))"
#eval RVTool.checkDefEq "orient"
  "fun (a b c : Fin 2 → ℝ) => ErdosSzekeres.orient a b c"
  "fun (a b c : Fin 2 → ℝ) => (b 0 - a 0) * (c 1 - a 1) - (b 1 - a 1) * (c 0 - a 0)"
#eval RVTool.checkDefEq "ResidualBound-118"
  "ErdosSzekeres.Omission.Partition.ResidualBound 118"
  "∀ (n : ℕ) (c : ErdosSzekeres.Omission.Configuration n), ¬ c.HasCap 6 → ¬ ErdosSzekeres.HasConvexNGon 8 (Finset.univ.image c.point) → ErdosSzekeres.Omission.Subsets.NoJunctionOn c.cup (Finset.range n) → n ≤ 118"

/-! ## 5. Definitions in the statements, printed from the oleans -/
#eval IO.println "=== DEFS"
#print ErdosSzekeres.Point
#print ErdosSzekeres.GeneralPosition
#print ErdosSzekeres.ConvexPosition
#print ErdosSzekeres.HasConvexNGon
#print ErdosSzekeres.ForcesConvexNGon
#print ErdosSzekeres.orient
#print ErdosSzekeres.Omission.Configuration
#print ErdosSzekeres.Omission.Configuration.HasCap
#print ErdosSzekeres.Omission.Configuration.HasCup
#print ErdosSzekeres.Omission.Configuration.cup
#print OmissionZRow.N66Bound
#print ErdosSzekeres.Omission.Partition.ResidualBound
#print ErdosSzekeres.Omission.Subsets.NoJunctionOn
#print ErdosSzekeres.Omission.Subsets.JunctionOn
#print OmissionBalancedZ.ExcludesHoleBudgetZ
#print Res118.BlockValid
#print Res118.ValidUnitRow
#print Res118.ResSliceExcludes
#print Res118.lsupp
#print Res118.F
#print Res118.Lo
#print Res118.InLo
#print Res118.loProfile
#print OmissionResidual32Transfer.holesOf
#print ErdosSzekeres.Omission.Configuration.residualOccupied
#print OmissionResidual32Bridge2650.support2650
#print OmissionResidual32Bridge2650.demand2650

/-! ## 6. Where the statement constants come from, and what fixes the statements' meaning -/
#eval IO.println "=== ORIGIN"
#eval RVTool.origin [``ErdosSzekeres.ForcesConvexNGon, ``ErdosSzekeres.GeneralPosition, ``ErdosSzekeres.HasConvexNGon,
  ``ErdosSzekeres.ConvexPosition, ``ErdosSzekeres.orient, ``ErdosSzekeres.Omission.Configuration,
  ``ErdosSzekeres.Omission.Configuration.HasCap, ``OmissionZRow.N66Bound, ``ErdosSzekeres.Omission.Partition.ResidualBound,
  ``OmissionBalancedZ.ExcludesHoleBudgetZ, ``Res118.BlockValid, ``Res118.ResSliceExcludes, ``Res118.F, ``Res118.rowsP,
  ``OmissionResidual32Bridge2650.support2650, ``OmissionResidual32Transfer.holesOf,
  ``ErdosSzekeres.Omission.Configuration.residualOccupied, ``E304Z.Final.excludes_67, ``E304Z.root,
  ``FV4A.forces_304_of_slices_rows_n66, ``Res118.forces_304_of_slices, ``ErdosSzekeres.not_forcesConvexNGon_64_8]
#eval IO.println "=== STMTDEPS"
#eval RVTool.stmtDeps "final304" [``E304Z.Final.forces_304_of_n66_res]
#eval RVTool.stmtDeps "combined" [``FV4A.forces_304_of_slices_rows_n66]
#eval RVTool.stmtDeps "excludes67" [``E304Z.Final.excludes_67]

/-! ## 7. Literal data in the hypotheses, decoded from the kernel terms -/
#eval IO.println "=== DATA"
#eval RVTool.dumpNatList ``Res118.fIndices
#eval RVTool.dumpNatList ``Res118.loIndices
#eval RVTool.dumpRows ``Res118.rowsP
#eval RVTool.dumpRows ``Res118.rowsQ
#eval RVTool.dumpRows ``Res118.rowsU
#eval RVTool.dumpRows ``Res118.rowsA

/-! ## 8. Every module of the environment with its direct imports (closures are computed outside Lean) -/
#eval IO.println "=== IMPORTS"
open Lean in
#eval show CoreM Unit from do
  let env ← getEnv
  let names := env.header.moduleNames
  let datas := env.header.moduleData
  IO.println s!"RV-NMODULES {names.size} {datas.size}"
  for (n, d) in names.zip datas do
    let imps := String.intercalate " " (d.imports.toList.map (fun imp => imp.module.toString))
    IO.println s!"RV-IMP {n} :: {imps}"
#eval IO.println "=== END"

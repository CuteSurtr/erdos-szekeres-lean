import Mathlib.Analysis.Convex.Caratheodory
import Mathlib.Data.Fintype.Pi
import Mathlib.Tactic.Ring
import Mathlib.Data.Finset.Powerset
import Mathlib.Data.Real.Basic
import Init
import Mathlib.Tactic.NormNum
import Mathlib.Order.Basic
import Mathlib.Data.List.Triplewise
import Mathlib.Tactic.FinCases
import Mathlib.Data.Finset.Sort
import Mathlib.Combinatorics.Enumerative.DoubleCounting
import Mathlib.LinearAlgebra.FiniteDimensional.Basic
import Mathlib.Tactic.Ring.RingNF
import Mathlib.Tactic.Linarith
import Std.Tactic
import Mathlib.Data.Finset.Lattice.Fold
import Mathlib.Analysis.Convex.Combination
import Mathlib.Data.Nat.Choose.Bounds
import Mathlib.Data.List.Basic
import Mathlib.Analysis.Convex.Hull
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.AffineSpace.FiniteDimensional
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Order.Synonym
import Mathlib.Data.Rat.Cast.Order
import Mathlib.Analysis.Convex.Independent
import Mathlib.Data.List.OfFn
import Mathlib.Data.Finset.Max
import Mathlib.Data.Finset.Card
import Mathlib.Data.List.Sublists
import Mathlib.Tactic.FieldSimp
import Mathlib.Data.Real.Sqrt
import Mathlib.Algebra.Algebra.Defs
import Std
import Mathlib.Data.List.GetD
import Mathlib.Data.List.MinMax
import Mathlib.Data.List.Sort
import Mathlib.Data.Finset.Image
import Mathlib.Tactic
import Mathlib.Data.List.Chain

/-! Kernel replay of the repository constants in the proof footprint of MirrorMain's 16 main theorems.
This file imports only library modules (Lean core, Batteries, Mathlib, ...), never a repository module. It reads
the repository's prebuilt .olean files with `readModuleData` (no import), takes the dependency closure of the
repository constants that MirrorMain.lean references directly, and sends every one of them to the kernel with
`Lean.Environment.replay` (the mechanism behind lean4checker). Written by mirrorM/lean_review. -/

open Lean Elab Command in
elab "#replay_repo " ids:ident* : command => do
  let env ← getEnv
  let isRepo (m : Name) : Bool := m.toString.startsWith "ErdosSzekeres"
  let preloaded := env.allImportedModuleNames.filter isRepo
  if !preloaded.isEmpty then throwError "repository modules already imported: {preloaded}"
  -- 1. module data of the repository module closure of MirrorMain's two imports
  let mut todo : Array Name := #[`ErdosSzekeres.Omission.BaekGeometry, `ErdosSzekeres.ConvexCycleCuts]
  let mut seen : NameSet := {}
  let mut allNew : Std.HashMap Name ConstantInfo := {}
  let mut nMods := 0
  while !todo.isEmpty do
    let m := todo.back!
    todo := todo.pop
    if seen.contains m then continue
    seen := seen.insert m
    let f ← findOLean m
    let (md, _) ← readModuleData f
    nMods := nMods + 1
    for ci in md.constants do
      allNew := allNew.insert ci.name ci
    for imp in md.imports do
      if isRepo imp.module then todo := todo.push imp.module
  -- 2. dependency closure of the roots; library constants must already be in the environment
  let mut visited : NameSet := {}
  let mut stack : Array Name := ids.map (·.getId)
  let mut sel : Std.HashMap Name ConstantInfo := {}
  let mut missing : Array Name := #[]
  while !stack.isEmpty do
    let n := stack.back!
    stack := stack.pop
    if visited.contains n then continue
    visited := visited.insert n
    match allNew[n]? with
    | some ci =>
      sel := sel.insert n ci
      let mut deps : Array Name := ci.type.getUsedConstants
      match ci with
      | .defnInfo v => deps := deps ++ v.value.getUsedConstants
      | .thmInfo v => deps := deps ++ v.value.getUsedConstants
      | .opaqueInfo v => deps := deps ++ v.value.getUsedConstants
      | .inductInfo v => deps := deps ++ v.ctors.toArray ++ v.all.toArray
      | .ctorInfo v => deps := deps.push v.induct
      | .recInfo v => deps := deps ++ v.all.toArray
      | _ => pure ()
      stack := stack ++ deps
    | none =>
      if !env.contains n then missing := missing.push n
  if !missing.isEmpty then
    throwError "constants neither in repository modules nor in the library environment: {missing}"
  let nUnsafe : Nat := sel.fold (fun (k : Nat) _ ci => if ci.isUnsafe || ci.isPartial then k + 1 else k) (0 : Nat)
  let nAx : Nat := sel.fold (fun (k : Nat) _ ci => match ci with | .axiomInfo _ => k + 1 | _ => k) (0 : Nat)
  logInfo m!"loaded {nMods} repository modules ({allNew.size} constants); replaying {sel.size} footprint constants ({nUnsafe} unsafe/partial, {nAx} axioms)"
  -- 3. kernel replay
  let t0 ← IO.monoMsNow
  let env' ← Lean.Environment.replay sel env
  let t1 ← IO.monoMsNow
  -- 4. every replayed constant must now be in the kernel environment, with the stored type
  let mut bad : Array Name := #[]
  for (n, ci) in sel.toList do
    match env'.find? n with
    | some c' => if !(c'.type == ci.type) then bad := bad.push n
    | none => bad := bad.push n
  if !bad.isEmpty then throwError "replayed constants missing or with changed type: {bad}"
  for id in ids do
    logInfo m!"{id.getId}: kernel-replayed"
  logInfo m!"kernel replay of all {sel.size} repository footprint constants succeeded in {t1 - t0} ms"

#replay_repo ErdosSzekeres.Omission.Configuration.xOrder Config.NGon ErdosSzekeres.Omission.Configuration.generalPosition ErdosSzekeres.ConvexPosition main ErdosSzekeres.Omission.Configuration.point ErdosSzekeres.Omission.ActualRanks.colorConfig Config.Gon Config.HasNCap ErdosSzekeres.Omission.BaekGeometry.geometric_capacity22 ErdosSzekeres.Omission.ListGeometry.hasCap_of_list ErdosSzekeres.Omission.Configuration.HasCap ErdosSzekeres.generalPosition_iff_orient_ne_zero Config.HasNGon ErdosSzekeres.Omission.BoundaryGeometry.Boundary.points ErdosSzekeres.Omission.Configuration.mk ErdosSzekeres.GeneralPosition ErdosSzekeres.HasConvexNGon.mono ErdosSzekeres.Omission.BaekGeometry.boundaryOfGon ErdosSzekeres.Omission.Configuration.cup ErdosSzekeres.Omission.BaekGeometry.boundaryOfGon_inside ErdosSzekeres.Omission.Configuration ErdosSzekeres.ConvexPosition.hasConvexNGon ErdosSzekeres.HasConvexNGon ErdosSzekeres.Point Config.Cup List.In ErdosSzekeres.orient._proof_1 ErdosSzekeres.Omission.BoundaryGeometry.boundary_polygon ErdosSzekeres.orient ErdosSzekeres.hasConvexNGon_of_positive_cycle ErdosSzekeres.convexPosition_iff Config.Cap 

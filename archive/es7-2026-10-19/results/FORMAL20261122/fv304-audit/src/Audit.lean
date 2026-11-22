-- fv304-audit (22 Nov 2026): closing audit of FV304. Imports E304Z.Final only (fv304-20261120/olean, read only),
-- re-prints the statements and axioms of the FV304 results, the definitions in their statements, and the module
-- list of the environment (= the import closure of E304Z.Final). Compiled without -o: no olean is written.
import E304Z.Final
set_option format.width 10000
set_option Elab.async false
#eval IO.println "=== CHECK"
#check E304Z.Final.excludes_67
#check E304Z.Final.forces_304_of_n66_res
#check E304Z.root
#eval IO.println "=== AXIOMS"
#print axioms E304Z.Final.excludes_67
#print axioms E304Z.Final.forces_304_of_n66_res
#print axioms E304Z.root
#print axioms E304Z.C260801.ex0
#print axioms E304Z.C325201.ex0
#eval IO.println "=== DEFS"
#print OmissionBalancedZ.ExcludesHoleBudgetZ
#print OmissionZRow.N66Bound
#print ErdosSzekeres.Omission.Partition.ResidualBound
#print ErdosSzekeres.ForcesConvexNGon
#eval IO.println "=== MODULES"
open Lean in
#eval show CoreM Unit from do
  for m in (← getEnv).header.moduleNames do
    IO.println s!"module {m}"
#eval IO.println "=== END"

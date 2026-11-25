-- fv302-audit (25 Nov 2026): closing audit of FV302. Imports E302ZZ.Final only (fv302-20261124/olean, read only),
-- re-prints the statements and axioms of the FV302 results, the definitions in their statements, and the module
-- list of the environment (= the import closure of E302ZZ.Final). Compiled without -o: no olean is written.
import E302ZZ.Final
set_option format.width 10000
set_option Elab.async false
#eval IO.println "=== CHECK"
#check E302ZZ.Final.excludes_69
#check E302ZZ.Final.forces_302_of_n54_res
#check E302ZZ.root
#check CompactChecker.BridgeZZs16.zzsn16_of_root
#eval IO.println "=== AXIOMS"
-- one transitive print (it covers excludes_69 and E302ZZ.root); Final.log printed both end theorems at compile time
#print axioms E302ZZ.Final.forces_302_of_n54_res
#eval IO.println "=== DEFS"
#print OmissionBalancedZZsN.ExcludesHoleBudgetZZsN
#print OmissionZRow.N66Bound
#print ErdosSzekeres.Omission.Partition.ResidualBound
#print ErdosSzekeres.ForcesConvexNGon
#eval IO.println "=== MODULES"
open Lean in
#eval show CoreM Unit from do
  for m in (← getEnv).header.moduleNames do
    IO.println s!"module {m}"
#eval IO.println "=== END"

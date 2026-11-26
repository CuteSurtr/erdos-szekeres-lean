-- combined part 3 audit (25 Nov 2026; PART3.md §5-6): imports Combined.ES302Final only (out/, after its compile) and
-- prints a mechanical statement check and the module list (= the import closure) for tools/audit3.py.
-- Compiled without -o: no olean is written. Not part of the pre-registered source; it re-reads it.
import Combined.ES302Final
set_option format.width 10000
#eval IO.println "=== CHECK"
#check Combined.es302_verdicts
#check Combined.es304_verdicts
#check Combined.residual_bound_118_verdicts

-- Fails the compile unless each end theorem has exactly 6 hypotheses and none of them mentions N66Bound, the hole
-- budget tree statement or a slice exclusion (so the tree and s35_20 are discharged, only verdict props remain).
open Lean Meta in
#eval show MetaM Unit from do
  for (n, k) in [(``Combined.es302_verdicts, 6), (``Combined.es304_verdicts, 6),
                 (``Combined.residual_bound_118_verdicts, 6)] do
    let ci ← getConstInfo n
    forallTelescope ci.type fun xs body => do
      unless xs.size == k do throwError "{n}: {xs.size} hypotheses, expected {k}"
      for x in xs do
        let cs := (← inferType x).getUsedConstants
        for bad in [``OmissionZRow.N66Bound, ``OmissionBalancedZZsN.ExcludesHoleBudgetZZsN, ``Res118.ResSliceExcludes] do
          if cs.contains bad then throwError "{n}: a hypothesis mentions {bad}"
      IO.println s!"STMT {n}: {xs.size} hypotheses, none mentions N66Bound, the tree or a slice; conclusion {← ppExpr body}"

#eval IO.println "=== MODULES"
open Lean in
#eval show CoreM Unit from do
  for m in (← getEnv).header.moduleNames do
    IO.println s!"module {m}"
#eval IO.println "=== END"

import LemmaZ
import BalancedBudgetsZ
import FixedStatesZ
import LemmaZStar
import BalancedBudgetsZZs
import BalancedBudgetsZZsN
import Composition305
import Composition304
import Composition303
import Composition306
set_option format.width 1000
#check OmissionBalancedZ.composition_304_z
#check OmissionBalancedZ.composition_305_z
#check OmissionBalancedZF.composition_304_zf
#check OmissionBalancedZF.composition_303_zf
#check OmissionBalancedZZsF.composition_303_zzsf
#check OmissionBalancedZZsF.composition_302_zzsf
#check OmissionBalancedZZsF.composition_301_zzsf
#check OmissionBalancedZZsF.composition_300_zzsf
#check OmissionBalancedZZsN.composition_302_n54
#check OmissionBalancedZZsN.composition_301_n53
#check composition_304
#check composition_303
#check composition_305
#check composition_306
#check OmissionZRow.z_row
#check OmissionZStarRow.zs_row
#check OmissionBalancedZZsN.z_row_of
#check OmissionBalancedZZsN.zs_row_of
#check OmissionBalancedZ.balanced_bound_of_hole_budget_z
#check OmissionBalancedZZsF.balanced_bound_of_hole_budget_zzsf
#check OmissionBalancedZZsN.balanced_bound_of_hole_budget_zzsn
#check OmissionZRow.Z_eq
#check OmissionZStarRow.Zs_eq
#check OmissionBalancedZ.feasible_holes_z
#check OmissionBalancedZF.feasible_holes_zf
#check OmissionBalancedZF.balanced_bound_of_hole_budget_zf
#check OmissionBalancedZZsN.zzsn_55_iff
#check avoiding_302
#check avoiding_303
#check avoiding_304
#check avoiding_305
#print axioms OmissionBalancedZ.composition_304_z
#print axioms OmissionBalancedZ.composition_305_z
#print axioms OmissionBalancedZF.composition_304_zf
#print axioms OmissionBalancedZF.composition_303_zf
#print axioms OmissionBalancedZZsF.composition_303_zzsf
#print axioms OmissionBalancedZZsF.composition_302_zzsf
#print axioms OmissionBalancedZZsF.composition_301_zzsf
#print axioms OmissionBalancedZZsF.composition_300_zzsf
#print axioms OmissionBalancedZZsN.composition_302_n54
#print axioms OmissionBalancedZZsN.composition_301_n53
#print axioms composition_304
#print axioms composition_303
#print axioms composition_305
#print axioms composition_306
#print axioms OmissionZRow.z_row
#print axioms OmissionZStarRow.zs_row
#print axioms OmissionBalancedZZsN.z_row_of
#print axioms OmissionBalancedZZsN.zs_row_of
#print axioms OmissionBalancedZ.balanced_bound_of_hole_budget_z
#print axioms OmissionBalancedZZsF.balanced_bound_of_hole_budget_zzsf
#print axioms OmissionBalancedZZsN.balanced_bound_of_hole_budget_zzsn
#print axioms OmissionZRow.Z_eq
#print axioms OmissionZStarRow.Zs_eq
#print axioms OmissionBalancedZ.feasible_holes_z
#print axioms OmissionBalancedZF.feasible_holes_zf
#print axioms OmissionBalancedZF.balanced_bound_of_hole_budget_zf
#print axioms OmissionBalancedZZsN.zzsn_55_iff
#print axioms avoiding_302
#print axioms avoiding_303
#print axioms avoiding_304
#print axioms avoiding_305
open Lean in
#eval show CoreM Unit from do
  for m in (← getEnv).header.moduleNames do
    IO.println s!"module {m}"

#!/bin/bash
# mutants.sh: the mutation tests of this package (each mutant must be KILLED).
W=/home/jay/research/data/formalize-20261122/sevenfold
T=$W/tools/mutant.sh
STD="EncBO.ModelO EncBO.SoundO EncBO.RulesO EncBO.AngO EncBO.SatisfiableO EncBO.Compose7"
GEO="Geo7.PolarData Geo7.ArcData Geo7.LayerLab Geo7.LayerBasic Geo7.Perturb Geo7.ModelOfLab Geo7.Main7"
{
echo "# mutants.sh $(date -Is)"
$T ruleA_at_m EncBO/ModelO.lean 'AltCCW (2 * m) psiLt (liftO hb a)|||AltCCW m psiLt (liftO hb a)' $STD
$T hbit_swapped EncBO/ModelO.lean 'if hb i then 0 else 1|||if hb i then 1 else 0' $STD
$T no_hb_zero EncBO/ModelO.lean '  hb_zero      : hb 0 = true
|||' $STD
$T ruleB_no_outer EncBO/ModelO.lean '→ b.1 ≤ a.1 → b.1 ≤ d.1 →
              chi a b d = true|||→
              chi a b d = true' $STD $GEO
$T nest_shifted EncBO/ModelO.lean 'chi (i, 0) (i, 1) (j, k) = true|||chi (i, 1) (i, 0) (j, k) = true' $STD
$T control_docstring_only_expect_SURVIVED EncBO/ModelO.lean 'lifted to `liftO hb a = (i, 2k + hbit hb i)`|||lifted to `liftO hb a = (i, 2k + hbit hb i)` ' $STD
$T hbP_wrong_threshold Geo7/ModelOfLab.lean 'decide (thP L η i < Real.pi / m)|||decide (thP L η i < 2 * Real.pi / m)' $GEO
$T perturb_all_layers_same Geo7/Perturb.lean '+ (a.1 : ℝ) * η)
|||+ η)
' $GEO
} 2>&1 | tee "$W/logs/mutants.log"

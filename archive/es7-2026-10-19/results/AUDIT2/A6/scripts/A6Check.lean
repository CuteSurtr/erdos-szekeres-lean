import V2L.FinalTree
open V2L
#check @V2L.mirrorExclusionLine_final
#print axioms V2L.mirrorExclusionLine_final
#print axioms V2L.treeOf_check
#check @V2L.treeOf_check
-- tree leaf counts as Lean evaluates them
#eval (caseTable.map fun p => (treeOf p.1).leaves.length).sum
#eval (caseTable.filter fun p => (treeOf p.1).leaves.isEmpty).length

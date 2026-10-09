import BalancedProof.Part00000
import Part00380

/- Actual production certificate chunks from both families in one Lean module.
This checks coexistence of the two catalogs and two successfully checked
subtrees. It does not import either full arithmetic root or prove ES(8) ≤ 317.
See docs/OMISSION_ASSEMBLY.md for the remaining full-root obligations. -/

#print axioms OmissionBalanced.code_correct
#print axioms OmissionBalanced.node0
#print axioms OmissionResidual.code_correct
#print axioms OmissionResidual.node1501

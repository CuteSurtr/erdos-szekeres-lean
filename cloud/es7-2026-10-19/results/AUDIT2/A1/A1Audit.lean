import V2L
-- AUDIT2 A1: statements and axioms of the final theorems, printed with full names.
set_option pp.fullNames true
set_option pp.proofs true
#check @V2L.mirrorExclusionLine_final
#check @V2L.axisInteriorLine_final
#check @V1L.hullVertexLine_of_leaves
#print Mir.MirrorExclusionLine
#print Mir.reflLine
#print ErdosSzekeres.GeneralPosition
#print ErdosSzekeres.ConvexPosition
#print ErdosSzekeres.HasConvexNGon
#print ErdosSzekeres.Point
#print ETV.DimacsSatisfiable
#print ETV.DimacsSat
#print Mir.cubeCnf
#print Mir.coverCheck
#print Mir.coverAux
#print Mir.restrict
#print Mir.Covers
#print Mir.CubeSat
#print Mir.LitSat
#print V2L.CTree.leaves
#print V2L.CTree.check
#print V2L.RootCertificate
#print V2L.UpCertificates
#print V2L.caseTable
#print V2L.treeOf
#print V2L.negClause
#print axioms V2L.mirrorExclusionLine_final
#print axioms V2L.axisInteriorLine_final
#print axioms V1L.hullVertexLine_of_leaves
#print axioms V2L.treeOf_check
#print axioms V1L.hullLeaves_coverCheck
#print axioms Mir.mirrorExclusionLine_of_unsat
#print axioms Mir.interiorTieBreak_holds

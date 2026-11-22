import V182Geo.End
import V182Ctl.WalkMut

/-! Reviewer audit (v182-lean, slot lrv3): the statements as elaborated, the definitions they unfold to, and the
axioms of every theorem on the path. Compiled once against oleans rebuilt from source in review/build. -/

open V182Geo V182Enc

-- the end theorems
#check @V182Geo.chiRainbow_eq_six
#check @V182Geo.chiRainbow_eq_six'
#check @V182Geo.not_rainbowColorable_five
#check @V182Geo.rainbowColorable_six
#check @V182Geo.pieces_shape

-- the statement's definitions
#print V182Geo.chiRainbow
#print V182Geo.RainbowColorable
#print V182Geo.IsRainbow
#print V182Geo.IsFourCycle
#print V182Geo.G
#print V182Geo.Adj
#print V182Geo.V

-- the hypothesis and the CNF objects it names
#print V182Geo.PieceVerdicts
#print V182Enc.pieces
#print V182Enc.splitSet
#print V182Enc.pieceText
#print V182Enc.pieceCube
#print V182Enc.starUnits
#print V182Enc.y1Star
#print V182Enc.y2Star
#print V182Enc.perms5
#print V182Enc.permsOf
#print V182Enc.baseCnf
#print V182Enc.nVars
#print V182Enc.lit
#print EncB.parseDimacs
#print EncB.parseDimacsChars
#print EncB.DimacsSatisfiable
#print EncB.DimacsSat
#print EncB.renderCube
#print EncB.cubeCnf
#print EncB.bodyR
#print EncB.headerR
#print EncB.cubeBodyR
#print EncB.pushClauseR

-- axioms
#print axioms V182Geo.chiRainbow_eq_six
#print axioms V182Geo.chiRainbow_eq_six'
#print axioms V182Geo.not_rainbowColorable_five
#print axioms V182Geo.rainbowColorable_six
#print axioms V182Geo.pieces_shape
#print axioms V182Geo.chiRainbow_eq_six_of
#print axioms V182Geo.normalize
#print axioms V182Geo.norm_finite
#print axioms V182Geo.exists_piece
#print axioms V182Geo.no_normal_colouring
#print axioms V182Geo.baseCnf_sat
#print axioms V182Geo.baseCnf_wf
#print axioms V182Geo.piece_unsat
#print axioms V182Geo.cyc_bridge
#print axioms V182Geo.conflict_ne
#print axioms V182Geo.col6_rainbow
#print axioms V182Geo.walk_all
#print axioms V182Geo.walk_spec
#print axioms V182Ctl.ctl_orig
#print axioms V182Ctl.ctl_mut
#print axioms EncB.parseDimacs_renderCube

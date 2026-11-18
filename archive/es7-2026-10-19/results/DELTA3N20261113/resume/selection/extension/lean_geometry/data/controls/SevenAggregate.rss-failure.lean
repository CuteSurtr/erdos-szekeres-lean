import SevenBlock00
import SevenBlock01
import SevenBlock02
import SevenBlock03
import SevenBlock04
import SevenBlock05
import SevenBlock06
import SevenBlock07
import SevenBlock08
import SevenBlock09
import SevenBlock10
import SevenBlock11
import SevenBlock12

set_option maxRecDepth 32768

namespace Delta3.Balanced15

def allSevenBlocks : List (List Index) :=
  sevenBlock00 ++ sevenBlock01 ++ sevenBlock02 ++ sevenBlock03 ++ sevenBlock04 ++ sevenBlock05 ++ sevenBlock06 ++ sevenBlock07 ++ sevenBlock08 ++ sevenBlock09 ++ sevenBlock10 ++ sevenBlock11 ++ sevenBlock12

theorem seven_cover : choose 7 indices = allSevenBlocks := by decide +kernel

theorem no_seven_sign_convex : (choose 7 indices).all (fun s => !signConvex s) = true := by
  rw [seven_cover]
  simp only [allSevenBlocks, List.all_append, no_seven_block_00, no_seven_block_01, no_seven_block_02, no_seven_block_03, no_seven_block_04, no_seven_block_05, no_seven_block_06, no_seven_block_07, no_seven_block_08, no_seven_block_09, no_seven_block_10, no_seven_block_11, no_seven_block_12, Bool.true_and]

#print axioms seven_cover
#print axioms no_seven_sign_convex

end Delta3.Balanced15

import SevenBlock06

set_option maxRecDepth 32768

namespace Delta3.Balanced15

theorem seven_cover_06 :
    ((choose 7 indices).drop 3072).take 512 = sevenBlock06 := by
  decide +kernel

#print axioms seven_cover_06

end Delta3.Balanced15

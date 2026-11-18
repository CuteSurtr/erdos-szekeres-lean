import SevenBlock00

set_option maxRecDepth 32768

namespace Delta3.Balanced15

theorem seven_cover_00 :
    ((choose 7 indices).drop 0).take 512 = sevenBlock00 := by
  decide +kernel

#print axioms seven_cover_00

end Delta3.Balanced15

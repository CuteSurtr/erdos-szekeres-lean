import SevenBlock01

set_option maxRecDepth 32768

namespace Delta3.Balanced15

theorem seven_cover_01 :
    ((choose 7 indices).drop 512).take 512 = sevenBlock01 := by
  decide +kernel

#print axioms seven_cover_01

end Delta3.Balanced15

import SevenBlock04

set_option maxRecDepth 32768

namespace Delta3.Balanced15

theorem seven_cover_04 :
    ((choose 7 indices).drop 2048).take 512 = sevenBlock04 := by
  decide +kernel

#print axioms seven_cover_04

end Delta3.Balanced15

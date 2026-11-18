import SevenBlock07

set_option maxRecDepth 32768

namespace Delta3.Balanced15

theorem seven_cover_07 :
    ((choose 7 indices).drop 3584).take 512 = sevenBlock07 := by
  decide +kernel

#print axioms seven_cover_07

end Delta3.Balanced15

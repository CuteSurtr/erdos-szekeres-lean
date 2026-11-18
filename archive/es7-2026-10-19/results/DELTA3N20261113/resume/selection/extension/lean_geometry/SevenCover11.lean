import SevenBlock11

set_option maxRecDepth 32768

namespace Delta3.Balanced15

theorem seven_cover_11 :
    ((choose 7 indices).drop 5632).take 512 = sevenBlock11 := by
  decide +kernel

#print axioms seven_cover_11

end Delta3.Balanced15

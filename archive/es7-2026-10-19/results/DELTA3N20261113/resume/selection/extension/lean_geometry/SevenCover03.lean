import SevenBlock03

set_option maxRecDepth 32768

namespace Delta3.Balanced15

theorem seven_cover_03 :
    ((choose 7 indices).drop 1536).take 512 = sevenBlock03 := by
  decide +kernel

#print axioms seven_cover_03

end Delta3.Balanced15

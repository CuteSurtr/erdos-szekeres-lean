import ErdosSzekeres.Omission.CoupledLrat
import ErdosSzekeres.Omission.CoupledSemantics

namespace ErdosSzekeres.Omission.CoupledCoreFifth
open Coupled
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

lrat_raw cnf_refutation
  (include_str "../../experiments/omission-coupled-fifth-2026-10-10/core13.cnf")
  (include_str "../../experiments/omission-coupled-fifth-2026-10-10/core13.lrat")

def support : List (Fin 154) := [16, 25, 30, 43, 50, 53, 62, 68, 77, 79, 91, 101, 110]

def states : Fin 13 → Fin 154 := support.get

def atoms : List (Atom 13) := [
  .before 0 1,
  .before 0 2,
  .before 0 4,
  .before 0 6,
  .before 0 7,
  .before 0 9,
  .before 1 2,
  .before 1 3,
  .before 1 4,
  .before 1 5,
  .before 1 6,
  .before 1 7,
  .before 1 8,
  .before 1 9,
  .capGe 1 9 2,
  .before 1 10,
  .before 2 4,
  .cupGe 2 4 2,
  .before 2 6,
  .cupGe 2 6 2,
  .before 2 7,
  .before 2 8,
  .before 2 9,
  .cupGe 2 9 2,
  .before 2 12,
  .before 3 5,
  .cupGe 3 5 2,
  .before 3 10,
  .before 4 6,
  .before 4 7,
  .before 4 8,
  .before 4 9,
  .cupGe 4 9 3,
  .before 4 12,
  .before 5 8,
  .cupGe 5 8 3,
  .before 5 9,
  .before 5 10,
  .before 6 7,
  .before 6 8,
  .before 6 9,
  .cupGe 6 9 3,
  .before 6 12,
  .before 7 8,
  .before 7 9,
  .before 7 12,
  .before 8 9,
  .capGe 8 9 2,
  .cupGe 8 9 4,
  .cupGe 8 9 5,
  .cupGe 8 9 6,
  .before 8 10,
  .before 8 12,
  .before 9 10,
  .capGe 9 10 3,
  .before 9 11,
  .capGe 9 11 3,
  .capGe 9 11 4,
  .cupGe 9 11 2,
  .cupGe 9 11 3,
  .cupGe 9 11 4,
  .cupGe 9 11 5,
  .cupGe 9 11 6,
  .before 9 12,
  .capGe 9 12 3,
  .capGe 9 12 4,
  .cupGe 9 12 2,
  .cupGe 9 12 3,
  .cupGe 9 12 4,
  .cupGe 9 12 5,
  .cupGe 9 12 6,
  .before 10 11,
  .capGe 10 11 4,
  .before 11 12,
  .positive 0 1 2,
  .positive 0 1 4,
  .positive 0 1 6,
  .positive 0 1 7,
  .positive 0 1 8,
  .positive 0 1 9,
  .positive 0 1 12,
  .positive 0 2 4,
  .positive 0 2 6,
  .positive 0 2 7,
  .positive 0 2 8,
  .positive 0 2 9,
  .positive 0 2 12,
  .positive 0 4 6,
  .positive 0 4 7,
  .positive 0 4 8,
  .positive 0 4 9,
  .positive 0 4 12,
  .positive 0 6 7,
  .positive 0 6 8,
  .positive 0 6 9,
  .positive 0 6 12,
  .positive 0 7 8,
  .positive 0 7 9,
  .positive 0 7 12,
  .positive 0 8 9,
  .positive 0 9 12,
  .positive 1 2 4,
  .positive 1 2 6,
  .positive 1 2 7,
  .positive 1 2 8,
  .positive 1 2 9,
  .positive 1 2 12,
  .positive 1 3 5,
  .positive 1 3 8,
  .positive 1 3 9,
  .positive 1 3 10,
  .positive 1 3 11,
  .positive 1 3 12,
  .positive 1 4 6,
  .positive 1 4 7,
  .positive 1 4 8,
  .positive 1 4 9,
  .positive 1 4 12,
  .positive 1 5 8,
  .positive 1 5 9,
  .positive 1 5 10,
  .positive 1 5 11,
  .positive 1 5 12,
  .positive 1 6 7,
  .positive 1 6 8,
  .positive 1 6 9,
  .positive 1 6 12,
  .positive 1 7 8,
  .positive 1 7 9,
  .positive 1 7 12,
  .positive 1 8 9,
  .positive 1 8 10,
  .positive 1 8 11,
  .positive 1 8 12,
  .positive 1 9 10,
  .positive 1 9 11,
  .positive 1 9 12,
  .positive 1 10 11,
  .positive 1 10 12,
  .positive 1 11 12,
  .positive 2 4 6,
  .positive 2 4 7,
  .positive 2 4 8,
  .positive 2 4 9,
  .positive 2 4 12,
  .positive 2 6 7,
  .positive 2 6 8,
  .positive 2 6 9,
  .positive 2 6 12,
  .positive 2 7 8,
  .positive 2 7 9,
  .positive 2 7 12,
  .positive 2 8 9,
  .positive 2 9 12,
  .positive 3 5 8,
  .positive 3 5 9,
  .positive 3 5 10,
  .positive 3 5 11,
  .positive 3 5 12,
  .positive 3 8 9,
  .positive 3 8 10,
  .positive 3 8 11,
  .positive 3 8 12,
  .positive 3 9 10,
  .positive 3 9 11,
  .positive 3 9 12,
  .positive 3 10 11,
  .positive 3 10 12,
  .positive 3 11 12,
  .positive 4 6 7,
  .positive 4 6 8,
  .positive 4 6 9,
  .positive 4 6 12,
  .positive 4 7 8,
  .positive 4 7 9,
  .positive 4 7 12,
  .positive 4 8 9,
  .positive 4 9 12,
  .positive 5 8 9,
  .positive 5 8 10,
  .positive 5 8 11,
  .positive 5 8 12,
  .positive 5 9 10,
  .positive 5 9 11,
  .positive 5 9 12,
  .positive 5 10 11,
  .positive 5 10 12,
  .positive 5 11 12,
  .positive 6 7 8,
  .positive 6 7 9,
  .positive 6 7 12,
  .positive 6 8 9,
  .positive 6 8 12,
  .positive 6 9 12,
  .positive 7 8 9,
  .positive 7 8 12,
  .positive 7 9 12,
  .positive 8 9 10,
  .positive 8 9 11,
  .positive 8 9 12,
  .positive 8 10 11,
  .positive 8 10 12,
  .positive 8 11 12,
  .positive 9 10 11,
  .positive 9 10 12,
  .positive 9 11 12,
  .positive 10 11 12,
  .convex 0 1 2 4,
  .convex 0 1 2 6,
  .convex 0 1 2 7,
  .convex 0 1 2 8,
  .convex 0 1 2 9,
  .convex 0 1 2 12,
  .convex 0 1 4 6,
  .convex 0 1 4 7,
  .convex 0 1 4 8,
  .convex 0 1 4 9,
  .convex 0 1 4 12,
  .convex 0 1 6 7,
  .convex 0 1 6 8,
  .convex 0 1 6 9,
  .convex 0 1 6 12,
  .convex 0 1 7 8,
  .convex 0 1 7 9,
  .convex 0 1 7 12,
  .convex 0 1 8 9,
  .convex 0 1 9 12,
  .convex 0 2 4 6,
  .convex 0 2 4 7,
  .convex 0 2 4 8,
  .convex 0 2 4 9,
  .convex 0 2 4 12,
  .convex 0 2 6 7,
  .convex 0 2 6 8,
  .convex 0 2 6 9,
  .convex 0 2 6 12,
  .convex 0 2 7 8,
  .convex 0 2 7 9,
  .convex 0 2 7 12,
  .convex 0 2 8 9,
  .convex 0 2 9 12,
  .convex 0 4 6 7,
  .convex 0 4 6 8,
  .convex 0 4 6 9,
  .convex 0 4 6 12,
  .convex 0 4 7 8,
  .convex 0 4 7 9,
  .convex 0 4 7 12,
  .convex 0 4 8 9,
  .convex 0 4 9 12,
  .convex 0 6 7 8,
  .convex 0 6 7 9,
  .convex 0 6 7 12,
  .convex 0 6 8 9,
  .convex 0 6 9 12,
  .convex 0 7 8 9,
  .convex 0 7 9 12,
  .convex 1 2 4 6,
  .convex 1 2 4 7,
  .convex 1 2 4 8,
  .convex 1 2 4 9,
  .convex 1 2 4 12,
  .convex 1 2 6 7,
  .convex 1 2 6 8,
  .convex 1 2 6 9,
  .convex 1 2 6 12,
  .convex 1 2 7 8,
  .convex 1 2 7 9,
  .convex 1 2 7 12,
  .convex 1 2 8 9,
  .convex 1 2 9 12,
  .convex 1 3 5 8,
  .convex 1 3 5 9,
  .convex 1 3 5 10,
  .convex 1 3 5 11,
  .convex 1 3 5 12,
  .convex 1 3 8 9,
  .convex 1 3 8 10,
  .convex 1 3 8 11,
  .convex 1 3 8 12,
  .convex 1 3 9 10,
  .convex 1 3 9 11,
  .convex 1 3 9 12,
  .convex 1 3 10 11,
  .convex 1 3 10 12,
  .convex 1 3 11 12,
  .convex 1 4 6 7,
  .convex 1 4 6 8,
  .convex 1 4 6 9,
  .convex 1 4 6 12,
  .convex 1 4 7 8,
  .convex 1 4 7 9,
  .convex 1 4 7 12,
  .convex 1 4 8 9,
  .convex 1 4 9 12,
  .convex 1 5 8 9,
  .convex 1 5 8 10,
  .convex 1 5 8 11,
  .convex 1 5 8 12,
  .convex 1 5 9 10,
  .convex 1 5 9 11,
  .convex 1 5 9 12,
  .convex 1 5 10 11,
  .convex 1 5 10 12,
  .convex 1 5 11 12,
  .convex 1 6 7 8,
  .convex 1 6 7 9,
  .convex 1 6 7 12,
  .convex 1 6 8 9,
  .convex 1 6 9 12,
  .convex 1 7 8 9,
  .convex 1 7 9 12,
  .convex 1 8 9 10,
  .convex 1 8 9 11,
  .convex 1 8 9 12,
  .convex 1 8 10 11,
  .convex 1 8 10 12,
  .convex 1 8 11 12,
  .convex 1 9 10 11,
  .convex 1 9 10 12,
  .convex 1 9 11 12,
  .convex 1 10 11 12,
  .convex 2 4 6 7,
  .convex 2 4 6 8,
  .convex 2 4 6 9,
  .convex 2 4 6 12,
  .convex 2 4 7 8,
  .convex 2 4 7 9,
  .convex 2 4 7 12,
  .convex 2 4 8 9,
  .convex 2 4 9 12,
  .convex 2 6 7 8,
  .convex 2 6 7 9,
  .convex 2 6 7 12,
  .convex 2 6 8 9,
  .convex 2 6 9 12,
  .convex 2 7 8 9,
  .convex 2 7 9 12,
  .convex 3 5 8 9,
  .convex 3 5 8 10,
  .convex 3 5 8 11,
  .convex 3 5 8 12,
  .convex 3 5 9 10,
  .convex 3 5 9 11,
  .convex 3 5 9 12,
  .convex 3 5 10 11,
  .convex 3 5 10 12,
  .convex 3 5 11 12,
  .convex 3 8 9 10,
  .convex 3 8 9 11,
  .convex 3 8 9 12,
  .convex 3 8 10 11,
  .convex 3 8 10 12,
  .convex 3 8 11 12,
  .convex 3 9 10 11,
  .convex 3 9 10 12,
  .convex 3 9 11 12,
  .convex 3 10 11 12,
  .convex 4 6 7 8,
  .convex 4 6 7 9,
  .convex 4 6 7 12,
  .convex 4 6 8 9,
  .convex 4 6 9 12,
  .convex 4 7 8 9,
  .convex 4 7 9 12,
  .convex 5 8 9 10,
  .convex 5 8 9 11,
  .convex 5 8 9 12,
  .convex 5 8 10 11,
  .convex 5 8 10 12,
  .convex 5 8 11 12,
  .convex 5 9 10 11,
  .convex 5 9 10 12,
  .convex 5 9 11 12,
  .convex 5 10 11 12,
  .convex 6 7 8 9,
  .convex 6 7 9 12,
  .convex 7 8 9 12,
  .convex 8 9 10 11,
  .convex 8 9 10 12,
  .convex 8 9 11 12,
  .convex 8 10 11 12,
  .convex 9 10 11 12]

private def clause000 : Sat.Clause := [.pos 0]
private def clause001 : Sat.Clause := [.pos 1]
private def clause002 : Sat.Clause := [.pos 2]
private def clause003 : Sat.Clause := [.pos 3]
private def clause004 : Sat.Clause := [.pos 4]
private def clause005 : Sat.Clause := [.pos 5]
private def clause006 : Sat.Clause := [.pos 7]
private def clause007 : Sat.Clause := [.pos 9]
private def clause008 : Sat.Clause := [.pos 11]
private def clause009 : Sat.Clause := [.pos 12]
private def clause010 : Sat.Clause := [.pos 13]
private def clause011 : Sat.Clause := [.pos 15]
private def clause012 : Sat.Clause := [.pos 16]
private def clause013 : Sat.Clause := [.pos 18]
private def clause014 : Sat.Clause := [.pos 21]
private def clause015 : Sat.Clause := [.pos 24]
private def clause016 : Sat.Clause := [.pos 25]
private def clause017 : Sat.Clause := [.pos 28]
private def clause018 : Sat.Clause := [.pos 30]
private def clause019 : Sat.Clause := [.pos 33]
private def clause020 : Sat.Clause := [.pos 34]
private def clause021 : Sat.Clause := [.pos 39]
private def clause022 : Sat.Clause := [.pos 42]
private def clause023 : Sat.Clause := [.pos 44]
private def clause024 : Sat.Clause := [.pos 45]
private def clause025 : Sat.Clause := [.neg 46, .pos 47, .neg 48, .pos 49]
private def clause026 : Sat.Clause := [.neg 46, .pos 47, .neg 49, .pos 50]
private def clause027 : Sat.Clause := [.neg 46, .pos 47, .neg 50]
private def clause028 : Sat.Clause := [.pos 52]
private def clause029 : Sat.Clause := [.neg 55, .neg 56, .pos 57, .neg 58, .pos 59]
private def clause030 : Sat.Clause := [.neg 55, .neg 56, .pos 57, .neg 59, .pos 60]
private def clause031 : Sat.Clause := [.neg 55, .neg 56, .pos 57, .neg 60, .pos 61]
private def clause032 : Sat.Clause := [.neg 55, .neg 56, .pos 57, .neg 61, .pos 62]
private def clause033 : Sat.Clause := [.neg 55, .neg 56, .pos 57, .neg 62]
private def clause034 : Sat.Clause := [.pos 55]
private def clause035 : Sat.Clause := [.neg 63, .neg 64, .pos 65, .neg 66, .pos 67]
private def clause036 : Sat.Clause := [.neg 63, .neg 64, .pos 65, .neg 67, .pos 68]
private def clause037 : Sat.Clause := [.neg 63, .neg 64, .pos 65, .neg 68, .pos 69]
private def clause038 : Sat.Clause := [.neg 63, .neg 64, .pos 65, .neg 69, .pos 70]
private def clause039 : Sat.Clause := [.neg 63, .neg 64, .pos 65, .neg 70]
private def clause040 : Sat.Clause := [.neg 63, .neg 65, .neg 66, .pos 67]
private def clause041 : Sat.Clause := [.neg 63, .neg 65, .neg 67, .pos 68]
private def clause042 : Sat.Clause := [.neg 63, .neg 65, .neg 68, .pos 69]
private def clause043 : Sat.Clause := [.neg 63, .neg 65, .neg 69, .pos 70]
private def clause044 : Sat.Clause := [.neg 63, .neg 65, .neg 70]
private def clause045 : Sat.Clause := [.pos 63]
private def clause046 : Sat.Clause := [.pos 71]
private def clause047 : Sat.Clause := [.pos 73]
private def clause048 : Sat.Clause := [.neg 0, .neg 13, .pos 14, .pos 79]
private def clause049 : Sat.Clause := [.neg 1, .neg 16, .pos 17, .neg 81]
private def clause050 : Sat.Clause := [.neg 1, .neg 18, .pos 19, .neg 82]
private def clause051 : Sat.Clause := [.neg 1, .neg 22, .pos 23, .neg 85]
private def clause052 : Sat.Clause := [.neg 5, .neg 63, .pos 66, .neg 100]
private def clause053 : Sat.Clause := [.neg 7, .neg 25, .pos 26, .neg 107]
private def clause054 : Sat.Clause := [.pos 8, .neg 11, .pos 29]
private def clause055 : Sat.Clause := [.pos 10, .neg 11, .pos 38]
private def clause056 : Sat.Clause := [.neg 13, .neg 55, .pos 58, .neg 135]
private def clause057 : Sat.Clause := [.neg 13, .neg 14, .neg 63, .pos 64, .pos 136]
private def clause058 : Sat.Clause := [.neg 13, .neg 63, .pos 66, .neg 136]
private def clause059 : Sat.Clause := [.neg 16, .pos 20, .neg 29]
private def clause060 : Sat.Clause := [.neg 16, .neg 17, .neg 31, .pos 32, .neg 143]
private def clause061 : Sat.Clause := [.neg 18, .neg 19, .neg 40, .pos 41, .neg 147]
private def clause062 : Sat.Clause := [.neg 21, .pos 22, .neg 46]
private def clause063 : Sat.Clause := [.neg 22, .neg 23, .neg 63, .pos 67, .neg 153]
private def clause064 : Sat.Clause := [.neg 25, .neg 26, .neg 34, .pos 35, .neg 154]
private def clause065 : Sat.Clause := [.neg 28, .pos 29, .neg 38]
private def clause066 : Sat.Clause := [.neg 30, .pos 31, .neg 46]
private def clause067 : Sat.Clause := [.neg 31, .neg 32, .neg 63, .pos 68, .neg 177]
private def clause068 : Sat.Clause := [.neg 34, .neg 35, .neg 46, .pos 48, .neg 178]
private def clause069 : Sat.Clause := [.neg 39, .pos 40, .neg 46]
private def clause070 : Sat.Clause := [.neg 40, .neg 41, .neg 63, .pos 68, .neg 193]
private def clause071 : Sat.Clause := [.pos 43, .neg 44, .pos 46]
private def clause072 : Sat.Clause := [.neg 44, .neg 63, .pos 66, .neg 196]
private def clause073 : Sat.Clause := [.neg 46, .neg 47, .neg 53, .pos 54, .pos 197]
private def clause074 : Sat.Clause := [.neg 46, .neg 47, .neg 55, .pos 56, .pos 198]
private def clause075 : Sat.Clause := [.neg 46, .neg 47, .neg 63, .pos 64, .pos 199]
private def clause076 : Sat.Clause := [.neg 53, .neg 54, .neg 71, .pos 72, .pos 203]
private def clause077 : Sat.Clause := [.neg 55, .neg 57, .neg 73, .pos 205]
private def clause078 : Sat.Clause := [.neg 71, .neg 72, .neg 73, .pos 206]
private def clause079 : Sat.Clause := [.neg 74]
private def clause080 : Sat.Clause := [.neg 75]
private def clause081 : Sat.Clause := [.neg 76]
private def clause082 : Sat.Clause := [.neg 77]
private def clause083 : Sat.Clause := [.neg 78]
private def clause084 : Sat.Clause := [.neg 79]
private def clause085 : Sat.Clause := [.pos 81]
private def clause086 : Sat.Clause := [.pos 82]
private def clause087 : Sat.Clause := [.pos 83]
private def clause088 : Sat.Clause := [.pos 84]
private def clause089 : Sat.Clause := [.pos 85]
private def clause090 : Sat.Clause := [.pos 86]
private def clause091 : Sat.Clause := [.pos 87]
private def clause092 : Sat.Clause := [.pos 88]
private def clause093 : Sat.Clause := [.pos 89]
private def clause094 : Sat.Clause := [.pos 90]
private def clause095 : Sat.Clause := [.pos 91]
private def clause096 : Sat.Clause := [.pos 92]
private def clause097 : Sat.Clause := [.pos 93]
private def clause098 : Sat.Clause := [.pos 94]
private def clause099 : Sat.Clause := [.pos 95]
private def clause100 : Sat.Clause := [.neg 97]
private def clause101 : Sat.Clause := [.pos 101]
private def clause102 : Sat.Clause := [.pos 102]
private def clause103 : Sat.Clause := [.pos 103]
private def clause104 : Sat.Clause := [.pos 104]
private def clause105 : Sat.Clause := [.pos 105]
private def clause106 : Sat.Clause := [.pos 107]
private def clause107 : Sat.Clause := [.pos 108]
private def clause108 : Sat.Clause := [.pos 109]
private def clause109 : Sat.Clause := [.pos 110]
private def clause110 : Sat.Clause := [.pos 111]
private def clause111 : Sat.Clause := [.pos 112]
private def clause112 : Sat.Clause := [.pos 113]
private def clause113 : Sat.Clause := [.pos 114]
private def clause114 : Sat.Clause := [.pos 115]
private def clause115 : Sat.Clause := [.pos 116]
private def clause116 : Sat.Clause := [.pos 118]
private def clause117 : Sat.Clause := [.pos 119]
private def clause118 : Sat.Clause := [.pos 120]
private def clause119 : Sat.Clause := [.pos 121]
private def clause120 : Sat.Clause := [.pos 122]
private def clause121 : Sat.Clause := [.pos 123]
private def clause122 : Sat.Clause := [.pos 124]
private def clause123 : Sat.Clause := [.pos 125]
private def clause124 : Sat.Clause := [.neg 127]
private def clause125 : Sat.Clause := [.neg 128]
private def clause126 : Sat.Clause := [.pos 130]
private def clause127 : Sat.Clause := [.pos 131]
private def clause128 : Sat.Clause := [.pos 132]
private def clause129 : Sat.Clause := [.pos 133]
private def clause130 : Sat.Clause := [.pos 134]
private def clause131 : Sat.Clause := [.pos 135]
private def clause132 : Sat.Clause := [.neg 137]
private def clause133 : Sat.Clause := [.neg 138]
private def clause134 : Sat.Clause := [.neg 139]
private def clause135 : Sat.Clause := [.pos 140]
private def clause136 : Sat.Clause := [.pos 141]
private def clause137 : Sat.Clause := [.pos 142]
private def clause138 : Sat.Clause := [.pos 143]
private def clause139 : Sat.Clause := [.pos 144]
private def clause140 : Sat.Clause := [.pos 145]
private def clause141 : Sat.Clause := [.pos 146]
private def clause142 : Sat.Clause := [.pos 147]
private def clause143 : Sat.Clause := [.pos 148]
private def clause144 : Sat.Clause := [.neg 150]
private def clause145 : Sat.Clause := [.pos 154]
private def clause146 : Sat.Clause := [.pos 155]
private def clause147 : Sat.Clause := [.pos 156]
private def clause148 : Sat.Clause := [.pos 157]
private def clause149 : Sat.Clause := [.pos 158]
private def clause150 : Sat.Clause := [.pos 159]
private def clause151 : Sat.Clause := [.pos 160]
private def clause152 : Sat.Clause := [.pos 161]
private def clause153 : Sat.Clause := [.pos 162]
private def clause154 : Sat.Clause := [.neg 166]
private def clause155 : Sat.Clause := [.neg 167]
private def clause156 : Sat.Clause := [.neg 168]
private def clause157 : Sat.Clause := [.pos 169]
private def clause158 : Sat.Clause := [.pos 170]
private def clause159 : Sat.Clause := [.pos 171]
private def clause160 : Sat.Clause := [.pos 172]
private def clause161 : Sat.Clause := [.neg 174]
private def clause162 : Sat.Clause := [.pos 178]
private def clause163 : Sat.Clause := [.pos 179]
private def clause164 : Sat.Clause := [.pos 180]
private def clause165 : Sat.Clause := [.pos 181]
private def clause166 : Sat.Clause := [.neg 185]
private def clause167 : Sat.Clause := [.neg 186]
private def clause168 : Sat.Clause := [.neg 187]
private def clause169 : Sat.Clause := [.neg 189]
private def clause170 : Sat.Clause := [.pos 194]
private def clause171 : Sat.Clause := [.neg 200]
private def clause172 : Sat.Clause := [.neg 201]
private def clause173 : Sat.Clause := [.neg 202]
private def clause174 : Sat.Clause := [.neg 203]
private def clause175 : Sat.Clause := [.neg 205]
private def clause176 : Sat.Clause := [.neg 206]
private def clause177 : Sat.Clause := [.pos 74, .pos 75, .neg 81, .neg 101, .pos 207]
private def clause178 : Sat.Clause := [.pos 74, .pos 76, .neg 82, .neg 102, .pos 208]
private def clause179 : Sat.Clause := [.pos 74, .pos 77, .neg 83, .neg 103, .pos 209]
private def clause180 : Sat.Clause := [.pos 74, .pos 78, .neg 84, .neg 104, .pos 210]
private def clause181 : Sat.Clause := [.pos 74, .pos 79, .neg 85, .neg 105, .pos 211]
private def clause182 : Sat.Clause := [.neg 0, .neg 6, .neg 24, .pos 74, .pos 80, .neg 86, .pos 106]
private def clause183 : Sat.Clause := [.pos 74, .pos 80, .neg 86, .neg 106, .pos 212]
private def clause184 : Sat.Clause := [.pos 75, .pos 76, .neg 87, .neg 113, .pos 213]
private def clause185 : Sat.Clause := [.pos 75, .pos 77, .neg 88, .neg 114, .pos 214]
private def clause186 : Sat.Clause := [.pos 75, .pos 78, .neg 89, .neg 115, .pos 215]
private def clause187 : Sat.Clause := [.pos 75, .pos 79, .neg 90, .neg 116, .pos 216]
private def clause188 : Sat.Clause := [.neg 0, .neg 8, .neg 33, .pos 75, .pos 80, .neg 91, .pos 117]
private def clause189 : Sat.Clause := [.pos 75, .pos 80, .neg 91, .neg 117, .pos 217]
private def clause190 : Sat.Clause := [.pos 76, .pos 77, .neg 92, .neg 123, .pos 218]
private def clause191 : Sat.Clause := [.pos 76, .pos 78, .neg 93, .neg 124, .pos 219]
private def clause192 : Sat.Clause := [.pos 76, .pos 79, .neg 94, .neg 125, .pos 220]
private def clause193 : Sat.Clause := [.neg 0, .neg 10, .neg 42, .pos 76, .pos 80, .neg 95, .pos 126]
private def clause194 : Sat.Clause := [.pos 76, .pos 80, .neg 95, .neg 126, .pos 221]
private def clause195 : Sat.Clause := [.pos 77, .pos 78, .pos 96, .pos 127, .pos 222]
private def clause196 : Sat.Clause := [.pos 77, .pos 79, .pos 97, .pos 128, .pos 223]
private def clause197 : Sat.Clause := [.pos 77, .pos 80, .pos 98, .pos 129, .pos 224]
private def clause198 : Sat.Clause := [.neg 0, .neg 13, .pos 46, .pos 78, .pos 79, .pos 99, .neg 130]
private def clause199 : Sat.Clause := [.pos 78, .pos 79, .neg 99, .neg 130, .pos 225]
private def clause200 : Sat.Clause := [.neg 0, .neg 13, .neg 63, .pos 79, .neg 80, .pos 100, .pos 136]
private def clause201 : Sat.Clause := [.pos 79, .pos 80, .pos 100, .pos 136, .pos 226]
private def clause202 : Sat.Clause := [.neg 81, .neg 82, .neg 87, .neg 140, .pos 227]
private def clause203 : Sat.Clause := [.neg 81, .neg 83, .neg 88, .neg 141, .pos 228]
private def clause204 : Sat.Clause := [.neg 81, .neg 84, .neg 89, .neg 142, .pos 229]
private def clause205 : Sat.Clause := [.neg 81, .neg 85, .neg 90, .neg 143, .pos 230]
private def clause206 : Sat.Clause := [.neg 81, .neg 86, .neg 91, .neg 144, .pos 231]
private def clause207 : Sat.Clause := [.neg 82, .neg 83, .neg 92, .neg 145, .pos 232]
private def clause208 : Sat.Clause := [.neg 82, .neg 84, .neg 93, .neg 146, .pos 233]
private def clause209 : Sat.Clause := [.neg 82, .neg 85, .neg 94, .neg 147, .pos 234]
private def clause210 : Sat.Clause := [.neg 82, .neg 86, .neg 95, .neg 148, .pos 235]
private def clause211 : Sat.Clause := [.neg 1, .neg 20, .neg 43, .neg 83, .neg 84, .pos 96, .neg 149]
private def clause212 : Sat.Clause := [.neg 83, .neg 84, .pos 96, .pos 149, .pos 236]
private def clause213 : Sat.Clause := [.neg 83, .neg 85, .pos 97, .pos 150, .pos 237]
private def clause214 : Sat.Clause := [.neg 83, .neg 86, .pos 98, .pos 151, .pos 238]
private def clause215 : Sat.Clause := [.neg 1, .neg 22, .pos 46, .neg 84, .neg 85, .neg 99, .pos 152]
private def clause216 : Sat.Clause := [.neg 84, .neg 85, .neg 99, .neg 152, .pos 239]
private def clause217 : Sat.Clause := [.neg 85, .neg 86, .pos 100, .pos 153, .pos 240]
private def clause218 : Sat.Clause := [.neg 87, .neg 88, .neg 92, .neg 169, .pos 241]
private def clause219 : Sat.Clause := [.neg 87, .neg 89, .neg 93, .neg 170, .pos 242]
private def clause220 : Sat.Clause := [.neg 87, .neg 90, .neg 94, .neg 171, .pos 243]
private def clause221 : Sat.Clause := [.neg 87, .neg 91, .neg 95, .neg 172, .pos 244]
private def clause222 : Sat.Clause := [.neg 2, .neg 29, .neg 43, .neg 88, .neg 89, .pos 96, .neg 173]
private def clause223 : Sat.Clause := [.neg 4, .pos 29, .neg 30, .neg 88, .neg 89, .pos 96, .neg 173]
private def clause224 : Sat.Clause := [.neg 88, .neg 89, .pos 96, .pos 173, .pos 245]
private def clause225 : Sat.Clause := [.neg 88, .neg 90, .pos 97, .pos 174, .pos 246]
private def clause226 : Sat.Clause := [.neg 4, .pos 29, .neg 33, .neg 88, .neg 91, .pos 98, .neg 175]
private def clause227 : Sat.Clause := [.neg 88, .neg 91, .pos 98, .pos 175, .pos 247]
private def clause228 : Sat.Clause := [.neg 2, .neg 31, .pos 46, .neg 89, .neg 90, .neg 99, .pos 176]
private def clause229 : Sat.Clause := [.neg 89, .neg 90, .neg 99, .neg 176, .pos 248]
private def clause230 : Sat.Clause := [.neg 90, .neg 91, .pos 100, .pos 177, .pos 249]
private def clause231 : Sat.Clause := [.neg 92, .neg 93, .pos 96, .pos 188, .pos 250]
private def clause232 : Sat.Clause := [.neg 92, .neg 94, .pos 97, .pos 189, .pos 251]
private def clause233 : Sat.Clause := [.neg 3, .neg 38, .neg 45, .neg 92, .neg 95, .pos 98, .neg 190]
private def clause234 : Sat.Clause := [.neg 4, .pos 38, .neg 42, .neg 92, .neg 95, .pos 98, .neg 190]
private def clause235 : Sat.Clause := [.neg 92, .neg 95, .pos 98, .pos 190, .pos 252]
private def clause236 : Sat.Clause := [.neg 3, .neg 40, .pos 46, .neg 93, .neg 94, .neg 99, .pos 191]
private def clause237 : Sat.Clause := [.neg 93, .neg 94, .neg 99, .neg 191, .pos 253]
private def clause238 : Sat.Clause := [.neg 94, .neg 95, .pos 100, .pos 193, .pos 254]
private def clause239 : Sat.Clause := [.neg 4, .neg 44, .pos 46, .neg 96, .pos 97, .neg 99, .neg 194]
private def clause240 : Sat.Clause := [.pos 96, .pos 97, .neg 99, .neg 194, .pos 255]
private def clause241 : Sat.Clause := [.neg 4, .neg 44, .neg 63, .pos 97, .neg 98, .pos 100, .pos 196]
private def clause242 : Sat.Clause := [.pos 97, .pos 98, .pos 100, .pos 196, .pos 256]
private def clause243 : Sat.Clause := [.neg 101, .neg 102, .neg 113, .neg 140, .pos 257]
private def clause244 : Sat.Clause := [.neg 101, .neg 103, .neg 114, .neg 141, .pos 258]
private def clause245 : Sat.Clause := [.neg 101, .neg 104, .neg 115, .neg 142, .pos 259]
private def clause246 : Sat.Clause := [.neg 101, .neg 105, .neg 116, .neg 143, .pos 260]
private def clause247 : Sat.Clause := [.neg 6, .neg 16, .neg 33, .neg 101, .pos 106, .neg 117, .neg 144]
private def clause248 : Sat.Clause := [.neg 101, .neg 106, .neg 117, .neg 144, .pos 261]
private def clause249 : Sat.Clause := [.neg 102, .neg 103, .neg 123, .neg 145, .pos 262]
private def clause250 : Sat.Clause := [.neg 102, .neg 104, .neg 124, .neg 146, .pos 263]
private def clause251 : Sat.Clause := [.neg 102, .neg 105, .neg 125, .neg 147, .pos 264]
private def clause252 : Sat.Clause := [.neg 102, .neg 106, .neg 126, .neg 148, .pos 265]
private def clause253 : Sat.Clause := [.neg 11, .pos 20, .neg 21, .neg 103, .neg 104, .pos 127, .neg 149]
private def clause254 : Sat.Clause := [.neg 103, .neg 104, .pos 127, .pos 149, .pos 266]
private def clause255 : Sat.Clause := [.neg 103, .neg 105, .pos 128, .pos 150, .pos 267]
private def clause256 : Sat.Clause := [.pos 6, .neg 11, .neg 45, .neg 103, .pos 106, .pos 129, .pos 151]
private def clause257 : Sat.Clause := [.neg 103, .neg 106, .pos 129, .pos 151, .pos 268]
private def clause258 : Sat.Clause := [.neg 13, .neg 21, .pos 22, .neg 104, .neg 105, .neg 130, .pos 152]
private def clause259 : Sat.Clause := [.neg 104, .neg 105, .neg 130, .neg 152, .pos 269]
private def clause260 : Sat.Clause := [.neg 105, .neg 106, .pos 136, .pos 153, .pos 270]
private def clause261 : Sat.Clause := [.neg 107, .neg 108, .neg 118, .neg 154, .pos 271]
private def clause262 : Sat.Clause := [.neg 107, .neg 109, .neg 119, .neg 155, .pos 272]
private def clause263 : Sat.Clause := [.neg 107, .neg 110, .neg 120, .neg 156, .pos 273]
private def clause264 : Sat.Clause := [.neg 107, .neg 111, .neg 121, .neg 157, .pos 274]
private def clause265 : Sat.Clause := [.neg 107, .neg 112, .neg 122, .neg 158, .pos 275]
private def clause266 : Sat.Clause := [.neg 108, .neg 109, .neg 130, .neg 159, .pos 276]
private def clause267 : Sat.Clause := [.neg 108, .neg 110, .neg 131, .neg 160, .pos 277]
private def clause268 : Sat.Clause := [.neg 108, .neg 111, .neg 132, .neg 161, .pos 278]
private def clause269 : Sat.Clause := [.neg 108, .neg 112, .neg 133, .neg 162, .pos 279]
private def clause270 : Sat.Clause := [.neg 7, .neg 27, .pos 53, .neg 109, .neg 110, .neg 134, .pos 163]
private def clause271 : Sat.Clause := [.neg 109, .neg 110, .neg 134, .neg 163, .pos 280]
private def clause272 : Sat.Clause := [.neg 109, .neg 111, .neg 135, .neg 164, .pos 281]
private def clause273 : Sat.Clause := [.neg 109, .neg 112, .neg 136, .neg 165, .pos 282]
private def clause274 : Sat.Clause := [.neg 110, .neg 111, .pos 137, .pos 166, .pos 283]
private def clause275 : Sat.Clause := [.neg 110, .neg 112, .pos 138, .pos 167, .pos 284]
private def clause276 : Sat.Clause := [.neg 111, .neg 112, .pos 139, .pos 168, .pos 285]
private def clause277 : Sat.Clause := [.neg 113, .neg 114, .neg 123, .neg 169, .pos 286]
private def clause278 : Sat.Clause := [.neg 113, .neg 115, .neg 124, .neg 170, .pos 287]
private def clause279 : Sat.Clause := [.neg 113, .neg 116, .neg 125, .neg 171, .pos 288]
private def clause280 : Sat.Clause := [.neg 8, .neg 28, .neg 42, .neg 113, .pos 117, .neg 126, .neg 172]
private def clause281 : Sat.Clause := [.neg 8, .neg 28, .neg 42, .neg 113, .neg 117, .pos 126, .neg 172]
private def clause282 : Sat.Clause := [.neg 113, .neg 117, .neg 126, .neg 172, .pos 289]
private def clause283 : Sat.Clause := [.neg 114, .neg 115, .pos 127, .pos 173, .pos 290]
private def clause284 : Sat.Clause := [.neg 114, .neg 116, .pos 128, .pos 174, .pos 291]
private def clause285 : Sat.Clause := [.pos 8, .neg 11, .neg 45, .neg 114, .pos 117, .pos 129, .pos 175]
private def clause286 : Sat.Clause := [.neg 114, .neg 117, .pos 129, .pos 175, .pos 292]
private def clause287 : Sat.Clause := [.neg 13, .neg 30, .pos 31, .neg 115, .neg 116, .neg 130, .pos 176]
private def clause288 : Sat.Clause := [.neg 115, .neg 116, .neg 130, .neg 176, .pos 293]
private def clause289 : Sat.Clause := [.neg 116, .neg 117, .pos 136, .pos 177, .pos 294]
private def clause290 : Sat.Clause := [.neg 118, .neg 119, .neg 130, .neg 178, .pos 295]
private def clause291 : Sat.Clause := [.neg 118, .neg 120, .neg 131, .neg 179, .pos 296]
private def clause292 : Sat.Clause := [.neg 118, .neg 121, .neg 132, .neg 180, .pos 297]
private def clause293 : Sat.Clause := [.neg 118, .neg 122, .neg 133, .neg 181, .pos 298]
private def clause294 : Sat.Clause := [.neg 9, .neg 37, .pos 53, .neg 119, .neg 120, .neg 134, .pos 182]
private def clause295 : Sat.Clause := [.neg 119, .neg 120, .neg 134, .neg 182, .pos 299]
private def clause296 : Sat.Clause := [.neg 119, .neg 121, .neg 135, .neg 183, .pos 300]
private def clause297 : Sat.Clause := [.neg 9, .neg 36, .neg 63, .neg 119, .neg 122, .pos 136, .neg 184]
private def clause298 : Sat.Clause := [.neg 119, .neg 122, .neg 136, .neg 184, .pos 301]
private def clause299 : Sat.Clause := [.neg 120, .neg 121, .pos 137, .pos 185, .pos 302]
private def clause300 : Sat.Clause := [.neg 120, .neg 122, .pos 138, .pos 186, .pos 303]
private def clause301 : Sat.Clause := [.neg 121, .neg 122, .pos 139, .pos 187, .pos 304]
private def clause302 : Sat.Clause := [.neg 11, .pos 38, .neg 39, .neg 123, .neg 124, .pos 127, .neg 188]
private def clause303 : Sat.Clause := [.neg 123, .neg 124, .pos 127, .pos 188, .pos 305]
private def clause304 : Sat.Clause := [.neg 123, .neg 125, .pos 128, .pos 189, .pos 306]
private def clause305 : Sat.Clause := [.pos 10, .neg 11, .neg 45, .neg 123, .pos 126, .pos 129, .pos 190]
private def clause306 : Sat.Clause := [.neg 123, .neg 126, .pos 129, .pos 190, .pos 307]
private def clause307 : Sat.Clause := [.neg 13, .neg 39, .pos 40, .neg 124, .neg 125, .neg 130, .pos 191]
private def clause308 : Sat.Clause := [.neg 124, .neg 125, .neg 130, .neg 191, .pos 308]
private def clause309 : Sat.Clause := [.neg 10, .neg 39, .neg 52, .neg 124, .pos 126, .neg 133, .pos 192]
private def clause310 : Sat.Clause := [.neg 10, .neg 39, .neg 52, .neg 124, .pos 126, .neg 133, .neg 192]
private def clause311 : Sat.Clause := [.neg 125, .neg 126, .pos 136, .pos 193, .pos 309]
private def clause312 : Sat.Clause := [.pos 127, .pos 128, .neg 130, .neg 194, .pos 310]
private def clause313 : Sat.Clause := [.neg 11, .neg 44, .neg 63, .pos 128, .pos 129, .neg 136, .pos 196]
private def clause314 : Sat.Clause := [.neg 11, .neg 44, .neg 63, .pos 128, .neg 129, .pos 136, .pos 196]
private def clause315 : Sat.Clause := [.neg 11, .neg 44, .neg 63, .pos 128, .neg 129, .neg 136, .pos 196]
private def clause316 : Sat.Clause := [.pos 128, .pos 129, .pos 136, .pos 196, .pos 311]
private def clause317 : Sat.Clause := [.neg 12, .neg 51, .pos 53, .neg 130, .neg 131, .neg 134, .pos 197]
private def clause318 : Sat.Clause := [.neg 15, .neg 46, .pos 51, .neg 130, .neg 131, .neg 134, .pos 197]
private def clause319 : Sat.Clause := [.neg 130, .neg 131, .neg 134, .neg 197, .pos 312]
private def clause320 : Sat.Clause := [.neg 130, .neg 132, .neg 135, .neg 198, .pos 313]
private def clause321 : Sat.Clause := [.neg 12, .neg 46, .neg 63, .neg 130, .neg 133, .pos 136, .neg 199]
private def clause322 : Sat.Clause := [.neg 130, .neg 133, .neg 136, .neg 199, .pos 314]
private def clause323 : Sat.Clause := [.neg 131, .neg 132, .pos 137, .pos 200, .pos 315]
private def clause324 : Sat.Clause := [.neg 131, .neg 133, .pos 138, .pos 201, .pos 316]
private def clause325 : Sat.Clause := [.neg 132, .neg 133, .pos 139, .pos 202, .pos 317]
private def clause326 : Sat.Clause := [.neg 134, .neg 135, .pos 137, .pos 203, .pos 318]
private def clause327 : Sat.Clause := [.neg 15, .pos 53, .neg 63, .neg 134, .neg 136, .pos 138, .neg 204]
private def clause328 : Sat.Clause := [.neg 134, .neg 136, .pos 138, .pos 204, .pos 319]
private def clause329 : Sat.Clause := [.neg 135, .neg 136, .pos 139, .pos 205, .pos 320]
private def clause330 : Sat.Clause := [.pos 137, .pos 138, .pos 139, .pos 206, .pos 321]
private def clause331 : Sat.Clause := [.neg 140, .neg 141, .neg 145, .neg 169, .pos 322]
private def clause332 : Sat.Clause := [.neg 140, .neg 142, .neg 146, .neg 170, .pos 323]
private def clause333 : Sat.Clause := [.neg 140, .neg 143, .neg 147, .neg 171, .pos 324]
private def clause334 : Sat.Clause := [.neg 140, .neg 144, .neg 148, .neg 172, .pos 325]
private def clause335 : Sat.Clause := [.neg 141, .neg 142, .pos 149, .pos 173, .pos 326]
private def clause336 : Sat.Clause := [.neg 141, .neg 143, .pos 150, .pos 174, .pos 327]
private def clause337 : Sat.Clause := [.neg 16, .pos 20, .neg 33, .neg 141, .neg 144, .neg 151, .pos 175]
private def clause338 : Sat.Clause := [.neg 141, .neg 144, .pos 151, .pos 175, .pos 328]
private def clause339 : Sat.Clause := [.neg 142, .neg 143, .neg 152, .neg 176, .pos 329]
private def clause340 : Sat.Clause := [.neg 143, .neg 144, .pos 153, .pos 177, .pos 330]
private def clause341 : Sat.Clause := [.neg 145, .neg 146, .pos 149, .pos 188, .pos 331]
private def clause342 : Sat.Clause := [.neg 145, .neg 147, .pos 150, .pos 189, .pos 332]
private def clause343 : Sat.Clause := [.neg 145, .neg 148, .pos 151, .pos 190, .pos 333]
private def clause344 : Sat.Clause := [.neg 145, .neg 148, .neg 151, .pos 190, .neg 333]
private def clause345 : Sat.Clause := [.neg 146, .neg 147, .neg 152, .neg 191, .pos 334]
private def clause346 : Sat.Clause := [.neg 147, .neg 148, .pos 153, .pos 193, .pos 335]
private def clause347 : Sat.Clause := [.neg 20, .neg 44, .pos 46, .neg 149, .pos 150, .neg 152, .neg 194]
private def clause348 : Sat.Clause := [.pos 149, .pos 150, .neg 152, .neg 194, .pos 336]
private def clause349 : Sat.Clause := [.neg 149, .pos 150, .neg 152, .neg 194, .neg 336]
private def clause350 : Sat.Clause := [.neg 20, .neg 44, .neg 63, .pos 150, .neg 151, .pos 153, .pos 196]
private def clause351 : Sat.Clause := [.pos 150, .pos 151, .pos 153, .pos 196, .pos 337]
private def clause352 : Sat.Clause := [.neg 154, .neg 155, .neg 159, .neg 178, .pos 338]
private def clause353 : Sat.Clause := [.neg 154, .neg 156, .neg 160, .neg 179, .pos 339]
private def clause354 : Sat.Clause := [.neg 154, .neg 157, .neg 161, .neg 180, .pos 340]
private def clause355 : Sat.Clause := [.neg 154, .neg 158, .neg 162, .neg 181, .pos 341]
private def clause356 : Sat.Clause := [.neg 25, .neg 36, .neg 53, .neg 155, .neg 156, .pos 163, .neg 182]
private def clause357 : Sat.Clause := [.neg 25, .pos 27, .neg 36, .neg 155, .neg 156, .pos 163, .neg 182]
private def clause358 : Sat.Clause := [.neg 155, .neg 156, .neg 163, .neg 182, .pos 342]
private def clause359 : Sat.Clause := [.neg 25, .neg 36, .neg 55, .neg 155, .neg 157, .pos 164, .neg 183]
private def clause360 : Sat.Clause := [.neg 155, .neg 157, .neg 164, .neg 183, .pos 343]
private def clause361 : Sat.Clause := [.neg 25, .neg 36, .neg 63, .neg 155, .neg 158, .pos 165, .neg 184]
private def clause362 : Sat.Clause := [.neg 155, .neg 158, .neg 165, .neg 184, .pos 344]
private def clause363 : Sat.Clause := [.neg 156, .neg 157, .pos 166, .pos 185, .pos 345]
private def clause364 : Sat.Clause := [.neg 156, .neg 158, .pos 167, .pos 186, .pos 346]
private def clause365 : Sat.Clause := [.neg 157, .neg 158, .pos 168, .pos 187, .pos 347]
private def clause366 : Sat.Clause := [.neg 159, .neg 160, .neg 163, .neg 197, .pos 348]
private def clause367 : Sat.Clause := [.neg 159, .neg 161, .neg 164, .neg 198, .pos 349]
private def clause368 : Sat.Clause := [.neg 159, .neg 162, .neg 165, .neg 199, .pos 350]
private def clause369 : Sat.Clause := [.neg 160, .neg 161, .pos 166, .pos 200, .pos 351]
private def clause370 : Sat.Clause := [.neg 160, .neg 162, .pos 167, .pos 201, .pos 352]
private def clause371 : Sat.Clause := [.neg 161, .neg 162, .pos 168, .pos 202, .pos 353]
private def clause372 : Sat.Clause := [.neg 163, .neg 164, .pos 166, .pos 203, .pos 354]
private def clause373 : Sat.Clause := [.neg 163, .neg 165, .pos 167, .pos 204, .pos 355]
private def clause374 : Sat.Clause := [.neg 164, .neg 165, .pos 168, .pos 205, .pos 356]
private def clause375 : Sat.Clause := [.pos 166, .pos 167, .pos 168, .pos 206, .pos 357]
private def clause376 : Sat.Clause := [.neg 169, .neg 170, .pos 173, .pos 188, .pos 358]
private def clause377 : Sat.Clause := [.neg 169, .neg 171, .pos 174, .pos 189, .pos 359]
private def clause378 : Sat.Clause := [.neg 169, .neg 172, .pos 175, .pos 190, .pos 360]
private def clause379 : Sat.Clause := [.neg 170, .neg 171, .neg 176, .neg 191, .pos 361]
private def clause380 : Sat.Clause := [.neg 171, .neg 172, .pos 177, .pos 193, .pos 362]
private def clause381 : Sat.Clause := [.pos 173, .pos 174, .neg 176, .neg 194, .pos 363]
private def clause382 : Sat.Clause := [.neg 29, .neg 44, .neg 63, .pos 174, .neg 175, .pos 177, .pos 196]
private def clause383 : Sat.Clause := [.pos 174, .pos 175, .pos 177, .pos 196, .pos 364]
private def clause384 : Sat.Clause := [.neg 34, .neg 46, .neg 53, .neg 178, .neg 179, .pos 182, .neg 197]
private def clause385 : Sat.Clause := [.neg 34, .pos 37, .neg 46, .neg 178, .neg 179, .pos 182, .neg 197]
private def clause386 : Sat.Clause := [.neg 178, .neg 179, .neg 182, .neg 197, .pos 365]
private def clause387 : Sat.Clause := [.neg 34, .neg 46, .neg 55, .neg 178, .neg 180, .pos 183, .neg 198]
private def clause388 : Sat.Clause := [.neg 178, .neg 180, .neg 183, .neg 198, .pos 366]
private def clause389 : Sat.Clause := [.neg 34, .neg 46, .neg 63, .neg 178, .neg 181, .pos 184, .neg 199]
private def clause390 : Sat.Clause := [.neg 34, .pos 36, .neg 52, .neg 178, .neg 181, .neg 184, .neg 199]
private def clause391 : Sat.Clause := [.neg 178, .neg 181, .pos 184, .neg 199, .neg 367]
private def clause392 : Sat.Clause := [.neg 178, .neg 181, .neg 184, .neg 199, .pos 367]
private def clause393 : Sat.Clause := [.neg 179, .neg 180, .pos 185, .pos 200, .pos 368]
private def clause394 : Sat.Clause := [.neg 179, .neg 181, .pos 186, .pos 201, .pos 369]
private def clause395 : Sat.Clause := [.neg 180, .neg 181, .pos 187, .pos 202, .pos 370]
private def clause396 : Sat.Clause := [.neg 182, .neg 183, .pos 185, .pos 203, .pos 371]
private def clause397 : Sat.Clause := [.pos 182, .neg 184, .pos 186, .pos 204, .neg 372]
private def clause398 : Sat.Clause := [.neg 182, .neg 184, .pos 186, .pos 204, .pos 372]
private def clause399 : Sat.Clause := [.pos 183, .neg 184, .pos 187, .pos 205, .neg 373]
private def clause400 : Sat.Clause := [.neg 183, .neg 184, .pos 187, .pos 205, .pos 373]
private def clause401 : Sat.Clause := [.pos 185, .pos 186, .pos 187, .pos 206, .pos 374]
private def clause402 : Sat.Clause := [.neg 38, .neg 44, .pos 46, .neg 188, .pos 189, .neg 191, .neg 194]
private def clause403 : Sat.Clause := [.neg 38, .neg 44, .pos 46, .neg 188, .pos 189, .pos 191, .neg 194]
private def clause404 : Sat.Clause := [.pos 188, .pos 189, .neg 191, .neg 194, .pos 375]
private def clause405 : Sat.Clause := [.pos 189, .pos 190, .pos 193, .pos 196, .pos 376]
private def clause406 : Sat.Clause := [.neg 44, .pos 46, .neg 52, .neg 194, .pos 195, .neg 196, .neg 199]
private def clause407 : Sat.Clause := [.neg 44, .pos 46, .neg 52, .neg 194, .neg 195, .neg 196, .neg 199]
private def clause408 : Sat.Clause := [.neg 194, .pos 195, .neg 196, .pos 199, .neg 377]
private def clause409 : Sat.Clause := [.neg 194, .pos 195, .neg 196, .neg 199, .neg 377]
private def clause410 : Sat.Clause := [.neg 194, .neg 195, .neg 196, .pos 199, .neg 377]
private def clause411 : Sat.Clause := [.neg 194, .neg 195, .neg 196, .neg 199, .pos 377]
private def clause412 : Sat.Clause := [.neg 197, .neg 198, .pos 200, .pos 203, .pos 378]
private def clause413 : Sat.Clause := [.pos 197, .neg 199, .pos 201, .pos 204, .neg 379]
private def clause414 : Sat.Clause := [.neg 197, .pos 199, .pos 201, .pos 204, .neg 379]
private def clause415 : Sat.Clause := [.neg 197, .neg 199, .pos 201, .pos 204, .pos 379]
private def clause416 : Sat.Clause := [.pos 198, .neg 199, .pos 202, .pos 205, .neg 380]
private def clause417 : Sat.Clause := [.neg 198, .neg 199, .pos 202, .pos 205, .pos 380]
private def clause418 : Sat.Clause := [.pos 200, .pos 201, .pos 202, .pos 206, .pos 381]
private def clause419 : Sat.Clause := [.neg 53, .neg 71, .neg 73, .pos 203, .neg 204, .pos 205, .pos 206]
private def clause420 : Sat.Clause := [.pos 203, .pos 204, .pos 205, .pos 206, .pos 382]
private def clause421 : Sat.Clause := [.pos 203, .neg 204, .pos 205, .pos 206, .neg 382]
private def clause422 : Sat.Clause := [.neg 207, .neg 208, .neg 209, .neg 210, .neg 211, .neg 213, .neg 214, .neg 215, .neg 216, .neg 218, .neg 219, .neg 220, .neg 222, .neg 223, .neg 225, .neg 227, .neg 228, .neg 229, .neg 230, .neg 232, .neg 233, .neg 234, .neg 236, .neg 237, .neg 239, .neg 241, .neg 242, .neg 243, .neg 245, .neg 246, .neg 248, .neg 250, .neg 251, .neg 253, .neg 255, .neg 257, .neg 258, .neg 259, .neg 260, .neg 262, .neg 263, .neg 264, .neg 266, .neg 267, .neg 269, .neg 286, .neg 287, .neg 288, .neg 290, .neg 291, .neg 293, .neg 305, .neg 306, .neg 308, .neg 310, .neg 322, .neg 323, .neg 324, .neg 326, .neg 327, .neg 329, .neg 331, .neg 332, .neg 334, .neg 336, .neg 358, .neg 359, .neg 361, .neg 363, .neg 375]
private def clause423 : Sat.Clause := [.neg 207, .neg 208, .neg 209, .neg 211, .neg 212, .neg 213, .neg 214, .neg 216, .neg 217, .neg 218, .neg 220, .neg 221, .neg 223, .neg 224, .neg 226, .neg 227, .neg 228, .neg 230, .neg 231, .neg 232, .neg 234, .neg 235, .neg 237, .neg 238, .neg 240, .neg 241, .neg 243, .neg 244, .neg 246, .neg 247, .neg 249, .neg 251, .neg 252, .neg 254, .neg 256, .neg 257, .neg 258, .neg 260, .neg 261, .neg 262, .neg 264, .neg 265, .neg 267, .neg 268, .neg 270, .neg 286, .neg 288, .neg 289, .neg 291, .neg 292, .neg 294, .neg 306, .neg 307, .neg 309, .neg 311, .neg 322, .neg 324, .neg 325, .neg 327, .neg 328, .neg 330, .neg 332, .neg 333, .neg 335, .neg 337, .neg 359, .neg 360, .neg 362, .neg 364, .neg 376]
private def clause424 : Sat.Clause := [.neg 271, .neg 272, .neg 273, .neg 274, .neg 275, .neg 276, .neg 277, .neg 278, .neg 279, .neg 280, .neg 281, .neg 282, .neg 283, .neg 284, .neg 285, .neg 295, .neg 296, .neg 297, .neg 298, .neg 299, .neg 300, .neg 301, .neg 302, .neg 303, .neg 304, .neg 312, .neg 313, .neg 314, .neg 315, .neg 316, .neg 317, .neg 318, .neg 319, .neg 320, .neg 321, .neg 338, .neg 339, .neg 340, .neg 341, .neg 342, .neg 343, .neg 344, .neg 345, .neg 346, .neg 347, .neg 348, .neg 349, .neg 350, .neg 351, .neg 352, .neg 353, .neg 354, .neg 355, .neg 356, .neg 357, .neg 365, .neg 366, .neg 367, .neg 368, .neg 369, .neg 370, .neg 371, .neg 372, .neg 373, .neg 374, .neg 378, .neg 379, .neg 380, .neg 381, .neg 382]

private def clauses : Sat.Fmla := [
  clause000, clause001, clause002, clause003, clause004, clause005, clause006, clause007, clause008, clause009, clause010, clause011, clause012, clause013, clause014, clause015, clause016, clause017, clause018, clause019, clause020, clause021, clause022, clause023, clause024, clause025, clause026, clause027, clause028, clause029, clause030, clause031, clause032, clause033, clause034, clause035, clause036, clause037, clause038, clause039, clause040, clause041, clause042, clause043, clause044, clause045, clause046, clause047, clause048, clause049, clause050, clause051, clause052, clause053, clause054, clause055, clause056, clause057, clause058, clause059, clause060, clause061, clause062, clause063, clause064, clause065, clause066, clause067, clause068, clause069, clause070, clause071, clause072, clause073, clause074, clause075, clause076, clause077, clause078, clause079, clause080, clause081, clause082, clause083, clause084, clause085, clause086, clause087, clause088, clause089, clause090, clause091, clause092, clause093, clause094, clause095, clause096, clause097, clause098, clause099, clause100, clause101, clause102, clause103, clause104, clause105, clause106, clause107, clause108, clause109, clause110, clause111, clause112, clause113, clause114, clause115, clause116, clause117, clause118, clause119, clause120, clause121, clause122, clause123, clause124, clause125, clause126, clause127, clause128, clause129, clause130, clause131, clause132, clause133, clause134, clause135, clause136, clause137, clause138, clause139, clause140, clause141, clause142, clause143, clause144, clause145, clause146, clause147, clause148, clause149, clause150, clause151, clause152, clause153, clause154, clause155, clause156, clause157, clause158, clause159, clause160, clause161, clause162, clause163, clause164, clause165, clause166, clause167, clause168, clause169, clause170, clause171, clause172, clause173, clause174, clause175, clause176, clause177, clause178, clause179, clause180, clause181, clause182, clause183, clause184, clause185, clause186, clause187, clause188, clause189, clause190, clause191, clause192, clause193, clause194, clause195, clause196, clause197, clause198, clause199, clause200, clause201, clause202, clause203, clause204, clause205, clause206, clause207, clause208, clause209, clause210, clause211, clause212, clause213, clause214, clause215, clause216, clause217, clause218, clause219, clause220, clause221, clause222, clause223, clause224, clause225, clause226, clause227, clause228, clause229, clause230, clause231, clause232, clause233, clause234, clause235, clause236, clause237, clause238, clause239, clause240, clause241, clause242, clause243, clause244, clause245, clause246, clause247, clause248, clause249, clause250, clause251, clause252, clause253, clause254, clause255, clause256, clause257, clause258, clause259, clause260, clause261, clause262, clause263, clause264, clause265, clause266, clause267, clause268, clause269, clause270, clause271, clause272, clause273, clause274, clause275, clause276, clause277, clause278, clause279, clause280, clause281, clause282, clause283, clause284, clause285, clause286, clause287, clause288, clause289, clause290, clause291, clause292, clause293, clause294, clause295, clause296, clause297, clause298, clause299, clause300, clause301, clause302, clause303, clause304, clause305, clause306, clause307, clause308, clause309, clause310, clause311, clause312, clause313, clause314, clause315, clause316, clause317, clause318, clause319, clause320, clause321, clause322, clause323, clause324, clause325, clause326, clause327, clause328, clause329, clause330, clause331, clause332, clause333, clause334, clause335, clause336, clause337, clause338, clause339, clause340, clause341, clause342, clause343, clause344, clause345, clause346, clause347, clause348, clause349, clause350, clause351, clause352, clause353, clause354, clause355, clause356, clause357, clause358, clause359, clause360, clause361, clause362, clause363, clause364, clause365, clause366, clause367, clause368, clause369, clause370, clause371, clause372, clause373, clause374, clause375, clause376, clause377, clause378, clause379, clause380, clause381, clause382, clause383, clause384, clause385, clause386, clause387, clause388, clause389, clause390, clause391, clause392, clause393, clause394, clause395, clause396, clause397, clause398, clause399, clause400, clause401, clause402, clause403, clause404, clause405, clause406, clause407, clause408, clause409, clause410, clause411, clause412, clause413, clause414, clause415, clause416, clause417, clause418, clause419, clause420, clause421, clause422, clause423, clause424]

private theorem formula_eq : cnf_refutation.formula = clauses := by rfl

variable {n : ℕ} (C : Context 13 n states)

-- Clause 1: empty_direction; source clause 30.
private theorem sound000 : C.clause (decodeClause atoms clause000) := by
  exact C.covered_clause _ _ (C.empty_clause 1 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 2: empty_direction; source clause 83.
private theorem sound001 : C.clause (decodeClause atoms clause001) := by
  exact C.covered_clause _ _ (C.empty_clause 2 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 3: empty_direction; source clause 186.
private theorem sound002 : C.clause (decodeClause atoms clause002) := by
  exact C.covered_clause _ _ (C.empty_clause 4 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 4: empty_direction; source clause 287.
private theorem sound003 : C.clause (decodeClause atoms clause003) := by
  exact C.covered_clause _ _ (C.empty_clause 6 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 5: empty_direction; source clause 337.
private theorem sound004 : C.clause (decodeClause atoms clause004) := by
  exact C.covered_clause _ _ (C.empty_clause 7 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 6: empty_direction; source clause 435.
private theorem sound005 : C.clause (decodeClause atoms clause005) := by
  exact C.covered_clause _ _ (C.empty_clause 9 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 7: empty_direction; source clause 683.
private theorem sound006 : C.clause (decodeClause atoms clause006) := by
  exact C.covered_clause _ _ (C.empty_clause 3 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 8: empty_direction; source clause 784.
private theorem sound007 : C.clause (decodeClause atoms clause007) := by
  exact C.covered_clause _ _ (C.empty_clause 5 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 9: empty_direction; source clause 883.
private theorem sound008 : C.clause (decodeClause atoms clause008) := by
  exact C.covered_clause _ _ (C.empty_clause 7 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 10: empty_direction; source clause 933.
private theorem sound009 : C.clause (decodeClause atoms clause009) := by
  exact C.covered_clause _ _ (C.empty_clause 8 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 11: empty_direction; source clause 983.
private theorem sound010 : C.clause (decodeClause atoms clause010) := by
  exact C.covered_clause _ _ (C.empty_clause 9 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 12: empty_direction; source clause 1033.
private theorem sound011 : C.clause (decodeClause atoms clause011) := by
  exact C.covered_clause _ _ (C.empty_clause 10 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 13: empty_direction; source clause 1237.
private theorem sound012 : C.clause (decodeClause atoms clause012) := by
  exact C.covered_clause _ _ (C.empty_clause 4 2 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 14: empty_direction; source clause 1342.
private theorem sound013 : C.clause (decodeClause atoms clause013) := by
  exact C.covered_clause _ _ (C.empty_clause 6 2 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 15: empty_direction; source clause 1440.
private theorem sound014 : C.clause (decodeClause atoms clause014) := by
  exact C.covered_clause _ _ (C.empty_clause 8 2 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 16: empty_direction; source clause 1630.
private theorem sound015 : C.clause (decodeClause atoms clause015) := by
  exact C.covered_clause _ _ (C.empty_clause 12 2 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 17: empty_direction; source clause 1735.
private theorem sound016 : C.clause (decodeClause atoms clause016) := by
  exact C.covered_clause _ _ (C.empty_clause 5 3 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 18: empty_direction; source clause 2185.
private theorem sound017 : C.clause (decodeClause atoms clause017) := by
  exact C.covered_clause _ _ (C.empty_clause 6 4 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 19: empty_direction; source clause 2287.
private theorem sound018 : C.clause (decodeClause atoms clause018) := by
  exact C.covered_clause _ _ (C.empty_clause 8 4 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 20: empty_direction; source clause 2485.
private theorem sound019 : C.clause (decodeClause atoms clause019) := by
  exact C.covered_clause _ _ (C.empty_clause 12 4 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 21: empty_direction; source clause 2638.
private theorem sound020 : C.clause (decodeClause atoms clause020) := by
  exact C.covered_clause _ _ (C.empty_clause 8 5 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 22: empty_direction; source clause 2940.
private theorem sound021 : C.clause (decodeClause atoms clause021) := by
  exact C.covered_clause _ _ (C.empty_clause 8 6 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 23: empty_direction; source clause 3142.
private theorem sound022 : C.clause (decodeClause atoms clause022) := by
  exact C.covered_clause _ _ (C.empty_clause 12 6 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 24: empty_direction; source clause 3247.
private theorem sound023 : C.clause (decodeClause atoms clause023) := by
  exact C.covered_clause _ _ (C.empty_clause 9 7 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 25: empty_direction; source clause 3406.
private theorem sound024 : C.clause (decodeClause atoms clause024) := by
  exact C.covered_clause _ _ (C.empty_clause 12 7 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 26: domain; source clause 3440.
private theorem sound025 : C.clause (decodeClause atoms clause025) := by
  exact C.covered_clause _ _ (C.domain_clause 8 9 (by decide) 1 4 (by decide +kernel)) (by decide +kernel)

-- Clause 27: domain; source clause 3441.
private theorem sound026 : C.clause (decodeClause atoms clause026) := by
  exact C.covered_clause _ _ (C.domain_clause 8 9 (by decide) 1 5 (by decide +kernel)) (by decide +kernel)

-- Clause 28: domain; source clause 3442.
private theorem sound027 : C.clause (decodeClause atoms clause027) := by
  exact C.covered_clause _ _ (C.domain_clause 8 9 (by decide) 1 6 (by decide +kernel)) (by decide +kernel)

-- Clause 29: empty_direction; source clause 3612.
private theorem sound028 : C.clause (decodeClause atoms clause028) := by
  exact C.covered_clause _ _ (C.empty_clause 12 8 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 30: domain; source clause 3707.
private theorem sound029 : C.clause (decodeClause atoms clause029) := by
  exact C.covered_clause _ _ (C.domain_clause 9 11 (by decide) 3 2 (by decide +kernel)) (by decide +kernel)

-- Clause 31: domain; source clause 3708.
private theorem sound030 : C.clause (decodeClause atoms clause030) := by
  exact C.covered_clause _ _ (C.domain_clause 9 11 (by decide) 3 3 (by decide +kernel)) (by decide +kernel)

-- Clause 32: domain; source clause 3709.
private theorem sound031 : C.clause (decodeClause atoms clause031) := by
  exact C.covered_clause _ _ (C.domain_clause 9 11 (by decide) 3 4 (by decide +kernel)) (by decide +kernel)

-- Clause 33: domain; source clause 3710.
private theorem sound032 : C.clause (decodeClause atoms clause032) := by
  exact C.covered_clause _ _ (C.domain_clause 9 11 (by decide) 3 5 (by decide +kernel)) (by decide +kernel)

-- Clause 34: domain; source clause 3711.
private theorem sound033 : C.clause (decodeClause atoms clause033) := by
  exact C.covered_clause _ _ (C.domain_clause 9 11 (by decide) 3 6 (by decide +kernel)) (by decide +kernel)

-- Clause 35: empty_direction; source clause 3718.
private theorem sound034 : C.clause (decodeClause atoms clause034) := by
  exact C.covered_clause _ _ (C.empty_clause 11 9 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 36: domain; source clause 3761.
private theorem sound035 : C.clause (decodeClause atoms clause035) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 3 2 (by decide +kernel)) (by decide +kernel)

-- Clause 37: domain; source clause 3762.
private theorem sound036 : C.clause (decodeClause atoms clause036) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 3 3 (by decide +kernel)) (by decide +kernel)

-- Clause 38: domain; source clause 3763.
private theorem sound037 : C.clause (decodeClause atoms clause037) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 3 4 (by decide +kernel)) (by decide +kernel)

-- Clause 39: domain; source clause 3764.
private theorem sound038 : C.clause (decodeClause atoms clause038) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 3 5 (by decide +kernel)) (by decide +kernel)

-- Clause 40: domain; source clause 3765.
private theorem sound039 : C.clause (decodeClause atoms clause039) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 3 6 (by decide +kernel)) (by decide +kernel)

-- Clause 41: domain; source clause 3766.
private theorem sound040 : C.clause (decodeClause atoms clause040) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 4 2 (by decide +kernel)) (by decide +kernel)

-- Clause 42: domain; source clause 3767.
private theorem sound041 : C.clause (decodeClause atoms clause041) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 4 3 (by decide +kernel)) (by decide +kernel)

-- Clause 43: domain; source clause 3768.
private theorem sound042 : C.clause (decodeClause atoms clause042) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 4 4 (by decide +kernel)) (by decide +kernel)

-- Clause 44: domain; source clause 3769.
private theorem sound043 : C.clause (decodeClause atoms clause043) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 4 5 (by decide +kernel)) (by decide +kernel)

-- Clause 45: domain; source clause 3770.
private theorem sound044 : C.clause (decodeClause atoms clause044) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 4 6 (by decide +kernel)) (by decide +kernel)

-- Clause 46: empty_direction; source clause 3771.
private theorem sound045 : C.clause (decodeClause atoms clause045) := by
  exact C.covered_clause _ _ (C.empty_clause 12 9 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 47: empty_direction; source clause 3825.
private theorem sound046 : C.clause (decodeClause atoms clause046) := by
  exact C.covered_clause _ _ (C.empty_clause 11 10 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 48: empty_direction; source clause 3932.
private theorem sound047 : C.clause (decodeClause atoms clause047) := by
  exact C.covered_clause _ _ (C.empty_clause 12 11 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 49: growth; source clause 4035.
private theorem sound048 : C.clause (decodeClause atoms clause048) := by
  exact C.covered_clause _ _ (C.growth_clause false 0 1 9 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 50: growth; source clause 4105.
private theorem sound049 : C.clause (decodeClause atoms clause049) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 2 4 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 51: growth; source clause 4127.
private theorem sound050 : C.clause (decodeClause atoms clause050) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 2 6 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 52: growth; source clause 4160.
private theorem sound051 : C.clause (decodeClause atoms clause051) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 2 9 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 53: growth; source clause 5040.
private theorem sound052 : C.clause (decodeClause atoms clause052) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 9 12 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 54: growth; source clause 5689.
private theorem sound053 : C.clause (decodeClause atoms clause053) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 3 5 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 55: order_transitive; source clause 6168.
private theorem sound054 : C.clause (decodeClause atoms clause054) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 7 4 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 56: order_transitive; source clause 6190.
private theorem sound055 : C.clause (decodeClause atoms clause055) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 7 6 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 57: growth; source clause 6481.
private theorem sound056 : C.clause (decodeClause atoms clause056) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 9 11 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 58: growth; source clause 6489.
private theorem sound057 : C.clause (decodeClause atoms clause057) := by
  exact C.covered_clause _ _ (C.growth_clause false 1 9 12 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 59: growth; source clause 6492.
private theorem sound058 : C.clause (decodeClause atoms clause058) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 9 12 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 60: order_transitive; source clause 7279.
private theorem sound059 : C.clause (decodeClause atoms clause059) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 4 7 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 61: growth; source clause 7307.
private theorem sound060 : C.clause (decodeClause atoms clause060) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 4 9 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 62: growth; source clause 7549.
private theorem sound061 : C.clause (decodeClause atoms clause061) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 6 9 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 63: order_transitive; source clause 7785.
private theorem sound062 : C.clause (decodeClause atoms clause062) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 8 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 64: growth; source clause 7945.
private theorem sound063 : C.clause (decodeClause atoms clause063) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 9 12 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 65: growth; source clause 8869.
private theorem sound064 : C.clause (decodeClause atoms clause064) := by
  exact C.covered_clause _ _ (C.growth_clause true 3 5 8 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 66: order_transitive; source clause 10425.
private theorem sound065 : C.clause (decodeClause atoms clause065) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 6 7 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 67: order_transitive; source clause 10689.
private theorem sound066 : C.clause (decodeClause atoms clause066) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 8 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 68: growth; source clause 10850.
private theorem sound067 : C.clause (decodeClause atoms clause067) := by
  exact C.covered_clause _ _ (C.growth_clause true 4 9 12 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 69: growth; source clause 12148.
private theorem sound068 : C.clause (decodeClause atoms clause068) := by
  exact C.covered_clause _ _ (C.growth_clause true 5 8 9 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 70: order_transitive; source clause 13593.
private theorem sound069 : C.clause (decodeClause atoms clause069) := by
  exact C.covered_clause _ _ (C.transitive_clause 6 8 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 71: growth; source clause 13754.
private theorem sound070 : C.clause (decodeClause atoms clause070) := by
  exact C.covered_clause _ _ (C.growth_clause true 6 9 12 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 72: order_transitive; source clause 15166.
private theorem sound071 : C.clause (decodeClause atoms clause071) := by
  exact C.covered_clause _ _ (C.transitive_clause 7 9 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 73: growth; source clause 15204.
private theorem sound072 : C.clause (decodeClause atoms clause072) := by
  exact C.covered_clause _ _ (C.growth_clause true 7 9 12 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 74: growth; source clause 16631.
private theorem sound073 : C.clause (decodeClause atoms clause073) := by
  exact C.covered_clause _ _ (C.growth_clause false 8 9 10 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 75: growth; source clause 16642.
private theorem sound074 : C.clause (decodeClause atoms clause074) := by
  exact C.covered_clause _ _ (C.growth_clause false 8 9 11 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 76: growth; source clause 16653.
private theorem sound075 : C.clause (decodeClause atoms clause075) := by
  exact C.covered_clause _ _ (C.growth_clause false 8 9 12 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 77: growth; source clause 18216.
private theorem sound076 : C.clause (decodeClause atoms clause076) := by
  exact C.covered_clause _ _ (C.growth_clause false 9 10 11 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 78: growth; source clause 18349.
private theorem sound077 : C.clause (decodeClause atoms clause077) := by
  exact C.covered_clause _ _ (C.growth_clause false 9 11 12 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 79: growth; source clause 19801.
private theorem sound078 : C.clause (decodeClause atoms clause078) := by
  exact C.covered_clause _ _ (C.growth_clause false 10 11 12 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 80: fixed_sign; source clause 22833.
private theorem sound079 : C.clause (decodeClause atoms clause079) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 1 2 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 81: fixed_sign; source clause 22835.
private theorem sound080 : C.clause (decodeClause atoms clause080) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 1 4 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 82: fixed_sign; source clause 22837.
private theorem sound081 : C.clause (decodeClause atoms clause081) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 1 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 83: fixed_sign; source clause 22838.
private theorem sound082 : C.clause (decodeClause atoms clause082) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 1 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 84: fixed_sign; source clause 22839.
private theorem sound083 : C.clause (decodeClause atoms clause083) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 1 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 85: fixed_sign; source clause 22840.
private theorem sound084 : C.clause (decodeClause atoms clause084) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 1 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 86: fixed_sign; source clause 22842.
private theorem sound085 : C.clause (decodeClause atoms clause085) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 4 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 87: fixed_sign; source clause 22844.
private theorem sound086 : C.clause (decodeClause atoms clause086) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 88: fixed_sign; source clause 22845.
private theorem sound087 : C.clause (decodeClause atoms clause087) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 89: fixed_sign; source clause 22846.
private theorem sound088 : C.clause (decodeClause atoms clause088) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 90: fixed_sign; source clause 22847.
private theorem sound089 : C.clause (decodeClause atoms clause089) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 91: fixed_sign; source clause 22850.
private theorem sound090 : C.clause (decodeClause atoms clause090) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 92: fixed_sign; source clause 22851.
private theorem sound091 : C.clause (decodeClause atoms clause091) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 4 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 93: fixed_sign; source clause 22852.
private theorem sound092 : C.clause (decodeClause atoms clause092) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 4 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 94: fixed_sign; source clause 22853.
private theorem sound093 : C.clause (decodeClause atoms clause093) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 4 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 95: fixed_sign; source clause 22854.
private theorem sound094 : C.clause (decodeClause atoms clause094) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 4 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 96: fixed_sign; source clause 22857.
private theorem sound095 : C.clause (decodeClause atoms clause095) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 4 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 97: fixed_sign; source clause 22858.
private theorem sound096 : C.clause (decodeClause atoms clause096) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 6 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 98: fixed_sign; source clause 22859.
private theorem sound097 : C.clause (decodeClause atoms clause097) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 6 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 99: fixed_sign; source clause 22860.
private theorem sound098 : C.clause (decodeClause atoms clause098) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 6 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 100: fixed_sign; source clause 22863.
private theorem sound099 : C.clause (decodeClause atoms clause099) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 6 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 101: fixed_sign; source clause 22864.
private theorem sound100 : C.clause (decodeClause atoms clause100) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 7 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 102: fixed_sign; source clause 22869.
private theorem sound101 : C.clause (decodeClause atoms clause101) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 4 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 103: fixed_sign; source clause 22871.
private theorem sound102 : C.clause (decodeClause atoms clause102) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 104: fixed_sign; source clause 22872.
private theorem sound103 : C.clause (decodeClause atoms clause103) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 105: fixed_sign; source clause 22873.
private theorem sound104 : C.clause (decodeClause atoms clause104) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 106: fixed_sign; source clause 22874.
private theorem sound105 : C.clause (decodeClause atoms clause105) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 107: fixed_sign; source clause 22875.
private theorem sound106 : C.clause (decodeClause atoms clause106) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 3 5 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 108: fixed_sign; source clause 22877.
private theorem sound107 : C.clause (decodeClause atoms clause107) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 3 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 109: fixed_sign; source clause 22878.
private theorem sound108 : C.clause (decodeClause atoms clause108) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 3 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 110: fixed_sign; source clause 22879.
private theorem sound109 : C.clause (decodeClause atoms clause109) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 3 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 111: fixed_sign; source clause 22880.
private theorem sound110 : C.clause (decodeClause atoms clause110) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 3 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 112: fixed_sign; source clause 22881.
private theorem sound111 : C.clause (decodeClause atoms clause111) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 3 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 113: fixed_sign; source clause 22882.
private theorem sound112 : C.clause (decodeClause atoms clause112) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 114: fixed_sign; source clause 22883.
private theorem sound113 : C.clause (decodeClause atoms clause113) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 115: fixed_sign; source clause 22884.
private theorem sound114 : C.clause (decodeClause atoms clause114) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 116: fixed_sign; source clause 22885.
private theorem sound115 : C.clause (decodeClause atoms clause115) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 117: fixed_sign; source clause 22887.
private theorem sound116 : C.clause (decodeClause atoms clause116) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 5 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 118: fixed_sign; source clause 22888.
private theorem sound117 : C.clause (decodeClause atoms clause117) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 5 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 119: fixed_sign; source clause 22889.
private theorem sound118 : C.clause (decodeClause atoms clause118) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 5 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 120: fixed_sign; source clause 22890.
private theorem sound119 : C.clause (decodeClause atoms clause119) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 5 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 121: fixed_sign; source clause 22891.
private theorem sound120 : C.clause (decodeClause atoms clause120) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 5 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 122: fixed_sign; source clause 22892.
private theorem sound121 : C.clause (decodeClause atoms clause121) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 123: fixed_sign; source clause 22893.
private theorem sound122 : C.clause (decodeClause atoms clause122) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 124: fixed_sign; source clause 22894.
private theorem sound123 : C.clause (decodeClause atoms clause123) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 125: fixed_sign; source clause 22895.
private theorem sound124 : C.clause (decodeClause atoms clause124) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 7 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 126: fixed_sign; source clause 22896.
private theorem sound125 : C.clause (decodeClause atoms clause125) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 7 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 127: fixed_sign; source clause 22898.
private theorem sound126 : C.clause (decodeClause atoms clause126) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 8 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 128: fixed_sign; source clause 22899.
private theorem sound127 : C.clause (decodeClause atoms clause127) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 8 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 129: fixed_sign; source clause 22900.
private theorem sound128 : C.clause (decodeClause atoms clause128) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 8 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 130: fixed_sign; source clause 22901.
private theorem sound129 : C.clause (decodeClause atoms clause129) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 8 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 131: fixed_sign; source clause 22902.
private theorem sound130 : C.clause (decodeClause atoms clause130) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 9 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 132: fixed_sign; source clause 22903.
private theorem sound131 : C.clause (decodeClause atoms clause131) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 9 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 133: fixed_sign; source clause 22904.
private theorem sound132 : C.clause (decodeClause atoms clause132) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 10 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 134: fixed_sign; source clause 22905.
private theorem sound133 : C.clause (decodeClause atoms clause133) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 10 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 135: fixed_sign; source clause 22906.
private theorem sound134 : C.clause (decodeClause atoms clause134) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 136: fixed_sign; source clause 22911.
private theorem sound135 : C.clause (decodeClause atoms clause135) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 137: fixed_sign; source clause 22912.
private theorem sound136 : C.clause (decodeClause atoms clause136) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 138: fixed_sign; source clause 22913.
private theorem sound137 : C.clause (decodeClause atoms clause137) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 139: fixed_sign; source clause 22914.
private theorem sound138 : C.clause (decodeClause atoms clause138) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 140: fixed_sign; source clause 22917.
private theorem sound139 : C.clause (decodeClause atoms clause139) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 141: fixed_sign; source clause 22918.
private theorem sound140 : C.clause (decodeClause atoms clause140) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 6 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 142: fixed_sign; source clause 22919.
private theorem sound141 : C.clause (decodeClause atoms clause141) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 6 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 143: fixed_sign; source clause 22920.
private theorem sound142 : C.clause (decodeClause atoms clause142) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 6 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 144: fixed_sign; source clause 22923.
private theorem sound143 : C.clause (decodeClause atoms clause143) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 6 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 145: fixed_sign; source clause 22924.
private theorem sound144 : C.clause (decodeClause atoms clause144) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 7 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 146: fixed_sign; source clause 22931.
private theorem sound145 : C.clause (decodeClause atoms clause145) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 147: fixed_sign; source clause 22932.
private theorem sound146 : C.clause (decodeClause atoms clause146) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 148: fixed_sign; source clause 22933.
private theorem sound147 : C.clause (decodeClause atoms clause147) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 149: fixed_sign; source clause 22934.
private theorem sound148 : C.clause (decodeClause atoms clause148) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 150: fixed_sign; source clause 22935.
private theorem sound149 : C.clause (decodeClause atoms clause149) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 151: fixed_sign; source clause 22939.
private theorem sound150 : C.clause (decodeClause atoms clause150) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 8 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 152: fixed_sign; source clause 22940.
private theorem sound151 : C.clause (decodeClause atoms clause151) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 8 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 153: fixed_sign; source clause 22941.
private theorem sound152 : C.clause (decodeClause atoms clause152) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 8 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 154: fixed_sign; source clause 22942.
private theorem sound153 : C.clause (decodeClause atoms clause153) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 8 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 155: fixed_sign; source clause 22943.
private theorem sound154 : C.clause (decodeClause atoms clause154) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 10 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 156: fixed_sign; source clause 22944.
private theorem sound155 : C.clause (decodeClause atoms clause155) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 10 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 157: fixed_sign; source clause 22945.
private theorem sound156 : C.clause (decodeClause atoms clause156) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 158: fixed_sign; source clause 22948.
private theorem sound157 : C.clause (decodeClause atoms clause157) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 6 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 159: fixed_sign; source clause 22949.
private theorem sound158 : C.clause (decodeClause atoms clause158) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 6 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 160: fixed_sign; source clause 22950.
private theorem sound159 : C.clause (decodeClause atoms clause159) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 6 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 161: fixed_sign; source clause 22953.
private theorem sound160 : C.clause (decodeClause atoms clause160) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 6 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 162: fixed_sign; source clause 22954.
private theorem sound161 : C.clause (decodeClause atoms clause161) := by
  exact C.covered_clause _ _ (C.fixed_negative 4 7 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 163: fixed_sign; source clause 22961.
private theorem sound162 : C.clause (decodeClause atoms clause162) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 8 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 164: fixed_sign; source clause 22962.
private theorem sound163 : C.clause (decodeClause atoms clause163) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 8 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 165: fixed_sign; source clause 22963.
private theorem sound164 : C.clause (decodeClause atoms clause164) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 8 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 166: fixed_sign; source clause 22964.
private theorem sound165 : C.clause (decodeClause atoms clause165) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 8 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 167: fixed_sign; source clause 22965.
private theorem sound166 : C.clause (decodeClause atoms clause166) := by
  exact C.covered_clause _ _ (C.fixed_negative 5 10 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 168: fixed_sign; source clause 22966.
private theorem sound167 : C.clause (decodeClause atoms clause167) := by
  exact C.covered_clause _ _ (C.fixed_negative 5 10 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 169: fixed_sign; source clause 22967.
private theorem sound168 : C.clause (decodeClause atoms clause168) := by
  exact C.covered_clause _ _ (C.fixed_negative 5 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 170: fixed_sign; source clause 22968.
private theorem sound169 : C.clause (decodeClause atoms clause169) := by
  exact C.covered_clause _ _ (C.fixed_negative 6 7 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 171: fixed_sign; source clause 22972.
private theorem sound170 : C.clause (decodeClause atoms clause170) := by
  exact C.covered_clause _ _ (C.fixed_positive 7 8 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 172: fixed_sign; source clause 22978.
private theorem sound171 : C.clause (decodeClause atoms clause171) := by
  exact C.covered_clause _ _ (C.fixed_negative 8 10 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 173: fixed_sign; source clause 22979.
private theorem sound172 : C.clause (decodeClause atoms clause172) := by
  exact C.covered_clause _ _ (C.fixed_negative 8 10 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 174: fixed_sign; source clause 22980.
private theorem sound173 : C.clause (decodeClause atoms clause173) := by
  exact C.covered_clause _ _ (C.fixed_negative 8 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 175: fixed_sign; source clause 22981.
private theorem sound174 : C.clause (decodeClause atoms clause174) := by
  exact C.covered_clause _ _ (C.fixed_negative 9 10 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 176: fixed_sign; source clause 22982.
private theorem sound175 : C.clause (decodeClause atoms clause175) := by
  exact C.covered_clause _ _ (C.fixed_negative 9 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 177: fixed_sign; source clause 22983.
private theorem sound176 : C.clause (decodeClause atoms clause176) := by
  exact C.covered_clause _ _ (C.fixed_negative 10 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 178: convex_four; source clause 23387.
private theorem sound177 : C.clause (decodeClause atoms clause177) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 179: convex_four; source clause 23803.
private theorem sound178 : C.clause (decodeClause atoms clause178) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 180: convex_four; source clause 24011.
private theorem sound179 : C.clause (decodeClause atoms clause179) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 181: convex_four; source clause 24219.
private theorem sound180 : C.clause (decodeClause atoms clause180) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 182: convex_four; source clause 24427.
private theorem sound181 : C.clause (decodeClause atoms clause181) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 183: packet; source clause 24856.
private theorem sound182 : C.clause (decodeClause atoms clause182) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 2 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 184: convex_four; source clause 25051.
private theorem sound183 : C.clause (decodeClause atoms clause183) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 185: convex_four; source clause 27339.
private theorem sound184 : C.clause (decodeClause atoms clause184) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 186: convex_four; source clause 27547.
private theorem sound185 : C.clause (decodeClause atoms clause185) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 187: convex_four; source clause 27755.
private theorem sound186 : C.clause (decodeClause atoms clause186) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 188: convex_four; source clause 27963.
private theorem sound187 : C.clause (decodeClause atoms clause187) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 189: packet; source clause 28392.
private theorem sound188 : C.clause (decodeClause atoms clause188) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 190: convex_four; source clause 28587.
private theorem sound189 : C.clause (decodeClause atoms clause189) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 191: convex_four; source clause 30251.
private theorem sound190 : C.clause (decodeClause atoms clause190) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 192: convex_four; source clause 30459.
private theorem sound191 : C.clause (decodeClause atoms clause191) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 193: convex_four; source clause 30667.
private theorem sound192 : C.clause (decodeClause atoms clause192) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 194: packet; source clause 31096.
private theorem sound193 : C.clause (decodeClause atoms clause193) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 195: convex_four; source clause 31291.
private theorem sound194 : C.clause (decodeClause atoms clause194) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 196: convex_four; source clause 31496.
private theorem sound195 : C.clause (decodeClause atoms clause195) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 197: convex_four; source clause 31704.
private theorem sound196 : C.clause (decodeClause atoms clause196) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 198: convex_four; source clause 32328.
private theorem sound197 : C.clause (decodeClause atoms clause197) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 199: packet; source clause 32352.
private theorem sound198 : C.clause (decodeClause atoms clause198) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 9 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 200: convex_four; source clause 32539.
private theorem sound199 : C.clause (decodeClause atoms clause199) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 201: packet; source clause 33593.
private theorem sound200 : C.clause (decodeClause atoms clause200) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 202: convex_four; source clause 33784.
private theorem sound201 : C.clause (decodeClause atoms clause201) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 203: convex_four; source clause 36711.
private theorem sound202 : C.clause (decodeClause atoms clause202) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 204: convex_four; source clause 36919.
private theorem sound203 : C.clause (decodeClause atoms clause203) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 4 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 205: convex_four; source clause 37127.
private theorem sound204 : C.clause (decodeClause atoms clause204) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 206: convex_four; source clause 37335.
private theorem sound205 : C.clause (decodeClause atoms clause205) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 4 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 207: convex_four; source clause 37959.
private theorem sound206 : C.clause (decodeClause atoms clause206) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 208: convex_four; source clause 39623.
private theorem sound207 : C.clause (decodeClause atoms clause207) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 209: convex_four; source clause 39831.
private theorem sound208 : C.clause (decodeClause atoms clause208) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 210: convex_four; source clause 40039.
private theorem sound209 : C.clause (decodeClause atoms clause209) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 6 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 211: convex_four; source clause 40663.
private theorem sound210 : C.clause (decodeClause atoms clause210) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 212: packet; source clause 40671.
private theorem sound211 : C.clause (decodeClause atoms clause211) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 213: convex_four; source clause 40868.
private theorem sound212 : C.clause (decodeClause atoms clause212) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 214: convex_four; source clause 41076.
private theorem sound213 : C.clause (decodeClause atoms clause213) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 215: convex_four; source clause 41700.
private theorem sound214 : C.clause (decodeClause atoms clause214) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 216: packet; source clause 41719.
private theorem sound215 : C.clause (decodeClause atoms clause215) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 9 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 217: convex_four; source clause 41911.
private theorem sound216 : C.clause (decodeClause atoms clause216) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 218: convex_four; source clause 43156.
private theorem sound217 : C.clause (decodeClause atoms clause217) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 219: convex_four; source clause 52935.
private theorem sound218 : C.clause (decodeClause atoms clause218) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 220: convex_four; source clause 53143.
private theorem sound219 : C.clause (decodeClause atoms clause219) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 221: convex_four; source clause 53351.
private theorem sound220 : C.clause (decodeClause atoms clause220) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 6 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 222: convex_four; source clause 53975.
private theorem sound221 : C.clause (decodeClause atoms clause221) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 223: packet; source clause 53983.
private theorem sound222 : C.clause (decodeClause atoms clause222) := by
  exact C.covered_clause _ _ (C.packet_clause 0 4 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 224: packet; source clause 53992.
private theorem sound223 : C.clause (decodeClause atoms clause223) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 225: convex_four; source clause 54180.
private theorem sound224 : C.clause (decodeClause atoms clause224) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 226: convex_four; source clause 54388.
private theorem sound225 : C.clause (decodeClause atoms clause225) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 227: packet; source clause 54824.
private theorem sound226 : C.clause (decodeClause atoms clause226) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 228: convex_four; source clause 55012.
private theorem sound227 : C.clause (decodeClause atoms clause227) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 229: packet; source clause 55031.
private theorem sound228 : C.clause (decodeClause atoms clause228) := by
  exact C.covered_clause _ _ (C.packet_clause 0 4 9 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 230: convex_four; source clause 55223.
private theorem sound229 : C.clause (decodeClause atoms clause229) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 231: convex_four; source clause 56468.
private theorem sound230 : C.clause (decodeClause atoms clause230) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 232: convex_four; source clause 61668.
private theorem sound231 : C.clause (decodeClause atoms clause231) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 233: convex_four; source clause 61876.
private theorem sound232 : C.clause (decodeClause atoms clause232) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 234: packet; source clause 62303.
private theorem sound233 : C.clause (decodeClause atoms clause233) := by
  exact C.covered_clause _ _ (C.packet_clause 0 6 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 235: packet; source clause 62312.
private theorem sound234 : C.clause (decodeClause atoms clause234) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 236: convex_four; source clause 62500.
private theorem sound235 : C.clause (decodeClause atoms clause235) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 237: packet; source clause 62519.
private theorem sound236 : C.clause (decodeClause atoms clause236) := by
  exact C.covered_clause _ _ (C.packet_clause 0 6 9 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 238: convex_four; source clause 62711.
private theorem sound237 : C.clause (decodeClause atoms clause237) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 239: convex_four; source clause 63956.
private theorem sound238 : C.clause (decodeClause atoms clause238) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 240: packet; source clause 64593.
private theorem sound239 : C.clause (decodeClause atoms clause239) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 9 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 241: convex_four; source clause 64779.
private theorem sound240 : C.clause (decodeClause atoms clause240) := by
  exact C.covered_clause _ _ (C.convex_clause 0 7 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 242: packet; source clause 65833.
private theorem sound241 : C.clause (decodeClause atoms clause241) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 243: convex_four; source clause 66024.
private theorem sound242 : C.clause (decodeClause atoms clause242) := by
  exact C.covered_clause _ _ (C.convex_clause 0 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 244: convex_four; source clause 71031.
private theorem sound243 : C.clause (decodeClause atoms clause243) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 245: convex_four; source clause 71239.
private theorem sound244 : C.clause (decodeClause atoms clause244) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 4 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 246: convex_four; source clause 71447.
private theorem sound245 : C.clause (decodeClause atoms clause245) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 247: convex_four; source clause 71655.
private theorem sound246 : C.clause (decodeClause atoms clause246) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 4 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 248: packet; source clause 72078.
private theorem sound247 : C.clause (decodeClause atoms clause247) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 249: convex_four; source clause 72279.
private theorem sound248 : C.clause (decodeClause atoms clause248) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 250: convex_four; source clause 73943.
private theorem sound249 : C.clause (decodeClause atoms clause249) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 251: convex_four; source clause 74151.
private theorem sound250 : C.clause (decodeClause atoms clause250) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 252: convex_four; source clause 74359.
private theorem sound251 : C.clause (decodeClause atoms clause251) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 253: convex_four; source clause 74983.
private theorem sound252 : C.clause (decodeClause atoms clause252) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 254: packet; source clause 75000.
private theorem sound253 : C.clause (decodeClause atoms clause253) := by
  exact C.covered_clause _ _ (C.packet_clause 1 7 2 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 255: convex_four; source clause 75188.
private theorem sound254 : C.clause (decodeClause atoms clause254) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 256: convex_four; source clause 75396.
private theorem sound255 : C.clause (decodeClause atoms clause255) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 257: packet; source clause 75865.
private theorem sound256 : C.clause (decodeClause atoms clause256) := by
  exact C.covered_clause _ _ (C.packet_clause 2 1 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 258: convex_four; source clause 76020.
private theorem sound257 : C.clause (decodeClause atoms clause257) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 259: packet; source clause 76056.
private theorem sound258 : C.clause (decodeClause atoms clause258) := by
  exact C.covered_clause _ _ (C.packet_clause 1 9 2 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 260: convex_four; source clause 76231.
private theorem sound259 : C.clause (decodeClause atoms clause259) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 261: convex_four; source clause 77476.
private theorem sound260 : C.clause (decodeClause atoms clause260) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 262: convex_four; source clause 80391.
private theorem sound261 : C.clause (decodeClause atoms clause261) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 263: convex_four; source clause 80599.
private theorem sound262 : C.clause (decodeClause atoms clause262) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 264: convex_four; source clause 80807.
private theorem sound263 : C.clause (decodeClause atoms clause263) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 265: convex_four; source clause 81015.
private theorem sound264 : C.clause (decodeClause atoms clause264) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 5 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 266: convex_four; source clause 81223.
private theorem sound265 : C.clause (decodeClause atoms clause265) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 267: convex_four; source clause 83719.
private theorem sound266 : C.clause (decodeClause atoms clause266) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 268: convex_four; source clause 83927.
private theorem sound267 : C.clause (decodeClause atoms clause267) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 269: convex_four; source clause 84135.
private theorem sound268 : C.clause (decodeClause atoms clause268) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 270: convex_four; source clause 84343.
private theorem sound269 : C.clause (decodeClause atoms clause269) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 271: packet; source clause 84359.
private theorem sound270 : C.clause (decodeClause atoms clause270) := by
  exact C.covered_clause _ _ (C.packet_clause 1 3 10 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 272: convex_four; source clause 84551.
private theorem sound271 : C.clause (decodeClause atoms clause271) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 273: convex_four; source clause 84759.
private theorem sound272 : C.clause (decodeClause atoms clause272) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 274: convex_four; source clause 84967.
private theorem sound273 : C.clause (decodeClause atoms clause273) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 275: convex_four; source clause 85172.
private theorem sound274 : C.clause (decodeClause atoms clause274) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 276: convex_four; source clause 85380.
private theorem sound275 : C.clause (decodeClause atoms clause275) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 277: convex_four; source clause 85588.
private theorem sound276 : C.clause (decodeClause atoms clause276) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 278: convex_four; source clause 87255.
private theorem sound277 : C.clause (decodeClause atoms clause277) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 279: convex_four; source clause 87463.
private theorem sound278 : C.clause (decodeClause atoms clause278) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 280: convex_four; source clause 87671.
private theorem sound279 : C.clause (decodeClause atoms clause279) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 281: packet; source clause 88094.
private theorem sound280 : C.clause (decodeClause atoms clause280) := by
  exact C.covered_clause _ _ (C.packet_clause 1 4 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 282: packet; source clause 88095.
private theorem sound281 : C.clause (decodeClause atoms clause281) := by
  exact C.covered_clause _ _ (C.packet_clause 1 4 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 283: convex_four; source clause 88295.
private theorem sound282 : C.clause (decodeClause atoms clause282) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 284: convex_four; source clause 88500.
private theorem sound283 : C.clause (decodeClause atoms clause283) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 285: convex_four; source clause 88708.
private theorem sound284 : C.clause (decodeClause atoms clause284) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 286: packet; source clause 89177.
private theorem sound285 : C.clause (decodeClause atoms clause285) := by
  exact C.covered_clause _ _ (C.packet_clause 4 1 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 287: convex_four; source clause 89332.
private theorem sound286 : C.clause (decodeClause atoms clause286) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 288: packet; source clause 89368.
private theorem sound287 : C.clause (decodeClause atoms clause287) := by
  exact C.covered_clause _ _ (C.packet_clause 1 9 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 289: convex_four; source clause 89543.
private theorem sound288 : C.clause (decodeClause atoms clause288) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 290: convex_four; source clause 90788.
private theorem sound289 : C.clause (decodeClause atoms clause289) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 291: convex_four; source clause 93911.
private theorem sound290 : C.clause (decodeClause atoms clause290) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 292: convex_four; source clause 94119.
private theorem sound291 : C.clause (decodeClause atoms clause291) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 293: convex_four; source clause 94327.
private theorem sound292 : C.clause (decodeClause atoms clause292) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 294: convex_four; source clause 94535.
private theorem sound293 : C.clause (decodeClause atoms clause293) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 295: packet; source clause 94551.
private theorem sound294 : C.clause (decodeClause atoms clause294) := by
  exact C.covered_clause _ _ (C.packet_clause 1 5 10 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 296: convex_four; source clause 94743.
private theorem sound295 : C.clause (decodeClause atoms clause295) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 297: convex_four; source clause 94951.
private theorem sound296 : C.clause (decodeClause atoms clause296) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 298: packet; source clause 94959.
private theorem sound297 : C.clause (decodeClause atoms clause297) := by
  exact C.covered_clause _ _ (C.packet_clause 1 5 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 299: convex_four; source clause 95159.
private theorem sound298 : C.clause (decodeClause atoms clause298) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 300: convex_four; source clause 95364.
private theorem sound299 : C.clause (decodeClause atoms clause299) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 301: convex_four; source clause 95572.
private theorem sound300 : C.clause (decodeClause atoms clause300) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 302: convex_four; source clause 95780.
private theorem sound301 : C.clause (decodeClause atoms clause301) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 303: packet; source clause 95800.
private theorem sound302 : C.clause (decodeClause atoms clause302) := by
  exact C.covered_clause _ _ (C.packet_clause 1 7 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 304: convex_four; source clause 95988.
private theorem sound303 : C.clause (decodeClause atoms clause303) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 305: convex_four; source clause 96196.
private theorem sound304 : C.clause (decodeClause atoms clause304) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 306: packet; source clause 96665.
private theorem sound305 : C.clause (decodeClause atoms clause305) := by
  exact C.covered_clause _ _ (C.packet_clause 6 1 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 307: convex_four; source clause 96820.
private theorem sound306 : C.clause (decodeClause atoms clause306) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 308: packet; source clause 96856.
private theorem sound307 : C.clause (decodeClause atoms clause307) := by
  exact C.covered_clause _ _ (C.packet_clause 1 9 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 309: convex_four; source clause 97031.
private theorem sound308 : C.clause (decodeClause atoms clause308) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 310: packet; source clause 97453.
private theorem sound309 : C.clause (decodeClause atoms clause309) := by
  exact C.covered_clause _ _ (C.packet_clause 1 6 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 311: packet; source clause 97454.
private theorem sound310 : C.clause (decodeClause atoms clause310) := by
  exact C.covered_clause _ _ (C.packet_clause 1 6 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 312: convex_four; source clause 98276.
private theorem sound311 : C.clause (decodeClause atoms clause311) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 313: convex_four; source clause 99099.
private theorem sound312 : C.clause (decodeClause atoms clause312) := by
  exact C.covered_clause _ _ (C.convex_clause 1 7 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 314: packet; source clause 100152.
private theorem sound313 : C.clause (decodeClause atoms clause313) := by
  exact C.covered_clause _ _ (C.packet_clause 1 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 315: packet; source clause 100153.
private theorem sound314 : C.clause (decodeClause atoms clause314) := by
  exact C.covered_clause _ _ (C.packet_clause 1 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 316: packet; source clause 100155.
private theorem sound315 : C.clause (decodeClause atoms clause315) := by
  exact C.covered_clause _ _ (C.packet_clause 1 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 317: convex_four; source clause 100344.
private theorem sound316 : C.clause (decodeClause atoms clause316) := by
  exact C.covered_clause _ _ (C.convex_clause 1 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 318: packet; source clause 100999.
private theorem sound317 : C.clause (decodeClause atoms clause317) := by
  exact C.covered_clause _ _ (C.packet_clause 1 8 10 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 319: packet; source clause 101016.
private theorem sound318 : C.clause (decodeClause atoms clause318) := by
  exact C.covered_clause _ _ (C.packet_clause 1 10 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 320: convex_four; source clause 101191.
private theorem sound319 : C.clause (decodeClause atoms clause319) := by
  exact C.covered_clause _ _ (C.convex_clause 1 8 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 321: convex_four; source clause 101399.
private theorem sound320 : C.clause (decodeClause atoms clause320) := by
  exact C.covered_clause _ _ (C.convex_clause 1 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 322: packet; source clause 101407.
private theorem sound321 : C.clause (decodeClause atoms clause321) := by
  exact C.covered_clause _ _ (C.packet_clause 1 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 323: convex_four; source clause 101607.
private theorem sound322 : C.clause (decodeClause atoms clause322) := by
  exact C.covered_clause _ _ (C.convex_clause 1 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 324: convex_four; source clause 101812.
private theorem sound323 : C.clause (decodeClause atoms clause323) := by
  exact C.covered_clause _ _ (C.convex_clause 1 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 325: convex_four; source clause 102020.
private theorem sound324 : C.clause (decodeClause atoms clause324) := by
  exact C.covered_clause _ _ (C.convex_clause 1 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 326: convex_four; source clause 102228.
private theorem sound325 : C.clause (decodeClause atoms clause325) := by
  exact C.covered_clause _ _ (C.convex_clause 1 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 327: convex_four; source clause 102436.
private theorem sound326 : C.clause (decodeClause atoms clause326) := by
  exact C.covered_clause _ _ (C.convex_clause 1 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 328: packet; source clause 102456.
private theorem sound327 : C.clause (decodeClause atoms clause327) := by
  exact C.covered_clause _ _ (C.packet_clause 1 10 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 329: convex_four; source clause 102644.
private theorem sound328 : C.clause (decodeClause atoms clause328) := by
  exact C.covered_clause _ _ (C.convex_clause 1 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 330: convex_four; source clause 102852.
private theorem sound329 : C.clause (decodeClause atoms clause329) := by
  exact C.covered_clause _ _ (C.convex_clause 1 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 331: convex_four; source clause 103048.
private theorem sound330 : C.clause (decodeClause atoms clause330) := by
  exact C.covered_clause _ _ (C.convex_clause 1 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 332: convex_four; source clause 112215.
private theorem sound331 : C.clause (decodeClause atoms clause331) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 333: convex_four; source clause 112423.
private theorem sound332 : C.clause (decodeClause atoms clause332) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 334: convex_four; source clause 112631.
private theorem sound333 : C.clause (decodeClause atoms clause333) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 6 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 335: convex_four; source clause 113255.
private theorem sound334 : C.clause (decodeClause atoms clause334) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 336: convex_four; source clause 113460.
private theorem sound335 : C.clause (decodeClause atoms clause335) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 337: convex_four; source clause 113668.
private theorem sound336 : C.clause (decodeClause atoms clause336) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 338: packet; source clause 114190.
private theorem sound337 : C.clause (decodeClause atoms clause337) := by
  exact C.covered_clause _ _ (C.packet_clause 7 2 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 339: convex_four; source clause 114292.
private theorem sound338 : C.clause (decodeClause atoms clause338) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 340: convex_four; source clause 114503.
private theorem sound339 : C.clause (decodeClause atoms clause339) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 341: convex_four; source clause 115748.
private theorem sound340 : C.clause (decodeClause atoms clause340) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 342: convex_four; source clause 120948.
private theorem sound341 : C.clause (decodeClause atoms clause341) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 343: convex_four; source clause 121156.
private theorem sound342 : C.clause (decodeClause atoms clause342) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 344: convex_four; source clause 121780.
private theorem sound343 : C.clause (decodeClause atoms clause343) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 345: convex_four; source clause 121782.
private theorem sound344 : C.clause (decodeClause atoms clause344) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true false) (by decide +kernel)

-- Clause 346: convex_four; source clause 121991.
private theorem sound345 : C.clause (decodeClause atoms clause345) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 347: convex_four; source clause 123236.
private theorem sound346 : C.clause (decodeClause atoms clause346) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 348: packet; source clause 123873.
private theorem sound347 : C.clause (decodeClause atoms clause347) := by
  exact C.covered_clause _ _ (C.packet_clause 2 7 9 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 349: convex_four; source clause 124059.
private theorem sound348 : C.clause (decodeClause atoms clause348) := by
  exact C.covered_clause _ _ (C.convex_clause 2 7 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 350: convex_four; source clause 124067.
private theorem sound349 : C.clause (decodeClause atoms clause349) := by
  exact C.covered_clause _ _ (C.convex_clause 2 7 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 351: packet; source clause 125113.
private theorem sound350 : C.clause (decodeClause atoms clause350) := by
  exact C.covered_clause _ _ (C.packet_clause 2 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 352: convex_four; source clause 125304.
private theorem sound351 : C.clause (decodeClause atoms clause351) := by
  exact C.covered_clause _ _ (C.convex_clause 2 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 353: convex_four; source clause 136343.
private theorem sound352 : C.clause (decodeClause atoms clause352) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 354: convex_four; source clause 136551.
private theorem sound353 : C.clause (decodeClause atoms clause353) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 355: convex_four; source clause 136759.
private theorem sound354 : C.clause (decodeClause atoms clause354) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 356: convex_four; source clause 136967.
private theorem sound355 : C.clause (decodeClause atoms clause355) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 357: packet; source clause 136975.
private theorem sound356 : C.clause (decodeClause atoms clause356) := by
  exact C.covered_clause _ _ (C.packet_clause 3 5 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 358: packet; source clause 137118.
private theorem sound357 : C.clause (decodeClause atoms clause357) := by
  exact C.covered_clause _ _ (C.packet_clause 10 3 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 359: convex_four; source clause 137175.
private theorem sound358 : C.clause (decodeClause atoms clause358) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 360: packet; source clause 137183.
private theorem sound359 : C.clause (decodeClause atoms clause359) := by
  exact C.covered_clause _ _ (C.packet_clause 3 5 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 361: convex_four; source clause 137383.
private theorem sound360 : C.clause (decodeClause atoms clause360) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 362: packet; source clause 137391.
private theorem sound361 : C.clause (decodeClause atoms clause361) := by
  exact C.covered_clause _ _ (C.packet_clause 3 5 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 363: convex_four; source clause 137591.
private theorem sound362 : C.clause (decodeClause atoms clause362) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 364: convex_four; source clause 137796.
private theorem sound363 : C.clause (decodeClause atoms clause363) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 365: convex_four; source clause 138004.
private theorem sound364 : C.clause (decodeClause atoms clause364) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 366: convex_four; source clause 138212.
private theorem sound365 : C.clause (decodeClause atoms clause365) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 367: convex_four; source clause 143623.
private theorem sound366 : C.clause (decodeClause atoms clause366) := by
  exact C.covered_clause _ _ (C.convex_clause 3 8 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 368: convex_four; source clause 143831.
private theorem sound367 : C.clause (decodeClause atoms clause367) := by
  exact C.covered_clause _ _ (C.convex_clause 3 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 369: convex_four; source clause 144039.
private theorem sound368 : C.clause (decodeClause atoms clause368) := by
  exact C.covered_clause _ _ (C.convex_clause 3 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 370: convex_four; source clause 144244.
private theorem sound369 : C.clause (decodeClause atoms clause369) := by
  exact C.covered_clause _ _ (C.convex_clause 3 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 371: convex_four; source clause 144452.
private theorem sound370 : C.clause (decodeClause atoms clause370) := by
  exact C.covered_clause _ _ (C.convex_clause 3 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 372: convex_four; source clause 144660.
private theorem sound371 : C.clause (decodeClause atoms clause371) := by
  exact C.covered_clause _ _ (C.convex_clause 3 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 373: convex_four; source clause 144868.
private theorem sound372 : C.clause (decodeClause atoms clause372) := by
  exact C.covered_clause _ _ (C.convex_clause 3 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 374: convex_four; source clause 145076.
private theorem sound373 : C.clause (decodeClause atoms clause373) := by
  exact C.covered_clause _ _ (C.convex_clause 3 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 375: convex_four; source clause 145284.
private theorem sound374 : C.clause (decodeClause atoms clause374) := by
  exact C.covered_clause _ _ (C.convex_clause 3 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 376: convex_four; source clause 145480.
private theorem sound375 : C.clause (decodeClause atoms clause375) := by
  exact C.covered_clause _ _ (C.convex_clause 3 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 377: convex_four; source clause 150068.
private theorem sound376 : C.clause (decodeClause atoms clause376) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 378: convex_four; source clause 150276.
private theorem sound377 : C.clause (decodeClause atoms clause377) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 379: convex_four; source clause 150900.
private theorem sound378 : C.clause (decodeClause atoms clause378) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 380: convex_four; source clause 151111.
private theorem sound379 : C.clause (decodeClause atoms clause379) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 381: convex_four; source clause 152356.
private theorem sound380 : C.clause (decodeClause atoms clause380) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 382: convex_four; source clause 153179.
private theorem sound381 : C.clause (decodeClause atoms clause381) := by
  exact C.covered_clause _ _ (C.convex_clause 4 7 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 383: packet; source clause 154233.
private theorem sound382 : C.clause (decodeClause atoms clause382) := by
  exact C.covered_clause _ _ (C.packet_clause 4 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 384: convex_four; source clause 154424.
private theorem sound383 : C.clause (decodeClause atoms clause383) := by
  exact C.covered_clause _ _ (C.convex_clause 4 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 385: packet; source clause 162351.
private theorem sound384 : C.clause (decodeClause atoms clause384) := by
  exact C.covered_clause _ _ (C.packet_clause 5 8 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 386: packet; source clause 162494.
private theorem sound385 : C.clause (decodeClause atoms clause385) := by
  exact C.covered_clause _ _ (C.packet_clause 10 5 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 387: convex_four; source clause 162551.
private theorem sound386 : C.clause (decodeClause atoms clause386) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 388: packet; source clause 162559.
private theorem sound387 : C.clause (decodeClause atoms clause387) := by
  exact C.covered_clause _ _ (C.packet_clause 5 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 389: convex_four; source clause 162759.
private theorem sound388 : C.clause (decodeClause atoms clause388) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 390: packet; source clause 162767.
private theorem sound389 : C.clause (decodeClause atoms clause389) := by
  exact C.covered_clause _ _ (C.packet_clause 5 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 391: packet; source clause 162860.
private theorem sound390 : C.clause (decodeClause atoms clause390) := by
  exact C.covered_clause _ _ (C.packet_clause 9 5 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 392: convex_four; source clause 162965.
private theorem sound391 : C.clause (decodeClause atoms clause391) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true) (by decide +kernel)

-- Clause 393: convex_four; source clause 162967.
private theorem sound392 : C.clause (decodeClause atoms clause392) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 394: convex_four; source clause 163172.
private theorem sound393 : C.clause (decodeClause atoms clause393) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 395: convex_four; source clause 163380.
private theorem sound394 : C.clause (decodeClause atoms clause394) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 396: convex_four; source clause 163588.
private theorem sound395 : C.clause (decodeClause atoms clause395) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 397: convex_four; source clause 163796.
private theorem sound396 : C.clause (decodeClause atoms clause396) := by
  exact C.covered_clause _ _ (C.convex_clause 5 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 398: convex_four; source clause 163996.
private theorem sound397 : C.clause (decodeClause atoms clause397) := by
  exact C.covered_clause _ _ (C.convex_clause 5 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 399: convex_four; source clause 164004.
private theorem sound398 : C.clause (decodeClause atoms clause398) := by
  exact C.covered_clause _ _ (C.convex_clause 5 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 400: convex_four; source clause 164204.
private theorem sound399 : C.clause (decodeClause atoms clause399) := by
  exact C.covered_clause _ _ (C.convex_clause 5 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 401: convex_four; source clause 164212.
private theorem sound400 : C.clause (decodeClause atoms clause400) := by
  exact C.covered_clause _ _ (C.convex_clause 5 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 402: convex_four; source clause 164408.
private theorem sound401 : C.clause (decodeClause atoms clause401) := by
  exact C.covered_clause _ _ (C.convex_clause 5 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 403: packet; source clause 164433.
private theorem sound402 : C.clause (decodeClause atoms clause402) := by
  exact C.covered_clause _ _ (C.packet_clause 6 7 9 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 404: packet; source clause 164435.
private theorem sound403 : C.clause (decodeClause atoms clause403) := by
  exact C.covered_clause _ _ (C.packet_clause 6 7 9 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 405: convex_four; source clause 164619.
private theorem sound404 : C.clause (decodeClause atoms clause404) := by
  exact C.covered_clause _ _ (C.convex_clause 6 7 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 406: convex_four; source clause 165864.
private theorem sound405 : C.clause (decodeClause atoms clause405) := by
  exact C.covered_clause _ _ (C.convex_clause 6 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 407: packet; source clause 169017.
private theorem sound406 : C.clause (decodeClause atoms clause406) := by
  exact C.covered_clause _ _ (C.packet_clause 7 9 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 408: packet; source clause 169019.
private theorem sound407 : C.clause (decodeClause atoms clause407) := by
  exact C.covered_clause _ _ (C.packet_clause 7 9 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 409: convex_four; source clause 169202.
private theorem sound408 : C.clause (decodeClause atoms clause408) := by
  exact C.covered_clause _ _ (C.convex_clause 7 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false) (by decide +kernel)

-- Clause 410: convex_four; source clause 169203.
private theorem sound409 : C.clause (decodeClause atoms clause409) := by
  exact C.covered_clause _ _ (C.convex_clause 7 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 411: convex_four; source clause 169206.
private theorem sound410 : C.clause (decodeClause atoms clause410) := by
  exact C.covered_clause _ _ (C.convex_clause 7 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true false) (by decide +kernel)

-- Clause 412: convex_four; source clause 169207.
private theorem sound411 : C.clause (decodeClause atoms clause411) := by
  exact C.covered_clause _ _ (C.convex_clause 7 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 413: convex_four; source clause 170868.
private theorem sound412 : C.clause (decodeClause atoms clause412) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 414: convex_four; source clause 171068.
private theorem sound413 : C.clause (decodeClause atoms clause413) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 415: convex_four; source clause 171072.
private theorem sound414 : C.clause (decodeClause atoms clause414) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 416: convex_four; source clause 171076.
private theorem sound415 : C.clause (decodeClause atoms clause415) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 417: convex_four; source clause 171276.
private theorem sound416 : C.clause (decodeClause atoms clause416) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 418: convex_four; source clause 171284.
private theorem sound417 : C.clause (decodeClause atoms clause417) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 419: convex_four; source clause 171480.
private theorem sound418 : C.clause (decodeClause atoms clause418) := by
  exact C.covered_clause _ _ (C.convex_clause 8 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 420: packet; source clause 171497.
private theorem sound419 : C.clause (decodeClause atoms clause419) := by
  exact C.covered_clause _ _ (C.packet_clause 9 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 421: convex_four; source clause 171688.
private theorem sound420 : C.clause (decodeClause atoms clause420) := by
  exact C.covered_clause _ _ (C.convex_clause 9 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 422: convex_four; source clause 171692.
private theorem sound421 : C.clause (decodeClause atoms clause421) := by
  exact C.covered_clause _ _ (C.convex_clause 9 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 423: no_octagon; source clause 171706.
private theorem sound422 : C.clause (decodeClause atoms clause422) := by
  exact C.no_octagon_clause {0, 1, 2, 4, 6, 7, 8, 9} (by decide +kernel) _ (by decide +kernel)

-- Clause 424: no_octagon; source clause 171709.
private theorem sound423 : C.clause (decodeClause atoms clause423) := by
  exact C.no_octagon_clause {0, 1, 2, 4, 6, 7, 9, 12} (by decide +kernel) _ (by decide +kernel)

-- Clause 425: no_octagon; source clause 171721.
private theorem sound424 : C.clause (decodeClause atoms clause424) := by
  exact C.no_octagon_clause {1, 3, 5, 8, 9, 10, 11, 12} (by decide +kernel) _ (by decide +kernel)

private theorem all_sound : List.Forall (fun cl => C.clause (decodeClause atoms cl)) clauses := by
  exact And.intro (sound000 C) (And.intro (sound001 C) (And.intro (sound002 C) (And.intro (sound003 C) (And.intro (sound004 C) (And.intro (sound005 C) (And.intro (sound006 C) (And.intro (sound007 C) (And.intro (sound008 C) (And.intro (sound009 C) (And.intro (sound010 C) (And.intro (sound011 C) (And.intro (sound012 C) (And.intro (sound013 C) (And.intro (sound014 C) (And.intro (sound015 C) (And.intro (sound016 C) (And.intro (sound017 C) (And.intro (sound018 C) (And.intro (sound019 C) (And.intro (sound020 C) (And.intro (sound021 C) (And.intro (sound022 C) (And.intro (sound023 C) (And.intro (sound024 C) (And.intro (sound025 C) (And.intro (sound026 C) (And.intro (sound027 C) (And.intro (sound028 C) (And.intro (sound029 C) (And.intro (sound030 C) (And.intro (sound031 C) (And.intro (sound032 C) (And.intro (sound033 C) (And.intro (sound034 C) (And.intro (sound035 C) (And.intro (sound036 C) (And.intro (sound037 C) (And.intro (sound038 C) (And.intro (sound039 C) (And.intro (sound040 C) (And.intro (sound041 C) (And.intro (sound042 C) (And.intro (sound043 C) (And.intro (sound044 C) (And.intro (sound045 C) (And.intro (sound046 C) (And.intro (sound047 C) (And.intro (sound048 C) (And.intro (sound049 C) (And.intro (sound050 C) (And.intro (sound051 C) (And.intro (sound052 C) (And.intro (sound053 C) (And.intro (sound054 C) (And.intro (sound055 C) (And.intro (sound056 C) (And.intro (sound057 C) (And.intro (sound058 C) (And.intro (sound059 C) (And.intro (sound060 C) (And.intro (sound061 C) (And.intro (sound062 C) (And.intro (sound063 C) (And.intro (sound064 C) (And.intro (sound065 C) (And.intro (sound066 C) (And.intro (sound067 C) (And.intro (sound068 C) (And.intro (sound069 C) (And.intro (sound070 C) (And.intro (sound071 C) (And.intro (sound072 C) (And.intro (sound073 C) (And.intro (sound074 C) (And.intro (sound075 C) (And.intro (sound076 C) (And.intro (sound077 C) (And.intro (sound078 C) (And.intro (sound079 C) (And.intro (sound080 C) (And.intro (sound081 C) (And.intro (sound082 C) (And.intro (sound083 C) (And.intro (sound084 C) (And.intro (sound085 C) (And.intro (sound086 C) (And.intro (sound087 C) (And.intro (sound088 C) (And.intro (sound089 C) (And.intro (sound090 C) (And.intro (sound091 C) (And.intro (sound092 C) (And.intro (sound093 C) (And.intro (sound094 C) (And.intro (sound095 C) (And.intro (sound096 C) (And.intro (sound097 C) (And.intro (sound098 C) (And.intro (sound099 C) (And.intro (sound100 C) (And.intro (sound101 C) (And.intro (sound102 C) (And.intro (sound103 C) (And.intro (sound104 C) (And.intro (sound105 C) (And.intro (sound106 C) (And.intro (sound107 C) (And.intro (sound108 C) (And.intro (sound109 C) (And.intro (sound110 C) (And.intro (sound111 C) (And.intro (sound112 C) (And.intro (sound113 C) (And.intro (sound114 C) (And.intro (sound115 C) (And.intro (sound116 C) (And.intro (sound117 C) (And.intro (sound118 C) (And.intro (sound119 C) (And.intro (sound120 C) (And.intro (sound121 C) (And.intro (sound122 C) (And.intro (sound123 C) (And.intro (sound124 C) (And.intro (sound125 C) (And.intro (sound126 C) (And.intro (sound127 C) (And.intro (sound128 C) (And.intro (sound129 C) (And.intro (sound130 C) (And.intro (sound131 C) (And.intro (sound132 C) (And.intro (sound133 C) (And.intro (sound134 C) (And.intro (sound135 C) (And.intro (sound136 C) (And.intro (sound137 C) (And.intro (sound138 C) (And.intro (sound139 C) (And.intro (sound140 C) (And.intro (sound141 C) (And.intro (sound142 C) (And.intro (sound143 C) (And.intro (sound144 C) (And.intro (sound145 C) (And.intro (sound146 C) (And.intro (sound147 C) (And.intro (sound148 C) (And.intro (sound149 C) (And.intro (sound150 C) (And.intro (sound151 C) (And.intro (sound152 C) (And.intro (sound153 C) (And.intro (sound154 C) (And.intro (sound155 C) (And.intro (sound156 C) (And.intro (sound157 C) (And.intro (sound158 C) (And.intro (sound159 C) (And.intro (sound160 C) (And.intro (sound161 C) (And.intro (sound162 C) (And.intro (sound163 C) (And.intro (sound164 C) (And.intro (sound165 C) (And.intro (sound166 C) (And.intro (sound167 C) (And.intro (sound168 C) (And.intro (sound169 C) (And.intro (sound170 C) (And.intro (sound171 C) (And.intro (sound172 C) (And.intro (sound173 C) (And.intro (sound174 C) (And.intro (sound175 C) (And.intro (sound176 C) (And.intro (sound177 C) (And.intro (sound178 C) (And.intro (sound179 C) (And.intro (sound180 C) (And.intro (sound181 C) (And.intro (sound182 C) (And.intro (sound183 C) (And.intro (sound184 C) (And.intro (sound185 C) (And.intro (sound186 C) (And.intro (sound187 C) (And.intro (sound188 C) (And.intro (sound189 C) (And.intro (sound190 C) (And.intro (sound191 C) (And.intro (sound192 C) (And.intro (sound193 C) (And.intro (sound194 C) (And.intro (sound195 C) (And.intro (sound196 C) (And.intro (sound197 C) (And.intro (sound198 C) (And.intro (sound199 C) (And.intro (sound200 C) (And.intro (sound201 C) (And.intro (sound202 C) (And.intro (sound203 C) (And.intro (sound204 C) (And.intro (sound205 C) (And.intro (sound206 C) (And.intro (sound207 C) (And.intro (sound208 C) (And.intro (sound209 C) (And.intro (sound210 C) (And.intro (sound211 C) (And.intro (sound212 C) (And.intro (sound213 C) (And.intro (sound214 C) (And.intro (sound215 C) (And.intro (sound216 C) (And.intro (sound217 C) (And.intro (sound218 C) (And.intro (sound219 C) (And.intro (sound220 C) (And.intro (sound221 C) (And.intro (sound222 C) (And.intro (sound223 C) (And.intro (sound224 C) (And.intro (sound225 C) (And.intro (sound226 C) (And.intro (sound227 C) (And.intro (sound228 C) (And.intro (sound229 C) (And.intro (sound230 C) (And.intro (sound231 C) (And.intro (sound232 C) (And.intro (sound233 C) (And.intro (sound234 C) (And.intro (sound235 C) (And.intro (sound236 C) (And.intro (sound237 C) (And.intro (sound238 C) (And.intro (sound239 C) (And.intro (sound240 C) (And.intro (sound241 C) (And.intro (sound242 C) (And.intro (sound243 C) (And.intro (sound244 C) (And.intro (sound245 C) (And.intro (sound246 C) (And.intro (sound247 C) (And.intro (sound248 C) (And.intro (sound249 C) (And.intro (sound250 C) (And.intro (sound251 C) (And.intro (sound252 C) (And.intro (sound253 C) (And.intro (sound254 C) (And.intro (sound255 C) (And.intro (sound256 C) (And.intro (sound257 C) (And.intro (sound258 C) (And.intro (sound259 C) (And.intro (sound260 C) (And.intro (sound261 C) (And.intro (sound262 C) (And.intro (sound263 C) (And.intro (sound264 C) (And.intro (sound265 C) (And.intro (sound266 C) (And.intro (sound267 C) (And.intro (sound268 C) (And.intro (sound269 C) (And.intro (sound270 C) (And.intro (sound271 C) (And.intro (sound272 C) (And.intro (sound273 C) (And.intro (sound274 C) (And.intro (sound275 C) (And.intro (sound276 C) (And.intro (sound277 C) (And.intro (sound278 C) (And.intro (sound279 C) (And.intro (sound280 C) (And.intro (sound281 C) (And.intro (sound282 C) (And.intro (sound283 C) (And.intro (sound284 C) (And.intro (sound285 C) (And.intro (sound286 C) (And.intro (sound287 C) (And.intro (sound288 C) (And.intro (sound289 C) (And.intro (sound290 C) (And.intro (sound291 C) (And.intro (sound292 C) (And.intro (sound293 C) (And.intro (sound294 C) (And.intro (sound295 C) (And.intro (sound296 C) (And.intro (sound297 C) (And.intro (sound298 C) (And.intro (sound299 C) (And.intro (sound300 C) (And.intro (sound301 C) (And.intro (sound302 C) (And.intro (sound303 C) (And.intro (sound304 C) (And.intro (sound305 C) (And.intro (sound306 C) (And.intro (sound307 C) (And.intro (sound308 C) (And.intro (sound309 C) (And.intro (sound310 C) (And.intro (sound311 C) (And.intro (sound312 C) (And.intro (sound313 C) (And.intro (sound314 C) (And.intro (sound315 C) (And.intro (sound316 C) (And.intro (sound317 C) (And.intro (sound318 C) (And.intro (sound319 C) (And.intro (sound320 C) (And.intro (sound321 C) (And.intro (sound322 C) (And.intro (sound323 C) (And.intro (sound324 C) (And.intro (sound325 C) (And.intro (sound326 C) (And.intro (sound327 C) (And.intro (sound328 C) (And.intro (sound329 C) (And.intro (sound330 C) (And.intro (sound331 C) (And.intro (sound332 C) (And.intro (sound333 C) (And.intro (sound334 C) (And.intro (sound335 C) (And.intro (sound336 C) (And.intro (sound337 C) (And.intro (sound338 C) (And.intro (sound339 C) (And.intro (sound340 C) (And.intro (sound341 C) (And.intro (sound342 C) (And.intro (sound343 C) (And.intro (sound344 C) (And.intro (sound345 C) (And.intro (sound346 C) (And.intro (sound347 C) (And.intro (sound348 C) (And.intro (sound349 C) (And.intro (sound350 C) (And.intro (sound351 C) (And.intro (sound352 C) (And.intro (sound353 C) (And.intro (sound354 C) (And.intro (sound355 C) (And.intro (sound356 C) (And.intro (sound357 C) (And.intro (sound358 C) (And.intro (sound359 C) (And.intro (sound360 C) (And.intro (sound361 C) (And.intro (sound362 C) (And.intro (sound363 C) (And.intro (sound364 C) (And.intro (sound365 C) (And.intro (sound366 C) (And.intro (sound367 C) (And.intro (sound368 C) (And.intro (sound369 C) (And.intro (sound370 C) (And.intro (sound371 C) (And.intro (sound372 C) (And.intro (sound373 C) (And.intro (sound374 C) (And.intro (sound375 C) (And.intro (sound376 C) (And.intro (sound377 C) (And.intro (sound378 C) (And.intro (sound379 C) (And.intro (sound380 C) (And.intro (sound381 C) (And.intro (sound382 C) (And.intro (sound383 C) (And.intro (sound384 C) (And.intro (sound385 C) (And.intro (sound386 C) (And.intro (sound387 C) (And.intro (sound388 C) (And.intro (sound389 C) (And.intro (sound390 C) (And.intro (sound391 C) (And.intro (sound392 C) (And.intro (sound393 C) (And.intro (sound394 C) (And.intro (sound395 C) (And.intro (sound396 C) (And.intro (sound397 C) (And.intro (sound398 C) (And.intro (sound399 C) (And.intro (sound400 C) (And.intro (sound401 C) (And.intro (sound402 C) (And.intro (sound403 C) (And.intro (sound404 C) (And.intro (sound405 C) (And.intro (sound406 C) (And.intro (sound407 C) (And.intro (sound408 C) (And.intro (sound409 C) (And.intro (sound410 C) (And.intro (sound411 C) (And.intro (sound412 C) (And.intro (sound413 C) (And.intro (sound414 C) (And.intro (sound415 C) (And.intro (sound416 C) (And.intro (sound417 C) (And.intro (sound418 C) (And.intro (sound419 C) (And.intro (sound420 C) (And.intro (sound421 C) (And.intro (sound422 C) (And.intro (sound423 C) (sound424 C))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

theorem context_impossible (C : Context 13 n states) : False := by
  have h : (C.valuation atoms).satisfies_fmla cnf_refutation.formula := by
    rw [formula_eq]
    constructor
    intro cl hc
    exact C.satisfies_of_clause atoms cl ((List.forall_iff_forall_mem.mp (all_sound C)) cl hc)
  exact cnf_refutation (C.valuation atoms) h

#print axioms context_impossible
end ErdosSzekeres.Omission.CoupledCoreFifth

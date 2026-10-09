import ErdosSzekeres.Omission.CoupledLrat
import ErdosSzekeres.Omission.CoupledSemantics

namespace ErdosSzekeres.Omission.CoupledCoreNine
open Coupled
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

lrat_raw cnf_refutation
  (include_str "../../experiments/omission-coupled-nine-2026-10-10/core9.cnf")
  (include_str "../../experiments/omission-coupled-nine-2026-10-10/core9.lrat")

def support : List (Fin 154) := [33, 43, 64, 68, 75, 87, 91, 99, 118]

def states : Fin 9 → Fin 154 := support.get

def atoms : List (Atom 9) := [
  .before 0 1,
  .capGe 0 1 2,
  .capGe 0 1 3,
  .capGe 0 1 4,
  .cupGe 0 1 2,
  .before 0 2,
  .before 0 3,
  .capGe 0 3 2,
  .capGe 0 3 3,
  .capGe 0 3 4,
  .cupGe 0 3 2,
  .before 0 4,
  .before 0 5,
  .before 0 6,
  .capGe 0 6 2,
  .capGe 0 6 3,
  .capGe 0 6 4,
  .cupGe 0 6 2,
  .before 0 7,
  .before 1 2,
  .cupGe 1 2 3,
  .before 1 3,
  .before 1 4,
  .before 1 6,
  .before 2 3,
  .before 2 4,
  .cupGe 2 4 4,
  .before 2 6,
  .before 2 8,
  .before 3 4,
  .capGe 3 4 2,
  .capGe 3 4 3,
  .capGe 3 4 4,
  .cupGe 3 4 3,
  .cupGe 3 4 4,
  .before 3 5,
  .before 3 6,
  .before 3 8,
  .before 4 5,
  .cupGe 4 5 5,
  .before 4 6,
  .before 4 7,
  .before 4 8,
  .before 5 6,
  .before 5 7,
  .cupGe 5 7 6,
  .before 5 8,
  .before 6 7,
  .before 6 8,
  .capGe 6 8 2,
  .capGe 6 8 3,
  .capGe 6 8 4,
  .cupGe 6 8 3,
  .cupGe 6 8 4,
  .cupGe 6 8 5,
  .cupGe 6 8 6,
  .before 7 8,
  .positive 0 1 2,
  .positive 0 1 3,
  .positive 0 1 4,
  .positive 0 1 5,
  .positive 0 1 6,
  .positive 0 1 7,
  .positive 0 1 8,
  .positive 0 2 4,
  .positive 0 2 5,
  .positive 0 2 6,
  .positive 0 2 7,
  .positive 0 2 8,
  .positive 0 3 4,
  .positive 0 3 6,
  .positive 0 3 8,
  .positive 0 4 5,
  .positive 0 4 6,
  .positive 0 4 7,
  .positive 0 4 8,
  .positive 0 5 6,
  .positive 0 5 7,
  .positive 0 5 8,
  .positive 0 6 7,
  .positive 0 6 8,
  .positive 0 7 8,
  .positive 1 2 3,
  .positive 1 2 4,
  .positive 1 2 5,
  .positive 1 2 6,
  .positive 1 2 7,
  .positive 1 2 8,
  .positive 1 3 4,
  .positive 1 3 5,
  .positive 1 3 6,
  .positive 1 3 7,
  .positive 1 3 8,
  .positive 1 4 5,
  .positive 1 4 6,
  .positive 1 4 7,
  .positive 1 4 8,
  .positive 1 5 6,
  .positive 1 5 7,
  .positive 1 5 8,
  .positive 1 6 7,
  .positive 1 6 8,
  .positive 1 7 8,
  .positive 2 3 4,
  .positive 2 3 5,
  .positive 2 3 6,
  .positive 2 3 7,
  .positive 2 3 8,
  .positive 2 4 5,
  .positive 2 4 6,
  .positive 2 4 7,
  .positive 2 4 8,
  .positive 2 5 6,
  .positive 2 5 7,
  .positive 2 5 8,
  .positive 2 6 7,
  .positive 2 6 8,
  .positive 2 7 8,
  .positive 3 4 5,
  .positive 3 4 6,
  .positive 3 4 7,
  .positive 3 4 8,
  .positive 3 5 6,
  .positive 3 5 7,
  .positive 3 5 8,
  .positive 3 6 7,
  .positive 3 6 8,
  .positive 3 7 8,
  .positive 4 5 6,
  .positive 4 5 7,
  .positive 4 5 8,
  .positive 4 6 7,
  .positive 4 6 8,
  .positive 4 7 8,
  .positive 5 6 7,
  .positive 5 6 8,
  .positive 5 7 8,
  .positive 6 7 8,
  .convex 0 1 2 4,
  .convex 0 1 2 5,
  .convex 0 1 2 6,
  .convex 0 1 2 7,
  .convex 0 1 2 8,
  .convex 0 1 4 5,
  .convex 0 1 4 6,
  .convex 0 1 4 7,
  .convex 0 1 4 8,
  .convex 0 1 5 6,
  .convex 0 1 5 7,
  .convex 0 1 5 8,
  .convex 0 1 6 7,
  .convex 0 1 6 8,
  .convex 0 1 7 8,
  .convex 0 2 4 5,
  .convex 0 2 4 6,
  .convex 0 2 4 7,
  .convex 0 2 4 8,
  .convex 0 2 5 6,
  .convex 0 2 5 7,
  .convex 0 2 5 8,
  .convex 0 2 6 7,
  .convex 0 2 6 8,
  .convex 0 2 7 8,
  .convex 0 4 5 6,
  .convex 0 4 5 7,
  .convex 0 4 5 8,
  .convex 0 4 6 7,
  .convex 0 4 6 8,
  .convex 0 4 7 8,
  .convex 0 5 6 7,
  .convex 0 5 6 8,
  .convex 0 5 7 8,
  .convex 0 6 7 8,
  .convex 1 2 3 4,
  .convex 1 2 3 5,
  .convex 1 2 3 6,
  .convex 1 2 3 7,
  .convex 1 2 3 8,
  .convex 1 2 4 5,
  .convex 1 2 4 6,
  .convex 1 2 4 7,
  .convex 1 2 4 8,
  .convex 1 2 5 6,
  .convex 1 2 5 7,
  .convex 1 2 5 8,
  .convex 1 2 6 7,
  .convex 1 2 6 8,
  .convex 1 2 7 8,
  .convex 1 3 4 5,
  .convex 1 3 4 6,
  .convex 1 3 4 7,
  .convex 1 3 4 8,
  .convex 1 3 5 6,
  .convex 1 3 5 7,
  .convex 1 3 5 8,
  .convex 1 3 6 7,
  .convex 1 3 6 8,
  .convex 1 3 7 8,
  .convex 1 4 5 6,
  .convex 1 4 5 7,
  .convex 1 4 5 8,
  .convex 1 4 6 7,
  .convex 1 4 6 8,
  .convex 1 4 7 8,
  .convex 1 5 6 7,
  .convex 1 5 6 8,
  .convex 1 5 7 8,
  .convex 1 6 7 8,
  .convex 2 3 4 5,
  .convex 2 3 4 6,
  .convex 2 3 4 7,
  .convex 2 3 4 8,
  .convex 2 3 5 6,
  .convex 2 3 5 7,
  .convex 2 3 5 8,
  .convex 2 3 6 7,
  .convex 2 3 6 8,
  .convex 2 3 7 8,
  .convex 2 4 5 6,
  .convex 2 4 5 7,
  .convex 2 4 5 8,
  .convex 2 4 6 7,
  .convex 2 4 6 8,
  .convex 2 4 7 8,
  .convex 2 5 6 7,
  .convex 2 5 6 8,
  .convex 2 5 7 8,
  .convex 2 6 7 8,
  .convex 3 4 5 6,
  .convex 3 4 5 7,
  .convex 3 4 5 8,
  .convex 3 4 6 7,
  .convex 3 4 6 8,
  .convex 3 4 7 8,
  .convex 3 5 6 7,
  .convex 3 5 6 8,
  .convex 3 5 7 8,
  .convex 3 6 7 8,
  .convex 4 5 6 7,
  .convex 4 5 6 8,
  .convex 4 5 7 8,
  .convex 4 6 7 8,
  .convex 5 6 7 8]

private def clause000 : Sat.Clause := [.neg 0, .pos 1, .pos 4]
private def clause001 : Sat.Clause := [.neg 0, .neg 1, .pos 2, .pos 4]
private def clause002 : Sat.Clause := [.neg 0, .neg 2, .pos 3, .pos 4]
private def clause003 : Sat.Clause := [.pos 0]
private def clause004 : Sat.Clause := [.pos 5]
private def clause005 : Sat.Clause := [.neg 6, .pos 7, .pos 10]
private def clause006 : Sat.Clause := [.neg 6, .neg 7, .pos 8, .pos 10]
private def clause007 : Sat.Clause := [.neg 6, .neg 8, .pos 9, .pos 10]
private def clause008 : Sat.Clause := [.neg 6, .neg 9, .pos 10]
private def clause009 : Sat.Clause := [.pos 11]
private def clause010 : Sat.Clause := [.pos 12]
private def clause011 : Sat.Clause := [.neg 13, .pos 14, .pos 17]
private def clause012 : Sat.Clause := [.neg 13, .neg 14, .pos 15, .pos 17]
private def clause013 : Sat.Clause := [.neg 13, .neg 15, .pos 16, .pos 17]
private def clause014 : Sat.Clause := [.neg 13, .neg 16, .pos 17]
private def clause015 : Sat.Clause := [.pos 18]
private def clause016 : Sat.Clause := [.pos 19]
private def clause017 : Sat.Clause := [.pos 22]
private def clause018 : Sat.Clause := [.pos 25]
private def clause019 : Sat.Clause := [.pos 28]
private def clause020 : Sat.Clause := [.neg 29, .neg 30, .pos 31, .neg 33, .pos 34]
private def clause021 : Sat.Clause := [.neg 29, .neg 31, .pos 32, .neg 33, .pos 34]
private def clause022 : Sat.Clause := [.neg 29, .neg 32, .neg 33, .pos 34]
private def clause023 : Sat.Clause := [.pos 36]
private def clause024 : Sat.Clause := [.pos 37]
private def clause025 : Sat.Clause := [.pos 38]
private def clause026 : Sat.Clause := [.pos 41]
private def clause027 : Sat.Clause := [.pos 42]
private def clause028 : Sat.Clause := [.pos 44]
private def clause029 : Sat.Clause := [.pos 46]
private def clause030 : Sat.Clause := [.neg 48, .neg 49, .pos 50, .neg 52, .pos 53]
private def clause031 : Sat.Clause := [.neg 48, .neg 49, .pos 50, .neg 53, .pos 54]
private def clause032 : Sat.Clause := [.neg 48, .neg 49, .pos 50, .neg 54, .pos 55]
private def clause033 : Sat.Clause := [.neg 48, .neg 49, .pos 50, .neg 55]
private def clause034 : Sat.Clause := [.neg 48, .neg 50, .pos 51, .neg 52, .pos 53]
private def clause035 : Sat.Clause := [.neg 48, .neg 50, .pos 51, .neg 53, .pos 54]
private def clause036 : Sat.Clause := [.neg 48, .neg 50, .pos 51, .neg 54, .pos 55]
private def clause037 : Sat.Clause := [.neg 48, .neg 50, .pos 51, .neg 55]
private def clause038 : Sat.Clause := [.neg 48, .neg 51, .neg 52, .pos 53]
private def clause039 : Sat.Clause := [.neg 48, .neg 51, .neg 53, .pos 54]
private def clause040 : Sat.Clause := [.neg 48, .neg 51, .neg 54, .pos 55]
private def clause041 : Sat.Clause := [.neg 48, .neg 51, .neg 55]
private def clause042 : Sat.Clause := [.pos 48]
private def clause043 : Sat.Clause := [.pos 56]
private def clause044 : Sat.Clause := [.neg 0, .neg 4, .neg 19, .pos 20, .neg 57]
private def clause045 : Sat.Clause := [.neg 0, .pos 6, .neg 21]
private def clause046 : Sat.Clause := [.neg 0, .neg 3, .neg 21, .pos 58]
private def clause047 : Sat.Clause := [.neg 0, .pos 13, .neg 23]
private def clause048 : Sat.Clause := [.neg 0, .neg 3, .neg 23, .pos 61]
private def clause049 : Sat.Clause := [.neg 5, .pos 6, .neg 24]
private def clause050 : Sat.Clause := [.neg 5, .pos 13, .neg 27]
private def clause051 : Sat.Clause := [.neg 6, .neg 10, .neg 29, .pos 33, .neg 69]
private def clause052 : Sat.Clause := [.neg 6, .pos 13, .neg 36]
private def clause053 : Sat.Clause := [.neg 11, .pos 13, .neg 40]
private def clause054 : Sat.Clause := [.neg 13, .neg 16, .pos 40, .neg 73]
private def clause055 : Sat.Clause := [.neg 13, .neg 17, .neg 48, .pos 52, .neg 80]
private def clause056 : Sat.Clause := [.neg 19, .pos 21, .neg 24]
private def clause057 : Sat.Clause := [.neg 19, .neg 20, .neg 25, .pos 26, .neg 83]
private def clause058 : Sat.Clause := [.neg 19, .pos 23, .neg 27]
private def clause059 : Sat.Clause := [.neg 21, .neg 29, .pos 30, .pos 88]
private def clause060 : Sat.Clause := [.neg 21, .pos 23, .neg 36]
private def clause061 : Sat.Clause := [.neg 22, .pos 23, .neg 40]
private def clause062 : Sat.Clause := [.neg 25, .neg 26, .neg 38, .pos 39, .neg 108]
private def clause063 : Sat.Clause := [.neg 29, .pos 35, .neg 38]
private def clause064 : Sat.Clause := [.neg 29, .neg 34, .neg 38, .pos 39, .neg 118]
private def clause065 : Sat.Clause := [.pos 29, .neg 36, .pos 40]
private def clause066 : Sat.Clause := [.neg 36, .neg 48, .pos 49, .pos 126]
private def clause067 : Sat.Clause := [.neg 38, .pos 40, .neg 43]
private def clause068 : Sat.Clause := [.neg 38, .neg 39, .neg 44, .pos 45, .neg 129]
private def clause069 : Sat.Clause := [.pos 40, .neg 41, .pos 47]
private def clause070 : Sat.Clause := [.neg 44, .neg 45, .neg 56, .neg 136]
private def clause071 : Sat.Clause := [.pos 57]
private def clause072 : Sat.Clause := [.pos 59]
private def clause073 : Sat.Clause := [.pos 60]
private def clause074 : Sat.Clause := [.pos 62]
private def clause075 : Sat.Clause := [.pos 63]
private def clause076 : Sat.Clause := [.pos 64]
private def clause077 : Sat.Clause := [.pos 65]
private def clause078 : Sat.Clause := [.pos 67]
private def clause079 : Sat.Clause := [.pos 68]
private def clause080 : Sat.Clause := [.pos 72]
private def clause081 : Sat.Clause := [.pos 74]
private def clause082 : Sat.Clause := [.pos 75]
private def clause083 : Sat.Clause := [.pos 77]
private def clause084 : Sat.Clause := [.pos 78]
private def clause085 : Sat.Clause := [.pos 81]
private def clause086 : Sat.Clause := [.pos 82]
private def clause087 : Sat.Clause := [.pos 83]
private def clause088 : Sat.Clause := [.pos 84]
private def clause089 : Sat.Clause := [.pos 85]
private def clause090 : Sat.Clause := [.pos 86]
private def clause091 : Sat.Clause := [.pos 87]
private def clause092 : Sat.Clause := [.neg 88]
private def clause093 : Sat.Clause := [.neg 89]
private def clause094 : Sat.Clause := [.neg 91]
private def clause095 : Sat.Clause := [.pos 93]
private def clause096 : Sat.Clause := [.pos 94]
private def clause097 : Sat.Clause := [.pos 95]
private def clause098 : Sat.Clause := [.pos 96]
private def clause099 : Sat.Clause := [.pos 97]
private def clause100 : Sat.Clause := [.pos 98]
private def clause101 : Sat.Clause := [.pos 99]
private def clause102 : Sat.Clause := [.neg 100]
private def clause103 : Sat.Clause := [.neg 101]
private def clause104 : Sat.Clause := [.pos 102]
private def clause105 : Sat.Clause := [.neg 103]
private def clause106 : Sat.Clause := [.neg 104]
private def clause107 : Sat.Clause := [.neg 106]
private def clause108 : Sat.Clause := [.pos 108]
private def clause109 : Sat.Clause := [.pos 109]
private def clause110 : Sat.Clause := [.pos 110]
private def clause111 : Sat.Clause := [.pos 111]
private def clause112 : Sat.Clause := [.pos 112]
private def clause113 : Sat.Clause := [.pos 113]
private def clause114 : Sat.Clause := [.pos 114]
private def clause115 : Sat.Clause := [.neg 115]
private def clause116 : Sat.Clause := [.neg 116]
private def clause117 : Sat.Clause := [.pos 117]
private def clause118 : Sat.Clause := [.pos 118]
private def clause119 : Sat.Clause := [.pos 120]
private def clause120 : Sat.Clause := [.pos 123]
private def clause121 : Sat.Clause := [.neg 125]
private def clause122 : Sat.Clause := [.neg 126]
private def clause123 : Sat.Clause := [.pos 127]
private def clause124 : Sat.Clause := [.pos 128]
private def clause125 : Sat.Clause := [.pos 129]
private def clause126 : Sat.Clause := [.pos 130]
private def clause127 : Sat.Clause := [.neg 131]
private def clause128 : Sat.Clause := [.neg 132]
private def clause129 : Sat.Clause := [.pos 133]
private def clause130 : Sat.Clause := [.neg 134]
private def clause131 : Sat.Clause := [.neg 135]
private def clause132 : Sat.Clause := [.pos 136]
private def clause133 : Sat.Clause := [.pos 137]
private def clause134 : Sat.Clause := [.neg 57, .neg 59, .neg 64, .neg 83, .pos 138]
private def clause135 : Sat.Clause := [.neg 57, .neg 60, .neg 65, .neg 84, .pos 139]
private def clause136 : Sat.Clause := [.neg 57, .neg 61, .neg 66, .neg 85, .pos 140]
private def clause137 : Sat.Clause := [.neg 57, .neg 62, .neg 67, .neg 86, .pos 141]
private def clause138 : Sat.Clause := [.neg 57, .neg 63, .neg 68, .neg 87, .pos 142]
private def clause139 : Sat.Clause := [.neg 0, .neg 21, .neg 36, .neg 58, .neg 61, .pos 70, .neg 90]
private def clause140 : Sat.Clause := [.neg 0, .neg 21, .neg 37, .neg 58, .neg 63, .pos 71, .neg 92]
private def clause141 : Sat.Clause := [.neg 59, .neg 60, .neg 72, .neg 93, .pos 143]
private def clause142 : Sat.Clause := [.neg 0, .neg 22, .neg 40, .neg 59, .neg 61, .pos 73, .neg 94]
private def clause143 : Sat.Clause := [.neg 59, .neg 61, .neg 73, .neg 94, .pos 144]
private def clause144 : Sat.Clause := [.neg 59, .neg 62, .neg 74, .neg 95, .pos 145]
private def clause145 : Sat.Clause := [.neg 59, .neg 63, .neg 75, .neg 96, .pos 146]
private def clause146 : Sat.Clause := [.neg 60, .neg 61, .neg 76, .neg 97, .pos 147]
private def clause147 : Sat.Clause := [.neg 60, .neg 62, .neg 77, .neg 98, .pos 148]
private def clause148 : Sat.Clause := [.neg 60, .neg 63, .neg 78, .neg 99, .pos 149]
private def clause149 : Sat.Clause := [.neg 61, .neg 62, .pos 79, .pos 100, .pos 150]
private def clause150 : Sat.Clause := [.neg 61, .neg 63, .pos 80, .pos 101, .pos 151]
private def clause151 : Sat.Clause := [.neg 62, .neg 63, .neg 81, .neg 102, .pos 152]
private def clause152 : Sat.Clause := [.neg 64, .neg 65, .neg 72, .neg 108, .pos 153]
private def clause153 : Sat.Clause := [.neg 13, .neg 25, .pos 27, .neg 64, .pos 66, .neg 73, .neg 109]
private def clause154 : Sat.Clause := [.neg 64, .neg 66, .neg 73, .neg 109, .pos 154]
private def clause155 : Sat.Clause := [.neg 64, .neg 67, .neg 74, .neg 110, .pos 155]
private def clause156 : Sat.Clause := [.neg 64, .neg 68, .neg 75, .neg 111, .pos 156]
private def clause157 : Sat.Clause := [.neg 65, .neg 66, .neg 76, .neg 112, .pos 157]
private def clause158 : Sat.Clause := [.neg 65, .neg 67, .neg 77, .neg 113, .pos 158]
private def clause159 : Sat.Clause := [.neg 65, .neg 68, .neg 78, .neg 114, .pos 159]
private def clause160 : Sat.Clause := [.neg 66, .neg 67, .pos 79, .pos 115, .pos 160]
private def clause161 : Sat.Clause := [.neg 5, .neg 27, .neg 48, .pos 66, .neg 68, .pos 80, .pos 116]
private def clause162 : Sat.Clause := [.pos 66, .neg 68, .pos 80, .pos 116, .neg 161]
private def clause163 : Sat.Clause := [.neg 66, .neg 68, .pos 80, .pos 116, .pos 161]
private def clause164 : Sat.Clause := [.neg 67, .neg 68, .neg 81, .neg 117, .pos 162]
private def clause165 : Sat.Clause := [.neg 6, .neg 36, .pos 40, .pos 69, .neg 70, .pos 73, .neg 119]
private def clause166 : Sat.Clause := [.neg 6, .neg 36, .neg 48, .pos 70, .neg 71, .pos 80, .pos 126]
private def clause167 : Sat.Clause := [.neg 72, .neg 73, .neg 76, .neg 128, .pos 163]
private def clause168 : Sat.Clause := [.neg 72, .neg 74, .neg 77, .neg 129, .pos 164]
private def clause169 : Sat.Clause := [.neg 72, .neg 75, .neg 78, .neg 130, .pos 165]
private def clause170 : Sat.Clause := [.neg 73, .neg 74, .pos 79, .pos 131, .pos 166]
private def clause171 : Sat.Clause := [.neg 11, .neg 40, .neg 48, .pos 73, .neg 75, .pos 80, .pos 132]
private def clause172 : Sat.Clause := [.neg 11, .neg 40, .neg 48, .pos 73, .neg 75, .neg 80, .pos 132]
private def clause173 : Sat.Clause := [.pos 73, .neg 75, .pos 80, .pos 132, .neg 167]
private def clause174 : Sat.Clause := [.neg 73, .neg 75, .pos 80, .pos 132, .pos 167]
private def clause175 : Sat.Clause := [.neg 73, .neg 75, .neg 80, .pos 132, .neg 167]
private def clause176 : Sat.Clause := [.neg 74, .neg 75, .neg 81, .neg 133, .pos 168]
private def clause177 : Sat.Clause := [.neg 13, .pos 43, .neg 44, .pos 76, .neg 77, .pos 79, .pos 134]
private def clause178 : Sat.Clause := [.neg 76, .neg 77, .pos 79, .pos 134, .pos 169]
private def clause179 : Sat.Clause := [.neg 12, .neg 43, .neg 48, .pos 76, .neg 78, .pos 80, .pos 135]
private def clause180 : Sat.Clause := [.neg 13, .pos 43, .neg 46, .pos 76, .neg 78, .pos 80, .pos 135]
private def clause181 : Sat.Clause := [.pos 76, .neg 78, .pos 80, .pos 135, .neg 170]
private def clause182 : Sat.Clause := [.neg 76, .neg 78, .pos 80, .pos 135, .pos 170]
private def clause183 : Sat.Clause := [.neg 77, .neg 78, .neg 81, .neg 136, .pos 171]
private def clause184 : Sat.Clause := [.neg 13, .neg 47, .neg 56, .neg 79, .pos 80, .neg 81, .neg 137]
private def clause185 : Sat.Clause := [.neg 18, .pos 47, .neg 48, .neg 79, .pos 80, .neg 81, .neg 137]
private def clause186 : Sat.Clause := [.pos 79, .pos 80, .neg 81, .neg 137, .pos 172]
private def clause187 : Sat.Clause := [.neg 79, .pos 80, .neg 81, .neg 137, .neg 172]
private def clause188 : Sat.Clause := [.neg 82, .neg 83, .pos 88, .pos 103, .pos 173]
private def clause189 : Sat.Clause := [.neg 82, .neg 84, .pos 89, .pos 104, .pos 174]
private def clause190 : Sat.Clause := [.neg 19, .neg 24, .neg 36, .neg 82, .neg 85, .pos 90, .neg 105]
private def clause191 : Sat.Clause := [.neg 19, .pos 23, .neg 36, .neg 82, .neg 85, .neg 90, .pos 105]
private def clause192 : Sat.Clause := [.neg 82, .neg 85, .pos 90, .pos 105, .pos 175]
private def clause193 : Sat.Clause := [.neg 82, .neg 86, .pos 91, .pos 106, .pos 176]
private def clause194 : Sat.Clause := [.neg 19, .neg 24, .neg 37, .neg 82, .neg 87, .pos 92, .neg 107]
private def clause195 : Sat.Clause := [.neg 19, .pos 21, .neg 28, .neg 82, .neg 87, .neg 92, .pos 107]
private def clause196 : Sat.Clause := [.neg 82, .neg 87, .pos 92, .pos 107, .pos 177]
private def clause197 : Sat.Clause := [.neg 83, .neg 84, .neg 93, .neg 108, .pos 178]
private def clause198 : Sat.Clause := [.neg 83, .neg 85, .neg 94, .neg 109, .pos 179]
private def clause199 : Sat.Clause := [.neg 83, .neg 86, .neg 95, .neg 110, .pos 180]
private def clause200 : Sat.Clause := [.neg 83, .neg 87, .neg 96, .neg 111, .pos 181]
private def clause201 : Sat.Clause := [.neg 84, .neg 85, .neg 97, .neg 112, .pos 182]
private def clause202 : Sat.Clause := [.neg 84, .neg 86, .neg 98, .neg 113, .pos 183]
private def clause203 : Sat.Clause := [.neg 84, .neg 87, .neg 99, .neg 114, .pos 184]
private def clause204 : Sat.Clause := [.neg 85, .neg 86, .pos 100, .pos 115, .pos 185]
private def clause205 : Sat.Clause := [.neg 85, .neg 87, .pos 101, .pos 116, .pos 186]
private def clause206 : Sat.Clause := [.neg 86, .neg 87, .neg 102, .neg 117, .pos 187]
private def clause207 : Sat.Clause := [.pos 88, .pos 89, .neg 93, .neg 118, .pos 188]
private def clause208 : Sat.Clause := [.pos 88, .pos 90, .neg 94, .neg 119, .pos 189]
private def clause209 : Sat.Clause := [.pos 88, .pos 91, .neg 95, .neg 120, .pos 190]
private def clause210 : Sat.Clause := [.pos 88, .pos 92, .neg 96, .neg 121, .pos 191]
private def clause211 : Sat.Clause := [.pos 89, .pos 90, .neg 97, .neg 122, .pos 192]
private def clause212 : Sat.Clause := [.pos 89, .pos 91, .neg 98, .neg 123, .pos 193]
private def clause213 : Sat.Clause := [.pos 89, .pos 92, .neg 99, .neg 124, .pos 194]
private def clause214 : Sat.Clause := [.pos 90, .pos 91, .pos 100, .pos 125, .pos 195]
private def clause215 : Sat.Clause := [.pos 21, .neg 23, .neg 48, .neg 90, .pos 92, .pos 101, .pos 126]
private def clause216 : Sat.Clause := [.pos 90, .pos 92, .pos 101, .pos 126, .pos 196]
private def clause217 : Sat.Clause := [.neg 90, .pos 92, .pos 101, .pos 126, .neg 196]
private def clause218 : Sat.Clause := [.pos 91, .pos 92, .neg 102, .neg 127, .pos 197]
private def clause219 : Sat.Clause := [.pos 91, .neg 92, .neg 102, .neg 127, .neg 197]
private def clause220 : Sat.Clause := [.neg 93, .neg 94, .neg 97, .neg 128, .pos 198]
private def clause221 : Sat.Clause := [.neg 93, .neg 95, .neg 98, .neg 129, .pos 199]
private def clause222 : Sat.Clause := [.neg 93, .neg 96, .neg 99, .neg 130, .pos 200]
private def clause223 : Sat.Clause := [.neg 94, .neg 95, .pos 100, .pos 131, .pos 201]
private def clause224 : Sat.Clause := [.neg 94, .neg 96, .pos 101, .pos 132, .pos 202]
private def clause225 : Sat.Clause := [.neg 95, .neg 96, .neg 102, .neg 133, .pos 203]
private def clause226 : Sat.Clause := [.neg 97, .neg 98, .pos 100, .pos 134, .pos 204]
private def clause227 : Sat.Clause := [.neg 97, .neg 99, .pos 101, .pos 135, .pos 205]
private def clause228 : Sat.Clause := [.neg 98, .neg 99, .neg 102, .neg 136, .pos 206]
private def clause229 : Sat.Clause := [.pos 100, .pos 101, .neg 102, .neg 137, .pos 207]
private def clause230 : Sat.Clause := [.pos 103, .pos 104, .neg 108, .neg 118, .pos 208]
private def clause231 : Sat.Clause := [.neg 25, .pos 27, .neg 36, .pos 103, .neg 105, .neg 109, .neg 119]
private def clause232 : Sat.Clause := [.pos 103, .pos 105, .neg 109, .neg 119, .pos 209]
private def clause233 : Sat.Clause := [.pos 103, .pos 106, .neg 110, .neg 120, .pos 210]
private def clause234 : Sat.Clause := [.pos 24, .neg 25, .neg 42, .pos 103, .neg 107, .neg 111, .neg 121]
private def clause235 : Sat.Clause := [.pos 103, .pos 107, .neg 111, .neg 121, .pos 211]
private def clause236 : Sat.Clause := [.pos 104, .pos 105, .neg 112, .neg 122, .pos 212]
private def clause237 : Sat.Clause := [.pos 104, .pos 106, .neg 113, .neg 123, .pos 213]
private def clause238 : Sat.Clause := [.pos 104, .pos 107, .neg 114, .neg 124, .pos 214]
private def clause239 : Sat.Clause := [.pos 105, .pos 106, .pos 115, .pos 125, .pos 215]
private def clause240 : Sat.Clause := [.pos 24, .neg 27, .neg 48, .neg 105, .pos 107, .pos 116, .pos 126]
private def clause241 : Sat.Clause := [.pos 105, .pos 107, .pos 116, .pos 126, .pos 216]
private def clause242 : Sat.Clause := [.neg 105, .pos 107, .pos 116, .pos 126, .neg 216]
private def clause243 : Sat.Clause := [.pos 106, .pos 107, .neg 117, .neg 127, .pos 217]
private def clause244 : Sat.Clause := [.pos 106, .neg 107, .neg 117, .neg 127, .neg 217]
private def clause245 : Sat.Clause := [.neg 108, .neg 109, .neg 112, .neg 128, .pos 218]
private def clause246 : Sat.Clause := [.neg 108, .neg 110, .neg 113, .neg 129, .pos 219]
private def clause247 : Sat.Clause := [.neg 108, .neg 111, .neg 114, .neg 130, .pos 220]
private def clause248 : Sat.Clause := [.neg 109, .neg 110, .pos 115, .pos 131, .pos 221]
private def clause249 : Sat.Clause := [.neg 109, .neg 111, .pos 116, .pos 132, .pos 222]
private def clause250 : Sat.Clause := [.neg 110, .neg 111, .neg 117, .neg 133, .pos 223]
private def clause251 : Sat.Clause := [.neg 112, .neg 113, .pos 115, .pos 134, .pos 224]
private def clause252 : Sat.Clause := [.neg 112, .neg 114, .pos 116, .pos 135, .pos 225]
private def clause253 : Sat.Clause := [.neg 113, .neg 114, .neg 117, .neg 136, .pos 226]
private def clause254 : Sat.Clause := [.pos 115, .pos 116, .neg 117, .neg 137, .pos 227]
private def clause255 : Sat.Clause := [.neg 118, .neg 119, .neg 122, .neg 128, .pos 228]
private def clause256 : Sat.Clause := [.neg 118, .neg 120, .neg 123, .neg 129, .pos 229]
private def clause257 : Sat.Clause := [.neg 118, .neg 121, .neg 124, .neg 130, .pos 230]
private def clause258 : Sat.Clause := [.neg 36, .pos 40, .neg 41, .pos 119, .neg 120, .pos 125, .pos 131]
private def clause259 : Sat.Clause := [.neg 119, .neg 120, .pos 125, .pos 131, .pos 231]
private def clause260 : Sat.Clause := [.pos 119, .neg 121, .pos 126, .pos 132, .neg 232]
private def clause261 : Sat.Clause := [.neg 119, .neg 121, .pos 126, .pos 132, .pos 232]
private def clause262 : Sat.Clause := [.neg 29, .neg 41, .neg 56, .neg 120, .pos 121, .neg 127, .neg 133]
private def clause263 : Sat.Clause := [.neg 120, .pos 121, .neg 127, .neg 133, .neg 233]
private def clause264 : Sat.Clause := [.neg 120, .neg 121, .neg 127, .neg 133, .pos 233]
private def clause265 : Sat.Clause := [.neg 36, .pos 43, .neg 44, .pos 122, .neg 123, .pos 125, .pos 134]
private def clause266 : Sat.Clause := [.neg 122, .neg 123, .pos 125, .pos 134, .pos 234]
private def clause267 : Sat.Clause := [.pos 122, .neg 124, .pos 126, .pos 135, .neg 235]
private def clause268 : Sat.Clause := [.neg 122, .neg 124, .pos 126, .pos 135, .pos 235]
private def clause269 : Sat.Clause := [.neg 35, .neg 44, .neg 56, .neg 123, .pos 124, .neg 127, .neg 136]
private def clause270 : Sat.Clause := [.neg 123, .pos 124, .neg 127, .neg 136, .neg 236]
private def clause271 : Sat.Clause := [.neg 123, .neg 124, .neg 127, .neg 136, .pos 236]
private def clause272 : Sat.Clause := [.pos 125, .pos 126, .neg 127, .neg 137, .pos 237]
private def clause273 : Sat.Clause := [.neg 128, .neg 129, .pos 131, .pos 134, .pos 238]
private def clause274 : Sat.Clause := [.neg 128, .neg 130, .pos 132, .pos 135, .pos 239]
private def clause275 : Sat.Clause := [.neg 129, .neg 130, .neg 133, .neg 136, .pos 240]
private def clause276 : Sat.Clause := [.pos 131, .pos 132, .neg 133, .neg 137, .pos 241]
private def clause277 : Sat.Clause := [.pos 134, .pos 135, .neg 136, .neg 137, .pos 242]
private def clause278 : Sat.Clause := [.neg 138, .neg 139, .neg 140, .neg 141, .neg 142, .neg 143, .neg 144, .neg 145, .neg 146, .neg 147, .neg 148, .neg 149, .neg 150, .neg 151, .neg 152, .neg 153, .neg 154, .neg 155, .neg 156, .neg 157, .neg 158, .neg 159, .neg 160, .neg 161, .neg 162, .neg 163, .neg 164, .neg 165, .neg 166, .neg 167, .neg 168, .neg 169, .neg 170, .neg 171, .neg 172, .neg 178, .neg 179, .neg 180, .neg 181, .neg 182, .neg 183, .neg 184, .neg 185, .neg 186, .neg 187, .neg 198, .neg 199, .neg 200, .neg 201, .neg 202, .neg 203, .neg 204, .neg 205, .neg 206, .neg 207, .neg 218, .neg 219, .neg 220, .neg 221, .neg 222, .neg 223, .neg 224, .neg 225, .neg 226, .neg 227, .neg 238, .neg 239, .neg 240, .neg 241, .neg 242]
private def clause279 : Sat.Clause := [.neg 173, .neg 174, .neg 175, .neg 176, .neg 177, .neg 178, .neg 179, .neg 180, .neg 181, .neg 182, .neg 183, .neg 184, .neg 185, .neg 186, .neg 187, .neg 188, .neg 189, .neg 190, .neg 191, .neg 192, .neg 193, .neg 194, .neg 195, .neg 196, .neg 197, .neg 198, .neg 199, .neg 200, .neg 201, .neg 202, .neg 203, .neg 204, .neg 205, .neg 206, .neg 207, .neg 208, .neg 209, .neg 210, .neg 211, .neg 212, .neg 213, .neg 214, .neg 215, .neg 216, .neg 217, .neg 218, .neg 219, .neg 220, .neg 221, .neg 222, .neg 223, .neg 224, .neg 225, .neg 226, .neg 227, .neg 228, .neg 229, .neg 230, .neg 231, .neg 232, .neg 233, .neg 234, .neg 235, .neg 236, .neg 237, .neg 238, .neg 239, .neg 240, .neg 241, .neg 242]

private def clauses : Sat.Fmla := [
  clause000, clause001, clause002, clause003, clause004, clause005, clause006, clause007, clause008, clause009, clause010, clause011, clause012, clause013, clause014, clause015, clause016, clause017, clause018, clause019, clause020, clause021, clause022, clause023, clause024, clause025, clause026, clause027, clause028, clause029, clause030, clause031, clause032, clause033, clause034, clause035, clause036, clause037, clause038, clause039, clause040, clause041, clause042, clause043, clause044, clause045, clause046, clause047, clause048, clause049, clause050, clause051, clause052, clause053, clause054, clause055, clause056, clause057, clause058, clause059, clause060, clause061, clause062, clause063, clause064, clause065, clause066, clause067, clause068, clause069, clause070, clause071, clause072, clause073, clause074, clause075, clause076, clause077, clause078, clause079, clause080, clause081, clause082, clause083, clause084, clause085, clause086, clause087, clause088, clause089, clause090, clause091, clause092, clause093, clause094, clause095, clause096, clause097, clause098, clause099, clause100, clause101, clause102, clause103, clause104, clause105, clause106, clause107, clause108, clause109, clause110, clause111, clause112, clause113, clause114, clause115, clause116, clause117, clause118, clause119, clause120, clause121, clause122, clause123, clause124, clause125, clause126, clause127, clause128, clause129, clause130, clause131, clause132, clause133, clause134, clause135, clause136, clause137, clause138, clause139, clause140, clause141, clause142, clause143, clause144, clause145, clause146, clause147, clause148, clause149, clause150, clause151, clause152, clause153, clause154, clause155, clause156, clause157, clause158, clause159, clause160, clause161, clause162, clause163, clause164, clause165, clause166, clause167, clause168, clause169, clause170, clause171, clause172, clause173, clause174, clause175, clause176, clause177, clause178, clause179, clause180, clause181, clause182, clause183, clause184, clause185, clause186, clause187, clause188, clause189, clause190, clause191, clause192, clause193, clause194, clause195, clause196, clause197, clause198, clause199, clause200, clause201, clause202, clause203, clause204, clause205, clause206, clause207, clause208, clause209, clause210, clause211, clause212, clause213, clause214, clause215, clause216, clause217, clause218, clause219, clause220, clause221, clause222, clause223, clause224, clause225, clause226, clause227, clause228, clause229, clause230, clause231, clause232, clause233, clause234, clause235, clause236, clause237, clause238, clause239, clause240, clause241, clause242, clause243, clause244, clause245, clause246, clause247, clause248, clause249, clause250, clause251, clause252, clause253, clause254, clause255, clause256, clause257, clause258, clause259, clause260, clause261, clause262, clause263, clause264, clause265, clause266, clause267, clause268, clause269, clause270, clause271, clause272, clause273, clause274, clause275, clause276, clause277, clause278, clause279]

private theorem formula_eq : cnf_refutation.formula = clauses := by rfl

variable {n : ℕ} (C : Context 9 n states)

-- Clause 1: domain; source clause 7.
private theorem sound000 : C.clause (decodeClause atoms clause000) := by
  exact C.covered_clause _ _ (C.domain_clause 0 1 (by decide) 1 1 (by decide +kernel)) (by decide +kernel)

-- Clause 2: domain; source clause 13.
private theorem sound001 : C.clause (decodeClause atoms clause001) := by
  exact C.covered_clause _ _ (C.domain_clause 0 1 (by decide) 2 1 (by decide +kernel)) (by decide +kernel)

-- Clause 3: domain; source clause 19.
private theorem sound002 : C.clause (decodeClause atoms clause002) := by
  exact C.covered_clause _ _ (C.domain_clause 0 1 (by decide) 3 1 (by decide +kernel)) (by decide +kernel)

-- Clause 4: empty_direction; source clause 30.
private theorem sound003 : C.clause (decodeClause atoms clause003) := by
  exact C.covered_clause _ _ (C.empty_clause 1 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 5: empty_direction; source clause 82.
private theorem sound004 : C.clause (decodeClause atoms clause004) := by
  exact C.covered_clause _ _ (C.empty_clause 2 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 6: domain; source clause 113.
private theorem sound005 : C.clause (decodeClause atoms clause005) := by
  exact C.covered_clause _ _ (C.domain_clause 0 3 (by decide) 1 1 (by decide +kernel)) (by decide +kernel)

-- Clause 7: domain; source clause 119.
private theorem sound006 : C.clause (decodeClause atoms clause006) := by
  exact C.covered_clause _ _ (C.domain_clause 0 3 (by decide) 2 1 (by decide +kernel)) (by decide +kernel)

-- Clause 8: domain; source clause 121.
private theorem sound007 : C.clause (decodeClause atoms clause007) := by
  exact C.covered_clause _ _ (C.domain_clause 0 3 (by decide) 3 1 (by decide +kernel)) (by decide +kernel)

-- Clause 9: domain; source clause 127.
private theorem sound008 : C.clause (decodeClause atoms clause008) := by
  exact C.covered_clause _ _ (C.domain_clause 0 3 (by decide) 4 1 (by decide +kernel)) (by decide +kernel)

-- Clause 10: empty_direction; source clause 182.
private theorem sound009 : C.clause (decodeClause atoms clause009) := by
  exact C.covered_clause _ _ (C.empty_clause 4 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 11: empty_direction; source clause 232.
private theorem sound010 : C.clause (decodeClause atoms clause010) := by
  exact C.covered_clause _ _ (C.empty_clause 5 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 12: domain; source clause 263.
private theorem sound011 : C.clause (decodeClause atoms clause011) := by
  exact C.covered_clause _ _ (C.domain_clause 0 6 (by decide) 1 1 (by decide +kernel)) (by decide +kernel)

-- Clause 13: domain; source clause 269.
private theorem sound012 : C.clause (decodeClause atoms clause012) := by
  exact C.covered_clause _ _ (C.domain_clause 0 6 (by decide) 2 1 (by decide +kernel)) (by decide +kernel)

-- Clause 14: domain; source clause 270.
private theorem sound013 : C.clause (decodeClause atoms clause013) := by
  exact C.covered_clause _ _ (C.domain_clause 0 6 (by decide) 3 1 (by decide +kernel)) (by decide +kernel)

-- Clause 15: domain; source clause 276.
private theorem sound014 : C.clause (decodeClause atoms clause014) := by
  exact C.covered_clause _ _ (C.domain_clause 0 6 (by decide) 4 1 (by decide +kernel)) (by decide +kernel)

-- Clause 16: empty_direction; source clause 329.
private theorem sound015 : C.clause (decodeClause atoms clause015) := by
  exact C.covered_clause _ _ (C.empty_clause 7 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 17: empty_direction; source clause 430.
private theorem sound016 : C.clause (decodeClause atoms clause016) := by
  exact C.covered_clause _ _ (C.empty_clause 2 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 18: empty_direction; source clause 530.
private theorem sound017 : C.clause (decodeClause atoms clause017) := by
  exact C.covered_clause _ _ (C.empty_clause 4 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 19: empty_direction; source clause 829.
private theorem sound018 : C.clause (decodeClause atoms clause018) := by
  exact C.covered_clause _ _ (C.empty_clause 4 2 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 20: empty_direction; source clause 1032.
private theorem sound019 : C.clause (decodeClause atoms clause019) := by
  exact C.covered_clause _ _ (C.empty_clause 8 2 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 21: domain; source clause 1071.
private theorem sound020 : C.clause (decodeClause atoms clause020) := by
  exact C.covered_clause _ _ (C.domain_clause 3 4 (by decide) 2 3 (by decide +kernel)) (by decide +kernel)

-- Clause 22: domain; source clause 1075.
private theorem sound021 : C.clause (decodeClause atoms clause021) := by
  exact C.covered_clause _ _ (C.domain_clause 3 4 (by decide) 3 3 (by decide +kernel)) (by decide +kernel)

-- Clause 23: domain; source clause 1080.
private theorem sound022 : C.clause (decodeClause atoms clause022) := by
  exact C.covered_clause _ _ (C.domain_clause 3 4 (by decide) 4 3 (by decide +kernel)) (by decide +kernel)

-- Clause 24: empty_direction; source clause 1185.
private theorem sound023 : C.clause (decodeClause atoms clause023) := by
  exact C.covered_clause _ _ (C.empty_clause 6 3 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 25: empty_direction; source clause 1288.
private theorem sound024 : C.clause (decodeClause atoms clause024) := by
  exact C.covered_clause _ _ (C.empty_clause 8 3 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 26: empty_direction; source clause 1342.
private theorem sound025 : C.clause (decodeClause atoms clause025) := by
  exact C.covered_clause _ _ (C.empty_clause 5 4 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 27: empty_direction; source clause 1443.
private theorem sound026 : C.clause (decodeClause atoms clause026) := by
  exact C.covered_clause _ _ (C.empty_clause 7 4 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 28: empty_direction; source clause 1495.
private theorem sound027 : C.clause (decodeClause atoms clause027) := by
  exact C.covered_clause _ _ (C.empty_clause 8 4 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 29: empty_direction; source clause 1598.
private theorem sound028 : C.clause (decodeClause atoms clause028) := by
  exact C.covered_clause _ _ (C.empty_clause 7 5 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 30: empty_direction; source clause 1651.
private theorem sound029 : C.clause (decodeClause atoms clause029) := by
  exact C.covered_clause _ _ (C.empty_clause 8 5 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 31: domain; source clause 1740.
private theorem sound030 : C.clause (decodeClause atoms clause030) := by
  exact C.covered_clause _ _ (C.domain_clause 6 8 (by decide) 2 3 (by decide +kernel)) (by decide +kernel)

-- Clause 32: domain; source clause 1741.
private theorem sound031 : C.clause (decodeClause atoms clause031) := by
  exact C.covered_clause _ _ (C.domain_clause 6 8 (by decide) 2 4 (by decide +kernel)) (by decide +kernel)

-- Clause 33: domain; source clause 1742.
private theorem sound032 : C.clause (decodeClause atoms clause032) := by
  exact C.covered_clause _ _ (C.domain_clause 6 8 (by decide) 2 5 (by decide +kernel)) (by decide +kernel)

-- Clause 34: domain; source clause 1743.
private theorem sound033 : C.clause (decodeClause atoms clause033) := by
  exact C.covered_clause _ _ (C.domain_clause 6 8 (by decide) 2 6 (by decide +kernel)) (by decide +kernel)

-- Clause 35: domain; source clause 1744.
private theorem sound034 : C.clause (decodeClause atoms clause034) := by
  exact C.covered_clause _ _ (C.domain_clause 6 8 (by decide) 3 3 (by decide +kernel)) (by decide +kernel)

-- Clause 36: domain; source clause 1745.
private theorem sound035 : C.clause (decodeClause atoms clause035) := by
  exact C.covered_clause _ _ (C.domain_clause 6 8 (by decide) 3 4 (by decide +kernel)) (by decide +kernel)

-- Clause 37: domain; source clause 1746.
private theorem sound036 : C.clause (decodeClause atoms clause036) := by
  exact C.covered_clause _ _ (C.domain_clause 6 8 (by decide) 3 5 (by decide +kernel)) (by decide +kernel)

-- Clause 38: domain; source clause 1747.
private theorem sound037 : C.clause (decodeClause atoms clause037) := by
  exact C.covered_clause _ _ (C.domain_clause 6 8 (by decide) 3 6 (by decide +kernel)) (by decide +kernel)

-- Clause 39: domain; source clause 1749.
private theorem sound038 : C.clause (decodeClause atoms clause038) := by
  exact C.covered_clause _ _ (C.domain_clause 6 8 (by decide) 4 3 (by decide +kernel)) (by decide +kernel)

-- Clause 40: domain; source clause 1750.
private theorem sound039 : C.clause (decodeClause atoms clause039) := by
  exact C.covered_clause _ _ (C.domain_clause 6 8 (by decide) 4 4 (by decide +kernel)) (by decide +kernel)

-- Clause 41: domain; source clause 1751.
private theorem sound040 : C.clause (decodeClause atoms clause040) := by
  exact C.covered_clause _ _ (C.domain_clause 6 8 (by decide) 4 5 (by decide +kernel)) (by decide +kernel)

-- Clause 42: domain; source clause 1752.
private theorem sound041 : C.clause (decodeClause atoms clause041) := by
  exact C.covered_clause _ _ (C.domain_clause 6 8 (by decide) 4 6 (by decide +kernel)) (by decide +kernel)

-- Clause 43: empty_direction; source clause 1753.
private theorem sound042 : C.clause (decodeClause atoms clause042) := by
  exact C.covered_clause _ _ (C.empty_clause 8 6 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 44: empty_direction; source clause 1807.
private theorem sound043 : C.clause (decodeClause atoms clause043) := by
  exact C.covered_clause _ _ (C.empty_clause 8 7 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 45: growth; source clause 1838.
private theorem sound044 : C.clause (decodeClause atoms clause044) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 1 2 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 46: order_transitive; source clause 1843.
private theorem sound045 : C.clause (decodeClause atoms clause045) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 1 3 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 47: growth; source clause 1847.
private theorem sound046 : C.clause (decodeClause atoms clause046) := by
  exact C.covered_clause _ _ (C.growth_clause false 0 1 3 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 48: order_transitive; source clause 1876.
private theorem sound047 : C.clause (decodeClause atoms clause047) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 1 6 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 49: growth; source clause 1880.
private theorem sound048 : C.clause (decodeClause atoms clause048) := by
  exact C.covered_clause _ _ (C.growth_clause false 0 1 6 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 50: order_transitive; source clause 1920.
private theorem sound049 : C.clause (decodeClause atoms clause049) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 2 3 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 51: order_transitive; source clause 1953.
private theorem sound050 : C.clause (decodeClause atoms clause050) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 2 6 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 52: growth; source clause 2014.
private theorem sound051 : C.clause (decodeClause atoms clause051) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 3 4 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 53: order_transitive; source clause 2030.
private theorem sound052 : C.clause (decodeClause atoms clause052) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 3 6 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 54: order_transitive; source clause 2107.
private theorem sound053 : C.clause (decodeClause atoms clause053) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 4 6 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 55: growth; source clause 2254.
private theorem sound054 : C.clause (decodeClause atoms clause054) := by
  exact C.covered_clause _ _ (C.growth_clause false 0 6 4 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 56: growth; source clause 2289.
private theorem sound055 : C.clause (decodeClause atoms clause055) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 6 8 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 57: order_transitive; source clause 2536.
private theorem sound056 : C.clause (decodeClause atoms clause056) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 2 3 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 58: growth; source clause 2554.
private theorem sound057 : C.clause (decodeClause atoms clause057) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 2 4 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 59: order_transitive; source clause 2569.
private theorem sound058 : C.clause (decodeClause atoms clause058) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 2 6 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 60: growth; source clause 2625.
private theorem sound059 : C.clause (decodeClause atoms clause059) := by
  exact C.covered_clause _ _ (C.growth_clause false 1 3 4 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 61: order_transitive; source clause 2646.
private theorem sound060 : C.clause (decodeClause atoms clause060) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 3 6 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 62: order_transitive; source clause 2723.
private theorem sound061 : C.clause (decodeClause atoms clause061) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 4 6 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 63: growth; source clause 3336.
private theorem sound062 : C.clause (decodeClause atoms clause062) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 4 5 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 64: order_transitive; source clause 3944.
private theorem sound063 : C.clause (decodeClause atoms clause063) := by
  exact C.covered_clause _ _ (C.transitive_clause 3 4 5 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 65: growth; source clause 3952.
private theorem sound064 : C.clause (decodeClause atoms clause064) := by
  exact C.covered_clause _ _ (C.growth_clause true 3 4 5 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 66: order_transitive; source clause 4098.
private theorem sound065 : C.clause (decodeClause atoms clause065) := by
  exact C.covered_clause _ _ (C.transitive_clause 3 6 4 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 67: growth; source clause 4132.
private theorem sound066 : C.clause (decodeClause atoms clause066) := by
  exact C.covered_clause _ _ (C.growth_clause false 3 6 8 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 68: order_transitive; source clause 4648.
private theorem sound067 : C.clause (decodeClause atoms clause067) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 5 6 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 69: growth; source clause 4668.
private theorem sound068 : C.clause (decodeClause atoms clause068) := by
  exact C.covered_clause _ _ (C.growth_clause true 4 5 7 (by decide) (by decide) (by decide) 5) (by decide +kernel)

-- Clause 70: order_transitive; source clause 4813.
private theorem sound069 : C.clause (decodeClause atoms clause069) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 7 6 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 71: growth; source clause 5450.
private theorem sound070 : C.clause (decodeClause atoms clause070) := by
  exact C.covered_clause _ _ (C.growth_clause true 5 7 8 (by decide) (by decide) (by decide) 6) (by decide +kernel)

-- Clause 72: fixed_sign; source clause 7376.
private theorem sound071 : C.clause (decodeClause atoms clause071) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 2 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 73: fixed_sign; source clause 7377.
private theorem sound072 : C.clause (decodeClause atoms clause072) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 4 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 74: fixed_sign; source clause 7378.
private theorem sound073 : C.clause (decodeClause atoms clause073) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 5 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 75: fixed_sign; source clause 7379.
private theorem sound074 : C.clause (decodeClause atoms clause074) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 76: fixed_sign; source clause 7380.
private theorem sound075 : C.clause (decodeClause atoms clause075) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 77: fixed_sign; source clause 7381.
private theorem sound076 : C.clause (decodeClause atoms clause076) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 4 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 78: fixed_sign; source clause 7382.
private theorem sound077 : C.clause (decodeClause atoms clause077) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 5 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 79: fixed_sign; source clause 7383.
private theorem sound078 : C.clause (decodeClause atoms clause078) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 80: fixed_sign; source clause 7384.
private theorem sound079 : C.clause (decodeClause atoms clause079) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 81: fixed_sign; source clause 7385.
private theorem sound080 : C.clause (decodeClause atoms clause080) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 4 5 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 82: fixed_sign; source clause 7386.
private theorem sound081 : C.clause (decodeClause atoms clause081) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 4 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 83: fixed_sign; source clause 7387.
private theorem sound082 : C.clause (decodeClause atoms clause082) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 4 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 84: fixed_sign; source clause 7388.
private theorem sound083 : C.clause (decodeClause atoms clause083) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 5 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 85: fixed_sign; source clause 7389.
private theorem sound084 : C.clause (decodeClause atoms clause084) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 5 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 86: fixed_sign; source clause 7390.
private theorem sound085 : C.clause (decodeClause atoms clause085) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 7 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 87: fixed_sign; source clause 7391.
private theorem sound086 : C.clause (decodeClause atoms clause086) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 3 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 88: fixed_sign; source clause 7392.
private theorem sound087 : C.clause (decodeClause atoms clause087) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 4 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 89: fixed_sign; source clause 7393.
private theorem sound088 : C.clause (decodeClause atoms clause088) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 5 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 90: fixed_sign; source clause 7394.
private theorem sound089 : C.clause (decodeClause atoms clause089) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 91: fixed_sign; source clause 7395.
private theorem sound090 : C.clause (decodeClause atoms clause090) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 92: fixed_sign; source clause 7396.
private theorem sound091 : C.clause (decodeClause atoms clause091) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 93: fixed_sign; source clause 7397.
private theorem sound092 : C.clause (decodeClause atoms clause092) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 3 4 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 94: fixed_sign; source clause 7398.
private theorem sound093 : C.clause (decodeClause atoms clause093) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 3 5 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 95: fixed_sign; source clause 7399.
private theorem sound094 : C.clause (decodeClause atoms clause094) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 3 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 96: fixed_sign; source clause 7400.
private theorem sound095 : C.clause (decodeClause atoms clause095) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 5 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 97: fixed_sign; source clause 7401.
private theorem sound096 : C.clause (decodeClause atoms clause096) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 98: fixed_sign; source clause 7402.
private theorem sound097 : C.clause (decodeClause atoms clause097) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 99: fixed_sign; source clause 7403.
private theorem sound098 : C.clause (decodeClause atoms clause098) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 100: fixed_sign; source clause 7404.
private theorem sound099 : C.clause (decodeClause atoms clause099) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 5 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 101: fixed_sign; source clause 7405.
private theorem sound100 : C.clause (decodeClause atoms clause100) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 5 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 102: fixed_sign; source clause 7406.
private theorem sound101 : C.clause (decodeClause atoms clause101) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 5 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 103: fixed_sign; source clause 7407.
private theorem sound102 : C.clause (decodeClause atoms clause102) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 6 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 104: fixed_sign; source clause 7408.
private theorem sound103 : C.clause (decodeClause atoms clause103) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 6 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 105: fixed_sign; source clause 7409.
private theorem sound104 : C.clause (decodeClause atoms clause104) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 7 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 106: fixed_sign; source clause 7410.
private theorem sound105 : C.clause (decodeClause atoms clause105) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 3 4 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 107: fixed_sign; source clause 7411.
private theorem sound106 : C.clause (decodeClause atoms clause106) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 3 5 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 108: fixed_sign; source clause 7412.
private theorem sound107 : C.clause (decodeClause atoms clause107) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 3 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 109: fixed_sign; source clause 7413.
private theorem sound108 : C.clause (decodeClause atoms clause108) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 5 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 110: fixed_sign; source clause 7414.
private theorem sound109 : C.clause (decodeClause atoms clause109) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 111: fixed_sign; source clause 7415.
private theorem sound110 : C.clause (decodeClause atoms clause110) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 112: fixed_sign; source clause 7416.
private theorem sound111 : C.clause (decodeClause atoms clause111) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 113: fixed_sign; source clause 7417.
private theorem sound112 : C.clause (decodeClause atoms clause112) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 5 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 114: fixed_sign; source clause 7418.
private theorem sound113 : C.clause (decodeClause atoms clause113) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 5 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 115: fixed_sign; source clause 7419.
private theorem sound114 : C.clause (decodeClause atoms clause114) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 5 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 116: fixed_sign; source clause 7420.
private theorem sound115 : C.clause (decodeClause atoms clause115) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 6 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 117: fixed_sign; source clause 7421.
private theorem sound116 : C.clause (decodeClause atoms clause116) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 6 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 118: fixed_sign; source clause 7422.
private theorem sound117 : C.clause (decodeClause atoms clause117) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 7 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 119: fixed_sign; source clause 7423.
private theorem sound118 : C.clause (decodeClause atoms clause118) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 4 5 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 120: fixed_sign; source clause 7424.
private theorem sound119 : C.clause (decodeClause atoms clause119) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 4 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 121: fixed_sign; source clause 7425.
private theorem sound120 : C.clause (decodeClause atoms clause120) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 122: fixed_sign; source clause 7426.
private theorem sound121 : C.clause (decodeClause atoms clause121) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 6 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 123: fixed_sign; source clause 7427.
private theorem sound122 : C.clause (decodeClause atoms clause122) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 6 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 124: fixed_sign; source clause 7428.
private theorem sound123 : C.clause (decodeClause atoms clause123) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 7 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 125: fixed_sign; source clause 7429.
private theorem sound124 : C.clause (decodeClause atoms clause124) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 5 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 126: fixed_sign; source clause 7430.
private theorem sound125 : C.clause (decodeClause atoms clause125) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 5 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 127: fixed_sign; source clause 7431.
private theorem sound126 : C.clause (decodeClause atoms clause126) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 5 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 128: fixed_sign; source clause 7432.
private theorem sound127 : C.clause (decodeClause atoms clause127) := by
  exact C.covered_clause _ _ (C.fixed_negative 4 6 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 129: fixed_sign; source clause 7433.
private theorem sound128 : C.clause (decodeClause atoms clause128) := by
  exact C.covered_clause _ _ (C.fixed_negative 4 6 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 130: fixed_sign; source clause 7434.
private theorem sound129 : C.clause (decodeClause atoms clause129) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 7 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 131: fixed_sign; source clause 7435.
private theorem sound130 : C.clause (decodeClause atoms clause130) := by
  exact C.covered_clause _ _ (C.fixed_negative 5 6 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 132: fixed_sign; source clause 7436.
private theorem sound131 : C.clause (decodeClause atoms clause131) := by
  exact C.covered_clause _ _ (C.fixed_negative 5 6 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 133: fixed_sign; source clause 7437.
private theorem sound132 : C.clause (decodeClause atoms clause132) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 7 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 134: fixed_sign; source clause 7438.
private theorem sound133 : C.clause (decodeClause atoms clause133) := by
  exact C.covered_clause _ _ (C.fixed_positive 6 7 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 135: convex_four; source clause 7854.
private theorem sound134 : C.clause (decodeClause atoms clause134) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 136: convex_four; source clause 8062.
private theorem sound135 : C.clause (decodeClause atoms clause135) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 137: convex_four; source clause 8270.
private theorem sound136 : C.clause (decodeClause atoms clause136) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 138: convex_four; source clause 8478.
private theorem sound137 : C.clause (decodeClause atoms clause137) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 139: convex_four; source clause 8686.
private theorem sound138 : C.clause (decodeClause atoms clause138) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 140: packet; source clause 9110.
private theorem sound139 : C.clause (decodeClause atoms clause139) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 141: packet; source clause 9526.
private theorem sound140 : C.clause (decodeClause atoms clause140) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 3 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 142: convex_four; source clause 9934.
private theorem sound141 : C.clause (decodeClause atoms clause141) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 143: packet; source clause 9942.
private theorem sound142 : C.clause (decodeClause atoms clause142) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 144: convex_four; source clause 10142.
private theorem sound143 : C.clause (decodeClause atoms clause143) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 145: convex_four; source clause 10350.
private theorem sound144 : C.clause (decodeClause atoms clause144) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 146: convex_four; source clause 10558.
private theorem sound145 : C.clause (decodeClause atoms clause145) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 147: convex_four; source clause 10766.
private theorem sound146 : C.clause (decodeClause atoms clause146) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 5 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 148: convex_four; source clause 10974.
private theorem sound147 : C.clause (decodeClause atoms clause147) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 149: convex_four; source clause 11182.
private theorem sound148 : C.clause (decodeClause atoms clause148) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 150: convex_four; source clause 11387.
private theorem sound149 : C.clause (decodeClause atoms clause149) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 151: convex_four; source clause 11595.
private theorem sound150 : C.clause (decodeClause atoms clause150) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 152: convex_four; source clause 11806.
private theorem sound151 : C.clause (decodeClause atoms clause151) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 153: convex_four; source clause 13054.
private theorem sound152 : C.clause (decodeClause atoms clause152) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 4 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 154: packet; source clause 13093.
private theorem sound153 : C.clause (decodeClause atoms clause153) := by
  exact C.covered_clause _ _ (C.packet_clause 0 6 2 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 155: convex_four; source clause 13262.
private theorem sound154 : C.clause (decodeClause atoms clause154) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 156: convex_four; source clause 13470.
private theorem sound155 : C.clause (decodeClause atoms clause155) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 4 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 157: convex_four; source clause 13678.
private theorem sound156 : C.clause (decodeClause atoms clause156) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 158: convex_four; source clause 13886.
private theorem sound157 : C.clause (decodeClause atoms clause157) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 5 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 159: convex_four; source clause 14094.
private theorem sound158 : C.clause (decodeClause atoms clause158) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 160: convex_four; source clause 14302.
private theorem sound159 : C.clause (decodeClause atoms clause159) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 161: convex_four; source clause 14507.
private theorem sound160 : C.clause (decodeClause atoms clause160) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 162: packet; source clause 14512.
private theorem sound161 : C.clause (decodeClause atoms clause161) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 163: convex_four; source clause 14707.
private theorem sound162 : C.clause (decodeClause atoms clause162) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 164: convex_four; source clause 14715.
private theorem sound163 : C.clause (decodeClause atoms clause163) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 165: convex_four; source clause 14926.
private theorem sound164 : C.clause (decodeClause atoms clause164) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 166: packet; source clause 15148.
private theorem sound165 : C.clause (decodeClause atoms clause165) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 6 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 167: packet; source clause 16592.
private theorem sound166 : C.clause (decodeClause atoms clause166) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 168: convex_four; source clause 17214.
private theorem sound167 : C.clause (decodeClause atoms clause167) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 5 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 169: convex_four; source clause 17422.
private theorem sound168 : C.clause (decodeClause atoms clause168) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 170: convex_four; source clause 17630.
private theorem sound169 : C.clause (decodeClause atoms clause169) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 171: convex_four; source clause 17835.
private theorem sound170 : C.clause (decodeClause atoms clause170) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 172: packet; source clause 17840.
private theorem sound171 : C.clause (decodeClause atoms clause171) := by
  exact C.covered_clause _ _ (C.packet_clause 0 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 173: packet; source clause 17842.
private theorem sound172 : C.clause (decodeClause atoms clause172) := by
  exact C.covered_clause _ _ (C.packet_clause 0 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 174: convex_four; source clause 18035.
private theorem sound173 : C.clause (decodeClause atoms clause173) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 175: convex_four; source clause 18043.
private theorem sound174 : C.clause (decodeClause atoms clause174) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 176: convex_four; source clause 18045.
private theorem sound175 : C.clause (decodeClause atoms clause175) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true false) (by decide +kernel)

-- Clause 177: convex_four; source clause 18254.
private theorem sound176 : C.clause (decodeClause atoms clause176) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 178: packet; source clause 18277.
private theorem sound177 : C.clause (decodeClause atoms clause177) := by
  exact C.covered_clause _ _ (C.packet_clause 0 6 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 179: convex_four; source clause 18459.
private theorem sound178 : C.clause (decodeClause atoms clause178) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 180: packet; source clause 18464.
private theorem sound179 : C.clause (decodeClause atoms clause179) := by
  exact C.covered_clause _ _ (C.packet_clause 0 5 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 181: packet; source clause 18485.
private theorem sound180 : C.clause (decodeClause atoms clause180) := by
  exact C.covered_clause _ _ (C.packet_clause 0 6 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 182: convex_four; source clause 18659.
private theorem sound181 : C.clause (decodeClause atoms clause181) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 183: convex_four; source clause 18667.
private theorem sound182 : C.clause (decodeClause atoms clause182) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 184: convex_four; source clause 18878.
private theorem sound183 : C.clause (decodeClause atoms clause183) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 185: packet; source clause 18885.
private theorem sound184 : C.clause (decodeClause atoms clause184) := by
  exact C.covered_clause _ _ (C.packet_clause 0 6 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 186: packet; source clause 18896.
private theorem sound185 : C.clause (decodeClause atoms clause185) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 187: convex_four; source clause 19074.
private theorem sound186 : C.clause (decodeClause atoms clause186) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 188: convex_four; source clause 19082.
private theorem sound187 : C.clause (decodeClause atoms clause187) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 189: convex_four; source clause 19291.
private theorem sound188 : C.clause (decodeClause atoms clause188) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 190: convex_four; source clause 19499.
private theorem sound189 : C.clause (decodeClause atoms clause189) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 191: packet; source clause 19510.
private theorem sound190 : C.clause (decodeClause atoms clause190) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 192: packet; source clause 19637.
private theorem sound191 : C.clause (decodeClause atoms clause191) := by
  exact C.covered_clause _ _ (C.packet_clause 3 6 1 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 193: convex_four; source clause 19707.
private theorem sound192 : C.clause (decodeClause atoms clause192) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 194: convex_four; source clause 19915.
private theorem sound193 : C.clause (decodeClause atoms clause193) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 195: packet; source clause 19926.
private theorem sound194 : C.clause (decodeClause atoms clause194) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 3 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 196: packet; source clause 20021.
private theorem sound195 : C.clause (decodeClause atoms clause195) := by
  exact C.covered_clause _ _ (C.packet_clause 3 1 2 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 197: convex_four; source clause 20123.
private theorem sound196 : C.clause (decodeClause atoms clause196) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 198: convex_four; source clause 20334.
private theorem sound197 : C.clause (decodeClause atoms clause197) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 4 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 199: convex_four; source clause 20542.
private theorem sound198 : C.clause (decodeClause atoms clause198) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 200: convex_four; source clause 20750.
private theorem sound199 : C.clause (decodeClause atoms clause199) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 4 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 201: convex_four; source clause 20958.
private theorem sound200 : C.clause (decodeClause atoms clause200) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 202: convex_four; source clause 21166.
private theorem sound201 : C.clause (decodeClause atoms clause201) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 5 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 203: convex_four; source clause 21374.
private theorem sound202 : C.clause (decodeClause atoms clause202) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 204: convex_four; source clause 21582.
private theorem sound203 : C.clause (decodeClause atoms clause203) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 205: convex_four; source clause 21787.
private theorem sound204 : C.clause (decodeClause atoms clause204) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 206: convex_four; source clause 21995.
private theorem sound205 : C.clause (decodeClause atoms clause205) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 207: convex_four; source clause 22206.
private theorem sound206 : C.clause (decodeClause atoms clause206) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 208: convex_four; source clause 22402.
private theorem sound207 : C.clause (decodeClause atoms clause207) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 4 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 209: convex_four; source clause 22610.
private theorem sound208 : C.clause (decodeClause atoms clause208) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 210: convex_four; source clause 22818.
private theorem sound209 : C.clause (decodeClause atoms clause209) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 4 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 211: convex_four; source clause 23026.
private theorem sound210 : C.clause (decodeClause atoms clause210) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 212: convex_four; source clause 23234.
private theorem sound211 : C.clause (decodeClause atoms clause211) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 5 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 213: convex_four; source clause 23442.
private theorem sound212 : C.clause (decodeClause atoms clause212) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 214: convex_four; source clause 23650.
private theorem sound213 : C.clause (decodeClause atoms clause213) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 215: convex_four; source clause 23855.
private theorem sound214 : C.clause (decodeClause atoms clause214) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 216: packet; source clause 23920.
private theorem sound215 : C.clause (decodeClause atoms clause215) := by
  exact C.covered_clause _ _ (C.packet_clause 3 1 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 217: convex_four; source clause 24063.
private theorem sound216 : C.clause (decodeClause atoms clause216) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 218: convex_four; source clause 24071.
private theorem sound217 : C.clause (decodeClause atoms clause217) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 219: convex_four; source clause 24274.
private theorem sound218 : C.clause (decodeClause atoms clause218) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 220: convex_four; source clause 24278.
private theorem sound219 : C.clause (decodeClause atoms clause219) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true true) (by decide +kernel)

-- Clause 221: convex_four; source clause 24494.
private theorem sound220 : C.clause (decodeClause atoms clause220) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 5 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 222: convex_four; source clause 24702.
private theorem sound221 : C.clause (decodeClause atoms clause221) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 223: convex_four; source clause 24910.
private theorem sound222 : C.clause (decodeClause atoms clause222) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 224: convex_four; source clause 25115.
private theorem sound223 : C.clause (decodeClause atoms clause223) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 225: convex_four; source clause 25323.
private theorem sound224 : C.clause (decodeClause atoms clause224) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 226: convex_four; source clause 25534.
private theorem sound225 : C.clause (decodeClause atoms clause225) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 227: convex_four; source clause 25739.
private theorem sound226 : C.clause (decodeClause atoms clause226) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 228: convex_four; source clause 25947.
private theorem sound227 : C.clause (decodeClause atoms clause227) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 229: convex_four; source clause 26158.
private theorem sound228 : C.clause (decodeClause atoms clause228) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 230: convex_four; source clause 26354.
private theorem sound229 : C.clause (decodeClause atoms clause229) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 231: convex_four; source clause 26562.
private theorem sound230 : C.clause (decodeClause atoms clause230) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 4 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 232: packet; source clause 26661.
private theorem sound231 : C.clause (decodeClause atoms clause231) := by
  exact C.covered_clause _ _ (C.packet_clause 3 6 2 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 233: convex_four; source clause 26770.
private theorem sound232 : C.clause (decodeClause atoms clause232) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 234: convex_four; source clause 26978.
private theorem sound233 : C.clause (decodeClause atoms clause233) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 4 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 235: packet; source clause 27045.
private theorem sound234 : C.clause (decodeClause atoms clause234) := by
  exact C.covered_clause _ _ (C.packet_clause 3 2 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 236: convex_four; source clause 27186.
private theorem sound235 : C.clause (decodeClause atoms clause235) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 237: convex_four; source clause 27394.
private theorem sound236 : C.clause (decodeClause atoms clause236) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 5 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 238: convex_four; source clause 27602.
private theorem sound237 : C.clause (decodeClause atoms clause237) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 239: convex_four; source clause 27810.
private theorem sound238 : C.clause (decodeClause atoms clause238) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 240: convex_four; source clause 28015.
private theorem sound239 : C.clause (decodeClause atoms clause239) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 241: packet; source clause 28080.
private theorem sound240 : C.clause (decodeClause atoms clause240) := by
  exact C.covered_clause _ _ (C.packet_clause 3 2 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 242: convex_four; source clause 28223.
private theorem sound241 : C.clause (decodeClause atoms clause241) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 243: convex_four; source clause 28231.
private theorem sound242 : C.clause (decodeClause atoms clause242) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 244: convex_four; source clause 28434.
private theorem sound243 : C.clause (decodeClause atoms clause243) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 245: convex_four; source clause 28438.
private theorem sound244 : C.clause (decodeClause atoms clause244) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true true) (by decide +kernel)

-- Clause 246: convex_four; source clause 28654.
private theorem sound245 : C.clause (decodeClause atoms clause245) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 5 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 247: convex_four; source clause 28862.
private theorem sound246 : C.clause (decodeClause atoms clause246) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 248: convex_four; source clause 29070.
private theorem sound247 : C.clause (decodeClause atoms clause247) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 249: convex_four; source clause 29275.
private theorem sound248 : C.clause (decodeClause atoms clause248) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 250: convex_four; source clause 29483.
private theorem sound249 : C.clause (decodeClause atoms clause249) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 251: convex_four; source clause 29694.
private theorem sound250 : C.clause (decodeClause atoms clause250) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 252: convex_four; source clause 29899.
private theorem sound251 : C.clause (decodeClause atoms clause251) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 253: convex_four; source clause 30107.
private theorem sound252 : C.clause (decodeClause atoms clause252) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 254: convex_four; source clause 30318.
private theorem sound253 : C.clause (decodeClause atoms clause253) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 255: convex_four; source clause 30514.
private theorem sound254 : C.clause (decodeClause atoms clause254) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 256: convex_four; source clause 30734.
private theorem sound255 : C.clause (decodeClause atoms clause255) := by
  exact C.covered_clause _ _ (C.convex_clause 3 4 5 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 257: convex_four; source clause 30942.
private theorem sound256 : C.clause (decodeClause atoms clause256) := by
  exact C.covered_clause _ _ (C.convex_clause 3 4 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 258: convex_four; source clause 31150.
private theorem sound257 : C.clause (decodeClause atoms clause257) := by
  exact C.covered_clause _ _ (C.convex_clause 3 4 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 259: packet; source clause 31173.
private theorem sound258 : C.clause (decodeClause atoms clause258) := by
  exact C.covered_clause _ _ (C.packet_clause 3 6 4 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 260: convex_four; source clause 31355.
private theorem sound259 : C.clause (decodeClause atoms clause259) := by
  exact C.covered_clause _ _ (C.convex_clause 3 4 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 261: convex_four; source clause 31555.
private theorem sound260 : C.clause (decodeClause atoms clause260) := by
  exact C.covered_clause _ _ (C.convex_clause 3 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 262: convex_four; source clause 31563.
private theorem sound261 : C.clause (decodeClause atoms clause261) := by
  exact C.covered_clause _ _ (C.convex_clause 3 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 263: packet; source clause 31573.
private theorem sound262 : C.clause (decodeClause atoms clause262) := by
  exact C.covered_clause _ _ (C.packet_clause 3 4 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 264: convex_four; source clause 31770.
private theorem sound263 : C.clause (decodeClause atoms clause263) := by
  exact C.covered_clause _ _ (C.convex_clause 3 4 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 265: convex_four; source clause 31774.
private theorem sound264 : C.clause (decodeClause atoms clause264) := by
  exact C.covered_clause _ _ (C.convex_clause 3 4 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 266: packet; source clause 31797.
private theorem sound265 : C.clause (decodeClause atoms clause265) := by
  exact C.covered_clause _ _ (C.packet_clause 3 6 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 267: convex_four; source clause 31979.
private theorem sound266 : C.clause (decodeClause atoms clause266) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 268: convex_four; source clause 32179.
private theorem sound267 : C.clause (decodeClause atoms clause267) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 269: convex_four; source clause 32187.
private theorem sound268 : C.clause (decodeClause atoms clause268) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 270: packet; source clause 32197.
private theorem sound269 : C.clause (decodeClause atoms clause269) := by
  exact C.covered_clause _ _ (C.packet_clause 3 5 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 271: convex_four; source clause 32394.
private theorem sound270 : C.clause (decodeClause atoms clause270) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 272: convex_four; source clause 32398.
private theorem sound271 : C.clause (decodeClause atoms clause271) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 273: convex_four; source clause 32594.
private theorem sound272 : C.clause (decodeClause atoms clause272) := by
  exact C.covered_clause _ _ (C.convex_clause 3 6 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 274: convex_four; source clause 32811.
private theorem sound273 : C.clause (decodeClause atoms clause273) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 275: convex_four; source clause 33019.
private theorem sound274 : C.clause (decodeClause atoms clause274) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 276: convex_four; source clause 33230.
private theorem sound275 : C.clause (decodeClause atoms clause275) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 277: convex_four; source clause 33426.
private theorem sound276 : C.clause (decodeClause atoms clause276) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 278: convex_four; source clause 33634.
private theorem sound277 : C.clause (decodeClause atoms clause277) := by
  exact C.covered_clause _ _ (C.convex_clause 5 6 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 279: no_octagon; source clause 33648.
private theorem sound278 : C.clause (decodeClause atoms clause278) := by
  exact C.no_octagon_clause {0, 1, 2, 4, 5, 6, 7, 8} (by decide +kernel) _ (by decide +kernel)

-- Clause 280: no_octagon; source clause 33649.
private theorem sound279 : C.clause (decodeClause atoms clause279) := by
  exact C.no_octagon_clause {1, 2, 3, 4, 5, 6, 7, 8} (by decide +kernel) _ (by decide +kernel)

private theorem all_sound : List.Forall (fun cl => C.clause (decodeClause atoms cl)) clauses := by
  exact And.intro (sound000 C) (And.intro (sound001 C) (And.intro (sound002 C) (And.intro (sound003 C) (And.intro (sound004 C) (And.intro (sound005 C) (And.intro (sound006 C) (And.intro (sound007 C) (And.intro (sound008 C) (And.intro (sound009 C) (And.intro (sound010 C) (And.intro (sound011 C) (And.intro (sound012 C) (And.intro (sound013 C) (And.intro (sound014 C) (And.intro (sound015 C) (And.intro (sound016 C) (And.intro (sound017 C) (And.intro (sound018 C) (And.intro (sound019 C) (And.intro (sound020 C) (And.intro (sound021 C) (And.intro (sound022 C) (And.intro (sound023 C) (And.intro (sound024 C) (And.intro (sound025 C) (And.intro (sound026 C) (And.intro (sound027 C) (And.intro (sound028 C) (And.intro (sound029 C) (And.intro (sound030 C) (And.intro (sound031 C) (And.intro (sound032 C) (And.intro (sound033 C) (And.intro (sound034 C) (And.intro (sound035 C) (And.intro (sound036 C) (And.intro (sound037 C) (And.intro (sound038 C) (And.intro (sound039 C) (And.intro (sound040 C) (And.intro (sound041 C) (And.intro (sound042 C) (And.intro (sound043 C) (And.intro (sound044 C) (And.intro (sound045 C) (And.intro (sound046 C) (And.intro (sound047 C) (And.intro (sound048 C) (And.intro (sound049 C) (And.intro (sound050 C) (And.intro (sound051 C) (And.intro (sound052 C) (And.intro (sound053 C) (And.intro (sound054 C) (And.intro (sound055 C) (And.intro (sound056 C) (And.intro (sound057 C) (And.intro (sound058 C) (And.intro (sound059 C) (And.intro (sound060 C) (And.intro (sound061 C) (And.intro (sound062 C) (And.intro (sound063 C) (And.intro (sound064 C) (And.intro (sound065 C) (And.intro (sound066 C) (And.intro (sound067 C) (And.intro (sound068 C) (And.intro (sound069 C) (And.intro (sound070 C) (And.intro (sound071 C) (And.intro (sound072 C) (And.intro (sound073 C) (And.intro (sound074 C) (And.intro (sound075 C) (And.intro (sound076 C) (And.intro (sound077 C) (And.intro (sound078 C) (And.intro (sound079 C) (And.intro (sound080 C) (And.intro (sound081 C) (And.intro (sound082 C) (And.intro (sound083 C) (And.intro (sound084 C) (And.intro (sound085 C) (And.intro (sound086 C) (And.intro (sound087 C) (And.intro (sound088 C) (And.intro (sound089 C) (And.intro (sound090 C) (And.intro (sound091 C) (And.intro (sound092 C) (And.intro (sound093 C) (And.intro (sound094 C) (And.intro (sound095 C) (And.intro (sound096 C) (And.intro (sound097 C) (And.intro (sound098 C) (And.intro (sound099 C) (And.intro (sound100 C) (And.intro (sound101 C) (And.intro (sound102 C) (And.intro (sound103 C) (And.intro (sound104 C) (And.intro (sound105 C) (And.intro (sound106 C) (And.intro (sound107 C) (And.intro (sound108 C) (And.intro (sound109 C) (And.intro (sound110 C) (And.intro (sound111 C) (And.intro (sound112 C) (And.intro (sound113 C) (And.intro (sound114 C) (And.intro (sound115 C) (And.intro (sound116 C) (And.intro (sound117 C) (And.intro (sound118 C) (And.intro (sound119 C) (And.intro (sound120 C) (And.intro (sound121 C) (And.intro (sound122 C) (And.intro (sound123 C) (And.intro (sound124 C) (And.intro (sound125 C) (And.intro (sound126 C) (And.intro (sound127 C) (And.intro (sound128 C) (And.intro (sound129 C) (And.intro (sound130 C) (And.intro (sound131 C) (And.intro (sound132 C) (And.intro (sound133 C) (And.intro (sound134 C) (And.intro (sound135 C) (And.intro (sound136 C) (And.intro (sound137 C) (And.intro (sound138 C) (And.intro (sound139 C) (And.intro (sound140 C) (And.intro (sound141 C) (And.intro (sound142 C) (And.intro (sound143 C) (And.intro (sound144 C) (And.intro (sound145 C) (And.intro (sound146 C) (And.intro (sound147 C) (And.intro (sound148 C) (And.intro (sound149 C) (And.intro (sound150 C) (And.intro (sound151 C) (And.intro (sound152 C) (And.intro (sound153 C) (And.intro (sound154 C) (And.intro (sound155 C) (And.intro (sound156 C) (And.intro (sound157 C) (And.intro (sound158 C) (And.intro (sound159 C) (And.intro (sound160 C) (And.intro (sound161 C) (And.intro (sound162 C) (And.intro (sound163 C) (And.intro (sound164 C) (And.intro (sound165 C) (And.intro (sound166 C) (And.intro (sound167 C) (And.intro (sound168 C) (And.intro (sound169 C) (And.intro (sound170 C) (And.intro (sound171 C) (And.intro (sound172 C) (And.intro (sound173 C) (And.intro (sound174 C) (And.intro (sound175 C) (And.intro (sound176 C) (And.intro (sound177 C) (And.intro (sound178 C) (And.intro (sound179 C) (And.intro (sound180 C) (And.intro (sound181 C) (And.intro (sound182 C) (And.intro (sound183 C) (And.intro (sound184 C) (And.intro (sound185 C) (And.intro (sound186 C) (And.intro (sound187 C) (And.intro (sound188 C) (And.intro (sound189 C) (And.intro (sound190 C) (And.intro (sound191 C) (And.intro (sound192 C) (And.intro (sound193 C) (And.intro (sound194 C) (And.intro (sound195 C) (And.intro (sound196 C) (And.intro (sound197 C) (And.intro (sound198 C) (And.intro (sound199 C) (And.intro (sound200 C) (And.intro (sound201 C) (And.intro (sound202 C) (And.intro (sound203 C) (And.intro (sound204 C) (And.intro (sound205 C) (And.intro (sound206 C) (And.intro (sound207 C) (And.intro (sound208 C) (And.intro (sound209 C) (And.intro (sound210 C) (And.intro (sound211 C) (And.intro (sound212 C) (And.intro (sound213 C) (And.intro (sound214 C) (And.intro (sound215 C) (And.intro (sound216 C) (And.intro (sound217 C) (And.intro (sound218 C) (And.intro (sound219 C) (And.intro (sound220 C) (And.intro (sound221 C) (And.intro (sound222 C) (And.intro (sound223 C) (And.intro (sound224 C) (And.intro (sound225 C) (And.intro (sound226 C) (And.intro (sound227 C) (And.intro (sound228 C) (And.intro (sound229 C) (And.intro (sound230 C) (And.intro (sound231 C) (And.intro (sound232 C) (And.intro (sound233 C) (And.intro (sound234 C) (And.intro (sound235 C) (And.intro (sound236 C) (And.intro (sound237 C) (And.intro (sound238 C) (And.intro (sound239 C) (And.intro (sound240 C) (And.intro (sound241 C) (And.intro (sound242 C) (And.intro (sound243 C) (And.intro (sound244 C) (And.intro (sound245 C) (And.intro (sound246 C) (And.intro (sound247 C) (And.intro (sound248 C) (And.intro (sound249 C) (And.intro (sound250 C) (And.intro (sound251 C) (And.intro (sound252 C) (And.intro (sound253 C) (And.intro (sound254 C) (And.intro (sound255 C) (And.intro (sound256 C) (And.intro (sound257 C) (And.intro (sound258 C) (And.intro (sound259 C) (And.intro (sound260 C) (And.intro (sound261 C) (And.intro (sound262 C) (And.intro (sound263 C) (And.intro (sound264 C) (And.intro (sound265 C) (And.intro (sound266 C) (And.intro (sound267 C) (And.intro (sound268 C) (And.intro (sound269 C) (And.intro (sound270 C) (And.intro (sound271 C) (And.intro (sound272 C) (And.intro (sound273 C) (And.intro (sound274 C) (And.intro (sound275 C) (And.intro (sound276 C) (And.intro (sound277 C) (And.intro (sound278 C) (sound279 C)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

theorem context_impossible (C : Context 9 n states) : False := by
  have h : (C.valuation atoms).satisfies_fmla cnf_refutation.formula := by
    rw [formula_eq]
    constructor
    intro cl hc
    exact C.satisfies_of_clause atoms cl ((List.forall_iff_forall_mem.mp (all_sound C)) cl hc)
  exact cnf_refutation (C.valuation atoms) h

#print axioms context_impossible
end ErdosSzekeres.Omission.CoupledCoreNine

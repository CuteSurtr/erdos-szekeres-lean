import ErdosSzekeres.Omission.CoupledCore13

/-! The frozen 407-clause proof applies to any literal support satisfying
its finite state-dependent prerequisites. No fresh SAT result is assumed. -/
namespace ErdosSzekeres.Omission.CoupledTemplate
open Coupled CoupledCore13
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

def emptyTests : List (Fin 13 × Fin 13) := [(1, 0), (2, 0), (5, 0), (7, 0), (9, 0), (4, 1), (9, 1), (10, 1), (12, 1), (3, 2), (4, 2), (7, 2), (10, 2), (5, 3), (7, 3), (10, 3), (6, 4), (10, 4), (7, 5), (10, 5), (8, 6), (10, 6), (10, 7), (10, 8), (11, 9), (12, 9), (12, 11)]

def domainTests : List (Fin 13 × Fin 13 × ℕ × ℕ) := [(2, 4, 1, 2), (2, 4, 1, 3), (2, 4, 1, 4), (4, 6, 3, 2), (4, 6, 4, 2), (10, 9, 1, 6), (9, 11, 3, 2), (9, 11, 3, 3), (9, 11, 3, 4), (9, 11, 3, 5), (9, 11, 3, 6), (9, 12, 3, 2), (9, 12, 3, 3), (9, 12, 3, 4), (9, 12, 3, 5), (9, 12, 3, 6), (9, 12, 4, 2), (9, 12, 4, 3), (9, 12, 4, 4), (9, 12, 4, 5), (9, 12, 4, 6)]

def positiveTests : List (Fin 13 × Fin 13 × Fin 13) := [(0, 2, 1), (0, 3, 1), (0, 5, 1), (0, 7, 1), (0, 9, 1), (0, 10, 1), (0, 2, 3), (0, 2, 4), (0, 2, 5), (0, 2, 7), (0, 2, 9), (0, 2, 10), (0, 2, 12), (0, 3, 5), (0, 3, 7), (0, 3, 9), (0, 3, 10), (0, 3, 12), (0, 5, 7), (0, 5, 9), (0, 5, 10), (0, 5, 12), (0, 7, 9), (0, 7, 10), (0, 7, 12), (1, 2, 3), (1, 2, 4), (1, 2, 5), (1, 2, 7), (1, 2, 9), (1, 2, 10), (1, 3, 5), (1, 3, 7), (1, 3, 9), (1, 3, 10), (1, 4, 6), (1, 4, 8), (1, 4, 9), (1, 4, 10), (1, 4, 11), (1, 4, 12), (1, 5, 7), (1, 5, 9), (1, 5, 10), (1, 6, 8), (1, 6, 9), (1, 6, 10), (1, 6, 11), (1, 6, 12), (1, 7, 9), (1, 7, 10), (1, 8, 9), (1, 8, 10), (1, 8, 11), (1, 8, 12), (1, 10, 9), (1, 9, 11), (1, 10, 11), (1, 10, 12), (1, 12, 11), (2, 3, 5), (2, 3, 7), (2, 3, 9), (2, 3, 10), (2, 3, 12), (2, 6, 4), (2, 5, 7), (2, 5, 9), (2, 5, 10), (2, 5, 12), (2, 7, 9), (2, 7, 10), (2, 7, 12), (3, 5, 7), (3, 5, 9), (3, 5, 10), (3, 5, 12), (3, 7, 9), (3, 7, 10), (3, 7, 12), (4, 6, 8), (4, 6, 9), (4, 6, 10), (4, 6, 11), (4, 6, 12), (4, 8, 9), (4, 8, 10), (4, 8, 11), (4, 8, 12), (4, 10, 9), (4, 10, 11), (4, 10, 12), (4, 12, 11), (5, 7, 9), (5, 7, 10), (5, 7, 12), (6, 8, 9), (6, 8, 10), (6, 8, 11), (6, 8, 12), (6, 10, 9), (6, 10, 11), (6, 10, 12), (6, 12, 11), (8, 10, 9), (8, 10, 11), (8, 10, 12), (8, 12, 11), (9, 12, 11), (10, 12, 11)]

def Compatible (σ : Fin 13 → Fin 154) : Prop :=
  (∀ t ∈ emptyTests, emptyCheck σ t.1 t.2 = true) ∧
  (∀ t ∈ domainTests, ¬Allowed σ t.1 t.2.1 (t.2.2.1, t.2.2.2)) ∧
  (∀ t ∈ positiveTests, CycleSigns.CheckTriple ResidualDomains.computedTable
    (σ t.1) (σ t.2.1) (σ t.2.2) = true)

instance (σ : Fin 13 → Fin 154) : Decidable (Compatible σ) := by
  unfold Compatible
  infer_instance

private def clause000 : Sat.Clause := [.pos 0]
private def clause001 : Sat.Clause := [.pos 1]
private def clause002 : Sat.Clause := [.pos 2]
private def clause003 : Sat.Clause := [.pos 3]
private def clause004 : Sat.Clause := [.pos 4]
private def clause005 : Sat.Clause := [.pos 7]
private def clause006 : Sat.Clause := [.pos 10]
private def clause007 : Sat.Clause := [.pos 11]
private def clause008 : Sat.Clause := [.pos 12]
private def clause009 : Sat.Clause := [.pos 13]
private def clause010 : Sat.Clause := [.neg 15, .pos 16, .neg 17, .pos 18]
private def clause011 : Sat.Clause := [.neg 15, .pos 16, .neg 18, .pos 19]
private def clause012 : Sat.Clause := [.neg 15, .pos 16, .neg 19, .pos 20]
private def clause013 : Sat.Clause := [.pos 15]
private def clause014 : Sat.Clause := [.pos 21]
private def clause015 : Sat.Clause := [.pos 24]
private def clause016 : Sat.Clause := [.pos 25]
private def clause017 : Sat.Clause := [.pos 27]
private def clause018 : Sat.Clause := [.pos 30]
private def clause019 : Sat.Clause := [.neg 31, .neg 32, .pos 33, .neg 34, .pos 35]
private def clause020 : Sat.Clause := [.neg 31, .neg 33, .neg 34, .pos 35]
private def clause021 : Sat.Clause := [.pos 31]
private def clause022 : Sat.Clause := [.pos 39]
private def clause023 : Sat.Clause := [.pos 41]
private def clause024 : Sat.Clause := [.pos 45]
private def clause025 : Sat.Clause := [.pos 46]
private def clause026 : Sat.Clause := [.pos 48]
private def clause027 : Sat.Clause := [.pos 51]
private def clause028 : Sat.Clause := [.pos 54]
private def clause029 : Sat.Clause := [.pos 56, .pos 57, .neg 58]
private def clause030 : Sat.Clause := [.neg 59, .neg 60, .pos 61, .neg 62, .pos 63]
private def clause031 : Sat.Clause := [.neg 59, .neg 60, .pos 61, .neg 63, .pos 64]
private def clause032 : Sat.Clause := [.neg 59, .neg 60, .pos 61, .neg 64, .pos 65]
private def clause033 : Sat.Clause := [.neg 59, .neg 60, .pos 61, .neg 65, .pos 66]
private def clause034 : Sat.Clause := [.neg 59, .neg 60, .pos 61, .neg 66]
private def clause035 : Sat.Clause := [.pos 59]
private def clause036 : Sat.Clause := [.neg 67, .neg 68, .pos 69, .neg 70, .pos 71]
private def clause037 : Sat.Clause := [.neg 67, .neg 68, .pos 69, .neg 71, .pos 72]
private def clause038 : Sat.Clause := [.neg 67, .neg 68, .pos 69, .neg 72, .pos 73]
private def clause039 : Sat.Clause := [.neg 67, .neg 68, .pos 69, .neg 73, .pos 74]
private def clause040 : Sat.Clause := [.neg 67, .neg 68, .pos 69, .neg 74]
private def clause041 : Sat.Clause := [.neg 67, .neg 69, .neg 70, .pos 71]
private def clause042 : Sat.Clause := [.neg 67, .neg 69, .neg 71, .pos 72]
private def clause043 : Sat.Clause := [.neg 67, .neg 69, .neg 72, .pos 73]
private def clause044 : Sat.Clause := [.neg 67, .neg 69, .neg 73, .pos 74]
private def clause045 : Sat.Clause := [.neg 67, .neg 69, .neg 74]
private def clause046 : Sat.Clause := [.pos 67]
private def clause047 : Sat.Clause := [.pos 76]
private def clause048 : Sat.Clause := [.neg 1, .neg 13, .pos 14, .neg 84]
private def clause049 : Sat.Clause := [.neg 1, .neg 15, .pos 17, .neg 85]
private def clause050 : Sat.Clause := [.neg 1, .neg 22, .pos 23, .neg 88]
private def clause051 : Sat.Clause := [.neg 4, .neg 67, .pos 70, .neg 104]
private def clause052 : Sat.Clause := [.neg 7, .neg 31, .pos 34, .neg 117]
private def clause053 : Sat.Clause := [.neg 7, .neg 36, .pos 37, .neg 119]
private def clause054 : Sat.Clause := [.neg 10, .neg 59, .pos 62, .neg 140]
private def clause055 : Sat.Clause := [.neg 10, .neg 67, .pos 70, .neg 141]
private def clause056 : Sat.Clause := [.neg 13, .neg 14, .neg 25, .pos 26, .neg 145]
private def clause057 : Sat.Clause := [.neg 13, .neg 14, .neg 28, .pos 29, .neg 147]
private def clause058 : Sat.Clause := [.neg 15, .neg 16, .neg 31, .pos 32, .pos 150]
private def clause059 : Sat.Clause := [.neg 15, .neg 20, .neg 36, .pos 38, .neg 151]
private def clause060 : Sat.Clause := [.neg 21, .pos 22, .neg 49]
private def clause061 : Sat.Clause := [.neg 22, .neg 23, .neg 67, .pos 71, .neg 161]
private def clause062 : Sat.Clause := [.neg 25, .neg 26, .neg 41, .pos 42, .neg 162]
private def clause063 : Sat.Clause := [.neg 25, .neg 26, .neg 43, .pos 44, .neg 163]
private def clause064 : Sat.Clause := [.neg 27, .pos 28, .neg 49]
private def clause065 : Sat.Clause := [.neg 28, .neg 29, .neg 67, .pos 72, .neg 170]
private def clause066 : Sat.Clause := [.neg 31, .neg 35, .neg 46, .pos 47, .neg 172]
private def clause067 : Sat.Clause := [.neg 36, .neg 38, .neg 59, .neg 182]
private def clause068 : Sat.Clause := [.neg 36, .pos 40, .neg 67]
private def clause069 : Sat.Clause := [.neg 36, .neg 37, .neg 67, .pos 71, .neg 183]
private def clause070 : Sat.Clause := [.pos 36, .neg 39, .pos 56]
private def clause071 : Sat.Clause := [.neg 41, .pos 43, .neg 49]
private def clause072 : Sat.Clause := [.neg 41, .neg 42, .neg 49, .pos 50, .neg 187]
private def clause073 : Sat.Clause := [.neg 41, .neg 42, .neg 51, .pos 52, .neg 188]
private def clause074 : Sat.Clause := [.neg 43, .neg 44, .neg 67, .pos 73, .neg 191]
private def clause075 : Sat.Clause := [.neg 46, .neg 47, .neg 54, .pos 55, .neg 193]
private def clause076 : Sat.Clause := [.neg 49, .pos 53, .neg 67]
private def clause077 : Sat.Clause := [.neg 49, .neg 50, .neg 67, .pos 74, .neg 203]
private def clause078 : Sat.Clause := [.neg 51, .pos 56, .pos 57, .neg 202]
private def clause079 : Sat.Clause := [.neg 51, .neg 52, .pos 56, .pos 58, .pos 202]
private def clause080 : Sat.Clause := [.neg 54, .neg 55, .pos 56, .pos 58, .pos 204]
private def clause081 : Sat.Clause := [.neg 59, .neg 61, .neg 76, .pos 212]
private def clause082 : Sat.Clause := [.pos 56, .neg 67, .pos 75]
private def clause083 : Sat.Clause := [.pos 56, .neg 57, .neg 59, .pos 60, .neg 210]
private def clause084 : Sat.Clause := [.pos 56, .neg 58, .neg 59, .pos 210]
private def clause085 : Sat.Clause := [.pos 56, .neg 57, .neg 67, .pos 68, .neg 211]
private def clause086 : Sat.Clause := [.neg 77]
private def clause087 : Sat.Clause := [.neg 78]
private def clause088 : Sat.Clause := [.neg 79]
private def clause089 : Sat.Clause := [.neg 80]
private def clause090 : Sat.Clause := [.neg 81]
private def clause091 : Sat.Clause := [.neg 82]
private def clause092 : Sat.Clause := [.pos 84]
private def clause093 : Sat.Clause := [.pos 85]
private def clause094 : Sat.Clause := [.pos 86]
private def clause095 : Sat.Clause := [.pos 87]
private def clause096 : Sat.Clause := [.pos 88]
private def clause097 : Sat.Clause := [.pos 89]
private def clause098 : Sat.Clause := [.pos 90]
private def clause099 : Sat.Clause := [.pos 91]
private def clause100 : Sat.Clause := [.pos 92]
private def clause101 : Sat.Clause := [.pos 93]
private def clause102 : Sat.Clause := [.pos 94]
private def clause103 : Sat.Clause := [.pos 95]
private def clause104 : Sat.Clause := [.pos 96]
private def clause105 : Sat.Clause := [.pos 97]
private def clause106 : Sat.Clause := [.pos 98]
private def clause107 : Sat.Clause := [.pos 99]
private def clause108 : Sat.Clause := [.pos 100]
private def clause109 : Sat.Clause := [.pos 101]
private def clause110 : Sat.Clause := [.pos 102]
private def clause111 : Sat.Clause := [.pos 105]
private def clause112 : Sat.Clause := [.pos 106]
private def clause113 : Sat.Clause := [.pos 107]
private def clause114 : Sat.Clause := [.pos 108]
private def clause115 : Sat.Clause := [.pos 109]
private def clause116 : Sat.Clause := [.pos 110]
private def clause117 : Sat.Clause := [.pos 112]
private def clause118 : Sat.Clause := [.pos 113]
private def clause119 : Sat.Clause := [.pos 114]
private def clause120 : Sat.Clause := [.pos 115]
private def clause121 : Sat.Clause := [.pos 117]
private def clause122 : Sat.Clause := [.pos 118]
private def clause123 : Sat.Clause := [.pos 119]
private def clause124 : Sat.Clause := [.pos 120]
private def clause125 : Sat.Clause := [.pos 121]
private def clause126 : Sat.Clause := [.pos 122]
private def clause127 : Sat.Clause := [.pos 123]
private def clause128 : Sat.Clause := [.pos 124]
private def clause129 : Sat.Clause := [.pos 125]
private def clause130 : Sat.Clause := [.pos 127]
private def clause131 : Sat.Clause := [.pos 128]
private def clause132 : Sat.Clause := [.pos 129]
private def clause133 : Sat.Clause := [.pos 130]
private def clause134 : Sat.Clause := [.pos 131]
private def clause135 : Sat.Clause := [.pos 132]
private def clause136 : Sat.Clause := [.pos 133]
private def clause137 : Sat.Clause := [.pos 135]
private def clause138 : Sat.Clause := [.pos 136]
private def clause139 : Sat.Clause := [.pos 137]
private def clause140 : Sat.Clause := [.pos 138]
private def clause141 : Sat.Clause := [.neg 139]
private def clause142 : Sat.Clause := [.pos 140]
private def clause143 : Sat.Clause := [.pos 142]
private def clause144 : Sat.Clause := [.pos 143]
private def clause145 : Sat.Clause := [.neg 144]
private def clause146 : Sat.Clause := [.pos 145]
private def clause147 : Sat.Clause := [.pos 146]
private def clause148 : Sat.Clause := [.pos 147]
private def clause149 : Sat.Clause := [.pos 148]
private def clause150 : Sat.Clause := [.pos 149]
private def clause151 : Sat.Clause := [.neg 150]
private def clause152 : Sat.Clause := [.pos 153]
private def clause153 : Sat.Clause := [.pos 154]
private def clause154 : Sat.Clause := [.pos 155]
private def clause155 : Sat.Clause := [.pos 156]
private def clause156 : Sat.Clause := [.pos 157]
private def clause157 : Sat.Clause := [.pos 158]
private def clause158 : Sat.Clause := [.pos 159]
private def clause159 : Sat.Clause := [.pos 162]
private def clause160 : Sat.Clause := [.pos 163]
private def clause161 : Sat.Clause := [.pos 164]
private def clause162 : Sat.Clause := [.pos 165]
private def clause163 : Sat.Clause := [.pos 166]
private def clause164 : Sat.Clause := [.pos 167]
private def clause165 : Sat.Clause := [.pos 168]
private def clause166 : Sat.Clause := [.pos 172]
private def clause167 : Sat.Clause := [.pos 173]
private def clause168 : Sat.Clause := [.pos 174]
private def clause169 : Sat.Clause := [.pos 175]
private def clause170 : Sat.Clause := [.pos 176]
private def clause171 : Sat.Clause := [.pos 177]
private def clause172 : Sat.Clause := [.pos 178]
private def clause173 : Sat.Clause := [.pos 179]
private def clause174 : Sat.Clause := [.pos 180]
private def clause175 : Sat.Clause := [.neg 181]
private def clause176 : Sat.Clause := [.pos 184]
private def clause177 : Sat.Clause := [.pos 185]
private def clause178 : Sat.Clause := [.neg 186]
private def clause179 : Sat.Clause := [.pos 187]
private def clause180 : Sat.Clause := [.pos 188]
private def clause181 : Sat.Clause := [.pos 189]
private def clause182 : Sat.Clause := [.pos 192]
private def clause183 : Sat.Clause := [.pos 193]
private def clause184 : Sat.Clause := [.pos 194]
private def clause185 : Sat.Clause := [.pos 195]
private def clause186 : Sat.Clause := [.neg 196]
private def clause187 : Sat.Clause := [.pos 199]
private def clause188 : Sat.Clause := [.pos 200]
private def clause189 : Sat.Clause := [.neg 201]
private def clause190 : Sat.Clause := [.neg 204]
private def clause191 : Sat.Clause := [.pos 207]
private def clause192 : Sat.Clause := [.pos 208]
private def clause193 : Sat.Clause := [.neg 209]
private def clause194 : Sat.Clause := [.neg 212]
private def clause195 : Sat.Clause := [.neg 213]
private def clause196 : Sat.Clause := [.pos 77, .pos 78, .neg 84, .neg 105, .pos 214]
private def clause197 : Sat.Clause := [.pos 77, .pos 79, .neg 86, .neg 107, .pos 215]
private def clause198 : Sat.Clause := [.pos 77, .pos 80, .neg 87, .neg 108, .pos 216]
private def clause199 : Sat.Clause := [.pos 77, .pos 81, .neg 88, .neg 109, .pos 217]
private def clause200 : Sat.Clause := [.pos 77, .pos 82, .neg 89, .neg 110, .pos 218]
private def clause201 : Sat.Clause := [.pos 77, .pos 83, .neg 90, .neg 111, .pos 219]
private def clause202 : Sat.Clause := [.pos 78, .pos 79, .neg 91, .neg 112, .pos 220]
private def clause203 : Sat.Clause := [.pos 78, .pos 80, .neg 92, .neg 113, .pos 221]
private def clause204 : Sat.Clause := [.pos 78, .pos 81, .neg 93, .neg 114, .pos 222]
private def clause205 : Sat.Clause := [.pos 78, .pos 82, .neg 94, .neg 115, .pos 223]
private def clause206 : Sat.Clause := [.pos 78, .pos 83, .neg 95, .neg 116, .pos 224]
private def clause207 : Sat.Clause := [.pos 79, .pos 80, .neg 96, .neg 123, .pos 225]
private def clause208 : Sat.Clause := [.pos 79, .pos 81, .neg 97, .neg 124, .pos 226]
private def clause209 : Sat.Clause := [.pos 79, .pos 82, .neg 98, .neg 125, .pos 227]
private def clause210 : Sat.Clause := [.pos 79, .pos 83, .neg 99, .neg 126, .pos 228]
private def clause211 : Sat.Clause := [.pos 80, .pos 81, .neg 100, .neg 132, .pos 229]
private def clause212 : Sat.Clause := [.pos 80, .pos 82, .neg 101, .neg 133, .pos 230]
private def clause213 : Sat.Clause := [.pos 80, .pos 83, .neg 102, .neg 134, .pos 231]
private def clause214 : Sat.Clause := [.neg 0, .neg 10, .neg 56, .pos 81, .pos 82, .neg 103, .pos 139]
private def clause215 : Sat.Clause := [.pos 81, .pos 82, .pos 103, .pos 139, .pos 232]
private def clause216 : Sat.Clause := [.neg 0, .neg 10, .neg 67, .pos 81, .neg 83, .pos 104, .pos 141]
private def clause217 : Sat.Clause := [.pos 81, .pos 83, .pos 104, .pos 141, .pos 233]
private def clause218 : Sat.Clause := [.neg 84, .neg 86, .neg 91, .neg 145, .pos 234]
private def clause219 : Sat.Clause := [.neg 84, .neg 87, .neg 92, .neg 146, .pos 235]
private def clause220 : Sat.Clause := [.neg 84, .neg 88, .neg 93, .neg 147, .pos 236]
private def clause221 : Sat.Clause := [.neg 84, .neg 89, .neg 94, .neg 148, .pos 237]
private def clause222 : Sat.Clause := [.neg 84, .neg 90, .neg 95, .neg 149, .pos 238]
private def clause223 : Sat.Clause := [.neg 86, .neg 87, .neg 96, .neg 153, .pos 239]
private def clause224 : Sat.Clause := [.neg 86, .neg 88, .neg 97, .neg 154, .pos 240]
private def clause225 : Sat.Clause := [.neg 86, .neg 89, .neg 98, .neg 155, .pos 241]
private def clause226 : Sat.Clause := [.neg 86, .neg 90, .neg 99, .neg 156, .pos 242]
private def clause227 : Sat.Clause := [.neg 87, .neg 88, .neg 100, .neg 157, .pos 243]
private def clause228 : Sat.Clause := [.neg 87, .neg 89, .neg 101, .neg 158, .pos 244]
private def clause229 : Sat.Clause := [.neg 87, .neg 90, .neg 102, .neg 159, .pos 245]
private def clause230 : Sat.Clause := [.neg 1, .neg 22, .neg 56, .neg 88, .neg 89, .pos 103, .neg 160]
private def clause231 : Sat.Clause := [.neg 88, .neg 89, .pos 103, .pos 160, .pos 246]
private def clause232 : Sat.Clause := [.neg 88, .neg 90, .pos 104, .pos 161, .pos 247]
private def clause233 : Sat.Clause := [.neg 91, .neg 92, .neg 96, .neg 162, .pos 248]
private def clause234 : Sat.Clause := [.neg 91, .neg 93, .neg 97, .neg 163, .pos 249]
private def clause235 : Sat.Clause := [.neg 91, .neg 94, .neg 98, .neg 164, .pos 250]
private def clause236 : Sat.Clause := [.neg 91, .neg 95, .neg 99, .neg 165, .pos 251]
private def clause237 : Sat.Clause := [.neg 92, .neg 93, .neg 100, .neg 166, .pos 252]
private def clause238 : Sat.Clause := [.neg 92, .neg 94, .neg 101, .neg 167, .pos 253]
private def clause239 : Sat.Clause := [.neg 92, .neg 95, .neg 102, .neg 168, .pos 254]
private def clause240 : Sat.Clause := [.neg 93, .neg 94, .pos 103, .pos 169, .pos 255]
private def clause241 : Sat.Clause := [.neg 93, .neg 95, .pos 104, .pos 170, .pos 256]
private def clause242 : Sat.Clause := [.neg 96, .neg 97, .neg 100, .neg 187, .pos 257]
private def clause243 : Sat.Clause := [.neg 96, .neg 98, .neg 101, .neg 188, .pos 258]
private def clause244 : Sat.Clause := [.neg 96, .neg 99, .neg 102, .neg 189, .pos 259]
private def clause245 : Sat.Clause := [.neg 2, .neg 43, .neg 56, .neg 97, .neg 98, .pos 103, .neg 190]
private def clause246 : Sat.Clause := [.neg 4, .pos 43, .neg 45, .neg 97, .neg 98, .pos 103, .neg 190]
private def clause247 : Sat.Clause := [.neg 97, .neg 98, .pos 103, .pos 190, .pos 260]
private def clause248 : Sat.Clause := [.neg 97, .neg 99, .pos 104, .pos 191, .pos 261]
private def clause249 : Sat.Clause := [.neg 3, .neg 49, .neg 56, .neg 100, .neg 101, .pos 103, .neg 202]
private def clause250 : Sat.Clause := [.neg 100, .neg 101, .pos 103, .pos 202, .pos 262]
private def clause251 : Sat.Clause := [.neg 100, .neg 102, .pos 104, .pos 203, .pos 263]
private def clause252 : Sat.Clause := [.neg 105, .neg 107, .neg 112, .neg 145, .pos 264]
private def clause253 : Sat.Clause := [.neg 105, .neg 108, .neg 113, .neg 146, .pos 265]
private def clause254 : Sat.Clause := [.neg 105, .neg 109, .neg 114, .neg 147, .pos 266]
private def clause255 : Sat.Clause := [.neg 105, .neg 110, .neg 115, .neg 148, .pos 267]
private def clause256 : Sat.Clause := [.neg 105, .neg 111, .neg 116, .neg 149, .pos 268]
private def clause257 : Sat.Clause := [.neg 5, .neg 15, .neg 40, .neg 106, .pos 111, .neg 122, .pos 152]
private def clause258 : Sat.Clause := [.neg 107, .neg 108, .neg 123, .neg 153, .pos 269]
private def clause259 : Sat.Clause := [.neg 107, .neg 109, .neg 124, .neg 154, .pos 270]
private def clause260 : Sat.Clause := [.neg 107, .neg 110, .neg 125, .neg 155, .pos 271]
private def clause261 : Sat.Clause := [.neg 107, .neg 111, .neg 126, .neg 156, .pos 272]
private def clause262 : Sat.Clause := [.neg 108, .neg 109, .neg 132, .neg 157, .pos 273]
private def clause263 : Sat.Clause := [.neg 108, .neg 110, .neg 133, .neg 158, .pos 274]
private def clause264 : Sat.Clause := [.neg 5, .neg 21, .neg 53, .neg 108, .neg 111, .pos 134, .neg 159]
private def clause265 : Sat.Clause := [.pos 5, .neg 9, .neg 53, .neg 108, .neg 111, .pos 134, .neg 159]
private def clause266 : Sat.Clause := [.pos 9, .neg 12, .neg 21, .neg 108, .neg 111, .pos 134, .neg 159]
private def clause267 : Sat.Clause := [.neg 108, .neg 111, .neg 134, .neg 159, .pos 275]
private def clause268 : Sat.Clause := [.neg 10, .pos 22, .neg 24, .neg 109, .neg 110, .pos 139, .neg 160]
private def clause269 : Sat.Clause := [.neg 109, .neg 110, .pos 139, .pos 160, .pos 276]
private def clause270 : Sat.Clause := [.pos 5, .neg 10, .neg 67, .neg 109, .pos 111, .pos 141, .pos 161]
private def clause271 : Sat.Clause := [.neg 109, .neg 111, .pos 141, .pos 161, .pos 277]
private def clause272 : Sat.Clause := [.neg 112, .neg 113, .neg 123, .neg 162, .pos 278]
private def clause273 : Sat.Clause := [.neg 112, .neg 114, .neg 124, .neg 163, .pos 279]
private def clause274 : Sat.Clause := [.neg 112, .neg 115, .neg 125, .neg 164, .pos 280]
private def clause275 : Sat.Clause := [.neg 112, .neg 116, .neg 126, .neg 165, .pos 281]
private def clause276 : Sat.Clause := [.neg 113, .neg 114, .neg 132, .neg 166, .pos 282]
private def clause277 : Sat.Clause := [.neg 113, .neg 115, .neg 133, .neg 167, .pos 283]
private def clause278 : Sat.Clause := [.neg 113, .pos 116, .neg 134, .neg 168, .neg 284]
private def clause279 : Sat.Clause := [.neg 113, .neg 116, .neg 134, .neg 168, .pos 284]
private def clause280 : Sat.Clause := [.neg 10, .pos 28, .neg 30, .neg 114, .neg 115, .pos 139, .neg 169]
private def clause281 : Sat.Clause := [.neg 114, .neg 115, .pos 139, .pos 169, .pos 285]
private def clause282 : Sat.Clause := [.pos 6, .neg 10, .neg 67, .neg 114, .pos 116, .pos 141, .pos 170]
private def clause283 : Sat.Clause := [.neg 114, .neg 116, .pos 141, .pos 170, .pos 286]
private def clause284 : Sat.Clause := [.neg 6, .neg 30, .neg 75, .neg 115, .pos 116, .neg 143, .pos 171]
private def clause285 : Sat.Clause := [.neg 6, .neg 30, .neg 75, .neg 115, .pos 116, .neg 143, .neg 171]
private def clause286 : Sat.Clause := [.neg 117, .neg 118, .neg 127, .neg 172, .pos 287]
private def clause287 : Sat.Clause := [.neg 117, .neg 119, .neg 128, .neg 173, .pos 288]
private def clause288 : Sat.Clause := [.neg 117, .neg 120, .neg 129, .neg 174, .pos 289]
private def clause289 : Sat.Clause := [.neg 117, .neg 121, .neg 130, .neg 175, .pos 290]
private def clause290 : Sat.Clause := [.neg 117, .neg 122, .neg 131, .neg 176, .pos 291]
private def clause291 : Sat.Clause := [.neg 118, .neg 119, .neg 135, .neg 177, .pos 292]
private def clause292 : Sat.Clause := [.neg 118, .neg 120, .neg 136, .neg 178, .pos 293]
private def clause293 : Sat.Clause := [.neg 118, .neg 121, .neg 137, .neg 179, .pos 294]
private def clause294 : Sat.Clause := [.neg 118, .neg 122, .neg 138, .neg 180, .pos 295]
private def clause295 : Sat.Clause := [.neg 119, .neg 120, .pos 139, .pos 181, .pos 296]
private def clause296 : Sat.Clause := [.neg 119, .neg 121, .neg 140, .neg 182, .pos 297]
private def clause297 : Sat.Clause := [.neg 119, .neg 122, .neg 141, .neg 183, .pos 298]
private def clause298 : Sat.Clause := [.neg 120, .neg 121, .neg 142, .neg 184, .pos 299]
private def clause299 : Sat.Clause := [.neg 120, .neg 122, .neg 143, .neg 185, .pos 300]
private def clause300 : Sat.Clause := [.neg 121, .neg 122, .pos 144, .pos 186, .pos 301]
private def clause301 : Sat.Clause := [.neg 123, .neg 124, .neg 132, .neg 187, .pos 302]
private def clause302 : Sat.Clause := [.neg 123, .neg 125, .neg 133, .neg 188, .pos 303]
private def clause303 : Sat.Clause := [.neg 8, .neg 41, .neg 53, .neg 123, .pos 126, .neg 134, .neg 189]
private def clause304 : Sat.Clause := [.neg 123, .pos 126, .neg 134, .neg 189, .neg 304]
private def clause305 : Sat.Clause := [.neg 123, .neg 126, .neg 134, .neg 189, .pos 304]
private def clause306 : Sat.Clause := [.neg 124, .neg 125, .pos 139, .pos 190, .pos 305]
private def clause307 : Sat.Clause := [.pos 8, .neg 10, .neg 67, .neg 124, .pos 126, .pos 141, .pos 191]
private def clause308 : Sat.Clause := [.neg 124, .neg 126, .pos 141, .pos 191, .pos 306]
private def clause309 : Sat.Clause := [.neg 127, .neg 128, .neg 135, .neg 192, .pos 307]
private def clause310 : Sat.Clause := [.neg 127, .neg 129, .neg 136, .neg 193, .pos 308]
private def clause311 : Sat.Clause := [.neg 127, .neg 130, .neg 137, .neg 194, .pos 309]
private def clause312 : Sat.Clause := [.neg 127, .neg 131, .neg 138, .neg 195, .pos 310]
private def clause313 : Sat.Clause := [.neg 128, .neg 129, .pos 139, .pos 196, .pos 311]
private def clause314 : Sat.Clause := [.neg 128, .neg 130, .neg 140, .neg 197, .pos 312]
private def clause315 : Sat.Clause := [.neg 128, .neg 131, .neg 141, .neg 198, .pos 313]
private def clause316 : Sat.Clause := [.neg 129, .neg 130, .neg 142, .neg 199, .pos 314]
private def clause317 : Sat.Clause := [.neg 129, .neg 131, .neg 143, .neg 200, .pos 315]
private def clause318 : Sat.Clause := [.neg 130, .neg 131, .pos 144, .pos 201, .pos 316]
private def clause319 : Sat.Clause := [.neg 10, .pos 49, .neg 51, .neg 132, .neg 133, .pos 139, .neg 202]
private def clause320 : Sat.Clause := [.neg 132, .neg 133, .pos 139, .pos 202, .pos 317]
private def clause321 : Sat.Clause := [.neg 132, .neg 134, .pos 141, .pos 203, .pos 318]
private def clause322 : Sat.Clause := [.neg 135, .neg 136, .pos 139, .pos 204, .pos 319]
private def clause323 : Sat.Clause := [.neg 135, .neg 137, .neg 140, .neg 205, .pos 320]
private def clause324 : Sat.Clause := [.neg 135, .neg 138, .neg 141, .neg 206, .pos 321]
private def clause325 : Sat.Clause := [.neg 136, .neg 137, .neg 142, .neg 207, .pos 322]
private def clause326 : Sat.Clause := [.neg 136, .neg 138, .neg 143, .neg 208, .pos 323]
private def clause327 : Sat.Clause := [.neg 137, .neg 138, .pos 144, .pos 209, .pos 324]
private def clause328 : Sat.Clause := [.pos 139, .neg 140, .neg 142, .pos 210, .pos 325]
private def clause329 : Sat.Clause := [.neg 11, .pos 56, .neg 67, .pos 139, .pos 141, .neg 143, .pos 211]
private def clause330 : Sat.Clause := [.pos 139, .neg 141, .neg 143, .pos 211, .pos 326]
private def clause331 : Sat.Clause := [.neg 140, .neg 141, .pos 144, .pos 212, .pos 327]
private def clause332 : Sat.Clause := [.neg 142, .neg 143, .pos 144, .pos 213, .pos 328]
private def clause333 : Sat.Clause := [.neg 145, .neg 146, .neg 153, .neg 162, .pos 329]
private def clause334 : Sat.Clause := [.neg 145, .neg 147, .neg 154, .neg 163, .pos 330]
private def clause335 : Sat.Clause := [.neg 145, .neg 148, .neg 155, .neg 164, .pos 331]
private def clause336 : Sat.Clause := [.neg 145, .neg 149, .neg 156, .neg 165, .pos 332]
private def clause337 : Sat.Clause := [.neg 146, .neg 147, .neg 157, .neg 166, .pos 333]
private def clause338 : Sat.Clause := [.neg 146, .neg 148, .neg 158, .neg 167, .pos 334]
private def clause339 : Sat.Clause := [.neg 146, .neg 149, .neg 159, .neg 168, .pos 335]
private def clause340 : Sat.Clause := [.neg 13, .neg 28, .neg 56, .neg 147, .neg 148, .pos 160, .neg 169]
private def clause341 : Sat.Clause := [.neg 147, .neg 148, .pos 160, .pos 169, .pos 336]
private def clause342 : Sat.Clause := [.neg 147, .neg 149, .pos 161, .pos 170, .pos 337]
private def clause343 : Sat.Clause := [.neg 15, .neg 36, .neg 67, .pos 151, .neg 152, .pos 161, .pos 183]
private def clause344 : Sat.Clause := [.neg 153, .neg 154, .neg 157, .neg 187, .pos 338]
private def clause345 : Sat.Clause := [.neg 153, .neg 155, .neg 158, .neg 188, .pos 339]
private def clause346 : Sat.Clause := [.neg 153, .neg 156, .neg 159, .neg 189, .pos 340]
private def clause347 : Sat.Clause := [.neg 154, .neg 155, .pos 160, .pos 190, .pos 341]
private def clause348 : Sat.Clause := [.neg 154, .neg 156, .pos 161, .pos 191, .pos 342]
private def clause349 : Sat.Clause := [.neg 157, .neg 158, .pos 160, .pos 202, .pos 343]
private def clause350 : Sat.Clause := [.neg 157, .neg 158, .neg 160, .pos 202, .neg 343]
private def clause351 : Sat.Clause := [.neg 157, .neg 159, .pos 161, .pos 203, .pos 344]
private def clause352 : Sat.Clause := [.neg 162, .neg 163, .neg 166, .neg 187, .pos 345]
private def clause353 : Sat.Clause := [.neg 162, .neg 164, .neg 167, .neg 188, .pos 346]
private def clause354 : Sat.Clause := [.neg 162, .neg 165, .neg 168, .neg 189, .pos 347]
private def clause355 : Sat.Clause := [.neg 163, .neg 164, .pos 169, .pos 190, .pos 348]
private def clause356 : Sat.Clause := [.neg 163, .neg 165, .pos 170, .pos 191, .pos 349]
private def clause357 : Sat.Clause := [.neg 166, .neg 167, .pos 169, .pos 202, .pos 350]
private def clause358 : Sat.Clause := [.neg 166, .neg 167, .neg 169, .pos 202, .neg 350]
private def clause359 : Sat.Clause := [.neg 166, .neg 168, .pos 170, .pos 203, .pos 351]
private def clause360 : Sat.Clause := [.neg 172, .neg 173, .neg 177, .neg 192, .pos 352]
private def clause361 : Sat.Clause := [.neg 172, .neg 174, .neg 178, .neg 193, .pos 353]
private def clause362 : Sat.Clause := [.neg 172, .neg 175, .neg 179, .neg 194, .pos 354]
private def clause363 : Sat.Clause := [.neg 172, .neg 176, .neg 180, .neg 195, .pos 355]
private def clause364 : Sat.Clause := [.neg 173, .neg 174, .pos 181, .pos 196, .pos 356]
private def clause365 : Sat.Clause := [.neg 173, .neg 175, .neg 182, .neg 197, .pos 357]
private def clause366 : Sat.Clause := [.neg 173, .neg 176, .neg 183, .neg 198, .pos 358]
private def clause367 : Sat.Clause := [.neg 174, .neg 175, .neg 184, .neg 199, .pos 359]
private def clause368 : Sat.Clause := [.neg 174, .neg 176, .neg 185, .neg 200, .pos 360]
private def clause369 : Sat.Clause := [.neg 175, .neg 176, .pos 186, .pos 201, .pos 361]
private def clause370 : Sat.Clause := [.neg 177, .neg 178, .pos 181, .pos 204, .pos 362]
private def clause371 : Sat.Clause := [.neg 177, .neg 179, .neg 182, .neg 205, .pos 363]
private def clause372 : Sat.Clause := [.neg 177, .neg 180, .neg 183, .neg 206, .pos 364]
private def clause373 : Sat.Clause := [.neg 178, .neg 179, .neg 184, .neg 207, .pos 365]
private def clause374 : Sat.Clause := [.neg 178, .neg 180, .neg 185, .neg 208, .pos 366]
private def clause375 : Sat.Clause := [.neg 179, .neg 180, .pos 186, .pos 209, .pos 367]
private def clause376 : Sat.Clause := [.neg 39, .pos 56, .neg 59, .pos 181, .pos 182, .neg 184, .pos 210]
private def clause377 : Sat.Clause := [.pos 181, .neg 182, .neg 184, .pos 210, .pos 368]
private def clause378 : Sat.Clause := [.neg 39, .pos 56, .neg 67, .pos 181, .pos 183, .neg 185, .pos 211]
private def clause379 : Sat.Clause := [.pos 181, .neg 183, .neg 185, .pos 211, .pos 369]
private def clause380 : Sat.Clause := [.neg 182, .neg 183, .pos 186, .pos 212, .pos 370]
private def clause381 : Sat.Clause := [.neg 184, .neg 185, .pos 186, .pos 213, .pos 371]
private def clause382 : Sat.Clause := [.neg 187, .neg 188, .pos 190, .pos 202, .pos 372]
private def clause383 : Sat.Clause := [.neg 187, .neg 189, .pos 191, .pos 203, .pos 373]
private def clause384 : Sat.Clause := [.neg 192, .neg 193, .pos 196, .pos 204, .pos 374]
private def clause385 : Sat.Clause := [.neg 192, .neg 194, .neg 197, .neg 205, .pos 375]
private def clause386 : Sat.Clause := [.neg 192, .neg 195, .neg 198, .neg 206, .pos 376]
private def clause387 : Sat.Clause := [.neg 193, .neg 194, .neg 199, .neg 207, .pos 377]
private def clause388 : Sat.Clause := [.neg 193, .neg 195, .neg 200, .neg 208, .pos 378]
private def clause389 : Sat.Clause := [.neg 194, .neg 195, .pos 201, .pos 209, .pos 379]
private def clause390 : Sat.Clause := [.neg 48, .pos 56, .neg 59, .pos 196, .pos 197, .neg 199, .pos 210]
private def clause391 : Sat.Clause := [.pos 196, .neg 197, .neg 199, .pos 210, .pos 380]
private def clause392 : Sat.Clause := [.neg 48, .pos 56, .neg 67, .pos 196, .pos 198, .neg 200, .pos 211]
private def clause393 : Sat.Clause := [.pos 196, .neg 198, .neg 200, .pos 211, .pos 381]
private def clause394 : Sat.Clause := [.neg 197, .neg 198, .pos 201, .pos 212, .pos 382]
private def clause395 : Sat.Clause := [.neg 199, .neg 200, .pos 201, .pos 213, .pos 383]
private def clause396 : Sat.Clause := [.neg 54, .pos 56, .neg 59, .pos 204, .pos 205, .neg 207, .pos 210]
private def clause397 : Sat.Clause := [.pos 204, .neg 205, .neg 207, .pos 210, .pos 384]
private def clause398 : Sat.Clause := [.neg 54, .pos 56, .neg 67, .pos 204, .pos 206, .neg 208, .pos 211]
private def clause399 : Sat.Clause := [.pos 204, .neg 206, .neg 208, .pos 211, .pos 385]
private def clause400 : Sat.Clause := [.neg 205, .neg 206, .pos 209, .pos 212, .pos 386]
private def clause401 : Sat.Clause := [.neg 207, .neg 208, .pos 209, .pos 213, .pos 387]
private def clause402 : Sat.Clause := [.pos 210, .pos 211, .pos 212, .pos 213, .pos 388]
private def clause403 : Sat.Clause := [.pos 210, .neg 211, .pos 212, .pos 213, .neg 388]
private def clause404 : Sat.Clause := [.neg 214, .neg 215, .neg 216, .neg 217, .neg 218, .neg 220, .neg 221, .neg 222, .neg 223, .neg 225, .neg 226, .neg 227, .neg 229, .neg 230, .neg 232, .neg 234, .neg 235, .neg 236, .neg 237, .neg 239, .neg 240, .neg 241, .neg 243, .neg 244, .neg 246, .neg 248, .neg 249, .neg 250, .neg 252, .neg 253, .neg 255, .neg 257, .neg 258, .neg 260, .neg 262, .neg 264, .neg 265, .neg 266, .neg 267, .neg 269, .neg 270, .neg 271, .neg 273, .neg 274, .neg 276, .neg 278, .neg 279, .neg 280, .neg 282, .neg 283, .neg 285, .neg 302, .neg 303, .neg 305, .neg 317, .neg 329, .neg 330, .neg 331, .neg 333, .neg 334, .neg 336, .neg 338, .neg 339, .neg 341, .neg 343, .neg 345, .neg 346, .neg 348, .neg 350, .neg 372]
private def clause405 : Sat.Clause := [.neg 214, .neg 215, .neg 216, .neg 217, .neg 219, .neg 220, .neg 221, .neg 222, .neg 224, .neg 225, .neg 226, .neg 228, .neg 229, .neg 231, .neg 233, .neg 234, .neg 235, .neg 236, .neg 238, .neg 239, .neg 240, .neg 242, .neg 243, .neg 245, .neg 247, .neg 248, .neg 249, .neg 251, .neg 252, .neg 254, .neg 256, .neg 257, .neg 259, .neg 261, .neg 263, .neg 264, .neg 265, .neg 266, .neg 268, .neg 269, .neg 270, .neg 272, .neg 273, .neg 275, .neg 277, .neg 278, .neg 279, .neg 281, .neg 282, .neg 284, .neg 286, .neg 302, .neg 304, .neg 306, .neg 318, .neg 329, .neg 330, .neg 332, .neg 333, .neg 335, .neg 337, .neg 338, .neg 340, .neg 342, .neg 344, .neg 345, .neg 347, .neg 349, .neg 351, .neg 373]
private def clause406 : Sat.Clause := [.neg 287, .neg 288, .neg 289, .neg 290, .neg 291, .neg 292, .neg 293, .neg 294, .neg 295, .neg 296, .neg 297, .neg 298, .neg 299, .neg 300, .neg 301, .neg 307, .neg 308, .neg 309, .neg 310, .neg 311, .neg 312, .neg 313, .neg 314, .neg 315, .neg 316, .neg 319, .neg 320, .neg 321, .neg 322, .neg 323, .neg 324, .neg 325, .neg 326, .neg 327, .neg 328, .neg 352, .neg 353, .neg 354, .neg 355, .neg 356, .neg 357, .neg 358, .neg 359, .neg 360, .neg 361, .neg 362, .neg 363, .neg 364, .neg 365, .neg 366, .neg 367, .neg 368, .neg 369, .neg 370, .neg 371, .neg 374, .neg 375, .neg 376, .neg 377, .neg 378, .neg 379, .neg 380, .neg 381, .neg 382, .neg 383, .neg 384, .neg 385, .neg 386, .neg 387, .neg 388]

private def clauses : Sat.Fmla := [
  clause000, clause001, clause002, clause003, clause004, clause005, clause006, clause007, clause008, clause009, clause010, clause011, clause012, clause013, clause014, clause015, clause016, clause017, clause018, clause019, clause020, clause021, clause022, clause023, clause024, clause025, clause026, clause027, clause028, clause029, clause030, clause031, clause032, clause033, clause034, clause035, clause036, clause037, clause038, clause039, clause040, clause041, clause042, clause043, clause044, clause045, clause046, clause047, clause048, clause049, clause050, clause051, clause052, clause053, clause054, clause055, clause056, clause057, clause058, clause059, clause060, clause061, clause062, clause063, clause064, clause065, clause066, clause067, clause068, clause069, clause070, clause071, clause072, clause073, clause074, clause075, clause076, clause077, clause078, clause079, clause080, clause081, clause082, clause083, clause084, clause085, clause086, clause087, clause088, clause089, clause090, clause091, clause092, clause093, clause094, clause095, clause096, clause097, clause098, clause099, clause100, clause101, clause102, clause103, clause104, clause105, clause106, clause107, clause108, clause109, clause110, clause111, clause112, clause113, clause114, clause115, clause116, clause117, clause118, clause119, clause120, clause121, clause122, clause123, clause124, clause125, clause126, clause127, clause128, clause129, clause130, clause131, clause132, clause133, clause134, clause135, clause136, clause137, clause138, clause139, clause140, clause141, clause142, clause143, clause144, clause145, clause146, clause147, clause148, clause149, clause150, clause151, clause152, clause153, clause154, clause155, clause156, clause157, clause158, clause159, clause160, clause161, clause162, clause163, clause164, clause165, clause166, clause167, clause168, clause169, clause170, clause171, clause172, clause173, clause174, clause175, clause176, clause177, clause178, clause179, clause180, clause181, clause182, clause183, clause184, clause185, clause186, clause187, clause188, clause189, clause190, clause191, clause192, clause193, clause194, clause195, clause196, clause197, clause198, clause199, clause200, clause201, clause202, clause203, clause204, clause205, clause206, clause207, clause208, clause209, clause210, clause211, clause212, clause213, clause214, clause215, clause216, clause217, clause218, clause219, clause220, clause221, clause222, clause223, clause224, clause225, clause226, clause227, clause228, clause229, clause230, clause231, clause232, clause233, clause234, clause235, clause236, clause237, clause238, clause239, clause240, clause241, clause242, clause243, clause244, clause245, clause246, clause247, clause248, clause249, clause250, clause251, clause252, clause253, clause254, clause255, clause256, clause257, clause258, clause259, clause260, clause261, clause262, clause263, clause264, clause265, clause266, clause267, clause268, clause269, clause270, clause271, clause272, clause273, clause274, clause275, clause276, clause277, clause278, clause279, clause280, clause281, clause282, clause283, clause284, clause285, clause286, clause287, clause288, clause289, clause290, clause291, clause292, clause293, clause294, clause295, clause296, clause297, clause298, clause299, clause300, clause301, clause302, clause303, clause304, clause305, clause306, clause307, clause308, clause309, clause310, clause311, clause312, clause313, clause314, clause315, clause316, clause317, clause318, clause319, clause320, clause321, clause322, clause323, clause324, clause325, clause326, clause327, clause328, clause329, clause330, clause331, clause332, clause333, clause334, clause335, clause336, clause337, clause338, clause339, clause340, clause341, clause342, clause343, clause344, clause345, clause346, clause347, clause348, clause349, clause350, clause351, clause352, clause353, clause354, clause355, clause356, clause357, clause358, clause359, clause360, clause361, clause362, clause363, clause364, clause365, clause366, clause367, clause368, clause369, clause370, clause371, clause372, clause373, clause374, clause375, clause376, clause377, clause378, clause379, clause380, clause381, clause382, clause383, clause384, clause385, clause386, clause387, clause388, clause389, clause390, clause391, clause392, clause393, clause394, clause395, clause396, clause397, clause398, clause399, clause400, clause401, clause402, clause403, clause404, clause405, clause406]

private theorem formula_eq : cnf_refutation.formula = clauses := by rfl

variable {n : ℕ} {σ : Fin 13 → Fin 154} (C : Context 13 n σ) (compatible : Compatible σ)
include compatible

-- Clause 1: empty_direction; source clause 30.
private theorem sound000 : C.clause (decodeClause atoms clause000) := by
  exact C.covered_clause _ _ (C.empty_clause 1 0 (by decide) (compatible.1 (1, 0) (by decide +kernel))) (by decide +kernel)

-- Clause 2: empty_direction; source clause 83.
private theorem sound001 : C.clause (decodeClause atoms clause001) := by
  exact C.covered_clause _ _ (C.empty_clause 2 0 (by decide) (compatible.1 (2, 0) (by decide +kernel))) (by decide +kernel)

-- Clause 3: empty_direction; source clause 238.
private theorem sound002 : C.clause (decodeClause atoms clause002) := by
  exact C.covered_clause _ _ (C.empty_clause 5 0 (by decide) (compatible.1 (5, 0) (by decide +kernel))) (by decide +kernel)

-- Clause 4: empty_direction; source clause 339.
private theorem sound003 : C.clause (decodeClause atoms clause003) := by
  exact C.covered_clause _ _ (C.empty_clause 7 0 (by decide) (compatible.1 (7, 0) (by decide +kernel))) (by decide +kernel)

-- Clause 5: empty_direction; source clause 439.
private theorem sound004 : C.clause (decodeClause atoms clause004) := by
  exact C.covered_clause _ _ (C.empty_clause 9 0 (by decide) (compatible.1 (9, 0) (by decide +kernel))) (by decide +kernel)

-- Clause 6: empty_direction; source clause 739.
private theorem sound005 : C.clause (decodeClause atoms clause005) := by
  exact C.covered_clause _ _ (C.empty_clause 4 1 (by decide) (compatible.1 (4, 1) (by decide +kernel))) (by decide +kernel)

-- Clause 7: empty_direction; source clause 990.
private theorem sound006 : C.clause (decodeClause atoms clause006) := by
  exact C.covered_clause _ _ (C.empty_clause 9 1 (by decide) (compatible.1 (9, 1) (by decide +kernel))) (by decide +kernel)

-- Clause 8: empty_direction; source clause 1040.
private theorem sound007 : C.clause (decodeClause atoms clause007) := by
  exact C.covered_clause _ _ (C.empty_clause 10 1 (by decide) (compatible.1 (10, 1) (by decide +kernel))) (by decide +kernel)

-- Clause 9: empty_direction; source clause 1139.
private theorem sound008 : C.clause (decodeClause atoms clause008) := by
  exact C.covered_clause _ _ (C.empty_clause 12 1 (by decide) (compatible.1 (12, 1) (by decide +kernel))) (by decide +kernel)

-- Clause 10: empty_direction; source clause 1193.
private theorem sound009 : C.clause (decodeClause atoms clause009) := by
  exact C.covered_clause _ _ (C.empty_clause 3 2 (by decide) (compatible.1 (3, 2) (by decide +kernel))) (by decide +kernel)

-- Clause 11: domain; source clause 1225.
private theorem sound010 : C.clause (decodeClause atoms clause010) := by
  exact C.covered_clause _ _ (C.domain_clause 2 4 (by decide) 1 2 (compatible.2.1 (2, 4, 1, 2) (by decide +kernel))) (by decide +kernel)

-- Clause 12: domain; source clause 1226.
private theorem sound011 : C.clause (decodeClause atoms clause011) := by
  exact C.covered_clause _ _ (C.domain_clause 2 4 (by decide) 1 3 (compatible.2.1 (2, 4, 1, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 13: domain; source clause 1227.
private theorem sound012 : C.clause (decodeClause atoms clause012) := by
  exact C.covered_clause _ _ (C.domain_clause 2 4 (by decide) 1 4 (compatible.2.1 (2, 4, 1, 4) (by decide +kernel))) (by decide +kernel)

-- Clause 14: empty_direction; source clause 1247.
private theorem sound013 : C.clause (decodeClause atoms clause013) := by
  exact C.covered_clause _ _ (C.empty_clause 4 2 (by decide) (compatible.1 (4, 2) (by decide +kernel))) (by decide +kernel)

-- Clause 15: empty_direction; source clause 1405.
private theorem sound014 : C.clause (decodeClause atoms clause014) := by
  exact C.covered_clause _ _ (C.empty_clause 7 2 (by decide) (compatible.1 (7, 2) (by decide +kernel))) (by decide +kernel)

-- Clause 16: empty_direction; source clause 1555.
private theorem sound015 : C.clause (decodeClause atoms clause015) := by
  exact C.covered_clause _ _ (C.empty_clause 10 2 (by decide) (compatible.1 (10, 2) (by decide +kernel))) (by decide +kernel)

-- Clause 17: empty_direction; source clause 1754.
private theorem sound016 : C.clause (decodeClause atoms clause016) := by
  exact C.covered_clause _ _ (C.empty_clause 5 3 (by decide) (compatible.1 (5, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 18: empty_direction; source clause 1861.
private theorem sound017 : C.clause (decodeClause atoms clause017) := by
  exact C.covered_clause _ _ (C.empty_clause 7 3 (by decide) (compatible.1 (7, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 19: empty_direction; source clause 2014.
private theorem sound018 : C.clause (decodeClause atoms clause018) := by
  exact C.covered_clause _ _ (C.empty_clause 10 3 (by decide) (compatible.1 (10, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 20: domain; source clause 2203.
private theorem sound019 : C.clause (decodeClause atoms clause019) := by
  exact C.covered_clause _ _ (C.domain_clause 4 6 (by decide) 3 2 (compatible.2.1 (4, 6, 3, 2) (by decide +kernel))) (by decide +kernel)

-- Clause 21: domain; source clause 2209.
private theorem sound020 : C.clause (decodeClause atoms clause020) := by
  exact C.covered_clause _ _ (C.domain_clause 4 6 (by decide) 4 2 (compatible.2.1 (4, 6, 4, 2) (by decide +kernel))) (by decide +kernel)

-- Clause 22: empty_direction; source clause 2214.
private theorem sound021 : C.clause (decodeClause atoms clause021) := by
  exact C.covered_clause _ _ (C.empty_clause 6 4 (by decide) (compatible.1 (6, 4) (by decide +kernel))) (by decide +kernel)

-- Clause 23: empty_direction; source clause 2417.
private theorem sound022 : C.clause (decodeClause atoms clause022) := by
  exact C.covered_clause _ _ (C.empty_clause 10 4 (by decide) (compatible.1 (10, 4) (by decide +kernel))) (by decide +kernel)

-- Clause 24: empty_direction; source clause 2618.
private theorem sound023 : C.clause (decodeClause atoms clause023) := by
  exact C.covered_clause _ _ (C.empty_clause 7 5 (by decide) (compatible.1 (7, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 25: empty_direction; source clause 2774.
private theorem sound024 : C.clause (decodeClause atoms clause024) := by
  exact C.covered_clause _ _ (C.empty_clause 10 5 (by decide) (compatible.1 (10, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 26: empty_direction; source clause 2976.
private theorem sound025 : C.clause (decodeClause atoms clause025) := by
  exact C.covered_clause _ _ (C.empty_clause 8 6 (by decide) (compatible.1 (8, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 27: empty_direction; source clause 3078.
private theorem sound026 : C.clause (decodeClause atoms clause026) := by
  exact C.covered_clause _ _ (C.empty_clause 10 6 (by decide) (compatible.1 (10, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 28: empty_direction; source clause 3331.
private theorem sound027 : C.clause (decodeClause atoms clause027) := by
  exact C.covered_clause _ _ (C.empty_clause 10 7 (by decide) (compatible.1 (10, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 29: empty_direction; source clause 3534.
private theorem sound028 : C.clause (decodeClause atoms clause028) := by
  exact C.covered_clause _ _ (C.empty_clause 10 8 (by decide) (compatible.1 (10, 8) (by decide +kernel))) (by decide +kernel)

-- Clause 30: domain; source clause 3691.
private theorem sound029 : C.clause (decodeClause atoms clause029) := by
  exact C.covered_clause _ _ (C.domain_clause 10 9 (by decide) 1 6 (compatible.2.1 (10, 9, 1, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 31: domain; source clause 3727.
private theorem sound030 : C.clause (decodeClause atoms clause030) := by
  exact C.covered_clause _ _ (C.domain_clause 9 11 (by decide) 3 2 (compatible.2.1 (9, 11, 3, 2) (by decide +kernel))) (by decide +kernel)

-- Clause 32: domain; source clause 3728.
private theorem sound031 : C.clause (decodeClause atoms clause031) := by
  exact C.covered_clause _ _ (C.domain_clause 9 11 (by decide) 3 3 (compatible.2.1 (9, 11, 3, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 33: domain; source clause 3729.
private theorem sound032 : C.clause (decodeClause atoms clause032) := by
  exact C.covered_clause _ _ (C.domain_clause 9 11 (by decide) 3 4 (compatible.2.1 (9, 11, 3, 4) (by decide +kernel))) (by decide +kernel)

-- Clause 34: domain; source clause 3730.
private theorem sound033 : C.clause (decodeClause atoms clause033) := by
  exact C.covered_clause _ _ (C.domain_clause 9 11 (by decide) 3 5 (compatible.2.1 (9, 11, 3, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 35: domain; source clause 3731.
private theorem sound034 : C.clause (decodeClause atoms clause034) := by
  exact C.covered_clause _ _ (C.domain_clause 9 11 (by decide) 3 6 (compatible.2.1 (9, 11, 3, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 36: empty_direction; source clause 3738.
private theorem sound035 : C.clause (decodeClause atoms clause035) := by
  exact C.covered_clause _ _ (C.empty_clause 11 9 (by decide) (compatible.1 (11, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 37: domain; source clause 3780.
private theorem sound036 : C.clause (decodeClause atoms clause036) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 3 2 (compatible.2.1 (9, 12, 3, 2) (by decide +kernel))) (by decide +kernel)

-- Clause 38: domain; source clause 3781.
private theorem sound037 : C.clause (decodeClause atoms clause037) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 3 3 (compatible.2.1 (9, 12, 3, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 39: domain; source clause 3782.
private theorem sound038 : C.clause (decodeClause atoms clause038) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 3 4 (compatible.2.1 (9, 12, 3, 4) (by decide +kernel))) (by decide +kernel)

-- Clause 40: domain; source clause 3783.
private theorem sound039 : C.clause (decodeClause atoms clause039) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 3 5 (compatible.2.1 (9, 12, 3, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 41: domain; source clause 3784.
private theorem sound040 : C.clause (decodeClause atoms clause040) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 3 6 (compatible.2.1 (9, 12, 3, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 42: domain; source clause 3786.
private theorem sound041 : C.clause (decodeClause atoms clause041) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 4 2 (compatible.2.1 (9, 12, 4, 2) (by decide +kernel))) (by decide +kernel)

-- Clause 43: domain; source clause 3787.
private theorem sound042 : C.clause (decodeClause atoms clause042) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 4 3 (compatible.2.1 (9, 12, 4, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 44: domain; source clause 3788.
private theorem sound043 : C.clause (decodeClause atoms clause043) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 4 4 (compatible.2.1 (9, 12, 4, 4) (by decide +kernel))) (by decide +kernel)

-- Clause 45: domain; source clause 3789.
private theorem sound044 : C.clause (decodeClause atoms clause044) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 4 5 (compatible.2.1 (9, 12, 4, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 46: domain; source clause 3790.
private theorem sound045 : C.clause (decodeClause atoms clause045) := by
  exact C.covered_clause _ _ (C.domain_clause 9 12 (by decide) 4 6 (compatible.2.1 (9, 12, 4, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 47: empty_direction; source clause 3791.
private theorem sound046 : C.clause (decodeClause atoms clause046) := by
  exact C.covered_clause _ _ (C.empty_clause 12 9 (by decide) (compatible.1 (12, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 48: empty_direction; source clause 3946.
private theorem sound047 : C.clause (decodeClause atoms clause047) := by
  exact C.covered_clause _ _ (C.empty_clause 12 11 (by decide) (compatible.1 (12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 49: growth; source clause 4108.
omit compatible in
private theorem sound048 : C.clause (decodeClause atoms clause048) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 2 3 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 50: growth; source clause 4119.
omit compatible in
private theorem sound049 : C.clause (decodeClause atoms clause049) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 2 4 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 51: growth; source clause 4174.
omit compatible in
private theorem sound050 : C.clause (decodeClause atoms clause050) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 2 9 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 52: growth; source clause 5054.
omit compatible in
private theorem sound051 : C.clause (decodeClause atoms clause051) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 9 12 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 53: growth; source clause 5835.
omit compatible in
private theorem sound052 : C.clause (decodeClause atoms clause052) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 4 6 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 54: growth; source clause 5868.
omit compatible in
private theorem sound053 : C.clause (decodeClause atoms clause053) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 4 9 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 55: growth; source clause 6495.
omit compatible in
private theorem sound054 : C.clause (decodeClause atoms clause054) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 9 11 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 56: growth; source clause 6506.
omit compatible in
private theorem sound055 : C.clause (decodeClause atoms clause055) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 9 12 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 57: growth; source clause 7156.
omit compatible in
private theorem sound056 : C.clause (decodeClause atoms clause056) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 3 5 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 58: growth; source clause 7200.
omit compatible in
private theorem sound057 : C.clause (decodeClause atoms clause057) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 3 9 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 59: growth; source clause 7284.
omit compatible in
private theorem sound058 : C.clause (decodeClause atoms clause058) := by
  exact C.covered_clause _ _ (C.growth_clause false 2 4 6 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 60: growth; source clause 7324.
omit compatible in
private theorem sound059 : C.clause (decodeClause atoms clause059) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 4 9 (by decide) (by decide) (by decide) 5) (by decide +kernel)

-- Clause 61: order_transitive; source clause 7678.
omit compatible in
private theorem sound060 : C.clause (decodeClause atoms clause060) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 7 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 62: growth; source clause 7959.
omit compatible in
private theorem sound061 : C.clause (decodeClause atoms clause061) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 9 12 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 63: growth; source clause 8873.
omit compatible in
private theorem sound062 : C.clause (decodeClause atoms clause062) := by
  exact C.covered_clause _ _ (C.growth_clause true 3 5 7 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 64: growth; source clause 8895.
omit compatible in
private theorem sound063 : C.clause (decodeClause atoms clause063) := by
  exact C.covered_clause _ _ (C.growth_clause true 3 5 9 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 65: order_transitive; source clause 9130.
omit compatible in
private theorem sound064 : C.clause (decodeClause atoms clause064) := by
  exact C.covered_clause _ _ (C.transitive_clause 3 7 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 66: growth; source clause 9412.
omit compatible in
private theorem sound065 : C.clause (decodeClause atoms clause065) := by
  exact C.covered_clause _ _ (C.growth_clause true 3 9 12 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 67: growth; source clause 10457.
omit compatible in
private theorem sound066 : C.clause (decodeClause atoms clause066) := by
  exact C.covered_clause _ _ (C.growth_clause true 4 6 8 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 68: growth; source clause 10856.
omit compatible in
private theorem sound067 : C.clause (decodeClause atoms clause067) := by
  exact C.covered_clause _ _ (C.growth_clause true 4 9 11 (by decide) (by decide) (by decide) 6) (by decide +kernel)

-- Clause 69: order_transitive; source clause 10857.
omit compatible in
private theorem sound068 : C.clause (decodeClause atoms clause068) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 9 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 70: growth; source clause 10863.
omit compatible in
private theorem sound069 : C.clause (decodeClause atoms clause069) := by
  exact C.covered_clause _ _ (C.growth_clause true 4 9 12 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 71: order_transitive; source clause 10956.
omit compatible in
private theorem sound070 : C.clause (decodeClause atoms clause070) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 10 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 72: order_transitive; source clause 12034.
omit compatible in
private theorem sound071 : C.clause (decodeClause atoms clause071) := by
  exact C.covered_clause _ _ (C.transitive_clause 5 7 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 73: growth; source clause 12042.
omit compatible in
private theorem sound072 : C.clause (decodeClause atoms clause072) := by
  exact C.covered_clause _ _ (C.growth_clause true 5 7 9 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 74: growth; source clause 12053.
omit compatible in
private theorem sound073 : C.clause (decodeClause atoms clause073) := by
  exact C.covered_clause _ _ (C.growth_clause true 5 7 10 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 75: growth; source clause 12317.
omit compatible in
private theorem sound074 : C.clause (decodeClause atoms clause074) := by
  exact C.covered_clause _ _ (C.growth_clause true 5 9 12 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 76: growth; source clause 13626.
omit compatible in
private theorem sound075 : C.clause (decodeClause atoms clause075) := by
  exact C.covered_clause _ _ (C.growth_clause true 6 8 10 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 77: order_transitive; source clause 15213.
omit compatible in
private theorem sound076 : C.clause (decodeClause atoms clause076) := by
  exact C.covered_clause _ _ (C.transitive_clause 7 9 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 78: growth; source clause 15222.
omit compatible in
private theorem sound077 : C.clause (decodeClause atoms clause077) := by
  exact C.covered_clause _ _ (C.growth_clause true 7 9 12 (by decide) (by decide) (by decide) 5) (by decide +kernel)

-- Clause 79: growth; source clause 15313.
omit compatible in
private theorem sound078 : C.clause (decodeClause atoms clause078) := by
  exact C.covered_clause _ _ (C.growth_clause false 7 10 9 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 80: growth; source clause 15321.
omit compatible in
private theorem sound079 : C.clause (decodeClause atoms clause079) := by
  exact C.covered_clause _ _ (C.growth_clause true 7 10 9 (by decide) (by decide) (by decide) 5) (by decide +kernel)

-- Clause 81: growth; source clause 16773.
omit compatible in
private theorem sound080 : C.clause (decodeClause atoms clause080) := by
  exact C.covered_clause _ _ (C.growth_clause true 8 10 9 (by decide) (by decide) (by decide) 5) (by decide +kernel)

-- Clause 82: growth; source clause 18363.
omit compatible in
private theorem sound081 : C.clause (decodeClause atoms clause081) := by
  exact C.covered_clause _ _ (C.growth_clause false 9 11 12 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 83: order_transitive; source clause 18469.
omit compatible in
private theorem sound082 : C.clause (decodeClause atoms clause082) := by
  exact C.covered_clause _ _ (C.transitive_clause 9 12 10 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 84: growth; source clause 19681.
omit compatible in
private theorem sound083 : C.clause (decodeClause atoms clause083) := by
  exact C.covered_clause _ _ (C.growth_clause false 10 9 11 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 85: growth; source clause 19689.
omit compatible in
private theorem sound084 : C.clause (decodeClause atoms clause084) := by
  exact C.covered_clause _ _ (C.growth_clause true 10 9 11 (by decide) (by decide) (by decide) 6) (by decide +kernel)

-- Clause 86: growth; source clause 19692.
omit compatible in
private theorem sound085 : C.clause (decodeClause atoms clause085) := by
  exact C.covered_clause _ _ (C.growth_clause false 10 9 12 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 87: fixed_sign; source clause 22847.
private theorem sound086 : C.clause (decodeClause atoms clause086) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 1 2 (by decide) (by decide) (by decide) (compatible.2.2 (0, 2, 1) (by decide +kernel))) (by decide +kernel)

-- Clause 88: fixed_sign; source clause 22848.
private theorem sound087 : C.clause (decodeClause atoms clause087) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 1 3 (by decide) (by decide) (by decide) (compatible.2.2 (0, 3, 1) (by decide +kernel))) (by decide +kernel)

-- Clause 89: fixed_sign; source clause 22850.
private theorem sound088 : C.clause (decodeClause atoms clause088) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 1 5 (by decide) (by decide) (by decide) (compatible.2.2 (0, 5, 1) (by decide +kernel))) (by decide +kernel)

-- Clause 90: fixed_sign; source clause 22852.
private theorem sound089 : C.clause (decodeClause atoms clause089) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 1 7 (by decide) (by decide) (by decide) (compatible.2.2 (0, 7, 1) (by decide +kernel))) (by decide +kernel)

-- Clause 91: fixed_sign; source clause 22854.
private theorem sound090 : C.clause (decodeClause atoms clause090) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 1 9 (by decide) (by decide) (by decide) (compatible.2.2 (0, 9, 1) (by decide +kernel))) (by decide +kernel)

-- Clause 92: fixed_sign; source clause 22855.
private theorem sound091 : C.clause (decodeClause atoms clause091) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 1 10 (by decide) (by decide) (by decide) (compatible.2.2 (0, 10, 1) (by decide +kernel))) (by decide +kernel)

-- Clause 93: fixed_sign; source clause 22856.
private theorem sound092 : C.clause (decodeClause atoms clause092) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 3 (by decide) (by decide) (by decide) (compatible.2.2 (0, 2, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 94: fixed_sign; source clause 22857.
private theorem sound093 : C.clause (decodeClause atoms clause093) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 4 (by decide) (by decide) (by decide) (compatible.2.2 (0, 2, 4) (by decide +kernel))) (by decide +kernel)

-- Clause 95: fixed_sign; source clause 22858.
private theorem sound094 : C.clause (decodeClause atoms clause094) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 5 (by decide) (by decide) (by decide) (compatible.2.2 (0, 2, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 96: fixed_sign; source clause 22860.
private theorem sound095 : C.clause (decodeClause atoms clause095) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 7 (by decide) (by decide) (by decide) (compatible.2.2 (0, 2, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 97: fixed_sign; source clause 22862.
private theorem sound096 : C.clause (decodeClause atoms clause096) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 9 (by decide) (by decide) (by decide) (compatible.2.2 (0, 2, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 98: fixed_sign; source clause 22863.
private theorem sound097 : C.clause (decodeClause atoms clause097) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 10 (by decide) (by decide) (by decide) (compatible.2.2 (0, 2, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 99: fixed_sign; source clause 22865.
private theorem sound098 : C.clause (decodeClause atoms clause098) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 12 (by decide) (by decide) (by decide) (compatible.2.2 (0, 2, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 100: fixed_sign; source clause 22866.
private theorem sound099 : C.clause (decodeClause atoms clause099) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 3 5 (by decide) (by decide) (by decide) (compatible.2.2 (0, 3, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 101: fixed_sign; source clause 22868.
private theorem sound100 : C.clause (decodeClause atoms clause100) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 3 7 (by decide) (by decide) (by decide) (compatible.2.2 (0, 3, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 102: fixed_sign; source clause 22870.
private theorem sound101 : C.clause (decodeClause atoms clause101) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 3 9 (by decide) (by decide) (by decide) (compatible.2.2 (0, 3, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 103: fixed_sign; source clause 22871.
private theorem sound102 : C.clause (decodeClause atoms clause102) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 3 10 (by decide) (by decide) (by decide) (compatible.2.2 (0, 3, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 104: fixed_sign; source clause 22873.
private theorem sound103 : C.clause (decodeClause atoms clause103) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 3 12 (by decide) (by decide) (by decide) (compatible.2.2 (0, 3, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 105: fixed_sign; source clause 22874.
private theorem sound104 : C.clause (decodeClause atoms clause104) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 5 7 (by decide) (by decide) (by decide) (compatible.2.2 (0, 5, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 106: fixed_sign; source clause 22876.
private theorem sound105 : C.clause (decodeClause atoms clause105) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 5 9 (by decide) (by decide) (by decide) (compatible.2.2 (0, 5, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 107: fixed_sign; source clause 22877.
private theorem sound106 : C.clause (decodeClause atoms clause106) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 5 10 (by decide) (by decide) (by decide) (compatible.2.2 (0, 5, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 108: fixed_sign; source clause 22879.
private theorem sound107 : C.clause (decodeClause atoms clause107) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 5 12 (by decide) (by decide) (by decide) (compatible.2.2 (0, 5, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 109: fixed_sign; source clause 22880.
private theorem sound108 : C.clause (decodeClause atoms clause108) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 7 9 (by decide) (by decide) (by decide) (compatible.2.2 (0, 7, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 110: fixed_sign; source clause 22881.
private theorem sound109 : C.clause (decodeClause atoms clause109) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 7 10 (by decide) (by decide) (by decide) (compatible.2.2 (0, 7, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 111: fixed_sign; source clause 22883.
private theorem sound110 : C.clause (decodeClause atoms clause110) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 7 12 (by decide) (by decide) (by decide) (compatible.2.2 (0, 7, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 112: fixed_sign; source clause 22885.
private theorem sound111 : C.clause (decodeClause atoms clause111) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 3 (by decide) (by decide) (by decide) (compatible.2.2 (1, 2, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 113: fixed_sign; source clause 22886.
private theorem sound112 : C.clause (decodeClause atoms clause112) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 4 (by decide) (by decide) (by decide) (compatible.2.2 (1, 2, 4) (by decide +kernel))) (by decide +kernel)

-- Clause 114: fixed_sign; source clause 22887.
private theorem sound113 : C.clause (decodeClause atoms clause113) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 5 (by decide) (by decide) (by decide) (compatible.2.2 (1, 2, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 115: fixed_sign; source clause 22889.
private theorem sound114 : C.clause (decodeClause atoms clause114) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 7 (by decide) (by decide) (by decide) (compatible.2.2 (1, 2, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 116: fixed_sign; source clause 22891.
private theorem sound115 : C.clause (decodeClause atoms clause115) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 9 (by decide) (by decide) (by decide) (compatible.2.2 (1, 2, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 117: fixed_sign; source clause 22892.
private theorem sound116 : C.clause (decodeClause atoms clause116) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 10 (by decide) (by decide) (by decide) (compatible.2.2 (1, 2, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 118: fixed_sign; source clause 22893.
private theorem sound117 : C.clause (decodeClause atoms clause117) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 3 5 (by decide) (by decide) (by decide) (compatible.2.2 (1, 3, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 119: fixed_sign; source clause 22895.
private theorem sound118 : C.clause (decodeClause atoms clause118) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 3 7 (by decide) (by decide) (by decide) (compatible.2.2 (1, 3, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 120: fixed_sign; source clause 22897.
private theorem sound119 : C.clause (decodeClause atoms clause119) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 3 9 (by decide) (by decide) (by decide) (compatible.2.2 (1, 3, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 121: fixed_sign; source clause 22898.
private theorem sound120 : C.clause (decodeClause atoms clause120) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 3 10 (by decide) (by decide) (by decide) (compatible.2.2 (1, 3, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 122: fixed_sign; source clause 22899.
private theorem sound121 : C.clause (decodeClause atoms clause121) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 6 (by decide) (by decide) (by decide) (compatible.2.2 (1, 4, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 123: fixed_sign; source clause 22900.
private theorem sound122 : C.clause (decodeClause atoms clause122) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 8 (by decide) (by decide) (by decide) (compatible.2.2 (1, 4, 8) (by decide +kernel))) (by decide +kernel)

-- Clause 124: fixed_sign; source clause 22901.
private theorem sound123 : C.clause (decodeClause atoms clause123) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 9 (by decide) (by decide) (by decide) (compatible.2.2 (1, 4, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 125: fixed_sign; source clause 22902.
private theorem sound124 : C.clause (decodeClause atoms clause124) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 10 (by decide) (by decide) (by decide) (compatible.2.2 (1, 4, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 126: fixed_sign; source clause 22903.
private theorem sound125 : C.clause (decodeClause atoms clause125) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 11 (by decide) (by decide) (by decide) (compatible.2.2 (1, 4, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 127: fixed_sign; source clause 22904.
private theorem sound126 : C.clause (decodeClause atoms clause126) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 12 (by decide) (by decide) (by decide) (compatible.2.2 (1, 4, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 128: fixed_sign; source clause 22905.
private theorem sound127 : C.clause (decodeClause atoms clause127) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 5 7 (by decide) (by decide) (by decide) (compatible.2.2 (1, 5, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 129: fixed_sign; source clause 22907.
private theorem sound128 : C.clause (decodeClause atoms clause128) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 5 9 (by decide) (by decide) (by decide) (compatible.2.2 (1, 5, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 130: fixed_sign; source clause 22908.
private theorem sound129 : C.clause (decodeClause atoms clause129) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 5 10 (by decide) (by decide) (by decide) (compatible.2.2 (1, 5, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 131: fixed_sign; source clause 22909.
private theorem sound130 : C.clause (decodeClause atoms clause130) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 8 (by decide) (by decide) (by decide) (compatible.2.2 (1, 6, 8) (by decide +kernel))) (by decide +kernel)

-- Clause 132: fixed_sign; source clause 22910.
private theorem sound131 : C.clause (decodeClause atoms clause131) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 9 (by decide) (by decide) (by decide) (compatible.2.2 (1, 6, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 133: fixed_sign; source clause 22911.
private theorem sound132 : C.clause (decodeClause atoms clause132) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 10 (by decide) (by decide) (by decide) (compatible.2.2 (1, 6, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 134: fixed_sign; source clause 22912.
private theorem sound133 : C.clause (decodeClause atoms clause133) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 11 (by decide) (by decide) (by decide) (compatible.2.2 (1, 6, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 135: fixed_sign; source clause 22913.
private theorem sound134 : C.clause (decodeClause atoms clause134) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 12 (by decide) (by decide) (by decide) (compatible.2.2 (1, 6, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 136: fixed_sign; source clause 22914.
private theorem sound135 : C.clause (decodeClause atoms clause135) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 7 9 (by decide) (by decide) (by decide) (compatible.2.2 (1, 7, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 137: fixed_sign; source clause 22915.
private theorem sound136 : C.clause (decodeClause atoms clause136) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 7 10 (by decide) (by decide) (by decide) (compatible.2.2 (1, 7, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 138: fixed_sign; source clause 22916.
private theorem sound137 : C.clause (decodeClause atoms clause137) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 8 9 (by decide) (by decide) (by decide) (compatible.2.2 (1, 8, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 139: fixed_sign; source clause 22917.
private theorem sound138 : C.clause (decodeClause atoms clause138) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 8 10 (by decide) (by decide) (by decide) (compatible.2.2 (1, 8, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 140: fixed_sign; source clause 22918.
private theorem sound139 : C.clause (decodeClause atoms clause139) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 8 11 (by decide) (by decide) (by decide) (compatible.2.2 (1, 8, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 141: fixed_sign; source clause 22919.
private theorem sound140 : C.clause (decodeClause atoms clause140) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 8 12 (by decide) (by decide) (by decide) (compatible.2.2 (1, 8, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 142: fixed_sign; source clause 22920.
private theorem sound141 : C.clause (decodeClause atoms clause141) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 9 10 (by decide) (by decide) (by decide) (compatible.2.2 (1, 10, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 143: fixed_sign; source clause 22921.
private theorem sound142 : C.clause (decodeClause atoms clause142) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 9 11 (by decide) (by decide) (by decide) (compatible.2.2 (1, 9, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 144: fixed_sign; source clause 22922.
private theorem sound143 : C.clause (decodeClause atoms clause143) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 10 11 (by decide) (by decide) (by decide) (compatible.2.2 (1, 10, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 145: fixed_sign; source clause 22923.
private theorem sound144 : C.clause (decodeClause atoms clause144) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 10 12 (by decide) (by decide) (by decide) (compatible.2.2 (1, 10, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 146: fixed_sign; source clause 22924.
private theorem sound145 : C.clause (decodeClause atoms clause145) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 11 12 (by decide) (by decide) (by decide) (compatible.2.2 (1, 12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 147: fixed_sign; source clause 22926.
private theorem sound146 : C.clause (decodeClause atoms clause146) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 3 5 (by decide) (by decide) (by decide) (compatible.2.2 (2, 3, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 148: fixed_sign; source clause 22928.
private theorem sound147 : C.clause (decodeClause atoms clause147) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 3 7 (by decide) (by decide) (by decide) (compatible.2.2 (2, 3, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 149: fixed_sign; source clause 22930.
private theorem sound148 : C.clause (decodeClause atoms clause148) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 3 9 (by decide) (by decide) (by decide) (compatible.2.2 (2, 3, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 150: fixed_sign; source clause 22931.
private theorem sound149 : C.clause (decodeClause atoms clause149) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 3 10 (by decide) (by decide) (by decide) (compatible.2.2 (2, 3, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 151: fixed_sign; source clause 22933.
private theorem sound150 : C.clause (decodeClause atoms clause150) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 3 12 (by decide) (by decide) (by decide) (compatible.2.2 (2, 3, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 152: fixed_sign; source clause 22935.
private theorem sound151 : C.clause (decodeClause atoms clause151) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 4 6 (by decide) (by decide) (by decide) (compatible.2.2 (2, 6, 4) (by decide +kernel))) (by decide +kernel)

-- Clause 153: fixed_sign; source clause 22939.
private theorem sound152 : C.clause (decodeClause atoms clause152) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 5 7 (by decide) (by decide) (by decide) (compatible.2.2 (2, 5, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 154: fixed_sign; source clause 22941.
private theorem sound153 : C.clause (decodeClause atoms clause153) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 5 9 (by decide) (by decide) (by decide) (compatible.2.2 (2, 5, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 155: fixed_sign; source clause 22942.
private theorem sound154 : C.clause (decodeClause atoms clause154) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 5 10 (by decide) (by decide) (by decide) (compatible.2.2 (2, 5, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 156: fixed_sign; source clause 22944.
private theorem sound155 : C.clause (decodeClause atoms clause155) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 5 12 (by decide) (by decide) (by decide) (compatible.2.2 (2, 5, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 157: fixed_sign; source clause 22945.
private theorem sound156 : C.clause (decodeClause atoms clause156) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 7 9 (by decide) (by decide) (by decide) (compatible.2.2 (2, 7, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 158: fixed_sign; source clause 22946.
private theorem sound157 : C.clause (decodeClause atoms clause157) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 7 10 (by decide) (by decide) (by decide) (compatible.2.2 (2, 7, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 159: fixed_sign; source clause 22948.
private theorem sound158 : C.clause (decodeClause atoms clause158) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 7 12 (by decide) (by decide) (by decide) (compatible.2.2 (2, 7, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 160: fixed_sign; source clause 22956.
private theorem sound159 : C.clause (decodeClause atoms clause159) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 7 (by decide) (by decide) (by decide) (compatible.2.2 (3, 5, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 161: fixed_sign; source clause 22958.
private theorem sound160 : C.clause (decodeClause atoms clause160) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 9 (by decide) (by decide) (by decide) (compatible.2.2 (3, 5, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 162: fixed_sign; source clause 22959.
private theorem sound161 : C.clause (decodeClause atoms clause161) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 10 (by decide) (by decide) (by decide) (compatible.2.2 (3, 5, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 163: fixed_sign; source clause 22961.
private theorem sound162 : C.clause (decodeClause atoms clause162) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 12 (by decide) (by decide) (by decide) (compatible.2.2 (3, 5, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 164: fixed_sign; source clause 22965.
private theorem sound163 : C.clause (decodeClause atoms clause163) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 7 9 (by decide) (by decide) (by decide) (compatible.2.2 (3, 7, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 165: fixed_sign; source clause 22966.
private theorem sound164 : C.clause (decodeClause atoms clause164) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 7 10 (by decide) (by decide) (by decide) (compatible.2.2 (3, 7, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 166: fixed_sign; source clause 22968.
private theorem sound165 : C.clause (decodeClause atoms clause165) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 7 12 (by decide) (by decide) (by decide) (compatible.2.2 (3, 7, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 167: fixed_sign; source clause 22973.
private theorem sound166 : C.clause (decodeClause atoms clause166) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 6 8 (by decide) (by decide) (by decide) (compatible.2.2 (4, 6, 8) (by decide +kernel))) (by decide +kernel)

-- Clause 168: fixed_sign; source clause 22974.
private theorem sound167 : C.clause (decodeClause atoms clause167) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 6 9 (by decide) (by decide) (by decide) (compatible.2.2 (4, 6, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 169: fixed_sign; source clause 22975.
private theorem sound168 : C.clause (decodeClause atoms clause168) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 6 10 (by decide) (by decide) (by decide) (compatible.2.2 (4, 6, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 170: fixed_sign; source clause 22976.
private theorem sound169 : C.clause (decodeClause atoms clause169) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 6 11 (by decide) (by decide) (by decide) (compatible.2.2 (4, 6, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 171: fixed_sign; source clause 22977.
private theorem sound170 : C.clause (decodeClause atoms clause170) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 6 12 (by decide) (by decide) (by decide) (compatible.2.2 (4, 6, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 172: fixed_sign; source clause 22979.
private theorem sound171 : C.clause (decodeClause atoms clause171) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 8 9 (by decide) (by decide) (by decide) (compatible.2.2 (4, 8, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 173: fixed_sign; source clause 22980.
private theorem sound172 : C.clause (decodeClause atoms clause172) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 8 10 (by decide) (by decide) (by decide) (compatible.2.2 (4, 8, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 174: fixed_sign; source clause 22981.
private theorem sound173 : C.clause (decodeClause atoms clause173) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 8 11 (by decide) (by decide) (by decide) (compatible.2.2 (4, 8, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 175: fixed_sign; source clause 22982.
private theorem sound174 : C.clause (decodeClause atoms clause174) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 8 12 (by decide) (by decide) (by decide) (compatible.2.2 (4, 8, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 176: fixed_sign; source clause 22983.
private theorem sound175 : C.clause (decodeClause atoms clause175) := by
  exact C.covered_clause _ _ (C.fixed_negative 4 9 10 (by decide) (by decide) (by decide) (compatible.2.2 (4, 10, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 177: fixed_sign; source clause 22984.
private theorem sound176 : C.clause (decodeClause atoms clause176) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 10 11 (by decide) (by decide) (by decide) (compatible.2.2 (4, 10, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 178: fixed_sign; source clause 22985.
private theorem sound177 : C.clause (decodeClause atoms clause177) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 10 12 (by decide) (by decide) (by decide) (compatible.2.2 (4, 10, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 179: fixed_sign; source clause 22986.
private theorem sound178 : C.clause (decodeClause atoms clause178) := by
  exact C.covered_clause _ _ (C.fixed_negative 4 11 12 (by decide) (by decide) (by decide) (compatible.2.2 (4, 12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 180: fixed_sign; source clause 22991.
private theorem sound179 : C.clause (decodeClause atoms clause179) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 7 9 (by decide) (by decide) (by decide) (compatible.2.2 (5, 7, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 181: fixed_sign; source clause 22992.
private theorem sound180 : C.clause (decodeClause atoms clause180) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 7 10 (by decide) (by decide) (by decide) (compatible.2.2 (5, 7, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 182: fixed_sign; source clause 22994.
private theorem sound181 : C.clause (decodeClause atoms clause181) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 7 12 (by decide) (by decide) (by decide) (compatible.2.2 (5, 7, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 183: fixed_sign; source clause 22998.
private theorem sound182 : C.clause (decodeClause atoms clause182) := by
  exact C.covered_clause _ _ (C.fixed_positive 6 8 9 (by decide) (by decide) (by decide) (compatible.2.2 (6, 8, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 184: fixed_sign; source clause 22999.
private theorem sound183 : C.clause (decodeClause atoms clause183) := by
  exact C.covered_clause _ _ (C.fixed_positive 6 8 10 (by decide) (by decide) (by decide) (compatible.2.2 (6, 8, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 185: fixed_sign; source clause 23000.
private theorem sound184 : C.clause (decodeClause atoms clause184) := by
  exact C.covered_clause _ _ (C.fixed_positive 6 8 11 (by decide) (by decide) (by decide) (compatible.2.2 (6, 8, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 186: fixed_sign; source clause 23001.
private theorem sound185 : C.clause (decodeClause atoms clause185) := by
  exact C.covered_clause _ _ (C.fixed_positive 6 8 12 (by decide) (by decide) (by decide) (compatible.2.2 (6, 8, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 187: fixed_sign; source clause 23002.
private theorem sound186 : C.clause (decodeClause atoms clause186) := by
  exact C.covered_clause _ _ (C.fixed_negative 6 9 10 (by decide) (by decide) (by decide) (compatible.2.2 (6, 10, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 188: fixed_sign; source clause 23003.
private theorem sound187 : C.clause (decodeClause atoms clause187) := by
  exact C.covered_clause _ _ (C.fixed_positive 6 10 11 (by decide) (by decide) (by decide) (compatible.2.2 (6, 10, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 189: fixed_sign; source clause 23004.
private theorem sound188 : C.clause (decodeClause atoms clause188) := by
  exact C.covered_clause _ _ (C.fixed_positive 6 10 12 (by decide) (by decide) (by decide) (compatible.2.2 (6, 10, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 190: fixed_sign; source clause 23005.
private theorem sound189 : C.clause (decodeClause atoms clause189) := by
  exact C.covered_clause _ _ (C.fixed_negative 6 11 12 (by decide) (by decide) (by decide) (compatible.2.2 (6, 12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 191: fixed_sign; source clause 23008.
private theorem sound190 : C.clause (decodeClause atoms clause190) := by
  exact C.covered_clause _ _ (C.fixed_negative 8 9 10 (by decide) (by decide) (by decide) (compatible.2.2 (8, 10, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 192: fixed_sign; source clause 23009.
private theorem sound191 : C.clause (decodeClause atoms clause191) := by
  exact C.covered_clause _ _ (C.fixed_positive 8 10 11 (by decide) (by decide) (by decide) (compatible.2.2 (8, 10, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 193: fixed_sign; source clause 23010.
private theorem sound192 : C.clause (decodeClause atoms clause192) := by
  exact C.covered_clause _ _ (C.fixed_positive 8 10 12 (by decide) (by decide) (by decide) (compatible.2.2 (8, 10, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 194: fixed_sign; source clause 23011.
private theorem sound193 : C.clause (decodeClause atoms clause193) := by
  exact C.covered_clause _ _ (C.fixed_negative 8 11 12 (by decide) (by decide) (by decide) (compatible.2.2 (8, 12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 195: fixed_sign; source clause 23012.
private theorem sound194 : C.clause (decodeClause atoms clause194) := by
  exact C.covered_clause _ _ (C.fixed_negative 9 11 12 (by decide) (by decide) (by decide) (compatible.2.2 (9, 12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 196: fixed_sign; source clause 23013.
private theorem sound195 : C.clause (decodeClause atoms clause195) := by
  exact C.covered_clause _ _ (C.fixed_negative 10 11 12 (by decide) (by decide) (by decide) (compatible.2.2 (10, 12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 197: convex_four; source clause 23209.
omit compatible in
private theorem sound196 : C.clause (decodeClause atoms clause196) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 198: convex_four; source clause 23625.
omit compatible in
private theorem sound197 : C.clause (decodeClause atoms clause197) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 199: convex_four; source clause 24041.
omit compatible in
private theorem sound198 : C.clause (decodeClause atoms clause198) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 200: convex_four; source clause 24457.
omit compatible in
private theorem sound199 : C.clause (decodeClause atoms clause199) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 201: convex_four; source clause 24665.
omit compatible in
private theorem sound200 : C.clause (decodeClause atoms clause200) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 202: convex_four; source clause 25081.
omit compatible in
private theorem sound201 : C.clause (decodeClause atoms clause201) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 203: convex_four; source clause 25497.
omit compatible in
private theorem sound202 : C.clause (decodeClause atoms clause202) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 204: convex_four; source clause 25913.
omit compatible in
private theorem sound203 : C.clause (decodeClause atoms clause203) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 205: convex_four; source clause 26329.
omit compatible in
private theorem sound204 : C.clause (decodeClause atoms clause204) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 206: convex_four; source clause 26537.
omit compatible in
private theorem sound205 : C.clause (decodeClause atoms clause205) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 207: convex_four; source clause 26953.
omit compatible in
private theorem sound206 : C.clause (decodeClause atoms clause206) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 208: convex_four; source clause 29033.
omit compatible in
private theorem sound207 : C.clause (decodeClause atoms clause207) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 209: convex_four; source clause 29449.
omit compatible in
private theorem sound208 : C.clause (decodeClause atoms clause208) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 210: convex_four; source clause 29657.
omit compatible in
private theorem sound209 : C.clause (decodeClause atoms clause209) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 211: convex_four; source clause 30073.
omit compatible in
private theorem sound210 : C.clause (decodeClause atoms clause210) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 212: convex_four; source clause 31737.
omit compatible in
private theorem sound211 : C.clause (decodeClause atoms clause211) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 213: convex_four; source clause 31945.
omit compatible in
private theorem sound212 : C.clause (decodeClause atoms clause212) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 214: convex_four; source clause 32361.
omit compatible in
private theorem sound213 : C.clause (decodeClause atoms clause213) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 215: packet; source clause 33206.
omit compatible in
private theorem sound214 : C.clause (decodeClause atoms clause214) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 216: convex_four; source clause 33398.
omit compatible in
private theorem sound215 : C.clause (decodeClause atoms clause215) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 217: packet; source clause 33623.
omit compatible in
private theorem sound216 : C.clause (decodeClause atoms clause216) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 218: convex_four; source clause 33814.
omit compatible in
private theorem sound217 : C.clause (decodeClause atoms clause217) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 219: convex_four; source clause 34869.
omit compatible in
private theorem sound218 : C.clause (decodeClause atoms clause218) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 220: convex_four; source clause 35285.
omit compatible in
private theorem sound219 : C.clause (decodeClause atoms clause219) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 221: convex_four; source clause 35701.
omit compatible in
private theorem sound220 : C.clause (decodeClause atoms clause220) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 222: convex_four; source clause 35909.
omit compatible in
private theorem sound221 : C.clause (decodeClause atoms clause221) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 223: convex_four; source clause 36325.
omit compatible in
private theorem sound222 : C.clause (decodeClause atoms clause222) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 224: convex_four; source clause 38405.
omit compatible in
private theorem sound223 : C.clause (decodeClause atoms clause223) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 225: convex_four; source clause 38821.
omit compatible in
private theorem sound224 : C.clause (decodeClause atoms clause224) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 226: convex_four; source clause 39029.
omit compatible in
private theorem sound225 : C.clause (decodeClause atoms clause225) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 227: convex_four; source clause 39445.
omit compatible in
private theorem sound226 : C.clause (decodeClause atoms clause226) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 228: convex_four; source clause 41109.
omit compatible in
private theorem sound227 : C.clause (decodeClause atoms clause227) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 229: convex_four; source clause 41317.
omit compatible in
private theorem sound228 : C.clause (decodeClause atoms clause228) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 230: convex_four; source clause 41733.
omit compatible in
private theorem sound229 : C.clause (decodeClause atoms clause229) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 231: packet; source clause 42573.
omit compatible in
private theorem sound230 : C.clause (decodeClause atoms clause230) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 232: convex_four; source clause 42770.
omit compatible in
private theorem sound231 : C.clause (decodeClause atoms clause231) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 233: convex_four; source clause 43186.
omit compatible in
private theorem sound232 : C.clause (decodeClause atoms clause232) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 234: convex_four; source clause 45893.
omit compatible in
private theorem sound233 : C.clause (decodeClause atoms clause233) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 235: convex_four; source clause 46309.
omit compatible in
private theorem sound234 : C.clause (decodeClause atoms clause234) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 236: convex_four; source clause 46517.
omit compatible in
private theorem sound235 : C.clause (decodeClause atoms clause235) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 237: convex_four; source clause 46933.
omit compatible in
private theorem sound236 : C.clause (decodeClause atoms clause236) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 238: convex_four; source clause 48597.
omit compatible in
private theorem sound237 : C.clause (decodeClause atoms clause237) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 239: convex_four; source clause 48805.
omit compatible in
private theorem sound238 : C.clause (decodeClause atoms clause238) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 240: convex_four; source clause 49221.
omit compatible in
private theorem sound239 : C.clause (decodeClause atoms clause239) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 241: convex_four; source clause 50258.
omit compatible in
private theorem sound240 : C.clause (decodeClause atoms clause240) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 242: convex_four; source clause 50674.
omit compatible in
private theorem sound241 : C.clause (decodeClause atoms clause241) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 243: convex_four; source clause 58789.
omit compatible in
private theorem sound242 : C.clause (decodeClause atoms clause242) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 244: convex_four; source clause 58997.
omit compatible in
private theorem sound243 : C.clause (decodeClause atoms clause243) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 245: convex_four; source clause 59413.
omit compatible in
private theorem sound244 : C.clause (decodeClause atoms clause244) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 246: packet; source clause 60253.
omit compatible in
private theorem sound245 : C.clause (decodeClause atoms clause245) := by
  exact C.covered_clause _ _ (C.packet_clause 0 5 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 247: packet; source clause 60262.
omit compatible in
private theorem sound246 : C.clause (decodeClause atoms clause246) := by
  exact C.covered_clause _ _ (C.packet_clause 0 9 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 248: convex_four; source clause 60450.
omit compatible in
private theorem sound247 : C.clause (decodeClause atoms clause247) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 249: convex_four; source clause 60866.
omit compatible in
private theorem sound248 : C.clause (decodeClause atoms clause248) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 250: packet; source clause 65453.
omit compatible in
private theorem sound249 : C.clause (decodeClause atoms clause249) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 251: convex_four; source clause 65650.
omit compatible in
private theorem sound250 : C.clause (decodeClause atoms clause250) := by
  exact C.covered_clause _ _ (C.convex_clause 0 7 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 252: convex_four; source clause 66066.
omit compatible in
private theorem sound251 : C.clause (decodeClause atoms clause251) := by
  exact C.covered_clause _ _ (C.convex_clause 0 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 253: convex_four; source clause 69189.
omit compatible in
private theorem sound252 : C.clause (decodeClause atoms clause252) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 254: convex_four; source clause 69605.
omit compatible in
private theorem sound253 : C.clause (decodeClause atoms clause253) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 255: convex_four; source clause 70021.
omit compatible in
private theorem sound254 : C.clause (decodeClause atoms clause254) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 256: convex_four; source clause 70229.
omit compatible in
private theorem sound255 : C.clause (decodeClause atoms clause255) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 257: convex_four; source clause 70645.
omit compatible in
private theorem sound256 : C.clause (decodeClause atoms clause256) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 258: packet; source clause 72107.
omit compatible in
private theorem sound257 : C.clause (decodeClause atoms clause257) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 259: convex_four; source clause 72725.
omit compatible in
private theorem sound258 : C.clause (decodeClause atoms clause258) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 260: convex_four; source clause 73141.
omit compatible in
private theorem sound259 : C.clause (decodeClause atoms clause259) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 261: convex_four; source clause 73349.
omit compatible in
private theorem sound260 : C.clause (decodeClause atoms clause260) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 262: convex_four; source clause 73765.
omit compatible in
private theorem sound261 : C.clause (decodeClause atoms clause261) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 263: convex_four; source clause 75429.
omit compatible in
private theorem sound262 : C.clause (decodeClause atoms clause262) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 264: convex_four; source clause 75637.
omit compatible in
private theorem sound263 : C.clause (decodeClause atoms clause263) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 265: packet; source clause 75853.
omit compatible in
private theorem sound264 : C.clause (decodeClause atoms clause264) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 266: packet; source clause 75894.
omit compatible in
private theorem sound265 : C.clause (decodeClause atoms clause265) := by
  exact C.covered_clause _ _ (C.packet_clause 2 1 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 267: packet; source clause 75917.
omit compatible in
private theorem sound266 : C.clause (decodeClause atoms clause266) := by
  exact C.covered_clause _ _ (C.packet_clause 2 7 1 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 268: convex_four; source clause 76053.
omit compatible in
private theorem sound267 : C.clause (decodeClause atoms clause267) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 269: packet; source clause 76902.
omit compatible in
private theorem sound268 : C.clause (decodeClause atoms clause268) := by
  exact C.covered_clause _ _ (C.packet_clause 1 9 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 270: convex_four; source clause 77090.
omit compatible in
private theorem sound269 : C.clause (decodeClause atoms clause269) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 271: packet; source clause 77351.
omit compatible in
private theorem sound270 : C.clause (decodeClause atoms clause270) := by
  exact C.covered_clause _ _ (C.packet_clause 2 1 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 272: convex_four; source clause 77506.
omit compatible in
private theorem sound271 : C.clause (decodeClause atoms clause271) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 273: convex_four; source clause 80213.
omit compatible in
private theorem sound272 : C.clause (decodeClause atoms clause272) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 274: convex_four; source clause 80629.
omit compatible in
private theorem sound273 : C.clause (decodeClause atoms clause273) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 275: convex_four; source clause 80837.
omit compatible in
private theorem sound274 : C.clause (decodeClause atoms clause274) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 276: convex_four; source clause 81253.
omit compatible in
private theorem sound275 : C.clause (decodeClause atoms clause275) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 277: convex_four; source clause 82917.
omit compatible in
private theorem sound276 : C.clause (decodeClause atoms clause276) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 278: convex_four; source clause 83125.
omit compatible in
private theorem sound277 : C.clause (decodeClause atoms clause277) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 279: convex_four; source clause 83537.
omit compatible in
private theorem sound278 : C.clause (decodeClause atoms clause278) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 280: convex_four; source clause 83541.
omit compatible in
private theorem sound279 : C.clause (decodeClause atoms clause279) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 281: packet; source clause 84390.
omit compatible in
private theorem sound280 : C.clause (decodeClause atoms clause280) := by
  exact C.covered_clause _ _ (C.packet_clause 1 9 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 282: convex_four; source clause 84578.
omit compatible in
private theorem sound281 : C.clause (decodeClause atoms clause281) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 283: packet; source clause 84839.
omit compatible in
private theorem sound282 : C.clause (decodeClause atoms clause282) := by
  exact C.covered_clause _ _ (C.packet_clause 3 1 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 284: convex_four; source clause 84994.
omit compatible in
private theorem sound283 : C.clause (decodeClause atoms clause283) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 285: packet; source clause 85211.
omit compatible in
private theorem sound284 : C.clause (decodeClause atoms clause284) := by
  exact C.covered_clause _ _ (C.packet_clause 1 3 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 286: packet; source clause 85212.
omit compatible in
private theorem sound285 : C.clause (decodeClause atoms clause285) := by
  exact C.covered_clause _ _ (C.packet_clause 1 3 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 287: convex_four; source clause 87493.
omit compatible in
private theorem sound286 : C.clause (decodeClause atoms clause286) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 288: convex_four; source clause 87701.
omit compatible in
private theorem sound287 : C.clause (decodeClause atoms clause287) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 289: convex_four; source clause 87909.
omit compatible in
private theorem sound288 : C.clause (decodeClause atoms clause288) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 290: convex_four; source clause 88117.
omit compatible in
private theorem sound289 : C.clause (decodeClause atoms clause289) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 291: convex_four; source clause 88325.
omit compatible in
private theorem sound290 : C.clause (decodeClause atoms clause290) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 292: convex_four; source clause 89573.
omit compatible in
private theorem sound291 : C.clause (decodeClause atoms clause291) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 293: convex_four; source clause 89781.
omit compatible in
private theorem sound292 : C.clause (decodeClause atoms clause292) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 294: convex_four; source clause 89989.
omit compatible in
private theorem sound293 : C.clause (decodeClause atoms clause293) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 295: convex_four; source clause 90197.
omit compatible in
private theorem sound294 : C.clause (decodeClause atoms clause294) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 296: convex_four; source clause 90402.
omit compatible in
private theorem sound295 : C.clause (decodeClause atoms clause295) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 297: convex_four; source clause 90613.
omit compatible in
private theorem sound296 : C.clause (decodeClause atoms clause296) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 298: convex_four; source clause 90821.
omit compatible in
private theorem sound297 : C.clause (decodeClause atoms clause297) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 299: convex_four; source clause 91029.
omit compatible in
private theorem sound298 : C.clause (decodeClause atoms clause298) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 300: convex_four; source clause 91237.
omit compatible in
private theorem sound299 : C.clause (decodeClause atoms clause299) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 301: convex_four; source clause 91442.
omit compatible in
private theorem sound300 : C.clause (decodeClause atoms clause300) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 302: convex_four; source clause 93109.
omit compatible in
private theorem sound301 : C.clause (decodeClause atoms clause301) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 303: convex_four; source clause 93317.
omit compatible in
private theorem sound302 : C.clause (decodeClause atoms clause302) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 304: packet; source clause 93532.
omit compatible in
private theorem sound303 : C.clause (decodeClause atoms clause303) := by
  exact C.covered_clause _ _ (C.packet_clause 1 5 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 305: convex_four; source clause 93729.
omit compatible in
private theorem sound304 : C.clause (decodeClause atoms clause304) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 306: convex_four; source clause 93733.
omit compatible in
private theorem sound305 : C.clause (decodeClause atoms clause305) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 307: convex_four; source clause 94770.
omit compatible in
private theorem sound306 : C.clause (decodeClause atoms clause306) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 308: packet; source clause 95031.
omit compatible in
private theorem sound307 : C.clause (decodeClause atoms clause307) := by
  exact C.covered_clause _ _ (C.packet_clause 5 1 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 309: convex_four; source clause 95186.
omit compatible in
private theorem sound308 : C.clause (decodeClause atoms clause308) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 310: convex_four; source clause 97061.
omit compatible in
private theorem sound309 : C.clause (decodeClause atoms clause309) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 311: convex_four; source clause 97269.
omit compatible in
private theorem sound310 : C.clause (decodeClause atoms clause310) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 312: convex_four; source clause 97477.
omit compatible in
private theorem sound311 : C.clause (decodeClause atoms clause311) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 313: convex_four; source clause 97685.
omit compatible in
private theorem sound312 : C.clause (decodeClause atoms clause312) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 314: convex_four; source clause 97890.
omit compatible in
private theorem sound313 : C.clause (decodeClause atoms clause313) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 315: convex_four; source clause 98101.
omit compatible in
private theorem sound314 : C.clause (decodeClause atoms clause314) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 316: convex_four; source clause 98309.
omit compatible in
private theorem sound315 : C.clause (decodeClause atoms clause315) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 317: convex_four; source clause 98517.
omit compatible in
private theorem sound316 : C.clause (decodeClause atoms clause316) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 318: convex_four; source clause 98725.
omit compatible in
private theorem sound317 : C.clause (decodeClause atoms clause317) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 319: convex_four; source clause 98930.
omit compatible in
private theorem sound318 : C.clause (decodeClause atoms clause318) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 320: packet; source clause 99782.
omit compatible in
private theorem sound319 : C.clause (decodeClause atoms clause319) := by
  exact C.covered_clause _ _ (C.packet_clause 1 9 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 321: convex_four; source clause 99970.
omit compatible in
private theorem sound320 : C.clause (decodeClause atoms clause320) := by
  exact C.covered_clause _ _ (C.convex_clause 1 7 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 322: convex_four; source clause 100386.
omit compatible in
private theorem sound321 : C.clause (decodeClause atoms clause321) := by
  exact C.covered_clause _ _ (C.convex_clause 1 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 323: convex_four; source clause 101218.
omit compatible in
private theorem sound322 : C.clause (decodeClause atoms clause322) := by
  exact C.covered_clause _ _ (C.convex_clause 1 8 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 324: convex_four; source clause 101429.
omit compatible in
private theorem sound323 : C.clause (decodeClause atoms clause323) := by
  exact C.covered_clause _ _ (C.convex_clause 1 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 325: convex_four; source clause 101637.
omit compatible in
private theorem sound324 : C.clause (decodeClause atoms clause324) := by
  exact C.covered_clause _ _ (C.convex_clause 1 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 326: convex_four; source clause 101845.
omit compatible in
private theorem sound325 : C.clause (decodeClause atoms clause325) := by
  exact C.covered_clause _ _ (C.convex_clause 1 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 327: convex_four; source clause 102053.
omit compatible in
private theorem sound326 : C.clause (decodeClause atoms clause326) := by
  exact C.covered_clause _ _ (C.convex_clause 1 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 328: convex_four; source clause 102258.
omit compatible in
private theorem sound327 : C.clause (decodeClause atoms clause327) := by
  exact C.covered_clause _ _ (C.convex_clause 1 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 329: convex_four; source clause 102460.
omit compatible in
private theorem sound328 : C.clause (decodeClause atoms clause328) := by
  exact C.covered_clause _ _ (C.convex_clause 1 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false) (by decide +kernel)

-- Clause 330: packet; source clause 102493.
omit compatible in
private theorem sound329 : C.clause (decodeClause atoms clause329) := by
  exact C.covered_clause _ _ (C.packet_clause 1 10 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 331: convex_four; source clause 102668.
omit compatible in
private theorem sound330 : C.clause (decodeClause atoms clause330) := by
  exact C.covered_clause _ _ (C.convex_clause 1 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false) (by decide +kernel)

-- Clause 332: convex_four; source clause 102882.
omit compatible in
private theorem sound331 : C.clause (decodeClause atoms clause331) := by
  exact C.covered_clause _ _ (C.convex_clause 1 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 333: convex_four; source clause 103090.
omit compatible in
private theorem sound332 : C.clause (decodeClause atoms clause332) := by
  exact C.covered_clause _ _ (C.convex_clause 1 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 334: convex_four; source clause 105173.
omit compatible in
private theorem sound333 : C.clause (decodeClause atoms clause333) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 335: convex_four; source clause 105589.
omit compatible in
private theorem sound334 : C.clause (decodeClause atoms clause334) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 336: convex_four; source clause 105797.
omit compatible in
private theorem sound335 : C.clause (decodeClause atoms clause335) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 337: convex_four; source clause 106213.
omit compatible in
private theorem sound336 : C.clause (decodeClause atoms clause336) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 338: convex_four; source clause 107877.
omit compatible in
private theorem sound337 : C.clause (decodeClause atoms clause337) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 339: convex_four; source clause 108085.
omit compatible in
private theorem sound338 : C.clause (decodeClause atoms clause338) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 340: convex_four; source clause 108501.
omit compatible in
private theorem sound339 : C.clause (decodeClause atoms clause339) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 341: packet; source clause 109341.
omit compatible in
private theorem sound340 : C.clause (decodeClause atoms clause340) := by
  exact C.covered_clause _ _ (C.packet_clause 2 3 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 342: convex_four; source clause 109538.
omit compatible in
private theorem sound341 : C.clause (decodeClause atoms clause341) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 343: convex_four; source clause 109954.
omit compatible in
private theorem sound342 : C.clause (decodeClause atoms clause342) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 344: packet; source clause 115575.
omit compatible in
private theorem sound343 : C.clause (decodeClause atoms clause343) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 345: convex_four; source clause 118069.
omit compatible in
private theorem sound344 : C.clause (decodeClause atoms clause344) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 346: convex_four; source clause 118277.
omit compatible in
private theorem sound345 : C.clause (decodeClause atoms clause345) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 347: convex_four; source clause 118693.
omit compatible in
private theorem sound346 : C.clause (decodeClause atoms clause346) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 348: convex_four; source clause 119730.
omit compatible in
private theorem sound347 : C.clause (decodeClause atoms clause347) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 349: convex_four; source clause 120146.
omit compatible in
private theorem sound348 : C.clause (decodeClause atoms clause348) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 350: convex_four; source clause 124930.
omit compatible in
private theorem sound349 : C.clause (decodeClause atoms clause349) := by
  exact C.covered_clause _ _ (C.convex_clause 2 7 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 351: convex_four; source clause 124932.
omit compatible in
private theorem sound350 : C.clause (decodeClause atoms clause350) := by
  exact C.covered_clause _ _ (C.convex_clause 2 7 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true false) (by decide +kernel)

-- Clause 352: convex_four; source clause 125346.
omit compatible in
private theorem sound351 : C.clause (decodeClause atoms clause351) := by
  exact C.covered_clause _ _ (C.convex_clause 2 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 353: convex_four; source clause 135541.
omit compatible in
private theorem sound352 : C.clause (decodeClause atoms clause352) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 354: convex_four; source clause 135749.
omit compatible in
private theorem sound353 : C.clause (decodeClause atoms clause353) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 355: convex_four; source clause 136165.
omit compatible in
private theorem sound354 : C.clause (decodeClause atoms clause354) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 356: convex_four; source clause 137202.
omit compatible in
private theorem sound355 : C.clause (decodeClause atoms clause355) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 357: convex_four; source clause 137618.
omit compatible in
private theorem sound356 : C.clause (decodeClause atoms clause356) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 358: convex_four; source clause 142402.
omit compatible in
private theorem sound357 : C.clause (decodeClause atoms clause357) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 359: convex_four; source clause 142404.
omit compatible in
private theorem sound358 : C.clause (decodeClause atoms clause358) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true false) (by decide +kernel)

-- Clause 360: convex_four; source clause 142818.
omit compatible in
private theorem sound359 : C.clause (decodeClause atoms clause359) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 361: convex_four; source clause 151141.
omit compatible in
private theorem sound360 : C.clause (decodeClause atoms clause360) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 362: convex_four; source clause 151349.
omit compatible in
private theorem sound361 : C.clause (decodeClause atoms clause361) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 363: convex_four; source clause 151557.
omit compatible in
private theorem sound362 : C.clause (decodeClause atoms clause362) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 364: convex_four; source clause 151765.
omit compatible in
private theorem sound363 : C.clause (decodeClause atoms clause363) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 365: convex_four; source clause 151970.
omit compatible in
private theorem sound364 : C.clause (decodeClause atoms clause364) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 366: convex_four; source clause 152181.
omit compatible in
private theorem sound365 : C.clause (decodeClause atoms clause365) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 367: convex_four; source clause 152389.
omit compatible in
private theorem sound366 : C.clause (decodeClause atoms clause366) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 368: convex_four; source clause 152597.
omit compatible in
private theorem sound367 : C.clause (decodeClause atoms clause367) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 369: convex_four; source clause 152805.
omit compatible in
private theorem sound368 : C.clause (decodeClause atoms clause368) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 370: convex_four; source clause 153010.
omit compatible in
private theorem sound369 : C.clause (decodeClause atoms clause369) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 371: convex_four; source clause 155298.
omit compatible in
private theorem sound370 : C.clause (decodeClause atoms clause370) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 372: convex_four; source clause 155509.
omit compatible in
private theorem sound371 : C.clause (decodeClause atoms clause371) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 373: convex_four; source clause 155717.
omit compatible in
private theorem sound372 : C.clause (decodeClause atoms clause372) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 374: convex_four; source clause 155925.
omit compatible in
private theorem sound373 : C.clause (decodeClause atoms clause373) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 375: convex_four; source clause 156133.
omit compatible in
private theorem sound374 : C.clause (decodeClause atoms clause374) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 376: convex_four; source clause 156338.
omit compatible in
private theorem sound375 : C.clause (decodeClause atoms clause375) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 377: packet; source clause 156365.
omit compatible in
private theorem sound376 : C.clause (decodeClause atoms clause376) := by
  exact C.covered_clause _ _ (C.packet_clause 4 10 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 378: convex_four; source clause 156540.
omit compatible in
private theorem sound377 : C.clause (decodeClause atoms clause377) := by
  exact C.covered_clause _ _ (C.convex_clause 4 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false) (by decide +kernel)

-- Clause 379: packet; source clause 156573.
omit compatible in
private theorem sound378 : C.clause (decodeClause atoms clause378) := by
  exact C.covered_clause _ _ (C.packet_clause 4 10 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 380: convex_four; source clause 156748.
omit compatible in
private theorem sound379 : C.clause (decodeClause atoms clause379) := by
  exact C.covered_clause _ _ (C.convex_clause 4 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false) (by decide +kernel)

-- Clause 381: convex_four; source clause 156962.
omit compatible in
private theorem sound380 : C.clause (decodeClause atoms clause380) := by
  exact C.covered_clause _ _ (C.convex_clause 4 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 382: convex_four; source clause 157170.
omit compatible in
private theorem sound381 : C.clause (decodeClause atoms clause381) := by
  exact C.covered_clause _ _ (C.convex_clause 4 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 383: convex_four; source clause 161330.
omit compatible in
private theorem sound382 : C.clause (decodeClause atoms clause382) := by
  exact C.covered_clause _ _ (C.convex_clause 5 7 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 384: convex_four; source clause 161746.
omit compatible in
private theorem sound383 : C.clause (decodeClause atoms clause383) := by
  exact C.covered_clause _ _ (C.convex_clause 5 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 385: convex_four; source clause 166738.
omit compatible in
private theorem sound384 : C.clause (decodeClause atoms clause384) := by
  exact C.covered_clause _ _ (C.convex_clause 6 8 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 386: convex_four; source clause 166949.
omit compatible in
private theorem sound385 : C.clause (decodeClause atoms clause385) := by
  exact C.covered_clause _ _ (C.convex_clause 6 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 387: convex_four; source clause 167157.
omit compatible in
private theorem sound386 : C.clause (decodeClause atoms clause386) := by
  exact C.covered_clause _ _ (C.convex_clause 6 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 388: convex_four; source clause 167365.
omit compatible in
private theorem sound387 : C.clause (decodeClause atoms clause387) := by
  exact C.covered_clause _ _ (C.convex_clause 6 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 389: convex_four; source clause 167573.
omit compatible in
private theorem sound388 : C.clause (decodeClause atoms clause388) := by
  exact C.covered_clause _ _ (C.convex_clause 6 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 390: convex_four; source clause 167778.
omit compatible in
private theorem sound389 : C.clause (decodeClause atoms clause389) := by
  exact C.covered_clause _ _ (C.convex_clause 6 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 391: packet; source clause 167805.
omit compatible in
private theorem sound390 : C.clause (decodeClause atoms clause390) := by
  exact C.covered_clause _ _ (C.packet_clause 6 10 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 392: convex_four; source clause 167980.
omit compatible in
private theorem sound391 : C.clause (decodeClause atoms clause391) := by
  exact C.covered_clause _ _ (C.convex_clause 6 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false) (by decide +kernel)

-- Clause 393: packet; source clause 168013.
omit compatible in
private theorem sound392 : C.clause (decodeClause atoms clause392) := by
  exact C.covered_clause _ _ (C.packet_clause 6 10 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 394: convex_four; source clause 168188.
omit compatible in
private theorem sound393 : C.clause (decodeClause atoms clause393) := by
  exact C.covered_clause _ _ (C.convex_clause 6 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false) (by decide +kernel)

-- Clause 395: convex_four; source clause 168402.
omit compatible in
private theorem sound394 : C.clause (decodeClause atoms clause394) := by
  exact C.covered_clause _ _ (C.convex_clause 6 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 396: convex_four; source clause 168610.
omit compatible in
private theorem sound395 : C.clause (decodeClause atoms clause395) := by
  exact C.covered_clause _ _ (C.convex_clause 6 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 397: packet; source clause 170717.
omit compatible in
private theorem sound396 : C.clause (decodeClause atoms clause396) := by
  exact C.covered_clause _ _ (C.packet_clause 8 10 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 398: convex_four; source clause 170892.
omit compatible in
private theorem sound397 : C.clause (decodeClause atoms clause397) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false) (by decide +kernel)

-- Clause 399: packet; source clause 170925.
omit compatible in
private theorem sound398 : C.clause (decodeClause atoms clause398) := by
  exact C.covered_clause _ _ (C.packet_clause 8 10 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 400: convex_four; source clause 171100.
omit compatible in
private theorem sound399 : C.clause (decodeClause atoms clause399) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false) (by decide +kernel)

-- Clause 401: convex_four; source clause 171314.
omit compatible in
private theorem sound400 : C.clause (decodeClause atoms clause400) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 402: convex_four; source clause 171522.
omit compatible in
private theorem sound401 : C.clause (decodeClause atoms clause401) := by
  exact C.covered_clause _ _ (C.convex_clause 8 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 403: convex_four; source clause 171718.
omit compatible in
private theorem sound402 : C.clause (decodeClause atoms clause402) := by
  exact C.covered_clause _ _ (C.convex_clause 9 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 404: convex_four; source clause 171722.
omit compatible in
private theorem sound403 : C.clause (decodeClause atoms clause403) := by
  exact C.covered_clause _ _ (C.convex_clause 9 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 405: no_octagon; source clause 171740.
omit compatible in
private theorem sound404 : C.clause (decodeClause atoms clause404) := by
  exact C.no_octagon_clause {0, 1, 2, 3, 5, 7, 9, 10} (by decide +kernel) _ (by decide +kernel)

-- Clause 406: no_octagon; source clause 171742.
omit compatible in
private theorem sound405 : C.clause (decodeClause atoms clause405) := by
  exact C.no_octagon_clause {0, 1, 2, 3, 5, 7, 9, 12} (by decide +kernel) _ (by decide +kernel)

-- Clause 407: no_octagon; source clause 171756.
omit compatible in
private theorem sound406 : C.clause (decodeClause atoms clause406) := by
  exact C.no_octagon_clause {1, 4, 6, 8, 9, 10, 11, 12} (by decide +kernel) _ (by decide +kernel)

private theorem all_sound : List.Forall (fun cl => C.clause (decodeClause atoms cl)) clauses := by
  exact And.intro (sound000 C compatible) (And.intro (sound001 C compatible) (And.intro (sound002 C compatible) (And.intro (sound003 C compatible) (And.intro (sound004 C compatible) (And.intro (sound005 C compatible) (And.intro (sound006 C compatible) (And.intro (sound007 C compatible) (And.intro (sound008 C compatible) (And.intro (sound009 C compatible) (And.intro (sound010 C compatible) (And.intro (sound011 C compatible) (And.intro (sound012 C compatible) (And.intro (sound013 C compatible) (And.intro (sound014 C compatible) (And.intro (sound015 C compatible) (And.intro (sound016 C compatible) (And.intro (sound017 C compatible) (And.intro (sound018 C compatible) (And.intro (sound019 C compatible) (And.intro (sound020 C compatible) (And.intro (sound021 C compatible) (And.intro (sound022 C compatible) (And.intro (sound023 C compatible) (And.intro (sound024 C compatible) (And.intro (sound025 C compatible) (And.intro (sound026 C compatible) (And.intro (sound027 C compatible) (And.intro (sound028 C compatible) (And.intro (sound029 C compatible) (And.intro (sound030 C compatible) (And.intro (sound031 C compatible) (And.intro (sound032 C compatible) (And.intro (sound033 C compatible) (And.intro (sound034 C compatible) (And.intro (sound035 C compatible) (And.intro (sound036 C compatible) (And.intro (sound037 C compatible) (And.intro (sound038 C compatible) (And.intro (sound039 C compatible) (And.intro (sound040 C compatible) (And.intro (sound041 C compatible) (And.intro (sound042 C compatible) (And.intro (sound043 C compatible) (And.intro (sound044 C compatible) (And.intro (sound045 C compatible) (And.intro (sound046 C compatible) (And.intro (sound047 C compatible) (And.intro (sound048 C) (And.intro (sound049 C) (And.intro (sound050 C) (And.intro (sound051 C) (And.intro (sound052 C) (And.intro (sound053 C) (And.intro (sound054 C) (And.intro (sound055 C) (And.intro (sound056 C) (And.intro (sound057 C) (And.intro (sound058 C) (And.intro (sound059 C) (And.intro (sound060 C) (And.intro (sound061 C) (And.intro (sound062 C) (And.intro (sound063 C) (And.intro (sound064 C) (And.intro (sound065 C) (And.intro (sound066 C) (And.intro (sound067 C) (And.intro (sound068 C) (And.intro (sound069 C) (And.intro (sound070 C) (And.intro (sound071 C) (And.intro (sound072 C) (And.intro (sound073 C) (And.intro (sound074 C) (And.intro (sound075 C) (And.intro (sound076 C) (And.intro (sound077 C) (And.intro (sound078 C) (And.intro (sound079 C) (And.intro (sound080 C) (And.intro (sound081 C) (And.intro (sound082 C) (And.intro (sound083 C) (And.intro (sound084 C) (And.intro (sound085 C) (And.intro (sound086 C compatible) (And.intro (sound087 C compatible) (And.intro (sound088 C compatible) (And.intro (sound089 C compatible) (And.intro (sound090 C compatible) (And.intro (sound091 C compatible) (And.intro (sound092 C compatible) (And.intro (sound093 C compatible) (And.intro (sound094 C compatible) (And.intro (sound095 C compatible) (And.intro (sound096 C compatible) (And.intro (sound097 C compatible) (And.intro (sound098 C compatible) (And.intro (sound099 C compatible) (And.intro (sound100 C compatible) (And.intro (sound101 C compatible) (And.intro (sound102 C compatible) (And.intro (sound103 C compatible) (And.intro (sound104 C compatible) (And.intro (sound105 C compatible) (And.intro (sound106 C compatible) (And.intro (sound107 C compatible) (And.intro (sound108 C compatible) (And.intro (sound109 C compatible) (And.intro (sound110 C compatible) (And.intro (sound111 C compatible) (And.intro (sound112 C compatible) (And.intro (sound113 C compatible) (And.intro (sound114 C compatible) (And.intro (sound115 C compatible) (And.intro (sound116 C compatible) (And.intro (sound117 C compatible) (And.intro (sound118 C compatible) (And.intro (sound119 C compatible) (And.intro (sound120 C compatible) (And.intro (sound121 C compatible) (And.intro (sound122 C compatible) (And.intro (sound123 C compatible) (And.intro (sound124 C compatible) (And.intro (sound125 C compatible) (And.intro (sound126 C compatible) (And.intro (sound127 C compatible) (And.intro (sound128 C compatible) (And.intro (sound129 C compatible) (And.intro (sound130 C compatible) (And.intro (sound131 C compatible) (And.intro (sound132 C compatible) (And.intro (sound133 C compatible) (And.intro (sound134 C compatible) (And.intro (sound135 C compatible) (And.intro (sound136 C compatible) (And.intro (sound137 C compatible) (And.intro (sound138 C compatible) (And.intro (sound139 C compatible) (And.intro (sound140 C compatible) (And.intro (sound141 C compatible) (And.intro (sound142 C compatible) (And.intro (sound143 C compatible) (And.intro (sound144 C compatible) (And.intro (sound145 C compatible) (And.intro (sound146 C compatible) (And.intro (sound147 C compatible) (And.intro (sound148 C compatible) (And.intro (sound149 C compatible) (And.intro (sound150 C compatible) (And.intro (sound151 C compatible) (And.intro (sound152 C compatible) (And.intro (sound153 C compatible) (And.intro (sound154 C compatible) (And.intro (sound155 C compatible) (And.intro (sound156 C compatible) (And.intro (sound157 C compatible) (And.intro (sound158 C compatible) (And.intro (sound159 C compatible) (And.intro (sound160 C compatible) (And.intro (sound161 C compatible) (And.intro (sound162 C compatible) (And.intro (sound163 C compatible) (And.intro (sound164 C compatible) (And.intro (sound165 C compatible) (And.intro (sound166 C compatible) (And.intro (sound167 C compatible) (And.intro (sound168 C compatible) (And.intro (sound169 C compatible) (And.intro (sound170 C compatible) (And.intro (sound171 C compatible) (And.intro (sound172 C compatible) (And.intro (sound173 C compatible) (And.intro (sound174 C compatible) (And.intro (sound175 C compatible) (And.intro (sound176 C compatible) (And.intro (sound177 C compatible) (And.intro (sound178 C compatible) (And.intro (sound179 C compatible) (And.intro (sound180 C compatible) (And.intro (sound181 C compatible) (And.intro (sound182 C compatible) (And.intro (sound183 C compatible) (And.intro (sound184 C compatible) (And.intro (sound185 C compatible) (And.intro (sound186 C compatible) (And.intro (sound187 C compatible) (And.intro (sound188 C compatible) (And.intro (sound189 C compatible) (And.intro (sound190 C compatible) (And.intro (sound191 C compatible) (And.intro (sound192 C compatible) (And.intro (sound193 C compatible) (And.intro (sound194 C compatible) (And.intro (sound195 C compatible) (And.intro (sound196 C) (And.intro (sound197 C) (And.intro (sound198 C) (And.intro (sound199 C) (And.intro (sound200 C) (And.intro (sound201 C) (And.intro (sound202 C) (And.intro (sound203 C) (And.intro (sound204 C) (And.intro (sound205 C) (And.intro (sound206 C) (And.intro (sound207 C) (And.intro (sound208 C) (And.intro (sound209 C) (And.intro (sound210 C) (And.intro (sound211 C) (And.intro (sound212 C) (And.intro (sound213 C) (And.intro (sound214 C) (And.intro (sound215 C) (And.intro (sound216 C) (And.intro (sound217 C) (And.intro (sound218 C) (And.intro (sound219 C) (And.intro (sound220 C) (And.intro (sound221 C) (And.intro (sound222 C) (And.intro (sound223 C) (And.intro (sound224 C) (And.intro (sound225 C) (And.intro (sound226 C) (And.intro (sound227 C) (And.intro (sound228 C) (And.intro (sound229 C) (And.intro (sound230 C) (And.intro (sound231 C) (And.intro (sound232 C) (And.intro (sound233 C) (And.intro (sound234 C) (And.intro (sound235 C) (And.intro (sound236 C) (And.intro (sound237 C) (And.intro (sound238 C) (And.intro (sound239 C) (And.intro (sound240 C) (And.intro (sound241 C) (And.intro (sound242 C) (And.intro (sound243 C) (And.intro (sound244 C) (And.intro (sound245 C) (And.intro (sound246 C) (And.intro (sound247 C) (And.intro (sound248 C) (And.intro (sound249 C) (And.intro (sound250 C) (And.intro (sound251 C) (And.intro (sound252 C) (And.intro (sound253 C) (And.intro (sound254 C) (And.intro (sound255 C) (And.intro (sound256 C) (And.intro (sound257 C) (And.intro (sound258 C) (And.intro (sound259 C) (And.intro (sound260 C) (And.intro (sound261 C) (And.intro (sound262 C) (And.intro (sound263 C) (And.intro (sound264 C) (And.intro (sound265 C) (And.intro (sound266 C) (And.intro (sound267 C) (And.intro (sound268 C) (And.intro (sound269 C) (And.intro (sound270 C) (And.intro (sound271 C) (And.intro (sound272 C) (And.intro (sound273 C) (And.intro (sound274 C) (And.intro (sound275 C) (And.intro (sound276 C) (And.intro (sound277 C) (And.intro (sound278 C) (And.intro (sound279 C) (And.intro (sound280 C) (And.intro (sound281 C) (And.intro (sound282 C) (And.intro (sound283 C) (And.intro (sound284 C) (And.intro (sound285 C) (And.intro (sound286 C) (And.intro (sound287 C) (And.intro (sound288 C) (And.intro (sound289 C) (And.intro (sound290 C) (And.intro (sound291 C) (And.intro (sound292 C) (And.intro (sound293 C) (And.intro (sound294 C) (And.intro (sound295 C) (And.intro (sound296 C) (And.intro (sound297 C) (And.intro (sound298 C) (And.intro (sound299 C) (And.intro (sound300 C) (And.intro (sound301 C) (And.intro (sound302 C) (And.intro (sound303 C) (And.intro (sound304 C) (And.intro (sound305 C) (And.intro (sound306 C) (And.intro (sound307 C) (And.intro (sound308 C) (And.intro (sound309 C) (And.intro (sound310 C) (And.intro (sound311 C) (And.intro (sound312 C) (And.intro (sound313 C) (And.intro (sound314 C) (And.intro (sound315 C) (And.intro (sound316 C) (And.intro (sound317 C) (And.intro (sound318 C) (And.intro (sound319 C) (And.intro (sound320 C) (And.intro (sound321 C) (And.intro (sound322 C) (And.intro (sound323 C) (And.intro (sound324 C) (And.intro (sound325 C) (And.intro (sound326 C) (And.intro (sound327 C) (And.intro (sound328 C) (And.intro (sound329 C) (And.intro (sound330 C) (And.intro (sound331 C) (And.intro (sound332 C) (And.intro (sound333 C) (And.intro (sound334 C) (And.intro (sound335 C) (And.intro (sound336 C) (And.intro (sound337 C) (And.intro (sound338 C) (And.intro (sound339 C) (And.intro (sound340 C) (And.intro (sound341 C) (And.intro (sound342 C) (And.intro (sound343 C) (And.intro (sound344 C) (And.intro (sound345 C) (And.intro (sound346 C) (And.intro (sound347 C) (And.intro (sound348 C) (And.intro (sound349 C) (And.intro (sound350 C) (And.intro (sound351 C) (And.intro (sound352 C) (And.intro (sound353 C) (And.intro (sound354 C) (And.intro (sound355 C) (And.intro (sound356 C) (And.intro (sound357 C) (And.intro (sound358 C) (And.intro (sound359 C) (And.intro (sound360 C) (And.intro (sound361 C) (And.intro (sound362 C) (And.intro (sound363 C) (And.intro (sound364 C) (And.intro (sound365 C) (And.intro (sound366 C) (And.intro (sound367 C) (And.intro (sound368 C) (And.intro (sound369 C) (And.intro (sound370 C) (And.intro (sound371 C) (And.intro (sound372 C) (And.intro (sound373 C) (And.intro (sound374 C) (And.intro (sound375 C) (And.intro (sound376 C) (And.intro (sound377 C) (And.intro (sound378 C) (And.intro (sound379 C) (And.intro (sound380 C) (And.intro (sound381 C) (And.intro (sound382 C) (And.intro (sound383 C) (And.intro (sound384 C) (And.intro (sound385 C) (And.intro (sound386 C) (And.intro (sound387 C) (And.intro (sound388 C) (And.intro (sound389 C) (And.intro (sound390 C) (And.intro (sound391 C) (And.intro (sound392 C) (And.intro (sound393 C) (And.intro (sound394 C) (And.intro (sound395 C) (And.intro (sound396 C) (And.intro (sound397 C) (And.intro (sound398 C) (And.intro (sound399 C) (And.intro (sound400 C) (And.intro (sound401 C) (And.intro (sound402 C) (And.intro (sound403 C) (And.intro (sound404 C) (And.intro (sound405 C) (sound406 C))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

theorem context_impossible (C : Context 13 n σ) : False := by
  have h : (C.valuation atoms).satisfies_fmla CoupledCore13.cnf_refutation.formula := by
    rw [formula_eq]
    constructor
    intro cl hc
    exact C.satisfies_of_clause atoms cl ((List.forall_iff_forall_mem.mp (all_sound C compatible)) cl hc)
  exact CoupledCore13.cnf_refutation (C.valuation atoms) h

#print axioms context_impossible
end ErdosSzekeres.Omission.CoupledTemplate

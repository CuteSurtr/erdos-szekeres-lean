import LeanCore

/-! The frozen 376-clause proof applies to any literal support satisfying
its finite state-dependent prerequisites. No fresh SAT result is assumed. -/
namespace ErdosSzekeres.Omission.CoupledTemplateSixth
open Coupled CoupledCoreSixth
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

def emptyTests : List (Fin 13 × Fin 13) := [(1, 0), (2, 0), (3, 0), (6, 0), (7, 0), (11, 0), (2, 1), (3, 1), (4, 1), (6, 1), (10, 1), (3, 2), (4, 2), (6, 2), (10, 2), (5, 3), (6, 3), (8, 3), (10, 3), (5, 4), (8, 5), (9, 6), (10, 6), (10, 7), (11, 7), (9, 8), (12, 9), (12, 10), (12, 11)]

def domainTests : List (Fin 13 × Fin 13 × ℕ × ℕ) := [(6, 10, 1, 5), (6, 10, 2, 5), (6, 10, 3, 5), (10, 11, 2, 2), (10, 11, 2, 3), (10, 11, 2, 4), (10, 11, 2, 5), (10, 11, 2, 6), (10, 11, 3, 3), (10, 11, 3, 4), (10, 11, 3, 5), (10, 11, 3, 6)]

def positiveTests : List (Fin 13 × Fin 13 × Fin 13) := [(0, 1, 2), (0, 1, 3), (0, 1, 6), (0, 1, 7), (0, 1, 10), (0, 1, 11), (0, 2, 3), (0, 2, 6), (0, 2, 7), (0, 2, 10), (0, 3, 6), (0, 3, 7), (0, 3, 10), (0, 6, 7), (0, 6, 10), (0, 10, 7), (0, 11, 7), (1, 2, 3), (1, 4, 2), (1, 2, 6), (1, 2, 7), (1, 2, 10), (1, 5, 3), (1, 3, 6), (1, 3, 7), (1, 3, 10), (1, 4, 10), (1, 4, 11), (1, 5, 10), (1, 5, 11), (1, 6, 7), (1, 9, 6), (1, 6, 10), (1, 10, 7), (1, 11, 7), (1, 9, 11), (1, 12, 10), (1, 12, 11), (2, 5, 3), (2, 3, 6), (2, 3, 7), (2, 3, 10), (2, 4, 5), (2, 4, 8), (2, 4, 9), (2, 4, 10), (2, 4, 11), (2, 4, 12), (2, 5, 8), (2, 5, 9), (2, 5, 10), (2, 5, 11), (2, 5, 12), (2, 6, 7), (2, 9, 6), (2, 6, 10), (2, 10, 7), (2, 11, 7), (2, 8, 9), (2, 8, 10), (2, 8, 11), (2, 8, 12), (2, 9, 10), (2, 9, 11), (2, 9, 12), (2, 12, 10), (2, 12, 11), (3, 5, 10), (3, 5, 11), (3, 6, 7), (3, 9, 6), (3, 6, 10), (3, 10, 7), (3, 11, 7), (3, 8, 10), (3, 8, 11), (3, 9, 10), (3, 9, 11), (3, 12, 10), (3, 12, 11), (4, 5, 8), (4, 5, 9), (4, 5, 10), (4, 5, 11), (4, 5, 12), (4, 8, 9), (4, 8, 10), (4, 8, 11), (4, 8, 12), (4, 9, 10), (4, 9, 11), (4, 9, 12), (4, 12, 10), (4, 12, 11), (5, 8, 9), (5, 8, 10), (5, 8, 11), (5, 8, 12), (5, 9, 10), (5, 9, 11), (5, 9, 12), (5, 12, 10), (5, 12, 11), (6, 10, 7), (6, 11, 7), (6, 9, 10), (6, 9, 11), (6, 12, 10), (6, 12, 11), (7, 10, 11), (8, 9, 10), (8, 9, 11), (8, 9, 12), (8, 12, 10), (8, 12, 11), (9, 12, 10), (9, 12, 11), (10, 12, 11)]

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
private def clause005 : Sat.Clause := [.pos 5]
private def clause006 : Sat.Clause := [.pos 6]
private def clause007 : Sat.Clause := [.pos 8]
private def clause008 : Sat.Clause := [.pos 9]
private def clause009 : Sat.Clause := [.pos 10]
private def clause010 : Sat.Clause := [.pos 11]
private def clause011 : Sat.Clause := [.pos 14]
private def clause012 : Sat.Clause := [.pos 16]
private def clause013 : Sat.Clause := [.pos 17]
private def clause014 : Sat.Clause := [.pos 18]
private def clause015 : Sat.Clause := [.pos 21]
private def clause016 : Sat.Clause := [.pos 22]
private def clause017 : Sat.Clause := [.pos 24]
private def clause018 : Sat.Clause := [.pos 25]
private def clause019 : Sat.Clause := [.pos 28]
private def clause020 : Sat.Clause := [.pos 31]
private def clause021 : Sat.Clause := [.pos 34]
private def clause022 : Sat.Clause := [.neg 35, .pos 36, .neg 39, .pos 40]
private def clause023 : Sat.Clause := [.neg 35, .neg 36, .pos 37, .neg 39, .pos 40]
private def clause024 : Sat.Clause := [.neg 35, .neg 37, .pos 38, .neg 39, .pos 40]
private def clause025 : Sat.Clause := [.pos 35]
private def clause026 : Sat.Clause := [.pos 42]
private def clause027 : Sat.Clause := [.pos 43]
private def clause028 : Sat.Clause := [.pos 44]
private def clause029 : Sat.Clause := [.pos 49]
private def clause030 : Sat.Clause := [.neg 50, .neg 51, .pos 52, .neg 54, .pos 55]
private def clause031 : Sat.Clause := [.neg 50, .neg 51, .pos 52, .neg 55, .pos 56]
private def clause032 : Sat.Clause := [.neg 50, .neg 51, .pos 52, .neg 56, .pos 57]
private def clause033 : Sat.Clause := [.neg 50, .neg 51, .pos 52, .neg 57, .pos 58]
private def clause034 : Sat.Clause := [.neg 50, .neg 51, .pos 52, .neg 58]
private def clause035 : Sat.Clause := [.neg 50, .neg 52, .pos 53, .neg 55, .pos 56]
private def clause036 : Sat.Clause := [.neg 50, .neg 52, .pos 53, .neg 56, .pos 57]
private def clause037 : Sat.Clause := [.neg 50, .neg 52, .pos 53, .neg 57, .pos 58]
private def clause038 : Sat.Clause := [.neg 50, .neg 52, .pos 53, .neg 58]
private def clause039 : Sat.Clause := [.pos 59]
private def clause040 : Sat.Clause := [.pos 60]
private def clause041 : Sat.Clause := [.neg 0, .neg 6, .pos 7, .neg 61]
private def clause042 : Sat.Clause := [.neg 0, .neg 11, .pos 12, .neg 65]
private def clause043 : Sat.Clause := [.neg 6, .neg 7, .neg 14, .pos 15, .neg 82]
private def clause044 : Sat.Clause := [.neg 6, .neg 7, .neg 18, .pos 19, .neg 86]
private def clause045 : Sat.Clause := [.neg 11, .neg 12, .neg 50, .pos 55, .neg 104]
private def clause046 : Sat.Clause := [.neg 14, .neg 15, .neg 22, .pos 23, .neg 108]
private def clause047 : Sat.Clause := [.neg 14, .neg 15, .neg 25, .pos 26, .neg 110]
private def clause048 : Sat.Clause := [.neg 17, .pos 20, .neg 41]
private def clause049 : Sat.Clause := [.neg 18, .neg 19, .neg 50, .pos 56, .neg 136]
private def clause050 : Sat.Clause := [.neg 22, .neg 23, .neg 35, .pos 39, .neg 143]
private def clause051 : Sat.Clause := [.neg 22, .pos 27, .neg 41]
private def clause052 : Sat.Clause := [.neg 25, .neg 26, .neg 50, .pos 57, .neg 151]
private def clause053 : Sat.Clause := [.neg 35, .neg 50, .pos 51, .pos 183]
private def clause054 : Sat.Clause := [.neg 35, .neg 40, .neg 50, .neg 183]
private def clause055 : Sat.Clause := [.neg 35, .neg 38, .neg 59, .pos 184]
private def clause056 : Sat.Clause := [.neg 42, .neg 50, .pos 54, .neg 186]
private def clause057 : Sat.Clause := [.neg 50, .neg 53, .neg 60, .pos 196]
private def clause058 : Sat.Clause := [.pos 61]
private def clause059 : Sat.Clause := [.pos 62]
private def clause060 : Sat.Clause := [.pos 63]
private def clause061 : Sat.Clause := [.pos 64]
private def clause062 : Sat.Clause := [.pos 65]
private def clause063 : Sat.Clause := [.pos 66]
private def clause064 : Sat.Clause := [.pos 67]
private def clause065 : Sat.Clause := [.pos 68]
private def clause066 : Sat.Clause := [.pos 69]
private def clause067 : Sat.Clause := [.pos 70]
private def clause068 : Sat.Clause := [.pos 72]
private def clause069 : Sat.Clause := [.pos 73]
private def clause070 : Sat.Clause := [.pos 74]
private def clause071 : Sat.Clause := [.pos 76]
private def clause072 : Sat.Clause := [.pos 77]
private def clause073 : Sat.Clause := [.neg 79]
private def clause074 : Sat.Clause := [.neg 80]
private def clause075 : Sat.Clause := [.pos 82]
private def clause076 : Sat.Clause := [.neg 83]
private def clause077 : Sat.Clause := [.pos 84]
private def clause078 : Sat.Clause := [.pos 85]
private def clause079 : Sat.Clause := [.pos 86]
private def clause080 : Sat.Clause := [.neg 88]
private def clause081 : Sat.Clause := [.pos 89]
private def clause082 : Sat.Clause := [.pos 90]
private def clause083 : Sat.Clause := [.pos 91]
private def clause084 : Sat.Clause := [.pos 93]
private def clause085 : Sat.Clause := [.pos 94]
private def clause086 : Sat.Clause := [.pos 95]
private def clause087 : Sat.Clause := [.pos 96]
private def clause088 : Sat.Clause := [.pos 97]
private def clause089 : Sat.Clause := [.neg 98]
private def clause090 : Sat.Clause := [.pos 99]
private def clause091 : Sat.Clause := [.neg 101]
private def clause092 : Sat.Clause := [.neg 102]
private def clause093 : Sat.Clause := [.pos 103]
private def clause094 : Sat.Clause := [.neg 105]
private def clause095 : Sat.Clause := [.neg 106]
private def clause096 : Sat.Clause := [.neg 107]
private def clause097 : Sat.Clause := [.pos 108]
private def clause098 : Sat.Clause := [.pos 109]
private def clause099 : Sat.Clause := [.pos 110]
private def clause100 : Sat.Clause := [.pos 112]
private def clause101 : Sat.Clause := [.pos 113]
private def clause102 : Sat.Clause := [.pos 114]
private def clause103 : Sat.Clause := [.pos 115]
private def clause104 : Sat.Clause := [.pos 116]
private def clause105 : Sat.Clause := [.pos 117]
private def clause106 : Sat.Clause := [.pos 118]
private def clause107 : Sat.Clause := [.pos 119]
private def clause108 : Sat.Clause := [.pos 120]
private def clause109 : Sat.Clause := [.pos 121]
private def clause110 : Sat.Clause := [.pos 122]
private def clause111 : Sat.Clause := [.pos 123]
private def clause112 : Sat.Clause := [.neg 124]
private def clause113 : Sat.Clause := [.pos 125]
private def clause114 : Sat.Clause := [.neg 127]
private def clause115 : Sat.Clause := [.neg 128]
private def clause116 : Sat.Clause := [.pos 129]
private def clause117 : Sat.Clause := [.pos 130]
private def clause118 : Sat.Clause := [.pos 131]
private def clause119 : Sat.Clause := [.pos 132]
private def clause120 : Sat.Clause := [.pos 133]
private def clause121 : Sat.Clause := [.pos 134]
private def clause122 : Sat.Clause := [.pos 135]
private def clause123 : Sat.Clause := [.neg 137]
private def clause124 : Sat.Clause := [.neg 138]
private def clause125 : Sat.Clause := [.pos 139]
private def clause126 : Sat.Clause := [.pos 140]
private def clause127 : Sat.Clause := [.pos 141]
private def clause128 : Sat.Clause := [.neg 142]
private def clause129 : Sat.Clause := [.pos 143]
private def clause130 : Sat.Clause := [.neg 145]
private def clause131 : Sat.Clause := [.neg 146]
private def clause132 : Sat.Clause := [.pos 147]
private def clause133 : Sat.Clause := [.pos 148]
private def clause134 : Sat.Clause := [.pos 149]
private def clause135 : Sat.Clause := [.pos 150]
private def clause136 : Sat.Clause := [.neg 152]
private def clause137 : Sat.Clause := [.neg 153]
private def clause138 : Sat.Clause := [.pos 154]
private def clause139 : Sat.Clause := [.pos 155]
private def clause140 : Sat.Clause := [.pos 156]
private def clause141 : Sat.Clause := [.pos 157]
private def clause142 : Sat.Clause := [.pos 158]
private def clause143 : Sat.Clause := [.pos 159]
private def clause144 : Sat.Clause := [.pos 160]
private def clause145 : Sat.Clause := [.pos 161]
private def clause146 : Sat.Clause := [.pos 162]
private def clause147 : Sat.Clause := [.pos 163]
private def clause148 : Sat.Clause := [.pos 164]
private def clause149 : Sat.Clause := [.pos 165]
private def clause150 : Sat.Clause := [.neg 167]
private def clause151 : Sat.Clause := [.neg 168]
private def clause152 : Sat.Clause := [.pos 169]
private def clause153 : Sat.Clause := [.pos 170]
private def clause154 : Sat.Clause := [.pos 171]
private def clause155 : Sat.Clause := [.pos 172]
private def clause156 : Sat.Clause := [.pos 173]
private def clause157 : Sat.Clause := [.pos 174]
private def clause158 : Sat.Clause := [.pos 175]
private def clause159 : Sat.Clause := [.neg 177]
private def clause160 : Sat.Clause := [.neg 178]
private def clause161 : Sat.Clause := [.neg 179]
private def clause162 : Sat.Clause := [.neg 180]
private def clause163 : Sat.Clause := [.pos 181]
private def clause164 : Sat.Clause := [.pos 182]
private def clause165 : Sat.Clause := [.neg 184]
private def clause166 : Sat.Clause := [.neg 185]
private def clause167 : Sat.Clause := [.pos 186]
private def clause168 : Sat.Clause := [.pos 187]
private def clause169 : Sat.Clause := [.pos 188]
private def clause170 : Sat.Clause := [.pos 189]
private def clause171 : Sat.Clause := [.neg 191]
private def clause172 : Sat.Clause := [.neg 192]
private def clause173 : Sat.Clause := [.neg 194]
private def clause174 : Sat.Clause := [.neg 195]
private def clause175 : Sat.Clause := [.neg 196]
private def clause176 : Sat.Clause := [.neg 61, .neg 62, .neg 67, .neg 82, .pos 197]
private def clause177 : Sat.Clause := [.neg 61, .neg 63, .neg 68, .neg 84, .pos 198]
private def clause178 : Sat.Clause := [.neg 61, .neg 64, .neg 69, .neg 85, .pos 199]
private def clause179 : Sat.Clause := [.neg 61, .neg 65, .neg 70, .neg 86, .pos 200]
private def clause180 : Sat.Clause := [.neg 0, .neg 6, .neg 20, .neg 61, .neg 66, .pos 71, .neg 87]
private def clause181 : Sat.Clause := [.neg 61, .neg 66, .neg 71, .neg 87, .pos 201]
private def clause182 : Sat.Clause := [.neg 62, .neg 63, .neg 72, .neg 89, .pos 202]
private def clause183 : Sat.Clause := [.neg 62, .neg 64, .neg 73, .neg 90, .pos 203]
private def clause184 : Sat.Clause := [.neg 62, .neg 65, .neg 74, .neg 91, .pos 204]
private def clause185 : Sat.Clause := [.neg 0, .neg 8, .neg 27, .neg 62, .neg 66, .pos 75, .neg 92]
private def clause186 : Sat.Clause := [.neg 62, .neg 66, .neg 75, .neg 92, .pos 205]
private def clause187 : Sat.Clause := [.neg 63, .neg 64, .neg 76, .neg 97, .pos 206]
private def clause188 : Sat.Clause := [.neg 63, .neg 65, .neg 77, .neg 99, .pos 207]
private def clause189 : Sat.Clause := [.neg 63, .neg 66, .neg 78, .neg 100, .pos 208]
private def clause190 : Sat.Clause := [.neg 64, .neg 65, .pos 79, .pos 101, .pos 209]
private def clause191 : Sat.Clause := [.neg 64, .neg 66, .pos 80, .pos 102, .pos 210]
private def clause192 : Sat.Clause := [.neg 65, .neg 66, .neg 81, .neg 104, .pos 211]
private def clause193 : Sat.Clause := [.neg 67, .neg 68, .neg 72, .neg 108, .pos 212]
private def clause194 : Sat.Clause := [.neg 67, .neg 69, .neg 73, .neg 109, .pos 213]
private def clause195 : Sat.Clause := [.neg 67, .neg 70, .neg 74, .neg 110, .pos 214]
private def clause196 : Sat.Clause := [.neg 5, .neg 14, .pos 20, .neg 67, .pos 71, .neg 75, .neg 111]
private def clause197 : Sat.Clause := [.neg 67, .neg 71, .neg 75, .neg 111, .pos 215]
private def clause198 : Sat.Clause := [.neg 68, .neg 69, .neg 76, .neg 123, .pos 216]
private def clause199 : Sat.Clause := [.neg 68, .neg 70, .neg 77, .neg 125, .pos 217]
private def clause200 : Sat.Clause := [.neg 68, .neg 71, .neg 78, .neg 126, .pos 218]
private def clause201 : Sat.Clause := [.neg 69, .neg 70, .pos 79, .pos 127, .pos 219]
private def clause202 : Sat.Clause := [.neg 69, .neg 71, .pos 80, .pos 128, .pos 220]
private def clause203 : Sat.Clause := [.neg 1, .neg 20, .pos 50, .neg 70, .pos 71, .neg 81, .neg 136]
private def clause204 : Sat.Clause := [.neg 70, .pos 71, .neg 81, .neg 136, .neg 221]
private def clause205 : Sat.Clause := [.neg 70, .neg 71, .neg 81, .neg 136, .pos 221]
private def clause206 : Sat.Clause := [.neg 72, .neg 73, .neg 76, .neg 141, .pos 222]
private def clause207 : Sat.Clause := [.neg 72, .neg 74, .neg 77, .neg 143, .pos 223]
private def clause208 : Sat.Clause := [.neg 5, .neg 22, .pos 27, .neg 72, .pos 75, .neg 78, .neg 144]
private def clause209 : Sat.Clause := [.neg 72, .neg 75, .neg 78, .neg 144, .pos 224]
private def clause210 : Sat.Clause := [.neg 73, .neg 74, .pos 79, .pos 145, .pos 225]
private def clause211 : Sat.Clause := [.neg 73, .neg 75, .pos 80, .pos 146, .pos 226]
private def clause212 : Sat.Clause := [.neg 2, .neg 27, .pos 50, .neg 74, .pos 75, .neg 81, .neg 151]
private def clause213 : Sat.Clause := [.neg 74, .pos 75, .neg 81, .neg 151, .neg 227]
private def clause214 : Sat.Clause := [.neg 74, .neg 75, .neg 81, .neg 151, .pos 227]
private def clause215 : Sat.Clause := [.neg 76, .neg 77, .pos 79, .pos 179, .pos 228]
private def clause216 : Sat.Clause := [.neg 4, .pos 41, .neg 43, .neg 76, .pos 78, .pos 80, .pos 180]
private def clause217 : Sat.Clause := [.neg 76, .neg 78, .pos 80, .pos 180, .pos 229]
private def clause218 : Sat.Clause := [.neg 3, .neg 41, .pos 50, .neg 77, .pos 78, .neg 81, .neg 183]
private def clause219 : Sat.Clause := [.neg 77, .neg 78, .neg 81, .neg 183, .pos 230]
private def clause220 : Sat.Clause := [.neg 4, .neg 43, .pos 50, .pos 79, .pos 80, .pos 81, .neg 186]
private def clause221 : Sat.Clause := [.pos 79, .pos 80, .neg 81, .neg 186, .pos 231]
private def clause222 : Sat.Clause := [.neg 82, .neg 84, .neg 89, .neg 108, .pos 232]
private def clause223 : Sat.Clause := [.neg 82, .neg 85, .neg 90, .neg 109, .pos 233]
private def clause224 : Sat.Clause := [.neg 82, .neg 86, .neg 91, .neg 110, .pos 234]
private def clause225 : Sat.Clause := [.neg 6, .neg 14, .neg 27, .neg 82, .neg 87, .pos 92, .neg 111]
private def clause226 : Sat.Clause := [.neg 82, .neg 87, .neg 92, .neg 111, .pos 235]
private def clause227 : Sat.Clause := [.neg 13, .neg 16, .pos 20, .pos 83, .pos 87, .neg 94, .neg 116]
private def clause228 : Sat.Clause := [.neg 6, .pos 13, .neg 16, .pos 83, .pos 87, .neg 94, .neg 116]
private def clause229 : Sat.Clause := [.neg 84, .neg 85, .neg 97, .neg 123, .pos 236]
private def clause230 : Sat.Clause := [.neg 84, .neg 86, .neg 99, .neg 125, .pos 237]
private def clause231 : Sat.Clause := [.neg 84, .neg 87, .neg 100, .neg 126, .pos 238]
private def clause232 : Sat.Clause := [.neg 85, .neg 86, .pos 101, .pos 127, .pos 239]
private def clause233 : Sat.Clause := [.neg 85, .neg 87, .pos 102, .pos 128, .pos 240]
private def clause234 : Sat.Clause := [.neg 6, .neg 20, .pos 50, .neg 86, .pos 87, .neg 104, .neg 136]
private def clause235 : Sat.Clause := [.neg 86, .neg 87, .neg 104, .neg 136, .pos 241]
private def clause236 : Sat.Clause := [.neg 13, .neg 21, .pos 27, .pos 88, .pos 92, .neg 96, .neg 140]
private def clause237 : Sat.Clause := [.neg 8, .pos 13, .neg 21, .pos 88, .pos 92, .neg 96, .neg 140]
private def clause238 : Sat.Clause := [.neg 89, .neg 90, .neg 97, .neg 141, .pos 242]
private def clause239 : Sat.Clause := [.neg 89, .neg 91, .neg 99, .neg 143, .pos 243]
private def clause240 : Sat.Clause := [.neg 89, .neg 92, .neg 100, .neg 144, .pos 244]
private def clause241 : Sat.Clause := [.neg 90, .neg 91, .pos 101, .pos 145, .pos 245]
private def clause242 : Sat.Clause := [.neg 90, .neg 92, .pos 102, .pos 146, .pos 246]
private def clause243 : Sat.Clause := [.neg 8, .neg 27, .pos 50, .neg 91, .pos 92, .neg 104, .neg 151]
private def clause244 : Sat.Clause := [.neg 91, .pos 92, .neg 104, .neg 151, .neg 247]
private def clause245 : Sat.Clause := [.neg 91, .neg 92, .neg 104, .neg 151, .pos 247]
private def clause246 : Sat.Clause := [.neg 9, .neg 29, .neg 50, .neg 93, .neg 94, .pos 104, .neg 166]
private def clause247 : Sat.Clause := [.neg 11, .pos 32, .neg 33, .neg 95, .neg 96, .pos 104, .neg 176]
private def clause248 : Sat.Clause := [.neg 97, .neg 99, .pos 101, .pos 179, .pos 248]
private def clause249 : Sat.Clause := [.neg 10, .pos 13, .neg 43, .neg 97, .pos 100, .pos 102, .pos 180]
private def clause250 : Sat.Clause := [.neg 97, .neg 100, .pos 102, .pos 180, .pos 249]
private def clause251 : Sat.Clause := [.neg 13, .neg 34, .pos 41, .pos 98, .pos 100, .neg 103, .neg 182]
private def clause252 : Sat.Clause := [.neg 10, .neg 41, .pos 50, .neg 99, .pos 100, .neg 104, .neg 183]
private def clause253 : Sat.Clause := [.neg 99, .neg 100, .neg 104, .neg 183, .pos 250]
private def clause254 : Sat.Clause := [.neg 11, .pos 13, .neg 43, .pos 101, .pos 102, .pos 104, .neg 186]
private def clause255 : Sat.Clause := [.pos 101, .pos 102, .neg 104, .neg 186, .pos 251]
private def clause256 : Sat.Clause := [.neg 13, .pos 50, .neg 59, .pos 104, .pos 105, .pos 106, .pos 196]
private def clause257 : Sat.Clause := [.neg 20, .neg 21, .pos 27, .pos 107, .pos 111, .neg 121, .neg 140]
private def clause258 : Sat.Clause := [.neg 14, .pos 20, .neg 21, .pos 107, .pos 111, .neg 121, .neg 140]
private def clause259 : Sat.Clause := [.neg 108, .neg 109, .neg 123, .neg 141, .pos 252]
private def clause260 : Sat.Clause := [.neg 108, .neg 110, .neg 125, .neg 143, .pos 253]
private def clause261 : Sat.Clause := [.neg 108, .neg 111, .neg 126, .neg 144, .pos 254]
private def clause262 : Sat.Clause := [.neg 109, .neg 110, .pos 127, .pos 145, .pos 255]
private def clause263 : Sat.Clause := [.neg 109, .neg 111, .pos 128, .pos 146, .pos 256]
private def clause264 : Sat.Clause := [.neg 14, .neg 27, .pos 50, .neg 110, .pos 111, .neg 136, .neg 151]
private def clause265 : Sat.Clause := [.neg 110, .pos 111, .neg 136, .neg 151, .neg 257]
private def clause266 : Sat.Clause := [.neg 110, .neg 111, .neg 136, .neg 151, .pos 257]
private def clause267 : Sat.Clause := [.neg 112, .neg 113, .neg 118, .neg 154, .pos 258]
private def clause268 : Sat.Clause := [.neg 112, .neg 114, .neg 119, .neg 155, .pos 259]
private def clause269 : Sat.Clause := [.neg 112, .neg 115, .neg 120, .neg 156, .pos 260]
private def clause270 : Sat.Clause := [.neg 112, .neg 116, .neg 121, .neg 157, .pos 261]
private def clause271 : Sat.Clause := [.neg 112, .neg 117, .neg 122, .neg 158, .pos 262]
private def clause272 : Sat.Clause := [.neg 113, .neg 114, .neg 129, .neg 159, .pos 263]
private def clause273 : Sat.Clause := [.neg 113, .neg 115, .neg 130, .neg 160, .pos 264]
private def clause274 : Sat.Clause := [.neg 113, .neg 116, .neg 131, .neg 161, .pos 265]
private def clause275 : Sat.Clause := [.neg 113, .neg 117, .neg 132, .neg 162, .pos 266]
private def clause276 : Sat.Clause := [.neg 114, .neg 115, .neg 133, .neg 163, .pos 267]
private def clause277 : Sat.Clause := [.neg 114, .neg 116, .neg 134, .neg 164, .pos 268]
private def clause278 : Sat.Clause := [.neg 114, .neg 117, .neg 135, .neg 165, .pos 269]
private def clause279 : Sat.Clause := [.neg 115, .neg 116, .pos 136, .pos 166, .pos 270]
private def clause280 : Sat.Clause := [.neg 115, .neg 117, .pos 137, .pos 167, .pos 271]
private def clause281 : Sat.Clause := [.neg 116, .neg 117, .pos 138, .pos 168, .pos 272]
private def clause282 : Sat.Clause := [.neg 118, .neg 119, .neg 129, .neg 169, .pos 273]
private def clause283 : Sat.Clause := [.neg 118, .neg 120, .neg 130, .neg 170, .pos 274]
private def clause284 : Sat.Clause := [.neg 118, .neg 121, .neg 131, .neg 171, .pos 275]
private def clause285 : Sat.Clause := [.neg 118, .neg 122, .neg 132, .neg 172, .pos 276]
private def clause286 : Sat.Clause := [.neg 119, .neg 120, .neg 133, .neg 173, .pos 277]
private def clause287 : Sat.Clause := [.neg 119, .neg 121, .neg 134, .neg 174, .pos 278]
private def clause288 : Sat.Clause := [.neg 119, .neg 122, .neg 135, .neg 175, .pos 279]
private def clause289 : Sat.Clause := [.neg 120, .neg 121, .pos 136, .pos 176, .pos 280]
private def clause290 : Sat.Clause := [.neg 120, .neg 122, .pos 137, .pos 177, .pos 281]
private def clause291 : Sat.Clause := [.neg 121, .neg 122, .pos 138, .pos 178, .pos 282]
private def clause292 : Sat.Clause := [.neg 123, .neg 125, .pos 127, .pos 179, .pos 283]
private def clause293 : Sat.Clause := [.neg 17, .pos 20, .neg 43, .neg 123, .pos 126, .pos 128, .pos 180]
private def clause294 : Sat.Clause := [.neg 123, .neg 126, .pos 128, .pos 180, .pos 284]
private def clause295 : Sat.Clause := [.neg 20, .neg 34, .pos 41, .pos 124, .pos 126, .neg 134, .neg 182]
private def clause296 : Sat.Clause := [.neg 17, .neg 41, .pos 50, .neg 125, .pos 126, .neg 136, .neg 183]
private def clause297 : Sat.Clause := [.neg 125, .pos 126, .neg 136, .neg 183, .neg 285]
private def clause298 : Sat.Clause := [.neg 125, .neg 126, .neg 136, .neg 183, .pos 285]
private def clause299 : Sat.Clause := [.neg 18, .pos 20, .neg 43, .pos 127, .pos 128, .pos 136, .neg 186]
private def clause300 : Sat.Clause := [.pos 127, .pos 128, .neg 136, .neg 186, .pos 286]
private def clause301 : Sat.Clause := [.neg 129, .neg 130, .neg 133, .neg 187, .pos 287]
private def clause302 : Sat.Clause := [.neg 129, .neg 131, .neg 134, .neg 188, .pos 288]
private def clause303 : Sat.Clause := [.neg 129, .neg 132, .neg 135, .neg 189, .pos 289]
private def clause304 : Sat.Clause := [.neg 130, .neg 131, .pos 136, .pos 190, .pos 290]
private def clause305 : Sat.Clause := [.neg 130, .neg 132, .pos 137, .pos 191, .pos 291]
private def clause306 : Sat.Clause := [.neg 131, .neg 132, .pos 138, .pos 192, .pos 292]
private def clause307 : Sat.Clause := [.neg 133, .neg 134, .pos 136, .pos 193, .pos 293]
private def clause308 : Sat.Clause := [.neg 133, .neg 135, .pos 137, .pos 194, .pos 294]
private def clause309 : Sat.Clause := [.neg 134, .neg 135, .pos 138, .pos 195, .pos 295]
private def clause310 : Sat.Clause := [.neg 20, .pos 50, .neg 59, .pos 136, .pos 137, .pos 138, .pos 196]
private def clause311 : Sat.Clause := [.pos 136, .pos 137, .pos 138, .pos 196, .pos 296]
private def clause312 : Sat.Clause := [.neg 136, .pos 137, .pos 138, .pos 196, .neg 296]
private def clause313 : Sat.Clause := [.neg 21, .neg 32, .neg 50, .neg 139, .neg 140, .pos 151, .neg 176]
private def clause314 : Sat.Clause := [.neg 141, .neg 143, .pos 145, .pos 179, .pos 297]
private def clause315 : Sat.Clause := [.neg 22, .pos 27, .neg 43, .neg 141, .pos 144, .pos 146, .pos 180]
private def clause316 : Sat.Clause := [.neg 141, .neg 144, .pos 146, .pos 180, .pos 298]
private def clause317 : Sat.Clause := [.neg 27, .neg 34, .pos 41, .pos 142, .pos 144, .neg 150, .neg 182]
private def clause318 : Sat.Clause := [.neg 22, .neg 41, .pos 50, .neg 143, .pos 144, .neg 151, .neg 183]
private def clause319 : Sat.Clause := [.neg 143, .neg 144, .neg 151, .neg 183, .pos 299]
private def clause320 : Sat.Clause := [.neg 25, .pos 27, .neg 43, .pos 145, .pos 146, .pos 151, .neg 186]
private def clause321 : Sat.Clause := [.pos 145, .pos 146, .neg 151, .neg 186, .pos 300]
private def clause322 : Sat.Clause := [.neg 24, .neg 45, .neg 50, .neg 147, .neg 148, .pos 151, .neg 190]
private def clause323 : Sat.Clause := [.neg 25, .pos 45, .neg 46, .neg 147, .neg 148, .pos 151, .neg 190]
private def clause324 : Sat.Clause := [.neg 25, .pos 47, .neg 48, .neg 149, .neg 150, .pos 151, .neg 193]
private def clause325 : Sat.Clause := [.neg 27, .pos 50, .neg 59, .pos 151, .pos 152, .pos 153, .pos 196]
private def clause326 : Sat.Clause := [.neg 154, .neg 155, .neg 159, .neg 169, .pos 301]
private def clause327 : Sat.Clause := [.neg 154, .neg 156, .neg 160, .neg 170, .pos 302]
private def clause328 : Sat.Clause := [.neg 154, .neg 157, .neg 161, .neg 171, .pos 303]
private def clause329 : Sat.Clause := [.neg 154, .neg 158, .neg 162, .neg 172, .pos 304]
private def clause330 : Sat.Clause := [.neg 155, .neg 156, .neg 163, .neg 173, .pos 305]
private def clause331 : Sat.Clause := [.neg 155, .neg 157, .neg 164, .neg 174, .pos 306]
private def clause332 : Sat.Clause := [.neg 155, .neg 158, .neg 165, .neg 175, .pos 307]
private def clause333 : Sat.Clause := [.neg 28, .pos 30, .neg 50, .neg 156, .neg 157, .neg 166, .pos 176]
private def clause334 : Sat.Clause := [.neg 156, .neg 157, .pos 166, .pos 176, .pos 308]
private def clause335 : Sat.Clause := [.neg 156, .neg 158, .pos 167, .pos 177, .pos 309]
private def clause336 : Sat.Clause := [.neg 157, .neg 158, .pos 168, .pos 178, .pos 310]
private def clause337 : Sat.Clause := [.neg 159, .neg 160, .neg 163, .neg 187, .pos 311]
private def clause338 : Sat.Clause := [.neg 159, .neg 161, .neg 164, .neg 188, .pos 312]
private def clause339 : Sat.Clause := [.neg 159, .neg 162, .neg 165, .neg 189, .pos 313]
private def clause340 : Sat.Clause := [.neg 160, .neg 161, .pos 166, .pos 190, .pos 314]
private def clause341 : Sat.Clause := [.neg 160, .neg 162, .pos 167, .pos 191, .pos 315]
private def clause342 : Sat.Clause := [.neg 161, .neg 162, .pos 168, .pos 192, .pos 316]
private def clause343 : Sat.Clause := [.neg 163, .neg 164, .pos 166, .pos 193, .pos 317]
private def clause344 : Sat.Clause := [.neg 163, .neg 165, .pos 167, .pos 194, .pos 318]
private def clause345 : Sat.Clause := [.neg 164, .neg 165, .pos 168, .pos 195, .pos 319]
private def clause346 : Sat.Clause := [.pos 29, .neg 30, .neg 60, .neg 166, .pos 167, .pos 168, .pos 196]
private def clause347 : Sat.Clause := [.pos 166, .pos 167, .pos 168, .pos 196, .pos 320]
private def clause348 : Sat.Clause := [.neg 166, .pos 167, .pos 168, .pos 196, .neg 320]
private def clause349 : Sat.Clause := [.neg 169, .neg 170, .neg 173, .neg 187, .pos 321]
private def clause350 : Sat.Clause := [.neg 169, .neg 171, .neg 174, .neg 188, .pos 322]
private def clause351 : Sat.Clause := [.neg 169, .neg 172, .neg 175, .neg 189, .pos 323]
private def clause352 : Sat.Clause := [.neg 31, .pos 33, .neg 50, .neg 170, .neg 171, .neg 176, .pos 190]
private def clause353 : Sat.Clause := [.neg 170, .neg 171, .pos 176, .pos 190, .pos 324]
private def clause354 : Sat.Clause := [.neg 170, .neg 172, .pos 177, .pos 191, .pos 325]
private def clause355 : Sat.Clause := [.neg 171, .neg 172, .pos 178, .pos 192, .pos 326]
private def clause356 : Sat.Clause := [.neg 173, .neg 174, .pos 176, .pos 193, .pos 327]
private def clause357 : Sat.Clause := [.neg 173, .neg 175, .pos 177, .pos 194, .pos 328]
private def clause358 : Sat.Clause := [.neg 174, .neg 175, .pos 178, .pos 195, .pos 329]
private def clause359 : Sat.Clause := [.pos 176, .pos 177, .pos 178, .pos 196, .pos 330]
private def clause360 : Sat.Clause := [.neg 176, .pos 177, .pos 178, .pos 196, .neg 330]
private def clause361 : Sat.Clause := [.neg 35, .pos 41, .neg 43, .pos 179, .pos 180, .pos 183, .neg 186]
private def clause362 : Sat.Clause := [.pos 179, .pos 180, .neg 183, .neg 186, .pos 331]
private def clause363 : Sat.Clause := [.neg 34, .neg 47, .neg 50, .neg 181, .neg 182, .pos 183, .neg 193]
private def clause364 : Sat.Clause := [.neg 41, .pos 50, .neg 59, .pos 183, .pos 184, .pos 185, .pos 196]
private def clause365 : Sat.Clause := [.neg 44, .pos 46, .neg 50, .neg 187, .neg 188, .neg 190, .pos 193]
private def clause366 : Sat.Clause := [.neg 187, .neg 188, .pos 190, .pos 193, .pos 332]
private def clause367 : Sat.Clause := [.neg 187, .neg 189, .pos 191, .pos 194, .pos 333]
private def clause368 : Sat.Clause := [.neg 188, .neg 189, .pos 192, .pos 195, .pos 334]
private def clause369 : Sat.Clause := [.pos 190, .pos 191, .pos 192, .pos 196, .pos 335]
private def clause370 : Sat.Clause := [.neg 190, .pos 191, .pos 192, .pos 196, .neg 335]
private def clause371 : Sat.Clause := [.pos 48, .neg 49, .neg 50, .neg 193, .pos 194, .pos 195, .pos 196]
private def clause372 : Sat.Clause := [.pos 193, .pos 194, .pos 195, .pos 196, .pos 336]
private def clause373 : Sat.Clause := [.neg 193, .pos 194, .pos 195, .pos 196, .neg 336]
private def clause374 : Sat.Clause := [.neg 197, .neg 198, .neg 199, .neg 200, .neg 201, .neg 202, .neg 203, .neg 204, .neg 205, .neg 206, .neg 207, .neg 208, .neg 209, .neg 210, .neg 211, .neg 212, .neg 213, .neg 214, .neg 215, .neg 216, .neg 217, .neg 218, .neg 219, .neg 220, .neg 221, .neg 222, .neg 223, .neg 224, .neg 225, .neg 226, .neg 227, .neg 228, .neg 229, .neg 230, .neg 231, .neg 232, .neg 233, .neg 234, .neg 235, .neg 236, .neg 237, .neg 238, .neg 239, .neg 240, .neg 241, .neg 242, .neg 243, .neg 244, .neg 245, .neg 246, .neg 247, .neg 248, .neg 249, .neg 250, .neg 251, .neg 252, .neg 253, .neg 254, .neg 255, .neg 256, .neg 257, .neg 283, .neg 284, .neg 285, .neg 286, .neg 297, .neg 298, .neg 299, .neg 300, .neg 331]
private def clause375 : Sat.Clause := [.neg 258, .neg 259, .neg 260, .neg 261, .neg 262, .neg 263, .neg 264, .neg 265, .neg 266, .neg 267, .neg 268, .neg 269, .neg 270, .neg 271, .neg 272, .neg 273, .neg 274, .neg 275, .neg 276, .neg 277, .neg 278, .neg 279, .neg 280, .neg 281, .neg 282, .neg 287, .neg 288, .neg 289, .neg 290, .neg 291, .neg 292, .neg 293, .neg 294, .neg 295, .neg 296, .neg 301, .neg 302, .neg 303, .neg 304, .neg 305, .neg 306, .neg 307, .neg 308, .neg 309, .neg 310, .neg 311, .neg 312, .neg 313, .neg 314, .neg 315, .neg 316, .neg 317, .neg 318, .neg 319, .neg 320, .neg 321, .neg 322, .neg 323, .neg 324, .neg 325, .neg 326, .neg 327, .neg 328, .neg 329, .neg 330, .neg 332, .neg 333, .neg 334, .neg 335, .neg 336]

private def clauses : Sat.Fmla := [
  clause000, clause001, clause002, clause003, clause004, clause005, clause006, clause007, clause008, clause009, clause010, clause011, clause012, clause013, clause014, clause015, clause016, clause017, clause018, clause019, clause020, clause021, clause022, clause023, clause024, clause025, clause026, clause027, clause028, clause029, clause030, clause031, clause032, clause033, clause034, clause035, clause036, clause037, clause038, clause039, clause040, clause041, clause042, clause043, clause044, clause045, clause046, clause047, clause048, clause049, clause050, clause051, clause052, clause053, clause054, clause055, clause056, clause057, clause058, clause059, clause060, clause061, clause062, clause063, clause064, clause065, clause066, clause067, clause068, clause069, clause070, clause071, clause072, clause073, clause074, clause075, clause076, clause077, clause078, clause079, clause080, clause081, clause082, clause083, clause084, clause085, clause086, clause087, clause088, clause089, clause090, clause091, clause092, clause093, clause094, clause095, clause096, clause097, clause098, clause099, clause100, clause101, clause102, clause103, clause104, clause105, clause106, clause107, clause108, clause109, clause110, clause111, clause112, clause113, clause114, clause115, clause116, clause117, clause118, clause119, clause120, clause121, clause122, clause123, clause124, clause125, clause126, clause127, clause128, clause129, clause130, clause131, clause132, clause133, clause134, clause135, clause136, clause137, clause138, clause139, clause140, clause141, clause142, clause143, clause144, clause145, clause146, clause147, clause148, clause149, clause150, clause151, clause152, clause153, clause154, clause155, clause156, clause157, clause158, clause159, clause160, clause161, clause162, clause163, clause164, clause165, clause166, clause167, clause168, clause169, clause170, clause171, clause172, clause173, clause174, clause175, clause176, clause177, clause178, clause179, clause180, clause181, clause182, clause183, clause184, clause185, clause186, clause187, clause188, clause189, clause190, clause191, clause192, clause193, clause194, clause195, clause196, clause197, clause198, clause199, clause200, clause201, clause202, clause203, clause204, clause205, clause206, clause207, clause208, clause209, clause210, clause211, clause212, clause213, clause214, clause215, clause216, clause217, clause218, clause219, clause220, clause221, clause222, clause223, clause224, clause225, clause226, clause227, clause228, clause229, clause230, clause231, clause232, clause233, clause234, clause235, clause236, clause237, clause238, clause239, clause240, clause241, clause242, clause243, clause244, clause245, clause246, clause247, clause248, clause249, clause250, clause251, clause252, clause253, clause254, clause255, clause256, clause257, clause258, clause259, clause260, clause261, clause262, clause263, clause264, clause265, clause266, clause267, clause268, clause269, clause270, clause271, clause272, clause273, clause274, clause275, clause276, clause277, clause278, clause279, clause280, clause281, clause282, clause283, clause284, clause285, clause286, clause287, clause288, clause289, clause290, clause291, clause292, clause293, clause294, clause295, clause296, clause297, clause298, clause299, clause300, clause301, clause302, clause303, clause304, clause305, clause306, clause307, clause308, clause309, clause310, clause311, clause312, clause313, clause314, clause315, clause316, clause317, clause318, clause319, clause320, clause321, clause322, clause323, clause324, clause325, clause326, clause327, clause328, clause329, clause330, clause331, clause332, clause333, clause334, clause335, clause336, clause337, clause338, clause339, clause340, clause341, clause342, clause343, clause344, clause345, clause346, clause347, clause348, clause349, clause350, clause351, clause352, clause353, clause354, clause355, clause356, clause357, clause358, clause359, clause360, clause361, clause362, clause363, clause364, clause365, clause366, clause367, clause368, clause369, clause370, clause371, clause372, clause373, clause374, clause375]

private theorem formula_eq : cnf_refutation.formula = clauses := by rfl

variable {n : ℕ} {σ : Fin 13 → Fin 154} (C : Context 13 n σ) (compatible : Compatible σ)
include compatible

-- Clause 1: empty_direction; source clause 29.
private theorem sound000 : C.clause (decodeClause atoms clause000) := by
  exact C.covered_clause _ _ (C.empty_clause 1 0 (by decide) (compatible.1 (1, 0) (by decide +kernel))) (by decide +kernel)

-- Clause 2: empty_direction; source clause 81.
private theorem sound001 : C.clause (decodeClause atoms clause001) := by
  exact C.covered_clause _ _ (C.empty_clause 2 0 (by decide) (compatible.1 (2, 0) (by decide +kernel))) (by decide +kernel)

-- Clause 3: empty_direction; source clause 132.
private theorem sound002 : C.clause (decodeClause atoms clause002) := by
  exact C.covered_clause _ _ (C.empty_clause 3 0 (by decide) (compatible.1 (3, 0) (by decide +kernel))) (by decide +kernel)

-- Clause 4: empty_direction; source clause 280.
private theorem sound003 : C.clause (decodeClause atoms clause003) := by
  exact C.covered_clause _ _ (C.empty_clause 6 0 (by decide) (compatible.1 (6, 0) (by decide +kernel))) (by decide +kernel)

-- Clause 5: empty_direction; source clause 330.
private theorem sound004 : C.clause (decodeClause atoms clause004) := by
  exact C.covered_clause _ _ (C.empty_clause 7 0 (by decide) (compatible.1 (7, 0) (by decide +kernel))) (by decide +kernel)

-- Clause 6: empty_direction; source clause 521.
private theorem sound005 : C.clause (decodeClause atoms clause005) := by
  exact C.covered_clause _ _ (C.empty_clause 11 0 (by decide) (compatible.1 (11, 0) (by decide +kernel))) (by decide +kernel)

-- Clause 7: empty_direction; source clause 621.
private theorem sound006 : C.clause (decodeClause atoms clause006) := by
  exact C.covered_clause _ _ (C.empty_clause 2 1 (by decide) (compatible.1 (2, 1) (by decide +kernel))) (by decide +kernel)

-- Clause 8: empty_direction; source clause 674.
private theorem sound007 : C.clause (decodeClause atoms clause007) := by
  exact C.covered_clause _ _ (C.empty_clause 3 1 (by decide) (compatible.1 (3, 1) (by decide +kernel))) (by decide +kernel)

-- Clause 9: empty_direction; source clause 726.
private theorem sound008 : C.clause (decodeClause atoms clause008) := by
  exact C.covered_clause _ _ (C.empty_clause 4 1 (by decide) (compatible.1 (4, 1) (by decide +kernel))) (by decide +kernel)

-- Clause 10: empty_direction; source clause 828.
private theorem sound009 : C.clause (decodeClause atoms clause009) := by
  exact C.covered_clause _ _ (C.empty_clause 6 1 (by decide) (compatible.1 (6, 1) (by decide +kernel))) (by decide +kernel)

-- Clause 11: empty_direction; source clause 1024.
private theorem sound010 : C.clause (decodeClause atoms clause010) := by
  exact C.covered_clause _ _ (C.empty_clause 10 1 (by decide) (compatible.1 (10, 1) (by decide +kernel))) (by decide +kernel)

-- Clause 12: empty_direction; source clause 1173.
private theorem sound011 : C.clause (decodeClause atoms clause011) := by
  exact C.covered_clause _ _ (C.empty_clause 3 2 (by decide) (compatible.1 (3, 2) (by decide +kernel))) (by decide +kernel)

-- Clause 13: empty_direction; source clause 1226.
private theorem sound012 : C.clause (decodeClause atoms clause012) := by
  exact C.covered_clause _ _ (C.empty_clause 4 2 (by decide) (compatible.1 (4, 2) (by decide +kernel))) (by decide +kernel)

-- Clause 14: empty_direction; source clause 1330.
private theorem sound013 : C.clause (decodeClause atoms clause013) := by
  exact C.covered_clause _ _ (C.empty_clause 6 2 (by decide) (compatible.1 (6, 2) (by decide +kernel))) (by decide +kernel)

-- Clause 15: empty_direction; source clause 1530.
private theorem sound014 : C.clause (decodeClause atoms clause014) := by
  exact C.covered_clause _ _ (C.empty_clause 10 2 (by decide) (compatible.1 (10, 2) (by decide +kernel))) (by decide +kernel)

-- Clause 16: empty_direction; source clause 1731.
private theorem sound015 : C.clause (decodeClause atoms clause015) := by
  exact C.covered_clause _ _ (C.empty_clause 5 3 (by decide) (compatible.1 (5, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 17: empty_direction; source clause 1784.
private theorem sound016 : C.clause (decodeClause atoms clause016) := by
  exact C.covered_clause _ _ (C.empty_clause 6 3 (by decide) (compatible.1 (6, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 18: empty_direction; source clause 1885.
private theorem sound017 : C.clause (decodeClause atoms clause017) := by
  exact C.covered_clause _ _ (C.empty_clause 8 3 (by decide) (compatible.1 (8, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 19: empty_direction; source clause 1988.
private theorem sound018 : C.clause (decodeClause atoms clause018) := by
  exact C.covered_clause _ _ (C.empty_clause 10 3 (by decide) (compatible.1 (10, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 20: empty_direction; source clause 2141.
private theorem sound019 : C.clause (decodeClause atoms clause019) := by
  exact C.covered_clause _ _ (C.empty_clause 5 4 (by decide) (compatible.1 (5, 4) (by decide +kernel))) (by decide +kernel)

-- Clause 21: empty_direction; source clause 2639.
private theorem sound020 : C.clause (decodeClause atoms clause020) := by
  exact C.covered_clause _ _ (C.empty_clause 8 5 (by decide) (compatible.1 (8, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 22: empty_direction; source clause 2997.
private theorem sound021 : C.clause (decodeClause atoms clause021) := by
  exact C.covered_clause _ _ (C.empty_clause 9 6 (by decide) (compatible.1 (9, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 23: domain; source clause 3032.
private theorem sound022 : C.clause (decodeClause atoms clause022) := by
  exact C.covered_clause _ _ (C.domain_clause 6 10 (by decide) 1 5 (compatible.2.1 (6, 10, 1, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 24: domain; source clause 3038.
private theorem sound023 : C.clause (decodeClause atoms clause023) := by
  exact C.covered_clause _ _ (C.domain_clause 6 10 (by decide) 2 5 (compatible.2.1 (6, 10, 2, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 25: domain; source clause 3043.
private theorem sound024 : C.clause (decodeClause atoms clause024) := by
  exact C.covered_clause _ _ (C.domain_clause 6 10 (by decide) 3 5 (compatible.2.1 (6, 10, 3, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 26: empty_direction; source clause 3051.
private theorem sound025 : C.clause (decodeClause atoms clause025) := by
  exact C.covered_clause _ _ (C.empty_clause 10 6 (by decide) (compatible.1 (10, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 27: empty_direction; source clause 3304.
private theorem sound026 : C.clause (decodeClause atoms clause026) := by
  exact C.covered_clause _ _ (C.empty_clause 10 7 (by decide) (compatible.1 (10, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 28: empty_direction; source clause 3357.
private theorem sound027 : C.clause (decodeClause atoms clause027) := by
  exact C.covered_clause _ _ (C.empty_clause 11 7 (by decide) (compatible.1 (11, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 29: empty_direction; source clause 3462.
private theorem sound028 : C.clause (decodeClause atoms clause028) := by
  exact C.covered_clause _ _ (C.empty_clause 9 8 (by decide) (compatible.1 (9, 8) (by decide +kernel))) (by decide +kernel)

-- Clause 30: empty_direction; source clause 3771.
private theorem sound029 : C.clause (decodeClause atoms clause029) := by
  exact C.covered_clause _ _ (C.empty_clause 12 9 (by decide) (compatible.1 (12, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 31: domain; source clause 3809.
private theorem sound030 : C.clause (decodeClause atoms clause030) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 2 2 (compatible.2.1 (10, 11, 2, 2) (by decide +kernel))) (by decide +kernel)

-- Clause 32: domain; source clause 3810.
private theorem sound031 : C.clause (decodeClause atoms clause031) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 2 3 (compatible.2.1 (10, 11, 2, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 33: domain; source clause 3811.
private theorem sound032 : C.clause (decodeClause atoms clause032) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 2 4 (compatible.2.1 (10, 11, 2, 4) (by decide +kernel))) (by decide +kernel)

-- Clause 34: domain; source clause 3812.
private theorem sound033 : C.clause (decodeClause atoms clause033) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 2 5 (compatible.2.1 (10, 11, 2, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 35: domain; source clause 3813.
private theorem sound034 : C.clause (decodeClause atoms clause034) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 2 6 (compatible.2.1 (10, 11, 2, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 36: domain; source clause 3815.
private theorem sound035 : C.clause (decodeClause atoms clause035) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 3 3 (compatible.2.1 (10, 11, 3, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 37: domain; source clause 3816.
private theorem sound036 : C.clause (decodeClause atoms clause036) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 3 4 (compatible.2.1 (10, 11, 3, 4) (by decide +kernel))) (by decide +kernel)

-- Clause 38: domain; source clause 3817.
private theorem sound037 : C.clause (decodeClause atoms clause037) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 3 5 (compatible.2.1 (10, 11, 3, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 39: domain; source clause 3818.
private theorem sound038 : C.clause (decodeClause atoms clause038) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 3 6 (compatible.2.1 (10, 11, 3, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 40: empty_direction; source clause 3876.
private theorem sound039 : C.clause (decodeClause atoms clause039) := by
  exact C.covered_clause _ _ (C.empty_clause 12 10 (by decide) (compatible.1 (12, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 41: empty_direction; source clause 3929.
private theorem sound040 : C.clause (decodeClause atoms clause040) := by
  exact C.covered_clause _ _ (C.empty_clause 12 11 (by decide) (compatible.1 (12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 42: growth; source clause 3959.
omit compatible in
private theorem sound041 : C.clause (decodeClause atoms clause041) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 1 2 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 43: growth; source clause 4047.
omit compatible in
private theorem sound042 : C.clause (decodeClause atoms clause042) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 1 10 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 44: growth; source clause 5544.
omit compatible in
private theorem sound043 : C.clause (decodeClause atoms clause043) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 2 3 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 45: growth; source clause 5621.
omit compatible in
private theorem sound044 : C.clause (decodeClause atoms clause044) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 2 10 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 46: growth; source clause 6600.
omit compatible in
private theorem sound045 : C.clause (decodeClause atoms clause045) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 10 11 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 47: growth; source clause 7151.
omit compatible in
private theorem sound046 : C.clause (decodeClause atoms clause046) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 3 6 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 48: growth; source clause 7195.
omit compatible in
private theorem sound047 : C.clause (decodeClause atoms clause047) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 3 10 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 49: order_transitive; source clause 7562.
omit compatible in
private theorem sound048 : C.clause (decodeClause atoms clause048) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 6 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 50: growth; source clause 8053.
omit compatible in
private theorem sound049 : C.clause (decodeClause atoms clause049) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 10 11 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 51: growth; source clause 9011.
omit compatible in
private theorem sound050 : C.clause (decodeClause atoms clause050) := by
  exact C.covered_clause _ _ (C.growth_clause true 3 6 10 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 52: order_transitive; source clause 9014.
omit compatible in
private theorem sound051 : C.clause (decodeClause atoms clause051) := by
  exact C.covered_clause _ _ (C.transitive_clause 3 6 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 53: growth; source clause 9506.
omit compatible in
private theorem sound052 : C.clause (decodeClause atoms clause052) := by
  exact C.covered_clause _ _ (C.growth_clause true 3 10 11 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 54: growth; source clause 13855.
omit compatible in
private theorem sound053 : C.clause (decodeClause atoms clause053) := by
  exact C.covered_clause _ _ (C.growth_clause false 6 10 11 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 55: growth; source clause 13864.
omit compatible in
private theorem sound054 : C.clause (decodeClause atoms clause054) := by
  exact C.covered_clause _ _ (C.growth_clause true 6 10 11 (by decide) (by decide) (by decide) 6) (by decide +kernel)

-- Clause 56: growth; source clause 13869.
omit compatible in
private theorem sound055 : C.clause (decodeClause atoms clause055) := by
  exact C.covered_clause _ _ (C.growth_clause false 6 10 12 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 57: growth; source clause 15311.
omit compatible in
private theorem sound056 : C.clause (decodeClause atoms clause056) := by
  exact C.covered_clause _ _ (C.growth_clause true 7 10 11 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 58: growth; source clause 19798.
omit compatible in
private theorem sound057 : C.clause (decodeClause atoms clause057) := by
  exact C.covered_clause _ _ (C.growth_clause false 10 11 12 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 59: fixed_sign; source clause 22830.
private theorem sound058 : C.clause (decodeClause atoms clause058) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 2 (by decide) (by decide) (by decide) (compatible.2.2 (0, 1, 2) (by decide +kernel))) (by decide +kernel)

-- Clause 60: fixed_sign; source clause 22831.
private theorem sound059 : C.clause (decodeClause atoms clause059) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 3 (by decide) (by decide) (by decide) (compatible.2.2 (0, 1, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 61: fixed_sign; source clause 22832.
private theorem sound060 : C.clause (decodeClause atoms clause060) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 6 (by decide) (by decide) (by decide) (compatible.2.2 (0, 1, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 62: fixed_sign; source clause 22833.
private theorem sound061 : C.clause (decodeClause atoms clause061) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 7 (by decide) (by decide) (by decide) (compatible.2.2 (0, 1, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 63: fixed_sign; source clause 22834.
private theorem sound062 : C.clause (decodeClause atoms clause062) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 10 (by decide) (by decide) (by decide) (compatible.2.2 (0, 1, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 64: fixed_sign; source clause 22835.
private theorem sound063 : C.clause (decodeClause atoms clause063) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 11 (by decide) (by decide) (by decide) (compatible.2.2 (0, 1, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 65: fixed_sign; source clause 22836.
private theorem sound064 : C.clause (decodeClause atoms clause064) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 3 (by decide) (by decide) (by decide) (compatible.2.2 (0, 2, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 66: fixed_sign; source clause 22837.
private theorem sound065 : C.clause (decodeClause atoms clause065) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 6 (by decide) (by decide) (by decide) (compatible.2.2 (0, 2, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 67: fixed_sign; source clause 22838.
private theorem sound066 : C.clause (decodeClause atoms clause066) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 7 (by decide) (by decide) (by decide) (compatible.2.2 (0, 2, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 68: fixed_sign; source clause 22839.
private theorem sound067 : C.clause (decodeClause atoms clause067) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 10 (by decide) (by decide) (by decide) (compatible.2.2 (0, 2, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 69: fixed_sign; source clause 22840.
private theorem sound068 : C.clause (decodeClause atoms clause068) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 3 6 (by decide) (by decide) (by decide) (compatible.2.2 (0, 3, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 70: fixed_sign; source clause 22841.
private theorem sound069 : C.clause (decodeClause atoms clause069) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 3 7 (by decide) (by decide) (by decide) (compatible.2.2 (0, 3, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 71: fixed_sign; source clause 22842.
private theorem sound070 : C.clause (decodeClause atoms clause070) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 3 10 (by decide) (by decide) (by decide) (compatible.2.2 (0, 3, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 72: fixed_sign; source clause 22852.
private theorem sound071 : C.clause (decodeClause atoms clause071) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 6 7 (by decide) (by decide) (by decide) (compatible.2.2 (0, 6, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 73: fixed_sign; source clause 22853.
private theorem sound072 : C.clause (decodeClause atoms clause072) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 6 10 (by decide) (by decide) (by decide) (compatible.2.2 (0, 6, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 74: fixed_sign; source clause 22856.
private theorem sound073 : C.clause (decodeClause atoms clause073) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 7 10 (by decide) (by decide) (by decide) (compatible.2.2 (0, 10, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 75: fixed_sign; source clause 22857.
private theorem sound074 : C.clause (decodeClause atoms clause074) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 7 11 (by decide) (by decide) (by decide) (compatible.2.2 (0, 11, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 76: fixed_sign; source clause 22862.
private theorem sound075 : C.clause (decodeClause atoms clause075) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 3 (by decide) (by decide) (by decide) (compatible.2.2 (1, 2, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 77: fixed_sign; source clause 22863.
private theorem sound076 : C.clause (decodeClause atoms clause076) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 2 4 (by decide) (by decide) (by decide) (compatible.2.2 (1, 4, 2) (by decide +kernel))) (by decide +kernel)

-- Clause 78: fixed_sign; source clause 22864.
private theorem sound077 : C.clause (decodeClause atoms clause077) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 6 (by decide) (by decide) (by decide) (compatible.2.2 (1, 2, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 79: fixed_sign; source clause 22865.
private theorem sound078 : C.clause (decodeClause atoms clause078) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 7 (by decide) (by decide) (by decide) (compatible.2.2 (1, 2, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 80: fixed_sign; source clause 22866.
private theorem sound079 : C.clause (decodeClause atoms clause079) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 10 (by decide) (by decide) (by decide) (compatible.2.2 (1, 2, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 81: fixed_sign; source clause 22868.
private theorem sound080 : C.clause (decodeClause atoms clause080) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 3 5 (by decide) (by decide) (by decide) (compatible.2.2 (1, 5, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 82: fixed_sign; source clause 22869.
private theorem sound081 : C.clause (decodeClause atoms clause081) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 3 6 (by decide) (by decide) (by decide) (compatible.2.2 (1, 3, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 83: fixed_sign; source clause 22870.
private theorem sound082 : C.clause (decodeClause atoms clause082) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 3 7 (by decide) (by decide) (by decide) (compatible.2.2 (1, 3, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 84: fixed_sign; source clause 22871.
private theorem sound083 : C.clause (decodeClause atoms clause083) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 3 10 (by decide) (by decide) (by decide) (compatible.2.2 (1, 3, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 85: fixed_sign; source clause 22876.
private theorem sound084 : C.clause (decodeClause atoms clause084) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 10 (by decide) (by decide) (by decide) (compatible.2.2 (1, 4, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 86: fixed_sign; source clause 22877.
private theorem sound085 : C.clause (decodeClause atoms clause085) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 11 (by decide) (by decide) (by decide) (compatible.2.2 (1, 4, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 87: fixed_sign; source clause 22882.
private theorem sound086 : C.clause (decodeClause atoms clause086) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 5 10 (by decide) (by decide) (by decide) (compatible.2.2 (1, 5, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 88: fixed_sign; source clause 22883.
private theorem sound087 : C.clause (decodeClause atoms clause087) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 5 11 (by decide) (by decide) (by decide) (compatible.2.2 (1, 5, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 89: fixed_sign; source clause 22885.
private theorem sound088 : C.clause (decodeClause atoms clause088) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 7 (by decide) (by decide) (by decide) (compatible.2.2 (1, 6, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 90: fixed_sign; source clause 22887.
private theorem sound089 : C.clause (decodeClause atoms clause089) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 6 9 (by decide) (by decide) (by decide) (compatible.2.2 (1, 9, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 91: fixed_sign; source clause 22888.
private theorem sound090 : C.clause (decodeClause atoms clause090) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 10 (by decide) (by decide) (by decide) (compatible.2.2 (1, 6, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 92: fixed_sign; source clause 22889.
private theorem sound091 : C.clause (decodeClause atoms clause091) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 7 10 (by decide) (by decide) (by decide) (compatible.2.2 (1, 10, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 93: fixed_sign; source clause 22890.
private theorem sound092 : C.clause (decodeClause atoms clause092) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 7 11 (by decide) (by decide) (by decide) (compatible.2.2 (1, 11, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 94: fixed_sign; source clause 22896.
private theorem sound093 : C.clause (decodeClause atoms clause093) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 9 11 (by decide) (by decide) (by decide) (compatible.2.2 (1, 9, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 95: fixed_sign; source clause 22898.
private theorem sound094 : C.clause (decodeClause atoms clause094) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 10 12 (by decide) (by decide) (by decide) (compatible.2.2 (1, 12, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 96: fixed_sign; source clause 22899.
private theorem sound095 : C.clause (decodeClause atoms clause095) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 11 12 (by decide) (by decide) (by decide) (compatible.2.2 (1, 12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 97: fixed_sign; source clause 22901.
private theorem sound096 : C.clause (decodeClause atoms clause096) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 3 5 (by decide) (by decide) (by decide) (compatible.2.2 (2, 5, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 98: fixed_sign; source clause 22902.
private theorem sound097 : C.clause (decodeClause atoms clause097) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 3 6 (by decide) (by decide) (by decide) (compatible.2.2 (2, 3, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 99: fixed_sign; source clause 22903.
private theorem sound098 : C.clause (decodeClause atoms clause098) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 3 7 (by decide) (by decide) (by decide) (compatible.2.2 (2, 3, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 100: fixed_sign; source clause 22904.
private theorem sound099 : C.clause (decodeClause atoms clause099) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 3 10 (by decide) (by decide) (by decide) (compatible.2.2 (2, 3, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 101: fixed_sign; source clause 22905.
private theorem sound100 : C.clause (decodeClause atoms clause100) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 5 (by decide) (by decide) (by decide) (compatible.2.2 (2, 4, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 102: fixed_sign; source clause 22907.
private theorem sound101 : C.clause (decodeClause atoms clause101) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 8 (by decide) (by decide) (by decide) (compatible.2.2 (2, 4, 8) (by decide +kernel))) (by decide +kernel)

-- Clause 103: fixed_sign; source clause 22908.
private theorem sound102 : C.clause (decodeClause atoms clause102) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 9 (by decide) (by decide) (by decide) (compatible.2.2 (2, 4, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 104: fixed_sign; source clause 22909.
private theorem sound103 : C.clause (decodeClause atoms clause103) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 10 (by decide) (by decide) (by decide) (compatible.2.2 (2, 4, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 105: fixed_sign; source clause 22910.
private theorem sound104 : C.clause (decodeClause atoms clause104) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 11 (by decide) (by decide) (by decide) (compatible.2.2 (2, 4, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 106: fixed_sign; source clause 22911.
private theorem sound105 : C.clause (decodeClause atoms clause105) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 12 (by decide) (by decide) (by decide) (compatible.2.2 (2, 4, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 107: fixed_sign; source clause 22913.
private theorem sound106 : C.clause (decodeClause atoms clause106) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 5 8 (by decide) (by decide) (by decide) (compatible.2.2 (2, 5, 8) (by decide +kernel))) (by decide +kernel)

-- Clause 108: fixed_sign; source clause 22914.
private theorem sound107 : C.clause (decodeClause atoms clause107) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 5 9 (by decide) (by decide) (by decide) (compatible.2.2 (2, 5, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 109: fixed_sign; source clause 22915.
private theorem sound108 : C.clause (decodeClause atoms clause108) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 5 10 (by decide) (by decide) (by decide) (compatible.2.2 (2, 5, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 110: fixed_sign; source clause 22916.
private theorem sound109 : C.clause (decodeClause atoms clause109) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 5 11 (by decide) (by decide) (by decide) (compatible.2.2 (2, 5, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 111: fixed_sign; source clause 22917.
private theorem sound110 : C.clause (decodeClause atoms clause110) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 5 12 (by decide) (by decide) (by decide) (compatible.2.2 (2, 5, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 112: fixed_sign; source clause 22918.
private theorem sound111 : C.clause (decodeClause atoms clause111) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 6 7 (by decide) (by decide) (by decide) (compatible.2.2 (2, 6, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 113: fixed_sign; source clause 22920.
private theorem sound112 : C.clause (decodeClause atoms clause112) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 6 9 (by decide) (by decide) (by decide) (compatible.2.2 (2, 9, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 114: fixed_sign; source clause 22921.
private theorem sound113 : C.clause (decodeClause atoms clause113) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 6 10 (by decide) (by decide) (by decide) (compatible.2.2 (2, 6, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 115: fixed_sign; source clause 22922.
private theorem sound114 : C.clause (decodeClause atoms clause114) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 7 10 (by decide) (by decide) (by decide) (compatible.2.2 (2, 10, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 116: fixed_sign; source clause 22923.
private theorem sound115 : C.clause (decodeClause atoms clause115) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 7 11 (by decide) (by decide) (by decide) (compatible.2.2 (2, 11, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 117: fixed_sign; source clause 22924.
private theorem sound116 : C.clause (decodeClause atoms clause116) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 8 9 (by decide) (by decide) (by decide) (compatible.2.2 (2, 8, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 118: fixed_sign; source clause 22925.
private theorem sound117 : C.clause (decodeClause atoms clause117) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 8 10 (by decide) (by decide) (by decide) (compatible.2.2 (2, 8, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 119: fixed_sign; source clause 22926.
private theorem sound118 : C.clause (decodeClause atoms clause118) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 8 11 (by decide) (by decide) (by decide) (compatible.2.2 (2, 8, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 120: fixed_sign; source clause 22927.
private theorem sound119 : C.clause (decodeClause atoms clause119) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 8 12 (by decide) (by decide) (by decide) (compatible.2.2 (2, 8, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 121: fixed_sign; source clause 22928.
private theorem sound120 : C.clause (decodeClause atoms clause120) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 9 10 (by decide) (by decide) (by decide) (compatible.2.2 (2, 9, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 122: fixed_sign; source clause 22929.
private theorem sound121 : C.clause (decodeClause atoms clause121) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 9 11 (by decide) (by decide) (by decide) (compatible.2.2 (2, 9, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 123: fixed_sign; source clause 22930.
private theorem sound122 : C.clause (decodeClause atoms clause122) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 9 12 (by decide) (by decide) (by decide) (compatible.2.2 (2, 9, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 124: fixed_sign; source clause 22931.
private theorem sound123 : C.clause (decodeClause atoms clause123) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 10 12 (by decide) (by decide) (by decide) (compatible.2.2 (2, 12, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 125: fixed_sign; source clause 22932.
private theorem sound124 : C.clause (decodeClause atoms clause124) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 11 12 (by decide) (by decide) (by decide) (compatible.2.2 (2, 12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 126: fixed_sign; source clause 22937.
private theorem sound125 : C.clause (decodeClause atoms clause125) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 10 (by decide) (by decide) (by decide) (compatible.2.2 (3, 5, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 127: fixed_sign; source clause 22938.
private theorem sound126 : C.clause (decodeClause atoms clause126) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 11 (by decide) (by decide) (by decide) (compatible.2.2 (3, 5, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 128: fixed_sign; source clause 22940.
private theorem sound127 : C.clause (decodeClause atoms clause127) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 6 7 (by decide) (by decide) (by decide) (compatible.2.2 (3, 6, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 129: fixed_sign; source clause 22942.
private theorem sound128 : C.clause (decodeClause atoms clause128) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 6 9 (by decide) (by decide) (by decide) (compatible.2.2 (3, 9, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 130: fixed_sign; source clause 22943.
private theorem sound129 : C.clause (decodeClause atoms clause129) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 6 10 (by decide) (by decide) (by decide) (compatible.2.2 (3, 6, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 131: fixed_sign; source clause 22944.
private theorem sound130 : C.clause (decodeClause atoms clause130) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 7 10 (by decide) (by decide) (by decide) (compatible.2.2 (3, 10, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 132: fixed_sign; source clause 22945.
private theorem sound131 : C.clause (decodeClause atoms clause131) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 7 11 (by decide) (by decide) (by decide) (compatible.2.2 (3, 11, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 133: fixed_sign; source clause 22947.
private theorem sound132 : C.clause (decodeClause atoms clause132) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 8 10 (by decide) (by decide) (by decide) (compatible.2.2 (3, 8, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 134: fixed_sign; source clause 22948.
private theorem sound133 : C.clause (decodeClause atoms clause133) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 8 11 (by decide) (by decide) (by decide) (compatible.2.2 (3, 8, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 135: fixed_sign; source clause 22950.
private theorem sound134 : C.clause (decodeClause atoms clause134) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 9 10 (by decide) (by decide) (by decide) (compatible.2.2 (3, 9, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 136: fixed_sign; source clause 22951.
private theorem sound135 : C.clause (decodeClause atoms clause135) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 9 11 (by decide) (by decide) (by decide) (compatible.2.2 (3, 9, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 137: fixed_sign; source clause 22953.
private theorem sound136 : C.clause (decodeClause atoms clause136) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 10 12 (by decide) (by decide) (by decide) (compatible.2.2 (3, 12, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 138: fixed_sign; source clause 22954.
private theorem sound137 : C.clause (decodeClause atoms clause137) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 11 12 (by decide) (by decide) (by decide) (compatible.2.2 (3, 12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 139: fixed_sign; source clause 22957.
private theorem sound138 : C.clause (decodeClause atoms clause138) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 5 8 (by decide) (by decide) (by decide) (compatible.2.2 (4, 5, 8) (by decide +kernel))) (by decide +kernel)

-- Clause 140: fixed_sign; source clause 22958.
private theorem sound139 : C.clause (decodeClause atoms clause139) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 5 9 (by decide) (by decide) (by decide) (compatible.2.2 (4, 5, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 141: fixed_sign; source clause 22959.
private theorem sound140 : C.clause (decodeClause atoms clause140) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 5 10 (by decide) (by decide) (by decide) (compatible.2.2 (4, 5, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 142: fixed_sign; source clause 22960.
private theorem sound141 : C.clause (decodeClause atoms clause141) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 5 11 (by decide) (by decide) (by decide) (compatible.2.2 (4, 5, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 143: fixed_sign; source clause 22961.
private theorem sound142 : C.clause (decodeClause atoms clause142) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 5 12 (by decide) (by decide) (by decide) (compatible.2.2 (4, 5, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 144: fixed_sign; source clause 22967.
private theorem sound143 : C.clause (decodeClause atoms clause143) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 8 9 (by decide) (by decide) (by decide) (compatible.2.2 (4, 8, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 145: fixed_sign; source clause 22968.
private theorem sound144 : C.clause (decodeClause atoms clause144) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 8 10 (by decide) (by decide) (by decide) (compatible.2.2 (4, 8, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 146: fixed_sign; source clause 22969.
private theorem sound145 : C.clause (decodeClause atoms clause145) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 8 11 (by decide) (by decide) (by decide) (compatible.2.2 (4, 8, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 147: fixed_sign; source clause 22970.
private theorem sound146 : C.clause (decodeClause atoms clause146) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 8 12 (by decide) (by decide) (by decide) (compatible.2.2 (4, 8, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 148: fixed_sign; source clause 22971.
private theorem sound147 : C.clause (decodeClause atoms clause147) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 9 10 (by decide) (by decide) (by decide) (compatible.2.2 (4, 9, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 149: fixed_sign; source clause 22972.
private theorem sound148 : C.clause (decodeClause atoms clause148) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 9 11 (by decide) (by decide) (by decide) (compatible.2.2 (4, 9, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 150: fixed_sign; source clause 22973.
private theorem sound149 : C.clause (decodeClause atoms clause149) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 9 12 (by decide) (by decide) (by decide) (compatible.2.2 (4, 9, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 151: fixed_sign; source clause 22974.
private theorem sound150 : C.clause (decodeClause atoms clause150) := by
  exact C.covered_clause _ _ (C.fixed_negative 4 10 12 (by decide) (by decide) (by decide) (compatible.2.2 (4, 12, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 152: fixed_sign; source clause 22975.
private theorem sound151 : C.clause (decodeClause atoms clause151) := by
  exact C.covered_clause _ _ (C.fixed_negative 4 11 12 (by decide) (by decide) (by decide) (compatible.2.2 (4, 12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 153: fixed_sign; source clause 22981.
private theorem sound152 : C.clause (decodeClause atoms clause152) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 8 9 (by decide) (by decide) (by decide) (compatible.2.2 (5, 8, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 154: fixed_sign; source clause 22982.
private theorem sound153 : C.clause (decodeClause atoms clause153) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 8 10 (by decide) (by decide) (by decide) (compatible.2.2 (5, 8, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 155: fixed_sign; source clause 22983.
private theorem sound154 : C.clause (decodeClause atoms clause154) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 8 11 (by decide) (by decide) (by decide) (compatible.2.2 (5, 8, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 156: fixed_sign; source clause 22984.
private theorem sound155 : C.clause (decodeClause atoms clause155) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 8 12 (by decide) (by decide) (by decide) (compatible.2.2 (5, 8, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 157: fixed_sign; source clause 22985.
private theorem sound156 : C.clause (decodeClause atoms clause156) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 9 10 (by decide) (by decide) (by decide) (compatible.2.2 (5, 9, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 158: fixed_sign; source clause 22986.
private theorem sound157 : C.clause (decodeClause atoms clause157) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 9 11 (by decide) (by decide) (by decide) (compatible.2.2 (5, 9, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 159: fixed_sign; source clause 22987.
private theorem sound158 : C.clause (decodeClause atoms clause158) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 9 12 (by decide) (by decide) (by decide) (compatible.2.2 (5, 9, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 160: fixed_sign; source clause 22988.
private theorem sound159 : C.clause (decodeClause atoms clause159) := by
  exact C.covered_clause _ _ (C.fixed_negative 5 10 12 (by decide) (by decide) (by decide) (compatible.2.2 (5, 12, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 161: fixed_sign; source clause 22989.
private theorem sound160 : C.clause (decodeClause atoms clause160) := by
  exact C.covered_clause _ _ (C.fixed_negative 5 11 12 (by decide) (by decide) (by decide) (compatible.2.2 (5, 12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 162: fixed_sign; source clause 22990.
private theorem sound161 : C.clause (decodeClause atoms clause161) := by
  exact C.covered_clause _ _ (C.fixed_negative 6 7 10 (by decide) (by decide) (by decide) (compatible.2.2 (6, 10, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 163: fixed_sign; source clause 22991.
private theorem sound162 : C.clause (decodeClause atoms clause162) := by
  exact C.covered_clause _ _ (C.fixed_negative 6 7 11 (by decide) (by decide) (by decide) (compatible.2.2 (6, 11, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 164: fixed_sign; source clause 22993.
private theorem sound163 : C.clause (decodeClause atoms clause163) := by
  exact C.covered_clause _ _ (C.fixed_positive 6 9 10 (by decide) (by decide) (by decide) (compatible.2.2 (6, 9, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 165: fixed_sign; source clause 22994.
private theorem sound164 : C.clause (decodeClause atoms clause164) := by
  exact C.covered_clause _ _ (C.fixed_positive 6 9 11 (by decide) (by decide) (by decide) (compatible.2.2 (6, 9, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 166: fixed_sign; source clause 22996.
private theorem sound165 : C.clause (decodeClause atoms clause165) := by
  exact C.covered_clause _ _ (C.fixed_negative 6 10 12 (by decide) (by decide) (by decide) (compatible.2.2 (6, 12, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 167: fixed_sign; source clause 22997.
private theorem sound166 : C.clause (decodeClause atoms clause166) := by
  exact C.covered_clause _ _ (C.fixed_negative 6 11 12 (by decide) (by decide) (by decide) (compatible.2.2 (6, 12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 168: fixed_sign; source clause 23001.
private theorem sound167 : C.clause (decodeClause atoms clause167) := by
  exact C.covered_clause _ _ (C.fixed_positive 7 10 11 (by decide) (by decide) (by decide) (compatible.2.2 (7, 10, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 169: fixed_sign; source clause 23002.
private theorem sound168 : C.clause (decodeClause atoms clause168) := by
  exact C.covered_clause _ _ (C.fixed_positive 8 9 10 (by decide) (by decide) (by decide) (compatible.2.2 (8, 9, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 170: fixed_sign; source clause 23003.
private theorem sound169 : C.clause (decodeClause atoms clause169) := by
  exact C.covered_clause _ _ (C.fixed_positive 8 9 11 (by decide) (by decide) (by decide) (compatible.2.2 (8, 9, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 171: fixed_sign; source clause 23004.
private theorem sound170 : C.clause (decodeClause atoms clause170) := by
  exact C.covered_clause _ _ (C.fixed_positive 8 9 12 (by decide) (by decide) (by decide) (compatible.2.2 (8, 9, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 172: fixed_sign; source clause 23005.
private theorem sound171 : C.clause (decodeClause atoms clause171) := by
  exact C.covered_clause _ _ (C.fixed_negative 8 10 12 (by decide) (by decide) (by decide) (compatible.2.2 (8, 12, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 173: fixed_sign; source clause 23006.
private theorem sound172 : C.clause (decodeClause atoms clause172) := by
  exact C.covered_clause _ _ (C.fixed_negative 8 11 12 (by decide) (by decide) (by decide) (compatible.2.2 (8, 12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 174: fixed_sign; source clause 23007.
private theorem sound173 : C.clause (decodeClause atoms clause173) := by
  exact C.covered_clause _ _ (C.fixed_negative 9 10 12 (by decide) (by decide) (by decide) (compatible.2.2 (9, 12, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 175: fixed_sign; source clause 23008.
private theorem sound174 : C.clause (decodeClause atoms clause174) := by
  exact C.covered_clause _ _ (C.fixed_negative 9 11 12 (by decide) (by decide) (by decide) (compatible.2.2 (9, 12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 176: fixed_sign; source clause 23009.
private theorem sound175 : C.clause (decodeClause atoms clause175) := by
  exact C.covered_clause _ _ (C.fixed_negative 10 11 12 (by decide) (by decide) (by decide) (compatible.2.2 (10, 12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 177: convex_four; source clause 23217.
omit compatible in
private theorem sound176 : C.clause (decodeClause atoms clause176) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 178: convex_four; source clause 23841.
omit compatible in
private theorem sound177 : C.clause (decodeClause atoms clause177) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 179: convex_four; source clause 24049.
omit compatible in
private theorem sound178 : C.clause (decodeClause atoms clause178) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 180: convex_four; source clause 24673.
omit compatible in
private theorem sound179 : C.clause (decodeClause atoms clause179) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 181: packet; source clause 24681.
omit compatible in
private theorem sound180 : C.clause (decodeClause atoms clause180) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 2 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 182: convex_four; source clause 24881.
omit compatible in
private theorem sound181 : C.clause (decodeClause atoms clause181) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 183: convex_four; source clause 25713.
omit compatible in
private theorem sound182 : C.clause (decodeClause atoms clause182) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 184: convex_four; source clause 25921.
omit compatible in
private theorem sound183 : C.clause (decodeClause atoms clause183) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 185: convex_four; source clause 26545.
omit compatible in
private theorem sound184 : C.clause (decodeClause atoms clause184) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 186: packet; source clause 26553.
omit compatible in
private theorem sound185 : C.clause (decodeClause atoms clause185) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 3 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 187: convex_four; source clause 26753.
omit compatible in
private theorem sound186 : C.clause (decodeClause atoms clause186) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 188: convex_four; source clause 30289.
omit compatible in
private theorem sound187 : C.clause (decodeClause atoms clause187) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 189: convex_four; source clause 30913.
omit compatible in
private theorem sound188 : C.clause (decodeClause atoms clause188) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 190: convex_four; source clause 31121.
omit compatible in
private theorem sound189 : C.clause (decodeClause atoms clause189) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 191: convex_four; source clause 31950.
omit compatible in
private theorem sound190 : C.clause (decodeClause atoms clause190) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 192: convex_four; source clause 32158.
omit compatible in
private theorem sound191 : C.clause (decodeClause atoms clause191) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 193: convex_four; source clause 34033.
omit compatible in
private theorem sound192 : C.clause (decodeClause atoms clause192) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 194: convex_four; source clause 35073.
omit compatible in
private theorem sound193 : C.clause (decodeClause atoms clause193) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 195: convex_four; source clause 35281.
omit compatible in
private theorem sound194 : C.clause (decodeClause atoms clause194) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 196: convex_four; source clause 35905.
omit compatible in
private theorem sound195 : C.clause (decodeClause atoms clause195) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 197: packet; source clause 35944.
omit compatible in
private theorem sound196 : C.clause (decodeClause atoms clause196) := by
  exact C.covered_clause _ _ (C.packet_clause 0 11 2 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 198: convex_four; source clause 36113.
omit compatible in
private theorem sound197 : C.clause (decodeClause atoms clause197) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 199: convex_four; source clause 39649.
omit compatible in
private theorem sound198 : C.clause (decodeClause atoms clause198) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 200: convex_four; source clause 40273.
omit compatible in
private theorem sound199 : C.clause (decodeClause atoms clause199) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 201: convex_four; source clause 40481.
omit compatible in
private theorem sound200 : C.clause (decodeClause atoms clause200) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 202: convex_four; source clause 41310.
omit compatible in
private theorem sound201 : C.clause (decodeClause atoms clause201) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 203: convex_four; source clause 41518.
omit compatible in
private theorem sound202 : C.clause (decodeClause atoms clause202) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 204: packet; source clause 43195.
omit compatible in
private theorem sound203 : C.clause (decodeClause atoms clause203) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 205: convex_four; source clause 43389.
omit compatible in
private theorem sound204 : C.clause (decodeClause atoms clause204) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 206: convex_four; source clause 43393.
omit compatible in
private theorem sound205 : C.clause (decodeClause atoms clause205) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 207: convex_four; source clause 47137.
omit compatible in
private theorem sound206 : C.clause (decodeClause atoms clause206) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 208: convex_four; source clause 47761.
omit compatible in
private theorem sound207 : C.clause (decodeClause atoms clause207) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 209: packet; source clause 47800.
omit compatible in
private theorem sound208 : C.clause (decodeClause atoms clause208) := by
  exact C.covered_clause _ _ (C.packet_clause 0 11 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 210: convex_four; source clause 47969.
omit compatible in
private theorem sound209 : C.clause (decodeClause atoms clause209) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 211: convex_four; source clause 48798.
omit compatible in
private theorem sound210 : C.clause (decodeClause atoms clause210) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 212: convex_four; source clause 49006.
omit compatible in
private theorem sound211 : C.clause (decodeClause atoms clause211) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 213: packet; source clause 50683.
omit compatible in
private theorem sound212 : C.clause (decodeClause atoms clause212) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 214: convex_four; source clause 50877.
omit compatible in
private theorem sound213 : C.clause (decodeClause atoms clause213) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 215: convex_four; source clause 50881.
omit compatible in
private theorem sound214 : C.clause (decodeClause atoms clause214) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 216: convex_four; source clause 62110.
omit compatible in
private theorem sound215 : C.clause (decodeClause atoms clause215) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 217: packet; source clause 62138.
omit compatible in
private theorem sound216 : C.clause (decodeClause atoms clause216) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 11 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 218: convex_four; source clause 62318.
omit compatible in
private theorem sound217 : C.clause (decodeClause atoms clause217) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 219: packet; source clause 63995.
omit compatible in
private theorem sound218 : C.clause (decodeClause atoms clause218) := by
  exact C.covered_clause _ _ (C.packet_clause 0 6 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 220: convex_four; source clause 64193.
omit compatible in
private theorem sound219 : C.clause (decodeClause atoms clause219) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 221: packet; source clause 66074.
omit compatible in
private theorem sound220 : C.clause (decodeClause atoms clause220) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 222: convex_four; source clause 66261.
omit compatible in
private theorem sound221 : C.clause (decodeClause atoms clause221) := by
  exact C.covered_clause _ _ (C.convex_clause 0 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 223: convex_four; source clause 69393.
omit compatible in
private theorem sound222 : C.clause (decodeClause atoms clause222) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 224: convex_four; source clause 69601.
omit compatible in
private theorem sound223 : C.clause (decodeClause atoms clause223) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 225: convex_four; source clause 70225.
omit compatible in
private theorem sound224 : C.clause (decodeClause atoms clause224) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 226: packet; source clause 70233.
omit compatible in
private theorem sound225 : C.clause (decodeClause atoms clause225) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 3 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 227: convex_four; source clause 70433.
omit compatible in
private theorem sound226 : C.clause (decodeClause atoms clause226) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 228: packet; source clause 71926.
omit compatible in
private theorem sound227 : C.clause (decodeClause atoms clause227) := by
  exact C.covered_clause _ _ (C.packet_clause 1 11 2 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 229: packet; source clause 72037.
omit compatible in
private theorem sound228 : C.clause (decodeClause atoms clause228) := by
  exact C.covered_clause _ _ (C.packet_clause 11 1 2 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 230: convex_four; source clause 73969.
omit compatible in
private theorem sound229 : C.clause (decodeClause atoms clause229) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 231: convex_four; source clause 74593.
omit compatible in
private theorem sound230 : C.clause (decodeClause atoms clause230) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 232: convex_four; source clause 74801.
omit compatible in
private theorem sound231 : C.clause (decodeClause atoms clause231) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 233: convex_four; source clause 75630.
omit compatible in
private theorem sound232 : C.clause (decodeClause atoms clause232) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 234: convex_four; source clause 75838.
omit compatible in
private theorem sound233 : C.clause (decodeClause atoms clause233) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 235: packet; source clause 77515.
omit compatible in
private theorem sound234 : C.clause (decodeClause atoms clause234) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 236: convex_four; source clause 77713.
omit compatible in
private theorem sound235 : C.clause (decodeClause atoms clause235) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 237: packet; source clause 80870.
omit compatible in
private theorem sound236 : C.clause (decodeClause atoms clause236) := by
  exact C.covered_clause _ _ (C.packet_clause 1 11 3 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 238: packet; source clause 80981.
omit compatible in
private theorem sound237 : C.clause (decodeClause atoms clause237) := by
  exact C.covered_clause _ _ (C.packet_clause 11 1 3 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 239: convex_four; source clause 81457.
omit compatible in
private theorem sound238 : C.clause (decodeClause atoms clause238) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 240: convex_four; source clause 82081.
omit compatible in
private theorem sound239 : C.clause (decodeClause atoms clause239) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 241: convex_four; source clause 82289.
omit compatible in
private theorem sound240 : C.clause (decodeClause atoms clause240) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 242: convex_four; source clause 83118.
omit compatible in
private theorem sound241 : C.clause (decodeClause atoms clause241) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 243: convex_four; source clause 83326.
omit compatible in
private theorem sound242 : C.clause (decodeClause atoms clause242) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 244: packet; source clause 85003.
omit compatible in
private theorem sound243 : C.clause (decodeClause atoms clause243) := by
  exact C.covered_clause _ _ (C.packet_clause 1 3 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 245: convex_four; source clause 85197.
omit compatible in
private theorem sound244 : C.clause (decodeClause atoms clause244) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 246: convex_four; source clause 85201.
omit compatible in
private theorem sound245 : C.clause (decodeClause atoms clause245) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 247: packet; source clause 90825.
omit compatible in
private theorem sound246 : C.clause (decodeClause atoms clause246) := by
  exact C.covered_clause _ _ (C.packet_clause 1 4 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 248: packet; source clause 95202.
omit compatible in
private theorem sound247 : C.clause (decodeClause atoms clause247) := by
  exact C.covered_clause _ _ (C.packet_clause 1 10 5 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 249: convex_four; source clause 96430.
omit compatible in
private theorem sound248 : C.clause (decodeClause atoms clause248) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 250: packet; source clause 96562.
omit compatible in
private theorem sound249 : C.clause (decodeClause atoms clause249) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 1 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 251: convex_four; source clause 96638.
omit compatible in
private theorem sound250 : C.clause (decodeClause atoms clause250) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 252: packet; source clause 97926.
omit compatible in
private theorem sound251 : C.clause (decodeClause atoms clause251) := by
  exact C.covered_clause _ _ (C.packet_clause 1 11 6 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 253: packet; source clause 98315.
omit compatible in
private theorem sound252 : C.clause (decodeClause atoms clause252) := by
  exact C.covered_clause _ _ (C.packet_clause 1 6 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 254: convex_four; source clause 98513.
omit compatible in
private theorem sound253 : C.clause (decodeClause atoms clause253) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 255: packet; source clause 100466.
omit compatible in
private theorem sound254 : C.clause (decodeClause atoms clause254) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 1 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 256: convex_four; source clause 100581.
omit compatible in
private theorem sound255 : C.clause (decodeClause atoms clause255) := by
  exact C.covered_clause _ _ (C.convex_clause 1 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 257: packet; source clause 102902.
omit compatible in
private theorem sound256 : C.clause (decodeClause atoms clause256) := by
  exact C.covered_clause _ _ (C.packet_clause 1 11 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 258: packet; source clause 105830.
omit compatible in
private theorem sound257 : C.clause (decodeClause atoms clause257) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 3 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 259: packet; source clause 105941.
omit compatible in
private theorem sound258 : C.clause (decodeClause atoms clause258) := by
  exact C.covered_clause _ _ (C.packet_clause 11 2 3 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 260: convex_four; source clause 106417.
omit compatible in
private theorem sound259 : C.clause (decodeClause atoms clause259) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 261: convex_four; source clause 107041.
omit compatible in
private theorem sound260 : C.clause (decodeClause atoms clause260) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 262: convex_four; source clause 107249.
omit compatible in
private theorem sound261 : C.clause (decodeClause atoms clause261) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 263: convex_four; source clause 108078.
omit compatible in
private theorem sound262 : C.clause (decodeClause atoms clause262) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 264: convex_four; source clause 108286.
omit compatible in
private theorem sound263 : C.clause (decodeClause atoms clause263) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 265: packet; source clause 109963.
omit compatible in
private theorem sound264 : C.clause (decodeClause atoms clause264) := by
  exact C.covered_clause _ _ (C.packet_clause 2 3 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 266: convex_four; source clause 110157.
omit compatible in
private theorem sound265 : C.clause (decodeClause atoms clause265) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 267: convex_four; source clause 110161.
omit compatible in
private theorem sound266 : C.clause (decodeClause atoms clause266) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 268: convex_four; source clause 111201.
omit compatible in
private theorem sound267 : C.clause (decodeClause atoms clause267) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 269: convex_four; source clause 111409.
omit compatible in
private theorem sound268 : C.clause (decodeClause atoms clause268) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 270: convex_four; source clause 111617.
omit compatible in
private theorem sound269 : C.clause (decodeClause atoms clause269) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 271: convex_four; source clause 111825.
omit compatible in
private theorem sound270 : C.clause (decodeClause atoms clause270) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 5 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 272: convex_four; source clause 112033.
omit compatible in
private theorem sound271 : C.clause (decodeClause atoms clause271) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 273: convex_four; source clause 114529.
omit compatible in
private theorem sound272 : C.clause (decodeClause atoms clause272) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 274: convex_four; source clause 114737.
omit compatible in
private theorem sound273 : C.clause (decodeClause atoms clause273) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 275: convex_four; source clause 114945.
omit compatible in
private theorem sound274 : C.clause (decodeClause atoms clause274) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 276: convex_four; source clause 115153.
omit compatible in
private theorem sound275 : C.clause (decodeClause atoms clause275) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 277: convex_four; source clause 115361.
omit compatible in
private theorem sound276 : C.clause (decodeClause atoms clause276) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 278: convex_four; source clause 115569.
omit compatible in
private theorem sound277 : C.clause (decodeClause atoms clause277) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 279: convex_four; source clause 115777.
omit compatible in
private theorem sound278 : C.clause (decodeClause atoms clause278) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 280: convex_four; source clause 115982.
omit compatible in
private theorem sound279 : C.clause (decodeClause atoms clause279) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 281: convex_four; source clause 116190.
omit compatible in
private theorem sound280 : C.clause (decodeClause atoms clause280) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 282: convex_four; source clause 116398.
omit compatible in
private theorem sound281 : C.clause (decodeClause atoms clause281) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 283: convex_four; source clause 118897.
omit compatible in
private theorem sound282 : C.clause (decodeClause atoms clause282) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 284: convex_four; source clause 119105.
omit compatible in
private theorem sound283 : C.clause (decodeClause atoms clause283) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 285: convex_four; source clause 119313.
omit compatible in
private theorem sound284 : C.clause (decodeClause atoms clause284) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 286: convex_four; source clause 119521.
omit compatible in
private theorem sound285 : C.clause (decodeClause atoms clause285) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 287: convex_four; source clause 119729.
omit compatible in
private theorem sound286 : C.clause (decodeClause atoms clause286) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 288: convex_four; source clause 119937.
omit compatible in
private theorem sound287 : C.clause (decodeClause atoms clause287) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 289: convex_four; source clause 120145.
omit compatible in
private theorem sound288 : C.clause (decodeClause atoms clause288) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 290: convex_four; source clause 120350.
omit compatible in
private theorem sound289 : C.clause (decodeClause atoms clause289) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 291: convex_four; source clause 120558.
omit compatible in
private theorem sound290 : C.clause (decodeClause atoms clause290) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 292: convex_four; source clause 120766.
omit compatible in
private theorem sound291 : C.clause (decodeClause atoms clause291) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 293: convex_four; source clause 121390.
omit compatible in
private theorem sound292 : C.clause (decodeClause atoms clause292) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 294: packet; source clause 121522.
omit compatible in
private theorem sound293 : C.clause (decodeClause atoms clause293) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 2 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 295: convex_four; source clause 121598.
omit compatible in
private theorem sound294 : C.clause (decodeClause atoms clause294) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 296: packet; source clause 122886.
omit compatible in
private theorem sound295 : C.clause (decodeClause atoms clause295) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 6 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 297: packet; source clause 123275.
omit compatible in
private theorem sound296 : C.clause (decodeClause atoms clause296) := by
  exact C.covered_clause _ _ (C.packet_clause 2 6 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 298: convex_four; source clause 123469.
omit compatible in
private theorem sound297 : C.clause (decodeClause atoms clause297) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 299: convex_four; source clause 123473.
omit compatible in
private theorem sound298 : C.clause (decodeClause atoms clause298) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 300: packet; source clause 125426.
omit compatible in
private theorem sound299 : C.clause (decodeClause atoms clause299) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 301: convex_four; source clause 125541.
omit compatible in
private theorem sound300 : C.clause (decodeClause atoms clause300) := by
  exact C.covered_clause _ _ (C.convex_clause 2 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 302: convex_four; source clause 126177.
omit compatible in
private theorem sound301 : C.clause (decodeClause atoms clause301) := by
  exact C.covered_clause _ _ (C.convex_clause 2 8 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 303: convex_four; source clause 126385.
omit compatible in
private theorem sound302 : C.clause (decodeClause atoms clause302) := by
  exact C.covered_clause _ _ (C.convex_clause 2 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 304: convex_four; source clause 126593.
omit compatible in
private theorem sound303 : C.clause (decodeClause atoms clause303) := by
  exact C.covered_clause _ _ (C.convex_clause 2 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 305: convex_four; source clause 126798.
omit compatible in
private theorem sound304 : C.clause (decodeClause atoms clause304) := by
  exact C.covered_clause _ _ (C.convex_clause 2 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 306: convex_four; source clause 127006.
omit compatible in
private theorem sound305 : C.clause (decodeClause atoms clause305) := by
  exact C.covered_clause _ _ (C.convex_clause 2 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 307: convex_four; source clause 127214.
omit compatible in
private theorem sound306 : C.clause (decodeClause atoms clause306) := by
  exact C.covered_clause _ _ (C.convex_clause 2 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 308: convex_four; source clause 127422.
omit compatible in
private theorem sound307 : C.clause (decodeClause atoms clause307) := by
  exact C.covered_clause _ _ (C.convex_clause 2 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 309: convex_four; source clause 127630.
omit compatible in
private theorem sound308 : C.clause (decodeClause atoms clause308) := by
  exact C.covered_clause _ _ (C.convex_clause 2 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 310: convex_four; source clause 127838.
omit compatible in
private theorem sound309 : C.clause (decodeClause atoms clause309) := by
  exact C.covered_clause _ _ (C.convex_clause 2 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 311: packet; source clause 127862.
omit compatible in
private theorem sound310 : C.clause (decodeClause atoms clause310) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 312: convex_four; source clause 128034.
omit compatible in
private theorem sound311 : C.clause (decodeClause atoms clause311) := by
  exact C.covered_clause _ _ (C.convex_clause 2 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 313: convex_four; source clause 128042.
omit compatible in
private theorem sound312 : C.clause (decodeClause atoms clause312) := by
  exact C.covered_clause _ _ (C.convex_clause 2 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 314: packet; source clause 137625.
omit compatible in
private theorem sound313 : C.clause (decodeClause atoms clause313) := by
  exact C.covered_clause _ _ (C.packet_clause 3 5 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 315: convex_four; source clause 138862.
omit compatible in
private theorem sound314 : C.clause (decodeClause atoms clause314) := by
  exact C.covered_clause _ _ (C.convex_clause 3 6 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 316: packet; source clause 138994.
omit compatible in
private theorem sound315 : C.clause (decodeClause atoms clause315) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 317: convex_four; source clause 139070.
omit compatible in
private theorem sound316 : C.clause (decodeClause atoms clause316) := by
  exact C.covered_clause _ _ (C.convex_clause 3 6 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 318: packet; source clause 140358.
omit compatible in
private theorem sound317 : C.clause (decodeClause atoms clause317) := by
  exact C.covered_clause _ _ (C.packet_clause 3 11 6 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 319: packet; source clause 140747.
omit compatible in
private theorem sound318 : C.clause (decodeClause atoms clause318) := by
  exact C.covered_clause _ _ (C.packet_clause 3 6 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 320: convex_four; source clause 140945.
omit compatible in
private theorem sound319 : C.clause (decodeClause atoms clause319) := by
  exact C.covered_clause _ _ (C.convex_clause 3 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 321: packet; source clause 142898.
omit compatible in
private theorem sound320 : C.clause (decodeClause atoms clause320) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 322: convex_four; source clause 143013.
omit compatible in
private theorem sound321 : C.clause (decodeClause atoms clause321) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 323: packet; source clause 144073.
omit compatible in
private theorem sound322 : C.clause (decodeClause atoms clause322) := by
  exact C.covered_clause _ _ (C.packet_clause 3 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 324: packet; source clause 144082.
omit compatible in
private theorem sound323 : C.clause (decodeClause atoms clause323) := by
  exact C.covered_clause _ _ (C.packet_clause 3 10 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 325: packet; source clause 144706.
omit compatible in
private theorem sound324 : C.clause (decodeClause atoms clause324) := by
  exact C.covered_clause _ _ (C.packet_clause 3 10 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 326: packet; source clause 145334.
omit compatible in
private theorem sound325 : C.clause (decodeClause atoms clause325) := by
  exact C.covered_clause _ _ (C.packet_clause 3 11 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 327: convex_four; source clause 148017.
omit compatible in
private theorem sound326 : C.clause (decodeClause atoms clause326) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 328: convex_four; source clause 148225.
omit compatible in
private theorem sound327 : C.clause (decodeClause atoms clause327) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 329: convex_four; source clause 148433.
omit compatible in
private theorem sound328 : C.clause (decodeClause atoms clause328) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 330: convex_four; source clause 148641.
omit compatible in
private theorem sound329 : C.clause (decodeClause atoms clause329) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 331: convex_four; source clause 148849.
omit compatible in
private theorem sound330 : C.clause (decodeClause atoms clause330) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 332: convex_four; source clause 149057.
omit compatible in
private theorem sound331 : C.clause (decodeClause atoms clause331) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 333: convex_four; source clause 149265.
omit compatible in
private theorem sound332 : C.clause (decodeClause atoms clause332) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 334: packet; source clause 149400.
omit compatible in
private theorem sound333 : C.clause (decodeClause atoms clause333) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 4 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 335: convex_four; source clause 149470.
omit compatible in
private theorem sound334 : C.clause (decodeClause atoms clause334) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 336: convex_four; source clause 149678.
omit compatible in
private theorem sound335 : C.clause (decodeClause atoms clause335) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 337: convex_four; source clause 149886.
omit compatible in
private theorem sound336 : C.clause (decodeClause atoms clause336) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 338: convex_four; source clause 155297.
omit compatible in
private theorem sound337 : C.clause (decodeClause atoms clause337) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 339: convex_four; source clause 155505.
omit compatible in
private theorem sound338 : C.clause (decodeClause atoms clause338) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 340: convex_four; source clause 155713.
omit compatible in
private theorem sound339 : C.clause (decodeClause atoms clause339) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 341: convex_four; source clause 155918.
omit compatible in
private theorem sound340 : C.clause (decodeClause atoms clause340) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 342: convex_four; source clause 156126.
omit compatible in
private theorem sound341 : C.clause (decodeClause atoms clause341) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 343: convex_four; source clause 156334.
omit compatible in
private theorem sound342 : C.clause (decodeClause atoms clause342) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 344: convex_four; source clause 156542.
omit compatible in
private theorem sound343 : C.clause (decodeClause atoms clause343) := by
  exact C.covered_clause _ _ (C.convex_clause 4 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 345: convex_four; source clause 156750.
omit compatible in
private theorem sound344 : C.clause (decodeClause atoms clause344) := by
  exact C.covered_clause _ _ (C.convex_clause 4 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 346: convex_four; source clause 156958.
omit compatible in
private theorem sound345 : C.clause (decodeClause atoms clause345) := by
  exact C.covered_clause _ _ (C.convex_clause 4 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 347: packet; source clause 157011.
omit compatible in
private theorem sound346 : C.clause (decodeClause atoms clause346) := by
  exact C.covered_clause _ _ (C.packet_clause 10 4 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 348: convex_four; source clause 157154.
omit compatible in
private theorem sound347 : C.clause (decodeClause atoms clause347) := by
  exact C.covered_clause _ _ (C.convex_clause 4 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 349: convex_four; source clause 157162.
omit compatible in
private theorem sound348 : C.clause (decodeClause atoms clause348) := by
  exact C.covered_clause _ _ (C.convex_clause 4 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 350: convex_four; source clause 162577.
omit compatible in
private theorem sound349 : C.clause (decodeClause atoms clause349) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 351: convex_four; source clause 162785.
omit compatible in
private theorem sound350 : C.clause (decodeClause atoms clause350) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 352: convex_four; source clause 162993.
omit compatible in
private theorem sound351 : C.clause (decodeClause atoms clause351) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 353: packet; source clause 163128.
omit compatible in
private theorem sound352 : C.clause (decodeClause atoms clause352) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 354: convex_four; source clause 163198.
omit compatible in
private theorem sound353 : C.clause (decodeClause atoms clause353) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 355: convex_four; source clause 163406.
omit compatible in
private theorem sound354 : C.clause (decodeClause atoms clause354) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 356: convex_four; source clause 163614.
omit compatible in
private theorem sound355 : C.clause (decodeClause atoms clause355) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 357: convex_four; source clause 163822.
omit compatible in
private theorem sound356 : C.clause (decodeClause atoms clause356) := by
  exact C.covered_clause _ _ (C.convex_clause 5 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 358: convex_four; source clause 164030.
omit compatible in
private theorem sound357 : C.clause (decodeClause atoms clause357) := by
  exact C.covered_clause _ _ (C.convex_clause 5 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 359: convex_four; source clause 164238.
omit compatible in
private theorem sound358 : C.clause (decodeClause atoms clause358) := by
  exact C.covered_clause _ _ (C.convex_clause 5 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 360: convex_four; source clause 164434.
omit compatible in
private theorem sound359 : C.clause (decodeClause atoms clause359) := by
  exact C.covered_clause _ _ (C.convex_clause 5 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 361: convex_four; source clause 164442.
omit compatible in
private theorem sound360 : C.clause (decodeClause atoms clause360) := by
  exact C.covered_clause _ _ (C.convex_clause 5 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 362: packet; source clause 165986.
omit compatible in
private theorem sound361 : C.clause (decodeClause atoms clause361) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 363: convex_four; source clause 166101.
omit compatible in
private theorem sound362 : C.clause (decodeClause atoms clause362) := by
  exact C.covered_clause _ _ (C.convex_clause 6 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 364: packet; source clause 167785.
omit compatible in
private theorem sound363 : C.clause (decodeClause atoms clause363) := by
  exact C.covered_clause _ _ (C.packet_clause 6 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 365: packet; source clause 168422.
omit compatible in
private theorem sound364 : C.clause (decodeClause atoms clause364) := by
  exact C.covered_clause _ _ (C.packet_clause 6 11 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 366: packet; source clause 170824.
omit compatible in
private theorem sound365 : C.clause (decodeClause atoms clause365) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 367: convex_four; source clause 170894.
omit compatible in
private theorem sound366 : C.clause (decodeClause atoms clause366) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 368: convex_four; source clause 171102.
omit compatible in
private theorem sound367 : C.clause (decodeClause atoms clause367) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 369: convex_four; source clause 171310.
omit compatible in
private theorem sound368 : C.clause (decodeClause atoms clause368) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 370: convex_four; source clause 171506.
omit compatible in
private theorem sound369 : C.clause (decodeClause atoms clause369) := by
  exact C.covered_clause _ _ (C.convex_clause 8 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 371: convex_four; source clause 171514.
omit compatible in
private theorem sound370 : C.clause (decodeClause atoms clause370) := by
  exact C.covered_clause _ _ (C.convex_clause 8 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 372: packet; source clause 171592.
omit compatible in
private theorem sound371 : C.clause (decodeClause atoms clause371) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 373: convex_four; source clause 171714.
omit compatible in
private theorem sound372 : C.clause (decodeClause atoms clause372) := by
  exact C.covered_clause _ _ (C.convex_clause 9 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 374: convex_four; source clause 171722.
omit compatible in
private theorem sound373 : C.clause (decodeClause atoms clause373) := by
  exact C.covered_clause _ _ (C.convex_clause 9 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 375: no_octagon; source clause 171734.
omit compatible in
private theorem sound374 : C.clause (decodeClause atoms clause374) := by
  exact C.no_octagon_clause {0, 1, 2, 3, 6, 7, 10, 11} (by decide +kernel) _ (by decide +kernel)

-- Clause 376: no_octagon; source clause 171755.
omit compatible in
private theorem sound375 : C.clause (decodeClause atoms clause375) := by
  exact C.no_octagon_clause {2, 4, 5, 8, 9, 10, 11, 12} (by decide +kernel) _ (by decide +kernel)

private theorem all_sound : List.Forall (fun cl => C.clause (decodeClause atoms cl)) clauses := by
  exact And.intro (sound000 C compatible) (And.intro (sound001 C compatible) (And.intro (sound002 C compatible) (And.intro (sound003 C compatible) (And.intro (sound004 C compatible) (And.intro (sound005 C compatible) (And.intro (sound006 C compatible) (And.intro (sound007 C compatible) (And.intro (sound008 C compatible) (And.intro (sound009 C compatible) (And.intro (sound010 C compatible) (And.intro (sound011 C compatible) (And.intro (sound012 C compatible) (And.intro (sound013 C compatible) (And.intro (sound014 C compatible) (And.intro (sound015 C compatible) (And.intro (sound016 C compatible) (And.intro (sound017 C compatible) (And.intro (sound018 C compatible) (And.intro (sound019 C compatible) (And.intro (sound020 C compatible) (And.intro (sound021 C compatible) (And.intro (sound022 C compatible) (And.intro (sound023 C compatible) (And.intro (sound024 C compatible) (And.intro (sound025 C compatible) (And.intro (sound026 C compatible) (And.intro (sound027 C compatible) (And.intro (sound028 C compatible) (And.intro (sound029 C compatible) (And.intro (sound030 C compatible) (And.intro (sound031 C compatible) (And.intro (sound032 C compatible) (And.intro (sound033 C compatible) (And.intro (sound034 C compatible) (And.intro (sound035 C compatible) (And.intro (sound036 C compatible) (And.intro (sound037 C compatible) (And.intro (sound038 C compatible) (And.intro (sound039 C compatible) (And.intro (sound040 C compatible) (And.intro (sound041 C) (And.intro (sound042 C) (And.intro (sound043 C) (And.intro (sound044 C) (And.intro (sound045 C) (And.intro (sound046 C) (And.intro (sound047 C) (And.intro (sound048 C) (And.intro (sound049 C) (And.intro (sound050 C) (And.intro (sound051 C) (And.intro (sound052 C) (And.intro (sound053 C) (And.intro (sound054 C) (And.intro (sound055 C) (And.intro (sound056 C) (And.intro (sound057 C) (And.intro (sound058 C compatible) (And.intro (sound059 C compatible) (And.intro (sound060 C compatible) (And.intro (sound061 C compatible) (And.intro (sound062 C compatible) (And.intro (sound063 C compatible) (And.intro (sound064 C compatible) (And.intro (sound065 C compatible) (And.intro (sound066 C compatible) (And.intro (sound067 C compatible) (And.intro (sound068 C compatible) (And.intro (sound069 C compatible) (And.intro (sound070 C compatible) (And.intro (sound071 C compatible) (And.intro (sound072 C compatible) (And.intro (sound073 C compatible) (And.intro (sound074 C compatible) (And.intro (sound075 C compatible) (And.intro (sound076 C compatible) (And.intro (sound077 C compatible) (And.intro (sound078 C compatible) (And.intro (sound079 C compatible) (And.intro (sound080 C compatible) (And.intro (sound081 C compatible) (And.intro (sound082 C compatible) (And.intro (sound083 C compatible) (And.intro (sound084 C compatible) (And.intro (sound085 C compatible) (And.intro (sound086 C compatible) (And.intro (sound087 C compatible) (And.intro (sound088 C compatible) (And.intro (sound089 C compatible) (And.intro (sound090 C compatible) (And.intro (sound091 C compatible) (And.intro (sound092 C compatible) (And.intro (sound093 C compatible) (And.intro (sound094 C compatible) (And.intro (sound095 C compatible) (And.intro (sound096 C compatible) (And.intro (sound097 C compatible) (And.intro (sound098 C compatible) (And.intro (sound099 C compatible) (And.intro (sound100 C compatible) (And.intro (sound101 C compatible) (And.intro (sound102 C compatible) (And.intro (sound103 C compatible) (And.intro (sound104 C compatible) (And.intro (sound105 C compatible) (And.intro (sound106 C compatible) (And.intro (sound107 C compatible) (And.intro (sound108 C compatible) (And.intro (sound109 C compatible) (And.intro (sound110 C compatible) (And.intro (sound111 C compatible) (And.intro (sound112 C compatible) (And.intro (sound113 C compatible) (And.intro (sound114 C compatible) (And.intro (sound115 C compatible) (And.intro (sound116 C compatible) (And.intro (sound117 C compatible) (And.intro (sound118 C compatible) (And.intro (sound119 C compatible) (And.intro (sound120 C compatible) (And.intro (sound121 C compatible) (And.intro (sound122 C compatible) (And.intro (sound123 C compatible) (And.intro (sound124 C compatible) (And.intro (sound125 C compatible) (And.intro (sound126 C compatible) (And.intro (sound127 C compatible) (And.intro (sound128 C compatible) (And.intro (sound129 C compatible) (And.intro (sound130 C compatible) (And.intro (sound131 C compatible) (And.intro (sound132 C compatible) (And.intro (sound133 C compatible) (And.intro (sound134 C compatible) (And.intro (sound135 C compatible) (And.intro (sound136 C compatible) (And.intro (sound137 C compatible) (And.intro (sound138 C compatible) (And.intro (sound139 C compatible) (And.intro (sound140 C compatible) (And.intro (sound141 C compatible) (And.intro (sound142 C compatible) (And.intro (sound143 C compatible) (And.intro (sound144 C compatible) (And.intro (sound145 C compatible) (And.intro (sound146 C compatible) (And.intro (sound147 C compatible) (And.intro (sound148 C compatible) (And.intro (sound149 C compatible) (And.intro (sound150 C compatible) (And.intro (sound151 C compatible) (And.intro (sound152 C compatible) (And.intro (sound153 C compatible) (And.intro (sound154 C compatible) (And.intro (sound155 C compatible) (And.intro (sound156 C compatible) (And.intro (sound157 C compatible) (And.intro (sound158 C compatible) (And.intro (sound159 C compatible) (And.intro (sound160 C compatible) (And.intro (sound161 C compatible) (And.intro (sound162 C compatible) (And.intro (sound163 C compatible) (And.intro (sound164 C compatible) (And.intro (sound165 C compatible) (And.intro (sound166 C compatible) (And.intro (sound167 C compatible) (And.intro (sound168 C compatible) (And.intro (sound169 C compatible) (And.intro (sound170 C compatible) (And.intro (sound171 C compatible) (And.intro (sound172 C compatible) (And.intro (sound173 C compatible) (And.intro (sound174 C compatible) (And.intro (sound175 C compatible) (And.intro (sound176 C) (And.intro (sound177 C) (And.intro (sound178 C) (And.intro (sound179 C) (And.intro (sound180 C) (And.intro (sound181 C) (And.intro (sound182 C) (And.intro (sound183 C) (And.intro (sound184 C) (And.intro (sound185 C) (And.intro (sound186 C) (And.intro (sound187 C) (And.intro (sound188 C) (And.intro (sound189 C) (And.intro (sound190 C) (And.intro (sound191 C) (And.intro (sound192 C) (And.intro (sound193 C) (And.intro (sound194 C) (And.intro (sound195 C) (And.intro (sound196 C) (And.intro (sound197 C) (And.intro (sound198 C) (And.intro (sound199 C) (And.intro (sound200 C) (And.intro (sound201 C) (And.intro (sound202 C) (And.intro (sound203 C) (And.intro (sound204 C) (And.intro (sound205 C) (And.intro (sound206 C) (And.intro (sound207 C) (And.intro (sound208 C) (And.intro (sound209 C) (And.intro (sound210 C) (And.intro (sound211 C) (And.intro (sound212 C) (And.intro (sound213 C) (And.intro (sound214 C) (And.intro (sound215 C) (And.intro (sound216 C) (And.intro (sound217 C) (And.intro (sound218 C) (And.intro (sound219 C) (And.intro (sound220 C) (And.intro (sound221 C) (And.intro (sound222 C) (And.intro (sound223 C) (And.intro (sound224 C) (And.intro (sound225 C) (And.intro (sound226 C) (And.intro (sound227 C) (And.intro (sound228 C) (And.intro (sound229 C) (And.intro (sound230 C) (And.intro (sound231 C) (And.intro (sound232 C) (And.intro (sound233 C) (And.intro (sound234 C) (And.intro (sound235 C) (And.intro (sound236 C) (And.intro (sound237 C) (And.intro (sound238 C) (And.intro (sound239 C) (And.intro (sound240 C) (And.intro (sound241 C) (And.intro (sound242 C) (And.intro (sound243 C) (And.intro (sound244 C) (And.intro (sound245 C) (And.intro (sound246 C) (And.intro (sound247 C) (And.intro (sound248 C) (And.intro (sound249 C) (And.intro (sound250 C) (And.intro (sound251 C) (And.intro (sound252 C) (And.intro (sound253 C) (And.intro (sound254 C) (And.intro (sound255 C) (And.intro (sound256 C) (And.intro (sound257 C) (And.intro (sound258 C) (And.intro (sound259 C) (And.intro (sound260 C) (And.intro (sound261 C) (And.intro (sound262 C) (And.intro (sound263 C) (And.intro (sound264 C) (And.intro (sound265 C) (And.intro (sound266 C) (And.intro (sound267 C) (And.intro (sound268 C) (And.intro (sound269 C) (And.intro (sound270 C) (And.intro (sound271 C) (And.intro (sound272 C) (And.intro (sound273 C) (And.intro (sound274 C) (And.intro (sound275 C) (And.intro (sound276 C) (And.intro (sound277 C) (And.intro (sound278 C) (And.intro (sound279 C) (And.intro (sound280 C) (And.intro (sound281 C) (And.intro (sound282 C) (And.intro (sound283 C) (And.intro (sound284 C) (And.intro (sound285 C) (And.intro (sound286 C) (And.intro (sound287 C) (And.intro (sound288 C) (And.intro (sound289 C) (And.intro (sound290 C) (And.intro (sound291 C) (And.intro (sound292 C) (And.intro (sound293 C) (And.intro (sound294 C) (And.intro (sound295 C) (And.intro (sound296 C) (And.intro (sound297 C) (And.intro (sound298 C) (And.intro (sound299 C) (And.intro (sound300 C) (And.intro (sound301 C) (And.intro (sound302 C) (And.intro (sound303 C) (And.intro (sound304 C) (And.intro (sound305 C) (And.intro (sound306 C) (And.intro (sound307 C) (And.intro (sound308 C) (And.intro (sound309 C) (And.intro (sound310 C) (And.intro (sound311 C) (And.intro (sound312 C) (And.intro (sound313 C) (And.intro (sound314 C) (And.intro (sound315 C) (And.intro (sound316 C) (And.intro (sound317 C) (And.intro (sound318 C) (And.intro (sound319 C) (And.intro (sound320 C) (And.intro (sound321 C) (And.intro (sound322 C) (And.intro (sound323 C) (And.intro (sound324 C) (And.intro (sound325 C) (And.intro (sound326 C) (And.intro (sound327 C) (And.intro (sound328 C) (And.intro (sound329 C) (And.intro (sound330 C) (And.intro (sound331 C) (And.intro (sound332 C) (And.intro (sound333 C) (And.intro (sound334 C) (And.intro (sound335 C) (And.intro (sound336 C) (And.intro (sound337 C) (And.intro (sound338 C) (And.intro (sound339 C) (And.intro (sound340 C) (And.intro (sound341 C) (And.intro (sound342 C) (And.intro (sound343 C) (And.intro (sound344 C) (And.intro (sound345 C) (And.intro (sound346 C) (And.intro (sound347 C) (And.intro (sound348 C) (And.intro (sound349 C) (And.intro (sound350 C) (And.intro (sound351 C) (And.intro (sound352 C) (And.intro (sound353 C) (And.intro (sound354 C) (And.intro (sound355 C) (And.intro (sound356 C) (And.intro (sound357 C) (And.intro (sound358 C) (And.intro (sound359 C) (And.intro (sound360 C) (And.intro (sound361 C) (And.intro (sound362 C) (And.intro (sound363 C) (And.intro (sound364 C) (And.intro (sound365 C) (And.intro (sound366 C) (And.intro (sound367 C) (And.intro (sound368 C) (And.intro (sound369 C) (And.intro (sound370 C) (And.intro (sound371 C) (And.intro (sound372 C) (And.intro (sound373 C) (And.intro (sound374 C) (sound375 C)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

theorem context_impossible (C : Context 13 n σ) : False := by
  have h : (C.valuation atoms).satisfies_fmla CoupledCoreSixth.cnf_refutation.formula := by
    rw [formula_eq]
    constructor
    intro cl hc
    exact C.satisfies_of_clause atoms cl ((List.forall_iff_forall_mem.mp (all_sound C compatible)) cl hc)
  exact CoupledCoreSixth.cnf_refutation (C.valuation atoms) h

#print axioms context_impossible
end ErdosSzekeres.Omission.CoupledTemplateSixth

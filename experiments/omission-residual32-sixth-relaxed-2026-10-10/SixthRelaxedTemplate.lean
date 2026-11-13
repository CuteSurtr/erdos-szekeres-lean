import SixthRelaxedCore

/-! The frozen 1029-clause proof applies to any literal support satisfying
its finite state-dependent prerequisites. No fresh SAT result is assumed. -/
namespace ErdosSzekeres.Omission.CoupledTemplateSixthRelaxed
open Coupled CoupledCoreSixthRelaxed
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

def emptyTests : List (Fin 13 × Fin 13) := [(1, 0), (10, 6), (12, 10), (12, 11)]

def domainTests : List (Fin 13 × Fin 13 × ℕ × ℕ) := [(10, 11, 2, 4), (10, 11, 2, 5), (10, 11, 2, 6), (10, 11, 3, 4), (10, 11, 3, 5), (10, 11, 3, 6)]

def positiveTests : List (Fin 13 × Fin 13 × Fin 13) := [(0, 1, 2), (0, 1, 7), (0, 11, 7), (1, 2, 3), (1, 2, 7), (1, 11, 7), (1, 12, 11), (2, 3, 6), (2, 3, 7), (2, 4, 5), (2, 4, 10), (2, 11, 7), (3, 6, 7), (3, 6, 10), (3, 11, 7), (4, 5, 8), (4, 5, 10), (4, 12, 10), (5, 8, 9), (5, 8, 10), (5, 12, 10), (6, 10, 7), (6, 11, 7), (6, 12, 10), (7, 10, 11), (8, 9, 10), (8, 9, 12), (8, 12, 10), (9, 12, 10), (9, 12, 11), (10, 12, 11)]

def Compatible (σ : Fin 13 → Fin 154) : Prop :=
  (∀ t ∈ emptyTests, emptyCheck σ t.1 t.2 = true) ∧
  (∀ t ∈ domainTests, ¬Allowed σ t.1 t.2.1 (t.2.2.1, t.2.2.2)) ∧
  (∀ t ∈ positiveTests, CycleSigns.CheckTriple ResidualDomains.computedTable
    (σ t.1) (σ t.2.1) (σ t.2.2) = true)

instance (σ : Fin 13 → Fin 154) : Decidable (Compatible σ) := by
  unfold Compatible
  infer_instance

private def clause000 : Sat.Clause := [.neg 0, .pos 3, .neg 10]
private def clause001 : Sat.Clause := [.neg 0, .neg 10, .pos 11, .neg 101]
private def clause002 : Sat.Clause := [.neg 0, .neg 1, .neg 10, .pos 12, .neg 101]
private def clause003 : Sat.Clause := [.neg 0, .neg 2, .neg 10, .pos 13, .neg 101]
private def clause004 : Sat.Clause := [.neg 0, .pos 4, .neg 14]
private def clause005 : Sat.Clause := [.neg 0, .pos 6, .neg 16]
private def clause006 : Sat.Clause := [.neg 3, .pos 4, .neg 21]
private def clause007 : Sat.Clause := [.neg 3, .pos 5, .neg 28]
private def clause008 : Sat.Clause := [.neg 3, .pos 8, .neg 32]
private def clause009 : Sat.Clause := [.neg 3, .pos 9, .neg 36]
private def clause010 : Sat.Clause := [.pos 4, .neg 6, .pos 42]
private def clause011 : Sat.Clause := [.pos 5, .neg 6, .pos 64]
private def clause012 : Sat.Clause := [.neg 6, .pos 9, .neg 73]
private def clause013 : Sat.Clause := [.neg 8, .neg 89, .pos 90, .pos 121]
private def clause014 : Sat.Clause := [.neg 9, .pos 73, .pos 74, .pos 120]
private def clause015 : Sat.Clause := [.neg 10, .pos 14, .neg 21]
private def clause016 : Sat.Clause := [.neg 10, .neg 11, .neg 21, .pos 22, .neg 122]
private def clause017 : Sat.Clause := [.neg 10, .neg 12, .neg 21, .pos 23, .neg 122]
private def clause018 : Sat.Clause := [.neg 10, .neg 13, .neg 21, .pos 24, .neg 122]
private def clause019 : Sat.Clause := [.neg 10, .pos 15, .neg 28]
private def clause020 : Sat.Clause := [.neg 10, .pos 18, .neg 32]
private def clause021 : Sat.Clause := [.neg 10, .neg 11, .neg 32, .pos 35, .neg 125]
private def clause022 : Sat.Clause := [.neg 10, .pos 19, .neg 36]
private def clause023 : Sat.Clause := [.neg 15, .neg 67, .pos 68, .pos 132]
private def clause024 : Sat.Clause := [.neg 15, .pos 19, .neg 71]
private def clause025 : Sat.Clause := [.pos 15, .neg 16, .pos 64]
private def clause026 : Sat.Clause := [.neg 18, .neg 89, .pos 90, .pos 137]
private def clause027 : Sat.Clause := [.pos 16, .neg 19, .pos 73]
private def clause028 : Sat.Clause := [.neg 21, .pos 28, .neg 38]
private def clause029 : Sat.Clause := [.neg 21, .neg 22, .neg 38, .pos 39, .neg 140]
private def clause030 : Sat.Clause := [.neg 21, .neg 23, .neg 38, .pos 40, .neg 140]
private def clause031 : Sat.Clause := [.neg 21, .neg 24, .neg 38, .pos 41, .neg 140]
private def clause032 : Sat.Clause := [.neg 21, .pos 36, .neg 44]
private def clause033 : Sat.Clause := [.neg 25, .pos 27, .neg 45]
private def clause034 : Sat.Clause := [.neg 25, .neg 45, .pos 47, .neg 144]
private def clause035 : Sat.Clause := [.neg 25, .pos 30, .neg 49]
private def clause036 : Sat.Clause := [.neg 25, .pos 31, .neg 50]
private def clause037 : Sat.Clause := [.neg 27, .pos 30, .neg 55]
private def clause038 : Sat.Clause := [.neg 27, .pos 31, .neg 58]
private def clause039 : Sat.Clause := [.pos 21, .neg 28, .pos 38]
private def clause040 : Sat.Clause := [.pos 25, .neg 28, .pos 48]
private def clause041 : Sat.Clause := [.neg 28, .pos 29, .neg 64]
private def clause042 : Sat.Clause := [.neg 28, .pos 30, .neg 65]
private def clause043 : Sat.Clause := [.neg 28, .pos 31, .neg 66]
private def clause044 : Sat.Clause := [.neg 28, .pos 32, .neg 67]
private def clause045 : Sat.Clause := [.neg 28, .neg 67, .pos 68, .pos 156]
private def clause046 : Sat.Clause := [.neg 28, .pos 36, .neg 71]
private def clause047 : Sat.Clause := [.pos 21, .neg 29, .pos 42]
private def clause048 : Sat.Clause := [.pos 28, .neg 29, .pos 64]
private def clause049 : Sat.Clause := [.neg 29, .pos 36, .neg 73]
private def clause050 : Sat.Clause := [.neg 30, .pos 31, .neg 76]
private def clause051 : Sat.Clause := [.pos 25, .neg 31, .pos 50]
private def clause052 : Sat.Clause := [.pos 25, .neg 32, .pos 51]
private def clause053 : Sat.Clause := [.pos 27, .neg 32, .pos 59]
private def clause054 : Sat.Clause := [.pos 30, .neg 32, .pos 79]
private def clause055 : Sat.Clause := [.pos 31, .neg 32, .pos 83]
private def clause056 : Sat.Clause := [.neg 32, .pos 36, .neg 89]
private def clause057 : Sat.Clause := [.neg 32, .neg 89, .pos 90, .pos 168]
private def clause058 : Sat.Clause := [.neg 32, .neg 33, .neg 89, .pos 91, .pos 168]
private def clause059 : Sat.Clause := [.neg 32, .neg 34, .neg 89, .pos 92, .pos 168]
private def clause060 : Sat.Clause := [.neg 32, .neg 35, .neg 89, .pos 93, .neg 168]
private def clause061 : Sat.Clause := [.neg 32, .pos 37, .neg 96]
private def clause062 : Sat.Clause := [.pos 28, .neg 36, .pos 71]
private def clause063 : Sat.Clause := [.pos 31, .neg 36, .pos 85]
private def clause064 : Sat.Clause := [.pos 32, .neg 36, .pos 89]
private def clause065 : Sat.Clause := [.pos 25, .neg 37, .pos 54]
private def clause066 : Sat.Clause := [.pos 31, .neg 37, .pos 86]
private def clause067 : Sat.Clause := [.neg 38, .pos 43, .neg 67]
private def clause068 : Sat.Clause := [.neg 38, .neg 39, .neg 67, .pos 69, .neg 172]
private def clause069 : Sat.Clause := [.neg 38, .neg 40, .neg 67, .pos 70, .neg 172]
private def clause070 : Sat.Clause := [.neg 38, .neg 41, .neg 67, .neg 172]
private def clause071 : Sat.Clause := [.neg 38, .pos 44, .neg 71]
private def clause072 : Sat.Clause := [.pos 38, .neg 42, .pos 64]
private def clause073 : Sat.Clause := [.neg 42, .pos 44, .neg 73]
private def clause074 : Sat.Clause := [.pos 42, .neg 43, .pos 72]
private def clause075 : Sat.Clause := [.neg 43, .neg 89, .pos 90, .pos 176]
private def clause076 : Sat.Clause := [.pos 43, .neg 44, .pos 89]
private def clause077 : Sat.Clause := [.pos 25, .neg 32, .pos 33, .neg 147]
private def clause078 : Sat.Clause := [.pos 25, .neg 26, .neg 32, .pos 34, .neg 147]
private def clause079 : Sat.Clause := [.neg 45, .pos 49, .neg 55]
private def clause080 : Sat.Clause := [.neg 45, .neg 55, .pos 57, .neg 177]
private def clause081 : Sat.Clause := [.neg 45, .pos 50, .neg 58]
private def clause082 : Sat.Clause := [.neg 45, .pos 51, .neg 59]
private def clause083 : Sat.Clause := [.neg 45, .neg 47, .neg 59, .pos 61, .neg 179]
private def clause084 : Sat.Clause := [.neg 45, .pos 53, .neg 62]
private def clause085 : Sat.Clause := [.neg 45, .pos 54, .neg 63]
private def clause086 : Sat.Clause := [.neg 48, .pos 51, .neg 67]
private def clause087 : Sat.Clause := [.neg 48, .pos 53, .neg 71]
private def clause088 : Sat.Clause := [.pos 45, .neg 49, .pos 55]
private def clause089 : Sat.Clause := [.neg 49, .pos 50, .neg 76]
private def clause090 : Sat.Clause := [.neg 49, .pos 51, .neg 79]
private def clause091 : Sat.Clause := [.neg 49, .pos 54, .neg 82]
private def clause092 : Sat.Clause := [.pos 45, .neg 50, .pos 58]
private def clause093 : Sat.Clause := [.pos 49, .neg 51, .pos 79]
private def clause094 : Sat.Clause := [.pos 50, .neg 51, .pos 83]
private def clause095 : Sat.Clause := [.neg 51, .pos 53, .neg 89]
private def clause096 : Sat.Clause := [.neg 51, .pos 54, .neg 96]
private def clause097 : Sat.Clause := [.neg 51, .neg 52, .neg 96, .pos 190]
private def clause098 : Sat.Clause := [.neg 53, .pos 54, .neg 98]
private def clause099 : Sat.Clause := [.pos 45, .neg 54, .pos 63]
private def clause100 : Sat.Clause := [.pos 49, .neg 54, .pos 82]
private def clause101 : Sat.Clause := [.pos 50, .neg 54, .pos 86]
private def clause102 : Sat.Clause := [.pos 25, .pos 26, .pos 45, .neg 144]
private def clause103 : Sat.Clause := [.pos 45, .neg 46, .neg 51, .pos 52, .neg 179]
private def clause104 : Sat.Clause := [.neg 55, .pos 58, .neg 76]
private def clause105 : Sat.Clause := [.neg 55, .neg 57, .neg 76, .pos 78, .neg 192]
private def clause106 : Sat.Clause := [.neg 55, .pos 59, .neg 79]
private def clause107 : Sat.Clause := [.neg 55, .neg 57, .neg 79, .pos 80, .neg 193]
private def clause108 : Sat.Clause := [.neg 55, .pos 62, .neg 81]
private def clause109 : Sat.Clause := [.neg 55, .pos 63, .neg 82]
private def clause110 : Sat.Clause := [.pos 58, .neg 59, .pos 83]
private def clause111 : Sat.Clause := [.neg 59, .pos 62, .neg 89]
private def clause112 : Sat.Clause := [.neg 59, .neg 60, .neg 89, .pos 91, .pos 199]
private def clause113 : Sat.Clause := [.neg 59, .neg 61, .neg 89, .pos 93, .neg 199]
private def clause114 : Sat.Clause := [.neg 59, .pos 63, .neg 96]
private def clause115 : Sat.Clause := [.pos 59, .neg 62, .pos 89]
private def clause116 : Sat.Clause := [.neg 62, .pos 63, .neg 98]
private def clause117 : Sat.Clause := [.pos 58, .neg 63, .pos 86]
private def clause118 : Sat.Clause := [.neg 64, .pos 71, .neg 73]
private def clause119 : Sat.Clause := [.pos 65, .neg 67, .pos 79]
private def clause120 : Sat.Clause := [.pos 66, .neg 67, .pos 83]
private def clause121 : Sat.Clause := [.neg 67, .pos 71, .neg 89]
private def clause122 : Sat.Clause := [.neg 67, .neg 89, .pos 90, .pos 205]
private def clause123 : Sat.Clause := [.neg 67, .neg 68, .neg 89, .pos 91, .pos 205]
private def clause124 : Sat.Clause := [.neg 67, .neg 69, .neg 89, .pos 95, .neg 205]
private def clause125 : Sat.Clause := [.neg 67, .neg 70, .neg 89, .neg 205]
private def clause126 : Sat.Clause := [.neg 67, .neg 96, .pos 97, .pos 206]
private def clause127 : Sat.Clause := [.pos 64, .neg 71, .pos 73]
private def clause128 : Sat.Clause := [.neg 0, .pos 1, .pos 6, .neg 104]
private def clause129 : Sat.Clause := [.neg 0, .pos 2, .pos 6, .neg 7, .neg 104]
private def clause130 : Sat.Clause := [.neg 10, .pos 13, .pos 16, .neg 17, .neg 124]
private def clause131 : Sat.Clause := [.neg 72, .pos 73, .neg 89]
private def clause132 : Sat.Clause := [.pos 72, .neg 73, .pos 89]
private def clause133 : Sat.Clause := [.neg 73, .pos 75, .neg 98]
private def clause134 : Sat.Clause := [.pos 45, .pos 46, .pos 55, .neg 56, .neg 177]
private def clause135 : Sat.Clause := [.pos 55, .neg 59, .pos 60, .neg 193]
private def clause136 : Sat.Clause := [.neg 76, .neg 78, .neg 83, .pos 84, .neg 211]
private def clause137 : Sat.Clause := [.neg 76, .pos 81, .neg 85]
private def clause138 : Sat.Clause := [.pos 76, .neg 79, .pos 83]
private def clause139 : Sat.Clause := [.neg 79, .pos 81, .neg 89]
private def clause140 : Sat.Clause := [.neg 79, .neg 80, .neg 89, .pos 93, .neg 214]
private def clause141 : Sat.Clause := [.neg 79, .pos 82, .neg 96]
private def clause142 : Sat.Clause := [.neg 81, .pos 82, .neg 98]
private def clause143 : Sat.Clause := [.pos 55, .pos 56, .pos 76, .neg 192]
private def clause144 : Sat.Clause := [.pos 55, .pos 76, .neg 77, .neg 192]
private def clause145 : Sat.Clause := [.neg 83, .pos 85, .neg 89]
private def clause146 : Sat.Clause := [.neg 83, .neg 84, .neg 89, .pos 94, .neg 217]
private def clause147 : Sat.Clause := [.neg 83, .pos 86, .neg 96]
private def clause148 : Sat.Clause := [.neg 85, .pos 86, .neg 98]
private def clause149 : Sat.Clause := [.pos 73, .neg 89, .neg 95, .neg 208]
private def clause150 : Sat.Clause := [.neg 89, .neg 90, .neg 98, .pos 99, .pos 220]
private def clause151 : Sat.Clause := [.neg 89, .neg 91, .neg 98, .pos 100, .pos 220]
private def clause152 : Sat.Clause := [.neg 89, .neg 92, .neg 98, .pos 220]
private def clause153 : Sat.Clause := [.pos 86, .pos 87, .neg 96, .neg 97, .pos 218]
private def clause154 : Sat.Clause := [.pos 6, .pos 7, .pos 73, .pos 120]
private def clause155 : Sat.Clause := [.pos 16, .pos 17, .pos 73, .neg 74, .pos 135]
private def clause156 : Sat.Clause := [.pos 86, .pos 88, .neg 98, .neg 99, .pos 219]
private def clause157 : Sat.Clause := [.pos 86, .neg 98, .neg 100, .pos 219]
private def clause158 : Sat.Clause := [.pos 50, .pos 86, .neg 88, .neg 188]
private def clause159 : Sat.Clause := [.pos 58, .pos 86, .neg 88, .neg 198]
private def clause160 : Sat.Clause := [.pos 76, .pos 77, .pos 86, .neg 87, .neg 213]
private def clause161 : Sat.Clause := [.pos 76, .pos 86, .neg 88, .neg 213]
private def clause162 : Sat.Clause := [.neg 0, .neg 10, .neg 21, .neg 101, .pos 102, .pos 107, .neg 122]
private def clause163 : Sat.Clause := [.neg 0, .neg 10, .neg 21, .neg 101, .pos 102, .neg 107, .neg 122]
private def clause164 : Sat.Clause := [.neg 0, .neg 10, .neg 21, .neg 101, .neg 102, .pos 107, .neg 122]
private def clause165 : Sat.Clause := [.neg 101, .neg 102, .neg 107, .neg 122, .pos 221]
private def clause166 : Sat.Clause := [.neg 101, .neg 103, .neg 108, .neg 123, .pos 222]
private def clause167 : Sat.Clause := [.neg 0, .neg 10, .neg 29, .neg 101, .neg 104, .pos 109, .neg 124]
private def clause168 : Sat.Clause := [.neg 3, .pos 10, .neg 16, .neg 101, .neg 104, .pos 109, .neg 124]
private def clause169 : Sat.Clause := [.neg 3, .pos 10, .neg 16, .neg 101, .neg 104, .neg 109, .neg 124]
private def clause170 : Sat.Clause := [.neg 0, .pos 3, .neg 16, .neg 101, .neg 104, .neg 109, .neg 124]
private def clause171 : Sat.Clause := [.neg 0, .pos 3, .neg 16, .neg 101, .neg 104, .pos 109, .neg 124]
private def clause172 : Sat.Clause := [.neg 0, .pos 6, .neg 10, .neg 101, .neg 104, .pos 109, .neg 124]
private def clause173 : Sat.Clause := [.neg 101, .neg 104, .neg 109, .neg 124, .pos 223]
private def clause174 : Sat.Clause := [.neg 101, .neg 105, .neg 110, .neg 125, .pos 224]
private def clause175 : Sat.Clause := [.neg 101, .neg 106, .neg 111, .neg 126, .pos 225]
private def clause176 : Sat.Clause := [.neg 0, .neg 14, .neg 38, .neg 102, .pos 103, .neg 112, .neg 127]
private def clause177 : Sat.Clause := [.neg 102, .neg 103, .neg 112, .neg 127, .pos 226]
private def clause178 : Sat.Clause := [.neg 6, .neg 14, .pos 16, .neg 102, .neg 104, .neg 113, .pos 128]
private def clause179 : Sat.Clause := [.neg 6, .neg 14, .pos 16, .neg 102, .neg 104, .pos 113, .pos 128]
private def clause180 : Sat.Clause := [.neg 0, .pos 6, .neg 14, .neg 102, .neg 104, .pos 113, .neg 128]
private def clause181 : Sat.Clause := [.neg 102, .neg 104, .neg 113, .neg 128, .pos 227]
private def clause182 : Sat.Clause := [.neg 0, .pos 4, .neg 18, .neg 102, .neg 105, .neg 114, .neg 129]
private def clause183 : Sat.Clause := [.neg 102, .neg 105, .neg 114, .neg 129, .pos 228]
private def clause184 : Sat.Clause := [.neg 102, .neg 106, .neg 115, .neg 130, .pos 229]
private def clause185 : Sat.Clause := [.neg 0, .neg 16, .pos 64, .neg 103, .neg 104, .neg 116, .pos 131]
private def clause186 : Sat.Clause := [.neg 103, .neg 104, .neg 116, .neg 131, .pos 230]
private def clause187 : Sat.Clause := [.neg 0, .neg 15, .neg 67, .neg 103, .pos 105, .neg 117, .neg 132]
private def clause188 : Sat.Clause := [.neg 103, .neg 105, .neg 117, .neg 132, .pos 231]
private def clause189 : Sat.Clause := [.neg 0, .neg 19, .pos 71, .neg 103, .pos 106, .neg 118, .neg 133]
private def clause190 : Sat.Clause := [.neg 103, .neg 106, .neg 118, .neg 133, .pos 232]
private def clause191 : Sat.Clause := [.neg 0, .neg 16, .neg 72, .neg 104, .neg 105, .pos 119, .neg 134]
private def clause192 : Sat.Clause := [.neg 104, .neg 105, .pos 119, .pos 134, .pos 233]
private def clause193 : Sat.Clause := [.neg 6, .pos 19, .neg 73, .neg 104, .pos 106, .pos 120, .pos 135]
private def clause194 : Sat.Clause := [.neg 0, .pos 9, .neg 73, .neg 104, .pos 106, .pos 120, .pos 135]
private def clause195 : Sat.Clause := [.neg 6, .pos 9, .pos 16, .neg 104, .pos 106, .pos 120, .pos 135]
private def clause196 : Sat.Clause := [.neg 6, .pos 9, .pos 16, .neg 104, .neg 106, .pos 120, .pos 135]
private def clause197 : Sat.Clause := [.neg 104, .neg 106, .pos 120, .pos 135, .pos 234]
private def clause198 : Sat.Clause := [.neg 0, .neg 18, .neg 89, .neg 105, .pos 106, .neg 121, .neg 137]
private def clause199 : Sat.Clause := [.neg 0, .neg 19, .pos 89, .neg 105, .pos 106, .neg 121, .neg 137]
private def clause200 : Sat.Clause := [.neg 9, .neg 18, .pos 19, .neg 105, .pos 106, .neg 121, .neg 137]
private def clause201 : Sat.Clause := [.pos 105, .neg 106, .neg 121, .neg 137, .neg 235]
private def clause202 : Sat.Clause := [.neg 105, .pos 106, .neg 121, .neg 137, .neg 235]
private def clause203 : Sat.Clause := [.neg 105, .neg 106, .neg 121, .neg 137, .pos 235]
private def clause204 : Sat.Clause := [.neg 3, .neg 21, .neg 38, .neg 107, .pos 108, .pos 112, .neg 140]
private def clause205 : Sat.Clause := [.neg 3, .neg 21, .neg 38, .neg 107, .pos 108, .neg 112, .neg 140]
private def clause206 : Sat.Clause := [.neg 3, .neg 21, .neg 38, .neg 107, .neg 108, .pos 112, .neg 140]
private def clause207 : Sat.Clause := [.neg 107, .neg 108, .neg 112, .neg 140, .pos 236]
private def clause208 : Sat.Clause := [.neg 3, .neg 21, .neg 42, .neg 107, .neg 109, .pos 113, .neg 141]
private def clause209 : Sat.Clause := [.neg 3, .pos 6, .neg 21, .neg 107, .neg 109, .pos 113, .neg 141]
private def clause210 : Sat.Clause := [.neg 107, .neg 109, .neg 113, .neg 141, .pos 237]
private def clause211 : Sat.Clause := [.neg 107, .neg 110, .neg 114, .neg 142, .pos 238]
private def clause212 : Sat.Clause := [.neg 107, .neg 111, .neg 115, .neg 143, .pos 239]
private def clause213 : Sat.Clause := [.neg 6, .neg 28, .pos 29, .neg 108, .pos 109, .neg 116, .neg 155]
private def clause214 : Sat.Clause := [.neg 3, .pos 6, .neg 28, .neg 108, .neg 109, .pos 116, .neg 155]
private def clause215 : Sat.Clause := [.neg 108, .neg 109, .neg 116, .neg 155, .pos 240]
private def clause216 : Sat.Clause := [.neg 3, .neg 28, .neg 67, .neg 108, .pos 110, .pos 117, .neg 156]
private def clause217 : Sat.Clause := [.neg 3, .neg 28, .neg 67, .neg 108, .pos 110, .neg 117, .neg 156]
private def clause218 : Sat.Clause := [.neg 3, .neg 28, .neg 67, .neg 108, .neg 110, .pos 117, .neg 156]
private def clause219 : Sat.Clause := [.neg 108, .neg 110, .neg 117, .neg 156, .pos 241]
private def clause220 : Sat.Clause := [.neg 3, .neg 28, .neg 71, .neg 108, .pos 111, .neg 118, .neg 157]
private def clause221 : Sat.Clause := [.pos 108, .neg 111, .neg 118, .neg 157, .neg 242]
private def clause222 : Sat.Clause := [.neg 108, .neg 111, .neg 118, .neg 157, .pos 242]
private def clause223 : Sat.Clause := [.neg 3, .neg 29, .neg 72, .neg 109, .neg 110, .pos 119, .neg 158]
private def clause224 : Sat.Clause := [.neg 3, .pos 6, .neg 32, .neg 109, .pos 110, .neg 119, .pos 158]
private def clause225 : Sat.Clause := [.neg 3, .pos 6, .neg 32, .neg 109, .neg 110, .neg 119, .pos 158]
private def clause226 : Sat.Clause := [.neg 109, .neg 110, .pos 119, .pos 158, .pos 243]
private def clause227 : Sat.Clause := [.neg 3, .pos 9, .neg 73, .neg 109, .pos 111, .pos 120, .pos 159]
private def clause228 : Sat.Clause := [.pos 109, .neg 111, .pos 120, .pos 159, .neg 244]
private def clause229 : Sat.Clause := [.neg 109, .neg 111, .pos 120, .pos 159, .pos 244]
private def clause230 : Sat.Clause := [.neg 3, .neg 36, .pos 89, .neg 110, .pos 111, .neg 121, .neg 168]
private def clause231 : Sat.Clause := [.neg 9, .neg 32, .pos 36, .neg 110, .pos 111, .neg 121, .neg 168]
private def clause232 : Sat.Clause := [.pos 110, .neg 111, .neg 121, .neg 168, .neg 245]
private def clause233 : Sat.Clause := [.neg 110, .neg 111, .neg 121, .neg 168, .pos 245]
private def clause234 : Sat.Clause := [.neg 4, .neg 38, .neg 64, .neg 112, .neg 113, .pos 116, .neg 171]
private def clause235 : Sat.Clause := [.neg 6, .neg 38, .pos 42, .neg 112, .pos 113, .neg 116, .neg 171]
private def clause236 : Sat.Clause := [.neg 4, .pos 6, .neg 38, .neg 112, .neg 113, .pos 116, .neg 171]
private def clause237 : Sat.Clause := [.neg 112, .neg 113, .neg 116, .neg 171, .pos 246]
private def clause238 : Sat.Clause := [.neg 4, .neg 38, .neg 67, .neg 112, .pos 114, .neg 117, .neg 172]
private def clause239 : Sat.Clause := [.neg 112, .neg 114, .neg 117, .neg 172, .pos 247]
private def clause240 : Sat.Clause := [.neg 4, .neg 38, .neg 71, .neg 112, .pos 115, .neg 118, .neg 173]
private def clause241 : Sat.Clause := [.pos 112, .neg 115, .neg 118, .neg 173, .neg 248]
private def clause242 : Sat.Clause := [.neg 112, .neg 115, .neg 118, .neg 173, .pos 248]
private def clause243 : Sat.Clause := [.neg 113, .neg 114, .pos 119, .pos 174, .pos 249]
private def clause244 : Sat.Clause := [.neg 113, .neg 114, .neg 119, .pos 174, .neg 249]
private def clause245 : Sat.Clause := [.neg 6, .pos 44, .neg 73, .neg 113, .pos 115, .pos 120, .pos 175]
private def clause246 : Sat.Clause := [.pos 6, .neg 9, .pos 44, .neg 113, .pos 115, .pos 120, .pos 175]
private def clause247 : Sat.Clause := [.neg 4, .pos 9, .neg 73, .neg 113, .pos 115, .pos 120, .pos 175]
private def clause248 : Sat.Clause := [.pos 113, .neg 115, .pos 120, .pos 175, .neg 250]
private def clause249 : Sat.Clause := [.neg 113, .neg 115, .pos 120, .pos 175, .pos 250]
private def clause250 : Sat.Clause := [.neg 4, .neg 43, .neg 89, .neg 114, .pos 115, .neg 121, .neg 176]
private def clause251 : Sat.Clause := [.neg 4, .neg 44, .pos 89, .neg 114, .pos 115, .neg 121, .neg 176]
private def clause252 : Sat.Clause := [.neg 4, .pos 9, .neg 43, .neg 114, .neg 115, .pos 121, .neg 176]
private def clause253 : Sat.Clause := [.neg 114, .neg 115, .neg 121, .neg 176, .pos 251]
private def clause254 : Sat.Clause := [.neg 5, .neg 64, .neg 72, .pos 116, .neg 117, .pos 119, .pos 202]
private def clause255 : Sat.Clause := [.neg 5, .neg 67, .pos 72, .pos 116, .neg 117, .pos 119, .pos 202]
private def clause256 : Sat.Clause := [.neg 6, .pos 64, .neg 67, .pos 116, .neg 117, .pos 119, .pos 202]
private def clause257 : Sat.Clause := [.neg 116, .pos 117, .pos 119, .pos 202, .neg 252]
private def clause258 : Sat.Clause := [.neg 116, .neg 117, .pos 119, .pos 202, .pos 252]
private def clause259 : Sat.Clause := [.neg 6, .pos 71, .neg 73, .neg 116, .pos 118, .pos 120, .pos 203]
private def clause260 : Sat.Clause := [.pos 6, .neg 9, .pos 71, .neg 116, .pos 118, .pos 120, .pos 203]
private def clause261 : Sat.Clause := [.neg 5, .pos 9, .neg 73, .neg 116, .pos 118, .pos 120, .pos 203]
private def clause262 : Sat.Clause := [.pos 116, .neg 118, .pos 120, .pos 203, .neg 253]
private def clause263 : Sat.Clause := [.neg 116, .neg 118, .pos 120, .pos 203, .pos 253]
private def clause264 : Sat.Clause := [.neg 5, .neg 67, .neg 89, .neg 117, .pos 118, .neg 121, .neg 205]
private def clause265 : Sat.Clause := [.neg 5, .neg 71, .pos 89, .neg 117, .pos 118, .neg 121, .neg 205]
private def clause266 : Sat.Clause := [.neg 117, .pos 118, .neg 121, .neg 205, .neg 254]
private def clause267 : Sat.Clause := [.neg 117, .neg 118, .neg 121, .neg 205, .pos 254]
private def clause268 : Sat.Clause := [.neg 6, .neg 72, .neg 89, .neg 119, .pos 120, .neg 121, .neg 208]
private def clause269 : Sat.Clause := [.neg 6, .neg 73, .pos 89, .pos 119, .pos 120, .pos 121, .neg 208]
private def clause270 : Sat.Clause := [.neg 6, .neg 73, .pos 89, .neg 119, .pos 120, .neg 121, .neg 208]
private def clause271 : Sat.Clause := [.neg 6, .neg 73, .pos 89, .neg 119, .pos 120, .pos 121, .neg 208]
private def clause272 : Sat.Clause := [.neg 8, .pos 72, .neg 73, .neg 119, .pos 120, .neg 121, .neg 208]
private def clause273 : Sat.Clause := [.pos 6, .neg 9, .pos 89, .pos 119, .pos 120, .pos 121, .neg 208]
private def clause274 : Sat.Clause := [.pos 119, .pos 120, .neg 121, .neg 208, .pos 255]
private def clause275 : Sat.Clause := [.neg 119, .pos 120, .neg 121, .neg 208, .neg 255]
private def clause276 : Sat.Clause := [.neg 10, .neg 21, .neg 38, .neg 122, .pos 123, .pos 127, .neg 140]
private def clause277 : Sat.Clause := [.neg 10, .neg 21, .neg 38, .neg 122, .pos 123, .neg 127, .neg 140]
private def clause278 : Sat.Clause := [.neg 10, .neg 21, .neg 38, .neg 122, .neg 123, .pos 127, .neg 140]
private def clause279 : Sat.Clause := [.neg 122, .neg 123, .neg 127, .neg 140, .pos 256]
private def clause280 : Sat.Clause := [.neg 10, .neg 21, .neg 42, .neg 122, .neg 124, .pos 128, .neg 141]
private def clause281 : Sat.Clause := [.neg 14, .pos 21, .neg 29, .neg 122, .neg 124, .pos 128, .neg 141]
private def clause282 : Sat.Clause := [.neg 14, .pos 21, .neg 29, .neg 122, .neg 124, .neg 128, .neg 141]
private def clause283 : Sat.Clause := [.neg 10, .pos 14, .neg 29, .neg 122, .neg 124, .neg 128, .neg 141]
private def clause284 : Sat.Clause := [.neg 10, .pos 14, .neg 29, .neg 122, .neg 124, .pos 128, .neg 141]
private def clause285 : Sat.Clause := [.neg 10, .pos 16, .neg 21, .neg 122, .neg 124, .pos 128, .neg 141]
private def clause286 : Sat.Clause := [.pos 10, .neg 14, .pos 29, .neg 122, .neg 124, .pos 128, .neg 141]
private def clause287 : Sat.Clause := [.pos 10, .neg 14, .pos 29, .neg 122, .neg 124, .neg 128, .neg 141]
private def clause288 : Sat.Clause := [.pos 14, .neg 21, .pos 29, .neg 122, .neg 124, .neg 128, .neg 141]
private def clause289 : Sat.Clause := [.pos 14, .neg 21, .pos 29, .neg 122, .neg 124, .pos 128, .neg 141]
private def clause290 : Sat.Clause := [.neg 122, .neg 124, .neg 128, .neg 141, .pos 257]
private def clause291 : Sat.Clause := [.neg 10, .neg 21, .neg 43, .neg 122, .neg 125, .pos 129, .neg 142]
private def clause292 : Sat.Clause := [.neg 122, .pos 125, .neg 129, .neg 142, .neg 258]
private def clause293 : Sat.Clause := [.neg 122, .neg 125, .neg 129, .pos 142, .neg 258]
private def clause294 : Sat.Clause := [.neg 122, .neg 125, .neg 129, .neg 142, .pos 258]
private def clause295 : Sat.Clause := [.neg 10, .neg 36, .pos 44, .neg 122, .neg 126, .neg 130, .pos 143]
private def clause296 : Sat.Clause := [.neg 122, .neg 126, .pos 130, .neg 143, .neg 259]
private def clause297 : Sat.Clause := [.neg 122, .neg 126, .neg 130, .pos 143, .neg 259]
private def clause298 : Sat.Clause := [.neg 122, .neg 126, .neg 130, .neg 143, .pos 259]
private def clause299 : Sat.Clause := [.neg 10, .pos 16, .neg 28, .neg 123, .neg 124, .pos 131, .neg 155]
private def clause300 : Sat.Clause := [.neg 123, .neg 124, .neg 131, .pos 155, .neg 260]
private def clause301 : Sat.Clause := [.neg 123, .neg 124, .neg 131, .neg 155, .pos 260]
private def clause302 : Sat.Clause := [.neg 10, .neg 28, .neg 67, .neg 123, .pos 125, .pos 132, .neg 156]
private def clause303 : Sat.Clause := [.neg 10, .neg 28, .neg 67, .neg 123, .pos 125, .neg 132, .neg 156]
private def clause304 : Sat.Clause := [.neg 10, .neg 28, .neg 67, .neg 123, .neg 125, .pos 132, .neg 156]
private def clause305 : Sat.Clause := [.neg 15, .pos 28, .neg 32, .neg 123, .neg 125, .neg 132, .neg 156]
private def clause306 : Sat.Clause := [.neg 15, .pos 18, .neg 32, .neg 123, .neg 125, .neg 132, .neg 156]
private def clause307 : Sat.Clause := [.neg 123, .neg 125, .pos 132, .neg 156, .neg 261]
private def clause308 : Sat.Clause := [.neg 123, .neg 125, .neg 132, .neg 156, .pos 261]
private def clause309 : Sat.Clause := [.neg 10, .pos 19, .neg 28, .neg 123, .neg 126, .pos 133, .neg 157]
private def clause310 : Sat.Clause := [.pos 123, .neg 126, .neg 133, .neg 157, .neg 262]
private def clause311 : Sat.Clause := [.neg 123, .pos 126, .neg 133, .neg 157, .neg 262]
private def clause312 : Sat.Clause := [.neg 123, .neg 126, .neg 133, .neg 157, .pos 262]
private def clause313 : Sat.Clause := [.neg 10, .pos 16, .neg 32, .neg 124, .neg 125, .neg 134, .pos 158]
private def clause314 : Sat.Clause := [.neg 124, .pos 125, .pos 134, .pos 158, .neg 263]
private def clause315 : Sat.Clause := [.neg 124, .neg 125, .pos 134, .pos 158, .pos 263]
private def clause316 : Sat.Clause := [.neg 16, .pos 36, .neg 73, .neg 124, .pos 126, .pos 135, .pos 159]
private def clause317 : Sat.Clause := [.neg 19, .pos 29, .pos 73, .neg 124, .neg 126, .pos 135, .pos 159]
private def clause318 : Sat.Clause := [.neg 19, .pos 29, .pos 73, .neg 124, .pos 126, .pos 135, .pos 159]
private def clause319 : Sat.Clause := [.pos 16, .neg 19, .neg 29, .neg 124, .neg 126, .pos 135, .pos 159]
private def clause320 : Sat.Clause := [.pos 16, .neg 19, .neg 29, .neg 124, .pos 126, .pos 135, .pos 159]
private def clause321 : Sat.Clause := [.pos 19, .neg 29, .neg 73, .neg 124, .pos 126, .pos 135, .pos 159]
private def clause322 : Sat.Clause := [.pos 19, .neg 29, .neg 73, .neg 124, .neg 126, .pos 135, .pos 159]
private def clause323 : Sat.Clause := [.pos 16, .neg 19, .pos 36, .neg 124, .pos 126, .pos 135, .pos 159]
private def clause324 : Sat.Clause := [.neg 10, .pos 19, .neg 73, .neg 124, .pos 126, .pos 135, .pos 159]
private def clause325 : Sat.Clause := [.neg 16, .pos 19, .pos 29, .neg 124, .pos 126, .pos 135, .pos 159]
private def clause326 : Sat.Clause := [.neg 16, .pos 19, .pos 29, .neg 124, .neg 126, .pos 135, .pos 159]
private def clause327 : Sat.Clause := [.neg 124, .neg 126, .pos 135, .pos 159, .pos 264]
private def clause328 : Sat.Clause := [.neg 10, .neg 32, .neg 89, .neg 125, .pos 126, .neg 137, .neg 168]
private def clause329 : Sat.Clause := [.neg 10, .neg 36, .pos 89, .neg 125, .pos 126, .neg 137, .neg 168]
private def clause330 : Sat.Clause := [.neg 125, .neg 126, .neg 137, .neg 168, .pos 265]
private def clause331 : Sat.Clause := [.neg 14, .neg 38, .neg 64, .neg 127, .neg 128, .pos 131, .neg 171]
private def clause332 : Sat.Clause := [.neg 16, .neg 38, .pos 42, .neg 127, .pos 128, .neg 131, .neg 171]
private def clause333 : Sat.Clause := [.pos 14, .neg 15, .pos 42, .neg 127, .neg 128, .neg 131, .neg 171]
private def clause334 : Sat.Clause := [.pos 15, .neg 38, .pos 42, .neg 127, .neg 128, .neg 131, .neg 171]
private def clause335 : Sat.Clause := [.neg 127, .neg 128, .pos 131, .neg 171, .neg 266]
private def clause336 : Sat.Clause := [.neg 127, .neg 128, .neg 131, .neg 171, .pos 266]
private def clause337 : Sat.Clause := [.neg 127, .neg 129, .neg 132, .neg 172, .pos 267]
private def clause338 : Sat.Clause := [.neg 19, .neg 38, .pos 44, .neg 127, .neg 130, .neg 133, .pos 173]
private def clause339 : Sat.Clause := [.pos 127, .neg 130, .neg 133, .neg 173, .neg 268]
private def clause340 : Sat.Clause := [.neg 127, .neg 130, .neg 133, .neg 173, .pos 268]
private def clause341 : Sat.Clause := [.neg 128, .neg 129, .pos 134, .pos 174, .pos 269]
private def clause342 : Sat.Clause := [.neg 16, .pos 42, .neg 44, .pos 128, .pos 130, .pos 135, .pos 175]
private def clause343 : Sat.Clause := [.neg 16, .pos 42, .neg 44, .pos 128, .neg 130, .pos 135, .pos 175]
private def clause344 : Sat.Clause := [.neg 16, .pos 44, .neg 73, .neg 128, .pos 130, .pos 135, .pos 175]
private def clause345 : Sat.Clause := [.neg 16, .pos 44, .neg 73, .pos 128, .neg 130, .pos 135, .pos 175]
private def clause346 : Sat.Clause := [.pos 16, .neg 19, .pos 44, .neg 128, .pos 130, .pos 135, .pos 175]
private def clause347 : Sat.Clause := [.neg 14, .pos 19, .neg 73, .neg 128, .pos 130, .pos 135, .pos 175]
private def clause348 : Sat.Clause := [.pos 128, .pos 130, .pos 135, .pos 175, .pos 270]
private def clause349 : Sat.Clause := [.pos 128, .neg 130, .pos 135, .pos 175, .neg 270]
private def clause350 : Sat.Clause := [.neg 128, .pos 130, .pos 135, .pos 175, .neg 270]
private def clause351 : Sat.Clause := [.neg 128, .neg 130, .pos 135, .pos 175, .pos 270]
private def clause352 : Sat.Clause := [.neg 14, .neg 43, .neg 89, .neg 129, .pos 130, .neg 137, .neg 176]
private def clause353 : Sat.Clause := [.neg 14, .neg 44, .pos 89, .neg 129, .pos 130, .neg 137, .neg 176]
private def clause354 : Sat.Clause := [.neg 19, .neg 43, .pos 44, .neg 129, .neg 130, .neg 137, .pos 176]
private def clause355 : Sat.Clause := [.pos 129, .neg 130, .neg 137, .neg 176, .neg 271]
private def clause356 : Sat.Clause := [.neg 129, .neg 130, .neg 137, .neg 176, .pos 271]
private def clause357 : Sat.Clause := [.neg 16, .pos 64, .neg 67, .pos 131, .neg 132, .pos 134, .pos 202]
private def clause358 : Sat.Clause := [.neg 131, .neg 132, .pos 134, .pos 202, .pos 272]
private def clause359 : Sat.Clause := [.neg 131, .neg 132, .neg 134, .pos 202, .neg 272]
private def clause360 : Sat.Clause := [.neg 15, .neg 64, .neg 73, .pos 131, .neg 133, .pos 135, .pos 203]
private def clause361 : Sat.Clause := [.neg 16, .pos 71, .neg 73, .neg 131, .pos 133, .pos 135, .pos 203]
private def clause362 : Sat.Clause := [.pos 16, .neg 19, .pos 71, .neg 131, .pos 133, .pos 135, .pos 203]
private def clause363 : Sat.Clause := [.neg 131, .pos 133, .pos 135, .pos 203, .neg 273]
private def clause364 : Sat.Clause := [.neg 131, .neg 133, .pos 135, .pos 203, .pos 273]
private def clause365 : Sat.Clause := [.neg 15, .neg 67, .neg 89, .neg 132, .pos 133, .neg 137, .neg 205]
private def clause366 : Sat.Clause := [.neg 15, .neg 71, .pos 89, .neg 132, .pos 133, .neg 137, .neg 205]
private def clause367 : Sat.Clause := [.neg 15, .pos 19, .neg 67, .neg 132, .neg 133, .pos 137, .neg 205]
private def clause368 : Sat.Clause := [.neg 132, .neg 133, .pos 137, .neg 205, .neg 274]
private def clause369 : Sat.Clause := [.neg 132, .neg 133, .neg 137, .neg 205, .pos 274]
private def clause370 : Sat.Clause := [.neg 16, .neg 72, .neg 89, .neg 134, .pos 135, .neg 137, .neg 208]
private def clause371 : Sat.Clause := [.neg 16, .neg 73, .pos 89, .pos 134, .pos 135, .pos 137, .neg 208]
private def clause372 : Sat.Clause := [.neg 18, .pos 72, .neg 73, .neg 134, .pos 135, .neg 137, .neg 208]
private def clause373 : Sat.Clause := [.neg 18, .pos 19, .neg 73, .pos 134, .pos 135, .pos 137, .neg 208]
private def clause374 : Sat.Clause := [.pos 134, .pos 135, .neg 137, .neg 208, .pos 275]
private def clause375 : Sat.Clause := [.neg 134, .pos 135, .neg 137, .neg 208, .neg 275]
private def clause376 : Sat.Clause := [.neg 19, .pos 73, .neg 75, .pos 135, .neg 136, .pos 139, .neg 210]
private def clause377 : Sat.Clause := [.pos 16, .neg 20, .pos 73, .pos 135, .neg 136, .pos 139, .neg 210]
private def clause378 : Sat.Clause := [.pos 16, .neg 20, .pos 73, .pos 135, .pos 136, .pos 139, .neg 210]
private def clause379 : Sat.Clause := [.pos 20, .pos 73, .neg 75, .pos 135, .pos 136, .pos 139, .neg 210]
private def clause380 : Sat.Clause := [.pos 20, .pos 73, .neg 75, .pos 135, .neg 136, .pos 139, .neg 210]
private def clause381 : Sat.Clause := [.pos 16, .pos 75, .neg 98, .pos 135, .neg 136, .pos 139, .neg 210]
private def clause382 : Sat.Clause := [.pos 16, .pos 75, .neg 98, .pos 135, .pos 136, .pos 139, .neg 210]
private def clause383 : Sat.Clause := [.neg 19, .pos 89, .neg 96, .pos 137, .pos 138, .pos 139, .pos 220]
private def clause384 : Sat.Clause := [.neg 19, .pos 89, .neg 96, .pos 137, .neg 138, .pos 139, .pos 220]
private def clause385 : Sat.Clause := [.neg 28, .pos 38, .neg 42, .neg 140, .neg 141, .pos 155, .neg 171]
private def clause386 : Sat.Clause := [.neg 28, .pos 38, .neg 42, .neg 140, .neg 141, .neg 155, .neg 171]
private def clause387 : Sat.Clause := [.neg 21, .pos 28, .neg 42, .neg 140, .neg 141, .neg 155, .neg 171]
private def clause388 : Sat.Clause := [.neg 21, .pos 28, .neg 42, .neg 140, .neg 141, .pos 155, .neg 171]
private def clause389 : Sat.Clause := [.neg 21, .pos 29, .neg 38, .neg 140, .neg 141, .pos 155, .neg 171]
private def clause390 : Sat.Clause := [.pos 21, .neg 28, .pos 42, .neg 140, .neg 141, .pos 155, .neg 171]
private def clause391 : Sat.Clause := [.pos 21, .neg 28, .pos 42, .neg 140, .neg 141, .neg 155, .neg 171]
private def clause392 : Sat.Clause := [.pos 28, .neg 38, .pos 42, .neg 140, .neg 141, .neg 155, .neg 171]
private def clause393 : Sat.Clause := [.pos 28, .neg 38, .pos 42, .neg 140, .neg 141, .pos 155, .neg 171]
private def clause394 : Sat.Clause := [.neg 140, .neg 141, .pos 155, .neg 171, .neg 276]
private def clause395 : Sat.Clause := [.neg 140, .neg 141, .neg 155, .neg 171, .pos 276]
private def clause396 : Sat.Clause := [.neg 21, .neg 38, .neg 67, .neg 140, .pos 142, .pos 156, .neg 172]
private def clause397 : Sat.Clause := [.neg 21, .neg 38, .neg 67, .neg 140, .pos 142, .neg 156, .neg 172]
private def clause398 : Sat.Clause := [.neg 21, .neg 38, .neg 67, .neg 140, .neg 142, .pos 156, .neg 172]
private def clause399 : Sat.Clause := [.pos 21, .neg 28, .neg 67, .neg 140, .neg 142, .pos 156, .neg 172]
private def clause400 : Sat.Clause := [.pos 21, .neg 28, .neg 67, .neg 140, .pos 142, .pos 156, .neg 172]
private def clause401 : Sat.Clause := [.neg 140, .neg 142, .pos 156, .neg 172, .neg 277]
private def clause402 : Sat.Clause := [.neg 140, .neg 142, .neg 156, .neg 172, .pos 277]
private def clause403 : Sat.Clause := [.neg 21, .pos 36, .neg 38, .neg 140, .neg 143, .neg 157, .pos 173]
private def clause404 : Sat.Clause := [.neg 140, .pos 143, .neg 157, .neg 173, .neg 278]
private def clause405 : Sat.Clause := [.neg 140, .neg 143, .neg 157, .neg 173, .pos 278]
private def clause406 : Sat.Clause := [.neg 29, .pos 32, .neg 43, .neg 141, .pos 142, .neg 158, .pos 174]
private def clause407 : Sat.Clause := [.neg 29, .pos 32, .neg 43, .neg 141, .neg 142, .neg 158, .pos 174]
private def clause408 : Sat.Clause := [.neg 21, .pos 29, .neg 43, .neg 141, .neg 142, .neg 158, .pos 174]
private def clause409 : Sat.Clause := [.pos 21, .neg 29, .pos 43, .neg 141, .neg 142, .neg 158, .pos 174]
private def clause410 : Sat.Clause := [.pos 21, .neg 29, .pos 43, .neg 141, .pos 142, .neg 158, .pos 174]
private def clause411 : Sat.Clause := [.neg 141, .neg 142, .pos 158, .pos 174, .pos 279]
private def clause412 : Sat.Clause := [.neg 141, .neg 142, .pos 158, .neg 174, .neg 279]
private def clause413 : Sat.Clause := [.neg 36, .pos 42, .pos 73, .neg 141, .neg 143, .pos 159, .pos 175]
private def clause414 : Sat.Clause := [.neg 36, .pos 42, .pos 73, .neg 141, .pos 143, .pos 159, .pos 175]
private def clause415 : Sat.Clause := [.pos 29, .neg 36, .neg 42, .neg 141, .neg 143, .pos 159, .pos 175]
private def clause416 : Sat.Clause := [.pos 29, .neg 36, .neg 42, .neg 141, .pos 143, .pos 159, .pos 175]
private def clause417 : Sat.Clause := [.pos 36, .neg 42, .neg 73, .neg 141, .pos 143, .pos 159, .pos 175]
private def clause418 : Sat.Clause := [.pos 36, .neg 42, .neg 73, .neg 141, .neg 143, .pos 159, .pos 175]
private def clause419 : Sat.Clause := [.neg 21, .pos 36, .neg 73, .neg 141, .pos 143, .pos 159, .pos 175]
private def clause420 : Sat.Clause := [.neg 29, .pos 36, .pos 42, .neg 141, .pos 143, .pos 159, .pos 175]
private def clause421 : Sat.Clause := [.neg 29, .pos 36, .pos 42, .neg 141, .neg 143, .pos 159, .pos 175]
private def clause422 : Sat.Clause := [.neg 141, .neg 143, .pos 159, .pos 175, .pos 280]
private def clause423 : Sat.Clause := [.neg 21, .neg 43, .neg 89, .neg 142, .pos 143, .neg 168, .neg 176]
private def clause424 : Sat.Clause := [.neg 21, .neg 44, .pos 89, .neg 142, .pos 143, .neg 168, .neg 176]
private def clause425 : Sat.Clause := [.pos 32, .neg 44, .pos 89, .neg 142, .neg 143, .neg 168, .neg 176]
private def clause426 : Sat.Clause := [.pos 142, .neg 143, .neg 168, .neg 176, .neg 281]
private def clause427 : Sat.Clause := [.neg 142, .neg 143, .neg 168, .neg 176, .pos 281]
private def clause428 : Sat.Clause := [.neg 25, .neg 45, .neg 55, .neg 144, .pos 145, .pos 150, .neg 177]
private def clause429 : Sat.Clause := [.neg 25, .neg 45, .neg 55, .neg 144, .pos 145, .neg 150, .neg 177]
private def clause430 : Sat.Clause := [.neg 25, .neg 45, .neg 55, .neg 144, .neg 145, .pos 150, .neg 177]
private def clause431 : Sat.Clause := [.pos 25, .neg 27, .neg 55, .neg 144, .neg 145, .pos 150, .neg 177]
private def clause432 : Sat.Clause := [.neg 144, .neg 145, .pos 150, .neg 177, .neg 282]
private def clause433 : Sat.Clause := [.neg 144, .neg 145, .neg 150, .neg 177, .pos 282]
private def clause434 : Sat.Clause := [.neg 25, .neg 45, .neg 58, .neg 144, .pos 146, .neg 151, .pos 178]
private def clause435 : Sat.Clause := [.neg 25, .neg 45, .neg 58, .neg 144, .pos 146, .neg 151, .neg 178]
private def clause436 : Sat.Clause := [.neg 25, .neg 45, .neg 58, .neg 144, .neg 146, .pos 151, .neg 178]
private def clause437 : Sat.Clause := [.neg 25, .neg 50, .pos 58, .neg 144, .pos 146, .neg 151, .neg 178]
private def clause438 : Sat.Clause := [.neg 25, .neg 50, .pos 58, .neg 144, .pos 146, .pos 151, .neg 178]
private def clause439 : Sat.Clause := [.pos 25, .neg 27, .neg 58, .neg 144, .neg 146, .pos 151, .neg 178]
private def clause440 : Sat.Clause := [.pos 27, .neg 31, .neg 45, .neg 144, .neg 146, .pos 151, .neg 178]
private def clause441 : Sat.Clause := [.neg 144, .neg 146, .neg 151, .neg 178, .pos 283]
private def clause442 : Sat.Clause := [.neg 25, .neg 45, .neg 59, .neg 144, .neg 147, .pos 152, .neg 179]
private def clause443 : Sat.Clause := [.neg 27, .pos 45, .neg 51, .neg 144, .neg 147, .pos 152, .neg 179]
private def clause444 : Sat.Clause := [.neg 27, .pos 45, .neg 51, .neg 144, .neg 147, .neg 152, .neg 179]
private def clause445 : Sat.Clause := [.pos 25, .neg 27, .neg 59, .neg 144, .neg 147, .pos 152, .neg 179]
private def clause446 : Sat.Clause := [.pos 27, .neg 32, .neg 45, .neg 144, .neg 147, .pos 152, .neg 179]
private def clause447 : Sat.Clause := [.neg 25, .pos 27, .neg 51, .neg 144, .neg 147, .neg 152, .neg 179]
private def clause448 : Sat.Clause := [.neg 25, .pos 27, .neg 51, .neg 144, .neg 147, .pos 152, .neg 179]
private def clause449 : Sat.Clause := [.pos 25, .neg 27, .pos 51, .neg 144, .neg 147, .pos 152, .neg 179]
private def clause450 : Sat.Clause := [.pos 25, .neg 27, .pos 51, .neg 144, .neg 147, .neg 152, .neg 179]
private def clause451 : Sat.Clause := [.pos 27, .neg 45, .pos 51, .neg 144, .neg 147, .neg 152, .neg 179]
private def clause452 : Sat.Clause := [.pos 27, .neg 45, .pos 51, .neg 144, .neg 147, .pos 152, .neg 179]
private def clause453 : Sat.Clause := [.neg 144, .neg 147, .neg 152, .neg 179, .pos 284]
private def clause454 : Sat.Clause := [.neg 25, .neg 45, .neg 62, .neg 144, .pos 148, .neg 153, .neg 180]
private def clause455 : Sat.Clause := [.neg 25, .neg 53, .pos 62, .neg 144, .pos 148, .neg 153, .neg 180]
private def clause456 : Sat.Clause := [.neg 36, .neg 45, .pos 53, .neg 144, .pos 148, .neg 153, .neg 180]
private def clause457 : Sat.Clause := [.pos 25, .neg 27, .neg 62, .neg 144, .neg 148, .pos 153, .neg 180]
private def clause458 : Sat.Clause := [.pos 27, .neg 36, .neg 45, .neg 144, .neg 148, .pos 153, .neg 180]
private def clause459 : Sat.Clause := [.neg 144, .neg 148, .neg 153, .neg 180, .pos 285]
private def clause460 : Sat.Clause := [.neg 25, .neg 54, .pos 63, .neg 144, .pos 149, .neg 154, .neg 181]
private def clause461 : Sat.Clause := [.neg 25, .neg 54, .pos 63, .neg 144, .pos 149, .pos 154, .neg 181]
private def clause462 : Sat.Clause := [.pos 25, .neg 27, .neg 63, .neg 144, .neg 149, .pos 154, .neg 181]
private def clause463 : Sat.Clause := [.pos 27, .neg 37, .neg 45, .neg 144, .neg 149, .pos 154, .neg 181]
private def clause464 : Sat.Clause := [.neg 144, .pos 149, .neg 154, .neg 181, .neg 286]
private def clause465 : Sat.Clause := [.neg 144, .neg 149, .neg 154, .neg 181, .pos 286]
private def clause466 : Sat.Clause := [.neg 25, .neg 49, .neg 76, .neg 145, .neg 146, .pos 161, .neg 182]
private def clause467 : Sat.Clause := [.neg 25, .neg 50, .pos 76, .neg 145, .pos 146, .neg 161, .neg 182]
private def clause468 : Sat.Clause := [.neg 25, .neg 50, .pos 76, .neg 145, .pos 146, .neg 161, .pos 182]
private def clause469 : Sat.Clause := [.pos 25, .neg 30, .neg 76, .neg 145, .neg 146, .pos 161, .neg 182]
private def clause470 : Sat.Clause := [.pos 25, .neg 30, .neg 76, .pos 145, .neg 146, .pos 161, .neg 182]
private def clause471 : Sat.Clause := [.neg 145, .neg 146, .neg 161, .neg 182, .pos 287]
private def clause472 : Sat.Clause := [.neg 25, .neg 49, .neg 79, .pos 145, .neg 147, .pos 162, .neg 183]
private def clause473 : Sat.Clause := [.neg 25, .neg 49, .neg 79, .neg 145, .neg 147, .pos 162, .neg 183]
private def clause474 : Sat.Clause := [.neg 25, .neg 51, .pos 79, .neg 145, .neg 147, .neg 162, .pos 183]
private def clause475 : Sat.Clause := [.neg 30, .pos 49, .neg 51, .neg 145, .neg 147, .pos 162, .neg 183]
private def clause476 : Sat.Clause := [.neg 30, .pos 49, .neg 51, .pos 145, .neg 147, .pos 162, .neg 183]
private def clause477 : Sat.Clause := [.pos 25, .neg 30, .neg 79, .neg 145, .neg 147, .pos 162, .neg 183]
private def clause478 : Sat.Clause := [.pos 25, .neg 30, .neg 79, .pos 145, .neg 147, .pos 162, .neg 183]
private def clause479 : Sat.Clause := [.pos 25, .neg 30, .neg 79, .pos 145, .neg 147, .neg 162, .neg 183]
private def clause480 : Sat.Clause := [.pos 25, .neg 32, .pos 79, .pos 145, .neg 147, .neg 162, .neg 183]
private def clause481 : Sat.Clause := [.pos 30, .neg 32, .neg 49, .pos 145, .neg 147, .neg 162, .neg 183]
private def clause482 : Sat.Clause := [.pos 30, .neg 32, .neg 49, .pos 145, .neg 147, .pos 162, .neg 183]
private def clause483 : Sat.Clause := [.pos 30, .neg 32, .neg 49, .neg 145, .neg 147, .pos 162, .neg 183]
private def clause484 : Sat.Clause := [.neg 25, .pos 30, .neg 51, .pos 145, .neg 147, .pos 162, .neg 183]
private def clause485 : Sat.Clause := [.neg 25, .pos 30, .neg 51, .neg 145, .neg 147, .pos 162, .neg 183]
private def clause486 : Sat.Clause := [.pos 25, .neg 32, .pos 49, .neg 145, .neg 147, .pos 162, .neg 183]
private def clause487 : Sat.Clause := [.pos 25, .neg 32, .pos 49, .pos 145, .neg 147, .pos 162, .neg 183]
private def clause488 : Sat.Clause := [.neg 145, .neg 147, .neg 162, .neg 183, .pos 288]
private def clause489 : Sat.Clause := [.neg 25, .neg 53, .pos 81, .neg 145, .neg 148, .neg 163, .pos 184]
private def clause490 : Sat.Clause := [.pos 30, .neg 36, .neg 49, .neg 145, .neg 148, .pos 163, .neg 184]
private def clause491 : Sat.Clause := [.neg 145, .neg 148, .neg 163, .neg 184, .pos 289]
private def clause492 : Sat.Clause := [.neg 25, .neg 49, .neg 82, .neg 145, .pos 149, .pos 164, .neg 185]
private def clause493 : Sat.Clause := [.neg 25, .neg 49, .neg 82, .neg 145, .pos 149, .neg 164, .neg 185]
private def clause494 : Sat.Clause := [.neg 25, .neg 49, .neg 82, .neg 145, .neg 149, .pos 164, .neg 185]
private def clause495 : Sat.Clause := [.neg 25, .neg 54, .pos 82, .neg 145, .pos 149, .neg 164, .neg 185]
private def clause496 : Sat.Clause := [.neg 25, .neg 54, .pos 82, .neg 145, .neg 149, .neg 164, .pos 185]
private def clause497 : Sat.Clause := [.pos 25, .neg 30, .neg 82, .neg 145, .neg 149, .pos 164, .neg 185]
private def clause498 : Sat.Clause := [.neg 145, .neg 149, .neg 164, .neg 185, .pos 290]
private def clause499 : Sat.Clause := [.neg 25, .neg 51, .pos 83, .neg 146, .neg 147, .neg 165, .pos 186]
private def clause500 : Sat.Clause := [.neg 32, .neg 50, .pos 51, .neg 146, .neg 147, .neg 165, .pos 186]
private def clause501 : Sat.Clause := [.pos 25, .neg 32, .pos 83, .neg 146, .neg 147, .neg 165, .pos 186]
private def clause502 : Sat.Clause := [.pos 25, .neg 32, .pos 83, .pos 146, .neg 147, .neg 165, .neg 186]
private def clause503 : Sat.Clause := [.neg 31, .pos 32, .pos 50, .pos 146, .neg 147, .pos 165, .neg 186]
private def clause504 : Sat.Clause := [.neg 31, .pos 32, .pos 50, .pos 146, .neg 147, .neg 165, .neg 186]
private def clause505 : Sat.Clause := [.neg 146, .neg 147, .neg 165, .neg 186, .pos 291]
private def clause506 : Sat.Clause := [.neg 36, .neg 50, .pos 53, .neg 146, .neg 148, .neg 166, .pos 187]
private def clause507 : Sat.Clause := [.pos 25, .neg 31, .neg 85, .neg 146, .neg 148, .pos 166, .neg 187]
private def clause508 : Sat.Clause := [.pos 31, .neg 36, .neg 50, .neg 146, .neg 148, .pos 166, .neg 187]
private def clause509 : Sat.Clause := [.neg 146, .pos 148, .neg 166, .neg 187, .neg 292]
private def clause510 : Sat.Clause := [.neg 146, .neg 148, .neg 166, .neg 187, .pos 292]
private def clause511 : Sat.Clause := [.neg 25, .neg 54, .pos 86, .neg 146, .pos 149, .neg 167, .neg 188]
private def clause512 : Sat.Clause := [.neg 37, .neg 50, .pos 54, .neg 146, .neg 149, .neg 167, .pos 188]
private def clause513 : Sat.Clause := [.neg 37, .neg 50, .pos 54, .neg 146, .pos 149, .neg 167, .neg 188]
private def clause514 : Sat.Clause := [.neg 37, .pos 50, .pos 86, .pos 146, .neg 149, .neg 167, .neg 188]
private def clause515 : Sat.Clause := [.neg 37, .pos 50, .pos 86, .pos 146, .neg 149, .pos 167, .neg 188]
private def clause516 : Sat.Clause := [.pos 25, .neg 31, .neg 86, .neg 146, .neg 149, .pos 167, .neg 188]
private def clause517 : Sat.Clause := [.pos 25, .neg 31, .neg 86, .pos 146, .neg 149, .pos 167, .neg 188]
private def clause518 : Sat.Clause := [.pos 25, .neg 31, .neg 86, .pos 146, .neg 149, .neg 167, .neg 188]
private def clause519 : Sat.Clause := [.pos 25, .neg 37, .pos 86, .pos 146, .neg 149, .neg 167, .neg 188]
private def clause520 : Sat.Clause := [.pos 25, .neg 37, .pos 86, .pos 146, .neg 149, .pos 167, .neg 188]
private def clause521 : Sat.Clause := [.pos 31, .neg 37, .neg 50, .pos 146, .neg 149, .neg 167, .neg 188]
private def clause522 : Sat.Clause := [.pos 31, .neg 37, .neg 50, .pos 146, .neg 149, .pos 167, .neg 188]
private def clause523 : Sat.Clause := [.pos 31, .neg 37, .neg 50, .neg 146, .neg 149, .pos 167, .neg 188]
private def clause524 : Sat.Clause := [.neg 31, .pos 37, .neg 54, .pos 146, .neg 149, .pos 167, .neg 188]
private def clause525 : Sat.Clause := [.neg 31, .pos 37, .neg 54, .pos 146, .neg 149, .neg 167, .neg 188]
private def clause526 : Sat.Clause := [.neg 146, .neg 149, .neg 167, .neg 188, .pos 293]
private def clause527 : Sat.Clause := [.neg 25, .neg 51, .neg 89, .neg 147, .pos 148, .pos 168, .neg 189]
private def clause528 : Sat.Clause := [.neg 25, .neg 51, .neg 89, .neg 147, .neg 148, .pos 168, .neg 189]
private def clause529 : Sat.Clause := [.pos 25, .neg 32, .neg 89, .neg 147, .neg 148, .pos 168, .neg 189]
private def clause530 : Sat.Clause := [.pos 25, .neg 32, .neg 89, .neg 147, .pos 148, .pos 168, .pos 189]
private def clause531 : Sat.Clause := [.pos 25, .neg 32, .neg 89, .neg 147, .pos 148, .pos 168, .neg 189]
private def clause532 : Sat.Clause := [.neg 147, .neg 148, .pos 168, .pos 189, .pos 294]
private def clause533 : Sat.Clause := [.neg 25, .neg 51, .neg 96, .neg 147, .pos 149, .neg 169, .pos 190]
private def clause534 : Sat.Clause := [.neg 32, .pos 51, .neg 54, .neg 147, .pos 149, .neg 169, .pos 190]
private def clause535 : Sat.Clause := [.neg 32, .pos 54, .neg 96, .neg 147, .pos 149, .pos 169, .pos 190]
private def clause536 : Sat.Clause := [.neg 32, .pos 54, .neg 96, .neg 147, .pos 149, .neg 169, .pos 190]
private def clause537 : Sat.Clause := [.pos 25, .neg 32, .neg 96, .neg 147, .pos 149, .pos 169, .pos 190]
private def clause538 : Sat.Clause := [.pos 25, .neg 32, .neg 96, .neg 147, .pos 149, .neg 169, .pos 190]
private def clause539 : Sat.Clause := [.pos 32, .neg 37, .neg 51, .neg 147, .neg 149, .pos 169, .pos 190]
private def clause540 : Sat.Clause := [.pos 32, .neg 37, .neg 51, .neg 147, .pos 149, .neg 169, .pos 190]
private def clause541 : Sat.Clause := [.pos 32, .neg 37, .neg 51, .neg 147, .pos 149, .pos 169, .pos 190]
private def clause542 : Sat.Clause := [.pos 37, .neg 51, .neg 96, .neg 147, .pos 149, .pos 169, .pos 190]
private def clause543 : Sat.Clause := [.pos 37, .neg 51, .neg 96, .neg 147, .pos 149, .neg 169, .pos 190]
private def clause544 : Sat.Clause := [.neg 25, .pos 32, .neg 54, .neg 147, .pos 149, .neg 169, .pos 190]
private def clause545 : Sat.Clause := [.pos 32, .neg 37, .pos 54, .neg 147, .neg 149, .neg 169, .pos 190]
private def clause546 : Sat.Clause := [.pos 32, .neg 37, .pos 54, .neg 147, .pos 149, .neg 169, .pos 190]
private def clause547 : Sat.Clause := [.pos 32, .neg 37, .pos 54, .neg 147, .pos 149, .pos 169, .pos 190]
private def clause548 : Sat.Clause := [.neg 25, .pos 37, .neg 96, .neg 147, .pos 149, .pos 169, .pos 190]
private def clause549 : Sat.Clause := [.neg 25, .pos 37, .neg 96, .neg 147, .pos 149, .neg 169, .pos 190]
private def clause550 : Sat.Clause := [.neg 147, .neg 149, .pos 169, .pos 190, .pos 295]
private def clause551 : Sat.Clause := [.neg 25, .neg 53, .neg 98, .pos 148, .neg 149, .pos 170, .pos 191]
private def clause552 : Sat.Clause := [.neg 36, .pos 53, .neg 54, .pos 148, .neg 149, .pos 170, .pos 191]
private def clause553 : Sat.Clause := [.neg 148, .pos 149, .pos 170, .pos 191, .neg 296]
private def clause554 : Sat.Clause := [.neg 148, .neg 149, .pos 170, .pos 191, .pos 296]
private def clause555 : Sat.Clause := [.neg 27, .neg 55, .neg 76, .neg 150, .pos 151, .pos 161, .neg 192]
private def clause556 : Sat.Clause := [.neg 27, .neg 55, .neg 76, .neg 150, .pos 151, .neg 161, .neg 192]
private def clause557 : Sat.Clause := [.neg 27, .neg 55, .neg 76, .neg 150, .neg 151, .pos 161, .neg 192]
private def clause558 : Sat.Clause := [.neg 27, .neg 58, .pos 76, .neg 150, .pos 151, .pos 161, .neg 192]
private def clause559 : Sat.Clause := [.pos 27, .neg 30, .neg 76, .pos 150, .neg 151, .neg 161, .neg 192]
private def clause560 : Sat.Clause := [.neg 150, .neg 151, .neg 161, .neg 192, .pos 297]
private def clause561 : Sat.Clause := [.neg 27, .neg 55, .neg 79, .neg 150, .pos 152, .neg 162, .neg 193]
private def clause562 : Sat.Clause := [.neg 32, .neg 55, .pos 59, .neg 150, .pos 152, .neg 162, .neg 193]
private def clause563 : Sat.Clause := [.pos 27, .neg 30, .neg 79, .pos 150, .neg 152, .neg 162, .neg 193]
private def clause564 : Sat.Clause := [.pos 30, .neg 32, .neg 55, .pos 150, .neg 152, .neg 162, .neg 193]
private def clause565 : Sat.Clause := [.neg 150, .neg 152, .neg 162, .neg 193, .pos 298]
private def clause566 : Sat.Clause := [.neg 27, .neg 62, .pos 81, .neg 150, .pos 153, .neg 163, .neg 194]
private def clause567 : Sat.Clause := [.neg 36, .neg 55, .pos 62, .neg 150, .neg 153, .neg 163, .pos 194]
private def clause568 : Sat.Clause := [.neg 36, .neg 55, .pos 62, .neg 150, .pos 153, .neg 163, .pos 194]
private def clause569 : Sat.Clause := [.neg 36, .neg 55, .pos 62, .neg 150, .pos 153, .neg 163, .neg 194]
private def clause570 : Sat.Clause := [.pos 27, .neg 30, .neg 81, .pos 150, .neg 153, .neg 163, .neg 194]
private def clause571 : Sat.Clause := [.pos 30, .neg 36, .neg 55, .pos 150, .neg 153, .neg 163, .neg 194]
private def clause572 : Sat.Clause := [.neg 150, .neg 153, .neg 163, .neg 194, .pos 299]
private def clause573 : Sat.Clause := [.neg 27, .neg 55, .neg 82, .neg 150, .pos 154, .neg 164, .neg 195]
private def clause574 : Sat.Clause := [.neg 27, .neg 63, .pos 82, .neg 150, .pos 154, .neg 164, .neg 195]
private def clause575 : Sat.Clause := [.neg 37, .neg 55, .pos 63, .neg 150, .neg 154, .neg 164, .pos 195]
private def clause576 : Sat.Clause := [.neg 150, .pos 154, .neg 164, .neg 195, .neg 300]
private def clause577 : Sat.Clause := [.neg 150, .neg 154, .neg 164, .pos 195, .neg 300]
private def clause578 : Sat.Clause := [.neg 150, .neg 154, .neg 164, .neg 195, .pos 300]
private def clause579 : Sat.Clause := [.neg 27, .neg 59, .pos 83, .neg 151, .neg 152, .neg 165, .pos 196]
private def clause580 : Sat.Clause := [.neg 32, .neg 58, .pos 59, .neg 151, .neg 152, .neg 165, .pos 196]
private def clause581 : Sat.Clause := [.pos 31, .neg 32, .neg 58, .neg 151, .neg 152, .pos 165, .neg 196]
private def clause582 : Sat.Clause := [.neg 151, .neg 152, .neg 165, .neg 196, .pos 301]
private def clause583 : Sat.Clause := [.neg 27, .neg 62, .pos 85, .neg 151, .neg 153, .neg 166, .pos 197]
private def clause584 : Sat.Clause := [.pos 151, .neg 153, .neg 166, .neg 197, .neg 302]
private def clause585 : Sat.Clause := [.neg 151, .neg 153, .neg 166, .pos 197, .neg 302]
private def clause586 : Sat.Clause := [.neg 151, .neg 153, .neg 166, .neg 197, .pos 302]
private def clause587 : Sat.Clause := [.neg 27, .neg 58, .neg 86, .neg 151, .neg 154, .pos 167, .neg 198]
private def clause588 : Sat.Clause := [.neg 27, .neg 63, .pos 86, .neg 151, .pos 154, .neg 167, .neg 198]
private def clause589 : Sat.Clause := [.pos 27, .neg 31, .neg 86, .neg 151, .neg 154, .pos 167, .neg 198]
private def clause590 : Sat.Clause := [.pos 31, .neg 37, .neg 58, .pos 151, .neg 154, .neg 167, .neg 198]
private def clause591 : Sat.Clause := [.neg 27, .pos 31, .neg 63, .neg 151, .neg 154, .neg 167, .neg 198]
private def clause592 : Sat.Clause := [.neg 151, .neg 154, .neg 167, .neg 198, .pos 303]
private def clause593 : Sat.Clause := [.neg 32, .pos 62, .neg 89, .neg 152, .pos 153, .pos 168, .pos 199]
private def clause594 : Sat.Clause := [.neg 32, .pos 62, .neg 89, .pos 152, .neg 153, .pos 168, .pos 199]
private def clause595 : Sat.Clause := [.pos 32, .neg 36, .neg 59, .neg 152, .neg 153, .pos 168, .pos 199]
private def clause596 : Sat.Clause := [.pos 36, .neg 59, .neg 89, .neg 152, .neg 153, .pos 168, .pos 199]
private def clause597 : Sat.Clause := [.pos 152, .neg 153, .pos 168, .pos 199, .neg 304]
private def clause598 : Sat.Clause := [.neg 152, .pos 153, .pos 168, .pos 199, .neg 304]
private def clause599 : Sat.Clause := [.neg 152, .neg 153, .pos 168, .pos 199, .pos 304]
private def clause600 : Sat.Clause := [.neg 32, .pos 59, .neg 63, .pos 152, .neg 154, .pos 169, .pos 200]
private def clause601 : Sat.Clause := [.neg 32, .pos 63, .neg 96, .neg 152, .pos 154, .pos 169, .pos 200]
private def clause602 : Sat.Clause := [.pos 27, .neg 32, .neg 96, .neg 152, .pos 154, .pos 169, .pos 200]
private def clause603 : Sat.Clause := [.pos 152, .neg 154, .pos 169, .pos 200, .neg 305]
private def clause604 : Sat.Clause := [.neg 152, .neg 154, .pos 169, .pos 200, .pos 305]
private def clause605 : Sat.Clause := [.neg 27, .neg 62, .neg 98, .pos 153, .neg 154, .pos 170, .pos 201]
private def clause606 : Sat.Clause := [.neg 36, .pos 62, .neg 63, .pos 153, .neg 154, .pos 170, .neg 201]
private def clause607 : Sat.Clause := [.neg 36, .pos 62, .neg 63, .pos 153, .neg 154, .pos 170, .pos 201]
private def clause608 : Sat.Clause := [.pos 153, .neg 154, .pos 170, .pos 201, .neg 306]
private def clause609 : Sat.Clause := [.pos 153, .neg 154, .pos 170, .neg 201, .neg 306]
private def clause610 : Sat.Clause := [.neg 153, .pos 154, .pos 170, .pos 201, .neg 306]
private def clause611 : Sat.Clause := [.neg 153, .neg 154, .pos 170, .pos 201, .pos 306]
private def clause612 : Sat.Clause := [.neg 153, .neg 154, .pos 170, .neg 201, .neg 306]
private def clause613 : Sat.Clause := [.neg 28, .neg 64, .neg 72, .pos 155, .neg 156, .pos 158, .pos 202]
private def clause614 : Sat.Clause := [.neg 29, .pos 64, .neg 67, .pos 155, .neg 156, .pos 158, .pos 202]
private def clause615 : Sat.Clause := [.neg 28, .pos 29, .neg 67, .neg 155, .neg 156, .neg 158, .pos 202]
private def clause616 : Sat.Clause := [.neg 155, .pos 156, .pos 158, .pos 202, .neg 307]
private def clause617 : Sat.Clause := [.neg 155, .neg 156, .pos 158, .pos 202, .pos 307]
private def clause618 : Sat.Clause := [.neg 155, .neg 156, .neg 158, .pos 202, .neg 307]
private def clause619 : Sat.Clause := [.neg 28, .neg 64, .neg 73, .pos 155, .neg 157, .pos 159, .pos 203]
private def clause620 : Sat.Clause := [.neg 29, .pos 64, .neg 71, .pos 155, .neg 157, .pos 159, .pos 203]
private def clause621 : Sat.Clause := [.neg 28, .pos 36, .neg 73, .neg 155, .pos 157, .pos 159, .pos 203]
private def clause622 : Sat.Clause := [.neg 28, .pos 29, .pos 73, .neg 155, .pos 157, .pos 159, .pos 203]
private def clause623 : Sat.Clause := [.neg 155, .pos 157, .pos 159, .pos 203, .neg 308]
private def clause624 : Sat.Clause := [.neg 155, .neg 157, .pos 159, .pos 203, .pos 308]
private def clause625 : Sat.Clause := [.neg 28, .neg 67, .neg 89, .pos 156, .pos 157, .neg 168, .pos 205]
private def clause626 : Sat.Clause := [.neg 28, .neg 67, .neg 89, .pos 156, .neg 157, .pos 168, .pos 205]
private def clause627 : Sat.Clause := [.neg 28, .neg 67, .neg 89, .pos 156, .neg 157, .neg 168, .pos 205]
private def clause628 : Sat.Clause := [.neg 28, .neg 67, .neg 89, .neg 156, .pos 157, .neg 168, .neg 205]
private def clause629 : Sat.Clause := [.neg 28, .neg 71, .pos 89, .neg 156, .pos 157, .neg 168, .neg 205]
private def clause630 : Sat.Clause := [.neg 36, .neg 67, .pos 71, .neg 156, .pos 157, .neg 168, .neg 205]
private def clause631 : Sat.Clause := [.neg 28, .pos 36, .neg 67, .pos 156, .neg 157, .pos 168, .neg 205]
private def clause632 : Sat.Clause := [.neg 28, .pos 36, .neg 67, .neg 156, .neg 157, .pos 168, .neg 205]
private def clause633 : Sat.Clause := [.neg 156, .neg 157, .neg 168, .pos 205, .neg 309]
private def clause634 : Sat.Clause := [.neg 156, .neg 157, .neg 168, .neg 205, .pos 309]
private def clause635 : Sat.Clause := [.neg 29, .neg 73, .pos 89, .pos 158, .pos 159, .pos 168, .neg 208]
private def clause636 : Sat.Clause := [.neg 29, .neg 73, .pos 89, .neg 158, .pos 159, .neg 168, .neg 208]
private def clause637 : Sat.Clause := [.neg 29, .neg 73, .pos 89, .neg 158, .pos 159, .pos 168, .neg 208]
private def clause638 : Sat.Clause := [.neg 32, .pos 72, .neg 73, .neg 158, .pos 159, .neg 168, .neg 208]
private def clause639 : Sat.Clause := [.pos 29, .neg 36, .pos 89, .neg 158, .pos 159, .pos 168, .neg 208]
private def clause640 : Sat.Clause := [.pos 29, .neg 36, .pos 89, .pos 158, .pos 159, .pos 168, .neg 208]
private def clause641 : Sat.Clause := [.neg 32, .pos 36, .neg 73, .pos 158, .pos 159, .pos 168, .neg 208]
private def clause642 : Sat.Clause := [.neg 29, .pos 32, .neg 73, .pos 158, .pos 159, .pos 168, .neg 208]
private def clause643 : Sat.Clause := [.pos 32, .neg 36, .pos 73, .pos 158, .pos 159, .pos 168, .neg 208]
private def clause644 : Sat.Clause := [.neg 29, .pos 36, .neg 89, .pos 158, .pos 159, .pos 168, .neg 208]
private def clause645 : Sat.Clause := [.pos 29, .pos 73, .neg 89, .neg 158, .pos 159, .pos 168, .neg 208]
private def clause646 : Sat.Clause := [.pos 29, .pos 73, .neg 89, .pos 158, .pos 159, .pos 168, .neg 208]
private def clause647 : Sat.Clause := [.pos 158, .pos 159, .neg 168, .neg 208, .pos 310]
private def clause648 : Sat.Clause := [.neg 158, .pos 159, .neg 168, .neg 208, .neg 310]
private def clause649 : Sat.Clause := [.neg 36, .pos 75, .neg 98, .pos 159, .neg 160, .pos 170, .neg 210]
private def clause650 : Sat.Clause := [.neg 36, .pos 75, .neg 98, .pos 159, .neg 160, .neg 170, .neg 210]
private def clause651 : Sat.Clause := [.pos 36, .neg 37, .pos 75, .pos 159, .neg 160, .neg 170, .neg 210]
private def clause652 : Sat.Clause := [.pos 36, .neg 37, .pos 75, .pos 159, .neg 160, .pos 170, .neg 210]
private def clause653 : Sat.Clause := [.pos 36, .neg 37, .pos 75, .pos 159, .pos 160, .pos 170, .neg 210]
private def clause654 : Sat.Clause := [.neg 32, .neg 76, .pos 79, .neg 161, .pos 162, .neg 165, .neg 211]
private def clause655 : Sat.Clause := [.pos 31, .neg 32, .neg 76, .pos 161, .neg 162, .neg 165, .neg 211]
private def clause656 : Sat.Clause := [.pos 161, .neg 162, .neg 165, .neg 211, .neg 311]
private def clause657 : Sat.Clause := [.neg 161, .neg 162, .neg 165, .neg 211, .pos 311]
private def clause658 : Sat.Clause := [.neg 36, .neg 76, .pos 81, .neg 161, .pos 163, .neg 166, .neg 212]
private def clause659 : Sat.Clause := [.neg 161, .neg 163, .neg 166, .neg 212, .pos 312]
private def clause660 : Sat.Clause := [.neg 30, .neg 82, .pos 86, .neg 161, .pos 164, .neg 167, .neg 213]
private def clause661 : Sat.Clause := [.neg 37, .pos 76, .pos 86, .pos 161, .neg 164, .neg 167, .neg 213]
private def clause662 : Sat.Clause := [.pos 30, .neg 31, .neg 86, .pos 161, .neg 164, .neg 167, .neg 213]
private def clause663 : Sat.Clause := [.pos 31, .neg 37, .neg 76, .pos 161, .neg 164, .neg 167, .neg 213]
private def clause664 : Sat.Clause := [.neg 161, .neg 164, .pos 167, .neg 213, .neg 313]
private def clause665 : Sat.Clause := [.neg 161, .neg 164, .neg 167, .neg 213, .pos 313]
private def clause666 : Sat.Clause := [.neg 30, .neg 79, .neg 89, .neg 162, .neg 163, .pos 168, .neg 214]
private def clause667 : Sat.Clause := [.neg 32, .pos 79, .neg 81, .neg 162, .neg 163, .pos 168, .neg 214]
private def clause668 : Sat.Clause := [.neg 32, .pos 81, .neg 89, .neg 162, .pos 163, .pos 168, .pos 214]
private def clause669 : Sat.Clause := [.neg 36, .neg 79, .pos 81, .neg 162, .neg 163, .pos 168, .pos 214]
private def clause670 : Sat.Clause := [.pos 30, .neg 32, .neg 89, .neg 162, .pos 163, .pos 168, .pos 214]
private def clause671 : Sat.Clause := [.neg 162, .neg 163, .pos 168, .pos 214, .pos 314]
private def clause672 : Sat.Clause := [.neg 32, .pos 79, .neg 82, .pos 162, .pos 164, .pos 169, .pos 215]
private def clause673 : Sat.Clause := [.neg 32, .pos 79, .neg 82, .pos 162, .neg 164, .pos 169, .pos 215]
private def clause674 : Sat.Clause := [.neg 32, .pos 82, .neg 96, .neg 162, .pos 164, .pos 169, .pos 215]
private def clause675 : Sat.Clause := [.neg 32, .pos 82, .neg 96, .pos 162, .neg 164, .pos 169, .pos 215]
private def clause676 : Sat.Clause := [.neg 32, .pos 82, .neg 96, .pos 162, .pos 164, .pos 169, .pos 215]
private def clause677 : Sat.Clause := [.pos 30, .neg 32, .neg 96, .neg 162, .pos 164, .pos 169, .pos 215]
private def clause678 : Sat.Clause := [.neg 162, .neg 164, .pos 169, .pos 215, .pos 315]
private def clause679 : Sat.Clause := [.neg 30, .neg 81, .neg 98, .pos 163, .neg 164, .pos 170, .pos 216]
private def clause680 : Sat.Clause := [.neg 36, .pos 81, .neg 82, .pos 163, .neg 164, .pos 170, .pos 216]
private def clause681 : Sat.Clause := [.neg 36, .pos 82, .neg 98, .pos 163, .neg 164, .pos 170, .pos 216]
private def clause682 : Sat.Clause := [.pos 163, .neg 164, .pos 170, .pos 216, .neg 316]
private def clause683 : Sat.Clause := [.neg 163, .neg 164, .pos 170, .pos 216, .pos 316]
private def clause684 : Sat.Clause := [.neg 31, .neg 83, .neg 89, .pos 165, .neg 166, .pos 168, .pos 217]
private def clause685 : Sat.Clause := [.neg 32, .pos 83, .neg 85, .pos 165, .neg 166, .pos 168, .pos 217]
private def clause686 : Sat.Clause := [.neg 32, .pos 85, .neg 89, .neg 165, .pos 166, .pos 168, .pos 217]
private def clause687 : Sat.Clause := [.neg 32, .pos 85, .neg 89, .pos 165, .neg 166, .pos 168, .pos 217]
private def clause688 : Sat.Clause := [.neg 32, .pos 85, .neg 89, .pos 165, .pos 166, .pos 168, .pos 217]
private def clause689 : Sat.Clause := [.neg 165, .neg 166, .pos 168, .pos 217, .pos 317]
private def clause690 : Sat.Clause := [.neg 32, .pos 83, .neg 86, .pos 165, .neg 167, .pos 169, .pos 218]
private def clause691 : Sat.Clause := [.neg 32, .pos 86, .neg 96, .neg 165, .pos 167, .pos 169, .pos 218]
private def clause692 : Sat.Clause := [.pos 165, .neg 167, .pos 169, .pos 218, .neg 318]
private def clause693 : Sat.Clause := [.neg 165, .neg 167, .pos 169, .pos 218, .pos 318]
private def clause694 : Sat.Clause := [.neg 165, .neg 167, .neg 169, .pos 218, .neg 318]
private def clause695 : Sat.Clause := [.neg 31, .neg 85, .neg 98, .pos 166, .neg 167, .pos 170, .pos 219]
private def clause696 : Sat.Clause := [.neg 36, .pos 85, .neg 86, .pos 166, .neg 167, .pos 170, .pos 219]
private def clause697 : Sat.Clause := [.neg 166, .neg 167, .pos 170, .pos 219, .pos 319]
private def clause698 : Sat.Clause := [.neg 166, .neg 167, .neg 170, .pos 219, .neg 319]
private def clause699 : Sat.Clause := [.neg 32, .neg 89, .neg 98, .pos 168, .pos 169, .neg 170, .pos 220]
private def clause700 : Sat.Clause := [.neg 32, .neg 89, .neg 98, .pos 168, .neg 169, .pos 170, .pos 220]
private def clause701 : Sat.Clause := [.neg 32, .neg 89, .neg 98, .pos 168, .neg 169, .neg 170, .pos 220]
private def clause702 : Sat.Clause := [.pos 168, .pos 169, .pos 170, .pos 220, .pos 320]
private def clause703 : Sat.Clause := [.neg 38, .neg 67, .pos 72, .neg 171, .neg 172, .neg 174, .pos 202]
private def clause704 : Sat.Clause := [.pos 38, .neg 43, .pos 72, .neg 171, .neg 172, .neg 174, .pos 202]
private def clause705 : Sat.Clause := [.neg 42, .pos 43, .neg 67, .neg 171, .neg 172, .neg 174, .pos 202]
private def clause706 : Sat.Clause := [.neg 38, .pos 42, .neg 67, .neg 171, .neg 172, .neg 174, .pos 202]
private def clause707 : Sat.Clause := [.pos 38, .neg 43, .pos 64, .neg 171, .neg 172, .neg 174, .pos 202]
private def clause708 : Sat.Clause := [.pos 38, .neg 43, .pos 64, .neg 171, .neg 172, .pos 174, .pos 202]
private def clause709 : Sat.Clause := [.pos 43, .pos 64, .neg 67, .neg 171, .neg 172, .pos 174, .pos 202]
private def clause710 : Sat.Clause := [.pos 43, .pos 64, .neg 67, .neg 171, .neg 172, .neg 174, .pos 202]
private def clause711 : Sat.Clause := [.neg 171, .neg 172, .pos 174, .pos 202, .pos 321]
private def clause712 : Sat.Clause := [.neg 42, .pos 71, .neg 73, .neg 171, .pos 173, .pos 175, .pos 203]
private def clause713 : Sat.Clause := [.neg 44, .pos 64, .pos 73, .neg 171, .neg 173, .pos 175, .pos 203]
private def clause714 : Sat.Clause := [.neg 44, .pos 64, .pos 73, .neg 171, .pos 173, .pos 175, .pos 203]
private def clause715 : Sat.Clause := [.pos 42, .neg 44, .neg 64, .neg 171, .neg 173, .pos 175, .pos 203]
private def clause716 : Sat.Clause := [.pos 42, .neg 44, .neg 64, .neg 171, .pos 173, .pos 175, .pos 203]
private def clause717 : Sat.Clause := [.pos 44, .neg 64, .neg 73, .neg 171, .pos 173, .pos 175, .pos 203]
private def clause718 : Sat.Clause := [.pos 44, .neg 64, .neg 73, .neg 171, .neg 173, .pos 175, .pos 203]
private def clause719 : Sat.Clause := [.pos 42, .neg 44, .pos 71, .neg 171, .pos 173, .pos 175, .pos 203]
private def clause720 : Sat.Clause := [.neg 42, .pos 44, .pos 64, .neg 171, .pos 173, .pos 175, .pos 203]
private def clause721 : Sat.Clause := [.neg 42, .pos 44, .pos 64, .neg 171, .neg 173, .pos 175, .pos 203]
private def clause722 : Sat.Clause := [.neg 171, .pos 173, .pos 175, .pos 203, .neg 322]
private def clause723 : Sat.Clause := [.neg 171, .neg 173, .pos 175, .pos 203, .pos 322]
private def clause724 : Sat.Clause := [.neg 38, .neg 67, .neg 89, .neg 172, .pos 173, .neg 176, .neg 205]
private def clause725 : Sat.Clause := [.neg 38, .neg 71, .pos 89, .neg 172, .pos 173, .neg 176, .neg 205]
private def clause726 : Sat.Clause := [.neg 172, .neg 173, .neg 176, .neg 205, .pos 323]
private def clause727 : Sat.Clause := [.neg 42, .neg 72, .neg 89, .neg 174, .pos 175, .pos 176, .neg 208]
private def clause728 : Sat.Clause := [.neg 42, .neg 72, .neg 89, .neg 174, .pos 175, .neg 176, .neg 208]
private def clause729 : Sat.Clause := [.neg 42, .neg 73, .pos 89, .pos 174, .pos 175, .pos 176, .neg 208]
private def clause730 : Sat.Clause := [.neg 42, .neg 73, .pos 89, .neg 174, .pos 175, .neg 176, .neg 208]
private def clause731 : Sat.Clause := [.neg 42, .neg 73, .pos 89, .neg 174, .pos 175, .pos 176, .neg 208]
private def clause732 : Sat.Clause := [.pos 42, .neg 43, .neg 89, .neg 174, .pos 175, .pos 176, .neg 208]
private def clause733 : Sat.Clause := [.pos 42, .neg 44, .pos 89, .pos 174, .pos 175, .pos 176, .neg 208]
private def clause734 : Sat.Clause := [.neg 43, .pos 44, .neg 73, .pos 174, .pos 175, .pos 176, .neg 208]
private def clause735 : Sat.Clause := [.pos 42, .pos 72, .pos 89, .neg 174, .pos 175, .neg 176, .neg 208]
private def clause736 : Sat.Clause := [.pos 42, .pos 72, .pos 89, .neg 174, .pos 175, .pos 176, .neg 208]
private def clause737 : Sat.Clause := [.pos 174, .pos 175, .pos 176, .neg 208, .neg 324]
private def clause738 : Sat.Clause := [.pos 174, .pos 175, .neg 176, .neg 208, .pos 324]
private def clause739 : Sat.Clause := [.neg 45, .neg 55, .neg 76, .neg 177, .pos 178, .pos 182, .neg 192]
private def clause740 : Sat.Clause := [.neg 45, .neg 55, .neg 76, .neg 177, .pos 178, .neg 182, .neg 192]
private def clause741 : Sat.Clause := [.neg 45, .neg 55, .neg 76, .neg 177, .neg 178, .pos 182, .neg 192]
private def clause742 : Sat.Clause := [.pos 45, .neg 49, .neg 76, .neg 177, .neg 178, .pos 182, .neg 192]
private def clause743 : Sat.Clause := [.pos 45, .neg 49, .neg 76, .neg 177, .pos 178, .pos 182, .neg 192]
private def clause744 : Sat.Clause := [.neg 177, .neg 178, .neg 182, .neg 192, .pos 325]
private def clause745 : Sat.Clause := [.neg 45, .neg 55, .neg 79, .neg 177, .neg 179, .pos 183, .neg 193]
private def clause746 : Sat.Clause := [.neg 49, .pos 55, .neg 59, .neg 177, .neg 179, .pos 183, .neg 193]
private def clause747 : Sat.Clause := [.neg 49, .pos 55, .neg 59, .neg 177, .neg 179, .neg 183, .neg 193]
private def clause748 : Sat.Clause := [.pos 45, .neg 49, .neg 79, .neg 177, .neg 179, .pos 183, .neg 193]
private def clause749 : Sat.Clause := [.pos 49, .neg 51, .neg 55, .neg 177, .neg 179, .pos 183, .neg 193]
private def clause750 : Sat.Clause := [.neg 45, .pos 49, .neg 59, .neg 177, .neg 179, .neg 183, .neg 193]
private def clause751 : Sat.Clause := [.neg 45, .pos 49, .neg 59, .neg 177, .neg 179, .pos 183, .neg 193]
private def clause752 : Sat.Clause := [.pos 45, .neg 51, .pos 55, .neg 177, .neg 179, .pos 183, .neg 193]
private def clause753 : Sat.Clause := [.neg 45, .pos 51, .neg 55, .neg 177, .neg 179, .pos 183, .neg 193]
private def clause754 : Sat.Clause := [.pos 45, .neg 49, .pos 59, .neg 177, .neg 179, .pos 183, .neg 193]
private def clause755 : Sat.Clause := [.pos 45, .neg 49, .pos 59, .neg 177, .neg 179, .neg 183, .neg 193]
private def clause756 : Sat.Clause := [.pos 49, .neg 55, .pos 59, .neg 177, .neg 179, .neg 183, .neg 193]
private def clause757 : Sat.Clause := [.pos 49, .neg 55, .pos 59, .neg 177, .neg 179, .pos 183, .neg 193]
private def clause758 : Sat.Clause := [.neg 177, .neg 179, .neg 183, .neg 193, .pos 326]
private def clause759 : Sat.Clause := [.neg 45, .neg 55, .neg 81, .neg 177, .pos 180, .neg 184, .neg 194]
private def clause760 : Sat.Clause := [.neg 45, .neg 62, .pos 81, .neg 177, .pos 180, .neg 184, .neg 194]
private def clause761 : Sat.Clause := [.neg 45, .neg 62, .pos 81, .neg 177, .pos 180, .neg 184, .pos 194]
private def clause762 : Sat.Clause := [.neg 45, .neg 62, .pos 81, .neg 177, .neg 180, .neg 184, .pos 194]
private def clause763 : Sat.Clause := [.neg 53, .neg 55, .pos 62, .neg 177, .pos 180, .neg 184, .neg 194]
private def clause764 : Sat.Clause := [.neg 45, .pos 53, .neg 55, .neg 177, .neg 180, .pos 184, .neg 194]
private def clause765 : Sat.Clause := [.neg 177, .neg 180, .pos 184, .neg 194, .neg 327]
private def clause766 : Sat.Clause := [.neg 177, .neg 180, .neg 184, .neg 194, .pos 327]
private def clause767 : Sat.Clause := [.neg 45, .neg 55, .neg 82, .neg 177, .pos 181, .pos 185, .neg 195]
private def clause768 : Sat.Clause := [.neg 45, .neg 55, .neg 82, .neg 177, .pos 181, .neg 185, .neg 195]
private def clause769 : Sat.Clause := [.neg 45, .neg 55, .neg 82, .neg 177, .neg 181, .pos 185, .neg 195]
private def clause770 : Sat.Clause := [.neg 45, .neg 63, .pos 82, .neg 177, .pos 181, .neg 185, .neg 195]
private def clause771 : Sat.Clause := [.neg 54, .neg 55, .pos 63, .neg 177, .pos 181, .neg 185, .neg 195]
private def clause772 : Sat.Clause := [.neg 177, .pos 181, .neg 185, .neg 195, .neg 328]
private def clause773 : Sat.Clause := [.neg 177, .neg 181, .neg 185, .neg 195, .pos 328]
private def clause774 : Sat.Clause := [.neg 45, .neg 58, .neg 83, .neg 178, .neg 179, .pos 186, .neg 196]
private def clause775 : Sat.Clause := [.neg 45, .pos 51, .neg 58, .neg 178, .neg 179, .pos 186, .neg 196]
private def clause776 : Sat.Clause := [.neg 178, .neg 179, .neg 186, .neg 196, .pos 329]
private def clause777 : Sat.Clause := [.neg 50, .pos 62, .neg 85, .neg 178, .neg 180, .neg 187, .neg 197]
private def clause778 : Sat.Clause := [.neg 45, .pos 53, .neg 58, .neg 178, .neg 180, .pos 187, .neg 197]
private def clause779 : Sat.Clause := [.neg 178, .neg 180, .neg 187, .neg 197, .pos 330]
private def clause780 : Sat.Clause := [.neg 45, .neg 58, .neg 86, .neg 178, .pos 181, .neg 188, .neg 198]
private def clause781 : Sat.Clause := [.neg 45, .neg 63, .pos 86, .neg 178, .pos 181, .neg 188, .neg 198]
private def clause782 : Sat.Clause := [.neg 45, .neg 63, .pos 86, .neg 178, .neg 181, .neg 188, .pos 198]
private def clause783 : Sat.Clause := [.neg 54, .pos 58, .pos 86, .pos 178, .neg 181, .neg 188, .neg 198]
private def clause784 : Sat.Clause := [.neg 54, .pos 58, .pos 86, .pos 178, .pos 181, .neg 188, .neg 198]
private def clause785 : Sat.Clause := [.neg 50, .pos 54, .pos 58, .pos 178, .neg 181, .neg 188, .neg 198]
private def clause786 : Sat.Clause := [.neg 178, .neg 181, .neg 188, .neg 198, .pos 331]
private def clause787 : Sat.Clause := [.neg 45, .neg 59, .neg 89, .neg 179, .neg 180, .pos 189, .neg 199]
private def clause788 : Sat.Clause := [.neg 51, .pos 62, .neg 89, .neg 179, .pos 180, .pos 189, .pos 199]
private def clause789 : Sat.Clause := [.neg 45, .pos 53, .neg 89, .neg 179, .pos 180, .pos 189, .pos 199]
private def clause790 : Sat.Clause := [.neg 45, .pos 53, .neg 89, .neg 179, .pos 180, .neg 189, .pos 199]
private def clause791 : Sat.Clause := [.neg 45, .pos 53, .neg 89, .neg 179, .neg 180, .neg 189, .pos 199]
private def clause792 : Sat.Clause := [.neg 179, .neg 180, .pos 189, .pos 199, .pos 332]
private def clause793 : Sat.Clause := [.pos 51, .neg 54, .neg 59, .neg 179, .neg 181, .pos 190, .pos 200]
private def clause794 : Sat.Clause := [.pos 51, .neg 54, .neg 59, .neg 179, .pos 181, .pos 190, .pos 200]
private def clause795 : Sat.Clause := [.pos 54, .neg 59, .neg 96, .neg 179, .pos 181, .pos 190, .pos 200]
private def clause796 : Sat.Clause := [.pos 54, .neg 59, .neg 96, .neg 179, .neg 181, .pos 190, .pos 200]
private def clause797 : Sat.Clause := [.pos 54, .pos 59, .neg 63, .neg 179, .neg 181, .pos 190, .pos 200]
private def clause798 : Sat.Clause := [.neg 45, .pos 54, .neg 96, .neg 179, .pos 181, .pos 190, .pos 200]
private def clause799 : Sat.Clause := [.neg 179, .neg 181, .pos 190, .pos 200, .pos 333]
private def clause800 : Sat.Clause := [.neg 45, .neg 62, .neg 98, .pos 180, .neg 181, .pos 191, .pos 201]
private def clause801 : Sat.Clause := [.neg 45, .neg 62, .neg 98, .pos 180, .neg 181, .pos 191, .neg 201]
private def clause802 : Sat.Clause := [.neg 45, .neg 62, .neg 98, .neg 180, .neg 181, .pos 191, .neg 201]
private def clause803 : Sat.Clause := [.pos 180, .neg 181, .pos 191, .pos 201, .neg 334]
private def clause804 : Sat.Clause := [.neg 180, .neg 181, .pos 191, .pos 201, .pos 334]
private def clause805 : Sat.Clause := [.neg 180, .neg 181, .neg 191, .pos 201, .neg 334]
private def clause806 : Sat.Clause := [.neg 182, .neg 183, .neg 186, .neg 211, .pos 335]
private def clause807 : Sat.Clause := [.neg 49, .neg 81, .pos 85, .neg 182, .pos 184, .neg 187, .neg 212]
private def clause808 : Sat.Clause := [.neg 182, .neg 184, .neg 187, .neg 212, .pos 336]
private def clause809 : Sat.Clause := [.neg 49, .neg 76, .neg 86, .neg 182, .pos 185, .pos 188, .neg 213]
private def clause810 : Sat.Clause := [.neg 49, .neg 76, .neg 86, .neg 182, .pos 185, .neg 188, .neg 213]
private def clause811 : Sat.Clause := [.neg 49, .neg 76, .neg 86, .neg 182, .neg 185, .pos 188, .neg 213]
private def clause812 : Sat.Clause := [.neg 49, .neg 82, .pos 86, .neg 182, .pos 185, .neg 188, .neg 213]
private def clause813 : Sat.Clause := [.pos 49, .neg 50, .neg 86, .neg 182, .neg 185, .pos 188, .neg 213]
private def clause814 : Sat.Clause := [.pos 49, .neg 50, .neg 86, .pos 182, .neg 185, .pos 188, .neg 213]
private def clause815 : Sat.Clause := [.pos 50, .neg 54, .neg 76, .pos 182, .neg 185, .pos 188, .neg 213]
private def clause816 : Sat.Clause := [.pos 50, .neg 54, .neg 76, .neg 182, .neg 185, .pos 188, .neg 213]
private def clause817 : Sat.Clause := [.neg 182, .neg 185, .neg 188, .neg 213, .pos 337]
private def clause818 : Sat.Clause := [.neg 49, .pos 53, .neg 89, .neg 183, .neg 184, .neg 189, .pos 214]
private def clause819 : Sat.Clause := [.neg 183, .neg 184, .pos 189, .pos 214, .pos 338]
private def clause820 : Sat.Clause := [.neg 51, .pos 79, .neg 82, .pos 183, .neg 185, .pos 190, .pos 215]
private def clause821 : Sat.Clause := [.neg 51, .pos 82, .neg 96, .neg 183, .pos 185, .pos 190, .pos 215]
private def clause822 : Sat.Clause := [.pos 49, .neg 51, .neg 96, .neg 183, .pos 185, .pos 190, .pos 215]
private def clause823 : Sat.Clause := [.pos 51, .neg 54, .neg 79, .neg 183, .neg 185, .pos 190, .pos 215]
private def clause824 : Sat.Clause := [.pos 51, .neg 54, .neg 79, .neg 183, .pos 185, .pos 190, .pos 215]
private def clause825 : Sat.Clause := [.pos 54, .neg 79, .neg 96, .neg 183, .pos 185, .pos 190, .pos 215]
private def clause826 : Sat.Clause := [.pos 54, .neg 79, .neg 96, .neg 183, .neg 185, .pos 190, .pos 215]
private def clause827 : Sat.Clause := [.pos 51, .neg 54, .pos 82, .neg 183, .pos 185, .pos 190, .pos 215]
private def clause828 : Sat.Clause := [.neg 49, .pos 54, .neg 96, .neg 183, .pos 185, .pos 190, .pos 215]
private def clause829 : Sat.Clause := [.neg 183, .neg 185, .pos 190, .pos 215, .pos 339]
private def clause830 : Sat.Clause := [.neg 49, .neg 81, .neg 98, .pos 184, .neg 185, .pos 191, .pos 216]
private def clause831 : Sat.Clause := [.neg 53, .pos 81, .neg 82, .pos 184, .neg 185, .pos 191, .pos 216]
private def clause832 : Sat.Clause := [.neg 53, .pos 82, .neg 98, .pos 184, .neg 185, .pos 191, .pos 216]
private def clause833 : Sat.Clause := [.neg 49, .pos 54, .neg 98, .neg 184, .neg 185, .neg 191, .pos 216]
private def clause834 : Sat.Clause := [.pos 184, .neg 185, .pos 191, .pos 216, .neg 340]
private def clause835 : Sat.Clause := [.neg 184, .neg 185, .pos 191, .pos 216, .pos 340]
private def clause836 : Sat.Clause := [.neg 51, .pos 83, .neg 85, .pos 186, .neg 187, .pos 189, .pos 217]
private def clause837 : Sat.Clause := [.neg 186, .neg 187, .pos 189, .pos 217, .pos 341]
private def clause838 : Sat.Clause := [.neg 51, .pos 83, .neg 86, .pos 186, .neg 188, .pos 190, .pos 218]
private def clause839 : Sat.Clause := [.neg 51, .pos 86, .neg 96, .neg 186, .pos 188, .pos 190, .pos 218]
private def clause840 : Sat.Clause := [.neg 51, .pos 86, .neg 96, .pos 186, .pos 188, .pos 190, .pos 218]
private def clause841 : Sat.Clause := [.pos 51, .neg 54, .pos 86, .pos 186, .pos 188, .pos 190, .pos 218]
private def clause842 : Sat.Clause := [.pos 51, .neg 54, .pos 86, .neg 186, .pos 188, .pos 190, .pos 218]
private def clause843 : Sat.Clause := [.pos 50, .pos 86, .neg 96, .pos 186, .neg 188, .pos 190, .pos 218]
private def clause844 : Sat.Clause := [.neg 186, .neg 188, .pos 190, .pos 218, .pos 342]
private def clause845 : Sat.Clause := [.neg 50, .neg 85, .neg 98, .pos 187, .neg 188, .pos 191, .pos 219]
private def clause846 : Sat.Clause := [.neg 53, .pos 85, .neg 86, .pos 187, .neg 188, .pos 191, .pos 219]
private def clause847 : Sat.Clause := [.neg 53, .pos 86, .neg 98, .pos 187, .neg 188, .pos 191, .pos 219]
private def clause848 : Sat.Clause := [.neg 50, .pos 54, .neg 98, .pos 187, .neg 188, .neg 191, .pos 219]
private def clause849 : Sat.Clause := [.neg 50, .pos 54, .neg 98, .neg 187, .neg 188, .neg 191, .pos 219]
private def clause850 : Sat.Clause := [.neg 187, .neg 188, .pos 191, .pos 219, .pos 343]
private def clause851 : Sat.Clause := [.neg 51, .neg 89, .neg 98, .pos 189, .pos 190, .neg 191, .pos 220]
private def clause852 : Sat.Clause := [.neg 51, .neg 89, .neg 98, .neg 189, .pos 190, .neg 191, .pos 220]
private def clause853 : Sat.Clause := [.pos 51, .neg 53, .neg 98, .neg 189, .pos 190, .pos 191, .pos 220]
private def clause854 : Sat.Clause := [.pos 51, .neg 53, .neg 98, .neg 189, .pos 190, .neg 191, .pos 220]
private def clause855 : Sat.Clause := [.pos 51, .neg 53, .neg 98, .pos 189, .pos 190, .neg 191, .pos 220]
private def clause856 : Sat.Clause := [.pos 53, .neg 54, .neg 89, .pos 189, .pos 190, .neg 191, .pos 220]
private def clause857 : Sat.Clause := [.pos 53, .neg 54, .neg 89, .neg 189, .pos 190, .neg 191, .pos 220]
private def clause858 : Sat.Clause := [.pos 53, .neg 54, .neg 89, .neg 189, .pos 190, .pos 191, .pos 220]
private def clause859 : Sat.Clause := [.pos 54, .neg 89, .neg 98, .neg 189, .pos 190, .pos 191, .pos 220]
private def clause860 : Sat.Clause := [.pos 189, .pos 190, .pos 191, .pos 220, .pos 344]
private def clause861 : Sat.Clause := [.neg 58, .pos 76, .neg 79, .neg 192, .neg 193, .pos 196, .neg 211]
private def clause862 : Sat.Clause := [.neg 58, .pos 76, .neg 79, .neg 192, .neg 193, .neg 196, .neg 211]
private def clause863 : Sat.Clause := [.neg 55, .pos 58, .neg 79, .neg 192, .neg 193, .neg 196, .neg 211]
private def clause864 : Sat.Clause := [.neg 55, .pos 58, .neg 79, .neg 192, .neg 193, .pos 196, .neg 211]
private def clause865 : Sat.Clause := [.neg 55, .pos 59, .neg 76, .neg 192, .neg 193, .pos 196, .neg 211]
private def clause866 : Sat.Clause := [.neg 58, .pos 59, .pos 76, .neg 192, .neg 193, .pos 196, .neg 211]
private def clause867 : Sat.Clause := [.pos 55, .neg 58, .pos 79, .neg 192, .neg 193, .pos 196, .neg 211]
private def clause868 : Sat.Clause := [.pos 55, .neg 58, .pos 79, .neg 192, .neg 193, .neg 196, .neg 211]
private def clause869 : Sat.Clause := [.pos 58, .neg 76, .pos 79, .neg 192, .neg 193, .neg 196, .neg 211]
private def clause870 : Sat.Clause := [.pos 58, .neg 76, .pos 79, .neg 192, .neg 193, .pos 196, .neg 211]
private def clause871 : Sat.Clause := [.neg 192, .neg 193, .neg 196, .neg 211, .pos 345]
private def clause872 : Sat.Clause := [.neg 55, .neg 81, .pos 85, .neg 192, .neg 194, .neg 197, .pos 212]
private def clause873 : Sat.Clause := [.neg 62, .neg 76, .pos 81, .neg 192, .pos 194, .neg 197, .neg 212]
private def clause874 : Sat.Clause := [.neg 55, .pos 62, .neg 76, .neg 192, .neg 194, .pos 197, .neg 212]
private def clause875 : Sat.Clause := [.pos 55, .neg 58, .pos 81, .neg 192, .neg 194, .neg 197, .neg 212]
private def clause876 : Sat.Clause := [.neg 192, .neg 194, .neg 197, .neg 212, .pos 346]
private def clause877 : Sat.Clause := [.neg 55, .neg 76, .neg 86, .neg 192, .pos 195, .pos 198, .neg 213]
private def clause878 : Sat.Clause := [.neg 55, .neg 76, .neg 86, .neg 192, .pos 195, .neg 198, .neg 213]
private def clause879 : Sat.Clause := [.neg 55, .neg 76, .neg 86, .neg 192, .neg 195, .pos 198, .neg 213]
private def clause880 : Sat.Clause := [.neg 55, .neg 82, .pos 86, .neg 192, .pos 195, .neg 198, .neg 213]
private def clause881 : Sat.Clause := [.neg 63, .neg 76, .pos 82, .neg 192, .pos 195, .neg 198, .neg 213]
private def clause882 : Sat.Clause := [.neg 55, .pos 58, .pos 86, .neg 192, .neg 195, .pos 198, .neg 213]
private def clause883 : Sat.Clause := [.neg 192, .neg 195, .neg 198, .neg 213, .pos 347]
private def clause884 : Sat.Clause := [.neg 55, .pos 62, .neg 89, .neg 193, .pos 194, .pos 199, .pos 214]
private def clause885 : Sat.Clause := [.neg 55, .pos 62, .neg 89, .neg 193, .pos 194, .neg 199, .pos 214]
private def clause886 : Sat.Clause := [.neg 55, .pos 62, .neg 89, .neg 193, .neg 194, .neg 199, .pos 214]
private def clause887 : Sat.Clause := [.neg 55, .pos 62, .neg 79, .neg 193, .neg 194, .pos 199, .pos 214]
private def clause888 : Sat.Clause := [.neg 193, .neg 194, .pos 199, .pos 214, .pos 348]
private def clause889 : Sat.Clause := [.neg 59, .pos 82, .neg 96, .neg 193, .pos 195, .pos 200, .pos 215]
private def clause890 : Sat.Clause := [.pos 59, .neg 63, .neg 79, .neg 193, .neg 195, .pos 200, .pos 215]
private def clause891 : Sat.Clause := [.pos 59, .neg 63, .neg 79, .neg 193, .pos 195, .pos 200, .pos 215]
private def clause892 : Sat.Clause := [.pos 63, .neg 79, .neg 96, .neg 193, .pos 195, .pos 200, .pos 215]
private def clause893 : Sat.Clause := [.pos 63, .neg 79, .neg 96, .neg 193, .neg 195, .pos 200, .pos 215]
private def clause894 : Sat.Clause := [.neg 55, .pos 63, .neg 96, .neg 193, .pos 195, .pos 200, .pos 215]
private def clause895 : Sat.Clause := [.neg 193, .pos 195, .pos 200, .pos 215, .neg 349]
private def clause896 : Sat.Clause := [.neg 193, .neg 195, .pos 200, .pos 215, .pos 349]
private def clause897 : Sat.Clause := [.neg 55, .neg 81, .neg 98, .pos 194, .neg 195, .pos 201, .pos 216]
private def clause898 : Sat.Clause := [.neg 55, .neg 81, .neg 98, .pos 194, .neg 195, .pos 201, .neg 216]
private def clause899 : Sat.Clause := [.neg 55, .neg 81, .neg 98, .neg 194, .neg 195, .pos 201, .neg 216]
private def clause900 : Sat.Clause := [.neg 62, .pos 81, .neg 82, .pos 194, .neg 195, .pos 201, .pos 216]
private def clause901 : Sat.Clause := [.neg 62, .pos 82, .neg 98, .neg 194, .pos 195, .pos 201, .pos 216]
private def clause902 : Sat.Clause := [.neg 62, .pos 82, .neg 98, .neg 194, .pos 195, .neg 201, .pos 216]
private def clause903 : Sat.Clause := [.neg 55, .pos 63, .neg 98, .neg 194, .neg 195, .neg 201, .pos 216]
private def clause904 : Sat.Clause := [.pos 194, .neg 195, .pos 201, .pos 216, .neg 350]
private def clause905 : Sat.Clause := [.pos 194, .neg 195, .pos 201, .neg 216, .neg 350]
private def clause906 : Sat.Clause := [.neg 194, .pos 195, .pos 201, .pos 216, .neg 350]
private def clause907 : Sat.Clause := [.neg 194, .neg 195, .pos 201, .pos 216, .pos 350]
private def clause908 : Sat.Clause := [.neg 194, .neg 195, .pos 201, .neg 216, .neg 350]
private def clause909 : Sat.Clause := [.neg 59, .pos 85, .neg 89, .pos 196, .neg 197, .pos 199, .pos 217]
private def clause910 : Sat.Clause := [.neg 58, .pos 62, .neg 89, .neg 196, .pos 197, .pos 199, .pos 217]
private def clause911 : Sat.Clause := [.pos 196, .neg 197, .pos 199, .pos 217, .neg 351]
private def clause912 : Sat.Clause := [.neg 196, .neg 197, .pos 199, .pos 217, .pos 351]
private def clause913 : Sat.Clause := [.neg 58, .neg 83, .neg 96, .pos 196, .neg 198, .pos 200, .pos 218]
private def clause914 : Sat.Clause := [.neg 59, .pos 83, .neg 86, .pos 196, .neg 198, .pos 200, .pos 218]
private def clause915 : Sat.Clause := [.neg 59, .pos 86, .neg 96, .neg 196, .pos 198, .pos 200, .pos 218]
private def clause916 : Sat.Clause := [.neg 59, .pos 86, .neg 96, .pos 196, .pos 198, .pos 200, .pos 218]
private def clause917 : Sat.Clause := [.pos 59, .neg 63, .pos 86, .neg 196, .pos 198, .pos 200, .pos 218]
private def clause918 : Sat.Clause := [.neg 58, .pos 63, .neg 96, .neg 196, .pos 198, .pos 200, .pos 218]
private def clause919 : Sat.Clause := [.neg 196, .neg 198, .pos 200, .pos 218, .pos 352]
private def clause920 : Sat.Clause := [.neg 58, .neg 85, .neg 98, .pos 197, .neg 198, .pos 201, .pos 219]
private def clause921 : Sat.Clause := [.neg 62, .pos 85, .neg 86, .pos 197, .neg 198, .pos 201, .pos 219]
private def clause922 : Sat.Clause := [.neg 58, .pos 63, .neg 98, .neg 197, .neg 198, .neg 201, .pos 219]
private def clause923 : Sat.Clause := [.pos 197, .neg 198, .pos 201, .pos 219, .neg 353]
private def clause924 : Sat.Clause := [.neg 197, .pos 198, .pos 201, .pos 219, .neg 353]
private def clause925 : Sat.Clause := [.neg 197, .neg 198, .pos 201, .pos 219, .pos 353]
private def clause926 : Sat.Clause := [.neg 197, .neg 198, .neg 201, .pos 219, .neg 353]
private def clause927 : Sat.Clause := [.neg 59, .neg 89, .neg 98, .pos 199, .pos 200, .neg 201, .pos 220]
private def clause928 : Sat.Clause := [.neg 59, .neg 89, .neg 98, .neg 199, .pos 200, .neg 201, .pos 220]
private def clause929 : Sat.Clause := [.pos 59, .neg 62, .neg 98, .neg 199, .pos 200, .pos 201, .pos 220]
private def clause930 : Sat.Clause := [.pos 59, .neg 62, .neg 98, .neg 199, .pos 200, .neg 201, .pos 220]
private def clause931 : Sat.Clause := [.pos 59, .neg 62, .neg 98, .pos 199, .pos 200, .neg 201, .pos 220]
private def clause932 : Sat.Clause := [.pos 62, .neg 63, .neg 89, .pos 199, .pos 200, .neg 201, .pos 220]
private def clause933 : Sat.Clause := [.pos 62, .neg 63, .neg 89, .neg 199, .pos 200, .neg 201, .pos 220]
private def clause934 : Sat.Clause := [.pos 62, .neg 63, .neg 89, .neg 199, .pos 200, .pos 201, .pos 220]
private def clause935 : Sat.Clause := [.pos 63, .neg 89, .neg 98, .neg 199, .pos 200, .neg 201, .pos 220]
private def clause936 : Sat.Clause := [.pos 199, .pos 200, .pos 201, .pos 220, .pos 354]
private def clause937 : Sat.Clause := [.neg 71, .neg 72, .pos 73, .pos 202, .pos 203, .neg 205, .neg 208]
private def clause938 : Sat.Clause := [.neg 71, .pos 72, .pos 89, .pos 202, .pos 203, .neg 205, .neg 208]
private def clause939 : Sat.Clause := [.neg 64, .pos 71, .neg 72, .pos 202, .pos 203, .neg 205, .neg 208]
private def clause940 : Sat.Clause := [.neg 67, .pos 71, .pos 72, .pos 202, .pos 203, .neg 205, .neg 208]
private def clause941 : Sat.Clause := [.pos 202, .pos 203, .neg 205, .neg 208, .pos 355]
private def clause942 : Sat.Clause := [.neg 67, .pos 75, .neg 96, .pos 202, .neg 204, .pos 206, .pos 209]
private def clause943 : Sat.Clause := [.neg 67, .pos 75, .neg 96, .pos 202, .pos 204, .pos 206, .pos 209]
private def clause944 : Sat.Clause := [.neg 71, .pos 73, .neg 75, .pos 203, .pos 204, .pos 207, .pos 210]
private def clause945 : Sat.Clause := [.neg 71, .pos 73, .neg 75, .pos 203, .neg 204, .pos 207, .pos 210]
private def clause946 : Sat.Clause := [.neg 67, .neg 89, .neg 98, .pos 205, .pos 206, .neg 207, .pos 220]
private def clause947 : Sat.Clause := [.neg 67, .neg 89, .neg 98, .neg 205, .pos 206, .neg 207, .pos 220]
private def clause948 : Sat.Clause := [.neg 71, .pos 89, .neg 96, .neg 205, .pos 206, .neg 207, .pos 220]
private def clause949 : Sat.Clause := [.neg 71, .pos 89, .neg 96, .pos 205, .pos 206, .pos 207, .pos 220]
private def clause950 : Sat.Clause := [.neg 71, .pos 89, .neg 96, .pos 205, .pos 206, .neg 207, .pos 220]
private def clause951 : Sat.Clause := [.neg 67, .pos 71, .neg 96, .pos 205, .pos 206, .neg 207, .pos 220]
private def clause952 : Sat.Clause := [.neg 67, .pos 71, .neg 96, .pos 205, .pos 206, .pos 207, .pos 220]
private def clause953 : Sat.Clause := [.neg 67, .pos 71, .neg 96, .neg 205, .pos 206, .neg 207, .pos 220]
private def clause954 : Sat.Clause := [.pos 75, .neg 89, .neg 98, .neg 208, .neg 209, .pos 210, .pos 220]
private def clause955 : Sat.Clause := [.pos 75, .pos 89, .neg 96, .neg 208, .neg 209, .pos 210, .pos 220]
private def clause956 : Sat.Clause := [.pos 75, .pos 89, .neg 96, .neg 208, .neg 209, .neg 210, .pos 220]
private def clause957 : Sat.Clause := [.neg 76, .neg 83, .neg 89, .neg 211, .neg 212, .pos 214, .neg 217]
private def clause958 : Sat.Clause := [.neg 76, .pos 81, .neg 89, .neg 211, .pos 212, .pos 214, .pos 217]
private def clause959 : Sat.Clause := [.neg 76, .pos 81, .neg 89, .neg 211, .pos 212, .neg 214, .pos 217]
private def clause960 : Sat.Clause := [.neg 76, .pos 81, .neg 89, .neg 211, .neg 212, .neg 214, .pos 217]
private def clause961 : Sat.Clause := [.neg 211, .neg 212, .pos 214, .pos 217, .pos 356]
private def clause962 : Sat.Clause := [.pos 79, .neg 82, .neg 83, .neg 211, .neg 213, .pos 215, .pos 218]
private def clause963 : Sat.Clause := [.pos 82, .neg 83, .neg 96, .neg 211, .neg 213, .pos 215, .pos 218]
private def clause964 : Sat.Clause := [.pos 76, .neg 82, .pos 83, .neg 211, .neg 213, .pos 215, .pos 218]
private def clause965 : Sat.Clause := [.pos 82, .pos 83, .neg 86, .neg 211, .neg 213, .pos 215, .pos 218]
private def clause966 : Sat.Clause := [.neg 211, .neg 213, .pos 215, .pos 218, .pos 357]
private def clause967 : Sat.Clause := [.neg 76, .neg 85, .neg 98, .pos 212, .neg 213, .pos 216, .pos 219]
private def clause968 : Sat.Clause := [.neg 81, .pos 85, .neg 86, .pos 212, .neg 213, .pos 216, .pos 219]
private def clause969 : Sat.Clause := [.pos 81, .neg 82, .neg 85, .neg 212, .neg 213, .pos 216, .pos 219]
private def clause970 : Sat.Clause := [.neg 76, .pos 82, .neg 98, .neg 212, .neg 213, .neg 216, .pos 219]
private def clause971 : Sat.Clause := [.pos 212, .neg 213, .pos 216, .pos 219, .neg 358]
private def clause972 : Sat.Clause := [.neg 212, .neg 213, .pos 216, .pos 219, .pos 358]
private def clause973 : Sat.Clause := [.neg 79, .neg 89, .neg 98, .pos 214, .pos 215, .neg 216, .pos 220]
private def clause974 : Sat.Clause := [.neg 79, .neg 89, .neg 98, .neg 214, .pos 215, .neg 216, .pos 220]
private def clause975 : Sat.Clause := [.pos 79, .neg 81, .neg 98, .neg 214, .pos 215, .pos 216, .pos 220]
private def clause976 : Sat.Clause := [.pos 79, .neg 81, .neg 98, .neg 214, .pos 215, .neg 216, .pos 220]
private def clause977 : Sat.Clause := [.pos 79, .neg 81, .neg 98, .pos 214, .pos 215, .neg 216, .pos 220]
private def clause978 : Sat.Clause := [.pos 81, .neg 82, .neg 89, .pos 214, .pos 215, .neg 216, .pos 220]
private def clause979 : Sat.Clause := [.pos 81, .neg 82, .neg 89, .neg 214, .pos 215, .pos 216, .pos 220]
private def clause980 : Sat.Clause := [.pos 82, .neg 89, .neg 98, .neg 214, .pos 215, .pos 216, .pos 220]
private def clause981 : Sat.Clause := [.pos 214, .pos 215, .pos 216, .pos 220, .pos 359]
private def clause982 : Sat.Clause := [.pos 83, .neg 85, .neg 98, .neg 217, .pos 218, .pos 219, .pos 220]
private def clause983 : Sat.Clause := [.pos 85, .neg 86, .neg 89, .neg 217, .pos 218, .pos 219, .pos 220]
private def clause984 : Sat.Clause := [.pos 86, .neg 89, .neg 98, .neg 217, .pos 218, .pos 219, .pos 220]
private def clause985 : Sat.Clause := [.pos 217, .pos 218, .pos 219, .pos 220, .pos 360]
private def clause986 : Sat.Clause := [.neg 221, .neg 222, .neg 223, .neg 224, .neg 225, .neg 226, .neg 227, .neg 228, .neg 229, .neg 230, .neg 231, .neg 232, .neg 233, .neg 234, .neg 235, .neg 236, .neg 237, .neg 238, .neg 239, .neg 240, .neg 241, .neg 242, .neg 243, .neg 244, .neg 245, .neg 246, .neg 247, .neg 248, .neg 249, .neg 250, .neg 251, .neg 252, .neg 253, .neg 254, .neg 255, .neg 256, .neg 257, .neg 258, .neg 259, .neg 260, .neg 261, .neg 262, .neg 263, .neg 264, .neg 265, .neg 266, .neg 267, .neg 268, .neg 269, .neg 270, .neg 271, .neg 272, .neg 273, .neg 274, .neg 275, .neg 276, .neg 277, .neg 278, .neg 279, .neg 280, .neg 281, .neg 307, .neg 308, .neg 309, .neg 310, .neg 321, .neg 322, .neg 323, .neg 324, .neg 355]
private def clause987 : Sat.Clause := [.neg 282, .neg 283, .neg 284, .neg 285, .neg 286, .neg 287, .neg 288, .neg 289, .neg 290, .neg 291, .neg 292, .neg 293, .neg 294, .neg 295, .neg 296, .neg 297, .neg 298, .neg 299, .neg 300, .neg 301, .neg 302, .neg 303, .neg 304, .neg 305, .neg 306, .neg 311, .neg 312, .neg 313, .neg 314, .neg 315, .neg 316, .neg 317, .neg 318, .neg 319, .neg 320, .neg 325, .neg 326, .neg 327, .neg 328, .neg 329, .neg 330, .neg 331, .neg 332, .neg 333, .neg 334, .neg 335, .neg 336, .neg 337, .neg 338, .neg 339, .neg 340, .neg 341, .neg 342, .neg 343, .neg 344, .neg 345, .neg 346, .neg 347, .neg 348, .neg 349, .neg 350, .neg 351, .neg 352, .neg 353, .neg 354, .neg 356, .neg 357, .neg 358, .neg 359, .neg 360]
private def clause988 : Sat.Clause := [.pos 0]
private def clause989 : Sat.Clause := [.pos 67]
private def clause990 : Sat.Clause := [.neg 89, .neg 90, .pos 91, .neg 93, .pos 94]
private def clause991 : Sat.Clause := [.neg 89, .neg 90, .pos 91, .neg 94, .pos 95]
private def clause992 : Sat.Clause := [.neg 89, .neg 90, .pos 91, .neg 95]
private def clause993 : Sat.Clause := [.neg 89, .neg 91, .pos 92, .neg 93, .pos 94]
private def clause994 : Sat.Clause := [.neg 89, .neg 91, .pos 92, .neg 94, .pos 95]
private def clause995 : Sat.Clause := [.neg 89, .neg 91, .pos 92, .neg 95]
private def clause996 : Sat.Clause := [.pos 96]
private def clause997 : Sat.Clause := [.pos 98]
private def clause998 : Sat.Clause := [.pos 101]
private def clause999 : Sat.Clause := [.pos 104]
private def clause1000 : Sat.Clause := [.neg 120]
private def clause1001 : Sat.Clause := [.pos 122]
private def clause1002 : Sat.Clause := [.pos 124]
private def clause1003 : Sat.Clause := [.neg 135]
private def clause1004 : Sat.Clause := [.neg 139]
private def clause1005 : Sat.Clause := [.pos 140]
private def clause1006 : Sat.Clause := [.pos 141]
private def clause1007 : Sat.Clause := [.pos 144]
private def clause1008 : Sat.Clause := [.pos 147]
private def clause1009 : Sat.Clause := [.neg 159]
private def clause1010 : Sat.Clause := [.pos 171]
private def clause1011 : Sat.Clause := [.pos 172]
private def clause1012 : Sat.Clause := [.neg 175]
private def clause1013 : Sat.Clause := [.pos 177]
private def clause1014 : Sat.Clause := [.pos 179]
private def clause1015 : Sat.Clause := [.neg 190]
private def clause1016 : Sat.Clause := [.pos 192]
private def clause1017 : Sat.Clause := [.pos 193]
private def clause1018 : Sat.Clause := [.neg 200]
private def clause1019 : Sat.Clause := [.neg 202]
private def clause1020 : Sat.Clause := [.neg 203]
private def clause1021 : Sat.Clause := [.neg 206]
private def clause1022 : Sat.Clause := [.pos 208]
private def clause1023 : Sat.Clause := [.pos 211]
private def clause1024 : Sat.Clause := [.pos 213]
private def clause1025 : Sat.Clause := [.neg 215]
private def clause1026 : Sat.Clause := [.neg 218]
private def clause1027 : Sat.Clause := [.neg 219]
private def clause1028 : Sat.Clause := [.neg 220]

private def clauses : Sat.Fmla := [
  clause000, clause001, clause002, clause003, clause004, clause005, clause006, clause007, clause008, clause009, clause010, clause011, clause012, clause013, clause014, clause015, clause016, clause017, clause018, clause019, clause020, clause021, clause022, clause023, clause024, clause025, clause026, clause027, clause028, clause029, clause030, clause031, clause032, clause033, clause034, clause035, clause036, clause037, clause038, clause039, clause040, clause041, clause042, clause043, clause044, clause045, clause046, clause047, clause048, clause049, clause050, clause051, clause052, clause053, clause054, clause055, clause056, clause057, clause058, clause059, clause060, clause061, clause062, clause063, clause064, clause065, clause066, clause067, clause068, clause069, clause070, clause071, clause072, clause073, clause074, clause075, clause076, clause077, clause078, clause079, clause080, clause081, clause082, clause083, clause084, clause085, clause086, clause087, clause088, clause089, clause090, clause091, clause092, clause093, clause094, clause095, clause096, clause097, clause098, clause099, clause100, clause101, clause102, clause103, clause104, clause105, clause106, clause107, clause108, clause109, clause110, clause111, clause112, clause113, clause114, clause115, clause116, clause117, clause118, clause119, clause120, clause121, clause122, clause123, clause124, clause125, clause126, clause127, clause128, clause129, clause130, clause131, clause132, clause133, clause134, clause135, clause136, clause137, clause138, clause139, clause140, clause141, clause142, clause143, clause144, clause145, clause146, clause147, clause148, clause149, clause150, clause151, clause152, clause153, clause154, clause155, clause156, clause157, clause158, clause159, clause160, clause161, clause162, clause163, clause164, clause165, clause166, clause167, clause168, clause169, clause170, clause171, clause172, clause173, clause174, clause175, clause176, clause177, clause178, clause179, clause180, clause181, clause182, clause183, clause184, clause185, clause186, clause187, clause188, clause189, clause190, clause191, clause192, clause193, clause194, clause195, clause196, clause197, clause198, clause199, clause200, clause201, clause202, clause203, clause204, clause205, clause206, clause207, clause208, clause209, clause210, clause211, clause212, clause213, clause214, clause215, clause216, clause217, clause218, clause219, clause220, clause221, clause222, clause223, clause224, clause225, clause226, clause227, clause228, clause229, clause230, clause231, clause232, clause233, clause234, clause235, clause236, clause237, clause238, clause239, clause240, clause241, clause242, clause243, clause244, clause245, clause246, clause247, clause248, clause249, clause250, clause251, clause252, clause253, clause254, clause255, clause256, clause257, clause258, clause259, clause260, clause261, clause262, clause263, clause264, clause265, clause266, clause267, clause268, clause269, clause270, clause271, clause272, clause273, clause274, clause275, clause276, clause277, clause278, clause279, clause280, clause281, clause282, clause283, clause284, clause285, clause286, clause287, clause288, clause289, clause290, clause291, clause292, clause293, clause294, clause295, clause296, clause297, clause298, clause299, clause300, clause301, clause302, clause303, clause304, clause305, clause306, clause307, clause308, clause309, clause310, clause311, clause312, clause313, clause314, clause315, clause316, clause317, clause318, clause319, clause320, clause321, clause322, clause323, clause324, clause325, clause326, clause327, clause328, clause329, clause330, clause331, clause332, clause333, clause334, clause335, clause336, clause337, clause338, clause339, clause340, clause341, clause342, clause343, clause344, clause345, clause346, clause347, clause348, clause349, clause350, clause351, clause352, clause353, clause354, clause355, clause356, clause357, clause358, clause359, clause360, clause361, clause362, clause363, clause364, clause365, clause366, clause367, clause368, clause369, clause370, clause371, clause372, clause373, clause374, clause375, clause376, clause377, clause378, clause379, clause380, clause381, clause382, clause383, clause384, clause385, clause386, clause387, clause388, clause389, clause390, clause391, clause392, clause393, clause394, clause395, clause396, clause397, clause398, clause399, clause400, clause401, clause402, clause403, clause404, clause405, clause406, clause407, clause408, clause409, clause410, clause411, clause412, clause413, clause414, clause415, clause416, clause417, clause418, clause419, clause420, clause421, clause422, clause423, clause424, clause425, clause426, clause427, clause428, clause429, clause430, clause431, clause432, clause433, clause434, clause435, clause436, clause437, clause438, clause439, clause440, clause441, clause442, clause443, clause444, clause445, clause446, clause447, clause448, clause449, clause450, clause451, clause452, clause453, clause454, clause455, clause456, clause457, clause458, clause459, clause460, clause461, clause462, clause463, clause464, clause465, clause466, clause467, clause468, clause469, clause470, clause471, clause472, clause473, clause474, clause475, clause476, clause477, clause478, clause479, clause480, clause481, clause482, clause483, clause484, clause485, clause486, clause487, clause488, clause489, clause490, clause491, clause492, clause493, clause494, clause495, clause496, clause497, clause498, clause499, clause500, clause501, clause502, clause503, clause504, clause505, clause506, clause507, clause508, clause509, clause510, clause511, clause512, clause513, clause514, clause515, clause516, clause517, clause518, clause519, clause520, clause521, clause522, clause523, clause524, clause525, clause526, clause527, clause528, clause529, clause530, clause531, clause532, clause533, clause534, clause535, clause536, clause537, clause538, clause539, clause540, clause541, clause542, clause543, clause544, clause545, clause546, clause547, clause548, clause549, clause550, clause551, clause552, clause553, clause554, clause555, clause556, clause557, clause558, clause559, clause560, clause561, clause562, clause563, clause564, clause565, clause566, clause567, clause568, clause569, clause570, clause571, clause572, clause573, clause574, clause575, clause576, clause577, clause578, clause579, clause580, clause581, clause582, clause583, clause584, clause585, clause586, clause587, clause588, clause589, clause590, clause591, clause592, clause593, clause594, clause595, clause596, clause597, clause598, clause599, clause600, clause601, clause602, clause603, clause604, clause605, clause606, clause607, clause608, clause609, clause610, clause611, clause612, clause613, clause614, clause615, clause616, clause617, clause618, clause619, clause620, clause621, clause622, clause623, clause624, clause625, clause626, clause627, clause628, clause629, clause630, clause631, clause632, clause633, clause634, clause635, clause636, clause637, clause638, clause639, clause640, clause641, clause642, clause643, clause644, clause645, clause646, clause647, clause648, clause649, clause650, clause651, clause652, clause653, clause654, clause655, clause656, clause657, clause658, clause659, clause660, clause661, clause662, clause663, clause664, clause665, clause666, clause667, clause668, clause669, clause670, clause671, clause672, clause673, clause674, clause675, clause676, clause677, clause678, clause679, clause680, clause681, clause682, clause683, clause684, clause685, clause686, clause687, clause688, clause689, clause690, clause691, clause692, clause693, clause694, clause695, clause696, clause697, clause698, clause699, clause700, clause701, clause702, clause703, clause704, clause705, clause706, clause707, clause708, clause709, clause710, clause711, clause712, clause713, clause714, clause715, clause716, clause717, clause718, clause719, clause720, clause721, clause722, clause723, clause724, clause725, clause726, clause727, clause728, clause729, clause730, clause731, clause732, clause733, clause734, clause735, clause736, clause737, clause738, clause739, clause740, clause741, clause742, clause743, clause744, clause745, clause746, clause747, clause748, clause749, clause750, clause751, clause752, clause753, clause754, clause755, clause756, clause757, clause758, clause759, clause760, clause761, clause762, clause763, clause764, clause765, clause766, clause767, clause768, clause769, clause770, clause771, clause772, clause773, clause774, clause775, clause776, clause777, clause778, clause779, clause780, clause781, clause782, clause783, clause784, clause785, clause786, clause787, clause788, clause789, clause790, clause791, clause792, clause793, clause794, clause795, clause796, clause797, clause798, clause799, clause800, clause801, clause802, clause803, clause804, clause805, clause806, clause807, clause808, clause809, clause810, clause811, clause812, clause813, clause814, clause815, clause816, clause817, clause818, clause819, clause820, clause821, clause822, clause823, clause824, clause825, clause826, clause827, clause828, clause829, clause830, clause831, clause832, clause833, clause834, clause835, clause836, clause837, clause838, clause839, clause840, clause841, clause842, clause843, clause844, clause845, clause846, clause847, clause848, clause849, clause850, clause851, clause852, clause853, clause854, clause855, clause856, clause857, clause858, clause859, clause860, clause861, clause862, clause863, clause864, clause865, clause866, clause867, clause868, clause869, clause870, clause871, clause872, clause873, clause874, clause875, clause876, clause877, clause878, clause879, clause880, clause881, clause882, clause883, clause884, clause885, clause886, clause887, clause888, clause889, clause890, clause891, clause892, clause893, clause894, clause895, clause896, clause897, clause898, clause899, clause900, clause901, clause902, clause903, clause904, clause905, clause906, clause907, clause908, clause909, clause910, clause911, clause912, clause913, clause914, clause915, clause916, clause917, clause918, clause919, clause920, clause921, clause922, clause923, clause924, clause925, clause926, clause927, clause928, clause929, clause930, clause931, clause932, clause933, clause934, clause935, clause936, clause937, clause938, clause939, clause940, clause941, clause942, clause943, clause944, clause945, clause946, clause947, clause948, clause949, clause950, clause951, clause952, clause953, clause954, clause955, clause956, clause957, clause958, clause959, clause960, clause961, clause962, clause963, clause964, clause965, clause966, clause967, clause968, clause969, clause970, clause971, clause972, clause973, clause974, clause975, clause976, clause977, clause978, clause979, clause980, clause981, clause982, clause983, clause984, clause985, clause986, clause987, clause988, clause989, clause990, clause991, clause992, clause993, clause994, clause995, clause996, clause997, clause998, clause999, clause1000, clause1001, clause1002, clause1003, clause1004, clause1005, clause1006, clause1007, clause1008, clause1009, clause1010, clause1011, clause1012, clause1013, clause1014, clause1015, clause1016, clause1017, clause1018, clause1019, clause1020, clause1021, clause1022, clause1023, clause1024, clause1025, clause1026, clause1027, clause1028]

private theorem formula_eq : cnf_refutation.formula = clauses := by rfl

variable {n : ℕ} {σ : Fin 13 → Fin 154} (C : Context 13 n σ) (compatible : Compatible σ)
include compatible

-- Clause 1: order_transitive; source clause 3954.
omit compatible in
private theorem sound000 : C.clause (decodeClause atoms clause000) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 1 2 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 2: growth; source clause 3959.
omit compatible in
private theorem sound001 : C.clause (decodeClause atoms clause001) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 1 2 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 3: growth; source clause 3960.
omit compatible in
private theorem sound002 : C.clause (decodeClause atoms clause002) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 1 2 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 4: growth; source clause 3961.
omit compatible in
private theorem sound003 : C.clause (decodeClause atoms clause003) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 1 2 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 5: order_transitive; source clause 3965.
omit compatible in
private theorem sound004 : C.clause (decodeClause atoms clause004) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 1 3 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 6: order_transitive; source clause 4009.
omit compatible in
private theorem sound005 : C.clause (decodeClause atoms clause005) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 1 7 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 7: order_transitive; source clause 4086.
omit compatible in
private theorem sound006 : C.clause (decodeClause atoms clause006) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 2 3 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 8: order_transitive; source clause 4119.
omit compatible in
private theorem sound007 : C.clause (decodeClause atoms clause007) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 2 6 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 9: order_transitive; source clause 4163.
omit compatible in
private theorem sound008 : C.clause (decodeClause atoms clause008) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 2 10 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 10: order_transitive; source clause 4174.
omit compatible in
private theorem sound009 : C.clause (decodeClause atoms clause009) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 2 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 11: order_transitive; source clause 4702.
omit compatible in
private theorem sound010 : C.clause (decodeClause atoms clause010) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 7 3 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 12: order_transitive; source clause 4735.
omit compatible in
private theorem sound011 : C.clause (decodeClause atoms clause011) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 7 6 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 13: order_transitive; source clause 4779.
omit compatible in
private theorem sound012 : C.clause (decodeClause atoms clause012) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 7 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 14: growth; source clause 5143.
omit compatible in
private theorem sound013 : C.clause (decodeClause atoms clause013) := by
  exact C.covered_clause _ _ (C.growth_clause false 0 10 11 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 15: growth; source clause 5235.
omit compatible in
private theorem sound014 : C.clause (decodeClause atoms clause014) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 11 7 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 16: order_transitive; source clause 5538.
omit compatible in
private theorem sound015 : C.clause (decodeClause atoms clause015) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 2 3 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 17: growth; source clause 5544.
omit compatible in
private theorem sound016 : C.clause (decodeClause atoms clause016) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 2 3 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 18: growth; source clause 5545.
omit compatible in
private theorem sound017 : C.clause (decodeClause atoms clause017) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 2 3 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 19: growth; source clause 5546.
omit compatible in
private theorem sound018 : C.clause (decodeClause atoms clause018) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 2 3 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 20: order_transitive; source clause 5571.
omit compatible in
private theorem sound019 : C.clause (decodeClause atoms clause019) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 2 6 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 21: order_transitive; source clause 5615.
omit compatible in
private theorem sound020 : C.clause (decodeClause atoms clause020) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 2 10 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 22: growth; source clause 5621.
omit compatible in
private theorem sound021 : C.clause (decodeClause atoms clause021) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 2 10 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 23: order_transitive; source clause 5626.
omit compatible in
private theorem sound022 : C.clause (decodeClause atoms clause022) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 2 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 24: growth; source clause 6100.
omit compatible in
private theorem sound023 : C.clause (decodeClause atoms clause023) := by
  exact C.covered_clause _ _ (C.growth_clause false 1 6 10 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 25: order_transitive; source clause 6110.
omit compatible in
private theorem sound024 : C.clause (decodeClause atoms clause024) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 6 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 26: order_transitive; source clause 6187.
omit compatible in
private theorem sound025 : C.clause (decodeClause atoms clause025) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 7 6 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 27: growth; source clause 6595.
omit compatible in
private theorem sound026 : C.clause (decodeClause atoms clause026) := by
  exact C.covered_clause _ _ (C.growth_clause false 1 10 11 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 28: order_transitive; source clause 6682.
omit compatible in
private theorem sound027 : C.clause (decodeClause atoms clause027) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 11 7 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 29: order_transitive; source clause 7144.
omit compatible in
private theorem sound028 : C.clause (decodeClause atoms clause028) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 3 6 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 30: growth; source clause 7151.
omit compatible in
private theorem sound029 : C.clause (decodeClause atoms clause029) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 3 6 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 31: growth; source clause 7152.
omit compatible in
private theorem sound030 : C.clause (decodeClause atoms clause030) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 3 6 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 32: growth; source clause 7153.
omit compatible in
private theorem sound031 : C.clause (decodeClause atoms clause031) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 3 6 (by decide) (by decide) (by decide) 5) (by decide +kernel)

-- Clause 33: order_transitive; source clause 7199.
omit compatible in
private theorem sound032 : C.clause (decodeClause atoms clause032) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 3 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 34: order_transitive; source clause 7254.
omit compatible in
private theorem sound033 : C.clause (decodeClause atoms clause033) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 4 5 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 35: growth; source clause 7259.
omit compatible in
private theorem sound034 : C.clause (decodeClause atoms clause034) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 4 5 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 36: order_transitive; source clause 7287.
omit compatible in
private theorem sound035 : C.clause (decodeClause atoms clause035) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 4 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 37: order_transitive; source clause 7298.
omit compatible in
private theorem sound036 : C.clause (decodeClause atoms clause036) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 4 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 38: order_transitive; source clause 7408.
omit compatible in
private theorem sound037 : C.clause (decodeClause atoms clause037) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 5 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 39: order_transitive; source clause 7419.
omit compatible in
private theorem sound038 : C.clause (decodeClause atoms clause038) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 5 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 40: order_transitive; source clause 7485.
omit compatible in
private theorem sound039 : C.clause (decodeClause atoms clause039) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 6 3 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 41: order_transitive; source clause 7496.
omit compatible in
private theorem sound040 : C.clause (decodeClause atoms clause040) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 6 4 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 42: order_transitive; source clause 7518.
omit compatible in
private theorem sound041 : C.clause (decodeClause atoms clause041) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 6 7 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 43: order_transitive; source clause 7529.
omit compatible in
private theorem sound042 : C.clause (decodeClause atoms clause042) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 6 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 44: order_transitive; source clause 7540.
omit compatible in
private theorem sound043 : C.clause (decodeClause atoms clause043) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 6 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 45: order_transitive; source clause 7551.
omit compatible in
private theorem sound044 : C.clause (decodeClause atoms clause044) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 6 10 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 46: growth; source clause 7552.
omit compatible in
private theorem sound045 : C.clause (decodeClause atoms clause045) := by
  exact C.covered_clause _ _ (C.growth_clause false 2 6 10 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 47: order_transitive; source clause 7562.
omit compatible in
private theorem sound046 : C.clause (decodeClause atoms clause046) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 6 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 48: order_transitive; source clause 7606.
omit compatible in
private theorem sound047 : C.clause (decodeClause atoms clause047) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 7 3 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 49: order_transitive; source clause 7639.
omit compatible in
private theorem sound048 : C.clause (decodeClause atoms clause048) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 7 6 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 50: order_transitive; source clause 7683.
omit compatible in
private theorem sound049 : C.clause (decodeClause atoms clause049) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 7 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 51: order_transitive; source clause 7782.
omit compatible in
private theorem sound050 : C.clause (decodeClause atoms clause050) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 8 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 52: order_transitive; source clause 7859.
omit compatible in
private theorem sound051 : C.clause (decodeClause atoms clause051) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 9 4 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 53: order_transitive; source clause 7980.
omit compatible in
private theorem sound052 : C.clause (decodeClause atoms clause052) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 10 4 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 54: order_transitive; source clause 7991.
omit compatible in
private theorem sound053 : C.clause (decodeClause atoms clause053) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 10 5 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 55: order_transitive; source clause 8024.
omit compatible in
private theorem sound054 : C.clause (decodeClause atoms clause054) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 10 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 56: order_transitive; source clause 8035.
omit compatible in
private theorem sound055 : C.clause (decodeClause atoms clause055) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 10 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 57: order_transitive; source clause 8046.
omit compatible in
private theorem sound056 : C.clause (decodeClause atoms clause056) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 10 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 58: growth; source clause 8047.
omit compatible in
private theorem sound057 : C.clause (decodeClause atoms clause057) := by
  exact C.covered_clause _ _ (C.growth_clause false 2 10 11 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 59: growth; source clause 8048.
omit compatible in
private theorem sound058 : C.clause (decodeClause atoms clause058) := by
  exact C.covered_clause _ _ (C.growth_clause false 2 10 11 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 60: growth; source clause 8049.
omit compatible in
private theorem sound059 : C.clause (decodeClause atoms clause059) := by
  exact C.covered_clause _ _ (C.growth_clause false 2 10 11 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 61: growth; source clause 8053.
omit compatible in
private theorem sound060 : C.clause (decodeClause atoms clause060) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 10 11 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 62: order_transitive; source clause 8057.
omit compatible in
private theorem sound061 : C.clause (decodeClause atoms clause061) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 10 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 63: order_transitive; source clause 8123.
omit compatible in
private theorem sound062 : C.clause (decodeClause atoms clause062) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 11 6 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 64: order_transitive; source clause 8156.
omit compatible in
private theorem sound063 : C.clause (decodeClause atoms clause063) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 11 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 65: order_transitive; source clause 8167.
omit compatible in
private theorem sound064 : C.clause (decodeClause atoms clause064) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 11 10 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 66: order_transitive; source clause 8222.
omit compatible in
private theorem sound065 : C.clause (decodeClause atoms clause065) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 12 4 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 67: order_transitive; source clause 8277.
omit compatible in
private theorem sound066 : C.clause (decodeClause atoms clause066) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 12 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 68: order_transitive; source clause 9003.
omit compatible in
private theorem sound067 : C.clause (decodeClause atoms clause067) := by
  exact C.covered_clause _ _ (C.transitive_clause 3 6 10 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 69: growth; source clause 9011.
omit compatible in
private theorem sound068 : C.clause (decodeClause atoms clause068) := by
  exact C.covered_clause _ _ (C.growth_clause true 3 6 10 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 70: growth; source clause 9012.
omit compatible in
private theorem sound069 : C.clause (decodeClause atoms clause069) := by
  exact C.covered_clause _ _ (C.growth_clause true 3 6 10 (by decide) (by decide) (by decide) 5) (by decide +kernel)

-- Clause 71: growth; source clause 9013.
omit compatible in
private theorem sound070 : C.clause (decodeClause atoms clause070) := by
  exact C.covered_clause _ _ (C.growth_clause true 3 6 10 (by decide) (by decide) (by decide) 6) (by decide +kernel)

-- Clause 72: order_transitive; source clause 9014.
omit compatible in
private theorem sound071 : C.clause (decodeClause atoms clause071) := by
  exact C.covered_clause _ _ (C.transitive_clause 3 6 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 73: order_transitive; source clause 9091.
omit compatible in
private theorem sound072 : C.clause (decodeClause atoms clause072) := by
  exact C.covered_clause _ _ (C.transitive_clause 3 7 6 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 74: order_transitive; source clause 9135.
omit compatible in
private theorem sound073 : C.clause (decodeClause atoms clause073) := by
  exact C.covered_clause _ _ (C.transitive_clause 3 7 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 75: order_transitive; source clause 9465.
omit compatible in
private theorem sound074 : C.clause (decodeClause atoms clause074) := by
  exact C.covered_clause _ _ (C.transitive_clause 3 10 7 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 76: growth; source clause 9499.
omit compatible in
private theorem sound075 : C.clause (decodeClause atoms clause075) := by
  exact C.covered_clause _ _ (C.growth_clause false 3 10 11 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 77: order_transitive; source clause 9619.
omit compatible in
private theorem sound076 : C.clause (decodeClause atoms clause076) := by
  exact C.covered_clause _ _ (C.transitive_clause 3 11 10 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 78: growth; source clause 10093.
omit compatible in
private theorem sound077 : C.clause (decodeClause atoms clause077) := by
  exact C.covered_clause _ _ (C.growth_clause false 4 2 10 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 79: growth; source clause 10094.
omit compatible in
private theorem sound078 : C.clause (decodeClause atoms clause078) := by
  exact C.covered_clause _ _ (C.growth_clause false 4 2 10 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 80: order_transitive; source clause 10312.
omit compatible in
private theorem sound079 : C.clause (decodeClause atoms clause079) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 5 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 81: growth; source clause 10317.
omit compatible in
private theorem sound080 : C.clause (decodeClause atoms clause080) := by
  exact C.covered_clause _ _ (C.growth_clause true 4 5 8 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 82: order_transitive; source clause 10323.
omit compatible in
private theorem sound081 : C.clause (decodeClause atoms clause081) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 5 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 83: order_transitive; source clause 10334.
omit compatible in
private theorem sound082 : C.clause (decodeClause atoms clause082) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 5 10 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 84: growth; source clause 10340.
omit compatible in
private theorem sound083 : C.clause (decodeClause atoms clause083) := by
  exact C.covered_clause _ _ (C.growth_clause true 4 5 10 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 85: order_transitive; source clause 10345.
omit compatible in
private theorem sound084 : C.clause (decodeClause atoms clause084) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 5 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 86: order_transitive; source clause 10356.
omit compatible in
private theorem sound085 : C.clause (decodeClause atoms clause085) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 5 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 87: order_transitive; source clause 10455.
omit compatible in
private theorem sound086 : C.clause (decodeClause atoms clause086) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 6 10 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 88: order_transitive; source clause 10466.
omit compatible in
private theorem sound087 : C.clause (decodeClause atoms clause087) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 6 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 89: order_transitive; source clause 10653.
omit compatible in
private theorem sound088 : C.clause (decodeClause atoms clause088) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 8 5 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 90: order_transitive; source clause 10686.
omit compatible in
private theorem sound089 : C.clause (decodeClause atoms clause089) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 8 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 91: order_transitive; source clause 10697.
omit compatible in
private theorem sound090 : C.clause (decodeClause atoms clause090) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 8 10 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 92: order_transitive; source clause 10719.
omit compatible in
private theorem sound091 : C.clause (decodeClause atoms clause091) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 8 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 93: order_transitive; source clause 10774.
omit compatible in
private theorem sound092 : C.clause (decodeClause atoms clause092) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 9 5 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 94: order_transitive; source clause 10928.
omit compatible in
private theorem sound093 : C.clause (decodeClause atoms clause093) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 10 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 95: order_transitive; source clause 10939.
omit compatible in
private theorem sound094 : C.clause (decodeClause atoms clause094) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 10 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 96: order_transitive; source clause 10950.
omit compatible in
private theorem sound095 : C.clause (decodeClause atoms clause095) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 10 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 97: order_transitive; source clause 10961.
omit compatible in
private theorem sound096 : C.clause (decodeClause atoms clause096) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 10 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 98: growth; source clause 10965.
omit compatible in
private theorem sound097 : C.clause (decodeClause atoms clause097) := by
  exact C.covered_clause _ _ (C.growth_clause false 4 10 12 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 99: order_transitive; source clause 11082.
omit compatible in
private theorem sound098 : C.clause (decodeClause atoms clause098) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 11 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 100: order_transitive; source clause 11137.
omit compatible in
private theorem sound099 : C.clause (decodeClause atoms clause099) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 12 5 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 101: order_transitive; source clause 11170.
omit compatible in
private theorem sound100 : C.clause (decodeClause atoms clause100) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 12 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 102: order_transitive; source clause 11181.
omit compatible in
private theorem sound101 : C.clause (decodeClause atoms clause101) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 12 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 103: growth; source clause 11721.
omit compatible in
private theorem sound102 : C.clause (decodeClause atoms clause102) := by
  exact C.covered_clause _ _ (C.growth_clause false 5 4 2 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 104: growth; source clause 11789.
omit compatible in
private theorem sound103 : C.clause (decodeClause atoms clause103) := by
  exact C.covered_clause _ _ (C.growth_clause false 5 4 10 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 105: order_transitive; source clause 12138.
omit compatible in
private theorem sound104 : C.clause (decodeClause atoms clause104) := by
  exact C.covered_clause _ _ (C.transitive_clause 5 8 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 106: growth; source clause 12144.
omit compatible in
private theorem sound105 : C.clause (decodeClause atoms clause105) := by
  exact C.covered_clause _ _ (C.growth_clause true 5 8 9 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 107: order_transitive; source clause 12149.
omit compatible in
private theorem sound106 : C.clause (decodeClause atoms clause106) := by
  exact C.covered_clause _ _ (C.transitive_clause 5 8 10 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 108: growth; source clause 12155.
omit compatible in
private theorem sound107 : C.clause (decodeClause atoms clause107) := by
  exact C.covered_clause _ _ (C.growth_clause true 5 8 10 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 109: order_transitive; source clause 12160.
omit compatible in
private theorem sound108 : C.clause (decodeClause atoms clause108) := by
  exact C.covered_clause _ _ (C.transitive_clause 5 8 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 110: order_transitive; source clause 12171.
omit compatible in
private theorem sound109 : C.clause (decodeClause atoms clause109) := by
  exact C.covered_clause _ _ (C.transitive_clause 5 8 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 111: order_transitive; source clause 12391.
omit compatible in
private theorem sound110 : C.clause (decodeClause atoms clause110) := by
  exact C.covered_clause _ _ (C.transitive_clause 5 10 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 112: order_transitive; source clause 12402.
omit compatible in
private theorem sound111 : C.clause (decodeClause atoms clause111) := by
  exact C.covered_clause _ _ (C.transitive_clause 5 10 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 113: growth; source clause 12404.
omit compatible in
private theorem sound112 : C.clause (decodeClause atoms clause112) := by
  exact C.covered_clause _ _ (C.growth_clause false 5 10 11 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 114: growth; source clause 12409.
omit compatible in
private theorem sound113 : C.clause (decodeClause atoms clause113) := by
  exact C.covered_clause _ _ (C.growth_clause true 5 10 11 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 115: order_transitive; source clause 12413.
omit compatible in
private theorem sound114 : C.clause (decodeClause atoms clause114) := by
  exact C.covered_clause _ _ (C.transitive_clause 5 10 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 116: order_transitive; source clause 12523.
omit compatible in
private theorem sound115 : C.clause (decodeClause atoms clause115) := by
  exact C.covered_clause _ _ (C.transitive_clause 5 11 10 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 117: order_transitive; source clause 12534.
omit compatible in
private theorem sound116 : C.clause (decodeClause atoms clause116) := by
  exact C.covered_clause _ _ (C.transitive_clause 5 11 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 118: order_transitive; source clause 12633.
omit compatible in
private theorem sound117 : C.clause (decodeClause atoms clause117) := by
  exact C.covered_clause _ _ (C.transitive_clause 5 12 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 119: order_transitive; source clause 13491.
omit compatible in
private theorem sound118 : C.clause (decodeClause atoms clause118) := by
  exact C.covered_clause _ _ (C.transitive_clause 6 7 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 120: order_transitive; source clause 13832.
omit compatible in
private theorem sound119 : C.clause (decodeClause atoms clause119) := by
  exact C.covered_clause _ _ (C.transitive_clause 6 10 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 121: order_transitive; source clause 13843.
omit compatible in
private theorem sound120 : C.clause (decodeClause atoms clause120) := by
  exact C.covered_clause _ _ (C.transitive_clause 6 10 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 122: order_transitive; source clause 13854.
omit compatible in
private theorem sound121 : C.clause (decodeClause atoms clause121) := by
  exact C.covered_clause _ _ (C.transitive_clause 6 10 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 123: growth; source clause 13855.
omit compatible in
private theorem sound122 : C.clause (decodeClause atoms clause122) := by
  exact C.covered_clause _ _ (C.growth_clause false 6 10 11 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 124: growth; source clause 13856.
omit compatible in
private theorem sound123 : C.clause (decodeClause atoms clause123) := by
  exact C.covered_clause _ _ (C.growth_clause false 6 10 11 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 125: growth; source clause 13863.
omit compatible in
private theorem sound124 : C.clause (decodeClause atoms clause124) := by
  exact C.covered_clause _ _ (C.growth_clause true 6 10 11 (by decide) (by decide) (by decide) 5) (by decide +kernel)

-- Clause 126: growth; source clause 13864.
omit compatible in
private theorem sound125 : C.clause (decodeClause atoms clause125) := by
  exact C.covered_clause _ _ (C.growth_clause true 6 10 11 (by decide) (by decide) (by decide) 6) (by decide +kernel)

-- Clause 127: growth; source clause 13866.
omit compatible in
private theorem sound126 : C.clause (decodeClause atoms clause126) := by
  exact C.covered_clause _ _ (C.growth_clause false 6 10 12 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 128: order_transitive; source clause 13942.
omit compatible in
private theorem sound127 : C.clause (decodeClause atoms clause127) := by
  exact C.covered_clause _ _ (C.transitive_clause 6 11 7 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 129: growth; source clause 14123.
omit compatible in
private theorem sound128 : C.clause (decodeClause atoms clause128) := by
  exact C.covered_clause _ _ (C.growth_clause true 7 0 1 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 130: growth; source clause 14124.
omit compatible in
private theorem sound129 : C.clause (decodeClause atoms clause129) := by
  exact C.covered_clause _ _ (C.growth_clause true 7 0 1 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 131: growth; source clause 14257.
omit compatible in
private theorem sound130 : C.clause (decodeClause atoms clause130) := by
  exact C.covered_clause _ _ (C.growth_clause true 7 1 2 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 132: order_transitive; source clause 15306.
omit compatible in
private theorem sound131 : C.clause (decodeClause atoms clause131) := by
  exact C.covered_clause _ _ (C.transitive_clause 7 10 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 133: order_transitive; source clause 15427.
omit compatible in
private theorem sound132 : C.clause (decodeClause atoms clause132) := by
  exact C.covered_clause _ _ (C.transitive_clause 7 11 10 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 134: order_transitive; source clause 15438.
omit compatible in
private theorem sound133 : C.clause (decodeClause atoms clause133) := by
  exact C.covered_clause _ _ (C.transitive_clause 7 11 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 135: growth; source clause 16221.
omit compatible in
private theorem sound134 : C.clause (decodeClause atoms clause134) := by
  exact C.covered_clause _ _ (C.growth_clause false 8 5 4 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 136: growth; source clause 16264.
omit compatible in
private theorem sound135 : C.clause (decodeClause atoms clause135) := by
  exact C.covered_clause _ _ (C.growth_clause false 8 5 10 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 137: growth; source clause 16633.
omit compatible in
private theorem sound136 : C.clause (decodeClause atoms clause136) := by
  exact C.covered_clause _ _ (C.growth_clause true 8 9 10 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 138: order_transitive; source clause 16637.
omit compatible in
private theorem sound137 : C.clause (decodeClause atoms clause137) := by
  exact C.covered_clause _ _ (C.transitive_clause 8 9 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 139: order_transitive; source clause 16747.
omit compatible in
private theorem sound138 : C.clause (decodeClause atoms clause138) := by
  exact C.covered_clause _ _ (C.transitive_clause 8 10 9 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 140: order_transitive; source clause 16758.
omit compatible in
private theorem sound139 : C.clause (decodeClause atoms clause139) := by
  exact C.covered_clause _ _ (C.transitive_clause 8 10 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 141: growth; source clause 16765.
omit compatible in
private theorem sound140 : C.clause (decodeClause atoms clause140) := by
  exact C.covered_clause _ _ (C.growth_clause true 8 10 11 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 142: order_transitive; source clause 16769.
omit compatible in
private theorem sound141 : C.clause (decodeClause atoms clause141) := by
  exact C.covered_clause _ _ (C.transitive_clause 8 10 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 143: order_transitive; source clause 16890.
omit compatible in
private theorem sound142 : C.clause (decodeClause atoms clause142) := by
  exact C.covered_clause _ _ (C.transitive_clause 8 11 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 144: growth; source clause 18046.
omit compatible in
private theorem sound143 : C.clause (decodeClause atoms clause143) := by
  exact C.covered_clause _ _ (C.growth_clause false 9 8 5 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 145: growth; source clause 18049.
omit compatible in
private theorem sound144 : C.clause (decodeClause atoms clause144) := by
  exact C.covered_clause _ _ (C.growth_clause false 9 8 5 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 146: order_transitive; source clause 18210.
omit compatible in
private theorem sound145 : C.clause (decodeClause atoms clause145) := by
  exact C.covered_clause _ _ (C.transitive_clause 9 10 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 147: growth; source clause 18218.
omit compatible in
private theorem sound146 : C.clause (decodeClause atoms clause146) := by
  exact C.covered_clause _ _ (C.growth_clause true 9 10 11 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 148: order_transitive; source clause 18221.
omit compatible in
private theorem sound147 : C.clause (decodeClause atoms clause147) := by
  exact C.covered_clause _ _ (C.transitive_clause 9 10 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 149: order_transitive; source clause 18342.
omit compatible in
private theorem sound148 : C.clause (decodeClause atoms clause148) := by
  exact C.covered_clause _ _ (C.transitive_clause 9 11 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 150: growth; source clause 19771.
omit compatible in
private theorem sound149 : C.clause (decodeClause atoms clause149) := by
  exact C.covered_clause _ _ (C.growth_clause true 10 11 7 (by decide) (by decide) (by decide) 6) (by decide +kernel)

-- Clause 151: growth; source clause 19796.
omit compatible in
private theorem sound150 : C.clause (decodeClause atoms clause150) := by
  exact C.covered_clause _ _ (C.growth_clause false 10 11 12 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 152: growth; source clause 19797.
omit compatible in
private theorem sound151 : C.clause (decodeClause atoms clause151) := by
  exact C.covered_clause _ _ (C.growth_clause false 10 11 12 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 153: growth; source clause 19798.
omit compatible in
private theorem sound152 : C.clause (decodeClause atoms clause152) := by
  exact C.covered_clause _ _ (C.growth_clause false 10 11 12 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 154: growth; source clause 19906.
omit compatible in
private theorem sound153 : C.clause (decodeClause atoms clause153) := by
  exact C.covered_clause _ _ (C.growth_clause false 10 12 9 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 155: growth; source clause 20778.
omit compatible in
private theorem sound154 : C.clause (decodeClause atoms clause154) := by
  exact C.covered_clause _ _ (C.growth_clause true 11 7 0 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 156: growth; source clause 20790.
omit compatible in
private theorem sound155 : C.clause (decodeClause atoms clause155) := by
  exact C.covered_clause _ _ (C.growth_clause true 11 7 1 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 157: growth; source clause 21359.
omit compatible in
private theorem sound156 : C.clause (decodeClause atoms clause156) := by
  exact C.covered_clause _ _ (C.growth_clause false 11 12 9 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 158: growth; source clause 21360.
omit compatible in
private theorem sound157 : C.clause (decodeClause atoms clause157) := by
  exact C.covered_clause _ _ (C.growth_clause false 11 12 9 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 159: growth; source clause 22515.
omit compatible in
private theorem sound158 : C.clause (decodeClause atoms clause158) := by
  exact C.covered_clause _ _ (C.growth_clause false 12 9 4 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 160: growth; source clause 22526.
omit compatible in
private theorem sound159 : C.clause (decodeClause atoms clause159) := by
  exact C.covered_clause _ _ (C.growth_clause false 12 9 5 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 161: growth; source clause 22558.
omit compatible in
private theorem sound160 : C.clause (decodeClause atoms clause160) := by
  exact C.covered_clause _ _ (C.growth_clause false 12 9 8 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 162: growth; source clause 22559.
omit compatible in
private theorem sound161 : C.clause (decodeClause atoms clause161) := by
  exact C.covered_clause _ _ (C.growth_clause false 12 9 8 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 163: packet; source clause 23014.
omit compatible in
private theorem sound162 : C.clause (decodeClause atoms clause162) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 2 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 164: packet; source clause 23016.
omit compatible in
private theorem sound163 : C.clause (decodeClause atoms clause163) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 2 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 165: packet; source clause 23017.
omit compatible in
private theorem sound164 : C.clause (decodeClause atoms clause164) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 2 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 166: convex_four; source clause 23217.
omit compatible in
private theorem sound165 : C.clause (decodeClause atoms clause165) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 167: convex_four; source clause 23841.
omit compatible in
private theorem sound166 : C.clause (decodeClause atoms clause166) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 168: packet; source clause 23849.
omit compatible in
private theorem sound167 : C.clause (decodeClause atoms clause167) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 2 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 169: packet; source clause 23858.
omit compatible in
private theorem sound168 : C.clause (decodeClause atoms clause168) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 1 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 170: packet; source clause 23861.
omit compatible in
private theorem sound169 : C.clause (decodeClause atoms clause169) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 1 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 171: packet; source clause 23942.
omit compatible in
private theorem sound170 : C.clause (decodeClause atoms clause170) := by
  exact C.covered_clause _ _ (C.packet_clause 2 0 1 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 172: packet; source clause 23945.
omit compatible in
private theorem sound171 : C.clause (decodeClause atoms clause171) := by
  exact C.covered_clause _ _ (C.packet_clause 2 0 1 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 173: packet; source clause 23992.
omit compatible in
private theorem sound172 : C.clause (decodeClause atoms clause172) := by
  exact C.covered_clause _ _ (C.packet_clause 7 0 1 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 174: convex_four; source clause 24049.
omit compatible in
private theorem sound173 : C.clause (decodeClause atoms clause173) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 175: convex_four; source clause 24673.
omit compatible in
private theorem sound174 : C.clause (decodeClause atoms clause174) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 176: convex_four; source clause 24881.
omit compatible in
private theorem sound175 : C.clause (decodeClause atoms clause175) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 177: packet; source clause 25512.
omit compatible in
private theorem sound176 : C.clause (decodeClause atoms clause176) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 178: convex_four; source clause 25713.
omit compatible in
private theorem sound177 : C.clause (decodeClause atoms clause177) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 179: packet; source clause 25746.
omit compatible in
private theorem sound178 : C.clause (decodeClause atoms clause178) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 1 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 180: packet; source clause 25749.
omit compatible in
private theorem sound179 : C.clause (decodeClause atoms clause179) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 1 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 181: packet; source clause 25864.
omit compatible in
private theorem sound180 : C.clause (decodeClause atoms clause180) := by
  exact C.covered_clause _ _ (C.packet_clause 7 0 1 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 182: convex_four; source clause 25921.
omit compatible in
private theorem sound181 : C.clause (decodeClause atoms clause181) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 183: packet; source clause 26438.
omit compatible in
private theorem sound182 : C.clause (decodeClause atoms clause182) := by
  exact C.covered_clause _ _ (C.packet_clause 3 0 1 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 184: convex_four; source clause 26545.
omit compatible in
private theorem sound183 : C.clause (decodeClause atoms clause183) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 185: convex_four; source clause 26753.
omit compatible in
private theorem sound184 : C.clause (decodeClause atoms clause184) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 186: packet; source clause 30097.
omit compatible in
private theorem sound185 : C.clause (decodeClause atoms clause185) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 7 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 187: convex_four; source clause 30289.
omit compatible in
private theorem sound186 : C.clause (decodeClause atoms clause186) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 188: packet; source clause 30712.
omit compatible in
private theorem sound187 : C.clause (decodeClause atoms clause187) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 189: convex_four; source clause 30913.
omit compatible in
private theorem sound188 : C.clause (decodeClause atoms clause188) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 190: packet; source clause 30923.
omit compatible in
private theorem sound189 : C.clause (decodeClause atoms clause189) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 11 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 191: convex_four; source clause 31121.
omit compatible in
private theorem sound190 : C.clause (decodeClause atoms clause190) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 192: packet; source clause 31753.
omit compatible in
private theorem sound191 : C.clause (decodeClause atoms clause191) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 193: convex_four; source clause 31950.
omit compatible in
private theorem sound192 : C.clause (decodeClause atoms clause192) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 194: packet; source clause 31978.
omit compatible in
private theorem sound193 : C.clause (decodeClause atoms clause193) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 11 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 195: packet; source clause 32082.
omit compatible in
private theorem sound194 : C.clause (decodeClause atoms clause194) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 196: packet; source clause 32106.
omit compatible in
private theorem sound195 : C.clause (decodeClause atoms clause195) := by
  exact C.covered_clause _ _ (C.packet_clause 11 0 7 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 197: packet; source clause 32109.
omit compatible in
private theorem sound196 : C.clause (decodeClause atoms clause196) := by
  exact C.covered_clause _ _ (C.packet_clause 11 0 7 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 198: convex_four; source clause 32158.
omit compatible in
private theorem sound197 : C.clause (decodeClause atoms clause197) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 199: packet; source clause 33832.
omit compatible in
private theorem sound198 : C.clause (decodeClause atoms clause198) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 200: packet; source clause 33835.
omit compatible in
private theorem sound199 : C.clause (decodeClause atoms clause199) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 201: packet; source clause 33864.
omit compatible in
private theorem sound200 : C.clause (decodeClause atoms clause200) := by
  exact C.covered_clause _ _ (C.packet_clause 0 11 1 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 202: convex_four; source clause 34025.
omit compatible in
private theorem sound201 : C.clause (decodeClause atoms clause201) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true true) (by decide +kernel)

-- Clause 203: convex_four; source clause 34029.
omit compatible in
private theorem sound202 : C.clause (decodeClause atoms clause202) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 204: convex_four; source clause 34033.
omit compatible in
private theorem sound203 : C.clause (decodeClause atoms clause203) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 205: packet; source clause 34870.
omit compatible in
private theorem sound204 : C.clause (decodeClause atoms clause204) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 206: packet; source clause 34872.
omit compatible in
private theorem sound205 : C.clause (decodeClause atoms clause205) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 207: packet; source clause 34873.
omit compatible in
private theorem sound206 : C.clause (decodeClause atoms clause206) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 208: convex_four; source clause 35073.
omit compatible in
private theorem sound207 : C.clause (decodeClause atoms clause207) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 209: packet; source clause 35081.
omit compatible in
private theorem sound208 : C.clause (decodeClause atoms clause208) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 210: packet; source clause 35224.
omit compatible in
private theorem sound209 : C.clause (decodeClause atoms clause209) := by
  exact C.covered_clause _ _ (C.packet_clause 7 0 2 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 211: convex_four; source clause 35281.
omit compatible in
private theorem sound210 : C.clause (decodeClause atoms clause210) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 212: convex_four; source clause 35905.
omit compatible in
private theorem sound211 : C.clause (decodeClause atoms clause211) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 213: convex_four; source clause 36113.
omit compatible in
private theorem sound212 : C.clause (decodeClause atoms clause212) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 214: packet; source clause 39480.
omit compatible in
private theorem sound213 : C.clause (decodeClause atoms clause213) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 2 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 215: packet; source clause 39592.
omit compatible in
private theorem sound214 : C.clause (decodeClause atoms clause214) := by
  exact C.covered_clause _ _ (C.packet_clause 7 0 2 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 216: convex_four; source clause 39649.
omit compatible in
private theorem sound215 : C.clause (decodeClause atoms clause215) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 217: packet; source clause 40070.
omit compatible in
private theorem sound216 : C.clause (decodeClause atoms clause216) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 218: packet; source clause 40072.
omit compatible in
private theorem sound217 : C.clause (decodeClause atoms clause217) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 219: packet; source clause 40073.
omit compatible in
private theorem sound218 : C.clause (decodeClause atoms clause218) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 220: convex_four; source clause 40273.
omit compatible in
private theorem sound219 : C.clause (decodeClause atoms clause219) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 221: packet; source clause 40280.
omit compatible in
private theorem sound220 : C.clause (decodeClause atoms clause220) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 222: convex_four; source clause 40473.
omit compatible in
private theorem sound221 : C.clause (decodeClause atoms clause221) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true true) (by decide +kernel)

-- Clause 223: convex_four; source clause 40481.
omit compatible in
private theorem sound222 : C.clause (decodeClause atoms clause222) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 224: packet; source clause 41113.
omit compatible in
private theorem sound223 : C.clause (decodeClause atoms clause223) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 225: packet; source clause 41207.
omit compatible in
private theorem sound224 : C.clause (decodeClause atoms clause224) := by
  exact C.covered_clause _ _ (C.packet_clause 7 0 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 226: packet; source clause 41208.
omit compatible in
private theorem sound225 : C.clause (decodeClause atoms clause225) := by
  exact C.covered_clause _ _ (C.packet_clause 7 0 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 227: convex_four; source clause 41310.
omit compatible in
private theorem sound226 : C.clause (decodeClause atoms clause226) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 228: packet; source clause 41442.
omit compatible in
private theorem sound227 : C.clause (decodeClause atoms clause227) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 0 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 229: convex_four; source clause 41510.
omit compatible in
private theorem sound228 : C.clause (decodeClause atoms clause228) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 230: convex_four; source clause 41518.
omit compatible in
private theorem sound229 : C.clause (decodeClause atoms clause229) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 231: packet; source clause 43195.
omit compatible in
private theorem sound230 : C.clause (decodeClause atoms clause230) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 232: packet; source clause 43224.
omit compatible in
private theorem sound231 : C.clause (decodeClause atoms clause231) := by
  exact C.covered_clause _ _ (C.packet_clause 0 11 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 233: convex_four; source clause 43385.
omit compatible in
private theorem sound232 : C.clause (decodeClause atoms clause232) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true true) (by decide +kernel)

-- Clause 234: convex_four; source clause 43393.
omit compatible in
private theorem sound233 : C.clause (decodeClause atoms clause233) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 235: packet; source clause 46937.
omit compatible in
private theorem sound234 : C.clause (decodeClause atoms clause234) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 236: packet; source clause 46968.
omit compatible in
private theorem sound235 : C.clause (decodeClause atoms clause235) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 237: packet; source clause 47080.
omit compatible in
private theorem sound236 : C.clause (decodeClause atoms clause236) := by
  exact C.covered_clause _ _ (C.packet_clause 7 0 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 238: convex_four; source clause 47137.
omit compatible in
private theorem sound237 : C.clause (decodeClause atoms clause237) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 239: packet; source clause 47560.
omit compatible in
private theorem sound238 : C.clause (decodeClause atoms clause238) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 240: convex_four; source clause 47761.
omit compatible in
private theorem sound239 : C.clause (decodeClause atoms clause239) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 241: packet; source clause 47768.
omit compatible in
private theorem sound240 : C.clause (decodeClause atoms clause240) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 242: convex_four; source clause 47961.
omit compatible in
private theorem sound241 : C.clause (decodeClause atoms clause241) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true true) (by decide +kernel)

-- Clause 243: convex_four; source clause 47969.
omit compatible in
private theorem sound242 : C.clause (decodeClause atoms clause242) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 244: convex_four; source clause 48798.
omit compatible in
private theorem sound243 : C.clause (decodeClause atoms clause243) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 245: convex_four; source clause 48800.
omit compatible in
private theorem sound244 : C.clause (decodeClause atoms clause244) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true false) (by decide +kernel)

-- Clause 246: packet; source clause 48826.
omit compatible in
private theorem sound245 : C.clause (decodeClause atoms clause245) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 11 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 247: packet; source clause 48913.
omit compatible in
private theorem sound246 : C.clause (decodeClause atoms clause246) := by
  exact C.covered_clause _ _ (C.packet_clause 7 0 11 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 248: packet; source clause 48930.
omit compatible in
private theorem sound247 : C.clause (decodeClause atoms clause247) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 0 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 249: convex_four; source clause 48998.
omit compatible in
private theorem sound248 : C.clause (decodeClause atoms clause248) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 250: convex_four; source clause 49006.
omit compatible in
private theorem sound249 : C.clause (decodeClause atoms clause249) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 251: packet; source clause 50680.
omit compatible in
private theorem sound250 : C.clause (decodeClause atoms clause250) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 252: packet; source clause 50683.
omit compatible in
private theorem sound251 : C.clause (decodeClause atoms clause251) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 253: packet; source clause 50824.
omit compatible in
private theorem sound252 : C.clause (decodeClause atoms clause252) := by
  exact C.covered_clause _ _ (C.packet_clause 11 0 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 254: convex_four; source clause 50881.
omit compatible in
private theorem sound253 : C.clause (decodeClause atoms clause253) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 255: packet; source clause 61907.
omit compatible in
private theorem sound254 : C.clause (decodeClause atoms clause254) := by
  exact C.covered_clause _ _ (C.packet_clause 0 6 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 256: packet; source clause 61920.
omit compatible in
private theorem sound255 : C.clause (decodeClause atoms clause255) := by
  exact C.covered_clause _ _ (C.packet_clause 0 6 10 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 257: packet; source clause 61928.
omit compatible in
private theorem sound256 : C.clause (decodeClause atoms clause256) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 258: convex_four; source clause 62106.
omit compatible in
private theorem sound257 : C.clause (decodeClause atoms clause257) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 259: convex_four; source clause 62110.
omit compatible in
private theorem sound258 : C.clause (decodeClause atoms clause258) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 260: packet; source clause 62138.
omit compatible in
private theorem sound259 : C.clause (decodeClause atoms clause259) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 11 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 261: packet; source clause 62225.
omit compatible in
private theorem sound260 : C.clause (decodeClause atoms clause260) := by
  exact C.covered_clause _ _ (C.packet_clause 7 0 11 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 262: packet; source clause 62242.
omit compatible in
private theorem sound261 : C.clause (decodeClause atoms clause261) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 0 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 263: convex_four; source clause 62310.
omit compatible in
private theorem sound262 : C.clause (decodeClause atoms clause262) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 264: convex_four; source clause 62318.
omit compatible in
private theorem sound263 : C.clause (decodeClause atoms clause263) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 265: packet; source clause 63992.
omit compatible in
private theorem sound264 : C.clause (decodeClause atoms clause264) := by
  exact C.covered_clause _ _ (C.packet_clause 0 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 266: packet; source clause 63995.
omit compatible in
private theorem sound265 : C.clause (decodeClause atoms clause265) := by
  exact C.covered_clause _ _ (C.packet_clause 0 6 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 267: convex_four; source clause 64189.
omit compatible in
private theorem sound266 : C.clause (decodeClause atoms clause266) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 268: convex_four; source clause 64193.
omit compatible in
private theorem sound267 : C.clause (decodeClause atoms clause267) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 269: packet; source clause 66072.
omit compatible in
private theorem sound268 : C.clause (decodeClause atoms clause268) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 270: packet; source clause 66074.
omit compatible in
private theorem sound269 : C.clause (decodeClause atoms clause269) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 271: packet; source clause 66075.
omit compatible in
private theorem sound270 : C.clause (decodeClause atoms clause270) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 272: packet; source clause 66077.
omit compatible in
private theorem sound271 : C.clause (decodeClause atoms clause271) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 273: packet; source clause 66083.
omit compatible in
private theorem sound272 : C.clause (decodeClause atoms clause272) := by
  exact C.covered_clause _ _ (C.packet_clause 0 10 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 274: packet; source clause 66129.
omit compatible in
private theorem sound273 : C.clause (decodeClause atoms clause273) := by
  exact C.covered_clause _ _ (C.packet_clause 7 0 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 275: convex_four; source clause 66261.
omit compatible in
private theorem sound274 : C.clause (decodeClause atoms clause274) := by
  exact C.covered_clause _ _ (C.convex_clause 0 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 276: convex_four; source clause 66269.
omit compatible in
private theorem sound275 : C.clause (decodeClause atoms clause275) := by
  exact C.covered_clause _ _ (C.convex_clause 0 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 277: packet; source clause 69190.
omit compatible in
private theorem sound276 : C.clause (decodeClause atoms clause276) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 278: packet; source clause 69192.
omit compatible in
private theorem sound277 : C.clause (decodeClause atoms clause277) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 279: packet; source clause 69193.
omit compatible in
private theorem sound278 : C.clause (decodeClause atoms clause278) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 280: convex_four; source clause 69393.
omit compatible in
private theorem sound279 : C.clause (decodeClause atoms clause279) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 281: packet; source clause 69401.
omit compatible in
private theorem sound280 : C.clause (decodeClause atoms clause280) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 282: packet; source clause 69410.
omit compatible in
private theorem sound281 : C.clause (decodeClause atoms clause281) := by
  exact C.covered_clause _ _ (C.packet_clause 1 3 2 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 283: packet; source clause 69413.
omit compatible in
private theorem sound282 : C.clause (decodeClause atoms clause282) := by
  exact C.covered_clause _ _ (C.packet_clause 1 3 2 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 284: packet; source clause 69494.
omit compatible in
private theorem sound283 : C.clause (decodeClause atoms clause283) := by
  exact C.covered_clause _ _ (C.packet_clause 3 1 2 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 285: packet; source clause 69497.
omit compatible in
private theorem sound284 : C.clause (decodeClause atoms clause284) := by
  exact C.covered_clause _ _ (C.packet_clause 3 1 2 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 286: packet; source clause 69544.
omit compatible in
private theorem sound285 : C.clause (decodeClause atoms clause285) := by
  exact C.covered_clause _ _ (C.packet_clause 7 1 2 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 287: packet; source clause 69555.
omit compatible in
private theorem sound286 : C.clause (decodeClause atoms clause286) := by
  exact C.covered_clause _ _ (C.packet_clause 7 2 1 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 288: packet; source clause 69557.
omit compatible in
private theorem sound287 : C.clause (decodeClause atoms clause287) := by
  exact C.covered_clause _ _ (C.packet_clause 7 2 1 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 289: packet; source clause 69566.
omit compatible in
private theorem sound288 : C.clause (decodeClause atoms clause288) := by
  exact C.covered_clause _ _ (C.packet_clause 7 2 3 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 290: packet; source clause 69568.
omit compatible in
private theorem sound289 : C.clause (decodeClause atoms clause289) := by
  exact C.covered_clause _ _ (C.packet_clause 7 2 3 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 291: convex_four; source clause 69601.
omit compatible in
private theorem sound290 : C.clause (decodeClause atoms clause290) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 292: packet; source clause 70025.
omit compatible in
private theorem sound291 : C.clause (decodeClause atoms clause291) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 293: convex_four; source clause 70221.
omit compatible in
private theorem sound292 : C.clause (decodeClause atoms clause292) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 294: convex_four; source clause 70224.
omit compatible in
private theorem sound293 : C.clause (decodeClause atoms clause293) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true false) (by decide +kernel)

-- Clause 295: convex_four; source clause 70225.
omit compatible in
private theorem sound294 : C.clause (decodeClause atoms clause294) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 296: packet; source clause 70241.
omit compatible in
private theorem sound295 : C.clause (decodeClause atoms clause295) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 11 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 297: convex_four; source clause 70431.
omit compatible in
private theorem sound296 : C.clause (decodeClause atoms clause296) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true) (by decide +kernel)

-- Clause 298: convex_four; source clause 70432.
omit compatible in
private theorem sound297 : C.clause (decodeClause atoms clause297) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true false) (by decide +kernel)

-- Clause 299: convex_four; source clause 70433.
omit compatible in
private theorem sound298 : C.clause (decodeClause atoms clause298) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 300: packet; source clause 73912.
omit compatible in
private theorem sound299 : C.clause (decodeClause atoms clause299) := by
  exact C.covered_clause _ _ (C.packet_clause 7 1 2 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 301: convex_four; source clause 73968.
omit compatible in
private theorem sound300 : C.clause (decodeClause atoms clause300) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true false) (by decide +kernel)

-- Clause 302: convex_four; source clause 73969.
omit compatible in
private theorem sound301 : C.clause (decodeClause atoms clause301) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 303: packet; source clause 74390.
omit compatible in
private theorem sound302 : C.clause (decodeClause atoms clause302) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 304: packet; source clause 74392.
omit compatible in
private theorem sound303 : C.clause (decodeClause atoms clause303) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 305: packet; source clause 74393.
omit compatible in
private theorem sound304 : C.clause (decodeClause atoms clause304) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 306: packet; source clause 74405.
omit compatible in
private theorem sound305 : C.clause (decodeClause atoms clause305) := by
  exact C.covered_clause _ _ (C.packet_clause 1 6 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 307: packet; source clause 74470.
omit compatible in
private theorem sound306 : C.clause (decodeClause atoms clause306) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 1 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 308: convex_four; source clause 74591.
omit compatible in
private theorem sound307 : C.clause (decodeClause atoms clause307) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true) (by decide +kernel)

-- Clause 309: convex_four; source clause 74593.
omit compatible in
private theorem sound308 : C.clause (decodeClause atoms clause308) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 310: packet; source clause 74744.
omit compatible in
private theorem sound309 : C.clause (decodeClause atoms clause309) := by
  exact C.covered_clause _ _ (C.packet_clause 11 1 2 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 311: convex_four; source clause 74793.
omit compatible in
private theorem sound310 : C.clause (decodeClause atoms clause310) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true true) (by decide +kernel)

-- Clause 312: convex_four; source clause 74797.
omit compatible in
private theorem sound311 : C.clause (decodeClause atoms clause311) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 313: convex_four; source clause 74801.
omit compatible in
private theorem sound312 : C.clause (decodeClause atoms clause312) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 314: packet; source clause 75528.
omit compatible in
private theorem sound313 : C.clause (decodeClause atoms clause313) := by
  exact C.covered_clause _ _ (C.packet_clause 7 1 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 315: convex_four; source clause 75626.
omit compatible in
private theorem sound314 : C.clause (decodeClause atoms clause314) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 316: convex_four; source clause 75630.
omit compatible in
private theorem sound315 : C.clause (decodeClause atoms clause315) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 317: packet; source clause 75658.
omit compatible in
private theorem sound316 : C.clause (decodeClause atoms clause316) := by
  exact C.covered_clause _ _ (C.packet_clause 1 7 11 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 318: packet; source clause 75678.
omit compatible in
private theorem sound317 : C.clause (decodeClause atoms clause317) := by
  exact C.covered_clause _ _ (C.packet_clause 1 11 7 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 319: packet; source clause 75681.
omit compatible in
private theorem sound318 : C.clause (decodeClause atoms clause318) := by
  exact C.covered_clause _ _ (C.packet_clause 1 11 7 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 320: packet; source clause 75702.
omit compatible in
private theorem sound319 : C.clause (decodeClause atoms clause319) := by
  exact C.covered_clause _ _ (C.packet_clause 2 7 1 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 321: packet; source clause 75704.
omit compatible in
private theorem sound320 : C.clause (decodeClause atoms clause320) := by
  exact C.covered_clause _ _ (C.packet_clause 2 7 1 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 322: packet; source clause 75707.
omit compatible in
private theorem sound321 : C.clause (decodeClause atoms clause321) := by
  exact C.covered_clause _ _ (C.packet_clause 2 7 11 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 323: packet; source clause 75709.
omit compatible in
private theorem sound322 : C.clause (decodeClause atoms clause322) := by
  exact C.covered_clause _ _ (C.packet_clause 2 7 11 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 324: packet; source clause 75745.
omit compatible in
private theorem sound323 : C.clause (decodeClause atoms clause323) := by
  exact C.covered_clause _ _ (C.packet_clause 7 1 11 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 325: packet; source clause 75762.
omit compatible in
private theorem sound324 : C.clause (decodeClause atoms clause324) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 1 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 326: packet; source clause 75786.
omit compatible in
private theorem sound325 : C.clause (decodeClause atoms clause325) := by
  exact C.covered_clause _ _ (C.packet_clause 11 1 7 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 327: packet; source clause 75789.
omit compatible in
private theorem sound326 : C.clause (decodeClause atoms clause326) := by
  exact C.covered_clause _ _ (C.packet_clause 11 1 7 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 328: convex_four; source clause 75838.
omit compatible in
private theorem sound327 : C.clause (decodeClause atoms clause327) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 329: packet; source clause 77512.
omit compatible in
private theorem sound328 : C.clause (decodeClause atoms clause328) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 330: packet; source clause 77515.
omit compatible in
private theorem sound329 : C.clause (decodeClause atoms clause329) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 331: convex_four; source clause 77713.
omit compatible in
private theorem sound330 : C.clause (decodeClause atoms clause330) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 332: packet; source clause 81257.
omit compatible in
private theorem sound331 : C.clause (decodeClause atoms clause331) := by
  exact C.covered_clause _ _ (C.packet_clause 1 3 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 333: packet; source clause 81288.
omit compatible in
private theorem sound332 : C.clause (decodeClause atoms clause332) := by
  exact C.covered_clause _ _ (C.packet_clause 1 7 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 334: packet; source clause 81413.
omit compatible in
private theorem sound333 : C.clause (decodeClause atoms clause333) := by
  exact C.covered_clause _ _ (C.packet_clause 7 3 1 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 335: packet; source clause 81422.
omit compatible in
private theorem sound334 : C.clause (decodeClause atoms clause334) := by
  exact C.covered_clause _ _ (C.packet_clause 7 3 6 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 336: convex_four; source clause 81455.
omit compatible in
private theorem sound335 : C.clause (decodeClause atoms clause335) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true) (by decide +kernel)

-- Clause 337: convex_four; source clause 81457.
omit compatible in
private theorem sound336 : C.clause (decodeClause atoms clause336) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 338: convex_four; source clause 82081.
omit compatible in
private theorem sound337 : C.clause (decodeClause atoms clause337) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 339: packet; source clause 82114.
omit compatible in
private theorem sound338 : C.clause (decodeClause atoms clause338) := by
  exact C.covered_clause _ _ (C.packet_clause 1 11 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 340: convex_four; source clause 82281.
omit compatible in
private theorem sound339 : C.clause (decodeClause atoms clause339) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true true) (by decide +kernel)

-- Clause 341: convex_four; source clause 82289.
omit compatible in
private theorem sound340 : C.clause (decodeClause atoms clause340) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 342: convex_four; source clause 83118.
omit compatible in
private theorem sound341 : C.clause (decodeClause atoms clause341) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 343: packet; source clause 83142.
omit compatible in
private theorem sound342 : C.clause (decodeClause atoms clause342) := by
  exact C.covered_clause _ _ (C.packet_clause 1 7 3 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 344: packet; source clause 83144.
omit compatible in
private theorem sound343 : C.clause (decodeClause atoms clause343) := by
  exact C.covered_clause _ _ (C.packet_clause 1 7 3 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 345: packet; source clause 83146.
omit compatible in
private theorem sound344 : C.clause (decodeClause atoms clause344) := by
  exact C.covered_clause _ _ (C.packet_clause 1 7 11 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 346: packet; source clause 83147.
omit compatible in
private theorem sound345 : C.clause (decodeClause atoms clause345) := by
  exact C.covered_clause _ _ (C.packet_clause 1 7 11 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 347: packet; source clause 83233.
omit compatible in
private theorem sound346 : C.clause (decodeClause atoms clause346) := by
  exact C.covered_clause _ _ (C.packet_clause 7 1 11 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 348: packet; source clause 83250.
omit compatible in
private theorem sound347 : C.clause (decodeClause atoms clause347) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 1 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 349: convex_four; source clause 83314.
omit compatible in
private theorem sound348 : C.clause (decodeClause atoms clause348) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 350: convex_four; source clause 83318.
omit compatible in
private theorem sound349 : C.clause (decodeClause atoms clause349) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 351: convex_four; source clause 83322.
omit compatible in
private theorem sound350 : C.clause (decodeClause atoms clause350) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 352: convex_four; source clause 83326.
omit compatible in
private theorem sound351 : C.clause (decodeClause atoms clause351) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 353: packet; source clause 85000.
omit compatible in
private theorem sound352 : C.clause (decodeClause atoms clause352) := by
  exact C.covered_clause _ _ (C.packet_clause 1 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 354: packet; source clause 85003.
omit compatible in
private theorem sound353 : C.clause (decodeClause atoms clause353) := by
  exact C.covered_clause _ _ (C.packet_clause 1 3 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 355: packet; source clause 85026.
omit compatible in
private theorem sound354 : C.clause (decodeClause atoms clause354) := by
  exact C.covered_clause _ _ (C.packet_clause 1 11 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 356: convex_four; source clause 85193.
omit compatible in
private theorem sound355 : C.clause (decodeClause atoms clause355) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true true) (by decide +kernel)

-- Clause 357: convex_four; source clause 85201.
omit compatible in
private theorem sound356 : C.clause (decodeClause atoms clause356) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 358: packet; source clause 96248.
omit compatible in
private theorem sound357 : C.clause (decodeClause atoms clause357) := by
  exact C.covered_clause _ _ (C.packet_clause 1 7 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 359: convex_four; source clause 96430.
omit compatible in
private theorem sound358 : C.clause (decodeClause atoms clause358) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 360: convex_four; source clause 96432.
omit compatible in
private theorem sound359 : C.clause (decodeClause atoms clause359) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true false) (by decide +kernel)

-- Clause 361: packet; source clause 96435.
omit compatible in
private theorem sound360 : C.clause (decodeClause atoms clause360) := by
  exact C.covered_clause _ _ (C.packet_clause 1 6 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 362: packet; source clause 96458.
omit compatible in
private theorem sound361 : C.clause (decodeClause atoms clause361) := by
  exact C.covered_clause _ _ (C.packet_clause 1 7 11 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 363: packet; source clause 96545.
omit compatible in
private theorem sound362 : C.clause (decodeClause atoms clause362) := by
  exact C.covered_clause _ _ (C.packet_clause 7 1 11 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 364: convex_four; source clause 96634.
omit compatible in
private theorem sound363 : C.clause (decodeClause atoms clause363) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 365: convex_four; source clause 96638.
omit compatible in
private theorem sound364 : C.clause (decodeClause atoms clause364) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 366: packet; source clause 98312.
omit compatible in
private theorem sound365 : C.clause (decodeClause atoms clause365) := by
  exact C.covered_clause _ _ (C.packet_clause 1 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 367: packet; source clause 98315.
omit compatible in
private theorem sound366 : C.clause (decodeClause atoms clause366) := by
  exact C.covered_clause _ _ (C.packet_clause 1 6 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 368: packet; source clause 98456.
omit compatible in
private theorem sound367 : C.clause (decodeClause atoms clause367) := by
  exact C.covered_clause _ _ (C.packet_clause 11 1 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 369: convex_four; source clause 98511.
omit compatible in
private theorem sound368 : C.clause (decodeClause atoms clause368) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true) (by decide +kernel)

-- Clause 370: convex_four; source clause 98513.
omit compatible in
private theorem sound369 : C.clause (decodeClause atoms clause369) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 371: packet; source clause 100392.
omit compatible in
private theorem sound370 : C.clause (decodeClause atoms clause370) := by
  exact C.covered_clause _ _ (C.packet_clause 1 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 372: packet; source clause 100394.
omit compatible in
private theorem sound371 : C.clause (decodeClause atoms clause371) := by
  exact C.covered_clause _ _ (C.packet_clause 1 7 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 373: packet; source clause 100403.
omit compatible in
private theorem sound372 : C.clause (decodeClause atoms clause372) := by
  exact C.covered_clause _ _ (C.packet_clause 1 10 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 374: packet; source clause 100466.
omit compatible in
private theorem sound373 : C.clause (decodeClause atoms clause373) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 1 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 375: convex_four; source clause 100581.
omit compatible in
private theorem sound374 : C.clause (decodeClause atoms clause374) := by
  exact C.covered_clause _ _ (C.convex_clause 1 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 376: convex_four; source clause 100589.
omit compatible in
private theorem sound375 : C.clause (decodeClause atoms clause375) := by
  exact C.covered_clause _ _ (C.convex_clause 1 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 377: packet; source clause 100823.
omit compatible in
private theorem sound376 : C.clause (decodeClause atoms clause376) := by
  exact C.covered_clause _ _ (C.packet_clause 1 11 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 378: packet; source clause 100919.
omit compatible in
private theorem sound377 : C.clause (decodeClause atoms clause377) := by
  exact C.covered_clause _ _ (C.packet_clause 11 7 1 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 379: packet; source clause 100920.
omit compatible in
private theorem sound378 : C.clause (decodeClause atoms clause378) := by
  exact C.covered_clause _ _ (C.packet_clause 11 7 1 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 380: packet; source clause 100923.
omit compatible in
private theorem sound379 : C.clause (decodeClause atoms clause379) := by
  exact C.covered_clause _ _ (C.packet_clause 11 7 12 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 381: packet; source clause 100924.
omit compatible in
private theorem sound380 : C.clause (decodeClause atoms clause380) := by
  exact C.covered_clause _ _ (C.packet_clause 11 7 12 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 382: packet; source clause 100943.
omit compatible in
private theorem sound381 : C.clause (decodeClause atoms clause381) := by
  exact C.covered_clause _ _ (C.packet_clause 11 12 7 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 383: packet; source clause 100944.
omit compatible in
private theorem sound382 : C.clause (decodeClause atoms clause382) := by
  exact C.covered_clause _ _ (C.packet_clause 11 12 7 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 384: packet; source clause 102902.
omit compatible in
private theorem sound383 : C.clause (decodeClause atoms clause383) := by
  exact C.covered_clause _ _ (C.packet_clause 1 11 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 385: packet; source clause 102904.
omit compatible in
private theorem sound384 : C.clause (decodeClause atoms clause384) := by
  exact C.covered_clause _ _ (C.packet_clause 1 11 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 386: packet; source clause 106226.
omit compatible in
private theorem sound385 : C.clause (decodeClause atoms clause385) := by
  exact C.covered_clause _ _ (C.packet_clause 2 6 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 387: packet; source clause 106229.
omit compatible in
private theorem sound386 : C.clause (decodeClause atoms clause386) := by
  exact C.covered_clause _ _ (C.packet_clause 2 6 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 388: packet; source clause 106310.
omit compatible in
private theorem sound387 : C.clause (decodeClause atoms clause387) := by
  exact C.covered_clause _ _ (C.packet_clause 6 2 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 389: packet; source clause 106313.
omit compatible in
private theorem sound388 : C.clause (decodeClause atoms clause388) := by
  exact C.covered_clause _ _ (C.packet_clause 6 2 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 390: packet; source clause 106360.
omit compatible in
private theorem sound389 : C.clause (decodeClause atoms clause389) := by
  exact C.covered_clause _ _ (C.packet_clause 7 2 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 391: packet; source clause 106371.
omit compatible in
private theorem sound390 : C.clause (decodeClause atoms clause390) := by
  exact C.covered_clause _ _ (C.packet_clause 7 3 2 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 392: packet; source clause 106373.
omit compatible in
private theorem sound391 : C.clause (decodeClause atoms clause391) := by
  exact C.covered_clause _ _ (C.packet_clause 7 3 2 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 393: packet; source clause 106382.
omit compatible in
private theorem sound392 : C.clause (decodeClause atoms clause392) := by
  exact C.covered_clause _ _ (C.packet_clause 7 3 6 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 394: packet; source clause 106384.
omit compatible in
private theorem sound393 : C.clause (decodeClause atoms clause393) := by
  exact C.covered_clause _ _ (C.packet_clause 7 3 6 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 395: convex_four; source clause 106415.
omit compatible in
private theorem sound394 : C.clause (decodeClause atoms clause394) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true) (by decide +kernel)

-- Clause 396: convex_four; source clause 106417.
omit compatible in
private theorem sound395 : C.clause (decodeClause atoms clause395) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 6 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 397: packet; source clause 106838.
omit compatible in
private theorem sound396 : C.clause (decodeClause atoms clause396) := by
  exact C.covered_clause _ _ (C.packet_clause 2 3 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 398: packet; source clause 106840.
omit compatible in
private theorem sound397 : C.clause (decodeClause atoms clause397) := by
  exact C.covered_clause _ _ (C.packet_clause 2 3 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 399: packet; source clause 106841.
omit compatible in
private theorem sound398 : C.clause (decodeClause atoms clause398) := by
  exact C.covered_clause _ _ (C.packet_clause 2 3 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 400: packet; source clause 106882.
omit compatible in
private theorem sound399 : C.clause (decodeClause atoms clause399) := by
  exact C.covered_clause _ _ (C.packet_clause 3 2 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 401: packet; source clause 106885.
omit compatible in
private theorem sound400 : C.clause (decodeClause atoms clause400) := by
  exact C.covered_clause _ _ (C.packet_clause 3 2 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 402: convex_four; source clause 107039.
omit compatible in
private theorem sound401 : C.clause (decodeClause atoms clause401) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true) (by decide +kernel)

-- Clause 403: convex_four; source clause 107041.
omit compatible in
private theorem sound402 : C.clause (decodeClause atoms clause402) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 404: packet; source clause 107193.
omit compatible in
private theorem sound403 : C.clause (decodeClause atoms clause403) := by
  exact C.covered_clause _ _ (C.packet_clause 11 2 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 405: convex_four; source clause 107245.
omit compatible in
private theorem sound404 : C.clause (decodeClause atoms clause404) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 406: convex_four; source clause 107249.
omit compatible in
private theorem sound405 : C.clause (decodeClause atoms clause405) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 407: packet; source clause 107956.
omit compatible in
private theorem sound406 : C.clause (decodeClause atoms clause406) := by
  exact C.covered_clause _ _ (C.packet_clause 3 10 2 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 408: packet; source clause 107961.
omit compatible in
private theorem sound407 : C.clause (decodeClause atoms clause407) := by
  exact C.covered_clause _ _ (C.packet_clause 3 10 2 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 409: packet; source clause 107976.
omit compatible in
private theorem sound408 : C.clause (decodeClause atoms clause408) := by
  exact C.covered_clause _ _ (C.packet_clause 7 2 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 410: packet; source clause 108034.
omit compatible in
private theorem sound409 : C.clause (decodeClause atoms clause409) := by
  exact C.covered_clause _ _ (C.packet_clause 10 3 2 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 411: packet; source clause 108039.
omit compatible in
private theorem sound410 : C.clause (decodeClause atoms clause410) := by
  exact C.covered_clause _ _ (C.packet_clause 10 3 2 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 412: convex_four; source clause 108078.
omit compatible in
private theorem sound411 : C.clause (decodeClause atoms clause411) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 413: convex_four; source clause 108079.
omit compatible in
private theorem sound412 : C.clause (decodeClause atoms clause412) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true) (by decide +kernel)

-- Clause 414: packet; source clause 108126.
omit compatible in
private theorem sound413 : C.clause (decodeClause atoms clause413) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 7 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 415: packet; source clause 108129.
omit compatible in
private theorem sound414 : C.clause (decodeClause atoms clause414) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 7 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 416: packet; source clause 108150.
omit compatible in
private theorem sound415 : C.clause (decodeClause atoms clause415) := by
  exact C.covered_clause _ _ (C.packet_clause 3 7 2 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 417: packet; source clause 108152.
omit compatible in
private theorem sound416 : C.clause (decodeClause atoms clause416) := by
  exact C.covered_clause _ _ (C.packet_clause 3 7 2 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 418: packet; source clause 108155.
omit compatible in
private theorem sound417 : C.clause (decodeClause atoms clause417) := by
  exact C.covered_clause _ _ (C.packet_clause 3 7 11 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 419: packet; source clause 108157.
omit compatible in
private theorem sound418 : C.clause (decodeClause atoms clause418) := by
  exact C.covered_clause _ _ (C.packet_clause 3 7 11 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 420: packet; source clause 108210.
omit compatible in
private theorem sound419 : C.clause (decodeClause atoms clause419) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 2 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 421: packet; source clause 108234.
omit compatible in
private theorem sound420 : C.clause (decodeClause atoms clause420) := by
  exact C.covered_clause _ _ (C.packet_clause 11 2 7 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 422: packet; source clause 108237.
omit compatible in
private theorem sound421 : C.clause (decodeClause atoms clause421) := by
  exact C.covered_clause _ _ (C.packet_clause 11 2 7 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 423: convex_four; source clause 108286.
omit compatible in
private theorem sound422 : C.clause (decodeClause atoms clause422) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 424: packet; source clause 109960.
omit compatible in
private theorem sound423 : C.clause (decodeClause atoms clause423) := by
  exact C.covered_clause _ _ (C.packet_clause 2 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 425: packet; source clause 109963.
omit compatible in
private theorem sound424 : C.clause (decodeClause atoms clause424) := by
  exact C.covered_clause _ _ (C.packet_clause 2 3 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 426: packet; source clause 110045.
omit compatible in
private theorem sound425 : C.clause (decodeClause atoms clause425) := by
  exact C.covered_clause _ _ (C.packet_clause 3 11 10 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 427: convex_four; source clause 110153.
omit compatible in
private theorem sound426 : C.clause (decodeClause atoms clause426) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true true) (by decide +kernel)

-- Clause 428: convex_four; source clause 110161.
omit compatible in
private theorem sound427 : C.clause (decodeClause atoms clause427) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 429: packet; source clause 110998.
omit compatible in
private theorem sound428 : C.clause (decodeClause atoms clause428) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 430: packet; source clause 111000.
omit compatible in
private theorem sound429 : C.clause (decodeClause atoms clause429) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 431: packet; source clause 111001.
omit compatible in
private theorem sound430 : C.clause (decodeClause atoms clause430) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 432: packet; source clause 111042.
omit compatible in
private theorem sound431 : C.clause (decodeClause atoms clause431) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 433: convex_four; source clause 111199.
omit compatible in
private theorem sound432 : C.clause (decodeClause atoms clause432) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true) (by decide +kernel)

-- Clause 434: convex_four; source clause 111201.
omit compatible in
private theorem sound433 : C.clause (decodeClause atoms clause433) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 435: packet; source clause 111207.
omit compatible in
private theorem sound434 : C.clause (decodeClause atoms clause434) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 436: packet; source clause 111208.
omit compatible in
private theorem sound435 : C.clause (decodeClause atoms clause435) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 437: packet; source clause 111209.
omit compatible in
private theorem sound436 : C.clause (decodeClause atoms clause436) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 438: packet; source clause 111211.
omit compatible in
private theorem sound437 : C.clause (decodeClause atoms clause437) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 9 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 439: packet; source clause 111213.
omit compatible in
private theorem sound438 : C.clause (decodeClause atoms clause438) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 9 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 440: packet; source clause 111250.
omit compatible in
private theorem sound439 : C.clause (decodeClause atoms clause439) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 441: packet; source clause 111273.
omit compatible in
private theorem sound440 : C.clause (decodeClause atoms clause440) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 2 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 442: convex_four; source clause 111409.
omit compatible in
private theorem sound441 : C.clause (decodeClause atoms clause441) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 443: packet; source clause 111417.
omit compatible in
private theorem sound442 : C.clause (decodeClause atoms clause442) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 444: packet; source clause 111426.
omit compatible in
private theorem sound443 : C.clause (decodeClause atoms clause443) := by
  exact C.covered_clause _ _ (C.packet_clause 2 5 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 445: packet; source clause 111429.
omit compatible in
private theorem sound444 : C.clause (decodeClause atoms clause444) := by
  exact C.covered_clause _ _ (C.packet_clause 2 5 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 446: packet; source clause 111458.
omit compatible in
private theorem sound445 : C.clause (decodeClause atoms clause445) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 447: packet; source clause 111481.
omit compatible in
private theorem sound446 : C.clause (decodeClause atoms clause446) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 448: packet; source clause 111510.
omit compatible in
private theorem sound447 : C.clause (decodeClause atoms clause447) := by
  exact C.covered_clause _ _ (C.packet_clause 5 2 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 449: packet; source clause 111513.
omit compatible in
private theorem sound448 : C.clause (decodeClause atoms clause448) := by
  exact C.covered_clause _ _ (C.packet_clause 5 2 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 450: packet; source clause 111571.
omit compatible in
private theorem sound449 : C.clause (decodeClause atoms clause449) := by
  exact C.covered_clause _ _ (C.packet_clause 10 4 2 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 451: packet; source clause 111573.
omit compatible in
private theorem sound450 : C.clause (decodeClause atoms clause450) := by
  exact C.covered_clause _ _ (C.packet_clause 10 4 2 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 452: packet; source clause 111582.
omit compatible in
private theorem sound451 : C.clause (decodeClause atoms clause451) := by
  exact C.covered_clause _ _ (C.packet_clause 10 4 5 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 453: packet; source clause 111584.
omit compatible in
private theorem sound452 : C.clause (decodeClause atoms clause452) := by
  exact C.covered_clause _ _ (C.packet_clause 10 4 5 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 454: convex_four; source clause 111617.
omit compatible in
private theorem sound453 : C.clause (decodeClause atoms clause453) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 455: packet; source clause 111624.
omit compatible in
private theorem sound454 : C.clause (decodeClause atoms clause454) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 5 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 456: packet; source clause 111627.
omit compatible in
private theorem sound455 : C.clause (decodeClause atoms clause455) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 11 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 457: packet; source clause 111656.
omit compatible in
private theorem sound456 : C.clause (decodeClause atoms clause456) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 4 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 458: packet; source clause 111666.
omit compatible in
private theorem sound457 : C.clause (decodeClause atoms clause457) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 5 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 459: packet; source clause 111689.
omit compatible in
private theorem sound458 : C.clause (decodeClause atoms clause458) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 2 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 460: convex_four; source clause 111825.
omit compatible in
private theorem sound459 : C.clause (decodeClause atoms clause459) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 5 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 461: packet; source clause 111835.
omit compatible in
private theorem sound460 : C.clause (decodeClause atoms clause460) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 12 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 462: packet; source clause 111837.
omit compatible in
private theorem sound461 : C.clause (decodeClause atoms clause461) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 12 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 463: packet; source clause 111874.
omit compatible in
private theorem sound462 : C.clause (decodeClause atoms clause462) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 464: packet; source clause 111897.
omit compatible in
private theorem sound463 : C.clause (decodeClause atoms clause463) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 2 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 465: convex_four; source clause 112029.
omit compatible in
private theorem sound464 : C.clause (decodeClause atoms clause464) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 466: convex_four; source clause 112033.
omit compatible in
private theorem sound465 : C.clause (decodeClause atoms clause465) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 467: packet; source clause 114329.
omit compatible in
private theorem sound466 : C.clause (decodeClause atoms clause466) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 468: packet; source clause 114331.
omit compatible in
private theorem sound467 : C.clause (decodeClause atoms clause467) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 9 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 469: packet; source clause 114332.
omit compatible in
private theorem sound468 : C.clause (decodeClause atoms clause468) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 9 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 470: packet; source clause 114370.
omit compatible in
private theorem sound469 : C.clause (decodeClause atoms clause469) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 471: packet; source clause 114375.
omit compatible in
private theorem sound470 : C.clause (decodeClause atoms clause470) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 472: convex_four; source clause 114529.
omit compatible in
private theorem sound471 : C.clause (decodeClause atoms clause471) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 473: packet; source clause 114532.
omit compatible in
private theorem sound472 : C.clause (decodeClause atoms clause472) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 474: packet; source clause 114537.
omit compatible in
private theorem sound473 : C.clause (decodeClause atoms clause473) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 475: packet; source clause 114545.
omit compatible in
private theorem sound474 : C.clause (decodeClause atoms clause474) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 10 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 476: packet; source clause 114546.
omit compatible in
private theorem sound475 : C.clause (decodeClause atoms clause475) := by
  exact C.covered_clause _ _ (C.packet_clause 2 8 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 477: packet; source clause 114551.
omit compatible in
private theorem sound476 : C.clause (decodeClause atoms clause476) := by
  exact C.covered_clause _ _ (C.packet_clause 2 8 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 478: packet; source clause 114578.
omit compatible in
private theorem sound477 : C.clause (decodeClause atoms clause477) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 479: packet; source clause 114583.
omit compatible in
private theorem sound478 : C.clause (decodeClause atoms clause478) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 480: packet; source clause 114584.
omit compatible in
private theorem sound479 : C.clause (decodeClause atoms clause479) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 481: packet; source clause 114587.
omit compatible in
private theorem sound480 : C.clause (decodeClause atoms clause480) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 10 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 482: packet; source clause 114595.
omit compatible in
private theorem sound481 : C.clause (decodeClause atoms clause481) := by
  exact C.covered_clause _ _ (C.packet_clause 4 8 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 483: packet; source clause 114596.
omit compatible in
private theorem sound482 : C.clause (decodeClause atoms clause482) := by
  exact C.covered_clause _ _ (C.packet_clause 4 8 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 484: packet; source clause 114601.
omit compatible in
private theorem sound483 : C.clause (decodeClause atoms clause483) := by
  exact C.covered_clause _ _ (C.packet_clause 4 8 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 485: packet; source clause 114628.
omit compatible in
private theorem sound484 : C.clause (decodeClause atoms clause484) := by
  exact C.covered_clause _ _ (C.packet_clause 8 2 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 486: packet; source clause 114633.
omit compatible in
private theorem sound485 : C.clause (decodeClause atoms clause485) := by
  exact C.covered_clause _ _ (C.packet_clause 8 2 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 487: packet; source clause 114642.
omit compatible in
private theorem sound486 : C.clause (decodeClause atoms clause486) := by
  exact C.covered_clause _ _ (C.packet_clause 8 4 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 488: packet; source clause 114647.
omit compatible in
private theorem sound487 : C.clause (decodeClause atoms clause487) := by
  exact C.covered_clause _ _ (C.packet_clause 8 4 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 489: convex_four; source clause 114737.
omit compatible in
private theorem sound488 : C.clause (decodeClause atoms clause488) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 490: packet; source clause 114753.
omit compatible in
private theorem sound489 : C.clause (decodeClause atoms clause489) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 11 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 491: packet; source clause 114809.
omit compatible in
private theorem sound490 : C.clause (decodeClause atoms clause490) := by
  exact C.covered_clause _ _ (C.packet_clause 4 8 2 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 492: convex_four; source clause 114945.
omit compatible in
private theorem sound491 : C.clause (decodeClause atoms clause491) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 493: packet; source clause 114950.
omit compatible in
private theorem sound492 : C.clause (decodeClause atoms clause492) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 494: packet; source clause 114952.
omit compatible in
private theorem sound493 : C.clause (decodeClause atoms clause493) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 495: packet; source clause 114953.
omit compatible in
private theorem sound494 : C.clause (decodeClause atoms clause494) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 496: packet; source clause 114955.
omit compatible in
private theorem sound495 : C.clause (decodeClause atoms clause495) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 12 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 497: packet; source clause 114961.
omit compatible in
private theorem sound496 : C.clause (decodeClause atoms clause496) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 12 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 498: packet; source clause 114994.
omit compatible in
private theorem sound497 : C.clause (decodeClause atoms clause497) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 499: convex_four; source clause 115153.
omit compatible in
private theorem sound498 : C.clause (decodeClause atoms clause498) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 500: packet; source clause 115169.
omit compatible in
private theorem sound499 : C.clause (decodeClause atoms clause499) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 10 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 501: packet; source clause 115186.
omit compatible in
private theorem sound500 : C.clause (decodeClause atoms clause500) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 4 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 502: packet; source clause 115210.
omit compatible in
private theorem sound501 : C.clause (decodeClause atoms clause501) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 10 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 503: packet; source clause 115211.
omit compatible in
private theorem sound502 : C.clause (decodeClause atoms clause502) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 10 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 504: packet; source clause 115308.
omit compatible in
private theorem sound503 : C.clause (decodeClause atoms clause503) := by
  exact C.covered_clause _ _ (C.packet_clause 10 2 9 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 505: packet; source clause 115313.
omit compatible in
private theorem sound504 : C.clause (decodeClause atoms clause504) := by
  exact C.covered_clause _ _ (C.packet_clause 10 2 9 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 506: convex_four; source clause 115361.
omit compatible in
private theorem sound505 : C.clause (decodeClause atoms clause505) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 507: packet; source clause 115394.
omit compatible in
private theorem sound506 : C.clause (decodeClause atoms clause506) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 4 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 508: packet; source clause 115410.
omit compatible in
private theorem sound507 : C.clause (decodeClause atoms clause507) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 509: packet; source clause 115433.
omit compatible in
private theorem sound508 : C.clause (decodeClause atoms clause508) := by
  exact C.covered_clause _ _ (C.packet_clause 4 9 2 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 510: convex_four; source clause 115565.
omit compatible in
private theorem sound509 : C.clause (decodeClause atoms clause509) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 511: convex_four; source clause 115569.
omit compatible in
private theorem sound510 : C.clause (decodeClause atoms clause510) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 512: packet; source clause 115579.
omit compatible in
private theorem sound511 : C.clause (decodeClause atoms clause511) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 513: packet; source clause 115602.
omit compatible in
private theorem sound512 : C.clause (decodeClause atoms clause512) := by
  exact C.covered_clause _ _ (C.packet_clause 2 12 4 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 514: packet; source clause 115608.
omit compatible in
private theorem sound513 : C.clause (decodeClause atoms clause513) := by
  exact C.covered_clause _ _ (C.packet_clause 2 12 4 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 515: packet; source clause 115610.
omit compatible in
private theorem sound514 : C.clause (decodeClause atoms clause514) := by
  exact C.covered_clause _ _ (C.packet_clause 2 12 9 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 516: packet; source clause 115615.
omit compatible in
private theorem sound515 : C.clause (decodeClause atoms clause515) := by
  exact C.covered_clause _ _ (C.packet_clause 2 12 9 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 517: packet; source clause 115618.
omit compatible in
private theorem sound516 : C.clause (decodeClause atoms clause516) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 518: packet; source clause 115623.
omit compatible in
private theorem sound517 : C.clause (decodeClause atoms clause517) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 519: packet; source clause 115624.
omit compatible in
private theorem sound518 : C.clause (decodeClause atoms clause518) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 520: packet; source clause 115627.
omit compatible in
private theorem sound519 : C.clause (decodeClause atoms clause519) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 521: packet; source clause 115628.
omit compatible in
private theorem sound520 : C.clause (decodeClause atoms clause520) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 522: packet; source clause 115635.
omit compatible in
private theorem sound521 : C.clause (decodeClause atoms clause521) := by
  exact C.covered_clause _ _ (C.packet_clause 4 9 2 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 523: packet; source clause 115636.
omit compatible in
private theorem sound522 : C.clause (decodeClause atoms clause522) := by
  exact C.covered_clause _ _ (C.packet_clause 4 9 2 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 524: packet; source clause 115641.
omit compatible in
private theorem sound523 : C.clause (decodeClause atoms clause523) := by
  exact C.covered_clause _ _ (C.packet_clause 4 9 2 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 525: packet; source clause 115655.
omit compatible in
private theorem sound524 : C.clause (decodeClause atoms clause524) := by
  exact C.covered_clause _ _ (C.packet_clause 4 12 2 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 526: packet; source clause 115656.
omit compatible in
private theorem sound525 : C.clause (decodeClause atoms clause525) := by
  exact C.covered_clause _ _ (C.packet_clause 4 12 2 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 527: convex_four; source clause 115777.
omit compatible in
private theorem sound526 : C.clause (decodeClause atoms clause526) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 528: packet; source clause 115782.
omit compatible in
private theorem sound527 : C.clause (decodeClause atoms clause527) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 529: packet; source clause 115785.
omit compatible in
private theorem sound528 : C.clause (decodeClause atoms clause528) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 530: packet; source clause 115826.
omit compatible in
private theorem sound529 : C.clause (decodeClause atoms clause529) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 531: packet; source clause 115827.
omit compatible in
private theorem sound530 : C.clause (decodeClause atoms clause530) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 532: packet; source clause 115829.
omit compatible in
private theorem sound531 : C.clause (decodeClause atoms clause531) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 533: convex_four; source clause 115982.
omit compatible in
private theorem sound532 : C.clause (decodeClause atoms clause532) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 534: packet; source clause 115991.
omit compatible in
private theorem sound533 : C.clause (decodeClause atoms clause533) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 535: packet; source clause 116004.
omit compatible in
private theorem sound534 : C.clause (decodeClause atoms clause534) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 536: packet; source clause 116010.
omit compatible in
private theorem sound535 : C.clause (decodeClause atoms clause535) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 12 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 537: packet; source clause 116015.
omit compatible in
private theorem sound536 : C.clause (decodeClause atoms clause536) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 12 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 538: packet; source clause 116035.
omit compatible in
private theorem sound537 : C.clause (decodeClause atoms clause537) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 539: packet; source clause 116036.
omit compatible in
private theorem sound538 : C.clause (decodeClause atoms clause538) := by
  exact C.covered_clause _ _ (C.packet_clause 4 2 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 540: packet; source clause 116054.
omit compatible in
private theorem sound539 : C.clause (decodeClause atoms clause539) := by
  exact C.covered_clause _ _ (C.packet_clause 4 10 2 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 541: packet; source clause 116055.
omit compatible in
private theorem sound540 : C.clause (decodeClause atoms clause540) := by
  exact C.covered_clause _ _ (C.packet_clause 4 10 2 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 542: packet; source clause 116056.
omit compatible in
private theorem sound541 : C.clause (decodeClause atoms clause541) := by
  exact C.covered_clause _ _ (C.packet_clause 4 10 2 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 543: packet; source clause 116059.
omit compatible in
private theorem sound542 : C.clause (decodeClause atoms clause542) := by
  exact C.covered_clause _ _ (C.packet_clause 4 10 12 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 544: packet; source clause 116060.
omit compatible in
private theorem sound543 : C.clause (decodeClause atoms clause543) := by
  exact C.covered_clause _ _ (C.packet_clause 4 10 12 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 545: packet; source clause 116087.
omit compatible in
private theorem sound544 : C.clause (decodeClause atoms clause544) := by
  exact C.covered_clause _ _ (C.packet_clause 10 2 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 546: packet; source clause 116091.
omit compatible in
private theorem sound545 : C.clause (decodeClause atoms clause545) := by
  exact C.covered_clause _ _ (C.packet_clause 10 2 12 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 547: packet; source clause 116092.
omit compatible in
private theorem sound546 : C.clause (decodeClause atoms clause546) := by
  exact C.covered_clause _ _ (C.packet_clause 10 2 12 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 548: packet; source clause 116097.
omit compatible in
private theorem sound547 : C.clause (decodeClause atoms clause547) := by
  exact C.covered_clause _ _ (C.packet_clause 10 2 12 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 549: packet; source clause 116114.
omit compatible in
private theorem sound548 : C.clause (decodeClause atoms clause548) := by
  exact C.covered_clause _ _ (C.packet_clause 10 12 2 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 550: packet; source clause 116119.
omit compatible in
private theorem sound549 : C.clause (decodeClause atoms clause549) := by
  exact C.covered_clause _ _ (C.packet_clause 10 12 2 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 551: convex_four; source clause 116190.
omit compatible in
private theorem sound550 : C.clause (decodeClause atoms clause550) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 552: packet; source clause 116195.
omit compatible in
private theorem sound551 : C.clause (decodeClause atoms clause551) := by
  exact C.covered_clause _ _ (C.packet_clause 2 4 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 553: packet; source clause 116216.
omit compatible in
private theorem sound552 : C.clause (decodeClause atoms clause552) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 554: convex_four; source clause 116394.
omit compatible in
private theorem sound553 : C.clause (decodeClause atoms clause553) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 555: convex_four; source clause 116398.
omit compatible in
private theorem sound554 : C.clause (decodeClause atoms clause554) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 556: packet; source clause 118694.
omit compatible in
private theorem sound555 : C.clause (decodeClause atoms clause555) := by
  exact C.covered_clause _ _ (C.packet_clause 2 5 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 557: packet; source clause 118696.
omit compatible in
private theorem sound556 : C.clause (decodeClause atoms clause556) := by
  exact C.covered_clause _ _ (C.packet_clause 2 5 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 558: packet; source clause 118697.
omit compatible in
private theorem sound557 : C.clause (decodeClause atoms clause557) := by
  exact C.covered_clause _ _ (C.packet_clause 2 5 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 559: packet; source clause 118701.
omit compatible in
private theorem sound558 : C.clause (decodeClause atoms clause558) := by
  exact C.covered_clause _ _ (C.packet_clause 2 5 9 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 560: packet; source clause 118744.
omit compatible in
private theorem sound559 : C.clause (decodeClause atoms clause559) := by
  exact C.covered_clause _ _ (C.packet_clause 5 2 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 561: convex_four; source clause 118897.
omit compatible in
private theorem sound560 : C.clause (decodeClause atoms clause560) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 562: packet; source clause 118904.
omit compatible in
private theorem sound561 : C.clause (decodeClause atoms clause561) := by
  exact C.covered_clause _ _ (C.packet_clause 2 5 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 563: packet; source clause 118936.
omit compatible in
private theorem sound562 : C.clause (decodeClause atoms clause562) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 564: packet; source clause 118952.
omit compatible in
private theorem sound563 : C.clause (decodeClause atoms clause563) := by
  exact C.covered_clause _ _ (C.packet_clause 5 2 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 565: packet; source clause 118963.
omit compatible in
private theorem sound564 : C.clause (decodeClause atoms clause564) := by
  exact C.covered_clause _ _ (C.packet_clause 5 8 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 566: convex_four; source clause 119105.
omit compatible in
private theorem sound565 : C.clause (decodeClause atoms clause565) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 567: packet; source clause 119115.
omit compatible in
private theorem sound566 : C.clause (decodeClause atoms clause566) := by
  exact C.covered_clause _ _ (C.packet_clause 2 5 11 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 568: packet; source clause 119138.
omit compatible in
private theorem sound567 : C.clause (decodeClause atoms clause567) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 569: packet; source clause 119143.
omit compatible in
private theorem sound568 : C.clause (decodeClause atoms clause568) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 570: packet; source clause 119144.
omit compatible in
private theorem sound569 : C.clause (decodeClause atoms clause569) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 571: packet; source clause 119160.
omit compatible in
private theorem sound570 : C.clause (decodeClause atoms clause570) := by
  exact C.covered_clause _ _ (C.packet_clause 5 2 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 572: packet; source clause 119171.
omit compatible in
private theorem sound571 : C.clause (decodeClause atoms clause571) := by
  exact C.covered_clause _ _ (C.packet_clause 5 8 2 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 573: convex_four; source clause 119313.
omit compatible in
private theorem sound572 : C.clause (decodeClause atoms clause572) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 574: packet; source clause 119320.
omit compatible in
private theorem sound573 : C.clause (decodeClause atoms clause573) := by
  exact C.covered_clause _ _ (C.packet_clause 2 5 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 575: packet; source clause 119323.
omit compatible in
private theorem sound574 : C.clause (decodeClause atoms clause574) := by
  exact C.covered_clause _ _ (C.packet_clause 2 5 12 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 576: packet; source clause 119346.
omit compatible in
private theorem sound575 : C.clause (decodeClause atoms clause575) := by
  exact C.covered_clause _ _ (C.packet_clause 2 12 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 577: convex_four; source clause 119517.
omit compatible in
private theorem sound576 : C.clause (decodeClause atoms clause576) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 578: convex_four; source clause 119520.
omit compatible in
private theorem sound577 : C.clause (decodeClause atoms clause577) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true false) (by decide +kernel)

-- Clause 579: convex_four; source clause 119521.
omit compatible in
private theorem sound578 : C.clause (decodeClause atoms clause578) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 580: packet; source clause 119537.
omit compatible in
private theorem sound579 : C.clause (decodeClause atoms clause579) := by
  exact C.covered_clause _ _ (C.packet_clause 2 5 10 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 581: packet; source clause 119554.
omit compatible in
private theorem sound580 : C.clause (decodeClause atoms clause580) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 582: packet; source clause 119593.
omit compatible in
private theorem sound581 : C.clause (decodeClause atoms clause581) := by
  exact C.covered_clause _ _ (C.packet_clause 5 9 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 583: convex_four; source clause 119729.
omit compatible in
private theorem sound582 : C.clause (decodeClause atoms clause582) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 584: packet; source clause 119745.
omit compatible in
private theorem sound583 : C.clause (decodeClause atoms clause583) := by
  exact C.covered_clause _ _ (C.packet_clause 2 5 11 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 585: convex_four; source clause 119929.
omit compatible in
private theorem sound584 : C.clause (decodeClause atoms clause584) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true true) (by decide +kernel)

-- Clause 586: convex_four; source clause 119936.
omit compatible in
private theorem sound585 : C.clause (decodeClause atoms clause585) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true false) (by decide +kernel)

-- Clause 587: convex_four; source clause 119937.
omit compatible in
private theorem sound586 : C.clause (decodeClause atoms clause586) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 588: packet; source clause 119945.
omit compatible in
private theorem sound587 : C.clause (decodeClause atoms clause587) := by
  exact C.covered_clause _ _ (C.packet_clause 2 5 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 589: packet; source clause 119947.
omit compatible in
private theorem sound588 : C.clause (decodeClause atoms clause588) := by
  exact C.covered_clause _ _ (C.packet_clause 2 5 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 590: packet; source clause 119986.
omit compatible in
private theorem sound589 : C.clause (decodeClause atoms clause589) := by
  exact C.covered_clause _ _ (C.packet_clause 5 2 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 591: packet; source clause 120003.
omit compatible in
private theorem sound590 : C.clause (decodeClause atoms clause590) := by
  exact C.covered_clause _ _ (C.packet_clause 5 9 2 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 592: packet; source clause 120038.
omit compatible in
private theorem sound591 : C.clause (decodeClause atoms clause591) := by
  exact C.covered_clause _ _ (C.packet_clause 9 2 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 593: convex_four; source clause 120145.
omit compatible in
private theorem sound592 : C.clause (decodeClause atoms clause592) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 594: packet; source clause 120170.
omit compatible in
private theorem sound593 : C.clause (decodeClause atoms clause593) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 11 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 595: packet; source clause 120171.
omit compatible in
private theorem sound594 : C.clause (decodeClause atoms clause594) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 11 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 596: packet; source clause 120214.
omit compatible in
private theorem sound595 : C.clause (decodeClause atoms clause595) := by
  exact C.covered_clause _ _ (C.packet_clause 5 10 2 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 597: packet; source clause 120221.
omit compatible in
private theorem sound596 : C.clause (decodeClause atoms clause596) := by
  exact C.covered_clause _ _ (C.packet_clause 5 10 11 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 598: convex_four; source clause 120342.
omit compatible in
private theorem sound597 : C.clause (decodeClause atoms clause597) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 599: convex_four; source clause 120346.
omit compatible in
private theorem sound598 : C.clause (decodeClause atoms clause598) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 600: convex_four; source clause 120350.
omit compatible in
private theorem sound599 : C.clause (decodeClause atoms clause599) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 601: packet; source clause 120376.
omit compatible in
private theorem sound600 : C.clause (decodeClause atoms clause600) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 602: packet; source clause 120378.
omit compatible in
private theorem sound601 : C.clause (decodeClause atoms clause601) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 12 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 603: packet; source clause 120403.
omit compatible in
private theorem sound602 : C.clause (decodeClause atoms clause602) := by
  exact C.covered_clause _ _ (C.packet_clause 5 2 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 604: convex_four; source clause 120550.
omit compatible in
private theorem sound603 : C.clause (decodeClause atoms clause603) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 605: convex_four; source clause 120558.
omit compatible in
private theorem sound604 : C.clause (decodeClause atoms clause604) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 606: packet; source clause 120563.
omit compatible in
private theorem sound605 : C.clause (decodeClause atoms clause605) := by
  exact C.covered_clause _ _ (C.packet_clause 2 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 607: packet; source clause 120583.
omit compatible in
private theorem sound606 : C.clause (decodeClause atoms clause606) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 608: packet; source clause 120584.
omit compatible in
private theorem sound607 : C.clause (decodeClause atoms clause607) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 609: convex_four; source clause 120758.
omit compatible in
private theorem sound608 : C.clause (decodeClause atoms clause608) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 610: convex_four; source clause 120759.
omit compatible in
private theorem sound609 : C.clause (decodeClause atoms clause609) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true) (by decide +kernel)

-- Clause 611: convex_four; source clause 120762.
omit compatible in
private theorem sound610 : C.clause (decodeClause atoms clause610) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 612: convex_four; source clause 120766.
omit compatible in
private theorem sound611 : C.clause (decodeClause atoms clause611) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 613: convex_four; source clause 120767.
omit compatible in
private theorem sound612 : C.clause (decodeClause atoms clause612) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true) (by decide +kernel)

-- Clause 614: packet; source clause 121187.
omit compatible in
private theorem sound613 : C.clause (decodeClause atoms clause613) := by
  exact C.covered_clause _ _ (C.packet_clause 2 6 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 615: packet; source clause 121208.
omit compatible in
private theorem sound614 : C.clause (decodeClause atoms clause614) := by
  exact C.covered_clause _ _ (C.packet_clause 2 7 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 616: packet; source clause 121288.
omit compatible in
private theorem sound615 : C.clause (decodeClause atoms clause615) := by
  exact C.covered_clause _ _ (C.packet_clause 7 2 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 617: convex_four; source clause 121386.
omit compatible in
private theorem sound616 : C.clause (decodeClause atoms clause616) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 618: convex_four; source clause 121390.
omit compatible in
private theorem sound617 : C.clause (decodeClause atoms clause617) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 619: convex_four; source clause 121392.
omit compatible in
private theorem sound618 : C.clause (decodeClause atoms clause618) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true false) (by decide +kernel)

-- Clause 620: packet; source clause 121395.
omit compatible in
private theorem sound619 : C.clause (decodeClause atoms clause619) := by
  exact C.covered_clause _ _ (C.packet_clause 2 6 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 621: packet; source clause 121416.
omit compatible in
private theorem sound620 : C.clause (decodeClause atoms clause620) := by
  exact C.covered_clause _ _ (C.packet_clause 2 7 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 622: packet; source clause 121522.
omit compatible in
private theorem sound621 : C.clause (decodeClause atoms clause621) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 2 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 623: packet; source clause 121577.
omit compatible in
private theorem sound622 : C.clause (decodeClause atoms clause622) := by
  exact C.covered_clause _ _ (C.packet_clause 11 7 2 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 624: convex_four; source clause 121594.
omit compatible in
private theorem sound623 : C.clause (decodeClause atoms clause623) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 625: convex_four; source clause 121598.
omit compatible in
private theorem sound624 : C.clause (decodeClause atoms clause624) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 626: packet; source clause 123266.
omit compatible in
private theorem sound625 : C.clause (decodeClause atoms clause625) := by
  exact C.covered_clause _ _ (C.packet_clause 2 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 627: packet; source clause 123267.
omit compatible in
private theorem sound626 : C.clause (decodeClause atoms clause626) := by
  exact C.covered_clause _ _ (C.packet_clause 2 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 628: packet; source clause 123269.
omit compatible in
private theorem sound627 : C.clause (decodeClause atoms clause627) := by
  exact C.covered_clause _ _ (C.packet_clause 2 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 629: packet; source clause 123272.
omit compatible in
private theorem sound628 : C.clause (decodeClause atoms clause628) := by
  exact C.covered_clause _ _ (C.packet_clause 2 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 630: packet; source clause 123275.
omit compatible in
private theorem sound629 : C.clause (decodeClause atoms clause629) := by
  exact C.covered_clause _ _ (C.packet_clause 2 6 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 631: packet; source clause 123304.
omit compatible in
private theorem sound630 : C.clause (decodeClause atoms clause630) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 632: packet; source clause 123415.
omit compatible in
private theorem sound631 : C.clause (decodeClause atoms clause631) := by
  exact C.covered_clause _ _ (C.packet_clause 11 2 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 633: packet; source clause 123416.
omit compatible in
private theorem sound632 : C.clause (decodeClause atoms clause632) := by
  exact C.covered_clause _ _ (C.packet_clause 11 2 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 634: convex_four; source clause 123472.
omit compatible in
private theorem sound633 : C.clause (decodeClause atoms clause633) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true false) (by decide +kernel)

-- Clause 635: convex_four; source clause 123473.
omit compatible in
private theorem sound634 : C.clause (decodeClause atoms clause634) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 636: packet; source clause 125354.
omit compatible in
private theorem sound635 : C.clause (decodeClause atoms clause635) := by
  exact C.covered_clause _ _ (C.packet_clause 2 7 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 637: packet; source clause 125355.
omit compatible in
private theorem sound636 : C.clause (decodeClause atoms clause636) := by
  exact C.covered_clause _ _ (C.packet_clause 2 7 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 638: packet; source clause 125357.
omit compatible in
private theorem sound637 : C.clause (decodeClause atoms clause637) := by
  exact C.covered_clause _ _ (C.packet_clause 2 7 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 639: packet; source clause 125363.
omit compatible in
private theorem sound638 : C.clause (decodeClause atoms clause638) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 640: packet; source clause 125406.
omit compatible in
private theorem sound639 : C.clause (decodeClause atoms clause639) := by
  exact C.covered_clause _ _ (C.packet_clause 7 2 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 641: packet; source clause 125409.
omit compatible in
private theorem sound640 : C.clause (decodeClause atoms clause640) := by
  exact C.covered_clause _ _ (C.packet_clause 7 2 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 642: packet; source clause 125426.
omit compatible in
private theorem sound641 : C.clause (decodeClause atoms clause641) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 643: packet; source clause 125443.
omit compatible in
private theorem sound642 : C.clause (decodeClause atoms clause642) := by
  exact C.covered_clause _ _ (C.packet_clause 10 2 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 644: packet; source clause 125456.
omit compatible in
private theorem sound643 : C.clause (decodeClause atoms clause643) := by
  exact C.covered_clause _ _ (C.packet_clause 10 2 11 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 645: packet; source clause 125475.
omit compatible in
private theorem sound644 : C.clause (decodeClause atoms clause644) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 2 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 646: packet; source clause 125486.
omit compatible in
private theorem sound645 : C.clause (decodeClause atoms clause645) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 7 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 647: packet; source clause 125488.
omit compatible in
private theorem sound646 : C.clause (decodeClause atoms clause646) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 7 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 648: convex_four; source clause 125541.
omit compatible in
private theorem sound647 : C.clause (decodeClause atoms clause647) := by
  exact C.covered_clause _ _ (C.convex_clause 2 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 649: convex_four; source clause 125549.
omit compatible in
private theorem sound648 : C.clause (decodeClause atoms clause648) := by
  exact C.covered_clause _ _ (C.convex_clause 2 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 650: packet; source clause 125788.
omit compatible in
private theorem sound649 : C.clause (decodeClause atoms clause649) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 12 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 651: packet; source clause 125793.
omit compatible in
private theorem sound650 : C.clause (decodeClause atoms clause650) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 12 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 652: packet; source clause 125866.
omit compatible in
private theorem sound651 : C.clause (decodeClause atoms clause651) := by
  exact C.covered_clause _ _ (C.packet_clause 11 2 12 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 653: packet; source clause 125871.
omit compatible in
private theorem sound652 : C.clause (decodeClause atoms clause652) := by
  exact C.covered_clause _ _ (C.packet_clause 11 2 12 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 654: packet; source clause 125872.
omit compatible in
private theorem sound653 : C.clause (decodeClause atoms clause653) := by
  exact C.covered_clause _ _ (C.packet_clause 11 2 12 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 655: packet; source clause 126008.
omit compatible in
private theorem sound654 : C.clause (decodeClause atoms clause654) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 656: packet; source clause 126035.
omit compatible in
private theorem sound655 : C.clause (decodeClause atoms clause655) := by
  exact C.covered_clause _ _ (C.packet_clause 8 9 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 657: convex_four; source clause 126169.
omit compatible in
private theorem sound656 : C.clause (decodeClause atoms clause656) := by
  exact C.covered_clause _ _ (C.convex_clause 2 8 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true true) (by decide +kernel)

-- Clause 658: convex_four; source clause 126177.
omit compatible in
private theorem sound657 : C.clause (decodeClause atoms clause657) := by
  exact C.covered_clause _ _ (C.convex_clause 2 8 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 659: packet; source clause 126216.
omit compatible in
private theorem sound658 : C.clause (decodeClause atoms clause658) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 660: convex_four; source clause 126385.
omit compatible in
private theorem sound659 : C.clause (decodeClause atoms clause659) := by
  exact C.covered_clause _ _ (C.convex_clause 2 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 661: packet; source clause 126395.
omit compatible in
private theorem sound660 : C.clause (decodeClause atoms clause660) := by
  exact C.covered_clause _ _ (C.packet_clause 2 8 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 662: packet; source clause 126426.
omit compatible in
private theorem sound661 : C.clause (decodeClause atoms clause661) := by
  exact C.covered_clause _ _ (C.packet_clause 2 12 9 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 663: packet; source clause 126440.
omit compatible in
private theorem sound662 : C.clause (decodeClause atoms clause662) := by
  exact C.covered_clause _ _ (C.packet_clause 8 2 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 664: packet; source clause 126451.
omit compatible in
private theorem sound663 : C.clause (decodeClause atoms clause663) := by
  exact C.covered_clause _ _ (C.packet_clause 8 9 2 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 665: convex_four; source clause 126591.
omit compatible in
private theorem sound664 : C.clause (decodeClause atoms clause664) := by
  exact C.covered_clause _ _ (C.convex_clause 2 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true) (by decide +kernel)

-- Clause 666: convex_four; source clause 126593.
omit compatible in
private theorem sound665 : C.clause (decodeClause atoms clause665) := by
  exact C.covered_clause _ _ (C.convex_clause 2 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 667: packet; source clause 126601.
omit compatible in
private theorem sound666 : C.clause (decodeClause atoms clause666) := by
  exact C.covered_clause _ _ (C.packet_clause 2 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 668: packet; source clause 126610.
omit compatible in
private theorem sound667 : C.clause (decodeClause atoms clause667) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 669: packet; source clause 126618.
omit compatible in
private theorem sound668 : C.clause (decodeClause atoms clause668) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 11 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 670: packet; source clause 126629.
omit compatible in
private theorem sound669 : C.clause (decodeClause atoms clause669) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 671: packet; source clause 126643.
omit compatible in
private theorem sound670 : C.clause (decodeClause atoms clause670) := by
  exact C.covered_clause _ _ (C.packet_clause 8 2 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 672: convex_four; source clause 126798.
omit compatible in
private theorem sound671 : C.clause (decodeClause atoms clause671) := by
  exact C.covered_clause _ _ (C.convex_clause 2 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 673: packet; source clause 126822.
omit compatible in
private theorem sound672 : C.clause (decodeClause atoms clause672) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 674: packet; source clause 126824.
omit compatible in
private theorem sound673 : C.clause (decodeClause atoms clause673) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 675: packet; source clause 126826.
omit compatible in
private theorem sound674 : C.clause (decodeClause atoms clause674) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 12 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 676: packet; source clause 126827.
omit compatible in
private theorem sound675 : C.clause (decodeClause atoms clause675) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 12 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 677: packet; source clause 126829.
omit compatible in
private theorem sound676 : C.clause (decodeClause atoms clause676) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 12 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 678: packet; source clause 126851.
omit compatible in
private theorem sound677 : C.clause (decodeClause atoms clause677) := by
  exact C.covered_clause _ _ (C.packet_clause 8 2 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 679: convex_four; source clause 127006.
omit compatible in
private theorem sound678 : C.clause (decodeClause atoms clause678) := by
  exact C.covered_clause _ _ (C.convex_clause 2 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 680: packet; source clause 127011.
omit compatible in
private theorem sound679 : C.clause (decodeClause atoms clause679) := by
  exact C.covered_clause _ _ (C.packet_clause 2 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 681: packet; source clause 127032.
omit compatible in
private theorem sound680 : C.clause (decodeClause atoms clause680) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 682: packet; source clause 127035.
omit compatible in
private theorem sound681 : C.clause (decodeClause atoms clause681) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 12 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 683: convex_four; source clause 127206.
omit compatible in
private theorem sound682 : C.clause (decodeClause atoms clause682) := by
  exact C.covered_clause _ _ (C.convex_clause 2 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 684: convex_four; source clause 127214.
omit compatible in
private theorem sound683 : C.clause (decodeClause atoms clause683) := by
  exact C.covered_clause _ _ (C.convex_clause 2 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 685: packet; source clause 127219.
omit compatible in
private theorem sound684 : C.clause (decodeClause atoms clause684) := by
  exact C.covered_clause _ _ (C.packet_clause 2 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 686: packet; source clause 127240.
omit compatible in
private theorem sound685 : C.clause (decodeClause atoms clause685) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 687: packet; source clause 127242.
omit compatible in
private theorem sound686 : C.clause (decodeClause atoms clause686) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 11 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 688: packet; source clause 127243.
omit compatible in
private theorem sound687 : C.clause (decodeClause atoms clause687) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 11 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 689: packet; source clause 127245.
omit compatible in
private theorem sound688 : C.clause (decodeClause atoms clause688) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 11 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 690: convex_four; source clause 127422.
omit compatible in
private theorem sound689 : C.clause (decodeClause atoms clause689) := by
  exact C.covered_clause _ _ (C.convex_clause 2 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 691: packet; source clause 127448.
omit compatible in
private theorem sound690 : C.clause (decodeClause atoms clause690) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 692: packet; source clause 127450.
omit compatible in
private theorem sound691 : C.clause (decodeClause atoms clause691) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 693: convex_four; source clause 127622.
omit compatible in
private theorem sound692 : C.clause (decodeClause atoms clause692) := by
  exact C.covered_clause _ _ (C.convex_clause 2 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 694: convex_four; source clause 127630.
omit compatible in
private theorem sound693 : C.clause (decodeClause atoms clause693) := by
  exact C.covered_clause _ _ (C.convex_clause 2 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 695: convex_four; source clause 127632.
omit compatible in
private theorem sound694 : C.clause (decodeClause atoms clause694) := by
  exact C.covered_clause _ _ (C.convex_clause 2 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true false) (by decide +kernel)

-- Clause 696: packet; source clause 127635.
omit compatible in
private theorem sound695 : C.clause (decodeClause atoms clause695) := by
  exact C.covered_clause _ _ (C.packet_clause 2 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 697: packet; source clause 127656.
omit compatible in
private theorem sound696 : C.clause (decodeClause atoms clause696) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 698: convex_four; source clause 127838.
omit compatible in
private theorem sound697 : C.clause (decodeClause atoms clause697) := by
  exact C.covered_clause _ _ (C.convex_clause 2 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 699: convex_four; source clause 127840.
omit compatible in
private theorem sound698 : C.clause (decodeClause atoms clause698) := by
  exact C.covered_clause _ _ (C.convex_clause 2 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true false) (by decide +kernel)

-- Clause 700: packet; source clause 127842.
omit compatible in
private theorem sound699 : C.clause (decodeClause atoms clause699) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 701: packet; source clause 127843.
omit compatible in
private theorem sound700 : C.clause (decodeClause atoms clause700) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 702: packet; source clause 127845.
omit compatible in
private theorem sound701 : C.clause (decodeClause atoms clause701) := by
  exact C.covered_clause _ _ (C.packet_clause 2 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 703: convex_four; source clause 128034.
omit compatible in
private theorem sound702 : C.clause (decodeClause atoms clause702) := by
  exact C.covered_clause _ _ (C.convex_clause 2 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 704: packet; source clause 138673.
omit compatible in
private theorem sound703 : C.clause (decodeClause atoms clause703) := by
  exact C.covered_clause _ _ (C.packet_clause 3 6 10 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 705: packet; source clause 138714.
omit compatible in
private theorem sound704 : C.clause (decodeClause atoms clause704) := by
  exact C.covered_clause _ _ (C.packet_clause 6 3 10 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 706: packet; source clause 138745.
omit compatible in
private theorem sound705 : C.clause (decodeClause atoms clause705) := by
  exact C.covered_clause _ _ (C.packet_clause 6 10 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 707: packet; source clause 138760.
omit compatible in
private theorem sound706 : C.clause (decodeClause atoms clause706) := by
  exact C.covered_clause _ _ (C.packet_clause 7 3 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 708: packet; source clause 138771.
omit compatible in
private theorem sound707 : C.clause (decodeClause atoms clause707) := by
  exact C.covered_clause _ _ (C.packet_clause 7 6 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 709: packet; source clause 138773.
omit compatible in
private theorem sound708 : C.clause (decodeClause atoms clause708) := by
  exact C.covered_clause _ _ (C.packet_clause 7 6 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 710: packet; source clause 138782.
omit compatible in
private theorem sound709 : C.clause (decodeClause atoms clause709) := by
  exact C.covered_clause _ _ (C.packet_clause 7 6 10 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 711: packet; source clause 138784.
omit compatible in
private theorem sound710 : C.clause (decodeClause atoms clause710) := by
  exact C.covered_clause _ _ (C.packet_clause 7 6 10 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 712: convex_four; source clause 138862.
omit compatible in
private theorem sound711 : C.clause (decodeClause atoms clause711) := by
  exact C.covered_clause _ _ (C.convex_clause 3 6 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 713: packet; source clause 138890.
omit compatible in
private theorem sound712 : C.clause (decodeClause atoms clause712) := by
  exact C.covered_clause _ _ (C.packet_clause 3 7 11 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 714: packet; source clause 138910.
omit compatible in
private theorem sound713 : C.clause (decodeClause atoms clause713) := by
  exact C.covered_clause _ _ (C.packet_clause 3 11 7 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 715: packet; source clause 138913.
omit compatible in
private theorem sound714 : C.clause (decodeClause atoms clause714) := by
  exact C.covered_clause _ _ (C.packet_clause 3 11 7 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 716: packet; source clause 138934.
omit compatible in
private theorem sound715 : C.clause (decodeClause atoms clause715) := by
  exact C.covered_clause _ _ (C.packet_clause 6 7 3 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 717: packet; source clause 138936.
omit compatible in
private theorem sound716 : C.clause (decodeClause atoms clause716) := by
  exact C.covered_clause _ _ (C.packet_clause 6 7 3 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 718: packet; source clause 138939.
omit compatible in
private theorem sound717 : C.clause (decodeClause atoms clause717) := by
  exact C.covered_clause _ _ (C.packet_clause 6 7 11 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 719: packet; source clause 138941.
omit compatible in
private theorem sound718 : C.clause (decodeClause atoms clause718) := by
  exact C.covered_clause _ _ (C.packet_clause 6 7 11 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 720: packet; source clause 138977.
omit compatible in
private theorem sound719 : C.clause (decodeClause atoms clause719) := by
  exact C.covered_clause _ _ (C.packet_clause 7 3 11 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 721: packet; source clause 139018.
omit compatible in
private theorem sound720 : C.clause (decodeClause atoms clause720) := by
  exact C.covered_clause _ _ (C.packet_clause 11 3 7 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 722: packet; source clause 139021.
omit compatible in
private theorem sound721 : C.clause (decodeClause atoms clause721) := by
  exact C.covered_clause _ _ (C.packet_clause 11 3 7 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 723: convex_four; source clause 139066.
omit compatible in
private theorem sound722 : C.clause (decodeClause atoms clause722) := by
  exact C.covered_clause _ _ (C.convex_clause 3 6 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 724: convex_four; source clause 139070.
omit compatible in
private theorem sound723 : C.clause (decodeClause atoms clause723) := by
  exact C.covered_clause _ _ (C.convex_clause 3 6 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 725: packet; source clause 140744.
omit compatible in
private theorem sound724 : C.clause (decodeClause atoms clause724) := by
  exact C.covered_clause _ _ (C.packet_clause 3 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 726: packet; source clause 140747.
omit compatible in
private theorem sound725 : C.clause (decodeClause atoms clause725) := by
  exact C.covered_clause _ _ (C.packet_clause 3 6 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 727: convex_four; source clause 140945.
omit compatible in
private theorem sound726 : C.clause (decodeClause atoms clause726) := by
  exact C.covered_clause _ _ (C.convex_clause 3 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 728: packet; source clause 142822.
omit compatible in
private theorem sound727 : C.clause (decodeClause atoms clause727) := by
  exact C.covered_clause _ _ (C.packet_clause 3 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 729: packet; source clause 142824.
omit compatible in
private theorem sound728 : C.clause (decodeClause atoms clause728) := by
  exact C.covered_clause _ _ (C.packet_clause 3 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 730: packet; source clause 142826.
omit compatible in
private theorem sound729 : C.clause (decodeClause atoms clause729) := by
  exact C.covered_clause _ _ (C.packet_clause 3 7 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 731: packet; source clause 142827.
omit compatible in
private theorem sound730 : C.clause (decodeClause atoms clause730) := by
  exact C.covered_clause _ _ (C.packet_clause 3 7 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 732: packet; source clause 142829.
omit compatible in
private theorem sound731 : C.clause (decodeClause atoms clause731) := by
  exact C.covered_clause _ _ (C.packet_clause 3 7 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 733: packet; source clause 142869.
omit compatible in
private theorem sound732 : C.clause (decodeClause atoms clause732) := by
  exact C.covered_clause _ _ (C.packet_clause 7 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 734: packet; source clause 142881.
omit compatible in
private theorem sound733 : C.clause (decodeClause atoms clause733) := by
  exact C.covered_clause _ _ (C.packet_clause 7 3 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 735: packet; source clause 142898.
omit compatible in
private theorem sound734 : C.clause (decodeClause atoms clause734) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 736: packet; source clause 143002.
omit compatible in
private theorem sound735 : C.clause (decodeClause atoms clause735) := by
  exact C.covered_clause _ _ (C.packet_clause 11 10 7 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 737: packet; source clause 143005.
omit compatible in
private theorem sound736 : C.clause (decodeClause atoms clause736) := by
  exact C.covered_clause _ _ (C.packet_clause 11 10 7 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 738: convex_four; source clause 143011.
omit compatible in
private theorem sound737 : C.clause (decodeClause atoms clause737) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false true) (by decide +kernel)

-- Clause 739: convex_four; source clause 143013.
omit compatible in
private theorem sound738 : C.clause (decodeClause atoms clause738) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 740: packet; source clause 147814.
omit compatible in
private theorem sound739 : C.clause (decodeClause atoms clause739) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 741: packet; source clause 147816.
omit compatible in
private theorem sound740 : C.clause (decodeClause atoms clause740) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 742: packet; source clause 147817.
omit compatible in
private theorem sound741 : C.clause (decodeClause atoms clause741) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 743: packet; source clause 147858.
omit compatible in
private theorem sound742 : C.clause (decodeClause atoms clause742) := by
  exact C.covered_clause _ _ (C.packet_clause 5 4 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 744: packet; source clause 147861.
omit compatible in
private theorem sound743 : C.clause (decodeClause atoms clause743) := by
  exact C.covered_clause _ _ (C.packet_clause 5 4 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 745: convex_four; source clause 148017.
omit compatible in
private theorem sound744 : C.clause (decodeClause atoms clause744) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 746: packet; source clause 148025.
omit compatible in
private theorem sound745 : C.clause (decodeClause atoms clause745) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 747: packet; source clause 148034.
omit compatible in
private theorem sound746 : C.clause (decodeClause atoms clause746) := by
  exact C.covered_clause _ _ (C.packet_clause 4 8 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 748: packet; source clause 148037.
omit compatible in
private theorem sound747 : C.clause (decodeClause atoms clause747) := by
  exact C.covered_clause _ _ (C.packet_clause 4 8 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 749: packet; source clause 148066.
omit compatible in
private theorem sound748 : C.clause (decodeClause atoms clause748) := by
  exact C.covered_clause _ _ (C.packet_clause 5 4 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 750: packet; source clause 148089.
omit compatible in
private theorem sound749 : C.clause (decodeClause atoms clause749) := by
  exact C.covered_clause _ _ (C.packet_clause 5 8 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 751: packet; source clause 148118.
omit compatible in
private theorem sound750 : C.clause (decodeClause atoms clause750) := by
  exact C.covered_clause _ _ (C.packet_clause 8 4 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 752: packet; source clause 148121.
omit compatible in
private theorem sound751 : C.clause (decodeClause atoms clause751) := by
  exact C.covered_clause _ _ (C.packet_clause 8 4 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 753: packet; source clause 148130.
omit compatible in
private theorem sound752 : C.clause (decodeClause atoms clause752) := by
  exact C.covered_clause _ _ (C.packet_clause 8 5 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 754: packet; source clause 148168.
omit compatible in
private theorem sound753 : C.clause (decodeClause atoms clause753) := by
  exact C.covered_clause _ _ (C.packet_clause 10 4 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 755: packet; source clause 148179.
omit compatible in
private theorem sound754 : C.clause (decodeClause atoms clause754) := by
  exact C.covered_clause _ _ (C.packet_clause 10 5 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 756: packet; source clause 148181.
omit compatible in
private theorem sound755 : C.clause (decodeClause atoms clause755) := by
  exact C.covered_clause _ _ (C.packet_clause 10 5 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 757: packet; source clause 148190.
omit compatible in
private theorem sound756 : C.clause (decodeClause atoms clause756) := by
  exact C.covered_clause _ _ (C.packet_clause 10 5 8 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 758: packet; source clause 148192.
omit compatible in
private theorem sound757 : C.clause (decodeClause atoms clause757) := by
  exact C.covered_clause _ _ (C.packet_clause 10 5 8 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 759: convex_four; source clause 148225.
omit compatible in
private theorem sound758 : C.clause (decodeClause atoms clause758) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 760: packet; source clause 148232.
omit compatible in
private theorem sound759 : C.clause (decodeClause atoms clause759) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 761: packet; source clause 148235.
omit compatible in
private theorem sound760 : C.clause (decodeClause atoms clause760) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 11 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 762: packet; source clause 148236.
omit compatible in
private theorem sound761 : C.clause (decodeClause atoms clause761) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 11 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 763: packet; source clause 148241.
omit compatible in
private theorem sound762 : C.clause (decodeClause atoms clause762) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 11 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 764: packet; source clause 148264.
omit compatible in
private theorem sound763 : C.clause (decodeClause atoms clause763) := by
  exact C.covered_clause _ _ (C.packet_clause 4 11 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 765: packet; source clause 148376.
omit compatible in
private theorem sound764 : C.clause (decodeClause atoms clause764) := by
  exact C.covered_clause _ _ (C.packet_clause 11 4 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 766: convex_four; source clause 148431.
omit compatible in
private theorem sound765 : C.clause (decodeClause atoms clause765) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true) (by decide +kernel)

-- Clause 767: convex_four; source clause 148433.
omit compatible in
private theorem sound766 : C.clause (decodeClause atoms clause766) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 768: packet; source clause 148438.
omit compatible in
private theorem sound767 : C.clause (decodeClause atoms clause767) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 769: packet; source clause 148440.
omit compatible in
private theorem sound768 : C.clause (decodeClause atoms clause768) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 770: packet; source clause 148441.
omit compatible in
private theorem sound769 : C.clause (decodeClause atoms clause769) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 771: packet; source clause 148443.
omit compatible in
private theorem sound770 : C.clause (decodeClause atoms clause770) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 12 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 772: packet; source clause 148472.
omit compatible in
private theorem sound771 : C.clause (decodeClause atoms clause771) := by
  exact C.covered_clause _ _ (C.packet_clause 4 12 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 773: convex_four; source clause 148637.
omit compatible in
private theorem sound772 : C.clause (decodeClause atoms clause772) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 774: convex_four; source clause 148641.
omit compatible in
private theorem sound773 : C.clause (decodeClause atoms clause773) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 775: packet; source clause 148649.
omit compatible in
private theorem sound774 : C.clause (decodeClause atoms clause774) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 776: packet; source clause 148792.
omit compatible in
private theorem sound775 : C.clause (decodeClause atoms clause775) := by
  exact C.covered_clause _ _ (C.packet_clause 10 4 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 777: convex_four; source clause 148849.
omit compatible in
private theorem sound776 : C.clause (decodeClause atoms clause776) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 778: packet; source clause 148878.
omit compatible in
private theorem sound777 : C.clause (decodeClause atoms clause777) := by
  exact C.covered_clause _ _ (C.packet_clause 4 9 11 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 779: packet; source clause 149000.
omit compatible in
private theorem sound778 : C.clause (decodeClause atoms clause778) := by
  exact C.covered_clause _ _ (C.packet_clause 11 4 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 780: convex_four; source clause 149057.
omit compatible in
private theorem sound779 : C.clause (decodeClause atoms clause779) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 781: packet; source clause 149064.
omit compatible in
private theorem sound780 : C.clause (decodeClause atoms clause780) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 782: packet; source clause 149067.
omit compatible in
private theorem sound781 : C.clause (decodeClause atoms clause781) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 783: packet; source clause 149073.
omit compatible in
private theorem sound782 : C.clause (decodeClause atoms clause782) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 784: packet; source clause 149098.
omit compatible in
private theorem sound783 : C.clause (decodeClause atoms clause783) := by
  exact C.covered_clause _ _ (C.packet_clause 4 12 9 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 785: packet; source clause 149101.
omit compatible in
private theorem sound784 : C.clause (decodeClause atoms clause784) := by
  exact C.covered_clause _ _ (C.packet_clause 4 12 9 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 786: packet; source clause 149217.
omit compatible in
private theorem sound785 : C.clause (decodeClause atoms clause785) := by
  exact C.covered_clause _ _ (C.packet_clause 12 4 9 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 787: convex_four; source clause 149265.
omit compatible in
private theorem sound786 : C.clause (decodeClause atoms clause786) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 788: packet; source clause 149273.
omit compatible in
private theorem sound787 : C.clause (decodeClause atoms clause787) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 789: packet; source clause 149290.
omit compatible in
private theorem sound788 : C.clause (decodeClause atoms clause788) := by
  exact C.covered_clause _ _ (C.packet_clause 4 10 11 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 790: packet; source clause 149394.
omit compatible in
private theorem sound789 : C.clause (decodeClause atoms clause789) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 4 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 791: packet; source clause 149399.
omit compatible in
private theorem sound790 : C.clause (decodeClause atoms clause790) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 4 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 792: packet; source clause 149400.
omit compatible in
private theorem sound791 : C.clause (decodeClause atoms clause791) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 4 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 793: convex_four; source clause 149470.
omit compatible in
private theorem sound792 : C.clause (decodeClause atoms clause792) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 794: packet; source clause 149542.
omit compatible in
private theorem sound793 : C.clause (decodeClause atoms clause793) := by
  exact C.covered_clause _ _ (C.packet_clause 5 10 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 795: packet; source clause 149544.
omit compatible in
private theorem sound794 : C.clause (decodeClause atoms clause794) := by
  exact C.covered_clause _ _ (C.packet_clause 5 10 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 796: packet; source clause 149547.
omit compatible in
private theorem sound795 : C.clause (decodeClause atoms clause795) := by
  exact C.covered_clause _ _ (C.packet_clause 5 10 12 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 797: packet; source clause 149549.
omit compatible in
private theorem sound796 : C.clause (decodeClause atoms clause796) := by
  exact C.covered_clause _ _ (C.packet_clause 5 10 12 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 798: packet; source clause 149598.
omit compatible in
private theorem sound797 : C.clause (decodeClause atoms clause797) := by
  exact C.covered_clause _ _ (C.packet_clause 10 5 12 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 799: packet; source clause 149602.
omit compatible in
private theorem sound798 : C.clause (decodeClause atoms clause798) := by
  exact C.covered_clause _ _ (C.packet_clause 10 12 4 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 800: convex_four; source clause 149678.
omit compatible in
private theorem sound799 : C.clause (decodeClause atoms clause799) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 801: packet; source clause 149683.
omit compatible in
private theorem sound800 : C.clause (decodeClause atoms clause800) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 802: packet; source clause 149684.
omit compatible in
private theorem sound801 : C.clause (decodeClause atoms clause801) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 803: packet; source clause 149689.
omit compatible in
private theorem sound802 : C.clause (decodeClause atoms clause802) := by
  exact C.covered_clause _ _ (C.packet_clause 4 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 804: convex_four; source clause 149878.
omit compatible in
private theorem sound803 : C.clause (decodeClause atoms clause803) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 805: convex_four; source clause 149886.
omit compatible in
private theorem sound804 : C.clause (decodeClause atoms clause804) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 806: convex_four; source clause 149888.
omit compatible in
private theorem sound805 : C.clause (decodeClause atoms clause805) := by
  exact C.covered_clause _ _ (C.convex_clause 4 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true false) (by decide +kernel)

-- Clause 807: convex_four; source clause 155297.
omit compatible in
private theorem sound806 : C.clause (decodeClause atoms clause806) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 808: packet; source clause 155307.
omit compatible in
private theorem sound807 : C.clause (decodeClause atoms clause807) := by
  exact C.covered_clause _ _ (C.packet_clause 4 8 11 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 809: convex_four; source clause 155505.
omit compatible in
private theorem sound808 : C.clause (decodeClause atoms clause808) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 810: packet; source clause 155510.
omit compatible in
private theorem sound809 : C.clause (decodeClause atoms clause809) := by
  exact C.covered_clause _ _ (C.packet_clause 4 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 811: packet; source clause 155512.
omit compatible in
private theorem sound810 : C.clause (decodeClause atoms clause810) := by
  exact C.covered_clause _ _ (C.packet_clause 4 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 812: packet; source clause 155513.
omit compatible in
private theorem sound811 : C.clause (decodeClause atoms clause811) := by
  exact C.covered_clause _ _ (C.packet_clause 4 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 813: packet; source clause 155515.
omit compatible in
private theorem sound812 : C.clause (decodeClause atoms clause812) := by
  exact C.covered_clause _ _ (C.packet_clause 4 8 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 814: packet; source clause 155554.
omit compatible in
private theorem sound813 : C.clause (decodeClause atoms clause813) := by
  exact C.covered_clause _ _ (C.packet_clause 8 4 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 815: packet; source clause 155559.
omit compatible in
private theorem sound814 : C.clause (decodeClause atoms clause814) := by
  exact C.covered_clause _ _ (C.packet_clause 8 4 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 816: packet; source clause 155572.
omit compatible in
private theorem sound815 : C.clause (decodeClause atoms clause815) := by
  exact C.covered_clause _ _ (C.packet_clause 8 9 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 817: packet; source clause 155577.
omit compatible in
private theorem sound816 : C.clause (decodeClause atoms clause816) := by
  exact C.covered_clause _ _ (C.packet_clause 8 9 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 818: convex_four; source clause 155713.
omit compatible in
private theorem sound817 : C.clause (decodeClause atoms clause817) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 819: packet; source clause 155848.
omit compatible in
private theorem sound818 : C.clause (decodeClause atoms clause818) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 820: convex_four; source clause 155918.
omit compatible in
private theorem sound819 : C.clause (decodeClause atoms clause819) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 821: packet; source clause 155944.
omit compatible in
private theorem sound820 : C.clause (decodeClause atoms clause820) := by
  exact C.covered_clause _ _ (C.packet_clause 4 10 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 822: packet; source clause 155946.
omit compatible in
private theorem sound821 : C.clause (decodeClause atoms clause821) := by
  exact C.covered_clause _ _ (C.packet_clause 4 10 12 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 823: packet; source clause 155971.
omit compatible in
private theorem sound822 : C.clause (decodeClause atoms clause822) := by
  exact C.covered_clause _ _ (C.packet_clause 8 4 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 824: packet; source clause 155990.
omit compatible in
private theorem sound823 : C.clause (decodeClause atoms clause823) := by
  exact C.covered_clause _ _ (C.packet_clause 8 10 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 825: packet; source clause 155992.
omit compatible in
private theorem sound824 : C.clause (decodeClause atoms clause824) := by
  exact C.covered_clause _ _ (C.packet_clause 8 10 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 826: packet; source clause 155995.
omit compatible in
private theorem sound825 : C.clause (decodeClause atoms clause825) := by
  exact C.covered_clause _ _ (C.packet_clause 8 10 12 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 827: packet; source clause 155997.
omit compatible in
private theorem sound826 : C.clause (decodeClause atoms clause826) := by
  exact C.covered_clause _ _ (C.packet_clause 8 10 12 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 828: packet; source clause 156033.
omit compatible in
private theorem sound827 : C.clause (decodeClause atoms clause827) := by
  exact C.covered_clause _ _ (C.packet_clause 10 4 12 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 829: packet; source clause 156050.
omit compatible in
private theorem sound828 : C.clause (decodeClause atoms clause828) := by
  exact C.covered_clause _ _ (C.packet_clause 10 12 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 830: convex_four; source clause 156126.
omit compatible in
private theorem sound829 : C.clause (decodeClause atoms clause829) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 831: packet; source clause 156131.
omit compatible in
private theorem sound830 : C.clause (decodeClause atoms clause830) := by
  exact C.covered_clause _ _ (C.packet_clause 4 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 832: packet; source clause 156152.
omit compatible in
private theorem sound831 : C.clause (decodeClause atoms clause831) := by
  exact C.covered_clause _ _ (C.packet_clause 4 11 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 833: packet; source clause 156155.
omit compatible in
private theorem sound832 : C.clause (decodeClause atoms clause832) := by
  exact C.covered_clause _ _ (C.packet_clause 4 11 12 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 834: packet; source clause 156264.
omit compatible in
private theorem sound833 : C.clause (decodeClause atoms clause833) := by
  exact C.covered_clause _ _ (C.packet_clause 11 12 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 835: convex_four; source clause 156326.
omit compatible in
private theorem sound834 : C.clause (decodeClause atoms clause834) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 836: convex_four; source clause 156334.
omit compatible in
private theorem sound835 : C.clause (decodeClause atoms clause835) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 837: packet; source clause 156360.
omit compatible in
private theorem sound836 : C.clause (decodeClause atoms clause836) := by
  exact C.covered_clause _ _ (C.packet_clause 4 10 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 838: convex_four; source clause 156542.
omit compatible in
private theorem sound837 : C.clause (decodeClause atoms clause837) := by
  exact C.covered_clause _ _ (C.convex_clause 4 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 839: packet; source clause 156568.
omit compatible in
private theorem sound838 : C.clause (decodeClause atoms clause838) := by
  exact C.covered_clause _ _ (C.packet_clause 4 10 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 840: packet; source clause 156570.
omit compatible in
private theorem sound839 : C.clause (decodeClause atoms clause839) := by
  exact C.covered_clause _ _ (C.packet_clause 4 10 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 841: packet; source clause 156573.
omit compatible in
private theorem sound840 : C.clause (decodeClause atoms clause840) := by
  exact C.covered_clause _ _ (C.packet_clause 4 10 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 842: packet; source clause 156654.
omit compatible in
private theorem sound841 : C.clause (decodeClause atoms clause841) := by
  exact C.covered_clause _ _ (C.packet_clause 10 4 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 843: packet; source clause 156657.
omit compatible in
private theorem sound842 : C.clause (decodeClause atoms clause842) := by
  exact C.covered_clause _ _ (C.packet_clause 10 4 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 844: packet; source clause 156682.
omit compatible in
private theorem sound843 : C.clause (decodeClause atoms clause843) := by
  exact C.covered_clause _ _ (C.packet_clause 10 12 9 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 845: convex_four; source clause 156750.
omit compatible in
private theorem sound844 : C.clause (decodeClause atoms clause844) := by
  exact C.covered_clause _ _ (C.convex_clause 4 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 846: packet; source clause 156755.
omit compatible in
private theorem sound845 : C.clause (decodeClause atoms clause845) := by
  exact C.covered_clause _ _ (C.packet_clause 4 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 847: packet; source clause 156776.
omit compatible in
private theorem sound846 : C.clause (decodeClause atoms clause846) := by
  exact C.covered_clause _ _ (C.packet_clause 4 11 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 848: packet; source clause 156779.
omit compatible in
private theorem sound847 : C.clause (decodeClause atoms clause847) := by
  exact C.covered_clause _ _ (C.packet_clause 4 11 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 849: packet; source clause 156886.
omit compatible in
private theorem sound848 : C.clause (decodeClause atoms clause848) := by
  exact C.covered_clause _ _ (C.packet_clause 11 12 4 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 850: packet; source clause 156888.
omit compatible in
private theorem sound849 : C.clause (decodeClause atoms clause849) := by
  exact C.covered_clause _ _ (C.packet_clause 11 12 4 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 851: convex_four; source clause 156958.
omit compatible in
private theorem sound850 : C.clause (decodeClause atoms clause850) := by
  exact C.covered_clause _ _ (C.convex_clause 4 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 852: packet; source clause 156962.
omit compatible in
private theorem sound851 : C.clause (decodeClause atoms clause851) := by
  exact C.covered_clause _ _ (C.packet_clause 4 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 853: packet; source clause 156967.
omit compatible in
private theorem sound852 : C.clause (decodeClause atoms clause852) := by
  exact C.covered_clause _ _ (C.packet_clause 4 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 854: packet; source clause 157011.
omit compatible in
private theorem sound853 : C.clause (decodeClause atoms clause853) := by
  exact C.covered_clause _ _ (C.packet_clause 10 4 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 855: packet; source clause 157012.
omit compatible in
private theorem sound854 : C.clause (decodeClause atoms clause854) := by
  exact C.covered_clause _ _ (C.packet_clause 10 4 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 856: packet; source clause 157017.
omit compatible in
private theorem sound855 : C.clause (decodeClause atoms clause855) := by
  exact C.covered_clause _ _ (C.packet_clause 10 4 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 857: packet; source clause 157026.
omit compatible in
private theorem sound856 : C.clause (decodeClause atoms clause856) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 858: packet; source clause 157031.
omit compatible in
private theorem sound857 : C.clause (decodeClause atoms clause857) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 859: packet; source clause 157032.
omit compatible in
private theorem sound858 : C.clause (decodeClause atoms clause858) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 860: packet; source clause 157035.
omit compatible in
private theorem sound859 : C.clause (decodeClause atoms clause859) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 12 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 861: convex_four; source clause 157154.
omit compatible in
private theorem sound860 : C.clause (decodeClause atoms clause860) := by
  exact C.covered_clause _ _ (C.convex_clause 4 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 862: packet; source clause 162386.
omit compatible in
private theorem sound861 : C.clause (decodeClause atoms clause861) := by
  exact C.covered_clause _ _ (C.packet_clause 5 9 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 863: packet; source clause 162389.
omit compatible in
private theorem sound862 : C.clause (decodeClause atoms clause862) := by
  exact C.covered_clause _ _ (C.packet_clause 5 9 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 864: packet; source clause 162470.
omit compatible in
private theorem sound863 : C.clause (decodeClause atoms clause863) := by
  exact C.covered_clause _ _ (C.packet_clause 9 5 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 865: packet; source clause 162473.
omit compatible in
private theorem sound864 : C.clause (decodeClause atoms clause864) := by
  exact C.covered_clause _ _ (C.packet_clause 9 5 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 866: packet; source clause 162520.
omit compatible in
private theorem sound865 : C.clause (decodeClause atoms clause865) := by
  exact C.covered_clause _ _ (C.packet_clause 10 5 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 867: packet; source clause 162523.
omit compatible in
private theorem sound866 : C.clause (decodeClause atoms clause866) := by
  exact C.covered_clause _ _ (C.packet_clause 10 5 9 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 868: packet; source clause 162531.
omit compatible in
private theorem sound867 : C.clause (decodeClause atoms clause867) := by
  exact C.covered_clause _ _ (C.packet_clause 10 8 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 869: packet; source clause 162533.
omit compatible in
private theorem sound868 : C.clause (decodeClause atoms clause868) := by
  exact C.covered_clause _ _ (C.packet_clause 10 8 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 870: packet; source clause 162542.
omit compatible in
private theorem sound869 : C.clause (decodeClause atoms clause869) := by
  exact C.covered_clause _ _ (C.packet_clause 10 8 9 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 871: packet; source clause 162544.
omit compatible in
private theorem sound870 : C.clause (decodeClause atoms clause870) := by
  exact C.covered_clause _ _ (C.packet_clause 10 8 9 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 872: convex_four; source clause 162577.
omit compatible in
private theorem sound871 : C.clause (decodeClause atoms clause871) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 873: packet; source clause 162593.
omit compatible in
private theorem sound872 : C.clause (decodeClause atoms clause872) := by
  exact C.covered_clause _ _ (C.packet_clause 5 8 11 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 874: packet; source clause 162616.
omit compatible in
private theorem sound873 : C.clause (decodeClause atoms clause873) := by
  exact C.covered_clause _ _ (C.packet_clause 5 11 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 875: packet; source clause 162728.
omit compatible in
private theorem sound874 : C.clause (decodeClause atoms clause874) := by
  exact C.covered_clause _ _ (C.packet_clause 11 5 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 876: packet; source clause 162741.
omit compatible in
private theorem sound875 : C.clause (decodeClause atoms clause875) := by
  exact C.covered_clause _ _ (C.packet_clause 11 8 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 877: convex_four; source clause 162785.
omit compatible in
private theorem sound876 : C.clause (decodeClause atoms clause876) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 878: packet; source clause 162790.
omit compatible in
private theorem sound877 : C.clause (decodeClause atoms clause877) := by
  exact C.covered_clause _ _ (C.packet_clause 5 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 879: packet; source clause 162792.
omit compatible in
private theorem sound878 : C.clause (decodeClause atoms clause878) := by
  exact C.covered_clause _ _ (C.packet_clause 5 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 880: packet; source clause 162793.
omit compatible in
private theorem sound879 : C.clause (decodeClause atoms clause879) := by
  exact C.covered_clause _ _ (C.packet_clause 5 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 881: packet; source clause 162795.
omit compatible in
private theorem sound880 : C.clause (decodeClause atoms clause880) := by
  exact C.covered_clause _ _ (C.packet_clause 5 8 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 882: packet; source clause 162824.
omit compatible in
private theorem sound881 : C.clause (decodeClause atoms clause881) := by
  exact C.covered_clause _ _ (C.packet_clause 5 12 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 883: packet; source clause 162968.
omit compatible in
private theorem sound882 : C.clause (decodeClause atoms clause882) := by
  exact C.covered_clause _ _ (C.packet_clause 12 9 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 884: convex_four; source clause 162993.
omit compatible in
private theorem sound883 : C.clause (decodeClause atoms clause883) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 885: packet; source clause 163122.
omit compatible in
private theorem sound884 : C.clause (decodeClause atoms clause884) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 886: packet; source clause 163127.
omit compatible in
private theorem sound885 : C.clause (decodeClause atoms clause885) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 887: packet; source clause 163128.
omit compatible in
private theorem sound886 : C.clause (decodeClause atoms clause886) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 888: packet; source clause 163142.
omit compatible in
private theorem sound887 : C.clause (decodeClause atoms clause887) := by
  exact C.covered_clause _ _ (C.packet_clause 11 5 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 889: convex_four; source clause 163198.
omit compatible in
private theorem sound888 : C.clause (decodeClause atoms clause888) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 890: packet; source clause 163226.
omit compatible in
private theorem sound889 : C.clause (decodeClause atoms clause889) := by
  exact C.covered_clause _ _ (C.packet_clause 5 10 12 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 891: packet; source clause 163270.
omit compatible in
private theorem sound890 : C.clause (decodeClause atoms clause890) := by
  exact C.covered_clause _ _ (C.packet_clause 8 10 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 892: packet; source clause 163272.
omit compatible in
private theorem sound891 : C.clause (decodeClause atoms clause891) := by
  exact C.covered_clause _ _ (C.packet_clause 8 10 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 893: packet; source clause 163275.
omit compatible in
private theorem sound892 : C.clause (decodeClause atoms clause892) := by
  exact C.covered_clause _ _ (C.packet_clause 8 10 12 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 894: packet; source clause 163277.
omit compatible in
private theorem sound893 : C.clause (decodeClause atoms clause893) := by
  exact C.covered_clause _ _ (C.packet_clause 8 10 12 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 895: packet; source clause 163330.
omit compatible in
private theorem sound894 : C.clause (decodeClause atoms clause894) := by
  exact C.covered_clause _ _ (C.packet_clause 10 12 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 896: convex_four; source clause 163402.
omit compatible in
private theorem sound895 : C.clause (decodeClause atoms clause895) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 897: convex_four; source clause 163406.
omit compatible in
private theorem sound896 : C.clause (decodeClause atoms clause896) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 898: packet; source clause 163411.
omit compatible in
private theorem sound897 : C.clause (decodeClause atoms clause897) := by
  exact C.covered_clause _ _ (C.packet_clause 5 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 899: packet; source clause 163412.
omit compatible in
private theorem sound898 : C.clause (decodeClause atoms clause898) := by
  exact C.covered_clause _ _ (C.packet_clause 5 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 900: packet; source clause 163417.
omit compatible in
private theorem sound899 : C.clause (decodeClause atoms clause899) := by
  exact C.covered_clause _ _ (C.packet_clause 5 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 901: packet; source clause 163432.
omit compatible in
private theorem sound900 : C.clause (decodeClause atoms clause900) := by
  exact C.covered_clause _ _ (C.packet_clause 5 11 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 902: packet; source clause 163434.
omit compatible in
private theorem sound901 : C.clause (decodeClause atoms clause901) := by
  exact C.covered_clause _ _ (C.packet_clause 5 11 12 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 903: packet; source clause 163439.
omit compatible in
private theorem sound902 : C.clause (decodeClause atoms clause902) := by
  exact C.covered_clause _ _ (C.packet_clause 5 11 12 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 904: packet; source clause 163544.
omit compatible in
private theorem sound903 : C.clause (decodeClause atoms clause903) := by
  exact C.covered_clause _ _ (C.packet_clause 11 12 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 905: convex_four; source clause 163606.
omit compatible in
private theorem sound904 : C.clause (decodeClause atoms clause904) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 906: convex_four; source clause 163607.
omit compatible in
private theorem sound905 : C.clause (decodeClause atoms clause905) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true) (by decide +kernel)

-- Clause 907: convex_four; source clause 163610.
omit compatible in
private theorem sound906 : C.clause (decodeClause atoms clause906) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 908: convex_four; source clause 163614.
omit compatible in
private theorem sound907 : C.clause (decodeClause atoms clause907) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 909: convex_four; source clause 163615.
omit compatible in
private theorem sound908 : C.clause (decodeClause atoms clause908) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true) (by decide +kernel)

-- Clause 910: packet; source clause 163643.
omit compatible in
private theorem sound909 : C.clause (decodeClause atoms clause909) := by
  exact C.covered_clause _ _ (C.packet_clause 5 10 11 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 911: packet; source clause 163746.
omit compatible in
private theorem sound910 : C.clause (decodeClause atoms clause910) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 912: convex_four; source clause 163814.
omit compatible in
private theorem sound911 : C.clause (decodeClause atoms clause911) := by
  exact C.covered_clause _ _ (C.convex_clause 5 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 913: convex_four; source clause 163822.
omit compatible in
private theorem sound912 : C.clause (decodeClause atoms clause912) := by
  exact C.covered_clause _ _ (C.convex_clause 5 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 914: packet; source clause 163827.
omit compatible in
private theorem sound913 : C.clause (decodeClause atoms clause913) := by
  exact C.covered_clause _ _ (C.packet_clause 5 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 915: packet; source clause 163848.
omit compatible in
private theorem sound914 : C.clause (decodeClause atoms clause914) := by
  exact C.covered_clause _ _ (C.packet_clause 5 10 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 916: packet; source clause 163850.
omit compatible in
private theorem sound915 : C.clause (decodeClause atoms clause915) := by
  exact C.covered_clause _ _ (C.packet_clause 5 10 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 917: packet; source clause 163853.
omit compatible in
private theorem sound916 : C.clause (decodeClause atoms clause916) := by
  exact C.covered_clause _ _ (C.packet_clause 5 10 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 918: packet; source clause 163937.
omit compatible in
private theorem sound917 : C.clause (decodeClause atoms clause917) := by
  exact C.covered_clause _ _ (C.packet_clause 10 5 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 919: packet; source clause 163954.
omit compatible in
private theorem sound918 : C.clause (decodeClause atoms clause918) := by
  exact C.covered_clause _ _ (C.packet_clause 10 12 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 920: convex_four; source clause 164030.
omit compatible in
private theorem sound919 : C.clause (decodeClause atoms clause919) := by
  exact C.covered_clause _ _ (C.convex_clause 5 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 921: packet; source clause 164035.
omit compatible in
private theorem sound920 : C.clause (decodeClause atoms clause920) := by
  exact C.covered_clause _ _ (C.packet_clause 5 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 922: packet; source clause 164056.
omit compatible in
private theorem sound921 : C.clause (decodeClause atoms clause921) := by
  exact C.covered_clause _ _ (C.packet_clause 5 11 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 923: packet; source clause 164168.
omit compatible in
private theorem sound922 : C.clause (decodeClause atoms clause922) := by
  exact C.covered_clause _ _ (C.packet_clause 11 12 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 924: convex_four; source clause 164230.
omit compatible in
private theorem sound923 : C.clause (decodeClause atoms clause923) := by
  exact C.covered_clause _ _ (C.convex_clause 5 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 925: convex_four; source clause 164234.
omit compatible in
private theorem sound924 : C.clause (decodeClause atoms clause924) := by
  exact C.covered_clause _ _ (C.convex_clause 5 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 926: convex_four; source clause 164238.
omit compatible in
private theorem sound925 : C.clause (decodeClause atoms clause925) := by
  exact C.covered_clause _ _ (C.convex_clause 5 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 927: convex_four; source clause 164240.
omit compatible in
private theorem sound926 : C.clause (decodeClause atoms clause926) := by
  exact C.covered_clause _ _ (C.convex_clause 5 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true false) (by decide +kernel)

-- Clause 928: packet; source clause 164242.
omit compatible in
private theorem sound927 : C.clause (decodeClause atoms clause927) := by
  exact C.covered_clause _ _ (C.packet_clause 5 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 929: packet; source clause 164247.
omit compatible in
private theorem sound928 : C.clause (decodeClause atoms clause928) := by
  exact C.covered_clause _ _ (C.packet_clause 5 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 930: packet; source clause 164291.
omit compatible in
private theorem sound929 : C.clause (decodeClause atoms clause929) := by
  exact C.covered_clause _ _ (C.packet_clause 10 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 931: packet; source clause 164292.
omit compatible in
private theorem sound930 : C.clause (decodeClause atoms clause930) := by
  exact C.covered_clause _ _ (C.packet_clause 10 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 932: packet; source clause 164297.
omit compatible in
private theorem sound931 : C.clause (decodeClause atoms clause931) := by
  exact C.covered_clause _ _ (C.packet_clause 10 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 933: packet; source clause 164306.
omit compatible in
private theorem sound932 : C.clause (decodeClause atoms clause932) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 934: packet; source clause 164311.
omit compatible in
private theorem sound933 : C.clause (decodeClause atoms clause933) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 935: packet; source clause 164312.
omit compatible in
private theorem sound934 : C.clause (decodeClause atoms clause934) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 936: packet; source clause 164316.
omit compatible in
private theorem sound935 : C.clause (decodeClause atoms clause935) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 12 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 937: convex_four; source clause 164434.
omit compatible in
private theorem sound936 : C.clause (decodeClause atoms clause936) := by
  exact C.covered_clause _ _ (C.convex_clause 5 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 938: packet; source clause 165942.
omit compatible in
private theorem sound937 : C.clause (decodeClause atoms clause937) := by
  exact C.covered_clause _ _ (C.packet_clause 6 11 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 939: packet; source clause 165949.
omit compatible in
private theorem sound938 : C.clause (decodeClause atoms clause938) := by
  exact C.covered_clause _ _ (C.packet_clause 6 11 10 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 940: packet; source clause 166053.
omit compatible in
private theorem sound939 : C.clause (decodeClause atoms clause939) := by
  exact C.covered_clause _ _ (C.packet_clause 11 6 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 941: packet; source clause 166062.
omit compatible in
private theorem sound940 : C.clause (decodeClause atoms clause940) := by
  exact C.covered_clause _ _ (C.packet_clause 11 6 10 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 942: convex_four; source clause 166101.
omit compatible in
private theorem sound941 : C.clause (decodeClause atoms clause941) := by
  exact C.covered_clause _ _ (C.convex_clause 6 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 943: packet; source clause 166139.
omit compatible in
private theorem sound942 : C.clause (decodeClause atoms clause942) := by
  exact C.covered_clause _ _ (C.packet_clause 6 10 12 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 944: packet; source clause 166141.
omit compatible in
private theorem sound943 : C.clause (decodeClause atoms clause943) := by
  exact C.covered_clause _ _ (C.packet_clause 6 10 12 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 945: packet; source clause 166342.
omit compatible in
private theorem sound944 : C.clause (decodeClause atoms clause944) := by
  exact C.covered_clause _ _ (C.packet_clause 6 11 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 946: packet; source clause 166344.
omit compatible in
private theorem sound945 : C.clause (decodeClause atoms clause945) := by
  exact C.covered_clause _ _ (C.packet_clause 6 11 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 947: packet; source clause 168402.
omit compatible in
private theorem sound946 : C.clause (decodeClause atoms clause946) := by
  exact C.covered_clause _ _ (C.packet_clause 6 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 948: packet; source clause 168407.
omit compatible in
private theorem sound947 : C.clause (decodeClause atoms clause947) := by
  exact C.covered_clause _ _ (C.packet_clause 6 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 949: packet; source clause 168420.
omit compatible in
private theorem sound948 : C.clause (decodeClause atoms clause948) := by
  exact C.covered_clause _ _ (C.packet_clause 6 11 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 950: packet; source clause 168422.
omit compatible in
private theorem sound949 : C.clause (decodeClause atoms clause949) := by
  exact C.covered_clause _ _ (C.packet_clause 6 11 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 951: packet; source clause 168425.
omit compatible in
private theorem sound950 : C.clause (decodeClause atoms clause950) := by
  exact C.covered_clause _ _ (C.packet_clause 6 11 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 952: packet; source clause 168498.
omit compatible in
private theorem sound951 : C.clause (decodeClause atoms clause951) := by
  exact C.covered_clause _ _ (C.packet_clause 11 6 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 953: packet; source clause 168501.
omit compatible in
private theorem sound952 : C.clause (decodeClause atoms clause952) := by
  exact C.covered_clause _ _ (C.packet_clause 11 6 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 954: packet; source clause 168503.
omit compatible in
private theorem sound953 : C.clause (decodeClause atoms clause953) := by
  exact C.covered_clause _ _ (C.packet_clause 11 6 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 955: packet; source clause 170557.
omit compatible in
private theorem sound954 : C.clause (decodeClause atoms clause954) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 12 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 956: packet; source clause 170606.
omit compatible in
private theorem sound955 : C.clause (decodeClause atoms clause955) := by
  exact C.covered_clause _ _ (C.packet_clause 11 10 12 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 957: packet; source clause 170608.
omit compatible in
private theorem sound956 : C.clause (decodeClause atoms clause956) := by
  exact C.covered_clause _ _ (C.packet_clause 11 10 12 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 958: packet; source clause 170697.
omit compatible in
private theorem sound957 : C.clause (decodeClause atoms clause957) := by
  exact C.covered_clause _ _ (C.packet_clause 8 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 959: packet; source clause 170818.
omit compatible in
private theorem sound958 : C.clause (decodeClause atoms clause958) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 960: packet; source clause 170823.
omit compatible in
private theorem sound959 : C.clause (decodeClause atoms clause959) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 961: packet; source clause 170824.
omit compatible in
private theorem sound960 : C.clause (decodeClause atoms clause960) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 962: convex_four; source clause 170894.
omit compatible in
private theorem sound961 : C.clause (decodeClause atoms clause961) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 963: packet; source clause 170966.
omit compatible in
private theorem sound962 : C.clause (decodeClause atoms clause962) := by
  exact C.covered_clause _ _ (C.packet_clause 9 10 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 964: packet; source clause 170973.
omit compatible in
private theorem sound963 : C.clause (decodeClause atoms clause963) := by
  exact C.covered_clause _ _ (C.packet_clause 9 10 12 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 965: packet; source clause 171013.
omit compatible in
private theorem sound964 : C.clause (decodeClause atoms clause964) := by
  exact C.covered_clause _ _ (C.packet_clause 10 9 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 966: packet; source clause 171022.
omit compatible in
private theorem sound965 : C.clause (decodeClause atoms clause965) := by
  exact C.covered_clause _ _ (C.packet_clause 10 9 12 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 967: convex_four; source clause 171102.
omit compatible in
private theorem sound966 : C.clause (decodeClause atoms clause966) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 968: packet; source clause 171107.
omit compatible in
private theorem sound967 : C.clause (decodeClause atoms clause967) := by
  exact C.covered_clause _ _ (C.packet_clause 8 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 969: packet; source clause 171128.
omit compatible in
private theorem sound968 : C.clause (decodeClause atoms clause968) := by
  exact C.covered_clause _ _ (C.packet_clause 8 11 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 970: packet; source clause 171174.
omit compatible in
private theorem sound969 : C.clause (decodeClause atoms clause969) := by
  exact C.covered_clause _ _ (C.packet_clause 9 11 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 971: packet; source clause 171240.
omit compatible in
private theorem sound970 : C.clause (decodeClause atoms clause970) := by
  exact C.covered_clause _ _ (C.packet_clause 11 12 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 972: convex_four; source clause 171302.
omit compatible in
private theorem sound971 : C.clause (decodeClause atoms clause971) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 973: convex_four; source clause 171310.
omit compatible in
private theorem sound972 : C.clause (decodeClause atoms clause972) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 974: packet; source clause 171314.
omit compatible in
private theorem sound973 : C.clause (decodeClause atoms clause973) := by
  exact C.covered_clause _ _ (C.packet_clause 8 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 975: packet; source clause 171319.
omit compatible in
private theorem sound974 : C.clause (decodeClause atoms clause974) := by
  exact C.covered_clause _ _ (C.packet_clause 8 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 976: packet; source clause 171363.
omit compatible in
private theorem sound975 : C.clause (decodeClause atoms clause975) := by
  exact C.covered_clause _ _ (C.packet_clause 10 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 977: packet; source clause 171364.
omit compatible in
private theorem sound976 : C.clause (decodeClause atoms clause976) := by
  exact C.covered_clause _ _ (C.packet_clause 10 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 978: packet; source clause 171369.
omit compatible in
private theorem sound977 : C.clause (decodeClause atoms clause977) := by
  exact C.covered_clause _ _ (C.packet_clause 10 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 979: packet; source clause 171378.
omit compatible in
private theorem sound978 : C.clause (decodeClause atoms clause978) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 980: packet; source clause 171384.
omit compatible in
private theorem sound979 : C.clause (decodeClause atoms clause979) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 981: packet; source clause 171387.
omit compatible in
private theorem sound980 : C.clause (decodeClause atoms clause980) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 12 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 982: convex_four; source clause 171506.
omit compatible in
private theorem sound981 : C.clause (decodeClause atoms clause981) := by
  exact C.covered_clause _ _ (C.convex_clause 8 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 983: packet; source clause 171571.
omit compatible in
private theorem sound982 : C.clause (decodeClause atoms clause982) := by
  exact C.covered_clause _ _ (C.packet_clause 10 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 984: packet; source clause 171592.
omit compatible in
private theorem sound983 : C.clause (decodeClause atoms clause983) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 985: packet; source clause 171595.
omit compatible in
private theorem sound984 : C.clause (decodeClause atoms clause984) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 12 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 986: convex_four; source clause 171714.
omit compatible in
private theorem sound985 : C.clause (decodeClause atoms clause985) := by
  exact C.covered_clause _ _ (C.convex_clause 9 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 987: no_octagon; source clause 171734.
omit compatible in
private theorem sound986 : C.clause (decodeClause atoms clause986) := by
  exact C.no_octagon_clause {0, 1, 2, 3, 6, 7, 10, 11} (by decide +kernel) _ (by decide +kernel)

-- Clause 988: no_octagon; source clause 171755.
omit compatible in
private theorem sound987 : C.clause (decodeClause atoms clause987) := by
  exact C.no_octagon_clause {2, 4, 5, 8, 9, 10, 11, 12} (by decide +kernel) _ (by decide +kernel)

-- Clause 989: empty_direction; source clause 29.
private theorem sound988 : C.clause (decodeClause atoms clause988) := by
  exact C.covered_clause _ _ (C.empty_clause 1 0 (by decide) (compatible.1 (1, 0) (by decide +kernel))) (by decide +kernel)

-- Clause 990: empty_direction; source clause 3051.
private theorem sound989 : C.clause (decodeClause atoms clause989) := by
  exact C.covered_clause _ _ (C.empty_clause 10 6 (by decide) (compatible.1 (10, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 991: domain; source clause 3811.
private theorem sound990 : C.clause (decodeClause atoms clause990) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 2 4 (compatible.2.1 (10, 11, 2, 4) (by decide +kernel))) (by decide +kernel)

-- Clause 992: domain; source clause 3812.
private theorem sound991 : C.clause (decodeClause atoms clause991) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 2 5 (compatible.2.1 (10, 11, 2, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 993: domain; source clause 3813.
private theorem sound992 : C.clause (decodeClause atoms clause992) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 2 6 (compatible.2.1 (10, 11, 2, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 994: domain; source clause 3816.
private theorem sound993 : C.clause (decodeClause atoms clause993) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 3 4 (compatible.2.1 (10, 11, 3, 4) (by decide +kernel))) (by decide +kernel)

-- Clause 995: domain; source clause 3817.
private theorem sound994 : C.clause (decodeClause atoms clause994) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 3 5 (compatible.2.1 (10, 11, 3, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 996: domain; source clause 3818.
private theorem sound995 : C.clause (decodeClause atoms clause995) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 3 6 (compatible.2.1 (10, 11, 3, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 997: empty_direction; source clause 3876.
private theorem sound996 : C.clause (decodeClause atoms clause996) := by
  exact C.covered_clause _ _ (C.empty_clause 12 10 (by decide) (compatible.1 (12, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 998: empty_direction; source clause 3929.
private theorem sound997 : C.clause (decodeClause atoms clause997) := by
  exact C.covered_clause _ _ (C.empty_clause 12 11 (by decide) (compatible.1 (12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 999: fixed_sign; source clause 22830.
private theorem sound998 : C.clause (decodeClause atoms clause998) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 2 (by decide) (by decide) (by decide) (compatible.2.2 (0, 1, 2) (by decide +kernel))) (by decide +kernel)

-- Clause 1000: fixed_sign; source clause 22833.
private theorem sound999 : C.clause (decodeClause atoms clause999) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 7 (by decide) (by decide) (by decide) (compatible.2.2 (0, 1, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 1001: fixed_sign; source clause 22857.
private theorem sound1000 : C.clause (decodeClause atoms clause1000) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 7 11 (by decide) (by decide) (by decide) (compatible.2.2 (0, 11, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 1002: fixed_sign; source clause 22862.
private theorem sound1001 : C.clause (decodeClause atoms clause1001) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 3 (by decide) (by decide) (by decide) (compatible.2.2 (1, 2, 3) (by decide +kernel))) (by decide +kernel)

-- Clause 1003: fixed_sign; source clause 22865.
private theorem sound1002 : C.clause (decodeClause atoms clause1002) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 7 (by decide) (by decide) (by decide) (compatible.2.2 (1, 2, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 1004: fixed_sign; source clause 22890.
private theorem sound1003 : C.clause (decodeClause atoms clause1003) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 7 11 (by decide) (by decide) (by decide) (compatible.2.2 (1, 11, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 1005: fixed_sign; source clause 22899.
private theorem sound1004 : C.clause (decodeClause atoms clause1004) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 11 12 (by decide) (by decide) (by decide) (compatible.2.2 (1, 12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 1006: fixed_sign; source clause 22902.
private theorem sound1005 : C.clause (decodeClause atoms clause1005) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 3 6 (by decide) (by decide) (by decide) (compatible.2.2 (2, 3, 6) (by decide +kernel))) (by decide +kernel)

-- Clause 1007: fixed_sign; source clause 22903.
private theorem sound1006 : C.clause (decodeClause atoms clause1006) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 3 7 (by decide) (by decide) (by decide) (compatible.2.2 (2, 3, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 1008: fixed_sign; source clause 22905.
private theorem sound1007 : C.clause (decodeClause atoms clause1007) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 5 (by decide) (by decide) (by decide) (compatible.2.2 (2, 4, 5) (by decide +kernel))) (by decide +kernel)

-- Clause 1009: fixed_sign; source clause 22909.
private theorem sound1008 : C.clause (decodeClause atoms clause1008) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 10 (by decide) (by decide) (by decide) (compatible.2.2 (2, 4, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 1010: fixed_sign; source clause 22923.
private theorem sound1009 : C.clause (decodeClause atoms clause1009) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 7 11 (by decide) (by decide) (by decide) (compatible.2.2 (2, 11, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 1011: fixed_sign; source clause 22940.
private theorem sound1010 : C.clause (decodeClause atoms clause1010) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 6 7 (by decide) (by decide) (by decide) (compatible.2.2 (3, 6, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 1012: fixed_sign; source clause 22943.
private theorem sound1011 : C.clause (decodeClause atoms clause1011) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 6 10 (by decide) (by decide) (by decide) (compatible.2.2 (3, 6, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 1013: fixed_sign; source clause 22945.
private theorem sound1012 : C.clause (decodeClause atoms clause1012) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 7 11 (by decide) (by decide) (by decide) (compatible.2.2 (3, 11, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 1014: fixed_sign; source clause 22957.
private theorem sound1013 : C.clause (decodeClause atoms clause1013) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 5 8 (by decide) (by decide) (by decide) (compatible.2.2 (4, 5, 8) (by decide +kernel))) (by decide +kernel)

-- Clause 1015: fixed_sign; source clause 22959.
private theorem sound1014 : C.clause (decodeClause atoms clause1014) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 5 10 (by decide) (by decide) (by decide) (compatible.2.2 (4, 5, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 1016: fixed_sign; source clause 22974.
private theorem sound1015 : C.clause (decodeClause atoms clause1015) := by
  exact C.covered_clause _ _ (C.fixed_negative 4 10 12 (by decide) (by decide) (by decide) (compatible.2.2 (4, 12, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 1017: fixed_sign; source clause 22981.
private theorem sound1016 : C.clause (decodeClause atoms clause1016) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 8 9 (by decide) (by decide) (by decide) (compatible.2.2 (5, 8, 9) (by decide +kernel))) (by decide +kernel)

-- Clause 1018: fixed_sign; source clause 22982.
private theorem sound1017 : C.clause (decodeClause atoms clause1017) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 8 10 (by decide) (by decide) (by decide) (compatible.2.2 (5, 8, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 1019: fixed_sign; source clause 22988.
private theorem sound1018 : C.clause (decodeClause atoms clause1018) := by
  exact C.covered_clause _ _ (C.fixed_negative 5 10 12 (by decide) (by decide) (by decide) (compatible.2.2 (5, 12, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 1020: fixed_sign; source clause 22990.
private theorem sound1019 : C.clause (decodeClause atoms clause1019) := by
  exact C.covered_clause _ _ (C.fixed_negative 6 7 10 (by decide) (by decide) (by decide) (compatible.2.2 (6, 10, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 1021: fixed_sign; source clause 22991.
private theorem sound1020 : C.clause (decodeClause atoms clause1020) := by
  exact C.covered_clause _ _ (C.fixed_negative 6 7 11 (by decide) (by decide) (by decide) (compatible.2.2 (6, 11, 7) (by decide +kernel))) (by decide +kernel)

-- Clause 1022: fixed_sign; source clause 22996.
private theorem sound1021 : C.clause (decodeClause atoms clause1021) := by
  exact C.covered_clause _ _ (C.fixed_negative 6 10 12 (by decide) (by decide) (by decide) (compatible.2.2 (6, 12, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 1023: fixed_sign; source clause 23001.
private theorem sound1022 : C.clause (decodeClause atoms clause1022) := by
  exact C.covered_clause _ _ (C.fixed_positive 7 10 11 (by decide) (by decide) (by decide) (compatible.2.2 (7, 10, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 1024: fixed_sign; source clause 23002.
private theorem sound1023 : C.clause (decodeClause atoms clause1023) := by
  exact C.covered_clause _ _ (C.fixed_positive 8 9 10 (by decide) (by decide) (by decide) (compatible.2.2 (8, 9, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 1025: fixed_sign; source clause 23004.
private theorem sound1024 : C.clause (decodeClause atoms clause1024) := by
  exact C.covered_clause _ _ (C.fixed_positive 8 9 12 (by decide) (by decide) (by decide) (compatible.2.2 (8, 9, 12) (by decide +kernel))) (by decide +kernel)

-- Clause 1026: fixed_sign; source clause 23005.
private theorem sound1025 : C.clause (decodeClause atoms clause1025) := by
  exact C.covered_clause _ _ (C.fixed_negative 8 10 12 (by decide) (by decide) (by decide) (compatible.2.2 (8, 12, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 1027: fixed_sign; source clause 23007.
private theorem sound1026 : C.clause (decodeClause atoms clause1026) := by
  exact C.covered_clause _ _ (C.fixed_negative 9 10 12 (by decide) (by decide) (by decide) (compatible.2.2 (9, 12, 10) (by decide +kernel))) (by decide +kernel)

-- Clause 1028: fixed_sign; source clause 23008.
private theorem sound1027 : C.clause (decodeClause atoms clause1027) := by
  exact C.covered_clause _ _ (C.fixed_negative 9 11 12 (by decide) (by decide) (by decide) (compatible.2.2 (9, 12, 11) (by decide +kernel))) (by decide +kernel)

-- Clause 1029: fixed_sign; source clause 23009.
private theorem sound1028 : C.clause (decodeClause atoms clause1028) := by
  exact C.covered_clause _ _ (C.fixed_negative 10 11 12 (by decide) (by decide) (by decide) (compatible.2.2 (10, 12, 11) (by decide +kernel))) (by decide +kernel)

private theorem all_sound : List.Forall (fun cl => C.clause (decodeClause atoms cl)) clauses := by
  exact And.intro (sound000 C) (And.intro (sound001 C) (And.intro (sound002 C) (And.intro (sound003 C) (And.intro (sound004 C) (And.intro (sound005 C) (And.intro (sound006 C) (And.intro (sound007 C) (And.intro (sound008 C) (And.intro (sound009 C) (And.intro (sound010 C) (And.intro (sound011 C) (And.intro (sound012 C) (And.intro (sound013 C) (And.intro (sound014 C) (And.intro (sound015 C) (And.intro (sound016 C) (And.intro (sound017 C) (And.intro (sound018 C) (And.intro (sound019 C) (And.intro (sound020 C) (And.intro (sound021 C) (And.intro (sound022 C) (And.intro (sound023 C) (And.intro (sound024 C) (And.intro (sound025 C) (And.intro (sound026 C) (And.intro (sound027 C) (And.intro (sound028 C) (And.intro (sound029 C) (And.intro (sound030 C) (And.intro (sound031 C) (And.intro (sound032 C) (And.intro (sound033 C) (And.intro (sound034 C) (And.intro (sound035 C) (And.intro (sound036 C) (And.intro (sound037 C) (And.intro (sound038 C) (And.intro (sound039 C) (And.intro (sound040 C) (And.intro (sound041 C) (And.intro (sound042 C) (And.intro (sound043 C) (And.intro (sound044 C) (And.intro (sound045 C) (And.intro (sound046 C) (And.intro (sound047 C) (And.intro (sound048 C) (And.intro (sound049 C) (And.intro (sound050 C) (And.intro (sound051 C) (And.intro (sound052 C) (And.intro (sound053 C) (And.intro (sound054 C) (And.intro (sound055 C) (And.intro (sound056 C) (And.intro (sound057 C) (And.intro (sound058 C) (And.intro (sound059 C) (And.intro (sound060 C) (And.intro (sound061 C) (And.intro (sound062 C) (And.intro (sound063 C) (And.intro (sound064 C) (And.intro (sound065 C) (And.intro (sound066 C) (And.intro (sound067 C) (And.intro (sound068 C) (And.intro (sound069 C) (And.intro (sound070 C) (And.intro (sound071 C) (And.intro (sound072 C) (And.intro (sound073 C) (And.intro (sound074 C) (And.intro (sound075 C) (And.intro (sound076 C) (And.intro (sound077 C) (And.intro (sound078 C) (And.intro (sound079 C) (And.intro (sound080 C) (And.intro (sound081 C) (And.intro (sound082 C) (And.intro (sound083 C) (And.intro (sound084 C) (And.intro (sound085 C) (And.intro (sound086 C) (And.intro (sound087 C) (And.intro (sound088 C) (And.intro (sound089 C) (And.intro (sound090 C) (And.intro (sound091 C) (And.intro (sound092 C) (And.intro (sound093 C) (And.intro (sound094 C) (And.intro (sound095 C) (And.intro (sound096 C) (And.intro (sound097 C) (And.intro (sound098 C) (And.intro (sound099 C) (And.intro (sound100 C) (And.intro (sound101 C) (And.intro (sound102 C) (And.intro (sound103 C) (And.intro (sound104 C) (And.intro (sound105 C) (And.intro (sound106 C) (And.intro (sound107 C) (And.intro (sound108 C) (And.intro (sound109 C) (And.intro (sound110 C) (And.intro (sound111 C) (And.intro (sound112 C) (And.intro (sound113 C) (And.intro (sound114 C) (And.intro (sound115 C) (And.intro (sound116 C) (And.intro (sound117 C) (And.intro (sound118 C) (And.intro (sound119 C) (And.intro (sound120 C) (And.intro (sound121 C) (And.intro (sound122 C) (And.intro (sound123 C) (And.intro (sound124 C) (And.intro (sound125 C) (And.intro (sound126 C) (And.intro (sound127 C) (And.intro (sound128 C) (And.intro (sound129 C) (And.intro (sound130 C) (And.intro (sound131 C) (And.intro (sound132 C) (And.intro (sound133 C) (And.intro (sound134 C) (And.intro (sound135 C) (And.intro (sound136 C) (And.intro (sound137 C) (And.intro (sound138 C) (And.intro (sound139 C) (And.intro (sound140 C) (And.intro (sound141 C) (And.intro (sound142 C) (And.intro (sound143 C) (And.intro (sound144 C) (And.intro (sound145 C) (And.intro (sound146 C) (And.intro (sound147 C) (And.intro (sound148 C) (And.intro (sound149 C) (And.intro (sound150 C) (And.intro (sound151 C) (And.intro (sound152 C) (And.intro (sound153 C) (And.intro (sound154 C) (And.intro (sound155 C) (And.intro (sound156 C) (And.intro (sound157 C) (And.intro (sound158 C) (And.intro (sound159 C) (And.intro (sound160 C) (And.intro (sound161 C) (And.intro (sound162 C) (And.intro (sound163 C) (And.intro (sound164 C) (And.intro (sound165 C) (And.intro (sound166 C) (And.intro (sound167 C) (And.intro (sound168 C) (And.intro (sound169 C) (And.intro (sound170 C) (And.intro (sound171 C) (And.intro (sound172 C) (And.intro (sound173 C) (And.intro (sound174 C) (And.intro (sound175 C) (And.intro (sound176 C) (And.intro (sound177 C) (And.intro (sound178 C) (And.intro (sound179 C) (And.intro (sound180 C) (And.intro (sound181 C) (And.intro (sound182 C) (And.intro (sound183 C) (And.intro (sound184 C) (And.intro (sound185 C) (And.intro (sound186 C) (And.intro (sound187 C) (And.intro (sound188 C) (And.intro (sound189 C) (And.intro (sound190 C) (And.intro (sound191 C) (And.intro (sound192 C) (And.intro (sound193 C) (And.intro (sound194 C) (And.intro (sound195 C) (And.intro (sound196 C) (And.intro (sound197 C) (And.intro (sound198 C) (And.intro (sound199 C) (And.intro (sound200 C) (And.intro (sound201 C) (And.intro (sound202 C) (And.intro (sound203 C) (And.intro (sound204 C) (And.intro (sound205 C) (And.intro (sound206 C) (And.intro (sound207 C) (And.intro (sound208 C) (And.intro (sound209 C) (And.intro (sound210 C) (And.intro (sound211 C) (And.intro (sound212 C) (And.intro (sound213 C) (And.intro (sound214 C) (And.intro (sound215 C) (And.intro (sound216 C) (And.intro (sound217 C) (And.intro (sound218 C) (And.intro (sound219 C) (And.intro (sound220 C) (And.intro (sound221 C) (And.intro (sound222 C) (And.intro (sound223 C) (And.intro (sound224 C) (And.intro (sound225 C) (And.intro (sound226 C) (And.intro (sound227 C) (And.intro (sound228 C) (And.intro (sound229 C) (And.intro (sound230 C) (And.intro (sound231 C) (And.intro (sound232 C) (And.intro (sound233 C) (And.intro (sound234 C) (And.intro (sound235 C) (And.intro (sound236 C) (And.intro (sound237 C) (And.intro (sound238 C) (And.intro (sound239 C) (And.intro (sound240 C) (And.intro (sound241 C) (And.intro (sound242 C) (And.intro (sound243 C) (And.intro (sound244 C) (And.intro (sound245 C) (And.intro (sound246 C) (And.intro (sound247 C) (And.intro (sound248 C) (And.intro (sound249 C) (And.intro (sound250 C) (And.intro (sound251 C) (And.intro (sound252 C) (And.intro (sound253 C) (And.intro (sound254 C) (And.intro (sound255 C) (And.intro (sound256 C) (And.intro (sound257 C) (And.intro (sound258 C) (And.intro (sound259 C) (And.intro (sound260 C) (And.intro (sound261 C) (And.intro (sound262 C) (And.intro (sound263 C) (And.intro (sound264 C) (And.intro (sound265 C) (And.intro (sound266 C) (And.intro (sound267 C) (And.intro (sound268 C) (And.intro (sound269 C) (And.intro (sound270 C) (And.intro (sound271 C) (And.intro (sound272 C) (And.intro (sound273 C) (And.intro (sound274 C) (And.intro (sound275 C) (And.intro (sound276 C) (And.intro (sound277 C) (And.intro (sound278 C) (And.intro (sound279 C) (And.intro (sound280 C) (And.intro (sound281 C) (And.intro (sound282 C) (And.intro (sound283 C) (And.intro (sound284 C) (And.intro (sound285 C) (And.intro (sound286 C) (And.intro (sound287 C) (And.intro (sound288 C) (And.intro (sound289 C) (And.intro (sound290 C) (And.intro (sound291 C) (And.intro (sound292 C) (And.intro (sound293 C) (And.intro (sound294 C) (And.intro (sound295 C) (And.intro (sound296 C) (And.intro (sound297 C) (And.intro (sound298 C) (And.intro (sound299 C) (And.intro (sound300 C) (And.intro (sound301 C) (And.intro (sound302 C) (And.intro (sound303 C) (And.intro (sound304 C) (And.intro (sound305 C) (And.intro (sound306 C) (And.intro (sound307 C) (And.intro (sound308 C) (And.intro (sound309 C) (And.intro (sound310 C) (And.intro (sound311 C) (And.intro (sound312 C) (And.intro (sound313 C) (And.intro (sound314 C) (And.intro (sound315 C) (And.intro (sound316 C) (And.intro (sound317 C) (And.intro (sound318 C) (And.intro (sound319 C) (And.intro (sound320 C) (And.intro (sound321 C) (And.intro (sound322 C) (And.intro (sound323 C) (And.intro (sound324 C) (And.intro (sound325 C) (And.intro (sound326 C) (And.intro (sound327 C) (And.intro (sound328 C) (And.intro (sound329 C) (And.intro (sound330 C) (And.intro (sound331 C) (And.intro (sound332 C) (And.intro (sound333 C) (And.intro (sound334 C) (And.intro (sound335 C) (And.intro (sound336 C) (And.intro (sound337 C) (And.intro (sound338 C) (And.intro (sound339 C) (And.intro (sound340 C) (And.intro (sound341 C) (And.intro (sound342 C) (And.intro (sound343 C) (And.intro (sound344 C) (And.intro (sound345 C) (And.intro (sound346 C) (And.intro (sound347 C) (And.intro (sound348 C) (And.intro (sound349 C) (And.intro (sound350 C) (And.intro (sound351 C) (And.intro (sound352 C) (And.intro (sound353 C) (And.intro (sound354 C) (And.intro (sound355 C) (And.intro (sound356 C) (And.intro (sound357 C) (And.intro (sound358 C) (And.intro (sound359 C) (And.intro (sound360 C) (And.intro (sound361 C) (And.intro (sound362 C) (And.intro (sound363 C) (And.intro (sound364 C) (And.intro (sound365 C) (And.intro (sound366 C) (And.intro (sound367 C) (And.intro (sound368 C) (And.intro (sound369 C) (And.intro (sound370 C) (And.intro (sound371 C) (And.intro (sound372 C) (And.intro (sound373 C) (And.intro (sound374 C) (And.intro (sound375 C) (And.intro (sound376 C) (And.intro (sound377 C) (And.intro (sound378 C) (And.intro (sound379 C) (And.intro (sound380 C) (And.intro (sound381 C) (And.intro (sound382 C) (And.intro (sound383 C) (And.intro (sound384 C) (And.intro (sound385 C) (And.intro (sound386 C) (And.intro (sound387 C) (And.intro (sound388 C) (And.intro (sound389 C) (And.intro (sound390 C) (And.intro (sound391 C) (And.intro (sound392 C) (And.intro (sound393 C) (And.intro (sound394 C) (And.intro (sound395 C) (And.intro (sound396 C) (And.intro (sound397 C) (And.intro (sound398 C) (And.intro (sound399 C) (And.intro (sound400 C) (And.intro (sound401 C) (And.intro (sound402 C) (And.intro (sound403 C) (And.intro (sound404 C) (And.intro (sound405 C) (And.intro (sound406 C) (And.intro (sound407 C) (And.intro (sound408 C) (And.intro (sound409 C) (And.intro (sound410 C) (And.intro (sound411 C) (And.intro (sound412 C) (And.intro (sound413 C) (And.intro (sound414 C) (And.intro (sound415 C) (And.intro (sound416 C) (And.intro (sound417 C) (And.intro (sound418 C) (And.intro (sound419 C) (And.intro (sound420 C) (And.intro (sound421 C) (And.intro (sound422 C) (And.intro (sound423 C) (And.intro (sound424 C) (And.intro (sound425 C) (And.intro (sound426 C) (And.intro (sound427 C) (And.intro (sound428 C) (And.intro (sound429 C) (And.intro (sound430 C) (And.intro (sound431 C) (And.intro (sound432 C) (And.intro (sound433 C) (And.intro (sound434 C) (And.intro (sound435 C) (And.intro (sound436 C) (And.intro (sound437 C) (And.intro (sound438 C) (And.intro (sound439 C) (And.intro (sound440 C) (And.intro (sound441 C) (And.intro (sound442 C) (And.intro (sound443 C) (And.intro (sound444 C) (And.intro (sound445 C) (And.intro (sound446 C) (And.intro (sound447 C) (And.intro (sound448 C) (And.intro (sound449 C) (And.intro (sound450 C) (And.intro (sound451 C) (And.intro (sound452 C) (And.intro (sound453 C) (And.intro (sound454 C) (And.intro (sound455 C) (And.intro (sound456 C) (And.intro (sound457 C) (And.intro (sound458 C) (And.intro (sound459 C) (And.intro (sound460 C) (And.intro (sound461 C) (And.intro (sound462 C) (And.intro (sound463 C) (And.intro (sound464 C) (And.intro (sound465 C) (And.intro (sound466 C) (And.intro (sound467 C) (And.intro (sound468 C) (And.intro (sound469 C) (And.intro (sound470 C) (And.intro (sound471 C) (And.intro (sound472 C) (And.intro (sound473 C) (And.intro (sound474 C) (And.intro (sound475 C) (And.intro (sound476 C) (And.intro (sound477 C) (And.intro (sound478 C) (And.intro (sound479 C) (And.intro (sound480 C) (And.intro (sound481 C) (And.intro (sound482 C) (And.intro (sound483 C) (And.intro (sound484 C) (And.intro (sound485 C) (And.intro (sound486 C) (And.intro (sound487 C) (And.intro (sound488 C) (And.intro (sound489 C) (And.intro (sound490 C) (And.intro (sound491 C) (And.intro (sound492 C) (And.intro (sound493 C) (And.intro (sound494 C) (And.intro (sound495 C) (And.intro (sound496 C) (And.intro (sound497 C) (And.intro (sound498 C) (And.intro (sound499 C) (And.intro (sound500 C) (And.intro (sound501 C) (And.intro (sound502 C) (And.intro (sound503 C) (And.intro (sound504 C) (And.intro (sound505 C) (And.intro (sound506 C) (And.intro (sound507 C) (And.intro (sound508 C) (And.intro (sound509 C) (And.intro (sound510 C) (And.intro (sound511 C) (And.intro (sound512 C) (And.intro (sound513 C) (And.intro (sound514 C) (And.intro (sound515 C) (And.intro (sound516 C) (And.intro (sound517 C) (And.intro (sound518 C) (And.intro (sound519 C) (And.intro (sound520 C) (And.intro (sound521 C) (And.intro (sound522 C) (And.intro (sound523 C) (And.intro (sound524 C) (And.intro (sound525 C) (And.intro (sound526 C) (And.intro (sound527 C) (And.intro (sound528 C) (And.intro (sound529 C) (And.intro (sound530 C) (And.intro (sound531 C) (And.intro (sound532 C) (And.intro (sound533 C) (And.intro (sound534 C) (And.intro (sound535 C) (And.intro (sound536 C) (And.intro (sound537 C) (And.intro (sound538 C) (And.intro (sound539 C) (And.intro (sound540 C) (And.intro (sound541 C) (And.intro (sound542 C) (And.intro (sound543 C) (And.intro (sound544 C) (And.intro (sound545 C) (And.intro (sound546 C) (And.intro (sound547 C) (And.intro (sound548 C) (And.intro (sound549 C) (And.intro (sound550 C) (And.intro (sound551 C) (And.intro (sound552 C) (And.intro (sound553 C) (And.intro (sound554 C) (And.intro (sound555 C) (And.intro (sound556 C) (And.intro (sound557 C) (And.intro (sound558 C) (And.intro (sound559 C) (And.intro (sound560 C) (And.intro (sound561 C) (And.intro (sound562 C) (And.intro (sound563 C) (And.intro (sound564 C) (And.intro (sound565 C) (And.intro (sound566 C) (And.intro (sound567 C) (And.intro (sound568 C) (And.intro (sound569 C) (And.intro (sound570 C) (And.intro (sound571 C) (And.intro (sound572 C) (And.intro (sound573 C) (And.intro (sound574 C) (And.intro (sound575 C) (And.intro (sound576 C) (And.intro (sound577 C) (And.intro (sound578 C) (And.intro (sound579 C) (And.intro (sound580 C) (And.intro (sound581 C) (And.intro (sound582 C) (And.intro (sound583 C) (And.intro (sound584 C) (And.intro (sound585 C) (And.intro (sound586 C) (And.intro (sound587 C) (And.intro (sound588 C) (And.intro (sound589 C) (And.intro (sound590 C) (And.intro (sound591 C) (And.intro (sound592 C) (And.intro (sound593 C) (And.intro (sound594 C) (And.intro (sound595 C) (And.intro (sound596 C) (And.intro (sound597 C) (And.intro (sound598 C) (And.intro (sound599 C) (And.intro (sound600 C) (And.intro (sound601 C) (And.intro (sound602 C) (And.intro (sound603 C) (And.intro (sound604 C) (And.intro (sound605 C) (And.intro (sound606 C) (And.intro (sound607 C) (And.intro (sound608 C) (And.intro (sound609 C) (And.intro (sound610 C) (And.intro (sound611 C) (And.intro (sound612 C) (And.intro (sound613 C) (And.intro (sound614 C) (And.intro (sound615 C) (And.intro (sound616 C) (And.intro (sound617 C) (And.intro (sound618 C) (And.intro (sound619 C) (And.intro (sound620 C) (And.intro (sound621 C) (And.intro (sound622 C) (And.intro (sound623 C) (And.intro (sound624 C) (And.intro (sound625 C) (And.intro (sound626 C) (And.intro (sound627 C) (And.intro (sound628 C) (And.intro (sound629 C) (And.intro (sound630 C) (And.intro (sound631 C) (And.intro (sound632 C) (And.intro (sound633 C) (And.intro (sound634 C) (And.intro (sound635 C) (And.intro (sound636 C) (And.intro (sound637 C) (And.intro (sound638 C) (And.intro (sound639 C) (And.intro (sound640 C) (And.intro (sound641 C) (And.intro (sound642 C) (And.intro (sound643 C) (And.intro (sound644 C) (And.intro (sound645 C) (And.intro (sound646 C) (And.intro (sound647 C) (And.intro (sound648 C) (And.intro (sound649 C) (And.intro (sound650 C) (And.intro (sound651 C) (And.intro (sound652 C) (And.intro (sound653 C) (And.intro (sound654 C) (And.intro (sound655 C) (And.intro (sound656 C) (And.intro (sound657 C) (And.intro (sound658 C) (And.intro (sound659 C) (And.intro (sound660 C) (And.intro (sound661 C) (And.intro (sound662 C) (And.intro (sound663 C) (And.intro (sound664 C) (And.intro (sound665 C) (And.intro (sound666 C) (And.intro (sound667 C) (And.intro (sound668 C) (And.intro (sound669 C) (And.intro (sound670 C) (And.intro (sound671 C) (And.intro (sound672 C) (And.intro (sound673 C) (And.intro (sound674 C) (And.intro (sound675 C) (And.intro (sound676 C) (And.intro (sound677 C) (And.intro (sound678 C) (And.intro (sound679 C) (And.intro (sound680 C) (And.intro (sound681 C) (And.intro (sound682 C) (And.intro (sound683 C) (And.intro (sound684 C) (And.intro (sound685 C) (And.intro (sound686 C) (And.intro (sound687 C) (And.intro (sound688 C) (And.intro (sound689 C) (And.intro (sound690 C) (And.intro (sound691 C) (And.intro (sound692 C) (And.intro (sound693 C) (And.intro (sound694 C) (And.intro (sound695 C) (And.intro (sound696 C) (And.intro (sound697 C) (And.intro (sound698 C) (And.intro (sound699 C) (And.intro (sound700 C) (And.intro (sound701 C) (And.intro (sound702 C) (And.intro (sound703 C) (And.intro (sound704 C) (And.intro (sound705 C) (And.intro (sound706 C) (And.intro (sound707 C) (And.intro (sound708 C) (And.intro (sound709 C) (And.intro (sound710 C) (And.intro (sound711 C) (And.intro (sound712 C) (And.intro (sound713 C) (And.intro (sound714 C) (And.intro (sound715 C) (And.intro (sound716 C) (And.intro (sound717 C) (And.intro (sound718 C) (And.intro (sound719 C) (And.intro (sound720 C) (And.intro (sound721 C) (And.intro (sound722 C) (And.intro (sound723 C) (And.intro (sound724 C) (And.intro (sound725 C) (And.intro (sound726 C) (And.intro (sound727 C) (And.intro (sound728 C) (And.intro (sound729 C) (And.intro (sound730 C) (And.intro (sound731 C) (And.intro (sound732 C) (And.intro (sound733 C) (And.intro (sound734 C) (And.intro (sound735 C) (And.intro (sound736 C) (And.intro (sound737 C) (And.intro (sound738 C) (And.intro (sound739 C) (And.intro (sound740 C) (And.intro (sound741 C) (And.intro (sound742 C) (And.intro (sound743 C) (And.intro (sound744 C) (And.intro (sound745 C) (And.intro (sound746 C) (And.intro (sound747 C) (And.intro (sound748 C) (And.intro (sound749 C) (And.intro (sound750 C) (And.intro (sound751 C) (And.intro (sound752 C) (And.intro (sound753 C) (And.intro (sound754 C) (And.intro (sound755 C) (And.intro (sound756 C) (And.intro (sound757 C) (And.intro (sound758 C) (And.intro (sound759 C) (And.intro (sound760 C) (And.intro (sound761 C) (And.intro (sound762 C) (And.intro (sound763 C) (And.intro (sound764 C) (And.intro (sound765 C) (And.intro (sound766 C) (And.intro (sound767 C) (And.intro (sound768 C) (And.intro (sound769 C) (And.intro (sound770 C) (And.intro (sound771 C) (And.intro (sound772 C) (And.intro (sound773 C) (And.intro (sound774 C) (And.intro (sound775 C) (And.intro (sound776 C) (And.intro (sound777 C) (And.intro (sound778 C) (And.intro (sound779 C) (And.intro (sound780 C) (And.intro (sound781 C) (And.intro (sound782 C) (And.intro (sound783 C) (And.intro (sound784 C) (And.intro (sound785 C) (And.intro (sound786 C) (And.intro (sound787 C) (And.intro (sound788 C) (And.intro (sound789 C) (And.intro (sound790 C) (And.intro (sound791 C) (And.intro (sound792 C) (And.intro (sound793 C) (And.intro (sound794 C) (And.intro (sound795 C) (And.intro (sound796 C) (And.intro (sound797 C) (And.intro (sound798 C) (And.intro (sound799 C) (And.intro (sound800 C) (And.intro (sound801 C) (And.intro (sound802 C) (And.intro (sound803 C) (And.intro (sound804 C) (And.intro (sound805 C) (And.intro (sound806 C) (And.intro (sound807 C) (And.intro (sound808 C) (And.intro (sound809 C) (And.intro (sound810 C) (And.intro (sound811 C) (And.intro (sound812 C) (And.intro (sound813 C) (And.intro (sound814 C) (And.intro (sound815 C) (And.intro (sound816 C) (And.intro (sound817 C) (And.intro (sound818 C) (And.intro (sound819 C) (And.intro (sound820 C) (And.intro (sound821 C) (And.intro (sound822 C) (And.intro (sound823 C) (And.intro (sound824 C) (And.intro (sound825 C) (And.intro (sound826 C) (And.intro (sound827 C) (And.intro (sound828 C) (And.intro (sound829 C) (And.intro (sound830 C) (And.intro (sound831 C) (And.intro (sound832 C) (And.intro (sound833 C) (And.intro (sound834 C) (And.intro (sound835 C) (And.intro (sound836 C) (And.intro (sound837 C) (And.intro (sound838 C) (And.intro (sound839 C) (And.intro (sound840 C) (And.intro (sound841 C) (And.intro (sound842 C) (And.intro (sound843 C) (And.intro (sound844 C) (And.intro (sound845 C) (And.intro (sound846 C) (And.intro (sound847 C) (And.intro (sound848 C) (And.intro (sound849 C) (And.intro (sound850 C) (And.intro (sound851 C) (And.intro (sound852 C) (And.intro (sound853 C) (And.intro (sound854 C) (And.intro (sound855 C) (And.intro (sound856 C) (And.intro (sound857 C) (And.intro (sound858 C) (And.intro (sound859 C) (And.intro (sound860 C) (And.intro (sound861 C) (And.intro (sound862 C) (And.intro (sound863 C) (And.intro (sound864 C) (And.intro (sound865 C) (And.intro (sound866 C) (And.intro (sound867 C) (And.intro (sound868 C) (And.intro (sound869 C) (And.intro (sound870 C) (And.intro (sound871 C) (And.intro (sound872 C) (And.intro (sound873 C) (And.intro (sound874 C) (And.intro (sound875 C) (And.intro (sound876 C) (And.intro (sound877 C) (And.intro (sound878 C) (And.intro (sound879 C) (And.intro (sound880 C) (And.intro (sound881 C) (And.intro (sound882 C) (And.intro (sound883 C) (And.intro (sound884 C) (And.intro (sound885 C) (And.intro (sound886 C) (And.intro (sound887 C) (And.intro (sound888 C) (And.intro (sound889 C) (And.intro (sound890 C) (And.intro (sound891 C) (And.intro (sound892 C) (And.intro (sound893 C) (And.intro (sound894 C) (And.intro (sound895 C) (And.intro (sound896 C) (And.intro (sound897 C) (And.intro (sound898 C) (And.intro (sound899 C) (And.intro (sound900 C) (And.intro (sound901 C) (And.intro (sound902 C) (And.intro (sound903 C) (And.intro (sound904 C) (And.intro (sound905 C) (And.intro (sound906 C) (And.intro (sound907 C) (And.intro (sound908 C) (And.intro (sound909 C) (And.intro (sound910 C) (And.intro (sound911 C) (And.intro (sound912 C) (And.intro (sound913 C) (And.intro (sound914 C) (And.intro (sound915 C) (And.intro (sound916 C) (And.intro (sound917 C) (And.intro (sound918 C) (And.intro (sound919 C) (And.intro (sound920 C) (And.intro (sound921 C) (And.intro (sound922 C) (And.intro (sound923 C) (And.intro (sound924 C) (And.intro (sound925 C) (And.intro (sound926 C) (And.intro (sound927 C) (And.intro (sound928 C) (And.intro (sound929 C) (And.intro (sound930 C) (And.intro (sound931 C) (And.intro (sound932 C) (And.intro (sound933 C) (And.intro (sound934 C) (And.intro (sound935 C) (And.intro (sound936 C) (And.intro (sound937 C) (And.intro (sound938 C) (And.intro (sound939 C) (And.intro (sound940 C) (And.intro (sound941 C) (And.intro (sound942 C) (And.intro (sound943 C) (And.intro (sound944 C) (And.intro (sound945 C) (And.intro (sound946 C) (And.intro (sound947 C) (And.intro (sound948 C) (And.intro (sound949 C) (And.intro (sound950 C) (And.intro (sound951 C) (And.intro (sound952 C) (And.intro (sound953 C) (And.intro (sound954 C) (And.intro (sound955 C) (And.intro (sound956 C) (And.intro (sound957 C) (And.intro (sound958 C) (And.intro (sound959 C) (And.intro (sound960 C) (And.intro (sound961 C) (And.intro (sound962 C) (And.intro (sound963 C) (And.intro (sound964 C) (And.intro (sound965 C) (And.intro (sound966 C) (And.intro (sound967 C) (And.intro (sound968 C) (And.intro (sound969 C) (And.intro (sound970 C) (And.intro (sound971 C) (And.intro (sound972 C) (And.intro (sound973 C) (And.intro (sound974 C) (And.intro (sound975 C) (And.intro (sound976 C) (And.intro (sound977 C) (And.intro (sound978 C) (And.intro (sound979 C) (And.intro (sound980 C) (And.intro (sound981 C) (And.intro (sound982 C) (And.intro (sound983 C) (And.intro (sound984 C) (And.intro (sound985 C) (And.intro (sound986 C) (And.intro (sound987 C) (And.intro (sound988 C compatible) (And.intro (sound989 C compatible) (And.intro (sound990 C compatible) (And.intro (sound991 C compatible) (And.intro (sound992 C compatible) (And.intro (sound993 C compatible) (And.intro (sound994 C compatible) (And.intro (sound995 C compatible) (And.intro (sound996 C compatible) (And.intro (sound997 C compatible) (And.intro (sound998 C compatible) (And.intro (sound999 C compatible) (And.intro (sound1000 C compatible) (And.intro (sound1001 C compatible) (And.intro (sound1002 C compatible) (And.intro (sound1003 C compatible) (And.intro (sound1004 C compatible) (And.intro (sound1005 C compatible) (And.intro (sound1006 C compatible) (And.intro (sound1007 C compatible) (And.intro (sound1008 C compatible) (And.intro (sound1009 C compatible) (And.intro (sound1010 C compatible) (And.intro (sound1011 C compatible) (And.intro (sound1012 C compatible) (And.intro (sound1013 C compatible) (And.intro (sound1014 C compatible) (And.intro (sound1015 C compatible) (And.intro (sound1016 C compatible) (And.intro (sound1017 C compatible) (And.intro (sound1018 C compatible) (And.intro (sound1019 C compatible) (And.intro (sound1020 C compatible) (And.intro (sound1021 C compatible) (And.intro (sound1022 C compatible) (And.intro (sound1023 C compatible) (And.intro (sound1024 C compatible) (And.intro (sound1025 C compatible) (And.intro (sound1026 C compatible) (And.intro (sound1027 C compatible) (sound1028 C compatible))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

theorem context_impossible (C : Context 13 n σ) : False := by
  have h : (C.valuation atoms).satisfies_fmla CoupledCoreSixthRelaxed.cnf_refutation.formula := by
    rw [formula_eq]
    constructor
    intro cl hc
    exact C.satisfies_of_clause atoms cl ((List.forall_iff_forall_mem.mp (all_sound C compatible)) cl hc)
  exact CoupledCoreSixthRelaxed.cnf_refutation (C.valuation atoms) h

#print axioms context_impossible
end ErdosSzekeres.Omission.CoupledTemplateSixthRelaxed

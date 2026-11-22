# ae33-lean DESIGN (M0): radius 1 around AE33, Lean-checked modulo the 203 cake_lpr verdicts

Written 22 Nov 2026, about 17:55 KST. Nothing here was compiled when it was written; the Lean blocks are
specifications (names and statement shapes). Later milestones record deviations in README.md.

Sources (abbreviations):

| short | file |
|---|---|
| REC | `archive/es7-2026-10-19/results/ROADMAP20261115/LOWERBOUND_RUN_1118_AE33R1.md` |
| VS | `…/ROADMAP20261115/VERIFY_AE33R1_SOUNDNESS.md` |
| AB | `…/ROADMAP20261115/ABSAT8_INDEPENDENT.md` §3 (R2, AC, OCT for one new point) |
| L2 | `/home/jay/research/data/roadmap-20261115/pm1115/l1118/copied/l2enc.cpp`, SHA-256 `171a3e7c…` |
| HT | `/home/jay/research/data/lower-20261121/ae33/hashes_203.tsv` (name, u, v, type, cnf_sha256, clauses, lrat hashes) |
| ENCB | `archive/es7-2026-10-19/results/ENCBLEAN` (`EncB.DimacsSatisfiable`, `EncB.render`, `EncB.parseDimacs_render`) |
| N66 | `/home/jay/research/data/formalize-20261122/n66enc` (the descriptor/`printClause_mem` pattern) |

## 0. Decisions

| # | decision | why |
|---|---|---|
| D1 | **Descriptor architecture.** A Std-only Lean generator `gen B : Array Desc` (port of L2's loops: sorts, DFS, chain bitset, dedupe) emits *descriptors*; a separate `clauseOf B : Desc → Option (List Int)` builds each clause from its descriptor **and checks the descriptor's validity witness** in B's integer orientation table. The CNF is `cnf B := (gen B).toList.filterMap (clauseOf B)`. | Soundness then never looks inside `gen` (no proof about sorting, DFS order, dedupe or numbering choices): every clause of `cnf B` is `clauseOf B d = some cl` for some `d` (`List.mem_filterMap`). `gen` only has to reproduce L2's bytes, which the hash binding checks. A descriptor that `clauseOf` rejects is dropped, which changes the bytes (hash mismatch), never soundness. |
| D2 | **Witnesses in the descriptor.** R2 carries (w, a, x, y, z, εx, εy, εz, polarity); OCT carries the whole hexagon, rotated so that the visible edge is (q5, q0); JK carries the pentagon, slot i and edge j; RAD/GP carry the term-sign vector σ of the forbidden assignment (not L2's mask); AC carries (w, a, b, c). | The ε's become arbitrary ±1 constrained only by the three ε-weighted cone signs (checked), so neither their coordinate definition nor the angular sort enters soundness (VS §2.1). The hexagon/pentagon witnesses let `clauseOf` check "all increasing triples positive" (20 resp. 10 orientations). The sign-vector clause equals L2's mask clause when the terms' variables are distinct (always here; §2 GP). |
| D3 | **The theorem's CNF is the printed CNF.** The exe prints `cnfText i := EncB.render (numVars B) (cnf B)` for `B = base u v`, `(u, v) = pairs203[i]`. `gen`, `clauseOf`, `cnf` are total definitions (no `partial`, `opaque`, `implemented_by`, `extern`), so trust item E4 (compiled code computes the kernel value) is meaningful. `clauseOf` returns only clauses with literals in `[-nv, nv] \ {0}`, so `parseDimacs (cnfText i) = some (nv, cnf B)` holds by `EncB.parseDimacs_render` with no runtime hypothesis. | ENCBLEAN pattern; the advisor's point that `filterMap` (not `mapM`) keeps the text hypothesis non-vacuous. |
| D4 | **Hypothesis = the verdicts on the texts.** `TextsUnsat203 : ∀ i < 203, ∀ nv F, parseDimacs (cnfText i) = some (nv, F) → ¬ DimacsSatisfiable F`, equivalent (by D3) to `CnfsUnsat203 : ∀ i < 203, ¬ DimacsSatisfiable (cnf (baseOf i))`. | E3 reading of cake_lpr's `s VERIFIED UNSAT` on the file whose bytes are `cnfText i` (E1). |
| D5 | **Realization in orientation form.** Core statements use `pt : ℕ → Point` (indices `0..30` the base, `31 = p`, `32 = q`) and signs; wrappers convert to `GeneralPosition` (via `generalPosition_iff_orient_ne_zero`) and `HasConvexNGon` / `ConvexPosition` (via `Suk.convexPosition_of_positive_triples`). The mirror case goes through `Suk.reflectY` (`orient_reflectY`). | Avoids affine-invariance proofs of `ConvexPosition`; uses library lemmas that exist (`ErdosSzekeres/OrientationGeometry.lean`, `Suk/OrientationClique.lean`, `Suk/Reflection.lean`). |
| D6 | **The slot lemma by three Grassmann–Plücker steps**, not by AB's normal-cone argument. | Everything reduces to three `ring` identities (AC, Radon, 3-term GP) plus sign reasoning (§3). |
| D7 | **n = 31 fixed on the theorem side.** The variable decoding `pairOf (pvar 31 a b - 1) = (a, b)` is a kernel check on 465 pairs. The generator is generic in `n = B.size`. | All 203 bases have 31 points; avoids a nonlinear injectivity proof of the triangular numbering. |
| D8 | **The only kernel computations on data**: `(base u v).size = 31` per pair, the decoding table, the 528-pair case split (pair in `pairs203` or disjoint from H), and H's 35 orientation signs on the AE33 integers (corollary). Never `cnf`/`gen` in the kernel. | n66enc build lessons (kernel evaluation of big tables). |

## 1. Target theorem (the record's statement, REC §1)

AE33 = AlphaEvolve's 33-point near miss for ES(7) with exactly one convex heptagon H = {14, 15, 17, 20, 23, 25, 32}
(ccw 14, 15, 17, 20, 23, 32, 25); integer file `ae33.txt` (`cb6a5327…`) = JSON × 10^17. For u < v, B(u, v) = AE33 − {u, v}
in file order, labels 0..30. "Radius 1" (VS §1, LOWERBOUND_PLAN E7-2): delete two points, keep the other 31 up to
labelled order type (or mirror), add two arbitrary new points.

```lean
namespace AE33
-- Std side (AE33Enc)
abbrev Pt := Int × Int
def ae33 : Array Pt                     -- the 33 integer points of ae33.txt, in file order
def pairs203 : Array (Nat × Nat)        -- (u, v) of HT, in HT order (= pairs.txt)
def base (u v : Nat) : Array Pt         -- ae33 without indices u, v, order kept
def iorient (a b c : Pt) : Int := (b.1 - a.1) * (c.2 - a.2) - (b.2 - a.2) * (c.1 - a.1)
def cnf (B : Array Pt) : List (List Int) := (gen B).toList.filterMap (clauseOf B)
def numVars (B : Array Pt) : Nat := 2 * n2 B.size + B.size      -- 961 for n = 31
def cnfText (i : Nat) : String := EncB.render (numVars (baseOf i)) (cnf (baseOf i))
def TextsUnsat203 : Prop :=
  ∀ i < 203, ∀ nv F, EncB.parseDimacs (cnfText i) = some (nv, F) → ¬ EncB.DimacsSatisfiable F

-- Mathlib side (AE33Geo)
open ErdosSzekeres
/-- `P` realizes the labelled order type of `B` (all orientation signs equal), or of its mirror. -/
def Realizes (B : Array Pt) (P : Fin 31 → Point) : Prop :=
  ∀ i j k : Fin 31, (0 < orient (P i) (P j) (P k) ↔ 0 < iorient B[i]! B[j]! B[k]!)
def RealizesMirror (B : Array Pt) (P : Fin 31 → Point) : Prop :=
  ∀ i j k : Fin 31, (0 < orient (P i) (P j) (P k) ↔ iorient B[i]! B[j]! B[k]! < 0)
def ConvexNGonThrough (m : ℕ) (S : Finset Point) (x : Point) : Prop :=
  ∃ t ⊆ S, t.card = m ∧ ConvexPosition t ∧ x ∈ t

/-- REC §1 Theorem, for pair i. -/
theorem ae33_pair (h : TextsUnsat203) (i : Fin 203) (P : Fin 31 → Point)
    (hP : Realizes (baseOf i) P ∨ RealizesMirror (baseOf i) P) (p q : Point)
    (hgp : GeneralPosition (insert p (insert q (Finset.univ.image P))))
    (hcard : (insert p (insert q (Finset.univ.image P))).card = 33) :
    ConvexNGonThrough 7 (insert p (insert q (Finset.univ.image P))) p ∨
    ConvexNGonThrough 7 (insert p (insert q (Finset.univ.image P))) q

/-- REC §1 Corollary: radius 1 around AE33 is empty at the order-type level. -/
theorem ae33_radius1 (h : TextsUnsat203) (S : Finset Point) (hgp : GeneralPosition S) (hcard : S.card = 33)
    (u v : Fin 33) (huv : u ≠ v) (φ : Fin 33 → Point) (hS : ∀ w, w ≠ u → w ≠ v → φ w ∈ S)
    (hφ : (∀ a b c, a ∉ ({u, v} : Finset _) → b ∉ … → c ∉ … →
            (0 < orient (φ a) (φ b) (φ c) ↔ 0 < iorient ae33[a]! ae33[b]! ae33[c]!)) ∨
          (∀ a b c, … → (0 < orient (φ a) (φ b) (φ c) ↔ iorient ae33[a]! ae33[b]! ae33[c]! < 0))) :
    HasConvexNGon 7 S
```

- `hcard = 33` says p, q are new and distinct (a `Finset` collapses duplicates, so `GeneralPosition` alone would
  not constrain triples through a repeated point). φ is injective on the 31 points by the sign condition.
- The corollary covers all C(33,2) = 528 pairs: the 203 of `pairs203` by `ae33_pair`; the other 325 miss H, so
  φ(H) ⊆ S is a convex heptagon (H's 35 increasing triples in ccw order are positive on the integers, a kernel check).
- Label when done: **Lean-checked modulo `TextsUnsat203` (203 cake_lpr verdicts) and trust items E1–E6.**

## 2. Model and clause-family inventory

Variables (L2:6-9, REC §2): for a < b < n (n = 31), N2 = n(n−1)/2 = 465,
`pvar n a b = a·n − a(a+1)/2 + (b − a − 1) + 1` (L2:50),
X(a,b) = pvar a b ⟺ orient(a,b,p) > 0; Y(a,b) = N2 + pvar a b ⟺ orient(a,b,q) > 0; W(a) = 2N2 + 1 + a ⟺
orient(a,p,q) > 0. 961 variables. Real assignment ν (Mathlib side) from `pt`.

`chi B i j k` (L2:66-77) over 0..n+1: bubble-sort the triple with parity s; three base points → constant
`sign iorient(B i, B j, B k)` (= L2's `CP·s·o(sorted)` by alternation); (a, b, new) → `s·(pvar a b [+ N2])`;
(a, p, q) → `s·W(a)`. **`chi_spec`**: for distinct i, j, k < n+2, not all < n, under general position,
`LitSat ν (chi i j k) ↔ 0 < orient (pt i) (pt j) (pt k)`.

Blocks in file order (L2:293-294): R2X, R2Y, ACX, ACY, RAD, GPA, GPP∪GPQ (interleaved per triple), OCTX, OCTY, JK.
Count check per pair: header `p cnf 961 <clauses>` with clauses = HT column.

| family | L2 lines | descriptor | `clauseOf` check | clause (literal order as L2) | soundness (written source; Lean route) |
|---|---|---|---|---|---|
| R2X/R2Y | 133-159 | `r2 w a x y z εx εy εz pol` | distinct a,x,y,z < n; ε ∈ {±1}; εxεy·sgn[axy] = εyεz·sgn[ayz] = εxεz·sgn[axz] = 1 | S_w = ε_w·chi(a, w, n+w′); pol=false `[-Sx, Sy, -Sz]`, pol=true `[Sx, -Sy, Sz]` | AB §3 R2, VS §2.1 (Cramer). Lean: GP identity at pivot a, `[axz][ayt] = [ayz][axt] + [axy][azt]`, multiplied by εxεz; S_w ⟺ ε_w·[awt] > 0 |
| ACX/ACY | 160-168 | `ac w a b c` | distinct < n; σ = sgn[abc] ∈ {±1} | `[σ·chi(a,b,t), σ·chi(b,c,t), σ·chi(c,a,t)]` | AB §3 AC. Lean: `[abt] + [bct] + [cat] = [abc]` (ring) |
| RAD | 221-227 | `rad a b σ` (σ ∈ {±1}⁴) | distinct < n; pred σ: σ0 = −σ1 = σ2 = −σ3; constants agree | terms `chi(b,p,q), chi(a,p,q), chi(a,b,q), chi(a,b,p)`; literal −σ_r·ℓ_r per literal term; sorted ascending, adjacent duplicates removed | REC §2 item 2, VS §2.3. Lean: `[bpq] − [apq] + [abq] − [abp] = 0` (ring) |
| GPA, GPP, GPQ | 215-220, 228-238 | `gp e f g h i σ` (σ ∈ {±1}⁶) | e..i distinct < n+2; pred σ: σ0σ1 = −σ2σ3 = σ4σ5; constants agree | terms `chi(e,f,g), chi(e,h,i), chi(e,f,h), chi(e,g,i), chi(e,f,i), chi(e,g,h)`; as RAD | REC §2 item 3, VS §2.4. Lean: `[efg][ehi] − [efh][egi] + [efi][egh] = 0` (ring) |
| OCTX/OCTY | 239-248 (chains 87-119) | `oct w q` (hexagon q0..q5) | q distinct < n; all 20 increasing triples sgn = +1 | `[chi(q5,q0,t), −chi(q4,q5,t), −chi(q0,q1,t)]` (L2's chain (a,b,c,d) = (q4,q5,q0,q1)) | AB §3 OCT (i)-(ii). Lean: slot lemma (§3) ⇒ (q0..q5, t) has all increasing triples positive ⇒ convex 7-gon through t |
| JK | 250-284 | `jk Q i j` (pentagon) | Q distinct < n; 10 triples +1; i < 5; j < 6; all six conjuncts literals | conj = `[−chi(Qi,Qi+1,p), chi(Qi−1,Qi,p), chi(Qi+1,Qi+2,p), −chi(v,w,q), chi(u,v,q), chi(w,z,q)]` with (u,v,w,z) the j-chain of Q1 = Q[0..i] ++ [p] ++ Q[i+1..]; clause = negations, sorted, adjacent-unique; none if tautology or empty | REC §2 item 4, VS §2.6 (slot of p). Lean: slot lemma on the rotated Q ⇒ Q1 all-positive (rotation invariance) ⇒ slot lemma on the rotated Q1 with q ⇒ convex 7-gon through p and q |

Every family is sound for **every** B (only orientation-sign data of B enter the checks), with the realization
transporting the checked signs to the real configuration. Not present (VS §1): symmetry breaking, units, cubes,
auxiliary variables, JKQ. L2's `forbid_terms` shortening never fires here (all GP/RAD variables distinct: 930 =
2·C(31,2), 107,880 = 8·31·C(30,2), 143,840 = 2·16·C(31,3)); the port emits full-length clauses only, and any
difference would show as a hash mismatch.

## 3. The geometric lemmas (Mathlib side)

- **GP3** (ring): for points o, x, y, z, t: `[oxz][oyt] = [oyz][oxt] + [oxy][ozt]`. Consequences: if [oxy], [oyz],
  [oxz] > 0 then ([oxt] > 0 ∧ [ozt] > 0 → [oyt] > 0) and ([oyt] > 0 ∧ [ozt] < 0 → [oxt] > 0).
- **Slot lemma.** x : Fin (k+1) → Point with all increasing triples positive, k ≥ 2, and p with [x0 x1 p] > 0,
  [x_{k−1} x_k p] > 0, [x0 x_k p] > 0. Then [x_a x_b p] > 0 for all a < b. Proof: (1) pivot x0 on (x1, x_b, x_k):
  [x0 x_b p] > 0; (2) pivot x_k on (x0, x_a, x_{k−1}): [x_a x_k p] > 0; (3) pivot x_a on (x_b, x_k, x0) for
  0 < a < b < k: [x_a x_b p] > 0. Hence (x0, …, x_k, p) has all increasing triples positive.
- **Rotation.** All increasing triples positive is invariant under cyclic rotation of the index (orient_cycle).
- **Polygon.** Positive increasing triples on m ≥ 4 points ⇒ injective and `ConvexPosition` of the image
  (`Suk.convexPosition_of_positive_triples`).
- **Mirror.** `Suk.reflectY` negates orient; reflect P, p, q, apply the direct case, reflect the 7-gon back (reverse
  its order so the triples are positive again).

## 4. Trust list (as ENCBLEAN / n66enc)

| item | content | evidence |
|---|---|---|
| E1 | the bytes the exe prints for pair i are the bytes cake_lpr certified | M9: SHA-256 of the exe output = HT `cnf_sha256` = L18 `cert/certify.jsonl` = `summary.jsonl` |
| E2 | the verdicts: cake_lpr `c14ff498…` printed exactly one line `s VERIFIED UNSAT` on (that CNF, the kept LRAT) | REC §4 (fresh run 203/203), VS §3.1 (two runs inspected), L18 `cert/*.cake.out`; M9 re-greps the recorded outputs |
| E3 | DIMACS semantics: that verdict means every parse of the file in ENCB's `parseDimacs` sense is unsatisfiable | ENCB M9 (parser agreement evidence only, `logs/m9_a2_cake_parse.log`) |
| E4 | the Lean compiler and runtime: the compiled exe computes the kernel value `cnfText i` | as ENCBLEAN/n66enc; this package's `gen`/`clauseOf`/`cnf` are total definitions without `partial`/`opaque`/`implemented_by`/`extern`. Core code they call is not: `Array.foldlM`/`Array.forIn'` (`@[implemented_by]`), `Array.replicate`/`push`/`set!`, `String.push` (`@[extern]`), `List.mergeSort` (`@[csimp]`), GMP integers, `Std.HashSet` hashing; all part of E4 (README §2) |
| E5 | kernel, Mathlib `f897ebcf`, and the definitions (Point, orient, GeneralPosition, ConvexPosition, the statement) | axiom audit `#print axioms` = [propext, Classical.choice, Quot.sound] |
| E6 | SHA-256 collision resistance | standard |
| (data) | the Lean constant `ae33` is ae33.txt | M9: the exe prints the 33 points in ae33.txt's format; SHA-256 = `cb6a5327…` (REC: = JSON × 10^17, EXACT) |

## 5. Lemma map (Lean files)

| module | content |
|---|---|
| `AE33Enc/Basic.lean` (Std) | `Pt`, `iorient`, `isgn`, `osgn`, `pvar`, `n2`, `numVars`, `Term`, `sort3`, `chi` |
| `AE33Enc/Clause.lean` (Std) | `Desc`, `ccwOk`, `forbidClause`, `jkClause`, `clauseOf`, `bounded` |
| `AE33Enc/Gen.lean` (Std) | `gen` (port of L2's loops), `cnf`, `numVars` |
| `AE33Enc/Data.lean` (Std) | `ae33`, `pairs203`, `base`, `baseOf`, `cnfText`, `TextsUnsat203`, `CnfsUnsat203` |
| `AE33Enc/Main.lean` (Std) | exe `ae33print`: `cnf i` → stdout `cnfText i`; `pts` → ae33.txt format; `stats i` |
| `AE33Enc/Bridge.lean` (Std) | `mem_cnf` (filterMap), `bounded_spec`, `cnf_bounded`, `parse_cnfText`, `texts_iff_cnfs` |
| `AE33Geo/Sem.lean` | `pt`, `realAssign`, `pairOf` decoding (kernel check), `chi_spec`, `osgn_spec` (realization) |
| `AE33Geo/Ident.lean` | AC, RAD, GP3 identities and sign corollaries |
| `AE33Geo/Slot.lean` | slot lemma, rotation, positive cycle ⇒ convex position |
| `AE33Geo/Sound.lean` | `clauseOf_sound` per family; `cnf_sat_of_no7` |
| `AE33Geo/Main.lean` | `pair_core`, mirror, `ae33_pair`, `ae33_radius1`, axiom guards |
| `tools/hash_binding.sh` | M9 |

## 6. Risks

- R1 byte identity: OCT key order, GPP/GPQ interleaving, JK sort/unique/dedupe, R2 sort uniqueness (strict total
  orders under general position). Pilot pairs ae_d14_15 (JK with W literals), ae_d14_16 (OCTX), ae_d0_14 (OCTY);
  on a mismatch compare block by block against `zstd -dc` of L18's `cnf/<name>.cnf.zst`.
- R2 memory/time of the exe (≈1.2M clauses per pair): keep everything in arrays; pipe to `sha256sum`.
- R3 kernel evaluation by accident (n66enc lesson): data definitions `@[irreducible]` where proofs could unfold them.

## 7. As built (22 Nov 2026, 18:50 KST)

Everything of §1 compiles with [propext, Classical.choice, Quot.sound]; deviations from the M0 text:

1. **Realization** uses `B.getD i (0, 0)` instead of `B[i]!` (`AE33Geo.Realizes`, `RealizesMirror`, `Realizes31`).
   Same meaning for in-range indices; all indices used are in range.
2. **Corollary signature** (`AE33Geo.ae33_radius1`): labels are `ℕ` with explicit bounds (`u v < 33`), φ : ℕ → Point,
   and the hypotheses are `hS` (the 31 images lie in S), `hinj` (φ is injective on the 31 labels: "a 31-point
   subset") and `OTEmb φ u v ∨ OTEmbMirror φ u v` (all orientation signs preserved, resp. reversed). Added
   `ae33_radius0` (REC: "Radius 0 follows"), an instance of `ae33_radius1` with t = (w + 1) % 33.
3. **Boundedness** is enforced once by `clauseB` (Gen.lean) around `clauseOf`; `cnf B = filterMap (clauseB B)`. The
   bounds inside `clauseOf` stay (they never reject anything); the printed bytes did not change (pilot re-run by M9).
4. **Modules**: `AE33Geo/{Slot, Sem, Sound, Pair, Radius1}.lean` instead of `{Sem, Ident, Slot, Sound, Main}`; the
   identities live in `Slot` (`gp3`) and `Sound` (`ac_id`, `rad_id`, `gp_id`).
5. **OCT/JK** both use one lemma, `insert_pos` (insertion after position j of a positive cyclic list), which is the
   slot lemma (`slot`, three GP steps) composed with two rotations (`posChain_rot`).
6. **Kernel checks on data** (`decide +kernel`): `pvar_spec_all` (465 pairs), `baseOf_size` (203), `keepIdx_len`
   (203), `pairs203_len`, `pairs_cover` (528 pairs; `List.any` form because list membership of pairs had no
   `Decidable` instance), `hept_ccw` (35 triples on the AE33 integers). Nothing evaluates `gen` or `cnf` in the kernel.
7. **E4 note**: `gen` uses `Std.HashSet` for l2enc's deduplication. Its result (which descriptors are kept) is pure
   set membership, so it does not depend on the hash function; the compiled runtime's hashing (and `List.mergeSort`'s
   `@[csimp]` replacement, a proved equation) cannot change the kernel value of `cnf B` short of a compiler/runtime
   bug, which is trust item E4.

Lemma map as built:

| theorem | file | content |
|---|---|---|
| `mem_cnf`, `parse_cnfText`, `texts_iff_cnfs` | AE33Enc/Bridge | every clause has an accepted descriptor; the printed text parses back; hypothesis equivalence |
| `pvar_spec_all`, `realAssign`, `chi_spec`, `osgn_spec` | AE33Geo/Sem | decoding; real assignment; literal semantics; base signs via realization |
| `gp3`, `slot`, `slot_chain`, `posChain_rot`, `insert_pos`, `posChain_card_convex` | AE33Geo/Slot | the geometry of §3 |
| `sound_r2`, `sound_ac`, `sound_rad`, `sound_gp`, `sound_oct`, `sound_jk`, `clauseOf_sound`, `cnf_sat` | AE33Geo/Sound | soundness of every family; `Ctx B pt → DimacsSatisfiable (cnf B)` |
| `core`, `core_mirror`, `pair_of_unsat`, `ae33_pair` | AE33Geo/Pair | REC §1 Theorem |
| `hept_ccw`, `pairs_cover`, `ae33_radius1`, `ae33_radius0` | AE33Geo/Radius1 | REC §1 Corollary and radius 0 |

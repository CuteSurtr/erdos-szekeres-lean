# n66enc DESIGN (M0): the N66 relaxation encoder in Lean

Written 22 Nov 2026, about 06:40-07:30 KST, by the `n66-encoder` agent (slot lenc6). Pattern: ENCBLEAN
(`archive/es7-2026-10-19/results/ENCBLEAN/DESIGN.md`, trust items E1-E6). Sources read (read-only): the N66 record
`N66N20261113/README.md` (§2, §6.2-§6.7) and `cubes20261115/` (README, STATUS_campaign.md), the generator sources in
`/home/jay/research/data/n66-20261113` (= W), `p2/c14/campaign_status.json` and the per-cube certificate folders,
the library (`ErdosSzekeres/Omission/*`, `OrientationPackets`, `OrientationObstructions`, `ConvexCycleCuts`,
`Suk/Reflection`), ES305N20261119/LemmaZ.lean, ENCBLEAN `EncB/{Dimacs,Cover,Render}.lean`.

Labels (es-research §2) are used exactly. Everything in §1-§3 marked [D] was checked on disk in this session with
read-only commands; [R] is read from a record and not re-verified.

---

## 0. Decisions

| # | decision | why |
|---|---|---|
| D1 | **Bind to `trim.cnf`, not `cert.cnf`.** The task text says "cert.cnf = F_c + cube units", but cake_lpr checked `trim.cnf`/`trim.lrat` and the untrimmed `cert.lrat` was deleted after trimming (`pipeline.log`: "full lrat sha256 …; deleting cert.lrat") [D]. The verdict hash of cube i is `trim_cnf_sha256` (cert.json, verify.json, campaign_status.json, STATUS_campaign.md) [D]. | Only a verdict that exists can be bound. |
| D2 | **The theorem's CNF is a closed, data-free Lean term `fullCnf R c`** (complete level-14 relaxation for cube c, rows R), never the 132 trimmed files themselves. | The 132 trims are 18,699,830 clauses / 1,183,383,419 bytes [D]; each cube's activated set has about 660,810 quadruples. None of it can be a Lean term that the kernel or the elaborator handles. |
| D3 | **The printer takes the per-cube selection as runtime input** (eager indices, (quadruple, j) pairs, unit/row/counter/SB indices) and Lean proves, for *every* input, that each clause it emits is a member of `fullCnf R0 c`. With `¬ Sat(sub) → ¬ Sat(super)` this turns the 132 verdicts into `∀ c ∈ leaves132, ¬ DimacsSatisfiable (fullCnf R0 c)`. | ENCBLEAN D9 (the kernel never evaluates instance data), generalised to trimmed certificates: soundness never depends on which clauses were selected. |
| D4 | **Rows are a named mathematical hypothesis `RowsValid R0`, not a trust item.** R0 = the 11,884 distinct row supports that occur in the 132 trims [D] (subset of `mono/rows_1832.json`; 173,134 row clauses with multiplicity [D]). | No clause family implies a row; each row rests on its own template/core verdicts plus transport, mirror and cycle arguments (N66 README §2.6-§2.9). Only used rows were re-justified (`tcert/justification.json` per cube), so R0 is the used union, not all 15,648. |
| D5 | **"Modulo the 132 verdicts" alone is not attainable in this design.** The end statement is "Lean-checked modulo CubesUnsat132 (132 cake_lpr verdicts), RowsValid R0 (rows, separately CERTIFIED) and trust items E1-E6". Discharging RowsValid R0 needs a second encoder (coupled5 templates/cores) and is a later stage (§6, M10+). | Never round up. |
| D6 | **SB needs the mirror.** The 79 lex-leader clauses (27 τ-pairs) hold for S *or* its mirror ρS, not for S itself (N66 README §6.7). The top-level proof picks S' ∈ {S, ρS} first. Hence RowsValid quantifies over all N66-class configurations, and the geometric mirror (Suk.reflectY: x kept, orientations negated) is a milestone (M6). | The task's M2-M3 wording ("every configuration … yields a satisfying assignment") is false for the CNF with SB clauses; true for S or ρS. |
| D7 | **Combinatorial interface = the triple-color function.** `Model` (§2) is an x-ordered point set given only by `cup : ℕ → ℕ → ℕ → Bool` on increasing triples, plus four fields: no 6-cap path, no 6-cup path, signotope packets, no (5-cap, 5-cup) pair on common endpoints. Labels, states, owners, refined domains and the six-order test are *derived* from `cup` with the library's `ActualRanks`/`StateInterface`. Orientation atoms in state-index order are defined from `cup` by permutation parity, so no geometry is needed for them. Chain atoms C_k/U_k are defined as paths of consecutive triples, so F5, F6 and the first half of F7 hold by definition. | Smallest geometric surface (M4-M6): build a `Model` from a `Configuration`; everything else is combinatorics. ENCBLEAN D5 analogue. |
| D8 | **Two packages.** `N66Enc` (Std-only; imports ENCBLEAN `EncB.Dimacs`, `EncB.Cover`, `EncB.Render` read-only for `DimacsSatisfiable`, `render`, `parseDimacs_render`): CNF definitions, numbering, printer, cover. `N66Geo` (Mathlib + library + N66Enc): `Model` semantics, soundness, geometry, assembly. | ENCBLEAN D2. Std-only side compiles in seconds; reusing EncB keeps one DIMACS semantics and gives E3's proved round trip for free (`parseDimacs_render` is generic in F, Render.lean:585). |
| D9 | **Numbering by allocation list.** `num : Atom → ℕ` = 1 + first position of the atom's code in `pyAlloc` (Python's allocation order, 1,647,808 entries), via `EncB.numberMap`; atoms outside `pyAlloc` get `BIG + code`. `ν v` decodes back. Soundness never depends on numbering correctness (ENCBLEAN D4); Python's exact numbers are checked by bytes only. | Reuses `numberMap_getD`/`decode_numberMap` (EncB/Dimacs.lean:156-178). |
| D10 | **Compute discipline.** Every compile/print job runs in `esr-ag-lenc6-*` units under the task's gates. The Python generator is never run in W (live c15 units): hash-pinned copies go to `ref/` in this directory with `ETV_A=4 ETV_B=4`. | Task rules 2-4. |

---

## 1. The target theorem and the trust base

> **Note (10:25 KST):** §8 (as built) supersedes §1.1-§2 where they differ: rows are `List (Fin 70)`, chain
> atoms use `SEPath`, the end theorem is `N66Geo.n66_bound_55_of_cubes` (End.lean), M9 is `tools/hash_binding.py`.

### 1.1 Statement (Lean; names provisional)

```lean
-- N66Enc (Std-only)
namespace N66Enc
/-- A cube: (state, occupied?) literals; `true` = occupied = +sel_s, `false` = hole = −sel_s. -/
abbrev Cube := List (Nat × Bool)
def leaves132 : List Cube := SplitTree.leaves tree14          -- the 200-node split tree of p2/c14 (§3)
def R0 : List (List Nat) := parseRows (include_str "data/rows_used.txt")   -- 11,884 sorted supports
/-- The complete level-14 relaxation for cube c and row set R (§1.2), DIMACS-numbered as the generator. -/
def fullCnf (R : List (List Nat)) (c : Cube) : List (List Int) := …
def CubesUnsat132 : Prop := ∀ c ∈ leaves132, ¬ EncB.DimacsSatisfiable (fullCnf R0 c)

-- N66Geo (Mathlib + library)
/-- No configuration of the N66 class occupies every state of T (the record's "demand-one row on T"). -/
def RowValid (T : List Nat) : Prop :=
  ∀ n (c : Configuration n), ¬ c.HasCap 6 → ¬ c.HasCup 6 →
    ¬ HasConvexNGon 8 (Finset.univ.image c.point) → ∃ s ∈ T, s ∉ n66Occupied c
def RowsValid (R : List (List Nat)) : Prop := ∀ T ∈ R, RowValid T

theorem n66_bound_of_full (R : List (List Nat)) (hR : RowsValid R)
    (h : ∀ c ∈ leaves132, ¬ EncB.DimacsSatisfiable (fullCnf R c)) : OmissionZRow.N66Bound 55
theorem n66_bound_55_of_cubes (h : CubesUnsat132) (hR : RowsValid R0) : OmissionZRow.N66Bound 55 :=
  n66_bound_of_full R0 hR h
-- audit: #print axioms = [propext, Classical.choice, Quot.sound], guarded by #guard_msgs
```

`OmissionZRow.N66Bound` is the record's definition (LemmaZ.lean:22, quoted in the task). `n66Occupied c` = the set
of N66 state indices (etv order, §1.2) of the points of c; it is well defined because ¬6-cap/¬6-cup put every label in
[1..4]² (`ActualRanks.rank_lt_of_avoids`).

**The bridge from the files to `CubesUnsat132` (outside the kernel, as in ENCBLEAN M9).** For each leaf i the
printer, run on runtime data D_i, writes `render 1647808 L_i` where `L_i = printClauses D_i`. Lean proves
`printClauses_sub : ∀ D L, printClauses D = some L → ∀ cl ∈ L, cl ∈ fullCnf R0 (leaf D)` and
`unsat_of_sub : (∀ cl ∈ L, cl ∈ F) → ¬ Sat L → ¬ Sat F`. E1: SHA-256 of the printed text = `trim_cnf_sha256` of leaf i.
E2: cake_lpr printed `s VERIFIED UNSAT` for that file. E3: cake_lpr reads the file as `parseDimacs` does, and
`parseDimacs (render nv L) = some (nv, L)` (proved, EncB). So `¬ Sat L_i`, hence `¬ Sat (fullCnf R0 leaf_i)`.

### 1.2 `fullCnf R c`: what it contains (the generator, by hash)

Generator files (W copies; equal by SHA-256 to the record copies in `N66N20261113/tools/` [D]; mtimes before the c14
start 15 Nov 05:50 [D]):

| file | SHA-256 | role |
|---|---|---|
| `etv_common.py` | `12f00cc6…2542725` | states (profiles sorted by (sum, f)), cells, capH/cupH, plain domains D, refined domains D', six-order table TT (from **plain** D), FIXED_OCC = [0, 1] |
| `tt_A4_B4.npz` | `7c98c546…6bf45` | cache of TT/TTR used by etv_common (Lean recomputes TT; byte identity checks it) |
| `coupled5.py` | `fbaf431a…bef8c` | variable allocation (before, cap_ge 2..4, cup_ge 2..4 per pair; orientation per triple; convex_four per 4-set), state-dependent clauses (empty/domain/positive); its `add` dedups, drops tautologies and constants, and sorts literals by |lit| |
| `lazymono.py` | `8fd6bd5d…be5fa` | eager stream (exact order below), chain/end atoms, `quad_clauses` (12 per ordered quadruple) |
| `p2_write.py` | `730bad3e…09efa6c` | cert.cnf layout: eager, quad (activated, sorted), units (sel0, sel1, cube units), rows, card, sb |
| `p2_sb.py` | `2c5844a0…df47` | the 79 lex-leader clauses for the 27 τ-pairs (aux e_j numbered after the counter) |
| `p2_batch_cube.py` | `999451d9…3515` | the cube driver (copy of p2_batch.py + `--cube`) |
| `p2_lrat_trim` / `.cpp` | `5f1f031e…dd7` / `6a1a9aca…9d9f` | trim.cnf = header `p cnf <nv> <marked>` + the marked original lines **verbatim, in CNF order** [D, source] |
| pysat 1.9.dev20 `CardEnc.atmost(seqcounter)` | (compiled extension; hash to be pinned in M1) | the counter; no source on disk, so the Lean port is fitted to dumps and grid-tested (M1) |

Per cube (all 132 [D]): W = range(70), L = 14, the same 27 SB pairs, rows_file `mono/rows_1832.json` (15,648 rows, all
d = 1), header vars 1,647,808. Layout of hhhhhh [D]: eager [1, 1,489,581]; quad [1,489,582, 9,419,301] (660,810 × 12);
units 8; rows 15,648; card 1,552; sb 79; sel_s = 988,541 + s; mono_top 1,647,026; card_top 1,647,782; SB aux
1,647,783-1,647,808.

`fullCnf R c` (Lean, order irrelevant for satisfiability; every part is a fixed function of the 70 states):

1. **eager** = lazymono's eager stream for W = range(70), exactly in Python order (index k ↦ clause; the printer uses
   eager indices). Families F1 (empty, domain; positive), F2 (threshold), F3 (transitivity), F4 (growth), F5 (C3/U3
   start), F7 (CE/UE links and exclusion) — §4.
2. **quad** = the 12 clauses `quad_clauses(a,b,c,d)` for every ordered quadruple of distinct states whose six pairs
   are all "can" (D' nonempty) in that order: F6 (chain step) and F8 (signotope). This is mono66's complete F6+F8
   (39,017,853 − eager clauses); the activated sets are subsets.
3. **units** `[sel0]`, `[sel1]`, then `[±sel_s]` for the literals of c.
4. **rows** `[−sel_s | s ∈ T]` for T ∈ R (T sorted).
5. **card** the seqcounter "at most 14 of the 68 hole literals −sel_s (s ∉ {0,1})", aux after mono_top, exactly
   pysat's clause and numbering order.
6. **sb** p2_sb's clauses for the 27 pairs (fixed list, §4.9), aux after the counter.

### 1.3 Trust items (with what is checked)

| # | item | evidence / plan |
|---|---|---|
| **E1** | **Printer output.** For each leaf i, the text the printer writes for (leaf i, D_i) has SHA-256 = the recorded `trim_cnf_sha256` of leaf i. Note: the 8 UP-refuted leaves share one trim hash (`06250f34…`) [D]; the binding is per leaf, never assuming 132 distinct hashes. | M9: `tools/hash_binding.sh` streams each print into sha256sum and compares with all four records (cert.json, verify.json, campaign_status.json, STATUS_campaign.md). Control first: print one complete cert.cnf (with runtime activated list and all 15,648 rows) and compare with `full_cnf_sha256` (cert.json). Computation. |
| **E2** | **Verdicts.** cake_lpr `c14ff498…` (same binary as ENCBLEAN [D]) printed exactly `s VERIFIED UNSAT` on (trim.cnf, trim.lrat) for each leaf. | cake.out per cube [D for hhhhhh]; campaign driver acceptance rules (STATUS_campaign.md); independent checks VS/VN/U1/VB [R]. trim.lrat kept zstd'd in `p2/c14/<id>/it1/` [D]. |
| **E3** | **DIMACS semantics.** cake_lpr reads each file in `parseDimacs`'s language as `parseDimacs` does; its UNSAT means `¬ EncB.DimacsSatisfiable` of the parsed list. | Inherited from ENCBLEAN E3 (same binary; `logs/m9_a2_cake_parse.log` there). Proved: `parseDimacs_render` (EncB/Render.lean:585), needs literals nonzero with `natAbs ≤ nv`; the printer refuses to print otherwise. |
| **E4** | **Lean compiler/runtime** for the printer (and the reading of its runtime input, which is irrelevant to soundness because `printClauses_sub` is ∀ D). | As ENCBLEAN E4. |
| **E5** | Kernel, Mathlib `f897ebcf…`, the library's definitions (`Configuration`, `HasCap/HasCup`, `HasConvexNGon`), `OmissionZRow.N66Bound`. | As ENCBLEAN E5. |
| **E6** | SHA-256 / `sha256sum`. | — |
| **H-rows** | **`RowsValid R0`** — a hypothesis of the theorem, not trusted silently. | CERTIFIED row by row in the record (per-cube `tcert/justification.json`: kinds transported/mirror/cycle/core; template and core CNFs cake_lpr-certified; `final_verify66.py`, `p2_recheck_rows.py`) [R]. M10+ (§6) would make it Lean-checked modulo template/core verdicts. |

Leaves the trust base relative to the record's chain: §6.3's written soundness of F1-F8 + tail, §6.7 (SB), the cover
(`cover_check.py`, VS/VN), `p2_verify.py`'s clause classification (replaced by `printClauses_sub` + E1).

---

## 2. Interfaces (frozen at M0; changes need a note here)

### 2.1 Combinatorial interface `Model` (input of M2)

```lean
namespace N66Geo
open ErdosSzekeres.Omission.ActualRanks
/-- An x-ordered point set given by the colors of its increasing triples (true = positive = cup). -/
structure Model where
  n : ℕ
  cup : ℕ → ℕ → ℕ → Bool
  noCap6 : Avoids n cup false 6
  noCup6 : Avoids n cup true 6
  signotope : ∀ a b c d, a < b → b < c → c < d → d < n →
    PacketValid (cup a b c) (cup a b d) (cup a c d) (cup b c d)       -- OrientationPackets.PacketValid
  noCapCup55 : ∀ p q, q < n → ¬ (StartEndPath cup false p q 5 ∧ StartEndPath cup true p q 5)
```

Derived (all combinatorial, M2): `labels cup u v` (library), the column heights of `Incoming (labels cup) v` in the
4×4 box, `state : Fin n → Fin 70` (etv order), its injectivity (`StateInterface.states_distinct`), `occupied`,
`owner : occupied state → Fin n`, the canonical assignment of §2.2, `Model.dual` (cup ↦ !cup on increasing triples;
a `Model` again because every field is symmetric) with `occupied (dual M) = τ '' occupied M`.

`StartEndPath cup color p q k`: a strictly increasing list of k indices from p to q whose consecutive triples all have
color `color` (to be defined next to `ActualRanks.EndingPath`).

### 2.2 The intended assignment (what M2 proves satisfies every non-cube clause)

For a `Model M`, with owner o(s) of an occupied state s:
- sel_s := [s occupied];
- before(i,j) (i < j) := [i, j occupied ∧ o(i) < o(j)];
- cap_ge(i,j,k) := [i, j occupied ∧ (labels of the pair in x-order).1 ≥ k], cup_ge likewise with .2;
- orientation(i<j<k) := cup of the x-sorted owners XOR parity of the sorting permutation (occupied; else false);
- convex_four := false (allocated by coupled5, used by no clause);
- C_k(a,b,c) := [a,b,c occupied ∧ o(a) < o(b) < o(c) ∧ StartEndPath cap from o(a) of length k ending (o(b), o(c))], U_k with cups;
- CE(p,q) := [∃ u, C_5(p,u,q)], UE likewise;
- counter aux s(a,j) := [at least j holes among the first a+1 hole literals];
- SB aux e_j := [the first j pairs agree];
- for `Model`s built from configurations with n ≥ 2 the fixed units hold; every clause with a ¬sel guard of an
  unoccupied state holds by the guard.

### 2.3 Geometric interface (output of M4-M6)

`modelOf (c : Configuration n) (h6cap) (h6cup) (hoct) : Model` with `cup := c.cup`;
`n66Occupied c = (modelOf c …).occupied`; `modelOf (reflect c) = (modelOf c).dual` up to `occupied`.

---

## 3. The cube cover (from `p2/c14/campaign_status.json` [D])

- 200 nodes: 64 roots = all sign patterns of states (25, 12, 16, 29, 17, 37) (bit 1 = occupied = +sel_s); 68 split
  nodes, each with exactly two children `lits + [[s,1]]` then `lits + [[s,0]]`; split states 23 (21×), 49 (12),
  44 (9), 52 (9), 46 (8), 40 (7), 45, 39; **132 leaves, all `certified`**, depth 6-12 [D].
- Lean: `inductive SplitTree | leaf | node (s : ℕ) (occ hole : SplitTree)`, the base 6 levels as nodes too;
  `leaves : SplitTree → List Cube`; `covers_leaves : ∀ t (x : ℕ → Bool), ∃ c ∈ leaves t, ∀ (s,b) ∈ c, x s = b`
  (structural induction; no meaning of 988541+s is needed). `leaves tree14` has 132 entries; their order is
  `seq` order of campaign_status (data; the printer maps leaf index → certdir).
- The printer's units for leaf i are the leaf's literals (a trim may keep only some of them; a subset is fine).

---

## 4. Clause families: inventory, written soundness, where each lives

Notation: s_u is the state of owner u; "guards" = trailing literals −sel of the owners a clause mentions (every
geometric clause has them, so it holds when one of those states is unoccupied). Literal order inside coupled5
clauses: sorted by |lit|, then guards; lazymono's own clauses: as written.

| # | family (Python) | clause | side condition | written soundness (record) | Lean (M2) | library lemma to reuse |
|---|---|---|---|---|---|---|
| 4.1 | F1 empty (coupled5:72-76, lazymono:35-36) | [−before(u,v)] + guards (u,v) | D'(s_u→s_v) = ∅ | N66 §2.3 state separation + §2.5 Lemma R | label(u,v) ∈ D'(s_u→s_v) for o(u) < o(v) | `StateInterface.incoming_admissible`, `ActualRanks.rank_attained`, `labels_increasing` |
| 4.2 | F1 domain (coupled5:77-81) | before(u,v) → label(i,j) ≠ (a,b) via cap_ge/cup_ge thresholds, sorted by |lit|, + guards (u,v) | (a,b) ∉ D'(s_u→s_v) | same | same; thresholds of one number | `Coupled.domain_clause` (residual analogue) |
| 4.3 | F1 positive (coupled5:82-85) | [±orientation(q)] + guards in tag order | TT[s_a,s_b,s_c] (plain domains) | §2.6/§2.7 item 9 (six-order test) | for the actual x-order the three plain domains contain the labels; growth forces the color (forced_cap/forced_cup); parity transfers it | `StateInterface.forced_cap/forced_cup`, `CycleSigns.CheckTriple` pattern |
| 4.4 | F2 threshold (lazymono:44-46) | cap_ge(k+1) → cap_ge(k), k = 2,3 + guards | — | §6.3 F2 | thresholds of one number | — |
| 4.5 | F3 transitivity (lazymono:52) | before(a,b) ∧ before(b,c) → before(a,c) + guards | can(a,b), can(b,c) | §6.3 F3 | x-order is a linear order | `Coupled.transitive_clause` |
| 4.6 | F4 growth with ceilings (lazymono:55-60) | before ∧ before ∧ (abc cap) ∧ cap_ge(a,b,k) → cap_ge(b,c,k+1), k = 1..4, constant ge(1)=T, ge(5)=F dropped as Python does; cup version | can(a,b), can(b,c), can(a,c) | §2.2, §6.3 F4 | `labels_increasing`; label ≤ 4 from no 6-cap/6-cup | `rank_lt_of_avoids`, `Coupled.growth_clause` |
| 4.7 | F5 chain start (lazymono:63-64) | before ∧ before ∧ cap → C3(a,b,c); cup → U3 | as 4.6 | §6.3 F5 | definitional (D7) | — |
| 4.8 | F7 (lazymono:66-72) | C5(p,u,q) → CE(p,q); U5 → UE; ¬CE ∨ ¬UE | C5 allocated | §6.3 F7: 5-cap + 5-cup on common endpoints = convex octagon | first two definitional; exclusion = `Model.noCapCup55` | geometry M5 |
| 4.9 | F6 chain step (quad_clauses, lazymono:83-85) | C_k(a,b,c) ∧ before(c,d) ∧ (bcd cap) → C_{k+1}(a,c,d), k = 3,4; U likewise | okquad | §6.3 F6 | definitional (append one point) | — |
| 4.10 | F8 signotope (quad_clauses, lazymono:81) | before(a,b) ∧ before(b,c) ∧ before(c,d) → (abc,abd,acd,bcd) ∉ BAD4 (8 patterns, ≥ 2 sign changes) | okquad | §6.3 F8 | `Model.signotope` + parity bookkeeping | `packetValid_of_xordered` (geometry M4) |
| 4.11 | fixed units (p2_write:33-34) | [sel0], [sel1] | n ≥ 2 | §2.4 | first point has empty state (0), second state (1,0,0,0) = 1 | — |
| 4.12 | cube units (p2_write:36) | [±sel_s] | — | cover (§3) | `covers_leaves` | — |
| 4.13 | rows (p2_write:41) | [−sel_s, s ∈ T] | T ∈ R | §2.6-§2.9 + certificates | hypothesis `RowsValid R` (D4) | — |
| 4.14 | card (p2_write:43-44) | pysat seqcounter ≤ 14 over the 68 hole literals | — | §6.3 tail | holes = 70 − n ≤ 14 when n ≥ 56; s(a,j) := prefix count ≥ j satisfies base/transfer/increment/overflow | — (generic, Std-only) |
| 4.15 | sb (p2_write:47-52, p2_sb:31-38) | LEX for 27 pairs (s, τ s) | pairs are τ-pairs from distinct orbits (decide on 27 pairs) | §6.7 | for x and x∘τ exactly one satisfies LEX unless equal on the pairs; choose S or ρS (D6) | `Suk.reflectY`, `orient_reflectY`, `hasConvexNGon_of_reflectY` (M6) |

Notes. (i) `positive` uses the **plain** table TT (`coupled5.TT = ec.TT`), the domain families the **refined** D'
(`coupled5.DIFF = ec.DREF`). (ii) F3-F5 are emitted only for permutations allowed by `can`; omitted clauses never
affect soundness. (iii) The convex_four atoms (916,895) are allocated but occur in no clause.

---

## 5. Lemma map (what is new, what is reused)

| step | statement | source |
|---|---|---|
| L1 | `atomOfCode (code a) = a` (mixed radix, bounds) | new, `omega` |
| L2 | `ν (num a) = meaning a` for every atom | EncB `numberMap_getD`, `decode_numberMap` + L1 |
| L3 | `printClauses_sub`, `unsat_of_sub` | new (membership by construction) |
| L4 | `covers_leaves` | new; pattern EncB `covers_signPatterns` |
| L5 | counter soundness (prefix counts) | new, generic |
| L6 | LEX lemma: x or x∘τ satisfies LEX; SB clauses satisfied with e_j = prefix agreement | new, generic (record's p2_sb self-test is the control) |
| L7 | labels in [1..4]², states in the 4×4 box (70 states), owner injective, n66 index | `ActualRanks.rank_lt_of_avoids`, `StateInterface.states_distinct`; the Z correspondence of LemmaZ (`Z_card = 70`, f(0) ≤ 4 ∧ f(4) = 0) |
| L8 | refined-domain membership (Lemma R) | `rank_attained` + predecessor on the attaining path (as N66 §2.5) |
| L9 | six-order test ⇒ forced color | `StateInterface.forced_cap/forced_cup` |
| L10 | growth/ceilings | `labels_increasing`, `rank_lt_of_avoids` |
| L11 | fixed states | `Incoming` of points 0 and 1 |
| L12 | `Model.dual`, occupancy transposes | new, combinatorial (ranks swap colors) |
| G1 | `modelOf`: cup = `Configuration.cup`, no 6-cap/6-cup | `Configuration.avoids_of_noCap/noCup` |
| G2 | signotope | `packetValid_of_xordered` |
| G3 | 5-cap + 5-cup on common endpoints ⇒ `HasConvexNGon 8` | **new geometry**; via `hasConvexNGon_of_positive_cycle` (ConvexCycleCuts.lean:11) on the cyclic order p, cup inner, q, cap inner reversed |
| G4 | mirror: reflected configuration is in the class and its model is the dual | `Suk.reflectY`, `orient_reflectY`, `hasConvexNGon_of_reflectY`, `generalPosition_reflectY` |
| A | assembly | — |

---

## 6. Milestones

| M | content | done when |
|---|---|---|
| M0 | this file | written |
| M1 | N66Enc definitions: states/domains/TT, atoms, `pyAlloc`/`num`, eager stream, quad clauses, units, rows, seqcounter (fitted to pysat), SB, `fullCnf`, `printClauses` with runtime data, printer exe (bare `lean` + `leanc`, linking ENCBLEAN's objects or a local Std-only build); Python extractor `tools/extract_desc.py` (untrusted: used_ids + layout ranges + trim lines). Byte identity: (a) eager stream and sample quad clauses vs the pinned Python copy; (b) one full cert.cnf vs `full_cnf_sha256`; (c) all 132 trims vs `trim_cnf_sha256`. **COMPUTED.** | 132/132 MATCH |
| M2 | `Model`, derived states, intended assignment, soundness of 4.1-4.11, 4.14, 4.15 (given LEX) | `fullCnf_sat_of_model` axioms-clean |
| M3 | cover + `printClauses_sub` + composition: `∀ R, (∀ c ∈ leaves132, ¬Sat (fullCnf R c)) → ∀ M, (rows hold for M) → (holes ≤ 14) → LEX M → False` | compiles |
| M4 | G1, G2 | |
| M5 | G3 | |
| M6 | G4 + LEX choice | |
| M8 | `n66_bound_55_of_cubes` | axioms audited |
| M9 | hash binding script (E1), self-test | 132/132 |
| M10+ | rows: coupled5 template encoder (Lean) + transport + mirror + cycle ⇒ `RowsValid R0` modulo template/core verdicts | later stage |

---

## 7. Risks

- R1 pysat seqcounter order has no source; mitigated by grid tests against the venv's pysat (exact clause lists).
- R2 Python constant handling in coupled5 (`True/False` literals, dedup, tautology drop, |lit| sort) — mitigated by
  stream hash comparison before the 132 trims.
- R3 printer memory: eager stream materialised (1.49M clauses) + numbering array (≈ 26.5M entries) — estimate below
  1.5 GB; measured with /usr/bin/time -v in the first unit.
- R4 G3 (cap+cup octagon) is new geometry; if it stalls, `noCapCup55` stays a field and the gap is named.
- R5 Machine heat: Tctl was 87.5 °C at 06:30 (gate 86 °C); compiles wait in bounded loops.


---

## 8. As built (22 Nov, 06:15-09:00 KST)

- **Statement.** `N66Geo.n66_bound_55_of_gaps3` (Final3.lean); `CubesUnsat132` (N66Enc/Full.lean) is over
  `fullCnf R0 c`; rows are `List (Fin 70)` (not `List Nat`); `RowValid` uses `n66Occ c.cup n` (states from the
  triple colors alone, so it does not depend on G3); LEX is `LexOcc` (Assembly.lean).
- **Numbering.** `num a = numWith pyMap nAlloc a` with `numWith` generic in the table and the length; all numbering
  lemmas (`decodeWith_numWith`, `numWith_pos`) are proved for a variable list and instantiated at `pyAlloc ()` by
  substitution only (DecodeB.lean). Data definitions are `@[irreducible]`; theorem-only lists are `noncomputable`;
  big generator lists are `Unit →` functions.
- **Printer.** `build/bin/n66print`, linked by hand (`tools/link.sh`: leanc on the IR C of N66Enc and of ENCBLEAN's
  Gen/Dimacs/Coded/Cover/Render, hashes in `logs/freeze_manifest.json`); exe `98d121ba…`; its nine sources are
  frozen since M9 (freeze check PASS). pysat's card extension `36cc2b80…`.
- **Guard stops (clean, no OOM kill):** `stats` (closed constants evaluated at start), `build5`, `build6`, `t7`
  (elaboration/kernel evaluating the numbering table); fixes in DecodeB's docstring.
- **Gaps left (Gaps5, 09:35):** G3 `capCup55`, G4 `mirror` (4.1-4.3 proved in Pair.lean / Pos.lean). Earlier plan notes:
  `pos` via
  `StateInterface.forced_cap/forced_cup` + `actual_incoming_admissible` + min/max bounds of `mnPlain/mxPlain`
  (prove `tt = ttF` through `Array.getElem?_ofFn` without evaluating `ttArr`); `pair` via `rank_attained` and the
  predecessor on the attaining path (N66 README §2.5); `mirror` via `Suk.reflectY`/`orient_reflectY` and a
  combinatorial lemma "cup ↦ !cup swaps the label coordinates, hence transposes the profile" plus `tauList_spec`;
  `capCup55` via `ConvexCycleCuts.hasConvexNGon_of_positive_cycle` on the cyclic order p, cup, q, cap reversed.

- **10:15 update:** G3 and G4 proved (`CapCup.lean`, `MirrorA/B.lean`); end theorem `n66_bound_55_of_cubes`
  (`End.lean`) with `#guard_msgs` axiom guard. The only hypotheses are `CubesUnsat132` and `RowsValid R0`.

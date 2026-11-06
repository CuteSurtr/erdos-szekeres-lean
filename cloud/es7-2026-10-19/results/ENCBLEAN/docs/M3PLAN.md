# ENCBLEAN M3: final plan for `encB_satisfiable` (judge of plans A and B)

Written 2026-11-06, about 16:50 KST. No ENCBLEAN file was edited, and `lake build` was not run there. Every Lean text
below was compiled in scratch with the toolchain's `lean` (v4.24.0, under the 4G cap, nice 10, one file at a time),
against copies of the M2 files whose hashes match ENCBLEAN HEAD `c77541836`:

| file | hash |
|---|---|
| Gen | `ec97b335…` |
| Dimacs | `48cbeac9…` |
| Coded | `2727e00b…` |
| Cover | `c59425ac…` |

**Concurrent edits.** At 16:45, `DESIGN.md` and `README.md` showed uncommitted changes from the other workflow.
They are documentation only: risk R1 is resolved, with 64 of 64 cube verdicts certified, so variant B and M7′ are not
needed. No Lean source changed.

**Directories.**
- `S = /tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/m3plan`
- `F = $S/final` holds the frozen U0 files and the unit starting points (`$F/SHA256SUMS`).
- `$S/judge` holds the judge's build and checks.

**Summary.**
- The final plan is plan B's interface (one change: the critical-path unit is split), with plan A's chain lemmas
  and test controls added.
- There are 6 parallel units between U0 and Integration.
- Integration is already written, and it compiles against stub units.

---

## 0. Checks against the code

### 0.1 The clause families of `genCoded` (enumerated from Coded.lean:281-285)

`genCoded m K t = transCl t ++ ad.flatMap angClOf ++ nest.map (fun l => [l]) ++ (rng 0 t).flatMap (chainCl m K t isF)`,
with `ad = (orbList m t).map fun c => (angOutsC m t c).1` and
`isF = isFalseIn (forcedOf (fBase m t) (ad.filterMap unitOf ++ nest))`.

| # | family | clause shapes (Coded lines) | proved by |
|---|---|---|---|
| 1 | ψ-order transitivity | `[-Y ij, -Y jk, Y ik]`, `[Y ij, Y jk, -Y ik]` over `triples (rng 1 t)` (194-197) | U1 `transCl_sound` |
| 2 | angular, per `c ∈ orbList m t` | unit `[l]` when `unitOf outs = some l`; otherwise `neg prem ++ [l]` for each entry with `o.2 = some l` (204-207). `l` is `±orbCode c` (rule A, Gen:162-165) or `olit a b cc` (rule B, Gen:167-181) | U3 `angCl_sound`, using U1 `orbListSpec` and U4 `patternSpec_of` (which uses U5 `wordSpec`) |
| 3 | nesting units | `[olit (i,0) (i,1) (j,k)]` (210-212, 285) | U1 `nestLits_sound` |
| 4 | chains, per pivot `i ∈ rng 0 t` | base `[F₂(a,b), -l]` (277); extension `[-F_lev(b,c), -lab, -lt, F_{lev+1}(a,b)]` (257-258); closing `[-F_lev(b,c), -lab, -lt]` (259) | U2 `chainCl_sound`, for every `isF` |

**Coverage.**
- Each family is covered exactly once.
- No other clause exists.
- Neither the H variables (odd m only) nor `Var.other` occurs in a clause for even m.
- `isF`, `keys`, the `none` literals and a failing `olit` only drop clauses, so the proofs hold for arbitrary values
  of them.

### 0.2 Claims of the two plans

| claim | plan | how checked | verdict |
|---|---|---|---|
| `Model` = DESIGN §2.2 with `Valid` → `PtOk` | A, B | mechanical token comparison of §2.2's code block against `$F/EncB/Model.lean` | **true** (806 = 806 tokens; Decidable instances and comments excluded) |
| τ needs a `.other` case (M2's fifth `Var` constructor) | A, B | Coded:41-52 | true |
| `hm : 2 ≤ m` suffices (only `(i,1)` in nesting) | A, B | U1 needs it only for `PtOk (i,1)`; Integration compiles with it | true |
| M2 "is not in git" | A | `git ls-files`; commit `c77541836` at 16:20:23 | **outdated**: M2 is committed (A's snapshot was 16:15) |
| 8 parallel units plus a test unit | A | task limit is 6 | **too many**; merged below |
| unit files under `EncB/M3/` | A | `scripts/audit.sh`: `SRCS=$(ls EncB.lean EncB/*.lean)` | would escape the audit; **flat `EncB/Sound*.lean`** (B, and DESIGN M3's names) needs no audit change |
| `olit_sound` needs `Distinct3` | A | B's `OlitSpec` derives distinctness from `orbVarC` | B's form adopted (proved, 94 lines) |
| premises give rank ↔ ψ (iff) | A | the glue below uses only one direction | B's `RkMono` adopted |
| eraseDups needs well-founded induction | A | core `eraseDups = eraseDupsBy (·==·)` with `loop` (Init/Data/List/Basic.lean:2228) | not needed: an accumulator invariant on `eraseDupsBy.loop` is structural |
| prototypes compile, with the listed axioms | B | recompiled `Model`, `ModelLemmas`, `SortLemmas`, `SoundOlit`, `RulesStart`, `AngStart`; `#print axioms` | **true**, exactly as listed |
| `example (M : Model 6 8 11) … := encB_satisfiable (by decide) (by decide) M` | B | ran `scripts/audit.sh` on it | **fails the audit**: `KERNEL EVALUATION RISK … token "example"`. Replaced by `encB_satisfiable_6811` with proof terms (audit PASS, compiles) |
| integration `rcases` shape over `simp only [genCoded, …]` | A, B | compiled (against stubs, and against plan A's probe) | true |
| `mem_levels`, `mem_extItems` | A | recompiled against the final interface | true (axioms: propext / propext, Quot.sound) |
| U5 Rules is the critical path (300–420 LOC) | B | — | **split**: U4 = sorting + glue (glue already compiled), U5 = cyclic words, with a new frozen `SortedSix`/`WordSpec` |
| early-warning test: 0 unsatisfied clauses wherever the laws hold; controls fail | A, B | re-ran B's SIX60 test (log `$S/judge/ewb_run.log`, 188 s) and read A's logs | true: (6,8,5) A, A-mirror, B-mirror, D: 89,530 clauses each, 0 UNSAT, all laws 0. K=5 control: `noChain_fail` 61, chain UNSAT 195. χ(A)/ψ(A-mirror) control: 3 UNSAT |

### 0.3 New checks made by the judge

1. **The `PatternSpec` glue composes.**
   - `Rules.patternSpec_of_sort (hS : SortSixStmt) (hW : WordSpec) M : PatternSpec M` compiles, with no sorry and
     axioms [propext, Classical.choice, Quot.sound].
   - File: `$F/start/SoundRules.lean:139`.
   - So `SortedSix` and `WordSpec` are exactly what rules A and B consume.
2. **`SortedSix` and `WordSpec` are true on the domain that matters.**
   - The check (`$F/start/ew/WordCheck.lean`, `#eval`) covered every ordered triple of distinct labels with
     distinct keys:
     - m ∈ {2,4,6,8}, t = 4;
     - 4 ψ orders;
     - 161,280 triples in all.
   - Result: 0 violations of the `SortedSix` conclusion for `insSort Obj.lt (objsEven …)`, and 0 violations of both
     `WordSpec` conclusions.
   - Alternating words plus PPP words account for every case.
   - Negative control (swapped picks): every triple fails. Run time 35 s.
3. **Integration compiles with the five unit modules stubbed.**
   - Checked with `$F/start/Satisfiable.lean` and the exact frozen statements.
   - The only errors are the two `#guard_msgs` lines, which report `sorryAx` from the stubs; that is what they are
     there to catch.
4. **The audit passes.** `scripts/audit.sh` over M2 plus the final interface, the three starting points and
   `Satisfiable.lean` gives AUDIT PASS.

---

## 1. The frozen interface (unit U0)

U0 copies four files verbatim from `$F/EncB/` (hashes in `$F/SHA256SUMS`):

| file | lines | sha256 | content |
|---|---|---|---|
| `EncB/Model.lean` | 196 | `42240829…` | defs, `Model`, `ChainFrom`, `baseVal`, `tauOf`, `Model.τ`, `Model.τc`, the unit specs, Decidable instances |
| `EncB/ModelLemmas.lean` | 162 | `db0d368b…` | literal semantics, `holds_*`, `perm012_cases`, `chi_perm3`, membership lemmas |
| `EncB/SortLemmas.lean` | 164 | `103f5bd1…` | `mem_perms`, `insSort_perm`, `insSort_pairwise`, `Obj.lt_iff`, position lemmas for strictly sorted lists |
| `EncB/SoundOlit.lean` | 94 | `48631ae6…` | `rotBy`, `chi_rotBy`, `orbVarC_some`, `olitSpec` |

### 1.1 `EncB/Model.lean` (exact text; it starts with `import EncB.Coded` and a module docstring)

```lean
namespace EncB

def rot (m : Nat) (a : Pt) : Pt := (a.1, (a.2 + 1) % m)
def Distinct3 (a b d : Pt) : Prop := a ≠ b ∧ a ≠ d ∧ b ≠ d
def InQ (m t i : Nat) (a : Pt) : Prop := i ≤ a.1 ∧ a.1 < t ∧ a.2 < m ∧ a ≠ (i, 0)
def cell (m : Nat) (o : Pt × Bool) : Nat := if o.2 then o.1.2 else (o.1.2 + m / 2) % m
def objLt (m : Nat) (psiLt : Nat → Nat → Bool) (o o' : Pt × Bool) : Prop :=
  cell m o < cell m o' ∨ (cell m o = cell m o' ∧ psiLt o.1.1 o'.1.1 = true)
def ccwIn {α : Type} (lt : α → α → Prop) (x z y : α) : Prop :=
  (lt x z ∧ lt z y) ∨ (lt y x ∧ lt x z) ∨ (lt z y ∧ lt y x)
def objs6 (a b d : Pt) : List (Pt × Bool) :=
  [(a, true), (b, true), (d, true), (a, false), (b, false), (d, false)]
def KeysDistinct (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) : Prop :=
  ∀ o ∈ objs6 a b d, ∀ o' ∈ objs6 a b d, o ≠ o' → objLt m psiLt o o' ∨ objLt m psiLt o' o
def ArcHasAntipode (m : Nat) (psiLt : Nat → Nat → Bool) (a b d x y : Pt) : Prop :=
  ∃ z ∈ [a, b, d], ccwIn (objLt m psiLt) (x, true) (z, false) (y, true)
def AltCCW (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) : Prop :=
  KeysDistinct m psiLt a b d ∧ ccwIn (objLt m psiLt) (a, true) (b, true) (d, true) ∧
  ArcHasAntipode m psiLt a b d a b ∧ ArcHasAntipode m psiLt a b d b d ∧
  ArcHasAntipode m psiLt a b d d a
def BlockCCW (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) : Prop :=
  KeysDistinct m psiLt a b d ∧ ccwIn (objLt m psiLt) (a, true) (b, true) (d, true) ∧
  ¬ ArcHasAntipode m psiLt a b d a b ∧ ¬ ArcHasAntipode m psiLt a b d b d
-- `Decidable` instances (each `inferInstanceAs`) for objLt, ccwIn [DecidableRel lt], KeysDistinct,
-- ArcHasAntipode, AltCCW, BlockCCW, InQ, Distinct3: used only by the early-warning test.

structure Model (m K t : Nat) where
  chi   : Pt → Pt → Pt → Bool
  psiLt : Nat → Nat → Bool
  psiLt_irrefl : ∀ i, psiLt i i = false
  psiLt_trans  : ∀ i j k, psiLt i j = true → psiLt j k = true → psiLt i k = true
  psiLt_total  : ∀ i j, i < t → j < t → i ≠ j → psiLt i j = true ∨ psiLt j i = true
  psiLt_zero   : ∀ i, 0 < i → i < t → psiLt 0 i = true
  chi_rot   : ∀ a b d, PtOk m t a → PtOk m t b → PtOk m t d →
                chi (rot m a) (rot m b) (rot m d) = chi a b d
  chi_cycle : ∀ a b d, PtOk m t a → PtOk m t b → PtOk m t d → Distinct3 a b d →
                chi b d a = chi a b d
  chi_swap  : ∀ a b d, PtOk m t a → PtOk m t b → PtOk m t d → Distinct3 a b d →
                chi a d b = !chi a b d
  ruleA : ∀ a b d, PtOk m t a → PtOk m t b → PtOk m t d → Distinct3 a b d →
            AltCCW m psiLt a b d → chi a b d = true
  ruleB : ∀ a b d, PtOk m t a → PtOk m t b → PtOk m t d → Distinct3 a b d →
            BlockCCW m psiLt a b d → b.1 ≤ a.1 → b.1 ≤ d.1 → chi a b d = true
  nest  : ∀ i j k, i < j → j < t → k < m → chi (i, 0) (i, 1) (j, k) = true
  noChain : ∀ i, i < t → ∀ q : Nat → Pt,
      (∀ s, s < K - 1 → InQ m t i (q s)) →
      (∀ s, s + 1 < K - 1 → chi (i, 0) (q s) (q (s + 1)) = true) →
      (∀ s, s + 2 < K - 1 → chi (q s) (q (s + 1)) (q (s + 2)) = true) → False

def ChainFrom (m t : Nat) (chi : Pt → Pt → Pt → Bool) (i l : Nat) (a b : Pt) : Prop :=
  ∃ q : Nat → Pt, q 0 = a ∧ q 1 = b ∧ (∀ s, s < l → InQ m t i (q s)) ∧
    (∀ s, s + 1 < l → chi (i, 0) (q s) (q (s + 1)) = true) ∧
    (∀ s, s + 2 < l → chi (q s) (q (s + 1)) (q (s + 2)) = true)

def baseVal (chi : Pt → Pt → Pt → Bool) (psiLt : Nat → Nat → Bool) : Var → Bool
  | .y i j => psiLt i j
  | .orb [a, b, d] => chi a b d
  | _ => false

def tauOf (m t : Nat) (chi : Pt → Pt → Pt → Bool) (psiLt : Nat → Nat → Bool) : Var → Prop
  | .f i l a b => ChainFrom m t chi i l a b
  | v => baseVal chi psiLt v = true

def Model.τ {m K t : Nat} (M : Model m K t) : Var → Prop := tauOf m t M.chi M.psiLt
def Model.τc {m K t : Nat} (M : Model m K t) (n : Nat) : Prop := M.τ (decodeCode m K t n)

def OlitSpec {m K t : Nat} (M : Model m K t) : Prop :=
  ∀ (P Q R : Pt) (l : Int), PtOk m t P → PtOk m t Q → PtOk m t R →
    olit m (orbVarC m t) P Q R = some l → l ≠ 0 ∧ (CodeLitHolds M.τc l ↔ M.chi P Q R = true)
def OrbListSpec (m t : Nat) : Prop :=
  ∀ c ∈ orbList m t, ∃ a b d, c = [a, b, d] ∧ PtOk m t a ∧ PtOk m t b ∧ PtOk m t d ∧ Distinct3 a b d
def RkMono (psiLt : Nat → Nat → Bool) (rk : Nat → Nat) (c : List Pt) : Prop :=
  ∀ x ∈ c, ∀ y ∈ c, rk x.1 < rk y.1 → psiLt x.1 y.1 = true
def PatternSpec {m K t : Nat} (M : Model m K t) : Prop :=
  ∀ (a b d : Pt) (rk h : Nat → Nat) (l : Int), PtOk m t a → PtOk m t b → PtOk m t d → Distinct3 a b d →
    RkMono M.psiLt rk [a, b, d] →
    (patternLit m false (orbVarC m t) [a, b, d] (orbCode m t [a, b, d]) rk h).1 = some l →
    CodeLitHolds M.τc l
def SortSpec : Prop :=
  ∀ (α : Type) (lt : α → α → Bool) (l : List α),
    (insSort lt l).Perm l ∧
    (l.Nodup → (∀ x ∈ l, lt x x = false) →
      (∀ x ∈ l, ∀ y ∈ l, ∀ z ∈ l, lt x y = true → lt y z = true → lt x z = true) →
      (∀ x ∈ l, ∀ y ∈ l, x ≠ y → lt x y = true ∨ lt y x = true) →
      (insSort lt l).Pairwise (fun x y => lt x y = true))
def ObjLtSpec : Prop :=
  ∀ a b : Obj, Obj.lt a b = true ↔
    (a.J < b.J ∨ (a.J = b.J ∧ (a.r < b.r ∨ (a.r = b.r ∧
      (a.kind < b.kind ∨ (a.kind = b.kind ∧ a.idx < b.idx))))))

def objImg (c : List Pt) (o : Obj) : Pt × Bool := (c.getD o.idx (0, 0), o.kind == 1)
structure SortedSix (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) (S : List Obj) : Prop where
  length : S.length = 6
  sorted : S.Pairwise fun o o' => objLt m psiLt (objImg [a, b, d] o) (objImg [a, b, d] o')
  cover  : ∀ x ∈ objs6 a b d, x ∈ S.map (objImg [a, b, d])
  idx_lt : ∀ o ∈ S, o.idx < 3
  points : ((S.filter (·.kind == 1)).map (·.idx)).Perm [0, 1, 2]
def WordSpec : Prop :=
  ∀ (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) (S : List Obj),
    (∀ i, psiLt i i = false) → (∀ i j k, psiLt i j = true → psiLt j k = true → psiLt i k = true) →
    Distinct3 a b d → SortedSix m psiLt a b d S →
    ((S.map (·.kind) = [1, 0, 1, 0, 1, 0] ∨ S.map (·.kind) = [0, 1, 0, 1, 0, 1]) →
      AltCCW m psiLt
        ([a, b, d].getD (((S.filter (·.kind == 1)).map (·.idx)).getD 0 0) (0, 0))
        ([a, b, d].getD (((S.filter (·.kind == 1)).map (·.idx)).getD 1 0) (0, 0))
        ([a, b, d].getD (((S.filter (·.kind == 1)).map (·.idx)).getD 2 0) (0, 0))) ∧
    (∀ st, st < 6 → (S.map (·.kind)).getD (st % 6) 0 = 1 → (S.map (·.kind)).getD ((st + 1) % 6) 0 = 1 →
      (S.map (·.kind)).getD ((st + 2) % 6) 0 = 1 →
      BlockCCW m psiLt ([a, b, d].getD (S.getD (st % 6) default).idx (0, 0))
        ([a, b, d].getD (S.getD ((st + 1) % 6) default).idx (0, 0))
        ([a, b, d].getD (S.getD ((st + 2) % 6) default).idx (0, 0)))

end EncB
```

### 1.2 What U0 proves (compiled; axioms ⊆ {propext, Classical.choice, Quot.sound})

**`ModelLemmas.lean`**
- `codeLitHolds_neg (hx : x ≠ 0) : CodeLitHolds τc (-x) ↔ ¬ CodeLitHolds τc x`
- `codeLitHolds_pos`
- `Model.τc_code`
- `holds_y (hi : i < t) (hj : j < t) : CodeLitHolds M.τc (yLit t i j) ↔ M.psiLt i j = true`
- `holds_orb (PtOk a b d) : CodeLitHolds M.τc (orbCode m t [a, b, d] : Int) ↔ M.chi a b d = true`
- `holds_f (hi : i < t) (hl : l < chainFL K) (PtOk a b) : CodeLitHolds M.τc (fCode m K t i l a b : Int) ↔ ChainFrom m t M.chi i l a b`
- `perm012_cases`
- `chi_perm3`: `M.chi` of `[c0,c1,c2].getD (s.getD j 0) (0,0)`, j = 0,1,2, equals
  `if permSign s > 0 then M.chi c0 c1 c2 else !M.chi c0 c1 c2` for `s.Perm [0,1,2]`
- `mem_rng`, `mem_labels`, `mem_chainQ`, `sublist_of_mem_pairs`, `mem_pairs_of_ne`, `sublist_of_mem_triples`,
  `rng_pairwise`

**`SortLemmas.lean`**
- `mem_perms`, `insSort_perm`, `insSort_pairwise`, `Obj.lt_iff : ObjLtSpec`, `Obj.lt_irrefl`, `sortSpec`
- `rel_getElem_iff`, `ccwIn_getElem_iff`, `ccwIn_consecutive`, `not_ccwIn_adjacent`, `ccwIn_distinct`
- `objLt_irrefl`, `objLt_asymm`

**`SoundOlit.lean`**
- `rotBy`, `ptOk_rotBy`, `chi_rotBy`, `orbVarC_some`
- `olitSpec (M) : OlitSpec M`

### 1.3 Deviations from DESIGN §2.2–2.3 (Integration records them in DESIGN and README)

- `Valid` is dropped in favour of Coded's `PtOk` (the same body).
- τ is `tauOf` with the computable `baseVal` catch-all. It covers `.h` and `.other`; DESIGN's match had no `.other`
  case and would not compile.
- `ChainFrom` takes `m t chi`, not `M`.
- `hm : 2 ≤ m` replaces the guess `4 ≤ m`.
- New: `OlitSpec`, `OrbListSpec`, `RkMono`, `PatternSpec`, `SortSpec`, `ObjLtSpec`, `objImg`, `SortedSix`,
  `WordSpec`.
- M6 is unaffected: no field changed.
- In DESIGN §3.2's lemma map:
  - H1 (`canon`) is needed only for `OrbListSpec`, not for `olit`;
  - H6b needs only one direction (`RkMono`);
  - KS prem uniqueness and KS dich (a) are not needed.

### 1.4 U0 task list (one agent, about 15 minutes)

1. Check the M2 hashes listed at the top (`sha256sum EncB/{Gen,Dimacs,Coded,Cover}.lean`) and that HEAD contains
   `c77541836`. On a mismatch, stop and re-run §0.3 before going on.
2. Copy `$F/EncB/{Model,ModelLemmas,SortLemmas,SoundOlit}.lean` into `ENCBLEAN/EncB/`. Verify them against
   `$F/SHA256SUMS`.
3. Append `import EncB.Model`, `import EncB.ModelLemmas`, `import EncB.SortLemmas` and `import EncB.SoundOlit` to
   `EncB.lean`.
4. Build and audit:
   - run `systemd-run --user --scope -q -p MemoryMax=4G nice -n 10 lake build 2>&1 | tee logs/m3_u0_build.log`;
   - then `bash scripts/audit.sh`, which must print AUDIT PASS.
5. Run `#print axioms` for `olitSpec`, `sortSpec`, `Obj.lt_iff`, `chi_perm3`, `holds_f` and `mem_perms` from a
   scratch file outside ENCBLEAN, with `lake env lean <scratch file>` run from ENCBLEAN. Each must be ⊆ {propext,
   Classical.choice, Quot.sound}. The judge observed: `olitSpec`, `holds_f` and `mem_perms` use [propext,
   Classical.choice, Quot.sound]; `sortSpec`, `Obj.lt_iff` and `chi_perm3` use [propext, Quot.sound].
6. Hand each unit its start file path from `$F/start/` (§2). Committing U0 is the user's or orchestrator's decision.
   The protocol in §2.1 does not need a commit.

---

## 2. Work units (6 in parallel after U0)

### 2.1 Rules for every unit

**Shared directory.** All units work in ENCBLEAN itself. No worktrees are needed.
- Each unit **adds only its own file** `EncB/<File>.lean`.
- No unit edits an existing file (`EncB.lean`, `lakefile.toml`, `scripts/`, M2 or U0 files).
- U6 may also add `scripts/ew_test.sh` and `logs/m3_early_warning.log`.
- No unit imports another unit's file. Dependencies between units are explicit hypotheses only.

**Build.**
- Use only `systemd-run --user --scope -q -p MemoryMax=4G nice -n 10 lake env lean EncB/<File>.lean`.
- **Never `lake build`**: only U0 and Integration write `.lake`.
- Run one compile at a time. The machine is at about 30 of 32 cores (ES(8) campaign until 2026-11-16 17:00).

**Names.**
- The frozen theorem goes in `namespace EncB`, exactly as below.
- Every helper is `private` or lives in the unit's namespace: `EncB.Orbit`, `EncB.Chain`, `EncB.Ang`,
  `EncB.Rules`, `EncB.Word` or `EncB.EW`.
- The file names `SoundOrbit`, `SoundChain`, `SoundAng`, `SoundRules`, `SoundWord`, `EarlyWarning` and
  `Satisfiable` collide with nothing in M2 (checked).

**Forbidden in code** (the `scripts/audit.sh` list): `sorry`, `admit`, `native_decide`, `implemented_by`,
`extern`, `unsafe`, `partial`, `axiom`, `opaque`, `set_option` and `ofReduceBool`. Also forbidden:
- `decide`, `rfl`, `simp` or `#eval` that evaluates `genCoded`, `encB`, `orbList` or `angOutsC` on numerals;
- `simp` or `unfold` of `patternLit` or `angOuts` at concrete lists. That exceeds the 200k heartbeats (found by
  plan B), and `set_option` is forbidden. Use the `rfl` bridges in the start files instead.
- Allowed: `decide` on closed small facts (e.g. `perm012_cases`-style).

**Done when** all of the following hold:
- `lake env lean` of the file prints no error and no `sorry` warning;
- the axioms are ⊆ {propext, Classical.choice, Quot.sound}. Units write no `.olean`, so a separate file cannot
  import theirs. Instead, end the unit file with `/-- info: … -/ #guard_msgs in #print axioms <frozen thm>`
  (KernelCheckB.lean style, with the exact text observed);
- `bash scripts/audit.sh` prints AUDIT PASS (it scans `EncB/*.lean`, so it includes the new file).

### 2.2 Units, exact statements, dependencies

| unit | new file (start from) | exact statement(s) | may assume | est. new LOC | risk |
|---|---|---|---|---|---|
| **U1** orbit list, order, nesting | `EncB/SoundOrbit.lean` (no start) | `orbListSpec`, `transCl_sound`, `nestLits_sound` | U0 | 160–250 | low–medium |
| **U2** chains | `EncB/SoundChain.lean` (from `$F/start/SoundChain.lean`, 77 lines, compiled) | `chainCl_sound` | U0 | 100–170 | low–medium |
| **U3** angular clauses | `EncB/SoundAng.lean` (from `$F/start/SoundAng.lean`, 77 lines, compiled) | `angCl_sound` | U0; `OrbListSpec`, `PatternSpec` **as hypotheses** | 200–300 | medium (longest unit) |
| **U4** patterns: sorting plus glue | `EncB/SoundRules.lean` (from `$F/start/SoundRules.lean`, 171 lines, compiled, glue included) | `patternSpec_of` | U0; `WordSpec` **as a hypothesis** | 100–160 | medium |
| **U5** cyclic words | `EncB/SoundWord.lean` (no start) | `wordSpec` | U0 | 150–230 | medium |
| **U6** early-warning test | `EncB/EarlyWarning.lean` (not imported by `EncB.lean`), `scripts/ew_test.sh`, `logs/m3_early_warning.log` (from `$F/start/ew/*`) | — (evidence, §4) | U0 | 250–350 (merge of prototypes) | low |

```lean
-- U1  EncB/SoundOrbit.lean
theorem orbListSpec (m t : Nat) : OrbListSpec m t
theorem transCl_sound {m K t : Nat} (M : Model m K t) :
    ∀ cl ∈ transCl t, ∃ x ∈ cl, CodeLitHolds M.τc x
theorem nestLits_sound {m K t : Nat} (M : Model m K t) (hm : 2 ≤ m) :
    ∀ l ∈ nestLits m t, CodeLitHolds M.τc l
-- U2  EncB/SoundChain.lean
theorem chainCl_sound {m K t : Nat} (M : Model m K t) (isF : Int → Bool) :
    ∀ i ∈ rng 0 t, ∀ cl ∈ chainCl m K t isF i, ∃ x ∈ cl, CodeLitHolds M.τc x
-- U3  EncB/SoundAng.lean
theorem angCl_sound {m K t : Nat} (M : Model m K t) (heven : m % 2 = 0) (hOL : OrbListSpec m t)
    (hP : PatternSpec M) :
    ∀ c ∈ orbList m t, ∀ cl ∈ angClOf (angOutsC m t c).1, ∃ x ∈ cl, CodeLitHolds M.τc x
-- U4  EncB/SoundRules.lean
theorem patternSpec_of (hW : WordSpec) {m K t : Nat} (M : Model m K t) : PatternSpec M
-- U5  EncB/SoundWord.lean
theorem wordSpec : WordSpec
```

**Dependencies.**

```
U0 ─┬─ U1 ─┐
    ├─ U2 ─┤
    ├─ U3 ─┤   (U3 uses OrbListSpec and PatternSpec only as hypotheses)
    ├─ U4 ─┼─ Integration
    ├─ U5 ─┤   (U4 uses WordSpec only as a hypothesis)
    └─ U6 ─┘   (gate: its base runs must pass; it runs first, within minutes)
```

The critical path is U0 → U3 → Integration. U3 is the largest unit; U4 is now small because its glue is done.

### 2.3 Routes (suggested, not frozen)

**U1 `orbListSpec`**
- `mem_dedupBy`: `x ∈ dedupBy key S l → x ∈ l`, by a foldl invariant, for any `key`. M2's `mem_dedup_foldl` is
  the other direction and only for `id`.
- `labels m t` is `Pairwise ptLt`, via core `List.pairwise_flatMap`, `List.pairwise_map` and `rng_pairwise`. So
  `sublist_of_mem_triples` gives three distinct labels, and `mem_labels` gives `PtOk`.
- `canon m tri = insSort ptLt (rotate m p0.2 tri)` for some `p0 ∈ tri`, by a foldl invariant on `canon`'s `step`.
- `rotate m k tri = tri.map (rotBy m (negMod m k))` holds by `rfl` (as in `olitSpec`).
- `insSort_perm` plus length 3 gives `[a, b, d]`, and `ptOk_rotBy` gives `PtOk`.
- `rotBy` is injective on sectors `< m`: case split on `x + s % m < m`, after `Nat.add_mod`, then omega.

**U1 `transCl_sound`**
- Uses `sublist_of_mem_triples`, `rng_pairwise`, `mem_rng`, `holds_y` and `codeLitHolds_neg` (`yLit ≥ 1`).
- Clause 1 is `psiLt_trans`.
- Clause 2: totality twice, then trans, then irrefl.

**U1 `nestLits_sound`**
- Uses `List.mem_flatMap`/`mem_filterMap` and `mem_rng`.
- Then `(olitSpec M …).2` together with `M.nest`; `PtOk (i, 1)` comes from `hm`.

**U2**
1. Split `chainCl` into the base part (`okL.map`) and the fold. `Chain.mem_levels` with initial `st.2 = []`,
   `Chain.mem_extItems` and `Chain.mem_okList` are compiled.
2. Get `InQ`/`PtOk` from `mem_chainQ`, and `i < t` from `mem_rng`.
3. Level bounds for `holds_f`: `2 < chainFL K`, `lev < K - 1 ≤ chainFL K`, `lev ≥ 2` (from `mem_rng`).
4. Base clause: `q s := if s = 0 then a else b`.
5. Extension clause: `q' s := if s = 0 then a else q (s - 1)`.
6. Closing clause: `lev + 1 = K - 1`, then `M.noChain i hi q'`.
7. Literals: `olitSpec` (`l ≠ 0`) and `codeLitHolds_neg`.

**U3**
- `Ang.angOutsC_even heven` rewrites `angOutsC` to `angOuts m false …`.
- `Ang.mem_angOuts_even` and `Ang.mem_angOuts_even'` give the entries and their converse.
- `Ang.unitOf_some` handles the unit case.
- `c = [a,b,d]` comes from `hOL`.
- `free`: its members are the nonzero layers of `c`.
  - eraseDups: the invariant `x ∈ eraseDupsBy.loop r as bs ↔ x ∈ as ∨ x ∈ bs`, plus Nodup.
  - Then `insSort_perm`.
- Premise literals are `±yLit` of pairs of `free`; they are nonzero, and `holds_y` applies.
- (i) All premises true ⇒ `RkMono`. Layer 0 uses `psiLt_zero` and `rk 0 = 0`. Two free layers use the pair premise
  and `psiLt_total`.
- (ii) Existence of an all-true pattern:
  - `s := insSort M.psiLt free`, `ranks := free.map s.idxOf`;
  - `ranks ~ range n`, via `Perm.map` and `l.Nodup → l.map l.idxOf = range l.length`;
  - then `mem_perms`, and `lookup L (free.zip (free.map f)) = some (f L)`.
- (iii) Unit case: the true pattern carries `l`, so `hP` applies. Conditional case: either a false premise, whose
  negation is in the clause, or `hP`.

**U4**
- Prove `Rules.sortSix : Rules.SortSixStmt`. The statement is in the start file.
- Then `patternSpec_of hW M := Rules.patternSpec_of_sort Rules.sortSix hW M`.
- For `sortSix`:
  - `objsEven_three` (`rfl`) gives the six objects explicitly.
  - Distinct keys make the objects Nodup and the key injective on them.
  - `Obj.lt_iff` plus omega make `Obj.lt` transitive, and total on distinct keys; `insSort_pairwise` follows.
  - `List.Pairwise.imp_of_mem` carries the order to `objLt ∘ objImg`. On these objects `cell (objImg o) = o.J` and
    `o.r = rk (objImg o).1.1`. When J are equal and r differ, use `RkMono`; when J and r are both equal the keys are
    equal, a contradiction.
  - `cover`, `idx_lt` and `points` follow from `insSort_perm` with `Perm.filter`/`Perm.map`.

**U5**
- Let `L := S.map (objImg [a,b,d])`. It is `Pairwise objLt` (`List.pairwise_map`) and has length 6.
- `objLt` is irreflexive and asymmetric (`objLt_irrefl`, `objLt_asymm`).
- Reason on positions with `ccwIn_getElem_iff`, `ccwIn_consecutive` and `not_ccwIn_adjacent`, using omega. Avoid
  6×6 case splits.
- Each element of `objs6 a b d` is some `L[q]` (`cover`, `List.mem_iff_getElem`).
- Alternating case: the points sit at {0,2,4} or {1,3,5}, and the antipodes in between, including the wrap-around.
  `points` gives that the antipode labels lie in `[x, y, z]`.
- Block case: there is nothing strictly between cyclically adjacent positions.

**U6** — see §4.

---

## 3. Integration unit (last; one agent)

1. Copy `$F/start/Satisfiable.lean` (52 lines) to `EncB/Satisfiable.lean`. It contains:
   - `genCoded_sound`;
   - `encB_satisfiable {m K t} (heven : m % 2 = 0) (hm : 2 ≤ m) (M : Model m K t) : DimacsSatisfiable (encB m K t)`;
   - `encB_satisfiable_6811 (M : Model 6 8 11) : DimacsSatisfiable (encB 6 8 11) := encB_satisfiable (Nat.mul_mod_right 2 3) (Nat.le_add_left 2 4) M`,
     which uses no `decide`, so the audit passes;
   - two `#guard_msgs in #print axioms` expecting `[propext, Classical.choice, Quot.sound]`.

   The judge compiled it against stub units; the only errors were the two guards, which saw `sorryAx`.
   Its core:

   ```lean
   theorem genCoded_sound {m K t : Nat} (heven : m % 2 = 0) (hm : 2 ≤ m) (M : Model m K t) :
       ∀ cl ∈ genCoded m K t, ∃ x ∈ cl, CodeLitHolds M.τc x := by
     intro cl hcl
     simp only [genCoded, List.mem_append, List.mem_flatMap, List.mem_map] at hcl
     rcases hcl with ((hcl | ⟨outs, ⟨c, hc, rfl⟩, hcl⟩) | ⟨l, hl, rfl⟩) | ⟨i, hi, hcl⟩
     · exact transCl_sound M cl hcl
     · exact angCl_sound M heven (orbListSpec m t) (patternSpec_of wordSpec M) c hc cl hcl
     · exact ⟨l, List.mem_singleton_self _, nestLits_sound M hm l hl⟩
     · exact chainCl_sound M _ i hi cl hcl
   theorem encB_satisfiable {m K t : Nat} (heven : m % 2 = 0) (hm : 2 ≤ m) (M : Model m K t) :
       DimacsSatisfiable (encB m K t) :=
     dimacsSatisfiable_of_holds M.τ (genCoded_sound heven hm M)
   ```

2. Append to `EncB.lean` the imports of `EncB.SoundOrbit`, `EncB.SoundChain`, `EncB.SoundAng`, `EncB.SoundRules`,
   `EncB.SoundWord` and `EncB.Satisfiable`. `EarlyWarning` is not imported.
3. Build and audit:
   - run `lake build` under the cap, logging to `logs/m3_build.log`;
   - `scripts/audit.sh` must pass (`logs/audit.log`);
   - regenerate `logs/axioms.log` with the recorded query (`logs/axioms_query.lean.txt`), covering every new
     declaration.
4. **Mutants**, in a scratch copy, never in ENCBLEAN; log to `logs/m3_mutants.log`.
   - Delete each of the 13 `Model` fields in turn; the build must fail every time. Users of each field:

     | field | used by |
     |---|---|
     | `psiLt_irrefl`, `psiLt_trans` | U1, U4, U5 |
     | `psiLt_total` | U1, U3 |
     | `psiLt_zero` | U3 |
     | `chi_rot`, `chi_cycle`, `chi_swap` | U0 (`olitSpec`, `chi_perm3`) |
     | `ruleA`, `ruleB` | U4 |
     | `nest` | U1 |
     | `noChain` | U2 |

   - Negate the literal in `nestLits` in a scratch Coded copy. `nestLits_sound` must break, and the early-warning
     run must report `nest_UNSAT > 0`.
5. Re-run `scripts/ew_test.sh` once; the result must be unchanged.
6. Documentation:
   - update README (new section "M3") and DESIGN (§1.3 deviations, §3.2 lemma map, the M3 row and the LOC
     estimate);
   - fix DESIGN §1.1's sketch: M8 should call `encB_satisfiable_6811` or use proof terms, not `by decide`, next to
     `encB 6 8 11`.

   Committing is the user's or orchestrator's decision.

**Fallback if a unit stalls.** Ship `encB_satisfiable_of` with the stalled unit's statement as an explicit
hypothesis (for example `(hW : WordSpec)`), name it in the README, and use no sorry. The likely candidates are U5
and then U3.

---

## 4. Early-warning test (unit U6; evidence only, never a kernel computation)

**What it is.** `EncB/EarlyWarning.lean` has `namespace EncB.EW` and `def main : IO Unit`. It imports only
`EncB.Model` (plus Gen and Coded through it). Run it as follows:

```
systemd-run --user --scope -q -p MemoryMax=4G nice -n 10 lake env lean --run EncB/EarlyWarning.lean \
  | tee logs/m3_early_warning.log
```

This is interpreted, needs no lakefile change, and does not write `.lake`. `scripts/ew_test.sh` wraps the command
and exits nonzero on failure.

**Parts.** U6 merges the prototypes in `$F/start/ew/`:

- **(a) SIX60, base runs** (`EW6_six60.lean`, from plan B).
  - Configurations: exact layer representatives of `SIX60/sets/c6_60pts_{A,B,C,D}` in the Eisenstein basis. `chi`
    is the sign of the integer determinant, and `psiLt` comes from ranks.
  - Chain variables: a level DP (the least fixpoint of the base and extension clauses = `ChainFrom`, not proved
    equal).
  - Laws: all 13 `Model` fields are checked as Bools over valid labels, using the interface's own `Decidable`
    instances for `AltCCW`/`BlockCCW`.
  - Clauses: every clause of `genCoded`, per family, is counted as unsatisfied or not under `baseVal`/`decodeCode`.
    That is the theorem's own τ on Y and orbit codes.
  - Runs: (6,8,3) for A, B, C, D and their mirrors; (6,8,5) for A and D.
- **(b) Non-monotone ψ** (`EW6_nonmono.lean`): A layers [0,2,5,7,9] (t=5) and D layers [0,3,6,9] (t=4), with
  mirrors.
- **(c) m = 4** (`EW4_squares.lean`): Gaussian nested squares sq2–sq4, K ∈ {6, 8}, with mirrors.
- **(d) Statement check** (`WordCheck.lean`, by the judge): the `SortedSix` and `WordSpec` conclusions for
  m ∈ {2,4,6,8}, t = 4, 4 ψ orders.
  - Copy `objsEven` into `EncB.EW`; do not import `EncB.SoundRules`.
- **Controls:**

  | control | expected result |
  |---|---|
  | K=5 on A, t=3 | `noChain_fail` 61; only chain clauses unsatisfied (195) |
  | χ(A) with ψ(A-mirror), t=4 | 3 unsatisfied |
  | mirrored χ at (6,8,3) (plan A's mutant 1; port it from `EW_planA_mutants.lean` to the frozen interface) | ruleA/ruleB/nest violations, about 164 unsatisfied clauses |
  | sq4 at K=6 (contains a convex hexagon) | `noChain` fails, chain clauses only |
  | WordCheck with swapped picks | every triple fails |

**Pass criterion** (printed as one `EW SUMMARY` line):
1. Every run where all law counts are 0 has `genCoded_UNSAT = 0`. Never may all laws hold while a clause fails.
2. Every base run in (a)–(c) has all law counts 0, so the check is not vacuous. sq4 at K=6 is a control.
3. WordCheck has 0 violations.
4. Every control is nonzero.

**Already run** (prototypes, against the final `Model.lean`):
- B's (a): 188 s, 0 UNSAT, controls as in §0.2.
- WordCheck: 35 s, 0 violations; the mutant fails everywhere.
- Plan A's synthetic ℤ[√3] runs also report 0 failures where the laws hold (`$S/ew_run2.log`, `ew_run3.log`,
  `ew_run4.log`, `stmt_check.log`).

The merged default `main` should take about 4–6 minutes interpreted.

**Gate.** U6 runs this within its first 15 minutes against the frozen `Model.lean` and reports. A failing base run
means the interface is wrong: the orchestrator stops U1–U5 and returns to U0. Integration requires a passing log.

---

## 5. Risks and mitigations

| # | risk | likelihood / impact | mitigation |
|---|---|---|---|
| 1 | The interface is wrong: a family needs a fact the `Model` cannot state, or a field is false for real configurations (blocks M6) | low / rework of M3 and M6 | Every family reduces to listed fields (§0.1, §3 mutant table). `Model` is token-identical to DESIGN §2.2. Early-warning test: 0 failures on exact SIX60 data at K=8. U6 gate. |
| 2 | A frozen intermediate statement (`OlitSpec`, `OrbListSpec`, `PatternSpec`/`RkMono`, `SortedSix`/`WordSpec`) is mis-stated | low / one unit reworked | `OlitSpec` is proved. The glue `patternSpec_of_sort` is compiled. Integration is compiled against stubs. `SortedSix`/`WordSpec` conclusions: 0 violations over 161,280 triples, and the mutant fails. |
| 3 | Elaboration or heartbeat blowups (no `set_option` allowed) | medium / slows U3–U5 | `rfl` bridges: `patternLit_even`, `patternCore_cases` (`generalize insSort Obj.lt objs = S`), `mem_angOuts_even`, `angOutsC_even`. Never unfold `patternLit` or `angOuts` at concrete lists. Work on positions with omega, not case trees. |
| 4 | Kernel evaluation of `encB 6 8 11` | low / build hangs | Theorems are generic in m K t. `encB_satisfiable_6811` uses proof terms. `audit.sh` check 4 (it rejects plan B's `by decide` example; verified). |
| 5 | Name clashes or shared-file edits between parallel units | low / Integration fails | Frozen names only in `EncB`; helpers in unit namespaces or `private`. Only U0 and Integration edit `EncB.lean`; nobody else edits existing files. |
| 6 | Concurrent `.lake` writes | low / corrupt build | Units use only `lake env lean` and `lean --run`; only U0 and Integration run `lake build`. |
| 7 | Machine load (ES(8) campaign, about 30/32 cores, until 2026-11-16 17:00) | certain / slower | 4G `MemoryMax` scope and nice 10 on every compile, one compile per agent at a time. Std-only files compile in about 1 s. Run the early-warning test once in U6 and once in Integration, not in loops. |
| 8 | M2 drift (`patternLit`, `angOuts`, `olit`, `orbList`, `chainCl`, `extItems` or `decodeCode` change) | low / bridges break | U0 and Integration check the four M2 hashes. On a change, recompile `$F/EncB` and `$F/start` before going on. |
| 9 | A unit stalls (most likely U5 words or U3 existence) | medium / delay | Fallback with the statement as an explicit hypothesis, no sorry (§3). Routes and compiled position lemmas are given (§2.3). |
| 10 | Vacuity: for K ≤ 2, `noChain` makes `Model` uninhabited | — / none at K=8 | Irrelevant at K=8. Test data satisfies every law (as Bools). M6 constructs the `Model` from geometry. |
| 11 | Odd m is not covered (`heven`) | certain / scope | As DESIGN R9: m = 7 stays a written proof. The theorem states `m % 2 = 0`. |
| 12 | DESIGN §1.1's `(by decide) (by decide)` trips a text audit in M8 | medium / M8 audit fails | Use `encB_satisfiable_6811` (Integration step 6). |

**Size.** About 0.9–1.4k new proof lines across U1–U5. A further 0.9k is already written: U0 616 lines, the starts
325, Integration 52. DESIGN estimated 1.0–1.3k for M3.

## 6. Files

**Frozen U0 files** (copy verbatim; hashes in `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/m3plan/final/SHA256SUMS`):
- `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/m3plan/final/EncB/Model.lean`
- `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/m3plan/final/EncB/ModelLemmas.lean`
- `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/m3plan/final/EncB/SortLemmas.lean`
- `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/m3plan/final/EncB/SoundOlit.lean`

**Unit starting points:**
- U2: `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/m3plan/final/start/SoundChain.lean`
- U3: `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/m3plan/final/start/SoundAng.lean`
- U4: `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/m3plan/final/start/SoundRules.lean`
- Integration: `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/m3plan/final/start/Satisfiable.lean`
- U6: `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/m3plan/final/start/ew/` (`EW6_six60`, `EW6_nonmono`, `EW4_squares`, `WordCheck`, `EW_planA_mutants`)

**Judge checks:**
- glue: `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/m3plan/judge/src/Judge/Glue.lean`
- integration against stubs: `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/m3plan/judge/src/Judge/Integ2.lean`
- statement check: `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/m3plan/judge/src/Judge/WordCheck.lean`, and its mutant `WordCheckMut.lean` in the same directory
- early-warning re-run: `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/m3plan/judge/ewb_run.log`
- audit runs: `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/m3plan/judge/audit2/` (PASS) and `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/m3plan/judge/audit/` (plan B's example: FAIL)
- compile helper: `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/m3plan/judge/chk.sh`

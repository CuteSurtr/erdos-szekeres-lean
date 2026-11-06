# ENCBLEAN: a Lean-verified encoder B for the k = 8 sixfold bound — design (M0) and lemma map

Written 2026-11-06, about 14:30 KST, by the M0 step of the workflow `encb-lean-m0-m1`. Nothing in this file has been
compiled. The Lean blocks below are specifications: names, signatures and the order of hypotheses are frozen here,
and proofs are not written yet. Line numbers refer to the files as they were at that time.

**Revision (2026-11-06, about 15:00 KST, fixer step after the review).** Every `Gen:` citation now refers to
`EncB/Gen.lean` with SHA-256 `ec97b335…` (most were two lines low, because Gen grew after this file was written; each was re-read and corrected). Other
changes in this revision: the text rendering of the emitter is named in the trust list (E3/E4, §1.4); the chain
variable code of §3.1 uses `FL = max (K−1) 3` instead of `K`; the sketch of `sixfold66_of_unsat` passes both
side conditions of `encB_satisfiable`; M9 emits the cubes from the Lean list `cubes64`.

**Revision (2026-11-06, about 15:50 KST, M2 step).** M2 is implemented: `EncB/Dimacs.lean`, `EncB/Coded.lean`,
`EncB/Cover.lean` and `EncB/KernelCheckB.lean`. The names of §3.1 and §1.1 are kept: `genCoded`, `allCodes`,
`encB`, `numVars`, `numberMap_getD`, `decode_numberMap`, `decodeCode`, `dimacsSat_of_holds`, `encB_wf`,
`covers_signPatterns`, `not_dimacsSatisfiable_of_cover`, `signPatterns`, `cubes64`, `CubesUnsat64`,
`encB_unsat_of_cubes64`. The code-decoding theorem is `decodeCode_code`. Deviations from §3.1 (details and reasons
in `README.md`, "M2"):
1. `numberMap` is an `Array Nat` indexed by the code, not a `Std.HashMap`; the kernel cannot reduce `HashMap`'s
   `USize` indexing.
2. `orbVar := orbVarC`, a code only for three distinct valid labels, instead of `some ∘ orbCode` (mirrors Gen's
   `orbTab` lookup and Python's `KeyError`).
3. `okpair` is not a map; the extension step recomputes `olit p a b`.
4. `Var` has a fifth constructor `other n` (codes outside every range; τ maps it to `False`).
5. The even kernel instance is (6,4,1); `encB 4 4 2` exceeds 8 GB in the kernel.
6. `encB`, `numVars` and `allCodes` are fields of one `encode m K t`, so that they are computed once
   (`encB_eq`, `numVars_eq`, `allCodes_eq` hold by `rfl`).
7. `cubes64 := signPatterns cubeVars64` with `cubeVars64 := [1, 2, 3, 10, 11, 18]` (the same term as §1.1).

**Revision (2026-11-06, about 16:20 KST, M2 review fixes).**
- `EncB/KernelCheckB.lean` also kernel-checks (4,5,1) for `encB` and `gen`, the only kernel instance with K > 4,
  so a chain of two levels.
- `scripts/audit.sh` checks every declaration that mentions the (6,8,11) instance, not just single lines, and also
  forbids `set_option` and `ofReduceBool`.
- `logs/axioms.log` covers every declaration of the package.

No definition or statement changed (README, "M2 review fixes").

**Revision (2026-11-06, about 16:35 KST, risk R1 resolved).** The unit `c6upper-noty12` finished at 15:40:35 KST:
cake_lpr accepted all 32 n-cubes (base + ¬Y(1,2) + pattern), 32/32, hash-bound, and `verify_final64.py` prints PASS.
The record is `C6UPPER/noty12-2026-11-06/` (`README.md`, `results.tsv`, `cubes.sha256`, `verify_final64.log`). With
the 32 encoder-B c-cubes of the replay, all 64 verdicts of `CubesUnsat64` are certified, so **variant A is the
primary target with every verdict in hand**; variant B (§1.2) and M7′ are not needed. Updated here: D1, E1, E2, M9,
R1 and Appendix B. KS line numbers in this file refer to `k8_soundness_p1.tex` before its revision of the same day
for this record (source `248bf037…`); that revision added Theorem (a′) and moved later lines down. No definition or
statement changed.

**Revision (2026-11-06, about 17:35 KST, M3 done).** M3 is implemented as planned in `docs/M3PLAN.md`. The frozen
interface (unit U0) is `EncB/Model.lean`, `ModelLemmas.lean`, `SortLemmas.lean` and `SoundOlit.lean`. The units are
`SoundOrbit` (U1), `SoundChain` (U2), `SoundAng` (U3), `SoundRules` (U4) and `SoundWord` (U5). The assembly is
`Satisfiable.lean`, and the early-warning test is `EarlyWarning.lean` (U6). `encB_satisfiable {m K t}
(heven : m % 2 = 0) (hm : 2 ≤ m) (M : Model m K t) : DimacsSatisfiable (encB m K t)` and `encB_satisfiable_6811` are
proved with axioms [propext, Classical.choice, Quot.sound] and no other hypothesis (README, "M3"). Deviations
from §2.2–2.3 (plan §1.3):
1. `Valid` is dropped in favour of Coded's `PtOk` (Coded.lean:76), which has the same body, `a.1 < t ∧ a.2 < m`.
2. τ is `tauOf m t chi psiLt`:
   - `.f i l a b ↦ ChainFrom m t chi i l a b`;
   - every other variable gets the computable `baseVal`: `.y i j ↦ psiLt i j`, `.orb [a, b, d] ↦ chi a b d`, false
     otherwise.

   This covers `.h` and M2's fifth constructor `.other`. The match of §2.3 had no `.other` case and would not compile.
   `Model.τ := tauOf m t M.chi M.psiLt` and `Model.τc n := M.τ (decodeCode m K t n)`.
3. `ChainFrom` takes `m t chi`, not `M`.
4. `hm : 2 ≤ m` replaces the guess `4 ≤ m` of §2.3. Only the nesting family needs it, to make `(i, 1)` a valid label.
5. New definitions in `Model.lean` state the interfaces between the units: `OlitSpec`, `OrbListSpec`, `RkMono`,
   `PatternSpec`, `SortSpec`, `ObjLtSpec`, `objImg`, `SortedSix` and `WordSpec`. Each is proved (`olitSpec`,
   `orbListSpec`, `patternSpec_of`, `sortSpec`, `Obj.lt_iff`, `wordSpec`), so none is a hypothesis of the final
   theorem.
6. No field of `Model` changed: the judge's token comparison of §2.2 with `Model.lean` (plan §0.2) gives 806 = 806
   tokens. M6 is therefore unaffected. `Model.lean` adds `Decidable` instances, which only the early-warning test uses.
7. In the lemma map §3.2:
   - H1 (`canon`) is needed only for `OrbListSpec`, not for `olit`;
   - H6b needs one direction only (`RkMono`: if every premise holds, the local ranks follow ψ);
   - the uniqueness part of KS prem and KS dich (a) are not needed;
   - H7 is the `rcases` in `genCoded_sound`, not a file of its own.

   The file names differ from the original M3 row of §4, which is now updated: `SoundOrder` and `SoundNest` became
   part of `SoundOrbit`, and `SoundRules` and `SoundWord` are new. The as-built map is at the end of §3.2.
8. §1.1's sketch now calls `encB_satisfiable_6811`. The old `encB_satisfiable (by decide) (by decide)` next to
   `encB 6 8 11` fails `scripts/audit.sh` check 4 (tested, `logs/audit.log`).

**Revision (2026-11-06, about 19:45 KST, M9 A2 and the fixes of its verification).** The twin now prints through
`EncB/Render.lean`, a Std-only printer with a proved round trip through the reference parser `parseDimacs`; M2's
twin printer (`bodyL`, `cubeBody`, `cubeBody_eq`) is removed from Emit.lean. Updated here: E1 (checked, 68/68),
E3 and E4 (narrowed to what A2 leaves trusted), the M9 row's Emit line numbers, the status list of §4 and
Appendix A item 8. No definition or statement of M0–M3 changed.

**Revision (2026-11-06, about 20:15 KST, M9 done).** M9 is done (not committed): the hash binding (A1, E1), the proved
DIMACS round trip (A2, E3/E4), the re-solve script and build recipe (A3, E2 provenance), each checked by an
independent verifier or reviewer and fixed, and the write-up (README "M9" and the E1–E6 table in its "Trust"; P1's
trust and gap text). Updated here: the E2 provenance row of §1.4, the M9 row of §4 with a comparison of "done when"
and what was built (below the table), the done list of §4, and R7. No definition or statement of M0–M3 changed.

**Revision (2026-11-06, about 20:55–21:06 KST, M9 review fixes).** The findings of two reviews of M9 were applied (README,
"M9 review fixes"; not committed). New module `EncB/Compose.lean` (not imported by the exe, which is unchanged):
the round trip on the UTF-8 bytes (`parseDimacsBytes`, `cnfText_ascii`, `parseDimacsBytes_cube64_get`) and the
composition of M3 with the text theorems, `no_model_6811_of_texts` / `no_model_6811_of_bytes`. `scripts/audit.sh`
forbids more tokens near (6,8,11) and has a time gate; `scripts/hash_binding.sh` checks that the build is up to date,
runs a copy of the exe and checks the range of `twin-cube64`. Updated here: E2 provenance (cost from the records, the
p1.tex line, the provenance of the cake_lpr source pins) and E3 (the parser agreement is not verified; the bytes) in
§1.4, the M9 comparison table, the done list of §4 and R7. No definition or statement of M0–M3 changed.

**Paths.** Paths are relative to `R = cloud/es7-2026-10-19/results/` unless they are absolute. Abbreviations:

| short | file |
|---|---|
| LL | `LAYERLEAN/LayerLemma.lean` |
| KS | `WRITEUP/P1/k8_soundness_p1.tex` |
| B | `C6UPPER/encb/gen_b2.py`, SHA-256 `3d47459a…` |
| Gen | `ENCBLEAN/EncB/Gen.lean` (the M1 port, written in parallel by the M1 step) |

**Inputs.** This design follows the plan `p1lean-design.md`, the critique `p1lean-crit.md` (where the two conflict,
the critique wins) and the reader reports `p1lean-{o,e,l}.md`, all in the session scratchpad. Every Lean statement
cited below was re-read at the given line.

---

## 0. Decisions

| # | Decision | Why |
|---|---|---|
| D1 | **The primary target is variant A**: F_B itself is UNSAT, shown by 64 cubes on Y(1,2), Y(1,3), Y(1,4), Y(2,3), Y(2,4), Y(3,4). No Y(1,2) symmetry breaking, so no reflection milestone (M7 is dropped). Variant B (32 cubes, Y(1,2) assumed) was kept only as a fallback (§1.2); since R1 is resolved it is not needed. | The re-solve `c6upper-noty12` of the 32 NOT-Y(1,2) cubes finished at 15:40:35 KST with 32/32 ACCEPTED and `verify_final64.py` PASS (`C6UPPER/noty12-2026-11-06`), so all 64 verdicts are certified (R1 resolved; at 14:27, when this was written, 4/32 were ACCEPTED). This drops KS Lemma refl, Lemma affine and S10 entirely. |
| D2 | **Two packages.** `R/ENCBLEAN` is Std-only: no `[[require]]`, builds in seconds. A later `R/ENCBLEAN/geo` requires Mathlib and the repository (M4 onwards, after the campaign cutoff). | Critique §2: H's `Dimacs.lean` and H3's `Cover.lean` pull in Mathlib. The definitions are copied, not imported. |
| D3 | **The theorem is about a functional twin `encB` of M1's `gen`** (§3.1). M1's imperative `gen` stays as a fast oracle. The emitter that binds hashes (E1) prints `encB`. | Gen is an `Id.run do` loop with mutable `Array` tables and a counter (Gen:240-380). Soundness proofs over that are brittle. Its pure helpers (`canon`, `olit`, `angOuts`, `patternLit`, `unitOf`, `perms`, `pairs`, `triples`, `permSign`, `insSort`) are reused unchanged. |
| D4 | **Soundness never depends on numbering correctness.** Every literal of `encB` decodes, by construction, to a variable whose meaning is fixed. Python's exact numbers are checked only by bytes. | The plan's "translation validation" idea, made structural. |
| D5 | **Interfaces.** The combinatorial `Model` that `encB_satisfiable` consumes states the angular rules on the *exact circular order of objects* (cell, then ψ-order), not on the generator's per-pattern keys. The geometric `PolarLabelling` is what M5 produces. One definition, `modelOfLabelling`, connects them (§2). | Critique §4.2: the key-to-circular-order step must be proved, not assumed. With this cut, M3 proves that the code implements the order spec, and M6 proves that the spec holds for real directions. |
| D6 | **Phase offset φ instead of normalising θ₀ = 0.** P(i,k) = polar c rᵢ (φ + ψᵢ + 2πk/6). | `orient_polar` (LL:935) depends only on differences of directions. Normalising would need a rotation of T (KS Lemma affine); the offset needs nothing. |
| D7 | **Weak radius order** rⱼ ≤ rᵢ for i ≤ j. Strictness is not part of the interface. | Rule B (LL:974) needs only `≤`. Nesting and chains do not use radii. Strictness is true, but it would be a new lemma with no consumer. |
| D8 | **No `Equiv.Perm`, no `word_dichotomy` and no bijection Λ → T on the critical path.** | §3.5 rows 1, 7 and 9: the encoder needs less than the KS chain. |
| D9 | **The kernel never evaluates `encB 6 8 11`.** `encB_satisfiable` is proved for general `m K t`. The cube cover is proved structurally (`covers_signPatterns`), not by `decide` on data. | Plan risk 5. |

---

## 1. The target theorem and the trust base

### 1.1 Variant A (primary): no Y(1,2), 64 cubes

```lean
-- ENCBLEAN/geo/ES8Geo/Main.lean   (Mathlib side; after the cutoff)
namespace EncB.Geo
open ErdosSzekeres ErdosSzekeres.LayerLemma

/-- The 64 sign patterns of variables 1, 2, 3, 10, 11, 18 of B(6,8,11)
    (= Y(1,2), Y(1,3), Y(1,4), Y(2,3), Y(2,4), Y(3,4), gen_b2.py:36-39 with t = 11), in mkcubes order:
    the 32 `c`-cubes (unit +1) first, then the 32 `n`-cubes (unit −1); inside each half,
    product((1,0), repeat=5) over the last five (C6UPPER/tools/mkcubes.py:16-20; noty12.py:76-78). -/
def cubes64 : List (List Int) := EncB.signPatterns [1, 2, 3, 10, 11, 18]

/-- The only external input: one cake_lpr verdict per cube file. -/
def CubesUnsat64 : Prop :=
  ∀ c ∈ cubes64, ¬ EncB.DimacsSatisfiable (EncB.cubeCnf (EncB.encB 6 8 11) c)

theorem encB_unsat_of_cubes64 (h : CubesUnsat64) : ¬ EncB.DimacsSatisfiable (EncB.encB 6 8 11) :=
  EncB.not_dimacsSatisfiable_of_cover (EncB.covers_signPatterns (by decide)) h
  -- `by decide` only checks that the six numerals are ≠ 0; it never touches `encB`

theorem sixfold66_of_unsat (h : ¬ EncB.DimacsSatisfiable (EncB.encB 6 8 11)) : Sixfold66   -- LL:1102
-- proof: intro T c hgp hc hinv hcard; by_contra hno;
--        obtain ⟨L⟩ := labelling_of_counterexample (m := 6) (K := 8) (t := 11) … hgp hc hinv hno hcard  (M5)
--        exact h (EncB.encB_satisfiable_6811 (modelOfLabelling … L))                              (M6, M3)
--        -- `encB_satisfiable_6811` (Satisfiable.lean:43) discharges `heven : 6 % 2 = 0` and `hm : 2 ≤ 6` with
--        -- proof terms; a `by decide` here would fail audit check 4 (it sits next to `encB 6 8 11`)

theorem sixfold66_of_cubes64 (h : CubesUnsat64) : Sixfold66 :=
  sixfold66_of_unsat (encB_unsat_of_cubes64 h)

theorem sixfold_es8 (h : CubesUnsat64) (S : Finset Point) (c : Point) (hgp : GeneralPosition S)
    (hinv : Invariant (rotAbout c (2 * Real.pi / 6)) S) (hcard : 61 ≤ S.card) :
    HasConvexNGon 8 S :=
  sixfold_octagon (sixfold66_of_cubes64 h) S c hgp hinv hcard                                   -- LL:1113

-- Audit (M8): #guard_msgs on #print axioms sixfold_es8 = [propext, Classical.choice, Quot.sound]
```

- **The statement is P1's thm:main(a) for m = 6.** `Invariant` (LL:105) only asks that the rotation maps S into
  itself, so the Lean hypothesis is weaker than P1's.
- **Optional add-on (critique §1).** Cor. cor:es8 for j = 5, i.e. invariance under ρ⁻¹, is a few lines on top of
  `sixfold_es8`.
- **No geometric meaning is attached to the cube variables.** The cover holds for any six nonzero variables, so
  `B_m6K8t11.meta.json` and `verify_cover.py`/`strict_cover.py` drop out of the trust path. The cube list is a
  Lean definition, and the hashes bind it to the files.

### 1.2 Variant B (fallback): Y(1,2) assumed, 32 cubes

Use this only if some n-cube is not ACCEPTED, or the n-cube results do not pass `verify_final64.py`.

```lean
def cubesY12 : List (List Int) := (EncB.signPatterns [2, 3, 10, 11, 18]).map (1 :: ·)
def CubesUnsatY12 : Prop :=
  ∀ c ∈ cubesY12, ¬ EncB.DimacsSatisfiable (EncB.cubeCnf (EncB.encB 6 8 11) c)
theorem sixfold66_of_cubesY12 (h : CubesUnsatY12) : Sixfold66
```

The proof needs three extra pieces:

- **A list identity.** `cubeCnf F (1 :: p) = cubeCnf (F ++ [[1]]) p` (`List.append_assoc`). Then the cover over
  `signPatterns [2,3,10,11,18]` gives `¬ DimacsSatisfiable (encB 6 8 11 ++ [[1]])`.
- **`encB_satisfiable_y12`.** A model with `psiLt 1 2 = true` satisfies `encB ++ [[1]]`. This uses
  `ν 1 ↔ psiLt 1 2`: Y(1,2) is the first entry of the variable list, so `numberMap_getD` gives it the number 1.
  About 40 LOC.
- **Milestone M7′, reflection.** `exists_labelling_y12`: a counterexample yields a counterexample with a labelling
  in which ψ₁ < ψ₂. Reflect T in the line through c at angle φ, then relabel with ψ′ᵢ = 2π/6 − ψᵢ for i ≥ 1. This
  needs:
  - hullVerts and peel commute with affine equivalences (new, about 120 LOC);
  - general position and n-gons transported through `SYMLEAN/AffineReduction.lean:1290`
    (`generalPosition_image_affineEquiv`) and `:1298` (`hasConvexNGon_image_affine`, applied to the inverse);
  - ρ⁻¹-invariance from finiteness (new, about 30 LOC);
  - σρσ = ρ⁻¹ (new, about 20 LOC);
  - the relabelling (new, about 80 LOC).

  Total about 250–350 LOC, 1.5–3 agent-days.

### 1.3 Not covered

- m = 7 (Sevenfold70). The odd branch of the port exists only for byte identity. Soundness for odd m needs H
  fields plus KS Lemma generic(b) (perturbation) and Lemma convpos.
- The lower bounds, Remark rem:affine and encoder A.

### 1.4 Trusted facts E1–E6 (with the critique's corrections)

| # | Fact | Evidence / where it is recorded |
|---|---|---|
| **E1** | **Emitter output.** For each `c ∈ cubes64`, printing `cubeCnf (encB 6 8 11) c` with the Std-only emitter in the layout of gen_b2.py:191-194 + mkcubes.py:11-15 gives bytes whose SHA-256 equals the recorded hash of the file cake_lpr checked. The base file is `479e31a9…`. | 32 c-cubes: `C6UPPER/SHA256SUMS.txt:88-119` and the B rows of `C6UPPER/replay-2026-11-06/results.tsv` (column 3). 32 n-cubes: `C6UPPER/noty12-2026-11-06/cubes.sha256` (written before solving; copied from `/home/jay/research/data/c6upper-noty12-20261106/` after the unit finished; also column 3 of `C6UPPER/noty12-2026-11-06/results.tsv`). Base: `C6UPPER/SHA256SUMS.txt:86`. **Checked in M9:** `scripts/hash_binding.sh` streams `twin-base 6 8 11` and `twin-cube64 6 8 11 I` for I = 0..63 (the string `cnfText (encode 6 8 11) (cubes64.get ⟨I, h⟩)`, E3) into sha256sum and compares each hash with every record of its name: 68/68 MATCH with the 3 other instances (`logs/m9_hash_binding.log`, A1; reruns `logs/m9_a2_hash_binding.log` and `logs/m9_a2fix_hash_binding.log` with the A2 exe `3d43fa8b…`). |
| **E2** | **Verdicts.** cake_lpr printed exactly `s VERIFIED UNSAT` on each (CNF, proof) pair. Only that line certifies (lrat-check is unsound, memory note `lrat-check-unsound`). | c-cubes: replay `results.tsv`, 32/32 B rows ACCEPTED. n-cubes: `C6UPPER/noty12-2026-11-06/results.tsv`, 32/32 ACCEPTED (finished 15:40:35 KST), and `verify_final64.py` PASS (`verify_final64.log`), including check (5) (CNF hash ↔ row ↔ cake log ↔ proof zst hash); this closes defect 1 of the scratchpad review `rev-cover.md`. |
| E2 provenance | The binary is SHA `c14ff498…`, rebuilt byte-identically from cake_lpr commit `033aad53`. That is **not** the vendored source `a36874a8` (`C6UPPER/replay-2026-11-06/README.md:96-104`). The proofs are not public (p1.tex:310-312). | M9 ships a re-solve script (CaDiCaL + cake_lpr from a pinned commit) so a reader can regenerate proofs. The cost, from the records, is about 20.1 h of CaDiCaL (72,284 s over the 64 cubes: 36,873.6 s for the c-half, replay `results.tsv`, and 35,410.6 s for the n-half, noty12 `results.tsv`) plus about 1.4 h of cake_lpr. **As built (M9):** `scripts/resolve.sh` emits each requested cube from the Lean exe (`twin-cube64`), requires its hash to equal both records before solving, and runs pinned copies of CaDiCaL 2.1.3 `4acf5860…` and cake_lpr `c14ff498…`; smoke test 2/2 ACCEPTED, twice (`logs/m9_resolve_smoke.log`, `logs/m9_resolve_fix.log`); `all` (about 22 h, about 110 GB of proofs) not run. `scripts/build_cake_lpr.sh` (the recipe for `033aad53`, pinned source hashes) was not run. Its pins for Makefile and basis_ffi.c are recorded nowhere before M9, and the replay README has only the prefix `d20ceae0` of cake_lpr.S; they are M9's own reading of the local clone (`git show`), recomputed with the same values in `logs/m9_review_fix.log`. |
| **E3** | **DIMACS semantics (narrowed in M9 A2).** cake_lpr reads every text in the language of the reference parser `parseDimacs` (Render.lean:321) as `parseDimacs` does, and its UNSAT verdict on such a text means `¬ EncB.DimacsSatisfiable` of that clause list. Its second half (the verdict means unsatisfiability of what cake_lpr parsed) rests on cake_lpr's HOL4/CakeML verification; its first half (the two parsers agree) is not verified (see below). **Proved in Lean (M9 A2, `EncB/Render.lean`, Std-only, axioms within [propext, Classical.choice, Quot.sound]): the text the exe writes is in that language and parses back to the theorem's list.** `cnfText_encode` (:156, by `rfl`): the string `cnfText (encode m K t) cube` that the exe writes is `renderCube (numVars m K t) (encB m K t) (bodyR (encB m K t)) cube`; `renderCube_eq` (:164): that is `render nv (cubeCnf F cube)`; `parseDimacs_render` (:585): `parseDimacs (render nv F) = some (nv, F)` for every `F` whose literals are nonzero with `natAbs ≤ nv`, which `encB_wf` gives symbolically; for (6,8,11), `parseDimacs_base6811` (:806) and `parseDimacs_cube64_get` (:800), with the cube literals bounded by `numVars_ge_45` (:780; the 45 Y codes are allocated first), so nothing evaluates the instance; `cubesUnsat64_of_texts_get` (:833) turns verdicts on exactly these 64 texts, by index, into `CubesUnsat64` (membership form: `cubesUnsat64_of_texts`, :814); `cnfText_bytes` (:711): its UTF-8 bytes are its characters' codes mapped by `·.val.toUInt8`; since the review fixes, `cnfText_ascii` (`EncB/Compose.lean`) states that every character is ASCII and `parseDimacsBytes_cube64_get` states the round trip on the bytes, read by `parseDimacsBytes` (each byte as the character with that code, then the automaton of `parseDimacs`), and `no_model_6811_of_texts` composes `cubesUnsat64_of_texts_get` with M3's `encB_satisfiable_6811`. The header line and counts, the clause lines, the unit tail and the decimal printing (Render's `pushNat`/`pushInt`, not core's `toString`) are all inside the proved term. **Not proved: that cake_lpr's parser agrees with `parseDimacs`.** Its source is not on this machine (the `HOL/` and `cakeml/` submodules of the clone at `033aad53` are empty), so `parseDimacs` is the plain subset (header `p cnf nv nc`; exactly `nc` lines `l₁ … lₖ 0` with single spaces, the empty clause as ` 0`; nonzero literals with no leading zero and no `+`, `l.natAbs ≤ nv`; every line ending in `\n`; nothing else; 14 kernel-checked examples, Render.lean:325-345), not a model of cake_lpr's code. | **Evidence for the trusted part** (`logs/m9_a2_cake_parse.log`, cake_lpr `c14ff498…` in its parse-and-print mode): its printout of what it parsed is byte-identical to 21 small and medium twin texts and to the (6,8,11) base and cubes 0 and 63, which have the recorded hashes; of the 13 texts `parseDimacs` rejects, cake_lpr rejects 5 and reads 8 the standard way, so the language accepted here is the stricter one on these examples. Earlier tests (scratchpad review `rev-cover.md`): one clause per line, the header clause count must match exactly, every variable ≤ nv, stray `0` literals rejected. **Correction (kept):** the numeral bound `l.natAbs ≤ 78059` is not proved; proving it would need evaluation of `encB 6 8 11`, and the symbolic bound suffices. The value nv = 78059 in the header is bound only by E1. |
| **E4** | **Lean compiler, runtime and the core code the emitter executes (narrowed in M9 A2).** The compiled code of `encode` (whose fields are `encB` and `numVars`) and of Render's printer (`pushNat`, `pushInt`, `pushClauseR`, `bodyR`, `headerR`, `cubeBodyR`, `renderCube`, `cnfText`) equals the kernel definitions up to the Lean compiler and core's runtime: `String.push`/`++` (`lean_string_push`, `lean_string_append`), `Nat` arithmetic (`/ 10`, `% 10`, comparisons), `Nat.digitChar`, the `List`/`Array` primitives, `String.toNat?` on the command-line arguments, and `IO.FS.Stream.putStr` writing `s.toUTF8` (whose bytes `cnfText_bytes` fixes). Also trusted: a reading of Emit's IO glue, i.e. that the string written to stdout is `cnfText e c` with `e = encode m K t` (`encodeChecked`, Emit.lean:129-136) and `c = cubes64.get ⟨i, h⟩` for `twin-cube64` (:172-186) or `c = []` for `twin-base` (:187-195), and that nothing else goes to stdout. **No longer on the twin's trust path (since A2):** core's `toString` on `Nat` (`Nat.repr`, `@[implemented_by reprFast]`, `Init/Data/Repr.lean:243`; `lean_string_of_usize`) and on `Int` (through the bodiless `opaque` `String.Internal.append`, `Init/Data/String/Bootstrap.lean:69-70`), M2's twin printer (`bodyL`, `cubeBody`, removed), and M1's printer `pushClause`/`body`/`header`/`cubeTail` (Emit.lean:57-70), which only the gen modes use. `toString` still formats the stderr lines (summary, cube name and units), which are not hashed. | **Correction:** ENCBLEAN itself has no `implemented_by`, `extern`, `unsafe` or `native_decide` (grep in M8; Gen's docstring Gen:34-36 already states this). The tie to the kernel holds only at project level; core's code is part of E4. `@[csimp]` replacements are proved, so they are not trust. |
| **E5** | **Kernel, Mathlib `f897ebcf…`, and the match between the paper's notions and the definitions.** `ErdosSzekeres/Definitions.lean:9-22`, `orient` (`ErdosSzekeres/Orientation.lean:9`), `rotAbout` LL:298, `Invariant` LL:105, `Sixfold66` LL:1102. | Unchanged from P1 (S1). |
| **E6** | SHA-256 and `sha256sum`. | — |

**Copied definitions (critique §2).** The emitter is Std-only and copies these definitions:

- `DimacsSat` and `DimacsSatisfiable` from H `ETVEncoding/Dimacs.lean:18,23`. Written with `Nat`/`Int` they are the
  same terms, so after the cutoff `EncB.DimacsSat = ETV.DimacsSat` holds by `rfl` (optional).
- The numbering from `ETVEncoding/Clauses.lean:148-157` and `Dimacs.lean:27-91,185-216`.
- `cubeCnf`, `Covers` and the cover theorems from H3 `MirrorEncoding/Cover.lean:29-114` and `CoverCore.lean:12-29`.

**Finding.** H's numbering proofs use two **Mathlib** lemmas: `List.idxOf_cons_ne` (Mathlib `Data/List/Basic.lean:487`)
and `List.getElem_idxOf` (`:551`). The Std-only copy must re-prove them, about 15 LOC. Core v4.24 does have
`List.idxOf_cons_self`, `List.idxOf_lt_length_of_mem`, `List.mergeSort_perm`, `List.sorted_mergeSort` and the
`Std.HashMap` `insertIfNew` lemmas.

### 1.5 What leaves the trust base relative to P1's written chain

With variant A and M1–M9 done, these steps of KS become Lean or disappear:

- **Become Lean:** S5, the layer assembly of gap G4, but only the part used (membership and injectivity); S7, the
  phases and labels; S8, genericity for m = 6; S11–S17, the assignment, orbit literals, order, angular, nesting and
  chain clauses, i.e. the code-to-clause correspondence of gap G1; S19, the cover; S22, the composition.
- **Disappear:** S4, the translation step (the Lean lemmas take an arbitrary centre c); S9, the normalisation
  (offset φ); S10, the reflection (variant A).
- **Leave the critical path:** Lemma collinear, Lemma affine and dichotomy (a) (§3.5).

What remains trusted is E1–E6.

---

## 2. Interfaces

### 2.1 The geometric interface (output of M5): `PolarLabelling`

This is the interface of critique §4.2.

```lean
namespace EncB.Geo
open ErdosSzekeres ErdosSzekeres.LayerLemma

/-- A polar labelling of the layers of `T` about `c`: layer `i` is the regular `m`-gon
    `P(i,k) = polar c (r i) (φ + ψ i + k·2π/m)`, the hull vertices of `peel T i`.
    `ψ 0 = 0 < ψ i < 2π/m` (i ≥ 1), all distinct; radii positive and weakly decreasing. -/
structure PolarLabelling (m t : ℕ) (T : Finset Point) (c : Point) where
  r : ℕ → ℝ
  ψ : ℕ → ℝ
  φ : ℝ
  r_pos  : ∀ i, i < t → 0 < r i
  r_anti : ∀ i j, i ≤ j → j < t → r j ≤ r i
  ψ_zero : ψ 0 = 0
  ψ_pos  : ∀ i, 0 < i → i < t → 0 < ψ i
  ψ_lt   : ∀ i, i < t → ψ i < 2 * Real.pi / m
  ψ_inj  : ∀ i j, i < t → j < t → ψ i = ψ j → i = j
  mem_layer : ∀ i k, i < t →
    polar c (r i) (φ + ψ i + (k : ℝ) * (2 * Real.pi / m)) ∈ hullVerts (peel T i)    -- polar: LL:932

/-- The label map. It is total; it matters only on valid labels. -/
noncomputable def PolarLabelling.P (L : PolarLabelling m t T c) (a : ℕ × ℕ) : Point :=
  polar c (L.r a.1) (L.φ + L.ψ a.1 + (a.2 : ℝ) * (2 * Real.pi / m))
```

**Standing hypotheses** of every M5/M6 theorem ("the counterexample"):

```lean
(hgp : GeneralPosition T) (hc : c ∉ T) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) T)
(hno : ¬ HasConvexNGon K T)
```

**Differences from the wording of the task, and why:**

- The offset φ is D6.
- Radii are weakly decreasing (D7).
- There is no bijection Λ → T and no "peel = union of layers". Membership plus injectivity, which M6 derives, are
  all the encoder needs (§3.5 row 1).

```lean
/-- **M5.** -/
theorem labelling_of_counterexample {m K t : ℕ} (hm : 2 ≤ m) (heven : Even m) (hK : K ≤ 2 * m)
    {T : Finset Point} {c : Point} (hgp : GeneralPosition T) (hc : c ∉ T)
    (hinv : Invariant (rotAbout c (2 * Real.pi / m)) T) (hno : ¬ HasConvexNGon K T)
    (hcard : T.card = m * t) : Nonempty (PolarLabelling m t T c)
```

At (6, 8, 11) the cast `(6 : ℕ) → ℝ` versus the real literal `6` in `Sixfold66` is bridged by `exact_mod_cast`, as
in `sixfold_octagon` (LL:1126-1130).

### 2.2 The combinatorial interface (input of M3): `Model`

This file is Std-only, `ENCBLEAN/EncB/Model.lean`. `Pt = Nat × Nat` is (layer, sector), as in Gen:42.

```lean
namespace EncB

def Valid (m t : Nat) (a : Pt) : Prop := a.1 < t ∧ a.2 < m
def rot (m : Nat) (a : Pt) : Pt := (a.1, (a.2 + 1) % m)
def Distinct3 (a b d : Pt) : Prop := a ≠ b ∧ a ≠ d ∧ b ≠ d
/-- Labels of the chain family for pivot layer `i` (gen_b2.py:159). -/
def InQ (m t i : Nat) (a : Pt) : Prop := i ≤ a.1 ∧ a.1 < t ∧ a.2 < m ∧ a ≠ (i, 0)

/-- Objects: `(a, true)` is the point of label `a`, `(a, false)` its antipode. Cell in units of 2π/m
    (m even), as in gen_b2.py:109 and KS:390-395. -/
def cell (m : Nat) (o : Pt × Bool) : Nat := if o.2 then o.1.2 else (o.1.2 + m / 2) % m

/-- **The exact circular order of objects**, counterclockwise from the direction of the point (0,0):
    first by cell, then by the ψ-order of the layer. This is the content of KS Lemma k8s:lem:keys,
    taken as a definition here and proved for real directions in M6 (§3.4, G8). -/
def objLt (m : Nat) (psiLt : Nat → Nat → Bool) (o o' : Pt × Bool) : Prop :=
  cell m o < cell m o' ∨ (cell m o = cell m o' ∧ psiLt o.1.1 o'.1.1 = true)

/-- `z` lies strictly inside the counterclockwise arc from `x` to `y` (a linear order read cyclically). -/
def ccwIn {α : Type} (lt : α → α → Prop) (x z y : α) : Prop :=
  (lt x z ∧ lt z y) ∨ (lt y x ∧ lt x z) ∨ (lt z y ∧ lt y x)

def objs6 (a b d : Pt) : List (Pt × Bool) :=
  [(a, true), (b, true), (d, true), (a, false), (b, false), (d, false)]
def KeysDistinct (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) : Prop :=
  ∀ o ∈ objs6 a b d, ∀ o' ∈ objs6 a b d, o ≠ o' → objLt m psiLt o o' ∨ objLt m psiLt o' o
def ArcHasAntipode (m : Nat) (psiLt : Nat → Nat → Bool) (a b d x y : Pt) : Prop :=
  ∃ z ∈ [a, b, d], ccwIn (objLt m psiLt) (x, true) (z, false) (y, true)

/-- Pattern of rule A (PAPAPA): `a → b → d` counterclockwise, and each arc holds an antipode. -/
def AltCCW (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) : Prop :=
  KeysDistinct m psiLt a b d ∧ ccwIn (objLt m psiLt) (a, true) (b, true) (d, true) ∧
  ArcHasAntipode m psiLt a b d a b ∧ ArcHasAntipode m psiLt a b d b d ∧
  ArcHasAntipode m psiLt a b d d a

/-- Pattern of rule B (a PPP run with middle `b`): `a → b → d` counterclockwise, and the arcs
    (a,b) and (b,d) hold no antipode. -/
def BlockCCW (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) : Prop :=
  KeysDistinct m psiLt a b d ∧ ccwIn (objLt m psiLt) (a, true) (b, true) (d, true) ∧
  ¬ ArcHasAntipode m psiLt a b d a b ∧ ¬ ArcHasAntipode m psiLt a b d b d

/-- What `encB_satisfiable` consumes. `chi a b d` means orient(P a, P b, P d) > 0, and `psiLt i j`
    means ψ_i < ψ_j. -/
structure Model (m K t : Nat) where
  chi   : Pt → Pt → Pt → Bool
  psiLt : Nat → Nat → Bool
  psiLt_irrefl : ∀ i, psiLt i i = false
  psiLt_trans  : ∀ i j k, psiLt i j = true → psiLt j k = true → psiLt i k = true
  psiLt_total  : ∀ i j, i < t → j < t → i ≠ j → psiLt i j = true ∨ psiLt j i = true
  psiLt_zero   : ∀ i, 0 < i → i < t → psiLt 0 i = true
  chi_rot   : ∀ a b d, Valid m t a → Valid m t b → Valid m t d →
                chi (rot m a) (rot m b) (rot m d) = chi a b d
  chi_cycle : ∀ a b d, Valid m t a → Valid m t b → Valid m t d → Distinct3 a b d →
                chi b d a = chi a b d
  chi_swap  : ∀ a b d, Valid m t a → Valid m t b → Valid m t d → Distinct3 a b d →
                chi a d b = !chi a b d
  ruleA : ∀ a b d, Valid m t a → Valid m t b → Valid m t d → Distinct3 a b d →
            AltCCW m psiLt a b d → chi a b d = true
  ruleB : ∀ a b d, Valid m t a → Valid m t b → Valid m t d → Distinct3 a b d →
            BlockCCW m psiLt a b d → b.1 ≤ a.1 → b.1 ≤ d.1 → chi a b d = true
  nest  : ∀ i j k, i < j → j < t → k < m → chi (i, 0) (i, 1) (j, k) = true
  noChain : ∀ i, i < t → ∀ q : Nat → Pt,
      (∀ s, s < K - 1 → InQ m t i (q s)) →
      (∀ s, s + 1 < K - 1 → chi (i, 0) (q s) (q (s + 1)) = true) →
      (∀ s, s + 2 < K - 1 → chi (q s) (q (s + 1)) (q (s + 2)) = true) → False
```

**As built (M3).** This is `EncB/Model.lean:81-102`, with `Valid m t` replaced by Coded's `PtOk m t` (the same body).
Every field is used: deleting any one of the 13 breaks the build (`logs/m3_mutants.log`).

### 2.3 The intended assignment, and what M3 proves

```lean
/-- A chain of length `l` for pivot `(i,0)` starting with `a, b` (KS:560-563). -/
def ChainFrom (M : Model m K t) (i l : Nat) (a b : Pt) : Prop :=
  ∃ q : Nat → Pt, q 0 = a ∧ q 1 = b ∧ (∀ s, s < l → InQ m t i (q s)) ∧
    (∀ s, s + 1 < l → M.chi (i, 0) (q s) (q (s + 1)) = true) ∧
    (∀ s, s + 2 < l → M.chi (q s) (q (s + 1)) (q (s + 2)) = true)

/-- Meaning of each variable (KS Def. k8s:def:assign). `Var` is the variable type of the functional
    twin (§3.1), either an inductive type or a decoded integer code. -/
def Model.τ (M : Model m K t) : Var → Prop
  | .y i j      => M.psiLt i j = true
  | .h _        => False                      -- odd m only; not used
  | .orb [a, b, d] => M.chi a b d = true      -- the sorted canonical triple
  | .orb _      => False
  | .f i l a b  => ChainFrom M i l a b

/-- **M3** (Std-only). -/
theorem encB_satisfiable {m K t : Nat} (heven : m % 2 = 0) (hm : 4 ≤ m) (M : Model m K t) :
    DimacsSatisfiable (encB m K t)
```

`hm : 4 ≤ m` is a guess at the side condition; M3 may weaken it. It must hold at m = 6.

**As built (M3).** The proved theorem has `hm : 2 ≤ m` (`EncB/Satisfiable.lean:37`). `ChainFrom` takes `m t chi`
instead of `M`. τ is `tauOf m t chi psiLt` (`Model.lean`), which sends `.f` to `ChainFrom` and every other variable to
the computable `baseVal`; `.h`, `.other` and malformed `.orb` are false. See the M3 revision note at the top.

### 2.4 The bridge (M6): `modelOfLabelling`

```lean
/-- `chi a b d = decide (0 < orient (L.P a) (L.P b) (L.P d))`, `psiLt i j = decide (L.ψ i < L.ψ j)`
    (classical `decide`). -/
noncomputable def modelOfLabelling {m K t : ℕ} (hm : 3 ≤ m) (heven : Even m) (hK4 : 4 ≤ K)
    (hK : K ≤ 2 * m) {T : Finset Point} {c : Point} (hgp : GeneralPosition T) (hc : c ∉ T)
    (hinv : Invariant (rotAbout c (2 * Real.pi / m)) T) (hno : ¬ HasConvexNGon K T)
    (L : PolarLabelling m t T c) : EncB.Model m K t
```

M6 consists of the proofs of the eleven proof fields. The table in §3.4 lists each field's source.

### 2.5 Why this cut

- **The critique's objection is met.** Its objection (§4.2) was to a `Model6` whose `angA`/`angB` are stated "on the
  generator's integer keys", which makes M3 tautological.
- **What M3 has to prove.** Here the keys appear only in the code (Gen:142-181, `patternLit`). M3 must prove that:
  1. some enumerated pattern has true premises (completeness of `perms`);
  2. true premises make the local ranks order-isomorphic to `psiLt`;
  3. sorting the six `Obj`s by key is the `objLt` order;
  4. the `kinds` test and the PPP search give `AltCCW`/`BlockCCW` with the right sign.

  This is the content of KS Lemmas prem and angB, the core of gap G1.
- **What M6 has to prove.** That `objLt` is the real circular order (KeyOrder), and that arcs in `objLt` are real
  arcs (new, G9). The real sign rules are already in LL and LEANEXT.
- **The `Model` is stated with `psiLt` directly**, not with a rank function. As a result `KeyOrder.cell_lt_iff`
  (KeyOrder:23) applies with no rank and no `StrictMonoOn` wrapper (§3.5 row 8).
- **A vacuous `Model` cannot make the final theorem false.** If `Model` were inconsistent, M6 would prove `False`
  from a counterexample, which is still a valid proof. The risk is only that M6 cannot be proved. An early warning:
  M3's tiny-instance test (§4, M3) evaluates `Model.τ` of an exact rational configuration on every clause. The
  K8EXACT20261106 assignments also already satisfy all clauses of B(7,8,9).

---

## 3. Lemma map

### 3.1 M2: the functional twin and the numbering bridge (Std-only)

**Why.** M1's `gen` (Gen:240-380) computes the clause list with `Id.run do`, mutable `Array` tables indexed by
`ptCode`/`triCode`/`fc`, and a counter `nv`. It is byte-identical to Python (§4, M1), but loop invariants over it
would be brittle.

**The plan:**

- `genCoded m K t : List (List Int)` uses the same helpers and the same order. Its variables are **closed-form
  injective codes** instead of counter values:
  - Y(i,j) ↦ `1 + i·t + j`;
  - H(i) ↦ `t² + 1 + i`;
  - orb c ↦ `oBase + triCode m N c`;
  - F(piv,l,a,b) ↦ `fBase + ((piv·FL + l)·N + ptCode a)·N + ptCode b`, with N = t·m and `FL = max (K−1) 3`
    (Gen's `FL`, Gen:325). The levels that occur are 2 ≤ l ≤ max 2 (K−2), so l < FL for **every** K. A multiplier
    `K` would fail for K ≤ 2: F₂ exists there (the base clauses are unconditional, gen_b2.py:174-175) but l = 2 ≥ K,
    and at K = 0 all pivots would share one code. Irrelevant at K = 8, but the M2/M3 statements are generic in K.

  It is written as list functions only (`flatMap`, `filterMap`, `foldl`; no `do`-loops, no arrays).
  - The orbit dedup (`orbList`), `forced` and the per-level F-key sets become `foldl`s.
  - Each is used **only** to order, to filter, or to allocate numbers. Soundness treats every filter as arbitrary.
  - `angOuts`, `patternLit`, `unitOf`, `olit` and `canon` are called exactly as in Gen, with
    `orbVar := some ∘ orbCode`, `yv := yCode` and `hv := hCode`.
- `allCodes m K t := dedupAppend (yCodes ++ hCodes ++ orbCodesFirstSeen) (codes of genCoded in stream order)`.
  - Every code that occurs is in it **by construction**.
  - It equals Python's `new()` order exactly when all orbit codes in the stream are already among `orbCodesFirstSeen`
    and the chain codes first occur in `fv` order (gen_b2.py:161-165,175,189).
  - That is true, but it is checked only by bytes.
- `encB m K t := (genCoded m K t).map (·.map (renumber (numberMap (allCodes m K t))))` and
  `numVars := (allCodes m K t).length`.
- The trust-path emitter (E1) prints `encB`. M1's `gen` stays as an oracle.

| Fact (Std-only) | Lean statement | Source | Estimate |
|---|---|---|---|
| numbering | `numberMap_getD : v ∈ l → (numberMap l).getD v 0 = l.idxOf v + 1` | copy of H `Dimacs.lean:77` (+ `numberStep_foldl` :27) | copy + re-prove `idxOf_cons_ne`, `getElem_idxOf` (15 LOC) |
| decoding | `decode_numberMap : v ∈ l → decode l ((numberMap l).getD v 0) = v` | copy of H `Dimacs.lean:85-91` | copy |
| code decoding | `decodeCode (code v) = v` for valid keys (layer < t, sector < m, pivot < t, chain level 2 ≤ l < FL; no hypothesis on K) | new | 60–100 |
| model transfer | `dimacsSat_of_holds : (∀ cl ∈ genCoded m K t, ∀-clause holds under τ ∘ decodeCode) → DimacsSat (encB m K t) (nuOf m K t τ)` | pattern of H `Dimacs.lean:193`; membership is now by construction | 60–100 |
| well-formedness | `encB_wf : ∀ cl ∈ encB m K t, ∀ l ∈ cl, l ≠ 0 ∧ l.natAbs ≤ numVars m K t` | new (from `numberMap_getD`) | 30 |
| cover | `covers_signPatterns : (∀ v ∈ vs, v ≠ 0) → Covers (signPatterns vs)`; `not_dimacsSatisfiable_of_cover` | new by induction on `vs`; copy of H3 `Cover.lean:34-48,95-108` | 40 + copy |
| twin = oracle | on the tiny grid: kernel `decide +kernel` for 4 instances (done: (3,4,1), (3,4,2), (6,4,1), (4,5,1)); compiled byte comparison on the 225-instance grid and the 4 recorded instances (done), plus `encB = gen` as Lean values on 229 instances (done) | test, not a theorem (a proof of `encB = (gen ·).clauses.toList` is optional and hard) | — |

**Alternative, if the twin is too slow.** It is a list program over about 2.4M clauses; Gen took 6 s and 426 MB at
(6,8,11), and the twin should be within about 10×. If it is too slow, prove soundness directly over `gen`. That
needs a ghost allocation log in `Result` and `forIn` invariants (or `Std.Do`/`mvcgen`), and costs more proof effort.

### 3.2 M3: combinatorial soundness (Std-only), mapped to the KS lemmas it replaces

| Fact | Statement (sketch) | Replaces | Estimate |
|---|---|---|---|
| H1 canon | `canon m tri = insSort ptLt (rotate m p0.2 tri)` for some `p0 ∈ tri` (Gen:103-109) | KS orbit (a), the part used | 40–60 |
| H2 olit | for valid distinct `P Q R`: `olit m orbVar P Q R = some l → (litHolds l ↔ M.chi P Q R = true)`, via `chi_rot` (s times), `chi_cycle`/`chi_swap` and `permSign` on the 6 orders of 3 distinct entries (`decide` on `Fin 3` patterns) | KS orbit (b); no `Equiv.Perm` (§3.5 row 7) | 120–160 |
| H3 order | the transitivity clauses (gen_b2.py:79-81) hold under `y i j ↦ psiLt i j` | KS order | 30 |
| H4 nesting | `olit (i,0) (i,1) (j,k)` holds (`Model.nest` + H2) | KS nestcl (code part) | 20 |
| H5 chains | base, extension and closing clauses hold under `ChainFrom`; closing gives `noChain` with q = (a, b, c, …) | KS chain (code part) | 120–180 |
| H6a patterns | every strict order of `free` (≤ 3 layers) is some `perms (range n)` entry (Gen:78-83); `decide` for n ≤ 3 or general | KS prem (existence) | 40–60 |
| H6b premises | all premise literals true ⇔ `rk` order-isomorphic to `psiLt` on `free`, with `rk 0 = 0` and `psiLt_zero` | KS prem (uniqueness of π_S is **not** needed) | 50–80 |
| H6c keys | under H6b, `Obj.lt` on the six `Obj`s of `c` (Gen:137-138) agrees with `objLt`; keys distinct ⇔ `KeysDistinct` | KS keys (combinatorial half) | 60–100 |
| H6d rule A | `insSort` sorts the six objects in `objLt` order; `kinds ∈ {PAPAPA, APAPAP}` (Gen:162) ⇒ `AltCCW (c[seq₀]) (c[seq₁]) (c[seq₂])`, and the literal `±v` (sign `permSign seq`) holds by `ruleA` + `chi_cycle`/`chi_swap` | KS angB, first bullet | 100–150 |
| H6e rule B | `find?` PPP at `st` (Gen:168-169) ⇒ `BlockCCW a b cc`; with `b.1 ≤ a.1, cc.1` the literal `olit a b cc` holds (`ruleB` + H2) | KS angB, second bullet | 60–100 |
| H6f merge | `unitOf` / conditional emission (Gen:210-213, gen_b2.py:134-141): a unit is the literal of the true pattern; a conditional clause has a false premise or a true literal | KS angB, opening paragraph | 40–60 |
| H7 shapes | membership lemmas for `genCoded`: every clause is one of the four families, with its labels valid and distinct as used above | KS Thm sound (a), "by reading the source" | 150–250 |

**Not needed:**

- `word_dichotomy`. If the PPP search fails, the port emits no clause; Python would raise (Gen:25-29; the `none` branch at Gen:170), and byte
  identity shows this never happens.
- KS orbit (c), the stabiliser.
- Lemma diam: omitted clauses are a weakening.

**As built (M3, 2026-11-06).** Every row is proved, and each theorem's axioms are within {propext,
Classical.choice, Quot.sound} (`logs/axioms.log`).

| Fact | Lean (file:line) | Unit |
|---|---|---|
| H1 canon | `Orbit.canon_eq` (SoundOrbit.lean:93): `canon m tri = insSort ptLt (tri.map (rotBy m s))` for some `s`; used only for `orbListSpec` (:161), together with `Orbit.mem_dedupBy` (:39) | U1 |
| H2 olit | `olitSpec : OlitSpec M` (SoundOlit.lean:38), with `chi_perm3` (ModelLemmas.lean:80) | U0 |
| H3 order | `transCl_sound` (SoundOrbit.lean:174) | U1 |
| H4 nesting | `nestLits_sound` (SoundOrbit.lean:212), `hm : 2 ≤ m` | U1 |
| H5 chains | `chainCl_sound` (SoundChain.lean:202), for every filter `isF` | U2 |
| H6a patterns | `Ang.exists_rkMono` (SoundAng.lean:301): the pattern `s := insSort M.psiLt free`, ranks `free.map s.idxOf` | U3 |
| H6b premises | `Ang.rkMono_of_prem` (SoundAng.lean:238): all premises true ⇒ `RkMono` (one direction) | U3 |
| H6c keys | `Rules.sortSix` (SoundRules.lean:218): `insSort Obj.lt` of the six objects is a `SortedSix` (sorted in `objLt` order) | U4 |
| H6d, H6e rules A, B | `wordSpec` (SoundWord.lean:222): a sorted word gives `AltCCW` (alternating) or `BlockCCW` (PPP run); `Rules.patternSpec_of_sort` (SoundRules.lean:139) applies `ruleA`/`ruleB` with `chi_perm3`/`olitSpec`; `patternSpec_of` (:270) | U5, U4 |
| H6f merge | `angCl_sound` (SoundAng.lean:329): a unit is the literal of the pattern that follows ψ; a conditional clause has a false premise or a true literal | U3 |
| H7 shapes | `genCoded_sound` (Satisfiable.lean:26): `simp only [genCoded, …]` and one `rcases` into the four families | Integration |

Size: about 1.56k lines of code, not counting blank, comment and docstring lines (2.0k lines in all). That splits
into 467 for the interface U0, 1,068 for U1–U5 (277 of them from the judge's start files) and 23 for
`Satisfiable.lean`. The early-warning test adds 298. The estimate above summed to 0.9–1.4k.

### 3.3 M5: `labelling_of_counterexample` (Mathlib)

LL line n is Capstone2 line n+8 for n ≥ 10 (§3.6), so either file can be the source.

| # | Needed fact | Lean source (file:line) | Hypothesis notes | Estimate |
|---|---|---|---|---|
| F1 | `peel T n` nonempty for n < t | `card_peel` LL:1037 with `ht : m*(t-1) < T.card` (from `hcard`, t ≥ 1) | gives `(peel T n).card + m*n = T.card` | 10 |
| F2 | `hullVerts (peel T n) = orbitFS ρ m xₙ`, `xₙ ∈ peel T n` | `layers_are_orbits` LL:402 | `0 < m`, `K ≤ 2m`, `c ∉ T`, `Invariant`, `¬HasConvexNGon K T` — all standing | 0 |
| F3 | `xₙ = polar c Rₙ θₙ` with `Rₙ = √(dist2 c xₙ) > 0` | `exists_angle` Capstone2:2056, `sqrt_dist2_pos` :2064, `ne_of_mem` :2073 (also `PhaseClassification.exists_polar` :459) | `xₙ ≠ c` from `c ∉ T` | 10 |
| F4 | `ρ^[k] (polar c r θ) = polar c r (θ + k·2π/m)` | `rotAbout_iterate` LL:465 + `rotAbout_polar` Merged:1241 (= OrbitConsistency:355) | — | 10 |
| F5 | `θₙ − φ = ψₙ + jₙ·(2π/m)`, ψₙ ∈ [0, 2π/m), with φ := θ₀ | Mathlib `toIcoMod_mem_Ico`, `self_sub_toIcoMod` (`Algebra/Order/ToIntervalMod.lean:74,121`) | ψ₀ = 0 by `toIcoMod` of 0 | 40 |
| F6 | `mem_layer`: `polar c Rₙ (φ + ψₙ + k·u) ∈ hullVerts (peel T n)` for every k | F2–F5 + `polar_add_int` Merged:1269 + `Finset.mem_image` (index (k − jₙ) mod m) | new glue | 60 |
| F7 | ψ distinct, and ψₙ > 0 for n ≥ 1 | `phase_ne_of_distinct_layers` Merged:1367 at k = 0 | `2 ≤ m`, `Even m` (m = 6) | 20 |
| F8 | `r_anti`: Rⱼ ≤ Rᵢ for i ≤ j | `dist2_le_of_later` LL:1012 + `dist2_polar` Linked:1390 (= Capstone:1398) + `nlinarith`, exactly as `orient_pos_of_layers` Capstone:1406-1421 does | squared to plain radii needs R > 0 | 15 |

M5 total: about 150–250 new LOC. The plan's estimate was 400–600, but the interface no longer asks for a
bijection, strict radii or θ₀ = 0.

### 3.4 M6: the fields of `modelOfLabelling` (Mathlib)

| Field / fact | Lean source (file:line) | Notes | Estimate |
|---|---|---|---|
| G1 `P (rot a) = ρ (P a)` | `rotAbout_polar` Merged:1241, `polar_add_int` Merged:1269 (the case k = m−1 ↦ 0 adds 2π) | needed for `chi_rot` and `nest` | 25 |
| G2 `P` injective on valid labels | distinct layers: `not_mem_hullVerts_peel_of_ne` Merged:1322; same layer: `rotAbout_injective` LL:319 + `minimalPeriod_rotAbout` LL:336 (period exactly m) | new glue | 40 |
| G3 `orient (P a) (P b) (P d) ≠ 0` for distinct valid labels | `generalPosition_iff_orient_ne_zero` (`ErdosSzekeres/OrientationGeometry.lean:66`) + G2 + `hullVerts_subset` LL:118 + `peel_subset` LL:381 | — | 15 |
| `chi_rot` | `orient_rotAbout_inv` OrbitConsistency:117 (re-state over LL's `rotAbout`; the definitions are verbatim copies) + G1 | — | 15 |
| `chi_cycle`, `chi_swap` | `orient_cycle`, `orient_swap` (`ErdosSzekeres/Orientation.lean:15,12`) + G3 | `chi_swap` needs ≠ 0 | 15 |
| `psiLt_*` | real `<`, `ψ_inj`, `ψ_zero`, `ψ_pos` | — | 20 |
| `nest` | `strict_nesting` LL:529 with x = P(i,0) ∈ hullVerts(peel T i), y = P(j,k) ∈ peel T j, and ρ x = P(i,1) (G1) | `2 ≤ m`, `n < n'` | 15 |
| `noChain` | `chain_clauses_sound` LL:914 with p = P(i,0), q s := P(q′ s); `q s ∈ peel T i` by `peel_antitone` LL:460 + `hullVerts_subset`; `q s ≠ p` by G2 | `3 ≤ m`, `4 ≤ K ≤ 2m`; no distinctness of q needed | 30 |
| G8 key bridge | reduced relative direction `rd(P(i,k)) = k·u + ψᵢ` and `rd(A(i,k)) = ((k + m/2) % m)·u + ψᵢ` by `KeyOrder.antipode_even` :115 and `reduce_mod_two_pi` :81; then `objLt o o' ↔ rd o < rd o'` by `KeyOrder.cell_lt_iff` :23, and equal keys ↔ equal directions by `cell_eq_iff` :45 | uses ψ directly, no rank function | 80–120 |
| G9 arc bridge | for reduced directions in [0, 2π): `ccwIn objLt x z y ↔ PhaseClassification.inArc (dir x) (gap x y) (dir z + …)` (`inArc` :117) | **new**: this is the "keys vs true circular order" item still listed outside Lean in `LEANEXT/README.md:24-25`; nothing in LEANEXT proves it | 150–250 |
| `ruleA` | AltCCW ⇒ after a cyclic relabelling (3 cases, `orient_cycle`) α < β < δ < α + 2π and `Alternating α β δ` (:126) via G9 ⇒ `orient_pos_of_alternating` (PhaseClassification:301 = Capstone2:1721), with points `polar c r (φ + rd)` | — | 60–100 |
| `ruleB` | BlockCCW ⇒ `RunMidB α β δ` (:132) via G9; `hg3 : α + 2π − δ ≠ π` from `KeysDistinct` + G8 ⇒ `orient_pos_of_runMidB` (:310 = Capstone2:1730) with `ra ≤ rb`, `rd ≤ rb` from `r_anti`; for a block that wraps past 2π use `polar_add_two_pi` (:111). Alternatively `Capstone.orient_pos_of_layers_runMidB` (Capstone:1977), which takes layers instead of radii. | — | 80–120 |

M6 total: about 550–800 new LOC. G9 is the one step with no existing ingredient.

### 3.5 Hypotheses of the existing Lean lemmas versus the KS lemmas (checked)

| # | KS | Lean | What was compared | Verdict |
|---|---|---|---|---|
| 1 | Lemma layer, KS:92-109 | `layers_are_orbits` LL:402, `card_peel` LL:1037; disjointness `not_mem_hullVerts_peel_of_lt/_ne` Merged:1316,1322 | KS: m ≥ 1, K ≤ 2m, t ≥ 1, ρ-invariant, K-free, O ∉ S, \|S\| = mt. Lean: `0 < m`, `K ≤ 2m`, `c ∉ S`, `Invariant`, `¬HasConvexNGon`, `peel` nonempty (`card_peel` needs m(t−1) < \|S\|). KS also concludes peel(S,n) = Lₙ ∪ … ∪ L_{t−1} and a bijection Λ → S; Lean does not. | **Match** for what the encoder uses. The union/bijection half (gap G4) is **not needed**: `chain_clauses_sound` needs `q s ∈ peel S i` and `q s ≠ p`, i.e. membership and injectivity only. KS's chain proof says "P is a bijection" (KS:587), but only injectivity is used. |
| 2 | Lemma affine, KS:121-129; Cor. geom translation, KS:809-816 | — | — | **Not needed in variant A.** The Lean lemmas are stated at an arbitrary centre c, and the normalisation is replaced by φ. Variant B needs only the reflection part (M7′). |
| 3 | Lemma centre, KS:165 | `centre_not_mem_of_even` LL:582 | `0 < m`, `Even m`, `Invariant`, GP, p ≠ c ∈ S | **Match.** Used only inside `sixfold_octagon`, already Lean. |
| 4 | Lemma nest, KS:181 | `strict_nesting` LL:529, `dist2_le_of_later` LL:1012 | KS: x ∈ Lᵢ, y ∈ Lⱼ, i < j (resp. ≤). Lean: x ∈ hullVerts(peel n), y ∈ peel n′. | **Match** (Lean is stronger: y only needs to be in `peel`). The radius comes squared; converting needs r > 0 (done in Capstone:1406-1421). |
| 5 | Def. phase, KS:195 | — (M5 builds it) | KS normalises θ₀ = 0 by rotating S (Lemma affine). | **Deliberate deviation** (D6): offset φ. ψ ∈ [0, 2π/m) as in KS. |
| 6 | Lemma collinear, KS:209 + generic (a), KS:248-252 | `phase_ne_of_distinct_layers` Merged:1367 (via `same_ray_false` Merged:1181 = OrbitConsistency:295) | KS generic (a): "nested m-gons in general position", no K-freeness. Lean: `2 ≤ m`, `Even m`, `K ≤ 2m`, `c ∉ S`, `Invariant`, GP, `¬HasConvexNGon K S`, hull vertices of distinct peels with polar forms r, r′ > 0. Conclusion ∀ k : ℤ, β − α ≠ k·2π/m, which is KS's θᵢ − θⱼ ∉ uℤ with u = 2π/m. | **Match.** Lean has more hypotheses, all available in the counterexample. The Lean route bypasses Lemma collinear (new, unreviewed), which leaves the critical path. |
| 7 | Lemma orbit (b), KS:334-371 | `encoder_literal_sound` OrbitConsistency:253 | Instantiates with σ₁ = id, σ₂ = ω, s = −k₀ mod m. `hr : ∀ i, P (r i) = ρ (P i)` is quantified over **all** labels; it holds for the uniform polar formula, including k ≥ m (by `polar_add_int`). **Mismatch:** `litVal` uses `Equiv.Perm.sign : ℤˣ`, while gen_b2/Gen compute `perm_sign` by counting inversions on a list (Gen:91-92). A 6-case bridge would be needed. | **Not used.** M3 proves the literal rule combinatorially from `chi_rot`/`chi_cycle`/`chi_swap` (H2), and M6 proves those three from `orient_rotAbout_inv` OrbitConsistency:117 and `orient_cycle`/`orient_swap`. Part (a) is reduced to H1; part (c) is not needed, as KS also says (KS:375). |
| 8 | Lemma keys, KS:401-424 | `KeyOrder.cell_lt_iff` :23, `cell_eq_iff` :45, `reduce_mod_two_pi` :81, `antipode_even` :115 (`reduced_lt_iff_key` :139) | (i) KS's rank rk : M → ℤ is on layer indices. `reduced_lt_iff_key` wants rank : ℝ → ℕ, `StrictMonoOn` on the set of phases: a different shape, needing ψ injective to transfer. (ii) KeyOrder reduces J·u + ψ mod 2π and uses J % N; gen_b2 uses already-reduced J = k ∈ [0,m) and (k + m/2) % m. The latter equals `antipode_even` with J = k. (iii) KS's "equal keys iff same-layer antipodal pair": only "distinct keys ⇒ distinct directions" is needed (`cell_eq_iff`). (iv) The generator's *local* ranks (1..\|F\|, layer 0 ↦ 0) are neither KS's rk_S nor a global rank. (v) KeyOrder measures from direction 0; ours are relative to φ. | **Usable, with the `Model` designed to avoid (i)**: `objLt` compares by `psiLt` itself, so `cell_lt_iff` applies with ψ and no rank. (iv) is M3's job (H6b–c, combinatorial). (v) is harmless, since `orient` depends only on differences. |
| 9 | Lemma dich, KS:426-472 | (a) `word_dichotomy` PhaseClassification:539; `phase_trichotomy` :285. (b) `orient_pos_of_alternating` :301. (c) `orient_pos_of_runMidB` :310, `Capstone.orient_pos_of_layers_runMidB` Capstone:1977. | (a) **Mismatch:** `word_dichotomy` is about Bool words with s(i+3) = ¬s(i); it says nothing about real directions and does not prove (a). (a)'s real content is `phase_trichotomy` (needs gaps ≠ π). (b) Hypotheses: radii > 0, α < β < δ < α + 2π, `Alternating` (arcs taken mod 2π with `inArc`). KS (b) is "the word alternates". (c) Hypotheses: ra, rd > 0, α < β < δ < α + 2π, α + 2π − δ ≠ π, `RunMidB`, ra ≤ rb, rd ≤ rb. KS (c) assumes a whole PPPAAA block; `RunMidB` only needs the two arcs to be antipode-free, which the code's PPP run (three consecutive objects) gives. | (a) is **not needed** on the Lean path (§3.2). (b) and (c) **match** once G9 turns "sorted word" into `inArc` facts. `hg3` follows from distinct keys, and the radii from `r_anti` plus the code's `b.1 ≤ a.1, cc.1` test (gen_b2.py:131). |
| 10 | Lemma prem, KS:479-489 | — (M3 H6a–b) | — | **New**, and simpler: only "true premises ⇒ order-isomorphic" and existence are needed, not π = π_S. |
| 11 | Lemma angB, KS:491-523 | — (M3 H6c–f) | — | **New** (code part of gap G1). |
| 12 | Lemma order, KS:535-544 | — (M3 H3) | — | trivial |
| 13 | Lemma nestcl, KS:549-560 | `strict_nesting` LL:529 | needs P(i,1) = ρP(i,0) (G1) | **Match.** |
| 14 | Lemma chain, KS:575-597 | `chain_clauses_sound` LL:914 | `3 ≤ m`, `4 ≤ K ≤ 2m`, `c ∉ S`, `Invariant`, `¬HasConvexNGon K S`, GP, `p ∈ hullVerts (peel S i)`, `q : ℕ → Point` with `q s ∈ peel S i`, `q s ≠ p` (s < K−1), fan, turn. KS: q in Qᵢ, l = K−1, 1-based. | **Match** (0- versus 1-based). No distinctness of q needed (critique confirmed). At (6,8): 3 ≤ 6, 4 ≤ 8 ≤ 12. |
| 15 | Lemma refl, KS:620-641 | — | — | **Dropped** (variant A). M7′ only for variant B. |
| 16 | Lemma cube, KS:775-783 | `Mir.not_dimacsSatisfiable_of_cover` H3 `Cover.lean:98`, `covers_of_coverCheck` :90 | — | **Match.** Copied into the Std-only package; the cover itself is proved structurally. |
| 17 | Cor. geom, KS:795-826 | replaced by `sixfold66_of_unsat` | — | No translation step; the Lean lemmas take centre c. |
| 18 | Lemma diam, KS:741-771 | — | — | **Not needed** (weakening). |

**Two further mismatches that M4 must remove:**

- **Duplicated definitions under different namespaces.** OrbitConsistency defines its own `iterate_mem`, `Invariant`,
  `toC`, `ofC`, `crot`, `rotAbout` and `polar` (OrbitConsistency:39-112) in `ErdosSzekeres.OrbitConsistency`.
  PhaseClassification has its own `polar` (PhaseClassification:41). They are verbatim copies, so equal by `rfl`
  (cf. `Capstone.polar_eq` Capstone:2001), but they are different constants.
- **The rotation angle.** `Sixfold66` (LL:1102-1105) uses the real literal `2 * Real.pi / 6`. The lemmas use
  `2 * Real.pi / (m : ℝ)` with m : ℕ. `exact_mod_cast` bridges them, as in LL:1126-1130.

### 3.6 Consolidation facts for M4 (checked by `diff`, read-only)

The LEANEXT files form a chain of textual extensions:

```
Merged.lean    lines 1-1147 = LayerLemma.lean lines 1-1147           (diff: only the final `end`)
Linked.lean    lines 1-1384 = Merged.lean lines 1-1384               (Linked adds §13 Link at 1385-1416)
Capstone.lean  lines 18-1424 = Linked.lean lines 10-1416             (two extra imports + header)
Capstone.lean  lines 1456-1965 = PhaseClassification.lean lines 36-545
Capstone2.lean lines 1-2003 = Capstone.lean lines 1-2003             (Capstone2 adds 2005-2132)
```

- **Capstone2.lean is therefore one source for nearly everything M5/M6 need:** LayerLemma, the even-m phase
  results, rule B on layers, PhaseClassification and the capstone statements. LL line n is Capstone2 line n+8 (n ≥ 10).
- **Not in it:** OrbitConsistency (a)/(b), of which we need only `orient_rotAbout_inv` (3 lines), and KeyOrder
  (158 lines, Mathlib only).
- **No `sorry`, `native_decide` or `axiom`** in Capstone2, KeyOrder or OrbitConsistency (grep).

M4 splits Capstone2 into modules under `geo/ES8Geo/`, with statements unchanged (checked by `diff`), and adds
KeyOrder and `orient_rotAbout_inv`.

---

## 4. Milestones (revised; M7 dropped)

| # | Milestone | Files | Done when | CPU / when | Est. |
|---|---|---|---|---|---|
| **M0** | Design, lemma map, reference corpus | `DESIGN.md`, `ref/hashes.tsv`, `ref/make_ref.py` | This file exists. The corpus covers the tiny grid plus the four recorded instances with gen_b2.py at `3d47459a…`, including rows where Python raises. | none | done (see below) |
| **M1** | Std-only port of gen_b2.py (both parities) and the emitter | `EncB/Gen.lean`, `EncB/Emit.lean`, `EncB/KernelCheck.lean`, `scripts/compare_b.sh`, `scripts/check_recorded.sh` | `lake build` (Std-only) is green; no `sorry`/`native_decide`/`implemented_by`/`extern`/`unsafe`. Byte-identical on the whole tiny grid and on (6,8,9) `9f638543…`, (7,8,9) `67cd613d…`, (7,8,10) `b4d29017…`, (6,8,11) base `479e31a9…`. A sample of the 64 cubes matches (the full 64 are in M9). | light, now | done by the parallel M1 step (see below) |
| **M2** | Functional twin and numbering bridge | `EncB/Coded.lean`, `EncB/Dimacs.lean`, `EncB/Cover.lean` | `genCoded`, `allCodes`, `encB`, `numVars`, `encB_wf`, `dimacsSat_of_holds`, `covers_signPatterns` and `not_dimacsSatisfiable_of_cover` are proved; axioms ⊆ {propext, Classical.choice, Quot.sound}. `encB` = `gen` = Python on the tiny grid (kernel on 3 instances, compiled on all) and on the 4 recorded instances (compiled, once each). | light, **now** (Std-only) | **done** 2026-11-06 (README "M2") |
| **M3** | Combinatorial soundness | `EncB/Model.lean` (frozen in §2.2), `EncB/{ModelLemmas,SortLemmas,SoundOlit}.lean`, `EncB/Sound{Orbit,Chain,Ang,Rules,Word}.lean`, `EncB/Satisfiable.lean`; test `EncB/EarlyWarning.lean` | `encB_satisfiable` is proved, with no `sorry` and standard axioms. **Early warning:** a computable τ (orientations of exact rational m = 6 configurations, chain variables by least fixpoint) satisfies every clause of `genCoded` under `tauOf ∘ decodeCode` (hence `encB`, through M2's `dimacsSat_of_holds`) at those instances (interpreted `lean --run`, evidence only; the base runs go up to t = 5, and the M3 review added t = 10 on the whole 60-point SIX60-A set, `logs/m3_review_t10/`). **Mutants:** dropping a `Model` field breaks the proof. | light, **now** | **done** 2026-11-06 (README "M3"): `hm : 2 ≤ m`, no extra hypothesis; early warning PASS (35 runs, exact SIX60 data at K = 8 among them); 13/13 field mutants and the nesting mutant break the build; about 1.56k code lines |
| **M4** | Merge LAYERLEAN + LEANEXT into an importable library | `geo/lakefile.toml` (requires the repo by path `../../../../..` and `encblean` by `..`), `geo/ES8Geo/{Layer,Phase,Link,PhaseClass,Capstone,Keys,Orbit}.lean` | `lake build` green in `geo`; axioms standard; statements equal to the source files (diff). **Infrastructure decision needed** (risk R5). | **Mathlib: after the cutoff (2026-11-16 17:00)** | 0.5–1 d |
| **M5** | Labelling | `geo/ES8Geo/Labelling.lean` | `labelling_of_counterexample` (§2.1) proved | Mathlib | 1–1.5 d |
| **M6** | Model of a labelling | `geo/ES8Geo/ModelOfLabelling.lean` | `modelOfLabelling` (§2.4) with every field proved. G9 first (go/no-go spike: 1 day) | Mathlib | 2–4 d |
| ~~M7~~ | ~~Reflection~~ | — | dropped; becomes M7′ only if variant B is needed (§1.2) | — | (1.5–3 d) |
| **M8** | Assembly, audit, mutants | `geo/ES8Geo/Main.lean`, `geo/ES8Geo/Audit.lean` | `sixfold_es8` (§1.1) with `#guard_msgs` on `#print axioms` = [propext, Classical.choice, Quot.sound]. A grep finds no `native_decide`/`implemented_by`/`extern`/`unsafe`/`sorry`, and no `decide`/`rfl` applied to `encB 6 8 11`. Mutation tests: changing a family in `genCoded` changes the hashes; deleting a `Model` field breaks M3. | Mathlib | 0.5 d |
| **M9** | Hash binding and write-up | `README.md`, `logs/hash_binding.log`, `scripts/resolve.sh` (as built: `EncB/Emit.lean` mode `twin-cube64`, `EncB/Render.lean`, `scripts/hash_binding.sh`, `scripts/resolve.sh`, `scripts/build_cake_lpr.sh`, `logs/m9_*`) | `encb_dimacs` prints base + 64 cubes from `encB`, taking the units from the Lean list `cubes64` itself (the theorem's definition, iterated in order), **not** from Emit's name-based `cubeUnits` (Emit.lean:73-84), so the hashes bind exactly the cubes the theorem quantifies over; each is hashed by streaming and deleted. The recorded hashes are read from the record files, never typed into the script. **65/65 equal the records** (base; 32 c-cubes `C6UPPER/SHA256SUMS.txt:88-119`; 32 n-cubes from `C6UPPER/noty12-2026-11-06/cubes.sha256`), plus the 3 other instances. The README has the trust table (§1.4) and P1's rigor line; the re-solve script covers E2 provenance. | light (one emission ≈ 6 s with Gen; the twin's time is unknown; as built: 7.5–14.6 s per cube, about 15 min per binding run) | **done** 2026-11-06, about 20:15 KST, not committed (README "M9"); "done when" against what was built: below the table |

**M9: "done when" against what was built.**

| "done when" says | as built (README "M9") |
|---|---|
| print base + 64 cubes from `encB`, units from the Lean list `cubes64` iterated in order, not from `cubeUnits` | `twin-base 6 8 11` and `twin-cube64 6 8 11 I` for I = 0..63: the exe writes the string `cnfText (encode 6 8 11) (cubes64.get ⟨I, h⟩)` with one `putStr` (one emission per cube, not one for all 64); `cubeUnits` is not used. `parseDimacs_cube64_get` is stated on exactly this expression |
| each file hashed by streaming and deleted | streamed into sha256sum; no file is written at all |
| recorded hashes read from the record files, never typed into the script | yes; each emitted hash compared on its own with every record of its name (two per file); n-cube units also against the noty12 row; Y map from `B_m6K8t11.meta.json`; every record row used exactly once; a self-test with one hex digit changed exits 1 |
| 65/65 equal the records, plus the 3 other instances | **68/68**, three runs (A1 exe `a0dff6f2…`; A2 exe `3d43fa8b…` twice), last one `logs/m9_a2fix_hash_binding.log`; the log file is `logs/m9_hash_binding.log`, not `logs/hash_binding.log` |
| not in the row | **added:** the DIMACS round trip (`EncB/Render.lean`): the exe's twin printer is a Lean function with `parseDimacs (render nv F) = some (nv, F)` proved, and `cubesUnsat64_of_texts_get`; E3/E4 narrowed (§1.4). After the M9 reviews (`EncB/Compose.lean`): the round trip on the UTF-8 bytes (`parseDimacsBytes_cube64_get`) and the composition with M3, `no_model_6811_of_texts`: if the 64 printed texts parse to unsatisfiable lists, no `Model 6 8 11` exists |
| the README has the trust table (§1.4) | README "Trust": a table of E1–E6 after M9 (what M9 settled, what stays trusted), and the details of E3/E4 |
| P1's rigor line | P1 updated (`WRITEUP/P1/p1.tex`: §1 "What is and is not claimed", §2 rigor labels, §3 "What is not in Lean", §6 "Checkers", Table 7, §8 "What is trusted" and a new paragraph "Encoder B in Lean", §10 "Formalization"; the soundness note in both copies: the rigor-label paragraph, the tag of Lemma k8s:lem:cube and the text after its proof, the 64-cube paragraph, the trust table, gaps (G1) and (G2); record in `WRITEUP/P1/README.md`, "Revision for the Lean encoder-B package"). The rigor note of Theorem 1.1 is unchanged; P1 says the sixfold bound is not formally verified end to end. `p1.pdf` rebuilt: 35 pages, 0 errors, 0 undefined references |
| the re-solve script covers E2 provenance | `scripts/resolve.sh` (reviewed, 10 defects fixed) and the build recipe `scripts/build_cake_lpr.sh`; smoke test 2/2 ACCEPTED twice; `resolve.sh all` and the build recipe **not run** (R7) |

**Totals (unverified):** about 1.9–2.8k new LOC (M2 0.4–0.6k, M3 1.0–1.3k, M5 0.15–0.25k, M6 0.55–0.8k, M8
0.1k), plus about 4k moved in M4. (M3 as built: about 1.56k lines of code, 2.0k in all, plus 0.3k of the
early-warning test; §3.2.) That is about 9–15 agent-days. Calendar time is shorter, because M2–M3 (Std-only)
can run now while M4–M6 wait for the cutoff.

**Done in this workflow:**

- **M0.** This file. The reference corpus `ref/hashes.tsv` (225 instances, made by `ref/make_ref.py` from gen_b2.py
  `3d47459a…`) was produced by the M1 step.
- **M1.** Done by the parallel M1 step. Its own README/report is authoritative; this is what its logs showed at 14:30:
  - `logs/compare_tiny.log`: `SUMMARY agree=225 disagree=0`.
  - `logs/check_recorded_small.log`: (6,8,9), (7,8,9) and (7,8,10) MATCH.
  - `logs/check_recorded_big.log`: one generation of (6,8,11) in 6.0 s and 426 MB RSS; base `479e31a9…`,
    `full_Y12`, c00000, c11011, c10101, c11111, n11111 and n00000 MATCH the records. The scratch files were deleted.
    I cross-checked three c-hashes against `C6UPPER/SHA256SUMS.txt:109,115,119` and n00000 against noty12
    `cubes.sha256:32`.
  - `EncB/KernelCheck.lean`: `decide +kernel` on (3,4,1), (3,4,2), (4,4,2); `#print axioms EncB.gen` = [propext].
- **M2.** Done by the M2 step (README "M2"). All the listed theorems are proved, with axioms within {propext,
  Classical.choice, Quot.sound}. `encB` = `gen` = Python as follows:
  - bytes on the 225-instance grid, on (6,8,9), (7,8,9) and (7,8,10), and on the (6,8,11) base and 7 cubes, taken
    from `cubes64`;
  - Lean values on 229 instances;
  - kernel evaluation on (3,4,1), (3,4,2), (6,4,1) and, after the review, (4,5,1) (two chain levels).

  `encB 6 8 11` takes 11.0 s to compute; the emission of base + 7 cubes took 15.3 s and 928 MB.
- **M3.** Done by the M3 workflow (README "M3"; plan `docs/M3PLAN.md`):
  - one interface unit (U0), six parallel units (U1–U6), each checked by an independent verifier, and an
    Integration step;
  - `encB_satisfiable` and `encB_satisfiable_6811` are proved with no `sorry`, no hypothesis beyond `heven`, `hm`
    and the `Model`, and axioms [propext, Classical.choice, Quot.sound].
- **M9.** Done (2026-11-06, about 20:15 KST; not committed; README "M9"):
  - A1: the mode `twin-cube64` and `scripts/hash_binding.sh`, 68/68 (E1);
  - A2: `EncB/Render.lean`, the twin's proved printer and the round trip through `parseDimacs` (E3/E4 narrowed, §1.4),
    with the index form `cubesUnsat64_of_texts_get` added after its verification;
  - A3: `scripts/resolve.sh` and `scripts/build_cake_lpr.sh` (E2 provenance), smoke test 2/2, 10 review defects fixed;
  - the write-up: README "M9" and "Trust", this file, and P1's trust and gap text;
  - the fixes of two reviews of M9 (README "M9 review fixes"): `EncB/Compose.lean` (bytes, `no_model_6811_of_texts`),
    a time gate and more forbidden tokens in `scripts/audit.sh`, build provenance in `scripts/hash_binding.sh`
    (68/68 again), and corrections of the README, this file, P1 and the note.
- **Not started:** M4–M8.

---

## 5. Open risks

| # | Risk | Likelihood / impact | Mitigation |
|---|---|---|---|
| R1 | ~~Some n-cube is not ACCEPTED, or `verify_final64.py` fails (4/32 ACCEPTED at 14:27, about 45–65 min each)~~ **Resolved 2026-11-06 15:40:35 KST:** 32/32 n-cubes ACCEPTED (hash-bound) and `verify_final64.py` PASS (`C6UPPER/noty12-2026-11-06/`). All 64 verdicts of `CubesUnsat64` are certified. | closed | Variant A is the primary target with every verdict certified. §1.2 (variant B, M7′) stays only as a record of the fallback; it is not needed. |
| R2 | M6's arc bridge G9 (key order → real arcs) stalls, as H2's `D3LabellingTarget` did (H2/README.md:179-189) | medium / blocks the end-to-end theorem | Spike G9 first in M6. Fallback: ship `sixfold66_of_unsat` conditional on a named Prop `ArcBridge`; M3 + M5 still remove most of gap G1. |
| R3 | The functional twin `encB` is too slow or too big at 2.4M clauses inside the 8G scope | low–medium / changes M2 | Stream the numbering; or prove directly over `gen` (§3.1 alternative). E1 must print the object the theorem is about. |
| R4 | Byte mismatch of the twin (Python dict/itertools order, `insSort` ties, numbering dedup) | low (Gen already matches everywhere) / found by testing | Gen is the oracle: compare twin against Gen at every grid point before any hash claim. |
| R5 | **Mathlib for `geo`**: lake would put Mathlib into `geo/.lake/packages` (clone + `lake exe cache get`, ≈5 GB, network), or reuse the parent's `.lake`, which these rules forbid touching. LAYERLEAN/LEANEXT were checked with `lake env lean` from the repo root, which also uses the parent's `.lake`. | certain / needs a user decision before M4 | Options: (a) cache get in `geo`; (b) user-approved `packagesDir` pointing at the parent's packages; (c) standalone files checked from the repo root after the cutoff. |
| R6 | Accidental kernel evaluation of `encB 6 8 11` (`decide`/`rfl`/`simp` unfolding) | low / build hangs | D9; theorems generic in m K t; review grep in M8. |
| R7 | E2 provenance: cake_lpr build `033aad53` ≠ vendored `a36874a8`; proofs not public | certain / reviewer objection, not a soundness gap | M9 re-solve script; record the build recipe; an archived deposit is a P1 open item (p1.tex:310-312). **Partly mitigated (M9):** `scripts/resolve.sh` regenerates any of the 64 verdicts from the Lean emitter with pinned CaDiCaL 2.1.3 and cake_lpr `c14ff498…` (smoke test 2/2 ACCEPTED, same proofs as recorded); `scripts/build_cake_lpr.sh` records the build of `033aad53` (source hashes pinned from the local clone, first recorded by M9; clean environment). **Open:** neither `resolve.sh all` (about 22 h, about 110 GB of proofs) nor the build recipe was run; the binary is still a build of `033aad53`, not of `a36874a8`; the proofs are still not public. |
| R8 | Interface drift: a `Model` field turns out unprovable from geometry (e.g. an edge case in `ccwIn` with equal keys) | low–medium / rework of M3 + M6 | The early-warning evaluation in M3 (done: every law held, as a Bool over valid labels, on exact SIX60 layer data at K = 8 and on the other base configurations, with 0 unsatisfied clauses; `logs/m3_early_warning.log`). Fields only constrain valid, distinct labels, and AltCCW/BlockCCW include `KeysDistinct`. |
| R9 | m = 7 stays written (perturbation), so P1's rigor line differs between its halves | certain / presentation | State it; m = 7 needs no byte identity (re-solve takes 802 s), only the perturbation lemma. |
| R10 | All LOC and day estimates are guesses calibrated on H2 and EHL | — | Re-estimate after the G9 spike and after M3. |

---

## Appendix A. Byte-identity checklist for the functional twin (from gen_b2.py and Gen)

1. `pts` is layer-major (gen_b2.py:51); triples come in `itertools.combinations` order (Gen:72-74).
2. `canon` compares sorted lists lexicographically on (i,k), choosing the first minimum over `tri` (Gen:103-109).
   Orbit variables are numbered in first-seen order.
3. The angular loop runs over orbit representatives in first-seen order. `free` = sorted layers ≠ 0.
   - Patterns come from `perms (range n)` in itertools order (Gen:78-83) and, for odd m, `bitTuples` (Gen:86-88).
   - Premises are `pairs free` then the H literals (Gen:198-204).
4. Key distinctness is tested **before** sorting (Gen:155). With distinct keys, any correct sort gives Python's
   order. `kinds` is a `List Nat`, and PPP is the first cyclic start (Gen:168-169).
5. Unit iff every pattern gives the same literal, which is not `none` (Gen:210-213). Otherwise conditional clauses
   are `(negated premises) ++ [l]`.
6. Nesting units use `olit (i,0) (i,1) (j,k)` in loop order (gen_b2.py:143-147).
7. Chains:
   - `okpair` in (a ∈ Q, b ∈ Q) order;
   - base clauses `[F₂(a,b), −l]`;
   - levels 2..L−1; skip pairs (b,c) with no F key at that level;
   - extension `[−F, −ok(a,b), −olit(a,b,c), F_{lev+1}]`, closing without the last literal;
   - skips: `a ∈ {b, c}`, `(a,b) ∉ okpair`, `is_false` turn literal.
8. Output: `p cnf nv nc\n`, then `' '.join(clause) + ' 0\n'`. No empty clause occurs; M1's `pushClause`
   (Emit.lean:57-60, gen modes only) and, since M9 A2, the twin's `pushClauseR` (Render.lean:127-130) print `" 0\n"`
   for one, as Python does, and `parseDimacs` reads that line as the empty clause (`parseDimacs_example`,
   Render.lean:325). The cube tail follows mkcubes.py:13-15 (gen: `cubeTail`, Emit.lean:69-70; twin: `cubeBodyR`,
   Render.lean:140, inside `renderCube`).
9. nv = the number of `new()` calls = `(allCodes m K t).length`, which must be duplicate-free (checked by bytes only).

## Appendix B. Checked while writing this (read-only)

- **Outlines and line numbers.** Declaration outlines (grep) and the cited statements were re-read in LL, Merged,
  Linked, Capstone, Capstone2, PhaseClassification, KeyOrder and OrbitConsistency; in
  `ErdosSzekeres/{Definitions,Orientation,OrientationGeometry}.lean`; in H `ETVEncoding/{Clauses,Dimacs}.lean` and
  H3 `MirrorEncoding/{Cover,CoverCore,Emit}.lean`; and in SYMLEAN `AffineReduction.lean:1263-1305`. Every line
  number cited above is from those reads.
- **The `diff`s of §3.6.** All empty except the noted trailing lines.
- **The Std-only claims.** `List.idxOf_cons_ne` and `List.getElem_idxOf` are in Mathlib, not core v4.24 (grep of
  `~/.elan/toolchains/leanprover--lean4---v4.24.0/src/lean` and `.lake/packages/mathlib`).
  `List.mergeSort_perm`/`sorted_mergeSort` are in core (`Init/Data/List/Sort/Lemmas.lean:274,299`).
  `Nat.repr` is `@[implemented_by reprFast]` (`Init/Data/Repr.lean:243`).
- **Cube layout and variable numbers.**
  - Python side: mkcubes.py:7,16-20 and noty12.py:76-82 (n-cube = header(nv, nc+6) + base + [−Y12] + pattern).
  - Y(1,2), Y(1,3), Y(1,4), Y(2,3), Y(2,4), Y(3,4) = 1, 2, 3, 10, 11, 18 at t = 11: by the numbering of
    gen_b2.py:36-39, the meta file, and the M1 log tail `1 0 2 0 3 0 -10 0 11 0 18 0` for c11011.
- **Status of `c6upper-noty12`, read-only.** `results.tsv` had 4 ACCEPTED rows (n00011, n00100, n00001, n00000)
  at 14:27. `verify_final64.py` exists in the job directory as the post-run gate. *Update 16:35:* the unit finished
  at 15:40:35 with 32/32 ACCEPTED, and `verify_final64.py` printed PASS; record `C6UPPER/noty12-2026-11-06/` (R1).

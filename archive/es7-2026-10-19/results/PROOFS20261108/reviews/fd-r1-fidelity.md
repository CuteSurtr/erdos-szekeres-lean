# Review fd, round 1, lens: fidelity

Section: `STAGE/sections/fd.tex` (1029 lines, last modified 15:43:52), map `STAGE/sections/fd.map.tsv` (32 rows).
Lean sources: `ErdosSzekeres/{Definitions,Orientation,OrientationGeometry,Basic,ConvexCycleCuts}.lean`,
`ErdosSzekeres/Suk/{FourPoint,SupportingLines,OrientationClique,Reflection}.lean`, `LAYERLEAN/LayerLemma.lean`,
`SYMLEAN/SymmetricReduction.lean`, `LEANEXT/orbit/OrbitConsistency.lean`, `MIRRORETV/lean/MirrorMain.lean`,
`SYMLEAN/mirror/ReductionThreeClasses.lean`, and (see F1) `SYMLEAN/AffineReduction.lean`.

**Verdict: FAIL** (no blocker; 1 major, 8 minor). Every statement that carries a Lean tag matches its declaration
exactly, and every contract `fd:` statement is true and correctly placed. The major finding is about attribution.
Lean has general counterparts of two contract facts, `fd:lem:affine-orient` and `fd:lem:affine-cp`, and partly of
`fd:lem:orient`(d). The section does not tag them. Its remarks and its Coverage paragraph also say that no such
counterpart exists.

## 1. Method

- Read the contract, both inventories (`MAIN-LIBRARY-coverage.json`, `LAYERLEAN.json`; also `SYMLEAN-core.json` for F1),
  the whole section and map, every cited Lean file at the cited lines, and the cited logs:
  `docs/validation/axiom-audit-lower-bound-2026-10-11.txt`, `LEANEXT/review/{axioms.log,REPORT.md}`,
  `LEANEXT/orbit/logs/{axioms.log,build.log}`, `LAYERLEAN/logs/build.log`, `SYMLEAN/logs/runs.tsv`,
  `MIRRORETV/lean/MirrorMain.out`, `SYMLEAN/mirror/README.md`.
- Checked the Mathlib definitions the section restates against the local Mathlib checkout at the pinned revision
  `f897ebcf72cd16f89ab4577d0c826cd14afaafc7` (read only): `ConvexIndependent` (Independent.lean:53),
  `convexIndependent_set_iff_notMem_convexHull_diff` (:145), `Collinear` (AffineSpace/FiniteDimensional.lean:366,
  `Module.rank k (vectorSpan k s) ≤ 1`), `collinear_iff_of_mem` (:420), `AffineIndependent` (Independent.lean:46),
  `convexHull` (Hull.lean:42, closure operator of `Convex`), `AffineMap.image_convexHull` (Hull.lean:193; its proof is
  the one the section describes), `Function.minimalPeriod` (PeriodicPts/Defs.lean:247), `Function.iterate_succ_apply'`,
  `ConvexIndependent.mono`, `Caratheodory.minCardFinsetOfMemConvexHull`. All match the section's descriptions.
- Recomputed all 14 SHA-256 prefixes in the source table: all match.
- Checked the commit (`7e32ee259`), the branch, the package name (`erdos_szekeres`), the toolchain (`lean-toolchain` =
  `leanprover/lean4:v4.24.0`) and Mathlib (`lake-manifest.json` rev `f897ebcf72cd…`). All match. The pins have not
  changed since 2026-10-04, so the 2026-10-11 audit ran under the stated versions. The last commits to the cited
  main-library files are dated 4 and 5 October 2026, as the section says.
- Checked every line cited in the axioms-evidence paragraph (audit lines 87/103/113/114/119/175/176; review log lines
  1/22/23/33; orbit `axioms.log` line 1). All match. Re-ran the source scans the section reports
  (sorry/admit/axiom/native_decide in the 9 main-library files plus BaseOrder/BaseChart/TriangleOrder, and in the five
  research files): clean, except the word "admits" in a docstring.
- Verified the claim "19 definitions of `rotAbout`, all with this same body": 19 found in RES, all with the identical
  two-line body.
- Checked the algebraic identities the section uses with a short sympy script. All 17 checks pass: the bracket form of
  `orient`; swap, cycle and translate; the `linear_combination` certificate `(p1 q0 − p0 q1)(u+v−1)`; the support sum;
  `rotAbout` (e) and (f); the composition law; orientation invariance under rotations; reflection det, orient sign,
  `F u = u` and `F u⊥ = −u⊥`; the affine det formula; all twelve support values in the proof of `fd:lem:four-positive`.
- Mechanical checks: the 32 map rows match the 32 statement environments (labels, Lean names, lines, 5 columns). The
  `\ref` targets are own labels or allowed export labels (`ll:def:hv`, `ll:def:peel`, `ll:def:66-70`,
  `oc:lem:rot-inv`). There are no machine paths or tool names. The existing compile log
  (`build/fd_wrapper.log`, 15:43:56, after the last edit) shows 13 pages and only these four expected undefined
  references.

## 2. Statement-by-statement fidelity (every name exists at exactly the cited line)

| label | Lean (file:line) | result |
|---|---|---|
| fd:def:point | `ErdosSzekeres.Point` Definitions.lean:9 | exact (`abbrev Point := Fin 2 → ℝ`) |
| fd:def:orient | `orient` Orientation.lean:9 | exact, over any `CommRing` |
| fd:def:conv | Mathlib `Convex`, `convexHull`, `AffineIndependent`, `AffineMap` | faithful restatements (checked at the pin) |
| fd:def:gp | `GeneralPosition` Definitions.lean:12 | exact (pairwise distinct, `¬ Collinear ℝ {a,b,c}`); `Collinear` = rank of `vectorSpan` ≤ 1 |
| fd:def:cp | `ConvexPosition` Definitions.lean:17 | exact (`ConvexIndependent ℝ` of the subtype inclusion; Mathlib definition quoted correctly) |
| fd:def:ngon | `HasConvexNGon` Definitions.lean:21 | exact (`t ⊆ s ∧ t.card = n ∧ ConvexPosition t`) |
| fd:def:forces | `ForcesConvexNGon` Definitions.lean:25 | exact (`GeneralPosition s → N ≤ s.card → …`) |
| fd:def:inv | `Invariant` LayerLemma.lean:105, SymmetricReduction.lean:271, OrbitConsistency.lean:47 | exact (maps into); the three are textually identical; full names correct (namespaces `ErdosSzekeres.LayerLemma`/`.SymReduction`/`.OrbitConsistency`) |
| fd:lem:inv-image (c) | `LayerLemma.iterate_mem` :52 | exact (arbitrary type `α`, `S : Finset α`, `∀ i`); (a),(b) are correctly marked written steps |
| fd:def:rot | `rotAbout` LayerLemma:298, SymmetricReduction:400, OrbitConsistency:93 | exact coordinate formula |
| fd:rem:angles | `Sixfold66`/`Sevenfold70` LayerLemma:1102/1107 | correct (`2 * Real.pi / 6`, real numerals) |
| fd:lem:rot (a) | `rotAbout_eq_crot` :302 | equivalent pointwise form; the Lean form `crot (toC c) (exp (θ I))` is quoted correctly |
| fd:lem:rot (b) | `rotAff` :311 (a `def`) | linear part `!![cos, −sin; sin, cos]` matches R_θ; see F2 |
| fd:lem:rot (c) | `rotAbout_iterate` :465 | exact (`(j:ℝ) * α`); the composition law is correctly marked a written step |
| fd:lem:rot (d) | `rotAbout_injective` :319 | Lean states injectivity only; the section states more (F2) |
| fd:lem:orient (a)-(c) | `orient_swap` :12, `orient_cycle` :15, `orient_translate` :18 | exact, any `CommRing` |
| fd:lem:collinear-mem | Mathlib `collinear_iff_of_mem` | exact (`p = r • v +ᵥ p₀`) |
| fd:lem:collinear (a),(b) | OrientationGeometry.lean:36, :66 | exact; the proof follows the Lean proof, including the private helper |
| fd:lem:cp-hull | `convexPosition_iff` Basic.lean:15 | exact |
| fd:lem:mono (a)-(d) | Basic.lean:11, :6, :20; `MirrorOdd.hasConvexNGon_of_le` MirrorMain.lean:2182 | exact; the full name `MirrorOdd.…` is right (top-level namespace); the copy at ReductionThreeClasses.lean:3741 is byte-identical (diffed) |
| fd:lem:ngon-basic | Basic.lean:25, :31 | exact |
| fd:lem:forces-basic | Basic.lean:47, :37 | exact |
| fd:lem:small (last assertion) | `convexPosition_of_card_three` Basic.lean:58 | exact; the rest is correctly marked a written step |
| fd:lem:four-subsets | FourPoint.lean:10, :40 | exact (`∀ t ⊆ s, t.card ≤ 4 → …`; `4 ≤ s.card`, `t.card = 4`) |
| fd:lem:halfplane | SupportingLines.lean:6, :11, :21 | exact (`u + v = 1`; strict and weak sets) |
| fd:lem:strict-supports | SupportingLines.lean:28 | exact (∀p ∃q ∀r ≠ p, 0 < orient p q r) |
| fd:lem:support-sum | SupportingLines.lean:40 | exact |
| fd:lem:four-positive | SupportingLines.lean:47 | exact (four strict inequalities; Finset `{a,b,c,d}`); the q's match the Lean `a+b−d`, `b+c−a`, `c+d−b`, `d+a−c` |
| fd:lem:pos-triples | OrientationClique.lean:9 | exact (linear order, `p` injective on all of ι, `4 ≤ s.card`, i<j<k in s, `s.image p`) |
| fd:lem:neg-triples | OrientationClique.lean:33 | exact |
| fd:lem:pos-cycle | ConvexCycleCuts.lean:11 | exact (`4 ≤ k`, `Fin N → Point` injective, `Fin k ↪ Fin N`, `∀ i, p (e i) ∈ P`, all increasing triples) |
| fd:rem:affine-orient-lean / affine-cp-lean / pos-cycle | OrbitConsistency:117, Reflection:47, :6, :52, ConvexCycleCuts:8, :31 | names, lines and statements correct (but see F1 and F7) |

All contract `fd:` statements (definitions and facts) are true and appear in the contract's order, each on the
statement named for it. Extra internal `fd:` labels (conv, inv-image, rot, collinear-mem, hull, ngon-basic,
forces-basic, small, halfplane, strict-supports, support-sum, neg-triples) are consistent with the contract.

## 3. Findings

### F1 (major): Lean counterparts exist for contract facts, but the section tags them as written steps and says no such counterparts exist

Where:
- `fd:lem:affine-orient` (fd.tex:417, head `[Orientation under affine maps; written step]`).
- `fd:rem:affine-orient-lean` (fd.tex:455-461): "Lean proves the special cases it needs separately".
- `fd:lem:affine-cp` (fd.tex:667, `written step`).
- `fd:rem:affine-cp-lean` (fd.tex:721-728).
- Coverage (fd.tex:1002-1007): "Written steps without a single Lean counterpart: \ref{fd:lem:orient}(d),(e),
  \ref{fd:lem:affine-orient}, … \ref{fd:lem:affine-cp} …".
- Map rows `fd:lem:affine-orient` and `fd:lem:affine-cp`.

Evidence. `SYMLEAN/AffineReduction.lean` (namespace `ErdosSzekeres.SymReduction`, SHA-256 prefix `41cfc0b60aec`) contains:
- `orient_affine` at :1241: `{g : Point → Point} {L : Matrix (Fin 2) (Fin 2) ℝ} {b : Point}
  (hg : ∀ p, g p = L *ᵥ p + b) (x y z : Point) : orient (g x) (g y) (g z) = L.det * orient x y z`. This is exactly the
  displayed formula of `fd:lem:affine-orient` and of the contract item.
- `convexPosition_image_affine` at :1263: injective `f : Point →ᵃ[ℝ] Point` maps convex position to convex position.
  This is the forward direction of `fd:lem:affine-cp`(b).
- `generalPosition_image_affine` at :1278 (hypotheses `∀ p, g p = L *ᵥ p + b` and `L.det ≠ 0`) and
  `generalPosition_image_affineEquiv` at :1290. These are the forward direction of (c).
- `hasConvexNGon_image_affine` at :1298: injective Mathlib affine map. This is the forward direction of (d).
- `injective_of_affine` at :1305: `det L ≠ 0` implies injective. This is the converse of the section's
  "injective ⇒ det A ≠ 0".

Section ar already cites these: ar.tex:345 (`ar:lem:orient-affine`), :393, :413, :440. There is axioms evidence:
`SYMLEAN/logs/runs.tsv` has the rows `AffineReduction.lean 41cfc0b6 exit 0` and `AffineReductionAxioms.lean exit 0`, and
`SYMLEAN/logs/AffineReductionAxioms.out` prints `hasConvexNGon_image_affine` and `generalPosition_image_affineEquiv`
with the three standard axioms.

A smaller instance of the same problem: for R = ℝ, `fd:lem:orient`(d) is `ErdosSzekeres.OrbitConsistency.orient3_perm`
(LEANEXT/orbit/OrbitConsistency.lean:178, export label `oc:lem:perm`, which fd may \ref). Yet the Coverage paragraph lists
(d) as having no single Lean counterpart. The section's (d) holds over any commutative ring, so it is more general, but
the Coverage sentence is still inaccurate.

Why this is a problem. The task scope requires each fd item to be "tagged with its Lean name(s) where one exists".
Contract rule 9 requires Coverage to be honest about scope. The remark and Coverage sentences are factually wrong about
the Lean record, and they lead a reader to think that the general orientation-scaling formula and the affine transport
lemmas are not Lean-checked. Nothing mathematical is affected: the written proofs are correct and the statements are
true.

Uncertainty. `SYMLEAN/AffineReduction.lean` is not in this task's list of Lean sources, and the contract item names no
Lean declaration. If the orchestrator rules that tagging is optional here, this finding drops to minor. The two false
sentences (the remark and Coverage) still have to be corrected.

Suggested fix:
- Tag `fd:lem:affine-orient` with `\leanref{ErdosSzekeres.SymReduction.orient_affine}{SYMLEAN/AffineReduction.lean:1241}`.
  The statement already matches if g is taken as given by `∀ p, g p = L *ᵥ p + b`.
- Tag the forward directions of `fd:lem:affine-cp`(b)-(d) with `convexPosition_image_affine` (:1263),
  `generalPosition_image_affine` (:1278) or `generalPosition_image_affineEquiv` (:1290), and
  `hasConvexNGon_image_affine` (:1298). Mark the reverse directions as written steps, and (a) as Mathlib's
  `AffineMap.image_convexHull`. Note `injective_of_affine` (:1305).
- Rewrite `fd:rem:affine-orient-lean` and `fd:rem:affine-cp-lean` so that they name the general research-file versions
  as well as the main-library special cases.
- Mention `orient3_perm` (`oc:lem:perm`) for `fd:lem:orient`(d) over ℝ.
- Correct the Coverage sentence.
- Add `SYMLEAN/AffineReduction.lean` (`41cfc0b60aec`) to the source table, and its runs/axioms logs to the evidence
  paragraph.

### F2 (minor): `fd:lem:rot`(d) and (b) attach a Lean name to a statement that says more than the declaration

- (d) at fd.tex:324-325: "ρ_θ is a bijection of R² with inverse ρ_{−θ}; in particular it is injective". It is tagged
  `rotAbout_injective`, but LayerLemma.lean:319 states only `Injective (rotAbout c θ)`.
- (b) at fd.tex:318-320 includes "In particular ρ_θ(c) = c", which is not part of the `def rotAff` (:311-317). In Lean
  that fact appears only as a `have` inside `invariant_erase_centre`, :330-332.
- Part (c) handles the same situation explicitly (fd.tex:322-323): "(The Lean declaration cited for (c) is this iterate
  formula; the composition law is a written step here.)"

Fix: add a matching parenthesis to (d), for example "(The Lean declaration cited for (d) states injectivity;
bijectivity and the inverse are a written step.)", and a similar one for ρ_θ(c) = c in (b). This also keeps the purpose
paragraph's promise (fd.tex:8) that Lean-tagged statements are "stated exactly as in Lean".

### F3 (minor): the path convention does not cover top-level repository files, so the section's own `lean-toolchain` and `lake-manifest.json` point to the wrong place

fd.tex:16-20 says that paths beginning with `ErdosSzekeres/`, `docs/`, `experiments/` or `scripts/` are relative to the
repository root and that "every other path" is relative to RES. Under that rule, "file `lean-toolchain`" and
"file `lake-manifest.json`" (fd.tex:27-29) resolve to `RES/lean-toolchain` and `RES/lake-manifest.json`. Neither exists:
both files are at the repository root (checked).

Fix: add "the files `lean-toolchain`, `lake-manifest.json` and `lakefile.toml` at the top of the repository" (or "a bare
file name without a directory names a file at the repository root").

### F4 (minor): the line-number convention lists only `def`, `abbrev` and `theorem`

fd.tex:21-22. Later sections cite `structure` and `inductive` declarations:
- `ErdosSzekeres.Omission.Configuration` is a `structure` at ErdosSzekeres/Omission/Realization.lean:8 (cited by
  mm.tex:127 as :9).
- `OrbitConsistency.RotComp` is an `inductive` at LEANEXT/orbit/OrbitConsistency.lean:145.

Fix: "the line that carries the declaration keyword (`def`, `abbrev`, `theorem`, `structure`, `inductive`, …)".

### F5 (minor): the prefix convention is ambiguous for names outside the `ErdosSzekeres` namespace

fd.tex:23-25 says that running text "sometimes omit[s] the common prefix `ErdosSzekeres.`". `MirrorOdd.hasConvexNGon_of_le`
is used in running text (fd.tex:152, :989). Under this convention it could be read as
`ErdosSzekeres.MirrorOdd.hasConvexNGon_of_le`, but its full name has no such prefix: `MirrorOdd` is a top-level
namespace (MirrorMain.lean:12; ReductionThreeClasses.lean:1571). The statement head does give the correct full name.

Fix: one clause saying that names in the namespace `MirrorOdd` (and any other non-`ErdosSzekeres` namespace) are
always written in full.

### F6 (minor): the axioms-evidence paragraph understates coverage

fd.tex:128-133 says that `ForcesConvexNGon.mono` and eleven other helpers "are not covered by a saved `#print axioms`
output that we identified". `ForcesConvexNGon.mono`, however, is used in the proof of `conjecturedBound_le_of_forces`
(ErdosSzekeres/LowerBound/Construction.lean:118, `h.mono …`). The same audit file prints that theorem at line 725 with
the three standard axioms. By the dependency-closure argument the section itself uses (fd.tex:120-127), the helper is
therefore covered.

`orient_cycle`, `orient_swap` and `convex_orient_nonnegative` are used in `Suk/AdjacentSpikes.lean` (:81-163) and
`Suk/SpikeGeometry.lean` (:108-112) and are probably in the closure of audited Suk theorems; I did not trace the full
closure. This understates the evidence rather than overclaiming it.

Fix: cite audit line 725 for `ForcesConvexNGon.mono`, and either trace the others or keep the hedge.

### F7 (minor): `fd:rem:pos-cycle` says `ConvexCycleCut` is "used in SAT searches"

fd.tex:934-936. The sources describe these searches differently:
- The Lean docstring (ConvexCycleCuts.lean:5-7) says "repair searches".
- The docstring of `convexCycleCut_of_avoids` (:28-30) says "This does not verify an SMT solver".
- docs/SAT.md:229-233 describes the clauses as cuts for SMT coordinate (planar-repair) searches.

Fix: say "used as clauses in the SMT repair searches" (or "solver searches").

### F8 (minor): map completeness and format

- (i) The seven `remark` environments have no map rows. Three of them name Lean declarations with file:line:
  `orient_rotAbout_inv` :117, `orient_reflectY` :47, `HasConvexNGon.linearEquiv` :6, `generalPosition_reflectY` :52,
  `ConvexCycleCut` :8 and `convexCycleCut_of_avoids` :31. Nine of the other ten section maps include their remarks
  (contract: "one row per statement environment").
- (ii) The `lean_name` column contains annotations such as "(part c)", "(a)", "(b)" and "Mathlib: …" instead of bare
  Lean names. This is harmless, but it breaks a mechanical cross-check.

### F9 (minor): the Coverage list of uncovered declarations is incomplete for a file in the section's source table

`ErdosSzekeres/Suk/Reflection.lean` is listed among the section's sources (fd.tex:100). Only three of its declarations
are mentioned (in remarks). `reflectY` (:34), `reflectY_x` (:42), `reflectY_y` (:43), `reflectY_reflectY` (:44) and
`hasConvexNGon_of_reflectY` (:64) are neither covered nor listed under "Deliberately not covered". That paragraph's
header reads "(declarations of the cited files outside the foundations list)", which suggests completeness. The file is
not in this task's scope list, so this is not a coverage failure.

Fix: one sentence saying that the remaining declarations of `Reflection.lean` and of the research files belong to other
sections or lie outside Stage 1.

## 4. Items checked and found correct (no action)

- The purpose paragraph and the three rigor labels. No overclaiming vocabulary appears. The project has no
  `native_decide`, so defining "Lean-checked" by the three standard axioms is consistent.
- The arithmetic conventions: casts, `x/0 = 0`, truncated subtraction, iterate order `f^[n+1] = f^[n] ∘ f`, and
  `minimalPeriod` (0 if aperiodic).
- Every Lean-tagged statement head uses the full name, which exists at exactly the cited line.
- All written proofs I checked for fidelity-relevant steps (the Lean-following proofs of collinear, four-subsets,
  strict-supports, four-positive, pos-triples, neg-triples, pos-cycle) match the Lean proof outlines they claim to follow.
  The direct proofs (cp-hull, small, affine-cp, Carathéodory, separation) are correct.

# Section `oc`, round 1: fidelity review

**Verdict: PASS.** No blocker or major findings. Four minor findings (F1 to F4) are listed at the end.

Paths: Lean and log files are relative to the results directory (`RES`). Section files are relative to the staging
directory (`sections/oc.tex`, `sections/oc.map.tsv`).

## What was checked and how

- Read `CONTRACT.md`, the `LEANEXT` inventory entries for this scope, all of `sections/oc.tex` (870 lines, 43 statement
  environments) and `sections/oc.map.tsv` (43 rows).
- Lean sources read in full or over the whole scope: `LEANEXT/orbit/OrbitConsistency.lean` (all 429 lines),
  `LEANEXT/merged/Merged.lean` lines 1140-1385, `LEANEXT/keys/KeyOrder.lean` (all 158 lines), `LEANEXT/README.md`.
  For the copied definitions and the layer-lemma facts: `LAYERLEAN/LayerLemma.lean` (orbitFS :48, iterate_mem :52,
  Invariant :105, hullVerts :111, complex helpers :231-308, minimalPeriod_rotAbout :336, hullVerts_eq_orbitFS_rotAbout
  :364, peel :374, invariant_peel :386, peel_antitone :460, rotAbout_iterate :465, centre_not_mem_of_even :582, polar
  :932). Core library: `ErdosSzekeres/Definitions.lean` (Point, GeneralPosition, ConvexPosition, HasConvexNGon),
  `ErdosSzekeres/Orientation.lean` (orient), `ErdosSzekeres/OrientationGeometry.lean:66`.
- Mathlib facts the section states were checked against a local source tree of the pinned Mathlib commit `f897ebcf72cd`:
  `toIcoDiv` (Algebra/Order/ToIntervalMod.lean:44, the unique `n` with `b - n • p ∈ Ico a (a+p)`), `toIcoMod` (:67,
  `b - toIcoDiv hp a b • p`), `toIcoMod_eq_iff` (:144, `toIcoMod hp a b = c ↔ c ∈ Ico a (a+p) ∧ ∃ z : ℤ, b = c + z • p`),
  `Prod.Lex.lt_iff` (Data/Prod/Lex.lean:58), `Equiv.Perm.swap_induction_on` (GroupTheory/Perm/Sign.lean:97, step
  `∀ f x y, x ≠ y → P f → P (swap x y * f)`), `Int.units_eq_one_or` (Algebra/Ring/Int/Units.lean:28). The section's
  Definition `oc:def:keys`, Lemma `oc:lem:toico` and Fact `oc:fact:sign` (S1)-(S4) match these exactly.
- Automated cross-checks (scripts, output discarded):
  - All 52 `\leanref{Name}{File:Line}` pairs resolve to a declaration of that name at exactly the cited line (offset 0
    in every case).
  - All 43 environments have a map row with the same label and kind. The map's `lean_name` and `file_line` columns
    equal the `\leanref` lists in the heads, element by element.
  - No label is defined twice. Every `\ref` is either an `oc:` label of this section or one of the allowed export labels
    `fd:def:{point,orient,gp,ngon,inv,rot}`, `fd:lem:{orient,affine-orient,collinear,cp-hull,mono,separation}`,
    `ll:def:{hv,peel}`, `ll:lem:{antitone,inv-peel,minperiod}`, `ll:thm:core-rot`, `lg:def:polar` and `lg:lem:centre`.
    Each of these is defined in its section file.
- Compile check in a separate wrapper (removed afterwards). `nice -n 15 pdflatex` ran twice with exit 0. The only
  undefined references are the 20 `fd:`/`ll:`/`lg:` labels, which is expected in a standalone build. No error, no
  "Missing $", no multiply-defined label.
- Hard rules: neither file contains a machine path, a tool name, `\newcommand`, `\usepackage` or
  `\begin{document}`.

## Statement-by-statement comparison with Lean

All match. "OC" is `LEANEXT/orbit/OrbitConsistency.lean`, "MG" is `LEANEXT/merged/Merged.lean` and "KO" is
`LEANEXT/keys/KeyOrder.lean`.

| label | Lean (file:line) | hypotheses, conclusion, types: result |
|---|---|---|
| oc:def:basic | OC Invariant :47, rotAbout :93, polar :112 | Formulas identical. `Finset Point`; Invariant is maps-into; r is unrestricted in polar. OK |
| oc:lem:iterate | OC :105; LAYERLEAN :465 | `(rotAbout c α)^[j] = rotAbout c (j*α)`, with j : ℕ cast to ℝ and no hypotheses. OK |
| oc:lem:iter-mem | OC :39; LAYERLEAN :52 | Any type, `Finset S`, `∀ y ∈ S, f y ∈ S`, `x ∈ S`, conclusion `∀ i`. The LAYERLEAN copy has `omit [DecidableEq α]`, so it adds no instance hypothesis. OK |
| oc:lem:rot-inv | OC :117 | No hypotheses; a, b, d arbitrary. OK |
| oc:def:preserves | OC :124 | `∀ a b d`. OK |
| oc:def:rotcomp | OC :145 | Rules id and step with `k : ℤ`, giving `rotAbout c (k*(2π/m)) ∘ g`; any m, with 2π/0 = 0 noted. OK |
| oc:lem:rotcomp-pres | OC :127, :129, :134, :141, :150, :157 | (a) states the four helpers exactly (`f ∘ g` order, `f^[n]` for all n). (b) holds for any m. (c) is `∀ s, RotComp c m (rotAbout c (2π/m))^[s]`. OK |
| oc:def:orient3 | OC :168 | OK |
| oc:lem:swap | OC :171 | `x ≠ y` in Fin 3, `t ∘ swap x y`. OK |
| oc:lem:perm | OC :178 | Quantifier order is ∀σ, ∀t; the sign is cast ℤˣ→ℤ→ℝ. OK |
| oc:lem:rot-perm | OC :194 | `g ∈ RotComp c m`, `t' = g ∘ t ∘ σ`. OK |
| oc:lem:two-reps | OC :204, :216 | (a) has the `orient3 t ≠ 0` hypothesis and concludes equality in ℤˣ. (b) has no nondegeneracy hypothesis and concludes equality in ℝ. Both g's share c and m. OK |
| oc:def:litval | OC :223 | ε ∈ ℤˣ; `if ε = 1 then 0 < o else ¬ 0 < o`. OK |
| oc:thm:literal | OC :228 | `C = g ∘ t ∘ σ` and `orient3 t ≠ 0`; iff with `litVal (sign σ) C`. OK |
| oc:thm:encoder | OC :253 | `ι : Type*`; `hr` quantified over all labels; `T₀ = T ∘ σ₁`; `C = r^[s] ∘ T₀ ∘ σ₂`; product of the signs in ℤˣ; P need not be injective; any m. OK |
| oc:lem:antipode | OC :273; MG :1160 | `Even m`, `0 < m`, Invariant, `x ∈ S`; conclusion `![2c₀−x₀, 2c₁−x₁] ∈ S`. OK |
| oc:lem:same-ray | OC :295; MG :1181 | `Even m`, `0 < m`, Invariant, GP, `x ≠ y`, `0 < l`. Lean's `hray → False` is written as `y − c ≠ l(x − c)`, and the section says so explicitly. OK |
| oc:lem:polar-rot | OC :355, :383; MG :1241, :1269 | No hypotheses; n : ℤ. OK |
| oc:lem:phase-nat | OC :363; MG :1249 | k : ℕ; r, r' > 0; both polar points in S; conclusion is an equality. OK |
| oc:lem:phase-int | OC :389; MG :1275 | k : ℤ; conclusion `∃ j : ℕ`. The choice "j = k mod m" is attributed to the proof only. OK |
| oc:thm:phase-orbit | OC :420; MG :1304 | `horb : ∀ j : ℕ, … ≠ …`; conclusion `∀ k : ℤ, β ≠ α + k(2π/m)`. OK |
| oc:lem:disjoint | MG :1316, :1322 | No hypothesis on S; (a) i < j; (b) i ≠ j, concluding False. OK |
| oc:lem:closed | MG :1330 | `0 < m`, `K ≤ 2m`, `c ∉ S`, Invariant, `¬HasConvexNGon K S`; no Even and no GP, as in Lean; `∀ k : ℕ`. OK |
| oc:thm:layers-ray | MG :1350 | `2 ≤ m`, Even, `K ≤ 2m`, `c ∉ S`, Invariant, GP, `¬HasConvexNGon K S`, `i ≠ j`, k : ℕ, `0 < l`; `hray → False`. OK |
| oc:thm:layers-phase | MG :1367 | The same, plus r, r' > 0 and the polar points in the two hull-vertex layers; conclusion `∀ k : ℤ, β − α ≠ k(2π/m)`. OK |
| oc:lem:cell | KO :23, :45 | `u > 0`, J : ℤ, `0 ≤ ψ < u` (right end strict). OK |
| oc:lem:rank | KO :62, :71 | Set vs Finset is kept apart: the Finset version has `StrictMonoOn rank (S : Set ℝ)` and Finset membership. rank : ℝ → ℕ; `toLex` in ℤ ×ₗ ℕ. OK |
| oc:lem:reduce | KO :81 | N : ℤ with N > 0; `u > 0` is kept although it is redundant; `N*u = 2π`; `toIcoMod two_pi_pos 0`; Euclidean `J % N`. OK |
| oc:lem:antipode-cell | KO :100, :115 | (a) has `0 < m` only (no oddness, as remarked), with `(J+m) % (2m)` formed in ℤ. (b) has `Even m`, with `(m/2 : ℕ)` cast to ℤ, then `% m`. OK |
| oc:thm:key | KO :139 | As in Lean, with `S : Set ℝ`. OK |

Written steps (`oc:lem:rot-add`, `oc:cor:period`, `oc:lem:toico`) and the paraphrased layer-lemma facts (L1)-(L3) were also
checked. (L1) is `peel_antitone` (`n ≤ n'`) plus `hullVerts_subset`. (L2) is `invariant_peel` (`0 < m`, `c ∉ S`,
Invariant ⇒ ∀ n). (L3) is `hullVerts_eq_orbitFS_rotAbout`, with orbitFS the image of `range m`. All three match the
LAYERLEAN statements and the `ll` section's statements. The hypotheses of `centre_not_mem_of_even` quoted in
Remark `oc:rem:layers`(1) match `LAYERLEAN/LayerLemma.lean:582`.

## Provenance and log claims verified

- SHA-256 prefixes: OrbitConsistency.lean `9b843180ac38`, Merged.lean `245b7d65407a`, KeyOrder.lean `6e34096cff52` and
  LayerLemma.lean `afb8542dceb0` are all correct. `ENCBLEAN/geo/ES8Geo/{OrbitConsistency,KeyOrder}.lean` have the same
  digests.
- Line counts 429, 1385 and 158 are correct. Section 13 of Merged.lean spans 1149-1383, and OC new content starts at 114.
- diff checks:
  - Merged 1-1147 = LayerLemma 1-1147 (empty diff).
  - Merged 1159-1311 vs OC 272-427: only doc comments differ.
  - Merged 1148-1383 = Capstone2 1156-1391 (empty diff).
  - OC copied block vs LayerLemma: toC through crot_iterate (OC 49-90 = LL 230-271), rotAbout and rotAbout_eq_crot
    (OC 92-103 = LL 297-308), rotAbout_iterate (OC 105-109 = LL 465-469) and Invariant are identical. iterate_mem
    differs only in the type-variable binder. polar differs in its doc comment (F1).
- Axiom logs:
  - `LEANEXT/orbit/logs/axioms.log` lines 1-15 print exactly the 15 names listed in the Axioms paragraph, then `exit=0`.
  - `LEANEXT/merged/axioms.log` lines 1-6 print the 3 in-scope names plus layers_are_orbits, convexNGon_of_layers and
    sevenfold_octagon.
  - `ENCBLEAN/logs/m4_build.log` lines 3-10 print the 8 KeyOrder theorems.
  - Every axiom set printed is `[propext, Classical.choice, Quot.sound]`.
- `decide` occurs only at OC:236 (`-1 ≠ 1` in ℤˣ) and MG:1125 (`Even 6`), as stated. None of the three files contains
  sorry, admit, an axiom declaration or native_decide. PreservesOrient.iterate is used only in its own recursive call,
  as the section says.
- Toolchain: `lean-toolchain` is v4.24.0 and the `lake-manifest.json` mathlib rev is `f897ebcf72cd`. Neither has changed
  since 2026-10-04 (read-only git log), so this was the toolchain of the 2026-11-04 LEANEXT build.
- External references:
  - `LEANEXT/README.md:6`: correct.
  - `ENCBLEAN/geo/ES8Geo/Orbit.lean:13`: `rotAbout_eq_orbitConsistency … := rfl`, correct.
  - `ErdosSzekeres/OrientationGeometry.lean:66`: correct.
  - `C7UPPER/gen.py:108` `sortpar`: bubble sort that flips the parity at each adjacent swap. The canonical-rep parity
    `s2` (gen.py:78-85) is also computed by sortpar, so the remark's account covers both σ₁ and σ₂.
  - `C6UPPER/encb/gen_b2.py:56` `perm_sign`: counts pairs x<y with a_x > a_y, as stated.
  - `LEANEXT/orbit/logs/check_literals.log` lines 1-5: 42840 + 39270 + 12144 + 274560 = 368,814 ordered triples with 0
    mismatches, and line 1 is the sortpar = sign check. Correct.
  - `ENCBLEAN/DESIGN.md:625` (row "Lemma orbit (b)": the mismatch, and "Not used") and `:626` (row "Lemma keys"):
    correct.
  - `LEANEXT/keys/REPORT.md:22-25` ("Still hypotheses"): correct.
- The six-case table of Remark `oc:rem:parity` was recomputed with the product convention (στ)(i) = σ(τ(i)). All six
  products, inversion counts and signs are correct.
- The example in Remark `oc:rem:layers`(3) was re-checked: m = 4, K = 8 ≤ 2m, c ∉ S, general position (every collinear
  triple would contain two points of the same kind, and the six plus six lines through such pairs carry no third
  point), layer 0 = outer points, layer 1 = inner points, ¬HasConvexNGon 8 S (|S| = 8 and S is not in convex
  position), and β − α = π/4 = π/m. All hypotheses of Theorem `oc:thm:layers-phase` hold.

## Coverage

All 13 export labels assigned to `oc` by the contract are defined on the right statements:
- rot-inv: orient_rotAbout_inv
- perm: orient3_perm
- literal: literal_sound
- encoder: encoder_literal_sound
- antipode: antipode_mem_of_even
- same-ray: same_ray_false
- phase-orbit: phase_ne_of_not_mem_orbit
- layers-ray: not_same_ray_of_distinct_layers
- layers-phase: phase_ne_of_distinct_layers
- cell: cell_lt_iff and cell_eq_iff
- rank: cell_lt_iff_rank
- antipode-cell: antipode_odd and antipode_even
- key: reduced_lt_iff_key

Every declaration in the scope is covered:
- OrbitConsistency (45 declarations): all covered, except 15 complex-coordinate helpers (lines 49-103), which are listed
  under "Not covered" with a valid reason.
- Merged section 13 (12 declarations): all covered.
- KeyOrder (8 theorems): all covered.

The Coverage paragraph lists all of these correctly.

The task notes are addressed. Remark `oc:rem:parity` says that the inversion-count parity is not modelled in Lean and
gives a written six-case bridge. The half-open intervals and `toIcoMod` are stated exactly: Definition `oc:def:keys`(a),
Lemma `oc:lem:toico`, and Remark `oc:rem:halfopen`, which shows that `ψ < u` cannot be weakened to `ψ ≤ u` and that the
reduction lands in [0, 2π).

## Findings

### F1 (minor): "same text" claim for the copied block is slightly too strong
- Location: Remark `oc:rem:copies`, sections/oc.tex:128-131.
- Issue: The remark says the copied declarations have "the same text (up to the declaration of a type variable)" as
  the LayerLemma ones. The code is identical, but the doc comment of `polar` differs.
- Evidence: `OrbitConsistency.lean:111` reads "The point `c + r (cos θ, sin θ)`." and `LAYERLEAN/LayerLemma.lean:931`
  reads "The point at distance `r` from `c` in direction `θ`." The diff of the other copied pieces is empty, apart from
  the iterate_mem binder.
- Suggested fix: write "the same code (up to the binder of a type variable; one doc comment differs)".

### F2 (minor): overview item (B) omits `m > 0`
- Location: sections/oc.tex:16-19.
- Issue: The overview says "For even $m$, a finite set in general position that is mapped into itself by the rotation
  ρ by 2π/m about c contains the antipode 2c−x of each of its points, and no two of its points lie on one open ray from
  c". Under Lean's convention 2π/0 = 0, which the section itself stresses at :107-108, m = 0 is even and ρ = id. Both
  claims then fail. For example, take S = {(1,0),(2,0)} and c = (0,0): S is in general position, but (−1,0) ∉ S and
  (2,0) − c = 2((1,0) − c). The formal Lemmas `oc:lem:antipode` and `oc:lem:same-ray` correctly include `0 < m`, so
  only the overview prose is affected.
- Suggested fix: "For even $m>0$".

### F3 (minor): the stated axiom evidence does not cover every statement labelled Lean-checked
- Location: the Rigor paragraph (sections/oc.tex:80-81), the Axioms paragraph (:55-78), and the map rows `oc:lem:iterate`
  and `oc:lem:iter-mem`.
- Issue: The Rigor paragraph says every statement with a Lean reference is "Lean-checked in the sense of the logs above",
  but the logs cited above do not cover two cases.
  - (i) `PreservesOrient.iterate`, in the head of Lemma `oc:lem:rotcomp-pres`, has no axiom output, as the Axioms
    paragraph itself says at :74. The evidence that it was checked is the clean compile of the whole file
    (`LEANEXT/orbit/logs/build.log`: `exit=0`) together with the absence of `sorry`. That log is not cited.
  - (ii) Lemmas `oc:lem:iterate` and `oc:lem:iter-mem` cite the LAYERLEAN copies (`LAYERLEAN/LayerLemma.lean:465`, `:52`).
    Their axiom output is in `LEANEXT/review/axioms.log` lines 33 and 1; iterate_mem uses only `[propext, Quot.sound]`.
    Alternatively they are covered transitively by `LAYERLEAN/logs/axioms.log`. Neither log is mentioned, and the two map
    rows give no axiom source. (The OrbitConsistency copies are covered transitively by `orbit/logs/axioms.log`
    through `antipode_mem_of_even`, but the section does not say so either.)
- Severity: This is not an overclaim in substance, because the declarations compile in files without `sorry`. It is a
  gap in the cited evidence.
- Suggested fix: cite `LEANEXT/orbit/logs/build.log` for the whole OrbitConsistency file and `LEANEXT/review/axioms.log`
  (or LAYERLEAN's logs) for the LAYERLEAN copies, and update the two map notes.

### F4 (minor): the Dependencies paragraph is incomplete
- Location: sections/oc.tex:88-97.
- Issue: The paragraph lists the `fd`, `ll` and `lg` labels used, but omits four that are referenced:
  - `fd:lem:affine-orient` (:210)
  - `ll:lem:minperiod` (:616)
  - `fd:lem:cp-hull` (:669)
  - `fd:lem:separation` (:672)

  All four are allowed by the contract and defined in their sections, so only the list is inaccurate.
- Suggested fix: add them, marking the remark-only and parenthetical uses as is already done for `lg:lem:centre`.

## Summary

Every Lean-referenced statement and definition in `oc` matches its Lean declaration, in hypotheses, conclusion,
quantifier order, types and casts, strictness, Finset vs Set, and maps-into. Every name sits at exactly the cited line.
All 13 export labels are defined on the right statements, coverage is complete, and the section compiles. The four
findings are minor documentation imprecisions.

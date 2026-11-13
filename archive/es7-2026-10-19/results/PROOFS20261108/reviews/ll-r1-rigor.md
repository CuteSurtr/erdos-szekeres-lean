# Review of section `ll` (round 1, lens: rigor)

Section: `STAGE/sections/ll.tex` (760 lines) and `STAGE/sections/ll.map.tsv` (31 rows).
Lean source: `LAYERLEAN/LayerLemma.lean` (1148 lines, SHA-256 `afb8542dceb0c170...`), lines 1-470 and 995-1148 read in
full, plus 470-640 for context.

**Verdict: PASS.** No blocker and no major finding. Eight minor findings (M1-M8) are listed at the end. Every proof was
checked step by step. Every algebraic and trigonometric identity was checked with sympy. Every statement was compared
with its Lean declaration (hypotheses, conclusion, quantifier order, casts, natural subtraction).

## 1. Fidelity of the statements to Lean

I compared each statement with the Lean text. All 31 statement environments match their declarations. The
`\leanref` line numbers are all exact (0 off).

| label | Lean declaration (line) | result |
|---|---|---|
| ll:def:orbit | orbitFS (48) | image of `range p` under `i ↦ f^[i] x`; matches |
| ll:lem:orbit (a)-(f) | iterate_mem 52, mem_orbitFS_self 59, orbitFS_subset 62, orbitFS_invariant 68, card_orbitFS_of_minimalPeriod 80, mem_orbitFS_of_not_disjoint 91 | hypotheses match exactly (`0<p`, `f^[p] x = x`, `f^[p] y = y`, `¬Disjoint`, `minimalPeriod f x = p`) |
| ll:def:inv | Invariant (105) | maps into; matches |
| ll:def:hv, ll:lem:hv-basic | hullVerts 111, mem_hullVerts 114, hullVerts_subset 118 | matches |
| ll:lem:hv (a)-(d) | 121, 130, 146, 139 | matches (extreme points of `conv S`; `S ⊆ conv hv S`; `S.Nonempty → (hv S).Nonempty`) |
| ll:lem:map-hv | map_mem_hullVerts 162 | injective affine f, maps-into hypothesis; matches |
| ll:thm:core | hullVerts_eq_orbitFS 189 | `0<m`, `K ≤ 2m`, maps-into, `minimalPeriod f y = m` on S, `¬HasConvexNGon K S`, then for every hull vertex x; matches, no general position |
| ll:lem:inv-sdiff | invariant_sdiff_hullVerts 217 | `0<m`, maps-into, `f^[m] y = y` on S; matches |
| ll:def:complex, ll:lem:complex (a)-(g) | toC 231, ofC 234, crot 252, the 13 lemmas 236-287 | matches (w ≠ 1 in (f), w ≠ 0 in (g)) |
| ll:def:rot, ll:lem:rot (a)-(d) | rotAbout 298, rotAbout_eq_crot 302, rotAff 311, rotAbout_injective 319, rotAbout_iterate 465 | matches; `Matrix.toLin'` acts on column vectors, as stated |
| ll:lem:erase | invariant_erase_centre 325 | any real θ; matches |
| ll:lem:minperiod | minimalPeriod_rotAbout 336 | `0<m`, `y ≠ c`; matches |
| ll:thm:core-rot | hullVerts_eq_orbitFS_rotAbout 364 | `c ∉ S`; matches |
| ll:def:peel, ll:lem:peel-basic, ll:lem:antitone | peel 374, peel_succ 378, peel_subset 381, peel_antitone 460 | matches |
| ll:lem:inv-peel | invariant_peel 386 | `0<m`, `c ∉ S`; matches |
| ll:thm:layers | layers_are_orbits 402 | ∃ x ∈ peel S n with (a)∧(b)∧(c); matches |
| ll:lem:exists-layer | exists_layer 419 | no further hypotheses; matches |
| ll:thm:card-peel | card_peel 1037 | `m*(t-1) < |S|`, truncated subtraction; matches |
| ll:thm:reduction | convexNGon_of_layers 1066 | premise H as an explicit hypothesis, bound variable renamed c' (stated); size condition on `S.erase c`; matches |
| ll:def:66-70 | Sixfold66 1102, Sevenfold70 1107 | real numerals 6, 7 in the angle; matches |
| ll:thm:sixfold, ll:thm:sevenfold | 1113, 1136 | Sixfold66 / Sevenfold70 as hypotheses, no `c ∉ S`, `61 ≤ |S|` / `65 ≤ |S|`; matches |

The theorems that take unproved propositions are stated as conditional (statement heads, Remark ll:rem:hyp, map
notes). This satisfies contract rule 7.

## 2. Proof checks (step by step)

- **(C1)-(C7).** The minimal-period facts (P1) and (P2) are correct for Mathlib's definition (least n ≥ 1, else 0).
  (C3) cites Rockafellar, Theorem 2.3 (conv S = the set of all convex combinations), which is correct. (C4) is
  equivalent to Mathlib's `extremePoints`: the condition on x_1 alone implies the one on x_2 by symmetry. (C5)'s
  inclusion conv(f(A)) ⊆ f(conv A) is proved directly (sympy: affine maps preserve combinations with Σλ = 1).
- **Lemma ll:lem:orbit.** In (e), 0 ≤ i < j ≤ p-1 gives 1 ≤ p-j+i ≤ p-1 (checked exhaustively for p ≤ 40), and
  f^{p-j}∘f^i = f^{p-j+i} is used correctly. The case p = 0 is handled. In (f), j < p, so p-j is a true subtraction;
  (d) supplies the invariance of the finite orbit set that (a) needs. Correct.
- **Lemma ll:lem:hv.**
  - (a) Correct.
  - (b) The splitting x = λ_j s_j + (1-λ_j) y_j and the fact that the coefficients of y_j sum to 1 were checked with
    sympy. 0 < λ_j < 1 holds for r ≥ 2, and (C4) is applied with all its hypotheses.
  - (c) The strong induction on |S| is well founded. The case split hv(S) = S versus not is exhaustive. In the exchange
    step, (1-λμ)z = Σ(α_a+λβ_a)a and the coefficient sum ((1-λ)+λ(1-μ))/(1-λμ) = 1 were checked with sympy. The case
    λμ = 1 forces λ = μ = 1 because λ, μ ∈ [0,1]. If A = ∅ then λμ = 1 automatically, so the λμ < 1 branch is
    nonvacuous only for A ≠ ∅. No circularity: (c) does not use (d).
  - (d) follows from (c). Correct.
- **Lemma ll:lem:map-hv.** The steps f(S) = S (injective map on a finite set, by cardinality),
  S∖{f(x)} ⊆ f(S∖{x}), conv(f(A)) ⊆ f(conv A), and injectivity on all of R² (u need not lie in S) are all correct.
- **Theorem ll:thm:core.**
  - Steps 1-3 use Lemma ll:lem:orbit(c) with the finite invariant set H and x ∈ H.
  - In Step 4, Lemma ll:lem:orbit(f) needs f^m x = x and f^m y = y. Both hold because H ⊆ S (Step 2).
  - Both orbits lie in H, by Step 1 and y ∈ H. Each has m elements by (ii) and Lemma ll:lem:orbit(e), applied to x and
    y in S.
  - Disjointness gives |H| ≥ 2m ≥ K. A K-subset of H is in convex position by Lemma ll:lem:hv(a) and
    Lemma fd:lem:mono(a), and it lies in S. This contradicts (iii).
  - Complete and correct, with no general position used.
- **Lemma ll:lem:inv-sdiff.** f^{m-1}(f(y)) = f^m(y) holds for m ≥ 1. Correct.
- **Lemma ll:lem:complex.** The identities in (d), (f) and (g) were checked with sympy. (e) is an induction using (c)
  and (d). In (f), C is a field and w ≠ 1. Correct.
- **Lemma ll:lem:rot.**
  - (a) Re and Im of γ + e^{iθ}(u-γ) match the coordinates of ρ_{c,θ}(p) (sympy).
  - (b) ρ(p) = A(p-c) + c and ρ(v+p) = Av + ρ(p) (sympy).
  - (d) (e^{iα})^j = e^{ijα} (sympy, exponential form, j ≤ 8; also numerically). The composition law
    ρ_{a1}∘ρ_{a2} = ρ_{a1+a2} was checked too.
- **Lemma ll:lem:minperiod.**
  - ω^m = 1. For 0 < k < m, 0 < 2πk/m < 2π gives cos < 1, hence ω^k ≠ 1 (sympy check for m ≤ 12).
  - (P2) gives 1 ≤ q ≤ m. The case q < m leads to y = c via (f) and the injectivity of toC.
  - Correct, and m > 0 is used where needed.
- **Theorem ll:thm:core-rot, Lemmas ll:lem:erase and ll:lem:inv-peel, Theorem ll:thm:layers.** Every hypothesis of
  each cited result is verified at its point of use: c ∉ peel(S,n) ⊆ S, the per-point period m, invariance, and
  K-freeness via Lemma fd:lem:mono(c). Correct.
- **Lemma ll:lem:exists-layer.**
  - The claim's induction is correct. In the nonempty case the IH gives the first alternative.
  - At n = |S|+1, nonemptiness gives |peel| ≥ 1, so the claimed inequality is impossible.
  - The least index exists by well-ordering of ℕ, and k ≠ 0. Correct.
- **Theorem ll:thm:card-peel.** The induction on n with the statement "n ≤ t → P(n)" is correct. In the step,
  n+1 ≤ t gives n ≤ t∸1, so mn ≤ m(t∸1) < |S|, hence the peel is nonempty. Then |hv| = m and the subtraction is legal
  because hv ⊆ peel. The arithmetic was checked.
- **Corollary ll:cor:decomp (written step).**
  - The case t = 0 is handled. For t ≥ 1, m(t∸1) = mt-m < mt (checked).
  - (b) is a downward induction with disjointness justified. (c) follows from antitonicity (i+1 ≤ j) and
    Theorem ll:thm:layers(c), which applies because peel(S,i) ≠ ∅.
  - Correct. It is properly marked as not a Lean declaration.
- **Theorem ll:thm:reduction.**
  - S' = S∖{c} is invariant, centre-free and K-free.
  - Theorem ll:thm:card-peel at n = t gives |T| = mt, using peel(S',t) ⊆ S'.
  - T is invariant: Lemma ll:lem:inv-peel applied to S', then ρ^{m-1}(ρy) = ρ^m y = y.
  - T is in general position and c ∉ T, so H applies with c' = c, and monotonicity finishes. Correct.
- **Theorems ll:thm:sixfold and ll:thm:sevenfold.**
  - p ≠ c exists.
  - The written centre-exclusion argument is checked by sympy: 3·(2π/6) = π, ρ_{c,π}(p) = 2c-p, and
    orient(p,c,2c-p) = 0 equals the displayed expression. The points are pairwise distinct.
  - The arithmetic holds: 6·(11∸1) = 60 < 61 and 7·(10∸1) = 63 < 64 ≤ |S|-1.
  - The premise H is instantiated correctly (6·11 = 66, 7·10 = 70, 8 ≤ 12, 8 ≤ 14).
  - The cited Lemma lg:lem:centre (statement read in `sections/lg.tex`) has exactly the hypotheses supplied (0 < 6,
    6 even, invariance, general position, p ∈ S, p ≠ c). Correct.
- **Remark ll:rem:numerals.** The casts match the Lean proofs: `exact_mod_cast` at 1126, 1128, 1130, 1141 and 1143,
  and `simpa` at 1130 and 1143.

Sympy scripts: `reviews/checks/ll_r1rigor_checks.py` (prints `ALL OK`; every residual is 0) and
`reviews/checks/ll_r1rigor_demoivre.py`. In a first version, de Moivre in trigonometric form for j = 5 and 6 did not
simplify to 0 in sympy. That is a simplification limit, not an error: the exponential form gives residual 0, and
numerical residuals are below 4e-15.

## 3. Evidence and contract mechanics

- **Hashes and identity.** Line count 1148 and SHA-256 `afb8542dceb0...` confirmed. The SHA-256
  `2425500eefd1...` of `ErdosSzekeres/Definitions.lean` confirmed. The first 1148 lines of
  `LAYERLEAN/logs/axioms_recheck_20261106/LayerLemmaAxioms.lean` are byte-identical to `LayerLemma.lean` (confirmed
  with `cmp`).
- **Axiom logs.** `axioms.log` has 28 lines and `out.txt` has 19 lines, all with the 3 standard axioms, exit 0.
  `LEANEXT/review/axioms.log` has 59 lines whose names exactly match the 59 non-`@[simp]` `theorem` declarations of
  the file. `iterate_mem` uses `[propext, Quot.sound]`.
- **Source scan.** grep finds no `sorry`, `admit`, `axiom` or `native_decide`. The only `decide` is at line 1125.
- **Remark ll:rem:hyp.** C6UPPER, C7UPPER and ENCBLEAN were checked: `C6UPPER/README.md` (64 cake_lpr verdicts, cube
  cover), `C7UPPER/README.md` (two encoders, each cake_lpr VERIFIED UNSAT), and
  `ENCBLEAN/geo/ES8Geo/Main.lean` (`sixfold66_of_cubes64`, `sixfold66_of_unsat`). The claims are accurate, apart from
  the omission noted in M4.
- **Labels and references.** All labels start with `ll:`. All 15 export labels of the contract are defined on the
  named statements. The only references are to fd export labels, lg export labels (`lg:lem:centre`,
  `lg:thm:nesting`) and own labels.
- **Preamble.** No `\newcommand`, `\usepackage` or `\begin{document}`.
- **Paths and names.** No machine paths and no tool names in the `.tex` or `.map.tsv`.
- **Map.** 31 rows for 31 statement environments, 5 fields each, with correct names and lines.
- **Compile check.** `STAGE/build/ll_r1rigor_wrapper.tex` compiles twice with exit 0. The only undefined references
  are to `fd:` and `lg:` labels, as expected. There are 35 overfull hboxes (see M1).

## 4. Findings (all minor)

**M1 (minor, layout): Lean references run off the page in several statement heads.**
- *Where.* The heads of Lemma ll:lem:orbit (ll.tex 104-109), Lemma ll:lem:complex (323-335), Lemma ll:lem:rot
  (383-386), Lemma ll:lem:inv-peel (493) and Theorem ll:thm:layers (507-508), among others.
- *What.* The heads overflow the right margin. In the PDF, Lean names and line numbers are cut off at the paper edge.
  For example `rotAbout_iterate ... LayerLemma.lean:46` is truncated, `invariant_peel` shows `...:38`, and
  `layers_are_orbits` shows `LAYERLEAN/LayerLemma.lea` with no line number.
- *Evidence.* `ll_r1rigor_wrapper.log` records 35 overfull hboxes, the largest being:
  - 149.3pt at lines 110-111;
  - 144.1pt at lines 336-337;
  - 123.1pt at lines 387-388;
  - 97.8pt at lines 509-512.

  I confirmed this visually on rendered pages 2, 5, 6 and 7. The other sections compiled so far have at most 32pt
  (`fd`) or none (`ar`, `lg`).
- *Fix.* Add `\sloppy` after the `\label` of each statement, as `fd.tex` does. Alternatively, move the long lists of
  `\leanref` items out of the bracketed head into the first line of the statement.

**M2 (minor, accuracy of a description of the Lean proofs).**
- *What.* The Coverage paragraph (ll.tex 733-734) and the map note for `ll:lem:hv` say that Lean's proofs of (b)-(d)
  "use Krein-Milman". Lean's proof of (b), `extreme_mem_hullVerts` (LayerLemma.lean 130-137), does not. It uses
  `extremePoints_convexHull_subset` and `Convex.mem_extremePoints_iff_convex_diff`. Only (d) (`IsCompact.extremePoints_nonempty`, line 142)
  and (c) (`closure_convexHull_extremePoints`, line 149) use the Krein-Milman file. The text inside the proof
  (185-188) is accurate.
- *A second imprecision.* At line 186 the criterion is quoted as "x is an extreme point of a convex set C iff C∖{x} is
  convex". Mathlib's statement is "iff x ∈ C and C∖{x} is convex".
- *Fix.* Write "(c) and (d) use Krein-Milman", and add "x ∈ C and" to the criterion.

**M3 (minor, convention versus the Lean definition).**
- *What.* (C2), line 59, introduces "f^{i+1} = f∘f^i (Lean `f^[i]`)". Lean's `Nat.iterate` is defined by the other
  recursion, f^[i+1] = f^[i]∘f. The section's version is the lemma `Function.iterate_succ'`, which the Lean proofs
  invoke at lines 56, 73 and 271.
- *Effect.* The two recursions define the same maps (an easy induction), so nothing changes mathematically.
- *Fix.* Add one clause saying that Lean's defining recursion is the other one and gives the same maps.

**M4 (minor, completeness of the provenance in Remark ll:rem:hyp, lines 699-706).**
- *What the remark says.* The supply of `Sixfold66` and `Sevenfold70` is "cake_lpr verdicts (certificate) + the
  written soundness proof in `WRITEUP/note/k8_soundness.tex` (written proof, not refereed) + further written steps in
  C6UPPER".
- *What it omits.* That note lists its own open trust items, gaps (G1)-(G4) (k8_soundness.tex lines 960-1025):
  - (G1) the correspondence between the Python code and the clauses rests on reading the code;
  - (G2) the passage from DIMACS to Sixfold66/Sevenfold70 is a written proof (Corollary k8s:cor:geom; formalized,
    up to trust items (E1)-(E6), only for encoder B at m = 6);
  - (G3) encoder A's angular part rests on binary64 arithmetic;
  - (G4) several written proofs have had no internal review.

  The remark also omits that encoder A of C7UPPER uses the symmetry-breaking unit H(1) (encoder B does not).
- *Effect.* This is not an overclaim about the section's own results, which are clearly conditional. But it is less
  complete than the inventory's first risk item ("gaps G1-G4").
- *Fix.* Add "modulo the gaps (G1)-(G4) recorded in that note".

**M5 (minor, an unverified repository-wide claim).**
- *What.* Line 607-608 says the premise (H) "is an explicit hypothesis ...; no Lean theorem proves it for any m,t".
  This is not checked here. It is also slightly too strong:
  - for K = 0, (H) is trivially true;
  - Remark ll:rem:hyp itself mentions the ENCBLEAN Lean derivation of `Sixfold66`, which is (H) for
    (m,K,t) = (6,8,11), from the cube-unsatisfiability hypothesis (`sixfold66_of_cubes64`).
- *Fix.* "no Lean theorem in this file proves it; no Lean theorem proves it unconditionally for the instances used
  below".

**M6 (minor, informal summary).** The introduction (lines 8-10) says the hull vertices "form a single f-orbit". This is
false for S = ∅, since hv(∅) = ∅ is not an orbit. The theorem statement ("for every x ∈ hv(S)") and Remark
ll:rem:core(2) are correct. Fix: add "if S is nonempty".

**M7 (minor, evidence wording).**
- *What.* Lines 33-37 call `LEANEXT/review/axioms.log` a review "of the same file, SHA-256 afb8542d...". The file that
  produced it (`AxiomsCheck.lean`, named in `LEANEXT/review/REPORT.md` line 62) is not archived. The identification
  therefore rests on REPORT.md lines 3-4 and 16.
- *Contrast.* The input file of the 6 November re-check is archived, and I re-verified it with `cmp`.
- *Fix.* "(according to `LEANEXT/review/REPORT.md`)".

**M8 (minor, wording).** Lines 40-41 say "every statement below whose head names a Lean declaration is Lean-checked in
this sense". That sentence also covers the ten definitions and the def `rotAff`, which have no axiom lines. For a
definition, "Lean-checked" can only mean "elaborated by the same check". Fix: restrict the sentence to theorems and
lemmas, or say what it means for definitions.

No other gaps were found. In particular:
- no case split is missing;
- every induction is well founded;
- every use of an earlier result meets its hypotheses exactly;
- the cited standard facts (Rockafellar 2.3, Euler's formula, cos t < 1 on (0, 2π)) are stated correctly;
- nothing is delegated to Lean.

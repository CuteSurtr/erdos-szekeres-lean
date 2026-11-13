# Section `ll`, polish round 1: independent referee report

Reviewed files: `sections/ll.tex` (792 lines, SHA-256 `a3e317cc04fb9d67...`) and `sections/ll.map.tsv` (31 rows,
SHA-256 `205d8bb165461723...`). Lean source: `LAYERLEAN/LayerLemma.lean`, all of lines 1-470 and 1020-1148 read, plus
`centre_not_mem_of_even` (582-616). Its SHA-256 `afb8542dceb0c170...` and its 1148 lines were recomputed. It is the
file of commit `393619a57` (`git show`, read-only). Paths below are relative to the staging directory (`sections/`,
`build/`), to RES (`LAYERLEAN/...`) or to the repository root (`ErdosSzekeres/...`).

I formed my view before reading `reviews/ll-r1-*.md`, `ll-polish-r1-fix.md`, `ll-p1-diff.md` and
`ll-writer-concerns.md`.

**Verdict: PASS.** No blocker and no major finding. One minor finding remains (m1 below). The polish diff audit had
already reported it, and it has not been fixed.

## 1. Statement fidelity (each statement against its Lean declaration)

I checked every statement environment against the Lean signature: hypotheses (implicit and explicit), conclusion,
quantifier order, `Finset` vs `Set`, maps-into vs equality, truncated subtraction and casts. All 31 are faithful.

| label | Lean | checked points |
|---|---|---|
| ll:def:orbit | orbitFS (48) | image of `range p` under `i ↦ f^[i] x`; empty for p = 0 |
| ll:lem:orbit (a)-(f) | 52, 59, 62, 68, 80, 91 | (a) and (c) need no positivity, and (c) holds for every p; (b) needs `0<p`; (d) needs `0<p` and `f^[p] x = x`; (e) needs only `minimalPeriod f x = p`; (f) needs `0<p` and both points fixed by `f^[p]`, and concludes `y ∈ orbitFS f p x` |
| ll:def:inv, ll:def:hv | 105, 111 | maps into; `S.filter (x ∉ conv(↑S \ {x}))` |
| ll:lem:hv-basic, ll:lem:hv | 114, 118, 121, 130, 146, 139 | (b) concerns extreme points of `convexHull ℝ ↑S`; (c) is an inclusion of coerced sets; (d) assumes `S.Nonempty` |
| ll:lem:map-hv | 162 | `f : Point →ᵃ[ℝ] Point`, `Injective ⇑f` on all of R², maps into |
| ll:thm:core | 189 | `0<m`, `K ≤ 2m`, maps into, `minimalPeriod f y = m` on S, `¬HasConvexNGon K S`, `∀ x ∈ hv S`; no general position |
| ll:lem:inv-sdiff | 217 | `0<m`, `f^[m] y = y` on S |
| ll:def:complex, ll:lem:complex | 231-287 | side conditions `w ≠ 1` (f) and `w ≠ 0` (g); all 13 names |
| ll:def:rot, ll:lem:rot | 298, 302, 311, 319, 465 | the formula agrees symbol for symbol; `rotAff` is `toLin'` of the column-vector matrix with `map_vadd'`; the iterate carries the `(j:ℝ)` cast |
| ll:lem:erase, ll:lem:minperiod | 325, 336 | any real θ; `0<m` and `y ≠ c` |
| ll:thm:core-rot | 364 | `0<m`, `K≤2m`, `c ∉ S`, invariance, K-free |
| ll:def:peel, ll:lem:peel-basic, ll:lem:antitone, ll:lem:inv-peel | 374, 378, 381, 460, 386 | `n ≤ n'` gives `peel n' ⊆ peel n`; `0<m` and `c ∉ S` |
| ll:thm:layers | 402 | `∃ x ∈ peel S n` with (a), (b), (c); (c) is the weak inclusion in the closed hull |
| ll:lem:exists-layer | 419 | no hypotheses beyond `y ∈ S` |
| ll:thm:card-peel | 1037 | `m*(t-1) < S.card` (truncated), `∀ n ≤ t` |
| ll:thm:reduction | 1066 | H is quantified over `T` and a fresh centre before `S, c`; the size condition is on `S.erase c`, and `c ∈ S` is allowed |
| ll:def:66-70 | 1102, 1107 | real numerals 6 and 7; hypotheses in the order GP, `c ∉ T`, invariance, card |
| ll:thm:sixfold, ll:thm:sevenfold | 1113, 1136 | `61 ≤ |S|` and `65 ≤ |S|`; no `c ∉ S` hypothesis; conditional on the Props, as the statement and title say |

A script compared each `\leanref` pair of the tex with the map (55 pairs, identical) and with the Lean source (the
cited line holds the named declaration; all exact). The section's scope (lines 1-469 and 1034-1148) contains 55
declarations: 44 theorems and 11 definitions. All 55 are covered.

## 2. Proof checks (each step redone)

- **(C2)-(C5).** (P1) and (P2) match Mathlib's `minimalPeriod` (`Dynamics/PeriodicPts/Defs.lean:247`, `Nat.find` on
  `periodicPts`, else 0). `Nat.iterate` has the recursion `f^[k+1] = f^[k] ∘ f`. `Function.iterate_succ'` and
  `Function.iterate_add` exist at the pin. (C4) is literally Mathlib's `Set.extremePoints` at f897ebcf, which asks
  only `x₁ = x`. The inclusion conv(f A) ⊆ f(conv A) in (C5) is correct.
- **ll:lem:orbit.** (e): for 0 ≤ i < j ≤ p-1, the iterate f^{p-j+i}(x) = x with 1 ≤ p-j+i ≤ p-1 contradicts
  minimality. (f): f^{p-j}(f^j y) = y, and (d) together with (a) gives the conclusion. Both correct.
- **ll:lem:hv.**
  - (b): the averaging step for r ≥ 2 has 0 < λ_j < 1 and y_j ∈ C.
  - (c): I redid the exchange argument. The cases λμ < 1 and λμ = 1 are both covered. When A = ∅, λ = μ = 1, so z = y,
    a contradiction. The induction covers S = ∅ and hv(S) = S.
  - (c) does not use (d), so there is no circularity.
- **ll:lem:map-hv.** f(S) = S follows by cardinality. Injectivity is used on all of R², at the preimage u, which need not
  lie in S.
- **ll:thm:core.** Step 4: disjointness comes from (f), the sizes from (e) with period exactly m on H ⊆ S, and the
  inequality 2m ≥ K lets one pick T ⊆ H. No hidden hypothesis.
- **ll:lem:inv-sdiff, ll:lem:erase, ll:lem:minperiod, ll:thm:core-rot, ll:lem:inv-peel, ll:thm:layers,
  ll:lem:exists-layer, ll:thm:card-peel.** Correct. For card-peel: the induction hypothesis is used at n ≤ t; the step
  has n ≤ t∸1, so peel(S,n) ≠ ∅ and |peel(S,n)| ≥ m holds before the subtraction. Edge case t = 0: S ≠ ∅ and only
  n = 0 occurs.
- **ll:cor:decomp (written step).** t = 0 forces S = ∅. For t ≥ 1, m(t∸1) < mt. Downward induction gives the disjoint
  union, and (c) follows from antitonicity and layers(c).
- **ll:thm:reduction.** T = S′ ∖ peel(S′,t) has mt points. It is invariant because peel(S′,t) is invariant and
  ρ^{m-1}(ρ y) = y. It is in general position and centre-free. Edge case t = 0: H forces K = 0, which is consistent.
- **ll:thm:sixfold, ll:thm:sevenfold.** For sixfold, Step 1, the included half-turn argument (ρ³ = ρ_{c,π}, q = 2c−p,
  the three points pairwise distinct, orient = 0) and Step 3 are correct. For sevenfold, |S∖{c}| ≥ 64 > 63.

**Sympy** (`build/ll_p1referee_sympy.py` and `build/ll_p1referee_sympy2.py`; every check holds):
- Rotations: the complex form of `rotAbout` (Lemma ll:lem:rot(a)); ρ(v+p) = A_θ v + ρ(p); ρ(c) = c; and iterates
  (ρ_{c,α})^j = ρ_{c,jα} for j ≤ 6, via the exponential form.
- Half-turn: 3·(2π/6) = π; ρ_{c,π}(p) = 2c − p; orient(p, c, 2c−p) = 0, including the displayed intermediate expression.
- Coefficient sum in the exchange argument of Lemma ll:lem:hv(c): ((1−λ) + λ(1−μ))/(1−λμ) = 1.
- Complex-coordinate lemmas: the identities of Lemma ll:lem:complex (d), (f) and (g).
- Primitive roots: cos(2πk/m) < 1 for 0 < k < m ≤ 12.
- Numerals: 6·(11−1) = 60 < 61, 7·(10−1) = 63 < 64, 6·11 = 66, 7·10 = 70, 8 ≤ 12 and 8 ≤ 14.

## 3. Records and cross-references (each claim of the text checked)

**Lean-evidence paragraph.**
- `LAYERLEAN/logs/axioms.log` has 28 lines and `axioms_recheck_20261106/out.txt` has 19. Every line reports exactly
  [propext, Classical.choice, Quot.sound], and the recheck exited 0.
- The first 1148 lines of `LayerLemmaAxioms.lean` match `LayerLemma.lean` byte for byte (`diff`).
- The theorem names in `LEANEXT/review/axioms.log` (59) equal the non-`@[simp]` theorems of the file (66 − 7; sorted
  diff empty). `iterate_mem` reports [propext, Quot.sound].
- `REPORT.md` names `afb8542d…`. It lists `AxiomsCheck.lean`, which is not in the record, so the text's caveat is
  correct.
- The source contains no `sorry`, `admit`, `axiom`, `native_decide`, `implemented_by` or `extern`. The only `decide` is
  at line 1125 (`Even 6`).
- The library target is `defaultTargets = ["ErdosSzekeres"]`, so the file is outside the default build.
- `git log` shows that `axioms.log` was regenerated in the commit that produced the final file.

**Remark ll:rem:hyp.**
- Theorems concluding `Sixfold66`: a grep of every `.lean` file finds only `sixfold66_of_no_model`, `sixfold66_of_unsat`
  and `sixfold66_of_cubes64` (`ENCBLEAN/geo/ES8Geo/Main.lean:78, 87, 91`), and each takes a hypothesis. No theorem
  concludes `Sevenfold70`.
- The namespace body of `ENCBLEAN/geo/ES8Geo/Capstone2.lean` begins with a verbatim copy of `LayerLemma.lean`'s
  namespace body (`diff`).
- `ENCBLEAN/geo/ErdosSzekeres/{Definitions,Basic,Orientation,OrientationGeometry,Suk/*}.lean` are byte-identical to the
  library files. `EncB.CubesUnsat64` (`ENCBLEAN/EncB/Cover.lean:110`) is as described.
- In Lean, `parseDimacs_cube64_get` ties the printed texts to `cubeCnf`. What stays outside Lean is (E1)-(E3), exactly as
  the text says.
- (G1)-(G4) and (E1)-(E6) match `WRITEUP/note/k8_soundness.tex:960-1023`. The note covers the reflection unit and the
  cube cover (`k8s:lem:refl`, `k8s:lem:cube`). The C7UPPER claims match `C7UPPER/README.md` §2-3.

**Foreign references.**
- `lg:lem:centre` (`sections/lg.tex:485`) assumes 0<m, m even, invariance, general position, p ∈ S and p ≠ c, and
  concludes c ∉ S. That is exactly what Step 2 of ll:thm:sixfold supplies.
- `lg:thm:nesting` is the strict nesting theorem.
- `fd:def:point`, `fd:def:gp`, `fd:def:cp`, `fd:def:ngon`, `fd:def:inv`, `fd:def:rot`, `fd:lem:cp-hull`, `fd:lem:mono`
  (a)-(c), `fd:lem:collinear`(a) and `fd:lem:affine-cp`(a) each say what ll uses them for.
- The mathlib names cited in the text exist at the pin: `iterate_succ'`, `iterate_add`, `isPrimitiveRoot_exp`,
  `IsCompact.extremePoints_nonempty` ("Krein-Milman lemma") and `closure_convexHull_extremePoints` ("Krein-Milman
  theorem").

**Mechanics.**
- The compile check (`build/ll_p1referee_wrapper.tex`, contract content; `nice -n 15 pdflatex` twice) exits 0 on both
  passes, with 0 overfull boxes. The only undefined references are the 10 `fd:` labels and the 2 `lg:` labels.
- I inspected pages 2 and 4 of the PDF; no head is clipped.
- The file has 31 statement environments, all labelled, for 31 map rows of 5 fields each, and 21 proofs for 21
  lemmas, theorems and corollaries.
- All 15 export labels are defined on the right statements. There is no `\newcommand`, `\usepackage` or `\sloppy`,
  and no machine path or tool name.
- "proved" occurs only as "not proved". "Verified" and "certified" do not occur. No hypothesis is presented as proved.

## 4. Findings

**m1 (minor; open since the polish diff audit `ll-p1-diff.md` m1, not fixed): `sections/ll.tex:719-723` (Remark
ll:rem:hyp, second paragraph).**
- *What the text says.* C6UPPER "gives the unsatisfiability of SAT encodings of octagon-free configurations of eleven
  nested regular hexagons in general position, by cake\_lpr verdicts on cube formulas". The next clause adds, for
  C7UPPER only, "(one of them with an added symmetry-breaking unit clause)".
- *Why it is imprecise.* At (6,8,11), encoder A's certificate is for F_A plus the unit Y(1,2), through 32 cubes. Only
  encoder B's base formula is certified on its own, through 64 cubes.
  - `WRITEUP/note/k8_soundness.tex:702-704`: "At (6,8,11) the certificate for B is also for F_B alone, through 64
    cubes, and the one for A is for F_A plus Y(1,2), through 32 cubes".
  - `C6UPPER/README.md:23`: "Encoder A, the cross-check, still uses the unit Y(1,2)".
- *Effect.* The qualification is stated for m = 7 but not for m = 6, so a reader may infer that no C6UPPER certificate
  uses symmetry breaking. Nothing false is said about the section's own results, which are conditional, and the next
  sentence says that the note covers the symmetry breaking.
- *Fix.* After "whose cover is checked there", insert "(for encoder B the formula itself, by 64 cubes; for encoder A the
  formula with an added symmetry-breaking unit clause, by 32 cubes)".

## 5. Checked and not findings

- **`build.log` has no hash or timestamp.** Its last git change is the first LAYERLEAN commit. Its content
  ("exit code 0, 0 messages") is generic, so git would not record an identical rewrite.
  - Separately, the 6 November recheck ran `lake env lean` on a byte-identical copy of the final file and exited 0, with
    no output besides the 19 axiom lines.
  - So the text's claim that the file builds without messages is supported for the final file.
- **Recheck date.** `out.txt` timestamps read 2026-11-05 (UTC). The text's "6 November 2026" agrees with
  `axioms_recheck_20261106/README.txt` (04:59 KST).
- **Wording on how the Lean proofs go.**
  - Lemma ll:lem:orbit(e) proves inline the injectivity that Lean takes from `iterate_injOn_Iio_minimalPeriod`.
  - Lemma ll:lem:minperiod gets ω^k ≠ 1 from cos < 1, where Lean uses `IsPrimitiveRoot`. The text names the Lean
    lemma.
  - Both proofs keep the Lean structure, so "We follow the Lean proof(s)" is acceptable.
- **The map note "(b)-(d) proved by elementary arguments"** describes the written proofs and claims no stronger label.

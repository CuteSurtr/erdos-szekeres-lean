# Review of section `ll`, round 1, lens: adversarial

Section: `sections/ll.tex` (760 lines), map `sections/ll.map.tsv` (31 rows).
Sources compared: `LAYERLEAN/LayerLemma.lean` lines 1-470 and 1034-1148 (SHA-256 afb8542d..., re-hashed: matches),
`ErdosSzekeres/Definitions.lean` (SHA-256 2425500e..., re-hashed: matches), `ErdosSzekeres/Basic.lean`,
`LAYERLEAN/logs/{build.log, axioms.log, axioms_recheck_20261106/out.txt, README.txt}`, `LEANEXT/review/{axioms.log,
REPORT.md}`, `C6UPPER/README.md`, `C7UPPER/README.md`, `WRITEUP/note/k8_soundness.tex` (head, Lemma k8s:lem:layer,
"Gaps that remain"), `ENCBLEAN/geo/ES8Geo/{Main.lean, Audit.lean, Capstone2.lean}`, `ENCBLEAN/EncB/Cover.lean`,
`SYM5/README.md` lines 60-80, and the `fd`/`lg` statements this section cites.

**Verdict: PASS** (no blocker, no major finding). Eight minor findings, listed at the end.

## 1. Mechanical checks

- Compile: `build/ll_r1adv_wrapper.tex` (contract wrapper, private file name), `nice -n 15 pdflatex` twice: both exit 0.
  The only undefined references are `fd:*` (10 labels) and `lg:lem:centre`, `lg:thm:nesting`, all allowed. No
  errors, no "Missing $". Many overfull boxes (see finding m1).
- Labels: all 15 export labels required by the contract are defined, each on the named statement
  (`ll:def:hv`, `ll:def:peel`, `ll:lem:hv` with all four declarations, `ll:lem:minperiod`, `ll:thm:core`,
  `ll:thm:core-rot`, `ll:lem:inv-peel`, `ll:thm:layers`, `ll:lem:exists-layer`, `ll:lem:antitone`,
  `ll:thm:card-peel`, `ll:thm:reduction`, `ll:def:66-70`, `ll:thm:sixfold`, `ll:thm:sevenfold`). Every `\ref` is to an
  own label, an `fd:` label of the contract list, or an `lg:` export label. No `\newcommand`, no preamble material.
- Map: a script compared every `\leanref` in the 31 statement heads with the TSV rows (names, file:line, kind) and with
  the Lean source (the cited line holds `theorem <name>` / `def <name>`). 0 mismatches; every line number is exact.
- Coverage: every declaration in lines 1-470 and 1034-1148 (21 defs/theorems of the orbit, hull and rotation parts,
  13 complex helpers, peel lemmas, card_peel, convexNGon_of_layers, Sixfold66, Sevenfold70, sixfold_octagon,
  sevenfold_octagon) is covered. 21 lemma/theorem/corollary environments, 21 proofs.
- Paths/tool names: no machine path and no tool name in `ll.tex` or `ll.map.tsv`.
- Lean-evidence paragraph: verified against the logs. `axioms.log` has 28 lines and `out.txt` 19, all
  `[propext, Classical.choice, Quot.sound]`; the head of `LayerLemmaAxioms.lean` is byte-identical to `LayerLemma.lean`
  (cmp); `LEANEXT/review/axioms.log` prints 59 theorems = 66 theorems of the file minus 7 `@[simp]` ones, contains every
  non-simp theorem of this section, and `iterate_mem` is `[propext, Quot.sound]`; the only `decide` is line 1125; no
  `sorry/admit/axiom/native_decide/implemented_by/extern/unsafe/opaque/set_option`; toolchain v4.24.0 and Mathlib
  f897ebcf72cd... match `lean-toolchain` and `lake-manifest.json`; `defaultTargets = ["ErdosSzekeres"]`.
- Symbolic checks (sympy, `build/ll_r1adv_checks/sym.py`): `orient(p,c,2c-p)=0`; `rotAbout c pi p = 2c-p`; the real
  formula of `rotAbout` equals `c+e^{i theta}(z-c)`; `rotAbout(v+p) = A_theta v + rotAbout(p)`; composition of
  rotations adds angles; `((1-l)+l(1-mu))/(1-l mu) = 1` (the exchange step of Lemma ll:lem:hv(c)); `3*(2pi/6)=pi`.
  All hold.

## 2. Fidelity (statement against Lean), declaration by declaration

Checked each written statement against the Lean signature: hypotheses, implicit/explicit arguments, quantifier order,
`Finset` vs `Set`, maps-into vs equality, natural subtraction, casts.

- orbitFS, iterate_mem, mem_orbitFS_self (needs `0<p`), orbitFS_subset (any p), orbitFS_invariant (`0<p`,
  `f^[p] x = x`), card_orbitFS_of_minimalPeriod (`minimalPeriod f x = p`, no positivity), mem_orbitFS_of_not_disjoint
  (`0<p`, both fixed by `f^[p]`): faithful.
- Invariant (maps into), hullVerts, mem_hullVerts, hullVerts_subset, convexPosition_hullVerts, extreme_mem_hullVerts,
  hullVerts_nonempty (`S.Nonempty`), subset_convexHull_hullVerts (coerced sets): faithful (for (b) see minor m7).
- map_mem_hullVerts (affine, injective on all of R^2, maps into): faithful.
- hullVerts_eq_orbitFS: `0<m`, `K<=2m`, maps into, `minimalPeriod f y = m` for all y in S, `not HasConvexNGon K S`,
  `{x} (hx : x in hullVerts S)`; conclusion `hullVerts S = orbitFS f m x`. Faithful, and no general position.
- invariant_sdiff_hullVerts (`0<m`, `f^[m] y = y` on S): faithful.
- toC/ofC/crot and the 13 helper lemmas (side conditions `w != 1`, `w != 0`): faithful.
- rotAbout (formula identical), rotAbout_eq_crot, rotAff (def: map + linear part `toLin'` of the rotation matrix),
  rotAbout_injective, rotAbout_iterate (`j` cast): faithful.
- invariant_erase_centre (any theta): faithful. minimalPeriod_rotAbout (`0<m`, `y != c`): faithful.
- hullVerts_eq_orbitFS_rotAbout (`0<m`, `K<=2m`, `c notin S`, invariance, K-free): faithful.
- peel, peel_succ, peel_subset, peel_antitone, invariant_peel (`0<m`, `c notin S`): faithful.
- layers_are_orbits (exists x in peel S n with (a),(b),(c); (c) is weak containment in the closed hull): faithful.
- exists_layer (no hypotheses): faithful.
- card_peel (`m*(t-1) < |S|` with truncated subtraction, conclusion for all n <= t): faithful.
- convexNGon_of_layers (premise H quantified over T and a fresh centre; size condition on `S.erase c`; c in S allowed):
  faithful, with the renaming c -> c' declared.
- Sixfold66, Sevenfold70 (real numerals 6, 7 in the angle; order of hypotheses GP, c notin T, invariance, card):
  faithful. sixfold_octagon (`61 <= |S|`, no `c notin S` hypothesis) and sevenfold_octagon (`65 <= |S|`): faithful,
  and stated as conditional on the propositions in the statement, the title and Remark ll:rem:hyp.

## 3. Attack log on the main statements (why each survives)

- **Core lemma (ll:thm:core).** Tried: m=1 (f fixes S; K<=2 forces |S|<=1; hv={x}=orb_1); m=2 with a point
  reflection (K=4: two non-collinear antipodal pairs form a parallelogram, so 4-freeness forces collinearity; then
  hv = the two extreme points = one orbit) and with a line reflection (two mirror pairs form an isosceles trapezoid
  unless all four are collinear); K=0 (hypothesis (iii) false, noted in Remark ll:rem:core); K=1,2; S empty (no x);
  non-orthogonal f of finite order (affine invariance makes no difference); collinear S (hv = endpoints). No
  counterexample. Proof checked step by step: Step 1 needs Lemma ll:lem:map-hv, whose proof uses injectivity on all of
  R^2 at the right place (the preimage u need not lie in S) and `conv(f A) subset f(conv A)` from (C5); Step 4 uses
  disjointness via ll:lem:orbit(f) with both points fixed by f^m, sizes via (e) with period exactly m, and
  `2m >= K` to pick T inside H. No hidden general position, distinctness or `c notin S` assumption.
- **Hull lemma (ll:lem:hv).** (a) direct. (b) `(*)` is proved correctly for r>=2 (coefficient strictly between 0 and
  1, renormalised remainder lies in C by convexity). (c) The exchange argument: checked the case A empty (forces
  lambda=mu=1, z=y), the case lambda*mu<1 (coefficients sum to 1, which also forces A nonempty) and lambda*mu=1
  (lambda=mu=1, z=y). The induction covers S empty and hv(S)=S. (d) follows from (c) with conv(empty)=empty. No gap,
  no circularity ((c) does not use (d)).
- **Exact period (ll:lem:minperiod).** m=1 (identity, period 1), m=2 (half-turn); the boundary 0<k<m gives
  0 < 2 pi k/m < 2 pi strictly, so cos < 1. 2 pi/m with m=0 is excluded by `0<m`.
- **Rotation form, peels, layers (ll:thm:core-rot, ll:lem:inv-peel, ll:thm:layers).** All need `c notin S`, which is
  stated; K-freeness of peels via monotonicity; invariance of peels via ll:lem:inv-sdiff with f^m = id on the peel,
  justified by ll:lem:minperiod (points differ from c). OK.
- **Exhaustion (ll:lem:exists-layer).** S empty: vacuous. The counting claim and the least-index argument are correct
  (k=0 excluded because y in S).
- **Sizes (ll:thm:card-peel).** t=0 (needs S nonempty, only n=0), t=1, the step's use of `n <= t-1` and
  `|peel| >= m` before subtracting: correct; no natural-subtraction underflow.
- **Decomposition (ll:cor:decomp, written step).** t=0 handled; t>=1 uses m(t-1) = mt-m < mt; disjointness by
  downward induction; (c) uses antitonicity and layers(c). Correct.
- **Reduction (ll:thm:reduction).** t=0 (then H forces K=0, consistent); c in S (erased); T = S' minus peel(S',t)
  has exactly mt points and is invariant (if rho(y) were in the invariant peel, so would be y = rho^{m-1}(rho y)).
  Correct.
- **Sixfold/sevenfold (ll:thm:sixfold, ll:thm:sevenfold).** Step 1 (61 > 1); the included half-turn argument for the
  centre: q = 2c-p is in S, the three points are pairwise distinct, orient(p,c,2c-p)=0 (sympy), contradiction with
  general position. Numerals: 6(11-1)=60<61, 7(10-1)=63<64<=|S|-1. Cast bridge (real numerals vs natural m) is named in
  Remark ll:rem:numerals. Correct and visibly conditional.

## 4. Findings (all minor)

**m1 (minor, LaTeX layout): several statement heads run off the page, so Lean names and line numbers are cut off in
the PDF.** Evidence: `build/ll_r1adv_wrapper.log` reports overfull boxes of 149pt (head of Lemma ll:lem:orbit, source
lines 104-109), 144pt (Lemma ll:lem:complex, 323-335), 123pt (Lemma ll:lem:rot, 383-386), 98pt (Theorem ll:thm:layers,
507-508), 80pt (Theorem ll:thm:sevenfold, 675-677), 75pt (Lemma ll:lem:hv, 171-174), 73pt (Lemma ll:lem:inv-peel, 493);
the margin is 0.9in = 65pt. In the rendered pages, e.g. the head of Theorem ll:thm:layers ends at
"LAYERLEAN/LayerLemma.lea", that of ll:lem:complex loses "ofC_zero"/"ofC_toC" entries, and that of ll:thm:sevenfold
ends at "sevenfold_octag". The source and the map are correct. Fix: put `\sloppy` after the label (as `fd.tex` does)
or start each `\leanref` of a long head on its own line.

**m2 (minor, typo): sections/ll.tex:91.** "(C7) ... For $m\in\N$ the subtraction $t\mathbin{\dot{-}}1$ is truncated"
should read "For $t\in\N$".

**m3 (minor, inconsistent summary): sections/ll.tex:733-734 and the `ll:lem:hv` row of `ll.map.tsv`.** "the proofs of
(b)-(d) are elementary and differ from the Lean proofs, which use Krein--Milman". The Lean proof of (b)
(`extreme_mem_hullVerts`, `LAYERLEAN/LayerLemma.lean:130-137`) does not use Krein-Milman; it uses
`Convex.mem_extremePoints_iff_convex_diff` and `extremePoints_convexHull_subset`. The proof text at lines 185-188 says
this correctly. Fix: "which use Krein--Milman for (c) and (d)".

**m4 (minor, overgeneralisation): sections/ll.tex:607-608.** "The premise (H) is an explicit hypothesis of the
theorem; no Lean theorem proves it for any $m,t$." Read literally (no theorem has (H) as its statement) it is true, but
read as "(H) is not established in Lean for any parameters" it is false or at least unclear: for K=3 and mt>=3, (H)
follows at once from the main-library theorem `forces_triangle : ForcesConvexNGon 3 3`
(`ErdosSzekeres/Basic.lean:72`), and for (m,K,t)=(6,8,11) the premise is Sixfold66 up to the cast, which
`EncB.Geo.sixfold66_of_cubes64` (`ENCBLEAN/geo/ES8Geo/Main.lean:91`) derives from `EncB.CubesUnsat64`. Fix: "no theorem
of `LAYERLEAN/LayerLemma.lean` proves it; for the instances used below it is supplied as the hypothesis Sixfold66 or
Sevenfold70 (Remark ll:rem:hyp)."

**m5 (minor, incomplete description of the supply chain): sections/ll.tex:699-706 (Remark ll:rem:hyp).** The remark
satisfies the contract (it names C6UPPER/C7UPPER, the rigor label certificate, and the written soundness proof as not
refereed), but two qualifications that the sources state are missing:
(i) `WRITEUP/note/k8_soundness.tex` lists "Gaps that remain" (G1)-(G4): the code-to-clause correspondence is by reading
the Python sources, the DIMACS-to-Sixfold66/Sevenfold70 passage is a written proof, encoder A's angular part rests on
binary64 arithmetic, and several of its proofs have had no internal review;
(ii) the ENCBLEAN theorem takes `EncB.CubesUnsat64`, the unsatisfiability of the 64 cube formulas of the Lean
definition `EncB.encB 6 8 11` (`ENCBLEAN/EncB/Cover.lean:110`), not of the certified files; the link to the files
and to the cake_lpr verdicts is the trust list (E1)-(E6) of `k8_soundness.tex`, gap (G2). Also, its `Sixfold66` is the
one in the verbatim copy `ENCBLEAN/geo/ES8Geo/Capstone2.lean:1110` (text identical to `LayerLemma.lean:1102-1104`,
checked with diff). Fix: add one sentence for each.

**m6 (minor, informal overstatement): sections/ll.tex:8-10.** The introduction says the hull vertices "form a single
$f$-orbit". For S empty, hv(S) is empty, which is not an orbit; the theorem only says hv(S) = orb_m(f,x) for every
x in hv(S). Fix: "if $S\ne\emptyset$, the hull vertices of $S$ form a single $f$-orbit".

**m7 (minor, definition not literally Mathlib's): sections/ll.tex:74-76, (C4).** (C4) is labelled "Mathlib
Set.extremePoints" but asks only for $x_1=x$, whereas Mathlib asks for $x_1=x$ and $x_2=x$ when $x$ lies in the open
segment. The two are equivalent (swap the roles of $x_1,x_2$ and $a,b$), and the proof of Lemma ll:lem:hv(b) only uses
the direction Mathlib => (C4), so the written statement is faithful; but the equivalence is not stated. Fix: add
"(equivalently $x_1=x_2=x$, by symmetry; this is Mathlib's definition via the open segment)".

**m8 (minor, label wording): sections/ll.tex:40-42.** "Every statement below whose head names a Lean declaration is
Lean-checked in this sense" also covers Definition ll:def:66-70, whose head names Sixfold66 and Sevenfold70; a hasty
reader may take this as "Sixfold66 is Lean-checked". The definition itself says "neither is proved in Lean", so there is
no real contradiction. Fix: "Every lemma and theorem below whose head names a Lean declaration ...; definitions are
Lean definitions that type-check".

## 5. Things I could not settle

- `LEANEXT/review/axioms.log` does not itself record the checked file; that it is LayerLemma.lean (afb8542d) rests on
  `LEANEXT/review/REPORT.md` (the check file `AxiomsCheck.lean` is not archived). The section's wording ("review of
  4 November 2026 of the same file") follows the report; the two LAYERLEAN logs, which are verifiable, already cover
  every headline theorem of the section, so nothing depends on this.

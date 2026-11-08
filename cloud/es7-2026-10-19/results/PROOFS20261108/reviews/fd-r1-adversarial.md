# Review of section `fd`, round 1, lens: adversarial

Section: `sections/fd.tex` (1028 lines), map `sections/fd.map.tsv` (32 rows).
Sources compared: `ErdosSzekeres/{Definitions, Orientation, OrientationGeometry, Basic}.lean`,
`ErdosSzekeres/Suk/{FourPoint, SupportingLines, OrientationClique, Reflection}.lean`, `ErdosSzekeres/ConvexCycleCuts.lean`,
`LAYERLEAN/LayerLemma.lean` (lines 1-335, 455-480, 1095-1148), `SYMLEAN/SymmetricReduction.lean` (lines 54-60, 265-275,
395-405), `LEANEXT/orbit/OrbitConsistency.lean` (lines 1-125, 168-186), `MIRRORETV/lean/MirrorMain.lean` (lines 1-20,
2170-2190), `SYMLEAN/mirror/ReductionThreeClasses.lean` (lines 3735-3746), `SYMLEAN/AffineReduction.lean` (lines
1238-1310), the axiom audit `docs/validation/axiom-audit-lower-bound-2026-10-11.txt`, the logs the section cites, the
inventories `LAYERLEAN.json` and `MAIN-LIBRARY-coverage.json`, and the Mathlib definitions of `Collinear`
(`Module.rank k (vectorSpan k s) <= 1`), `ConvexIndependent` (`forall s x, p x in convexHull (p '' s) -> x in s`),
`collinear_iff_of_mem` and `convexIndependent_set_iff_notMem_convexHull_diff`.

**Verdict: PASS** (no blocker, no major finding). Nine minor findings, listed in Section 4. The most important one
(m1) is that three foundation facts are called "written steps without a single Lean counterpart" although Lean
counterparts exist in `SYMLEAN/AffineReduction.lean` and `LEANEXT/orbit/OrbitConsistency.lean`; this contradicts the
scope instruction "each tagged with its Lean name(s) where one exists", but it under-states Lean coverage and has no
effect on correctness. No contract statement of `fd` is false or mismatched with Lean.

## 1. Mechanical checks

- Compile: private wrapper `build/fd_r1_adv/fd_adv_wrapper.tex` (contract wrapper, separate folder), `nice -n 15
  pdflatex` twice: both exit 0. Undefined references only `ll:def:hv`, `ll:def:peel`, `ll:def:66-70`,
  `oc:lem:rot-inv` (all export labels of other sections, allowed). No errors, no "Missing $". Two overfull boxes
  (2.1pt, 5.1pt), see m9.
- Labels: all 20 `fd:` labels of the contract are defined, on the named statements, in the contract order (extra
  helper labels are interleaved; no other section `\ref`s a non-contract `fd:` label, checked by script over all
  section files). Every `\ref` in `fd.tex` is to an own label or an allowed export label.
- Lean references: a script resolved every `\leanref{name}{file:line}` (43) and every `\dirn{file:N}` (11) in
  `fd.tex`; each cited line carries the keyword and the short name of the declaration (or, for the `\dirn` citations,
  the code the text describes). 0 mismatches, every line number exact.
- Hash table: all 14 SHA-256 prefixes re-computed: all match. HEAD is `7e32ee259` on branch `es7-night-2026-11-01`;
  `lean-toolchain` = `leanprover/lean4:v4.24.0`; `lake-manifest.json` mathlib rev
  `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`; `defaultTargets = ["ErdosSzekeres"]`, package `erdos_szekeres`.
- Axioms evidence: audit lines 87, 103, 113, 114, 119, 175, 176 hold the seven named declarations with
  `[propext, Classical.choice, Quot.sound]`. `git diff 7f0868fdb HEAD` (the audit commit) over all 13 cited main-library
  files (including BaseOrder, BaseChart, TriangleOrder, CupsCaps) is empty, so the audit applies to the current files.
  `LEANEXT/review/axioms.log` lines 1, 22, 23, 33 are as stated; `SYMLEAN/logs/runs.tsv` has SymmetricReduction.lean
  `6d5ec90a`, exit 0, 0 output lines; `LEANEXT/orbit/logs/axioms.log` line 1 is `orient_rotAbout_inv` with the three
  standard axioms; `MIRRORETV/lean/MirrorMain.out` contains warnings only; `SYMLEAN/mirror/README.md:49-50` records exit
  0. Text search of the five research files and of the 13 main-library files (including `Suk/CupsCaps.lean`): no `sorry`, `admit`, `axiom`
  declaration or `native_decide` (one false hit: the word "admits" in a comment of `Suk/BaseOrder.lean:17`).
- `rotAbout`: 19 definitions in the research records, normalised bodies all identical (claim at fd.tex:296 holds);
  the three `Invariant` definitions are textually identical.
- Symbolic checks (sympy, `build/fd_r1_adv/check_fd.py`): `orient_swap`, `orient_cycle`, `orient_translate`; the
  bracket expansion `orient = [a,b]+[b,c]+[c,a]`; `orient(g a,g b,g c) = det(A) orient(a,b,c)` for `g x = Ax+v`;
  Lemma rot (c), (e), (f); invariance of `orient` under `rotAbout`; `det F_phi = -1`, `F_phi u = u`,
  `F_phi u^perp = -u^perp`; the certificate `(p1 q0 - p0 q1)(u+v-1)` of `orient_affine_combination`;
  `orient_support_sum`; all twelve support values in the proof of Lemma fd:lem:four-positive. All hold.
- Paths and names: no machine path, no tool name in `fd.tex` or `fd.map.tsv`; no `\newcommand`,
  `\usepackage` or preamble material.

## 2. Fidelity (statement against Lean / Mathlib)

Every statement head that names a Lean declaration was compared with the source, hypothesis by hypothesis:
`Point` (abbrev `Fin 2 -> R`); `orient` (any `CommRing`, same formula); `GeneralPosition` (pairwise distinct
`a b c in s`, `not Collinear R {a,b,c}` as a Set); `ConvexPosition` (`ConvexIndependent R` of the subtype coercion;
the paraphrase "for every T subset S and x in S, x in conv T implies x in T" is exact); `HasConvexNGon` (exact
cardinality, no emptiness); `ForcesConvexNGon` (`N <= card`); the three `Invariant` (maps into); the three `rotAbout`;
`iterate_mem` (hypothesis `forall y in S, f y in S`, arbitrary type; stated so); `rotAbout_eq_crot`, `rotAff`,
`rotAbout_iterate` (`(j : R) * alpha`), `rotAbout_injective`; `orient_swap/cycle/translate`;
`orient_eq_zero_iff_collinear`, `generalPosition_iff_orient_ne_zero`; `convexPosition_iff`; the three `.mono`;
`MirrorOdd.hasConvexNGon_of_le` (renamed variables only); `HasConvexNGon.card_le`, `ConvexPosition.hasConvexNGon`,
`ForcesConvexNGon.mono`, `forcesConvexNGon_iff_exact`; `convexPosition_of_card_three`; `convexPosition_of_subsets_
card_le_four` (`t.card <= 4`), `convexPosition_of_four_subsets` (`4 <= s.card`, `t.card = 4`);
`orient_affine_combination` (`u + v = 1`, no sign condition), `convex_orient_positive/nonnegative`;
`convexPosition_of_strict_supports` (`r != p`); `orient_support_sum` (argument order `a p b r`);
`convexPosition_four_of_positive` (the four hypotheses in Lean's order, Finset `{a,b,c,d}`);
`convexPosition_of_positive_triples` / `_negative_triples` (`LinearOrder`, `p` injective on all of the index type,
`4 <= s.card`, conclusion on `s.image p`); `hasConvexNGon_of_positive_cycle` (`4 <= k`, `p : Fin N -> Point`
injective, `e : Fin k embeds Fin N`, implicit `P`, membership `forall i, p (e i) in P`, all increasing triples).
No missing, extra or changed hypothesis; same conclusions; quantifier order preserved. The Mathlib definitions are
stated faithfully (`Collinear` via `Module.rank` of `vectorSpan`; `ConvexIndependent`; `convexHull` as smallest convex
superset; `AffineIndependent` for a finite set; `AffineMap` of the plane = `x -> Ax + v`).

## 3. Adversarial attacks per statement (all survive)

- fd:def:ngon / fd:rem:ngon: `K = 0` (no set is 0-free: correct, empty T); `K <= K'` monotonicity is the contrapositive
  of mono(d), correct direction.
- fd:def:inv / fd:lem:inv-image: non-injective f is excluded in (a), (b); `S` empty fine; (b) uses (a) correctly;
  (c) for arbitrary types, induction with `f^[i+1] = f o f^[i]` (base case trivial, not written; harmless).
- fd:def:rot / fd:rem:angles / fd:lem:rot: `m = 0` gives `2pi/(0:R) = 0` and `rho_0 = id` (checked); real numerals 6, 7
  are the casts of the naturals (Nat.cast_ofNat); `p = c` gives orientation 0, consistent with (e); (e) uses the open
  interval `0 < theta < pi` (boundaries give `sin = 0`, correctly excluded); composition law verified symbolically.
- fd:lem:orient: over a commutative ring (commutativity is used in (e) for `b = c`; R is commutative); (d) all six
  permutations covered with correct signs; (e) all three coincidences.
- fd:lem:affine-orient: det multiplicativity; rotation det 1; reflection `F_phi` det -1 and its fixed line verified.
- fd:lem:collinear-mem / fd:lem:collinear: degenerate triples (`a = b`, `a = b = c`, `b = c`) handled; the case split
  `u0 = 0` / `u0 != 0` matches the private helper `exists_smul_of_det_zero`; rank vs dimension in R^2 is fine.
- fd:lem:hull: (b) both inclusions; (c) needs `m >= 1` (stated); (d) works for `w = 0`.
- fd:lem:cp-hull, fd:lem:mono, fd:lem:ngon-basic, fd:lem:forces-basic: `n = 0`, `N = 0` fine; no circularity
  (mono(d) only mentions ngon-basic(b) when describing the Lean proof; its own proof uses mono(a)).
- fd:lem:small: empty set and singletons; (c) needs pairwise distinct points (stated), the middle-parameter argument
  gives `lambda in (0,1)` and the identity `tau(x) = lambda tau(y) + (1-lambda) tau(z)` (checked).
- fd:lem:affine-cp: (a) holds for every affine map (true, stated so); injectivity forces `det A != 0` (the explicit
  kernel vectors are correct in all sub-cases, including `A = 0`); (b)-(d) both directions, using injectivity where
  needed (`g(S) \ {g(p)} = g(S \ {p})`, membership reflection, preimage witness in (d)).
- fd:lem:caratheodory: `Y` infinite or empty; minimal T has all weights positive; the reduction step keeps
  nonnegativity and sum 1; `k <= 3` from linear dependence in R^2.
- fd:lem:four-subsets: `|s| < 4` in (a) (hypothesis covers `s` itself); (b) extension to a 4-set exists because
  `|s| - |t| >= 4 - |t|`.
- fd:lem:halfplane, fd:lem:strict-supports, fd:lem:support-sum: `s = {p}` and `s` empty fine; `u = 0` case of (b)
  handled.
- fd:lem:four-positive: coincident letters are handled by the argument "r equals one of the three other letters"
  (no distinctness used); twelve values verified.
- fd:lem:pos-triples / fd:lem:neg-triples: `iota` infinite allowed; `u = {i in s : p i in t}` has `p(u) = t`,
  `|u| = 4` by injectivity; the reversed order is a linear order; the sign flip uses the (1 3) transposition. The
  variant for `|s| <= 3` in fd:rem:pos-triples(iii) is correct and is labelled as a variant.
- fd:lem:pos-cycle: `N < k` is vacuous (no embedding); `T = q(Fin k)` has `k` elements by injectivity of `p o e`.
- fd:lem:separation: `F` empty (both sides true, `l = 0`); nearest point on the compact simplex; the first-order
  inequality and the strict final inequality are correct.

## 4. Findings (all minor)

**m1 (minor; tagging / coverage honesty).** Lean counterparts exist for three foundation facts that the section calls
written steps "without a single Lean counterpart" (fd.tex:1002-1007), and Remark fd:rem:affine-orient-lean
(fd.tex:455-461) says "Lean proves the special cases it needs separately":
- fd:lem:affine-orient = `ErdosSzekeres.SymReduction.orient_affine` (`SYMLEAN/AffineReduction.lean:1241`):
  `(hg : forall p, g p = L *v p + b) (x y z : Point) : orient (g x) (g y) (g z) = L.det * orient x y z`, exactly the
  displayed formula of the lemma.
- fd:lem:affine-cp, forward directions of (b), (c), (d): `convexPosition_image_affine` (`:1263`, injective
  `Point ->a[R] Point`), `generalPosition_image_affine` (`:1278`, `det L != 0`) and `generalPosition_image_affineEquiv`
  (`:1290`), `hasConvexNGon_image_affine` (`:1298`); (a) is Mathlib's `AffineMap.image_convexHull` (named only inside
  the proof). The section's Remark fd:rem:affine-cp-lean is correct as written ("the main library contains ...") but
  the Coverage sentence is not.
- fd:lem:orient(d), real case: `ErdosSzekeres.OrbitConsistency.orient3_perm` (`LEANEXT/orbit/OrbitConsistency.lean:178`),
  `orient3 (t o sigma) = sign(sigma) * orient3 t`.
`SYMLEAN/AffineReduction.lean` (SHA-256 `41cfc0b6...`, current) compiles with exit 0 (`SYMLEAN/logs/runs.tsv`), and
`SYMLEAN/logs/AffineReductionAxioms.out` lists `hasConvexNGon_image_affine` and `generalPosition_image_affineEquiv`
with the standard axioms; section `ar` tags these declarations (ar.tex:345, 393, 413, 440). The scope instruction asks
for each statement to be tagged with its Lean name where one exists. Fix: tag Lemma fd:lem:affine-orient with
`SymReduction.orient_affine` (statement already faithful: `A = L`, `v = b`), name the forward-direction counterparts
of fd:lem:affine-cp (b)-(d) and `AffineMap.image_convexHull` for (a), name `orient3_perm` for fd:lem:orient(d) (as the
real case of the ring statement), and correct the remark and the Coverage sentence. (fd cannot `\ref` the `ar:lem:*`
labels, which are not export labels; naming the declarations and file:line is enough.)

**m2 (minor; evidence understated).** fd.tex:128-133 lists twelve main-library declarations as "not covered by a saved
`#print axioms` output that we identified". At least five are covered by the cited audit itself:
`ErdosSzekeres.esNumber_three` (audit line 732) is proved from `forces_triangle` (`Basic.lean:72-75`), which uses
`forcesConvexNGon_iff_exact` and `convexPosition_of_card_three`; the proof of `forcesConvexNGon_iff_exact` uses
`GeneralPosition.mono` and `HasConvexNGon.mono` (`Basic.lean:45`); `conjecturedBound_le_of_forces` (audit line 725) uses
`ForcesConvexNGon.mono` (`ErdosSzekeres/LowerBound/Construction.lean:118`). The hedge "that we identified" keeps the sentence from
being false, and the fallback evidence (compile + text search) is sound. Fix: cite lines 725 and 732 for these five.

**m3 (minor; path convention).** fd.tex:16-20 says every path not beginning with `ErdosSzekeres/`, `docs/`,
`experiments/` or `scripts/` is relative to `cloud/es7-2026-10-19/results`, but fd.tex:27-29 cites `lean-toolchain`
and `lake-manifest.json`, which exist only at the repository root (not under the results directory). Fix: add
"files at the repository root (`lean-toolchain`, `lake-manifest.json`, `lakefile.toml`)" to the root list.

**m4 (minor; line-number convention).** fd.tex:21-22: "for a declaration it is the line that carries the keyword def,
abbrev or theorem". Later sections cite lines carrying `structure` or `inductive`: `mb` (`ErdosSzekeres/Vendor/ETV/
Config/Defs.lean:20`, `structure Config`), `oc` (`LEANEXT/orbit/OrbitConsistency.lean:145`, `inductive RotComp`), `mm`
(`ErdosSzekeres/Omission/Realization.lean:9`, `structure Configuration`), `cb` (`C3LEAN/C3Cover.lean:45, 146, 245`).
Fix: say "the line that carries the declaration keyword (`def`, `abbrev`, `theorem`, `structure`, `inductive`, ...)".

**m5 (minor; map).** `fd.map.tsv` has no rows for the seven `remark` environments (`fd:rem:norm`, `fd:rem:ngon`,
`fd:rem:angles`, `fd:rem:affine-orient-lean`, `fd:rem:affine-cp-lean`, `fd:rem:pos-triples`, `fd:rem:pos-cycle`);
the contract asks for one row per statement environment, and eight of the other ten maps list their remarks.
`fd:rem:pos-triples` contains a variant statement with a proof. Also the `lean_name` column of two written steps reads
`Mathlib: ...` (`fd:def:conv`, `fd:lem:collinear-mem`) where the contract asks for `-` (the Mathlib names fit the note
column).

**m6 (minor; part labelling).** Lemma fd:lem:rot (fd.tex:309) tags (d) with `rotAbout_injective`, but (d) states
"rho_theta is a bijection of R^2 with inverse rho_{-theta}; in particular it is injective". Lean proves only
injectivity; the bijection and the inverse are a written step (proved correctly from (c)). Item (c) marks its extra
part ("the composition law is a written step here"); (d) should do the same. Similarly "In particular
rho_theta(c) = c" in (b) is not part of `rotAff` (Lean proves it inside `invariant_erase_centre`, `LayerLemma.lean:330`).

**m7 (minor; rigor convention).** The rigor paragraph (fd.tex:31-52) defines the three labels but never says which
statements of this section carry "Lean-checked". `ll.tex:40-41` and `oc.tex:80` state the rule explicitly ("every
statement below whose head names a Lean declaration is Lean-checked"). In `fd` several heads mix Lean parts and
written steps (fd:lem:orient, fd:lem:rot, fd:lem:small, fd:lem:inv-image), so one sentence ("a statement or part whose
head names a Lean declaration is Lean-checked in this sense; parts marked 'written step' are not") would remove the
ambiguity for all later sections.

**m8 (minor; label definition).** "Computer-assisted" is defined as "a statement whose proof contains a finite
computation carried out by a machine: kernel evaluation of a decision procedure (Lean's `decide`), ..."
(fd.tex:43-48). Read literally, every statement whose Lean proof uses `decide` qualifies, so Remark fd:rem:pos-triples
(ii) (fd.tex:887-889) has to override the definition ("not computer-assisted in substance"). Fix: define the label by
the written proof: "a statement whose written proof relies on a finite computation that we do not carry out by hand".

**m9 (minor; typesetting).** Overfull boxes of 2.1pt (lines 765-766, head of fd:lem:four-subsets) and 5.1pt (lines
788-789, head of fd:lem:halfplane). Cosmetic.

## 5. Notes (no finding)

- "This section relies on no other section" (fd.tex:85) is accurate in the logical sense; the four `\ref`s to `ll:`
  and `oc:` labels are pointers in notation and remarks only.
- The section adds helper labels (`fd:def:conv`, `fd:lem:inv-image`, `fd:lem:rot`, `fd:lem:collinear-mem`,
  `fd:lem:hull`, `fd:lem:ngon-basic`, `fd:lem:forces-basic`, `fd:lem:small`, `fd:lem:halfplane`,
  `fd:lem:strict-supports`, `fd:lem:support-sum`, `fd:lem:neg-triples`); they are used only inside `fd`.
- The cited usage of `fd:` labels in the other ten sections (`\ref` with sub-items (a)-(d)) matches the content of the
  corresponding `fd` statements (checked by script and by reading the contexts of the `affine-orient`, `affine-cp`,
  `separation`, `pos-triples` and `rot` citations).

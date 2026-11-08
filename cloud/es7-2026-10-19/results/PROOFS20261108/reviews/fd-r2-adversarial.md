# Review of section `fd`, round 2, lens: adversarial

Section: `sections/fd.tex` (1190 lines), map `sections/fd.map.tsv` (40 rows).
Sources read: `ErdosSzekeres/{Definitions,Orientation,OrientationGeometry,Basic,ConvexCycleCuts}.lean`,
`ErdosSzekeres/Suk/{FourPoint,SupportingLines,OrientationClique,Reflection}.lean`, `LAYERLEAN/LayerLemma.lean`
(1-120, 150-380, 455-480, 1095-1115), `SYMLEAN/SymmetricReduction.lean` (50-58, 265-275, 395-405),
`SYMLEAN/AffineReduction.lean` (1-70, 1225-1320, 1444-1533), `LEANEXT/orbit/OrbitConsistency.lean` (1-130, 160-190),
`MIRRORETV/lean/MirrorMain.lean` (1-20, 2176-2190, 2498-2520), `SYMLEAN/mirror/ReductionThreeClasses.lean` (1265-1273,
3736-3746, 4057-4079), the cited logs (`docs/validation/axiom-audit-lower-bound-2026-10-11.txt`, `docs/VALIDATION.md`,
`LAYERLEAN/logs/build.log`, `LEANEXT/review/{axioms.log,REPORT.md}`, `SYMLEAN/logs/{runs.tsv,AffineReductionAxioms.out}`,
`LEANEXT/orbit/{logs/build.log,logs/axioms.log,REPORT.md}`, `MIRRORETV/lean/MirrorMain.out`, `MIRRORETV/README.md`,
`SYMLEAN/mirror/{axioms.out,README.md}`), `docs/SAT.md:160-236`, the inventories `LAYERLEAN.json` and
`MAIN-LIBRARY-coverage.json`, and the Lean 4.24.0 core file `Init/Core.lean` (for `trustCompiler`). Mathlib definitions
(`Collinear` = `Module.rank k (vectorSpan k s) <= 1`; `ConvexIndependent p` = `forall s x, p x in convexHull (p '' s) ->
x in s`; `convexIndependent_set_iff_notMem_convexHull_diff`; `collinear_iff_of_mem`) compared from knowledge of Mathlib
and from their uses in the repository files that compile against the pinned revision.

**Verdict: PASS.** No blocker, no major finding. Three minor findings (m1-m3) and two notes. Both round-1 major
findings are fixed. Every contract `fd:` statement is true and matches its Lean declaration; I found no contract
discrepancy.

## 1. Round-1 major findings: re-check

Both round-1 majors (fidelity F1, claims M1) concerned the same facts: Lean counterparts of `fd:lem:affine-orient`,
`fd:lem:affine-cp` and of `fd:lem:orient`(d) over the reals existed but were not tagged, and the remark and Coverage
said they did not exist.

- `fd:lem:affine-orient` is now tagged `\leanref{ErdosSzekeres.SymReduction.orient_affine}{SYMLEAN/AffineReduction.lean:1241}`
  (fd.tex:504). Source line 1241: `theorem orient_affine {g} {L} {b} (hg : forall p, g p = L *v p + b) (x y z) :
  orient (g x) (g y) (g z) = L.det * orient x y z`. The statement now reads "a map with g(x)=Ax+v for every x",
  which matches `hg`. The verbatim copy at `SYMLEAN/mirror/ReductionThreeClasses.lean:1267` is byte-identical over
  lines 1240-1246 / 1266-1272 (diff empty; namespace `ErdosSzekeres.SymReduction` there too). **Fixed.**
- `fd:lem:affine-cp` now states the Lean forms (b')-(e') and tags all five declarations; all five statements were
  compared with the source (`:1263`, `:1278`, `:1290`, `:1298`, `:1305`) hypothesis by hypothesis: exact. The proof of
  (b')-(e') is complete (adjugate identity checked with sympy). **Fixed.**
- New Remark `fd:rem:orient-lean` correctly identifies `OrbitConsistency.orient3_perm` (`:178`) as the case R = reals
  of (d); the index translation `t(i)=p_{i+1}`, `sigma(i)=pi(i+1)-1`, `(t o sigma)(i)=p_{pi(i+1)}` and the sign
  argument are correct. **Fixed.**
- The false sentences ("Lean proves the special cases it needs separately"; "Written steps without a single Lean
  counterpart") are gone. One residual inaccuracy of the same kind, at the level of a sub-part, remains (m1 below).
- Evidence added by the fixer checks out: `SYMLEAN/logs/runs.tsv` line 4 (`AffineReduction.lean 41cfc0b6 ... exit 0,
  0 output lines`), line 5 (`AffineReductionAxioms.lean`, exit 0); `diff AffineReduction.lean AffineReductionAxioms.lean`
  shows only appended lines; `AffineReductionAxioms.out` lines 9-11, 13-15, 16 are as cited; the uses at `:1528`,
  `:1462`, `:1295`, `:1281`, `:1303` are as cited.

## 2. Mechanical checks (all pass)

- Compile: private wrapper `build/fd_r2_adv/fd_adv2_wrapper.tex` (contract wrapper), `nice -n 15 pdflatex
  -interaction=nonstopmode -halt-on-error`, twice: both exit 0; 15 pages; 0 overfull boxes; undefined references only
  `ll:def:hv`, `ll:def:peel`, `ll:def:66-70`, `oc:lem:perm`, `oc:lem:rot-inv` (all contract export labels, all defined
  in `ll.tex`/`oc.tex`). No `\newcommand`, `\usepackage`, `\def`, `\documentclass`; only preamble environments.
- Labels: all 20 contract `fd:` labels defined once, on the named statements, in contract order. Every `\ref` is an own
  label or one of the five export labels above.
- Lean references: script `build/fd_r2_adv/checkrefs.py` resolved all 49 `\leanref`s: each cited line carries a
  declaration keyword and the declaration's short name; 0 mismatches. All 40 map rows (5 columns, header as required)
  match the 40 statement environments in label, kind and order; every map name occurs on its cited line.
- All `\dirn{file:N}` citations in the running text (41) were opened: each points at the claimed declaration or proof
  step (e.g. `LayerLemma.lean:165` `have himg`, `:330` `have hcc`, `:368` `rotAff`, `Reflection.lean:55`,
  `Construction.lean:54/118`, `Placement.lean:20`, `OrientationObstructions.lean:64/68`, `SpikeChain.lean:140`,
  `VisibleEdgeInsertion.lean:77`, `FiniteDensityBound.lean:66`, `MirrorMain.lean:2520`, `ReductionThreeClasses.lean:4079`);
  the enclosing theorem of each cited proof line is the theorem named (checked by script).
- SHA-256 prefixes: all 15 in the table recomputed; all match. HEAD is `7e32ee25931883f2...` on
  `es7-night-2026-11-01`; worktree clean; every cited research file is tracked. `lean-toolchain` =
  `leanprover/lean4:v4.24.0`; manifest Mathlib rev `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`; `lakefile.toml` name
  `erdos_szekeres`, `defaultTargets = ["ErdosSzekeres"]`; `lean-toolchain`, `lake-manifest.json`, `lakefile.toml` exist
  at the root only.
- Axioms evidence: audit lines 49 (multi-line entry 49-51), 87, 88, 103, 113, 114, 119, 132, 175, 176, 178, 624, 720,
  725, 732 are exactly the declarations named, with `[propext, Classical.choice, Quot.sound]`. `git diff 7f0868fdb HEAD`
  over all main-library files named, plus the import closure of `Basic`, `Suk/OrientationClique`, `Suk/Reflection`
  (computed by script: adds `Suk/{BaseChart,BaseOrder,CupsCaps,TriangleOrder}` and the four `Vendor/ErdosSzekeresConvex`
  files), is empty; 7f0868fdb is the commit that added the audit and the last commit touching `ErdosSzekeres/`. Text
  search of that closure and of the six research files: no `sorry`, `admit`, `axiom` declaration or `native_decide`.
  `LEANEXT/review/axioms.log` lines 1, 22, 23, 26, 33; `LEANEXT/orbit/logs/axioms.log` lines 1, 5;
  `MirrorMain.out` line 858; `SYMLEAN/mirror/axioms.out` line 11; `docs/VALIDATION.md:73` (`--wfail`): as cited.
  `Lean.trustCompiler` is `axiom trustCompiler : True` at `Init/Core.lean:2340` of the 4.24.0 toolchain, `ofReduceBool`
  at `:2392`: the native_decide sentence is right.
- "19 definitions of `rotAbout`": 19 in the research records, identical signature line and identical two-line body;
  none in the main library. The three `Invariant` definitions are textually identical.
- Symbolic checks (`build/fd_r2_adv/sym_check.py`, sympy 1.13.3): bracket expansion of orient; swap, cycle, translate;
  affine law with det; rot (c), (e), (f); invariance under rotAbout; det F = -1, F u = u, F u_perp = -u_perp,
  reflection sign; adjugate identity; kernel vector of a singular matrix; support sum; the halfplane certificate
  `(p1 q0 - p0 q1)(u+v-1)`; all twelve support values of `fd:lem:four-positive`; the separation expansion; the
  middle-parameter identity of `fd:lem:small`(c). 20 checks, all 0.
- No machine path, tool name, or non-ASCII character in `fd.tex` or `fd.map.tsv`.
- Cross-section use: every `\ref{fd:...}` in the other ten sections is to a contract label, and every cited part
  (`mono`(a)-(d), `orient`(a),(b),(d)) exists here with the meaning used there (contexts read for `affine-orient`,
  `affine-cp`, `separation`, `pos-triples`, `orient`(d)).

## 3. Adversarial attacks, statement by statement (all survive)

- **fd:def:point, fd:def:orient, fd:def:gp, fd:def:cp, fd:def:ngon, fd:def:forces**: compared token by token with
  `Definitions.lean:9-26` and `Orientation.lean:9`; `orient` over any `CommRing` (and used over Z in
  `IntegerCertificates.lean`, over Q in `Orientation.lean`, so the "Q and Z" sentence is true); the paraphrase of
  `ConvexIndependent` for the subtype inclusion is exact (injectivity of the inclusion makes `x in t` equivalent to
  `p x in p '' t`). `K = 0`: `HasConvexNGon 0 S` holds via the empty set, so "0-free" is contradictory, as fd:rem:ngon
  says. Upward closure of K-freeness uses mono(d) in the right direction.
- **fd:def:inv / fd:lem:inv-image**: non-injective f is excluded in (a), (b); f injective but not surjective
  (f(x) = 2x, S = {0}) satisfies (a), (b); S empty fine. (c) for an arbitrary type, induction with the iterate identity
  derived from Lean's convention `f^[n+1] = f^[n] o f` (base case now written).
- **fd:def:rot / fd:rem:angles / fd:lem:rot**: m = 0 gives `2*pi/(0:R) = 0` and rho_0 = id; real numerals 6, 7 equal
  the casts; (e) uses the open interval 0 < theta < pi (boundaries give sin = 0, correctly excluded) and p != c; the
  extra content of (b) (rho(c) = c), (c) (composition law, rho_0 = id) and (d) (bijectivity) is marked as written steps.
- **fd:lem:orient**: over a commutative ring; (e) for b = c needs commutativity (assumed); (d) covers all six
  permutations with correct signs (the two intermediate applications of (b) use the right argument order).
- **fd:lem:affine-orient**: singular A gives 0 = 0; (i) for every centre and angle; (ii) for every line (F_phi
  fixes u, negates u_perp); F_0 = diag(1,-1).
- **fd:lem:collinear-mem / fd:lem:collinear**: degenerate triples a = b, a = c, b = c, a = b = c all handled; the case
  split u_0 != 0 / u_0 = 0 is exhaustive and matches the private helper `exists_smul_of_det_zero`.
- **fd:lem:hull, fd:lem:cp-hull, fd:lem:mono, fd:lem:ngon-basic, fd:lem:forces-basic**: empty sets, n = 0, n' = 0,
  N = 0 (forces-basic(b) with N = 0 goes through T = empty set) all fine; no circularity (mono(d) mentions
  ngon-basic(b) only to describe the Lean proof).
- **fd:lem:small**: empty set and singletons; (c) needs pairwise distinct points (stated); in the collinear case the
  direction v is automatically nonzero, distinct points have distinct parameters, lambda in (0,1).
- **fd:lem:affine-cp**: (a) for every affine map, including non-injective ones and Y empty; the kernel vectors cover
  (alpha,beta) != 0, alpha = beta = 0 with (gamma,delta) != 0, and A = 0; (b)-(d) both directions use injectivity on
  all of R^2 where needed; (b')-(e') match Lean exactly (f a Mathlib `AffineMap`/`AffineEquiv`; h with `h p = L p + b`).
- **fd:lem:caratheodory**: Y infinite or empty (vacuous); x in Y (k = 1); minimal T has all weights positive; exchange
  step keeps weights >= 0 and sum 1 and forces k >= 2; k <= 3 by linear dependence in R^2.
- **fd:lem:four-subsets**: |s| < 4 in (a); (b) padding exists since |s| - |t| >= 4 - |t|; no general position used.
- **fd:lem:halfplane, fd:lem:strict-supports, fd:lem:support-sum**: no sign condition on u, v in (a) (as in Lean);
  u = 0 case of (b); s empty or a singleton in strict-supports.
- **fd:lem:four-positive**: coincident letters cannot occur (each pair lies in a triple with positive orientation);
  the "r equals one of the three other letters" step does not need distinctness; all twelve values verified.
- **fd:lem:pos-triples / fd:rem:pos-triples / fd:lem:neg-triples**: iota infinite allowed; u = {i in s : p(i) in t}
  has p(u) = t and |u| = 4; the variant for |s| <= 3 is correct and labelled as a variant; the reversed order is a
  linear order and the sign flip is the (1 3) transposition.
- **fd:lem:pos-cycle / fd:rem:pos-cycle**: N < k is vacuous (no embedding); quantifier order as in Lean;
  `ConvexCycleCut` is exactly the negated positivity; the `docs/SAT.md:168-233` citation describes these cuts.
- **fd:lem:separation**: F empty (both sides true, l = 0); x in F (both sides false); minimiser on the nonempty compact
  simplex (Rudin 2.41 and 4.16 are Heine-Borel and the extreme value theorem); first-order inequality and strict final
  inequality correct.
- **Conventions**: casts `(m:R)`, `x/0 = 0`, truncated subtraction, iterate order, `minimalPeriod` (0 if aperiodic),
  path rule (root files and the four root directories; everything else under RES; no section cites a root file such as
  `README.md` or `math.md` that the rule would misplace), keyword-line rule, namespace rule, three rigor labels and the
  rule for mixed heads: all accurate.

## 4. Findings (all minor)

**m1 (minor; tagging/coverage, residual of round-1 F1).** Part (i) of `fd:lem:affine-orient` has an exact Lean
counterpart but is tagged as a written step, and the Coverage paragraph says no Lean declaration states it.
- Where: fd.tex:504 (head "(i), (ii) written step"); fd.tex:1149-1154 (Coverage: "No Lean declaration states the
  following statements or parts in the form given here; ... parts (i) and (ii) of fd:lem:affine-orient (Lean special
  cases OrbitConsistency.orient_rotAbout_inv and Suk.orient_reflectY ...)"); map row `fd:lem:affine-orient` (note
  "(i),(ii) written step").
- Evidence: (i) reads "for all o,a,b,d in R^2 and theta in R, orient(rho_{o,theta}(a),rho_{o,theta}(b),rho_{o,theta}(d))
  = orient(a,b,d)". `LEANEXT/orbit/OrbitConsistency.lean:117`: `theorem orient_rotAbout_inv (c : Point) (theta : R)
  (a b d : Point) : orient (rotAbout c theta a) (rotAbout c theta b) (rotAbout c theta d) = orient a b d`, with
  `OrbitConsistency.rotAbout` one of the three textually identical copies cited in fd:def:rot. This is (i) itself, not a
  special case of it. The section's own Remark fd:rem:affine-orient-lean (fd.tex:551-555) says so ("Lean also proves
  (i) ... that is, (i), is OrbitConsistency.orient_rotAbout_inv"), and the axioms paragraph (fd.tex:209-212) cites its
  axioms line. So the head and Coverage contradict the remark, and under the rigor rule of fd.tex:67-69 ("a part marked
  'written step' is not [Lean-checked]") (i) is presented as not Lean-checked although it is. (ii) is a genuine special
  case (o = 0, phi = 0) and is described correctly.
- Why minor and not major: the declaration is named with file:line and export label in the adjacent remark; the error
  understates Lean coverage; the contract item itself is tagged with its exact counterpart `orient_affine`. A strict
  reading of the scope rule ("each tagged with its Lean name(s) where one exists") could rate it higher; I am not sure
  the rule is meant for sub-parts.
- Fix: in the head write "(i) \leanref{ErdosSzekeres.OrbitConsistency.orient_rotAbout_inv}{LEANEXT/orbit/OrbitConsistency.lean:117}
  (stated for the copy of rotAbout in that file); (ii) written step"; update the map row; in Coverage move (i) to the
  covered list and keep only (ii) (Lean special case `Suk.orient_reflectY`) in the written-steps list.

**m2 (minor; evidence precision).** fd.tex:209-210: "`LEANEXT/orbit/logs/build.log` records that
`LEANEXT/orbit/OrbitConsistency.lean` compiles (exit code 0)". The log is the 7-byte file `exit=0\n`; it names neither
the file nor its hash. The identification comes from `LEANEXT/orbit/REPORT.md` (line 3: the file is
`OrbitConsistency.lean`, SHA-256 `9b843180...`, "The coordinator re-checked the build, the sorry scan, the hash and the
axioms"), which the section does not cite. The claim is supported, but not by the log alone. Fix: add "(the log records
only the exit code; `LEANEXT/orbit/REPORT.md` identifies the file and its hash `9b843180...`)".

**m3 (minor; wording).** fd.tex:197-198: "`SYMLEAN/AffineReductionAxioms.lean` is `SYMLEAN/AffineReduction.lean`
followed by `#print axioms` commands". The diff shows 9 appended `#print axioms` lines and one `#check` line
(`#check @ErdosSzekeres.SymReduction.heptagon_of_nontrivial_affineEquiv`, whose output is
`AffineReductionAxioms.out` lines 18-27). Harmless. Fix: "followed by `#print axioms` and `#check` commands".

## 5. Notes (no finding)

- Understated, hedged evidence: `Suk.reflectY_x` and `Suk.reflectY_y` are used in the proof of `Suk.orient_reflectY`
  (`Reflection.lean:49`), hence covered by audit line 176 (and `reflectY_x` also by line 178 via
  `FiniteDensityBound.lean:62`). fd.tex:173-176 lists them among the declarations "not covered by a printed line that
  we identified". The hedge makes the sentence true; the fallback evidence is sound.
- `ErdosSzekeres.Omission.BoundaryGeometry.exposed_not_in_hull` (`ErdosSzekeres/Omission/BoundaryGeometry.lean:30`) is a partial Lean
  counterpart of the easy direction of `fd:lem:separation` (affine function zero at p, positive on S \ {p}). It is not
  the same statement, so tagging fd:lem:separation as a written step is correct; a one-line pointer would be optional.

## 6. Contract discrepancies

None. Every contract `fd:` definition and fact is true and is stated as in its Lean declaration (where one exists);
helper statements tagged with Lean names match their declarations; the variants (fd:lem:orient(d) over any commutative
ring, fd:rem:pos-triples(iii)) are labelled as such.

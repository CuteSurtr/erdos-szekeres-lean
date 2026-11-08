# Contract for the written proofs of the Lean-checked results (Stage 1)

Every writer, verifier and fixer reads this file first. It fixes the paths, the conventions, the labels that sections may
share, and the quality bar.

## Paths

- Repository checkout (git worktree, branch `es7-night-2026-11-01`, commit `7e32ee259`):
  `REPO` (a git worktree of the branch; machine path omitted)
- Research records: `RES = REPO/cloud/es7-2026-10-19/results`. Main Lean library: `REPO/ErdosSzekeres`.
- Staging area (all output goes here, never into REPO): `STAGE` (the staging directory; machine path omitted)
  - `STAGE/preamble.tex`: the only preamble. Section files use its macros and environments only.
  - `STAGE/sections/<key>.tex`: one section per key (written by the section's writer, edited by its fixer).
  - `STAGE/sections/<key>.map.tsv`: the statement map of the section (see below).
  - `STAGE/build/`: scratch for compile checks (`<key>_wrapper.tex` etc.).
  - `STAGE/reviews/`: verifier reports, `<key>-r<round>-<lens>.md`.
  - `STAGE/inventory/<UNIT>.json`: the read-only inventory of each Lean unit (statements, file:line, outlines, risks).
- Symbolic algebra for checking identities: `STAGE/../symvenv/bin/python` has sympy 1.13.3.

## Hard rules

1. **Never modify anything under REPO.** Read only. No git commands that change state.
2. **No heavy computation.** A long CPU campaign runs on this machine. Do NOT run lake, lean, elan, lean-lsp tools, SAT
   solvers, or anything long-running. Allowed: cat/sed/grep/rg/head/wc/find/diff/shasum, the Read/Write/Edit tools,
   `nice -n 15 pdflatex` (for compile checks of your own files), and short sympy scripts under `nice -n 15`.
3. **No machine paths and no tool names in any output file.** In the LaTeX, refer to files by paths
   relative to `RES` (e.g. `LAYERLEAN/LayerLemma.lean:189`) or, for the main library and experiments, relative to the
   repository root (e.g. `ErdosSzekeres/Definitions.lean:12`, `experiments/...`). Never write an absolute path of the build machine or a tool name.
4. **Fidelity.** Every theorem, lemma, proposition or definition that corresponds to a Lean declaration must be stated
   exactly as in Lean: every hypothesis (including side conditions such as `c ∉ S`, `0 < m`, `K ≤ 2*m`, `Finset` vs
   `Set`, maps-into vs equality, strict vs weak inequalities, natural-number subtraction, casts such as `(m : ℝ)` and
   `2*π/m` with `m = 0` giving `0`), the same conclusion, the same quantifier order. If the Lean statement is awkward,
   state it faithfully and add a remark explaining it. Never strengthen or weaken a Lean statement silently. If you
   state a convenient variant, label it as a variant and prove it from the Lean-faithful statement.
5. **Full proofs.** Every statement gets a complete proof that a mathematician can check without Lean. Never write
   "Lean-checked, proof omitted" or "see the Lean file". You may follow the Lean proof's structure or give a different
   correct proof; say which. You may cite standard textbook facts with a precise statement and a reference
   (Carathéodory's theorem, separation of a point from a compact convex set, Minkowski/Krein–Milman for polytopes,
   primitive roots of unity, pigeonhole, the classification of plane isometries via Mazur–Ulam, basic trigonometric
   identities). You may cite published theorems used by the Lean code as black boxes, stated exactly as used (e.g.
   Baek's theorem, formalized in the vendored code under `ErdosSzekeres/Vendor`), saying that they are cited.
6. **Computations.** If a Lean theorem is a finite computation (`decide`, `decide +kernel`, `rfl` on data, generated
   certificate files), give the full mathematical reduction to the computation, state the computation precisely (what
   is enumerated, how many cases, what is checked), and say how Lean checks it (kernel evaluation via `decide`; or
   `native_decide`, which trusts the compiler and adds the axiom `Lean.ofReduceBool`). Label such statements
   "computer-assisted". Never claim a hand proof of a computation you did not do by hand.
7. **Hypotheses are hypotheses.** If a Lean theorem takes unproved propositions or SAT verdicts as hypotheses (for
   example `Sixfold66`, the case classes `HalfTurn34` etc., or unsatisfiability of a CNF), say so in the statement
   and in a remark naming what in the project supplies them (certificate records) and with which rigor label. Never
   present such a theorem as unconditional.
8. **Rigor labels.** The Lean theorems keep their label *Lean-checked* (cite the axioms log the inventory names). The
   proofs in this document are *written proofs (not refereed)*. Do not call anything "verified", "certified" or
   "proved" beyond that. Do not repeat overclaiming wording from docstrings (e.g. "Corollary 3 exactly as written").
9. **Honesty about scope.** At the end of each section, a short paragraph "Coverage" lists the Lean declarations of
   the section's scope that are covered (by label) and any that are deliberately not covered, with the reason (e.g.
   verbatim duplicate, test or audit file, `#print axioms` line, helper absorbed into a proof).

## LaTeX rules

- The section file starts with `\section{...}\label{<key>:sec}` and contains no preamble, no `\begin{document}`,
  no `\usepackage`, no new macros (`\newcommand` is forbidden; ask for a macro in your report instead).
- Environments: `theorem, lemma, proposition, corollary, fact, definition, remark, proof` (from `STAGE/preamble.tex`).
- Head of every statement that corresponds to a Lean declaration:
  `\begin{lemma}[short name; \leanref{Full.Lean.Name}{DIR/File.lean:LINE}]\label{<key>:lem:...}`.
  Several names: `\leanref{A}{F:l1}, \leanref{B}{F:l2}`. Statements introduced only for the written proof: tag
  `[short name; written step]`.
- Labels: every label you define starts with `<key>:`. You may `\ref` your own labels, the foundations labels
  (`fd:...`, listed below), and the export labels of other sections (listed below). Nothing else.
- Every export label assigned to your section MUST be defined in your section, on the statement named for it.
- Compile check: create `STAGE/build/<key>_wrapper.tex`:
  ```
  \documentclass[10pt]{amsart}
  \input{../preamble}
  \begin{document}
  \input{../sections/<key>}
  \end{document}
  ```
  and run, from `STAGE/build`, `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error <key>_wrapper.tex` twice.
  It must exit 0. Undefined references to `fd:` or other sections' export labels are expected in this standalone check;
  any other undefined reference, any error, and any "Missing $" etc. is not acceptable.
- Statement map `STAGE/sections/<key>.map.tsv`: header `label\tkind\tlean_name\tfile_line\tnote`, one row per
  statement environment (kind = theorem/lemma/...; lean_name `-` for written steps; note = e.g. "computer-assisted",
  "takes hypotheses: Sixfold66").

## Shared conventions (all sections use these; the foundations section `fd` defines and proves them)

Points: $\R^2$, with $p=(p_0,p_1)$; Lean `Point = Fin 2 → ℝ` (`ErdosSzekeres/Definitions.lean`).
$\orient(a,b,c)=(b_0-a_0)(c_1-a_1)-(b_1-a_1)(c_0-a_0)$ (Lean `ErdosSzekeres.orient`, `ErdosSzekeres/Orientation.lean:9`);
positive means counterclockwise. $\conv$ = convex hull. $\card{S}$ = cardinality. For finite $X$:
$\hv(X)=\{x\in X: x\notin\conv(X\setminus\{x\})\}$ (Lean `hullVerts`), $\peel(X,0)=X$, $\peel(X,n+1)=\peel(X,n)\setminus\hv(\peel(X,n))$.
"$S$ is $K$-free" means $\neg\,$`HasConvexNGon K S`. Rotations act counterclockwise.

### Foundations export labels (section `fd`; every section may \ref these)

Definitions:
- `fd:def:point` points, coordinates, `Finset` vs set.
- `fd:def:orient` orient (formula above).
- `fd:def:gp` GeneralPosition: for all pairwise distinct $a,b,c\in S$, $\{a,b,c\}$ is not collinear (Mathlib `Collinear`).
- `fd:def:cp` ConvexPosition: `ConvexIndependent ℝ` of the inclusion of $S$.
- `fd:def:ngon` HasConvexNGon $n$ $S$: some $T\subseteq S$ with $\card T=n$ in convex position (no emptiness condition);
  $K$-free.
- `fd:def:forces` ForcesConvexNGon $N$ $n$: every $S$ in general position with $N\le\card S$ has a convex $n$-gon.
- `fd:def:inv` Invariant $f$ $S$: $f(p)\in S$ for all $p\in S$ (maps into). For injective $f$ and finite $S$ this is
  equivalent to $f(S)=S$ (and then $f^{-1}(S)=S$ as well).
- `fd:def:rot` `rotAbout c θ p = (c_0 + cos θ (p_0−c_0) − sin θ (p_1−c_1), c_1 + sin θ (p_0−c_0) + cos θ (p_1−c_1))`
  (`LAYERLEAN/LayerLemma.lean:298`; the same formula is defined separately in `SYMLEAN/SymmetricReduction.lean:400`
  and `LEANEXT/orbit/OrbitConsistency.lean:93`); in complex form $z\mapsto c+e^{i\theta}(z-c)$.

Facts (each with a full proof in `fd`):
- `fd:lem:orient` (a) $\orient(a,c,b)=-\orient(a,b,c)$ (`orient_swap`); (b) $\orient(b,c,a)=\orient(a,b,c)$
  (`orient_cycle`); (c) translation invariance (`orient_translate`); (d) for a permutation $\pi$ of $\{1,2,3\}$,
  $\orient(p_{\pi(1)},p_{\pi(2)},p_{\pi(3)})=\sgn(\pi)\orient(p_1,p_2,p_3)$.
- `fd:lem:affine-orient` for a linear map $A$ and $v\in\R^2$, $g(x)=Ax+v$:
  $\orient(g a,g b,g c)=\det(A)\,\orient(a,b,c)$. Rotations have $\det=1$, reflections $\det=-1$.
- `fd:lem:collinear` $\orient(a,b,c)=0$ iff $\{a,b,c\}$ is collinear (including degenerate triples)
  (`orient_eq_zero_iff_collinear`, `ErdosSzekeres/OrientationGeometry.lean:36`); hence $S$ is in general position iff
  $\orient(a,b,c)\ne0$ for all pairwise distinct $a,b,c\in S$ (`generalPosition_iff_orient_ne_zero`, `:66`).
- `fd:lem:cp-hull` $S$ is in convex position iff $p\notin\conv(S\setminus\{p\})$ for every $p\in S$
  (`convexPosition_iff`, `ErdosSzekeres/Basic.lean:15`).
- `fd:lem:mono` (a) a subset of a set in convex position is in convex position (`ConvexPosition.mono`); (b) a subset of
  a set in general position is in general position (`GeneralPosition.mono`); (c) `HasConvexNGon n S` and $S\subseteq S'$
  imply `HasConvexNGon n S'` (`HasConvexNGon.mono`); (d) `HasConvexNGon n S` and $n'\le n$ imply `HasConvexNGon n' S`.
- `fd:lem:affine-cp` an injective affine map $g$ of $\R^2$ satisfies $g(\conv Y)=\conv(gY)$; it preserves and reflects
  convex position, general position and `HasConvexNGon n` of finite sets.
- `fd:lem:caratheodory` (Carathéodory in the plane) if $x\in\conv(Y)$ then $x\in\conv(Y')$ for some $Y'\subseteq Y$
  with $\card{Y'}\le3$ (affinely independent).
- `fd:lem:four-subsets` (`Suk.convexPosition_of_subsets_card_le_four`, `ErdosSzekeres/Suk/FourPoint.lean:10`, and
  `Suk.convexPosition_of_four_subsets`, `:40`) a finite $S$ all of whose subsets with at most 4 points are in convex
  position is in convex position; if $\card S\ge4$ it suffices that all 4-subsets are.
- `fd:lem:four-positive` (`Suk.convexPosition_four_of_positive`, `ErdosSzekeres/Suk/SupportingLines.lean:47`) if
  $\orient(a,b,c),\orient(a,b,d),\orient(a,c,d),\orient(b,c,d)>0$ then $\{a,b,c,d\}$ is in convex position.
- `fd:lem:pos-triples` (`Suk.convexPosition_of_positive_triples`, `ErdosSzekeres/Suk/OrientationClique.lean:9`)
  exactly as in Lean: a linear order $\iota$, $p:\iota\to\R^2$ injective, a finite $s\subseteq\iota$ with
  $\card s\ge4$ and $\orient(p_i,p_j,p_k)>0$ for all $i<j<k$ in $s$; then $p(s)$ is in convex position.
- `fd:lem:pos-cycle` (`hasConvexNGon_of_positive_cycle`, `ErdosSzekeres/ConvexCycleCuts.lean:11`) exactly as in Lean.
- `fd:lem:separation` for finite $F\subset\R^2$ and $x\in\R^2$: $x\notin\conv F$ iff there is a linear functional
  $\ell$ with $\ell(x)>\ell(y)$ for all $y\in F$. (Only the easy direction is elementary; give both.)

### Sections of Stage 1 and their export labels

Each section MUST define its export labels on the named statements. Other sections may \ref them.

| key | title | export labels → Lean declaration |
|---|---|---|
| `fd` | Conventions and foundations | the `fd:` labels above |
| `ll` | The layer lemma and the reduction to exactly $mt$ points | `ll:def:hv` hullVerts; `ll:def:peel` peel; `ll:lem:hv` (convexPosition_hullVerts, hullVerts_nonempty, subset_convexHull_hullVerts, extreme_mem_hullVerts); `ll:lem:minperiod` minimalPeriod_rotAbout; `ll:thm:core` hullVerts_eq_orbitFS; `ll:thm:core-rot` hullVerts_eq_orbitFS_rotAbout; `ll:lem:inv-peel` invariant_peel; `ll:thm:layers` layers_are_orbits; `ll:lem:exists-layer` exists_layer; `ll:lem:antitone` peel_antitone; `ll:thm:card-peel` card_peel; `ll:thm:reduction` convexNGon_of_layers; `ll:def:66-70` Sixfold66 and Sevenfold70; `ll:thm:sixfold` sixfold_octagon; `ll:thm:sevenfold` sevenfold_octagon |
| `lg` | Geometry of the layers: nesting, chains, polar rules | `lg:lem:orient-rot` orient_rotAbout; `lg:lem:regular` orient_regular_nonneg (with trig_layer); `lg:thm:nesting` strict_nesting; `lg:lem:centre` centre_not_mem_of_even; `lg:thm:fan` hasConvexNGon_of_fan; `lg:lem:halfplane` lin_pos_of_peel; `lg:thm:chain` chain_clauses_sound; `lg:def:polar` polar; `lg:lem:polar` orient_polar; `lg:lem:ruleA` orient_polar_centre_inside; `lg:lem:sinadd` sin_add_lt; `lg:lem:ruleB` orient_polar_halfplane; `lg:thm:radius` dist2_le_of_later |
| `oc` | Orbit literals, rays and phases, key order | `oc:lem:rot-inv` orient_rotAbout_inv; `oc:lem:perm` orient3_perm; `oc:thm:literal` literal_sound; `oc:thm:encoder` encoder_literal_sound; `oc:lem:antipode` antipode_mem_of_even; `oc:lem:same-ray` same_ray_false; `oc:thm:phase-orbit` phase_ne_of_not_mem_orbit; `oc:thm:layers-ray` not_same_ray_of_distinct_layers; `oc:thm:layers-phase` phase_ne_of_distinct_layers; `oc:lem:cell` cell_lt_iff and cell_eq_iff; `oc:lem:rank` cell_lt_iff_rank; `oc:lem:antipode-cell` antipode_odd and antipode_even; `oc:thm:key` reduced_lt_iff_key |
| `pc` | Phase patterns and angular rules | `pc:def:arc` inArc, arcHasAntipode, Alternating, RunMid*; `pc:thm:alternating` alternating_iff_gaps_lt_pi; `pc:thm:runB` runMidB_iff; `pc:thm:trichotomy` phase_trichotomy; `pc:thm:rule-alt` orient_pos_of_alternating; `pc:thm:rule-run` orient_pos_of_runMidB (with D and A); `pc:thm:phase` orient_pos_of_phase; `pc:thm:sign` orient_sign_of_phase; `pc:thm:word` word_dichotomy; `pc:thm:layers` orient_pos_of_layers and the Capstone layer rules |
| `ec` | Small k = 7 and k = 8 corollaries (LEANEXT es7corr, ES8SYM, PRIMEFOLD compat) | `ec:thm:fivefold` fivefold_heptagon (and variants); `ec:thm:fourfold` fourfold_heptagon (and variant); `ec:thm:big-order` RefuteC6.part_a; `ec:lem:polar-u` C7.orient_polar; `ec:thm:nested` C7.nested_regular_orient; `ec:thm:compat` PCompat.classification (with dvd_card, card_mod, exists_iff); `ec:thm:l0` L0Check.L0_rot |
| `sr` | Reduction of symmetric sets to case classes (isometries) | `sr:def:iso` eDist2 and IsEucIsometry; `sr:def:classes` HalfTurn34, Threefold33, Fivefold35, MirrorOneAxis33, MirrorNoAxis34, Fourfold32; `sr:thm:structure` isometry_structure (with isometry_complex_cases); `sr:lem:concyclic` convexPosition_of_concyclic; `sr:lem:orbit` orbit_select and orbit_select_minimalPeriod; `sr:thm:main` heptagon_of_nontrivial_isometry; `sr:thm:variant` halfTurn_of_symmetric_counterexample; `sr:lem:mirror-line` mirrorOneAxis33_of_exclusionLine |
| `ar` | Affine symmetries | `ar:thm:transfer` hasConvexNGon_of_affine_symmetry; `ar:thm:main` heptagon_of_nontrivial_affineEquiv (and the variants affine, affineMap, image, coords) |
| `mm` | The mirror lemma and Theorem A | `mm:def:config` Configuration, HasCap, sorting; `mm:lem:slope` the slope/cap facts used; `mm:thm:mirror-polygon` cap_mirror_polygon; `mm:thm:axis-polygon` axis_left_polygon and axis_right_polygon; `mm:thm:odd` mirror_odd_general; `mm:thm:even` mirror_even_general; `mm:thm:line` the _line versions (with transport); `mm:thm:small` mirror_four, mirror_five, mirror_six (and _line) |
| `mb` | Mirror bounds via Baek's theorem and the three-class reduction | `mb:thm:baek` the cited vendored statement(s) exactly as used; `mb:thm:seven` mirror_seven and mirror_seven_line; `mb:thm:eight` mirror_eight and mirror_eight_line; `mb:thm:nine` mirror_nine and mirror_nine_line (with config_capacity113); `mb:thm:refl32` card_le_32_of_reflLine (with reflLine_eq_lineRefl); `mb:thm:classes` mirrorOneAxis33_proved and mirrorNoAxis34_proved; `mb:thm:main3` heptagon_of_nontrivial_isometry_3 and heptagon_of_nontrivial_affineEquiv_3 |
| `cb` | Case-split bookkeeping (threefold cover, central 34) | `cb:lem:run` run_sound and checkRoot_sound; `cb:thm:c3` all_roots_covered; `cb:thm:c2` all_cases_closed |

## Quality bar (what verifiers check; severity scale)

- **blocker**: a false statement; a statement that does not match its Lean declaration (missing, extra or changed
  hypothesis; different conclusion; wrong quantifier order); an invalid proof step or a real gap; circularity; an
  overclaimed rigor label (an assumption presented as proved; a computation presented as a hand proof); a nonexistent
  Lean name; a machine path or tool name in the output.
- **major**: a gap a competent reader could fill but that is not filled (missing case, true but unproved claim used);
  an ambiguous statement; a headline declaration of the scope missing without explanation; LaTeX that fails to
  compile; a \ref to a label not allowed by these rules; a wrong file or a line number off by more than 3.
- **minor**: style, typos, small imprecision with no effect on correctness.

A section passes when no verifier reports a blocker or major finding.

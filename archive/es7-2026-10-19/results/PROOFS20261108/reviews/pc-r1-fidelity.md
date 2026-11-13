# pc, round 1, lens: fidelity

**Verdict: pass.** No blocker and no major finding. Seven minor findings are listed below.

Paths are relative to the results directory `cloud/es7-2026-10-19/results` (RES), unless they start with
`ErdosSzekeres/` (repository root) or `sections/`, `build/` (staging area).

## What was checked

- **Inputs read.** CONTRACT.md; the pc-relevant entries of `inventory/LEANEXT.json` (definitions, main_results,
  risks, non_results, recommended_writeup); `sections/pc.tex` (951 lines); `sections/pc.map.tsv` (32 rows).
- **Lean sources read.**
  - `LEANEXT/phase/PhaseClassification.lean`, all 545 lines.
  - `LEANEXT/linked/Linked.lean`: lines 925-1060 (polar, rules, dist2, dist2_le_of_later) and 1375-1416 (new).
  - `LEANEXT/capstone/Capstone.lean`: lines 1-18 and 1955-2004.
  - `LEANEXT/capstone/Capstone2.lean`: lines 1995-2132.
  - The definitions used by the layer theorems: Invariant (Linked:105), hullVerts (:111), rotAbout (:298) and
    peel (:374); HasConvexNGon (`ErdosSzekeres/Definitions.lean:21`); orient, orient_swap and orient_cycle
    (`ErdosSzekeres/Orientation.lean:9-16`).
- **Mechanical checks.**
  - **Head references.** All 53 `\leanref{Name}{File:Line}` heads were extracted. Each named declaration is on
    exactly the cited line (offset 0 in every case). The namespaces are `PhaseClassification`,
    `ErdosSzekeres.LayerLemma` and `ErdosSzekeres.Capstone`.
  - **Labels and kinds.** The labels and environment kinds of the 32 statement environments equal the 32 map rows,
    in the same order. Every row has 5 tab-separated fields.
  - **References.** Every `\ref` points to a pc: label, an fd: label from the contract list, or an export label of
    ll or lg (ll:def:hv, ll:def:peel, lg:def:polar, lg:lem:polar, lg:lem:ruleA, lg:lem:sinadd, lg:lem:ruleB,
    lg:thm:radius). I checked in `sections/lg.tex` and `sections/ll.tex` that these labels exist on the matching
    declarations (lg.tex:446, 720, 728, 749, 768, 778; ll.tex:152-153, 466).
  - **Compile check.** I used my own wrapper, `build/pc_fidr1_wrapper.tex`. Two pdflatex passes both exit 0. The
    only undefined references are fd:, ll: and lg:; there are no errors and no "Missing $".
  - **Forbidden text.** No machine path or tool name appears in `pc.tex` or `pc.map.tsv`.
- **Diff and hash claims in "Sources".** All re-checked and true:
  - PhaseClassification 40-102 against LayerLemma 931-996: only docstring lines differ.
  - Linked 1-1147 equals LayerLemma 1-1147, and Linked 1-1384 equals Merged 1-1384.
  - Capstone 19-1424 equals Linked 11-1416; Capstone line 1425 is blank; Capstone 1426-1965 equals
    PhaseClassification 6-545.
  - Capstone2 1-2003 equals Capstone 1-2003, and Capstone2 line 2004 is blank.
  - Capstone2 is byte-identical to `ENCBLEAN/geo/ES8Geo/Capstone2.lean` (cmp; `ENCBLEAN/geo/SOURCES.sha256:4`).
  - Line counts 545/1416/2004/2132 and all nine 12-hex hash prefixes match.
  - The toolchain pins are v4.24.0 and Mathlib f897ebcf. `git log` shows they are unchanged since 2026-10-04.
- **Rigor claims.**
  - `LEANEXT/phase/logs/axioms.log` lists exactly the 16 names given, each with the three standard axioms.
  - Each other PhaseClassification declaration is used in the statement or proof of one of the 16.
  - A text search of the four files finds no sorry, admit, axiom declaration or native_decide. In this section's
    declarations, `decide` occurs only at PhaseClassification:543. The other `by decide` is at Linked:1125, which
    is outside the scope.
  - `ENCBLEAN/logs/m4_build.log` shows a successful build in which only KeyOrder prints (axiom lines). According
    to `ENCBLEAN/README.md:266,283`, M4 added the Capstone2 copy.
  - The uses on the ENCBLEAN route are real:
    - Labelling.lean:63-65 (ne_of_mem, exists_angle, sqrt_dist2_pos) is in exists_layer_polar, which feeds the
      pinned labelling_of_counterexample.
    - Labelling.lean:133 (dist2_polar) is inside labelling_of_counterexample.
    - ArcBridge.lean:155-156 (polar_add_int_two_pi, polar_eq) is in P_eq_polar.
    - ArcBridge.lean:464 and :481 (orient_pos_of_alternating, orient_pos_of_runMidB) are in labelling_ruleA and
      labelling_ruleB, which feed the pinned modelOfLabelling (ModelOfLabelling.lean:29-30).
    - The pins are at Audit.lean:30-70.
  - The REPORT citations are correct: phase/REPORT.md "Not in Lean" item 2; capstone/REPORT.md:41-44 "Open
    issues"; mutants.log M7 is the `decide` failure when the premise is dropped.

## Statement-by-statement comparison (Lean vs section)

Each row: hypotheses, conclusion, quantifier order, types, strictness and casts compared against the Lean text.

| label | Lean declaration(s) (file:line) | result |
|---|---|---|
| pc:def:polar | PhaseClassification.polar (PC:41); LayerLemma.dist2 (LAYERLEAN:999) | `![c0 + r cos θ, c1 + r sin θ]`, r unrestricted; dist2 = (y0-c0)^2+(y1-c1)^2. Exact. |
| pc:lem:polar-facts | orient_polar (PC:44), orient_polar_centre (:407), orient_polar_centre_inside (:51), sin_add_lt (:64), orient_polar_halfplane (:80) | (a)-(e) exact. Rule A uses `α-δ+2π` in both bounds, as in Lean. Rule B does not assume `0<rb`. |
| pc:lem:periodic | polar_add_int_two_pi (:106), polar_add_two_pi (:111), polar_toIcoMod (:485) | Exact. k ∈ ℤ cast to ℝ. toIcoMod has base α and argument θ, as in Mathlib `toIcoMod hp a b`. (T1)/(T2) are toIcoMod_mem_Ico and toIcoMod_add_toIcoDiv_zsmul. |
| pc:lem:exists-polar | exists_polar (:459) | `p ≠ c → ∃ r θ, 0 < r ∧ p = polar c r θ`. Exact. |
| pc:lem:helpers | Capstone.polar_eq (Capstone:2001), polar_zero (Capstone2:2051), LayerLemma.dist2_polar (Linked:1390), exists_angle (Capstone2:2056), sqrt_dist2_pos (:2064), ne_of_mem (:2073) | Exact. The section states that (b)-(e) use LayerLemma.polar. ne_of_mem is over a Finset S. |
| pc:def:arc | inArc (:117), arcHasAntipode (:120), Alternating (:126), RunMidB (:132), RunMidD (:136), RunMidA (:140) | Exact. RunMidA = ¬H3 ∧ ¬H1 in Lean's conjunct order, which the proof of (ii) of trichotomy relies on. |
| pc:lem:inarc | inArc_of (:143), not_inArc (:147) | Exact. The closed bounds `s+g ≤ θ+2πm ≤ s+2π` match. |
| pc:lem:empty | arc1_empty (:161), arc2_empty (:169), arc2_empty' (:177), arc3_empty (:185), arc3_empty' (:193), arc1_empty' (:201) | Exact, including the hypothesis subsets: (c) has no α<β, (e) has no β<δ, and (f) keeps the unused α<β as in Lean. The claimed integers m are (0,0,0), (0,0,0), (1,0,0), (1,0,0), (1,1,0), (0,0,-1), the same as the Lean proofs. All inequalities re-derived. |
| pc:lem:arc12 | arc12_nonempty (:229) | Exact: `π < δ-α → H1 ∨ H2`. |
| pc:thm:alternating | alternating_iff_gaps_lt_pi (:210) | Exact, with no genericity. The witnesses (δ+π, k=-1), (α+π, 0), (β+π, 0) match Lean. |
| pc:prop:exactly-one | alternating_exactly_one (:386) | Exact: a three-fold conjunction with the same nine inArc atoms. The non-membership m values (0,0 / 0,0 / 1,0) match Lean. |
| pc:thm:runB | runMidB_iff (:251) | Exact. The hypothesis is `α+2π-δ ≠ π`. |
| pc:prop:gaps | gap_classification (:268) | Exact. The four disjuncts are in Lean's order and form. Remark 2 correctly notes that "exactly one" is only in the docstring. |
| pc:thm:trichotomy | phase_trichotomy (:285) | Exact: (Alt ∨ A ∨ B ∨ D) ∧ (Alt → ¬A ∧ ¬B ∧ ¬D). pc:rem:runs says the mutual exclusion of runs is not in Lean and proves it separately. |
| pc:thm:rule-alt | orient_pos_of_alternating (:301) | Exact. |
| pc:thm:rule-run | orient_pos_of_runMidB (:310), _runMidD (:318), _runMidA (:342) | Exact. Positivity hypotheses: (B) ra, rd; (D) ra, rb; (A) rb, rd. Gap hypotheses: (B) g3, (D) g1, (A) g2. Radius orders: (D) rb≤rd, ra≤rd; (A) rb≤ra, rd≤ra. |
| pc:thm:phase | orient_pos_of_phase (:372) | Exact. The three implications are written exactly as hA, hB, hD. |
| pc:prop:centre | centre_inside_of_alternating (:414) | Exact: orient(a,b,c), orient(b,d,c), orient(d,a,c), all > 0. |
| pc:prop:halfplane | halfplane_of_runMidB (:431) | Exact: ∃ φ, ∀ p ∈ {a,b,d}, 0 < (p0-c0)cos φ + (p1-c1)sin φ. |
| pc:thm:sign | orient_sign_of_phase (:496) | Exact. The outer hypotheses are ha, hb, hd, β'≠α and δ'≠α. Each conjunct takes its order, three gap conditions and three radius implications. In (ii) the radius roles of b and d are swapped exactly as in Lean (:514-519). a, b, d use the original β and δ. |
| pc:thm:word | word_dichotomy (:539) | Exact: ∀ s : Fin 6 → Bool, (∀ i, s(i+3) = !s i) → (alt ∨ run) ∧ ¬(alt ∧ run). The section explains Bool-as-Prop and Fin 6 addition mod 6. It is labelled computer-assisted, gives a hand proof (all 8 words checked by me) and says no native_decide is used. |
| pc:thm:layers | LayerLemma.orient_pos_of_layers (Linked:1398); Capstone.orient_pos_of_layers_runMidB (Capstone:1977); _runMidD (Capstone2:2011); _runMidA (:2031); _runMidB_intrinsic (:2082); _runMidD_intrinsic (:2098); _runMidA_intrinsic (:2115) | Exact for all seven. (L) = 0<m, K≤2m, c∉S, Invariant (maps-into), ¬HasConvexNGon K S, with S a Finset, m, K ∈ ℕ and m cast in 2π/m. The hull-vertex point and the index inequalities are correct per case (b: nb≤na, nb≤nd; d: nd≤na, nd≤nb; a: na≤nb, na≤nd). Positivity of all three radii is in (P). (a) uses 0<β-α, 0<δ-β, δ-α<π. The intrinsic versions use √(dist2 c ·) with no radius variables. |
| pc:cor:alt-polar | Capstone.orient_pos_of_alternating_polar (Capstone:1992) | Exact, stated with LayerLemma.polar. |
| pc:lem:shift, remarks | written steps | Correctly tagged as written steps. The line ranges cited for the Lean have-steps (PC 323-335, 346-362) are right. |

**Coverage.**
- PhaseClassification.lean has 39 declarations (7 defs and 32 theorems); all are covered.
- The 14 new declarations of Linked (2), Capstone (3) and Capstone2 (9) are all covered.
- The 10 export labels assigned to pc (pc:def:arc, pc:thm:alternating, pc:thm:runB, pc:thm:trichotomy, pc:thm:rule-alt,
  pc:thm:rule-run, pc:thm:phase, pc:thm:sign, pc:thm:word, pc:thm:layers) are all defined on the named statements.
- The exclusions in the Coverage paragraph (the copies in Linked 1-1384 and Capstone(2) 1426-1965) are accurate, and
  the declarations they defer are present in ll/lg/oc.
- The task notes are addressed:
  - phase_trichotomy is stated as the disjunction plus "Alternating excludes runs" (Theorem pc:thm:trichotomy and
    Remark pc:rem:runs).
  - gap = π is treated in pc:rem:alt-boundary, pc:rem:runB-example ((0, π/2, π)) and pc:rem:gaps(1) ((0, π, 3π/2),
    checked: all four disjuncts false).
  - The decide computation is described.

## Findings (all minor)

1. **minor: intro bullet for rule B drops its gap hypothesis** (pc.tex:15-17).
   - The bullet says "Rule B: a triple with a run turns counterclockwise if the middle point of the run has the
     largest radius". Every Lean rule-B statement also needs the gap opposite the run to be ≠ π (hg3/hg1/hg2) and
     positive radii for the two outer points. The second bullet (pc.tex:11-12) does state its proviso
     `α+2π-δ ≠ π`.
   - The formal Theorem pc:thm:rule-run is faithful, so only the overview is affected.
   - Fix: add "(given the corresponding gap ≠ π)".
2. **minor: Remark pc:rem:layers-scope is imprecise for part (a)** (pc.tex:906-909).
   - The remark lists "the gap condition ≠π and the pattern" as hypotheses of Theorem pc:thm:layers. Part (a)
     (orient_pos_of_layers, Linked:1398-1404) has neither; it assumes `0<β-α`, `0<δ-β` and `δ-α<π`.
   - Fix: say "in (b)-(e)", or list the hypotheses of (a) separately.
3. **minor: "How Lean checks it" could state the checked proposition per function** (pc.tex:742-748).
   - The text says that for each of the 64 functions the kernel evaluates the premise, the alternation condition
     and the run condition. The `Decidable` instance for an implication does not evaluate the conclusion when the
     premise is false.
   - The paragraph never states the per-function check itself: premise ⇒ ((alt ∨ run) ∧ ¬(alt ∧ run)), which the
     8 premise-satisfying words must pass.
   - Correctness is not affected. I am unsure whether the contract's "state the computation precisely" requires
     this.
   - Fix: one sentence, "for each s the procedure decides premise → ((alt ∨ run) ∧ ¬(alt ∧ run)); exactly 8 of the
     64 functions satisfy the premise".
4. **minor: ambiguous parenthetical in "Rigor and axioms"** (pc.tex:72-75).
   - "the final theorems of the ENCBLEAN geometric package (ENCBLEAN/geo/ES8Geo/Labelling.lean and ArcBridge.lean)"
     reads as if the final theorems were in those two files. The pinned theorems are in Main.lean,
     ModelOfLabelling.lean and Labelling.lean; Labelling.lean and ArcBridge.lean are where the helpers are used.
   - The substance (transitive coverage by the pins at Audit.lean:30-70) is correct; see the checks above.
   - Fix: "are used in Labelling.lean and ArcBridge.lean, in the proofs of the final theorems ...".
5. **minor: map notes use LEANEXT-relative paths** (pc.map.tsv rows pc:def:polar, pc:lem:polar-facts,
   pc:lem:periodic, pc:rem:word-scope).
   - Examples: `linked/Linked.lean:999`, `capstone/Capstone2.lean:1007`, `phase/logs/axioms.log`, `phase/REPORT.md`.
     Elsewhere the map and the LaTeX use the RES-relative form `LEANEXT/...`.
   - Fix: prefix `LEANEXT/`.
6. **minor: polar constant not named in the subsection "Arbitrary real directions"** (pc.tex:688-693).
   - The convention "polar is PhaseClassification.polar" is declared only for the preceding subsection
     (pc.tex:576-577). Theorem pc:thm:sign introduces a, b, d with `polar` again without saying which constant;
     Lean uses PhaseClassification.polar.
   - This is immaterial by Lemma pc:lem:helpers(a) (rfl).
   - Fix: add "(PhaseClassification.polar)" in the theorem.
7. **minor (cosmetic): overfull boxes** in the compile log.
   - 59 pt in the head of Theorem pc:thm:layers (pc.tex:816-818), from the seven `\leanref`s in the optional
     argument.
   - 42 pt in Corollary pc:cor:alt-polar (pc.tex:893-898).
   - 12 pt at pc.tex:131-132 and 6 pt at pc.tex:419-420.
   - Compilation succeeds.

## Points examined that are not findings

- **The two polar constants.** The section distinguishes them correctly and states each theorem with the constant
  its Lean statement uses: PhaseClassification.polar in PC theorems; LayerLemma.polar in Linked, Capstone and
  Capstone2 statements, and in dist2_polar, exists_angle and sqrt_dist2_pos.
- **The written equivalences in Lemma pc:lem:shift.** They are stronger than the one-directional Lean have-steps.
  They are tagged "written step" and proved in both directions, and the text says that Lean proves only left to
  right. This is not a silent strengthening of a Lean statement.
- **The hand proof of word_dichotomy.** The 8-row table was checked by me; every word and run position is correct.
  The shorter argument (equal pair, antipodal pair, extension to PPP) is also correct. The statement is labelled
  computer-assisted and Lean's `decide` is described as kernel evaluation, so no hand proof is claimed for the Lean
  computation.
- **Axioms of the new Linked/Capstone(2) declarations.** The section states honestly that there is no recorded
  axiom check for orient_pos_of_layers, the six Capstone layer rules and orient_pos_of_alternating_polar. This
  matches the inventory's axioms_status and risks.

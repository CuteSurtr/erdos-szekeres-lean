# Section `lg`, polish round 1: diff audit

Lens: diff. Inputs:
- the passed snapshot `snapshots/sections-r1pass/lg.tex` and `lg.map.tsv`;
- the current `sections/lg.tex` (940 lines) and `lg.map.tsv` (31 rows);
- the fix log `reviews/lg-polish-r1-fix.md`;
- the round-1 reports `reviews/lg-r1-{fidelity,rigor,adversarial,claims}.md` and `reviews/lg-writer-concerns.md`.

No earlier polish-round audit or referee report for `lg` exists. The fixer's own pre-edit snapshot
`snapshots/polish-r1-pre/lg.{tex,map.tsv}` is byte-identical to the passed snapshot, so every change audited here comes
from this round. Paths below are relative to STAGE, to RES (`LAYERLEAN/...`, `LEANEXT/...`, `WRITEUP/...`) or to the
repository root (`ErdosSzekeres/...`). "LL" is `LAYERLEAN/LayerLemma.lean`.

**Verdict: pass.**
- No blocker or major finding.
- Two minor findings (m1: the word "certified" in the new *Encoders* paragraph; m2: the overview's "In the main
  statements" still does not fit Theorem lg:thm:fan).
- 13 fixes confirmed, 9 duplicates accepted, 1 decline accepted; the 13 "other changes" of the log are all correct.
- Build clean: both passes exit 0, no error, no overfull box.

## 1. Hunks checked (tex: 22 hunks; tsv: 7 rows changed)

Every hunk is in the fix log; no undocumented change was found. "OK" means: mathematics correct, claim supported by
the cited Lean source or record (re-read for this audit), no rigor label raised, no machine path or tool name.

| # | Current lines | Change | Check |
|---|---|---|---|
| 1 | 3-30 | Overview: "In the main statements ... (m >= 1)"; hypotheses added to each bullet; half-plane wording; fan "gives n+1 points in convex position"; chain bullet restated geometrically | Each bullet matches its declaration: strict_nesting (LL:529, `2 ≤ m`, GP), centre_not_mem_of_even (LL:582, `0 < m`, `Even m`, `p ∈ S`, `p ≠ c`; "m ≥ 2 even" is equivalent), dist2_le_of_later (LL:1012, `n ≤ n'`; peel(S,n) is the union of layer n and later layers), hasConvexNGon_of_fan (LL:700; hhalf forces w ≠ 0 since n ≥ 3, so the chain lies in an open half-plane whose boundary passes through p), lin_pos_of_peel (LL:864, `3 ≤ m`, GP), chain_clauses_sound (LL:914, `4 ≤ K`, hq, hqp, hfan, hturn). OK, except m2 (lead sentence) |
| 2 | 32-49 | Sources: "heads a statement"; §1.1 declarations lie outside 465-1032 and are restated in ll; main-library list made complete; fd:lem:mono(c) not used by Lean | All 27 heads are in LL 465-1032 (every `\leanref` line number re-checked: 27/27 match). §1.1 recalls orbitFS (LL:48), Invariant (LL:105), hullVerts, peel, rotAbout (LL:298), subset_convexHull_hullVerts, peel_antitone (LL:460), invariant_peel, hullVerts_eq_orbitFS_rotAbout (LL:364): all < 465 and all restated in `sections/ll.tex` (lines 110, 158, 389, 188, 465, ...). Identifiers of LL 465-1032 from the main library (grep): Point, GeneralPosition, ConvexPosition, HasConvexNGon, orient, orient_cycle, generalPosition_iff_orient_ne_zero, Suk.convexPosition_of_positive_triples; Invariant is LL's own. Orientation.lean lines 9 and 15, OrientationGeometry.lean:66, OrientationClique.lean:9, Basic.lean:20 (HasConvexNGon.mono) and the five SHA-256 prefixes re-checked. No `.mono` in LL 465-1032. fd restates orient_cycle (fd:lem:orient(b)) and generalPosition_iff_orient_ne_zero (fd:lem:collinear(b)). OK |
| 3 | 51-57 | Build: build.log has no hash; REPORT.md gives the same result for afb8542d (1148 lines); the 6 Nov re-check compiled LayerLemmaAxioms.lean, whose first 1148 lines are LL, exit 0 | build.log is three lines (command, `exit code: 0`, `messages: 0 lines`), no hash. REPORT.md:3-4 (4 November 2026; afb8542d…, 1148 lines) and :15 ("Build. Exit 0, no messages."). LayerLemmaAxioms.lean has 1168 lines; `head -n 1148` equals LL (diff empty; SHA-256 afb8542dceb0…); 19 `#print axioms` lines follow; out.txt ends with "Exit status: 0" and "exit 0"; README.txt dates the run 6 November 2026, 04:59 KST. OK |
| 4 | 59-69 | Axioms: review log covers 59 declarations = all `theorem`s except the 7 `@[simp]`; file has 66; REPORT.md's wording quoted; "in each of the two logs ... that it prints" | LL has 66 `theorem` declarations, 7 of them `@[simp]` (LL:236-254). The 59 names of LEANEXT/review/axioms.log equal the 59 non-simp theorem names (set difference empty). All 23 of the section are printed there with [propext, Classical.choice, Quot.sound]; the only line with fewer axioms is iterate_mem, not in this section. LAYERLEAN/logs/axioms.log prints exactly 16 of the 23 (the 7 named ones absent). REPORT.md:16 says "All 59 theorem declarations were checked". Hashes 3c4b7aac502e, 386c4f578725, a59c3816cbe7 re-checked. OK |
| 5 | 71-84 | Rigor: "follow the structure"; automatic-tactic identities derived by hand; every other difference stated; per-written-step relation to Lean | Proof-by-proof comparison with LL: the only non-tactic differences are rotAbout_iterate (complex form; parenthetical l. 253-256), x ≠ ρ(x) (Remark (1) after nesting), ρ(p') = p (Remark (2) after lin_pos_of_peel), the Cramer route for the three `ring` identities (parentheticals l. 577, 608; Remark (1) l. 750), Step 2 of the fan theorem (l. 687), the `HasConvexNGon` unfolding (l. 776), orient_polar (l. 816), trig_layer (l. 305). All are stated. The per-step descriptions match LL (crot_comp/crot_one in rotAbout_iterate; nlinarith with sin²+cos² in dist2_le_of_later; minimalPeriod in lin_pos_of_peel; three `ring` instances). OK |
| 6 | 86-97 | New paragraph *Encoders* | README.md:97-104 lists "From phase patterns to the rules" and "Code to clauses" under "What is not in Lean"; README.md:120-125 gives "(written proof, review and tests)". k8_soundness.tex:923-924 (trust table: code-to-clause "written proof (not refereed) by reading the source"), :961-978 (G1: closed in Lean on a second route for encoder B, m = 6, for the Lean definition EncB.encB), :993-995 (E1: "evidence from running compiled code, not a Lean theorem"). REPORT.md item 8 supports "rule B needs the weak radius order". OK, except m1 |
| 7 | 116-121 | (lg:eq:J) split with `gathered` | Same five identities; number beside the display (page 2 of the PDF). OK |
| 8 | 141-144 | "every statement ... in which 2π/m occurs assumes m ≥ 1" | Statements with 2π/m: lg:lem:layer, lg:cor:period, regular, lin-orbit, next-prev, nesting, centre, radius, halfplane, chain, and (L3)/(L4): each has 0 < m or more. OK |
| 9 | 152-159 | Paragraph *Sine and cosine*, (S1), (S2), Rudin Ch. 8 and three Mathlib names | (S1), (S2) true. Same inline citation style as fd (fd.tex:1125); Rudin is in `bibliography.tex`. The three names exist in namespace Real at the pinned Mathlib f897ebcf72 (checked in a local Mathlib checkout at that commit): sin_pos_of_pos_of_lt_pi (Trigonometric/Basic.lean:396), cos_eq_one_iff (:516, `cos x = 1 ↔ ∃ n : ℤ, n * (2π) = x`), cos_le_one (Analysis/Complex/Trigonometric.lean:624). OK |
| 10 | 178 | (L1) cites ll:lem:hv(c) | ll.tex:193: item (c) is subset_convexHull_hullVerts. OK |
| 11 | 253-256 | rot-iter parenthetical: γ = c₀+ic₁, rotAbout_eq_crot (line 302), crot_iterate (line 267) | LL:302 `rotAbout c θ = crot (toC c) (Complex.exp (θ * Complex.I))`; LL:267 `(crot c w)^[k] = crot c (w ^ k)`; LL:465-469 then uses `Complex.exp_nat_mul`. OK |
| 12 | 305-307 | trig_layer parenthetical | LL:483-485: `rw [cos_two_mul ×2, sin_two_mul ×2, sin_sub]; linear_combination (…) * sin_sq_add_cos_sq t − (…) * sin_sq_add_cos_sq s`. OK |
| 13 | 329, 335, 377, 397 | (S1)/(S2) tags | Each use is the stated fact on the stated interval. OK |
| 14 | 402, 411-412 | Title `{orient(a,b,·) ≥ 0} is convex`; sentence on a ≠ b / a = b | Statement unchanged and exact (LL:516). orient(a,b,q) = det(b−a, q−a): a non-zero linear functional of q for a ≠ b; identically 0 for a = b by (O3). OK |
| 15 | 419-421, 434 | Lead "(Closed disks are convex.)" removed; sentence after the proof | Statement exact (LL:1002, every R ∈ ℝ). For R ≥ 0 the closed disk of radius √R (a point for R = 0); empty for R < 0. OK |
| 16 | 472-482 | Remark (2): segment convexity proved in place; Remark (3) points to *Encoders* | The convex-combination argument is correct (parameter uλ₁+vλ₂ ∈ [0,1]); the segment contains L = {x, ρ(x)} (λ = 0, 1). OK |
| 17 | 577-578, 585, 608-609 | trans / fan_step: "Lean checks ... by ring"; "(here c is an arbitrary point, not a centre)" | LL:633-635 and :645-647 (`simp only [orient, lin]`/`[orient]; ring`). fan_step's binders `{p a b c e : Point}` are arbitrary; statement otherwise unchanged and exact (LL:641). OK |
| 18 | 668, 687-688 | Title "fan chains give convex polygons"; Step 2 parenthetical | Statement unchanged and exact (LL:700-704). LL:731-783: explicit choice of k (three cases), `orient_cycle`, `hzero : orient a a c = 0`. OK |
| 19 | 755-786 | Title "geometric chain soundness"; (C1)-(C4); unfolding note; remark with REPORT.md F5 | Statement re-compared with LL:914-920: all hypotheses (3 ≤ m, 4 ≤ K, K ≤ 2m, c ∉ S, Invariant, ¬HasConvexNGon K S, GP, p ∈ hullVerts (peel S i), hq, hqp, hfan, hturn with `K - 1`), conclusion False, binder order: unchanged. (C1)-(C4) = hq, hqp, hfan, hturn; no old (i)-(iv) reference remains. LL:924-926 unfolds HasConvexNGon. REPORT.md:52 (F5) is quoted correctly. The title matches k8_soundness.tex:914 ("chain soundness (…, geometry)"). OK |
| 20 | 816-817 | orient_polar parenthetical | LL:938-940 (`simp only [..., Real.sin_sub]; ring`). OK |
| 21 | 831-848, 868 | ruleA proof/text, sinadd, ruleB (S1)/(S2) tags; gaps named | Gaps β−α, δ−β, α+2π−δ sum to 2π. LL:951-953 uses sin_add_two_pi ("2π-periodicity"). OK |
| 22 | 874-883 | Rule B remark: r_y ≤ r_x for r = √dist2; REPORT.md F2 | √ is monotone on [0,∞). REPORT.md:46-48 (F2) quoted correctly. OK |
| 23 | 885-940 | Coverage: scope = all declarations of LL 465-1032 (23 + 4); rotAbout_iterate also in ll; trig_layer placement; "adjoin"; eight copies; other namespaces | LL 465-1032 holds exactly 27 declarations (23 theorems; lin, fanPt, polar, dist2), nothing else (no instance, notation, attribute). ll.tex:401 restates rotAbout_iterate. Eight copies: each contains LL 11-1147 byte for byte (start lines 19, 19, 11, 11, 11, 11, 19, 11; compared with `cmp`). A search of the repository (ignore files disabled, files up to 50 MB, `.git` excluded) for `theorem chain_clauses_sound` finds only LL and these eight; the repository holds 219 archives, so "uncompressed" is the right qualifier. Same-short-name declarations elsewhere: PhaseClassification.lean (polar, orient_polar, orient_polar_centre_inside, sin_add_lt, orient_polar_halfplane; namespace PhaseClassification), OrbitConsistency.lean in LEANEXT/orbit and ENCBLEAN/geo (rotAbout_iterate, polar; ErdosSzekeres.OrbitConsistency), ES8SYM/lean/PolarOrient.lean (orient_polar; C7), SYMLEAN/review/ReviewSanity.lean (orient_rotAbout; ErdosSzekeres.SymReduction.Review): exactly the four namespaces named. pc.tex:123 and :141 treat the PhaseClassification declarations. OK |
| T | map rows rotfacts, regular, cramer, trans, fan-step, halfplane, chain | notes only | Labels, kinds, Lean names and file:line unchanged; notes agree with the text. Generator constraints (`tools/make_appendix.py`): header correct, 31 rows × 5 fields, ASCII only, every label token in the notes resolves (36 distinct, all defined), 31 rows = 31 non-remark statement environments. OK |

Note on row T: the chain note "(that the encoders emit these clauses is not in Lean)" is consistent with the text,
since "the encoders" are the project's generator programs (README "Code to clauses"); the ENCBLEAN route of l. 95-97
concerns a Lean definition of the formula, not the programs. No change needed.

## 2. Statements whose environment text changed (re-compared with Lean)

lg:lem:halfplane-convex (LL:516; title), lg:lem:disk (LL:1002; lead parenthetical removed), lg:lem:fan-step (LL:641;
parenthetical on c), lg:thm:fan (LL:700; title), lg:thm:chain (LL:914; title and item labels). For each: hypotheses,
conclusion, quantifier/binder order, `K - 1` (truncated subtraction, with K ≥ 4 in the statement), Finset vs Set and
maps-into are unchanged and exact. No statement was strengthened or weakened.

## 3. The fixer's findings table

Fixed, and confirmed fixed correctly:
- #1 (fidelity m1): eight copies listed and verified (row 23).
- #2 (fidelity m2): Coverage l. 891 and map note say where trig_layer is stated; keeping one `\leanref` per head is right.
- #3 (fidelity m3): overview and fan title no longer say "is a convex (n+1)-gon"; the proof remark still says so
  correctly (it is shown by the proof).
- #4 (fidelity m4): (C1)-(C4), all uses updated.
- #5 (fidelity m5): attribution corrected and the 59/66/7 counts verified (row 4).
- #7 (rigor m2): Rigor paragraph and the notes in the proofs (row 5).
- #8 (rigor m3): half-plane title and the a = b sentence (row 14).
- #9 (rigor m4): (S1)/(S2) with reference and existing Mathlib names; segment fact proved in place (rows 9, 16).
- #10 (rigor m5): parenthetical in fan-step.
- #13 (adversarial F3): "heads a statement" plus the sentence on the recalled declarations (row 2).
- #14 (adversarial F4): main-library list complete (grep of LL 465-1032), plus the HasConvexNGon.mono sentence.
- #20 (claims M5): overview and title no longer claim clause soundness; *Encoders* paragraph added.
- #22 (claims M7): display split; number beside it.

Duplicates, accepted (each points to a primary fix verified above; the extra parts are handled): #6, #11, #16 (= #5);
#12 (= #1); #15 (= #7; rotfacts sentence covers crot_comp); #17 (= #14; orient_cycle listed, HasConvexNGon.mono
sentence added); #18 (= #1; other-namespace item added and checked, row 23); #19 (= #7; notes at trans, fan_step,
orient_polar added); #23 (= #2).

Declined, accepted: #21 (claims M6, map rows for the 8 remarks). The remarks are unlabelled, a map row needs a label,
and the generated appendix says "Labelled remarks appear where a section lists them" (`tools/make_appendix.py`), so
listing remarks is optional. Not an inaccuracy. (Nine of the eleven sections do list theirs; consistency only.)

The writer concerns are all answered in the log (preamble `\es@sloppy`; `\texttt` for multi-word Lean text; axioms;
the two Lean-different steps; (L1)-(L4) re-checked against ll.tex; no overfull boxes).

## 4. Findings

**m1 (minor, rigor vocabulary). lg.tex:96-97, paragraph *Encoders*.**
- Text: "on that route, that the texts printed from this definition are the certified files is trust item (E1)".
- The word "certified" is new in this round; the passed snapshot contained neither "verified" nor "certified", and
  the vocabulary rule forbids both.
- It raises the label of no statement of this section and echoes the k = 8 note's own wording of (E1)
  (k8_soundness.tex:993, "the certified cube files"), so it does not misstate the records. But on the ENCBLEAN route
  the cake_lpr verdicts on those files are themselves trust item (E2), so the adjective presents a trusted status as
  settled.
- Fix: use the wording of the layer-lemma section (ll.tex:735), e.g. "that the texts printed from this definition
  are the cube files that carry the cake_lpr verdicts is trust item (E1)".

**m2 (minor, imprecision). lg.tex:4-6, overview lead sentence.**
- Text: "In the main statements, S is a finite set of points that is mapped into itself by the counterclockwise
  rotation ρ by 2π/m (m ≥ 1) about a point c".
- This replaced "Throughout" to make the sentence exact, but it is still not exact for Theorem lg:thm:fan
  (hasConvexNGon_of_fan, an export statement): its S has no centre, rotation or invariance hypothesis.
- No Lean statement is misstated: the fan bullet (l. 20-22) gives the fan hypotheses correctly.
- Fix: "In the statements about the layers, S is ..." (or "In the statements that involve a rotation, ...").

## 5. Compile check

Wrapper `build/lg_p1diff_wrapper.tex` (the contract's wrapper with `\input{../sections/lg}`), two runs of
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error lg_p1diff_wrapper.tex` from `build/`:
- exit status 0 and 0; no line starting with "!"; no "Missing", "Error" or "Emergency"; 12 pages;
- overfull boxes: none (so none > 1pt); underfull: one page-level `\vbox` on page 1 (output routine, page breaking of
  the standalone build), not a box overflow;
- undefined references only to allowed export labels: fd:def:cp, fd:def:gp, fd:def:inv, fd:def:ngon, fd:def:orient,
  fd:def:point, fd:def:rot, fd:lem:collinear, fd:lem:mono, fd:lem:orient, fd:lem:pos-triples, ll:def:hv, ll:def:peel,
  ll:lem:antitone, ll:lem:hv, ll:lem:inv-peel, ll:lem:minperiod, ll:thm:card-peel, ll:thm:core-rot; no undefined
  `lg:` reference, no multiply defined label, no other warning.
- The section defines no macro, loads no package, and has no `\sloppy`.

Hygiene: no machine path and no tool name in `lg.tex` or `lg.map.tsv`. "proved" occurs only for the written proofs of
this document (l. 78, 90, 774, 839; map rows nesting and halfplane, "proved here"); "verified" does not occur;
"certified" occurs once (m1).

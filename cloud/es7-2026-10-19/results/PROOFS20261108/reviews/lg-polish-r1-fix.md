# lg, polish round 1: fix log

Files: `sections/lg.tex` (940 lines after the fix) and `sections/lg.map.tsv` (31 rows, unchanged set of rows).
Snapshot before editing: `snapshots/polish-r1-pre/lg.tex`, `snapshots/polish-r1-pre/lg.map.tsv`.
Paths below are relative to STAGE (`sections/`, `reviews/`, `build/`), to RES (`LAYERLEAN/...`, `LEANEXT/...`) or to
the repository root (`ErdosSzekeres/...`). Line numbers refer to `sections/lg.tex` after the fix.

Inputs read: `reviews/lg-r1-fidelity.md`, `reviews/lg-r1-rigor.md`, `reviews/lg-r1-adversarial.md`,
`reviews/lg-r1-claims.md` (one round, no blocker or major finding) and `reviews/lg-writer-concerns.md`.
Lean sources re-read for every statement touched: `LAYERLEAN/LayerLemma.lean` (lines 1-460 for the definitions and
helpers, 465-1032 for the scope, 1037 for `card_peel`). Records re-read: `LAYERLEAN/README.md`,
`LAYERLEAN/logs/build.log`, `LAYERLEAN/logs/axioms.log`, `LAYERLEAN/logs/axioms_recheck_20261106/{README.txt,out.txt,run.sh}`,
`LEANEXT/review/REPORT.md`, `LEANEXT/review/axioms.log`, `WRITEUP/note/k8_soundness.tex` (trust table and gaps
(G1)-(G4)), `ErdosSzekeres/{Definitions,Orientation,OrientationGeometry,Basic}.lean`,
`ErdosSzekeres/Suk/OrientationClique.lean`, and the Mathlib sources at the pinned revision `f897ebcf72` (for the
names `Real.sin_pos_of_pos_of_lt_pi`, `Real.cos_le_one`, `Real.cos_eq_one_iff`).

## Findings

| # | Report and id | Summary | Action | Location after the fix | Reason (declined) / note |
|---|---|---|---|---|---|
| 1 | lg-r1-fidelity.md m1 | Coverage list of verbatim copies incomplete (4 more files) | fixed | Coverage, second item, l. 924-934 | All eight files listed (diffed lines 11-1147 against each: identical; start lines 19/19/11/11/11/11/19/11). Instead of "exactly", the text says that a search of the uncompressed files finds no further copy (the repository holds archives that grep cannot search). |
| 2 | lg-r1-fidelity.md m2 | Contract pairs `lg:lem:regular` with "(with trig_layer)"; trig_layer is a separate lemma | fixed | Coverage l. 891; map row `lg:lem:regular` | Coverage now says trig_layer is Lemma lg:lem:trig, stated just before Lemma lg:lem:regular, whose proof uses it; same in the map note. The head of lg:lem:regular is unchanged: a second `\leanref` would make the head claim a statement (trig_layer) that the environment does not state. |
| 3 | lg-r1-fidelity.md m3 | Overview credits the fan theorem with "is a convex (n+1)-gon" | fixed | Overview l. 20-22; head of Theorem lg:thm:fan l. 668 | Overview: "gives n+1 points in convex position (Theorem; by its proof, the pivot and the chain points themselves)". Title "a fan chain is a convex polygon" changed to "fan chains give convex polygons" for the same reason. |
| 4 | lg-r1-fidelity.md m4 | Item labels (i)-(iv) clash with the layer index i | fixed | Theorem lg:thm:chain l. 761-764, proof l. 770-776 | Renamed (C1)-(C4); all uses in the proof updated. |
| 5 | lg-r1-fidelity.md m5 | "non-simp" attributed to REPORT.md, which does not say it | fixed | Axioms, l. 62-67 | Now: the review log covers 59 declarations, all `theorem` declarations of the file except the 7 marked `@[simp]`; the file has 66 in all; REPORT.md speaks of "all 59 theorem declarations". Re-verified: 66 theorems, 7 `@[simp]`, logged names = the 59 others (grep set difference). |
| 6 | lg-r1-rigor.md m1 | Same as #5 | duplicate of fidelity m5 | Axioms, l. 62-67 | |
| 7 | lg-r1-rigor.md m2 | "They follow the Lean proofs, except where a remark says otherwise" and "written steps collect facts that the Lean proofs establish inline" are inaccurate (Cramer identity, rho^m = id) | fixed | Rigor l. 71-84; Coverage l. 917-919; notes in proofs l. 577, 609, 687, 776, 816; map notes | Rigor now says: proofs follow the structure of the Lean proofs; identities/inequalities that Lean closes by an automatic tactic (ring, linear_combination, nlinarith, positivity) are derived by hand; every other difference is stated in a remark or parenthetical. It says per written step how it relates to Lean (layer: opening steps of three named proofs; rotfacts: obtained in Lean through the complex form, direct computation or minimal periods; cramer: Lean checks only the three instances, each by ring; period: restates rot-iter and adds rho^m = id, replacing a minimal-period argument of the proof of lin_pos_of_peel). Parentheticals added where the written proof differs and nothing said so: trans and fan_step (Lean checks the key identity by ring, without the Cramer lemma), orient_polar (Lean expands by the subtraction formula, ring), fan Step 2 (Lean's case analysis with orient_cycle), chain (Lean unfolds HasConvexNGon instead of fd:lem:mono(c)). |
| 8 | lg-r1-rigor.md m3 | Title "closed half-planes are convex" too strong when a = b | fixed | Head l. 402; sentence after the proof l. 411-412; overview l. 13-14 | Title now "{orient(a,b,.) >= 0} is convex"; after the proof: for a != b the closed half-plane left of a->b with the line, for a = b the whole plane (by (O3)). The analogous case in Lemma lg:lem:disk (R < 0 gives the empty set) is handled the same way (see other changes). |
| 9 | lg-r1-rigor.md m4 | Standard facts (cos = 1 only on 2piZ; sin > 0 on (0,pi), >= 0 on [0,pi]; hull of two points is the segment) used without a reference | fixed | New paragraph "Sine and cosine" l. 152-159; uses tagged (S1)/(S2) at l. 329, 335, 377, 397, 831, 846, 868; Remark after Theorem lg:thm:nesting l. 472-476 | (S1), (S2) stated precisely with a textbook pointer (Rudin, Principles of Mathematical Analysis, 3rd ed., Chapter 8, same reference style as section fd) and the Mathlib names (checked to exist at the pinned Mathlib revision). The segment fact is now proved in place: the segment is convex and contains {x, rho(x)}, so it contains the hull (convexHull_min). |
| 10 | lg-r1-rigor.md m5 | Letter c is a generic point in Lemma lg:lem:fan-step without the warning given in lg:lem:trans | fixed | Lemma lg:lem:fan-step l. 585 | Parenthetical "(here c is an arbitrary point, not a centre)" added. |
| 11 | lg-r1-adversarial.md F1 | Same as #5 | duplicate of fidelity m5 | Axioms, l. 62-67 | |
| 12 | lg-r1-adversarial.md F2 | Same as #1 | duplicate of fidelity m1 | Coverage l. 924-934 | |
| 13 | lg-r1-adversarial.md F3 | "Every Lean declaration stated in this section ... lines 465-1032" is too broad (recalled results lie outside) | fixed | Sources l. 32-37 | Now "Every Lean declaration that heads a statement of this section ..."; added that the declarations recalled in the notation subsection lie outside these lines and are restated in the section on the layer lemma. |
| 14 | lg-r1-adversarial.md F4 | Main-library list omits orient_cycle | fixed | Sources list l. 38-47, sentence l. 48-49 | The list is now explicitly "declarations of the main library that the Lean proofs use" and is complete for lines 465-1032 (grep): Point, GeneralPosition, ConvexPosition, HasConvexNGon; orient (Orientation.lean:9) and orient_cycle (:15); generalPosition_iff_orient_ne_zero; Suk.convexPosition_of_positive_triples. Added: the written proofs also use fd:lem:mono(c) (HasConvexNGon.mono, ErdosSzekeres/Basic.lean:20), which the Lean proofs do not use (checked: no `.mono` in the scope). |
| 15 | lg-r1-adversarial.md F5 | Written steps do not all "collect facts that the Lean proofs establish inline" (Cramer; rotfacts(b) is crot_comp via the complex form) | duplicate of rigor m2 | Rigor l. 78-84 | The rotfacts sentence covers the crot_comp point (complex form). |
| 16 | lg-r1-claims.md M1 | Same as #5 | duplicate of fidelity m5 | Axioms, l. 62-67 | |
| 17 | lg-r1-claims.md M2 | Source list omits orient_cycle and HasConvexNGon.mono | duplicate of adversarial F4 | Sources l. 38-49 | Both parts handled (orient_cycle in the list; HasConvexNGon.mono in the sentence after it). |
| 18 | lg-r1-claims.md M3 | Coverage copies not exhaustive; PhaseClassification has same-named copies of the polar statements | duplicate of fidelity m1 | Coverage l. 924-938 | Extra part handled: new item on declarations in other namespaces sharing a short name (ErdosSzekeres.OrbitConsistency, PhaseClassification, C7, ErdosSzekeres.SymReduction.Review; found by grep over the checkout); those of PhaseClassification.lean are treated in the section on phase patterns (checked in `sections/pc.tex`). |
| 19 | lg-r1-claims.md M4 | Wording about how the proofs relate to Lean is looser than the content; unmarked deviations at trans, fan_step, orient_polar | duplicate of rigor m2 | Rigor l. 71-84; l. 577, 609, 816 | Extra part handled: notes added at the three named proofs. |
| 20 | lg-r1-claims.md M5 | Overview "hence the chain clauses are sound" overclaims (code-to-clause not in Lean) | fixed | Overview l. 23-27; new paragraph "Encoders" l. 86-97; head of Theorem lg:thm:chain l. 755; remark l. 779-786 | Overview now states the geometric content and points to "Encoders". Title "soundness of the chain clauses" changed to "geometric chain soundness" (the wording of the trust table of WRITEUP/note/k8_soundness.tex). |
| 21 | lg-r1-claims.md M6 | Map has no rows for the 8 (unlabelled) remarks | declined | - | The binding map rule for this stage is one row per non-remark statement environment (rows for labelled remarks may stay); lg's remarks are unlabelled, and adding labels only to add rows would not make the text clearer. |
| 22 | lg-r1-claims.md M7 | Display (lg:eq:J) too wide; its number sits on its own line | fixed | l. 116-121 | Split into two lines with `gathered` inside the numbered equation; the number is now set beside the display. |
| 23 | lg-r1-claims.md M8 | Same as #2 | duplicate of fidelity m2 | Coverage l. 891 | |

Writer concerns (`reviews/lg-writer-concerns.md`): (1) the head-breaking problem is resolved by the preamble update
(`\es@sloppy`); I rebuilt, and every head retitled in this round (lg:lem:halfplane-convex, lg:thm:fan, lg:thm:chain)
was tried in several wordings until the head broke without any box warning (two intermediate wordings produced an
overfull box of 1.2pt and an underfull head, both removed); the section had no `\sloppy` to remove. (2) `\lean` drops
spaces: multi-word Lean expressions stay in `\texttt`, no change. (3) Axioms evidence: consistent with the logs; the
"non-simp" attribution is fixed (#5). (4) The two proof steps that differ from Lean keep their remarks. (5) (L1)-(L4)
re-checked against the current `sections/ll.tex`; (L1) now cites part (c) of ll:lem:hv. (6) Overfull boxes in the full
build: none before, none after (see below).

## Other changes (inaccuracies found while re-checking, and consequential edits)

1. Overview (l. 3-30): "Throughout" replaced by "In the main statements ... (m >= 1)"; each bullet now carries the
   hypotheses that the summarised result needs and the old text omitted: m >= 2 and general position for strict
   nesting; m >= 2 even (the old "for even m" was false for m = 0, which is even) for the centre; m >= 3 and general
   position for the tangent lemma; K >= 4 for the chain theorem. The radius bullet now says "the points of a layer and
   of all later layers" (the theorem has n <= n').
2. Sources (l. 51-57): build.log names no file hash; added that REPORT.md (4 November 2026) reports the same build
   result for the reviewed file (SHA-256 prefix afb8542d, 1148 lines) and that the 6 November re-check compiled
   `LAYERLEAN/logs/axioms_recheck_20261106/LayerLemmaAxioms.lean`, whose first 1148 lines are this file (verified
   here: head -n 1148 equals LayerLemma.lean, hash afb8542dceb0...; 19 `#print axioms` lines follow; exit status 0).
3. Axioms (l. 66-67): "In both logs every one of these theorems depends only on ..." could be read as both logs
   printing all 23; now "In each of the two logs, every theorem of this section that it prints ...".
4. New paragraph "Encoders" (l. 86-97), referenced from Remark (3) after Theorem lg:thm:nesting (l. 480-482), the remark
   after Theorem lg:thm:chain (l. 779-786) and the remark after Lemma lg:lem:ruleB (l. 874-882). The old remarks said the
   code-to-clause step "is not part of the Lean development", which could be read as "no Lean code covers it", while
   WRITEUP/note/k8_soundness.tex records a Lean-checked second route for encoder B at m = 6 (ENCBLEAN). The paragraph
   now says: these steps are not part of LAYERLEAN/LayerLemma.lean; LAYERLEAN/README.md lists them under "What is not in
   Lean" with the status "written proof, review and tests"; for the k = 8 encoders the code-to-clause step is gap (G1)
   of the k = 8 soundness note (written proof, not refereed, by reading the code), with the ENCBLEAN route for
   encoder B at m = 6 on which the link from the Lean definition to the certified files is trust item (E1), evidence
   from compiled code and not a Lean theorem. The chain remark adds REPORT.md finding F5 (least-fixpoint values of
   auxiliary chain variables); the rule B remark adds REPORT.md finding F2 (no Lean lemma puts the layers in polar form).
5. Rotations paragraph (l. 141-144): "every statement of this section assumes m >= 1" was false for statements without
   m (e.g. rotAbout_iterate); now "every statement ... in which 2pi/m occurs".
6. Lemma lg:lem:rot-iter, parenthetical (l. 253-256): gamma is now defined (gamma = c_0 + i c_1), the Lean lemmas are
   named with lines (rotAbout_eq_crot, line 302; crot_iterate, line 267), and the vague "the two arguments are
   equivalent" is replaced by the actual Lean route.
7. Lemma lg:lem:trig, parenthetical (l. 305-307): states exactly what Lean rewrites with (cos 2x = 2cos^2 x - 1,
   sin 2x = 2 sin x cos x for x = s, t, sin_sub) and that linear_combination closes it with sin^2 + cos^2 = 1; the old
   "the identity is the same" was vague.
8. Lemma lg:lem:disk (l. 419-434): the lead "(Closed disks are convex.)" inside the statement is removed (for R < 0 the
   set is empty); after the proof: for R >= 0 the closed disk of radius sqrt R, for R < 0 empty. Title "disks" kept
   (a longer title produced an underfull head).
9. Text after Lemma lg:lem:ruleA (l. 836-839): gaps named explicitly; "only the orientation statement is proved and
   used" (it is not used in this section) replaced by "that geometric fact is neither stated nor used here, and only
   the orientation statement is proved".
10. Remark after Lemma lg:lem:ruleB (l. 874-876): "which is what the weak radius order of Theorem lg:thm:radius
    provides" made precise: the theorem gives dist2(c,y) <= dist2(c,x), i.e. r_y <= r_x for r = sqrt(dist2(c,.)).
11. Coverage (l. 885-940): the scope is stated as all declarations of lines 465-1032 (verified: exactly these 27);
    rotAbout_iterate is noted as also restated in the section on the layer lemma (ll:lem:rot, which is not an export
    label, so no `\ref`); "which lie in the same line range of the file" (false for 460 and 1037 relative to the stated
    465-1032) replaced by "which adjoin these lines"; the written-steps sentence now points to the Rigor paragraph.
12. (L1) (l. 178) cites Lemma ll:lem:hv(c), the part that is subset_convexHull_hullVerts.
13. Map TSV notes updated (no row added, removed or reordered; labels, kinds, Lean names and file:line unchanged):
    lg:lem:rotfacts, lg:lem:regular, lg:lem:cramer, lg:lem:trans, lg:lem:fan-step, lg:lem:halfplane (now "via
    lg:cor:period (rotAbout_iterate and rotation by 2pi)" plus the ring note), lg:thm:chain (geometric statement only).

No statement was weakened or strengthened. Statement environments whose text changed: the heads of
lg:lem:halfplane-convex, lg:thm:fan and lg:thm:chain (titles only); the body of lg:lem:disk (lead parenthetical
removed); the body of lg:lem:fan-step (parenthetical on c); the item labels of lg:thm:chain ((i)-(iv) to (C1)-(C4)).
Each was re-compared with its Lean declaration (LayerLemma.lean:516, 1002, 641, 700, 914): hypotheses, conclusion,
binder order, natural-number subtraction (K - 1), Finset/Set and maps-into are unchanged. No proof was restructured.

## Compile check

Contract wrapper `build/lg_wrapper.tex`, two runs of `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error
lg_wrapper.tex` from `build/`: both exit 0, no errors, no "Missing". Undefined references only to fd:/ll: export labels
(fd:def:cp, gp, inv, ngon, orient, point, rot; fd:lem:collinear, mono, orient, pos-triples; ll:def:hv, ll:def:peel,
ll:lem:antitone, ll:lem:hv, ll:lem:inv-peel, ll:lem:minperiod, ll:thm:card-peel, ll:thm:core-rot). Overfull boxes:
0. Underfull: one page-level `\vbox` on page 1 of the standalone build (page breaking only; it does not occur in the
full build). 12 pages.

Full document (`proofs.tex`, three passes into the private directory `build/lg_polish/full`, nothing shared
overwritten): exit 0, 143 pages, 0 overfull boxes in the whole document, no box warning inside lg (the one underfull
`\hbox` reported just after `sections/lg.tex` is opened comes from the last paragraph of `sections/ll.tex`), no
undefined `lg:` reference.

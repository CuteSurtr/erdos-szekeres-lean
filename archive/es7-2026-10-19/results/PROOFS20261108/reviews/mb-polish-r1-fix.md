# Section `mb`, polish round 1: fix log

Inputs: `reviews/mb-r1-fidelity.md` (fid F1-F8), `reviews/mb-r1-rigor.md` (rig F1-F9), `reviews/mb-r1-adversarial.md`
(adv 1-9), `reviews/mb-r1-claims.md` (cl F1-F11), `reviews/mb-writer-concerns.md`. Snapshot before editing:
`snapshots/polish-r1-pre/mb.tex`, `snapshots/polish-r1-pre/mb.map.tsv`. Line numbers below refer to `sections/mb.tex`
after the fix (1196 lines). Paths of records are relative to the results directory, `ErdosSzekeres/...` and `docs/...`
to the repository root, RTC = `SYMLEAN/mirror/ReductionThreeClasses.lean`.

Every edited claim was re-checked against its source before editing:
- Lean: `ErdosSzekeres/Omission/{Realization,ActualRanks,PlanarChains,ListGeometry,BoundaryGeometry,BaekGeometry,Baek}.lean`
  (all declarations listed and their uses on the proof paths traced with grep), `ErdosSzekeres/Vendor/ETV/Config/Defs.lean`
  (`Cap3` at :30, `NCap` :51, `NCup` :54), `Main/CapCup.lean` (split by first entries of `(a+2)`-caps in the step to
  `(a+1, b+1)`), `Main/Main.lean` header, `Lib/List/{Defs,Lemmas}.lean`, `MIRRORETV/lean/MirrorMain.lean` (generated
  block 22-1506; the four lemmas with `cyc7`/`cyc8` end at line 991; products `pX_YZ`; `mirror_seven'`/`mirror_eight'`
  2631/2636; `mirror_odd_general` uses `cap_mirror_polygon`, `axis_left/right_polygon`), `MirrorNine_append.lean`, RTC
  (Part A theorem binders at 1023/1050/1503-1547, Part C 4237-4322, `#check` lines 4312-4316).
- Records: `SYMLEAN/mirror/axioms.out` (lines 17-20, 39-40), `docs/THIRD_PARTY.md` (lines 111-118 and the module tables),
  `MIRRORETV/README.md` §4, §8, §9, `MIRRORETV/PROOFS.md` (proof of Corollary 7.2, lines 362-367),
  `SYMLEAN/mirror/README.md` §4, `SYMLEAN/README.md` §5, §6, §9, `C2FINAL/README.md` (statement, status, §2, §9),
  `C2RECHECK/README.md` (§6 final totals), `C3FINAL/README.md`, `C3LEAN/README.md` (status, §4 lines 137-139, §6),
  `C3SPOT/README.md`, `SYM5/README.md` (§1 perturbation, §2), `MIRRORETV/review/MirrorA.lean:706` (`refl`).
- After the edits, all 78 `\leanref` pairs were re-checked by script: each cited line declares the named identifier;
  the map has 42 rows in the order and with the kinds of the 42 statement environments, and its Lean-name and
  file:line columns equal the `\leanref` pairs in order.

No statement changed its mathematical content. Two heads changed (Definition `mb:def:config` gained `Config.Cap3`;
Lemma `mb:lem:signs` lost `cup_false_iff`), Lemma `mb:lem:signs` now names `c.cup` explicitly, and Lemma
`mb:lem:boundary`(b) renames its bound variable. Each still matches its Lean declarations exactly.

## Findings

| report / id | summary | action | location after the fix | reason (if declined) |
|---|---|---|---|---|
| fidelity F1 | Remark capcup: classical split is by first entries of (a+1)-caps, not (a+2)-caps | fixed: "(a+1)-caps, that is, of caps one entry shorter than the target (a+2)-cap"; added "(target 5-cap, split by the first entries of 4-caps)" for the repeated step; "exactly this form" -> "this form" (the vendored proof is a pincer recursion) | Remark `mb:rem:capcup`, lines 220-224 | |
| fidelity F2 | `Realization.lean` listed as adapted from Schroeder's archive | fixed: listed separately as the project's own code (no adaptation header; `docs/THIRD_PARTY.md` says its connections were added in the project, using the archive's strategy); the six other files remain "adapted from that archive (MIT licence)" | Sources, lines 43-53 | |
| fidelity F3 | Remark baek(3): "every N-gon" cites a proposition stated only for m in {7,8,9} | fixed: "for N in {7,8,9} every N-gon of C_c with entries in [n] yields N of the points of c in convex position (Proposition gon; its proof does not use the value of N)"; also "C_c-caps and C_c-cups with entries in [n]" | Remark `mb:rem:baek`(3), lines 206-209 | |
| fidelity F4 | `Configuration.cup_false_iff` is not in the cone of any printed theorem, yet covered by "the bridge lemmas ... Lean-checked (axioms evidence above)" | fixed: `cup_false_iff` removed from the head of Lemma `mb:lem:signs` and from the map row (the second claim of the lemma is `cap_sign`, which is on the path); the proof now says that the Fin-index companion `cup_false_iff` (Realization.lean:44) is not used on the proof paths and not covered; it is listed under "not covered" in Coverage. The cone sentence now reads "Every other Lean declaration named in the head of a statement below is used by one of the printed theorems" (checked for all 78 head declarations) | Lemma `mb:lem:signs`, lines 266-285; axioms paragraph, lines 77-81; Coverage, line 1190; map row `mb:lem:signs` | |
| fidelity F5 | axioms.out: "its two `#check` outputs are truncated" is imprecise | fixed: "of the five `#check` commands of RTC (lines 4312-4316) only the two for the `_3` theorems have output in it (lines 17-20, the first one again at lines 39-40), truncated after the binders HalfTurn34 and Threefold33" | axioms paragraph, lines 72-75 | |
| fidelity F6 | "according to README §8 this is Theorem 2.7 in the arXiv numbering" not supported | fixed: Theorem `mb:thm:baek` is now described as the theorem `main` of the vendored file, adapted from Baek's own Lean code (header: changes only imports and Lean/Mathlib 4.24.0 compatibility); "README §8 states that Baek's Theorem 2.7 holds for all colourings with weak gons; we have not compared the wording of that theorem with Theorem `mb:thm:baek`". No identification of `main` with Theorem 2.7 remains | Remark `mb:rem:baek`(1), lines 189-199 | |
| fidelity F7 | Remark main3 omits the centre-perturbation lemma | fixed as part of the rewrite of the remark: "Threefold33 and Fivefold35 also rest on the written centre-perturbation lemma `C2ENC/perturbation.md`" (SYMLEAN/README.md §6, SYM5 §1) | Remark `mb:rem:main3`, lines 1103-1104 | |
| fidelity F8 | Coverage list of skipped bridge declarations reads as exhaustive | fixed: Coverage restructured as a list; the off-path item now names `cup_false_iff`, `hasCup_of_list`, `hasNCup_octagon`, `chain3_of_all`, `listCup_of_hasCup`, `listCap_of_hasCap`, `PlanarChains.cup_all` and "the declarations of Realization.lean and ActualRanks.lean not named in this section (they belong to the project's ErdosSzekeres/Omission development and are outside this section)"; checked by grep that none of these is used on the proof paths | Coverage, lines 1190-1194 | |
| rigor F1 | Realization.lean attribution | duplicate of fidelity F2 | Sources, lines 43-53 | |
| rigor F2 | `cup_false_iff` axioms coverage | duplicate of fidelity F4 | as fidelity F4 | |
| rigor F3 | Remark baek(3) claims more than Proposition gon states | duplicate of fidelity F3 | lines 206-209 | |
| rigor F4 | "for every N>=3" attributed to Theorem 1.6 without a repository source | fixed: the range is the one quoted in `MIRRORETV/PROOFS.md` (proof of Corollary 7.2: "For any n >= 3, ... C(n-1,2)+2 points ... 4-cap or a n-gon", general position including x-distinctness); the remark now cites that quotation | Remark `mb:rem:baek`(1), lines 190-193 | |
| rigor F5 | off-by-one in Remark capcup | duplicate of fidelity F1 | lines 220-224 | |
| rigor F6 | Remark generated: (a) is not a special case; products with the axis point omitted | fixed: "Statements (b), (c) and (d) are special cases of them (m=4), and (a) follows from (b) applied to P u {mir c_0} by deleting the point mir c_0"; products are now "products of a positive ordinate and a positive difference of abscissae, y(c_i)(x(q)-x(q'))>0 with q,q' two of the four given points and x(q')<x(q) (for example y(c_0)(x(c_0)-x(a)) in (c))"; "with hints found offline" added | Remark `mb:rem:generated`, lines 671-686 | |
| rigor F7 (n, c) | notation overload: n in the proof of Prop. cap16; c (configuration vs line offset) in the proof of Theorem nine(b),(c) | fixed: "Theorem `mb:thm:baek` with the value 4 for its parameter (called n there)"; in the paraphrase of `mirror_odd_general` the quantified configuration is now e of r points | Proof of `mb:prop:cap16`, line 504; proof of `mb:thm:nine`(b),(c), lines 965-966 | |
| rigor F7 (R) | R is the right end point, the upper part R(S) and the ternary relation of Lemma chain | declined | - | R in Lemma `mb:lem:chain` is the Lean binder of `chain3_all`/`OrderedTriples R l`, and each of the three uses is local to one statement and its proof, so a rename would touch many formulas without removing any ambiguity |
| rigor F8 | status line after Theorem classes lists only Baek | fixed: "the written proof rests, through Theorems refl32(b) and seven(b), on the cited Theorem baek and on Theorems mm:thm:mirror-polygon and mm:thm:axis-polygon"; the same dependency sentence was added to the status line of Theorem `mb:thm:refl32` | lines 1039-1041; lines 1004-1006 | |
| rigor F9 | duplicate coverage with section mm | fixed: new paragraph at the start of Subsection `mb:ssec:red`: the Lean declarations of that subsection and of Definition frame and Lemmas frame, affine, transport "are also stated (and, where they are lemmas, proved) in the section of Theorem mm:thm:odd; we repeat them here, with proofs, so that this section is self-contained" (checked against `mm.map.tsv`: mm:def:mir, mm:lem:count, mm:lem:injx, mm:def:config, mm:lem:sort, mm:prop:small-polygons, mm:def:frame, mm:lem:frame, mm:lem:ngon, mm:thm:line); Coverage repeats it | lines 536-539; Coverage, lines 1156-1158 | |
| adversarial 1 | Theorem 2.7 (4-cap, n-cup or (3,n-1)-gon) is stronger than `main`; the remark says `main` "is" Theorem 2.7 | duplicate of fidelity F6 (the remark no longer identifies `main` with Theorem 2.7 and says the wording was not compared; the paper itself could not be consulted with the allowed tools) | lines 193-199 | |
| adversarial 2 | off-by-one in Remark capcup | duplicate of fidelity F1 | lines 220-224 | |
| adversarial 3 | Realization.lean misattributed | duplicate of fidelity F2 | lines 43-53 | |
| adversarial 4 | `cup_false_iff` not covered by the axiom lines | duplicate of fidelity F4 | as fidelity F4 | |
| adversarial 5 | Remark baek(3) "every N-gon" | duplicate of fidelity F3 | lines 206-209 | |
| adversarial 6 | Remark generated: (a) not a special case | duplicate of rigor F6 | lines 671-686 | |
| adversarial 7 | (i) BoundaryGeometry helpers on the path neither named nor listed; (ii) Coverage lists `Config.Cap3` but the map row of `mb:def:config` omits it | fixed: (i) the "helpers absorbed" item of Coverage now lists `CupArc`, `first`, `last`, `reflect`, `reflect_reflect`, `orient_reflect`, `Boundary`, `Boundary.points`, `Boundary.flip`, `reflect_mem_flip`, `Boundary.finite`, `Boundary.finite_coe`, `affine`, `affine_mix`, `affine_positive_convex`, `supporting_edges_expose`, `point_x_bounds`, `first_x_strict`, `last_x_strict` (each checked to be used inside `BoundaryGeometry.lean` by a path lemma); (ii) `\leanref{Config.Cap3}{ErdosSzekeres/Vendor/ETV/Config/Defs.lean:30}` added to the head and to the map row | Coverage, lines 1178-1189; head of `mb:def:config`, line 123; map row `mb:def:config` | |
| adversarial 8 | notation overloads: "configuration" (abstract vs point configurations); c; n; v in Lemma boundary(b) | fixed: sentence added after the definition of point configurations ("A configuration of n points is not a configuration in the sense of Definition config; the link between the two notions is C_c"); Lemma boundary(b) now uses p (as Step 5 of the proof does); the c and n parts are the same as rigor F7 (n, c) | line 251-253; line 377; lines 504, 965-966 | |
| adversarial 9 | duplication with mm | duplicate of rigor F9 | lines 536-539, 1156-1158 | |
| claims F1 | Realization.lean attribution | duplicate of fidelity F2 | lines 43-53 | |
| claims F2 | `cup_false_iff` evidence | duplicate of fidelity F4 | as fidelity F4 | |
| claims F3 | description of axioms.out | duplicate of fidelity F5 | lines 72-75 | |
| claims F4 | Remark main3: "not retained" for Threefold33 should cite `C3LEAN/README.md` | fixed as part of the rewrite of the remark: "Its 116,883 piece records carry verdicts recorded at solve time (both proof checkers accepted the proof); the proofs were not kept (C3LEAN/README.md, §4), and 2,120 randomly chosen pieces were re-solved (C3SPOT)" | Remark `mb:rem:main3`, lines 1094-1099 | |
| claims F5 | Coverage not exhaustive: (a) path helpers absent; (b) off-path bridge list incomplete | duplicate of adversarial 7(i) for (a) and of fidelity F8 for (b); in addition (a) now lists `mir_zero`, `mir_one`, `xset_card`, `emb_mem`, `OrderedTriples`, `Config.NCap`, `Config.NCup`, `Config.DecidableCap3` and the list lemmas `List.takeHead`, `List.takeHead2`, `List.takeLast2`, `List.in_superset`, `List.cons_in` ("among them", so not claimed exhaustive) | Coverage, lines 1178-1194 | |
| claims F6 | duplication with mm unacknowledged | duplicate of rigor F9 | lines 536-539, 1156-1158 | |
| claims F7 | "the two parametrisations of line reflections used in the project" (the project also has `MirrorA.refl`) | fixed: "that occur in the Lean files of this section" | opening paragraph, line 17 | |
| claims F8 | Remark generated "special cases" | duplicate of rigor F6 | lines 671-686 | |
| claims F9 | Remark baek(3) scope | duplicate of fidelity F3 | lines 206-209 | |
| claims F10 | packaged statements: Lemma signs (Fin/Boolean forms) and Lemma boundary (change of variables) not marked | fixed: Lemma signs now states "c.cup(a,b,d)=true, that is Cup3_{C_c}(a,b,d)" and "c.cup(a,b,d) != true, that is Cap3_{C_c}(a,b,d)", for a,b,d in N with a,b,d<n (exactly `cup_sign`/`cap_sign`), and the proof explains that `cup_true_iff` is the same first claim with indices in Fin n and `c.point`; Remark boundary now says that the change of variables is a bijection between the data of the lemma and the values of type `Boundary s t`, that `Boundary.card` counts `Boundary.finite` = B, "so the lemma is the Lean statement in this encoding, not a variant of it" | Lemma `mb:lem:signs`, lines 270-284; Remark `mb:rem:boundary`, lines 392-394 | |
| claims F11 | `mirror_seven'`, `mirror_eight'` render with a typographic right quote | fixed in this section without a new macro: such names are typeset as `\texttt{...\textquotesingle}` (straight ASCII quote, same LMMono font; checked with pdftotext), with `\allowbreak` after `MirrorOdd.`; the same was done for `List.Chain3'` and the pseudo-code `l'.head?`, `l'.getLast?`. Section `mm` still uses `\lean{mirror_seven'}`; a preamble-level fix would cover the whole document | Remarks `mb:rem:seven`, `mb:rem:eight` (lines 848, 892), Remark `mb:rem:config` (lines 151, 153), Coverage (lines 1129, 1167) | |
| writer concerns (overfull boxes) | list of overfull boxes > 1pt in the full build: none | no overfull box before or after; re-checked: standalone wrapper 0, and a full-document copy built in `build/mb-polish-r1/full` (not in the shared `build/full`) 0 in the whole document | - | |
| writer concerns (other) | head typesetting with `\\` and `\raggedright`; Theorem 2.7 attribution unchecked; duplication with mm | the preamble now sets statements with high tolerance; the `\\` and `\raggedright` were left in place as instructed (they cause no problem; 0 overfull boxes); the Theorem 2.7 point is fidelity F6; the duplication is rigor F9 | - | |

Counts: 37 findings in the four reports (rigor F7 split into two rows because its parts got different actions), i.e.
38 rows: 19 fixed, 1 declined (rigor F7, part R), 18 duplicates.

Not counted as findings: rigor "points considered and not reported" suggests an optional two-line conceptual proof of
(mb:eq:chord). Declined: the expansion proof given is complete and checked symbolically; a second proof adds length,
not precision.

## Other changes (not tied to a single finding)

1. **Remark `mb:rem:main3` rewritten** (lines 1084-1114) so that it states every recorded trust gap of the three class
   hypotheses and does not round the label up ("computer-assisted certificate records" -> "computer-assisted claims,
   supplied by the following records"), as an itemized list:
   - HalfTurn34: claimed in C2FINAL; hull cover and 120 hexagonal hulls of C2C34 with retained proofs; most
     parallelogram pieces (C2P-C2P5) rest on verdicts recorded at solve time (both checkers accepted, proof then
     deleted), with re-solved samples and re-checks (C2FINAL status paragraph; C2RECHECK); encoder and the two
     reductions of the case split are written proofs.
   - Threefold33: C3FINAL; 116,883 piece records with verdicts recorded at solve time, proofs not kept (C3LEAN
     §4); 2,120 pieces re-solved (C3SPOT); C3LEAN Lean-checks only that the named leaves cover the 910 roots (that
     every leaf has such a record is checked outside Lean); normal form C3-S/soundness.md, encoding C3a,
     exhaustiveness of the splits and the reductions are written proofs. The records' own word "certified" is not
     used in the section, to keep the contract's rigor vocabulary.
   - Fivefold35: SYM5, two normal forms of one encoder, retained proofs accepted by both checkers; encoder and layer
     lemma are written proofs.
   - Both Threefold33 and Fivefold35 rest on the written perturbation lemma; for none of the three is the step from a
     certificate to the Lean proposition formal (the match was checked by reading, SYMLEAN/README.md §6 and §9).
   The last part (other affine variants and `halfTurn_of_symmetric_counterexample` still take five classes) is
   unchanged and was re-checked against RTC 1050 and 1503-1547.
2. **Remark `mb:rem:generated`**: the line range "22-1506" was imprecise for the four lemmas; now "lines 22-991,
   including the wrappers cyc7 and cyc8; the rest of the generated block, up to line 1506, contains the smaller mirror
   polygons used for k=4,5,6 and their wrappers" (checked: `axis_right_heptagon` ends at 991, line 993 starts the
   small-k block; the small polygons are used only by `mirror_four`/`five`/`six`).
3. **Remark `mb:rem:seven`**: "its only additional ingredient is the general mirror lemma" was imprecise; now: "in
   place of `mirror_seven_of` and the generated polygon lemmas it uses the general reduction `mirror_odd_general`,
   which rests on the general mirror lemma (Theorems mm:thm:mirror-polygon and mm:thm:axis-polygon)" (checked:
   `mirror_odd_general` calls `cap_mirror_polygon`, `axis_left_polygon`, `axis_right_polygon`). Remark `mb:rem:eight`
   reworded to the same sentence pattern (removes an underfull line; content unchanged).
4. **Coverage** (lines 1125-1196) restructured as a list. Besides the items above: "Part B of RTC is a verbatim copy
   of MirrorMain.lean" -> "is MirrorMain.lean verbatim after its two import lines" (RTC header and lines 1561-1562);
   the wrappers `cyc4`-`cyc6` were wrongly grouped with the derivation of the four polygon lemmas (they serve the small
   polygons); new entries for `Configuration`, `Configuration.HasCap` (Subsection bridge, Definition mm:def:config),
   `List.Chain3'`, `List.In` (Remark config), and `hasCap3_of`, `capacity_cup` (subject of mm); "generated certificate
   proofs" -> "generated Lean proofs" (no confusion with SAT certificates).
5. **Opening paragraph**: "proved here in full (written proofs, not refereed)"; "as their only hypotheses" ->
   "as their only case-class hypotheses"; "conditional on these three unproved statements" -> "conditional on these
   three statements; they are not proved in Lean or in this document, see Remark main3". **Dependencies and rigour**:
   "three unproved propositions" -> "three propositions that are not proved in Lean or in this document" (they are
   computer-assisted claims in the project, so "unproved" alone could mislead).
6. **Sources**: the path convention now covers `docs/...` (repository root) and the record directories of Remark
   main3 (results directory).
7. **Conventions**: x(p), y(p) are used for all points, not only for indexed ones (wording fixed);
   orient(a,b,a) = orient(a,b,b) = 0 are attributed to the formula of Definition fd:def:orient (they are not items of
   Lemma fd:lem:orient).
8. **Map TSV** (42 rows, 5 columns, ASCII): `mb:def:config` gains `Config.Cap3` (`Defs.lean:30`); `mb:lem:signs` loses
   `cup_false_iff` (`Realization.lean:44`) and its note explains the Fin/natural-number forms; `mb:prop:gon` note
   "identical proofs" -> "proofs identical up to the value of m"; `mb:lem:polygons` note "generated certificates" ->
   "generated code (linarith with hints found offline)"; `mb:thm:main3` note now says "not proved in Lean;
   computer-assisted claims ... resting also on written encoder-soundness and perturbation proofs and in part on
   verdicts recorded at solve time; see mb:rem:main3".

## Compile check

`build/mb_wrapper.tex` (inputs `../preamble` and `../sections/mb`), `nice -n 15 pdflatex -interaction=nonstopmode
-halt-on-error mb_wrapper.tex`, run twice from `build/`:
- both passes exit 0; 16 pages; no `!` error, no "Missing", no multiply defined label;
- overfull boxes > 1pt: 0 (also 0 before the fix); 3 underfull boxes (cosmetic: one paragraph of long Lean names and
  two page-break vboxes);
- undefined references only to allowed labels of other sections: `fd:def:{cp,gp,inv,ngon,orient,point}`,
  `fd:lem:{affine-cp,affine-orient,collinear,cp-hull,mono,orient,pos-cycle,separation}`, `mm:def:config`,
  `mm:thm:{axis-polygon,even,line,mirror-polygon,odd,small}`, `sr:def:{classes,iso}`, `sr:thm:main`, `ar:thm:main`;
- the seven export labels `mb:thm:{baek,seven,eight,nine,refl32,classes,main3}` are defined on the required
  statements; no `\newcommand`, `\usepackage`, machine path or tool name in `mb.tex` or `mb.map.tsv`.

Full-document copy (`build/mb-polish-r1/full/fullcheck.tex`, the same inputs as `proofs.tex`, three passes, all exit 0):
0 overfull boxes in the whole document, 0 undefined references, no multiply defined labels.

## Notes for the integrator

- Section `mm` renders `mirror_seven'` and `mirror_eight'` through `\lean{...}`, which prints a typographic right quote
  in T1 typewriter. A preamble-level fix (for example a straight quote in `\lean`) would settle this for all sections;
  `mb` now uses `\texttt{...\textquotesingle}` for its four primed names.

# Section mb, polish round 1: diff audit (lens: diff)

**Verdict: pass.** There are no blocker or major findings. There are three minor findings (m1–m3). m1 is a
one-character slip in the map, introduced in this round, that would garble one row of the generated appendix. It
should be fixed before the appendix is regenerated.

**Inputs.**
- The passed version: `snapshots/sections-r1pass/mb.tex` and `mb.map.tsv`.
- The current version: `sections/mb.tex` (1,196 lines) and `sections/mb.map.tsv` (42 rows).
- The fix log `reviews/mb-polish-r1-fix.md`, the four round-1 reports `reviews/mb-r1-{fidelity,rigor,adversarial,claims}.md`,
  and `reviews/mb-writer-concerns.md`.
- No earlier polish audit (`mb-p*-diff.md`, `mb-p*-referee.md`) exists.

**Path conventions in this report.** Paths are relative to STAGE (`sections/`, `build/`, `reviews/`, `tools/`), to RES
(`MIRRORETV/...`, `SYMLEAN/...`, `C2FINAL/...`, ...) or to the repository root (`ErdosSzekeres/...`, `docs/...`).
`mb.tex:N` refers to the current file. RTC is `SYMLEAN/mirror/ReductionThreeClasses.lean`.

## 1. Scope of the diff

- `snapshots/polish-r1-pre/mb.tex` and `mb.map.tsv` (the fixer's pre-edit snapshot) have the same SHA-1 as the passed
  snapshot. Every hunk is therefore the work of this round.
- `diff -u` gives 24 hunks in `mb.tex` (1,113 → 1,196 lines) and 4 in `mb.map.tsv`. Table §2 splits them by topic
  into items H1–H26 and T1–T3.
- The diffs are saved as `build/mb_p1diff_tex.diff` and `build/mb_p1diff_tsv.diff`.
- Statement environments changed in three places:
  - the head of Definition `mb:def:config` gained `Config.Cap3`;
  - Lemma `mb:lem:signs` lost `cup_false_iff` from its head, and its statement now names `c.cup` explicitly;
  - Lemma `mb:lem:boundary`(b) renames its bound variable.
- Each of the three was re-read against Lean (H8, H13, H14 below). No other statement head or body changed.

## 2. Hunk-by-hunk check

| # | where (current) | change | check | result |
|---|---|---|---|---|
| H1 | mb.tex:10–22 | opening: "(written proofs, not refereed)"; "parametrisations ... that occur in the Lean files of this section"; "only case-class hypotheses"; "not proved in Lean or in this document" | the only definitions of reflections parametrised by a line in the section's files are `reflLine` (RTC:449) and `lineRefl` (MirrorMain.lean:1879, RTC:3438); `mir` and `BoundaryGeometry.reflect` are the one fixed x-axis reflection, and `isometry_complex_cases` (RTC:347) is a classification lemma, not a definition; `heptagon_of_nontrivial_isometry_3`/`_affineEquiv_3` take h2, h3, h5 plus S, g and the geometric premises (RTC:4292–4309) | correct; labels not rounded up |
| H2 | mb.tex:25–28 | path convention: `ErdosSzekeres/`, `docs/` relative to the repository root, everything else relative to RES | every full path in the file resolves under the stated base (script loop over all `\dirn`); the bare short names do not, see m2 | correct, minor m2 |
| H3 | mb.tex:43–53 | `Realization.lean` listed as the project's own code; six files "adapted from that archive (MIT licence)" | `Realization.lean` line 1 is `import ...` (no header); ActualRanks, PlanarChains, ListGeometry, BoundaryGeometry, BaekGeometry and Baek each begin "Adapted from Michael Schroeder ... MIT"; `docs/THIRD_PARTY.md:111–118`: "`Realization.lean` connects attained paths ... These connections ... were added here, using the archive's balanced-state/cycle strategy" | correct |
| H4 | mb.tex:72–75 | description of `SYMLEAN/mirror/axioms.out` | RTC:4312–4316 are the five `#check` commands; axioms.out lines 17–18 and 19–20 hold the truncated `#check` output of `heptagon_of_nontrivial_isometry_3` and `_affineEquiv_3`, cut after `HalfTurn34 →` and `Threefold33 →`; lines 39–40 repeat the first; SHA-256 prefix ab92257c6f17 | correct |
| H5 | mb.tex:77–81 | "Every other Lean declaration named in the head of a statement below is used by one of the printed theorems" | traced by grep for all 78 head declarations, for example: `hasNCap_supset` → `Config.cap_cup` (CapCup.lean:100) and `config_capacity113` (MirrorNine_append.lean:61); `hasNGon_supset` → `config_capacity113` (:54); `four_point_identity_*` → `positive_four`/`negative_four` → `cup_list_all`/`cap_list_all` → `cupArc`/`capArc`/`hasCap_of_list` → `capacity16` → `mirror_seven`; `Boundary.card`, `boundary_convex_position` → `boundary_polygon` (BoundaryGeometry.lean:406–411) → `hasNGon_*`; `cap_mirror_octagon` → `mirror_eight` (MirrorMain.lean:1839); frame lemmas, `hasConvexNGon_affineMap` → `transport` (1928–1958) → `mirror_*_line`; `reflLine` → `reflLine_eq_lineRefl`; `cup_true_iff` → `cup_sign` (ListGeometry.lean:22). With `cup_false_iff` gone from the heads, the claim holds | correct |
| H6 | mb.tex:104 | "takes as hypotheses three propositions that are not proved in Lean or in this document" | consistent with Theorem `mb:thm:main3` and Remark `mb:rem:main3` | correct |
| H7 | mb.tex:107–116 | conventions: x(p), y(p) for all points; orient(a,b,a) = orient(a,b,b) = 0 from the formula of `fd:def:orient` | elementary; the other three identities are items (a), (b), (d) of `fd:lem:orient` | correct |
| H8 | mb.tex:123, 133; map row 1 | `\leanref{Config.Cap3}{...Defs.lean:30}`; the "line 30" in the text is dropped | Defs.lean:30 is `def Cap3 (a b c : α) : Prop := ¬C.Cup3 a b c`, which is exactly the definition's sentence | exact |
| H9 | mb.tex:151–153 | `List.Chain3'`, `l'.head?`, `l'.getLast?` set with `\textquotesingle` | Lib/List/Defs.lean:46 `def Chain3'` inside `namespace List` (line 31); `pdftotext` shows the ASCII quote | correct |
| H10 | mb.tex:190–199 | Remark `mb:rem:baek`(1): Theorem 1.6 "quoted in MIRRORETV/PROOFS.md, proof of Corollary 7.2"; `main` "adapted from Baek's own Lean code (according to its header ...)"; README §8 on Theorem 2.7 with "we have not compared the wording" | PROOFS.md:365–367 quotes Theorem 1.6 of arXiv v2 verbatim ("For any n ≥ 3 ... C(n−1,2)+2 points ... either a 4-cap or a n-gon"; general position including x-distinctness); Main.lean header: "Adapted from Jineon Baek's erdos-tuza-valtr proof code ... Changes: local imports and compatibility with Lean/Mathlib v4.24.0"; MIRRORETV/README.md §8 (lines 197–227), at 225–226: "Baek's Theorem 2.7 holds for all colourings with weak gons". `main` is no longer identified with Theorem 2.7 | supported |
| H11 | mb.tex:206–209 | Remark `mb:rem:baek`(3) restricted to entries in [n] and N ∈ {7,8,9}; "its proof does not use the value of N" | matches Lemma `mb:lem:lists` (entries < n) and Proposition `mb:prop:gon` (m ∈ {7,8,9}); the proof of `mb:prop:gon` never uses m | correct |
| H12 | mb.tex:220–224 | Remark `mb:rem:capcup`: split by first entries of (a+1)-caps, "one entry shorter than the target (a+2)-cap"; "(target 5-cap, split by the first entries of 4-caps)" | the classical step for an (a+2)-cap/(b+2)-cup target splits by (a+1)-caps. CapCup.lean:55–68: in the step to (a+1, b+1) (target (a+3)-cap) `is_start_of_cap` uses `c.length = a + 2`, one shorter, consistent with the remark. The vendored proof is a pincer recursion (line 49), hence "of this form", not "exactly". `config_capacity113` (MirrorNine_append.lean:26–28): T = first entries of 4-caps, target no 5-cap | correct |
| H13 | mb.tex:251–253 | sentence distinguishing point configurations from Definition `mb:def:config` | the link is `colorConfig c.cup true` (ActualRanks.lean:28) | correct |
| H14 | mb.tex:266–285; map row | Lemma `mb:lem:signs`: head without `cup_false_iff`; statement "a,b,d ∈ ℕ with a,b,d < n; c.cup(a,b,d)=true, that is Cup3 ...; c.cup(a,b,d) ≠ true, that is Cap3 ..."; parenthesis in the proof | ListGeometry.lean:19–20: `cup_sign (c) (a b d : Nat) (ha hb hd) : c.cup a b d=true ↔ 0<orient (pointAt c a) ...`; :24–26: `cap_sign ... (ab : a<b) (bd : b<d) : (¬c.cup a b d=true) ↔ orient ... <0`; `pointAt c a = c_a` for a < n (Definition `mb:def:color`); `Cap3` of `colorConfig c.cup true` is `¬(c.cup a b d = true)`. Realization.lean:39–40: `cup_true_iff` with i j k : Fin n and `c.point i`; :44–46: `cup_false_iff` with i<j<k and `c.cup i j k = false`. Its only uses are Realization.lean:114 and ListGeometry.lean:156 (off-path) | exact; parenthesis accurate |
| H15 | mb.tex:377 | Lemma `mb:lem:boundary`(b): bound variable v → p | `boundary_convex_position` (BoundaryGeometry.lean:317): `∀ v ∈ b.points, v ∉ convexHull ℝ (b.points \ {v})`; p is not used elsewhere in the statement | exact |
| H16 | mb.tex:392–394 | Remark `mb:rem:boundary`: the change of variables is a bijection onto values of `Boundary s t`; `Boundary.card` counts `Boundary.finite`, which is B | `Boundary` (120–124) = two `CupArc`s (56–59, Prop fields only besides `point`) plus `first_eq`/`last_eq`; (u, v) ↦ (u, ρ∘v) is inverse to w ↦ ρ∘w, since ρ fixes x and negates orient (69–73). `Boundary.finite` (350–352) is image(lower) ∪ image(reflect ∘ upperReflected) = U ∪ V = B. `Boundary.card` (359): `b.finite.card = k+l+2` | correct |
| H17 | mb.tex:503–505 | proof of `mb:prop:cap16`: "the value 4 for its parameter (called n there)" | removes the clash with the size n of c | correct |
| H18 | mb.tex:536–539 | Subsection `mb:ssec:red`: its Lean declarations, those of Definition frame and Lemmas frame, affine, transport are also stated (and proved) in section mm | `sections/mm.map.tsv`: mir/Rset/Aset (`mm:def:mir`), card_split/card_A_le (`mm:lem:count`), injOn_x (`mm:lem:injx`), cfg (`mm:def:config`), sortPt_image (`mm:lem:sort`), the four generated polygons (`mm:prop:small-polygons` (d),(e),(h),(i), with a proof from the general theorems), lineRefl/frame/unframe (`mm:def:frame`), the six frame lemmas (`mm:lem:frame`), hasConvexNGon_affineMap (`mm:lem:ngon`), transport (`mm:thm:line`). Lemma `mb:lem:interior` is a written step without a Lean name | correct |
| H19 | mb.tex:672–685 | Remark `mb:rem:generated`: lines 22–991 including cyc7/cyc8; the rest of the block up to 1506 serves k = 4, 5, 6; linarith "with hints found offline"; products y(c_i)(x(q)−x(q')); (b), (c), (d) are special cases (m = 4) and (a) follows from (b) by deleting mir c_0 | MirrorMain.lean: cyc7 :22, cyc8 :103, the four lemmas :212/:392/:639/:816, last line of `axis_right_heptagon` :991, ":993 /-! Small k ... (generated by gen_lean.py)", cyc4–cyc6 :995–1068, small polygons :1126–1506, used only in `mirror_four`/`five`/`six` (2033–2147). The header (line 8) says "closed by `linarith` with an exact certificate found offline (gen_certs.py)". There are 35+56+35+35 = 161 `have h... : 0 < orient` lines, every one closed by `linarith` (no `nlinarith`). Products such as p0_21 `c0 1 * (c2 0 - c1 0)` (:234) and p0_10 `c0 1 * (c0 0 - a 0)` (:661) all have the stated form. The derivation sentence matches the proof of `mb:lem:polygons` (mb.tex:652–668) | correct |
| H20 | mb.tex:847–853 | Remark `mb:rem:seven`: second Lean proof via `mirror_odd_general`, which rests on the general mirror lemma | MirrorMain.lean:2631–2633 is `mirror_odd_general 3 16 ... capacity16`; `mirror_odd_general` (2498–2598) calls `cap_mirror_polygon`, `axis_left_polygon` and `axis_right_polygon` once each; `mirror_seven` (1805) uses `mirror_seven_of` with the three generated lemmas | correct |
| H21 | mb.tex:891–895 | Remark `mb:rem:eight` reworded | 2636–2638 `mirror_even_general 4 22 ... capacity22g` | correct |
| H22 | mb.tex:964–969 | paraphrase of `mirror_odd_general` with e of r points | 2498–2502: `∀ (n : ℕ) (c : Configuration n), ¬ c.HasCap (j+1) → ¬ HasConvexNGon (2*j+1) (univ.image c.point) → n ≤ M`, conclusion `S.card ≤ 2*M` | exact (renaming only) |
| H23 | mb.tex:1004–1006 | status of `mb:thm:refl32`: (b) rests on `mb:thm:seven`(b), hence on Baek and `mm:thm:mirror-polygon`/`mm:thm:axis-polygon` | proof (b) (1021–1022) uses `mb:thm:seven`(b); `mb:thm:seven`'s status line (834–835) lists the same three | correct |
| H24 | mb.tex:1039–1041 | status of `mb:thm:classes`, the same dependency chain | proof (1044–1046) uses `mb:thm:refl32`(b) only | correct |
| H25 | mb.tex:1085–1113 | Remark `mb:rem:main3` rewritten | §3 below | supported |
| H26 | mb.tex:1125–1196 | Coverage restructured | §4 below | correct, minor m2, m3 |
| T1 | map row `mb:def:config` | `Config.Cap3` / `Defs.lean:30` added in position 2 | equals the head | consistent |
| T2 | map row `mb:lem:signs` | `cup_false_iff` and its file:line removed; note extended | names and lines equal the head, but the remaining separator lost its space | m1 |
| T3 | map rows `mb:prop:gon`, `mb:lem:polygons`, `mb:thm:main3` | notes reworded | the three proofs of `hasNGon_heptagon`/`_octagon`/`_nonagon` differ only in the number and the name of the local hypothesis (seven/eight/nine); "hints found offline" is from the MirrorMain.lean header; the main3 note matches the remark | consistent |

**Other checks over all hunks.**
- No machine path and no name forbidden by hard rule 3 of the contract appears in `mb.tex` or `mb.map.tsv`.
- The section uses no `\newcommand` or `\usepackage`.
- The rigor vocabulary was checked with a case-insensitive grep for "verif", "certif", "proved", "proves", "proven" and
  "refereed". Every hit is either a correctly labelled statement or a negative statement ("not proved in Lean or in this
  document"). Two hits describe Lean or records: "is proved by linarith" and "what its certificate proves", the latter
  paraphrasing `SYMLEAN/README.md` §9. Nothing is rounded up, and no hypothesis is presented as proved.

**Map check.** `build/mb_p1diff_mapcheck.py` gives the following:
- The header is correct. There are 42 rows of 5 fields each, in ASCII.
- Labels and kinds equal the 42 statement environments, in order.
- With a tolerant split on `;`, the Lean names and file:lines equal the `\leanref` pairs.
- Each of the 78 cited lines declares the named identifier.
- With the split of `tools/make_appendix.py`, row `mb:lem:signs` does not split correctly (m1).

## 3. Remark `mb:rem:main3`: the new claims about records

| claim | record evidence | result |
|---|---|---|
| sources: "SYMLEAN/mirror/README.md §4, and the table in SYMLEAN/README.md §5" | mirror README §4 "Scope" names C2FINAL with C2C34, C3FINAL with C3LEAN, SYM5 and the written encoder proofs; README §5 is the table "The classes and their certificates" | ok |
| HalfTurn34 "claimed in C2FINAL"; "the hull cover and the 120 hexagonal hulls of C2C34 have retained proofs" | C2FINAL/README.md statement "(claimed; computer-assisted)"; status: "The hull cover and the 120 hexagonal hulls have retained proofs"; §1 item 3 "All 120 cases are UNSAT with archived proofs (C2C34 §3)"; SYMLEAN §5 table: "C2C34 (encoder, hull cover, 120 hexagonal hulls)" | ok |
| "most parallelogram pieces (C2P–C2P5) rest on verdicts recorded at solve time (both proof checkers accepted the proof, which was then deleted), with re-solved samples and re-checks (status paragraph of C2FINAL/README.md; C2RECHECK)" | C2FINAL status: "Most parallelogram pieces rest on recorded verdicts: both checkers accepted the proof at solve time, and the proof was then deleted"; §5 sample 24/24 and a second draw 8/8; §9 re-checks; SYMLEAN §5 "totals in C2RECHECK"; the directories C2P, C2P5 and C2RECHECK exist | ok |
| "the encoder and the two reductions of the case split have written proofs" | C2FINAL §1 (C2ENC refereed; reductions A and B reviewed in `C2P/review`); SYMLEAN §5 | ok |
| Threefold33: "116,883 piece records carry verdicts recorded at solve time (both proof checkers accepted the proof); the proofs were not kept (C3LEAN/README.md §4)" | C3LEAN/README.md §4: "Each one records that both checkers accepted its proof when it was solved. The proofs were not kept."; C3FINAL "116,883 / 116,741" | ok |
| "2,120 randomly chosen pieces were re-solved (C3SPOT)" | C3LEAN §6; SYMLEAN §5 and §9 (the draw excluded σ-cube records, which the remark does not need to say) | ok |
| "C3LEAN Lean-checks only that the leaves named in it cover the 910 roots ... (that every leaf has such a record is checked outside Lean)" | C3LEAN statement and status: `all_roots_covered`, 73,567 leaves, 910 roots; "That every leaf names a certified record is checked in Python ... outside Lean" | ok |
| "the normal form C3-S/soundness.md, the encoding C3a, the exhaustiveness of the splits and the reductions of the case split are written proofs" | C3LEAN status ("That the splits are exhaustive, and that the reflection maps of Lemma 5 and Lemma H6M are the right maps, are written proofs"); SYMLEAN §5 ("normal form and encoding: written proofs (reviewed, C3AUDIT–C3AUDIT4)"); WRITEUP/SYMMETRIC.md §3; AUDIT3/reports/A2_threefold.md row 2 ("written proof, re-derived by the auditor"). Note: the older C3AUDIT/REPORT.md:10 and C3LEAN §6 call the C3a encoding "tested, not proved"; the later audit and the two summary records classify it as an audited written proof, so the remark's wording is supported | ok |
| Fivefold35: "SYM5, two normal forms of one encoder, each with a retained proof accepted by both proof checkers; the encoder and the layer lemma have written proofs" | SYM5/README.md, "What is here" and §2; WRITEUP §1 Theorem 5. The layer lemma is also Lean-checked (LAYERLEAN); the remark understates this, which is not an overclaim | ok |
| "Threefold33 and Fivefold35 also rest on the written centre-perturbation lemma C2ENC/perturbation.md" | perturbation.md title "(odd rotation orders; used for m = 3 and m = 5)", and "For the half-turn (m = 2) no such lemma is needed"; SYM5 README line 44 | ok |
| "For none of the three is the step from a certificate to the Lean proposition formal ... checked by reading (SYMLEAN/README.md §6 and §9)" | §6: "The match itself was checked by reading: no formal link joins a Lean class to its CNF"; §9 last item | ok |

Wherever WRITEUP §3 (revised 6 November) says "both checkers", the certificate is the cake_lpr verdict. The remark's
"both proof checkers accepted" repeats the records exactly and does not claim more.

## 4. Coverage paragraph

- **Names.** Every newly listed name exists at its place:
  - `mir_zero`, `mir_one`: MirrorMain.lean:18–19;
  - `xset_card` :1551 and `emb_mem` :1555;
  - `OrderedTriples`: PlanarChains.lean:54;
  - `Config.NCap` :51, `Config.NCup` :54 and `Config.DecidableCap3` :33 (Defs.lean);
  - in Lib/List/Lemmas.lean: `List.takeHead` :72, `takeHead2` :76, `takeLast2` :105, `in_superset` :24 and
    `cons_in` :34;
  - the 19 BoundaryGeometry names: together with the declarations named in the head and in the proof of
    `mb:lem:boundary` they are all 37 declarations of the file, and each is used inside the file,
    `Boundary.finite_coe` through dot notation in `boundary_polygon`;
  - `hasCap3_of` :1991 and `capacity_cup` :2002 are used at 2015, 2048 and 2139.
- **Off-path list.** `cup_false_iff`, `hasCup_of_list`, `hasNCup_octagon`, `chain3_of_all`, `listCup_of_hasCup`,
  `listCap_of_hasCap` and `PlanarChains.cup_all` are used only off the paths:
  - in each other: `hasCup_of_list` → `hasNCup_octagon`; `chain3_of_all` → `listCup_of_hasCup`/`listCap_of_hasCap`;
    `cup_false_iff` → `listCap_of_hasCap` and `endingPath_hasCap`;
  - or in `Subsets`, `Partition`, `ThreeChain`, `Residual*` and `SlopePartition`, none of which MirrorMain, the
    append file or RTC imports or uses.
- **Realization.lean and ActualRanks.lean.** A grep over 27 names covered the bridge files on the path,
  MirrorMain.lean, MirrorNine_append.lean and RTC. The 27 names are the 20 declarations of ActualRanks.lean other than
  `colorConfig`, plus seven of Realization.lean (`ofGeneralPosition`, `HasCup`, `endingPath_embedding`,
  `avoids_of_noCup`/`noCap`, `balancedOwner`, `balanced_universe_bound`). The only hits are:
  - `HasCup` and `false_cup_iff_cap`, inside the off-path declarations above;
  - the word "lengths" in a comment.

  The remaining Realization.lean declarations occur only in that file: `endingPath_hasCup`/`hasCap`, the private
  `chain3_getElem` and `balancedOwner_injective`.
- **Part B of RTC.** It "is MirrorMain.lean verbatim after its two import lines": `diff` of RTC 1562–4236 against
  MirrorMain.lean 3–2677 is empty.
- **Configuration and Configuration.HasCap.** "stated as Definition mm:def:config" agrees with `sections/mm.map.tsv`,
  row `mm:def:config`.

## 5. The fixer's dispositions

All 19 "fixed" items are fixed correctly:

| finding | evidence |
|---|---|
| fid F1, rig F5, adv 2 | H12 |
| fid F2, rig F1, adv 3, cl F1 | H3 |
| fid F3, rig F3, adv 5, cl F9 | H11 |
| fid F4, rig F2, adv 4, cl F2 | H5 and H14; `cup_false_iff` is gone from the head and the map, named in the proof parenthesis and listed as off-path in Coverage |
| fid F5, cl F3 | H4 |
| fid F6, adv 1 | H10. The remark no longer asserts the identification, so the strength mismatch with Theorem 2.7 that adv 1 found cannot mislead |
| fid F7 | H25 |
| fid F8, cl F5(b) | §4 |
| rig F4 | H10, the PROOFS.md quotation |
| rig F6, adv 6, cl F8 | H19 |
| rig F7 (n, c), adv 8 | H13, H15, H17, H22 |
| rig F8 | H23, H24 |
| rig F9, adv 9, cl F6 | H18 and Coverage line 1156–1158 |
| adv 7 | §4 and T1 |
| cl F4 | §3 |
| cl F5(a) | §4 |
| cl F7 | H1 |
| cl F10 | H14, H16 |
| cl F11 | H9 and H20/H21; `pdftotext` renders `mirror_seven'`, `mirror_eight'`, `List.Chain3'` with the ASCII quote |

- **The 18 "duplicate" rows** each point at one of the fixes above. The mapping is correct.
- **Declined: rig F7 (R).** R denotes a ternary relation (Lemma `mb:lem:chain`, the Lean binder name), the upper part
  R(S) (Definition `mb:def:mir`) and the right end point inside the proof of `mb:lem:boundary`. Each use is local to one
  statement and its proof. Declining is acceptable: this is style only, with no inaccuracy.
- **Declined: the optional conceptual proof of (mb:eq:chord).** Acceptable. The expansion proof is complete.

## 6. Compile check

`build/mb_p1diff_wrapper.tex` is the contract's wrapper for `mb`. It was run from `build/` with
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error mb_p1diff_wrapper.tex`, twice.

- **Exit codes and errors.** Both passes exit with code 0. The output has 16 pages. No line starts with `!`. There is
  no "Missing", no "multiply defined" and no missing-character warning.
- **Overfull boxes > 1pt:** none (0 overfull boxes in total).
- **Underfull boxes:** 3, all cosmetic:
  - an hbox in the axioms paragraph, at source lines 69–76, a run of long Lean names;
  - two vboxes while `\output` is active.
- **Undefined references:** only allowed labels.
  - `fd:`: `def:{cp,gp,inv,ngon,orient,point}` and `lem:{affine-cp,affine-orient,collinear,cp-hull,mono,orient,pos-cycle,separation}`;
  - `mm:`: `def:config` and `thm:{axis-polygon,even,line,mirror-polygon,odd,small}`;
  - `sr:`: `def:{classes,iso}` and `thm:main`;
  - `ar:thm:main`.
  No `mb:` reference is undefined.
- **Rendering.** Pages 1, 3, 4, 15 and 16, rendered at 70 dpi, show the new itemized lists and the remarks laid out
  correctly.

## 7. Findings

**m1 (minor; introduced in this round). Map row `mb:lem:signs`: separator without a space.**
- *Location.* `sections/mb.map.tsv`, row `mb:lem:signs`, columns `lean_name` and `file_line`.
- *Issue.* The row reads `...Configuration.cup_true_iff;ErdosSzekeres.Omission.ListGeometry.cup_sign; ...` and
  `...Realization.lean:39;ErdosSzekeres/Omission/ListGeometry.lean:19; ...`. The space after the first `;` is missing.
  Every other row of every section map uses `; ` (a grep over `sections/*.map.tsv` finds `;` followed by a non-space
  only in this row). The passed snapshot had `; `.
- *Effect.* `tools/make_appendix.py` splits these columns with `re.split(r'[;,]\s+', s)`, so the appendix row would
  show one entry `\lean{...cup_true_iff;...cup_sign}` and one entry `\dirn{...Realization.lean:39;...ListGeometry.lean:19}`
  in place of two separate names and paths. The section itself is unaffected.
- *Fix.* Insert a space after the first `;` in both columns.

**m2 (minor). The new path convention does not cover the bare file names.**
- *Location.* mb.tex:25–27 (convention). The bare names are at mb.tex:32, 67, 88–90, 92, 1174, and, new in this round,
  1182 (`BoundaryGeometry.lean`) and 1192–1193 (`Realization.lean`, `ActualRanks.lean`).
- *Issue.* The new sentence says that every path not beginning with `ErdosSzekeres/` or `docs/` is relative to the
  results directory. The section also uses bare file names as short forms: `MirrorMain.lean`, `MirrorNine_append.lean`,
  `SymmetricReduction.lean`, and the three new ones above. None of these exists at the root of the results directory.
  Context makes each one clear, since each is listed with its full path in Sources or nearby.
- *Fix.* Add "bare file names refer to the files listed below", or write the three new ones with full paths.

**m3 (minor). Coverage: "they are the subject of Theorems ..." also covers helpers that mm treats in lemmas.**
- *Location.* mb.tex:1168–1175.
- *Issue.* The item lists `cap_below_lines` and, new in this round, `hasCap3_of` and `capacity_cup`. In section mm these
  are the subject of Lemma `mm:lem:slope` (an mm export label that mb may cite) and Lemma `mm:lem:cup` (not an export
  label), not of the theorems listed in the parenthesis. The wording is slightly loose and has no effect on correctness.
- *Fix.* Write "(they are the subject of Lemma mm:lem:slope and of Theorems ..., or are used in their proofs)".

## 8. Checked, with no finding

- **Statements.** Each statement touched by the diff (`mb:def:config`, `mb:lem:signs`, `mb:lem:boundary`) still
  matches its Lean declarations exactly (H8, H14, H15). No statement gained or lost a hypothesis.
- **Lean paraphrases in proofs and remarks** (`mirror_odd_general`, `mirror_seven'`, `mirror_eight'`, `cup_true_iff`,
  `cup_false_iff`, `Boundary`, `Boundary.finite`, `Boundary.card`): all accurate.
- **Records.** Every new claim about records (Sources, axioms paragraph, Remarks `mb:rem:baek` and `mb:rem:main3`,
  Coverage) is supported by the files cited. The only tension found is between records, on the status of the C3a
  encoding (§3). The remark follows the later audit and the summary records.
- **Rigor labels.**
  - The conditional theorem stays conditional, and its three hypotheses are described as computer-assisted claims,
    "not proved in Lean or in this document".
  - The section's own proofs are "written proofs (not refereed)".
  - The words "certified" and "verified" do not occur.
- **LaTeX.** Sound: no forbidden macro or package, no disallowed `\ref`, and all seven export labels defined on the
  required statements (unchanged).

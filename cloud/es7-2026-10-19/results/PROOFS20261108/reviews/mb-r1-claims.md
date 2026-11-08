# Review of section `mb` (Mirror bounds via Baek's theorem and the three-class reduction), round 1, lens: claims, labels and LaTeX

**Verdict: pass.** No blocker and no major finding. There are eleven minor findings, F1 to F11.

Files reviewed: `sections/mb.tex` (1,113 lines) and `sections/mb.map.tsv` (42 rows plus a header). Paths:
- `sections/`, `build/` and `reviews/` are relative to STAGE;
- `MIRRORETV/...`, `SYMLEAN/...`, `C2FINAL/...`, `C3FINAL/...`, `C3LEAN/...`, `C3SPOT/...`, `SYM5/...` and `H3/...` are
  relative to RES;
- `ErdosSzekeres/...`, `docs/...` and `lake-manifest.json` are relative to the repository root;
- RTC is `SYMLEAN/mirror/ReductionThreeClasses.lean`.

My helper scripts and outputs are in `build/claims-mb-r1/`.

## Checks performed, with evidence

1. **Compilation.** I ran `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error -output-directory=claims-mb-r1
   mb_wrapper.tex` twice from `build/`.
   - Both passes exited 0 and produced 15 pages.
   - The log has no `!` error, no "Missing $", no overfull box and no multiply-defined label. It has 3 underfull hboxes
     and 1 underfull vbox, all cosmetic.
   - After pass 2 every undefined reference is an allowed one:
     - `fd:def:{point,orient,gp,cp,ngon,inv}` and `fd:lem:{orient,affine-orient,collinear,cp-hull,mono,affine-cp,pos-cycle,separation}`;
     - `mm:def:config` and `mm:thm:{mirror-polygon,axis-polygon,odd,even,line,small}`;
     - `sr:def:iso`, `sr:def:classes` and `sr:thm:main`;
     - `ar:thm:main`.
   - All 25 of these labels are defined in the current `sections/fd.tex`, `mm.tex`, `sr.tex` and `ar.tex`. Each sits on
     an environment of the kind the text names (Definition, Lemma or Theorem), so the full document will resolve them
     with the right words.

2. **Labels.**
   - The section defines 57 labels, each once, all with the prefix `mb:`.
   - There are 71 distinct `\ref`/`\eqref` targets. Every `mb:` target is defined. Every other target is an `fd:` label
     or an export label from the contract table; there is no `\ref` to a non-export label of another section.
   - All seven export labels are defined on the statements the contract names:
     - `mb:thm:baek` on `main`;
     - `mb:thm:seven` on `mirror_seven` and `mirror_seven_line`;
     - `mb:thm:eight` on `mirror_eight` and `mirror_eight_line`;
     - `mb:thm:nine` on `config_capacity113`, `mirror_nine` and `mirror_nine_line`;
     - `mb:thm:refl32` on `reflLine_eq_lineRefl` and `card_le_32_of_reflLine`;
     - `mb:thm:classes` on the two `_proved` theorems;
     - `mb:thm:main3` on the two `_3` theorems.
   - Other sections reference `mb:thm:{baek,seven,eight,nine,classes,main3}`, and all of these exist.

3. **Map (`build/claims-mb-r1/mapcheck.py`).**
   - The section has 42 statement environments (5 definitions, 16 lemmas, 4 propositions, 8 theorems, 9 remarks) and the
     map has 42 rows, in the same order.
   - Kind, `lean_name` and `file_line` of every row match the `\leanref`s in the environment head. Remarks and the
     written step `mb:lem:interior` have `-` in both columns.
   - The header is as the contract requires and every row has 5 fields. The file is ASCII, has no CR characters and
     ends with a newline.
   - The notes state the hypotheses (Hcap/HL/HR for `mirror_seven_of`; HalfTurn34, Threefold33 and Fivefold35 for
     `mb:thm:main3`, with the supplying records named) and the `decide` binomials.

4. **Lean names and line numbers.**
   - `build/claims-mb-r1/leancheck.py` read the line cited by every `\leanref{name}{file:line}`. All 78 pairs point
     exactly at a `theorem`, `def` or `structure` of that name. The namespace prefixes (`MirrorOdd`, `C12Check`,
     `ErdosSzekeres.Omission.*`, `ErdosSzekeres.SymReduction`) agree with the `namespace` blocks.
   - Root-namespace vendored names (`main`, `ncup_is_ngon`, `hasNCap_supset`, `hasNGon_supset`) are correctly unprefixed:
     `Config/Lemmas.lean` ends `namespace Config` at line 273, before them.
   - All 193 distinct `\lean{...}` names in the running text exist as declarations (`build/claims-mb-r1/namecheck.py`),
     except `Cup3`, `lower`, `upperReflected`, `first_eq` and `last_eq`, which are correctly described as structure fields.
     `PlanarChains.cup_all` (`PlanarChains.lean:105`) and `Mir.MirrorExclusionLine` (`H3/MirrorEncoding/Line.lean:94`)
     exist.
   - Every line number in the running text is exact. I checked:
     - `Config.Cap3` at line 30; `List.Chain3'` at `Lib/List/Defs.lean:46`; `List.In` at `:22`;
     - `Boundary` at `:120`; `CupArc` at line 56; `reflect` at line 69; `chord_identity` at line 64; `exposed_not_in_hull`
       at line 30;
     - `boundaryOfGon` at `:62` and `boundaryOfGon_inside` at line 77;
     - `mir_mir` at 1543 and `unframeLin` at 1886;
     - `cap_mirror_polygon` at 2233, `axis_left_polygon` at 2309, `axis_right_polygon` at 2403, `mirror_odd_general` at
       2498, `mirror_seven'` at 2631, `mirror_eight'` at 2636 and `mirror_odd_general_line` at 2641;
     - the generated range 22–1506 (`cyc7` at 22; the last generated proof ends at 1506);
     - `reflLine` at RTC:449 and at `SymmetricReduction.lean:423`;
     - in RTC: 1023, 1050, 1078, 1503, 1515, 1527, 1536 and 1547; `SymmetricReduction.lean:997`;
       `AffineReduction.lean:1501`;
     - `Realization.lean:9` and `:64`.
   - The statements of `main`, `Config.cap_cup`, the Config definitions, the bridge lemmas, `capacity16`, `capacity22g`,
     `mirror_seven_of`, `mirror_seven(_line)`, `mirror_eight(_line)`, `config_capacity113`, `capacity113`,
     `mirror_nine(_line)` and the six Part C theorems agree with the Lean text I read. For the Part C theorems I checked
     the binders, `hu`, `Invariant`, the explicit affine-equivalence form and `g ≠ AffineEquiv.refl ℝ Point`. Fidelity
     itself is another lens; see F10 for two packaged statements.

5. **SHA-256 prefixes.** I recomputed all 18 with `shasum -a 256`, and all are correct:
   - `MirrorMain.lean` ca623e55a1b9, `MirrorNine_append.lean` c2afca380211, RTC 0cc83994fe8c;
   - the vendored files: `Main.lean` 83dd0a214204, `CapCup.lean` fb8fbefac260, `Config/Defs.lean` ce2ccf7c1d28,
     `Config/Lemmas.lean` 5395e27a82cc, `Lib/List/Defs.lean` 46d750763528;
   - the bridge files: `Realization` ae4970e0808e, `ActualRanks` 3788f5149b3a, `PlanarChains` 21161d053dc0,
     `ListGeometry` 1a03c283176b, `BoundaryGeometry` f55a711e7aa9, `BaekGeometry` db8ac3c30dc0, `Baek` 3433c3c2124d;
   - the logs: `MirrorMain.out` c6024155067e, `MirrorNine.out` 976fda168e70, `axioms.out` ab92257c6f17.

   The MIRRORETV values also agree with `MIRRORETV/SHA256SUMS`. The concatenation `MirrorMain.lean ++
   MirrorNine_append.lean` hashes to d0831d4d1d59…, the value recorded at `MIRRORETV/README.md:181,263`.

6. **Axioms logs.**
   - `MirrorMain.out`: lines 848–863 are the 16 `MirrorOdd` lines, all `[propext, Classical.choice, Quot.sound]`.
     `mirror_seven` is at 848, `mirror_eight` at 849, `mirror_seven_line` at 850, `mirror_eight_line` at 851,
     `mirror_odd_general` at 858 and `mirror_odd_general_line` at 862. A grep finds no "error" in the log.
   - `MirrorNine.out`: lines 879–882 give the four `C12Check` theorems with the standard axioms. The log uses
     line numbers of the concatenation, and the shift 2677 is right: `MirrorMain.lean` has 2,677 lines, and the warning
     lines 2740/2742/2743/2746 are `<;>` lines 63/65/66/69 of the appended file.
   - `axioms.out`:
     - lines 1–16 are the 16 `MirrorOdd` theorems;
     - lines 21–38 are the six Part C theorems (some repeated);
     - lines 17–20 and 39–40 are truncated `#check` output showing the binders `HalfTurn34 → Threefold33 →` (see F3).
   - The per-statement Status lines cite the right logs and lines: 848/850, 849/851, 879/881/882 and `axioms.out`.
   - Lean 4.24.0 and Mathlib f897ebcf agree with `lake-manifest.json` (`mathlib f897ebcf72cd…`), with
     `SYMLEAN/mirror/README.md:49` and with `MIRRORETV/README.md:74`. The README says the lake files of commit
     5bdebbb48 equal this branch's.

7. **`decide`, `native_decide`, `sorry`, axioms.**
   - `decide` occurs 22 times in `MirrorMain.lean`, 2 times in `MirrorNine_append.lean` and 22 times in RTC, all of
     them inside the `MirrorOdd` copy. The uses are `Fin` index comparisons and `Nat.choose (4+2) 2 = 15`,
     `Nat.choose (6+2) 2 = 28` and `Nat.choose (3+6) 3 = 84`. This is exactly what the text says, and the description
     "the kernel evaluates" is right (no `Lean.ofReduceBool`).
   - A grep for `native_decide|sorry|admit|axiom|ofReduceBool|implemented_by|extern|unsafe` over the three files, the
     whole `ErdosSzekeres/Vendor` tree and the seven bridge files finds nothing.
   - No statement of the section is itself a finite computation. The polygon lemmas get a conceptual derivation, so no
     "computer-assisted" label is needed in the statements.

8. **Copies.** I checked with `sed` and `diff`:
   - RTC 1562–4236 is byte-identical to `MirrorMain.lean` 3–2677 (offset 1559);
   - RTC 38–1559 is byte-identical to `AffineReduction.lean` 12–1533;
   - RTC 38–1084 is byte-identical to `SymmetricReduction.lean` 12–1058 (offset 26).

   `sr:thm:main` cites `SymmetricReduction.lean:997` and `ar:thm:main` cites `AffineReduction.lean:1501`, the originals
   of RTC 1023 and 1527. So "the written proofs ... apply verbatim" is consistent.

9. **Hypotheses and records.**
   - `mb:thm:main3` is marked "conditional" in the head, the statement and the Status line. The map note says
     "takes hypotheses".
   - Remark `mb:rem:main3` names the records C2FINAL/C2C34, C3FINAL/C3LEAN and SYM5. This is exactly
     `SYMLEAN/mirror/README.md` §4 (line 64–65). The remark says "computer-assisted" and "not Lean-checked".
   - The caveat about recorded verdicts matches the `C2FINAL/README.md` Status paragraph (lines 17–20). For the
     threefold class it matches `C3LEAN/README.md:137–138`; see F4 for the citation.
   - `mb:thm:classes` and `mb:thm:refl32` really use no SAT input and no unproved hypothesis: RTC 4253–4286.
   - The unused axis hypotheses are stated as such.
   - Remark `mb:rem:axis` is consistent with RTC:1078 and `H3/MirrorEncoding/Line.lean:94`. It correctly says RTC does
     not state the implication.
   - The docstring overclaims ("Corollary 3 ...", "Lean-verified there from CNF facts") are not repeated.

10. **Overclaiming, paths, tool names.**
    - A grep of `mb.tex` and `mb.map.tsv` finds no hit for the four absolute path prefixes forbidden by contract rule 3,
      for the staging directory's parent, for `cloud/` or `results/`, or for tool names.
    - All paths have the contract's relative form. The source is pure ASCII. There is no `\newcommand` or
      `\usepackage`, and the file starts with `\section{...}\label{mb:sec}`.
    - The rigour wording is consistent: "Lean-checked", "written proof (not refereed)", "cited", "conditional" and
      "computer-assisted" for the records. Nothing is called verified or certified.

11. **Identities.** `build/claims-mb-r1/identities.py` (sympy 1.13.3) confirms all 17 polynomial identities that the
    section says were "checked symbolically":
    - the four-point identities (`mb:eq:four-left` and `mb:eq:four-right`) and the chord identity (`mb:eq:chord`);
    - the axis-interior identity and the vertical-collinearity identity of `injOn_x`;
    - the four frame identities with their `(ν−1)` right-hand sides and the second frame coordinate;
    - the two `reflLine`/`lineRefl` identities, including the intermediate expressions written in the proof of
      `mb:thm:refl32`(a).

    Baek's Theorem 1.6 as paraphrased in Remark `mb:rem:baek`(1) matches the quotation in `MIRRORETV/PROOFS.md:365–367`.
    Cups–caps is cited correctly (Compositio Math. 2 (1935) 463–470).

## Minor findings

**F1 (attribution).** `mb.tex:39–41`, Sources paragraph: "the bridge files (adapted from M. Schroeder's archive, MIT
licence)" includes `ErdosSzekeres/Omission/Realization.lean`.
- Evidence: six of the seven files carry an "Adapted from Michael Schroeder ..." header. `Realization.lean` has none.
- `docs/THIRD_PARTY.md:111–117` says `Realization.lean` "connects attained paths to this project's all-triples cups,
  caps and general-position predicate ... These connections ... were added here".
- Fix: say "six of them adapted from ...; `Realization.lean` is the project's own".

**F2 (evidence for one bridge lemma).** `mb.tex:71–73` says the printed axioms lines cover "the bridge lemmas", and
`mb.tex:92–93` says every Lean declaration stated below is Lean-checked by that evidence. One cited declaration is
outside the cone.
- `Configuration.cup_false_iff`, in the head of `mb:lem:signs`, is not in the dependency cone of any printed theorem.
  Its only uses are `Realization.lean:114` (`endingPath_hasCap`) and `ListGeometry.lean:156` (`listCap_of_hasCap`), and
  neither is on the path. The path uses `cap_sign` (which uses `cup_sign`, which uses `cup_true_iff`).
- It is still Lean-checked: its module compiles as an import of `MirrorMain.lean` (0 errors, no `sorry` in the file).
  But no `#print axioms` line covers it.
- Fix: drop `cup_false_iff` from the head (the written statement is `cap_sign`), or add half a sentence saying it is
  checked as part of the compiled import.

**F3 (description of `axioms.out`).** `mb.tex:67–69` says "its two `#check` outputs are truncated (they show the binders
HalfTurn34 and Threefold33 ...)".
- RTC has five `#check` commands (RTC:4312–4316). `axioms.out` shows truncated output for only the two `_3` theorems
  (lines 17–20), and the first one again at lines 39–40.
- Fix: "it contains truncated `#check` output for only two of the five `#check` commands of RTC (the two `_3` theorems);
  the binder `Fivefold35` is cut off".

**F4 (citation precision).** `mb.tex:1046–1048`, Remark `mb:rem:main3`, says that part of the case split rests on
verdicts recorded at solve time rather than retained proofs "(see ... `C2FINAL/README.md` and the record C3SPOT)".
- For Threefold33 the explicit statement is `C3LEAN/README.md:137–138` ("proofs were not kept ... the leaves rest on
  recorded verdicts"). `C3SPOT` documents only the sampled re-solve.
- The claim is correct; add `C3LEAN/README.md` as the source for the "not retained" part.

**F5 (Coverage paragraph not exhaustive).** `mb.tex:1068–1113`.
- (a) Helpers on the proof path are absent from both lists:
  - `MirrorOdd.xset_card`, `emb_mem`, `mir_zero`, `mir_one`;
  - `Config.NCap`, `Config.NCup`, `Config.DecidableCup3`, `Config.DecidableCap3`;
  - in `BoundaryGeometry`: `affine`, `affine_mix`, `affine_positive_convex`, `supporting_edges_expose`, `point_x_bounds`,
    `first`, `last`, `first_x_strict`, `last_x_strict`, `reflect_reflect`, `orient_reflect`, `reflect_mem_flip`,
    `Boundary.finite_coe`;
  - the vendored list lemmas `List.takeHead`, `List.takeLast2`, `List.takeHead2`, `List.in_superset` and `List.cons_in`
    used by `config_capacity113`.
- (b) "declarations of the bridge files not on these paths (hasCup_of_list, ...)" names five declarations. But
  `Realization.lean` (16 declarations) and `ActualRanks.lean` (21) contain many more that are off the path, for example
  `ofGeneralPosition`, `HasCup`, `endingPath_*`, `avoids_of_*`, `balancedOwner*`, `EndingPath`, `rank` and `labels`.
- Fix: write "for example" and add one sentence: the remaining declarations of these files belong to the Omission
  development and are outside this section.

**F6 (duplication with section mm, unacknowledged).** `mm.tex` states the following with its own labels:
- mir/Rset/Aset (`mm.tex:85`);
- `card_split`/`card_A_le` (`:501`) and `injOn_x` (`:524`);
- sorting (`:158`);
- `hasConvexNGon_affineMap` (`:191`);
- lineRefl/frame/unframe (`:673`) and the frame identities (`:696`);
- `transport` (`mm:thm:line`).

`mb` restates all of these, and its Coverage lists them as covered by `mb` labels. The `\ref` rules force the restatement
(those `mm` labels are not exports), so this is acceptable. But only `transport` carries the note "the same statement is
part (a) of Theorem mm:thm:line" (`mb.tex:770`). A one-line note for the others would tell the reader. The integrator
should check that the two versions of each agree.

**F7 (wording).** `mb.tex:16`: "the two parametrisations of line reflections used in the project". The project has a
third, `MirrorA.refl` (`MIRRORETV/review/MirrorA.lean:706`, a point and a unit direction; listed in the MIRRORETV
inventory risks). Suggest "the two parametrisations used in the Lean files of this section".

**F8 (wording).** `mb.tex:646–647`, Remark `mb:rem:generated`: "the generated statements are special cases of them".
`cap_mirror_octagon`, `axis_left_heptagon` and `axis_right_heptagon` are instances with m = 4. `cap_mirror_heptagon` is
not an instance: the proof derives it from the octagon by deleting one point. Suggest "special cases of them or, for (a),
consequences by deleting a point".

**F9 (reference scope).** `mb.tex:191–193`, Remark `mb:rem:baek`(3): "every N-gon of C_c yields N points in convex
position (Proposition mb:prop:gon)". The proposition is stated only for m ∈ {7, 8, 9}. The claim is true for every
N ≥ 2 by Lemma `mb:lem:boundary`; either restrict it to N = 7, 8, 9 or cite the lemma.

**F10 (packaged statements; for the fidelity lens).**
- `mb:lem:signs` is attributed to four Lean lemmas. Two of them (`cup_true_iff`, `cup_false_iff`) are stated with `Fin`
  indices and the Boolean equations `c.cup i j k = true/false`. The written statement is about `Cup3_{C_c}`/`Cap3_{C_c}`
  on natural numbers, which is `cup_sign`/`cap_sign` after unfolding `colorConfig` and `pointAt`.
- `mb:lem:boundary` is stated after a change of variables from the Lean `Boundary` structure. Remark `mb:rem:boundary`
  and the map note explain it.
- Neither changes the mathematics, but the heads do not say "variant". I am unsure whether the fidelity lens will want
  the word added. The claims attributions themselves are accurate.

**F11 (cosmetic, preamble).** `\lean{MirrorOdd.mirror_seven'}`, `\lean{mirror_seven'}` and the `mirror_eight'` names
render with a typographic right quote. In T1 typewriter, slot 0x27 is quoteright, so the PDF shows `mirror_seven’`
instead of the straight prime of the Lean name. A fix (e.g. `upquote`) would go in the shared preamble, which a section
may not change; noted for the preamble owner.

## Summary

All checks of this lens pass: the hash prefixes, axioms-log line citations, Lean name/line pairs, copy identities, the
`decide` description, the presentation of the hypotheses and records, the labels, the map and the compilation. The
findings are attribution or wording precision (F1, F3, F4, F7–F9), one evidence citation (F2), coverage completeness
(F5), cross-section duplication (F6), statement packaging for the fidelity lens (F10) and a cosmetic preamble issue (F11).
None affects correctness or the rigour labels.

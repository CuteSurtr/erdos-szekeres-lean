# docfix-mb-r1 recheck: section mb after the whole-document review, round 1

Inputs: reviews/docfix-mb-r1-fix.md (fix log), reviews/doc-r1-xref-mmmb.md (findings F1-F3 on mb),
snapshots/docfix-r1-pre/mb.tex and snapshots/docfix-r1-pre/mb.map.tsv (before), sections/mb.tex and
sections/mb.map.tsv (after). The fixer declined nothing.

Verdict: **pass**. All three findings are resolved correctly. No blocker or major finding remains or was introduced.
Three new minor wording points are listed at the end (m1-m3); none affects correctness.

## 1. The three findings

**F1 (Remark mb:rem:main3, rigor labels of the bookkeeping): resolved.**
- HalfTurn34 item (sections/mb.tex:1105-1108). The added sentence says that the listed subcases meet every orbit of
  second-layer subcases, that this is Lean-checked by kernel evaluation and so computer-assisted (Theorem cb:thm:c2),
  and that the refutation of the listed subcases rests on the records. I re-read C2FINAL/Central34Orbits.lean:250-296.
  `all_cases_closed` (line 291) is `(List.range 8).all (fun k => (uncovered (k+1) (closed (k+1))).isEmpty) = true`,
  proved by `decide +kernel`. `uncovered a C` keeps the subcases V such that neither mask V nor mask (refl a V) is in
  bitset C. So the statement says exactly that every orbit {V, refl V} meets the list. The file contains no
  `native_decide`. The header comment says that the file checks only the combinatorics, not the SAT records, the
  covers or reductions A and B. That matches "rests on the records". The wording now agrees with Remark
  sr:rem:records (HalfTurn34 item), Remark ar:rem:classes ("Exact computations") and Remark cb:rem:c2-scope. One
  wording point: "eight parallelogram hull cases" is imprecise (m1 below).
- Threefold33 item (sections/mb.tex:1111-1113). "C3LEAN Lean-checks, by kernel evaluation and so computer-assisted
  (Theorem cb:thm:c3), only that the leaves named in it cover the 910 roots": correct. In C3LEAN/C3Cover.lean,
  `all_roots_covered` (line 2251) combines `roots_match`, `roots_codes_match` (lines 1720, 1725) and the 127 batch
  theorems, all proved by `decide +kernel`, with the soundness lemma `checkRoot_sound`. The only occurrence of
  `native_decide` is the docstring at line 13, which says that it is not used. The wording matches sr:rem:records
  and cb:thm:c3 ("Computer-assisted").
- No rigor label is rounded up. Both bookkeeping steps get "Lean-checked ... computer-assisted", the hypotheses stay
  unproved, and the remark keeps its cake_lpr sentence.

**F2 (dependency paragraph incomplete): resolved.**
- `fd:lem:separation` is added to the list of foundations lemmas (sections/mb.tex:99). It is used in Step 5 of the
  proof of Lemma mb:lem:boundary (line 456), which uses the easy direction and also proves it inline.
- The new sentence (lines 103-106) names the remarks that cite results no proof of mb uses:
  - Remark mb:rem:generated cites Lemma fd:lem:pos-cycle (line 691).
  - Remark mb:rem:main3 cites Theorems ll:thm:layers, lg:thm:nesting, cb:thm:c2 and cb:thm:c3 (lines 1107, 1112,
    1119-1120).
- I mapped every cross-section `\ref` of mb.tex to its enclosing environment with a script. Each of these five labels
  is cited only in that remark and in the dependency paragraph, so the claim "no proof of this section uses" is true.
- The words before the references match the target environments: fd.tex:1077 and 1109 are lemmas; ll.tex:532,
  lg.tex:448, cb.tex:1121 and 1374 are theorems. The fix log gives older line numbers for ll, lg and cb, but those
  numbers appear only in the log.
- After the fix, every cross-section label used in mb.tex is in the paragraph except mm:lem:slope and mm:thm:small.
  Both occur only in the Coverage list, as pointers to where excluded declarations are treated, which is acceptable.
- All labels are fd labels or contract export labels.
- One minor inconsistency in the new split between "used by proofs" and "cited only in remarks" is listed as m2.

**F3 ([n] versus Fin n; P(c) versus pts): resolved.**
- Conventions (lines 116-118): the new sentence says that [n] is Lean's `Fin n` where it indexes a configuration or
  is the domain or codomain of a cap map. I checked every bracket use in mb.tex:
  - The Fin uses are lines 256 and 258-259 (Configuration, HasCap), 370-371 (the cap map built in Lemma
    mb:lem:lists(c)), 717 (`f : [4] -> [|T|]`) and 892 (`f : [4] -> [|R|]`). All are configuration index sets or cap
    maps, so the new sentence covers them.
  - All other uses (216-217, 355-364, 484-540, 968-970) are subsets of the naturals, that is `Finset.range n`.
- The sentence agrees with mm's convention ("[m] ... stands for Lean's Fin m", mm.tex Conventions) and with
  ErdosSzekeres/Omission/Realization.lean:9-13 (`point : Fin n -> Point`) and :64-66 (`HasCap`,
  `exists f : Fin k -> Fin n`).
- One wording point is listed as m3.
- P(c) (lines 259-261): the addition "it is the point set pts(c) of Definition mm:def:config(a)" is correct.
  mm:def:config(a) defines pts(C) = {C_i : i in [n]} as Lean `Finset.univ.image c.point`, the same expression that mb
  gives for P(c), and Realization-based statements such as BaekGeometry.lean:96 and :113 use it. The parentheses
  balance, and the text renders as "(Lean Finset.univ.image c.point; it is the point set pts(c) of Definition
  ??(a)); since ...".

## 2. Diff review, hunk by hunk

The `diff -u` of snapshot against current has four hunks in mb.tex and one in mb.map.tsv. No statement environment,
label, Lean name or file:line is touched; the 42 labelled statement environments are the same before and after.

1. mb.tex at line 96 (Dependencies and rigour): mathematically neutral, and the references resolve to the right kinds
   (see F2). "Two remarks refer to further results that no proof of this section uses" is true as written. Minor m2.
2. mb.tex at line 109 (Conventions): correct. `\texttt{Fin n}` is used because the expression contains a space, as the
   contract requires. Minor m3.
3. mb.tex at line 250 (P(c)): correct (see F3).
4. mb.tex at line 1094 (Remark mb:rem:main3): correct against both Lean files and the records C2FINAL/README.md
   (Status; section 1, item 4; section 6: "decide +kernel, axioms propext only", "The file checks the combinatorics
   only"). Minor m1.
5. mb.map.tsv, row mb:rem:main3: the note now ends "the case-split bookkeeping (cb:thm:c2, cb:thm:c3) is Lean-checked
   by kernel evaluation, so computer-assisted". This is consistent with the remark. I rendered it read-only with the
   `note_tex` function of tools/make_appendix.py, writing nothing: both label tokens become `Theorem~\ref{...}`, and
   every mb note renders with no undefined label. The map has 42 rows, each with 5 fields; it is ASCII only, the kinds
   match the environments, and there is one row per statement environment.

Other checks:
- No machine path and no tool name in mb.tex or mb.map.tsv.
- No `\newcommand` or `\usepackage`.
- None of the added lines contains "verified", "certified" or "proved".
- No hypothesis is presented as proved.

## 3. Compile

build/mb_recheck_r1_wrapper.tex has the contract content. Ran `nice -n 15 pdflatex -interaction=nonstopmode
-halt-on-error` twice from build/:
- Both runs exit 0 and produce 16 pages.
- No `!` error, no "Missing $" or runaway message, and no "Label(s) may have changed" on the second run.
- 0 overfull boxes.
- One underfull hbox (source lines 71-78, the axioms paragraph) and one underfull vbox. The same warnings appear in a
  build of the pre-fix snapshot (build/mb_recheck_r1_pre_wrapper.tex), so the fix did not introduce them.
- The undefined references are only fd labels and export labels of ar, cb, lg, ll, mm and sr, including the new
  cb:thm:c2, cb:thm:c3, fd:lem:separation, ll:thm:layers and lg:thm:nesting. No mb label is undefined.

Pipeline note, not a finding against mb: appendix_map.tex was generated at 20:03, before the map edit at 20:39. Its
mb:rem:main3 row still has the old note. Regenerate it with `python3 tools/make_appendix.py` before the next
whole-document build.

## 4. New findings (all minor)

- **m1 (minor), sections/mb.tex:1106.** "the listed subcases of the eight parallelogram hull cases" suggests that
  there are eight parallelogram hull cases. The hull cover has 16 quadrilateral cases P_1, ..., P_16 and 120
  hexagonal ones (136 cubes; C2C34/README.md section 2). The Lean file treats the eight canonical cases P_1-P_8, and
  reduction A (a written proof) pairs P_a with P_(17-a) (C2FINAL/README.md section 1, item 4). cb defines P_a for
  1 <= a <= 8 before it says "the eight hull cases"; mb has no such context. Fix: "the listed subcases of the eight
  canonical parallelogram hull cases $P_1,\dots,P_8$ (to which reduction A reduces the others)".
- **m2 (minor), sections/mb.tex:101-106.** The new sentence separates results used by proofs from results that only
  remarks cite. Theorem mm:thm:even stays in the main "We use" list, but it is cited only in Remark mb:rem:eight
  (line 904, on the duplicate `mirror_eight'`) and in Coverage, never in a proof. Fix: move it to the remarks
  sentence ("Three remarks ...: ..., Remark~\ref{mb:rem:eight} to Theorem~\ref{mm:thm:even}, ...") and drop it from
  the main list. The alternative is to soften the contrast, for example by deleting "further".
- **m3 (minor), sections/mb.tex:116-118.** The sentence uses n both as the generic index of [n] and as the codomain
  in the example f:[k]->[n]. For the domain [k] of f the Lean type is `Fin k`, not `Fin n`. A reader will understand
  it, but the wording is loose. Fix: "Where $[m]$ is the index set of a configuration of $m$ points, or the domain or
  codomain of a cap map (such as $f\colon[k]\to[n]$ in Subsection~\ref{mb:ssec:bridge}), it is the same set viewed as
  Lean's \texttt{Fin m}, as in Definition~\ref{mm:def:config}."

No blocker or major finding remains or was introduced.

# Review mm, round 1, lens: claims, labels and LaTeX

Section: `sections/mm.tex` (920 lines) with `sections/mm.map.tsv` (20 rows).
Verdict: **pass**. There are no blocker or major findings and 11 minor findings, listed below.

Paths below are relative to RES (`cloud/es7-2026-10-19/results`) or to the repository root, as in the contract.

## What was checked, and the results

1. **Lean references (71 `\leanref`s).** A script resolved each `\leanref{Name}{File:Line}` and checked that the line
   declares that name. All 71 resolve exactly: 64 in `MIRRORETV/lean/MirrorMain.lean`, 2 in
   `ErdosSzekeres/Omission/Realization.lean` (`Configuration` :9, `HasCap` :64), and the 5 `cyc_k` and 9 generated
   polygons at their lines.
   - Other line citations in the prose are also correct:
     - `MirrorMain.lean:1587`, the `generalPosition` field of `cfg`;
     - 2542-2557, the inline interior-point argument in `mirror_odd_general`;
     - 2060 and 1716, the local claim `interior` in `mirror_five` and `mirror_seven_of`;
     - 2631 and 2636 (`mirror_seven'`, `mirror_eight'`);
     - `MirrorNine_append.lean:131` (`C12Check.mirror_nine`);
     - the `#print axioms` lines 2662-2677;
     - the Coverage line numbers 1512, 1529, 1676, 1803, 1812, 1820, 1969 and 1977;
     - the `FarFlat.lean` lines 12, 15, 34, 55, 60, 67 and 89.
2. **SHA-256 prefixes (recomputed with `shasum -a 256`).** All 9 match:
   - `MirrorMain.lean` ca623e55a1b9;
   - `Realization.lean` ae4970e0808e;
   - `ConvexCycleCuts.lean` b4ad0ba9e583;
   - `Definitions.lean` 2425500eefd1;
   - `Basic.lean` 13667aa2d3dc;
   - `Orientation.lean` f67955ac7091;
   - `OrientationGeometry.lean` c7db9bbbb65e;
   - `SYMLEAN/mirror/ReductionThreeClasses.lean` 0cc83994fe8c;
   - `FarFlat.lean` 08a79f881eea.

   A read-only `git diff 5bdebbb48 HEAD -- ErdosSzekeres lakefile.lean lake-manifest.json lean-toolchain` is empty. So
   the cited library hashes describe the tree on which the recorded log was produced; the README says that log was made
   at 5bdebbb48. The toolchain claim is correct: `lean-toolchain` is v4.24.0 and the Mathlib rev in `lake-manifest.json`
   is f897ebcf72cd…
3. **Other claims in the Sources paragraph.**
   - "2677 lines": correct.
   - "lines 3-2677 occur verbatim as lines 1562-4236 of `SYMLEAN/mirror/ReductionThreeClasses.lean`, offset +1559":
     verified with `diff`, identical. Part A of that file closes its namespace before Part B, so the context is the same.
   - "Lines 22-1506 generated (5 `cyc_k` and 9 polygons)": consistent with the file. The only `gen_lean.py` in the
     repository is `C2FINAL/gen_lean.py`, an unrelated generator for Central34 data, so "not part of the record" holds.
4. **Axioms logs.**
   - `MIRRORETV/lean/MirrorMain.out` lines 848-863 hold exactly the 16 listed theorems, each with
     [propext, Classical.choice, Quot.sound]. The log has 0 errors and 121 warnings, all "This simp argument is
     unused".
   - Lines 860-861 are `mirror_seven'` and `mirror_eight'`.
   - `MirrorNine.out` line 881 is `C12Check.mirror_nine`, with the standard axioms.
   - `FarFlat.out` prints 5 theorems, all with the standard axioms; see finding 3.
5. **Contents of `MirrorMain.lean`.**
   - It contains no `sorry`, `admit`, `native_decide`, `axiom`, `ofReduceBool`, `implemented_by`, `extern` or `opaque`.
   - In the scoped declarations, `decide` is used only on comparisons of explicit `Fin` elements: in `cyc_k`,
     `hasCap3_of`, `mirror_five` and `mirror_six`. The `Nat.choose` evaluation at line 1532 is in `capacity16`, which is
     out of scope, as the text says.
   - The claim "every other treated declaration is used by one of the 16 printed theorems" was checked by tracing the
     uses, and it holds.
6. **Hypotheses.**
   - (hM) is stated as an explicit, unproved hypothesis in Theorems mm:thm:odd and mm:thm:even and in parts (b) and (c)
     of mm:thm:line. It is quantified exactly as the Lean `hM`: for all n and every configuration, no (j+1)-cap
     (resp. j-cap) and no convex (2j+1)-gon (resp. 2j-gon) imply n ≤ M.
   - M is called an assumed upper bound, not N.
   - The supplying instances are named and checked against the code:
     - (3,16) by `capacity16` in `mirror_seven'`;
     - (4,22) by `capacity22g` in `mirror_eight'`;
     - (4,113) by `capacity113` in `C12Check.mirror_nine`.
   - The small-j observations are correct and labelled as not the Lean route: (2,4) and (3,5) via `capacity_cup` with
     K = 5 and 6, and (2,1) via 2-caps.
   - The index shift (Lean j = j' − 1; k = 3 not covered) is stated correctly.
   - No SAT verdict, Sixfold66, Sevenfold70 or case class is involved, and the section claims none.
7. **Computations and rigor labels.**
   - No statement of the section is a finite computation. The generated polygon lemmas are described accurately: I
     counted 468 `linarith`, 111 `mul_pos` products of the form `y_i·(x_b − x_a) > 0`, distinctness by one coordinate,
     then `cyc_k`.
   - The written proof derives them from the general theorems, so no "computer-assisted" label is needed, and none is
     claimed.
   - The vertex orders passed to `cyc_k` match the Proposition (all 9 checked).
   - Each `cyc_k` has k memberships, C(k,2) distinctness hypotheses and C(k,3) orientation hypotheses, as stated.
   - "Written proofs (not refereed)" is present, and so is "Lean was not re-run".
   - No "verified", "certified" or docstring overclaim is used. For example, `cap_mirror_polygon` is stated as "P has a
     convex 2m-gon", not as the docstring's "is a convex 2m-gon".
8. **"We follow the Lean proof" claims.** These were compared case by case with the Lean code and are accurate:
   - `cap_mirror_polygon` cases 1-4: `orient_mir3`, `orient_mir2` + `cap_below_lines`, `orient_cycl` + `orient_swap12`
     + `cap_below_lines`, `orient_rev` + cap;
   - `axis_left_polygon` / `axis_right_polygon`: the special case r = 0 (resp. r = m − 1), and q indexed by 2m−1−r
     (resp. 2m−2−r);
   - `mirror_odd_general` (keyT, hR, `Aset` split);
   - `mirror_even_general`;
   - the transport proofs;
   - `mirror_four` / `mirror_five` / `mirror_six`, including the parenthetical on the Lean case split of `mirror_five`.

   The `linear_combination` multiples cited for the frame lemmas match the Lean code. The four underlying polynomial
   identities, the mir identities, the middle case of `cap_below_lines`, the identity of `mm:lem:slope`(b) and the
   collinearity identity of `injOn_x` were all checked with sympy, and all hold.
9. **Citations of written sources.** All are accurate:
   - PROOFS.md Lemma 2.1(b) ("Consequences (b)": every 3-subset of a cap is a cap triple);
   - PROOFS.md Lemma 3.1 (hypotheses as paraphrased);
   - the remark after Lemma 3.1, which gives a five-point example that winds twice;
   - the consecutive-triple cap definitions in README §1 and PROOFS §1.
10. **Machine paths and tool names.**
    - A grep of `mm.tex` and `mm.map.tsv` for the four absolute-path prefixes forbidden by the contract, for the
      scratch directory name and for the user name finds nothing.
    - A grep for names of software tools finds one hit, a three-letter match inside the name of the small-matrix
      environment at `mm.tex:692`, which is a false positive.
    - All paths are relative; see finding 9 for the bare file names.
11. **Labels and references.**
    - 21 labels, all `mm:`-prefixed and unique.
    - Every `\ref` target is either an own label, one of the 13 `fd:` labels of the contract, or an `mb:` export label
      (`mb:thm:seven`, `mb:thm:eight`, `mb:thm:nine`, which are defined in `mb.tex`).
    - All 8 export labels of mm are defined, each on the named statement: `mm:def:config`, `mm:lem:slope`,
      `mm:thm:mirror-polygon`, `mm:thm:axis-polygon`, `mm:thm:odd`, `mm:thm:even`, `mm:thm:line`, `mm:thm:small`.
    - Other sections reference only these mm export labels.
    - The `fd:` sub-parts cited (fd:lem:orient (a)/(d), fd:lem:mono (a)-(d)) exist in `fd.tex` with the meaning used.
12. **Map TSV.**
    - The header is correct and every row has 5 columns.
    - There is one row per labelled statement environment (20), with kind, Lean names and file:line identical to the
      `\leanref`s in the head, in the same order.
    - The written step `mm:lem:upper-caps` has `-` for name and line, as required.
    - The notes record hM and the written-step parts.
    - The five unlabelled remarks have no rows; see finding 10.
13. **Coverage.**
    - All 79 `theorem`/`def` declarations of `MirrorMain.lean` are accounted for: covered by label, or listed as not
      covered with a reason. The three small `_line` theorems are covered as "their `_line` versions".
    - The FarFlat lemmas are listed with a reason (not imported by `MirrorMain.lean`, which is correct).
14. **Compile.** From `STAGE/build`, I ran `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error
    -output-directory=claims-mm-r1 mm_wrapper.tex` twice. Both runs exited with 0 and produced 12 pages.
    - No errors and no "Missing $".
    - 0 overfull boxes. There are 73 underfull boxes, from the section's local `\emergencystretch`; they are cosmetic.
    - The only undefined references are `fd:` labels (13 distinct) and `mb:thm:seven`, `mb:thm:eight`, `mb:thm:nine`,
      all expected in the standalone check.
    - There is one hyperref PDF-string warning; see finding 11.

## Findings (all minor)

1. **Unsupported claim about who wrote the code** (`mm.tex:40-42`).
   - The text says "the remaining lines are written by hand."
   - The record does not say this. The header of `MIRRORETV/lean/MirrorMain.lean` (lines 4-11) says only that
     `MirrorPolygons.lean` and `small_polygons.lean` were generated by `gen_lean.py` (certificates from `gen_certs.py`).
     It names the other source files (`MirrorReduction.lean`, `general_section.lean`, `smallk_section.lean`,
     `generalk_section.lean`, `generalk_line.lean`) without saying how they were written. The clause may be inaccurate,
     and nothing in the record supports it.
   - Fix: "the remaining lines were not produced by that script", or drop the clause.
2. **Blanket rigor sentence** (`mm.tex:50`).
   - The text says "Every statement below that carries a Lean reference is Lean-checked."
   - Lemma mm:lem:orient-mir (part (e)) and Lemma mm:lem:slope (part (b)) carry Lean references but contain parts that
     the text itself marks as written steps with no Lean declaration. Each part is clearly marked, so nothing is
     actually misrepresented, but the sentence is imprecise.
   - Fix: add "except the parts marked as written steps".
3. **FarFlat item in Coverage** (`mm.tex:907-913`).
   - The text says "They are inequalities … their recorded axioms (`MIRRORETV/lean/FarFlat.out`) are the standard
     three."
   - `FarFlat.out` prints axioms only for `orient_wzq_neg`, `orient_uqz_neg`, `orient_sum`, `inside_triangle` and
     `line_misses`.
   - `orient_cyclic` (line 55) has no `#print axioms` line (`FarFlat.lean` lines 111-115), and `orient` (line 12) is a
     definition.
   - Also, `orient_sum` and `orient_cyclic` are identities and `inside_triangle` gives barycentric coordinates, so they
     are not inequalities.
   - Fix: "the five theorems printed in `FarFlat.out` use the standard three axioms; `orient_cyclic` is not printed",
     and "estimates and identities" instead of "inequalities".
4. **Remark mm "the hypothesis (hM), and indexing", item (2)** (`mm.tex:653-659).
   - The text says "In README.md and PROOFS.md (Theorem A), M is the number N(2j+1,j+1,2j+1)".
   - This formula is in the Lean indexing. The sources write N(2j−1, j, 2j−1) with their own j (README §2, PROOFS §4).
     Item (3) explains the shift, but item (2) attributes the Lean-indexed formula to the sources without saying so.
   - Fix: add "(in the indexing of Theorem mm:thm:odd; the sources write N(2j'−1, j', 2j'−1), see (3))".
5. **Same remark, item (2): an omission, not an error** (`mm.tex:657-659`).
   - The text says "it is not part of the Lean development".
   - This is true for MirrorOdd. However, the record contains `MIRRORETV/review/MirrorA.lean`, which Lean-checks
     Theorem A directly for the N-type class: `InClass` with consecutive-triple caps, via `cap_all` and
     `cup_convexPos`; `theoremA_even`/`odd`/`_bound`/`_line`, axioms in `review/MirrorA.out`. It covers k = 3 as well.
   - I am unsure whether this must be mentioned, since the review files are declared out of scope in Coverage.
   - Optional fix: one clause noting that an independent Lean version in the N-form exists there.
6. **Same remark, item (1)** (`mm.tex:646-648`).
   - The text says "These instances rest on the repository's Lean formalization of Baek's theorem".
   - The (4,113) instance (`C12Check.capacity113` via `config_capacity113`) also rests on the vendored cups–caps
     theorem `Config.cap_cup` (header of `MIRRORETV/lean/MirrorNine_append.lean`: "by the vendored cups–caps theorem
     `cap_cup 3 6`").
   - Fix: "… Baek's theorem (and, for (4,113), the vendored cups–caps theorem)".
7. **Coverage, first item** (`mm.tex:896-899`).
   - The text says "they use Baek's theorem".
   - `hasNGon_heptagon` (line 1512) does not use `main`. It is the geometric bridge (`boundary_polygon` ∘
     `boundaryOfGon`) from a Config 7-gon to a convex heptagon. The other listed declarations do use `main`, through
     `capacity16`/`capacity22g`.
   - Fix: "they use Baek's theorem or its geometric bridges".
8. **"everything below applies to both copies"** (`mm.tex:45`).
   - For the SYMLEAN copy, the Lean-checked label rests on a different log: `SYMLEAN/mirror/axioms.out`, lines 1-16,
     with the same 16 theorems, standard axioms and no error. This log is not cited.
   - Fix: cite it next to the copy.
9. **Bare file names** (`mm.tex:40, 43, 45, 646, 910`).
   - `\dirn{MirrorMain.lean}` and `\dirn{MirrorNine_append.lean}` are used as shorthand after the full paths. The
     contract asks for paths relative to RES.
   - Fix: write `MIRRORETV/lean/MirrorMain.lean` and `MIRRORETV/lean/MirrorNine_append.lean`.
10. **Remarks not in the map** (`mm.tex:149, 308, 395, 633, 687`).
    - The five `remark` environments are unlabelled and have no map rows.
    - The contract's environment list includes `remark`. Most other sections label remarks and give them map rows: ar,
      cb, ec, ll, mb, oc, pc and sr. fd and lg do not.
    - The remark on (hM) is the remark that contract rule 7 requires, the one naming the supplying records.
    - I am unsure whether remarks count as "statement environments" for the map.
    - Fix, if they do: add `mm:rem:…` labels and rows.
11. **Cosmetic** (`mm.tex:783`).
    - `\subsection{Small $k$}` triggers the hyperref warning "Token not allowed in a PDF string … removing `math
      shift'", so the PDF bookmark reads "Small k".
    - Optional fix: `\texorpdfstring{$k$}{k}`, which is a hyperref command, not a new macro.

## Not findings (checked and correct)

- The index shift is stated correctly, including that k = 3 is not covered by Theorem mm:thm:odd.
- M is presented as an assumed bound, never as N.
- The axioms citations are correct (848-863, 860-861, 881).
- No overclaimed rigor label was found.
- The local `\begingroup\setlength{\emergencystretch}…\endgroup` around the section body is not a new macro. Similar
  local settings appear in ar, ec, fd, oc and pc.

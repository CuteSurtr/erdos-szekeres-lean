# Diff audit of section `mm` (The mirror lemma and Theorem A), polish round 1

**Verdict: pass.** There is no blocker and no major finding. There are 2 minor findings (section 5).

Paths: `sections/`, `snapshots/`, `reviews/` and `build/` are relative to STAGE. `MIRRORETV/...` and `SYMLEAN/...`
are relative to RES. `ErdosSzekeres/...` is relative to the repository root.

## 0. Inputs

- Passed version: `snapshots/sections-r1pass/mm.tex` (920 lines) and `mm.map.tsv` (21 lines, 20 rows).
- Current version: `sections/mm.tex` (961 lines) and `mm.map.tsv` (22 lines, 21 rows).
- `snapshots/polish-r1-pre/mm.*` is byte-identical to `snapshots/sections-r1pass/mm.*`, so the diff consists
  exactly of the fixer's edits.
- Fixer log: `reviews/mm-polish-r1-fix.md`. There are no earlier polish audit reports (`mm-p*-diff.md`,
  `mm-p*-referee.md`).
- Records re-read for this audit:
  - `MIRRORETV/lean/MirrorMain.lean`:
    - header lines 1-21; the comment at 993; the declaration list of 22-1506;
    - all 111 `mul_pos` lines and the `simp only [orient...] at` lines of 22-1506;
    - 1508-1545, 1549-1593, 1676-1860, 1965-1990, 2040-2160, 2200-2316, 2403-2410, 2628-2660.
  - `MIRRORETV/lean/MirrorNine_append.lean` (1-40, 99-140).
  - `MIRRORETV/lean/MirrorMain.out` (848-863), `MirrorNine.out:881`, `FarFlat.out`, `FarFlat.lean`.
  - `MIRRORETV/review/MirrorA.lean` (1-40, 425-450, 685-705) and `MirrorA.out`.
  - `MIRRORETV/README.md` (1-20, 45-86, 178-182) and `MIRRORETV/PROOFS.md` (§1, §2 including Lemma 2.3, §4).
  - `SYMLEAN/mirror/axioms.out`, `SYMLEAN/mirror/README.md` and `SYMLEAN/mirror/ReductionThreeClasses.lean`. For the
    last: grep for forbidden constructs, the namespace and `open` commands before line 1562, and a `diff` of the copy.
  - From the repository: `ErdosSzekeres/Omission/Realization.lean` (9-20, 60-72),
    `ErdosSzekeres/Omission/BaekGeometry.lean:111-125`, `ErdosSzekeres/Omission/Baek.lean`,
    `ErdosSzekeres/Vendor/ETV/Main/Main.lean:87` and `ErdosSzekeres/Vendor/ETV/Main/CapCup.lean:1-46`.
  - `sections/mb.tex` (the statement `mb:thm:baek`).

## 1. Hunk-by-hunk check of `mm.tex`

Line numbers refer to the current `sections/mm.tex`.

| # | location | change | check against the record | result |
|---|---|---|---|---|
| 1 | intro, l. 18 | "every triple of the list, taken in list order" | Claim 1 is `r<s<t`; the Lean `hpos` (`MirrorMain.lean:2247`) is the same | correct |
| 2 | Sources, l. 39-47 | the "written by hand" provenance is replaced by what the header says | see the provenance checks below this table | correct |
| 3 | Sources, l. 47-53 | the SYMLEAN copy's own record is cited | see the SYMLEAN checks below this table | correct |
| 4 | Rigor, l. 58-60 | exception for the written-step parts orient-mir(e) and slope(b); upper-caps carries no Lean reference | the parts are marked in place (l. 115, 240) and the head of upper-caps (l. 561) has no `\leanref` | correct; no rounding up |
| 5 | Rigor, l. 73 | the forward reference now cites `Remark~\ref{mm:rem:hm}` | the label is defined at l. 652 | correct |
| 6 | Dependencies, l. 79-82 | "(for k=9 also with the vendored cups–caps theorem)" | see the cups-caps checks below this table | correct |
| 7 | Conventions, l. 90-92 | `m-1` added to the truncated subtractions | occurs only in `axis_right_polygon` (`hlast : c ⟨m - 1, _⟩ 1 = 0`, `i.val < m - 1`, `:2403-2404`), where `3 ≤ m` | correct |
| 8 | Definition `mm:def:config`(c), l. 148-156 | `xset` defined for every finite T; x-injectivity assumed from `emb` on; note on non-circularity | `xset (T)` at `:1549` takes only `T`; `emb`, `sortPt`, `cfg` (`:1553, 1558, 1584`) take `hx`. Sort (a) (`xset_card`) and (b) (`emb_mem`) involve only `xset` and `emb` | matches Lean exactly; see minor 2 for wording |
| 9 | mirror polygon, Case 4, l. 304-307 | indices renamed α, β, δ; `q_r=c_α` etc. made explicit | δ<β<α follows from r<s<t; `orient_rev` and the cap on (δ,β,α), exactly as the Lean branch `:2270-2277` | correct |
| 10 | Remark after the mirror polygon, l. 323-324 | "every triple q_r,q_s,q_t with r<s<t" | — | correct |
| 11 | axis polygon (a), Claim 2, l. 375-377 | "The case s<m≤r is symmetric" | — | correct |
| 12 | axis polygon (b), Claim 2, l. 403-405 | both-<m / both-≥m sentence added; the mixed case is handled in both orders | (q_s)_1 = y_{2m-2-s} with 0 ≤ 2m-2-s ≤ m-2, hence positive; (q_r)_1 = -y_r ≤ 0 (y_{m-1}=0) | correct; the false "other cases" sentence (adv-m3) is gone |
| 13 | generated polygons, l. 418-427 | products `(c_i)_1 (u_0-v_0) > 0` with u, v two of the lemma's points, v_0<u_0, possibly the axis point a; "(with the cap orientations expanded)" | see the products check below this table | correct |
| 14 | after Proposition `mm:prop:small-polygons`, l. 513-515 | "In Lean, items ... are used in the proofs of ..." | see the item-uses check below this table | correct |
| 15 | upper-caps, l. 570-572 | the parenthetical is restricted to odd, even, small (b), (c); `keyT` (odd case and k=5), `hR` (even case and k=6) | `keyT` at `:2504` (odd) and `:2043` (`mirror_five`); the cap argument sits in `hR` at `:2605` (even) and `:2132` (`mirror_six`). `mirror_four`'s `hR` (`:2022`) has no configuration or cap argument | correct |
| 16 | Remark `mm:rem:hm`, l. 652 | label added | 22 labels in total, unique, all `mm:`-prefixed | correct |
| 17 | Remark `mm:rem:hm`(1), l. 664-669 | full paths; rests on `main` (Theorem `mb:thm:baek`) and, for (4,113), on `Config.cap_cup` | see the Remark (1) checks below this table | correct |
| 18 | Remark `mm:rem:hm`(2), l. 675-689 | the sources' own index j'; derivation of (hM) for M = N; MirrorA mentioned | see the Remark (2) checks below this table | correct; see minor 1 |
| 19 | l. 813 | `\subsection{Small \texorpdfstring{$k$}{k}}` | hyperref is loaded by the preamble; the PDF-string warning is gone (log checked) | correct |
| 20 | small (b), l. 865-871 | substitutions spelled out: (g) with (a,c_0,c_1):=(c_2,c_0,c_1); (f) with (a,c_0,c_1):=(c_0,c_1,c_2) | see the `mirror_five` check below this table | correct |
| 21 | Coverage, l. 921-926 | the three written-step items; part (e) "used implicitly" by `cap_below_lines` | `cap_below_lines` (`:2204-2231`) expands `orient` with `simp only [orient, mir_zero, mir_one]` in each of its five branches and closes each by `nlinarith` | correct |
| 22 | Coverage, l. 930-937 | the role of `hasNGon_heptagon`; how the others rest on `main` | see the Coverage checks below this table | correct |
| 23 | Coverage, l. 940-941 | `Remark~\ref{mm:rem:hm}` | — | correct |
| 24 | Coverage, FarFlat, l. 945-954 | "definition `orient`"; 3 estimates, 2 identities, 1 barycentric representation; axioms printed for 5 of the 6 theorems | see the FarFlat checks below this table | correct |

Details for the hunks that need them:

- **Hunk 2: provenance.**
  - The header is lines 4-10 (`/-! Mirror polygons ...` to `generalk_line.lean. -/`). It describes the 4-cap
    polygons and says: "Every orientation inequality is closed by `linarith` with an exact certificate found offline
    (gen_certs.py). Assembled from MirrorPolygons.lean and small_polygons.lean (generated by gen_lean.py),
    MirrorReduction.lean, …".
  - Line 993 reads `### Small k: mirror polygons for caps of length 2 and 3 (generated by gen_lean.py)`.
  - Lines 22-1506 hold exactly `cyc7`, `cyc8`, `cyc4`-`cyc6` and the nine polygons (plus one `set_option`). Line 1506
    ends `axis_right_pentagon`, and line 1508 opens `section Baek17`.
  - No `gen_*` file exists under `MIRRORETV`. In the repository, the only one is the unrelated `C2FINAL/gen_lean.py`.
    No file named `MirrorPolygons.lean`, `small_polygons.lean` or `gen_certs.py` exists anywhere.
- **Hunk 3: the SYMLEAN copy.**
  - `SYMLEAN/mirror/axioms.out` lines 1-16 list exactly the sixteen theorems of the Rigor paragraph, each with
    `[propext, Classical.choice, Quot.sound]`.
  - `SYMLEAN/mirror/README.md` §3 reports "exit 0, 121 linter warnings (unused simp arguments), no errors".
  - `ReductionThreeClasses.lean` contains no `sorry`, `admit`, `native_decide`, `axiom` or `ofReduceBool`.
  - Every `open` command before line 1562 is inside `ErdosSzekeres.SymReduction`, which closes at 1559.
  - The copy is verbatim: `diff` of `MirrorMain.lean` 3-2677 against `ReductionThreeClasses.lean` 1562-4236 is empty.
- **Hunk 6: the cups-caps theorem.**
  - `C12Check.capacity113` uses `config_capacity113`, which calls `main 6` and `C.cap_cup 3 6`
    (`MirrorNine_append.lean:37, 60, 116-121`).
  - `capacity16` and `capacity22g` do not use `cap_cup`. No vendored file other than `CapCup.lean` mentions
    `cap_cup`, and `Main.lean` does not import it.
- **Hunk 13: the auxiliary products.**
  - All 111 `mul_pos` lines in 22-1506 have the form `ci 1 * (X 0 - Y 0)` with X, Y ∈ {c0..c3, a}, proved by
    `mul_pos yi (by linarith)`.
  - 26 of them involve `a 0`.
  - The cap orientations are expanded by `simp only [orient(, ha)] at o012 …` in all 8 lemmas that have them.
  - Only `linarith` is used in this range (no `nlinarith`).
- **Hunk 14: the uses of the nine items.**
  - (a): `:2033-2034` (`mirror_four`).
  - (b), (g), (f): `:2068`, `:2076`, `:2088` (`mirror_five`).
  - (c): `:2147` (`mirror_six`).
  - (d), (h), (i): `:1805` (`mirror_seven`).
  - (e): `:1839` (`mirror_eight`).
- **Hunk 17: Remark (1).**
  - The full paths are `MIRRORETV/lean/MirrorNine_append.lean` and `MIRRORETV/lean/MirrorMain.lean`.
  - `main` is the root-namespace theorem at `ErdosSzekeres/Vendor/ETV/Main/Main.lean:87`. It is exactly the
    declaration of `mb:thm:baek` (`mb.tex:183`).
  - `Config.cap_cup` is at `ErdosSzekeres/Vendor/ETV/Main/CapCup.lean:46` (namespace `Config`, no enclosing
    namespace).
  - `mirror_seven'` and `mirror_eight'` (`:2631, 2636`) call `capacity16` and `capacity22g`. `mirror_nine`
    (`MirrorNine_append.lean:131`) calls `capacity113`.
- **Hunk 18: Remark (2).**
  - README l. 6-10 and 59 and PROOFS §1 and §4 state Theorem A with N(2j,j,2j) (even case) and N(2j-1,j,2j-1) (odd
    case), using r_j and r'_j. Caps and cups are defined by consecutive triples (README l. 49-50, PROOFS §1).
  - The index translation j' = j+1 (odd) and j' = j (even) is right, and agrees with README l. 78 ("the Lean j is the
    j − 1 of the text").
  - The derivation of (hM) for M = N is valid. pts(C) is x-distinct and in general position. A consecutive (j+1)-cap
    would be an all-triples cap by PROOFS Lemma 2.1, Consequences (b). A (2j+1)-cup would be a convex (2j+1)-gon by
    PROOFS §1 ("A 2j-cup is a convex 2j-gon … likewise"). Since C is injective, n = |pts(C)| ≤ N.
  - `MirrorA.lean` imports only Mathlib (line 1) and has its own definitions. README l. 82-83 calls it an
    independent formalization by a review, importing only Mathlib.
  - `theoremA_odd_bound` (`:694`) has `hN : ∀ X, InClass (2*j-1) j (2*j-1) X → X.card ≤ Nb`. `InClass` (`:445`) is
    "XDistinct, GenPos, ¬HasGon n, ¬HasCap a, ¬HasCup b". So the description is exact, with MirrorA's j equal to j'.
  - No rigor label is claimed for MirrorA.
- **Hunk 20: the case split of `mirror_five`.**
  - `:2076`: `axis_right_pentagon (c 2) (c 0) (c 1)`, branch y0>0, y2=0.
  - `:2088`: `axis_left_pentagon (c 0) (c 1) (c 2)`, branch y0=0.
  - `:2068`: `cap_mirror_pentagon`, all three ordinates positive.
  - `:2070`: `interior`, the case y1=0.
- **Hunk 22: Coverage, first item.**
  - `hasNGon_heptagon` (`:1512-1525`) turns `(colorConfig c.cup true).HasNGon 7 (Finset.range n)` into
    `HasConvexNGon 7 (univ.image c.point)`. It is used only by `capacity16` (`:1537`), and `colorConfig` exists
    (`ErdosSzekeres/Omission/ActualRanks.lean:28`).
  - `capacity16` calls `main 4` directly (`:1535`).
  - `capacity22g` calls `geometric_capacity22`, which calls `Baek.capacity22`, which calls `main 5` through
    `four_cap_or_eight_gon` (`BaekGeometry.lean:111-116`, `Baek.lean:12-20`).
  - Of the remaining five: `mirror_seven_of` applies `capacity16` (`:1701`); `mirror_seven` goes through
    `mirror_seven_of`; `mirror_eight` applies `capacity22g`; the two `_line` versions go through `mirror_seven` and
    `mirror_eight`.
- **Hunk 24: FarFlat.**
  - `orient` is a `def` (`FarFlat.lean:12`).
  - The two orientation estimates are `orient_wzq_neg` and `orient_uqz_neg` (`< 0`). `line_misses` gives `orient ≠ 0`
    by sign estimates.
  - The two identities are `orient_cyclic` and `orient_sum` (`ring`). `inside_triangle` gives barycentric
    coordinates.
  - `FarFlat.out` prints exactly 5 lines (all but `orient_cyclic`), each with the standard three axioms.

**Map (`mm.map.tsv`).**
- The `mm:thm:mirror-polygon` note was changed to the list-order wording (rig-1).
- The `mm:thm:odd` note now reads "Lean j (used in this section) = README/PROOFS j minus 1" (fid-5). This agrees with
  README l. 78.
- A new row `mm:rem:hm` (kind `remark`, `-`, `-`) gives an accurate note: the instances (3,16), (4,22), (4,113) via
  `capacity16`, `capacity22g` and `capacity113`, with Baek and, for (4,113), cups-caps.
- Every row has 5 tab-separated fields and all fields are ASCII. The rows follow the 21 labelled environments in
  order. No `\leanref` and no Lean column changed, so all statement heads still equal their rows.

**Touched statements re-read against Lean.**
- Definition `mm:def:config`: `Configuration`, `HasCap` (`Realization.lean:9, 64`), `xset`, `emb`, `sortPt`, `cfg`.
- The statements of `cap_mirror_polygon` (`:2233`) and `axis_left_polygon`/`axis_right_polygon` (`:2309, 2403`),
  whose proofs were edited.
- `mirror_five` (`:2040`), whose described proof was edited.
- The upper-caps lemma (written step; its content is unchanged) and Remark `mm:rem:hm` (no statement).
- No statement changed its mathematical content, and every statement with a Lean reference still matches its
  declaration exactly: hypotheses, quantifier order, maps-into symmetry, strict vs weak inequalities, truncated
  subtraction.

## 2. The fixer's dispositions

| finding(s) | disposition | audit |
|---|---|---|
| fid-1, rig-6, adv-m2, cl-1 (provenance "written by hand") | fixed / duplicates | fixed correctly (hunk 2): only what the header and l. 993 say |
| fid-2, rig-5, adv-m5, cl-3 (FarFlat axioms; "inequalities") | fixed / duplicates | fixed correctly (hunk 24) |
| fid-3, cl-7 (`hasNGon_heptagon` does not use Baek) | fixed / duplicate | fixed correctly, more precisely than asked (hunk 22) |
| fid-4, rig-9, cl-4 (indexing of the sources' formula) | fixed / duplicates | fixed correctly (hunk 18) |
| fid-5, adv-m1 (map note) | fixed / duplicate | fixed correctly |
| fid-6, rig-3, adv-m6, cl-2 (blanket Lean-checked sentence) | fixed / duplicates | fixed correctly (hunk 4) |
| fid-7, adv-m7 (`xset` restricted; forward references) | fixed / duplicate | fixed correctly (hunk 8) |
| fid-8, rig-4 (product notation; axis abscissa) | fixed / duplicate | fixed correctly (hunk 13) |
| rig-1 ("every ordered triple") | fixed | fixed in all three places (intro, remark, map) |
| rig-2, adv-m3 (Claim 2 of axis polygon) | fixed / duplicate | fixed correctly in (a) and (b) (hunks 11, 12) |
| rig-7, adv-m4 (implicit relabelling in small (b)) | fixed / duplicate | fixed correctly (hunk 20) |
| rig-8 (index letters a, b, d) | fixed | fixed correctly (hunk 9) |
| adv-m8, cl-5 (`review/MirrorA.lean` ignored) | fixed / duplicate | fixed correctly (hunk 18) |
| cl-6 (the (4,113) instance also rests on `cap_cup`) | fixed | fixed correctly in Remark (1) and in Dependencies (hunks 6, 17) |
| cl-8 (the SYMLEAN copy's log not cited) | fixed | fixed correctly (hunk 3) |
| cl-9 (bare file names) | fixed | fixed: no bare `MirrorMain.lean` or `MirrorNine_append.lean` is left. The four new bare names (`gen_certs.py`, `MirrorPolygons.lean`, `small_polygons.lean`, `gen_lean.py`) are names quoted from the header for files that do not exist in the repository, so no RES path exists; acceptable |
| cl-11 (hyperref PDF-string warning) | fixed | fixed (hunk 19) |
| fid-9, cl-10 (unlabelled remarks without map rows) | declined in part (the (hM) remark got a label and a row) | acceptable: not an inaccuracy. The four remaining remarks state nothing tied to a Lean declaration. `tools/make_appendix.py` prints "Labelled remarks appear where a section lists them". Observation for the editor: 9 of the 11 sections now give every remark a row (fd now does too), while mm has 1 of 5 and lg 0 of 8 |
| writer concerns | no change | acceptable; the preamble now handles statement heads, and the local `\emergencystretch` group causes no overfull box |

Side note on the fix log (not on the section): the log says "13 [products] involve `a 0`". The count is 26: 9 in
each axis heptagon and 4 in each axis pentagon. The section states no count, so nothing in the text depends on it.

## 3. Compile check

- Wrapper: `build/mm_p1diff_wrapper.tex`, same content as the contract's wrapper.
- Ran `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error mm_p1diff_wrapper.tex` twice from `build/`. Both
  runs exited 0 and produced 13 pages.
- The log has no `!` line, no error and no "Missing $".
- There are **0 overfull boxes**, so there is no minor finding from this item. There are 76 underfull boxes, from the
  section's local `\emergencystretch`; they are cosmetic.
- The only undefined references are the 13 contract `fd:` labels and the `mb` export labels `mb:thm:baek`,
  `mb:thm:seven`, `mb:thm:eight` and `mb:thm:nine`, all of which `mb.tex` defines. There is no other LaTeX or
  package warning, and the hyperref "Token not allowed" warning is gone.
- A text extraction of the PDF confirms that the new passages render as intended: `gen_certs.py`, §1, j′, the
  Rigor exceptions and "Remark 1.19".
- Files left in `build/`: `mm_p1diff_wrapper.{tex,aux,log,out,pdf,txt}`, `mm_p1diff_pass1.out` and
  `mm_p1diff_pass2.out`.

## 4. Other checks

- No machine path and no tool name appear in `mm.tex` or `mm.map.tsv`.
- The section has no `\newcommand`, `\usepackage` or other macro definition.
- No "verified" or "certified" appears. "certificate" occurs only for the `linarith` certificates. "proved" occurs
  only in "not proved here" and for Lean proofs.
- Every `\ref` points to an own label, a contract `fd:` label or an `mb` export label (`mb:thm:baek` is one).
- The 8 export labels are unchanged and sit on the same statements.
- Hypotheses stay hypotheses: (hM) is still stated as an unproved hypothesis. Its discharges are attributed only to
  the theorems `capacity16`, `capacity22g` and `capacity113`, whose dependents' axioms are recorded. The derivation
  for M = N is marked as written in the sources and not used.

## 5. Findings

1. **minor — citation order in Remark `mm:rem:hm`(2)** (`sections/mm.tex:682-684`).
   - **Issue:** "two facts stated in writing in `MIRRORETV/PROOFS.md` (§1 and Lemma 2.1(b)): consecutive clockwise
     triples imply that all increasing triples are clockwise, and a cup is in convex position". The sources are
     listed in the reverse order of the facts:
     - the first fact is PROOFS Lemma 2.1, Consequences (b);
     - the second is in §1 ("A 2j-cup is a convex 2j-gon", also Lemma 2.3).

     A reader who looks up §1 for the first fact will not find it.
   - **Fix:** "(Lemma 2.1(b) and §1, respectively)".
2. **minor — wording in Definition `mm:def:config`(c), (d)** (`sections/mm.tex:148-149, 157`).
   - **Issue:** "Now let $T$ be moreover $x$-injective" is awkward, and (d) repeats "moreover". The content is right
     and matches Lean.
   - **Fix:** "From now on let $T$ also be $x$-injective."

No blocker and no major finding: the diff introduces no false statement, no Lean mismatch, no unsupported claim about
the records, no rounded-up rigor label and no LaTeX problem.

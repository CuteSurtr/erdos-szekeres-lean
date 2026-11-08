# Review of section `mm` (The mirror lemma and Theorem A): round 1, lens: rigor

Verdict: **pass**. I found no blocker and no major finding. There are nine minor findings, listed at the end.

Paths are relative to STAGE (`sections/`, `build/`, `inventory/`), to RES (`MIRRORETV/...`, `SYMLEAN/...`), or to the
repository root (`ErdosSzekeres/...`), as the contract requires.

## What was checked, and how

### 1. Statements against Lean (every declaration in scope)

I read `MIRRORETV/lean/MirrorMain.lean` lines 1-21 and 1506-2677 in full, the headers and several bodies of the
generated lemmas (lines 22-1506), `ErdosSzekeres/Omission/Realization.lean` (Configuration, HasCap),
`ErdosSzekeres/ConvexCycleCuts.lean` (positive-cycle lemma), `ErdosSzekeres/Definitions.lean` and
`ErdosSzekeres/Basic.lean`. Each written statement was compared hypothesis by hypothesis with its Lean declaration.

- **Definitions.** `mir`, `Rset` (strict `0 < p 1`), `Aset` (`p 1 = 0`): exact. `Configuration` (strictly increasing
  abscissae; `orient ≠ 0` on increasing triples), `HasCap` (strictly increasing `f : Fin k → Fin n`, ALL increasing
  triples `< 0`): exact. `xset`, `emb` (`orderEmbOfFin`), `sortPt` (`Classical.choose`), `cfg`: exact.
  `lineRefl`, `frame`, `unframeLin`, `unframe`: the four coordinate formulas agree with lines 1879-1894.
- **Small lemmas.** `mir_zero/one`, `mir_mir`, `orient_mir3`, `orient_mir2`, `orient_cycl`, `orient_swap12`,
  `orient_rev`: exact. `xset_card`, `emb_mem`, `sortPt_mem/x/strictMono/injective/image`: exact; part (h) of the
  sorting lemma is the `generalPosition` field of `cfg` (line 1587). `hasConvexNGon_of_le` (`n ≤ m`) and
  `hasConvexNGon_affineMap` (injective affine map, image set): exact.
- **`cap_below_lines`.** Hypotheses `StrictMono x`, `∀ i, 0 ≤ c i 1`, all-triples cap; implicit `i j`, explicit
  `l`, `i < j`, `0 < c l 1`; conclusion `orient (c i) (c j) (mir (c l)) < 0`. The text has exactly these.
- **`cap_mirror_polygon`** (`2 ≤ m`, `0 < c i 1` for all `i`, cap, `c i ∈ P`, `mir (c i) ∈ P`,
  `HasConvexNGon (2*m) P`), **`axis_left_polygon`** (`3 ≤ m`, `c ⟨0⟩ 1 = 0`, `0 < i.val → 0 < c i 1`) and
  **`axis_right_polygon`** (`3 ≤ m`, `c ⟨m-1⟩ 1 = 0`, `i.val < m-1 → 0 < c i 1`), conclusion
  `HasConvexNGon (2*m-1) P` with truncated subtraction harmless since `m ≥ 3`: exact.
- **`cyc4`-`cyc8`**: `k` memberships, `C(k,2)` disequalities, `C(k,3)` hypotheses `0 < orient q_r q_s q_t`
  (I counted 56 for `cyc8`): exact.
- **The nine generated polygons** (lines 212, 392, 639, 816, 1126, 1168, 1282, 1358, 1433): I compared all nine headers
  with items (a)-(i). Hypotheses (x-order, positivity, the listed orientations, `a 1 = 0`) and the membership lists
  (pentagon without `c0`, heptagon without `mir c0`) match. I also checked that the vertex orders passed to `cyc_k`
  (lines 388, 635, 812, 989, 1164, 1278, 1354, 1429, 1504) are exactly the orders in which the memberships are listed,
  as the text claims.
- **`card_split`** (no general position), **`card_A_le`**, **`injOn_x`** (`T ⊆ S`, `0 ≤ p 1` on `T`, at most one
  axis point): exact.
- **`mirror_odd_general`**: `(j M) (hj : 2 ≤ j)`, `hM : ∀ n (c : Configuration n), ¬ c.HasCap (j+1) →
  ¬ HasConvexNGon (2*j+1) (univ.image c.point) → n ≤ M`, then `S gp sym noGon`, conclusion `S.card ≤ 2*M`. The
  text states (hM) with the same quantifier order and says that it is an unproved hypothesis, part of the statement,
  and that `M` is an assumed bound and not `N` itself.
  **`mirror_even_general`**: `HasCap j`, `2*j`, `2*M+2`: exact.
- **`transport`** (four conclusions (i)-(iv)), **`mirror_odd_general_line`**, **`mirror_even_general_line`**
  (`n0^2+n1^2 = 1`, `lineRefl` symmetry): exact.
- **`hasCap3_of`** and **`capacity_cup`** (`4 ≤ K`, no 3-cap, no `K`-gon in `univ.image c.point`, `n ≤ K - 1`):
  exact.
- **`mirror_four/five/six`** and their `_line` versions: exact, with no extra hypotheses.

There is no silent strengthening or weakening. The index shift is stated correctly: Lean `j` = written `j' − 1` in
the odd case, and `2 ≤ j` excludes `k = 3`.

### 2. Proofs, step by step

- **Lemma `mm:lem:orient-mir`.** (b), (e) are explicit expansions, and (c) follows from (b) and `mir ∘ mir = id`.
  (d) is correctly attributed to the sign rule of `fd:lem:orient`(d): one 3-cycle (+1) and two transpositions (−1).
- **Lemma `mm:lem:sort`.** (a)-(h) are each correct. (g) is the subset-of-equal-cardinality argument (as in Lean
  `eq_of_subset_of_card_le`). (h) gets pairwise distinctness from (f) and membership from (c). There is no
  circularity: the definition in part (c) uses only (a) and (b), which depend only on `xset` and `emb`.
- **Lemma `mm:lem:ngon`.** For (b), affine maps preserve affine combinations, so `f(conv Y) = conv f(Y)`. Injectivity
  gives `f(T)∖{f p} = f(T∖{p})`, and then `p ∈ conv(T∖{p})` gives a contradiction. Complete.
- **Lemma `mm:lem:slope`(a)** (`cap_below_lines`). The five positions `l<i`, `l=i`, `i<l<j`, `l=j`, `l>j` are
  exhaustive. Each sign argument is correct:
  - `l<i` and `l>j`: the cap gives a negative first term of `(*)`.
  - `l=i` or `l=j`: the first term is 0.
  - `i<l<j`: the expansion has three nonpositive terms and the first is strictly negative.

  The in-words gloss (right of the directed chord means below the line, since `x_i < x_j`) is correct.
  **(b)**: the expansion with `a_1 = 0` is correct, and `≥ 0` needs exactly `p_0<a_0<q_0` and `p_1, q_1 ≥ 0`.
- **Theorem `mm:thm:mirror-polygon`.** The cyclic order is `q_r = mir c_r` for `r<m` and `q_r = c_{2m-1-r}`
  otherwise. Claim 1 splits into Cases 1-4 by how many of `r<s<t` are `< m`; these are exhaustive and disjoint.
  - Case 1 uses `orient_mir3` and the cap.
  - Case 2 uses `orient_mir2` and slope(a) with `(r,s,u)`, `y_u > 0`.
  - Case 3 rotates and swaps to `-orient(c_u, c_{u'}, mir c_r)`, with `u<u'` since `s<t`, then applies slope(a)
    with `(u,u',r)`, `y_r>0`.
  - Case 4 uses `orient_rev` and the cap on `d<b<a`.

  Every hypothesis of slope(a) is met: all `y ≥ 0`. Claim 2 (injectivity) covers both-lower, mixed (with the
  symmetric case) and both-upper. The positive-cycle lemma is applied with `N=k=2m ≥ 4`, `p=q`, `e=id`, `P`: these
  are exactly its hypotheses as stated in `fd:lem:pos-cycle`. This is the Lean route, and it proves positivity of
  every increasing triple in full, as the task notes require.
- **Theorem `mm:thm:axis-polygon`.**
  - (a): `mir c_0 = c_0`, and the list has `2m-1` entries. Upper indices `2m-1-r` lie in `{1..m-1}`, hence
    `y > 0`. Case 3a (`r=0`) uses `orient(c_0,c_{u'},c_u) = -orient(c_0,c_u,c_{u'})` (`fd:lem:orient`(a)) and the
    cap with `0<u<u'`. Case 3b (`r ≥ 1`) has `y_r > 0`. Case 2 with `r=0` is still covered, because the `orient_mir2`
    identity holds for all points.
  - (b): upper indices `2m-2-r` lie in `{0..m-2}`. Case 3a (`r=m-1`) uses `orient_rev` and the cap on
    `u<u'<m-1`.

  Claim 2 is correct in both parts: `(q_r)_1 = -y_r ≤ 0 < (q_s)_1`. `2m-1 ≥ 5 ≥ 4`. The Case 3 split matches the
  Lean proofs (`MIRRORETV/lean/MirrorMain.lean` lines 2346-2364 and 2440-2457).
- **Lemma `mm:lem:cyc`, Proposition `mm:prop:small-polygons`.**
  - (a), (c), (e) are the mirror theorem with `m=2,3,4`; the listed orientations are exactly the triples of `[m]`.
  - (f), (h) are axis-(a) with `(a,c_0[,c_1],c_1/c_2)`, using `mir a = a`. (g), (i) are axis-(b).
  - (b) and (d) are proved as subsets of the 6- and 8-point sets: (c) or (e) applied to `Q` forces `T = Q`, hence the
    points are distinct and `Q` is in convex position; then a 5- or 7-subset follows by `fd:lem:mono`(a).

  The order (c), (e) before (b), (d) avoids circularity. Correct.
- **Lemma `mm:lem:count`.** (a) is the trichotomy plus the bijection `mir: R(S) → N`; (b) holds because three axis
  points have `orient = 0`. Correct.
- **Lemma `mm:lem:injx`.** `p`, `q` and `mir p` are pairwise distinct for the stated reasons, and the orientation
  vanishes when `q_0 = p_0`. The case analysis on `p_1`, `q_1` is exhaustive. Correct.
- **Lemma `mm:lem:upper-caps`** (written step).
  - (a) is the mirror theorem.
  - (b): if all points are above the axis, the mirror theorem gives a `2m`-gon, hence a `(2m−1)`-gon. Otherwise
    there is a unique axis point `i_0`: uniqueness follows from the hypothesis on axis points and the x-order. The
    cases `i_0=0`, `i_0=m-1`, `0<i_0<m-1` are exhaustive, and the interior case is excluded by slope(b). Every
    hypothesis of axis-(a) and axis-(b) is checked, including `m ≥ 3`.
- **Theorems `mm:thm:odd`, `mm:thm:even`.** In the odd case, Step 1 uses upper-caps(b) with `m=j+1 ≥ 3` and the
  identity `2(j+1)-1 = 2j+1`; (hM) is applied with `n=|T|`. Step 3 uses `|R|+1 ≤ M ⇒ 2|R|+2 ≤ 2M`. In the even case
  upper-caps(a) is used with `m=j ≥ 2`. Both match the Lean proofs (`keyT` and `hR`) and are complete.
- **Remark (hM).** I checked each instance claim:
  - `capacity16` and `capacity113` are (hM) for odd `(3,16)` and `(4,113)`.
  - `capacity22g` is (hM) for even `(4,22)`.
  - `capacity_cup` with `K=5` and `K=6` is exactly (hM) for odd `(2,4)` and even `(3,5)`.
  - Even `(2,1)` holds since `n ≥ 2` gives a 2-cap.
  - `2·4=8`, `2·5+2=12` and `2·1+2=4` match Theorem `mm:thm:small`.

  The relation to `N(n,a,b)` is correct: the passage from consecutive to all-triples caps needs `PROOFS.md`
  Lemma 2.1(b), and a cup is in convex position. The remark labels this correctly as not part of the Lean
  development.
- **Definition and Lemma `mm:lem:frame`.** The polynomial identities (see §3) are correct for all `n0, n1, c`, and
  setting `s=1` gives (a)-(d). For (e), left inverses give injectivity. The remark's claims (reflection, rotation by
  a determinant-1 matrix, line onto axis) are correct.
- **Theorem `mm:thm:line`.**
  - (a)(i): distinct images come from distinct preimages, then use `orient_frame` and `fd:lem:collinear`.
  - (a)(ii): use `frame_lineRefl`.
  - (a)(iii): pull back along the injective affine `unframe` with `unframe ∘ frame = id`.
  - (a)(iv): `frame` is injective.
  - (b), (c): apply (a), then Theorem `mm:thm:odd` or `mm:thm:even`.

  Complete.
- **Lemma `mm:lem:cup`.** (a) is direct. For (b), `n ≥ K` and the inclusion `e` give increasing triples whose
  orientations are `≠ 0` (configuration) and not `< 0` (else (a) gives a 3-cap), hence `> 0`. The positive-cycle
  lemma then applies with `N=n`, `k=K ≥ 4`; `p=C` is injective by the x-order. Complete.
- **Theorem `mm:thm:small`.**
  - (a): `|R| ≤ 1` via `injOn_x` and item (a), then `|S| ≤ 4`.
  - (b): the Step 1/2/3 counting gives `≤ 8`.
  - (c): `≤ 2·5+2 = 12`.
  - (d)-(f): transport.

  Complete. The Lean case split described for `mirror_five` matches lines 2065-2088.

Nothing is delegated to Lean. Every proof is a complete written argument. The generated lemmas get a genuine hand
proof (a different one from the Lean proof), so no "computer-assisted" label is needed. The text describes the Lean
proofs correctly as `linarith` with generated certificates.

### 3. Symbolic and numeric checks

- `build/mm_r1rigor_sympy.py` (output `build/mm_r1rigor_sympy.out`) checks **53 identities, all OK**:
  - Lemma orient-mir (b)-(e), including both displayed intermediate expressions.
  - Slope(a): `(*)`, the case expansion and the degenerate cases. Slope(b): both forms.
  - The rotation and swap chains of Cases 3, 3a and 4, and count(b).
  - `injOn_x`: the displayed expression.
  - `frame`: the explicit form `Rp − (0,cs)`. `unframe∘frame` and `frame∘unframe`, with every displayed
    intermediate. `lineRefl = p − 2λn`, `Rn = (0,s)`, `frame∘lineRefl − mir∘frame = (0, −2(s−1)(n0p0+n1p1))`, and
    `orient_frame = s·orient`.
  - All six Lean `linear_combination` certificates quoted in the text (multiples `p0−cn0`, `p1−cn1`, `q0`, `q1`,
    `−2(n0p0+n1p1)`, `orient(a,b,d)` of `s−1`).
  - The remark's `λ(lineRefl p) = λ − 2λs` and the invariance of `n1x − n0y`.
- `build/mm_r1rigor_numeric.py` (output `build/mm_r1rigor_numeric.out`) is an exact rational sanity check of the three
  cyclic orders, exactly as written (`2m−1−r` and `2m−2−r`), and of slope(a), on 400 random concave caps with
  `m = 2..9` (axis versions for `m ≥ 3`). It checked 299,028 increasing triples with 0 failures, and 0 violations of
  slope(a) in the case `i<l<j` with `y_i, y_j ≥ 0` (zeros allowed).
- `build/mm_r1rigor_fivept.py` checks the five-point example cited from `MIRRORETV/PROOFS.md` (remark after
  Lemma 3.1). All five turns are left (701, 8580, 17966, 15889, 6259), and `(-18,-62)` is strictly inside the
  triangle (signs 2080, 7306, 8580). The remark's warning is therefore justified.

### 4. Records, references, compile

- **SHA-256 prefixes.** All nine are correct: `MirrorMain.lean` ca623e55a1b9 (2677 lines), `Realization.lean`
  ae4970e0808e, `ConvexCycleCuts.lean` b4ad0ba9e583, `Definitions.lean` 2425500eefd1, `Basic.lean` 13667aa2d3dc,
  `Orientation.lean` f67955ac7091, `OrientationGeometry.lean` c7db9bbbb65e, `ReductionThreeClasses.lean`
  0cc83994fe8c, `FarFlat.lean` 08a79f881eea.
- **Copy claim.** `diff` of `MirrorMain.lean` lines 3-2677 against `SYMLEAN/mirror/ReductionThreeClasses.lean` lines
  1562-4236 shows them identical. The offset is +1559. In the copy, `namespace MirrorOdd` opens at line 1571 and
  closes at line 4219, after `ErdosSzekeres.SymReduction` has been closed at line 1559. So the full names agree, and
  "applies to both copies" holds.
- **Toolchain.** `lean-toolchain` is v4.24.0, and `lake-manifest.json` has Mathlib rev f897ebcf.
- **Axioms.** `MirrorMain.out` lines 848-863 hold exactly the 16 named theorems with
  `[propext, Classical.choice, Quot.sound]`. Lines 860-861 are `mirror_seven'` and `mirror_eight'`. The log has 0
  errors and 121 warnings, all unused-simp-argument. `MirrorNine.out:881` is `C12Check.mirror_nine`, and
  `MirrorNine_append.lean:131` is its declaration line.
- **Forbidden constructs.** The file contains no `sorry`, `admit`, `native_decide`, `axiom` or `ofReduceBool`. In the
  treated declarations, `decide` only compares `Fin` elements; the only other `decide` is `Nat.choose` at line 1532,
  inside `capacity16`, which is out of scope.
- **Line numbers.** Every `\leanref` line number and every line cited in the text is exact, including:
  - 1587 (`cfg` field);
  - 2542-2557, 2060 and 1716 (interior arguments);
  - 1512, 1529, 1676, 1803, 1812, 1820, 1969, 1977, 2631, 2636 and 2662-2677 (Coverage);
  - `Realization.lean` 9 and 64;
  - `FarFlat.lean` 12, 15, 34, 55, 60, 67, 89.
- **Dependency claim.** The Rigor paragraph says every other treated declaration is used by one of the 16 printed
  theorems. This holds (e.g. `unframe_apply` → `unframe_frame` → `transport`; `frame_unframe` →
  `unframe_injective`; `hasConvexNGon_of_le` → `mirror_odd_general`).
- **Compile check.** `build/mm_r1rigor_wrapper.tex`, two passes of `nice -n 15 pdflatex`, both exit 0. The only
  undefined references are `fd:` labels (all in the contract's list) and `mb:thm:seven`, `mb:thm:eight`,
  `mb:thm:nine` (export labels of `mb`). There are no errors and no overfull boxes; 73 underfull boxes are style only.
- **Labels and map.** All 20 statement environments have `mm:` labels, and the map has the same 20 rows in the same
  order, five tab-separated columns each. All eight export labels sit on the right statements. Every `\ref` is to
  `mm:`, an allowed `fd:` label or an `mb:` export label.
- **Forbidden content.** The section and its map contain no machine paths and no tool names.
  "Verified" and "certified" do not occur; "proved" is used only neutrally.
- **Coverage.** Every declaration of `MirrorMain.lean` is accounted for, either covered or deliberately excluded
  with a reason. The FarFlat lemmas are not used by anything in scope: the file imports only Mathlib and is not
  imported. They are listed in Coverage, as the task requires.

Side note, not a finding: `MirrorOdd.hasConvexNGon_of_le` is mapped both in `fd` (`fd:lem:mono`(d)) and here
(`mm:lem:ngon`(a)). The text says "This is Lemma fd:lem:mono(d)", so the double mapping is consistent.

## Findings

All findings are minor. None affects correctness.

1. **minor: ambiguous "every ordered triple"** (`sections/mm.tex` lines 17-18 and 309-310).
   - **Issue:** "checks that every ordered triple of the list is counterclockwise" and "checks the sign of every
     ordered triple of the list q" can be read as all orderings of three points. For those the claim is false, since
     `orient` is alternating. Claim 1 itself (line 275) is precise: `r<s<t`.
   - **Fix:** write "every triple taken in list order (`r<s<t`)".
2. **minor: symmetric mixed case not mentioned in Claim 2 of Theorem `mm:thm:axis-polygon`** (lines 361-363 for (a),
   389-390 for (b)).
   - **Issue:** only `r<m≤s` is treated. The case `s<m≤r` follows by exchanging names, as line 299 says for Theorem
     `mm:thm:mirror-polygon`, but here it is not said.
   - **Fix:** add "the case `s<m≤r` is symmetric".
3. **minor: blanket rigor sentence slightly overbroad** (line 50).
   - **Issue:** "Every statement below that carries a Lean reference is Lean-checked", but Lemma `mm:lem:orient-mir`
     (part (e)) and Lemma `mm:lem:slope` (part (b)) carry Lean references and contain parts that are not Lean
     declarations. These parts are flagged locally ("written step; not a separate Lean declaration") and in Coverage,
     so no reader is misled.
   - **Fix:** add "(parts marked as written steps excepted)".
4. **minor: description of the generated proofs** (lines 405-408).
   - **Issue:** "auxiliary products `(c_i)_1((c_b)_0-(c_a)_0) > 0`". The axis lemmas also use products with the axis
     point's abscissa, e.g. `c0 1 * (c0 0 - a 0)` (`MIRRORETV/lean/MirrorMain.lean:1373-1378`).
   - **Fix:** "products of a positive ordinate with a positive difference of abscissae (including that of the axis
     point)".
5. **minor: FarFlat axioms sentence** (lines 912-913).
   - **Issue:** "their recorded axioms (`MIRRORETV/lean/FarFlat.out`) are the standard three", but `FarFlat.out`
     prints axioms for five of the six theorems listed (`orient_wzq_neg`, `orient_uqz_neg`, `orient_sum`,
     `inside_triangle`, `line_misses`). `orient_cyclic` is not printed.
   - **Fix:** "the five printed in `FarFlat.out`".
6. **minor: provenance claim not supported by the record** (line 42).
   - **Issue:** "the remaining lines are written by hand". The file header (lines 4-10) only says the file was
     assembled from `MirrorPolygons.lean` and `small_polygons.lean` (generated by `gen_lean.py`), `MirrorReduction.lean`,
     `general_section.lean`, and so on. Nothing in the unit documents how the other parts were produced.
   - **Fix:** "the remaining lines were not produced by that generator", or drop the clause.
7. **minor: implicit relabeling in the description of the Lean proof of `mirror_five`** (lines 836-840).
   - **Issue:** when `c_0` lies on the axis, item (f) is applied with `a = c_0` and with the cap's `(c_1,c_2)` in the
     roles of the proposition's `(c_0,c_1)`. When `c_2` lies on the axis, (g) is applied with `a = c_2` and
     `(c_0,c_1)` unchanged. The renaming is left implicit. This is a parenthetical description of the Lean proof only;
     the written proof uses Lemma `mm:lem:upper-caps`(b).
8. **minor: index names clash with point names** (line 291).
   - **Issue:** Case 4 of Theorem `mm:thm:mirror-polygon` names indices `a, b, d`. These letters denote points in
     Lemma `mm:lem:orient-mir`, whose identity (d) is invoked in the same sentence.
   - **Fix:** use e.g. `α, β, δ` or `u_1, u_2, u_3`. Style only.
9. **minor: Remark (hM)(2) uses the Lean `j` for the sources' formula** (lines 653-656).
   - **Issue:** "In README/PROOFS (Theorem A), M is the number N(2j+1,j+1,2j+1)". Those sources write
     `N(2j−1, j, 2j−1)` with their own `j`. The translation is correct in the `j` of Theorem `mm:thm:odd`, and item (3)
     explains the shift right after.
   - **Fix:** add "(with the j of Theorem `mm:thm:odd`)".

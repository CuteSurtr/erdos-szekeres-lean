# Review of section `mm` (The mirror lemma and Theorem A), round 1, lens: fidelity

Verdict: **pass** (no blocker, no major finding; 9 minor findings below).

Files checked: `sections/mm.tex` (921 lines), `sections/mm.map.tsv` (20 rows), against
`MIRRORETV/lean/MirrorMain.lean` (all non-generated lines 1-21 and 1507-2677 read in full; the generated
range 22-1506 read at every statement head and every closing `cyc_k` call, plus tactic-pattern counts),
`MIRRORETV/lean/FarFlat.lean`, `ErdosSzekeres/Omission/Realization.lean:1-80`,
`ErdosSzekeres/ConvexCycleCuts.lean:1-30`, `ErdosSzekeres/Orientation.lean`, `ErdosSzekeres/Definitions.lean`,
`MIRRORETV/lean/MirrorMain.out`, `MIRRORETV/lean/MirrorNine.out`, `MIRRORETV/lean/FarFlat.out`,
`MIRRORETV/lean/MirrorNine_append.lean`, `MIRRORETV/README.md`, `MIRRORETV/PROOFS.md` (sections 1-4), the
inventory `inventory/MIRRORETV.json`, and the foundations statements `fd:lem:pos-cycle`, `fd:lem:mono`,
`fd:lem:collinear`, `fd:lem:orient` in `sections/fd.tex`.

## 1. Statement-by-statement comparison with Lean

Every cited name exists at exactly the cited line (offset 0 in all 60 citations; checked with a declaration
listing of `MirrorMain.lean`).

| label | Lean | result |
|---|---|---|
| `mm:def:mir` | `mir` :16 `![p 0, -p 1]`; `Rset` :1598 `S.filter (0 < p 1)`; `Aset` :1599 `S.filter (p 1 = 0)` | match; symmetry stated as maps-into |
| `mm:lem:orient-mir` | `mir_zero` :18, `mir_one` :19, `mir_mir` :1543, `orient_mir3` :2187, `orient_mir2` :2190, `orient_cycl` :2193, `orient_swap12` :2196, `orient_rev` :2199 | all 8 equations match verbatim (argument order and signs); (e) is a marked written step |
| `mm:def:config` | `Configuration` Realization.lean:9 (fields `point`, `xOrder : StrictMono (point · 0)`, `generalPosition : i<j→j<k→orient ≠ 0`); `HasCap` :64 (strictly increasing `f : Fin k → Fin n`, ALL triples `< 0`); `xset` :1549, `emb` :1553 (`orderEmbOfFin`), `sortPt` :1558 (`Classical.choose`), `cfg` :1584 | match (see minor 7 on `xset`) |
| `mm:lem:sort` | `xset_card` :1551, `emb_mem` :1555, `sortPt_mem` :1560, `sortPt_x` :1563, `sortPt_strictMono` :1566, `sortPt_injective` :1572, `sortPt_image` :1576 (`univ.image (sortPt T hx) = T`); (h) = field at :1587 | match, hypotheses `T` finite + `Set.InjOn (· 0) T` |
| `mm:lem:ngon` | `hasConvexNGon_of_le` :2182 (`HasConvexNGon m S → n ≤ m → HasConvexNGon n S`); `hasConvexNGon_affineMap` :1859 (`f : Point →ᵃ[ℝ] Point`, injective, conclusion on `S.image f`) | match |
| `mm:lem:slope` (export) | `cap_below_lines` :2204: `{m} c hx (hy : ∀ i, 0 ≤ c i 1) hcap {i j} l (hij : i<j) (hl : 0 < c l 1) : orient (c i) (c j) (mir (c l)) < 0` | (a) match (weak `≥0` on all, strict on `l`); (b) marked written step, equivalent to the local `interior` claims at :1716, :2060 and the inline argument :2542-2557 (lines verified) |
| `mm:thm:mirror-polygon` (export) | `cap_mirror_polygon` :2233: `(hm : 2 ≤ m) c hx (hy : ∀ i, 0 < c i 1) hcap {P} (hP) (hPm) : HasConvexNGon (2*m) P` | match; the cyclic list `q` (:2238) and the four cases (:2247-2277) match the written proof, including the rewrites `orient_mir3`, `orient_mir2`, `orient_cycl`+`orient_swap12`, `orient_rev` |
| `mm:thm:axis-polygon` (export) | `axis_left_polygon` :2309 (`3 ≤ m`, `h0 : c 0 1 = 0`, `hy : 0 < i.val → 0 < c i 1`); `axis_right_polygon` :2403 (`hlast : c (m-1) 1 = 0`, `hy : i.val < m-1 → 0 < c i 1`); conclusion `HasConvexNGon (2*m-1) P` | match; lists `q` (indices `2m-1-r`, resp. `2m-2-r`) and the special cases r = 0 (:2348-2358) and r = m-1 (:2442-2451) match Cases 3a |
| `mm:lem:cyc` | `cyc4` :995, `cyc5` :1026, `cyc6` :1068, `cyc7` :22, `cyc8` :103: k memberships, `q_r ≠ q_s` for r<s, `0 < orient q_r q_s q_t` for r<s<t | match |
| `mm:prop:small-polygons` | 9 lemmas at :1126, :1282, :1168, :212, :392, :1358, :1433, :639, :816 | every hypothesis list (x-order chain, `0 < y`, orientation hypotheses, `a 1 = 0`) and every membership list matches; the membership order equals the vertex order of the closing `cyc_k` call in each lemma (:388, :635, :812, :989, :1164, :1278, :1354, :1429, :1504) |
| `mm:lem:count` | `card_split` :1601 (only `sym`); `card_A_le` :1636 (only `gp`) | match |
| `mm:lem:injx` | `injOn_x` :1647: `S gp sym {T} (hTS) (hT0 : ∀ p ∈ T, 0 ≤ p 1) (hT1 : ∀ p q ∈ T, p 1 = 0 → q 1 = 0 → p = q) : Set.InjOn (· 0) T` | match |
| `mm:lem:upper-caps` | written step | correctly tagged; matches the local claims `keyT`/`hR` |
| `mm:thm:odd` (export) | `mirror_odd_general` :2498: `(j M : ℕ) (hj : 2 ≤ j) (hM : ∀ n (c : Configuration n), ¬ c.HasCap (j+1) → ¬ HasConvexNGon (2*j+1) (univ.image c.point) → n ≤ M) S gp sym noGon : S.card ≤ 2*M` | match: same quantifier order, hM stated as an assumed hypothesis (not N), Lean j used, index shift explained in the remark |
| `mm:thm:even` (export) | `mirror_even_general` :2599 (`HasCap j`, `2*j`, `≤ 2*M+2`) | match |
| `mm:def:frame` | `lineRefl` :1879, `frame` :1883, `unframeLin` :1886, `unframe` :1892 | all four coordinate formulas match verbatim; no unit-normal hypothesis in the definitions, as in Lean |
| `mm:lem:frame` | `unframe_apply` :1897 (no hypothesis), `unframe_frame` :1900, `frame_unframe` :1907, `frame_lineRefl` :1914, `orient_frame` :1920, `frame_injective` :1925, `unframe_injective` :1930 (all with `hn : n0^2+n1^2 = 1`) | match; the stated `linear_combination` multiples equal those in Lean |
| `mm:thm:line` (export) | `transport` :1937 (4-part conjunction, maps-into for `mir`, `S.image frame`); `mirror_odd_general_line` :2641, `mirror_even_general_line` :2650 (order `j M hj hM {n0 n1 c} hn S gp sym noGon`) | match |
| `mm:lem:cup` | `hasCap3_of` :1991; `capacity_cup` :2002 (`4 ≤ K`, conclusion `n ≤ K - 1`, natural subtraction addressed in Conventions) | match |
| `mm:thm:small` (export) | `mirror_four` :2019 (≤4), `mirror_five` :2040 (≤8), `mirror_six` :2129 (≤12), `_line` :2159, :2165, :2171 (with `hn`) | match; the description of the Lean case split in (b) (pentagon / `axis_right_pentagon` with a = c2 / `axis_left_pentagon` with a = c0 / interior) matches :2065-2089 |

No missing, extra or changed hypothesis; no strict/weak swap; no Finset/Set or maps-into/equality confusion;
natural subtractions (`2*m-1`, `K-1`, `m-1`) are covered by the Conventions paragraph and occur only where
the hypotheses make them ordinary.

## 2. Export labels and coverage

- All eight `mm:` export labels of the contract are defined, each on the named statement:
  `mm:def:config`, `mm:lem:slope`, `mm:thm:mirror-polygon`, `mm:thm:axis-polygon`, `mm:thm:odd`,
  `mm:thm:even`, `mm:thm:line`, `mm:thm:small`.
- Every declaration of `MirrorMain.lean` (80 declarations) is either covered by a label or listed under
  "Not covered here, deliberately" with a reason; the Baek-dependent ones are in fact covered in `mb`
  (`mb:prop:cap16`, `mb:prop:cap22`, `mb:prop:gon`, `mb:lem:seven-of`, `mb:thm:seven`, `mb:thm:eight`).
- FarFlat.lean: not imported by `MirrorMain.lean` (which imports only `ErdosSzekeres.Omission.BaekGeometry`
  and `ErdosSzekeres.ConvexCycleCuts`), so it is correctly listed in Coverage with all seven declarations at
  the right lines (12, 15, 34, 55, 60, 67, 89).
- The `\ref`s go only to own labels, `fd:` labels, and the `mb` export labels `mb:thm:seven/eight/nine`.

## 3. Other factual claims checked

- SHA-256 prefixes of all nine cited files match (`ca623e55a1b9`, `ae4970e0808e`, `b4ad0ba9e583`,
  `2425500eefd1`, `13667aa2d3dc`, `f67955ac7091`, `c7db9bbbb65e`, `0cc83994fe8c`, `08a79f881eea`).
- `MirrorMain.lean` lines 3-2677 equal `SYMLEAN/mirror/ReductionThreeClasses.lean` lines 1562-4236 (diff empty),
  so the offset +1559 is right.
- `MirrorMain.out`: lines 848-863 hold the 16 axiom lines, all `[propext, Classical.choice, Quot.sound]`;
  121 warnings, all "This simp argument is unused"; no error. `mirror_seven'`/`mirror_eight'` at 860/861;
  `MirrorNine.out` line 881 is `C12Check.mirror_nine`. `#print axioms` lines are 2662-2677.
- No `sorry`, `admit`, `native_decide`, `axiom`, `ofReduceBool`, `opaque` in `MirrorMain.lean`; in the
  declarations of this section `decide` only decides `Fin` comparisons (the `Nat.choose` decide at :1532 is in
  `capacity16`, not treated here).
- Generated range: line 1506 is the last line of `axis_right_pentagon`, line 1508 starts `section Baek17`;
  215 = 4+10+20+35+56+10+10+35+35 orientation `have`s, all closed by `linarith` (no `nlinarith`);
  distinctness by `congrFun h 0` or `congrFun h 1`.
- Toolchain: `lean-toolchain` is v4.24.0, `lake-manifest.json` has Mathlib rev `f897ebcf…`.
- (hM) instances in the remark: `capacity16` (¬HasCap 4, ¬7-gon, ≤16), `capacity22g` (¬HasCap 4, ¬8-gon, ≤22),
  `capacity113` (¬HasCap 5, ¬9-gon, ≤113; `MirrorNine_append.lean:116`, used at :131) are exactly hM for
  (j,M) = (3,16), (4,22) even, (4,113). The small cases (2,4), (3,5), (2,1) are correct.
- The algebraic identities used (orient-mir (b)-(e), the middle case of cap_below_lines, slope (b), the
  collinearity in injOn_x, and the four frame identities with the factor s = n0^2+n1^2) were re-checked
  symbolically: all 18 differences expand to 0.
- Standalone compile (private copy of the wrapper, removed afterwards): pdflatex exits 0 twice; the only undefined references are
  `fd:` labels and `mb:thm:seven/eight/nine`; no errors; only underfull boxes.

## 4. Findings

All minor. None changes a statement.

1. **minor — unsupported provenance claim.** `mm.tex:42`: "the remaining lines are written by hand". The record
   says only which parts were generated: `MirrorMain.lean:8-10` ("Assembled from MirrorPolygons.lean and
   small_polygons.lean (generated by gen_lean.py), MirrorReduction.lean, …") and `:993`. Nothing in the record
   says how the other parts were written. Suggested fix: "the remaining lines are not marked as generated".

2. **minor — axioms claim slightly broader than the record.** `mm.tex:912`: "their recorded axioms
   (`MIRRORETV/lean/FarFlat.out`) are the standard three" follows a list of seven declarations, but
   `FarFlat.out` prints axioms for only five (`orient_wzq_neg`, `orient_uqz_neg`, `orient_sum`,
   `inside_triangle`, `line_misses`); the definition `orient` and `orient_cyclic` have no `#print axioms` line.
   Suggested fix: "the five theorems printed in `FarFlat.out` use the standard three axioms".

3. **minor — imprecise reason in Coverage.** `mm.tex:896-899` says that `hasNGon_heptagon` (and the others)
   "use Baek's theorem". `hasNGon_heptagon` (`MirrorMain.lean:1512-1525`) does not use `main`; it is a
   bridge from a Config 7-gon in Baek's model to a convex 7-gon (via `boundary_polygon`, `boundaryOfGon`).
   Suggested fix: "they use Baek's theorem or its Config model and bridges".

4. **minor — indexing of the cited sources.** `mm.tex:653-656`: "In README.md and PROOFS.md (Theorem A), M is the
   number N(2j+1,j+1,2j+1), respectively N(2j,j,2j)". Those sources write N(2j-1,j,2j-1) in their own j
   (`README.md:10, 59`; `PROOFS.md` §1, r'_j). The formula is right in the Lean j used by the section, and
   item (3) explains the shift, but a reader comparing with the sources will not find this formula. Suggested
   fix: add "(in the j of Theorem odd; the sources write N(2j'-1,j',2j'-1) with j' = j+1)".

5. **minor — ambiguous map note.** `mm.map.tsv`, row `mm:thm:odd`: "Lean j = text j minus 1". In this section's
   text j is the Lean j; the shift is relative to README/PROOFS. Suggested fix: "Lean j (used in the section) =
   README/PROOFS j minus 1".

6. **minor — rigor sentence vs. embedded written steps.** `mm.tex:50`: "Every statement below that carries a Lean
   reference is Lean-checked". Lemma `mm:lem:orient-mir` part (e) and Lemma `mm:lem:slope` part (b) sit inside
   statements that carry Lean references but are written steps (each is marked in place, so nothing is hidden).
   The contract format puts written steps in separate statements tagged `[...; written step]`. Suggested fix:
   qualify the sentence ("except the parts marked as written steps"), or move (e) and slope (b) into separate
   written-step statements.

7. **minor — extra context on `xset`.** `mm.tex:137`: xset(T) is introduced under "Let T be finite and
   x-injective". In Lean `xset` (`MirrorMain.lean:1549`) takes only `T`; x-injectivity is needed only by
   `xset_card`, `emb` and `sortPt`. This narrows the definition harmlessly. Suggested fix: define xset(T) for
   every finite T and assume x-injectivity from `emb` on.

8. **minor — notation clash in the description of the generated proofs.** `mm.tex:407`: the auxiliary products are
   written $(c_i)_1((c_b)_0-(c_a)_0)$ with a and b as indices, while in the same subsection `a` is the axis
   point. In the axis lemmas the products involve that point (e.g. `c0 1 * (c0 0 - a 0)`,
   `MirrorMain.lean:1373`). Suggested fix: use other index letters or "differences of abscissae of two
   vertices".

9. **minor — map rows for remarks.** The section has 5 unlabeled `remark` environments with no rows in
   `mm.map.tsv`. The contract asks for "one row per statement environment"; it is unclear whether remarks
   count, and most other sections (ll, pc, oc, ec, sr, ar, mb, cb) list theirs, while fd and lg do not. This
   affects consistency only.

## 5. Notes on things that are right and might look wrong

- Lemma `mm:lem:upper-caps` is a written step, not a variant of a Lean statement. It isolates the local claims
  `keyT` (odd, five) and `hR` (even, four, six). Its case analysis is the one at `MirrorMain.lean:2519-2557`.
- The written proofs of the nine generated lemmas derive them from Theorems `mm:thm:mirror-polygon` and
  `mm:thm:axis-polygon`. The text says that this differs from Lean. There is no circularity: the general
  theorems do not use the Proposition, and (b), (d) are obtained from (c), (e) by restricting to the set Q of
  listed points.
- Theorem `mm:thm:line`(a) is `transport` with exactly its four conclusions, and (iii) uses `unframe` as an
  injective affine map, as in Lean (`:1956-1965`).

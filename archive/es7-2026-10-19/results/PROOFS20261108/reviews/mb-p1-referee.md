# Section `mb`, polish round 1: independent referee report

**Verdict: PASS.** No blocker or major finding. Three minor findings (R1–R3 below). None affects a statement or a proof.

I read the whole section (`sections/mb.tex`, 1196 lines) and its map (`sections/mb.map.tsv`, 42 rows). I read the Lean
source of every statement in the vendored files, the bridge files, `MIRRORETV/lean/MirrorMain.lean`,
`MIRRORETV/lean/MirrorNine_append.lean` and RTC (`SYMLEAN/mirror/ReductionThreeClasses.lean`). I also read every
cross-section statement that the section cites. I checked each step myself first. Only then did I read the earlier
reports (`mb-r1-*.md`, `mb-polish-r1-fix.md`, `mb-writer-concerns.md`). Every finding they made has been fixed in the
current text, and the new text the fixer added holds up (checked below).

## What I checked, and how

1. **Fidelity, statement by statement.** I compared every head with its declaration: binders, implicit arguments,
   `Finset` vs `Set`, strict vs weak inequalities, natural-number subtraction, and maps-into vs equality. Each one
   matches its Lean declaration.
   - **Vendored.** `Config` (Defs:20), `Cap3` (:30), `Cap`/`Cup` (`IsChain (·<·)` ∧ `Chain3'`), `Gon` (:45; both lengths
     ≥ 2, `head?`/`getLast?` equal), `NGon`, `HasNCap`/`HasNCup`/`HasNGon` (`List.In`). The lemmas `hasNCap_supset`
     (Lemmas:293), `hasNGon_supset` (:305) and `ncup_is_ngon` (:275, `2 ≤ n`) are in the root namespace, as the heads
     say. `main` (Main:87) has the bound `choose (n+2) 2 + 2 ≤ card` and the conclusion `HasNCap 4 ∨ HasNGon (n+3)`.
     `Config.cap_cup` (CapCup:46) has `choose (a+b) a < card`, with `a+2` and `b+2`.
   - **Bridge.** `cup` (Realization:33; `false` unless all three indices are `< n`) and `colorConfig … true`.
     `pointAt` (`0` for `i ≥ n`). `cup_true_iff` (Fin form), `cup_sign`, and `cap_sign` (with `a<b<d`). The four-point
     lemmas. `chain3_all` (`S : Set α`, `Pairwise`, `Chain3'`). `cup_list_all`, `cap_list_all` and `hasCap_of_list`.
   - **Boundary.** `boundary_polygon`, `Boundary.card` and `boundary_convex_position`. The change of variables in
     Remark `mb:rem:boundary` is an exact bijection: `lower` = (u_i), `upperReflected` = (ρ v_j),
     `first_eq`/`last_eq` ⇔ u_0 = v_0 and u_{s+1} = v_{t+1}, and `Boundary.finite` = `points` = B. So the u/v form is
     the Lean statement, not a variant of it.
   - **Gon proposition.** In `hasNGon_heptagon`/`octagon`/`nonagon`, the cap is `xs` with `k = |xs|−2`, which is the
     section's t. The cup is `ys` with `l = |ys|−2`, which is s. This matches "Lean calls these numbers l and k".
   - **Capacity bounds.** `capacity16`, `geometric_capacity22` (with `S ⊆ range n`), `capacity22g`,
     `config_capacity113` and `capacity113`.
   - **Mirror declarations.** `mir`, `Rset`, `Aset`. `card_split` (no general position needed). `card_A_le`.
     `injOn_x` (`T ⊆ S`, `0 ≤ y`, at most one axis point). `cfg`/`sortPt_image`.
   - **Polygon lemmas.** The four polygon lemmas, with all hypotheses and membership lists: (a) has no `mir c0 ∈ P`.
     `mirror_seven_of`: Hcap, HL and HR quantify over the points and over every `{P : Finset Point}`.
   - **Frame and transport.** `lineRefl`, `frame`, `unframe` and its linear part. The six frame lemmas (`{n0 n1}`,
     explicit `c`, `hn`). `hasConvexNGon_affineMap`. `transport` (four conjuncts). The seven/eight/nine theorems and
     their `_line` versions.
   - **Reflections and the three-class reduction.** `reflLine` (RTC:449): n₀ = −u₁, n₁ = u₀, c = −u₁a₀ + u₀a₁.
     `card_le_32_of_reflLine` (`Invariant`). The class definitions (RTC 508 and 514) inside `mirrorOneAxis33_proved`
     and `mirrorNoAxis34_proved`. Both `_3` theorems: the three class binders come first, then
     `S g hgp hcard hg hne hinv`. The second one uses `g : Point ≃ᵃ[ℝ] Point` and `hne : g ≠ AffineEquiv.refl ℝ Point`.
2. **Every `\leanref` and every line number in the prose.** All 78 heads, and every cited line, name the right
   declaration:
   - Defs:46/22. Realization:9/44/64.
   - BoundaryGeometry:30/56/64/69/120. BaekGeometry:62/77.
   - MirrorMain:1543/1886/2233/2309/2403/2498/2631/2636/2641. The generated block is 22–991 for the four lemmas
     (calls to `cyc7`/`cyc8` at 388, 635, 812 and 989); the small-k block ends at 1506.
   - RTC:1023/1050/1078/1503/1515/1527/1536/1547/4238/4253/4264/4274/4282/4292/4303/4312–4316.
   - SymmetricReduction:423/997. AffineReduction:1501.
   - Logs: `MirrorMain.out` 848–863 (848, 849, 850, 851, 858 and 862 named correctly), `MirrorNine.out` 879–882, and
     `axioms.out` 1–40, including the truncated `#check` lines 17–20 and 39–40.
3. **Records.**
   - All 21 SHA-256 prefixes in the Sources and the axioms paragraph match the files.
   - `diff` confirms the three claimed byte-identities:
     - RTC 1562–4236 = MirrorMain 3–2677;
     - RTC 38–1559 = AffineReduction 12–1533;
     - RTC 38–1084 = SymmetricReduction 12–1058.
   - The shift of 2677 in `MirrorNine.out` checks out: its linter warnings at 2742/2743 map to append lines 65/66.
   - Lean 4.24.0 and Mathlib `f897ebcf` agree with `lean-toolchain` and `lake-manifest.json`.
   - `decide` occurs in the three files only on explicit `Fin` comparisons and on `choose (4+2) 2 = 15`,
     `choose (6+2) 2 = 28` and `choose (3+6) 3 = 84`. RTC Part A has none.
   - There is no `native_decide`, `sorry`, `admit` or `axiom` in these files, in the 12 listed vendored and bridge
     files, or anywhere under `Vendor/ETV`.
   - All 161 generated orientation facts of the four polygon lemmas (35 + 56 + 35 + 35) and all 91 distinctness facts
     use `linarith` only, as Remark `mb:rem:generated` says.
   - Every declaration of `BoundaryGeometry`, `BaekGeometry`, `ListGeometry`, `PlanarChains` and `Baek.lean` is named
     in the section (script check).
   - `cup_false_iff` is used only off the proof paths (`listCap_of_hasCap`, `endingPath_hasCap`).
   - The citations agree with their sources: `MIRRORETV/PROOFS.md` (proof of Cor. 7.2, Lemma 2.3 "⇐"),
     `MIRRORETV/README.md` §4 and §8, `docs/THIRD_PARTY.md` 111–118, `C2FINAL` (status), `C3LEAN` (§4: 910 roots,
     116,883 records, proofs not kept), `SYM5` (two normal forms, P1 and L1 retained), `C2ENC/perturbation.md`
     (m = 3, 5) and `SYMLEAN/README.md` §5, §6 and §9.
4. **Proofs, step by step.**
   - **Chain closure.** Downward induction, with inner induction on k. Step A uses Q(i+1) with i+1 < k−1 < k. Step B
     uses the second conclusion of the transitivity condition. Lists with r ≤ 2 hold vacuously.
   - **Boundary, Steps 1–6.** Signs on the chord. Only the endpoints are shared. Edge support through the chord
     identity, using x(L) < x(w) < x(R) and the w ∈ U case at L and R. The reflected data of Step 4 satisfy the
     hypotheses with s and t exchanged. In Step 5 the exposing functionals give g(p) = 0 and g > 0 on B∖{p} in all four
     cases, including w = u_{i−1} and w = v_{j+1}.
   - **Gon proposition** (s + t + 2 = m). The capacity bounds 16, 22 and 113.
   - **Lemma `mb:lem:split`.** In (c), p, q and mir p are pairwise distinct and lie in S by symmetry.
   - **Lemma `mb:lem:polygons`.** I re-derived (a)–(d) from `mm:thm:mirror-polygon` and `mm:thm:axis-polygon` with
     m = 4. For (a), I deleted mir c₀ from an 8-gon of P ∪ {mir c₀}. Then |T'| ≥ 7, and `fd:lem:mono`(a),(d) apply.
   - **Key claim of `mirror_seven_of`.** The five cases on y(d₀), y(d₃), y(d₁), y(d₂) are exhaustive and match the
     Lean `rcases` tree. The counting gives 2·15 + 2 = 32.
   - **Theorem `mb:thm:eight`(a).** 2·22 + 2 = 46.
   - **Theorem `mb:thm:nine`(a).** Both claims hold. In the Cup3 branch, (z₀,…,z₇,r) is a 9-cup. In the Cap3 branch,
     (p,q,r,r₂,r₃) is a 5-cap, and its consecutive triples are (p,q,r) and those of the cap. The result is
     29 + 84 = 113.
   - **(b), (c).** These are the instance j = 4, M = 113 of `mm:thm:odd` and `mm:thm:line`(b).
   - **Transport, `mb:thm:refl32`, classes and `mb:thm:main3`.**
5. **Identities checked with sympy** (`build/mbref/check_mb.py`; every residual is 0):
   - the two four-point identities, the chord identity (`mb:eq:chord`) and the interior identity;
   - ρ negates orient; three axis points are collinear; orient(p, q, mir p) = 0 when x(q) = x(p);
   - the four ν-defect identities of Lemma `mb:lem:frame`, and the second frame coordinate n₀p₀ + n₁p₁ − cν;
   - both coordinates of the `reflLine`/`lineRefl` difference, including the intermediate expressions written in the
     proof, and the identity ⟨n,p⟩ − c = ⟨n,w⟩;
   - the geometric form a + ⟨w,u⟩u − ⟨w,n⟩n, valid exactly when u₀² + u₁² = 1;
   - the binomials 15, 21, 28 and 84, and the thresholds 17, 23 and 30.
6. **Cross-references.** All 25 external labels are allowed by the contract and are defined in `fd`, `mm`, `sr` and
   `ar`, and each says what `mb` uses:
   - `fd:lem:mono`(a)–(d), `fd:lem:affine-orient` (any map x ↦ Ax + v, with the reflection worked out in (ii)), and
     `fd:lem:affine-cp`(b) for injective affine maps;
   - `fd:lem:separation` (its easy direction is the exposing-functional fact) and `fd:lem:pos-cycle`;
   - `mm:thm:mirror-polygon` and `mm:thm:axis-polygon` (exactly the forms quoted in the proof of
     `mb:lem:polygons`), `mm:thm:odd` (with (hM)) and `mm:thm:line`(a),(b);
   - `sr:def:classes` (4) and (5), `sr:thm:main` and `ar:thm:main`(a).

   There is no circularity: the proofs in `mm` use none of the `mb` statements. Every `mb:` reference made from other
   sections (`mm`, `sr`, `ar`, `fd`) points at the statement that the referring text intends.
7. **Hygiene.**
   - A standalone compile in `build/mbref` (my own wrapper, so the shared `build/` was left alone) exits 0 on both
     passes. It shows no error and no overfull box, and its only undefined references are the allowed external labels.
   - All seven export labels are defined on the statements named for them.
   - The map has 42 rows of 5 tab-separated fields, in environment order, with matching kinds.
   - There is no `\newcommand` or `\usepackage`, no machine path, and no tool name in `mb.tex` or
     `mb.map.tsv`.
   - The rigor vocabulary is respected. "Proved" appears only for written proofs or for Lean proofs.
     "Certificates" appears only in the sense of `linear_combination` coefficients. The three class hypotheses are
     never presented as proved.

## Findings

### R1 (minor): the opening paragraph says more is restated than Theorem `mb:thm:main3` restates

- **Location.** `mb.tex` lines 19–20, in "What this section proves": "restate the reduction
  Theorems~\ref{sr:thm:main} and~\ref{ar:thm:main} with the three remaining case classes as their only case-class
  hypotheses (Theorem~\ref{mb:thm:main3} …)".
- **Evidence.**
  - Theorem `ar:thm:main` (`ar.tex` 647–670) has five parts, (a)–(e):
    - `heptagon_of_nontrivial_affineEquiv`;
    - `heptagon_of_nontrivial_affineEquiv_image`;
    - `heptagon_of_nontrivial_affineMap`;
    - `heptagon_of_nontrivial_affine`;
    - `heptagon_of_nontrivial_affine_coords`.
  - Theorem `mb:thm:main3`(b) restates only part (a). RTC has no `_3` versions of the other four (RTC 1503, 1515, 1536,
    1547 still take five classes).
  - Remark `mb:rem:main3` says so itself (lines 1108–1113), so the paragraph and the remark disagree in scope.
- **Fix.** Write "restate Theorem~\ref{sr:thm:main} and part~(a) of Theorem~\ref{ar:thm:main} (the \lean{AffineEquiv}
  form) with the three remaining case classes …". Optionally, in the proof of Theorem `mb:thm:main3`(b) (line 1076),
  write "Theorem~\ref{ar:thm:main}(a)".

### R2 (minor): Remark `mb:rem:main3` does not say that the project trusts only one of the two checkers

- **Location.** `mb.tex` lines 1090–1101. Three passages say "both proof checkers accepted the proof": the HalfTurn34
  pieces, the 116,883 Threefold33 records, and the two SYM5 proofs.
- **Evidence.**
  - Since 6 November 2026, the project's trust base is `cake_lpr` alone, and lrat-check is a secondary check
    (`WRITEUP/SYMMETRIC.md` §3, lines 229–235: "Where this section says 'both checkers', the certificate is the
    cake_lpr verdict").
  - The lrat-check build used on one machine was found unsound (`LRATCHECK20261105/README.md`, line 1).
  - The sentences are literally true, since `cake_lpr` accepted each of these, so nothing is rounded up. But read on
    their own, they suggest two independent trusted checks. Section `sr` states the caveat (`sr.tex` 249–251).
- **Fix.** After the first sentence of the remark, add "(where both checkers are named, the trusted verdict is that of
  `cake_lpr`; lrat-check is a secondary check, \dirn{WRITEUP/SYMMETRIC.md} \S3)". Cite the record, not
  `sr:rem:records`, which is not an allowed export label.

### R3 (minor): the Fivefold35 item understates and slightly misplaces the layer lemma

- **Location.** `mb.tex` lines 1100–1101: "the encoder and the layer lemma have written proofs".
- **Evidence.**
  - `SYM5/README.md` (notes under the table in §2) says: "Each of P1 and L1 alone proves the theorem. P1 needs no
    layer lemma." Only the layer normal form (L1) uses the layer lemma.
  - The layer lemma is moreover Lean-checked (`LAYERLEAN`; Theorem `ll:thm:layers`, an allowed export label).
  - The sentence is not false, and it understates rather than overclaims. A reader may still conclude that Fivefold35
    needs an unformalized layer lemma.
- **Fix.** Write "the encoder has a written proof; the angle normal form (P1) needs no layer lemma, and the layer
  normal form (L1) uses the layer lemma, which is Lean-checked (Theorem~\ref{ll:thm:layers})". If you prefer not to add
  a reference, just drop "and the layer lemma".

## Notes (not findings)

- Lemma `mb:lem:boundary` is stated in u/v variables, not with the `Boundary` structure. I confirmed that the
  encoding is an exact bijection, so the statement is the Lean statement, and Remark `mb:rem:boundary` documents this.
- Theorem `mb:thm:baek` is the vendored combinatorial statement (arbitrary ternary relation, weak gons). The contract
  allows citing it as used, and its formalization is in the axioms cone of the printed theorems. A geometric-only
  citation of Theorem 1.6 would not cover the use in Theorem `mb:thm:nine`(a), which applies it to an arbitrary
  configuration.
- The `\\` and `\raggedright` in the heads cause no problem: the compile has no overfull boxes.

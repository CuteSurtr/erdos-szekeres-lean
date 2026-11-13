# doc-r1, lens xref-mmmb: cross-references from sections mm and mb

Scope: every `\ref`/`\eqref` in `sections/mm.tex` and `sections/mb.tex` whose label prefix differs from the citing
section (159 occurrences, 55 in mm, 104 in mb; there is no cross-section `\eqref`), plus the prose claims of these two
sections about other sections ("proved elsewhere", "the section of Theorem ...", "the same statement is part (a) of
...", pointers to Lean copies and logs that other sections also cite).

Method: each target was read in its own section file (fd, ll, lg, sr, ar, mm, mb); hypotheses were matched at the point
of use; restatements of another section's theorem were compared clause by clause; the Lean sources were consulted
read-only where a citing sentence makes a claim about them (MirrorMain.lean, MirrorNine_append.lean,
ReductionThreeClasses.lean, SymmetricReduction.lean, AffineReduction.lean, Baek.lean, Main.lean, LayerLemma.lean);
the byte-identity claims about the copies in ReductionThreeClasses.lean were checked with sed and diff
(RTC 38-1559 = AffineReduction.lean 12-1533; RTC 38-1084 = SymmetricReduction.lean 12-1058;
RTC 1562-4236 = MirrorMain.lean 3-2677: all identical). Build `build/doc-r1`: no undefined or multiply defined
reference. Every cross-section label used is a foundations label or an export label of the contract, and the word
before each `\ref` (Lemma, Theorem, Definition) matches the environment of the target.

## Findings

- F1 (minor, mb, Remark mb:rem:main3, lines 1094-1104). The Threefold33 item says "C3LEAN Lean-checks only that the
  leaves named in it cover the 910 roots" without the label computer-assisted (the check is kernel evaluation,
  Theorem cb:thm:c3) and without the reference; the HalfTurn34 item omits the Lean-checked, computer-assisted
  bookkeeping of the subcase orbits (Theorem cb:thm:c2). Remarks sr:rem:records and ar:rem:classes describe the same
  evidence with both labels and both references. Fix: add "(Lean-checked by kernel evaluation, so computer-assisted;
  Theorem~\ref{cb:thm:c3})" to the C3LEAN sentence, and to the HalfTurn34 item "the bookkeeping of the subcase orbits
  is Lean-checked by kernel evaluation, so computer-assisted (Theorem~\ref{cb:thm:c2}); that the listed subcases are
  refuted rests on the records".
- F2 (minor, mb, paragraph "Dependencies and rigour", lines 96-102). The list of foundations lemmas omits
  fd:lem:separation (cited in Step 5 of the proof of Lemma mb:lem:boundary, line 448) and fd:lem:pos-cycle (Remark
  mb:rem:generated, line 683), and the cross-section list omits ll:thm:layers and lg:thm:nesting (Remark mb:rem:main3,
  lines 1108-1109). Fix: add them ("and, in Remark~\ref{mb:rem:main3}, Theorems~\ref{ll:thm:layers}
  and~\ref{lg:thm:nesting}").
- F3 (minor, mb, Conventions line 112 and the restatement of mm:def:config at lines 247-253). mb glosses $[n]$ as
  "Lean Finset.range n" but also uses it for the Fin-indexed objects of Definition mm:def:config (a configuration
  $c\colon[n]\to\R^2$, a cap map $f\colon[k]\to[n]$, lines 249-251, 363, 709, 884), where mm's $[m]$ stands for
  Fin m; and mb's $\mathcal P(c)$ is mm's $\mathrm{pts}(C)$ (same Lean expression) without a link. No mathematical
  effect (both are $\{0,\dots,n-1\}$). Fix: one sentence in the Conventions ("where a configuration or a cap map is
  concerned, $[n]$ is the same set viewed as Lean's Fin n, as in Definition~\ref{mm:def:config}") and
  "(written $\mathrm{pts}(c)$ in Definition~\ref{mm:def:config})" after the definition of $\mathcal P(c)$.
- F4 (minor, mm, Coverage line 942; also Remark mm:rem:hm(1), line 669). "They belong to Theorems mb:thm:seven and
  mb:thm:eight" points at the theorems, but hasNGon_heptagon, capacity16, mirror_seven_of and capacity22g are stated in
  mb as Proposition mb:prop:gon, Proposition mb:prop:cap16, Lemma mb:lem:seven-of and Proposition mb:prop:cap22 (not
  export labels, so mm cannot cite them). Fix: "They are treated in the section of Theorems~\ref{mb:thm:seven}
  and~\ref{mb:thm:eight}, as statements used in their proofs"; similarly "treated in the section of" at line 669.

No blocker or major finding. All 159 references point to the intended statement, the hypotheses of each cited
statement are met where it is used, and no citing text uses more than the cited statement gives.

## Every cross-section reference (citing location -> target (number in doc-r1): verdict)

- sections/mm.tex:35 -> \ref{fd:lem:pos-cycle} (1.38): OK: file ErdosSzekeres/ConvexCycleCuts.lean and hash prefix b4ad0ba9e583 agree with the head and source table of fd.
- sections/mm.tex:76 -> \ref{fd:def:point} (1.1): OK (dependency list; every fd label used in mm is listed, and every listed one is used).
- sections/mm.tex:77 -> \ref{fd:def:orient} (1.3): OK (dependency list).
- sections/mm.tex:77 -> \ref{fd:def:gp} (1.5): OK (dependency list).
- sections/mm.tex:77 -> \ref{fd:def:cp} (1.6): OK (dependency list).
- sections/mm.tex:77 -> \ref{fd:def:ngon} (1.7): OK (dependency list).
- sections/mm.tex:77 -> \ref{fd:def:inv} (1.10): OK (dependency list).
- sections/mm.tex:78 -> \ref{fd:lem:orient} (1.15): OK (dependency list).
- sections/mm.tex:78 -> \ref{fd:lem:affine-orient} (1.17): OK (dependency list).
- sections/mm.tex:78 -> \ref{fd:lem:collinear} (1.20): OK (dependency list).
- sections/mm.tex:78 -> \ref{fd:lem:cp-hull} (1.22): OK (dependency list).
- sections/mm.tex:79 -> \ref{fd:lem:mono} (1.23): OK (dependency list).
- sections/mm.tex:79 -> \ref{fd:lem:affine-cp} (1.27): OK (dependency list).
- sections/mm.tex:79 -> \ref{fd:lem:pos-cycle} (1.38): OK (dependency list).
- sections/mm.tex:81 -> \ref{mb:thm:seven} (10.31): OK: k=7 bound 32 (mirror_seven, mirror_seven_line); its Lean proof uses the generated polygons of this section.
- sections/mm.tex:81 -> \ref{mb:thm:eight} (10.33): OK: k=8 bound 46.
- sections/mm.tex:82 -> \ref{mb:thm:nine} (10.35): OK: k=9 bound 226; part (a) uses Config.cap_cup as the text says (checked in MirrorNine_append.lean:24-60).
- sections/mm.tex:85 -> \ref{fd:def:point} (1.1): OK.
- sections/mm.tex:88 -> \ref{fd:def:ngon} (1.7): OK: restated identically (T subset X, |T|=n, convex position).
- sections/mm.tex:102 -> \ref{fd:def:inv} (1.10): OK: maps-into; the equivalence with mir(S)=S for injective mir and finite S is the one fd states.
- sections/mm.tex:122 -> \ref{fd:def:orient} (1.3): OK: same formula.
- sections/mm.tex:133 -> \ref{fd:lem:orient} (1.15): OK: part (d) (written step, R = reals) covers the 3-cycle (sign +1) and the transpositions (1 2), (1 3) (sign -1).
- sections/mm.tex:199 -> \ref{fd:lem:collinear} (1.20): OK: part (b) applied to the finite general-position set T and pairwise distinct s_i,s_j,s_k.
- sections/mm.tex:215 -> \ref{fd:lem:mono} (1.23): OK: part (d) is the same Lean declaration MirrorOdd.hasConvexNGon_of_le (MirrorMain.lean:2182).
- sections/mm.tex:217 -> \ref{fd:lem:mono} (1.23): OK: part (a).
- sections/mm.tex:226 -> \ref{fd:lem:cp-hull} (1.22): OK.
- sections/mm.tex:228 -> \ref{fd:lem:cp-hull} (1.22): OK.
- sections/mm.tex:228 -> \ref{fd:lem:affine-cp} (1.27): OK: forward direction of (d), and (d-prime) for Mathlib affine maps, contain mm:lem:ngon(b).
- sections/mm.tex:317 -> \ref{fd:lem:pos-cycle} (1.38): OK: N=k=2m>=4 (m>=2), p=q injective (Claim 2), e = identity embedding, P finite with all q_r in P, positivity of all increasing triples = Claim 1.
- sections/mm.tex:324 -> \ref{fd:lem:pos-cycle} (1.38): OK: fd requires all increasing triples, as stated.
- sections/mm.tex:366 -> \ref{fd:lem:orient} (1.15): OK: part (a) orient(a,c,b) = -orient(a,b,c) with (a,b,c)=(c_0,c_u,c_u').
- sections/mm.tex:379 -> \ref{fd:lem:pos-cycle} (1.38): OK: N=k=2m-1>=5 (m>=3, so the truncated subtraction is ordinary), e identity.
- sections/mm.tex:411 -> \ref{fd:lem:pos-cycle} (1.38): OK: "at least four points" is the hypothesis 4<=k.
- sections/mm.tex:438 -> \ref{fd:lem:pos-cycle} (1.38): OK: N=k in {4,...,8}, injectivity from pairwise distinctness, e identity.
- sections/mm.tex:504 -> \ref{fd:lem:mono} (1.23): OK: part (a).
- sections/mm.tex:514 -> \ref{mb:thm:seven} (10.31): OK: checked in Lean, mirror_seven (MirrorMain.lean:1805) passes cap_mirror_heptagon, axis_left_heptagon, axis_right_heptagon = items (d), (h), (i).
- sections/mm.tex:515 -> \ref{mb:thm:eight} (10.33): OK: mirror_eight applies cap_mirror_octagon = item (e) (MirrorMain.lean:1839).
- sections/mm.tex:539 -> \ref{fd:lem:collinear} (1.20): OK.
- sections/mm.tex:554 -> \ref{fd:lem:collinear} (1.20): OK.
- sections/mm.tex:576 -> \ref{fd:lem:mono} (1.23): OK: part (b), T subset S.
- sections/mm.tex:620 -> \ref{fd:lem:mono} (1.23): OK: part (c).
- sections/mm.tex:647 -> \ref{fd:lem:mono} (1.23): OK: part (c).
- sections/mm.tex:667 -> \ref{mb:thm:baek} (10.4): OK: the vendored theorem main (Main.lean:87); capacity16 applies main 4 directly (MirrorMain.lean:1535), capacity22g goes through geometric_capacity22 and Baek.capacity22 (main 5), config_capacity113 uses main 6 and Config.cap_cup.
- sections/mm.tex:669 -> \ref{mb:thm:seven} (10.31): OK but loose (finding F4): capacity16 and mirror_seven' are treated in Proposition mb:prop:cap16 and Remark mb:rem:seven, not in the theorem itself.
- sections/mm.tex:669 -> \ref{mb:thm:eight} (10.33): OK but loose (F4): capacity22g and mirror_eight' are in Proposition mb:prop:cap22 and Remark mb:rem:eight.
- sections/mm.tex:669 -> \ref{mb:thm:nine} (10.35): OK: capacity113 is Proposition mb:prop:cap113, mirror_nine is part (b) of the theorem (MirrorNine.out line 881 consistent).
- sections/mm.tex:765 -> \ref{fd:lem:affine-orient} (1.17): OK: frame(x) = Rx - (0,cs) for every x, det R = n_0^2+n_1^2 = s.
- sections/mm.tex:800 -> \ref{fd:lem:collinear} (1.20): OK: (b), forward direction for pairwise distinct a,b,d in S.
- sections/mm.tex:801 -> \ref{fd:lem:collinear} (1.20): OK: (b), converse for S'.
- sections/mm.tex:838 -> \ref{fd:lem:pos-cycle} (1.38): OK: N=n, k=K>=4, p=C injective (strict x-order), e=Fin.castLEEmb (needs K<=n, assumed), P=pts(C) finite, positivity proved.
- sections/mm.tex:942 -> \ref{mb:thm:seven} (10.31): Imprecise pointer (F4): hasNGon_heptagon, capacity16 and mirror_seven_of are Proposition mb:prop:gon, Proposition mb:prop:cap16 and Lemma mb:lem:seven-of, not parts of Theorem mb:thm:seven.
- sections/mm.tex:942 -> \ref{mb:thm:eight} (10.33): Imprecise pointer (F4): capacity22g is Proposition mb:prop:cap22.
- sections/mm.tex:946 -> \ref{mb:thm:seven} (10.31): OK: mirror_seven' = mirror_odd_general 3 16 with capacity16 (MirrorMain.lean:2631-2634); bound 32.
- sections/mm.tex:947 -> \ref{mb:thm:eight} (10.33): OK: mirror_eight' = mirror_even_general 4 22 with capacity22g (MirrorMain.lean:2636-2639); bound 46.
- sections/mm.tex:961 -> \ref{mb:thm:nine} (10.35): OK.
- sections/mb.tex:15 -> \ref{mm:thm:mirror-polygon} (9.8): OK: used in Lemma mb:lem:polygons.
- sections/mb.tex:15 -> \ref{mm:thm:axis-polygon} (9.10): OK: used in Lemma mb:lem:polygons(c),(d).
- sections/mb.tex:15 -> \ref{mm:thm:odd} (9.17): OK: used in Theorem mb:thm:nine(b) with (hM) supplied by Proposition mb:prop:cap113; "proved elsewhere" = the conditional theorem of mm.
- sections/mb.tex:16 -> \ref{mm:thm:line} (9.23): OK: part (b) used in Theorem mb:thm:nine(c).
- sections/mb.tex:18 -> \ref{sr:def:classes} (7.7): OK: classes (4), (5) are the mirror classes; RTC copies have the same text (RTC 38-1084 = SymmetricReduction.lean 12-1058, checked with diff).
- sections/mb.tex:19 -> \ref{sr:thm:main} (7.39): OK.
- sections/mb.tex:20 -> \ref{ar:thm:main} (8.28): OK: part (a) is heptagon_of_nontrivial_affineEquiv, the AffineEquiv form.
- sections/mb.tex:97 -> \ref{fd:def:point} (1.1): OK (dependency list; incomplete, finding F2).
- sections/mb.tex:97 -> \ref{fd:def:orient} (1.3): OK (dependency list).
- sections/mb.tex:97 -> \ref{fd:def:gp} (1.5): OK (dependency list).
- sections/mb.tex:97 -> \ref{fd:def:cp} (1.6): OK (dependency list).
- sections/mb.tex:98 -> \ref{fd:def:ngon} (1.7): OK (dependency list).
- sections/mb.tex:98 -> \ref{fd:def:inv} (1.10): OK (dependency list).
- sections/mb.tex:98 -> \ref{fd:lem:orient} (1.15): OK (dependency list).
- sections/mb.tex:98 -> \ref{fd:lem:affine-orient} (1.17): OK (dependency list).
- sections/mb.tex:98 -> \ref{fd:lem:collinear} (1.20): OK (dependency list).
- sections/mb.tex:99 -> \ref{fd:lem:cp-hull} (1.22): OK (dependency list).
- sections/mb.tex:99 -> \ref{fd:lem:mono} (1.23): OK (dependency list).
- sections/mb.tex:99 -> \ref{fd:lem:affine-cp} (1.27): OK (dependency list). The list omits fd:lem:separation (cited at line 448) and fd:lem:pos-cycle (line 683) (F2).
- sections/mb.tex:100 -> \ref{mm:def:config} (9.3): OK (dependency list).
- sections/mb.tex:100 -> \ref{mm:thm:mirror-polygon} (9.8): OK (dependency list).
- sections/mb.tex:100 -> \ref{mm:thm:axis-polygon} (9.10): OK (dependency list).
- sections/mb.tex:100 -> \ref{mm:thm:odd} (9.17): OK (dependency list).
- sections/mb.tex:101 -> \ref{mm:thm:even} (9.18): OK (dependency list; used in Remark mb:rem:eight).
- sections/mb.tex:101 -> \ref{mm:thm:line} (9.23): OK (dependency list).
- sections/mb.tex:101 -> \ref{sr:def:iso} (7.1): OK (dependency list).
- sections/mb.tex:102 -> \ref{sr:def:classes} (7.7): OK (dependency list).
- sections/mb.tex:102 -> \ref{sr:thm:main} (7.39): OK (dependency list).
- sections/mb.tex:102 -> \ref{ar:thm:main} (8.28): OK (dependency list). ll:thm:layers and lg:thm:nesting (Remark mb:rem:main3) are not listed (F2).
- sections/mb.tex:109 -> \ref{fd:def:point} (1.1): OK.
- sections/mb.tex:111 -> \ref{fd:def:orient} (1.3): OK.
- sections/mb.tex:113 -> \ref{fd:def:ngon} (1.7): OK.
- sections/mb.tex:114 -> \ref{fd:def:cp} (1.6): OK.
- sections/mb.tex:116 -> \ref{fd:lem:orient} (1.15): OK: parts (a), (b), (d) and (e) give the four identities (the last two are also (d), (e)).
- sections/mb.tex:117 -> \ref{fd:def:orient} (1.3): OK.
- sections/mb.tex:247 -> \ref{mm:def:config} (9.3): OK in content (xOrder, generalPosition, all-triples HasCap, point set = Finset.univ.image c.point); notation differs without a link (F3): [n] is glossed "Lean Finset.range n" (line 112) but used for Fin n here, and P(c) is mm's pts(C).
- sections/mb.tex:379 -> \ref{fd:lem:cp-hull} (1.22): OK: B finite.
- sections/mb.tex:438 -> \ref{fd:lem:affine-orient} (1.17): OK: A = diag(1,-1), det -1 (part (ii) with o=0, phi=0).
- sections/mb.tex:448 -> \ref{fd:lem:separation} (1.40): OK: the stated fact is the easy direction with l = -(linear part of g); it is also proved inline; Lean counterpart BoundaryGeometry.lean:30 as named in fd.
- sections/mb.tex:465 -> \ref{fd:lem:cp-hull} (1.22): OK.
- sections/mb.tex:540 -> \ref{mm:thm:odd} (9.17): OK: "the section of Theorem mm:thm:odd" = mm. Each Lean declaration of mb:ssec:red, mb:def:frame, mb:lem:frame, mb:lem:affine, mb:lem:transport is stated (and proved) in mm (mm:def:mir; mm:lem:count, mm:lem:injx; mm:def:config(d), mm:lem:sort(g); mm:prop:small-polygons(d),(e),(h),(i); mm:def:frame; mm:lem:frame; mm:lem:ngon(b); mm:thm:line(a)), and the two statements agree in hypotheses and conclusions.
- sections/mb.tex:555 -> \ref{fd:lem:affine-orient} (1.17): OK.
- sections/mb.tex:577 -> \ref{fd:lem:collinear} (1.20): OK.
- sections/mb.tex:596 -> \ref{mm:def:config} (9.3): OK: parts (c), (d) (xset, emb, sortPt, cfg).
- sections/mb.tex:600 -> \ref{fd:lem:collinear} (1.20): OK.
- sections/mb.tex:614 -> \ref{mm:thm:mirror-polygon} (9.8): OK.
- sections/mb.tex:614 -> \ref{mm:thm:axis-polygon} (9.10): OK.
- sections/mb.tex:645 -> \ref{mm:thm:mirror-polygon} (9.8): OK: paraphrase faithful (m>=2, strictly increasing x, y>0, all increasing triples negative, P finite containing e_i and mir e_i, conclusion 2m points); line 2233 correct. Applications (a), (b) verified: (b) m=4; (a) via P union {mir c_0}, then fd:lem:mono(a),(d).
- sections/mb.tex:648 -> \ref{mm:thm:axis-polygon} (9.10): OK: paraphrase faithful (m>=3, left/right axis conditions as in mm (a)/(b)); lines 2309, 2403 correct. Applications (c) e=(a,c0,c1,c2) and (d) e=(c0,c1,c2,a) verified (mir a = a, four triples, 2*4-1=7).
- sections/mb.tex:660 -> \ref{fd:lem:mono} (1.23): OK: part (a).
- sections/mb.tex:661 -> \ref{fd:lem:mono} (1.23): OK: part (d), 7 <= |T'|.
- sections/mb.tex:683 -> \ref{fd:lem:pos-cycle} (1.38): OK: cyc7, cyc8 are the positive-cycle wrappers (mm:lem:cyc).
- sections/mb.tex:684 -> \ref{mm:thm:mirror-polygon} (9.8): OK.
- sections/mb.tex:684 -> \ref{mm:thm:axis-polygon} (9.10): OK.
- sections/mb.tex:705 -> \ref{fd:lem:mono} (1.23): OK: part (b).
- sections/mb.tex:708 -> \ref{fd:lem:mono} (1.23): OK: part (c).
- sections/mb.tex:784 -> \ref{fd:lem:affine-orient} (1.17): OK: frame is affine with linear part M, det M = nu.
- sections/mb.tex:796 -> \ref{fd:lem:affine-cp} (1.27): OK: part (b), g injective affine, T finite.
- sections/mb.tex:810 -> \ref{mm:thm:line} (9.23): OK: part (a) is transport with the same four conclusions.
- sections/mb.tex:813 -> \ref{fd:lem:collinear} (1.20): OK.
- sections/mb.tex:814 -> \ref{fd:lem:collinear} (1.20): OK.
- sections/mb.tex:837 -> \ref{mm:thm:mirror-polygon} (9.8): OK (written proof via Lemma mb:lem:polygons).
- sections/mb.tex:837 -> \ref{mm:thm:axis-polygon} (9.10): OK.
- sections/mb.tex:852 -> \ref{mm:thm:odd} (9.17): OK: j=3, M=16, 2<=j; (hM) is exactly Proposition mb:prop:cap16; 2M=32; Lean mirror_seven' at line 2631.
- sections/mb.tex:855 -> \ref{mm:thm:mirror-polygon} (9.8): OK: mirror_odd_general uses cap_mirror_polygon (MirrorMain.lean:2520).
- sections/mb.tex:855 -> \ref{mm:thm:axis-polygon} (9.10): OK: mirror_odd_general uses axis_left_polygon and axis_right_polygon (lines 2534, 2539).
- sections/mb.tex:877 -> \ref{mm:thm:mirror-polygon} (9.8): OK (through Lemma mb:lem:polygons(b)).
- sections/mb.tex:882 -> \ref{fd:lem:mono} (1.23): OK: part (b).
- sections/mb.tex:884 -> \ref{fd:lem:mono} (1.23): OK: part (c).
- sections/mb.tex:896 -> \ref{mm:thm:even} (9.18): OK: j=4, M=22; (hM) is exactly Proposition mb:prop:cap22; 2M+2=46; Lean mirror_eight' at line 2636.
- sections/mb.tex:922 -> \ref{mm:thm:odd} (9.17): OK.
- sections/mb.tex:922 -> \ref{mm:thm:line} (9.23): OK.
- sections/mb.tex:966 -> \ref{mm:thm:odd} (9.17): OK: paraphrase faithful (j>=2, (hM) for every r and every configuration, same quantifier order, conclusion 2M). Instance j=4, M=113: (hM) = Proposition mb:prop:cap113; Lean mirror_nine = mirror_odd_general 4 113.
- sections/mb.tex:970 -> \ref{mm:thm:line} (9.23): OK: part (b), mirror_odd_general_line at line 2641.
- sections/mb.tex:981 -> \ref{sr:def:classes} (7.7): OK: classes (4), (5) use reflLine.
- sections/mb.tex:1001 -> \ref{fd:def:inv} (1.10): OK: Invariant = maps into (RTC copy of SymReduction.Invariant, same text).
- sections/mb.tex:1008 -> \ref{mm:thm:mirror-polygon} (9.8): OK.
- sections/mb.tex:1008 -> \ref{mm:thm:axis-polygon} (9.10): OK.
- sections/mb.tex:1030 -> \ref{sr:def:classes} (7.7): OK: (a), (b) agree with sr (4), (5) and with the Lean text (SymmetricReduction.lean:482, 488; RTC copies at +26).
- sections/mb.tex:1043 -> \ref{mm:thm:mirror-polygon} (9.8): OK.
- sections/mb.tex:1043 -> \ref{mm:thm:axis-polygon} (9.10): OK.
- sections/mb.tex:1055 -> \ref{sr:def:classes} (7.7): OK: classes (1)-(3).
- sections/mb.tex:1059 -> \ref{sr:def:iso} (7.1): OK.
- sections/mb.tex:1073 -> \ref{sr:thm:main} (7.39): OK: hypotheses (S finite, general position, 33<=|S|, IsEucIsometry g, g != id, Invariant g S, five classes) are exactly supplied; argument order matches the Lean term at RTC:4296.
- sections/mb.tex:1078 -> \ref{ar:thm:main} (8.28): OK: part (a) (AffineEquiv, g != refl, maps into), with the five classes.
- sections/mb.tex:1082 -> \ref{sr:thm:main} (7.39): OK: RTC line 1023 is the byte-identical copy of SymmetricReduction.lean:997 (diff RTC 38-1084 vs SR 12-1058).
- sections/mb.tex:1082 -> \ref{ar:thm:main} (8.28): OK: RTC line 1527 is the copy of AffineReduction.lean:1501 (diff RTC 38-1559 vs AR 12-1533).
- sections/mb.tex:1108 -> \ref{ll:thm:layers} (2.22): OK: hypotheses 0<m, K<=2m, c notin S, invariance, K-free hold for a Fivefold35 counterexample (m=5, K=7). Note: the SYM5 layer lemma also asserts that the centre lies strictly inside each layer; the text does not claim that part is Lean-checked (no LayerLemma declaration states it), so no overclaim.
- sections/mb.tex:1109 -> \ref{lg:thm:nesting} (3.16): OK: additionally 2<=m and general position hold.
- sections/mb.tex:1141 -> \ref{mm:def:config} (9.3): OK.
- sections/mb.tex:1166 -> \ref{mm:thm:odd} (9.17): OK (same claim as line 540).
- sections/mb.tex:1172 -> \ref{mm:thm:mirror-polygon} (9.8): OK.
- sections/mb.tex:1172 -> \ref{mm:thm:axis-polygon} (9.10): OK.
- sections/mb.tex:1180 -> \ref{mm:lem:slope} (9.7): OK: cap_below_lines is part (a).
- sections/mb.tex:1181 -> \ref{mm:thm:mirror-polygon} (9.8): OK.
- sections/mb.tex:1181 -> \ref{mm:thm:axis-polygon} (9.10): OK.
- sections/mb.tex:1181 -> \ref{mm:thm:odd} (9.17): OK.
- sections/mb.tex:1181 -> \ref{mm:thm:even} (9.18): OK.
- sections/mb.tex:1182 -> \ref{mm:thm:line} (9.23): OK.
- sections/mb.tex:1182 -> \ref{mm:thm:small} (9.25): OK: hasCap3_of, capacity_cup are Lemma mm:lem:cup, used in its proof ("or are used in their proofs").
- sections/mb.tex:1184 -> \ref{sr:def:iso} (7.1): OK.
- sections/mb.tex:1184 -> \ref{sr:def:classes} (7.7): OK.
- sections/mb.tex:1185 -> \ref{sr:thm:main} (7.39): OK.
- sections/mb.tex:1185 -> \ref{ar:thm:main} (8.28): OK.

## Prose cross-section claims and pointers checked (no \ref)

- sections/mm.tex:32-39 -> source hashes of MirrorMain.lean, Realization.lean and the four main-library files: OK,
  equal to the fd source table and to mb's list.
- sections/mm.tex:47-53 -> "MirrorMain.lean lines 3-2677 = RTC lines 1562-4236, offset 1559": OK (diff); mb lines 89-91
  say the same.
- sections/mm.tex:60-66 -> MirrorMain.out lines 848-863 (sixteen theorems, three axioms): OK; mb lines 63-65 cite the
  same lines with the same line-to-theorem assignment (848 mirror_seven, 849, 850, 851, 858, 862).
- sections/mm.tex:658-666 -> (hM) instances (3,16) capacity16 in mirror_seven' (2631), (4,22) capacity22g in
  mirror_eight' (2636), (4,113) capacity113 in C12Check.mirror_nine (MirrorNine_append.lean:131); logs MirrorMain.out
  860-861 and MirrorNine.out 881: OK, consistent with mb (Propositions mb:prop:cap16, mb:prop:cap22, mb:prop:cap113,
  Remarks mb:rem:seven, mb:rem:eight, Theorem mb:thm:nine and its status line).
- sections/mm.tex:935-942 -> "capacity16 applies main directly, capacity22g through geometric_capacity22, the remaining
  five through these two": OK (MirrorMain.lean:1529-1539, 1812-1817; Baek.lean:12-20).
- sections/mb.tex:538-541 and 1164-1166 -> "also stated (and proved) in the section of Theorem mm:thm:odd": OK (see the
  line-540 entry above); the restated statements (mb:def:mir, mb:lem:split, mb:lem:sort, mb:lem:polygons,
  mb:def:frame, mb:lem:frame, mb:lem:affine, mb:lem:transport) agree with their mm counterparts in every hypothesis.
- sections/mb.tex:810 -> "The same statement is part (a) of Theorem mm:thm:line": OK.
- sections/mb.tex:989-990 -> "The same definition is SymmetricReduction.lean:423" (= Definition sr:def:maps(d)): OK;
  RTC:449 = 423 + 26; formula identical to sr's.
- sections/mb.tex:1080-1083 -> RTC 1023 and 1527 = SymmetricReduction.lean:997 and AffineReduction.lean:1501: OK (diff
  and line check), so the written proofs of sr:thm:main and ar:thm:main apply.
- sections/mb.tex:1088 -> SYMLEAN/mirror/README.md section 4 and SYMLEAN/README.md section 5: OK (scope paragraph and
  the class table exist and say this).
- sections/mb.tex:1094-1104 -> evidence for HalfTurn34 and Threefold33: see F1.
- sections/mb.tex:1105-1109 -> SYM5/README.md section 2 (layer lemma): OK; the two parts said to be Lean-checked are
  covered by ll:thm:layers and lg:thm:nesting under hypotheses that hold for a Fivefold35 counterexample.
- sections/mb.tex:1117-1121 -> RTC lines 1503, 1515, 1536, 1547 (the affine variants) and 1050
  (halfTurn_of_symmetric_counterexample): OK, the copies of AffineReduction.lean 1477, 1489, 1510, 1521 (Theorem
  ar:thm:main (d), (c), (b), (e)) and SymmetricReduction.lean 1024 (Theorem sr:thm:variant), each at +26.
- sections/mb.tex:1127-1130 -> MirrorExclusionLineCopy at RTC line 1078 (= SymmetricReduction.lean:1052 + 26): OK; the
  paraphrase agrees with Definition sr:def:exclusion-line.

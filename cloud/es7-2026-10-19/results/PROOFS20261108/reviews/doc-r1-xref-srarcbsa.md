# doc-r1, lens xref-srarcbsa: cross-references from sr, ar, cb, sa to other sections

Scope: every `\ref`/`\eqref` in `sections/sr.tex`, `sections/ar.tex`, `sections/cb.tex`, `sections/sa.tex` whose label
prefix differs from the citing section (131 occurrences, extracted with a regex over the four files; no `\eqref`
crosses sections, and no reference to another section's subsection, remark or equation label occurs except
`sa:sec`), plus the prose references to other sections ("the section on ...", "the remark that follows ...", "the
convention ... at the beginning of this document", "treated in Section ..."). For each, the target was read in its
own section file and checked for (1) intended target, (2) hypotheses satisfied at the point of use, (3) no more used
than the target gives, (4) notation. All 131 labels resolve in `build/doc-r1/proofs.aux` (no `??` in `proofs.txt`).
Spot checks against the read-only repository: byte-identity of SymmetricReduction.lean 1-1058 with
AffineReduction.lean 1-1058, of RTC 38-1084 / 38-1559 with SymmetricReduction.lean 12-1058 / AffineReduction.lean
12-1533 (diff, all identical); line numbers of mirrorOneAxis33_proved (4274), mirrorNoAxis34_proved (4282),
heptagon_of_nontrivial_isometry_3 (4292), heptagon_of_nontrivial_affineEquiv_3 (4303), Vendor main (Main.lean:87,
variables at :26), baek_seven (:6); Lean signatures of heptagon_of_nontrivial_isometry (:997) and
hasConvexNGon_of_affine_symmetry (:1330); capacity16 used by mirror_seven_of (MirrorMain.lean:1701).

Format: citing location | target | verdict.

## sr.tex

- sr.tex:76 | fd:def:point | OK (dependency list; Definition, used at :87)
- sr.tex:76 | fd:def:orient | OK (used at :89)
- sr.tex:76 | fd:def:gp | OK (used at :90)
- sr.tex:77 | fd:def:cp | OK (used at :90)
- sr.tex:77 | fd:def:ngon | OK (used at :91)
- sr.tex:77 | fd:def:inv | OK (used at :147)
- sr.tex:77 | fd:def:rot | OK (used at :185)
- sr.tex:77 | fd:lem:collinear | OK (used at :94, :691)
- sr.tex:78 | fd:lem:cp-hull | OK (used at :96, :639)
- sr.tex:78 | fd:lem:mono | OK (used at :98, :676)
- sr.tex:79 | cb:thm:c2 | OK ("Lean-checked by kernel evaluation and so computer-assisted": cb:thm:c2 is a closed `decide +kernel` statement, marked computer-assisted; Lean-checked label rests on C2FINAL/README as cb says)
- sr.tex:79 | cb:thm:c3 | OK (all_roots_covered, computer-assisted through the kernel-evaluated batch facts)
- sr.tex:81 | mb:thm:classes | OK ("written proofs of the two mirror classes"; mb's proof rests on the cited Baek theorem, as mb says)
- sr.tex:81 | mb:thm:main3 | OK
- sr.tex:82 | ar:thm:main | OK ("no proof of this section uses them": true, all five uses are in Remarks 7.8 and 7.40)
- sr.tex:87 | fd:def:point | OK
- sr.tex:89 | fd:def:orient | OK (same formula)
- sr.tex:90 | fd:def:gp | OK
- sr.tex:90 | fd:def:cp | OK
- sr.tex:91 | fd:def:ngon | OK
- sr.tex:94 | fd:lem:collinear | OK (part (b), as paraphrased)
- sr.tex:96 | fd:lem:cp-hull | OK
- sr.tex:98 | fd:lem:mono | OK (parts (b), (a), (c) in that order)
- sr.tex:147 | fd:def:inv | OK (maps into; equality only for injective f, as fd says)
- sr.tex:185 | fd:def:rot | OK (identical formula; fd's head also cites SymReduction.rotAbout at SymmetricReduction.lean:400)
- sr.tex:266 | cb:thm:c2 | OK (bookkeeping of the subcase orbits of HalfTurn34; "that the listed subcases are refuted rests on the records" matches cb:rem:c2-scope)
- sr.tex:272 | cb:thm:c3 | OK (cover of the 910 roots; leaf records checked outside Lean matches cb:rem:use)
- sr.tex:286 | mb:thm:classes | OK (the same bullet explains that RTC's classes are byte-identical copies, verified)
- sr.tex:639 | fd:lem:cp-hull | OK (applied to the finite set s)
- sr.tex:633-647 (no ref) | fd:lem:strict-supports | PROBLEM (minor): Lemma sr:lem:supports restates fd:lem:strict-supports (same Lean declaration ErdosSzekeres.Suk.convexPosition_of_strict_supports, ErdosSzekeres/Suk/SupportingLines.lean:28, same statement) without referring to it; the appendix map lists the declaration under both labels
- sr.tex:676 | fd:lem:mono | OK (part (c), T a subset of S)
- sr.tex:691 | fd:lem:collinear | OK (part (b): q, c, q' pairwise distinct points of S with orientation 0)
- sr.tex:973 | mb:thm:main3 | OK (part (a) has exactly HalfTurn34, Threefold33, Fivefold35 as hypotheses; stated in RTC for the copies)
- sr.tex:978 | ar:thm:main | OK
- sr.tex:1129-1130 (prose) | "the section on affine symmetries" (ar) | OK (ar covers AffineReduction.lean 1059-1533)
- sr.tex:1133-1134 (prose) | "the section on mirror bounds" (mb) | OK (mb covers RTC Part C and the MIRRORETV files)

## ar.tex

- ar.tex:4 | sr:thm:main | OK
- ar.tex:11 | sr:thm:main | OK (E(33,7) supplied under the five class hypotheses, said in the next sentence)
- ar.tex:14 | sr:thm:main | OK ("five of the six classes, all except Fourfold32" = the hypotheses of sr:thm:main)
- ar.tex:14 | sr:def:classes | OK
- ar.tex:32 | sr:thm:main ("the section of") | OK (lines 1-1058 byte-identical, verified)
- ar.tex:82 | fd:def:point | OK
- ar.tex:82 | fd:def:orient | OK
- ar.tex:82 | fd:def:gp | OK
- ar.tex:82 | fd:def:cp | OK
- ar.tex:83 | fd:def:ngon | OK
- ar.tex:83 | fd:def:inv | OK
- ar.tex:83 | fd:lem:collinear | OK
- ar.tex:84 | fd:lem:cp-hull | OK
- ar.tex:85 | fd:lem:affine-orient | OK (announces the re-proof; ar:lem:orient-affine shares the Lean name and says "This is Lemma 1.17")
- ar.tex:85 | fd:lem:affine-cp | OK (ar:lem:cp-affine, gp-affine, ngon-affine, inj share Lean names with fd (b')-(e'); statements agree; the duplication is announced here)
- ar.tex:86 | sr:def:iso | OK
- ar.tex:87 | sr:def:classes | OK
- ar.tex:87 | sr:thm:main | OK
- ar.tex:112 | fd:def:inv | OK (AffineReduction.lean:271 is the identical copy)
- ar.tex:114 | fd:def:gp | OK
- ar.tex:114 | fd:def:cp | OK
- ar.tex:114 | fd:def:ngon | OK
- ar.tex:114 | fd:lem:collinear | OK (part (b))
- ar.tex:116 | fd:lem:cp-hull | OK
- ar.tex:123 | sr:def:iso | OK (lines 265, 268 identical in both files)
- ar.tex:289 | fd:lem:affine-orient | OK ("the case v = 0": lin2(a,b,c,d) has matrix (a b; c d), determinant ad - bc)
- ar.tex:375 | fd:lem:affine-orient | OK (same Lean theorem orient_affine at :1241; L, b versus A, v is explained in fd)
- ar.tex:410 | fd:lem:collinear | OK (part (b) for the finite image f(S))
- ar.tex:412 | fd:lem:collinear | OK
- ar.tex:455 | fd:lem:cp-hull | OK (f(S) finite)
- ar.tex:461 | fd:lem:cp-hull | OK
- ar.tex:515 | fd:lem:collinear | OK
- ar.tex:658 | sr:def:classes | OK (copies explained at :29-33)
- ar.tex:682 | sr:thm:main | OK (premises and their order equal (hE) with N = 33, n = 7; checked against the Lean signatures)
- ar.tex:705 | sr:thm:main | OK
- ar.tex:711 | sr:def:classes | OK (the five summaries match the class texts)
- ar.tex:717 | mb:thm:classes | PROBLEM (minor): line numbers 4274 and 4282 are right, but the remark is about the Lean premises hm1, hm0 of ar:thm:main, which are the constants of AffineReduction.lean; mirrorOneAxis33_proved and mirrorNoAxis34_proved prove the same-text copies in RTC (a separately compiled file). sr:rem:records and mb ("Copies of the same code") state this identification by text; ar:rem:classes does not
- ar.tex:720 | mb:thm:baek | OK
- ar.tex:722 | mb:thm:main3 | OK (heptagon_of_nontrivial_affineEquiv_3, RTC:4303 = mb:thm:main3(b), the three-class form of ar:thm:main(a))
- ar.tex:742 | cb:thm:c3 | OK ("cover of the 910 threefold roots", decide +kernel)
- ar.tex:742 | cb:thm:c2 | OK ("closure of the central parallelogram orbits")
- ar.tex:760 | sr:thm:variant | OK
- ar.tex:798 | sr:thm:main ("the section of") | OK (iterate_mem :69 and point_ext :502 are in sr:lem:iterate and sr:lem:complex)
- ar.tex:805 | mb:thm:main3 ("the section of") | OK (mb treats RTC Part C, lines 4238-4322)

## cb.tex

- cb.tex:11 | sr:def:classes | OK (Threefold33: 33 points, rotation by 2pi/3, centre not in S, hence 11 orbits)
- cb.tex:21 | sr:def:classes | OK (HalfTurn34: 34 points, 17 antipodal pairs)
- cb.tex:96 (prose) | "The proofs of this section use no other section" | OK (the three cross-section refs are outside proofs)
- cb.tex:1486 | sa:sec | OK (sa treats SizeArith.lean, 20 theorems; AssembledSizes.lean, 7 theorems and the example; BaekSeven.lean, baek_seven; resolves to Section 12). Note: sa:sec is not in the contract's export table because sa is new in this run; accepted as in the cb doc-r0 and doc-r1 audits

## sa.tex

- sa.tex:3 (prose) | "no other section covers" | OK (consistent with cb.tex:1482-1486)
- sa.tex:15 | sr:def:classes | OK
- sa.tex:26 | mb:thm:baek | OK (instance n = 4: 17 elements, 4-cap or 7-gon)
- sa.tex:40 | ec:thm:compat | OK (parts (a), (b) under (O): m divides |T| for 0 not in T, and |S| mod m = [0 in S] mod m; ec writes m for the order, sa writes s; the renaming is harmless)
- sa.tex:42 | sr:lem:orbit | OK
- sa.tex:43 | sr:thm:main | OK (the counting is in halfTurn_facts, rot_erase_facts, case_mirror used by its proof)
- sa.tex:44 | ll:thm:layers | OK (used by the ec proofs through ll:thm:reduction, whose proof applies card_peel, which applies layers_are_orbits)
- sa.tex:44 | ll:thm:card-peel | OK (same remark; ll:thm:reduction would be the direct citation, but the sentence is true)
- sa.tex:45 | ec:thm:fourfold | OK ("exactly 32": m = 4, t = 8)
- sa.tex:45 | ec:thm:fivefold | OK ("exactly 35": m = 5, t = 7; order of "respectively" matches)
- sa.tex:46 | ll:lem:minperiod | OK (used at :452)
- sa.tex:46 | lg:lem:centre | OK (used at :461)
- sa.tex:49 | sr:thm:main | OK
- sa.tex:50 | ar:thm:main | OK
- sa.tex:110 (prose) | rigor-label convention "at the beginning of this document" | OK (fd.tex:73-75: decide only on facts the written proof establishes by hand does not make a statement computer-assisted)
- sa.tex:113 | mb:thm:baek | OK
- sa.tex:346 | mb:thm:baek | OK (recalled notions agree with mb:def:config: caps and cups by consecutive triples, gons with |l| + |l'| = n + 2, HasNCap, HasNGon)
- sa.tex:371 | mb:thm:baek | OK
- sa.tex:374 | mb:thm:baek | OK (all hypotheses: linear order, n = 4, C, finite S, binom(6,2) + 2 = 17 <= |S|)
- sa.tex:385 | mb:thm:baek | OK
- sa.tex:392 | mb:thm:baek | OK (argument order and Main.lean:87 with the variables of :26 match mb's head; verified)
- sa.tex:407 | mb:thm:baek | OK (capacity16 = mb:prop:cap16 at MirrorMain.lean:1529, the N = 7 instance for point configurations)
- sa.tex:408 | mm:def:config | OK ("configuration of n points" and "has a k-cap" are defined there)
- sa.tex:409 | mb:thm:seven | OK (mirror_seven_of, used by mirror_seven, applies capacity16 at MirrorMain.lean:1701; mb records the axioms of mirror_seven at MirrorMain.out:848)
- sa.tex:419 | fd:def:rot | OK (rho_{c,theta} notation and complex form are fd's)
- sa.tex:426 | fd:def:inv | OK (maps into)
- sa.tex:436 | sr:def:classes | OK (the displayed sigma equals reflLine of sr:def:maps(d))
- sa.tex:452 | ll:lem:minperiod | OK (hypotheses 0 < s and y != c hold; per = s gives rho^s(y) = y and rho^i(y) != y for 0 < i < s by the definition in ll (C2), (P1), (P2))
- sa.tex:461 | lg:lem:centre | OK (0 < s, s even, invariance, general position, a point p in S with p != c)
- sa.tex:469 | sr:def:classes | PROBLEM (minor): "(This is also shown after Definition 7.7.)" The fixed-point argument is the last paragraph of Definition 7.7 itself (sr.tex:231-235, inside the definition environment), not after it
- sa.tex:477 | fd:def:gp | OK (collinear = span of differences of dimension at most 1)
- sa.tex:480 | fd:lem:mono | OK (parts (b) and (c))
- sa.tex:498 | sr:def:classes | OK (HalfTurn34 for T and c: general position, |T| = 34, c not in T, invariance under halfTurn c = rho_{c,pi})
- sa.tex:512 | sr:thm:variant | OK (the only reduction theorem with Fourfold32)
- sa.tex:513 | ec:thm:fourfold | OK (its hypothesis is LayerLemma.Fourfold32, ec:def:cases)
- sa.tex:524 | sr:lem:concyclic | OK (O(y) finite, all points at the same squared distance from c)
- sa.tex:525 | fd:lem:mono | OK (part (a); |O(y)| = s >= 7)
- sa.tex:526 | fd:def:ngon | OK
- sa.tex:539 | sr:thm:structure | OK (part (b): n >= 33 > 1, isometry, g != id, maps S into S; alternatives (i), (ii) restated correctly)
- sa.tex:545 | ar:thm:transfer | OK
- sa.tex:546 | ar:thm:main | OK
- sa.tex:554 | sr:thm:main | OK
- sa.tex:554 | ar:thm:main | OK
- sa.tex:555 | sr:thm:main | OK ("passes to a power ... half-turn or odd prime order": sr's proof via sr:lem:root-cases)
- sa.tex:557 | mb:thm:classes | OK (mb:thm:classes states the two classes of Definition 7.7 hold; the copy issue is explained in the remark that sa.tex:559 points to)
- sa.tex:558 | mb:thm:main3 | OK (conditional on HalfTurn34, Threefold33, Fivefold35)
- sa.tex:559 | sr:def:classes + "the remark that follows" | OK (Remark 7.8 = sr:rem:records follows Definition 7.7)
- sa.tex:576 | ec:thm:fourfold | OK (at least 29 points, rotAbout(c, 2pi/4), no hypothesis c not in S; hence bound 28)
- sa.tex:579 | ec:thm:fivefold | OK (at least 32 points; bound 31)
- sa.tex:581 | mb:thm:refl32 | OK (part (b): no class hypothesis, any number of points on the mirror)
- sa.tex:582 | mb:thm:seven | OK (part (b) is what the proof of mb:thm:refl32(b) applies)
- sa.tex:583 | mb:thm:classes | OK
- sa.tex:601 | mb:thm:baek | OK

## Findings

1. minor, sr (sr.tex:633-647): Lemma sr:lem:supports duplicates fd:lem:strict-supports (same Lean declaration and
   file:line) without a cross-reference. Fix: cite Lemma fd:lem:strict-supports in the proof of sr:lem:concyclic and drop
   sr:lem:supports (and its map row), or keep it and add "This is Lemma fd:lem:strict-supports; the proof is repeated
   for convenience" to its proof and to the Coverage paragraph.
2. minor, ar (ar.tex:715-717): ar:rem:classes calls MirrorOneAxis33 and MirrorNoAxis34 Lean-checked theorems without
   saying that mirrorOneAxis33_proved and mirrorNoAxis34_proved prove the byte-identical copies in RTC, not the
   constants of AffineReduction.lean that are the premises hm1, hm0 of ar:thm:main. Fix: add "(for the byte-identical
   copies of the class definitions in that file, which does not import SYMLEAN/AffineReduction.lean; the two texts are
   identified by text, as in Remark 7.8)".
3. minor, sa (sa.tex:469): "(This is also shown after Definition sr:def:classes.)" should read "(This is also shown
   at the end of Definition sr:def:classes.)".

No blocker or major finding: every cross-reference resolves to the intended statement, every cited hypothesis is
met at the point of use, no citing text uses more than the cited statement gives, and the notational differences
(m versus s, Invariant f S versus Invariant(f, S), L, b versus A, v, iterate recursions) are explained or harmless.

# A7: lower-bound examples

Component audit, 1 November 2026 (UTC), against `es7-cloud` at 9cf4949a5. Texts returned by the auditor and by the independent verifier of each finding, lightly edited: machine paths replaced by placeholders and internal job names by descriptions; trust-table labels as explained in `../README.md`, §7.

**Component.** LOWER-BOUND EXAMPLES (SYMMAX 3-/4-/5-/6-fold and mirror sets, SYMMAX/k6 hexagon sets, SYM2 central 32-point set, SYM5/c5_31minus_centre)

**Statement audited.** Each example file cited in the symmetric tables has the claimed number of points and the claimed exact symmetry, has no three points collinear, and has no K points in convex position (K = 7, or K = 6 for k6/). The files are: SYMMAX/{c3_27,c3_30,c3_31,c4_28,c5_30,c5_31,c6_30,mirror_32}points.txt, SYMMAX/k6/{c2_16,c3_13,c4_16,c5_16,mirror_12}points.txt, SYM2/sym7_32points.txt and SYM5/c5_31minus_centre.txt. These examples give the lower bounds N(C3)>=31, N(mirror)>=32, N(C6)>=30, N(C4)>=28, N(C5)>=31, N(C2)>=32, plus the hexagon rows (C2, C4, C5 >= 16; C3 >= 13; mirror >= 12).

**Verdict.** `sound_with_caveats`

## Summary

Verdict: sound with caveats. Every lower-bound example in the symmetric tables is correct. I re-checked all 15 files with my own exact-arithmetic code, written independently. The checks were exact symmetry and orbit structure, distinctness, general position (with orientation computed by two exact formulas plus high-precision numerics), and an O(n^4) cup/cap DP run in four linear orders. Each file was also enumerated exhaustively in C over every K-subset with two convexity criteria, and the DP was compared with brute force on random subsets. Results: c3_27 (27 points), c3_30 (30), c3_31 (31 with centre), c6_30 (30), c4_28 (28), c5_30 (30), c5_31 (31 with centre), c5_31minus_centre (30), mirror_32 (32, no axis point) and SYM2/sym7_32 (32 antipodal points) all have largest convex subset exactly 6 and 0 convex 7-subsets. The k6 sets c2_16, c3_13, c4_16, c5_16 and mirror_12 all have largest convex subset 5 and 0 convex 6-subsets. Every count and coordinate bound stated in the READMEs is reproduced, including 27,055 convex 6-subsets for sym7_32. The project's own checkers reproduce on copies, and their orientation tables are identical to mine. Exactness for the irrational rotations comes from exact algebraic coordinates (Z[w] for 3- and 6-fold, Z[zeta5] for 5-fold), not from approximations. Caveats, both documentation only: (A7-1) the Z[zeta5] files are correct only for zeta = e^{+-2pi i/5}; with the Galois-conjugate embedding the same integers contain convex 10-gons (or a 7-gon for k6), and the files do not record the convention, which is stated only in SYMMAX/README.md. (A7-2) The LaTeX note wrongly says the SYM2 example was found by annealing; it is the explicit construction, and build.py regenerates it exactly. The examples also show that the threshold 33 is sharp for symmetric sets. Upper bounds and Corollary 3 are outside this component. All scripts and logs are in AUDIT3/A7_examples/ (main ones: a7lib.py, verify_all.py, brute_a7.c, verify_all.log, summary.json, embedding_test.log, check_provenance.log).

## Trust table

| # | claim | basis | notes |
|---|---|---|---|
| 0 | c3_31points.txt: 31 distinct points of Z[w] (w=e^{2pi i/3}): the centre plus 10 orbits of 3. Invariant under the exact 120-degree rotation, no collinear triple (centre included), largest convex subset 6. All 2,629,575 7-subsets are non-convex. | exact computation (two independent methods) | Re-checked by the auditor with exact integer arithmetic. Two independent algorithms of my own: a DP using the leftmost-anchor cup/cap decomposition, run in 4 different linear orders, and an exhaustive C enumeration that tests every subset with 2 different convexity criteria. The project's verifyg.py and brute.c, run on copies, give identical results, and the orientation tables match entry by entry. |
| 1 | c3_30 (30 points, 10 orbits, no centre) and c3_27 (27 points, 9 orbits): 3-fold, general position, max convex 6, 0 convex 7-subsets (2,035,800 and 888,030 subsets). | exact computation (two independent methods) | Same method as c3_31. |
| 2 | c6_30: 30 points in 5 orbits of 6, no centre. Invariant under the exact 60-degree rotation (so also under C3 and C2). General position, max convex 6, 0 of 2,035,800 7-subsets convex. | exact computation (two independent methods) |  |
| 3 | c4_28: 28 integer points in 7 orbits of 4, invariant under (x,y)->(-y,x), no centre, general position, max convex 6, 0 of 1,184,040 7-subsets convex. \|coord\| <= 147. Each of its 7 convex layers is a single orbit (a quadrilateral). | exact computation (two independent methods) |  |
| 4 | c5_31: 31 points of Z[zeta5] (centre plus 6 orbits of 5) with zeta=e^{2pi i/5}. Invariant under multiplication by zeta, general position including the centre, max convex 6, 0 of 2,629,575 7-subsets convex. | exact computation (two independent methods) | Orientation signs are computed exactly in Z[sqrt5] by two different exact formulas: my own affine coordinates (4Re, 2Im/sin72), and the cyclotomic Im(conj(u)v) formula. They agree on every triple, and 90-digit numerics agree; the smallest \|cross\| is 0.489. The result holds only for zeta=e^{+-2pi i/5}; see finding A7-1. |
| 5 | c5_30 (30 points, 6 orbits) and c5_31minus_centre (30 points, exactly c5_31 without 0): 5-fold, general position, max convex 6, 0 of 2,035,800 7-subsets convex. Each has 6 convex layers, each a single orbit. | exact computation (two independent methods) |  |
| 6 | mirror_32: 32 integer points in 16 pairs under (x,y)->(-x,y), none on the axis. General position, max convex 6, 0 of 3,365,856 7-subsets convex. | exact computation (two independent methods) |  |
| 7 | SYM2/sym7_32points.txt: 32 integer points (\|coord\| <= 1,250,000) in 16 antipodal pairs, origin not in the set. General position, max convex 6, 0 of 3,365,856 7-subsets convex, and exactly 27,055 of the 906,192 6-subsets convex, as the README states. | exact computation (two independent methods) | build.py's sym(7,X=50,Y=10000,K=3) reproduces the file exactly, as the same ordered list. |
| 8 | k6 sets: c2_16 (C2 only, 8 pairs), c3_13 (C3, centre plus 4 orbits, Eisenstein), c4_16 (C4), c5_16 (C5, centre plus 3 orbits) and mirror_12 (5 pairs plus 2 axis points). All are in general position with max convex 5 and 0 convex 6-subsets (8,008 / 1,716 / 8,008 / 8,008 / 924 subsets). | exact computation (two independent methods) |  |
| 9 | Exactness for the irrational-angle rotations (120, 60 and 72 degrees). The symmetries are exact ring multiplications (by w, 1+w and zeta) acting on integer coordinates, and orientation signs are decided exactly (Z^2 after a linear map of determinant sqrt3/2 > 0; Z[sqrt5] after an orientation-preserving diagonal scaling). No rational approximation or margin argument is used. | written proof, re-derived by the auditor | Derived independently; the integer maps were also confirmed numerically to be the claimed rotations, with error below 1e-84. |
| 10 | The table lower bounds: N(C3)>=31, N(mirror)>=32, N(C6)>=30, N(C4)>=28, N(C5)>=31, N(C2)>=32; hexagons C2, C4, C5 >= 16, C3 >= 13, mirror >= 12. | exact computation (follows from rows 0-8) | These follow directly from the verified examples. The upper bounds are outside this component. |
| 11 | The overall threshold 33 is sharp for symmetric sets: 32-point 7-gon-free sets with a mirror (mirror_32) and with central symmetry (sym7_32) exist. | exact computation (follows from rows 6-7) |  |
| 12 | SYM2 general construction: for every odd k there is a centrally symmetric set of 2^(k-2) points in general position with no convex k-gon. | written proof, re-derived by the auditor | I re-derived the cubic-cluster proof (slope identity, chain lemma, count) and found no error. Epsilon is qualitative; the k=7 instance is exactly verified, and k=9 by DP only (next item). |
| 13 | SYM2/sym9_128points.txt (k=9): 128 points, centrally symmetric, general position, largest convex subset 8. | exact computation (one method; no full enumeration) | My exact DP in 2 orders, with the witness verified, plus 40 random or window subsets checked exhaustively against the DP. A full 9-subset enumeration is infeasible. The file is outside the ES(7) tables. |
| 14 | Novelty or attribution of the examples (for example 'no earlier counterpart' for the 5-fold 31-point set). | not assessed | Not assessed in this component. |

## Findings

### A7-1 (minor): The Z[zeta5] example files depend on the choice of embedding and do not say which one; the convention is stated only in SYMMAX/README.md

The 5-fold files (c5_30, c5_31, c5_31minus_centre, k6/c5_16) contain integer 4-tuples. These define a planar set only after zeta is fixed. With the documented zeta = e^{2pi i/5}, or its complex conjugate (a mirror image), every claim holds. With the Galois-conjugate embeddings zeta -> e^{+-4pi i/5} (sqrt5 -> -sqrt5), the same integers give C5-invariant sets in general position that contain convex 10-gons (c5_30, c5_31) and a convex 7-gon (k6/c5_16, where K=6). The convention appears in SYMMAX/README.md ('z = e^(2 pi i/5)') and implicitly in verify5.py, which SYM5/validate_layers.py also executes, so the SYM5 validation uses the correct embedding. However, the data files have no header, and SYMMETRIC.md section 2 and the LaTeX note (Prop. C) cite the files without the convention. A similar, harmless point applies to the 3-fold and 6-fold files: read as Cartesian integers they are only affinely symmetric (under an integer matrix of order 3 or 6). The Euclidean-symmetric set is their image under (a,b) -> (a - b/2, b*sqrt3/2). The claims are correct as documented, but someone re-checking with a computer-algebra system's default primitive root could get a contradicting result.

*Evidence.* AUDIT3/A7_examples/embedding_test.log (max convex 6/6/5 with j=1 and j=4; 10/10/7 with j=2 and j=3)

*Suggested fix.* Add a '#' header line to each data file stating the format and embedding (the project parsers already skip '#' lines). State the coordinate conventions in the note next to Prop. C, or in an appendix.

**Independent check:** real = yes; severity minor -> **minor**.

I re-checked this from scratch. I did not use verify5.py's Im(conj(u)v) formula or the auditor's a7lib. I computed planar coordinates exactly in Z[sqrt5] (4x = X and 2y/sin72 = Y, from closed forms of cos and sin of 2*pi*m/5) and took orientations as exact 2x2 determinants. I also recomputed every sign with 80-digit Decimal numerics, using pi by Machin's formula and cos/sin by Taylor series, so the closed forms are not trusted. I found the largest convex subset with two algorithms of my own: a branch and bound over 4-point convexity bitmasks, and an angular DP anchored at the leftmost vertex. Both match brute force on random subsets.

What is confirmed:
(1) All four Z[zeta5] files are bare integer 4-tuples with no header; every line is numeric. The files are c5_30, c5_31, SYM5/c5_31minus_centre (exactly c5_31 without its centre line) and k6/c5_16.
(2) With zeta -> e^{2 pi i j/5} for j=1 (the documented choice) and j=4 (its mirror image), all four sets are C5-invariant with 0 collinear triples. Their largest convex subsets are 6, 6, 6 and 5, and none has a convex 7-subset (6-subset for k6). The counts of convex 6-subsets (3270, 8445, 6525) and of convex 5-subsets for k6 (723) match the auditor's brute force exactly.
(3) With j=2 or 3 (the Galois conjugates, sqrt5 -> -sqrt5), the sets are still C5-invariant and in general position. That is expected: three points are collinear exactly when conj(u)v is real, and that does not depend on the embedding. But the largest convex subset becomes 10 for c5_30, c5_31 and c5_31minus_centre, and 7 for k6/c5_16 (K=6). I found explicit convex 10-gons and a convex 7-gon and verified each by the 4-point criterion and by cyclic left turns. This reproduces the auditor's 6/6/5 versus 10/10/7 and adds c5_31minus_centre, which the auditor's log did not cover.
(4) The orientation in the project's verify5.py agrees with my j=1 orientation on every triple. It agrees with j=4 on none (a global flip) and with j=2 or 3 on about half. So the project's checker uses j=1, and so do validate_layers.py, which runs that code, and anneal5.c, which uses the same formula. Every claim holds under the documented convention.
(5) SYMMETRIC.md §2 cites SYMMAX/c5_31points.txt, and the proof of Prop. C in the note says "exact examples in SYMMAX". Neither says how the coordinates are encoded.
(6) The 3-fold/6-fold remark is correct and harmless. The files are closed under the integer maps (a,b)->(-b,a-b) and (a,b)->(a-b,a), of order 3 and 6, which are not orthogonal. M(a,b) = (a-b/2, b*sqrt3/2) turns them into Euclidean 120° and 60° rotations and keeps every orientation (0 mismatches). SYMMAX/README.md and verifyg.py already document this.

Small inaccuracies in the finding, none of which changes the verdict:
- The convention is not only implicit in verify5.py: its docstring states "z = e^(2 pi i/5)", anneal5.c's header states it too, and SYM5/README.md points to verify5.py's arithmetic. "Stated only in SYMMAX/README.md" is true of the prose documentation, not of the code.
- Sage's CyclotomicField uses e^{2 pi i/n} by default, so the real risk is a re-checker who picks an arbitrary root of Phi5, not one who takes a CAS default.
- The suggested '#' header would break shrink.py and shrink5.py, which do not skip '#' lines. The verification parsers (verify5.py, verifyg.py, validate_layers.py, validate_z2.py) do skip them.

Severity is minor. No claim is threatened: the README next to the files fixes the embedding, including the exact orientation formula, and the official verifier hard-codes it. But the data files and both write-ups leave the embedding unstated, and the wrong guess (2 of the 4 roots of Phi5) gives a contradicting result with convex 10-gons. A cheap fix is to add a header line to each file and one sentence near Prop. C.

*Verifier's evidence.* Scripts and logs are in AUDIT3/A7_examples/verify_A7-1/:

- embed_check.py and embed_check.log: the independent exact check for every file and every embedding j=1..4. Numeric sign mismatches 0; collinear triples 0. Largest convex subset 6/6/6/5 for j=1,4 and 10/10/10/7 for j=2,3, with explicit witness polygons. For example, for c5_31 under j=2, the 10-gon is [-71 6 -25 -46] [-46 19 86 -33] [-31 -52 -6 -77] [67 -52 -19 -65] [46 -25 52 21] [33 -13 52 119] [77 46 25 71] [65 132 13 46] [-21 25 -46 31] [-119 -86 -132 -67].
- convention_check.py and convention_check.log:
  - verify5.py's orientation agrees with j=1 on all triples (4060/4060, 4495/4495, 4060/4060, 560/560), with j=4 on 0, and with j=2/3 on about 50%.
  - The Eisenstein files are closed under order-3/6 non-orthogonal integer maps, and integer and Euclidean orientations agree on every triple.

Repository files: R=results
- R/SYMMAX/README.md, 'Coordinates' section: z = e^(2πi/5), with the orientation formula.
- R/SYMMAX/verify5.py, docstring: z = e^(2 pi i/5).
- R/SYMMAX/anneal5.c, lines 1-4.
- R/SYM5/README.md §3: 'arithmetic as in results/SYMMAX/verify5.py'.
- R/WRITEUP/SYMMETRIC.md line 82: cites the file with no coordinate convention.
- R/WRITEUP/note/symmetric_es7.tex lines 157-168 (Prop. C): 'exact examples in SYMMAX', with no coordinate convention.
- R/SYMMAX/shrink.py line 11 and shrink5.py: do not skip '#' lines.

### A7-2 (minor): The LaTeX note says all lower-bound examples were found by simulated annealing, but the SYM2 set is an explicit construction

The proof of Prop. C (symmetric_es7.tex, line 163) says: 'Lower bounds are exact examples in SYMMAX and SYM2, found by simulated annealing with exact arithmetic'. SYM2/sym7_32points.txt is not an annealing output. I confirmed that build.py's sym(7, X=50, Y=10000, K=3) reproduces it exactly, as the same ordered list, and that sym(9, 10^15, 10^15, 10^9) reproduces sym9_128points.txt. This is a provenance wording error only and has no mathematical effect.

*Evidence.* AUDIT3/A7_examples/check_provenance.log

*Suggested fix.* Change it to: the SYMMAX examples were found by simulated annealing; the SYM2 example is the explicit construction of Prop. B (build.py).

**Independent check:** real = yes; severity minor -> **minor**.

The finding is correct: the note says the SYM2 set was found by annealing, but it comes from the explicit construction. I checked the files myself and did not rely on the auditor's scripts.

(1) The note's wording. symmetric_es7.tex line 163, in the proof of Prop. C, says: "Lower bounds are exact examples in SYMMAX and SYM2, found by simulated annealing with exact arithmetic and checked by a dynamic program and by brute force over all 7-subsets." As written, "found by simulated annealing" covers every lower-bound example. The compiled PDF has the same sentence (pdftotext line 152).

(2) SYM2/sym7_32points.txt is the construction's output, not a search result:
- build.py regenerates the file exactly. I ran a byte-identical copy (same sha256) with the parameters stated in the SYM2 README. sym(7, X=50, Y=10000, K=3) gives the file as the same ordered list. sym(9, 10^15, 10^15, 10^9) does the same for sym9_128points.txt.
- The match is specific to those parameters. Five control runs with K=2, K=4, X=49, Y=9999 and the default parameters all fail to match.
- Checked without build.py, the file has exactly the cluster structure of Prop. B. There are 6 clusters of sizes 1, 5, 10, 10, 5, 1. Each cluster's bounding-box centre is exactly (50q, 10000q^3) for q = -5, -3, -1, 1, 3, 5. The 5-point cluster has no 3-cup and no 6-cap. The 10-point cluster has no 4-cup and no 5-cap. Each right cluster is the half-turn of its left partner.
- Git history agrees. Commit 5392b3584 added the point file in the same commit as build.py and the construction README, and the point file has not changed since; only the README was edited later, in 189ab709a.
- The SYMMAX README has said "The 2-fold example is the explicit construction of results/SYM2" since its first commit, e37ef4d82. Its section "How they were found" lists the annealing runs, and none is a 2-fold run. annealg.c can handle G=2, but no 2-fold run is recorded anywhere.
- The note contradicts itself: lines 200-202 present the SYM2 set as an integer instance of Prop. B.

(3) The rest of line 163 is accurate for SYMMAX. annealg.c computes orientations exactly with __int128. anneal5.c decides the sign of A + B*sqrt5 with integers. The search hits were then scaled down by shrink.py.

(4) The error has no mathematical effect. N(C2) >= 32 depends only on the properties of the set, not on how it was found, and I re-checked those properties exactly:
- the set is centrally symmetric and does not contain the origin;
- there are no collinear triples;
- none of the 3,365,856 7-subsets is in convex position (my own C brute force);
- 27,055 of the 906,192 6-subsets are in convex position, matching the SYM2 README;
- the largest absolute coordinate is 1,250,000, matching note line 200.

On a 10-point positive control, the brute force agreed with a separate convex-hull count (55 convex 7-subsets, 135 convex 6-subsets).

Severity: minor. This is a wrong factual statement in a proof in the draft (and its PDF). It conflicts with the note's own Prop. B paragraph and with the SYMMAX README. It could also suggest a computer-found example, when the note elsewhere credits the construction to Valtr via Baek and Balko. It is fixed with one sentence and does not threaten any claim.

The auditor's suggested fix is accurate. A slightly fuller version: "The SYMMAX examples were found by simulated annealing with exact orientation tests and then scaled down (shrink.py); the SYM2 example is the integer instance of Proposition B generated by SYM2/build.py, sym(7, X=50, Y=10000, K=3)."

*Verifier's evidence.* Scripts and logs, all in AUDIT3/A7_examples/verify_A7-2/:
- AUDIT3/A7_examples/verify_A7-2/check_sym2_provenance.py and AUDIT3/A7_examples/verify_A7-2/check_sym2_provenance.log: regeneration test with controls, cluster and cup/cap structure, general position.
- AUDIT3/A7_examples/verify_A7-2/no_convex.c and AUDIT3/A7_examples/verify_A7-2/no_convex.log: K=7 gives 0 of 3,365,856 subsets convex; K=6 gives 27,055 of 906,192; no anomalies in the orientation table.
- AUDIT3/A7_examples/verify_A7-2/control.log: the C brute force and a Python monotone-chain hull count agree, 55 and 135.
- AUDIT3/A7_examples/verify_A7-2/build_copy.py: copy of build.py; sha256 02c924ce... equals the repository file.

Key results:
- sym(7, X=50, Y=10000, K=3) equals the file as an ordered list (True); sym(9, 10^15, 10^15, 10^9) equals sym9_128points.txt (True); all five parameter controls are False.
- Cluster sizes are [1, 5, 10, 10, 5, 1], with centres at (50q, 10000q^3).

Sources checked (R = results):
- R/WRITEUP/note/symmetric_es7.tex: line 163 has the wrong claim; lines 200-202 call the SYM2 set an integer instance of Prop. B. The compiled PDF repeats the line 163 sentence.
- R/SYMMAX/README.md: lines 13 and 21-23 say the 2-fold example is the explicit construction; lines 73-87 list the annealing runs, and none is 2-fold.
- R/SYM2/README.md line 49 gives the build parameters.
- Git: commit 5392b3584 added sym7_32points.txt together with build.py; only README.md changed afterwards (189ab709a). The SYMMAX README at e37ef4d82 already credits SYM2 as the construction.
- R/SYMMAX/annealg.c (exact __int128 orientation) and R/SYMMAX/anneal5.c (integer sign of A+B*sqrt5) confirm "with exact arithmetic" for the SYMMAX searches.

### A7-3 (note): Exactly what is proven for the irrational-angle rotations: exact algebraic coordinates, with no approximation

3-fold and 6-fold: a row (a,b) is a + b*w in Z[w]. Rotation by 120 degrees is (a,b) -> (-b, a-b) (multiplication by w), and rotation by 60 degrees is (a,b) -> (a-b, a) (multiplication by 1+w = e^{i pi/3}). Invariance is checked by exact set equality of integer pairs. The map (a,b) -> (a - b/2, b*sqrt3/2) has determinant sqrt3/2 > 0, so every orientation sign of the true planar set equals an integer determinant. 5-fold: a row is c0 + c1 z + c2 z^2 + c3 z^3 with z = e^{2pi i/5}. Using z^4 = -1-z-z^2-z^3, multiplication by z is (c0,c1,c2,c3) -> (-c3, c0-c3, c1-c3, c2-c3). The representation is unique because 1, z, z^2, z^3 is a Q-basis. w -> (4Re w, 2Im w/sin72) maps the set into Z[sqrt5]^2 by an orientation-preserving scaling, and signs of a + b*sqrt5 are decided exactly. So for each file, the algebraic planar set itself is exactly invariant, in general position, and free of convex K-gons. Irrational coordinates are unavoidable for 5-fold symmetry, since no rational 2x2 matrix has order 5 (Phi_5 has degree 4). The smallest |orientation determinant| in true coordinates is 0.489 for c5_31 (coordinates up to about 1.2e3), so even double-precision arithmetic would have had ample margin; exact arithmetic was used anyway.

*Evidence.* a7lib.py (affine_coords, orient_A, orient_B, MAPS); verify_all.log; summary.json (numeric_isometry_max_error <= 1e-84; min_abs_numeric_cross)

### A7-4 (note): All 15 example files pass every check; results match the README numbers and the project's own checkers

Point counts, distinctness, symmetry, orbit structure and centre status (centre present exactly in c3_31, c5_31, k6/c3_13, k6/c5_16; no point on the mirror axis in mirror_32; 2 axis points in k6/mirror_12) are all as claimed. Every file has 0 collinear triples. The DP gives K-1 in all four orders. The exhaustive count of convex K-subsets is 0 under both criteria, with the subset totals equal to C(n,K) as in the README. Every coordinate bound in the README matches (287, 306, 1017, 147, 456, 614, 1,250,000). The layer structure agrees with the layer lemma and with the SYM5 section 3 and C2SGN/midpoint statements: c4_28 has 7 single-orbit quadrilaterals, c5_30 and c5_31minus_centre have 6 single-orbit pentagons, c6_30 has 5 single-orbit hexagons. In the odd-order sets no pair is collinear with the centre; in the even-order sets exactly the antipodal pairs are.

*Evidence.* verify_all.log, summary.json, project_checkers_on_copies/project_checkers.log, orient_table_comparison.log, centre_collinearity.log

### A7-5 (note): Scope: the examples give only lower bounds, and they show that the threshold 33 in the overall claim is sharp

mirror_32 (a mirror and no point on the axis) and sym7_32 (central symmetry) are 32-point symmetric sets with no convex 7-gon. The overall statement 'at least 33 symmetric points contain a convex 7-gon' therefore cannot be lowered to 32. The upper bounds (Theorems 1, 2a, 2b, the fivefold and fourfold exclusions, central 34) and the group-theoretic Corollary 3 are not part of this component and were not audited here. The SYM2 odd-k construction proof was re-derived and found correct. sym9_128 (k=9) was checked by DP only, the same as the project's own check.

## Tests run by the auditor

- test_dp_random.py: my DP compared with exhaustive brute force (Andrew hull test) on 740 random general-position sets (Z2, Eisenstein, Z[zeta5], pairs of concentric pentagons), with true maxima from 4 to 11: 0 failures (test_dp_random.log)
- test_dp_extremes: 30 points on a parabola give 30; Erdos-Szekeres sets g(4,4)=4, g(5,5)=6, g(4,6)=6, matching the cup+cap bound (test_dp_extremes.log)
- test_brute.py: brute_a7.c convex-subset counts (TRI and WRAP criteria) compared with independent Python hull counts on 30 random sets: 0 mismatches (test_brute.log)
- verify_all.py on all 15 files: exact parsing, size, distinctness, exact symmetry and orbit check with numeric rotation-angle confirmation, general position, orientation by 2 exact methods plus 90-digit numerics, DP in 4 linear orders with witnesses verified by 2 criteria, exhaustive C enumeration of all K- and (K-1)-subsets, 40-60 random-subset checks of DP against brute force per file, convex layers: all PASS (verify_all.log, summary.json, per-file JSON)
- check_provenance.py: build.py reproduces sym7_32points.txt and sym9_128points.txt exactly; c5_31minus_centre equals c5_31 without 0 (check_provenance.log)
- embedding_test.py: 5-fold files under all four embeddings of zeta: claims hold for j=1 and 4, and fail (convex 10-gons or a 7-gon) for j=2 and 3 (embedding_test.log)
- verify_sym9.py (bonus): sym9_128, central symmetry, general position, DP max 8 in 2 orders, 40 subsets brute-force consistent (verify_sym9.log)
- centre collinearity check for centre-free sets (centre_collinearity.log)
- Project's own verifyg.py / verify5.py + brute.c run on copies of all 15 files in my output directory: all PASS with the same numbers (project_checkers_on_copies/project_checkers.log)
- Orientation tables compared entry by entry with the project's .orient output: identical for all 15 files (orient_table_comparison.log)
- git status of the read-only worktree after the audit: clean, HEAD 9cf4949a5


# Cross-reference review of oc, pc, ec (document round 1, lens xref-ocpcec)

Scope: every \ref in sections/oc.tex, sections/pc.tex, sections/ec.tex whose label belongs to another section (116 occurrences; no \eqref, \cref, \hyperref or split \ref; none inside comments), plus prose claims about other sections. For each: target read in its own section file; hypotheses at the point of use; no stronger use; notation. Rendered numbers are from build/doc-r1/proofs.aux (all labels resolve; proofs.log has no undefined or multiply defined reference). All targets are contract export labels; the kind word (Definition/Lemma/Theorem) matches the target environment in every case. Lean line numbers cited at the points of use were checked against the files under RES.

Format: citing location -> target (rendered number): verdict.


## sections/oc.tex

- oc.tex:107 -> fd:def:point (1.1): OK (Dependencies paragraph; target exists, kind matches; every use checked below)
- oc.tex:108 -> fd:def:orient (1.3): OK (Dependencies paragraph; target exists, kind matches; every use checked below)
- oc.tex:108 -> fd:def:gp (1.5): OK (Dependencies; general position is a hypothesis of oc:lem:same-ray, oc:lem:phase-nat/int, oc:thm:phase-orbit, oc:thm:layers-ray/phase; not \ref-ed elsewhere)
- oc.tex:108 -> fd:def:ngon (1.7): OK (Dependencies paragraph; target exists, kind matches; every use checked below)
- oc.tex:108 -> fd:def:inv (1.10): OK (Dependencies paragraph; target exists, kind matches; every use checked below)
- oc.tex:108 -> fd:def:rot (1.12): OK (Dependencies paragraph; target exists, kind matches; every use checked below)
- oc.tex:109 -> fd:lem:orient (1.15): OK (Dependencies; parts (a),(b) used at 329, part (e) at 418; "symmetries" literally covers (a),(b) only, (e) is a degenerate-case fact of the same lemma -- wording only)
- oc.tex:110 -> fd:lem:collinear (1.20): OK (Dependencies paragraph; target exists, kind matches; every use checked below)
- oc.tex:110 -> fd:lem:mono (1.23): OK (Dependencies; part (c) used at 658)
- oc.tex:112 -> fd:lem:affine-orient (1.17): OK (claim "parenthetical comparison in the proof of oc:lem:rot-inv" is true: only use is line 237)
- oc.tex:113 -> fd:lem:cp-hull (1.22): OK (claim "used in the example of oc:rem:layers" true: only use is line 722)
- oc.tex:113 -> fd:lem:separation (1.40): OK (claim "used in the example of oc:rem:layers" true: only use is line 725)
- oc.tex:114 -> ll:def:hv (2.4): OK (Dependencies paragraph; target exists, kind matches; every use checked below)
- oc.tex:114 -> ll:def:peel (2.18): OK (Dependencies paragraph; target exists, kind matches; every use checked below)
- oc.tex:114 -> ll:lem:antitone (2.20): OK (Dependencies paragraph; target exists, kind matches; every use checked below)
- oc.tex:115 -> ll:lem:inv-peel (2.21): OK (Dependencies paragraph; target exists, kind matches; every use checked below)
- oc.tex:115 -> ll:thm:core-rot (2.17): OK (Dependencies paragraph; target exists, kind matches; every use checked below)
- oc.tex:115 -> ll:lem:minperiod (2.16): OK (claim "cited only in a comparison with the Lean proof (proof of oc:lem:closed)" true: only use is line 664)
- oc.tex:117 -> lg:def:polar (3.34): OK (Dependencies paragraph; target exists, kind matches; every use checked below)
- oc.tex:119 -> lg:lem:centre (3.18): OK (claim "only in comments on hypotheses (oc:lem:same-ray, oc:rem:layers)" true: uses at 515 and 705, neither in a proof)
- oc.tex:123 -> fd:def:point (1.1): OK: p=(p_0,p_1), coordinatewise operations, Finset Point -- identical to fd
- oc.tex:126 -> fd:def:orient (1.3): OK: same formula (third argument named d because c is the centre); det form also stated in fd
- oc.tex:137 -> fd:def:inv (1.10): OK: maps-into ("Invariant f S"), same as fd; no equality claimed
- oc.tex:138 -> fd:def:rot (1.12): OK for the formula (identical to fd); NOTATION: oc writes the map R_{c,theta} and its matrix M_theta, fd writes rho_{c,theta} for the map and R_theta for the matrix (fd:lem:rot, fd:lem:affine-orient); not explained -> finding F1 (minor)
- oc.tex:145 -> lg:def:polar (3.34): OK: same formula, no sign condition on r (as in lg); the two Lean constants (OrbitConsistency/LayerLemma) are explained in oc:rem:copies
- oc.tex:237 -> fd:lem:affine-orient (1.17): OK: fd part (i) is exactly "rotations preserve orient (det R_theta = 1)" and fd heads it with the same Lean theorem orient_rotAbout_inv; no circularity (fd proves (i) from fd:lem:rot(b), oc proves the lemma directly). Notation: fd's matrix R_theta = oc's M_theta, see F1
- oc.tex:329 -> fd:lem:orient(a) (1.15): OK: fd (a) orient(a,c,b)=-orient(a,b,c) and (b) orient(b,c,a)=orient(a,b,c), used exactly in this form (c is a generic point here)
- oc.tex:418 -> fd:lem:orient(e) (1.15): OK: part (e) exists (written step): orient=0 when two arguments are equal; equal labels give equal points, so orient_3(P o T)!=0 forces distinct labels
- oc.tex:491 -> fd:lem:collinear (1.20): OK: part (b) (general position => orient!=0 for pairwise distinct points); the remark's condition "distinct points of a set in general position" is exactly its hypothesis
- oc.tex:515 -> lg:lem:centre (3.18): OK: lg hypotheses (0<m, m even, rho maps S into S, S in general position, p in S, p!=c) are hypotheses of oc:lem:same-ray except p, which x!=y supplies; not used in the proof, as stated
- oc.tex:529 -> fd:lem:collinear (1.20): OK: part (b); Lean name generalPosition_iff_orient_ne_zero and ErdosSzekeres/OrientationGeometry.lean:66 agree with fd's head; pairwise distinctness of x,y,q shown in (i)-(iii)
- oc.tex:623 -> ll:def:hv (2.4): OK: hv(X)={x in X : x notin conv(X\{x})}, identical to ll
- oc.tex:624 -> ll:def:peel (2.18): OK: identical recursion; "n-th layer = hv(peel(S,n))" as in ll
- oc.tex:628 -> ll:lem:antitone (2.20): OK: (L1) restates ll (n<=n' => peel(S,n') subset peel(S,n)), no hypotheses
- oc.tex:629 -> ll:lem:inv-peel (2.21): OK: (L2) has exactly ll's hypotheses (0<m, c notin S, rho maps S into S); at the use (proof of oc:lem:closed) all three are hypotheses of oc:lem:closed
- oc.tex:631 -> ll:thm:core-rot (2.17): OK: (L3) = ll statement (0<m, K<=2m, finite X, c notin X, rho maps X into X, X K-free, x in hv(X) => hv(X)={rho^[a](x):0<=a<m} = ll's orb_m(rho,x)); Lean name and LAYERLEAN/LayerLemma.lean:364 match ll and the file; at the use, X=peel(S,i) has c notin X and K-freeness by (L1)+fd:lem:mono(c), invariance by (L2)
- oc.tex:636 -> fd:def:ngon (1.7): OK: "no K points in convex position" = not HasConvexNGon K S = "K-free" of fd
- oc.tex:658 -> fd:lem:mono(c) (1.23): OK: contrapositive of (c) for X subset S
- oc.tex:664 -> ll:lem:minperiod (2.16): OK: comparison only; its hypotheses 0<m and x!=c (from c notin X) hold; the Lean proof does use minimalPeriod_rotAbout (LEANEXT/merged/Merged.lean:1342)
- oc.tex:705 -> lg:lem:centre (3.18): OK: hypotheses listed in parentheses match lg exactly; 0<m from 2<=m; the point p!=c comes from the two given points, distinct by oc:lem:disjoint(b) and in S by (L1)
- oc.tex:722 -> fd:lem:cp-hull (1.22): OK: an inner point is a convex combination of outer points, so lies in conv(S\{p}); fd:lem:cp-hull then says S is not in convex position
- oc.tex:725 -> fd:lem:separation (1.40): OK: "easy direction" is fd's (<=, elementary); a unique maximiser of a linear functional (+-x, +-y, +-x+-y) over S resp. peel(S,1) is not in the hull of the other points

## sections/pc.tex

- pc.tex:104 -> fd:def:point (1.1): OK (Dependencies paragraph; target exists, kind matches; uses checked below)
- pc.tex:104 -> fd:def:orient (1.3): OK (Dependencies paragraph; target exists, kind matches; uses checked below)
- pc.tex:104 -> fd:def:rot (1.12): OK (Dependencies paragraph; target exists, kind matches; uses checked below)
- pc.tex:105 -> fd:def:inv (1.10): OK (Dependencies paragraph; target exists, kind matches; uses checked below)
- pc.tex:105 -> fd:def:ngon (1.7): OK (Dependencies paragraph; target exists, kind matches; uses checked below)
- pc.tex:105 -> fd:lem:orient (1.15): OK (Dependencies paragraph; target exists, kind matches; uses checked below)
- pc.tex:106 -> ll:def:hv (2.4): OK (Dependencies paragraph; target exists, kind matches; uses checked below)
- pc.tex:106 -> ll:def:peel (2.18): OK (Dependencies paragraph; target exists, kind matches; uses checked below)
- pc.tex:107 -> lg:def:polar (3.34): OK (Dependencies paragraph; target exists, kind matches; uses checked below)
- pc.tex:108 -> lg:lem:polar (3.35): OK (Dependencies; written proofs cite them as the LayerLemma originals of pc:lem:polar-facts (173-175, 927, 963); the Lean layer theorems call them -- "we use" is accurate)
- pc.tex:108 -> lg:lem:ruleA (3.36): OK (Dependencies; written proofs cite them as the LayerLemma originals of pc:lem:polar-facts (173-175, 927, 963); the Lean layer theorems call them -- "we use" is accurate)
- pc.tex:108 -> lg:lem:sinadd (3.37): OK (Dependencies; written proofs cite them as the LayerLemma originals of pc:lem:polar-facts (173-175, 927, 963); the Lean layer theorems call them -- "we use" is accurate)
- pc.tex:108 -> lg:lem:ruleB (3.38): OK (Dependencies; written proofs cite them as the LayerLemma originals of pc:lem:polar-facts (173-175, 927, 963); the Lean layer theorems call them -- "we use" is accurate)
- pc.tex:109 -> lg:thm:radius (3.20): OK (Dependencies paragraph; target exists, kind matches; uses checked below)
- pc.tex:113 -> fd:def:point (1.1): OK: same as fd (Lean Point, coordinatewise equality)
- pc.tex:115 -> fd:def:orient (1.3): OK: same formula, third point named d
- pc.tex:116 -> fd:lem:orient (1.15): OK: fd (a),(b),(c) with c renamed d; Lean names orient_swap, orient_cycle, orient_translate match fd's head
- pc.tex:142 -> lg:def:polar (3.34): OK: same formula (c_0+r cos, c_1+r sin), no sign condition; LAYERLEAN/LayerLemma.lean:932, LEANEXT/linked/Linked.lean:932, LEANEXT/capstone/Capstone2.lean:940 verified in the files
- pc.tex:173 -> lg:lem:polar (3.35): OK: identical to pc:lem:polar-facts(a) (formula, no hypotheses)
- pc.tex:173 -> lg:lem:ruleA (3.36): OK: hypotheses (three positive radii, 0<b-a<pi, 0<d-b<pi, 0<a-d+2pi<pi) identical to part (c)
- pc.tex:174 -> lg:lem:ruleB (3.38): OK: hypotheses 0<r_a, 0<r_d, r_a<=r_b, r_d<=r_b, 0<b-a, 0<d-b, d-a<pi identical to part (e); r_b>0 not assumed in either
- pc.tex:175 -> lg:lem:sinadd (3.37): OK: identical to part (d). "The Lean proofs are the same": diff of LEANEXT/phase/PhaseClassification.lean:40-102 against LAYERLEAN/LayerLemma.lean:931-996 shows only docstring lines differ
- pc.tex:849 -> fd:def:rot (1.12): OK: rho=rotAbout(c,2pi/m), m cast to R (fd:rem:angles)
- pc.tex:854 -> fd:def:inv (1.10): OK: maps-into
- pc.tex:856 -> fd:def:ngon (1.7): OK: some K-element subset in convex position
- pc.tex:862 -> ll:def:hv (2.4): OK: hv(T) subset T by definition (Lean hullVerts_subset)
- pc.tex:863 -> ll:def:peel (2.18): OK: peel(S,n+1) subset peel(S,n), induction gives peel(S,n) subset S (Lean peel_subset)
- pc.tex:864 -> lg:thm:radius (3.20): OK: restated with (L) = lg hypotheses (0<m, K<=2m, c notin S, invariance, K-free; no general position), n<=n', x in hv(peel(S,n)), y in peel(S,n') => dist2(c,y)<=dist2(c,x); Lean name and LAYERLEAN:1012 / Linked:1012 / Capstone2:1020 verified; pc:def:polar's dist2 is the same Lean constant (LAYERLEAN:999) and formula as lg's; instantiations in pc:thm:layers (a) (n_b,n_a,b,a),(n_b,n_d,b,d), (c) (n_d,n_a,d,a),(n_d,n_b,d,b), (d) (n_a,n_b,a,b),(n_a,n_d,a,d) satisfy n<=n' and the hull-vertex condition
- pc.tex:927 -> lg:lem:ruleB (3.38): OK: the Lean proof of orient_pos_of_layers ends with orient_polar_halfplane of namespace LayerLemma (LEANEXT/linked/Linked.lean:1412); the written proof uses pc:lem:polar-facts(e), the same statement
- pc.tex:963 -> lg:lem:ruleA (3.36): OK: the Lean proof of Capstone.orient_pos_of_alternating_polar calls orient_polar_centre_inside with LayerLemma opened (LEANEXT/capstone/Capstone.lean:1997)

## sections/ec.tex

- ec.tex:69 -> ll:thm:reduction (2.26): OK (Rigor and dependencies paragraph; target exists, kind matches; uses checked below)
- ec.tex:69 -> lg:lem:centre (3.18): OK (Rigor and dependencies paragraph; target exists, kind matches; uses checked below)
- ec.tex:70 -> fd:def:point (1.1): OK (Rigor and dependencies paragraph; target exists, kind matches; uses checked below)
- ec.tex:70 -> fd:def:orient (1.3): OK (Rigor and dependencies paragraph; target exists, kind matches; uses checked below)
- ec.tex:70 -> fd:def:gp (1.5): OK (Rigor and dependencies paragraph; target exists, kind matches; uses checked below)
- ec.tex:71 -> fd:def:cp (1.6): OK (Rigor and dependencies paragraph; target exists, kind matches; uses checked below)
- ec.tex:71 -> fd:def:ngon (1.7): OK (Rigor and dependencies paragraph; target exists, kind matches; uses checked below)
- ec.tex:71 -> fd:def:inv (1.10): OK (Rigor and dependencies paragraph; target exists, kind matches; uses checked below)
- ec.tex:71 -> fd:def:rot (1.12): OK (Rigor and dependencies paragraph; target exists, kind matches; uses checked below)
- ec.tex:72 -> ll:lem:minperiod (2.16): OK (listed as used in remarks: only ec:rem:orbits, line 255)
- ec.tex:72 -> ll:thm:layers (2.22): OK (remarks only: ec:rem:cases 136, ec:rem:thr 450)
- ec.tex:72 -> ll:thm:card-peel (2.24): OK (remark only: ec:rem:thr 450)
- ec.tex:72 -> lg:lem:polar (3.35): OK (remark only: ec:rem:polar 623)
- ec.tex:73 -> oc:lem:rot-inv (4.7): OK (remark only: ec:rem:cases 137-145)
- ec.tex:73 -> oc:lem:perm (4.14): OK (remark only: ec:rem:cases 137-145)
- ec.tex:73 -> oc:lem:same-ray (4.23): OK (remark only: ec:rem:cases 137-145)
- ec.tex:73 -> oc:thm:phase-orbit (4.28): OK (remark only: ec:rem:cases 137-145)
- ec.tex:74 -> sr:def:classes (7.7): OK (remark only: ec:rem:cases 148)
- ec.tex:88 -> fd:def:rot (1.12): OK: counterclockwise rotation by theta about c
- ec.tex:89 -> fd:def:inv (1.10): OK: maps-into
- ec.tex:90 -> fd:def:gp (1.5): OK
- ec.tex:91 -> fd:def:ngon (1.7): OK: some n-element subset in convex position, no emptiness condition -- as fd
- ec.tex:93 -> ll:thm:reduction (2.26): OK: angle 2pi/m with m in N cast to R; the identification with the real numerals 5 and 4 is stated (Lean exact_mod_cast, ES7Corollaries.lean:1175, 1208). The sentence names only ll:thm:reduction although (C)=lg:lem:centre has the same cast and is applied with a numeral in ec:thm:fourfold -> finding F2 (minor)
- ec.tex:136 -> ll:thm:layers (2.22): OK: every nonempty layer is one orbit of m points (the Lean-checked layer lemma; K=7<=2m for m=4,5)
- ec.tex:137 -> oc:lem:same-ray (4.23): OK: paraphrase (even m>0, finite, general position, invariant; no two distinct points on one open ray from c) is the lemma; c notin S not needed, as in oc
- ec.tex:137 -> oc:thm:phase-orbit (4.28): OK: paraphrase reads "directions of x,y" as angles of polar forms with radii |x-c|,|y-c|>0 (x,y!=c), "orbit" as {rho^j x : j in N} (oc's hypothesis), conclusion beta!=alpha+k*2pi/m for all k in Z; no more than the theorem gives (it quantifies over all polar representations)
- ec.tex:144 -> oc:lem:rot-inv (4.7): OK: rotation invariance of orient
- ec.tex:145 -> oc:lem:perm (4.14): OK: sign rule under permutations of an ordered triple
- ec.tex:148 -> sr:def:classes (7.7): OK: SYMLEAN/SymmetricReduction.lean:477 (Fivefold35) and :496 (Fourfold32) have the same text as LEANEXT/es7corr/ES7Corollaries.lean:1157/1164 (checked); different constants (namespace SymReduction, own Invariant :271 and rotAbout :400), as stated
- ec.tex:157 -> ll:thm:reduction (2.26): OK: (R) is ll's statement verbatim (0<m, K<=2m, premise (H) with c' -- ll renames the bound centre c' too --, conclusion for S in general position, invariant, m(t-1)<|S\{c}| with natural subtraction); Lean name and LAYERLEAN/LayerLemma.lean:1066 agree. Uses: ec:thm:fivefold-erase (m=5,K=7,t=7: 0<5, 7<=10, 5*7=35, 5*6=30) and ec:thm:fourfold-erase (m=4,K=7,t=8: 0<4, 7<=8, 32, 28): all hypotheses satisfied, premise supplied by Fivefold35/Fourfold32 with the hypotheses permuted
- ec.tex:163 -> lg:lem:centre (3.18): OK: (C) is lg's statement (0<m, m even, S finite, invariant, general position, p in S, p!=c => c notin S); LAYERLEAN:582. Use in ec:thm:fourfold: m=4 (0<4, even), invariance and general position given, p from |S|>=29>1 -- satisfied; the numeral/cast identification for 2pi/4 is only stated for ll:thm:reduction, see F2
- ec.tex:241 -> fd:def:rot (1.12): OK: the complex form z->c+e^{i theta}(z-c) gives rho^j=rotAbout(c,2pi jk/s) and e^{2pi i jk/s}=e^{2pi i/s} for jk=1 mod s (the iterate step is elementary; fd states it as fd:lem:rot(c), not an export label)
- ec.tex:255 -> ll:lem:minperiod (2.16): OK: hypotheses 0<m (m in {4,5}) and y!=c hold; minimal period m gives orbits of exactly m points
- ec.tex:260 -> ll:thm:reduction (2.26): OK: the Lean proofs call convexNGon_of_layers (ES7Corollaries.lean:1174, 1207); ll's proof takes T=S'\peel(S',t), the t outermost layers, as stated
- ec.tex:283 -> fd:def:cp (1.6): OK: convex position = convex independence of the inclusion family, as fd
- ec.tex:407 -> fd:def:rot (1.12): OK: complex form gives phi(rotAbout(c,theta)p)=e^{i theta}phi(p)
- ec.tex:417 -> fd:def:cp (1.6): OK: the unpacked form "for every U subset T and x in T, x in conv U => x in U" is fd's
- ec.tex:450 -> ll:thm:layers (2.22): OK: applied to S\{c}: c notin S\{c}, invariant (stated), 8-free as a subset of S, 0<m, K=8<=2m for m>=4
- ec.tex:450 -> ll:thm:card-peel (2.24): OK: same hypotheses; with t the number of nonempty layers (equivalently t=ceil(|S'|/m)) the hypothesis m(t-1)<|S'| holds and n=t gives |S'|=mt
- ec.tex:452 -> lg:lem:centre (3.18): OK: needs m even >0, invariance, general position and a point !=c (S not subset {c}) -- all available
- ec.tex:618 -> fd:def:orient (1.3): OK: cross(p,q,r)=orient(p^,q^,r^) with p^_0=p_1, p^_1=p_2; the index shift is explained
- ec.tex:623 -> lg:lem:polar (3.35): OK: formula and LAYERLEAN/LayerLemma.lean:935 agree with lg; polar(c,r,alpha) as in lg:def:polar; the stated correspondence (r=1/u, times u_1u_2u_3 gives Sigma) checks
- ec.tex:904 -> ll:thm:reduction (2.26): OK (Coverage: used from the layer-lemma section)
- ec.tex:904 -> lg:lem:centre (3.18): OK (Coverage: used from the layer-geometry section)

## Prose claims about other sections (no \ref)

- oc.tex:44-46 "Lines 1--1147 of [Merged.lean] coincide line by line with lines 1--1147 of LAYERLEAN/LayerLemma.lean; hull vertices, peels and the layer lemma used in oc:sub:layers come from there": OK (diff of the two prefixes is empty).
- oc.tex:106 "From the foundations section we use ...": OK (each item checked above).
- oc.tex:113-116 "From the layer-lemma section we use ... Lemma ll:lem:minperiod is cited only in a comparison": OK.
- oc.tex:116-119 "From the layer-geometry section we use the definition of polar and, only in comments on hypotheses, Lemma lg:lem:centre": OK.
- oc.tex:150-155 (oc:rem:copies) LAYERLEAN line numbers iterate_mem 52, Invariant 105, complex helpers 231--308, rotAbout 298, rotAbout_iterate 465, polar 932: OK (checked in the file; they agree with the heads of fd:lem:inv-image(c), ll:def:inv/fd:def:inv, fd:def:rot, fd:lem:rot(c)/ll:lem:rot/lg:lem:rot-iter, lg:def:polar).
- oc.tex:624-625 "We use three facts from the layer-lemma section": OK ((L1)-(L3) are ll statements).
- oc.tex:928-929 complex helpers "belong to the layer-lemma unit": OK (ll:def:complex, ll:lem:complex).
- oc.tex:930-931 "Lines 1--1147 of Merged.lean ... treated in the layer-lemma and layer-geometry sections": OK (ll covers LAYERLEAN lines 1-464 and 1033-1148, lg covers 465-1032, per their Coverage paragraphs).
- pc.tex:42-45 "Lines 40--102 of PhaseClassification.lean repeat lines 931--996 of LAYERLEAN/LayerLemma.lean ...; only the docstrings differ": OK (diff: 5 docstring hunks only).
- pc.tex:45-47 "Lines 1--1147 of Linked.lean are lines 1--1147 of LAYERLEAN/LayerLemma.lean": OK (diff empty).
- pc.tex:105-109 "From the layer sections we use ...": OK.
- pc.tex:860-868 "We use two facts from the layer sections": OK (inclusions derived from ll:def:hv/ll:def:peel; radius order = lg:thm:radius verbatim).
- pc.tex:982-983 "copies of lines 931--996 of LAYERLEAN/LayerLemma.lean, whose originals also have written proofs in the section on layer geometry": OK (lg:def:polar, lg:lem:polar, lg:lem:ruleA, lg:lem:sinadd, lg:lem:ruleB, each with a proof).
- pc.tex:1006-1010 "lines 1--1384 of Linked.lean ... treated in the sections on the layer lemma, layer geometry and orbit literals": OK (LayerLemma copy -> ll, lg; Merged section 13 -> oc).
- ec.tex:80-85 "Lines 1--1147 of this file coincide ... Invariant, rotAbout, centre_not_mem_of_even and convexNGon_of_layers ... at the same lines (105, 298, 582, 1066)": OK (diff empty; lines match the heads of ll:def:inv/fd:def:inv, fd:def:rot, lg:lem:centre, ll:thm:reduction).
- ec.tex:155 "two Lean-checked results whose written proofs are in other sections": OK (ll:thm:reduction proved in ll, lg:lem:centre proved in lg).
- ec.tex:902-904 "a verbatim copy of lines 1--1147 of LAYERLEAN/LayerLemma.lean, which belongs to the layer-lemma sections": OK.
- ec.tex:135-136 "Apart from the layer lemma and the ray fact ... Both have Lean-checked forms": OK (ll:thm:layers; oc:lem:same-ray and oc:thm:phase-orbit, see the lines above).

## Findings

- F1 (minor, section oc). oc.tex:138-143 (Definition oc:def:basic(b)) and oc.tex:237. oc writes the rotation map as R_{c,theta} and its matrix as M_theta, citing Definition fd:def:rot, whose notation is rho_{c,theta} = rotAbout c theta for the map, while fd (Lemmas fd:lem:rot and fd:lem:affine-orient, the latter cited at oc.tex:237) uses R_theta for the matrix. A reader who follows the pointer at line 237 meets "the linear part R_theta of rho_{o,theta}" where oc's R is a map. Fix: in Definition oc:def:basic(b) add a clause such as "(Definition fd:def:rot writes rho_{c,theta} for this map; the matrix M_theta is written R_theta there)". No mathematical effect.
- F2 (minor, section ec). ec.tex:92-95 (Conventions of ec:ssec:es7) say that the real-numeral angles 2pi/5, 2pi/4 of the case statements and theorems equal the cast angle 2pi/m "in Theorem ll:thm:reduction". The other cited statement with a cast angle, (C) = Lemma lg:lem:centre (ec.tex:163), is applied in the proof of Theorem ec:thm:fourfold (ec.tex:227) to a set invariant under rotAbout(c,2pi/4) with the real numeral 4; the identification is true and the Lean proof makes it with exact_mod_cast (LEANEXT/es7corr/ES7Corollaries.lean:1228), but the text names only ll:thm:reduction. Fix: "in Theorem ll:thm:reduction and Lemma lg:lem:centre the angle is 2pi/m with m in N cast to R".

No blocker or major finding: every cross-section target is the intended statement, every hypothesis (c notin S, 0<m, K<=2m, general position, Finset, maps-into, casts, natural subtraction) is satisfied or explicitly supplied at each point of use, no citation uses a nonexistent part or more than the target states, and notation agrees apart from F1.

## Note outside this lens

- ec.tex:59-60 (Axioms) mentions decide only for PCompat.ex341; the proof of fourfold_heptagon also discharges the side goal Even 4 by decide (LEANEXT/es7corr/ES7Corollaries.lean:1227; kernel evaluation, no extra axiom). The text does not claim exclusivity, and oc.tex:92-95 records the analogous Even 6 decide; mentioned only for the rigor reviewer of ec.

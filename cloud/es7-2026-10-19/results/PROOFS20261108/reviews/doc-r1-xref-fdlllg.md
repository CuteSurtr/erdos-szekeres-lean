# doc-r1, lens xref-fdlllg: cross-references from sections fd, ll, lg

Build reviewed: `build/doc-r1/` (proofs.pdf, proofs.log, proofs.aux, proofs.txt). Sources: `sections/fd.tex`,
`sections/ll.tex`, `sections/lg.tex` (citing), and the target statements read in their own section files
(`fd.tex`, `ll.tex`, `lg.tex`, `oc.tex` lines 80-400, `mb.tex` lines 150-260, `pc.tex` heads).

Method. Every `\ref`/`\eqref` in the three citing files whose label prefix differs from the file's key was extracted
with a script that also catches references broken across lines (83 in all: fd 6, ll 34, lg 43; no `\eqref` crosses a
section). For each: (1) the target was read in its own file and compared with the description at the point of use;
(2) the hypotheses of the cited statement were checked at the point of use (c not in S, 0<m, K<=2m, general position,
Finset vs set, maps-into vs equality, m=0, natural subtraction); (3) the citing text was checked to use no more than
the target gives (part letters exist, no stronger conclusion, same quantifier order); (4) notation was compared.
Where the citing text makes a claim about a Lean proof or a Lean statement of a cited declaration, the Lean source in
the research records was read (LAYERLEAN/LayerLemma.lean lines 100-470, 525-625, 860-932, 1030-1148;
LEANEXT/orbit/OrbitConsistency.lean lines 110-200; LEANEXT/phase/PhaseClassification.lean heads). Mechanical checks:
all 83 targets are export labels allowed by the contract; all are defined exactly once; the kind word before each
reference (Definition/Lemma/Theorem) matches the target environment; the doc-r1 log has no undefined or multiply
defined reference and proofs.txt contains no "??".

## Cross-section references (83), one line each

- sections/fd.tex:12 -> mb:thm:baek (10.4; defined sections/mb.tex:185): OK. Theorem `main` (Vendor/ETV/Main/Main.lean:87), environment theorem, head 'Baek's theorem, cited'; mb:rem:baek says it is cited in its Lean form and not reproved, exactly as fd states.
- sections/fd.tex:102 -> ll:def:hv (2.4; defined sections/ll.tex:168): OK. Definition of hullVerts, same formula as fd's hv(X); Lean name given.
- sections/fd.tex:102 -> ll:def:peel (2.18; defined sections/ll.tex:481): OK. Definition of peel, same recursion as fd's peel(X,n); Lean name given.
- sections/fd.tex:398 -> ll:def:66-70 (2.27; defined sections/ll.tex:650): OK. Both propositions written with real numerals 2 * Real.pi / 6 and / 7 (checked in LAYERLEAN/LayerLemma.lean:1102,1107); consistent with ll:rem:numerals.
- sections/fd.tex:522 -> oc:lem:perm (4.14; defined sections/oc.tex:338): OK. orient3_perm (OrbitConsistency.lean:178): for every sigma and every t, orient3(t o sigma) = sgn(sigma) orient3(t); same quantifier order as Lean; fd's translation sigma = s^-1 pi s is correct; orient3 at :168 as fd says.
- sections/fd.tex:583 -> oc:lem:rot-inv (4.7; defined sections/oc.tex:224): OK. orient_rotAbout_inv (c theta a b d), no hypotheses; equals fd (i) with o renamed c, as the remark explains. Note oc writes the map as R_{c,theta} while fd's R_theta is the matrix (see finding F1, minor).
- sections/ll.tex:24 -> lg:thm:nesting (3.16; defined sections/lg.tex:443): OK. strict_nesting (LayerLemma.lean:529) lies in lines 471-1032 as claimed.
- sections/ll.tex:24 -> lg:lem:centre (3.18; defined sections/lg.tex:490): OK. centre_not_mem_of_even (:582) lies in lines 471-1032 as claimed.
- sections/ll.tex:26 -> fd:def:point (1.1; defined sections/fd.tex:250): OK. Recalled definitions; Definitions.lean hash 2425500eefd1 agrees with fd's source table.
- sections/ll.tex:26 -> fd:def:gp (1.5; defined sections/fd.tex:308): OK. Recalled definitions; Definitions.lean hash 2425500eefd1 agrees with fd's source table.
- sections/ll.tex:26 -> fd:def:cp (1.6; defined sections/fd.tex:316): OK. Recalled definitions; Definitions.lean hash 2425500eefd1 agrees with fd's source table.
- sections/ll.tex:26 -> fd:def:ngon (1.7; defined sections/fd.tex:326): OK. Recalled definitions; Definitions.lean hash 2425500eefd1 agrees with fd's source table.
- sections/ll.tex:55 -> fd:def:point (1.1; defined sections/fd.tex:250): OK as a dependency pointer (target exists and is used in ll).
- sections/ll.tex:55 -> fd:def:gp (1.5; defined sections/fd.tex:308): OK as a dependency pointer (target exists and is used in ll).
- sections/ll.tex:56 -> fd:def:cp (1.6; defined sections/fd.tex:316): OK as a dependency pointer (target exists and is used in ll).
- sections/ll.tex:56 -> fd:def:ngon (1.7; defined sections/fd.tex:326): OK as a dependency pointer (target exists and is used in ll).
- sections/ll.tex:56 -> fd:def:inv (1.10; defined sections/fd.tex:345): OK as a dependency pointer (target exists and is used in ll).
- sections/ll.tex:56 -> fd:def:rot (1.12; defined sections/fd.tex:380): OK as a dependency pointer (target exists and is used in ll).
- sections/ll.tex:56 -> fd:lem:cp-hull (1.22; defined sections/fd.tex:673): OK as a dependency pointer (target exists and is used in ll).
- sections/ll.tex:57 -> fd:lem:mono (1.23; defined sections/fd.tex:691): OK as a dependency pointer (target exists and is used in ll).
- sections/ll.tex:57 -> fd:lem:collinear (1.20; defined sections/fd.tex:603): OK as a dependency pointer (target exists and is used in ll).
- sections/ll.tex:57 -> fd:lem:affine-cp (1.27; defined sections/fd.tex:794): OK as a dependency pointer (target exists and is used in ll).
- sections/ll.tex:58 -> lg:lem:centre (3.18; defined sections/lg.tex:490): OK. Description 'exclusion of the centre for even m' matches; used in Step 2 of ll:thm:sixfold.
- sections/ll.tex:97 -> fd:lem:affine-cp (1.27; defined sections/fd.tex:794): OK. Part (a), g(conv Y) = conv(g(Y)) for affine g(x)=Ax+v, contains the inclusion conv(f(A)) in f(conv A); a Lean affine map f(v)=Lv+b is of this form (fd:def:conv).
- sections/ll.tex:99 -> fd:def:cp (1.6; defined sections/fd.tex:316): OK. Recalled as the meaning of convex position / general position / HasConvexNGon.
- sections/ll.tex:99 -> fd:def:gp (1.5; defined sections/fd.tex:308): OK. Recalled as the meaning of convex position / general position / HasConvexNGon.
- sections/ll.tex:99 -> fd:def:ngon (1.7; defined sections/fd.tex:326): OK. Recalled as the meaning of convex position / general position / HasConvexNGon.
- sections/ll.tex:101 -> fd:lem:cp-hull (1.22; defined sections/fd.tex:673): OK. Quoted verbatim (S in convex position iff p not in conv(S minus p) for every p in S).
- sections/ll.tex:102 -> fd:lem:mono (1.23; defined sections/fd.tex:691): OK. Monotonicity; the consequence drawn (empty set in convex position, HasConvexNGon 0 S) follows from fd:lem:cp-hull vacuously.
- sections/ll.tex:162 -> fd:def:inv (1.10; defined sections/fd.tex:345): OK. Same maps-into definition; 'injective implies f(S)=S' agrees with fd:def:inv / fd:lem:inv-image(a).
- sections/ll.tex:205 -> fd:lem:cp-hull (1.22; defined sections/fd.tex:673): OK. Applied to the finite set hv(S).
- sections/ll.tex:296 -> fd:lem:mono (1.23; defined sections/fd.tex:691): OK. Part (a): T subset of H, H in convex position by ll:lem:hv(a).
- sections/ll.tex:394 -> fd:def:rot (1.12; defined sections/fd.tex:380): OK. Same coordinate formula; counterclockwise as in fd:lem:rot(e).
- sections/ll.tex:540 -> fd:lem:mono (1.23; defined sections/fd.tex:691): OK. Part (c), contrapositive, U = peel(S,n) subset of S.
- sections/ll.tex:630 -> fd:lem:mono (1.23; defined sections/fd.tex:691): OK. Part (c), S' = S minus c subset of S.
- sections/ll.tex:643 -> fd:lem:mono (1.23; defined sections/fd.tex:691): OK. Part (b), T subset of S.
- sections/ll.tex:644 -> fd:lem:mono (1.23; defined sections/fd.tex:691): OK. Part (c), T subset of S.
- sections/ll.tex:675 -> lg:lem:centre (3.18; defined sections/lg.tex:490): OK. Hypotheses checked: m=6 > 0 and even; S maps into itself under rotAbout c (2*pi/6) (real numeral = cast of natural 6, ll:rem:numerals; Lean uses exact_mod_cast); general position; p in S, p != c from Step 1. Conclusion c not in S is exactly what is used. No circularity: lg:lem:centre's proof uses no ll result.
- sections/ll.tex:682 -> fd:lem:collinear (1.20; defined sections/fd.tex:603): OK. Part (a) (orient = 0 implies collinear) is the part used; the part letter is not named (harmless).
- sections/ll.tex:683 -> fd:def:gp (1.5; defined sections/fd.tex:308): OK. p, c, q are pairwise distinct points of S (c in S by the indirect assumption).
- sections/lg.tex:51 -> fd:lem:mono (1.23; defined sections/fd.tex:691): OK. Part (c) is HasConvexNGon.mono, ErdosSzekeres/Basic.lean:20, as in fd's head; the Lean proofs of lg indeed unfold HasConvexNGon instead (checked in strict_nesting, lin_pos_of_peel, chain_clauses_sound).
- sections/lg.tex:105 -> fd:def:point (1.1; defined sections/fd.tex:250): OK as a dependency pointer (target exists and is used in lg).
- sections/lg.tex:105 -> fd:def:orient (1.3; defined sections/fd.tex:274): OK as a dependency pointer (target exists and is used in lg).
- sections/lg.tex:105 -> fd:def:gp (1.5; defined sections/fd.tex:308): OK as a dependency pointer (target exists and is used in lg).
- sections/lg.tex:105 -> fd:def:cp (1.6; defined sections/fd.tex:316): OK as a dependency pointer (target exists and is used in lg).
- sections/lg.tex:105 -> fd:def:ngon (1.7; defined sections/fd.tex:326): OK as a dependency pointer (target exists and is used in lg).
- sections/lg.tex:106 -> fd:def:inv (1.10; defined sections/fd.tex:345): OK as a dependency pointer (target exists and is used in lg).
- sections/lg.tex:106 -> fd:def:rot (1.12; defined sections/fd.tex:380): OK as a dependency pointer (target exists and is used in lg).
- sections/lg.tex:106 -> fd:lem:orient (1.15; defined sections/fd.tex:478): OK as a dependency pointer (target exists and is used in lg).
- sections/lg.tex:106 -> fd:lem:collinear (1.20; defined sections/fd.tex:603): OK as a dependency pointer (target exists and is used in lg).
- sections/lg.tex:106 -> fd:lem:mono (1.23; defined sections/fd.tex:691): OK as a dependency pointer (target exists and is used in lg).
- sections/lg.tex:107 -> fd:lem:pos-triples (1.35; defined sections/fd.tex:1032): OK as a dependency pointer; but fd:lem:pos-triples is NOT recalled in Subsection 3.1 as the paragraph claims (finding F3).
- sections/lg.tex:107 -> ll:def:hv (2.4; defined sections/ll.tex:168): OK as a dependency pointer (target exists; recalled in Subsection 3.1).
- sections/lg.tex:107 -> ll:def:peel (2.18; defined sections/ll.tex:481): OK as a dependency pointer (target exists; recalled in Subsection 3.1).
- sections/lg.tex:108 -> ll:lem:hv (2.6; defined sections/ll.tex:188): OK as a dependency pointer (target exists; recalled as (L1)-(L4)).
- sections/lg.tex:108 -> ll:lem:antitone (2.20; defined sections/ll.tex:500): OK as a dependency pointer (target exists; recalled as (L1)-(L4)).
- sections/lg.tex:108 -> ll:lem:inv-peel (2.21; defined sections/ll.tex:510): OK as a dependency pointer (target exists; recalled as (L1)-(L4)).
- sections/lg.tex:108 -> ll:thm:core-rot (2.17; defined sections/ll.tex:465): OK as a dependency pointer (target exists; recalled as (L1)-(L4)).
- sections/lg.tex:113 -> fd:def:point (1.1; defined sections/fd.tex:250): OK.
- sections/lg.tex:128 -> fd:def:orient (1.3; defined sections/fd.tex:274): OK. (O1) is the defining formula.
- sections/lg.tex:131 -> fd:lem:orient (1.15; defined sections/fd.tex:478): OK. Part (b) gives orient(a,b,c)=orient(b,c,a)=orient(c,a,b), hence orient(a,b,o)=orient(o,a,b)=det(a-o,b-o).
- sections/lg.tex:141 -> fd:def:rot (1.12; defined sections/fd.tex:380): OK. Coordinate formula identical; the matrix form uses lg's R_theta, which is fd's R_theta (fd:lem:rot).
- sections/lg.tex:168 -> fd:def:inv (1.10; defined sections/fd.tex:345): OK. Maps-into, Lean Invariant (rotAbout c (2 * Real.pi / m)) S.
- sections/lg.tex:170 -> fd:def:cp (1.6; defined sections/fd.tex:316): OK.
- sections/lg.tex:170 -> fd:def:ngon (1.7; defined sections/fd.tex:326): OK.
- sections/lg.tex:170 -> fd:lem:mono (1.23; defined sections/fd.tex:691): OK. Part (c), contrapositive: subsets of K-free sets are K-free.
- sections/lg.tex:171 -> fd:def:gp (1.5; defined sections/fd.tex:308): OK.
- sections/lg.tex:171 -> fd:lem:collinear (1.20; defined sections/fd.tex:603): OK. Part (b) as quoted.
- sections/lg.tex:178 -> ll:def:hv (2.4; defined sections/ll.tex:168): OK. Same formula; hv(X) subset of X.
- sections/lg.tex:179 -> ll:def:peel (2.18; defined sections/ll.tex:481): OK. Same recursion.
- sections/lg.tex:183 -> ll:lem:hv (2.6; defined sections/ll.tex:188): OK. (L1) is part (c), subset_convexHull_hullVerts, for every finite X.
- sections/lg.tex:184 -> ll:lem:antitone (2.20; defined sections/ll.tex:500): OK. (L2): n <= n' gives peel(S,n') subset of peel(S,n); with n=0, subset of S.
- sections/lg.tex:187 -> ll:lem:inv-peel (2.21; defined sections/ll.tex:510): OK. (L3) hypotheses 0<m, c not in S, maps-into: identical to ll:lem:inv-peel and Lean invariant_peel.
- sections/lg.tex:189 -> ll:thm:core-rot (2.17; defined sections/ll.tex:465): OK. (L4) hypotheses 0<m, K<=2m, c not in S, maps-into, K-free, x in hv(S); conclusion hv(S) = {rho^j(x): 0<=j<m} = orb_m(rho,x).
- sections/lg.tex:470 -> fd:lem:collinear (1.20; defined sections/fd.tex:603): OK. x, rho(x), y are pairwise distinct points of S.
- sections/lg.tex:476 -> ll:lem:minperiod (2.16; defined sections/ll.tex:443): OK. Remark on the Lean proof: x != c and m >= 2 > 0 give period m; Lean strict_nesting does use minimalPeriod_rotAbout and minimalPeriod_eq_one_iff_isFixedPt (checked).
- sections/lg.tex:506 -> fd:lem:collinear (1.20; defined sections/fd.tex:603): OK. p, c, q pairwise distinct points of S (c in S by the indirect assumption).
- sections/lg.tex:695 -> fd:lem:pos-triples (1.35; defined sections/fd.tex:1032): OK. iota = Fin (n+1) with its order; injective on all of iota by Step 2; s = all of iota with n+1 >= 4 elements; positivity of all increasing triples by Step 1; conclusion p(s) = T in convex position.
- sections/lg.tex:756 -> ll:lem:minperiod (2.16; defined sections/ll.tex:443): OK. Remark on the Lean proof: p != c, 0 < m; Lean lin_pos_of_peel uses minimalPeriod_rotAbout hm0 hpc (checked).
- sections/lg.tex:780 -> fd:lem:mono (1.23; defined sections/fd.tex:691): OK. Part (c): peel(S,i) subset of S.
- sections/lg.tex:781 -> fd:lem:mono (1.23; defined sections/fd.tex:691): OK. Same, in the parenthetical comparison with Lean (Lean unfolds HasConvexNGon: checked).
- sections/lg.tex:928 -> ll:lem:antitone (2.20; defined sections/ll.tex:500): OK. peel_antitone at LayerLemma.lean:460 (checked).
- sections/lg.tex:928 -> ll:thm:card-peel (2.24; defined sections/ll.tex:566): OK. card_peel at :1037, docstring at :1036 (checked).

## Prose claims about other sections, and implicit references

- fd.tex:10-13, "published theorems ... (for example Baek's theorem, Theorem 10.4) are cited in the exact form in which they are used and are not reproved": OK (mb:thm:baek and mb:rem:baek say exactly this; mb:thm:capcup is cited the same way).
- fd.tex:28-31 and 60-62, "each section names the build and axioms logs it relies on": OK (spot-checked all 12 sections, including the new sa, which names SizeArith.lean.log, AssembledSizes.lean.log, BaekSeven.out).
- fd.tex:54-57, the section that cites a native_decide declaration names Lean.ofReduceBool and Lean.trustCompiler: OK, vacuous (ll, pc, cb, ec, sa and the others state that no native_decide is used).
- fd.tex:89-92 and 96-105, conventions "We write rho_{c,theta}", "we write f^[n]", natural subtraction written as max(a-b,0) or with b<=a, under the heading "Notation shared by all sections": PROBLEM (finding F1, minor). lg, pc, ec write rotAbout(c,theta); oc writes R_{c,theta} for the map (and M_theta for the matrix, while fd's R_theta is the matrix); sr writes rotAbout_{c,theta}; ll and lg write iterates f^i, f^j; ll writes t -. 1 (dot-minus). Each of these sections defines its own notation, so nothing is wrong mathematically.
- fd.tex:102, hv and peel "defined formally, with their Lean names, in Definitions 2.4 and 2.18": OK.
- fd.tex:110, "basic facts that all later sections use": loose but harmless; OK.
- fd.tex:115, "This section relies on no other section": OK (the six references to mb, ll, oc are pointers for notation and Lean counterparts; no proof of fd uses them; oc:lem:rot-inv cites fd:lem:affine-orient only in a parenthetical comparison, so there is no circular proof).
- fd.tex:395-400, "In later sections the angle is usually written 2 * Real.pi / m": OK.
- fd.tex:1240-1242, other declarations "treated in other sections or lie outside Stage 1": OK (hedged).
- ll.tex:21-24, ll treats lines 1-469 and 1034-1148, lines 471-1032 belong to other sections: OK (lg covers 465-1032; the overlap rotAbout_iterate at line 465 is acknowledged in both coverage paragraphs; fd:lem:rot(c) and oc:lem:iterate restate it too).
- ll.tex:55-59, Dependencies "... Nothing else from other sections is used": PROBLEM (finding F2, minor). Step 2 of the proof of Theorem 2.28 (ll.tex:681) computes orient(p,c,2c-p) from the coordinate formula of Definition fd:def:orient, which ll never cites and which the list omits.
- ll.tex:719-726, Remark 2.30 "These unsatisfiability results have the rigor label certificate": PROBLEM (finding F4, minor). fd says the document uses exactly three rigor labels; "certificate" is the project's label (k8 soundness note), which the sentence does not say; sr labels the analogous SAT-backed records "computer-assisted".
- lg.tex:35-40, the declarations recalled in Subsection 3.1 lie outside lines 465-1032 and are restated in the layer-lemma section; the foundations section restates the listed main-library declarations and proves the lemmas among them: OK (orbitFS, Invariant, hullVerts, rotAbout, peel, subset_convexHull_hullVerts, invariant_peel, hullVerts_eq_orbitFS_rotAbout, peel_antitone are all in ll; Point, GeneralPosition, ConvexPosition, HasConvexNGon, orient, orient_cycle, generalPosition_iff_orient_ne_zero, Suk.convexPosition_of_positive_triples are all in fd; hashes agree with fd's source table).
- lg.tex:104-109, "These are recalled in Subsection 3.1": PROBLEM (finding F3, minor) for Lemma fd:lem:pos-triples, which Subsection 3.1 does not recall (it is cited only in Step 3 of the proof of Theorem 3.28); all other listed results are recalled there.
- lg.tex:62-72, axiom-log counts (16 of the 23 lg theorems in LAYERLEAN/logs/axioms.log; 11 in the re-check): OK and consistent with ll.tex:31-33 (28 and 19 theorems): checked against the logs, 16 lg + 12 ll = 28 and 11 lg + 8 ll = 19.
- lg.tex:181, (L1)-(L4) "results of the section on the layer lemma": OK (see the reference lines above).
- lg.tex:894, rotAbout_iterate "the section on the layer lemma restates it as well": OK (ll:lem:rot(d)).
- lg.tex:927-928, peel_antitone (line 460) and card_peel (line 1037, docstring 1036) belong to the layer-lemma section: OK.
- lg.tex:943-944, the PhaseClassification declarations polar, orient_polar, orient_polar_centre_inside, sin_add_lt, orient_polar_halfplane "are treated in the section on phase patterns": OK (pc:def:polar and pc:lem:polar-facts, with the same file lines 41, 44, 51, 64, 80).
- Implicit references by section name (lg: "the foundations section", "the section on the layer lemma", "the section on phase patterns"; ll: "the foundations section"): OK; the section labels are not export labels, so naming the section is the right form.

## Findings

F1 (minor, fd). fd.tex:96 heads a paragraph "Notation shared by all sections" and fixes rho_{c,theta} for rotAbout c theta;
fd.tex:89-92 likewise fixes f^[n] for iterates and max(a-b,0) or an explicit b<=a for natural subtraction. Other
sections do not follow these conventions: lg (38 uses), pc and ec write rotAbout(c,theta); oc writes R_{c,theta} for the
rotation map and M_theta for its matrix, whereas fd (and lg) use R_theta for the matrix, so a reader who follows the
pointer of Remark 1.18 to Lemma 4.7 meets R with a different meaning; sr writes rotAbout_{c,theta}; ll and lg write
iterates f^i, f^j; ll writes the truncated difference t -. 1 (its (C7)). Every section defines its own notation, so no
statement is affected. Fix: retitle the paragraph (for example "Common notation") and add one sentence saying that
later sections may fix their own symbols for rotations, iterates and truncated subtraction at their start, naming the
variants (rotAbout(c,theta), R_{c,theta} with matrix M_theta, rotAbout_{c,theta}, f^i, t -. 1) and noting that R_theta in
this section is a matrix.

F2 (minor, ll). ll.tex:681 (Step 2 of the proof of Theorem 2.28) evaluates orient(p,c,2c-p) by the coordinate formula of
Definition fd:def:orient, but ll never references fd:def:orient, and its Dependencies paragraph (ll.tex:55-59) lists
the foundations definitions used without it and ends "Nothing else from other sections is used". Fix: add
Definition~\ref{fd:def:orient} to the Dependencies list and cite it at ll.tex:681 ("by Definition~\ref{fd:def:orient}").

F3 (minor, lg). lg.tex:104-109 lists the dependencies, including Lemma fd:lem:pos-triples, and says "These are recalled
in \S3.1"; Subsection 3.1 (lg.tex:111-216) recalls all of them except fd:lem:pos-triples, which is used only in Step 3
of the proof of Theorem 3.28 (lg.tex:695). Fix: say "These, except Lemma~\ref{fd:lem:pos-triples}, which is used only in
the proof of Theorem~\ref{lg:thm:fan}, are recalled in ...", or add a one-line recall of it to Subsection 3.1.

F4 (minor, ll). ll.tex:725-726 (Remark 2.30): "These unsatisfiability results have the rigor label \emph{certificate}."
fd.tex:48-82 says the document uses exactly three rigor labels (Lean-checked, written proof (not refereed),
computer-assisted), and sr labels the analogous SAT-backed records "computer-assisted" (Remark sr:rem:records). The
paragraph does begin "In the project, ...", and contract rule 7 asks for the project's label, but the sentence reads as
a fourth label of this document. Fix: "These unsatisfiability results carry the project's rigor label
\emph{certificate} (cake\_lpr verdicts; not one of the labels of this document, in whose terms they would be
computer-assisted)", or align with sr.

No blocker or major finding: every cross-section reference points at the intended statement, every cited hypothesis
is satisfied at the point of use, and no citing text uses a nonexistent part, a stronger conclusion or a different
quantifier order.

## Outside this lens (noted, not reported as findings)

- ll.tex:28-30 cites LAYERLEAN/logs/build.log as recording exit code 0 without noting that the log names no file hash;
  fd.tex:204-206 declines to use that log for this reason, and lg.tex:55-60 states the caveat. ll's Lean-checked label
  also rests on the hash-identified re-check, so nothing depends on it; a rigor or consistency pass may want the same
  caveat in ll.

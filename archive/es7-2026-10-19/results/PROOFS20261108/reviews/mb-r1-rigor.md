# Review of section `mb` (round 1, lens: rigor)

Section: `sections/mb.tex` (1113 lines), map `sections/mb.map.tsv` (42 rows).
Verdict: **pass**. I found no blocker and no major problem. There are 9 minor findings, listed below.

## What I checked

1. **Every Lean statement against its source.** I read each Lean declaration named in a statement head and compared it
   with the section's statement. That includes hypotheses, their order, Finset vs set, and implicit vs explicit
   arguments. Sources:
   - `ErdosSzekeres/Vendor/ETV/Config/Defs.lean`, `Config/Lemmas.lean`, `Main/Main.lean`, `Main/CapCup.lean`,
     `Lib/List/Defs.lean`;
   - `ErdosSzekeres/Omission/{Realization,ActualRanks,PlanarChains,ListGeometry,BoundaryGeometry,BaekGeometry,Baek}.lean`;
   - `MIRRORETV/lean/MirrorMain.lean` (lines 1–30, 212–236, 380–416, 630–660, 806–840, 985–995, 1500–2000, 2225–2240,
     2300–2320, 2398–2420, 2490–2677);
   - `MIRRORETV/lean/MirrorNine_append.lean` (all);
   - `SYMLEAN/mirror/ReductionThreeClasses.lean` (header, 285–300, 440–530, 1015–1090, 1495–1560, 4230–4322).

   All statements match. These include:
   - `main`: `choose (n+2) 2 + 2 ≤ |S|` gives `HasNCap 4 S ∨ HasNGon (n+3) S`;
   - `Config.cap_cup`: `choose (a+b) a < |S|`;
   - `geometric_capacity22`, with its side condition `S ⊆ range n`;
   - `config_capacity113`, `capacity113`, `mirror_nine(_line)`;
   - `mirror_seven_of`, with the exact premises Hcap/HL/HR;
   - `transport`;
   - `reflLine_eq_lineRefl`, with `n0=-u1`, `n1=u0`, `c=-u1 a0+u0 a1`;
   - `card_le_32_of_reflLine`;
   - the two `_proved` theorems, against the definitions `MirrorOneAxis33` and `MirrorNoAxis34` at RTC:508 and 514;
   - the two `_3` theorems, whose explicit arguments are (h2 h3 h5 S g hgp hcard hg hne hinv) and
     (h2 h3 h5 S g hgp hcard hne hinv).
2. **Every proof, step by step.** For each proof I checked inequality directions, that case splits are exhaustive, that
   inductions are well founded, and that each use of an earlier result meets its hypotheses exactly. Details are in
   "Proof-by-proof notes" below.
3. **Every algebraic identity, with sympy 1.13.3.** The script was run with `nice -n 15`. Its essential content is
   reproduced at the end of this report. Every difference reduced to 0:
   - (mb:eq:four-left) and (mb:eq:four-right);
   - (mb:eq:chord);
   - the expansion in Lemma mb:lem:interior;
   - `orient(ρa,ρb,ρd) = -orient(a,b,d)`, and `orient(ρa,ρb,ρw) = orient(b,a,w)`, which is used in Step 4 of
     Lemma mb:lem:boundary;
   - the collinearity computations in Lemma mb:lem:split(b) and (c);
   - the four ν-identities of Lemma mb:lem:frame, plus "second coordinate of frame(p) = n0p0+n1p1-cν";
   - both coordinates of Theorem mb:thm:refl32(a), in the Lean certificate form `2(p_i-a_i)(u0²+u1²-1)` and in the
     written form;
   - the identity `-u1 p0+u0 p1-c = -u1 w0+u0 w1`;
   - the claim that both reflections send p to `a+<w,u>u-<w,n>n` when `u0²+u1²=1`.

   Numerical values checked:
   - C(6,2)=15, C(7,2)=21, C(8,2)=28, C(9,3)=84;
   - C(N-1,2)+1 = 16, 22, 29 for N = 7, 8, 9;
   - 2·15+2=32, 2·22+2=46, 29+84=113, 2·113=226;
   - C(7,3)=35 and C(8,3)=56, as stated in Remark mb:rem:generated.
4. **Logs and hashes.**
   - The SHA-256 prefixes of all 22 files listed in "Sources" and "Lean version and axioms" match.
   - `MirrorMain.out`: lines 848–863 are the 16 axiom lines, in the stated order. The words "error" and "sorry" do not
     occur in it.
   - `MirrorNine.out`: lines 879–882 are the axiom lines. The +2677 shift checks out: the warning at
     `MirrorNine.lean:2746` is line 69 of the appended file, which contains `<;>`.
   - `axioms.out` content is as described, including the truncated `#check` lines.
5. **Copy claims.** I checked these with `sed`+`cmp`. All are byte-identical:
   - RTC 1562–4236 and MirrorMain 3–2677;
   - RTC 38–1559 and AffineReduction 12–1533;
   - RTC 38–1084 and SymmetricReduction 12–1058.

   The derived line correspondences also hold: SymmetricReduction:423/997 and AffineReduction:1501 are `reflLine`,
   `heptagon_of_nontrivial_isometry` and `heptagon_of_nontrivial_affineEquiv`.
6. **Unsafe constructs.** I grepped all files named in the section and the whole `ErdosSzekeres/Vendor/ETV` tree for
   `native_decide`, `sorry`, `admit`, `axiom`, `ofReduceBool` and `implemented_by`. There are none.
   - The 22 `decide` occurrences in RTC are all in Part B.
   - In MirrorMain and MirrorNine_append, `decide` is used only on `Fin` index comparisons and on
     `Nat.choose (4+2) 2`, `(6+2) 2` and `(3+6) 3`. This is as the section states.
7. **Line numbers.** Every `file:line` in the statement heads, the map and the running text is exact, including
   helper references such as `chord_identity` (line 64), `exposed_not_in_hull` (30), `boundaryOfGon` (62/77),
   `unframeLin` (1886), RTC 1023/1050/1078/1503/1515/1527/1536/1547, and H3's `Mir.MirrorExclusionLine`.
8. **Compile check.** I compiled the section in a private wrapper (same preamble, run twice): exit 0.
   - The only undefined references are to allowed labels. These are the fd: labels, plus the mm:, sr: and ar: exports
     mm:def:config, mm:thm:{mirror-polygon, axis-polygon, odd, even, line, small}, sr:def:{iso, classes},
     sr:thm:main and ar:thm:main.
   - Every mb: reference resolves. All 7 export labels are defined on the required statements.
   - The 42 statement environments match the 42 map rows exactly.
9. **Circularity.**
   - mm.tex refers to mb: labels only in remarks and summaries; its proofs of mm:thm:mirror-polygon, axis-polygon,
     odd and line do not use mb.
   - Inside mb, Theorem mb:thm:nine(a) is proved before Proposition mb:prop:cap113, which is proved before (b),(c).
     There is no loop.
10. **Hypothesis use.** I checked that every cited external result is used within its stated hypotheses:
    - mm:thm:mirror-polygon with m=4;
    - mm:thm:axis-polygon (a)/(b) with m=4 ≥ 3 and `mir a = a`;
    - mm:thm:odd and mm:thm:line(b) with j=4, M=113;
    - sr:thm:main and ar:thm:main(a) with the two mirror classes discharged.

## Proof-by-proof notes (all correct)

- **mb:lem:config-mono (b).** `((l_0,l_{n-1}), l)` is an n-gon. The length-2 list is a cap because it has no
  consecutive triple, and n ≥ 2 gives `|l| ≥ 2`.
- **mb:lem:chain.** The downward induction on i is well founded, with Q(i) vacuous for i ≥ r-2.
  - Step A is an inner induction on k. It uses Q(i+1) with i+1 < k-1 < k, valid because k > i+2.
  - Step B uses Step A with j ≥ i+2, Q(i+1), and the second conclusion of (mb:eq:trans).
  - All elements lie in D.
- **mb:lem:lists.** (mb:eq:trans) is verified on D=[n] through mb:lem:signs and mb:lem:four. That needs x-sortedness of
  c, and the cap sign needs a<b<d, which holds. Part (c) uses f(i)=l_i.
- **mb:lem:boundary.**
  - Step 1 signs are correct: the lower chain is a cup with positive orientation, so interior u_i lie below the chord.
  - Step 2 gives U∩V={L,R}, and |B| follows from inclusion–exclusion.
  - Step 3 is exhaustive: w=u_j has three subcases; w=v_j at an end reduces to U; w=v_j interior uses the chord
    identity with coefficients x(R)-x(w)>0, x(w)-x(L)>0 and x(u_{i+1})-x(u_i)>0. No cross-chain x-distinctness is
    needed, so interleaving abscissae are fine.
  - Step 4 is a valid application of Step 3 to the reflected data, which satisfies all the hypotheses.
  - Step 5 has four exhaustive cases. Each exposing function is affine, vanishes at p and is >0 on B∖{p}. The
    strictness cases use u_{i-1} ∉ {u_i,u_{i+1}} and v_{j+1} ∉ {v_{j-1},v_j}.
  - The "elementary fact" is proved, via convex combinations.
  - The degenerate cases s=0 and t=0 are covered.
- **mb:prop:gon.** The index bookkeeping is right: s=|l'|-2 and t=|l|-2 are Lean's l and k, and s+t+2=m. The common
  ends come from the equal head/last entries of nonempty lists.
- **mb:prop:cap16, mb:lem:gc22, mb:prop:cap22.** The thresholds are 17 and 23, and both contradictions are correct.
- **mb:lem:split.**
  - (a) The bijection R(S)↔N is given by mir.
  - (b) Three axis points are collinear.
  - (c) p, q and mir p are pairwise distinct (y(q) ≥ 0 > -y(p)) and lie on a vertical line. The second case split
    (y(p)>0 or y(q)>0, else both on the axis) is exhaustive.
- **mb:lem:sort.** Sorting is correct: injectivity plus the cardinality count give image = T.
- **mb:lem:polygons.**
  - (b) is the case m=4 of mm:thm:mirror-polygon. The four triples of {0,1,2,3} are exactly the four hypotheses.
  - (a) adds mir c0, applies (b), and removes the extra point. T' ⊆ P, |T'| ≥ 7, then mono(a) and mono(d).
  - (c) and (d) use e=(a,c0,c1,c2) and e=(c0,c1,c2,a) in axis-left and axis-right with m=4, and `mir a = a`.
- **mb:lem:seven-of.** The y-sign split on (d0, d3, d1, d2) has five branches and is exhaustive.
  - Interior axis points are excluded by mb:lem:interior. The hypotheses x-order, y(p),y(q) ≥ 0 and y(a)=0 hold in
    both uses.
  - The one-axis-point condition forces y>0 on the other three points in the HL/HR branches.
  - Membership lists match Hcap, HL and HR verbatim.
  - The count is 2·15+2 = 32.
- **mb:lem:frame, mb:lem:affine, mb:lem:transport.** Correct. The conceptual proof uses M=[[n1,-n0],[n0,n1]],
  det M=ν and MᵀM=νI.
- **mb:thm:seven, mb:thm:eight.** Correct. The bound 44+2=46 uses only R(S).
- **mb:thm:nine (a).**
  - Claim 1: a 4-cap in S∖T has its head in T, which is a contradiction; a 9-gon in S∖T is a 9-gon in S.
  - Claim 2: the 5-cap case is impossible. In the 8-cup case, p<q<r, and the Cup3/Cap3 dichotomy is exhaustive
    because Cap3 = ¬Cup3. The two extensions are a 9-cup, which gives a 9-gon by mb:lem:config-mono(b), and a 5-cap.
    Both have entries in S.
- **mb:thm:nine (b),(c).** These are the case j=4, M=113 of mm:thm:odd and mm:thm:line(b).
- **mb:thm:refl32, mb:thm:classes, mb:thm:main3.** Correct. The three remaining classes are clearly marked as
  hypotheses, and Remark mb:rem:main3 names the records and the rigor label.

## Findings

All findings are minor. None affects the correctness of a statement or proof.

### F1 (minor): attribution of `Realization.lean`

- **Location:** mb.tex lines 39–47 ("the bridge files (adapted from M. Schroeder's archive, MIT licence)").
- **Issue:** `ErdosSzekeres/Omission/Realization.lean` is listed as adapted from Schroeder's archive. It has no
  attribution header: its first line is `import ErdosSzekeres.Omission.Domains`. `docs/THIRD_PARTY.md` (lines 111–116)
  says that `Realization.lean` "connects attained paths to this project's all-triples cups, caps …" and that "these
  connections … were added here". The other six bridge files do carry the Schroeder/MIT header.
- **Fix:** list `Realization.lean` separately as project code, or say "adapted from or built on".

### F2 (minor): axioms coverage of `cup_false_iff`

- **Location:**
  - lines 71–73, "these lines also cover … the bridge lemmas";
  - line 92, "Every Lean declaration stated below is Lean-checked (axioms evidence above)";
  - Lemma mb:lem:signs, whose head lists `Configuration.cup_false_iff`.
- **Issue:** `cup_false_iff` (Realization.lean:44) is not in the dependency cone of any printed theorem. The project
  uses it only in `ListGeometry.listCap_of_hasCap` and at Realization.lean:114, which are off the paths of this
  section, so none of the cited `#print axioms` lines covers it. It is still Lean-checked, because it compiles with the
  library and the file has no `sorry` or `axiom`, but the stated evidence does not show that.
- **Fix:** add "(compiled with the library; not in the printed cones)" for `cup_false_iff`. Alternatively, drop it
  from the head: `cap_sign` is the form actually used.

### F3 (minor): Remark mb:rem:baek(3) claims more than Proposition mb:prop:gon states

- **Location:** lines 191–193, "every N-gon of C_c yields N points in convex position (Proposition~\ref{mb:prop:gon})".
- **Issue:** Proposition mb:prop:gon is stated only for m ∈ {7,8,9}. The claim for every N is true, since the proof
  never uses the value of m, but the cited result does not state it. No proof in the section depends on the general
  claim.
- **Fix:** write "for N = 7, 8, 9", or add "(the proof of Proposition mb:prop:gon works for every m)".

### F4 (minor, unsure): range "for every N ≥ 3" attributed to Baek's Theorem 1.6

- **Location:** lines 179–181.
- **Issue:** The remark says the published Theorem 1.6 holds "for every N≥3". No repository source states this range:
  `MIRRORETV/README.md` gives only the theorem number and the form C(n-1,2)+2. I could not check it against the paper.
  The geometric statement does hold for all N ≥ 3 as a consequence of the vendored `main` and the bridges, so this is
  only about what the paper says.
- **Fix:** drop "for every N≥3", or say the range follows from the Lean form.

### F5 (minor): off-by-one in the description of the cups–caps induction step

- **Location:** Remark mb:rem:capcup, lines 204–205, "split S into the first entries of (a+2)-caps and the rest".
- **Issue:** In the notation of Theorem mb:thm:capcup, the target is an (a+2)-cap. The classical step, and the
  vendored step read in that notation, splits by first entries of **(a+1)-caps**, caps one shorter than the target.
  The vendored code splits by (a+2)-caps only because its step goes from (a,b+1),(a+1,b) to (a+1,b+1). The proof of
  Theorem mb:thm:nine(a) does it correctly: target 5-cap, split by 4-caps.
- **Fix:** write "(a+1)-caps", or say which induction step is meant.

### F6 (minor): wording in Remark mb:rem:generated

- **Location:** lines 643–647.
- **Issue 1:** "the generated statements are special cases of them" is not accurate for `cap_mirror_heptagon`. That
  statement is a sub-polygon of the octagon (seven of its eight points), not an instance of `cap_mirror_polygon`. The
  proof of mb:lem:polygons(a) handles this correctly through P ∪ {mir c0}.
- **Issue 2:** "the products y(c_i)(x(c_j)-x(c_k))" leaves out the products that involve the axis point, for example
  `c0 1 * (c0 0 - a 0)` at MirrorMain.lean:653.
- **Fix:** write "special cases or sub-polygons of them", and "products of a positive ordinate with a positive
  abscissa difference".

### F7 (minor): notation overloading

- **Locations:**
  - Proof of Proposition mb:prop:cap16 (lines 476–478): "Theorem~\ref{mb:thm:baek} with n=4 … and S=[n]". Here n is
    both Baek's parameter (4) and the number of points of c.
  - R denotes the right endpoint (Lemma mb:lem:boundary), the upper part R(S), and a ternary relation (Lemma
    mb:lem:chain).
  - c denotes the configuration, the line offset in lineRefl, the points c_0,…,c_3 and a point in Lemma mb:lem:four.
    In the proof of Theorem mb:thm:nine(b),(c), the quoted statement of mm:thm:odd uses c for a configuration, while
    part (c) uses c for the line offset.
- **Issue:** Each use is locally unambiguous, but a reader has to track the switches.
- **Fix:** in Proposition mb:prop:cap16, write "Theorem mb:thm:baek with parameter 4 (in place of its n)". Consider
  renaming the configuration to 𝔠, or the offset to c₀.

### F8 (minor): incomplete dependency list in a status line

- **Location:** status line after Theorem mb:thm:classes (line 997–998).
- **Issue:** "the written proof rests on the cited Theorem~\ref{mb:thm:baek}". Through Theorem mb:thm:seven and Lemma
  mb:lem:polygons, it also rests on Theorems mm:thm:mirror-polygon and mm:thm:axis-polygon. The status line of
  Theorem mb:thm:seven does list them.
- **Fix:** add "and on Theorems mm:thm:mirror-polygon, mm:thm:axis-polygon (through Theorem mb:thm:seven)".

### F9 (minor, editorial): duplicate coverage with section `mm`

- **Location:** Lemma mb:lem:polygons, Definition mb:def:mir, Lemma mb:lem:split, Lemma mb:lem:sort, Definition
  mb:def:frame, Lemma mb:lem:frame, Lemma mb:lem:affine, Lemma mb:lem:transport.
- **Issue:** The same Lean declarations are also stated and proved in mm.tex:
  - mm:prop:small-polygons (d),(e),(h),(i): `cap_mirror_heptagon`, `cap_mirror_octagon`, `axis_left_heptagon`,
    `axis_right_heptagon`;
  - mm:def:mir; mm:lem:count, mm:lem:injx; mm:def:config, mm:lem:sort; mm:def:frame, mm:lem:frame;
  - mm:lem:ngon(b) (`hasConvexNGon_affineMap`);
  - mm:thm:line(a) (`transport`).

  The two versions agree, both are correct, and mb acknowledges the overlap for `transport`. Still, the assembled
  document will carry two statements and two proofs per Lean name, and both Coverage paragraphs claim them.
- **Fix:** none needed for correctness. At assembly, either cite one version or add a cross-reference sentence.

## Points considered and not reported

- **Polynomial identities proved "by expansion".** Lemma mb:lem:four, the chord identity and Lemma mb:lem:frame are
  justified by expansion, with a note that they were "checked symbolically". This is acceptable for a written proof,
  since a reader can expand by hand. Optionally, (mb:eq:chord) has a two-line conceptual proof. Both sides minus the
  first two terms are affine in w and vanish at w=L and w=R, so they are a multiple of orient(L,R,w). Comparing the
  coefficient of y(w) gives the factor x(b)-x(a).
- **Lemma mb:lem:sort as an existence statement.** It is stated as "there is a configuration cfg(T) …", whereas the
  Lean `cfg` is a specific definition built with `Classical.choose`. Later proofs use only the stated properties, so
  there is no gap.
- **Theorem mb:thm:baek and the abstract cups–caps form are cited black boxes.** The contract and the task notes allow
  this explicitly. The section states both exactly as in the vendored Lean, says they are cited, and gives the
  sources.
- **Theorems mb:thm:classes and mb:thm:main3 refer to sr:def:classes, sr:thm:main and ar:thm:main.** Those are stated
  for SymmetricReduction.lean and AffineReduction.lean, while the Lean theorems use the RTC copies. The byte-identity
  that the section asserts holds, so the identification is valid.

## sympy script (essential content)

```python
from sympy import symbols, expand, simplify, binomial
# points A=(a0,a1), B, C=(c0,c1), D, W, P, Q; L=(s0,s1), R=(t0,t1); n0,n1,cc,u0,u1
orient = lambda A,B,C: (B[0]-A[0])*(C[1]-A[1]) - (B[1]-A[1])*(C[0]-A[0])
# four_left/right, chord, interior(y(a)=0), rho_orient, upper_edge, axis3, vertical,
# frame_lineRefl (both coords; second = -2(n0p0+n1p1)(nu-1)), orient_frame = (nu-1)orient,
# unframe_frame = (nu-1)(p-c n), frame_unframe = (nu-1)q, frame second coord = n.p - c nu,
# reflLine - lineRefl(-u1,u0,-u1 a0+u0 a1) = 2(p-a)(u0^2+u1^2-1) (both coords, Lean and written forms),
# geometric form a + <w,u>u - <w,n>n for both maps under u1^2 = 1-u0^2.
# Output: every difference expands to 0; binomials 15 21 28 84; C(N-1,2)+1 = 16 22 29; 32 46 226 113; 35 56.
```

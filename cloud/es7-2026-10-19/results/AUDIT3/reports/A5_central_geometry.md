# A5: central 34, geometric and combinatorial reductions

Component audit, 1 November 2026 (UTC), against `es7-cloud` at 471d5f63a. Texts returned by the auditor and by the independent verifier of each finding, lightly edited: machine paths replaced by placeholders and internal job names by descriptions; trust-table labels as explained in `../README.md`, §7.

**Component.** CENTRAL 34: geometric and combinatorial reductions (angular normal form, hull cubes, reduction A, second-layer split and covers, reduction B, interaction with the base formula's symmetry breaking)

**Statement audited.** Every centrally symmetric 34-point set in general position without a convex 7-gon (and so every such set of 34 or more points) yields a model of one of the solved unit CNFs. The chain: (1) every real configuration has an angular normal-form labelling whose first point is a hull vertex; (2) each of the 136 hull cubes says exactly that the hull is a given polygon, and the 136-way cover is certified; (3) reduction A: case P_a is equivalent to case P_(17-a); (4) each P_a (a = 1..8) splits into 560 second-layer subcases with a certified cover; (5) reduction B: subcases (P_a, V) and (P_a, {(a - i) mod 17}) are equivalent; (6) the base formula's symmetry breaking does not conflict with applying A and B on top of it.

**Verdict.** `sound_with_caveats`

## Summary

I found no blocking or major problem in the central-34 geometric and combinatorial reductions.

- **Normal form.** Every real configuration can be labelled from any of its hull vertices. I proved this myself and tested it on every hull vertex of 3,000 configurations.
- **Hull and second-layer cubes.** Each cube says exactly that the hull (or the second layer) is a given ccw polygon. The cube files equal my independently built cubes, and in real labellings exactly the geometric cube holds.
- **Reductions A and B.** I derived both myself (A: P_a to P_(17-a); B: (P_a,V) to (P_a,(a-V) mod 17), including which classes switch to the antipode). I also checked both mechanically on the full base: each relabelling maps every base clause into the base plus the hull clauses of (a,0), and maps the solved cube onto the excluded cube. Mutated maps are all detected. So the reductions need only one extra geometric line: in case P_a, the point (a,0) is a hull vertex. This is stronger than the repository's claim that B holds 'for real configurations only'.
- **Symmetry breaking.** The base breaks symmetry only by the 136 angular-order units and the clauses saying the first point is a hull vertex. There is no lex-leader, and no conflict with applying A and B on top.
- **Base validity and closure.** All 16.65M base clauses hold on real labellings except genuine 7-gon clauses, including on the exact unit CNF for the 34-point two-heptagon near-miss, whose subcase orbit is closed. My own closure from my cubes matches 2,596/2,596 recorded hashes and closes all covers, all hexagons and all orbits.

Caveats:
- The closure depends on B for 2,183 orbits and on A for P9..P16.
- Encoder validity is tested, not proved.
- My checks are my own unreviewed scripts.
- The write-up does not yet state A and B or update the central status (minor), and one README description is off by one (minor).

All scripts and logs are in AUDIT3/A5_central_geometry/.

## Trust table

| # | claim | basis | notes |
|---|---|---|---|
| 0 | Every real centrally symmetric 34-point set in general position has a normal-form labelling from ANY hull vertex p0: the centre is not a point; no other point lies on the line through c and p0; each other pair has exactly one point in the open half-plane left of c->p0; the angles are distinct. | written proof, re-derived by the auditor | My own proof. Tested on every hull vertex of 3,000 exact-integer configurations (geomtests_3000.log); the normal form never failed. |
| 1 | All 16,653,336 clauses of the base (sha b0061e90..., re-hashed by me) hold in every real normal-form labelling, except the clauses for genuinely convex 7-sets. | computational evidence (234 labellings; a test, not a proof) | Every clause evaluated, including the convex 7-gon encoding with auxiliary variables (my own rebuild of the variable numbering gives exactly 838,032). Ran on 234 labellings: the two-heptagon set, 30 perturbations of it, and 6 random sets with parallelogram, hexagonal and 10-gon hulls. The falsified clauses equalled, as a set, the 7-set clauses of the convex 7-sets, and each 7-set was rechecked from coordinates. The normal-form units and hull clauses also held on 53,196 labellings. This is a test, not a proof of encoder soundness. |
| 2 | The base's only labelling-dependent constraints are 136 angular-order units and 10,880 clauses saying the first point is a hull vertex. There is no lex-leader or other symmetry breaking. | written proof, re-derived by the auditor | Checked exhaustively on the actual file by streaming it. The unit clauses and the 3-literal clauses equal my own derivation exactly. No other clauses have 1 to 3 literals. zcnf.py has no lex option; the run used 'rot 17 7 --m 2 --hull'. The mutation tests show that every other clause is unchanged by any relabelling that keeps antipodal pairs together, with or without reflection. |
| 3 | Each hull cube (16 P_a, 120 H_a-b) asserts exactly that the hull is the ccw polygon (0,0),(a,0)[,(b,0)],(0,1),(a,1)[,(b,1)]: for every edge, every other point lies strictly left. In normal form that is equivalent to 'the hull classes are {0,a}' (or {0,a,b}). | written proof, re-derived by the auditor | All 136 cubes in cubes.txt equal my semantic cubes built from every polygon edge (static_checks.log). In 53,196 real labellings exactly one hull cube held, and it was the geometric one. |
| 4 | The 136 hull cubes cover the base. | certificate accepted by both checkers (auditor's label) | As recorded in CERTIFICATES.md and evidence/central34-cover. The LRAT proof is archived. I rebuilt the cover CNF hash bb60facb from my own semantic cubes and the streamed base. The checker logs themselves do not print the CNF hash. |
| 5 | All 120 hexagonal-hull cases are UNSAT. | certificate accepted by both checkers (auditor's label) | As recorded in hex_cases.tsv; proofs archived. All 120 recorded CNF hashes match my rebuild from my semantic cubes. Known caveat from C2FINAL: cake_lpr ran on a rebuilt CNF that was not hashed. |
| 6 | Reduction A: a real configuration in case P_a, relabelled from p_a, is in case P_(17-a). Old class i goes to new (i-a) mod 17, and old classes 0..a-1 are represented by their antipodes. | written proof, re-derived by the auditor | Derived myself. The exact predicted relabelling matched on 7,200 real labellings, and the classification checks passed on 14,400. Added by this audit: an exhaustive check at the CNF level. sigma_A(base) is contained in base + H_a (16,653,336 of 16,653,336 clause images present), sigma_A(P_b cube) = P_(17-b) cube, and sigma_A(H_b) lies in the base's own hull clauses, for b = 1..8. The scripts are mine and not independently reviewed; clauses are compared by 128-bit hash. |
| 7 | Second-layer cube (P_a,V) = the P_a hull cube plus: the 30 inner points have exactly the ccw hull (v1,0)..(vh,0),(v1,1)..(vh,1). | written proof, re-derived by the auditor | All 8x560 cubes in C2P/cubes equal my semantic cubes; the pilot P8 file is identical. In real labellings exactly one subcase cube held when the inner hull had 4 or 6 vertices (1,268 Q and 3,196 H labellings), and none held when it had 8 or more (2,736). |
| 8 | The inner 30 points of a 7-gon-free set have a hull with 4 or 6 vertices. | written proof, re-derived by the auditor | Uses the no-7-gon hypothesis: 8 or more hull vertices contain a convex 7-gon. Not load-bearing, because the 560-way covers are certified at the CNF level. |
| 9 | Each P_a cover (a = 1..8) is certified: base + P_a hull units + the negation of each of the 560 second-layer cubes is UNSAT. | certificate accepted by both checkers (auditor's label) | Recorded verdicts, both checkers. The P1-P7 proofs were deleted. The P8 cover was re-solved on 2026-11-01 (8851e2ac) with its proof archived. All 8 recorded CNF hashes match my rebuild from my own semantic cubes in lane.py format. |
| 10 | Reduction B: reflect, then start at rho(p_a). Old class i goes to new (a-i) mod 17. New (j,0) is rho(old (a-j,0)) for j<a, rho(old (0,0)) for j=a, and rho(old (17+a-j,1)) for j>a. So (P_a,V) maps to (P_a,(a-V) mod 17). | written proof, re-derived by the auditor | Derived myself. The exact predicted relabelling matched on 7,200 real labellings (14,400 classification checks, 320 fixed). Added by this audit: an exhaustive check at the CNF level, for a = 1..8: sigma_B(base) is contained in base + H_a, sigma_B(P_a cube) = P_a cube, and sigma_B(cube(V')) = cube(V) for all 560 subcases. Mutants were detected. |
| 11 | H_a ('(a,0) is not inside a triangle of three other points') holds in every real configuration satisfying the P_a cube. | written proof, re-derived by the auditor | One line: all other points lie strictly left of the line (0,0)->(a,0), which passes through (a,0). This is the only geometric fact the CNF-level forms of A and B add. |
| 12 | Every orbit of P1..P8 has a refuted member; all 8 covers and all 120 hexagons are refuted. | Lean-checked bookkeeping (project's file) and exact computation (auditor's closure); verdicts recorded | Lean (Central34Orbits.lean, authors) checks the bookkeeping only. I independently recomputed the closure in Python using only my semantic cubes and my derivation of the maps. 2,596/2,596 recorded hashes match my rebuild, 0 mismatch; 287/287 orbits closed per case. The underlying SAT verdicts are recorded both-checker verdicts, mostly with deleted proofs. |
| 13 | Excluding 34 points excludes every centrally symmetric set of 33 or more points. | written proof, re-derived by the auditor | In general position the centre cannot be a point, since c, p, -p are collinear. So the size is even, and deleting antipodal pairs reaches 34. A point reflection is the only affine involution with an isolated fixed point. |

## Findings

### A5-1 (note): Reductions A and B hold at the CNF level, which is stronger than the repository claims

For each relabelling I built the induced map sigma. On triple variables it is chi_new(T) = eps * chi_old(pi(T)), with eps = +1 for A and -1 for B. On convex-set variables it maps conv(S) to conv(canon(pi(S))). sigma is consistent on every triple class and is a bijection on the 838,032 variables. For all 8 A maps (b = 1..8, a = 17-b) and all 8 B maps (a = 1..8), every one of the 16,653,336 base clauses maps into base + H_a, where H_a is the 10,880 clauses saying '(a,0) is not inside a triangle of three other points'. The cube parts also map exactly: sigma_A(P_b) = P_(17-b), sigma_A(H_b) lies in the base hull clauses, sigma_B(P_a) = P_a, and sigma_B(cube(P_a,V')) = cube(P_a,V) for all 560 subcases of each case. So UNSAT(base + cube(V')) implies UNSAT(base + H_a + cube(V)), and H_a holds in every real P_a configuration (one line). The mutation tests show the check has teeth: no sign change gives 136 missing images; no switch to the antipode gives 72; two classes swapped gives 1; A with the wrong switch gives 70; the wrong extra hull set gives 10,880; wrong partner rules give 560 of 560 cube mismatches. C2P/README says (B) 'holds for real configurations only, not as a symmetry of the CNF'. That undersells it: the only labelling-dependent clauses are the 136 order units and the hull clauses, and the maps carry them onto order units and onto hull clauses of another hull vertex.

*Evidence.* AUDIT3/A5_central_geometry/symcheck.log, symmaps.log, hullimage.log, symmut.log, cubemut.log (scripts symmaps.py, symmaps_lib.py, symcheck.c, symmut.py, cubemut.py in the same directory)

*Suggested fix.* State A and B in the write-up in this form (literal map plus the H_a remark) and add an equivalent check script to the evidence. This turns both reductions from prose arguments into a mechanical check plus one geometric line.

### A5-2 (minor): The write-up has no self-contained statement of reductions A and B and still calls the central case open

WRITEUP/SYMMETRIC.md ('Status of the central 34-point search (2026-10-29)') and note/symmetric_es7.tex still give the old status. C2C34/README §6 still calls the reflection argument 'not yet independently reviewed'. The explicit relabellings appear nowhere in the write-up: old i to new (i-a) mod 17 with classes 0..a-1 switched to their antipodes for A, and old i to new (a-i) mod 17 with classes i > a switched for B. The arguments are correct: I re-derived both, and the exact predicted index maps matched on 7,200 + 7,200 real labellings. But a public claim should carry them. Partly known (C2FINAL finding 6).

*Evidence.* grep of WRITEUP/SYMMETRIC.md lines 184-199 and note/symmetric_es7.tex lines 244-249; C2C34/README.md §6

*Suggested fix.* Before claiming, add a short lemma with the two index maps, the representative rule, why the second-layer cube depends only on the class set and the ccw order, and the 'P_a cube implies H_a' remark (or cite the CNF-level check of A5-1).

**Independent check:** real = yes; severity minor -> **minor**.

The finding is correct. Every documentary claim in it checks out, and so does the mathematics it reports.

1. The write-up gives the old status and lacks reductions A and B.
- The status section of WRITEUP/SYMMETRIC.md is still the old one. Lines 186-198 say "The 8 canonical parallelogram cases are open" and quote the P8 pilot at 64 of 287. The file was last committed in de02b4914 on 2026-10-30.
- The note says "The parallelogram cases are open" (symmetric_es7.tex, about lines 243-251, last committed in a49b92d6d).
- The same holds for one place the auditor did not list: WRITEUP/CERTIFICATES.md line 154, "the central 34-point case remains open".
- The records say otherwise. C2FINAL/recount.json shows all eight cases P1..P8 with 287 of 287 orbits closed and their covers certified.
- Nothing in WRITEUP/*.md or the .tex states A or B. A grep for antipod, reduction, "(a − i) mod 17" and P_(17−a) finds nothing relevant.

2. Where the reductions do appear.
- The class maps appear only in brief, without the rule for which point represents each class: C2P/README.md:60, C2P/review/README.md:3-4, C2FINAL/README.md:14-16, and C2C34/README.md:129 (for a = 8 only).
- The representative rule (which classes switch to their antipode) is written down only in code. The docstring of C2P/review/litcheck.py gives the position model, and the docstring of C2C34/l2cubes.py states the ccw-order fact.
- C2C34/README.md line 126 still says "not yet independently reviewed". But C2P/review (2026-10-31) and C2FINAL §8 both reviewed A and B.
- C2FINAL finding 6 records only part of this: the stale "open" status in C2C34/README and SYMMETRIC.md. So "partly known" is accurate.

3. The index maps are correct. I checked them with my own exact-integer script, which uses no project or auditor code.
- The script built 2,500 centrally symmetric 34-point sets with a parallelogram hull, giving 10,000 labellings. All 16 hull cases occur, with 2,250 distinct (a, V).
- **Reduction A** (start again at p_a): old (i, s) goes to ((i−a) mod 17, s xor [i < a]), and the hull case becomes P_(17−a). 0 failures.
- **Reduction B** (reflect, then start again at the image of p_a): old (i, s) goes to ((a−i) mod 17, s xor [i > a]), and the hull case stays P_a. 0 failures.
- The complementary conventions also give 0 failures. Starting again at −p_a or at its image flips the side rule.
- 7,816 labellings have a second layer with 4 or 6 vertices. In each, the geometric hull cube and second-layer cube hold, as I defined them from l2cubes.py. No other subcase cube holds, and the predicted image cube holds after both A and B.
- As a negative control, seven wrong variants (off-by-one side rules, wrong class maps) each mismatched on 1,200 of 1,200 labellings. The claimed maps mismatched on 0.

4. Two refinements.
- Calling the central case "open" agrees with the project's stated position. C2FINAL lines 5-7 say the result is not yet claimed until the random re-solve sample finishes. So that wording is out of date, not wrong. What is stale is the progress detail, the "not yet independently reviewed" phrase, and the missing lemma.
- The side rule depends on which hull point the labelling restarts from. C2P/review restarts at the image of (a,1), which gives the complementary rule. The lemma should fix one convention.

5. Severity: minor, as the auditor rated it. The claim depends on these reductions: A carries P9..P16 and B carries nearly all orbits not fixed by the reflection. But the reductions are correct and have been independently reviewed. What is missing is the written exposition, which is fixable and must be added before any public claim. It does not threaten the claim.

*Verifier's evidence.* Re-read for this check:
- R/WRITEUP/SYMMETRIC.md lines 184-198
- R/WRITEUP/note/symmetric_es7.tex lines 242-251
- R/WRITEUP/CERTIFICATES.md line 154
- R/C2C34/README.md lines 12, 53-59 and 117-170 (line 126: "not yet independently reviewed")
- R/C2P/README.md:56-64 and R/C2P/review/README.md
- R/C2P/review/litcheck.py (docstring), R/C2C34/l2cubes.py and R/C2C34/hullcubes.py
- R/C2FINAL/README.md lines 5-7, 14-16 and 163-164 (finding 6)
- R/C2FINAL/recount.json: P1..P8 each 287/287 orbits closed, cover_certified 1

Last commits from git log: SYMMETRIC.md de02b4914 (2026-10-30); tex and CERTIFICATES a49b92d6d (2026-10-29); C2C34/README de02b4914. All predate C2P/review (00ef95bd4, 2026-10-31) and C2FINAL (2026-11-01).

The grep found no antipod, reduction, (a−i) mod 17 or P_(17−a) in WRITEUP/*.md or the .tex.

My scripts are in AUDIT3/A5_central_geometry/verify_A5-2/:
- indexmaps.py, log indexmaps_2500.log: 2,500 sets, 10,000 labellings. A, A', B and B' each had 0 failures. 7,816 subcase checks for each of A and B. Second-layer cube unique in 7,816 of 7,816. 16 hull cases, 2,250 distinct (a, V). 27 s.
- mutcheck.py, log mutcheck.log: claimed maps mismatched on 0 of 1,200 labellings; every wrong variant on 1,200 of 1,200.

### A5-3 (minor): Off-by-one wording: 'numbers of antipodal classes between consecutive hull vertices ... summing to 17'

The classes strictly between consecutive hull vertices number (a-1, 16-a) for a parallelogram, summing to 15, and (a-1, b-a-1, 16-b) for a hexagon, summing to 14. What sums to 17 is the index gaps (a, 17-a) or (a, b-a, 17-b). The canonical counts (8 and 24) are right for the gaps. Not load-bearing: all 120 hexagons were solved directly, and reduction A is verified separately.

*Evidence.* C2C34/README.md §2 'Canonical cases'; SYMZ/README.md lines 147-151

*Suggested fix.* Say 'index gaps between consecutive hull classes'.

**Independent check:** real = yes; severity minor -> **minor**.

The auditor is right: the sentence is off by one.

**The normal form.** I re-read zcnf.py (SB docstring lines 34-37, add_sb, add_hull_sb) and hullcubes.py (lines 2-7, 29-34).
- In angular order around c the points are (0,0), (1,0), ..., (16,0), (0,1), (1,1), ..., (16,1).
- Case P_a has hull classes {0, a}. Case H_{a,b} has hull classes {0, a, b}.

**What the counts actually are.**
- Classes strictly between consecutive hull classes: (a-1, 16-a), sum 15, or (a-1, b-a-1, 16-b), sum 14.
- Points strictly between consecutive vertices of the full polygon: 30 or 28.
- Only the index gaps (a, 17-a) and (a, b-a, 17-b) sum to 17. These count each hull class together with the classes up to the next hull class, which is not the usual meaning of "between".

**The two READMEs.**
- SYMZ/README.md lines 147-148 also say "positive integers". Read literally, that is false too: P1 gives (0,15) and H1-2 gives (0,0,14).
- The SYMZ sentence only holds together under the gap reading. So the authors meant gaps but wrote "classes between". This is not a misreading by the auditor.

**Why it threatens nothing.**
- The strict counts are just the index gaps minus 1 in each entry. That map is one-to-one, preserves lexicographic order and commutes with rotation and reversal.
- So the least-sequence rule picks out exactly the same cases under either reading: 8 + 24 = 32 orbits, identical to canonical.txt.
- The rotation and reversal steps of the argument also hold.
- The wording has no mathematical effect. It is a fixable documentation error in two README files, which is minor on the given scale. It is not blocking or major.
- The auditor's suggested fix ("index gaps between consecutive hull classes") is appropriate.
- The main write-up (SYMMETRIC.md line 188: "136 cases (32 up to rotation and reflection)") and C2P/review/coverage.py line 51 ("cyclic gap sequence") are worded correctly. Only the two cited READMEs carry the slip.

*Verifier's evidence.* **Wording confirmed verbatim in:**
- C2C34/README.md line 54
- SYMZ/README.md lines 147-148

**My check:** AUDIT3/A5_central_geometry/verify_A5-3/check_gaps.py, log check_gaps.log in the same directory. Exact integer arithmetic, 0 failures.

**Part 1, all 136 cases (the case list matches cubes.txt name for name):**
- Index gaps sum to 17 in all 136 cases.
- Classes strictly between consecutive hull classes sum to 15 in all 16 P cases and 14 in all 120 H cases.
- Over the full polygon the strictly-between point counts sum to 30 or 28.
- 44 cases have a zero strict count (P1 (0,15), P16, H1-2 (0,0,14), ...), so "positive integers" fails under the literal reading.
- The least form under rotation and reversal gives 8 P + 24 H, equal to canonical.txt, under both readings; 32 orbits either way.

**Part 2, geometry:**
- 408 random centrally symmetric 34-point sets in general position (3 per case, all 136 cases).
- 4,704 normal-form labellings recomputed from scratch, starting from every hull vertex of each set and of its mirror image.
- The geometric count of classes strictly between consecutive hull vertices always equals the index gap minus 1, with sum 17 - k (k = 2 or 3 hull classes).
- Changing the starting vertex rotates the gap sequence; mirroring reverses it.
- Exactly one canonical.txt case is reached per configuration.

**Mutation tests** (mut/ in the same directory):
- Requiring the geometric counts to equal the index gaps (the literal sum-17 reading) fails in all 1,568 labellings.
- Reversing the rotation direction gives 480 failures.
- A mutated canonical.txt gives 10 failures.

### A5-4 (note): Symmetry breaking in the base is exactly the normal form; no stacked-symmetry-breaking conflict

I streamed the base (sha re-hashed: b0061e90): 136 unit clauses, exactly my angular-order units chi(c,(0,0),(o,0)) = + and chi(c,(o,0),(o',0)) = + for o < o'; 10,880 three-literal clauses, exactly my 'first point not inside a triangle' clauses (16 tautological triangles skipped, consistently); no other clauses with 1 to 3 literals. Everything else is 4- or 6-literal triple clauses (A4/GP) or convex-encoding clauses. zcnf.py has no lex-leader option, and the run used 'rot 17 7 --m 2 --hull'. The normal form is existential: any hull vertex may come first. So every relabelling used by A and B yields another valid normal form. The A5-1 check confirms this mechanically.

*Evidence.* base_structure.log, base_units.txt, static_checks.log, symmut.log

### A5-5 (note): Full-base evaluation, including the 7-gon encoding; the two-heptagon near-miss lies in a closed orbit

All 16,653,336 clauses were evaluated with auxiliary variables set to the true convexity, on 234 real normal-form labellings. The falsified clauses equalled, as a set, the 7-set clauses of the canonical convex 7-sets, with counts from 1 to 61,351. Each such 7-set was rechecked from coordinates. For the 34-point two-heptagon set (C2P/nestsets) exactly 1 clause is falsified in all 8 labellings (4 hull vertices, original and reflected), and still exactly 1 when its own subcase cube is appended, i.e. on the exact unit CNF solved. Its labellings fall into P8_7-11 / P8_1-14 (after A for the P9 labellings), which form one B-orbit, refuted by the pilot record P8_1-14 (both checkers; hash matches my rebuild). This is consistent and shows the encoding is not over-constrained in the hard region.

*Evidence.* fullbase_heptagon.log, fullbase_perturb.log, fullbase_random.log (fullbase.py, evalcnf.c)

### A5-6 (note): The closure depends entirely on reductions A and B; my independent orbit closure agrees

Using only my semantic cubes and the recorded hashes: 2,619 records, 16 third-layer records skipped, 7 without hash (re-solved later), 2,596 hash matches and 0 mismatches. All 120 hexagons, all 8 covers and 287/287 orbits per case are closed. Only one orbit (in P6) has both members refuted. So 2,183 of 2,296 orbits rely on B, and P9..P16 rely on A. Given A5-1, the remaining non-SAT trust base is: (i) every base clause is valid in real normal-form labellings (tested, not proved); (ii) a normal form exists; (iii) the P_a cube implies H_a. Because the hull and second-layer covers are certified at the CNF level, the converse cube semantics, and the 'inner hull has 4 or 6 vertices' fact (which needs no 7-gon), are not load-bearing.

*Evidence.* orbitclosure.log, hashcheck.log

### A5-7 (note): Hull-cover checker logs do not record which CNF was checked

C2FINAL/evidence/central34-cover shows the CaDiCaL header 'p cnf 838032 16653472' and both verdicts, but no CNF hash. The link to bb60facb comes from CERTIFICATES.md; the CNF and proof are archived and can be rechecked. I rebuilt bb60facb from the streamed base and my own semantic cubes (comment line dropped, as hullcubes.py does). This belongs to the certificate audit.

*Evidence.* hashcheck.log; C2FINAL/evidence/central34-cover/*.out

*Suggested fix.* Optionally re-hash the archived cover.cnf.zst and re-run one checker on it.

## Tests run by the auditor

- static_checks.py: base units and hull clauses against my derivation; rebuilt variable numbering (838,032); all 136 hull cubes and 8x560 second-layer cubes equal my semantic cubes; orbit files equal i->(a-i) mod 17 (287 orbits, 14 fixed per case). 0 failures.
- geomtests.py (3,000 exact-integer configurations, 53,196 labellings): order units and hull clauses hold; exactly one hull cube true and it is the geometric one; second-layer cubes as geometry says; A and B relabellings equal my predicted index maps exactly (7,200 each); classification checks 14,400 for A and 14,400 for B. 0 failures.
- fullbase.py + evalcnf.c: every base clause on 234 real labellings plus 8 unit CNFs (two-heptagon set, 30 perturbations, 6 random sets); falsified set = convex-7-set clauses exactly. All OK.
- hashcheck.py / orbitclosure.py: recorded CNF hashes rebuilt from the streamed base and my semantic cubes: 2,596/2,596 match; hull cover bb60facb; 8 covers; 120 hexagons; 287/287 orbits per case closed.
- symmaps.py + symcheck.c (16 runs over the full base): sigma(base) in base + H_a with 0 missing for A (b=1..8) and B (a=1..8); cube maps exact for all 4,480 subcases; hullimage.py: sigma_A(H_b) in base.
- symmut.py / cubemut.py: 5 base-level mutants and 3 wrong partner rules, all detected (1 to 10,880 missing images; 546 to 560 of 560 cube mismatches).
- base sha256 streamed: b0061e90... (matches); base.json sha 2476faff... (matches).


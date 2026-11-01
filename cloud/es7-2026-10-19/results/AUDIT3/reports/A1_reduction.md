# A1: reduction to the case theorems

Component audit, 1 November 2026 (UTC), against `es7-cloud` at 9cf4949a5. Texts returned by the auditor and by the independent verifier of each finding, lightly edited: machine paths replaced by placeholders and internal job names by descriptions; trust-table labels as explained in `../README.md`, §7.

**Component.** REDUCTION: Corollary 3 (WRITEUP/SYMMETRIC.md §1-2, note/symmetric_es7.tex Lemma sizes, Cor. cor:only, Prop. prop:C), extended by the central 34-point case, plus the table of largest symmetric 7-gon-free sizes

**Statement audited.** Claim: if S has at least 33 points in general position and has a nontrivial symmetry, isometric or affine, then S contains a convex 7-gon. It follows from the case theorems C3-33, M33 (16 pairs + 1 axis point), M34 (17 pairs, no axis point), C5 (35 or more points), C4-32 and C2-34, together with the elementary orbit facts. Also audited: the table N(C2)=32, N(C3)=31, N(C4)=28, N(C5)=31, N(C6)=30, N(mirror)=32, and the same statements for affine symmetries.

**Verdict.** `sound_with_caveats`

## Summary

The reduction is correct. No blocking or major issue was found.

My own proof: S spans the plane, so its isometry group (and its affine symmetry group) acts faithfully on S. The group is therefore finite and fixes the centroid. In the affine case, averaging an inner product conjugates the group into O(2), and the conjugating map preserves general position and convex 7-gons. A nontrivial element is either a reflection or a rotation with a subgroup of prime order p:
- p >= 7: any orbit other than the centre is a regular convex p-gon.
- p = 2: the centre is not in S (it would be collinear with p and -p), the size is even and >= 34, and 17 antipodal pairs give C2-34.
- p = 3: the size is 3k+e with e <= 1, so k >= 11 and 11 orbits give C3-33.
- p = 5: sizes 33 and 34 are impossible, so C5 >= 35 applies.
- Reflection: at most 2 points lie on the axis. With none, 17 pairs give M34; with one or two, 16 pairs plus one axis point give M33.

Deleting whole orbits keeps general position and the symmetry. The exact hypotheses of every case theorem match what this supplies, including whether the centre or an axis point is in the set. The implicit encoder preconditions also hold: the perturbation for C3 and C5 is valid, and even orders need none.

The arithmetic is Lean-checked for all n (core Lean, omega, standard axioms) and was also checked exhaustively up to n = 600 and order 60.

The minimal set of case theorems is {C3-33, C5>=35, M33, M34, C2-34} plus the regular-orbit lemma. Each one is necessary. The fourfold and sixfold cases are redundant for the claim once C2-34 holds; the fourfold result is still needed for N(C4) = 28. The 33-point statement alone needs only C3-33 and M33.

The table entries C2 32, C3 31, C4 28, C5 31, C6 30 and mirror 32 are re-derived. All cited example files exist with the right sizes. Each example's full symmetry group is exactly the listed type.

Caveats, all documentation-level:
- A1-F1: the assembled theorem is not written anywhere. SYMMETRIC.md and the tex note still treat the central case as open and assume the fourfold result.
- A1-F2: the fourfold case is cited to arXiv:2506.00224, which C4CUT says ends on a heuristic step. C4CUT's own README still says its encoder review is pending, although the review is recorded.
- A1-F3: the affine extension is one sentence with the finiteness argument missing; I checked that it is correct.
- A1-F4: the overall claim is conditional on C2-34, which C2FINAL/README.md does not yet claim. The live sample shows 23 of 24 units done, all accepted by both checkers, with P8_1-10 still running.

Outputs, all in AUDIT3/A1_reduction/:
- size_arith.py and size_arith.log
- SizeArith.lean and SizeArith.lean.log
- examples_check.py and examples_check.log
- affine_controls.py and affine_controls.log
- c5_group.py and c5_group.log
- SHA256SUMS.txt

## Trust table

| # | claim | basis | notes |
|---|---|---|---|
| 0 | The isometry group G of a finite planar set S with at least 3 non-collinear points is finite, fixes the centroid, and so is C_n or D_n about the centroid. Every element is a rotation about the centroid or a reflection in a line through it, so there are no translations or glide reflections. | written proof, re-derived by the auditor | Proof: an isometry fixing 3 affinely independent points is the identity, so G embeds in Perm(S). Affine maps preserve barycentres. Then Leonardo's theorem. Exact sanity check: the full affine groups of the 6 example sets and of 4 controls all fix the centroid. |
| 1 | Affine version: the affine symmetry group of S is finite, fixes the centroid, and is conjugate by a linear T into O(2). A finite-order linear map with det -1 is conjugate to a reflection; one with det +1 is conjugate to a rotation. T(S) is in general position and has the same convex subsets, so every case theorem transfers. | written proof, re-derived by the auditor | SYMMETRIC.md states this in one sentence; the tex note does not state it. Averaging check: B = sum of L^T L satisfies L^T B L = B for every symmetry found on the examples, including the non-orthogonal Eisenstein-coordinate C3 and C6 symmetries (B=[[4,-2],[-2,4]]). |
| 2 | Rotation of order s about c: every orbit other than {c} has exactly s points and forms a regular s-gon. For s >= 7, any non-centre orbit is a convex 7-gon. | written proof, re-derived by the auditor |  |
| 3 | Even order: c is not in S (c, p, -p would be collinear), so s divides \|S\|. Odd order: \|S\| is 0 or 1 mod s, and c may be in S. | written proof, re-derived by the auditor | Only \|S\| >= 2 is needed, not \|S\| >= 3. The examples agree: the C3 and C5 examples contain the centre, the C2, C4 and C6 examples do not. |
| 4 | Size arithmetic for every n >= 33 and every type: C3 has >= 11 non-central orbits. C5 sizes 33 and 34 are impossible, so n >= 35. C4 has n >= 36, with >= 8 orbits and >= 17 pairs. C6 has >= 11 C3-orbits and >= 17 pairs. C2 has n >= 34. Mirror has >= 17 pairs if b = 0 and >= 16 if b >= 1. Every order s >= 2 is divisible by 2, 3 or 5, or is >= 7. | Lean-checked | Core Lean 4.24.0, omega/decide, 20 theorems for all n. Axioms: propext, Classical.choice, Quot.sound; no sorry. Also checked by exhaustive script for n <= 600, s <= 60. |
| 5 | Mirror reduction: b <= 2 points lie on the axis and n is congruent to b mod 2. b = 0 gives 17 pairs (M34). b = 1 or 2 gives 16 pairs + 1 axis point (M33). | written proof, re-derived by the auditor | Arithmetic is Lean-checked. |
| 6 | Deleting whole orbits of the chosen cyclic subgroup, the centre, mirror pairs or axis points keeps general position and invariance under the chosen rotation or reflection. | written proof, re-derived by the auditor |  |
| 7 | The hypotheses of each case theorem match what the reduction supplies, including centre and axis status. C3: 33 points, c not in S, rotation by +120 deg (same group as -120). C5: >= 35 points, centre allowed. C4: 32 points. C2: 34 points (c not in S automatically). M33: exactly 1 axis point. M34: none. | written proof, re-derived by the auditor | Implicit encoder preconditions checked. C3 (C3a/C3-S) and C5 (SYM5 §1) assume no two points collinear with c; this is justified by rotating each orbit by its own small angle, since same-orbit angles are multiples of 120 or 72 deg, never 180. Even orders need no perturbation: a line through c holds at most one antipodal pair. Mirror: distinct pair heights, and no axis point at a pair's height, both by general position. |
| 8 | Minimal set of case theorems for the claim: {C3-33, C5>=35, M33, M34, C2-34} plus the regular-orbit lemma. Each is necessary. C4-32 and any sixfold argument are redundant once C2-34 holds. | Lean-checked (arithmetic only) | The arithmetic is Lean-checked; necessity and redundancy were also checked by script. Exactly 33 points needs only C3-33 and M33. |
| 9 | Upper bounds in the table: N(C3) <= 31, N(C5) <= 31, N(C4) <= 28, N(C6) <= 30, N(C2) <= 32, N(mirror) <= 32, each given its case theorems. | Lean-checked (arithmetic only) | Arithmetic only. The inputs are: C3 uses C3-33. C5 uses C5>=35. C4 uses C4-32 (C2-34 alone gives only 32). C6 uses C3-33 or C2-34. C2 uses C2-34. Mirror uses M33 and M34. |
| 10 | The lower-example files exist with the stated sizes: SYMMAX/c3_31points.txt (31), c4_28points.txt (28), c5_31points.txt (31), c6_30points.txt (30), mirror_32points.txt (32), SYM2/sym7_32points.txt (32). | exact computation (auditor's own script) | Own exact-arithmetic script, not reusing project code. Points are distinct and invariant; the centre is present only in C3/C5; mirror has no axis point; no three points are collinear. Each full symmetry group is exactly the listed type (C3, C4, C5, C6, D1, C2). Freedom from convex 7-gons was NOT checked by A1. |
| 11 | INPUT C3-33 (C3FINAL), not re-verified by A1 | recorded verdict only (proofs not retained) | Per-piece proofs deleted. Composition replayed; 2,120 pieces re-solved (sampled_reverification). |
| 12 | INPUT M33 (SYMZ 2a; MIRROR.md Lean chain), not re-verified by A1 | certificate accepted by both checkers (auditor's label) | SYMZ keeps the LRAT proof. The Lean chain's statement (card 33, any line) is equivalent, since odd size forces exactly one axis point. |
| 13 | INPUT M34 (SYMZ 2b), not re-verified by A1 | certificate accepted by both checkers (auditor's label) |  |
| 14 | INPUT C5>=35 (SYM5), not re-verified by A1 | certificate accepted by both checkers (auditor's label) |  |
| 15 | INPUT C4-32 (C4CUT), not re-verified by A1; needed only for N(C4)=28 | certificate accepted by both checkers (auditor's label) | Also rests on the soundness of the even-m layered encoder (written argument plus independent review) and on the 6 cuts (two verifiers). |
| 16 | INPUT C2-34 (C2FINAL + C2C34), not re-verified by A1 | recorded verdict only (proofs not retained) | Composition, hash match and Lean bookkeeping replayed; random re-solves are sampled_reverification. C2FINAL/README.md says the claim is NOT yet made. |

## Findings

### A1-F1 (minor): The assembled theorem is not written anywhere; the write-up still treats the central case as open

No document states and proves the overall claim. SYMMETRIC.md is out of date in Cor. 3, in the §2 table row for C2 ('at least 32; exactly 32 if ES(7) = 33') and in §4 ('open'). The tex note is out of date in its abstract, in cor:only (which still assumes the fourfold result), in prop:C ('N(C_2) >= 32') and in 'What remains open'. C2FINAL review item 6 already notes this. The missing step is one correct line: a set whose only symmetry is the half-turn has c not in S and even size >= 34, so it contains 17 antipodal pairs, and C2-34 applies.

*Evidence.* WRITEUP/SYMMETRIC.md lines 59-72, 83, 184-198; note/symmetric_es7.tex lines 121-131, 157-168, 242-251; C2FINAL/README.md §8 item 6

*Suggested fix.* State one theorem with exactly the hypotheses {Thm 1, Thm 2a, Thm 2b, Thm E (C5 >= 35), C2-34}. Prove it via a prime-order subgroup: C2 -> 17 pairs; C3 -> 11 orbits; C5 -> sizes 33-34 impossible; p >= 7 -> regular p-gon; reflection -> b = 0 or b >= 1. Update the C2 row to 32.

**Independent check:** real = yes; severity minor -> **minor**.

The finding is correct in substance. It is documentation only and does not threaten the claim, so minor stands.

1. The assembled theorem is not written anywhere. At tip 9cf4949a5 no document states "every set of >= 33 points in general position with a nontrivial symmetry contains a convex 7-gon", with or without C2-34 as a hypothesis. The nearest statements fall short:
- SYMMETRIC.md Cor. 3 and tex cor:only still assume the published fourfold exclusion and leave the half-turn case.
- SYMMAX/README.md:29 states only the 33-point version.

2. The cited passages are stale exactly as described. SYMMETRIC.md was last changed on 2026-10-30 and the tex note on 2026-10-29. Since then the C2P waves (to 2026-10-31), C2FINAL and C4CUT (2026-11-01) were committed. Even so:
- SYMMETRIC.md:194-198 still says "The 8 canonical parallelogram cases are open ... Neither closes the case".
- tex:248 says "The parallelogram cases are open".
- The abstract, cor:only and prop:C still rely on the fourfold result and on N(C2) >= 32.

3. The proposed step and assembly are correct. This covers the half-turn line and the prime-order assembly with the hypotheses {C3-33, M33, M34, C5>=35, C2-34}:
- If c were in S, then c, p and 2c-p would be three collinear points. So c is not in S, the size is even and at least 34, and 17 pairs give a C2-34 instance.
- I checked this by hand, mechanically for n <= 3000 and primes <= 400, and in core Lean for all n (omega, standard axioms only).
- The fourfold result is redundant given C2-34, since a rotation of order 4 squares to the half-turn.
- The central 32-point example checks out exactly: half-turn symmetric about (0,0), centre not in the set, no collinear triple, largest convex subset 6. So N(C2) = 32 once C2-34 holds.

Imprecisions in the finding:
(a) C2FINAL §8 item 6 only partly "already notes this". It names C2C34/README.md and SYMMETRIC.md as calling the parallelogram cases open. It does not mention the tex note, Cor. 3's fourfold hypothesis, the C2 row or prop:C, or the missing assembled theorem.
(b) The "missing step" is already written as a remark: SYMMETRIC.md:184-185 ("Excluding 34 points excludes all of them, since pairs can be deleted"), tex:243-245 and C2C34/README.md:8. What is missing is the assembled statement with the minimal hypotheses, not the step.
(c) The list of stale documents is incomplete. Also stale: SYMMAX/README.md:13 and :41 ("open", "Not excluded: centrally symmetric sets of 34 or more"), SYMZ/README.md:126, C2C34/README.md:12 and :22, and WRITEUP/CERTIFICATES.md:154.
(d) "Update the C2 row to 32" is premature. C2FINAL says C2-34 is "not yet claimed", and at 12:35Z the re-solves of P8_1-10 and P8_4-9 were still running. Until the claim is made, "at least 32" is the correct official status. The write-up's conclusion that the central case is open matches that status; what is stale is its account of the progress.

Severity: no current document overclaims (one could argue for note), but the write-up must be rewritten before the overall result is claimed.

*Verifier's evidence.* Output directory: AUDIT3/A1_reduction/verify_A1-F1/
- scan_docs.py and scan_docs.log: all 15 quoted stale phrases are present at the cited lines (SYMMETRIC.md 59-63, 83, 184-198; tex 21-24, 122-123, 160, 244-248; C2FINAL 6-7, 163-164). C2FINAL item 6 does not mention the tex note, the corollary, the table row, N(C2) or a theorem. Of the 11 candidate paragraphs about symmetric sets of 33 or more points, none states the assembled theorem; SYMMAX/README.md:29 states only the 33-point version. Seven files still call the central case open.
- reduction_arith.py and reduction_arith.log: for n = 33..3000 and primes up to 400, 0 witnesses are uncovered. The half-turn line holds and the smallest possible half-turn size is 34. Fivefold sizes 33 and 34 are impossible. Without C2-34 only half-turns are left. Every fourfold size is covered by C2-34. At n = 33 only C3-33, M33 and the regular-orbit lemma are used.
- AssembledSizes.lean and AssembledSizes.lean.log: Lean 4.24.0 core, omega, axioms at most [propext, Classical.choice, Quot.sound], no sorry. Proves the half-turn (17 pairs, n >= 34), threefold, fivefold, both mirror and fourfold-via-half-turn bookkeeping for all n, with a control showing the half-turn bound fails at 32.
- c2_example_check.py, c2_example_controls.py and their logs: SYM2/sym7_32points.txt has 32 distinct points, is half-turn invariant about (0,0), does not contain the centre, has 0 collinear triples and has largest convex subset 6. The exact DP matches brute force on 260 random sets; a mutated DP is caught on 164 of 200 sets; convex 7- to 12-gons are recognised.
- status.log: last change to SYMMETRIC.md was de02b4914 (2026-10-30) and to the tex note a49b92d6d (2026-10-29). C4CUT (755081b76) and C2FINAL (9cf4949a5) are from 2026-11-01. The live re-solve of P8_1-10 was still running at 2026-11-01T12:35Z.
- SHA256SUMS.txt lists hashes of all outputs.

### A1-F2 (minor): Fourfold dependency: redundant for the main claim, but cited to a source whose rigor the repository itself disputes

Cor. 3 and the tex corollary assume 'the published fourfold exclusion (arXiv:2506.00224 §6.2)', and prop:C credits N(C4)=28 to it. C4CUT/README.md says that paper's final unrealizability step rests on a heuristic realizer failing. SYM5/README.md §4 instead describes an exhaustive enumeration with no realizable inner 12 points, so the repository contradicts itself. For the >= 33 claim the fourfold case is not needed: a fourfold set is centrally symmetric with size 4k >= 36, so C2-34 applies. The fourfold 32-point exclusion is needed only for the table entry N(C4)=28, which should cite C4CUT. C4CUT/README.md still says 'An independent review is pending' and 'conditional on the encoder review above', but C4CUT/review/README.md records a completed review with no blocking or major finding.

*Evidence.* SYMMETRIC.md lines 59-60, 81; tex lines 122-123, 166; C4CUT/README.md lines 10-14, 81; C4CUT/review/README.md; SYM5/README.md lines 124-128

*Suggested fix.* Drop the fourfold assumption from the main theorem. Cite C4CUT, with SMQH25 credited for the statement, as the basis of N(C4)=28. Fix the 'review pending' wording in C4CUT/README.md and reconcile SYM5 §4.

**Independent check:** real = yes; severity minor -> **minor**.

The finding is correct, and minor is the right severity. It is a documentation and citation problem. The fourfold exclusion it depends on is supplied by the repository's own certificate, C4CUT, so no mathematical claim fails.

1. **Citations.** The cited lines say what the auditor reports. SYMMETRIC.md lines 59-60 and 81, and tex lines 122-123 and 165-166, base Cor. 3 and N(C4)=28 only on arXiv:2506.00224 §6.2. The same reliance appears in places the auditor did not cite:
   - tex abstract (lines 21-23), intro (line 37) and lines 249-251;
   - SYMMETRIC.md lines 200-202;
   - SYMZ/README.md lines 82-85;
   - SYMMAX/README.md line 12;
   - SYM2/README.md lines 13-20;
   - LIT/RELATED.md lines 98-100;
   - WRITEUP/MIRROR.md line 84.

   No write-up file references C4CUT, and CERTIFICATES.md does not list its archive.

2. **What the source says.** I downloaded the paper; v1 is the only version. Its §6.2 says the authors attempted realizations "using heuristics", the inner 12 points "were never realizable", and the six inner patterns are such that "none of those are realizable". It never says how that last fact was established. Footnote 2 of §6.1 says the realizer "can only determine realizability, not unrealizability". The paper's public code repository has no 32-point or 7-gon files and no certificates. So no verifiable proof of the last step exists in the source, and the repository is right to question it.

   C4CUT's sentence "rests on a heuristic realizer failing" goes slightly beyond the text, which leaves the method unstated. The repository's older note docs/RELATED_WORK_2026-10-14.md (lines 568-571) words it accurately.

3. **SYM5 inconsistency.** SYM5 §4 (lines 123-134) says the authors found that none of the inner 12-point configurations is realizable. It says the exclusion "rests on the enumeration" and that "the abstract route fails". The first two statements conflict with C4CUT's view of the source's rigor. The third is outdated, because C4CUT closes the abstract route with six cuts. C4CUT/review/README.md item 5 already records that SYM5 §4 is waiting for an update.

4. **Stale wording in C4CUT.** C4CUT/README.md lines 13-14 say "no independent review" and "An independent review is pending", and line 81 says "conditional on the encoder review above". The review is recorded with the verdict "No blocking or major finding". Git shows that the review commit, 755081b76, edited C4CUT/README.md (it added the map hash and reworded the "match" claim) but left those lines unchanged.

5. **Redundancy for the 33-point claim.** I checked this by argument and by script for orders up to 60 and sizes up to 600. A fourfold rotation squared is the half-turn, so a fourfold set has size 4k >= 36, and 17 of its antipodal pairs give a C2-34 instance. With C2-34, the fourfold result is redundant for every n >= 33.

   One refinement: C2FINAL/README.md says C2-34 is "not yet claimed". Without C2-34, the fourfold 32-point result is exactly what excludes order 4 (sizes 36, 40, ...) in Cor. 3's "exactly C2". SYM2's statement that 2 is the largest rotation order for a 32-point set also uses it. So "needed only for N(C4)=28" is true only once C2-34 holds. For now, Cor. 3 should be re-based on C4CUT, not stripped of the fourfold assumption. For N(C4)=28 the 32-point result is indispensable only at n = 32.

6. **C4CUT checked as a replacement basis.** I re-checked its six cuts with my own verifier, written from scratch:
   - the map is consistent with the rotation, and its variable classes are exactly the rotation orbits;
   - each clause's variables are exactly the 55 inner orbit variables;
   - every minority term was recomputed independently, and the weighted exponents cancel exactly;
   - all 282 mutations were rejected;
   - the map hash f72b186e matches the README.

   I did not replay the 1 GB LRAT proof (the audit rules' resource limits) or re-derive the encoder's soundness. C4CUT is therefore a sound basis for N(C4)=28, given the encoder review and the recorded checker verdicts.

*Verifier's evidence.* Paper text (arxiv.org/html/2506.00224v1, sha256 55b82919...): §6.2: "We attempted to realize several of them using heuristics ... the inner 12 points were never realizable. Afterwards we observed that all 310 million solutions have only 6 different configurations to the inner 12 points and none of those are realizable." §6.1 footnote 2: "The realizer tool can only determine realizability, not unrealizability." The public repository bsubercaseaux/automatic-symmetries (19 files) has only 16-point experiments.

Repository at 9cf4949a5:
- C4CUT/README.md lines 10-14 and 81 as quoted.
- SYM5/README.md lines 123-134.
- SYMMETRIC.md lines 59-60, 81 and 200-202.
- tex lines 21-23, 37, 122-123, 165-166 and 249-251.
- C2FINAL/README.md: "not yet claimed".
- git show 755081b76: README edited, pending lines untouched.
- C4CUT/review/README.md item 5.

My outputs, in AUDIT3/A1_reduction/verify_A1-F2/:
- source_check.log: verbatim excerpts and the code repository's file list.
- fourfold_role.py and fourfold_role.log: with C2-34, nothing needs C4-32 for n >= 33. Without C2-34 and C4-32, orders {2,4} survive. For N(C4) the only gap is n = 32.
- my_check_c4cuts.py and my_check_c4cuts.log: all six cuts are valid and 282/282 mutations were rejected.
- SHA256SUMS.txt.

### A1-F3 (minor): The affine-symmetry extension is a single unproved sentence

SYMMETRIC.md line 72 assumes the group is finite; the tex note does not mention affine symmetries at all. Missing steps, each checked by A1 and correct: (a) the affine symmetry group acts faithfully on S, since S spans the plane, so it is finite; (b) affine maps fix the centroid; (c) averaging gives T with TGT^-1 in O(2); (d) a finite-order linear map with det -1 is conjugate to a reflection, and one with det +1 to a rotation; (e) T preserves general position and convex position, so the case theorems apply to T(S) and 7-gons pull back to S. Exact check: enumerating all affine symmetries of the integer-coordinate examples found only centroid-fixing maps with an invariant averaged form, including the genuinely non-orthogonal Eisenstein-coordinate rotations.

*Evidence.* WRITEUP/SYMMETRIC.md line 72; A1_reduction/examples_check.log, affine_controls.log

*Suggested fix.* Add a short paragraph with (a)-(e) to both documents, and define 'symmetry' in the theorem statement as an isometry or affine bijection g != id with g(S) = S.

**Independent check:** real = yes; severity minor -> **minor**.

The finding is correct, and its rating of minor is right, at the low end. Both factual claims hold.

(1) SYMMETRIC.md line 72 is the only argument for the affine case: "The same holds for affine symmetries, after a change of inner product that makes the finite group orthogonal." It assumes finiteness without proof. Line 66 ("A finite symmetry group fixes the centroid") also assumes it. MIRROR.md §2 (lines 92-95) proves finiteness, but only for isometries.

(2) The tex note never uses "affine", "isometry" or "inner product", and neither does the compiled PDF text. It never defines "symmetry". Its sentence at line 45 ("The symmetry group of a finite set fixes its centroid, so it is a cyclic group C_s of rotations or a dihedral group") is true for isometries. For affine maps it holds only up to conjugacy. Example: if the Eisenstein pairs of c3_31points.txt are read as Cartesian coordinates, the affine group is C3 but contains no Euclidean rotation.

The missing steps (a)-(e) are all mathematically correct, so the affine extension is true and the claim is not threatened. There is an even shorter complete proof that needs neither averaging nor finiteness. Let Σ = Σ_p (p−c)(p−c)^T. It is positive definite because S spans the plane. Every affine symmetry x -> c + L(x−c) satisfies LΣL^T = Σ, so Σ^{-1/2} conjugates the whole group into O(2). Finiteness also follows from the faithful action on S. A linear bijection preserves general position and convex position. The repository already relies on this for Eisenstein coordinates and proves it in Lean as convexPosition_of_image_affine / hasConvexNGon_of_image_affine.

The Lean mirror statement MirrorExclusionLine covers only Euclidean reflections (unit direction). So oblique reflections are covered only by the one-sentence remark. That makes it a real but small gap in the write-up, fixed by two or three sentences. In the tex note, the needed fix is to define "symmetry" (as an isometry, or explicitly as an affine bijection); adding the affine extension there is optional. The auditor's computational evidence reproduces exactly with independent code.

*Verifier's evidence.* Documents checked (read-only), paths under R = results:
- R/WRITEUP/SYMMETRIC.md line 72: the text quoted in the reasoning. Line 66 also assumes finiteness.
- R/WRITEUP/MIRROR.md lines 92-95: proves finiteness for isometries only.
- Grep for "affine" over every .md and .tex file in R: the only statement about affine symmetries of the set is SYMMETRIC.md:72. The other hits are coordinate changes inside encodings and the Lean pullback lemmas in V1-L and H3.
- symmetric_es7.tex, and the pdftotext output of the compiled PDF: no "affine", "isometr" or "inner product" anywhere.

Own exact check, no A1 code reused: AUDIT3/A1_reduction/verify_A1-F3/verify_affine.py, log in verify_affine.log in the same folder (run: 30.5 s, 32 MB).

Method:
- Enumerates every affine bijection with g(S) = S by trying all images of an affine basis.
- Does not assume the centroid is fixed, that the order is finite, or that |det| = 1.
- Uses Fractions for the integer files. The fivefold file is mapped to (Re z, Im z / sin72) in Q(sqrt5)^2 and enumerated directly; A1 handled that file by an argument instead.

Results:
- Groups found: C3, C4, C5, C6, D1 (no points on the axis) and C2, matching the A1 logs.
- In every example, every element:
  - fixes the centroid;
  - has det ±1;
  - satisfies L Sigma L^T = Sigma.
- In every example, the averaged Gram matrix is invariant and the maps are closed under composition.
- Every det −1 element is an involution with trace 0. Every det +1 element of order k has trace 2cos(2πj/k).
- The C3, C5 and C6 groups are not orthogonal in the file coordinates; a float whitening check (illustration only) gives an orthogonality error ≤ 4.5e-16.

Controls, all passed (ALL_OK true):
- Random non-orthogonal integer affine images give the same group, with chirotope equal to sign(det) times the original on every triple.
- Regular hexagon: D6, order 12. Regular pentagon: D5, order 10. Square: D4, order 8.
- Sheared mirror_32: D1 with an oblique reflection.
- Three random 14-point sets: trivial group.

Checksums: SHA256SUMS.txt in the same folder.

### A1-F4 (note): The overall claim depends on C2-34, which C2FINAL does not yet claim

At repository snapshot 9cf4949a5, C2FINAL/README.md says the C2-34 statement is not yet claimed: 21/24 main sample units and 8/8 extra units were done. The live run directory, outside the repository, shows two of the three missing Q units, P6_9-11 and P7_1-15, re-solved and accepted by both checkers (resolve/repro3b.jsonl). P8_1-10 was still running at about 21:24. The reduction itself has no gap. Until C2FINAL releases its claim, the overall theorem should be described as conditional on C2-34.

*Evidence.* C2FINAL/README.md lines 5-7, 93-99; C2FINAL/sample/out.jsonl (23 lines); <night run>/repro3b.jsonl

### A1-F5 (note): Minimal set of case theorems and which theorem each size needs

Necessary and sufficient: C3-33, C5>=35, M33, M34, C2-34, plus the regular-orbit lemma. Dropping one leaves the first uncovered case at C2/34, C3/33, C5/35, mirror b=1/33, mirror b=0/34 and C11/33 respectively. Fourfold and sixfold arguments are redundant once C2-34 holds. The fourfold result is still needed for N(C4)=28 (C2-34 gives only <= 32). N(C6)=30 follows from either C3-33 or C2-34. By size: n=33 needs only C3-33 and M33; n=34 needs C2, C3, M33, M34; n=35 needs C5 and M33.

*Evidence.* A1_reduction/size_arith.log (dropping_each_minimal_theorem_first_uncovered, redundancy, non_elementary_theorems_touched_per_size)

### A1-F6 (note): Case-theorem interfaces verified, including centre and axis status and implicit encoder preconditions

C3FINAL: 33 points, 11 orbits, c not in S, rotation by +120 deg; the reduction supplies this, and the 3k+1 sizes drop the centre. C3a/C3-S state their perturbation assumption (no two points collinear with c) in one sentence; the SYM5 §1 argument applies verbatim. SYM5 covers >= 35 with the centre allowed and supplies its own reduction and perturbation. C4CUT: 32 points; even order, so no centre and no perturbation needed. C2: 34 points; the encoder's zero triples are exactly {c,p,-p}, since a line through c holds at most one antipodal pair. SYMZ: 2a is exactly one axis point and 2b is none. The normal-form units (distinct pair heights) hold by general position. MIRROR.md's Lean statement (card 33, any line) is equivalent to 2a.

*Evidence.* C3FINAL/README.md line 37-38; C3-S/soundness.md lines 3-5; C3a/README.md lines 27-29; SYM5/README.md §1; SYMZ/zcnf.py docstring and add_sb; C2C34/README.md §1; MIRROR.md §1

### A1-F7 (note): Size table re-derived; example files checked; each example has exactly the listed symmetry group

Upper bounds are Lean-checked from the case theorems. The cited files exist with sizes 31/28/31/30/32/32. They are invariant under the stated symmetry, the centre is present only in the C3 and C5 examples, the mirror example has 16 pairs and no axis point, and no three points are collinear. Full symmetry groups: C3, C4, C5, C6, D1, C2. The entries therefore hold whether N(Gamma) means 'invariant under Gamma' or 'symmetry group exactly Gamma'. N(C2)=32 is conditional on C2-34, and N(C4)=28 on C4CUT. A1 did not check freedom from convex 7-gons.

*Evidence.* A1_reduction/examples_check.log, c5_group.log, SizeArith.lean

### A1-F8 (note): Small imprecisions in the lemmas

(i) tex line 45: 'the symmetry group of a finite set fixes its centroid, so it is cyclic or dihedral' fails for |S| <= 1, where the group is O(2). (ii) Lemma sizes(a): 'S != {c}' should read 'S not contained in {c}'. (iii) Lemma sizes(b) needs only |S| >= 2. (iv) In lem:layers, m >= 4 is unnecessary; K <= 2m suffices. (v) In the SYMMAX table, the row 'order 7 or more: N = none' should be N = 1 for odd order (the centre alone) and 0 for even order. (vi) prop:C should define 'with symmetry Gamma'. (vii) SYMMETRIC.md Theorem 1 says 'rotation of order 3' while C3FINAL says '+120 deg'; these are equivalent (same group), but worth stating.

*Evidence.* note/symmetric_es7.tex lines 45, 50-52, 135, 158; SYMMAX/README.md table

### A1-F9 (note): Stale status statements elsewhere in the repository

MIRROR.md §1 still says the class of sets invariant under a 120 deg rotation is open, which C3FINAL supersedes. SYMZ/README.md §5 and C2C34/README.md still say the central case is open. SYMMAX/README.md says centrally symmetric sets of 34 or more points are not excluded. Update these together with A1-F1.

*Evidence.* WRITEUP/MIRROR.md lines 52-58; SYMZ/README.md §5; C2C34/README.md 'Status: open'; SYMMAX/README.md lines 46-47

## Tests run by the auditor

- python3 -I A1_reduction/size_arith.py 600 60: ALL_OK. Exhaustive over n=33..600 and orders s=2..60: no uncovered case with the minimal set; Cor. 3 residual is exactly even C2 >= 34; each minimal theorem is necessary; C4 and C6 redundant given C2-34; table N = C2 32, C3 31, C4 28, C5 31, C6 30, mirror 32 (log: size_arith.log)
- lean SizeArith.lean (core Lean 4.24.0, ~340 MB RSS): 20 theorems proved for all n with omega/decide; #print axioms shows only propext/Classical.choice/Quot.sound; no sorry or admit (log: SizeArith.lean.log)
- python3 -I A1_reduction/examples_check.py <results>: ALL_OK. Exact checks of the 6 example files (size, distinctness, invariance, fixed points, no 3 collinear) and full affine symmetry group enumeration for the 5 integer-coordinate files (log: examples_check.log)
- python3 -I A1_reduction/affine_controls.py: CONTROLS_OK (regular hexagon D6, square D4, affine image of a square D4, random 12 points C1)
- python3 -I A1_reduction/c5_group.py SYMMAX/c5_31points.txt: full symmetry group exactly C5, exact arithmetic in Z[zeta5], with controls
- Read and grep of WRITEUP/SYMMETRIC.md, note/symmetric_es7.tex, C3FINAL/README.md, C3-S/soundness.md, C3a/README.md, SYMZ/README.md and zcnf.py, SYM5/README.md and symcnf.py docstring, C4CUT/README.md and review/README.md, C2FINAL/README.md and sample/*.jsonl, C2C34/README.md, SYMMAX/README.md, MIRROR.md §1, LIT/RELATED.md §3
- Read-only look at live run directory/resolve/*.jsonl and the process list for the status of the C2 sample


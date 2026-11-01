# A2: threefold 33 (Theorem 1)

Component audit, 1 November 2026 (UTC), against `es7-cloud` at 9cf4949a5. Texts returned by the auditor and by the independent verifier of each finding, lightly edited: machine paths replaced by placeholders and internal job names by descriptions; trust-table labels as explained in `../README.md`, §7.

**Component.** THREEFOLD 33 (Theorem 1): every 33-point set in general position invariant under a rotation of order 3 contains a convex 7-gon (C3a chain encoding + C3-S normal form + Lemma H6M + sigma-cube refinements; 116,883 certified pieces; C3FINAL composition; C3SPOT spot check)

**Statement audited.** Encoded statement: for m = 11, k = 7, every node CNF = base CNF (c3cnf.py 11 7 chain, header p cnf 168399 4154921, sha256 bf0e502e...dd6da) + the node's unit clauses (layer units, sigma units, cube units). The claim is that the certified UNSAT pieces form a cut of the reduced layer tree. The tree is: root -> 11 top cases (H3, H6(a,s), a = 1..5); H3 -> 100 of 190 layer-2 options (Lemma 5); each H6(a,s) -> 81 of 153 options (Lemma H6M); depth >= 2 -> all next layers, with sigma splits and rule-3 cube layer splits. Together with the normal-form lemmas this implies that no 3-fold 33-point set in general position without a convex 7-gon exists. Write-up claim (SYMMETRIC.md Theorem 1, C3FINAL): 116,883 certified records over 116,741 nodes, all CNF hashes re-derived, all 910 depth-2 roots covered by two composers, proofs not retained, 26,436 records carry a proof SHA-256, and a 2,120-piece random re-solve passed.

**Verdict.** `sound_with_caveats`

## Summary

Verdict: sound with caveats. I found no logical gap. The main caveat is about evidence: every piece's UNSAT verdict was recorded at solve time and its proof deleted, so it cannot be re-checked now.

(1) Encoded statement and soundness. I re-derived the C3a identities and the chain encoding in both directions, Lemmas 1-5, Lemma H6M and the sigma-split rules, and found them correct. Three small imprecisions:
- The distinct-x WLOG step is used but never stated (F3).
- The symmetric perturbation is asserted without proof (I checked it constructively on the sixfold set).
- The C3a README names the wrong direction of the chain argument as the one soundness needs (F4).

(2) Cover. My own composer (its own parser, unit generator, mirror maps and sha re-derivation from a regenerated base) agrees with the records:
- It reproduces 116,883 records, 116,741 nodes and 26,748 cube nodes, with 0 hash mismatches.
- It finds the class covered and all 910 roots covered, with one explicit cut of 73,567 pieces.
- All 11 tampering tests make it report the class uncovered.
- Both mirror reductions are load-bearing.

(3) Replayability. No threefold proof is retained. Only 26,436 records (34% of the cut) carry proof hashes. The spot check is genuine: the first 2,120 rows of the shuffled sample, all passing, hashes matching mine, 480/485 identical proofs. But it re-verified only 1,337 cut pieces, and it excluded 396 nodes that the cover needs (F2).

(4) Encoding tests. My exact-integer evaluator found 0 failures over 1,630 cases. That includes 1,155 k-gon-free sets, among them the 7-gon-free 27- and 30-point sets and 840 orbit-deleted subsets of them, plus m = 11 sets at k = 8 and 9. The k = 7 gon clauses can only be tested on in-class sets up to m = 10.

Residual risk is mainly isolated bad records among the roughly 72,000 cut pieces that were never re-verified (F1, rated major), plus the written, not Lean-checked, soundness proofs (F5, F6). What would reduce it most: re-solve and re-check one cut on independent hardware (about 1,750 core-hours from the recorded times) and keep compressed proofs or hashes; then Lean-formalize the base encoding, Lemma 5 and H6M.

Files are in AUDIT3/A2_threefold/. The main scripts are a2compose.py, indep_eval.py, gen_base_stream.py and check_spot.py. The cut list is in logs/a2compose_report.json.

## Trust table

| # | claim | basis | notes |
|---|---|---|---|
| 0 | Reduction: a threefold set with >= 33 points contains a 33-point threefold set without the centre (orbits have size 3 except the centre; 33 = 0 mod 3, so c is not in S; 32 points impossible) | written proof, re-derived by the auditor | Trivial counting; R and R^-1 give the same class. |
| 1 | WLOG genericity: an R-equivariant perturbation keeps the order type and removes collinearities with c; l can be chosen in its gap so that no segment of S is parallel to l (distinct x) | written proof, re-derived by the auditor | The perturbation is only asserted in the sources. The distinct-x step is not stated at all (finding F3). I checked the perturbation constructively on SYMMAX/c6_30points: all 4,060 triple orientations kept and no pair collinear with c. |
| 2 | C3a base encoding is sound: identities 1-5 (labels, R(i) = i - m, chi_S = chi' * (-1)^(sum sigma), the eps rule, the sigma orbit pattern, the inv/x-order rule, the prefix and forced rules, sb), the parity definitions, and the chain gon encoding (with least-fixpoint Y/W, a 7-gon-free set satisfies every gon clause) | written proof, re-derived by the auditor | I re-derived every identity and both directions of the chain argument. My own exact-integer evaluator found 0 failures: 1,155 k-gon-free sets (2,310 frames) satisfied every clause, including 4 near-extremal 7-gon-free SYMMAX sets at m = 9, 10 and 840 orbit-deleted in-class subsets at m = 5..9. Each variable's orbit map was checked for consistency against true values in every frame. Not Lean-checked (C3L is a generator only). |
| 3 | The base CNF used by every record is exactly c3cnf.py 11 7 (sha bf0e502e...) | exact computation (auditor's full regeneration) | I regenerated it by streaming with the byte-identical vendored c3cnf.py: header p cnf 168399 4154921, sha256 matches. The C3L Lean generator is also documented as byte-identical. |
| 4 | Lemmas 1-4: angular order is the (sigma, label) order; WLOG label 0 on the hull, sigma_0 = 0, a <= 5, 11 top cases; layer units ccw(u,v,w) for every ccw-consecutive layer pair against all later points; every layer is 1 or 2 orbits and layer2_options lists every next layer | written proof, re-derived by the auditor | I re-derived the hull orders H3: 0,2m,m; H6(a,0): 0,a,2m,a+2m,m,a+m; H6(a,1): 0,a+m,2m,a,m,a+2m. 2,585,438 node-unit evaluations on true assignments were all true. Every observed layer path was a path of the unreduced tree, and canonical paths were unique for odd m. |
| 5 | Lemma 5 (H3 mirror: (r,s) -> (m-r, 1-s)) and Lemma H6M (phi_{a,s}(r,s) = ((a-r) mod m, s xor [r<a] xor [s0=0])); keeping one member of each pair covers the class | written proof, re-derived by the auditor | I derived the H6M sigma term independently before reading C3H6M, and checked that it is an involution: 81 pairs and 9 self-paired per H6 case; 100 pairs and 10 self-paired for H3. The mirror path prediction held for all layers on 1,445 sets; a mutation without the sigma flip was caught on 761 sets. Both reductions are load-bearing (F6). |
| 6 | Sigma-split (rule 2) and cube layer split (rule 3) are complete covers; a childless node is covered only if certified | written proof, re-derived by the auditor | My own composer uses single-bit sigma splits on any free residue, which compose to any K-bit split, and rule-3 splits with conflict dropping. It never covers through an empty child list. The C3AUDIT3 childless-node bug is fixed in the C3U2 compose.py used by C3FINAL. |
| 7 | Every certified record's CNF = base + units(name): 116,883 records, 116,741 nodes, 26,748 cube nodes | exact computation (auditor's full recomputation) | Full independent recomputation (a2compose.py): 0 hash mismatches. My unit generator agrees with hullcase.node_units on all 116,741 names, and every record's 'units' field matches. Category chosen as closest available: this is a complete recomputation, not a sample. |
| 8 | The certified nodes form a cut of the reduced tree (class covered; all 910 recorded roots covered) | exact computation (auditor's own composer) | My composer (own parser, tree, phi maps, pair-based mirror rule, own sha derivation) finds class_covered = true and all 910 roots of C3FINAL_mirrorh6_roots.tsv covered. One explicit cut has 73,567 certified nodes. 11 of 11 tampering tests (drop a record, alter cnf_sha256, alter the cake_lpr string, rename the node) made it report 'not covered'. |
| 9 | Each of the 73,567 pieces in the cut is UNSAT (CaDiCaL LRAT proof accepted by lrat-check E2 and cake_lpr at solve time) | recorded verdict only (proofs not retained) | Proofs deleted and none archived. 72,230 of the cut pieces rest only on the recorded strings. 24,733 carry a proof SHA-256, which cannot be checked without re-solving. No record in the set shows a checker rejection: the 26 uncertified UNSAT records are cake_lpr OOM ('none'), all later re-certified. |
| 10 | Random re-solve: 2,120 pieces re-solved from scratch, fresh proofs accepted by both checkers, CNF hashes match | project's re-solve sample (records checked by the auditor, not re-solved) | I did not re-solve; node CNFs are about 110 MB, above the solve limit. I verified the records: the 2,120 are exactly the first 2,120 rows of the shuffled 3,084-row sample, all pass, and all CNF hashes equal my own derivation. 1,337 of them are in my cut. 480 of 485 with recorded proof hashes reproduced the identical proof. The population excluded 396 sigma_cubes-format nodes the cover depends on (F2). |
| 11 | LRAT checkers are sound (cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch); CaDiCaL is only untrusted search | argument only | External trust base: cake_lpr is CakeML/HOL4-verified (not Lean). The archived arm64 cake_lpr (sha 2fee767a...) contains no x18/w18 instruction (Apple reserves x18). |
| 12 | Theorem 1 second sentence: the largest threefold set without a convex 7-gon has exactly 31 points | exact computation (lower bound) and counting from Theorem 1 (upper bound) | My exact DP (self-tested against brute force on 299 sets) on SYMMAX/c3_31points: 31 points, rotation-invariant, no 3 collinear, largest convex subset 6. The upper bound is Theorem 1 plus 32 = 2 mod 3. |

## Findings

### F1 (major): Piece verdicts are recorded only and not replayable: proofs deleted, 98% of an explicit cut never re-checked

The cover logic is sound and holds given the records, but the UNSAT fact for each piece now exists only as a recorded checker string. No threefold proof is archived (proof-archives/es7-symmetry has only c3hex k=6 files). In one explicit cut of 73,567 pieces, 72,230 were never re-verified. Only 24,733 cut pieces (34%) carry a proof SHA-256: hashes exist only from C3W4 onward, and C3WAVE1/2, C3W3, C3S0, C3SIG/SIG2 and C3W3S records have none. A hash cannot recreate or verify a proof without re-solving. The 0/2,120 spot check bounds a systematic error rate (about 0.14% at 95%) but cannot exclude isolated bad records, and soundness needs every cut piece correct. I found no evidence of any bad record: 0 hash mismatches, 0 checker rejections, and the spot check is consistent. The write-up (SYMMETRIC.md section 3) discloses this as 'recorded historical verdicts (not replayable now)'. Rated major because a publishable 'theorem' should rest on re-checkable certificates, and the remedy is concrete and affordable.

*Evidence.* logs/a2compose.log (116,883 certified records, 26,436 with proof_sha256); logs/a2compose_report.json 'cut' (73,567 names). From the recorded times, the cut costs 1,266 core-h solve + 476 core-h check and about 10.5 TB of ASCII LRAT; all certified records together cost 1,472 h + 697 h and 13.4 TB.

*Suggested fix.* Re-solve every piece of one cut (list in logs/a2compose_report.json) on independent hardware with the recorded options, about 1,750 core-h. Check each proof with cake_lpr, keep zstd-compressed (preferably binary) LRAT or at least the proof hashes, then re-compose. Alternatively, Lean-formalize the soundness, or find an encoding that closes the class with a few retained certificates (as SYMZ did for the mirror case).

**Independent check:** real = yes; severity major -> **minor**.

The facts in F1 are correct. I recounted every number with my own code, which does not import the auditor's scripts.
- No threefold k=7 proof is kept anywhere. The archive has only the c3hex k=6 proofs, its MANIFEST lists the threefold case under "Not in this archive", and a search of the local disk and scratch areas found no other LRAT files.
- The cut has 73,567 names. Every one has a certified record, and 24,733 of them (33.6%) carry a proof hash.
- Proof hashes appear only in C3W4–C3W7, C3H1 and C3COMP1. C3WAVE1/2, C3W3, C3S0, C3SIG/SIG2 and C3W3S have none.
- 1,337 cut pieces were re-solved in C3SPOT, so 72,230 (98.2%) were never re-verified.
- Recorded cost of the cut: 1,266.4 h solve, 476.2 h check, 10.46 TB of LRAT. All certified records: 1,471.9 h, 696.7 h, 13.42 TB.
- 480 of 485 re-solved proofs are bit-identical to the recorded hash. The rule-of-three bound is about 0.14%.

I rate it minor rather than major for these reasons.

(1) There is no logical gap, and nothing is overclaimed. The project already states this limitation in SYMMETRIC.md §1 and §3, in CERTIFICATES.md (which has a regeneration plan) and in the MANIFEST.

(2) The evidence that the records are genuine is much stronger than the sampling bound the finding relies on:
- All five scripts that wrote records do the same thing: write the CNF, hash that exact file, solve, run both checkers on that CNF and proof, and mark the piece certified only on the exact checker strings.
- Both composers re-derive every CNF hash from the node name, so each record is tied to the right formula.
- The pipeline handles failures safely. There are 26 UNSAT records where cake_lpr printed nothing; all 26 were recorded as not certified and were re-certified later, with the same proof size.
- 2,107 of the 2,120 re-solves reproduced the original record's exact proof size, including 1,635 records that have no proof hash. So the sampled records come from real solver runs.
- Timings are plausible across all 116,883 records. The fastest combined check rate is 36 MB/s, against 35 MB/s measured in the spot check on this Mac.
- 116,874 records carry the field layout of one of the record-writing scripts. Only 9 are re-check records with notes added by hand.

(3) For a piece that is actually satisfiable to be recorded as certified, CaDiCaL would have to report UNSAT wrongly and the record would also have to be corrupted or fabricated, since cake_lpr is formally verified.

(4) The pieces can still be replayed by re-solving, which is deterministic. Re-solving costs about 3.7 times as much as re-checking a stored proof, but that is a difference in cost, not in principle.

(5) Large SAT results are commonly accepted on proofs checked by a verified checker when they were generated and then not kept, provided this is disclosed.

Where the finding is imprecise:
- "Not replayable" and "never re-checked" overstate things: every piece was checked by both checkers when it was solved.
- The 34% hash coverage does not matter for soundness, as the finding itself says.
- The summary's "26,436 records (34% of the cut)" mixes up 26,436 records with 24,733 cut pieces.
- The 1,750 core-h figure comes from cloud times. On this Mac, solves ran at 0.64x and checks at 0.55x of the recorded times, so a local run would take about 1,000–1,100 core-h. That is about 64% of the whole recorded campaign (2,712 h), not a full campaign as CERTIFICATES.md suggests.

The finding leaves out two things that slightly raise the remaining risk:
- 39 lane directories (separate machines or sessions), holding 1,319 cut pieces, had no record re-solved at all.
- 340 cut pieces rest only on sigma_cubes.py-format records, which were outside C3SPOT's sample (this overlaps F2).

Recommendation: re-solve and check one cut, about 1,000–1,750 core-h, and keep the proof hashes or about 2 TB of compressed proofs. It is worth doing before journal submission, because the original runs were spread over many sessions. On the evidence, though, that missing check does not threaten the claim. Under the stricter rule the project applied when it replaced the mirror proof chain with a kept proof (SYMZ), this would sit at the minor/major boundary.

*Verifier's evidence.* Scripts and logs are in AUDIT3/A2_threefold/verify_F1/: f1_stats.py, f1_integrity.py, f1_lanes.py and f1_keyorder.py, each with a .log.

**Counts and cost (f1_stats.log)**
- 128,803 records; 116,883 certified records (116,741 nodes); 26,436 certified records with proof_sha256.
- The cut has 73,567 names, all with a certified record; 24,733 (33.62%) have a hashed record.
- Cost of the cut: 1,266.4 h solve, 476.2 h check, 10.46 TB. All certified records: 1,471.9 h, 696.7 h, 13.42 TB.
- C3SPOT: 2,120 rows, all pass; 1,337 lie in the cut, so 72,230 (98.18%) were never re-solved.
- 480 of 485 re-solved proofs have the original hash. The 5 that differ had a different -t cap or a different run.

**Record integrity (f1_integrity.log)**
- 26 UNSAT records have cake_lpr output 'none'. All are certified false, and all 26 nodes are certified elsewhere.
- Check rates: median 2.5 MB/s, maximum 36.1 MB/s.
- No certified record has a proof under 1,000 bytes or a zero solve time.
- 142 nodes have duplicate records; their CNF hashes all agree.
- 67 of 236 contributing record files have no re-solved cut piece (1,899 pieces).

**Lane coverage and timing (f1_lanes.log)**
- 39 of 229 lane directories had no record re-solved at all; they hold 1,319 cut pieces.
- 2,107 of 2,120 re-solves reproduced the original proof size exactly.
- On this Mac, re-solves took 0.64x and checks 0.55x of the recorded times (f1_stats/f1_lanes runs; spot 22.9 h solve vs 31.4 h originally).

**Field layout (f1_keyorder.log)**
- 116,874 records match one of four layouts written by the record scripts; 9 are re-check records with notes added by hand.
- 21 cut pieces rest only on rare layouts: 17 from close_node.py and 4 annotated re-checks.
- 340 cut pieces rest only on sigma_cubes.py-format records, which C3SPOT did not sample.

**Archive and project documents**
- <proof-archives>/es7-symmetry/MANIFEST.md, "Not in this archive", lists the threefold 33 case. A find for *.lrat* turned up no threefold k=7 proof.
- Every record-writing script hashes the CNF file the checkers read and requires exact strings from both checkers: R/C3-S/tools/close_tree.py (solve(), lines 42-73), R/C3-S/tools/controls.py dual(), R/C3PLAN/scripts/sigma_cubes.py, R/C3-S/tools/close_node.py, and R/C3U2/tools/close_tree.py, which adds proof_sha256.
- The project already discloses all this: R/WRITEUP/SYMMETRIC.md §1 and §3 ("Recorded historical verdicts (not replayable now)"), and R/WRITEUP/CERTIFICATES.md (the threefold section and its regeneration plan).
- The whole recorded campaign took 2,712 h, including 543 h of timeouts.

### F2 (minor): Spot-check population excluded 396 sigma_cubes-format nodes on which the cover depends

C3SPOT drew only from nodes with a plain-format certified record (116,345). 396 nodes exist only as sigma_cubes.py-format records (C3SIG 160, C3W3S 144, C3SIG2 92), and 340 of them lie in my explicit cut. Re-running my composer without those records gives class_covered = false with 5 open H3 mirror pairs. These pieces therefore had zero chance of being re-verified, and the 'random subset of the certified pieces' wording overstates how well the sample represents the cut.

*Evidence.* logs/a2compose_skip_cubefmt.txt ('0s0 ... open pairs: 5'); population counts computed from units6.tsv vs the 280 record files.

*Suggested fix.* Re-solve the 396 nodes (direct solves took about 60-300 s, so roughly 35 core-h). In future samples, draw from the cut rather than from record files.

**Independent check:** real = yes; severity minor -> **minor**.

The finding is correct, and it understates how far the cover depends on these pieces. Minor is the right severity.

What I re-checked:

(1) Population, with my own parser over the 280 files. There are 116,741 certified nodes. 116,345 of them have a plain-format certified record, which is exactly the C3SPOT population. 396 are certified only by sigma_cubes.py-format records: C3SIG 160, C3W3S 144, C3SIG2 92. All 3,084 rows of units6.tsv are plain-format nodes, and none is one of the 396. 340 of the 396 are in the auditor's cut (C3SIG 120, C3SIG2 92, C3W3S 128), and 1,337 of the re-solved spot rows are in that cut.

(2) Re-running a2compose.py with --skip-cube-format gives class_covered false and 5 open pairs at 0s0. But that run stops at the first failing top case. I also ran the project's own C3U2 compose.py, unchanged, with --mirror-h6 --no-sha, on copies of the records with the sigma-format records removed. It reports class_covered false with 1,384 uncovered frontier nodes. Both project composers find 22 of the 910 roots open: 5 under H3 and 17 under H6. The control run with all records leaves 0 open.

(3) Refinement:
- Removing only the C3SIG sigma records leaves the class covered. Those pilot nodes were also closed by layer splits, so C3SIG is redundant. The auditor's cut just happens to use 120 of them.
- Removing C3SIG2 opens 7 roots; removing C3W3S opens 15.
- Tested one node at a time, 204 sigma-only nodes (C3SIG2 84, C3W3S 120) are each indispensable: removing any single one makes the class uncovered.

(4) None of these load-bearing pieces has been re-solved anywhere in the results tree. The only reproductions of sigma-only pieces are of redundant C3SIG cubes (3 in C3AUDIT3, 16 in the C3U m11 tests). C3W4/O01 tried four of the indispensable C3SIG2 cubes on the identical CNF and timed out at 300 s, where C3SIG2 had finished in 220-252 s.

(5) Disclosure:
- The "Sample" section of the C3SPOT README does state that sigma-cube records are excluded.
- Its opening line ("A random sample of the certified pieces behind results/C3FINAL") and the write-ups do not: SYMMETRIC.md ("drawn at random", "6 per source directory"), CERTIFICATES.md and symmetric_es7.tex. C3SIG and C3SIG2 had 0 rows drawn.
- The regeneration plan in CERTIFICATES.md ("rerun close_tree.py on its node with the record's cadical_args") also does not fit these records: they have no cadical_args, and their "node" field is the parent node, not the cube node.

The auditor's quote is not verbatim (the README says "random subset of the sample"), but the point stands.

Why minor and not major:
- There is no logical gap. Every one of these records carries both checker verdicts from solve time.
- Both composers re-derive their CNF hashes.
- They come from the unmodified sigma_cubes.run with the same pinned tools and the same dual() checker wrapper, and that pipeline was reproduced on C3SIG cubes, three of them with proof sizes identical to the byte.
- The remaining risk is isolated bad records, the same class as F1. The difference is that 204 indispensable pieces had zero chance of being sampled.

The fix is cheap and should be done. From the recorded times, the 204 indispensable pieces need 8.0 h of solving plus 2.4 h of checking; all 396 need 15.5 h plus 4.7 h, about 20 core-hours. The auditor's 35 core-hours is an overestimate. The write-up wording should also be corrected.

*Verifier's evidence.* Scripts and outputs are in AUDIT3/A2_threefold/verify_F2/:
- count_pop.py -> count_pop.json: 116,741 certified nodes; 116,345 plain-format; 396 sigma-only (C3SIG 160 / C3W3S 144 / C3SIG2 92); units6 rows in sigma-only: 0; sigma-only nodes in the auditor's cut: 340; sigma-only solve times 9-289 s, total 15.48 h solve + 4.65 h check.
- a2_skipcube.out: the auditor's composer gives "0s0 ... open pairs: 5".
- compose_none.json / compose_all.json: the project's C3U2 compose.py, unchanged, --mirror-h6 --no-sha, on a base regenerated by gen_base_full.py (sha bf0e502e confirmed). All records: covered, 1,747 sigma splits. Without sigma-format records: class_covered false, 1,384 uncovered frontier nodes.
- roots_nosha.py -> roots_{none,all,C3SIG,C3SIG2,C3W3S}.json: open roots out of 910 are 0 / 22 / 0 / 7 / 15, and compose and mycompose agree on every root.
- necessity.py -> necessity_C3SIG2_C3W3S.jsonl: 204 of the 236 nodes are individually necessary.
- A search of the whole results tree for the sigma-only CNF hashes finds re-solves only for C3SIG cubes (C3AUDIT3/logs/resolve_*.jsonl, C3U/tests/logs/m11). C3W4/O01/out.jsonl shows UNKNOWN at 300.1 s on 4 indispensable C3SIG2 cubes.

Project documents:
- C3SPOT/README.md, "Sample" section: "Every certified record that is not a σ-cube record".
- WRITEUP/SYMMETRIC.md lines 157-160, WRITEUP/CERTIFICATES.md lines 210, 224 and 231, and note/symmetric_es7.tex line 75 do not mention the exclusion.

### F3 (minor): Distinct x-coordinates (no segment of S parallel to l) is used but not stated as a WLOG step

The B (x-order) and inv variables, and the prefix/forced/xorB clauses, assume all points have distinct x-coordinates in the frame of l. Neither C3-S/soundness.md nor the C3a README states this. C3a's validator redrew failing sets instead of moving l. It is trivially achievable: l can be rotated within its gap, which keeps labels and sigma. Lemma 5 and Lemma H6M re-choose l, so the same remark applies there. It does not affect soundness.

*Evidence.* results/C3a/README.md 'Validation': distinct x-coordinates are checked and failing sets redrawn; C3-S/soundness.md 'Normal form' paragraph; C3b DERIVATION.md mentions the issue only for the D3 variant.

*Suggested fix.* Add one sentence to the normal form: choose l generic inside its gap so that no two points of S share an x-coordinate.

**Independent check:** real = yes; severity minor -> **minor**.

The finding is partly correct. The verdict holds: the assumption is unstated, harmless, and fixable in one sentence. But the finding overstates which parts depend on it, and one detail about the validator is wrong.

WHAT IS RIGHT
(1) No threefold document says that l is chosen so that no two points of S lie on a line parallel to l. I checked:
- C3-S/soundness.md:7-10, the normal form;
- C3a/README.md:26-31, the setup;
- C3H6M/soundness_h6m.md;
- WRITEUP/SYMMETRIC.md and note/symmetric_es7.tex;
- C3PLAN/PLAN.md.
The only mentions are C3a README:84-86, which is about generating test sets, and C3b DERIVATION:56-64, which is about the unused --d3 variant.

(2) The written chain lemma does assume a strict x-order. With a tie, these sentences are false or ambiguous:
- C3a README:56-60: "leftmost vertex x (in the x-order of S, given by the literals B)" and "open half-plane right of x";
- c3cnf.py:17-18 and 28-31: "open right half-plane";
- C3b DERIVATION:43-45: "strictly to the right of p".
The project states and proves its tie step elsewhere (Caudit/README.md:50, the mirror case; H's DistinctXReduction). So by its own standard this is an omission.

(3) The proposed fix is valid. Turning l inside its gap changed no label, σ, chi', chi_S or layer path in any of 4,614 canonical gaps. inv and B did change in 24,209 frames. Lemmas 2(a), 5 and H6M pin l down only up to its gap, so the same remark covers them.

WHAT IS OVERSTATED
The encoding itself does not need the assumption. Only the prose relies on it. The base CNF is satisfied by the true assignment even when l is parallel to a segment of S. (I regenerated the base: p cnf 168399 4154921, sha256 bf0e502e…6cdd6da, the same as C3FINAL's. Its clause families are sig, sb, prefix, forced, xorB, xorT, Y, W and gon; xsig is off.)
- inv_ij = [1/x_i > 1/x_j] is well defined.
- A triple contains at most one tied pair; otherwise three points would lie on a line parallel to l. The strict-inversion pattern is still a prefix.
- The forced clauses only concern pairs with σ_i ≠ σ_j. Such points lie on opposite sides of l, so they never tie.
- xorB defines B. On a tie, B puts the larger label first, so B is the strict order by (x, −label).
- The gon direction that soundness needs is "a chain forces a convex k-gon". Every chain point p has B(x,p), so x_p ≥ x_x, with equality for at most one p (no three collinear points). So the chain lies in an open half-plane bounded by a line through x. Angles about x increase over less than 180°, and all turns are left. Together with x, the chain is a convex k-gon.

So it is wrong to say that the B/inv variables and the prefix/forced/xorB clauses "assume" distinct x.

The detail "C3a's validator redrew failing sets instead of moving l" is also wrong about the code:
- c3geom.frame (c3geom.py:119-129) picks a new direction for l when there is a tie; only the README sentence says that sets are redrawn.
- C3-S validate_hull.label_order (49-54) also rejects tie directions, and check_identities.py goes through the same frame code.
As a result, no project test ever exercised a tie.

MY CHECK
I used my own exact Eisenstein-integer geometry, with the encoder and unit generator copied byte for byte. In every canonical gap I placed l parallel to segments of S: first edges of a largest convex polygon and of the convex layers, then random segments. I also placed it once in a generic direction. On every frame I evaluated:
- all clauses of C3Enc(m,k);
- the layer units for every prefix of the true layer path;
- a transitivity condition that guarantees every chain is convex;
- that the longest chain plus 1 equals the largest convex subset.
Coverage: 27,024 tie frames, including 11,145 at k = 7 for sets with no convex 7-gon and 1,164 against the real m = 11 base. There were 0 failures. In 132 frames a strict x-order relation would miss the largest polygon, and the parity-defined B found it.

SEVERITY
Minor, as the auditor said. The claim is unaffected. Either one-sentence fix works: the auditor's genericity sentence, re-applied each time l is re-chosen, or a remark that ties are harmless.

*Verifier's evidence.* Documents (relative to R = results):
- No statement that l is generic or that x-coordinates are distinct: C3-S/soundness.md:7-10; C3a/README.md:26-31; C3H6M/soundness_h6m.md; WRITEUP/SYMMETRIC.md; WRITEUP/note/symmetric_es7.tex; C3PLAN/PLAN.md.
- Prose that assumes a strict x-order: C3a/README.md:56-60; C3a/c3cnf.py:17-18 and 28-31; C3b/DERIVATION.md:43-45.
- The only tie mentions: C3a/README.md:84-86 (test sets) and C3b/DERIVATION.md:56-64 (the --d3 variant).
- Contrast: Caudit/README.md:50, where the mirror case states, proves and tests its tie step.
- Lemmas that re-choose l: soundness.md:24-27 (Lemma 2(a)), soundness.md:66-68 (Lemma 5), soundness_h6m.md:32 and 39 (H6M).
- C3AUDIT2/REPORT.md:74-76 says the base's only WLOG constraint is sb.

Code:
- c3geom.py:119-129: frame() draws a new direction u for l when x-coordinates tie; the set is not redrawn. Labelled also asserts that inv and before are strict.
- C3-S/tools/validate_hull.py:49-54 rejects tie directions.
- check_identities.py uses Labelled.

My scripts are in AUDIT3/A2_threefold/verify_F3/: ties.py, prefix_ties.py, find_example.py, summarize.py, run_*.sh.
- vendor/: byte-identical copies of c3cnf.py (cf730939…) and hullcase.py (d393bdeb…).
- logs/basesha.json: vars 168399, clauses 4154921, sha256 bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da; xsig and acy off, gon chain.
- logs/summary_all.txt (from small.jsonl, big.jsonl, m11.jsonl):
  - 1,561 sets; 27,024 tie frames (27,088 tied pairs); 6,780 generic frames.
  - Encoder evaluations on tie frames: 62,979 across k = 5..8, of which 12,090 are for sets with no convex k-gon (11,145 at k = 7).
  - Unit clauses evaluated on canonical tie frames: 29.5M.
  - 132 tie-critical frames; 0 angular-order failures; FAILURES 0.
- Coverage:
  - random sets, m = 3..10;
  - SYMMAX c3_27points, c3_30points, and c3_31points without its centre (all 7-gon-free), with 40 tie directions per gap;
  - 450 orbit-deleted subsets of these;
  - m = 11, k = 7 on the real base: 48 sets, 1,164 tie frames, 6 tie-critical, 0 failures.
- prefix_ties.py: 59,280 non-collinear grid triples, 18,144 with a Y' tie, 0 prefix violations.
- logs/example_m3.json: a canonical H6(1,·) frame with d = (3770,481). Labels 3 and 4 share x = −14,422,213. The parity-defined B chain 4|0,1,6,7,3 is a convex hexagon (largest convex subset 6). With tied pairs dropped, the longest chain gives only 5.

### F4 (minor): C3a README names the wrong direction of the chain equivalence as the one soundness needs

The README says the gon encodings are one-directional 'so only "a real convex k-gon forces a contradiction" is needed for soundness'. Soundness of UNSAT claims needs the converse: in the least-fixpoint model, a chain of k-1 points implies a real convex k-gon, so a 7-gon-free set satisfies every gon clause. The converse is argued in the next sentences and in C3b DERIVATION.md, and my tests confirm the gon clauses match brute force exactly. This is a documentation error, not a gap.

*Evidence.* results/C3a/README.md, section 'The encoding', paragraph 'No convex k-gon'.

*Suggested fix.* Correct the sentence so it names the chain-implies-k-gon direction as the one used for soundness.

**Independent check:** real = yes; severity minor -> **minor**.

The finding is correct. The quote is verbatim at results/C3a/README.md lines 53-54: "both one-directional, so only 'a real convex k-gon forces a contradiction' is needed for soundness".

Which direction soundness needs:
- An UNSAT claim is sound only if every set in the class (no convex 7-gon) satisfies the CNF.
- The Y/W definitions are upward Horn clauses. So the least-fixpoint assignment satisfies every definitional clause, and the gon clauses hold exactly when the least fixpoint has no complete chain.
- Soundness therefore rests on "a complete chain implies a real convex k-gon".
- "A real convex k-gon forces a contradiction" is the other direction. It only shows that the CNF really forbids k-gons, which matters for SAT models, not UNSAT.

The project's own documents agree with the auditor, so the README contradicts its surroundings:
- C3-S/soundness.md, Theorem (cover), cites "C3a/C3b soundness" for "the true assignment of the C3a variables satisfies the base CNF". That is the chain-implies-k-gon direction.
- C3-S Lemma 3 uses "soundness" in the same sense ("Conversely (not needed for soundness ...)").
- The module docstring of c3cnf.py (lines 28-31) calls the chain-implies-k-gon direction "Soundness".

The README encoding is load-bearing. C3U2/tools/gen_case.py imports C3a/c3cnf.py, and the C3FINAL base (gen_case.py 11 7 none, sha bf0e502e) is the C3a chain CNF.

It is not a gap:
- The needed converse is argued in the README (lines 59-61) and in C3b/DERIVATION.md (lines 50-54).
- I re-proved it. The chain points lie right of x with angles about x strictly increasing inside a span under 180°, so the fan from x is a simple polygon. Left turns at p2..p_{k-2} are encoded. The turns at p1 and p_{k-1} come from ccw(x,.,.), and the turn at x from the span being under 180°. A simple polygon with all left turns is convex.
- c3cnf.py lines 214-250 implement exactly the stated rules with no off-by-one: W[r] for r = 2..k-2, and the gon clause W[k-2] ∧ Y ∧ left turn involves k points.

My own tests (exact arithmetic, my own normal form and Horn least-fixpoint evaluator):
- Generic chain lemma, 3,000 random integer sets: 0 failures. 464 sets without a k-gon had no violation; all 2,536 with a k-gon were violated. 288,915 complete chains were each checked to be a convex k-gon in ccw order.
- Actual c3cnf.py CNFs, m = 3..6 and k = 6, 7, on 1,670 exact 3-fold symmetric sets in Q(√3): 0 failures. All 509 sets without a k-gon satisfy every gon clause, and all non-gon clauses held on every set.
- Mutation tests show the README's named direction cannot carry soundness. Three broken chain encodings (no B condition, no left-turn condition, chain one point short) all still satisfy "a real k-gon forces a contradiction" (0 failures of that direction). Yet they fail soundness on 83, 121 and 83 of 600 sets.
- The CNF for k-1 judged against k flagged 39 of 40 sets without a k-gon. The 40th set has no (k-1)-gon either.

Severity is minor, as the auditor rated it. This is a false meta-statement in the written soundness text of the encoding behind the final theorem, and the geometric trust base is exactly such written proofs. But the correct direction is proved right next to it and has been tested, so the claim is not threatened.

The same inversion appears elsewhere, and a fix should cover all of it:
- The build_conv docstring in c3cnf.py (line 256) says "Sound: a real k-set in convex position makes every conv flag below it true". The conv variant is not used in the final cover.
- C3b/README.md line 84 says "soundness only needs one direction" without naming which.

*Verifier's evidence.* Cited text: results/C3a/README.md:53-54 (wrong direction named), :59-61 (the converse argument).

Project documents that use the correct direction:
- C3a/c3cnf.py:28-31 (module docstring calls chain implies k-gon "Soundness")
- C3-S/soundness.md:50 (Lemma 3, "Conversely (not needed for soundness...)")
- C3-S/soundness.md:81-87 (Theorem cover: true assignment satisfies the base CNF)
- C3b/DERIVATION.md:43-54

Same inversion elsewhere: C3a/c3cnf.py:256 (build_conv docstring). C3b/README.md:84 is ambiguous.

Load-bearing: C3U2/tools/gen_case.py:10,24 imports C3a/c3cnf.py; C3FINAL/README.md:12-13 gives the base as gen_case.py 11 7 none, sha bf0e502e (the C3a chain CNF, per the C3a README table).

My scripts and logs are in AUDIT3/A2_threefold/verify_F4/:
- chain_lemma_check.py → chain_lemma_s2.log: 3,000 sets, 464 without a k-gon, 288,915 chains checked, 0 failures.
- chain_lemma_mutants.py → chain_lemma_mutants.log:
  - none: 0/0
  - noB: 118 soundness / 0 completeness failures
  - noturn: 121 / 0
  - short: 83 / 0
- cnf_level_check.py + run_cnf_suite.sh → cnf_suite.log: real CNFs m = 3..6, k = 6, 7, 1,670 sets, 509 without a k-gon, 0 failures. Mutation controls flagged 39/40.
- mutant_crosscheck_m4k6_s21.log: the one unflagged set has no 6-gon.
- The CNFs and maps were generated with python3 -B from the read-only C3a/c3cnf.py and are in cnf/.

### F5 (note): Both mirror reductions are load-bearing written lemmas

Without Lemma 5, 90 of the 190 H3 layer-2 options are uncovered by the records. Without Lemma H6M, 9 of the 10 H6 cases have uncovered options (between 4 and 72 each). Both are written proofs, not Lean. I re-derived both, including the H6M term sigma xor [r<a] xor [s=0] and the involution property, and tested them on 1,445 sets with 0 failures (the no-sigma-flip mutation was caught 761 times). C3AUDIT2 independently tested H6M on 14,000 sets.

*Evidence.* Covered depth-2 counts per top case from logs/a2compose_report.json (0s0: 100/190; H6 cases 81-153/153); logs/aggregate_tests.txt.

*Suggested fix.* Include Lemma 5 and H6M in any formalization (the C3L plan covers the base only).

### F6 (note): No Lean proof for the threefold soundness

results/C3L is a Lean generator whose base and node CNFs are documented as byte-identical to the Python ones. It contains no theorems. The trust base is the written proofs (C3a README, C3b DERIVATION, C3-S soundness.md, C3H6M addendum) plus tests. SYMMETRIC.md section 3 states this correctly.

*Evidence.* results/C3L/README.md ('There are no theorems yet: this is the generator only').

*Suggested fix.* Prove c3_base_sound and the layer/mirror lemmas in Lean as planned in C3L/PLAN.md.

### F7 (note): Recorded proof hashes are only partly reproducible by re-solving

Of the 485 spot-checked nodes with a recorded proof_sha256, 480 reproduced the identical proof and 5 did not. Of the 1,635 without a hash, 8 differed in proof size; 6 of those are C3W3S pieces originally solved with default options but re-solved with --sat. A hash mismatch on re-solve is therefore not evidence of a bad record, and the 26,436 hashes add limited assurance beyond the fresh re-check.

*Evidence.* My comparison of C3SPOT/out.jsonl with the original records: 480 equal / 5 differ; sizes 1,627 equal / 8 differ.

*Suggested fix.* When regenerating, record the exact options and archive the proofs rather than relying on hashes.

### F8 (note): Independent recomputations by this audit all agree with the recorded claims

(a) The base CNF regenerates with the documented header and sha. (b) My own composer reproduces 116,883 records / 116,741 nodes / 26,748 cube nodes / 26,436 proof hashes, re-derives all CNF hashes with 0 mismatches, finds the class covered and all 910 roots covered, and detects 11 of 11 tampering cases. (c) The record files used by C3FINAL are unchanged between f788780c and HEAD 9cf4949a5; only C3FINAL and C3SPOT were added. (d) The exact-integer encoding tests found 0 failures: 1,630 (set, k) cases, 3,260 frames, 1,155 k-gon-free; at m = 11 all 11 top cases were hit, 55 sets with no 8- or 9-gon satisfied the whole m = 11 formula, and 40 sets tested with k = 7 all contain a 7-gon, as Theorem 1 predicts. One test boundary: the k = 7 gon clauses can only be tested on in-class sets up to m = 10, because no 33-point in-class set is known.

*Evidence.* logs/base_m11k7_info.json, logs/a2compose.log, logs/mutate_results.txt, logs/aggregate_tests.txt, logs/indep_symmax_m10.log, logs/indep_extend_*.log, logs/check_spot.log.

*Suggested fix.* None needed.

## Tests run by the auditor

- gen_base_stream.py 11 7 (streaming, vendored byte-identical c3cnf.py): header p cnf 168399 4154921, sha256 bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da (match); check_stream_small.sh: stream output byte-identical to C3Enc.write for (3,5),(4,7),(5,6),(6,7)
- git diff f788780c..9cf4949a5 over the C3 directories (only C3FINAL and C3SPOT added); all 280 record files present, 128,803 records
- a2compose.py (independent composer, own units, own sha derivation, own tree and phi maps) over the 280 files: class_covered true, 0 CNF-hash mismatches, 0 units-field mismatches, own units equal hullcase.node_units on all 116,741 names, all 910 recorded roots covered, explicit cut 73,567 nodes, 39 s, 535 MB RSS
- a2compose.py --skip-cube-format: not covered (5 open H3 pairs), so the cover depends on the 396 sigma_cubes-format nodes
- mutate_records.py + 11 composer runs (drop, cnf_sha alteration, cake_lpr string alteration, node rename on 3 cut pieces): all 11 report class_covered false
- check_spot.py: C3SPOT re-solved rows are exactly rows 0..2119 of the shuffled sample; 2,120/2,120 pass; 0 CNF-hash mismatches against my derivation
- Spot-check proof reproducibility: 480/485 identical proof hashes; 1,627/1,635 equal proof sizes
- Record survey: no SAT status anywhere; 26 uncertified UNSAT records are cake_lpr 'none' (OOM), all later re-certified; certified-record solve 1,472 h, check 697 h, 13.4 TB proofs; cut 1,266 h + 476 h, 10.5 TB
- indep_eval.py selftest: convex-subset DP equals brute force on 299 random 3-fold sets
- indep_eval.py random (seeds 1, 2, 31, 101): 630 sets, m = 3..11, k = 5..9, 0 failures
- indep_eval.py file: SYMMAX c3_30points (m=10), c6_30points perturbed with all 4,060 orientations kept (m=10), c3_31points minus centre (m=10), c3_27points (m=9), k6/c3_13points minus centre (m=4,k=6); 3 reps x 3 frames each; every clause and every node unit true; mutations caught
- indep_eval.py subsets: 840 orbit-deleted 7-gon-free subsets (m = 5..9, k = 7) of the SYMMAX sets, 1,680 frames, 0 failures
- indep_eval.py extend: 80 m = 11 sets (30-point 7-gon-free set plus one orbit) with k = 7, 8, 9; k = 7: all contain a 7-gon, non-gon clauses and 168,972 units true; k = 8/9: 55 k-gon-free sets satisfy every clause; 0 failures
- aggregate_tests.py: 1,630 (set,k) cases, 3,260 frames, 1,155 k-gon-free, 2,585,438 unit checks, 1,445 mirror checks, 0 failures
- c3_31points check with my DP: 31 points, rotation-invariant, no 3 collinear, largest convex subset 6
- otool disassembly of the archived arm64 cake_lpr (sha 2fee767a...): 0 uses of x18/w18


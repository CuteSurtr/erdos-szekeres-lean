# A8: completeness review

Completeness review of the seven component audits, 1 November 2026 (UTC). Text returned by the review, lightly edited: machine paths replaced by placeholders and internal job names by descriptions (see `../README.md`, §7). "Bogdan" below is B. C. Dumitru, the author of arXiv:2512.24061 (`../README.md`, §5 row 7).

## Overall assessment

Between them, the seven audits cover every logical link of the claim, and none found a logical gap:
- the reduction (A1; separately, a Lean proof of the reduction, including affine symmetries (`SYMLEAN`), outside the seven audits);
- encoding soundness for C3 (A2), the mirror cases (A3) and the fivefold case (A4);
- exact regeneration of every certified CNF;
- an independent composer for the threefold cover (A2);
- an independent orbit closure for C2 with CNF-level reductions A and B (A5);
- the lower-bound examples (A7);
- integrity of 55 archives (A6).

What is missing is concentrated in four places.

**1. No independent proof replay.** No independent party has replayed any retained critical-path proof with hash-bound logs. Neither checker has ever been re-run on mirror33, fivefold P1 or central34-cover, and cake_lpr has never been re-run on any retained proof. [Editorial note: by then the hexagon re-check had already run cake_lpr on 30 of the 120 retained hull proofs, on hash-checked files (item 3); the statement holds for the five critical-path certificates of item 1.] Beyond these, the case theorems rest on solve-time verdicts whose proofs were deleted (about 98% of the threefold cut and about 98% of the central orbit facts), with project-run samples as the only re-check.

**2. Blind spots in the samples.** The threefold sample skipped the sigma-cube pieces (known from A2; 204 indispensable pieces still not re-solved). Additional finding: the central sample skipped the Mac's LOCAL records. 60 central orbit facts and 5 of 8 covers rest only on those records, which also lack any record of the tools used. These facts fell between A5, which counted them, and A6, which checked only re-solved units. The covers have a geometric backup; the 60 facts do not.

**3. Hand-offs between audits.**
- A6 left the 120 hexagon proofs to 'another job'. That job, hexcheck, is running: 30 of 120 were clean at 13:48Z. Its output is unaudited, as are the pilot re-solves (8 of 58) and the newly completed sample.
- For the central rot encoder, A3 audited only the mirror branch and A5 only tested it. Its soundness rests on a docstring sketch and a review with no logs.

**4. Trust weaker than the wording.** These overstatements are already documented by the audits: 'checks actually replayed' cites untracked logs; 'two independent encodings' for the fivefold case; 'two proofs' of Theorem 2a, one built on unretained verdicts; 'random sample' wording for both C3 and C2. Attribution for Theorem 1, the Bogdan fivefold overlap and the assembled theorem was not audited.

Structurally, the exact-33 statement needs only C3-33, M33 and elementary facts, so its trust base is the threefold recorded verdicts plus the never-replayed mirror33 certificate. The statement for 33 or more points adds C2-34, M34 and C5.

Cheapest high-value next steps:
- one replay session for mirror33, mirror34, P1, L1 and the cover (about 1 h, needs about 30 GB free);
- re-solve the 60 LOCAL-only central facts (about 5 h on one lane);
- re-solve the 204 indispensable threefold sigma-cube pieces (about 6-10 h);
- audit and commit the live outputs once they finish.

My forensic pass over all 2,385 certified central records was clean. Scripts and logs are in AUDIT3/A8_completeness/: c2_dependency.py and .log, c2_forensics.py and .log, c2_local_cost.py and .log, and lane_tools.txt. Nothing in the worktree or the archives was modified.

## Missing checks

### 1. Retained certificates on the critical path have never been replayed by anyone independent, with logs tied to input hashes

**Why it matters.** The audit rules barred all seven auditors from loading CNFs over 50 MB and from running cake_lpr. Every audit therefore rated these certificates as solve-time verdicts only. Never replayed at all: mirror33 (Theorem 2a, neither checker), fivefold P1 (neither checker) and central34-cover (neither checker). mirror34 and L1 have only an lrat-check replay, which is untracked (<audit-2026-10-29>, not in git). cake_lpr has never been re-run on any of the five. No checker log records its input hashes (A3-F2, A6-2), and the mirror34 'final' log cannot be told apart from the 'def' log. The exact-33 statement needs only C3-33 and M33, so the mirror33 certificate is on the shortest path to the claim.

**Suggested check.** Run one replay session with a wrapper modelled on the hexagon re-check script (hexcheck.py). For each certificate: require the archive SHA-256, decompress and hash the proof, rebuild or verify the CNF hash, then run lrat-check and cake_lpr on exactly those files. Log both SHA-256s, the command lines, the exit codes and the verdict lines. Commit these logs together with the untracked 2026-10-29 replay logs. Add C4CUT to the session for the N(C4)=28 entry.

**Cost.** From the recorded logs: lrat-check takes under 1 min per proof and cake_lpr about 3-6 min, plus 1-2 min of decompression per 2-4 GB proof. About 45-60 min wall time for the five (or six), run one after another. cake_lpr needs a 20-30 GB heap (30 GB for the mirror proofs), so this must wait until hexcheck and the pilot re-solves finish; the machine had about 30 GB in use at 13:36Z.

### 2. Central 34: 60 orbit facts rest only on the Mac's LOCAL records, which the random re-solve sample excluded by design and which carry no record of the tools used

**Why it matters.** The C2FINAL sample drew only cloud records of kind H or Q. I ran a dependency pass over all 2,492 records (AUDIT3/A8_completeness/c2_dependency.log). It shows that 60 of the 2,296 P1-P8 orbit facts are supported only by records in C2P5/LOCAL (29), C2P4/LOCAL (14), C2P3/LOCAL (8), C2P2/LOCAL (8) and C2P/LOCAL_DEEP (1): 55 hexagonal and 5 quadrilateral. None of these could have been drawn. Each is a single UNSAT fact with no backup argument. All 274 cloud lanes recorded tools.txt (tool hashes, the forged-proof sanity check, the base hash); the 7 LOCAL folders contain only out.jsonl (AUDIT3/A8_completeness/lane_tools.txt). This fell between audits: A5 counted these facts as refuted on their verdict strings, and A6 checked only the archives of the 38 re-solved units. The covers P1-P5 also rest only on C2P3/LOCAL records, and none of P1-P7 was re-solved. The covers have a written geometric backup (the inner hull has 4 or 6 vertices, audited by A5), so they are secondary.

**Suggested check.** Re-solve the cheapest supporting member of each of the 60 orbits, optionally also the 7 covers. Use reproduce.py-style hash binding (rebuild the CNF and require the recorded hash), both checkers, and archived proofs or at least proof hashes. Also recover from the session scripts and logs which cadical, lrat-check and cake_lpr binaries the Mac lanes used, and record them.

**Cost.** From the recorded times (AUDIT3/A8_completeness/c2_local_cost.log): the 60 orbits need about 3.3 h solving, 0.4 h lrat-check and 1.6 h cake_lpr, about 5.2 h on one Mac lane. Peak RSS is 11.8 GB and the raw proofs total 116 GB (roughly 20 GB after zstd). The 7 covers add about 1.8 h (RSS up to 13.4 GB, 33 GB raw). About 3.5-4 h wall time on two lanes, plus about 30 min to trace the Mac's binaries.

### 3. Central 34: tonight's live re-checks are not yet audited, committed or listed in CERTIFICATES.md

**Why it matters.** Jobs outside the seven audits are closing gaps that C2FINAL found:
- hexcheck.py is re-checking the 120 hexagonal-hull proofs on hash-checked files. A6 explicitly left these to 'another job', and A5 checked only their CNF hashes. At 13:48Z, 30 of 120 were done, all hash-matched and accepted by both checkers.
- reproduce_pilot.py is re-solving the 58 P8 orbits whose cake_lpr ran on an unhashed rebuilt CNF. 8 of 58 were done.
- The main sample is complete. P8_1-10 was freshly certified, but its proof is not identical to the cloud record.

The new proofs sit in archives absent from the repository and from CERTIFICATES.md: es7-central34-pilot-orbits-2026-11-01, and P6_9-11, P7_1-15 and P8_1-10 in the resample archive. Each exists in one local copy only.

**Suggested check.** When the jobs finish, run an independent pass over the outputs:
- each of the 120 + 58 lines has cnf, archive and proof matches all true and the exact verdict strings;
- compute your own SHA-256 of every new archive file;
- recompute the orbit closure separately for (a) re-verified records and (b) recorded-only records, so the write-up can say what remains recorded-only;
- commit the records, the archive hashes and the hexcheck out.jsonl.

**Cost.** About 30-60 min after the jobs end. hexcheck has about 3-4 h left on 2 lanes and the pilot re-solves about 3-4 h. Independent archive hashing takes about 1-2 min per 10 GB.

### 4. Threefold: the 204 cut pieces that are each indispensable and exist only in sigma-cube format have never been re-solved, and no targeted re-solve is scheduled

**Why it matters.** A2-F2, confirmed by its verifier: C3SPOT drew only plain-format records. 396 nodes exist only in sigma_cubes.py format, and 204 of them are each individually necessary for the cover (C3SIG2 84, C3W3S 120). Four of the C3SIG2 cubes timed out at 300 s in C3W4/O01 on the identical CNF. Also, 39 of 229 lanes, holding 1,319 cut pieces, had no piece re-solved. The night's notes record a no-go only for a full re-proof (a separate feasibility study). The exact-33 statement depends on C3-33.

**Suggested check.** Re-solve the 204 indispensable nodes (list: AUDIT3/A2_threefold/verify_F2/necessity_C3SIG2_C3W3S.jsonl) plus one random cut piece from each never-sampled lane. Use both checkers and keep the proof hashes. Note that a sigma-cube record's 'node' field is the parent node, so rebuild each CNF from the cube itself.

**Cost.** At recorded cloud speed: about 8.0 h solving and 2.4 h checking for the 204 nodes (about 6-7 h on the Mac), and about 2 core-h for the 39 lane pieces. Node CNFs are about 110 MB, so the project must run this; the audit rules' limits rule out an auditor run.

### 5. Central encoder (zcnf.py rot, m = 2, --hull): its soundness was never audited as a proof and never mutation-tested

**Why it matters.** No audit checked this as a proof:
- A3 audited only the mirror branch.
- A5 states that encoder validity is 'tested, not proved'.
- A1 checked only the zero-triple interface.

The written argument for the rot branch is one sentence in SYMZ/README.md §1 plus a sketch in the zcnf.py docstring. The 2026-10-29 review covered rot m=2 with --no-sb and committed only scripts (C2C34/review has no README and no logs), yet C2FINAL §1 cites it as 'the encoder was reviewed'.

The empirical evidence is real: val_real.log (sym7_32 SAT at t=16 with --hull), rt_run_all.log (rot m=2, t=5-7, K=5-7, 0 mismatches) and A5's 234 full-base labellings. But nobody showed that these evaluators would catch a broken rot clause family.

**Suggested check.** Write and audit a half-page proof for the rot branch:
- the half-turn is diag(1,-1,-1) with det +1 and fixes v_c;
- the zero triples are exactly {c,p,-p};
- chi(c,p,q) = chi(-p,p,q), from v_c = (v_p + v_-p)/2;
- every vector has first coordinate 1, so A4 holds without the epsilon used for Z;
- one conv variable per half-turn orbit is valid;
- A5's results cover the normal form and hull clauses.

Then run A3's myeval.py and mutate.py approach in kind=rot, m=2, t=4..10, K=5..7 with --hull, using mutants: flipped centre identity, wrong group sign, wrong sector unit.

**Cost.** 2-3 h of writing and review, plus at most 1 h of compute (under 1 GB).

### 6. Link from the certificates to the Lean case classes: the centre-perturbation lemma and a class-by-class match

**Why it matters.** SymmetricReduction.lean and AffineReduction.lean (`SYMLEAN`) are outside the seven audits; a follow-up definitions review checked them. They prove the reduction from five Props. Threefold33 and Fivefold35 are stated without 'no two points collinear with c', which the C3a and symcnf normal forms need. The link is a per-orbit rotation by a small angle. It is one sentence in SYM5 §1 and absent from the threefold documents (A1, A2). None of the seven audits checked each class Prop against what its certificate plus soundness argument actually delivers: size, centre status, axis status, and Euclidean against oblique reflections. The Euclidean-reflection classes are reached from affine symmetries only through AffineReduction.lean.

**Suggested check.** Write the perturbation lemma with an explicit statement and proof for m = 3 and m = 5: the order type of S is kept, invariance is kept, and c becomes generic. Add a table mapping each Lean class to its CNF, normal-form lemma and soundness document. In the assembled theorem, cite the Lean reduction, including the affine file.

**Cost.** 1-2 h of writing. Optional Lean formalization of the perturbation: 1-3 days.

### 7. Attribution and priority were not audited for Theorem 1, for the fivefold overlap with Bogdan, or for the assembled theorem

**Why it matters.** Literature was checked only for the central case (C2FINAL §7) and the mirror case (the A3-F4 verdict). A4-11 explicitly skipped Bogdan (arXiv:2512.24061 §7, the '5^6' UNSAT run). SYM5 and SYMMETRIC.md say that run implies the fivefold bound, while C2FINAL §7 says the paper has no symmetric results. The only basis for credit is SYM5's argument that his generator imposes nothing beyond within-layer convexity and nesting, and nobody has checked that argument. The CICM 2025 chapter of SMQH25 is still unread, so the write-up itself calls priority provisional.

**Suggested check.** Read Bogdan §7 and es_sat_gen.py to confirm that his model relaxes 'six strictly nested convex pentagons plus three interior points', as the layer lemma gives. Obtain the CICM chapter. Apply the wording 'no matching prior result found in the sources inspected', with the list of sources, to Theorem 1 and to the assembled theorem.

**Cost.** 2-4 h plus library access for the Springer chapter.

### 8. Central 34: the sample cannot bound errors confined to one lane, and no lane-stratified spot check was run

**Why it matters.** Re-solves so far cover 38 of the 2,296 orbit facts; the random part contains only 8 of the 448 quadrilateral facts. 250 of the 281 lanes with certified units never had any unit re-verified, and they hold 1,815 of the 2,232 orbit facts supported by a single lane. Two long quadrilateral re-solves (P6_1-7, P8_1-10) produced proofs different from their records, so recorded proof hashes cannot replace re-checks for long solves. My forensic pass over all 2,385 certified records (AUDIT3/A8_completeness/c2_forensics.log) found nothing wrong: no proof hash shared between units, one CNF hash per unit, no tiny proofs or zero times, and checker speeds within each host's band (cloud cake_lpr at most 17 MB/s, Mac at most 35 MB/s). Every cloud lane also logged tool hashes and forged-proof sanity checks. This lowers the risk of an isolated bad record but does not remove it.

**Suggested check.** Re-solve one short hexagonal unit from each of about 40 never-re-verified lanes, stratified by wave, with hash binding and both checkers.

**Cost.** About 4-6 h on one Mac lane. Covering all 250 lanes would take about 25-40 core-h.

### 9. Threefold mirror reductions (Lemma 5, Lemma H6M) were never checked at the CNF level

**Why it matters.** Both are load-bearing: without them, 90 of 190 H3 options and 9 of 10 H6 cases are uncovered. They rest on written proofs plus real-set tests (1,445 sets in A2, 14,000 in C3AUDIT2). For the central reductions A and B, A5 showed that a literal-map check turns the prose into a mechanical check whose mutants are caught: the map sends the base into the base plus one geometric line, and sends cubes exactly onto cubes. Nobody tried this for the threefold reductions.

**Suggested check.** Try the same literal-map check for Lemma 5 and H6M on the C3a base (168,399 variables, 4.15M clauses, streamable). If the x-order and inv variables do not map literally when l is re-chosen, record why and fall back to Lean, as in the C3L plan.

**Cost.** 1-2 days, and it may prove infeasible. Lean: weeks.

### 10. Every case except Theorem 2a rests on a single encoder

**Why it matters.** C3-33, C2-34 and M34 each rest on one encoder. The fivefold result uses two normal forms of the same encoder (A4-3). A bug in a clause family shared by all of an encoder's pieces would affect every piece. The audits guard against this only by exact clause evaluation on real sets, not with a second model. C2SGN, a signotope encoding at 0.1-0.3 GB per solve, has not closed the parallelogram case, and nothing compares it with zcnf on shared sub-cases.

**Suggested check.** State the single-encoder limitation in the write-up. As a cheap partial check, give a few real configurations to both zcnf and C2SGN, and to both C3a and symcnf for m = 3, and confirm that both models accept each one and reject deliberately wrong labellings. A full independent closure is a separate project.

**Cost.** Partial check: about 2-4 h. Full C2SGN closure: hundreds of core-hours (C2SGN §6).


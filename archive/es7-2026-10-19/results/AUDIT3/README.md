# AUDIT3: adversarial audit of the symmetric ES(7) claim

Local runs on an Apple M5 Pro, 1 November 2026 (UTC), about 12:10–13:50, against `es7-cloud` at 471d5f63a. The
status of the follow-up checks (§5) is as of 19:43 UTC the same day.

**Statement audited.** Every set of at least 33 points in general position with a nontrivial symmetry, isometric or
affine, contains a convex 7-gon.

**Status.** Seven component audits each returned *sound with caveats*. None found a logical gap. Every finding rated
minor or major was checked again by a separate verifier. One finding remains major: the write-up's trust base
(`WRITEUP/SYMMETRIC.md`, `WRITEUP/CERTIFICATES.md`) did not yet cover the central-34 and C4CUT certificates (A6-1).
The other 58 findings are minor (24) or notes (34). This directory records an audit; it claims no theorem. At
471d5f63a the statement depends on the central 34-point theorem C2-34, which `C2FINAL` had not yet claimed.

## 1. Method

- **Seven component audits** (A1–A7). Each reviewer got the repository at 471d5f63a and the local proof archives,
  both read-only, and wrote its own scripts.
- **Limits.** At most 1.5 GB per process, no SAT solve longer than 15 minutes or on a CNF above 100 MB, no CNF above
  50 MB loaded into memory, and no run of cake_lpr. So no large certificate was replayed. Certificates were checked
  through hashes, regeneration of the CNFs and fingerprints of the checker logs.
- **Verification of findings.** Each of the 26 findings rated minor or major went to a separate verifier, who decided
  whether it was real and set its severity. The 33 notes were not re-checked.
- **Completeness review** (A8). A last review looked for checks that no audit covered.
- **Full texts.** `reports/A1_reduction.md` … `reports/A8_completeness.md` hold each audit's verdict, trust table,
  findings with the verifier's reasoning, and tests. `findings.tsv` has one line per finding.

## 2. The chain and what each link rests on

The minimal set of case theorems is C3-33, C5 ≥ 35, M33, M34 and C2-34, plus the fact that every non-central orbit
of a rotation of order p ≥ 7 is a regular p-gon and so contains a convex 7-gon (A1-F5; the size arithmetic is
Lean-checked for all n, minimality was checked by script). Exactly 33 points needs only C3-33 and M33. The fourfold
case is on no critical path once C2-34 holds: a fourfold set in general position with 33 or more points has at least
36 points, so it contains 17 antipodal pairs and C2-34 applies (A4-6). C4CUT is still what gives N(C4) = 28.

| link | rests on | audit |
|---|---|---|
| reduction to the case theorems, isometric and affine | written proof (reviewed: re-derived in A1); size arithmetic Lean-checked (`A1_reduction/SizeArith.lean`, 20 theorems, core Lean 4.24.0); the implication from the five case classes Lean-checked outside the seven audits (`SYMLEAN`, §5 row 6) | A1 |
| C3-33 (Theorem 1): encoding, Lemmas 1–5, Lemma H6M | written proof (reviewed in A2); computational evidence (exact tests, 1,630 cases, 0 failures) | A2 |
| C3-33: cover of the case split | exact computation (A2's own composer over 116,883 records, every CNF hash re-derived, class covered); bookkeeping Lean-checked after the audit (`C3LEAN`, last rows of §5) | A2 |
| C3-33: the 73,567 pieces of one explicit cut | certificates accepted by both checkers when solved; proofs not retained (recorded verdicts); 1,337 of them re-solved in `C3SPOT`; the 204 indispensable σ-cube pieces were outside that sample (§5 row 4) | A2, A6 |
| M33 (Theorem 2a) | certificate accepted by both checkers (retained proof `e1b2689d…` on CNF `e45464ed…`, checked at solve time only); encoding: written proof (reviewed in A3) | A3, A6 |
| M34 (Theorem 2b) | certificate accepted by both checkers (retained proof `98e4d02a…` on CNF `b175eac0…`, checked at solve time; one lrat-check replay of 29 October, log untracked, A3-F1); encoding: written proof (reviewed in A3) | A3, A6 |
| C5 ≥ 35 | two certificates accepted by both checkers at solve time (P1 `eff67c0f…` on `ead55228…`, L1 `8625b321…` on `90dea1cf…`; L1 also passed a hash-bound lrat-check replay, §5 row 1); two normal forms of one encoder (A4-3), written proof (reviewed in A4) and computational evidence; layer lemma: written proof (proved in full by A4, A4-7) | A4, A6 |
| C2-34: hull cover and the 120 hexagonal hulls | certificates accepted by both checkers, proofs retained (cover `3255391a…` on `bb60facb…`); for the hexagons cake_lpr first ran on a rebuilt CNF that was not hashed, and the re-check on hash-checked files accepted all 120 (§5 row 3b) | A5, A6 |
| C2-34: the 8 parallelogram cases | 2,385 UNSAT records, each accepted by both checkers when solved (for the 58 P8 pilot orbits, cake_lpr ran on an unhashed rebuilt CNF), proofs deleted (recorded verdicts); 38 units re-solved with archived proofs by 471d5f63a, more since (§5 rows 3a, 3c); 60 orbit facts and the P1–P5 covers rested only on the Mac's LOCAL records, which keep no record of the tools used; 44 of these 65 were re-solved by 1 November 2026, 19:43 UTC (§5 row 2); reductions A and B: written proof (reviewed) and exact computation at the CNF level (A5-1); bookkeeping Lean-checked (`C2FINAL` §6) | A5, A6, A8 |
| C2-34: the encoder `SYMZ/zcnf.py rot 17 7 --m 2 --hull` | computational evidence only at audit time (234 full-base labellings in A5); a written proof was completed later that day and refereed (§5 row 5) | A5, A8 |
| lower-bound examples (the threshold 33 is sharp) | exact computation, two independent exact methods per file | A7 |

## 3. Component verdicts

| | component | verdict | findings after verification | main checks |
|---|---|---|---|---|
| A1 | reduction and size table | sound with caveats | 3 minor, 6 notes | own proof of the reduction, isometric and affine; size arithmetic for all n in core Lean, and by script for n ≤ 600 and orders ≤ 60; full symmetry groups of the example files |
| A2 | threefold 33 | sound with caveats | 4 minor (F1 lowered from major), 4 notes | own composer over the 280 record files: 0 hash mismatches, class covered, all 910 roots covered, 11/11 tampering tests detected; base CNF regenerated (`bf0e502e…`); exact-integer encoding tests |
| A3 | mirror (2, 2a, 2b) | sound with caveats | 4 minor, 5 notes | soundness proof re-derived; both CNFs regenerated byte-identical; two own evaluators on 2,460 configurations (27 small instances) and 128 on the certified 33- and 34-point CNFs; 14 mutation runs |
| A4 | fivefold, layer lemma, even-m encoder | sound with caveats | 4 minor, 7 notes (A4-2 lowered to a note) | layer lemma proved in full; 4,415 + 5,688 exact evaluations of both encoders, 1,750 wrong labellings caught; the six C4CUT cuts re-verified, 36/36 mutations rejected |
| A5 | central 34: normal form, cubes, reductions | sound with caveats | 2 minor, 5 notes | normal form from any hull vertex (3,000 sets); all cube files rebuilt; reductions A and B checked against all 16,653,336 base clauses; own orbit closure: 2,596/2,596 hashes, 287/287 orbits per case |
| A6 | certificate trail | sound with caveats | 1 major, 5 minor, 4 notes | 55 archives: size, SHA-256 and decompression round trip; lrat-check log fingerprints equal the archived proofs; every regenerable CNF byte-identical; c3hex replayed with lrat-check |
| A7 | lower-bound examples | sound with caveats | 2 minor, 3 notes | 15 files: exact symmetry and orbits, general position, convex-subset DP in four orders, exhaustive C enumeration; the project's checkers re-run on copies |

All 26 re-checked findings were confirmed as real. The verifiers changed two severities: A2-F1 from major to minor,
A4-2 from minor to note.

## 4. Findings and their checked severity

"auditor" is the severity the auditor gave; "checked" is the verifier's. Notes were not re-checked (—). A2 numbered
its findings F1–F8; they are cited here as A2-F1 … A2-F8.

**The major finding (A6-1, confirmed).** At 471d5f63a, `WRITEUP/SYMMETRIC.md` (revised 2026-10-29) still calls the
central 34-point case open (in §4; the auditor first wrote §3) and assumes the published fourfold exclusion in
Corollary 3. Its list of replayed checks covers only the threefold, mirror and fivefold cases. It does not say that
the parallelogram part of C2-34 rests on recorded verdicts of deleted proofs: of the 2,304 facts the case split needs
(8 covers and 8 × 287 orbits), 38 units, about 1.6%, had been re-solved with archived proofs. `WRITEUP/CERTIFICATES.md`
lists none of the three archives of 1 November (`es7-c4-32-cuts-2026-11-01`, `es7-central34-pilot-resolve-2026-11-01`,
`es7-central34-resample-2026-11-01`), and its central34-cover entry says the case "remains open". `C4CUT/README.md`
still says its review is pending. No certificate failed; the claim cannot be stated on this trust base as written.

#### A1: reduction

| ID | auditor | checked | finding |
|---|---|---|---|
| A1-F1 | minor | minor | The assembled theorem is not written anywhere; the write-up still treats the central case as open |
| A1-F2 | minor | minor | Fourfold dependency: redundant for the main claim, but cited to a source whose rigor the repository itself disputes |
| A1-F3 | minor | minor | The affine-symmetry extension is a single unproved sentence |
| A1-F4 | note | — | The overall claim depends on C2-34, which C2FINAL does not yet claim |
| A1-F5 | note | — | Minimal set of case theorems and which theorem each size needs |
| A1-F6 | note | — | Case-theorem interfaces verified, including centre and axis status and implicit encoder preconditions |
| A1-F7 | note | — | Size table re-derived; example files checked; each example has exactly the listed symmetry group |
| A1-F8 | note | — | Small imprecisions in the lemmas |
| A1-F9 | note | — | Stale status statements elsewhere in the repository |

Verifiers' corrections: the one-line half-turn step is already written as a remark, so what is missing is the
assembled statement (A1-F1); changing the C2 table row to 32 must wait until C2-34 is claimed. arXiv:2506.00224 §6.2
gives no method for its unrealizability step; without C2-34, the fourfold 32-point result is still needed in
Corollary 3 (A1-F2). Oblique reflections were covered only by the one-sentence remark (A1-F3); the Lean affine
extension of §5 now covers them, conditional on the case classes.

#### A2: threefold 33

| ID | auditor | checked | finding |
|---|---|---|---|
| A2-F1 | major | minor | Piece verdicts are recorded only and not replayable: proofs deleted, 98% of an explicit cut never re-checked |
| A2-F2 | minor | minor | Spot-check population excluded 396 sigma_cubes-format nodes on which the cover depends |
| A2-F3 | minor | minor | Distinct x-coordinates (no segment of S parallel to l) is used but not stated as a WLOG step |
| A2-F4 | minor | minor | C3a README names the wrong direction of the chain equivalence as the one soundness needs |
| A2-F5 | note | — | Both mirror reductions are load-bearing written lemmas |
| A2-F6 | note | — | No Lean proof for the threefold soundness |
| A2-F7 | note | — | Recorded proof hashes are only partly reproducible by re-solving |
| A2-F8 | note | — | Independent recomputations by this audit all agree with the recorded claims |

Verifiers' corrections: A2-F1 is factually right (73,567 cut pieces, 24,733 with a proof hash, 72,230 never
re-solved) but was lowered to minor. Every record-writing script hashes the CNF the checkers read and certifies only on
the exact verdict strings; 2,107 of the 2,120 re-solves reproduced the recorded proof size; the limitation is
disclosed. "Not replayable" overstates: every piece was checked by both checkers when solved, and can be re-solved.
The verifier added that 39 of 229 lanes (1,319 cut pieces) had no piece re-solved. For A2-F2, 204 of the 396 nodes
are each indispensable (C3SIG2 84, C3W3S 120). For A2-F3, the encoding itself is sound with tied x-coordinates
(argument, and 27,024 tie frames with 0 failures); only the prose assumes distinct ones.

#### A3: mirror

| ID | auditor | checked | finding |
|---|---|---|---|
| A3-F1 | minor | minor | No independent replay is on record for the 33-point mirror proof; the 34-point 'independent replay' has no log |
| A3-F2 | minor | minor | Checker logs are not tied to file hashes |
| A3-F3 | minor | minor | The written soundness proof is correct but leaves several steps implicit |
| A3-F4 | minor | minor | The Theorem 2b heading in SYMMETRIC.md uses a bare novelty word |
| A3-F5 | note | — | Theorem 2b rests on a single computer proof whose encoding soundness is a hand proof, not a Lean proof |
| A3-F6 | note | — | Earlier reviews of SYMZ left no committed outputs |
| A3-F7 | note | — | tau() maps the axis point to Z's index |
| A3-F8 | note | — | The model is tight at the extremal example; the binary clauses are understood |
| A3-F9 | note | — | The old Lean chain for 2a depends on unretained verdicts; Theorem 2 does not need it |

Verifiers' corrections: the mirror34 lrat-check replay of 29 October does have a log, untracked in the main
repository (exit 0, 45.45 s, input hashes equal to `WRITEUP/CERTIFICATES.md`); the mirror33 proof was never replayed
(A3-F1). The lrat-check logs bind more than reported (Added, Deleted and Max live all equal the archived proofs), but
the CNF is bound only by its header and cake_lpr logs not at all (A3-F2). Mutation M6 does not exercise the fast path
of the Grassmann–Plücker clauses; the fast path was checked separately (A3-F3).

#### A4: fivefold, layer lemma, even-m encoder

| ID | auditor | checked | finding |
|---|---|---|---|
| A4-1 | minor | minor | Even-m sector normal form: the argument that every real set has such a labelling is never written down |
| A4-2 | minor | note | Layer lemma is stated without all the facts the encoder uses |
| A4-3 | minor | minor | 'Two independent encodings' overstates independence |
| A4-4 | minor | minor | Stale statements about the fourfold case across documents |
| A4-5 | minor | minor | C4CUT does not record which checker binaries produced its verdicts |
| A4-6 | note | — | Fourfold is on no critical path once central-34 holds; fivefold is indispensable |
| A4-7 | note | — | Layer lemma: proved in full |
| A4-8 | note | — | Exact soundness tests of both encoders found no violation |
| A4-9 | note | — | C4CUT cut soundness confirmed independently; hash chain reproduced |
| A4-10 | note | — | Checker verdicts taken from logs, not replayed |
| A4-11 | note | — | Prior-work remarks not checked |

Verifiers' corrections: A4-2 was lowered because the centre-inside units are base-model units, and strict nesting is
written in `SYM5/README.md`. The P1 and L1 CNFs have the same first 7,923,894 clauses; after that P1 has 15
normal-form units and L1 has 133, none in common (A4-3). C2-34 cannot give N(C4) = 28, since a central 32-point
example exists; only C4CUT does (A4-4). An unpatched lrat-check that accepts a forged proof exists on the machine,
but the final step of the C4 proof is a genuine RUP conflict, and cake_lpr also accepted the proof (A4-5).

#### A5: central 34, reductions

| ID | auditor | checked | finding |
|---|---|---|---|
| A5-1 | note | — | Reductions A and B hold at the CNF level, which is stronger than the repository claims |
| A5-2 | minor | minor | The write-up has no self-contained statement of reductions A and B and still calls the central case open |
| A5-3 | minor | minor | Off-by-one wording: 'numbers of antipodal classes between consecutive hull vertices ... summing to 17' |
| A5-4 | note | — | Symmetry breaking in the base is exactly the normal form; no stacked-symmetry-breaking conflict |
| A5-5 | note | — | Full-base evaluation, including the 7-gon encoding; the two-heptagon near-miss lies in a closed orbit |
| A5-6 | note | — | The closure depends entirely on reductions A and B; my independent orbit closure agrees |
| A5-7 | note | — | Hull-cover checker logs do not record which CNF was checked |

Verifiers' corrections: the index maps of A and B were re-checked on 10,000 labellings of 2,500 sets with 0 failures;
the lemma should fix one restart convention (A5-2). The off-by-one wording has no mathematical effect (A5-3).

#### A6: certificate trail

| ID | auditor | checked | finding |
|---|---|---|---|
| A6-1 | major | major | The write-up's trust base does not cover the central-34 and C4CUT certificates (see above) |
| A6-2 | minor | minor | Checker logs do not name or hash their inputs, and cake_lpr logs cannot be tied to a specific proof |
| A6-3 | minor | minor | C4CUT keeps no raw checker output, and its archive hashes are recorded only inside the archive |
| A6-4 | minor | minor | The 'independent audit' replays are not logged anywhere in the repository |
| A6-5 | minor | minor | The c3hex checker log is not in the repository, contrary to CERTIFICATES.md |
| A6-6 | minor | minor | The random re-solve sample is incomplete in the repository, and the draw cannot be reproduced |
| A6-7 | note | — | cake_lpr heap set through an environment variable this build ignores |
| A6-8 | note | — | Archived logs are redacted copies; the solver build is identified only by the C4 log |
| A6-9 | note | — | Every retained proof exists in one local copy only |
| A6-10 | note | — | Which certificates are bound to a hashed CNF |

Verifiers' corrections: the cover's cake_lpr command (heap 20,000 MiB) is in no committed script, and the
`heap12000` log name records a setting that never took effect (A6-2). C4CUT is not the only certificate that keeps a
single verdict line (A6-3). The 29 October replay logs exist, untracked (mirror34 45.45 s, L1 18.1 s), and only need
committing (A6-4). Both c3hex proofs were replayed with lrat-check and with the verifier's own RUP checker (A6-5). The
sample draw *is* reproducible: the verifier re-drew 24/24 and 8/8 units from the committed records with the README's
seeds (A6-6). The missing part was real: the three missing units were re-solved later on 1 November (§5 row 3a), and
their records are not yet committed.

#### A7: lower-bound examples

| ID | auditor | checked | finding |
|---|---|---|---|
| A7-1 | minor | minor | The Z[zeta5] example files depend on the choice of embedding and do not say which one; the convention is stated only in SYMMAX/README.md |
| A7-2 | minor | minor | The LaTeX note says all lower-bound examples were found by simulated annealing, but the SYM2 set is an explicit construction |
| A7-3 | note | — | Exactly what is proven for the irrational-angle rotations: exact algebraic coordinates, with no approximation |
| A7-4 | note | — | All 15 example files pass every check; results match the README numbers and the project's own checkers |
| A7-5 | note | — | Scope: the examples give only lower bounds, and they show that the threshold 33 in the overall claim is sharp |

Verifiers' corrections: under the Galois-conjugate embeddings the 30- and 31-point Z[zeta5] files contain convex
10-gons and `SYMMAX/k6/c5_16points.txt` a convex 7-gon; the verifier confirmed this for `SYM5/c5_31minus_centre.txt`
as well. The convention is also stated in the docstring of `SYMMAX/verify5.py` and in `SYMMAX/anneal5.c`; it is
missing from the data files and the write-ups. A header line in the data files would break `shrink.py` and
`shrink5.py`, which do not skip `#` lines (A7-1).

## 5. Missing checks named by the completeness review, and what was done on 1 November

Numbering as in `reports/A8_completeness.md`. Status as of 1 November 2026, 19:43 UTC (first written at 15:08 UTC). The
status column says whether each missing check is now closed, partly closed or open.

| # | missing check | status | result so far |
|---|---|---|---|
| 1 | Replay of the retained critical-path certificates with logs tied to the input hashes | partly closed | A replay kit lists 191 retained certificates. Its hash stage is complete for all 191: archive, proof and CNF SHA-256 equal the records (198 archive files). Every generator it ran rebuilt its CNF byte-identically; `SYMZ/hullcubes.py` was not run, and the cover CNF was rebuilt by a separate streaming script instead. lrat-check was replayed with hash-bound logs on the 18 entries whose proofs are under 2 GB: all `c VERIFIED`, including c5-L2, which no checker had run on before. On 1 November (17:59–18:02 UTC) the kit ran the full replay with both checkers on c5-L1, c3hex-15, c3hex-16 and c4cut-final: all four certified, with the recorded hashes before and after the checks (`REPLAY`). At 20:10 UTC the full replay also accepted the hull cover (central34-cover) with both checkers (`REPLAY` §6). Open: cake_lpr has not been re-run on mirror33, mirror34, c5-P1 or c5-L2 (the cover is now done), and lrat-check has not been replayed with hash-bound logs on mirror33, c5-P1 or central34-cover; mirror34 has only the untracked lrat-check replay of 29 October. None of these had been run by 1 November 2026, 19:43 UTC (cake_lpr heaps 30,000 MiB for mirror33, mirror34 and c5-P1, 20,000 MiB for the cover, 8,000 MiB for c5-L2). |
| 2 | Central 34: 60 orbit facts and 5 of 8 covers resting only on the Mac's LOCAL records | partly closed (running) | 65 units (60 orbit representatives and the P1–P5 covers) in two lanes, started when the P8 lanes of row 3c finished. Each CNF is rebuilt and must match the recorded hash; both checkers; proofs to the local archive `es7-central34-local-2026-11-01` (outside Git). A build-only test rebuilt the recorded CNF hashes of P8_1-9, P4_cover and P1_cover. Result: 44 of 65 by 1 November 2026, 19:43 UTC, the five covers among them; all 44 rebuilt the recorded CNF, reproduced the recorded proof and passed both checkers, none failed (`C2RECHECK`). Not done: tracing which binaries the LOCAL lanes used. |
| 3a | Central 34: the three missing units of the random sample | closed | All three re-solved, CNF hashes equal to the records, both checkers accept. P6_9-11 and P7_1-15 reproduced the recorded proofs (`2238c76e…`, `8384801a…`). P8_1-10 (CNF `163f52ea…`) gave a different proof (`e98aa3ee…`, 9,952,275,647 bytes). Archived in `es7-central34-resample-2026-11-01` (`P6_9-11.lrat.zst` `9cb332e4…`, `P7_1-15.lrat.zst` `98934f65…`, `P8_1-10.lrat.zst` `2e701cb3…`). The main sample is 24 of 24. Records not yet committed. |
| 3b | Central 34: the 120 hexagonal-hull proofs re-checked on hash-checked files | closed | 120 of 120 done (finished 17:59 UTC). In all 120 the rebuilt CNF, the archive and the decompressed proof equal the recorded SHA-256, and both checkers accept (cake_lpr heap 8,000 MB) (`C2RECHECK`). |
| 3c | Central 34: the 58 P8 orbits whose cake_lpr ran on an unhashed CNF | closed | 58 of 58 done (finished 17:33 UTC). All 58 rebuild the recorded CNF, reproduce the recorded proof and pass both checkers; proofs in the local archive `es7-central34-pilot-orbits-2026-11-01` (`C2RECHECK`). |
| 3d | Central 34: independent pass over these outputs, closure split by evidence, commit | partly closed | The replay kit hash-checked the 20 pilot-orbit units then finished and all 34 resample units, and its hull hashes agree with those of row 3b on the 47 cases compared. Closure split: by 1 November 2026, 19:43 UTC, 224 of the 2,304 facts (8 covers and 8 × 287 orbits), 9.7%, had a re-solve on a hash-checked CNF with both checkers and an archived proof (`C2FINAL` §9, `C2FINAL/closure_split.py`); the other 2,080 rest on recorded verdicts. Entries for the re-solves are in `WRITEUP/CERTIFICATES.md` (revised copy, with the records in `C2RECHECK`, both not yet committed). Open: an independent re-hash of the archives written on 1 November (so far only the jobs' own round trips). |
| 4 | Threefold: the 204 indispensable σ-cube pieces never re-solved | closed | The list was confirmed: removing any one of the 204 leaves the class uncovered under the unchanged `C3U2` composer, and the list equals A2's. All 204 rebuilt CNF hashes match their records. The re-solve run (hash-bound, both checkers, proofs archived in the local archive `es7-c3-indispensable-2026-11-01`) started at 15:02 UTC on two lanes; each piece CNF is about 110 MB. All 204 were done at 18:22 UTC: every piece rebuilt the recorded CNF and passed both checkers; 200 gave a proof of the recorded size and 4 a different proof (σ-cube records carry no proof hash) (`C3PIECES`). Not included: one piece from each of the 39 lanes with no re-solved piece. This closes only the σ-cube gap; about 98% of the plain-format cut stays recorded-only. |
| 5 | Central encoder `zcnf.py rot`, m = 2, `--hull`: soundness never audited as a proof | closed | A written proof covers every clause family of the base CNF `b0061e90…`: every real centrally symmetric 34-point set in general position without a convex 7-gon satisfies it, from every hull vertex. Computational evidence with it: a generator written from the proof's statements matches the base family by family (GP 12,588,160; A4 413,440; CONV4–6 950,912; KGON 2,689,808; SB 136; HULL 10,880 clauses); in 122 exact hull-vertex labellings of 25 real sets the violated clauses are exactly those of genuinely convex 7-sets (25 non-hull controls also violate the predicted hull clauses); 12 mutation defects, every unsound one caught. Refereed on 1 November: sound, with minor documentation gaps, no blocking or major finding; its findings R1–R8 are resolved in `C2ENC` §4 (R5 and R7 need no change). Location: `C2ENC` (not yet committed). |
| 6 | Link from the certificates to the Lean case classes | partly closed | `SYMLEAN`: `heptagon_of_nontrivial_isometry` derives the statement for Euclidean isometries from the five case classes, and `heptagon_of_nontrivial_affineEquiv` extends it to affine symmetries; axioms `propext`, `Classical.choice`, `Quot.sound`. A definitions review found that all six classes (Fourfold32 included) match their certificates' statements, none is vacuous and none is stronger than its certificate; for Threefold33 and Fivefold35 the match uses a written perturbation argument. Written and refereed with the encoder proof of row 5 (`C2ENC`): the centre-perturbation lemma for odd orders (m = 3, 5) with an exact m = 3 illustration on 30 sets, and a table from each Lean class to its encoder, CNF hashes, normal form, soundness document and certificate. The two mirror classes are now Lean-checked theorems from Baek's theorem, with no SAT input (`SYMLEAN/mirror`). Open: no step from a CNF to its Lean class is formalized. |
| 7 | Attribution for Theorem 1, the fivefold overlap and the assembled statement | closed | No matching prior result was found in the sources inspected for Theorem 1, the mirror theorems, the central 34-point theorem or the assembled statement. Sources: arXiv:2506.00224v1 (Subercaseaux, Mackey, Qian, Heule) and its public code; arXiv:2607.02958v1 (Krapivin, Przybocki, Heule); arXiv:2512.24061v1 (B. C. Dumitru) with his generator at commit 9520cea; the Mackey thesis CMU-CS-25-108 (in part); Heule–Scheucher arXiv:2403.00737 (in part); Scheucher arXiv:2105.08406 and arXiv:1807.10848, Subercaseaux et al. arXiv:2403.17370 and arXiv:2311.03645 (text search); Koshelev–Koshka arXiv:2604.20120v1; Baek–Balko (SoCG 2025; in part); Morris–Soltan (2000; Thm 2.6); Georgiev, Gómez-Serrano, Tao, Wagner arXiv:2511.02864 (Problem 6.58); Zeng et al. (SSRN 7334758); Schroeder (Zenodo 22842891; text search); the 2025–26 publication files of M. Heule; and index searches (OpenAlex, Semantic Scholar, arXiv API, erdosproblems.com #107 and its forum thread). Not inspected: the text of the CICM 2025 chapter of arXiv:2506.00224 (not accessible; metadata only), Dumitru's announced second version. The fivefold case is implied by Dumitru's reported, unverified 5^6 run, which has priority. Corrections: the author is B. C. Dumitru, not "D. Bogdan" (8 places); the 32-point mirror lower bound follows from the classical Erdős–Szekeres construction in Lovász's form with mirror-image clusters (checked exactly on one instance); arXiv:2506.00224 §3.2 states a special case of the layer lemma. |
| 8 | Central 34: lane-stratified spot check | partly closed (running) | Started on 1 November: one unit from each of the 242 lanes of `C2P`–`C2P5` that no earlier re-solve had reached (of 281 lanes with certified records; `C2P/LOCAL_L3`, whose pieces close no orbit, left out), re-solved on hash-checked CNFs with both checkers, proofs in the local archive `es7-central34-lanespot-2026-11-01`. 81 of 242 by 1 November 2026, 19:43 UTC, from 81 lanes: all certified, all reproducing the recorded proof (`C2RECHECK`). |
| 9 | Threefold: Lemma 5 and Lemma H6M checked at the CNF level | open | — |
| 10 | Every case except Theorem 2a rests on one encoder | closed in the write-up | Stated as a limitation in the revised `WRITEUP/SYMMETRIC.md` (§3) and in the trust base of the note (not yet committed). |
| – | (not on the list) Lean check of the threefold bookkeeping | closed (reviewed) | `C3LEAN`: `all_roots_covered` proves that all 910 depth-2 roots are covered by the 73,567 leaves (core Lean 4.24.0, `decide +kernel`, axioms `propext` and `Quot.sound`; `C3Cover.lean` `4b64293d…`). Lean does not check certification; that every leaf names a certified record is checked in Python, and the review re-derived the CNF SHA-256 of all 73,707 certified records behind the leaves with 0 mismatches. |
| – | Write-up corrections from §4 (A6-1, A1-F1, A5-2, A4-4 and the rest) | partly closed | Made in revised copies of `WRITEUP/SYMMETRIC.md`, `WRITEUP/CERTIFICATES.md`, the note and the READMEs of `C2C34`, `C2FINAL`, `C4CUT`, `SYM5` and `SYMMAX`, not yet committed. Stale statements remain in some files that were not edited. |

## 6. What is not checked

- During the audit no retained certificate was replayed in full. By 1 November 2026, 19:43 UTC, cake_lpr had been re-run
  on retained proofs in the hexagon re-check (all 120 hull proofs, §5 row 3b) and in the full replay of c5-L1,
  c3hex-15, c3hex-16 and the C4CUT proof (§5 row 1). It has not been re-run on mirror33, mirror34, c5-P1, c5-L2 or the
  hull cover.
- At audit time about 98% of the pieces in the threefold cut and about 98% of the central orbit facts rested on
  recorded verdicts of deleted proofs. The re-checks are samples or targeted re-solves: 2,120 threefold pieces in
  `C3SPOT` (1,337 of them in the cut) and the 204 pieces of §5 row 4 (all certified); 38 central units by 471d5f63a, plus
  the units of §5 rows 3a, 3c, 2 and 8: 224 of the 2,304 central facts by 1 November 2026, 19:43 UTC (§5 row 3d).
- No step from a CNF to its Lean case class is Lean-checked. Encoder soundness rests everywhere on written proofs and
  computational evidence.
- Each case except Theorem 2a rests on one encoder; the fivefold case uses two normal forms of one encoder (A4-3).
- The outputs of the re-check, re-solve and replay jobs of §5 have had no independent pass beyond the replay kit's hash
  checks and the jobs' own round trips (§5 row 3d). The encoder proof was refereed (§5 row 5).
- The auditors' and verifiers' scripts were not reviewed, except where a verifier re-ran them.
- The lower-bound examples give lower bounds only.
- Literature: only the sources listed in §5, row 7.

## 7. Files

- `README.md`; `findings.tsv` (59 findings: component, ID, auditor's and checked severity, whether confirmed, title);
  `reports/` (the seven audits with the verifiers' texts, and the completeness review); `fetch_repo_copies.sh`.
- `A1_reduction/` … `A8_completeness/`: the auditors' scripts and logs, 460 files. `verify_<ID>/` holds the
  verifier's scripts and logs for finding `<ID>`.
- **Reports.** The texts returned by the auditors, the verifiers and the completeness review, lightly edited: machine
  paths replaced by placeholders, internal job names by descriptions, and the audit brief called "the audit rules".
  "Bogdan" in these texts is B. C. Dumitru, the author of arXiv:2512.24061 (§5 row 7). In the trust tables, the
  basis column is the auditor's own classification. "(auditor's label)" marks a certificate label taken from the
  project's logs, not from a replay by the auditor. Where an auditor had filed its own exact computation or test
  under a certificate, written-proof or re-verification label, the row was relabelled "exact computation" or
  "computational evidence"; the auditor's notes are unchanged.
- **Placeholders.** Bare relative paths are relative to `cloud/es7-2026-10-19/results`. In logs and reports, machine
  paths were replaced: `<proof-archives>` is the local proof archive (outside Git); `<central base.cnf>` the central
  base CNF (`SYMZ/zcnf.py rot 17 7 --m 2 --hull`, `b0061e90…`); `<bin>` the directory with CaDiCaL 3.0.1, lrat-check
  (E2 patch) and cake_lpr; `<main-repo>` a local checkout of the main repository and `<audit-2026-10-29>` its
  untracked directory with the logs of the 29 October audit; `<local checkpoint ref>` a local Git ref; `<work>`,
  `<earlier work dir>`, `<night run>`, `<local-tools>` and `<host>` other local locations or the host name.
- **Scripts.** Hard-coded machine paths were replaced by the script's own directory or by environment variables:
  `ES7_RESULTS` (default `.` in the Python scripts; the enclosing results directory in the shell scripts), `ES7_REPO`,
  `PROOF_ARCHIVES`, `BASE_CNF`, `TOOLS_BIN`, `MAIN_REPO`, `AUDIT_1029_DIR`, `PY` (default `python3`). After this
  edit, four light scripts were re-run against the results tree and reproduced their logs byte for byte:
  `A1_reduction/size_arith.py`, `A1_reduction/examples_check.py`, `A3_mirror/check32.py` and
  `A7_examples/check_provenance.py`; `A1_reduction/SizeArith.lean` was recompiled and reproduced its log. Every
  Python and shell file parses and every C file compiles; the other scripts were not re-run.
- **Not copied.**
  - CNFs and proofs of any size. Scripts that read a CNF need it regenerated first; the self-test of
    `A3_mirror/verify_A3-F2/run_verify.sh` also needs its four small benchmark CNFs, which are not included.
  - Files over 1 MB, among them A2's report with the explicit 73,567-piece cut (`a2compose_report.json`, 2.5 MB;
    `a2compose.py` writes it in about 40 s) and A5's 20 binary relabelling maps of 3.3 MB each (written by
    `symmaps.py`).
  - Compiled binaries (the C sources are included), CNF variable maps and other generator outputs, and mutated copies
    of records and encoders (written by `mutate_records.py` and `mutate.py`).
  - 41 byte-identical copies of repository files, which `fetch_repo_copies.sh` restores with a SHA-256 check. The
    pre-review `verify_cuts.py` read from the C4CUT archive is not in Git.
  - Downloaded third-party pages, resource logs (`*.time`), one listing of local scratch paths, and the auditors'
    per-directory `SHA256SUMS.txt` files (two of the logs they list were edited for paths).

## Reproduction

From `cloud/es7-2026-10-19/results`, with `W` a scratch directory:

```sh
bash AUDIT3/fetch_repo_copies.sh
python3 -I AUDIT3/A1_reduction/size_arith.py 600 60
lean AUDIT3/A1_reduction/SizeArith.lean           # Lean 4.24.0, no Mathlib needed
python3 -I AUDIT3/A1_reduction/examples_check.py .
python3 -I -B AUDIT3/A2_threefold/gen_base_stream.py 11 7 $W/base_m11k7.body
python3 -I -B AUDIT3/A2_threefold/a2compose.py $W/base_m11k7.body . C3FINAL/compose_files.txt --report $W/a2compose_report.json
python3 -I AUDIT3/A3_mirror/check32.py
python3 SYMZ/zcnf.py rot 17 7 --m 2 --hull -o $W/base.cnf --map $W/base.json
python3 -I AUDIT3/A5_central_geometry/hashcheck.py $W/base.cnf $W/base.json .
python3 -I AUDIT3/A5_central_geometry/orbitclosure.py $W/base.cnf $W/base.json .
python3 -I AUDIT3/A6_certificates/records_crosscheck.py .
cc -O2 -o AUDIT3/A7_examples/brute_a7 AUDIT3/A7_examples/brute_a7.c
python3 -I AUDIT3/A7_examples/verify_all.py $W/a7
python3 -I AUDIT3/A8_completeness/c2_dependency.py .
```

The scripts that read the proof archive need `PROOF_ARCHIVES`; those that run the solver or the checkers need the
pinned tools of `WRITEUP/CERTIFICATES.md`. The usage line of every script is in its docstring or header comment.

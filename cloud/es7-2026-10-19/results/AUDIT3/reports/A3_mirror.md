# A3: mirror cases (Theorems 2, 2a, 2b)

Component audit, 1 November 2026 (UTC), against `es7-cloud` at 9cf4949a5. Texts returned by the auditor and by the independent verifier of each finding, lightly edited: machine paths replaced by placeholders and internal job names by descriptions; trust-table labels as explained in `../README.md`, §7.

**Component.** MIRROR (Theorems 2, 2a, 2b): SYMZ encoder zcnf.py / zcnf_v1.py with the reflection's point at infinity Z, its written soundness proof, the mirror33 / mirror34 certificates, the 32-point lower example, and the earlier Lean chain for 2a (MIRROR.md)

**Statement audited.** Theorem 2: every set of at least 33 points in general position that is symmetric under a reflection contains 7 points in convex position, and the largest mirror-symmetric 7-gon-free set has exactly 32 points. It is assembled from Theorem 2a (33 points, exactly one point on the axis: CNF `zcnf.py mirror 16 7 --axis 1`, sha e45464ed…73739d02, plus the older Lean chain of MIRROR.md) and Theorem 2b (34 points, no point on the axis: CNF `zcnf_v1.py mirror 17 7`, sha b175eac0…09a6c5b).

**Verdict.** `sound_with_caveats`

## Summary

Verdict: sound with caveats. I found nothing blocking or major in the mirror component.

- **Soundness proof:** I re-derived every step of the written proof for the Z-element encoding, including the axis-point extension and the height-order units. It is correct, though terse (A3-F3).
- **CNF identity:** the recorded hashes reproduce exactly from the recorded commands, and the archived CNFs and LRAT proofs have the recorded hashes. Both proofs end with an empty clause.
- **Own evaluators:** I wrote two exact-arithmetic evaluators of my own, independent of the repository's test scripts. They checked 2,460 configurations on 27 small instances and 128 configurations on the actual certified 33- and 34-point CNFs, including near-extremal sets with only 4 or 5 convex 7-gons. Every clause holds except the clauses for convex 7-gons that are actually present, with exact counts in both directions. Mutation tests show both evaluators catch subtle encoding errors.
- **Variable classes:** an independent recomputation matches the encoder's exactly.
- **Unit clauses:** they are exactly the height-order units.
- **32-point example:** verified exactly, so "exactly 32" stands.
- **Assembly:** the derivation of Theorem 2 from 2a and 2b is correct.

**Caveats:**
- The checker verdicts are solve-time records. I did not replay them because the rules forbid it here.
- No independent replay exists for the 33-point proof, and the claimed replay of the 34-point proof has no log (A3-F1).
- Checker logs are not tied to file hashes (A3-F2).
- Theorem 2b rests on one certificate plus a hand soundness proof, not a Lean proof (A3-F5).
- The old Lean chain for 2a depends on proofs that were not retained. Theorem 2 does not need it (A3-F9).
- One novelty wording issue (A3-F4).

All scripts and logs are in AUDIT3/A3_mirror/: myeval.py, myuf.py, mkconf.py, evalbig.c, mutate.py, check32.py, regen_hash.sh, run_small.sh, run_big.sh, and the logs in gen/, small/, big/ and mut/.

## Trust table

| # | claim | basis | notes |
|---|---|---|---|
| 0 | Assembly: Theorem 2 follows from 2a and 2b. By general position at most 2 points lie on the axis. With b=0 there are at least 17 pairs, giving a 34-point axis-free subset. With b=1 or 2 there are at least 16 pairs; keeping 16 pairs and one axis point gives 33 points. Subsets keep general position, the symmetry and freedom from 7-gons. | written proof, re-derived by the auditor | Parity cases rechecked: 2k>=33 gives k>=17; 2k+1>=33 gives k>=16; 2k+2>=33 gives k>=16. Finite sets admit no glide reflections. |
| 1 | Lower example: SYMMAX/mirror_32points.txt is mirror-symmetric in the y-axis, has no point on the axis, is in general position with distinct pair heights, and has no 7 points in convex position. | exact computation (auditor's DP) | Fully re-checked with my exact integer DP (check32.py; largest convex subset = 6). The DP was cross-validated against brute force on 300 random sets. The same real set also satisfies all 11,833,512 clauses of `zcnf.py mirror 16 7` (evalbig: 0 violated). |
| 2 | Encoding soundness (SYMZ/README.md §1, including the axis-point extension): every real mirror-symmetric configuration in general position, labelled in the normal form, satisfies every clause when given its true chirotope (with Z=(0,1,0)) and true convexity values. The only exceptions are K-clauses of convex 7-gons actually present. | written proof, re-derived by the auditor | Each step re-derived. det(vZ,vp,vq)=y_p-y_q, so the only zero triples are {Z,L_i,R_i}. A=diag(1,-1,1) has det -1 and A vZ=-vZ: point triples flip sign, Z-triples keep it, axis points are fixed. vR-vL=2a vZ gives chi(Z,L,q)=chi(R,L,q)=chi(Z,R,q) for every q, axis points included. Three-term Grassmann-Pluecker relation; both 8-clause families of the fast path checked by hand. Interiority clauses via the 4-term Cramer identity plus the functional w+eps*x, which is positive on Z. 4-point and Caratheodory convexity. Height-order units. The proof is correct but terse (see findings). |
| 3 | The implementation matches the written encoding. Variable classes are exactly the orbits under the group and pair identities, with no extra merges (2616 and 2856 classes, equal to the closed formula (C(N,3)-t*axis)/2 + t*axis - C(t,2) + [axis=2]). All clause families are valid. | exact computation (independent recomputation) | An independent signed BFS (myuf.py) reproduces partition, signs and numbering with 0 mismatches. Exact clause evaluation: 2,460 random configurations on 27 small instances (K=5,6,7; 0, 1, 2 axis points), and 64 configurations each on the archived certified 33- and 34-point CNFs. All non-K clauses are true, and violated clauses equal the K-clauses of canonical convex 7-sets in both directions. 14 mutation runs: unsound mutants are caught, the sound weakening passes. |
| 4 | The normal-form (symmetry-breaking) units are exactly the 120 (33 points) / 136 (34 points) units chi(Z,L_o,L_o2)=+ for o<o2, i.e. pairs by decreasing height, and nothing else. | written proof, re-derived by the auditor | Decoded from the archived CNFs against the variable map (big/units_decode.log). Valid because pair heights are distinct under general position. No unit constrains the axis point. |
| 5 | CNF identity. `zcnf.py mirror 16 7 --axis 1` gives e45464ed…73739d02. `zcnf_v1.py mirror 17 7` gives b175eac0…09a6c5b. `zcnf.py mirror 17 7` gives 1b61bf2f…92825 with an identical clause body. The archived .zst files decompress to these hashes. | exact computation (full regeneration) | Full regeneration by me, not a sample: 22.9 s / 157 MB and 28 s / 217 MB, within the 2 min / 1.5 GB limit. Clause bodies of v1 and final are identical (sha d3882e64…). Archive hashes checked by streaming. |
| 6 | The mirror33 CNF (e45464ed…) is UNSAT. | certificate accepted by both checkers (auditor's label) | The retained LRAT proof matches its record (sha e1b2689d…, 4,120,793,950 bytes) and ends with an empty-clause line that carries hints. Logs record lrat-check VERIFIED and cake_lpr 's VERIFIED UNSAT', but carry no input hashes. I did not replay them: the rules forbid cake_lpr and loading CNFs over 50 MB. No independent replay is on record. |
| 7 | The mirror34 CNF (b175eac0… and the comment-variant 1b61bf2f…) is UNSAT. | certificate accepted by both checkers (auditor's label) | Proof sha 98e4d02a…, 4,373,364,691 bytes, verified by me; it ends with the empty clause. Both checkers ran on both files (logs). The claimed independent lrat-check replay (45.45 s) has no log in the repository. Not replayed by me. |
| 8 | Theorem 2a, old chain: the Lean reduction (encoding soundness, normal forms, reduction from an arbitrary line, case split, leaf cover) proves MirrorExclusionLine from the CNF facts. | Lean-checked per the project's records (not re-run by the auditor) | Taken from the MIRROR.md / V2-L records. I read the statement and definitions (reflLine is a correct reflection; GeneralPosition and HasConvexNGon are the standard definitions). Not replayed: there is no built .lake, and the Mathlib import and tree modules (2.98 GB peak) exceed the 1.5 GB per-process limit. |
| 9 | Theorem 2a, old chain: about 75,000 CNF facts are UNSAT. | recorded verdict only (proofs not retained) | The proof files were not retained. The emission and driver steps are unverified, and V3 leaf files are equisatisfiable with the Lean terms but not byte-identical (MIRROR.md §6). Not needed for Theorem 2, since the mirror33 certificate covers 2a independently. |
| 10 | Affine (non-orthogonal) reflections are also covered (the remark under Corollary 3). | written proof, re-derived by the auditor | Averaging the inner product over {id, sigma} makes sigma an orthogonal reflection. General position and convex position are affine-invariant. |

## Findings

### A3-F1 (minor): No independent replay is on record for the 33-point mirror proof; the 34-point 'independent replay' has no log

mirror33 (Theorem 2a, new proof) was checked only at solve time (chk_m33_def_*.out). For mirror34, CERTIFICATES.md, SYMMETRIC.md §3 and the SYMZ README cite an 'independent audit: lrat-check replay, exit 0, 45.45 s, hashes matched', but no log of that replay exists anywhere under results/. My rules did not allow a replay (no cake_lpr, no loading CNFs over 50 MB). Both proofs are retained and their archive hashes are correct, so a replay is possible. This does not threaten the claim; it is a gap in provenance.

*Evidence.* grep for m33_def / e1b2689d / e45464ed finds only the solve-time logs, sha256.txt, README.md and CERTIFICATES.md; grep for 45.45 finds no mirror log. Archived proofs re-hashed: AUDIT3/A3_mirror/big/units_decode.log

*Suggested fix.* Replay lrat-check and cake_lpr on both archived (CNF, proof) pairs on a machine with at least 32 GB, and commit the logs together with the input SHA-256s.

**Independent check:** real = yes; severity minor -> **minor**.

The finding has two halves. The mirror33 half is correct. The mirror34 half is partly wrong.

(1) Mirror33 (Theorem 2a, new proof) was never replayed independently. The only checker verdicts are the solve-time chk_m33_def_lrat-check.out and chk_m33_def_cake_lpr.out, written in the solving session at 12:37 and 12:42 KST on 2026-10-29. I searched for any other record and found none. Places searched:
- the HEAD tree (9cf4949a5);
- every git ref, including local checkpoint refs;
- the main repo's experiments/ folder (text files under 5 MB);
- the proof archive;
- the original solving work directory.

The timeline explains why. The 2026-10-29 independent audit ran 03:18–03:38Z (12:18–12:38 KST) and wrote its mirror34 replay at 12:34:24. The mirror33 proof file was only finished at 12:36:25. The project documents do not claim a replay for mirror33; SYMMETRIC.md §3 says only "accepted by both checkers". So this is a missing check, not an overclaim.

(2) The claim that the 34-point "independent replay" has no log is incorrect as stated. It is literally true that no log exists under results/. But the log does exist:
- Location: <audit-2026-10-29>/mirror34-lrat-replay.log and .json, plus REPORT.md.
- Hashes: the SHA-256s of the CNF (b175eac0…), the proof (98e4d02a…) and lrat-check (f2046212…) all equal those in CERTIFICATES.md.
- Result: exit 0, 45.4486 s, which matches the cited 45.45 s.
- Statistics: the lrat-check counts (parsed/VERIFIED/Added 41860266/Deleted 36974924/Max live 16642786) are identical to the solve-time log.

The real defect is narrower. That record is untracked in git (status "??"). It is on no branch and survives only in two local checkpoint refs. No project document cites where it is. The suggested fix should therefore change: commit or cite the existing mirror34 replay record (it covers lrat-check only; cake_lpr was not rerun), and run a fresh replay of mirror33.

Neither half threatens the claim:
- Both proofs have solve-time verdicts from lrat-check and from the CakeML-verified cake_lpr.
- I re-hashed all four archived mirror files myself by streaming them. Each one decompresses to its recorded SHA-256 and byte count, so a replay is possible.
- Theorem 2a also has the older Lean proof chain.

So this is a provenance gap: minor.

I did not replay any proof myself. The audit rules forbid cake_lpr and loading CNFs over 50 MB, and lrat-check parses the whole 518–620 MB formula.

*Verifier's evidence.* Replay record (exists, uncommitted):
- Files: <audit-2026-10-29>/mirror34-lrat-replay.log (sha256 323d79bd…) and mirror34-lrat-replay.json (sha256 77949512…).
- Git status in the main working tree: "?? <audit-2026-10-29>/".
- The directory is not in the HEAD 9cf4949a5 tree. Only two local checkpoint refs contain it, and those copies are byte-identical to the files on disk.
- Cited nowhere: CERTIFICATES.md:39, SYMZ/README.md:108-109, SYMMETRIC.md:56,163 and note/symmetric_es7.tex:239-240 claim the replay but give no path.
- The JSON records exit_code 0 and elapsed 45.448623 s. Its three hashes appear in CERTIFICATES.md. Its lrat-check statistics equal those in results/SYMZ/logs/chk_mr34_def_lrat-check.out.
- The audit's REPORT.md says cake_lpr was "not rerun here" and that "the older 33-point proof chain was not fully replayed". Its session.json gives 03:18:25Z to 03:38:06Z.

Mirror33:
- m33_def.lrat has mtime 12:36:25 KST. The solve-time checks have mtimes 12:37:34 and 12:42:02, in <earlier work dir>/c2c/.
- No other m33 check record was found by git grep over all refs, the experiments/ search, the archive mirror33/ folder (solve-time logs only) or the work directory search.

My scripts and logs:
- AUDIT3/A3_mirror/verify_A3-F1/provenance_check.py and provenance_check.log.
- AUDIT3/A3_mirror/verify_A3-F1/rehash_archives.sh and rehash_archives.log. All four checks are OK:
  - m33_def.lrat: e1b2689d…, 4,120,793,950 bytes
  - m_t16k7a1.cnf: e45464ed…, 518,452,724 bytes
  - mr34_def.lrat: 98e4d02a…, 4,373,364,691 bytes
  - m_t17k7.cnf: b175eac0…, 620,842,936 bytes
  - The compressed archive SHA-256s also match.

### A3-F2 (minor): Checker logs are not tied to file hashes

The chk.sh logs (lrat-check, cake_lpr) record neither the input paths nor their hashes. Which files the verdicts apply to rests on chk.sh and the CERTIFICATES.md text. Partial binding I could establish: each lrat-check log reports the formula size from the CNF header (695928/14080656; 838032/16642456), and its 'Added clauses' count equals the last clause id of the archived proof (35,510,866; 41,860,266). For the cake_lpr logs there is no such binding at all.

*Evidence.* SYMZ/logs/chk_m33_def_*.out, chk_mr34_def_*.out; last lines of the archived proofs in AUDIT3/A3_mirror/big/m33_def.lrat.tail and mr34_def.lrat.tail

*Suggested fix.* Have chk.sh write the sha256 of the CNF and the proof, and the command line, into each checker log.

**Independent check:** real = yes; severity minor -> **minor**.

The finding is correct, and "minor" is the right severity. Two qualifications: the lrat-check binding is stronger than the auditor says, and the gap that remains is slightly different from the one described.

1. **What the logs record (confirmed).** chk.sh writes only three things to each log: the checker's own output, the `/usr/bin/time -l` usage figures, and a line of the form "exit N wall N s". It records no input paths, hashes or command line. It also records no checker-binary hash, which the auditor did not mention. The repository logs are byte-identical to the copies in the proof archive.

2. **The header line binds only the header (confirmed).** In lrat-check.c at 2e3b2dc, the "parsed a formula" line prints the values read from "p cnf", not the number of clauses actually parsed. I tested this: with the header changed to 430 clauses while 429 were present, lrat-check printed 430 and still said VERIFIED.

3. **The binding to the archived proofs is stronger than reported.** I wrote an independent counter (lratstat.c) that applies lrat-check's counting rules. It reproduced the "Added / Deleted / Max live" line of the hashed lrat-check binary exactly on 4 small proofs, plus a double-deletion case and a wrong-header case. I then streamed both archived proofs through it, computing SHA-256 in the same pass. The hashes match the records, and all three statistics match the logs exactly:
   - **33-point proof:**
     - Added = 35,510,866: the 14,080,656 CNF clauses plus 21,430,210 lemma lines with contiguous ids.
     - Deleted = 32,165,860.
     - Max live = 14,080,967.
   - **34-point proof:** Added 41,860,266; Deleted 36,974,924; Max live 16,642,786.
   - **Solver logs:** they name the CNF and proof files and give the header. They also give the proof size, 4,120,793,950 and 4,373,364,691 bytes, equal to the archived sizes, and added/deleted counts equal to those in the proofs.
   - So the auditor's "Added equals the last clause id" holds, but it is only part of the match.

4. **What remains unbound (a real gap).**
   - **CNF content:** only the header and the clause count are tied to the logs. A CNF with the same counts but different literals would produce the same log.
   - **cake_lpr:** its log contains only "s VERIFIED UNSAT", the usage figures and the exit line. It is linked to lrat-check only because chk.sh runs both checkers in one invocation with the same arguments and tag.
   - **The 34-point "final" logs:** the chk_mr34_final_* logs are identical to the chk_mr34_def_* logs except for timing and resource lines. Nothing in them shows they were run on m34_final.cnf (1b61bf2f). That file differs from the original only in its comment line, which lrat-check skips.
   - **The 33-point case:** no replay with recorded hashes exists (see A3-F1). The verdict's link to the archived CNF therefore rests on the documentation.
   - **Side note:** the committed chk.sh calls binaries in `$D/../local/bin`, which does not exist in the repository, so the script cannot run as committed.

5. **Why minor and not major.** The claim is not threatened:
   - the archived files carry verified hashes;
   - three independent lrat-check statistics plus the header match them;
   - a mix-up would require a CNF with identical counts but different content, and nothing suggests one existed.

   The gap can be closed by re-running both checkers on the decompressed archive files with SHA-256 and the command line logged. The suggested change to chk.sh only helps future runs. The existing 33-point certificate and the m34_final claim need that re-run.

*Verifier's evidence.* Files I read:
- $R/SYMZ/chk.sh (no hash, path or command logging).
- $R/SYMZ/logs/chk_{m33_def,mr34_def,mr34_final}_{lrat-check,cake_lpr}.out (byte-identical to the archive copies in <proof-archives>/es7-symmetry/mirror3{3,4}/).
- $R/SYMZ/logs/cad_m33_def.out lines 18-26 and 381-384, and cad_mr34_def.out lines 19-26 and 228-231 (file names, header, LRAT added/deleted/bytes).
- <local-tools>/sat/src/drat-trim/lrat-check.c at 2e3b2dc, lines 247-272 and 396-506.

Scripts and outputs are in AUDIT3/A3_mirror/verify_A3-F2/: cnfstat.c, lratstat.c, run_verify.sh, run_verify.log, cnf_m_t16k7a1.stat, cnf_m_t17k7.stat, lrat_m33_def.stat, lrat_mr34_def.stat, and selftest/.
- Self-test: lratstat matches the hashed lrat-check (sha f2046212) on uuf-100-1, uuf-100-5, php8 and r3, and on the double-deletion and wrong-header cases.

Archive streams, recomputed:
- m_t16k7a1.cnf: sha e45464ed..., p cnf 695928 14080656, 14,080,656 clauses present, no empty clause.
- m_t17k7.cnf: sha b175eac0..., p cnf 838032 16642456, 16,642,456 clauses present.
- m33_def.lrat: sha e1b2689d..., 4,120,793,950 bytes; 21,430,210 additions with contiguous ids 14,080,657 to 35,510,866; 32,165,860 deleted ids; last line is the empty clause. Recomputed: Added 35510866, Deleted 32165860, Max live 14080967, equal to the log.
- mr34_def.lrat: sha 98e4d02a..., 4,373,364,691 bytes; 25,217,810 additions with ids 16,642,457 to 41,860,266; 36,974,924 deleted ids; last line is the empty clause. Recomputed: 41860266 / 36974924 / 16642786, equal to the log.

Log comparison:
- chk_mr34_final_* differs from chk_mr34_def_* only in timing and resource lines.
- The cake_lpr logs contain only "s VERIFIED UNSAT", the usage figures and "exit 0 wall N s".

### A3-F3 (minor): The written soundness proof is correct but leaves several steps implicit

I checked SYMZ/README.md §1 line by line and every stated fact is true. Implicit steps: (a) the overall argument that X_v := chi(root) is well defined (each union-find edge is a valid identity, and validity is closed under composition), with conv set to true convexity; (b) the existence of the normal-form labelling for every configuration (a rigid motion puts the axis on the y-axis, pairs are labelled by decreasing height, left point first); (c) in item 5, the 4-term identity det(q,r,t)p - det(p,r,t)q + det(p,q,t)r - det(p,q,r)t = 0 that turns the positive functional into the interiority clauses, and the skipping of 4-sets that contain a zero triple; (d) the 16 hand-written fast-path Grassmann-Pluecker clauses are not justified separately from the enumerated generic path (I verified them by hand, and mutation M6 confirms they are tested); (e) item 1 does not mention axis-point heights explicitly (an axis point at a pair's height is collinear with that pair). The LaTeX note's items (i)-(v) have the same terseness.

*Evidence.* zcnf.py lines 159-200, 226-273, 330-351; my re-derivation is summarized in trust items 3-5

*Suggested fix.* Add a short paragraph that states the satisfying assignment explicitly, and give the Cramer identity and the fast-path clause derivation.

**Independent check:** real = yes; severity minor -> **minor**.

The main claim holds. The proof in SYMZ/README.md §1 is correct, and the LaTeX items (i)-(v) are correct too. The steps the auditor lists are either left implicit or only pointed at. I re-derived each step and checked it with exact arithmetic.

What I confirmed:
- **Identities (c):** the 4-term Cramer identity, written in the literal order add_a4 uses (det(t,q,r)p + det(p,t,r)q + det(p,q,t)r - det(p,q,r)t = 0), expands to the zero polynomial. So does the 3-term Grassmann-Pluecker relation with the code's signs k = (+1,-1,+1). A wrong-sign control does not vanish.
- **Satisfying assignment (a):** the assignment the proof leaves implicit works. It is X_class := chi(member)*sign for each class and conv := true convexity. I tested 300 random exact configurations over 10 mirror instances (t = 4..7, K = 5..7, with 0, 1 and 2 axis points):
  - every union-find class is sign-consistent;
  - the zero triples are exactly {Z, L_i, R_i}, axis points included;
  - every clause holds except the K-set clauses of K-sets that really are convex, with exact counts in both directions.
- **Fast path (d):** the 16 hand-written clauses are correct.
  - In all 46,080 abstract literal configurations they equal the generic enumeration and the semantic GP condition.
  - In a copy of zcnf.py with the fast path disabled, the clause multiset is identical on 9 instances. On those instances the fast path writes 60-84% of all clauses.

Corrections to the finding:
- **(a)** README item 6 states the conv half explicitly. Only the triple-variable assignment and the fact that it is well defined are implicit.
- **(b)** The normal form is stated: the Setting plus item 7. Only the one-line existence argument is missing (a rigid motion, and distinct heights by item 1).
- **(c)** Item 5 already says to skip 4-sets with a zero triple ("without a zero triple"). Dropping clauses needs no justification for soundness. Only the Cramer step is genuinely missing.
- **(d)** The auditor's statement that "mutation M6 confirms they are tested" is wrong.
  - M6 flips the middle k, but the fast path throws k away (`(_, (l12,l34)), ... = terms`).
  - On 9 instances the fast-path clauses do not change under M6. M6 is caught only through the generic path.
  - The fast path is still tested by evaluating clauses on real configurations: a sign mutant in the fast path gave 3,311 and 6,656 unexplained violations in my evaluator.
- **(e)** README item 1 says "a second point at the height of a pair would put three points on a line", which already covers an axis point at a pair's height. Only the trivial case of two axis points is not stated. (e) does hold in full for the LaTeX item (i): it mentions neither general position nor axis points, and the LaTeX encoding paragraph leaves out the axis point entirely, although Theorem M33 needs it.

Two more small imprecisions: 'w' is never defined (README item 5 and the LaTeX), and "second point" should read "another point".

Severity: nothing here threatens Theorem 2, 2a or 2b, and every omitted step is routine. I keep minor, at the low end close to note. The reasons not to go lower:
- The soundness of the encoding behind Theorem 2b rests only on this written proof, with no Lean.
- The LaTeX version is even terser.
- The suggested fix is cheap and worthwhile: state the assignment explicitly, give the Cramer identity, and add a sentence on the fast path.

*Verifier's evidence.* All scripts and logs are in AUDIT3/A3_mirror/verify_A3-F3/.
- **identities.py / identities.log:** exact polynomial expansion. Cramer identity: zero in all 3 coordinates. GP with k = (+1,-1,+1): zero. Control with k = (+1,+1,+1): nonzero. RESULT PASS.
- **fastpath_check.py / fastpath_check.log:**
  - Part A: 46,080 configurations, 0 mismatches.
  - Part B, on 9 mirror instances (t = 4..6, axis 0/1/2), run on zcnf_copy.py (sha256 13d6c162..., identical to SYMZ/zcnf.py):
    - original vs. no-fast-path copy: identical clause multisets on all 9;
    - fast-path clauses unchanged under M6: True on all 9;
    - M6 changes 1,052-8,470 non-fast clauses.
  - The GP code in zcnf_v1.py, which generated the 34-point CNF, is identical.
- **assign_check.py / assign_check.log:**
  - 10 instances x 30 configurations: e1_bad = 0, e2_bad = 0, e3_unexplained = 0, e3_missing = 0. Convex K-sets range from 314 to 6,083 per instance.
  - Fast-path sign mutant: 3,311 and 6,656 unexplained violations. RESULT PASS.
- **Text cited:**
  - README §1 item 1 ("a second point at the height of a pair..."), item 5 ("without a zero triple"; 'w' undefined), item 6 (conv := actual convexity stated).
  - symmetric_es7.tex lines 100-113: no axis point and no general-position mention.
  - zcnf.py line 240 discards k in the fast path.

### A3-F4 (minor): The Theorem 2b heading in SYMMETRIC.md uses a bare novelty word

SYMMETRIC.md §1 heads Theorem 2b '(34 points, no point on the axis; new, results/SYMZ)'. The project's own rule, and that of the audit rules, is to say 'no matching prior result found in the sources inspected' rather than 'new'. The scope paragraph of SYMMETRIC.md mitigates this, but the heading still reads as a priority claim.

*Evidence.* WRITEUP/SYMMETRIC.md line 53

*Suggested fix.* Replace 'new' with 'proved here; no matching prior result found in the sources of §5'.

**Independent check:** real = yes; severity minor -> **minor**.

The finding is correct and minor is the right severity. Line 53 of SYMMETRIC.md reads "**Theorem 2b (34 points, no point on the axis; new, `results/SYMZ`).**" That is a bare novelty word in a theorem heading. Two rules forbid it:
- the audit rules: say "no matching prior result found in the sources inspected" and list the sources.
- The project's own rule in LIT/TASK.md line 36: "never claim priority or novelty". MIRROR.md follows it with "We did not find prior work stating ... No priority is claimed."

The Scope paragraph helps less than the auditor implies. Its disclaimer (lines 10-12) covers only the phrase "No matching prior result found", and that phrase never appears anywhere else in SYMMETRIC.md. So no sentence in the document literally carries the disclaimer, and it does not reach the heading's "new". Only the general hedge at the end of §5 ("priority statements stay provisional") applies.

The likely origin is innocent. Git history shows the heading came in with commit 189ab709a, the "correctness and novelty audit" revision. Before that commit, the axis-free 34-point case was listed as open. So "new" probably meant "newly proved in this revision", like line 47's "New proof of 2026-10-29". But Theorem 2a has an older proof to contrast with; Theorem 2b has none. A reader therefore sees "new" as a claim of a new result, which is exactly the ambiguity the rule exists to prevent.

The problem is confined to this one heading:
- The same theorem in SYMZ/README.md (line 5) and in the LaTeX note (thm:M34, line 92) has no novelty word.
- The other uses of "new" in SYMMETRIC.md are chronological or hedged: lines 47, 164 and 175 are chronological, line 98 is hedged ("may be new"), and line 110 is a negation.

The claim is unhedged but not shown to be false. My own literature check (two web searches plus the full HTML text of arXiv:2506.00224v1) found no prior result on reflection-symmetric sets without a convex 7-gon:
- arXiv:2506.00224 treats only rotational symmetry and says nothing about 33 or 34 points.
- The only axial-symmetry hit, arXiv:2604.20120, is about empty hexagons, a different problem.
- The CICM proceedings version was not checked.

So the wording issue does not threaten Theorem 2b or Theorem 2, which fits minor: a fixable imprecision. The auditor's suggested fix works. It would read better if it also said what each §5 source covers, for example that arXiv:2506.00224 studies only rotational symmetry.

*Verifier's evidence.* Verification script and output:
- AUDIT3/A3_mirror/verify_A3-F4/check_novelty_wording.py
- AUDIT3/A3_mirror/verify_A3-F4/check_novelty_wording.log (all checks pass)

Paths below are relative to R = results:
- R/WRITEUP/SYMMETRIC.md:53 is exactly "**Theorem 2b (34 points, no point on the axis; new, `results/SYMZ`).**"
- R/WRITEUP/SYMMETRIC.md:10-12 is the Scope disclaimer. It covers only the phrase "No matching prior result found", which appears nowhere else in the file.
- R/WRITEUP/SYMMETRIC.md:217 says "priority statements stay provisional".
- Other whole-word uses of "new" in SYMMETRIC.md: lines 47, 164 and 175 are chronological, line 98 is hedged ("may be new"), line 110 is a negation.
- Rules: the audit rules; R/LIT/TASK.md:36 ("never claim priority or novelty"); model wording in R/WRITEUP/MIRROR.md:77-88.
- The same theorem without "new": R/SYMZ/README.md:5 and R/WRITEUP/note/symmetric_es7.tex:92-93 (thm:M34).
- History: commit 189ab709a introduced the heading. In its parent (8a88ed9df), the axis-free 34-point mirror case was listed as open.
- Literature check: two web searches and a WebFetch of arxiv.org/html/2506.00224v1. That paper covers only s-fold rotation and makes no claim about 33 or 34 points. arXiv:2604.20120's axial-symmetry result concerns empty hexagons. No prior mirror-symmetric 7-gon result was found.

### A3-F5 (note): Theorem 2b rests on a single computer proof whose encoding soundness is a hand proof, not a Lean proof

Unlike 2a, 2b has one proof. Its trust base is: (1) the written soundness of zcnf_v1.py, which I re-derived; (2) generator and file identity, which I regenerated; (3) the LRAT certificate checked at solve time by lrat-check and cake_lpr. My independent exact evaluations of the archived 34-point CNF found every clause valid on 64 real configurations. These include near-extremal ones (the 32-point set plus one pair) with only 4 or 5 convex 7-gons, where all other clauses hold. A Lean formalization of the zcnf mirror soundness would raise this to lean_checked; it is optional.

*Evidence.* AUDIT3/A3_mirror/big/m34.eval.log

### A3-F6 (note): Earlier reviews of SYMZ left no committed outputs

SYMZ/README.md §2 and REVIEW.md cite two source audits, an exact clause check of 240 configurations, 13 evaluations of the real 33-point CNF (review/evalcnf.c) and five mutation tests. Only the scripts review/indep.py and evalcnf.c are committed, with no logs. This audit independently supersedes them with 2,460 + 128 exact configurations and 14 mutation runs, all logged in my directory.

*Evidence.* SYMZ/review/ contains only indep.py and evalcnf.c

### A3-F7 (note): tau() maps the axis point to Z's index

In the 33-point instance tau(32) = 33 = Z. Every current call site is guarded (is_zero checks a,b < NP; the centre loop runs over range(NP)), so the output is unaffected. This is a latent hazard for future edits. Already noted in REVIEW.md.

*Evidence.* zcnf.py lines 122-130, 174

### A3-F8 (note): The model is tight at the extremal example; the binary clauses are understood

The real 7-gon-free 32-point mirror set satisfies all 11,833,512 clauses of `zcnf.py mirror 16 7` exactly, so the encoding is not over-constrained at the extremal size. The 240 (33-point) and 272 (34-point) binary clauses are the 4-set convexity clauses of the trapezoids {L_i,R_i,L_j,R_j}, whose four triples fall into one class. Both patterns are convex, so conv is forced true, which is valid.

*Evidence.* AUDIT3/A3_mirror/big/m32.eval.log

### A3-F9 (note): The old Lean chain for 2a depends on unretained verdicts; Theorem 2 does not need it

MIRROR.md's chain is Lean-checked (per its records) from about 75,000 CNF facts. Their proofs are gone, the emission and driver steps are unverified, and the V3 leaf files are not byte-identical to the Lean terms (acknowledged in MIRROR.md §6). I could not replay the Lean part within limits. Since the retained mirror33 certificate proves 2a independently, this affects only the 'two independent proofs' wording, not Theorem 2.

## Tests run by the auditor

- Regenerated `zcnf.py mirror 16 7 --axis 1` (22.9 s, 157 MB): sha256 e45464ed…73739d02 matches. Regenerated `zcnf_v1.py mirror 17 7` (27.9 s, 217 MB): b175eac0…09a6c5b matches. Regenerated `zcnf.py mirror 17 7`: 1b61bf2f…92825 matches. Clause bodies of v1 and final are identical (d3882e64…). Logs in AUDIT3/A3_mirror/gen/*.log.
- Streamed the archive: m_t16k7a1.cnf.zst decompresses to e45464ed… and m_t17k7.cnf.zst to b175eac0…. m33_def.lrat.zst gives e1b2689d…, 4,120,793,950 bytes; mr34_def.lrat.zst gives 98e4d02a…, 4,373,364,691 bytes. Both proofs end with an empty-clause line that has hints.
- myuf.py: an independent signed BFS of the identifications versus the zcnf maps (t=16 axis 1; t=17 axis 0 with both generators; t=8 axis 2; t=4 axis 1). Partition, sign and numbering mismatches: 0. Class counts equal the closed formula.
- myeval.py (exact Python evaluator, convexity by hull-edge count): 27 small instances (t=3..8, K=5,6,7, axis 0/1/2), 2,460 random exact configurations, 226 of them without a convex K-gon. 0 failures; violated clauses (377,568) equal canonical convex K-sets (377,568).
- evalbig.c (64 configurations in parallel per pass; independent numbering of convexity variables; convexity by edge count, cross-checked against the triangle criterion and Caratheodory) on the archived certified CNFs. 33 points: 64 configurations (21 = 32-point set plus an axis point at various heights, 23 uniform, 10 near-degenerate, 10 near-circle): PASS, 0 unexplained violations; per configuration, violated clauses equal canonical convex 7-sets. 34 points: 64 configurations (21 = 32-point set plus an extra pair, some with only 4 or 5 convex 7-gons): PASS. K-type clauses equal canonical 7-sets (2,136,304 / 2,689,808).
- evalbig on the real 32-point mirror set against `zcnf.py mirror 16 7`: 0 of 11,833,512 clauses violated.
- Exact DP cross-check: for all 128 big-CNF configurations, the largest convex subset is at least 7 exactly when evalbig counts convex 7-sets.
- Decoded the unit clauses of both archived CNFs: exactly the 120 / 136 height-order units chi(Z,L_o,L_o2)=+.
- Mutation tests: 9 mutated zcnf.py copies times 3 instances with myeval, and 5 mutants with evalbig. Unsound mutants are caught by the generator's contradiction check (group signs; axis-point swap with 2 axis points) or by the evaluators (reversed pair identity, reversed units, interiority sign, middle GP sign, a too-wide 4-point convex pattern list). The sound weakening (axis-point identities dropped) and the no-op cases pass.
- check32.py on SYMMAX/mirror_32points.txt: symmetric, general position, distinct heights, largest convex subset 6. The DP was validated against brute force on 300 random sets.
- Known-value CaDiCaL runs on small hexagon instances: mirror 10 points no axis SAT, 12 points no axis UNSAT, 12 points with 2 axis points SAT, 11 points with 1 axis point SAT, 13 points with 1 axis point UNSAT. All agree with the README.


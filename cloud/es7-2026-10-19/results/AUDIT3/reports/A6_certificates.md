# A6: certificate trail

Component audit, 1 November 2026 (UTC), against `es7-cloud` at 471d5f63a. Texts returned by the auditor and by the independent verifier of each finding, lightly edited: machine paths replaced by placeholders and internal job names by descriptions; trust-table labels as explained in `../README.md`, §7.

**Component.** CERTIFICATE TRAIL (A6): retained proof archives, checker logs vs recorded (CNF hash, proof hash) pairs, SYMMETRIC.md §3 replay and retention claims, tool versions

**Statement audited.** The audit covered every retained proof in WRITEUP/CERTIFICATES.md, C4CUT (README, final.json), C2FINAL/pilot/out.jsonl and C2FINAL/sample/*.jsonl, leaving out the 120 central34-hull archives, which another job checks. For each one it asked four things: (1) does the archive file exist under "<proof-archives>/" with the recorded SHA-256; (2) do the checker logs in the repository match the recorded (formula hash, proof hash) pairs; (3) do the claims in SYMMETRIC.md §3 ("Checks actually replayed", "Retained proofs") follow from the logs; (4) which certificates are bound to a hashed CNF, and which tool versions are recorded.

**Verdict.** `sound_with_caveats`

## Summary

I found no integrity failure in the certificate trail. All 55 in-scope archives exist with the recorded size and SHA-256 (the 120 central34-hull archives were left to the other job), and every one decompresses to the recorded CNF or proof hash. The binding from logs to archives also holds. For mirror34, mirror33, P1, L1 and the cover, each lrat-check log's formula size and Added/Deleted counts, and each CaDiCaL log's added/deleted/bytes, equal those of the archived proof exactly. Every generator CNF I could regenerate came out byte-identical: mirror34 (both versions, same clauses), mirror33, both c5 CNFs, the c4 base and map, and both c3hex CNFs. The cover and all 38 re-solved unit CNF hashes rebuild from the base. The C4 CNF is exactly the base plus the six verified cuts. I replayed both c3hex certificates with lrat-check; the binary rejects the E2 forged proof. All 31 sample re-solves reproduce their cloud records byte-for-byte. The C3SPOT figures recount exactly.

Caveats:
- **Major (A6-1):** SYMMETRIC.md §3 and CERTIFICATES.md predate the central-34 completion and the C4CUT certificate. Most central-34 parallelogram units rest on recorded verdicts with deleted proofs; only 38 units were re-solved with archived proofs. §3 must say so before the overall claim is made.
- **Minor (A6-2 to A6-6):**
  - The checker logs carry no input hashes, and the cake_lpr verdicts can be tied to the recorded pairs only by file name.
  - C4CUT has no raw checker logs, and its archive hashes are not recorded in the repository.
  - The 2026-10-29 audit replays have no logs.
  - chk_c3hex.log is not in the repository.
  - The sample is still missing 3 Q units, and its draw script is not committed.

Tool versions recorded: CaDiCaL 3.0.1 c6073042 (printed in every solver log), lrat-check 2e3b2dc with the E2 patch, and cake_lpr a36874a8. The binary hashes match the records. The checker logs and the pilot, sample and C4CUT JSON records do not record tool identity. All scripts and logs are in AUDIT3/A6_certificates/.

## Trust table

| # | claim | basis | notes |
|---|---|---|---|
| 0 | Retained-proof integrity (SYMMETRIC.md §3 'Retained proofs'). The 55 in-scope archive files (15 from CERTIFICATES.md, L2, 2 from C4CUT, 7 pilot, 31 sample) exist, have the recorded size and archive SHA-256, and decompress to the recorded CNF/proof SHA-256. | exact computation (all 55 in-scope files) | All 55 in-scope files were rechecked: shasum -a 256 one file at a time, and zstd -dc \| shasum for every round trip. There were 0 mismatches, and all 8 CNF headers match. The 120 central34-hull archives were left out, so this covers 55 of the 175 retained files. The archive hashes for C4CUT and L2 are recorded only inside the archive (SHA256SUMS and c5/archive_hashes.tsv), not in the repository. |
| 1 | mirror34 (Theorem 2b): CNF b175eac0 (p cnf 838032 16642456) is UNSAT, with retained LRAT proof 98e4d02a | certificate accepted by both checkers (auditor's label) | Both lrat-check logs (def and final) match the archived proof exactly by fingerprint: formula dimensions, Added 41,860,266 (= 16,642,456 clauses + 25,217,810 additions, which equals the largest clause ID), and Deleted 36,974,924. The archived proof ends in one empty clause and has the byte count in the CaDiCaL log. The cake_lpr logs contain only the verdict. I regenerated the CNF with zcnf_v1.py (b175eac0) and with zcnf.py (1b61bf2f); the two have identical non-comment lines, so the 'identical clauses' claim holds. I did not replay either checker (CNF over 50 MB). |
| 2 | mirror33 (Theorem 2a, new proof): CNF e45464ed is UNSAT, with proof e1b2689d | certificate accepted by both checkers (auditor's label) | The fingerprint matches: 21,430,210 additions, 32,165,860 deleted, top ID 35,510,866, 4,120,793,950 bytes. I regenerated the CNF byte-identically with zcnf.py. The cake_lpr evidence is the verdict only. |
| 3 | Fivefold P1 (angle form): CNF ead55228 is UNSAT, with proof eff67c0f | certificate accepted by both checkers (auditor's label) | The fingerprint matches (14,119,432 / 18,307,782 / 22,043,341). The CNF and its map were regenerated identically. The command for the heap-30000 cake_lpr run is not in any committed script. |
| 4 | Fivefold L1 (layer form): CNF 90dea1cf is UNSAT, with proof 8625b321 | certificate accepted by both checkers (auditor's label) | The fingerprint matches (10,824,961 / 15,150,487 / 18,748,988). I regenerated the CNF hash myself. The 'audit replay, 18.1 s' has no log in the repository. |
| 5 | c3-hex-15 and c3-hex-16: CNFs fc089011 and 15766b1e are UNSAT, with proofs 659a3db6 and 1c4c5e37 | certificate accepted by both checkers (auditor's label) | I replayed lrat-check on the hash-checked archive copies, using the recorded binary: both VERIFIED. Regenerating with symcnf.py gives byte-identical CNFs, and so do the SYMMAX/k6 gzip copies. The cake_lpr verdict exists only in the archive's chk_c3hex.log, which is not in the repository and records no hashes. |
| 6 | central34-cover: cover CNF bb60facb is UNSAT, with proof 3255391a | certificate accepted by both checkers (auditor's label) | I rebuilt the cover hash by streaming base b0061e90 plus C2C34/cubes.txt, following hullcubes.py. The lrat-check fingerprint matches (Added 38,354,806, Deleted 32,114,856). The cake_lpr evidence is the verdict only. |
| 7 | C4CUT: CNF 2aa18f1e (base c3933d9a plus 6 cut clauses) is UNSAT, with proof 6e1199aa | certificate accepted by both checkers (auditor's label) | I checked that the archived CNF is exactly the base (reconstructed hash c3933d9a) with the 6 cuts.jsonl clauses appended in order. Base and map regenerate identically (c3933d9a, f72b186e), and the repository's verify_cuts.py accepts all 6 cuts. The CaDiCaL log fingerprint matches the archive. The checker verdicts survive only as grep lines in final.json, written by the same script that hashed the CNF; there are no raw checker logs. |
| 8 | Pilot re-solves (P8_cover and 6 subcases) are certified UNSAT on CNFs with the recorded hashes | certificate accepted by both checkers (auditor's label) | I rebuilt all 7 unit CNF hashes independently. All 7 proofs are archived and pass the round trip. The verdict strings come from resolve.py running on the file it had just hashed. Six proofs equal the pilot's recorded proof hashes; P8_cover differs, as the README states. No raw solver or checker logs are in the repository. |
| 9 | Random re-solve sample: 21 main and 8 extra drawn units, plus 2 reproducibility units, reproduce their cloud records and both checkers accept them | exact computation (auditor's comparison of the 31 project re-solves with their records) | For all 31, the CNF hash, proof hash and proof size equal the original C2P* certified record. I rebuilt all 31 CNF hashes, and the archives pass the round trip. Three drawn Q units have no record in the repository: P6_9-11, P7_1-15 and P8_1-10. Archive files for P6_9-11 and P7_1-15 appeared tonight. The script that drew the sample is not committed. |
| 10 | Central-34 parallelogram units outside the pilot and sample (about 2,350 certified records) | recorded verdict only (proofs not retained) | lane.py deleted these proofs. According to C2FINAL, hashmatch re-derived their CNF hashes; I re-derived only the 38 re-solved units. |
| 11 | Threefold composition: 116,883 CNF hashes matched and 910 roots covered by both composers | recorded (project's run log; not re-run by the auditor) | C3FINAL/run_final.log and tools.txt support the claim; I did not rerun it. The rerun attributed to the 'independent audit' has no log in the repository. |
| 12 | Threefold spot-check: 2,120 re-solved, all accepted by both checkers with matching CNF hashes; 3,084 drawn = 14×6 + 3,000; 716 and 485 σ-cube nodes | exact computation (auditor's recount of the project's spot check) | I recounted from C3SPOT/out.jsonl and units6.tsv and confirmed every number. Each expected hash equals the original certified record's hash, and the solved rows are the first 2,120 of the shuffled list. The RNG draw cannot be reproduced because no draw script is committed. |
| 13 | Threefold pieces (116,883 records) | recorded verdict only (proofs not retained) | The proofs were deleted; 26,436 records carry a proof hash. |
| 14 | The 2026-10-29 independent-audit replays (mirror34 lrat-check 45.45 s with matching hashes; L1 lrat-check 18.1 s; threefold composition rerun) | unknown (no log in the repository) | These appear only as statements in SYMZ/README.md, CERTIFICATES.md and SYMMETRIC.md. No log exists anywhere in the repository. |
| 15 | Tools: CaDiCaL 3.0.1 c6073042, lrat-check 2e3b2dc with the E2 patch, cake_lpr a36874a8 | exact computation (binary hashes); tool identity of each verdict recorded only in part | The archived tools/ binaries and resolve/bin are identical and match the recorded hashes (e12ecc8c, f2046212, 2fee767a). The patch matches results/E2. Every CaDiCaL log prints 3.0.1 c6073042; the checker logs print no version. The JSON records for pilot, sample and C4CUT store no tool hashes. In my test, the lrat-check binary rejects the E2 forged proof and a mutated proof. |

## Findings

### A6-1 (major): The write-up's trust base does not cover the central-34 and C4CUT certificates the overall claim rests on

SYMMETRIC.md §3 (revised 2026-10-29) still calls the central 34-point case open. It still assumes the published fourfold exclusion in Corollary 3, and lists replayed checks only for threefold, mirror and fivefold. It never says that the central-34 parallelogram part rests on about 2,385 check-and-delete records (proofs deleted, verdicts recorded). Only 38 of those units were re-solved with archived proofs: 7 pilot and 31 sample, including 2 reproducibility tests. It also omits the C4CUT certificate. CERTIFICATES.md has no entries for the three 2026-11-01 archives (es7-c4-32-cuts, es7-central34-pilot-resolve, es7-central34-resample), and its central34-cover entry still says the case 'remains open'. The C4CUT README still says 'An independent review is pending', although commit fcf202869 recorded one. No certificate failed, but the overall claim cannot be stated with this trust base as written.

*Evidence.* WRITEUP/SYMMETRIC.md §1 (Corollary 3), §3 and §4; WRITEUP/CERTIFICATES.md (central34-cover; no 2026-11-01 entries); C4CUT/README.md line 14; C2FINAL/README.md §8 finding 6; C2P/README.md ('Every UNSAT proof was checked ... and then deleted')

*Suggested fix.* Before claiming: add a central-34 trust-base paragraph to §3 covering the records, hashmatch 2,589/2,589, the Lean bookkeeping, the pilot re-solve and the sample with its final 3 Q units, all labelled as recorded verdicts plus sampled re-verification. Replace the published-fourfold assumption with C4CUT and its review. Add the three new archives, with archive hashes, to CERTIFICATES.md.

**Independent check:** real = yes; severity major -> **major**.

Every factual part of the finding checks out except one misattribution: it is §4 of SYMMETRIC.md (line 194) that says the parallelogram cases are open, not §3. §3 does not mention the central case at all.

Confirmed:
- SYMMETRIC.md is dated "Revised 2026-10-29". Corollary 3 (line 59) assumes the published fourfold exclusion. "Checks actually replayed" lists only threefold, mirror and fivefold. C4CUT, C2P, C2FINAL and the deleted central-34 proofs are not mentioned anywhere.
- CERTIFICATES.md has no entry for es7-c4-32-cuts, es7-central34-pilot-resolve or es7-central34-resample. Its central34-cover entry says the case "remains open" (line 154).
- C4CUT/README.md line 14 still says "An independent review is pending", and line 81 still says "conditional on the encoder review". Commit fcf202869 edited that README and added review/README.md ("No blocking or major finding") without changing either line.

My own recount (recount_a61.py) agrees with the auditor's numbers:
- 2,492 records (2,424 from the waves, 68 from the pilot).
- 2,385 UNSAT, all with both checker verdicts; 107 UNKNOWN; no proof kept. lane.py and lane3.py delete the proof after checking.
- The records cover the 2,304 facts the claim needs (8 covers plus 8 x 287 orbits); there are 2,321 distinct certified units.
- At the audited commit 471d5f63a, exactly 38 units have archived re-solved proofs: 7 pilot, 2 reproducibility tests, 21 main sample, 8 extra sample. All are accepted by both checkers and pass the decompression round trip, and all 31 sample re-solves reproduce the recorded proof SHA-256.

Further staleness the auditor did not cite, all in the same direction:
- The LaTeX note (line 122 assumes the fourfold exclusion of SMQH25; line 248 says the parallelogram cases are open).
- C2C34/README.md ("Status: open").
- No single document states the central-34 trust base. C2FINAL mentions deleted proofs only for the 7 pilot records; the deletion of all wave proofs appears only in the wave READMEs.

Severity:
- Not blocking. The evidence exists and I found it intact, no committed document overclaims (C2FINAL says "not yet claimed"), and nothing here threatens the truth of the claim.
- Not minor. The main write-up states the opposite of the planned claim and leaves out the trust base of both new components. The key caveat is missing: nearly all of the 2,304 parallelogram facts rest on recorded verdicts of deleted proofs, with only 38 (about 1.6%) re-verified with retained proofs. SYMMETRIC.md states the same kind of caveat for Theorem 1.
- Fixing it means real rewriting before the claim can be made: SYMMETRIC.md §1, §3 and §4, CERTIFICATES.md, the LaTeX note and the C4CUT README.
- The project's own review rated only the "open" wording minor (C2FINAL §8 finding 6). It rated "the claim waits on a step" as major (finding 1), and that convention fits here.

One part of the suggested fix is lighter than stated. Per-file archive SHA-256 values for the pilot-resolve and resample archives are already in the repository (C2FINAL/pilot/out.jsonl, sample/out.jsonl, extra_out.jsonl); they only need collecting into CERTIFICATES.md. The C4 archive (.zst) hashes exist only in the archive's own SHA256SUMS, outside Git.

Context outside the audited snapshot: after 471d5f63a, P6_9-11 and P7_1-15 were re-solved in the work directory (repro3b.jsonl, uncommitted). Both reproduced the recorded proof and passed both checkers. P8_1-10 was still running. This does not change the finding.

*Verifier's evidence.* Scripts and outputs are in AUDIT3/A6_certificates/verify_A6-1/ (recount_a61.py/.out, doccheck_a61.py/.out).

doccheck results, with R = results:
- R/WRITEUP/SYMMETRIC.md:
  - line 3 "Revised 2026-10-29"
  - line 59 "Assume ... the published fourfold exclusion (arXiv:2506.00224, §6.2)"
  - §3 (lines 126-180) has no mention of the central case or "open"
  - "Checks actually replayed" headings: Threefold composition, Threefold spot-check, Mirror 34, Mirror 33, Fivefold
  - line 194 "The 8 canonical parallelogram cases are open"
  - no mention of C4CUT, C2P or C2FINAL
- R/WRITEUP/CERTIFICATES.md:
  - line 154 "the central 34-point case remains open"
  - no entry for es7-c4-32-cuts, es7-central34-pilot-resolve or es7-central34-resample
  - "Not in the archive" covers only the threefold and mirror-chain proofs
- R/C4CUT/README.md line 14 "An independent review is pending", line 81 "conditional on the encoder review above". Commit fcf202869 changed this README in 2 hunks and added review/README.md (line 7: "No blocking or major finding").
- R/C4CUT/final.json has no .zst SHA-256. The archive's SHA256SUMS lists c4_n32L_cuts.cnf.zst as 3dcb8921... and c4cuts.lrat.zst as 0bf2d79e...; git grep finds neither hash in the repository.
- R/C2FINAL/README.md: line 7 "not yet claimed"; line 163 is finding 6 (Minor: SYMMETRIC.md still describes the parallelogram cases as open); deleted proofs are mentioned only for the 7 pilot records (lines 51-53).
- R/C2P/README.md line 10 "Every UNSAT proof was checked by lrat-check and cake_lpr and then deleted"; R/C2P/tools/lane.py line 120 and lane3.py line 134 call os.remove on the proof.
- Not cited by the auditor: R/WRITEUP/note/symmetric_es7.tex lines 122 (fourfold exclusion assumed) and 248 ("The parallelogram cases are open"); R/C2C34/README.md line 12 "Status: open".

recount output:
- wave records 2424, pilot rows 68, total 2492
- statuses: UNSATISFIABLE 2385, UNKNOWN 107; proof_kept True: 0 (pilot: 65 False, 3 blank on the UNKNOWN rows)
- distinct certified units 2321
- pilot/out.jsonl 7, sample/out.jsonl 23, sample/extra_out.jsonl 8: 38 re-solves, all certified, archived with archive_sha256, round trip verified
- sample rows reproducing the recorded proof: 31/31; sample rows whose CNF matches the record: 31/31
- main sample drawn 24, done 21 (16 H, 5 Q), missing P6_9-11, P7_1-15, P8_1-10
- reproducibility units P6_7-8-9 and P2_7-9-10 are not in the drawn list

Live state (uncommitted): <night run>/repro3b.jsonl shows P6_9-11 and P7_1-15 re-solved with proof_reproduces_record=True and both checkers passing (12:05Z, 12:16Z); P8_1-10 was in progress.

### A6-2 (minor): Checker logs do not name or hash their inputs, and cake_lpr logs cannot be tied to a specific proof

SYMZ/chk.sh and SYM5/check.sh take file names, do not hash them, and do not log the command line. lrat-check logs record the formula dimensions and the Added/Deleted counts. Those match the archived proofs exactly, so each lrat-check verdict is tied to its (CNF, proof) pair by fingerprint, but not by hash. The cake_lpr logs hold only 's VERIFIED UNSAT' and resource usage. So for mirror34 (both runs), mirror33, P1, L1 and the cover, the verdict of the formally verified checker is linked to the recorded pair only by file naming. No P1 heap-30000 command appears in any committed script (check.sh passes no heap flag).

*Evidence.* AUDIT3/A6_certificates/fingerprints.tsv compared with SYMZ/logs/chk_*.out, SYM5/chk_*.out, C2FINAL/evidence/central34-cover/*.out and the cad_*.out 'LRAT ... added/deleted/bytes' lines

*Suggested fix.* Rerun cake_lpr (and lrat-check) on the archived CNF/proof pairs with a wrapper that logs the sha256 of both inputs and the full command, as resolve.py does. Archive those logs.

**Independent check:** real = yes; severity minor -> **minor**.

The finding is correct in every factual part, and minor is the right severity.

(1) Scripts. SYMZ/chk.sh (CNF PROOF TAG) and SYM5/check.sh (NAME CNFBASE CHECKER) compute no hash and log no command line. The only text they add is "exit N wall S s", and BSD /usr/bin/time -l prints resource usage only.

(2) cake_lpr logs cannot name their inputs. The binary's hash equals the recorded one (2fee767a). Its strings contain no file-name output, only verdicts such as "s VERIFIED UNSAT". Each of the six cited logs (mr34_def, mr34_final, m33_def, P1_heap30000, L1, hc34_cover) has exactly one line that is not resource usage, "s VERIFIED UNSAT", and no file name or hash. The link to the pair is the TAG in the file name, plus prose written afterwards in CERTIFICATES.md, the archive MANIFEST.md and manifest.json, and SYM5/README.md. That prose is also name-based.

(3) lrat-check fingerprints, checked independently. I wrote my own streaming counter with in-process SHA-256 and did not reuse the auditor's lratcount. On both c3hex pairs it reproduced lrat-check's Added (= C + additions), Deleted (= deleted IDs) and Max live exactly. I then streamed the five archived pairs:
- every CNF and proof SHA-256 equals the recorded value;
- in all six lrat-check logs, V, C, Added, Deleted and also Max live equal my counts of the archived pair (the auditor did not use Max live);
- every CaDiCaL log names both files, and its header and LRAT added/deleted/bytes match;
- in every proof the first addition ID is C+1.

(4) No committed script runs P1 at heap 30000. SYMZ/chk.sh hardcodes --CML_HEAP_SIZE=30000 only as a generic TAG run. SYM5/check.sh only exports CML_HEAP_SIZE, which this build ignores: the binary has only the flag strings, and the docs say the same. The P1 command exists only as text in SYM5/README.md:89-90 and CERTIFICATES.md:81.

The auditor missed three points. They are the same kind of gap and do not change the severity:
(a) The cover run's command is not in any committed script either. CERTIFICATES.md:172 gives heap 20000, and the log's peak footprint of 20030 MiB agrees (the heap-30000 runs show 30260-30328 MiB). Yet the log is named as SYMZ/chk.sh names logs, and chk.sh hardcodes 30000.
(b) chk_P1_cake_lpr_heap12000.out actually ran at the default heap of about 4 GiB (RSS 4099 MiB, footprint 4100 MiB). Its file name records a setting that never took effect; the README correctly says "default heap". File names are therefore not a reliable link.
(c) The lrat-check fingerprint ties the proof strongly but the CNF only by (V, C). The chk_mr34_def and chk_mr34_final logs are identical although they ran on different files: the archived b175eac0 and m34_final.cnf 1b61bf2f, which is not archived. Likewise the L1 cake_lpr log could not tell L1 from L2.

Why minor and not major: the UNSAT claims do not rest on the cake_lpr link.
- The archives match their hashes.
- The CNFs regenerate byte-identically.
- The CaDiCaL and lrat-check logs (lrat-check carries the E2 patch) match the archived pairs on several exact counts.
- Nothing inconsistent was found: the cake_lpr footprints agree with the documented heaps.
The gap only weakens the record of the extra check by the formally verified checker. A re-run on the archived pairs with hash logging would close it; that needs a 20-30 GB heap, so it was not run here. The project's own C2FINAL review rated the similar gap (cake_lpr on unhashed rebuilt CNFs) as minor. One small correction to the suggested fix: resolve.py logs both SHA-256 values and the heap, not literally the full command.

*Verifier's evidence.* Directory: AUDIT3/A6_certificates/verify_A6-2/

My files there:
- fp.c: own streaming counter with SHA-256; my own code, not the auditor's.
- calibration_c3hex.log: my counts against lrat-check on both c3hex pairs; Added, Deleted and Max live agree exactly.
- run_fp.sh and fp_out/*.fp: fingerprints of the archived m_t17k7/mr34_def, m_t16k7a1/m33_def, c5_n35/P1, c5_n35L/L1 and cover/hc34_coverL pairs.
- compare_fp.py and compare_fp.log: comparison with the logs, ending "ALL NUMERIC CHECKS OK".

What compare_fp.log shows:
- All recorded SHA-256 values match.
- In all six lrat-check logs, V, C, Added, Deleted and Max live equal the archived pair. Example, mr34: 838032 / 16642456 / 41860266 / 36974924 / 16642786.
- The CaDiCaL logs' added/deleted/bytes match, and each names both files.
- Every cake_lpr log has only "s VERIFIED UNSAT" (or "CakeML heap space exhausted.") plus time output, with no file names or hashes.

cake_lpr peak footprints:
- 30328, 30328, 30260 and 30020 MiB for the mirror34 (def and final), mirror33 and P1 heap-30000 runs;
- 20030 MiB for the cover;
- 4100 and 4101 MiB for P1 "heap12000" and L1, i.e. the default heap.

Files cited:
- Scripts: SYMZ/chk.sh (hardcodes heap 30000); results/SYM5/check.sh (exports an env var that the binary ignores).
- Docs: results/WRITEUP/CERTIFICATES.md:81 and :172 (P1 heap 30000, cover heap 20000, as text only); results/SYM5/README.md:88-90.
- Binary: `strings` of <bin>/cake_lpr shows only the --CML_HEAP_SIZE= flag and no getenv string.

Incidental: results/SYM5/__pycache__/symcnf.cpython-314.pyc was written into the read-only worktree at 21:26, during the auditor's regeneration. Git ignores it and it is harmless.

### A6-3 (minor): C4CUT keeps no raw checker output, and its archive hashes are recorded only inside the archive

c4final.sh keeps one grep'd line from each checker in final.json and throws away the rest of the output. That makes the C4CUT verdicts the only ones in CERTIFICATES-class certificates that cannot be fingerprint-checked. final.json records 'archive_roundtrip: ok' but no archive SHA-256. The archive hashes exist only in the archive's own SHA256SUMS, which was produced by steps that are not in c4final.sh: it lists c4cut.log, controls.py, c4final.sh and final.json, none of which the script copies. The archived verify_cuts.py is the version from before the review. The CNF, solver log and binding are otherwise sound: I checked them as base plus cuts, regenerated base and map, and saw verify_cuts pass.

*Evidence.* C4CUT/c4final.sh; C4CUT/final.json; archive es7-c4-32-cuts-2026-11-01/SHA256SUMS; AUDIT3/A6_certificates/c4_base_check.log

*Suggested fix.* Record the two archive SHA-256s (3dcb8921…, 0bf2d79e…) in the repository. Rerun lrat-check, and cake_lpr if memory allows, on the archived pair with logs that include hashes.

**Independent check:** real = yes; severity minor -> **minor**.

The finding's factual core is right. One comparative claim is wrong, and the archive-hash point matters less than the finding suggests.

Confirmed:
1. c4final.sh keeps only the first grep'd line of each checker's output (line 25 for lrat-check, line 27 for cake_lpr). Exit codes are not kept either. final.json says archive_roundtrip "ok" but records no SHA-256 of the .zst files.
2. Neither 3dcb8921... nor 0bf2d79e... appears anywhere in the repo working tree at 471d5f63a.
3. The archive's SHA256SUMS lists 11 files, but the script copies only the two .zst files (line 30) and five small files (line 31). So c4cut.log, controls.py, c4final.sh and final.json were added by hand; all four have mtime 16:26, the same as SHA256SUMS. The SHA256SUMS written by line 40 was then regenerated outside the script. All 11 entries verify.
4. The archived verify_cuts.py is the pre-review version. It lacks the distinct-anchor assert, the type(w) is int check and the map-hash print.

Wrong or overstated:
- "The only ones in CERTIFICATES-class certificates that cannot be fingerprint-checked" is false. Other certificates keep the same single grep'd verdict line:
  - c3-hex-15/16 (in CERTIFICATES.md): the archived c3hex/chk_c3hex.log is 179 bytes of one-line verdicts.
  - The 120 central34-hull cases (in CERTIFICATES.md): hlane.sh:17 and hchecker.sh:26 keep one line, and hex_cases.tsv has no committed solver or checker logs.
  - The pilot and sample units: resolve.py:98,109 and reproduce.py:96,99 do the same.
  - C4CUT is actually better off than the hull cases, because its CaDiCaL log is kept and matches the archived proof.
  - What is true: among the certificates the auditor covered, C4CUT is the only one whose checker verdict was neither logged in full nor replayed. The auditor replayed c3hex.
- Missing .zst hashes are not an integrity gap. The repo's final.json pins the uncompressed CNF and proof hashes, and the archive decompresses to exactly those (I checked).

Not mentioned by the auditor:
- The committed final.json and cad_c4cuts.out are redacted copies of the archived originals: archive_dir was rewritten and the CaDiCaL build-host line removed. This is harmless.
- The project's review (minor finding 4) says the verdicts are in "final.json and the logs", but no checker logs exist.

Why minor and not major: the claim is not threatened. My own checks:
- The archive is intact.
- The proof is 1,040,775,249 bytes, with 6,493,272 additions, 9,880,546 deleted IDs and one final empty clause. All match cad_c4cuts.out.
- Addition IDs run contiguously from 5,272,501, which fits the 5,272,500-clause base-plus-cuts CNF.
- Each of the six cut clauses is cited as a hint exactly once.
- Both verify_cuts.py versions pass.

What remains is one cheap missing check: an independent lrat-check replay of the archived pair with a full, hash-stamped log. I could not run it here, because the CNF is 183 MB (over the 50 MB load limit) and cake_lpr is barred.

*Verifier's evidence.* Repo (R = results):
- R/C4CUT/c4final.sh lines 25, 27, 30-31, 40
- R/C4CUT/final.json
- R/C4CUT/review/README.md, minor finding 4
- R/C2C34/hlane.sh:17
- R/C2C34/hchecker.sh:26
- R/C2C34/logs/hex_cases.tsv (120 rows, verdict columns only)
- R/C2FINAL/pilot/resolve.py:98,109
- R/C2FINAL/sample/reproduce.py:96,99

Archive:
- <proof-archives>/es7-c4-32-cuts-2026-11-01/SHA256SUMS
- <proof-archives>/es7-symmetry/c3hex/chk_c3hex.log

Repo copies that differ from the archive:
- final.json: archive_dir path only
- cad_c4cuts.out: build-host line removed
- verify_cuts.py: review fixes

My logs (all in AUDIT3/A6_certificates/verify_A6-3/):
- archive_hashes.log: .zst SHA-256s match SHA256SUMS. Decompressed CNF is 2aa18f1e... (183,470,218 bytes); proof is 6e1199aa... (1,040,775,249 bytes). Both equal final.json.
- proof_fingerprint.log: additions 6,493,272; deleted IDs 9,880,546; one empty clause as the last line; max ID 11,765,772. Equal to the 'c LRAT' lines in cad_c4cuts.out.
- proof_ids_cuts.log: addition IDs contiguous from 5,272,501 to 11,765,772. Cut-clause IDs 5,272,495 to 5,272,500 are each cited as a hint once and deleted once.
- verify_cuts_both.log: the archived and repo verify_cuts.py both print "6 cuts verified".
- scripts/lrat_fingerprint.awk and scripts/lrat_ids_cuts.awk

Repo grep at 471d5f63a: no file contains 3dcb8921 or 0bf2d79e.

### A6-4 (minor): The 'independent audit' replays are not logged anywhere in the repository

The following appear only as prose: 'lrat-check replay, exit 0, 45.45 s, hashes matched' (mirror34), 'lrat-check replay, exit 0, 18.1 s; CNF hash regenerated' (L1), and 'rerun again by the independent audit' (threefold composition). A git grep found no log for any of them. I confirmed the CNF-hash parts myself by regenerating the L1, P1 and mirror34 CNFs. The lrat-check replays could not be repeated under the audit's resource rules.

*Evidence.* git grep '45\.45 s' shows only SYMZ/README.md:108 and WRITEUP/CERTIFICATES.md:39; WRITEUP/SYMMETRIC.md lines 56, 155, 163 and 165

*Suggested fix.* Commit the audit logs, or reword these as unlogged statements.

**Independent check:** real = yes; severity minor -> **minor**.

The finding is correct as stated: no log of the 2026-10-29 audit replays is in the repository. The auditor missed one thing that matters for the fix: the logs do exist on disk, untracked, and they support the stated numbers exactly.

Severity stays minor. No claim depends on these replays. Each certificate already has its own committed logs (SYMZ/logs/chk_mr34_{def,final}_lrat-check.out, SYM5/chk_L1_*.out, C3FINAL/run_final.log) and its archived proof. The gap is provenance: the write-up's trust base lists these replays under "Checks actually replayed", but the evidence is outside git. It is also outside the proof archive, whose MANIFEST.md and manifest.json only repeat the prose, so the only copy could be lost. The fix is to commit the existing logs and cite them. Rewording the statements as unlogged is unnecessary.

Smaller corrections to the auditor:
- (a) The '45.45 s' match is on SYMZ/README.md:109; the bullet starts on line 108.
- (b) The same unlogged claims also appear at CERTIFICATES.md:223 and symmetric_es7.tex lines 74 and 239–240, which the auditor did not list.
- (c) The composition-replay log has no timestamp or exit code, and its JSON and TSV outputs are byte-identical to C3FINAL's. That is expected from a deterministic rerun with the same tools path, but the log alone cannot tell a rerun from a copy. Only the audit's prose gives a runtime (48.31 s).

I agree that the lrat-check replays cannot be repeated under the rules. The CNFs are 620 MB and 283 MB, both over the 50 MB in-memory limit, and lrat-check holds the whole formula in memory.

*Verifier's evidence.* The repository (worktree at 471d5f63a and all refs) has no replay logs:
- git grep HEAD for 'verification time = (45.x|17.x|18.x) secs' finds nothing.
- Pickaxe search over all refs for the lrat-check count lines 'Added clauses = 41860266' (mirror34) and 'Added clauses = 18748988' (L1) finds only the original logs, added in 40eec3337 and 1406f90d4. Their verification times are 58.14 s, 50.15 s and 14.26 s.
- git log --all finds no commit touching *lrat-replay*, *composition-replay* or the audit directory.
- No audit directory in the repository dates from 2026-10-29. C3AUDIT4 (2026-10-24) is the latest.
- C3FINAL holds only the single 2026-10-28 run.
- The prose was added in 189ab709a and 40eec3337 at 2026-10-29 13:03 KST, about 25 minutes after the audit ended (its session.json says it completed at 03:38Z), and none of the audit files came with it.

The logs exist, untracked, in "<audit-2026-10-29>/". git status shows '??' (untracked and not ignored).
- mirror34-lrat-replay.json: exit_code 0, elapsed_seconds 45.4486. Hashes: CNF b175eac0…, proof 98e4d02a…, lrat-check f2046212… (the same as the tool hash recorded in CERTIFICATES.md).
- mirror34-lrat-replay.log: 'c VERIFIED', 'verification time = 45.39 secs'.
- c5-layer-lrat-replay.json and .log: exit 0, 18.117 s, 'verification time = 18.10 secs'. Hashes: CNF 90dea1cf…, L1 8625b321….
- c5-regenerated-hash.json: 90dea1cf….
- composition-replay.json and composition-replay_roots.tsv have the same SHA-256 as C3FINAL_mirrorh6.json and C3FINAL_mirrorh6_roots.tsv. composition-replay.log equals run_final.log without its start and exit lines.
- REPORT.md and certificates-audit.md are also there.
- In both replay logs, the Added, Deleted and Max live counts equal those in the committed original logs.

My own checks, with scripts and logs in AUDIT3/A6_certificates/verify_A6-4/:
- I regenerated c5_n35L.cnf from generator copies whose hashes I checked (symcnf.py a8056da0…, symcnf_layers.py 71b2d7e7…). It came out at 283,069,961 bytes with sha256 90dea1cf…, a match. Log: AUDIT3/A6_certificates/verify_A6-4/regen_L1_cnf.log.
- I stream-hashed the archived proofs. L1.lrat.zst gives 8625b321… (1,812,130,098 bytes) and mr34_def.lrat.zst gives 98e4d02a… (4,373,364,691 bytes). These are the hashes the untracked replay records name. Log: AUDIT3/A6_certificates/verify_A6-4/hash_replayed_proofs.log.
- I did not run lrat-check, cake_lpr or any solver.

Side note: SYM5/__pycache__ in the worktree is gitignored and has mtime 21:26. That matches the time A6's regen.sh ran the generator from inside the read-only worktree.

### A6-5 (minor): The c3hex checker log is not in the repository, contrary to CERTIFICATES.md

CERTIFICATES.md says copies of the checker logs are in results/SYMZ, results/SYM5 and tools/symmetric. tools/symmetric holds no logs, and chk_c3hex.log (four lines, no hashes) exists only in the archive. I replayed lrat-check on both c3hex certificates (VERIFIED) and regenerated both CNFs byte-identically. cake_lpr remains a recorded verdict.

*Evidence.* AUDIT3/A6_certificates/c3hex_replay.log

*Suggested fix.* Commit chk_c3hex.log, or a fresh dual-check log with input hashes, under results/SYMMAX/k6.

**Independent check:** real = yes; severity minor -> **minor**.

The finding is correct, and minor is the right severity.

1. **CERTIFICATES.md is wrong for c3hex.** Line 10 says: "Copies of the generators and checker logs are also in results/SYMZ, results/SYM5 and tools/symmetric." I compared every small file in the archive against every file in the worktree by SHA-256. Every archived checker log has a byte-identical copy in the repository except c3hex/chk_c3hex.log. The copies found are 4 for mirror34 and 2 for mirror33 (results/SYMZ/logs), 5 for c5 (results/SYM5) and 2 for the cover (results/C2FINAL/evidence/central34-cover).
   - No same-name file or copy of chk_c3hex.log exists in the worktree.
   - No path containing "c3hex" or "chk_c3" appears in the git history of any ref.
   - No ref tip contains the log's lines.
   - From 2026-10-26 on, the only c3hex files ever committed are the two CNF .gz files and the points files in results/SYMMAX/k6.

2. **One part of the finding is weak on its own.** "tools/symmetric holds no logs" is true; it holds only source files. But the sentence can be read as "spread over the three directories", and on that reading this is not a defect by itself. The real defect is that the c3hex log is in none of the three directories, nor anywhere else in the repository.

3. **Two extra imprecisions in the same sentence.**
   - The cover logs are in results/C2FINAL/evidence, not in the three named directories. They were added in 57bc5a901 on 2026-11-01, after the sentence was written in 189ab709a on 2026-10-29.
   - c3hex is the only certificate with no solver log anywhere. It was solved with -q, and the original session's scratch folder has no c3hex CaDiCaL log either.

4. **The archived log is as described.** It has 179 bytes and 4 lines: the file stems, the p cnf headers and the two verdicts. It has no hashes, no proof file names, no timings and no tool identity. A byte-identical copy survives only in a temporary work folder.

5. **Why the severity is not higher.** The certificates themselves are intact, and I reproduced the auditor's checks:
   - All 8 recorded hashes match: both archives and their decompressed files, for each CNF and each proof.
   - The CNFs regenerate byte-identically from the repository's symcnf.py (a8056da0). The SYMMAX/k6 .gz copies decompress to the recorded CNF hashes.
   - lrat-check accepts both proofs (c VERIFIED, exit 0). Its binary hash f2046212 matches the record.
   - I wrote a second, strict RUP-only LRAT checker (lratpy.py). It also accepts both proofs, with the empty clause derived at id 156685 and at id 145359.
   - Both checkers reject two mutated proofs (one hint dropped, one literal flipped).
   - So the c3hex claims stand on two checkers replayed today, even though cake_lpr remains a recorded verdict only (the audit rules forbid running it).
   - The c3hex results are companion observations for hexagons (k = 6), not part of the ES(7) claims. The 16-point case agrees with arXiv:2506.00224.
   - Because the missing log has no hashes, committing it would add little evidence.

6. **Why it still counts.** It is a fixable inaccuracy in a certificate document. Every other retained certificate has its raw checker output in Git; c3hex does not.

7. **A better fix than the auditor's.** The two proofs are only 855,150 and 451,192 bytes compressed. Commit them under results/SYMMAX/k6 next to the CNFs, together with a fresh log recording the input and tool SHA-256s. Then correct the CERTIFICATES.md sentence.

*Verifier's evidence.* All paths below are under <work>/.

**Scripts and logs written for this check** (in AUDIT3/A6_certificates/verify_A6-5/):
- find_log_copies.py writes log_copies.tsv. It compares every small archive file with the worktree by SHA-256. Every chk_* log is marked COPY except "c3hex/chk_c3hex.log 179 e510ad144bf9ba7c NO-COPY", with no same-name file in the worktree.
- touched_since_1026.txt lists the files touched in any ref since 2026-10-26. The only c3hex entries are SYMMAX/k6/c3_n15k6.cnf.gz and c3_n16k6c.cnf.gz (commit 01ac07fb2) and the points files.
- replay_c3hex.sh writes replay_c3hex.log, with per-run outputs in run/. It records:
  - MATCH for all 8 recorded hashes: fc089011, 659a3db6, 15766b1e and 1c4c5e37, plus the four archive hashes.
  - lrat-check: c3_n15k6 exit 0 "c VERIFIED"; c3_n16k6c exit 0 "c VERIFIED".
  - lratpy.py: both "s VERIFIED". The 15-point proof has 29,900 additions and the empty clause at line 56056, id 156685. The 16-point proof has 16,188 additions and the empty clause at id 145359.
  - The regenerated CNFs and the SYMMAX gz copies give MATCH.
  - Both mutated proofs are rejected by both checkers.
- lratpy.py is my own strict RUP-only LRAT checker.

**Repository and archive files:**
- results/WRITEUP/CERTIFICATES.md line 10 holds the "Copies of the generators and checker logs ..." sentence. It was added in 189ab709a on 2026-10-29.
- es7w/cloud/es7-2026-10-19/tools/symmetric holds source files only.
- results/SYMMAX/k6 holds the CNF .gz files only: no logs and no proofs.
- In the archive, <proof-archives>/es7-symmetry/c3hex/chk_c3hex.log has 4 lines and SHA-256 e510ad14...b90, with no input hashes. The c3hex folder there has no cad_*.out.
- The cover logs live in results/C2FINAL/evidence/central34-cover. They were added in 57bc5a901 on 2026-11-01 and are not in the directories the sentence names.

### A6-6 (minor): The random re-solve sample is incomplete in the repository, and the draw cannot be reproduced

Three of the 24 main-sample units have no record: P6_9-11, P7_1-15 and P8_1-10, all Q. C2FINAL itself says the statement is not claimed until they finish. The archive already holds P6_9-11.lrat.zst (21:02 local) and P7_1-15.lrat.zst (21:05), with no repository record. The script that drew the sample with seeds 20261101 and 20261102 is not committed, so 'drawn before any result was seen' cannot be checked.

*Evidence.* C2FINAL/sample/sample.txt vs out.jsonl; compare.py 'unreferenced archive file' lines in AUDIT3/A6_certificates/phase12_compare.tsv

*Suggested fix.* Commit the final records with archive hashes, and the draw script, before stating the theorem.

**Independent check:** real = yes; severity minor -> **minor**.

Half of the finding holds and half is overstated.

What holds:
- At the repository tip 471d5f63a (= origin/es7-cloud), sample.txt lists 24 units: 2 H and 1 Q per case. out.jsonl has 23 lines: the 2 reproducibility tests plus 21 main-sample units (16 H, 5 Q).
- P6_9-11@C2P3/M31, P7_1-15@C2P/M40 and P8_1-10@C2P2/M02 have no record. All three are Q.
- C2FINAL's own status line says the theorem is not yet claimed for this reason. No other document (C2C34 'open', SYMMETRIC.md, CERTIFICATES.md) claims it, so nothing is overclaimed. The gap is real but disclosed.
- No draw script exists anywhere in git history. `git log -S` finds the seeds only in the README, and reproduce.py takes the units as arguments.
- The archive holds P6_9-11.lrat.zst and P7_1-15.lrat.zst, and the repository mentions neither archive.
- I hashed both archives. Their sizes and SHA-256 equal the local, uncommitted records in resolve/repro3b.jsonl. Decompressed, they give exactly the proof bytes and SHA-256 recorded by the cloud lanes (C2P3/M31, C2P/M40).
- So for 2 of the 3 units the gap is only bookkeeping. P8_1-10 was still solving at 12:44Z: the proof was at 9.41 GB, against 9.98 GB in the cloud record.

What is wrong:
- The title says the draw 'cannot be reproduced', and the detail says 'drawn before any result was seen' cannot be checked. Both are wrong in substance. I reproduced both draws exactly from the committed records with Python's standard random module and the README's seeds.
- The population is the distinct units that have a certified record from a non-LOCAL source, sorted by name, each paired with its first source in sorted path order.
- Main draw: Random(20261101); for each of P1..P8, sample 2 H then 1 Q; list all H, then all Q. This gives 24/24 in order.
- Extra draw: Random(20261102); for each case, sample 1 H from the H units not already in the main sample. This gives 8/8 in order.
- Neighbouring seeds and the string seed do not give the list. A chance match is negligible: about 1 in 200^16 × 56^8.
- So the selection is a fixed function of a date seed and the committed records, and it could not have depended on re-solve outcomes.
- Git alone cannot show the wall-clock order: sample.txt was first committed in 7cf0a65eb together with 5 result lines. That matters little once the seeded selection reproduces. Local files agree with the timing claim: resolve/sample.txt was created at 07:16:23Z, before the first re-solve at 07:33:27Z.
- What remains is documentation: the dedup and sort rules and the exclusion rule for the extra draw are not written down.
- Small slip: the P7_1-15 archive's mtime is 21:12:40 local, not 21:05. zstd copies the proof's mtime; the record finished at 21:16:13 local, and its solve only started at 21:05:26 local.

Severity: minor. This is fixable bookkeeping that does not threaten the claim: commit the three records with archive hashes once P8_1-10 finishes, and commit the draw script or describe its procedure. The claim is already withheld until then.

*Verifier's evidence.* Scripts and logs in AUDIT3/A6_certificates/verify_A6-6/:

- **population.py / population.log**
  - 24 units in sample.txt; 23 lines in out.jsonl.
  - Missing: P6_9-11@C2P3/M31, P7_1-15@C2P/M40, P8_1-10@C2P2/M02 (all kind Q).
  - Each of the 21 recorded units has cnf_matches_record, proof_reproduces_record, certified and roundtrip all true.
- **try_draw.py / try_draw.log:** 960 candidate procedures tried; one family (equivalent orderings) reproduces sample.txt 24/24 in order.
- **redraw.py / redraw.log**
  - Main draw: `random.Random(20261101)`; per case, `sample(H,2)` then `sample(Q,1)`.
  - Population: distinct units with a certified non-LOCAL record, first source in sorted path order, sorted by name. Sizes are, for example, P1 227 H / 56 Q and P8 178 H / 43 Q.
  - Result: True. Other seeds tried give no match.
  - Extra draw: `random.Random(20261102)`, `sample(H minus main-sample units, 1)` per case. Result: True, 8/8. Without the exclusion: 2/8.
- **archive_hashes.tsv**
  - P6_9-11.lrat.zst: 633018051 bytes, sha 9cb332e4…
  - P7_1-15.lrat.zst: 877653260 bytes, sha 98934f65…
  - Both equal the uncommitted <night run>/repro3b.jsonl.
- **decomp_hashes.tsv**
  - P6_9-11: 3607879160 bytes, sha 2238c76e…, equal to the C2P3/M31 record.
  - P7_1-15: 4592627388 bytes, sha 8384801a…, equal to the C2P/M40 record.
- **Git**
  - `git grep` of the tip finds neither archive hash and no seed outside C2FINAL/README.md.
  - The C2FINAL/sample history is 7cf0a65eb (adds sample.txt, reproduce.py and out.jsonl with 5 lines), 57bc5a901, then 471d5f63a (adds extra_sample.txt and extra_out.jsonl).
- **Timestamps**
  - `stat` of P7_1-15.lrat.zst gives birth and mod time 2026-11-01 21:12:40 KST, not 21:05.
  - resolve/reproduce.log: P7_1-15 solve started 12:05:26Z and ended 12:16:13Z.
  - P8_1-10 was still running at 12:43:52Z.
  - resolve/sample.txt (identical to the committed file) was created 07:16:23Z; the first re-solve started 07:33:27Z.
- **Claim status**
  - C2FINAL/README.md lines 6-7: 'not yet claimed'.
  - C2C34/README.md: 'Status: open'.

### A6-7 (note): cake_lpr heap set through an environment variable this build ignores

SYM5/check.sh and C3U2/controls.py dual(), which C3SPOT and the threefold pieces use, set CML_HEAP_SIZE in the environment. According to CERTIFICATES.md, this build reads only the --CML_HEAP_SIZE flag. The runs therefore used the default heap: the 'heap12000' P1 log shows about 4.3 GB RSS and heap exhaustion. C3SPOT/README's 'CML_HEAP_SIZE=12000' misdescribes this. Verdicts are unaffected, since every passing run passed.

*Evidence.* SYM5/check.sh; C3U2/tools/controls.py lines 25-31; SYM5/chk_P1_cake_lpr_heap12000.out

*Suggested fix.* Correct the C3SPOT README wording.

### A6-8 (note): Archived logs are redacted copies; the solver build is identified only by the C4 log

The archive copies of the CaDiCaL logs carry the same '[build date and host line removed]' line as the repository copies, so no unredacted original survives for mirror, c5 or the cover. The archived C4 log keeps the build line ('Sun Oct 25 15:14:29 KST 2026 … arm64'), which matches the --build output of the archived cadical binary. 31 log and generator copies are byte-identical between repository and archive.

*Evidence.* AUDIT3/A6_certificates/log_copies.txt

### A6-9 (note): Every retained proof exists in one local copy only

All archives live on one disk, kept out of Git only by .git/info/exclude, and no off-machine copy is recorded. Losing that disk would turn these certificates into recorded verdicts. There is also an empty es7-symmetry/central34-layers directory. L2 is archived but no checker has ever run on it; CERTIFICATES.md labels it correctly.

*Evidence.* git status --ignored in <main-repo> shows '!! proof-archives/'

*Suggested fix.* Keep a second, off-machine copy with its own manifest.

### A6-10 (note): Which certificates are bound to a hashed CNF

Bound at check time, meaning the script hashed the exact file that both checkers read: C4CUT (c4final.sh), the pilot (resolve.py), the sample (reproduce.py), the cloud parallelogram records (lane.py) and the threefold pieces and C3SPOT (close_tree.py). The last two groups have deleted proofs. Not bound at check time: mirror34, mirror33, c5 P1 and L1, the cover and c3hex. For these the hashes were recorded separately (sha256.txt, archive_hashes.tsv), and the binding rests on file names plus fingerprints, which I verified. My own c3hex replay is hash-bound. L2 was never checked. For central34-hull, per C2FINAL finding 2, cake_lpr ran on a CNF that was rebuilt but not hashed (out of scope here).

## Tests run by the auditor

- build_manifest.py: parsed CERTIFICATES.md, C4CUT/final.json and the C2FINAL pilot/sample jsonl into 55 archive entries (manifest.tsv)
- hash_archives.sh: stat plus shasum -a 256, one file at a time, on all 55 archives; 55/55 exist with matching size and SHA-256 (observed_archive.tsv)
- roundtrip.sh: zstd -dc | shasum -a 256 on all 55; every decompressed hash and size equals the recorded original, and 8/8 DIMACS headers match (roundtrip.tsv, phase12_compare.tsv)
- compare.py: 0 failures; unreferenced archives P6_9-11.lrat.zst and P7_1-15.lrat.zst
- lratcount.c with fingerprint.sh: streaming counts over 9 archived LRAT proofs; additions, deleted IDs, top ID and bytes equal the CaDiCaL and lrat-check log values, and each proof ends in exactly one empty clause (fingerprints.tsv)
- records_crosscheck.py: 31/31 sample rows equal their original C2P* certified records (CNF hash, proof hash, size); pilot hashes equal hashmatch computed_for_no_hash; 6/7 proofs equal the pilot's
- unit_cnf_hash.py: streamed rebuild of 38/38 re-solve unit CNF hashes from base b0061e90 (base ends with a newline)
- cover_hash.py: rebuilt cover CNF hash bb60facb from base plus C2C34/cubes.txt
- c4_base_check.py: archived C4 CNF = base c3933d9a plus the 6 cuts.jsonl clauses in order (my first version had an ordering bug, fixed before the reported run)
- C4CUT/verify_cuts.py (repository version): 6 cuts verified, map f72b186e
- regen.sh: regenerated c4_n32L (c3933d9a, map f72b186e), c5_n35L (90dea1cf), c5_n35 (ead55228, map equals the repository's); peak RSS at most 118 MB
- regen_mirror.sh: regenerated m_t16k7a1 (e45464ed), m_t17k7 via zcnf_v1 (b175eac0) and m34_final via zcnf (1b61bf2f); non-comment lines of the last two are identical
- c3hex_replay.sh: lrat-check VERIFIED on both hash-checked c3hex pairs; regenerated and SYMMAX CNFs identical; forged hintless empty clause and mutated proof both rejected
- c3spot_check.py: confirmed 3,084 / 14 groups / 716 / 2,120 / 485, all four checks passing, expected hashes equal the original records
- log_copies.sh: 31 archive log and generator copies byte-identical to the repository copies (gen_m_t17k7.log vs gen.log are different files by design)
- Tool binaries: archive tools/ = resolve/bin = recorded hashes; cadical --build matches the C4 log
- No cake_lpr run, no SAT solve, no CNF over 50 MB loaded (all streaming). A few sub-second 3-stage pipelines (zstd | head | grep) briefly went over the 2-process limit.


# Referee report on MIRROR.md, NUMBERS.tsv and README.md

Task `REVIEW_TASK.md` (committed at c0ad8895), H = 1.0, Z = c0ad8895. Run on 2026-10-21, starting about 00:57 UTC, in one cloud session. It reviews the first pass (commit 3c829b65) against the files on branch es7-cloud at 3d22e5d6. All paths are relative to `cloud/es7-2026-10-19/`. "Section" means a section of `MIRROR.md` unless stated otherwise.

**Severity counts:** 4 wrong, 13 incomplete, 10 unclear, 8 cosmetic (35 in total). Every problem except C8 was corrected in `MIRROR.md`, `NUMBERS.tsv` or `README.md`; the list of changes is at the end.

**Most serious problems:**
- **W1.** The stated vacuous-case rule matches 57 cases, not 56.
- **W2.** The sub-case (i) normal form calls a reflection a rotation and mixes two frames.
- **W3.** The wrong commit is given for the V2-L tree data.
- **I1, I3, I4, I7.** The trust base was overstated or incomplete:
  - the forbidden-word grep covers V2-L only;
  - the lrat-check versions were not stated correctly;
  - the driver grep covers WAVE1 only;
  - the "no SAT anywhere" claim went beyond its sources.

## How the checks were done

- **Numbers.** Every number was re-derived from the data files with short Python scripts:
  - `results/Mii-S/cases.jsonl`, `cover_lrat.jsonl`, `pass2_lrat.jsonl`;
  - `results/Haudit/t3_cover_lrat.jsonl`, `t5_all172.jsonl`, `geo_*.jsonl`;
  - `results/FINAL/READY.json`;
  - `results/V3Z/inputs.txt`, `problems.txt`, `covers.jsonl`, `accepted_final.tsv`, `aggregate_inputs.txt` and the 78 record files it lists;
  - the `results/V1-L/SUMMARY.md` table;
  - `verify/hull_leaves.icnf` (sha256 recomputed);
  - machine directories containing `env.txt`.
- **Commit hashes.** Each was checked with `git cat-file` and against `results/FINAL/COMMIT_MAP.tsv`.
- **Lean statements.** These were compared with the sources:
  - `results/V2-L/V2L/FinalTree.lean`, `Main.lean`, `Tree.lean`, `Audit.lean`;
  - `results/H3/MirrorEncoding/Line.lean`, `Frame.lean`, `Sound.lean`;
  - `results/V1-L/V1L/Main.lean`, `Cover.lean`.
- **Mathematics.** The mathematical arguments were re-derived by hand. The vacuous-case count was recomputed with `results/Mii-S/scripts/hullsplit.py` (`cube`).

## Problems found

Each entry gives the location, what the first pass said, what the source says, and the severity.

### Wrong

**W1. Section 4, tests paragraph (vacuous cases).**
- **Text:** "the 56 vacuous ones (2 ∈ U or 3 ∈ L, contradicting the X(1,2,3) unit)".
- **Source:** `results/Mii-S/cases.jsonl`. 29 cases have 2 ∈ U and 29 have 3 ∈ L, with one overlap, so the stated rule matches 57 cases.
- **Why the count is still 56:**
  - Exactly 56 cubes contain ¬X(1,2,3). These are the cases with 2 ∈ U, or with 3 ∈ L and 2 ∉ L.
  - The case U = ∅, L = {2,3} is not vacuous: its lower chain 1, 2, 3 is ccw, and the Haudit tests hit it.
  - `results/Haudit/t4_summary.txt` states the rule correctly: "U2.. or L3.. pairs".
  - `results/Haudit/AUDIT.md` NOTE-3 has the same wrong wording as the text.
- **Severity:** wrong.

**W2. Section 3, sub-case (i) paragraph.**
- **Text:**
  - "a rotation makes c leftmost on the axis, and a projective map (x, y) ↦ (x/d, 1/d) with d = y₀ − y sends c to vertical infinity";
  - "pairing i ↔ N − i".
- **Source:** `results/H3/MirrorEncoding/Frame.lean` header and `rotA`/`rotB`.
  - The map is `rotA` (x,y) ↦ (−y,x) or `rotB` (x,y) ↦ (y,x). `rotB` is a reflection: it reverses orientation (`orient_rotB`).
  - Sorting by slope from c then gives the hull frame. The formula x/(y₀ − y) is `results/C`'s description of the same frame; it is not a second map applied after the rotation.
  - The pairing σ(N−k, N−j, N−i) = σ(i,j,k) is 0-based. The rest of the text uses 1-based labels.
- `results/H3/README.md` §2 also calls both maps "a rotation".
- **Severity:** wrong.

**W3. Section 7, Commits.**
- **Text:** "V2-L tree data and `FinalTree.lean`: last changed in 6ba4e377 (the commit cited as e1d13c7b … maps to the same new hash)".
- **Source:**
  - `git log` shows that `results/V2-L/V2L/Trees/` and `scripts/gen_trees.py` were last changed in 8f3fdb83 ("V2G: tree data at Zf, …"), old hash 14fdad2c (`results/FINAL/COMMIT_MAP.tsv`).
  - 6ba4e377 is the last change to `FinalTree.lean`. It is also the new hash of e1d13c7b, which `results/V2-L/README.md` §9.5 cites only for the *trial* data.
- **Severity:** wrong.

**W4. NUMBERS.tsv, row "manifest leaf lines WAVE1 / 2 / 3 / 4 = 30151 / 12429 / 8850 / 28871".**
- **Source:** `results/V3Z/inputs.txt`. These are the leaf lines that `v3_jsonl_leaves.py` writes (jtree1..4) before merging. They sum to 80,301, while the manifest has 73,880 distinct leaves.
- **Severity:** wrong (label).

### Incomplete

**I1. Section 6, opening paragraph (overstated).**
- **Text:** the claim of no `sorry`/`admit`/`native_decide`/`axiom`/`implemented_by`/`extern` over the packages H, H3, V1-L and V2-L.
- **Source:** `results/V2-L/logs/tree_grep_forbidden.log` covers V2-L only (its 517 Lean files). `results/H/README.md`, `results/H3/README.md` and `results/V1-L/README.md` each say only: no `sorry`, `admit`, `native_decide` or new axiom.
- **Severity:** incomplete.

**I2. Section 6, trust base item 1.**
- **Problem:** the list of trusted definitions leaves out several definitions the theorem uses:
  - `ConvexPosition`, which `HasConvexNGon` is built on (`ErdosSzekeres/Definitions.lean`);
  - `hullLeaves` (V1-L, `V1L/Leaves.lean`, not V2-L);
  - `RootCertificate` and `UpCertificates` (`V2L/Main.lean`);
  - `upCubes`, `upTable`, `caseTable`, `casesOf` (`V2L/Facts.lean`) and `treeOf` (`V2L/Trees/Table.lean`).
- `convexHull` is Mathlib's, not H3's.
- **Severity:** incomplete.

**I3. Section 6, trust base item 2.**
- **Text:** "CaDiCaL, march_cu and the unpatched lrat-check (unsound) are not trusted".
- **Source:** `results/V2-L/README.md` §6 says the *patched* lrat-check is not trusted. `results/V1-L/SUMMARY.md` says the same and that drat-trim's unpatched lrat-check is unsound. Neither version is trusted.
- The text also does not say where the verdicts behind each hypothesis are recorded. `results/V2-L/README.md` §9.6 has a table of them.
- **Severity:** incomplete.

**I4. Section 6, trust base item 4.**
- **Problem:**
  - The grep that confirms "case file + leaf units" covers only the 56 WAVE1 driver scripts (`results/V2-L/README.md` §3), but the tree leaves come from WAVE1–WAVE4 (§9.6).
  - For sub-case (i), 291 of the leaves were checked by V1-L's backup driver `scripts/backup_leaves.py`, not by V1-0..V1-3 (`results/V1-L/SUMMARY.md`).
- **Severity:** incomplete.

**I5. Section 5, "Why the wave records were not accepted".**
- **Text:** "The waves ran 36 separately modified drivers".
- **Source:** `results/Haudit/AUDIT.md` RISK-3 is about the 36 WAVE1 machines. The drivers of WAVE2–WAVE4 were not reviewed ("Not checked").
- **Severity:** incomplete.

**I6. Sections 5 and 6, V3 contradicting-leaf path.**
- **Problem:** the text describes the path on which V3 accepts a leaf without a solver run, but does not say that no final leaf took it.
- **Source:** `results/V3Z/problems.txt` reports timings for n = 73,880 solved leaves, and `aggregate_final.py` times only leaves that do not contradict their cube.
- **Severity:** incomplete.

**I7. Section 1, "No SAT result occurred anywhere in the mirror runs" (overstated).**
- **Source:** `results/V3Z/README.md` covers the leaf and cover files of V3T, V3A–V3E and V3Z, and `results/Mii-S/README.md` §5 covers Mii-S. Neither covers the WAVE1–WAVE4 records.
- A grep by this review found no `SAT` status in the wave `leaves.jsonl` files. That is not stated in any source file, so it was not added to the text.
- **Severity:** incomplete.

**I8. Section 1, related work.**
- **Problem:**
  - The text cites only `docs/RELATED_WORK_2026-10-14.md`, not the dedicated search `results/LIT/RELATED.md` (21 Oct 2026, §3–§4: "We did not find prior work …"), or its limitation that sources were read from abstracts and snippets only.
  - Subercaseaux et al. are summarized as "3-, 4- and 5-fold at 16 points, 4-fold at 32 points" without the results. Per the source: for 16 points without a convex hexagon, 3-fold is UNSAT and 4- and 5-fold are realizable; for 32 points without a 7-gon, there is no realizable 4-fold set.
  - For Koshelev–Koshka, LIT §3 found only a 25-point 3-fold example for a hexagon-type variant. This disagrees with the 14 Oct survey's "axially symmetric 18 points" mention.
- The wording "we did not find prior work" and "No priority is claimed" was already correct.
- **Severity:** incomplete.

**I9. Section 3, mirror normalization.**
- **Problem:** X(i,j,k) = X(34−k,34−j,34−i) is the form for sub-case (ii) only. In sub-case (i), `results/C/scripts/mirgen.py` uses m = N + 2 on points 2..33. The text also does not give the reason the sign is + (the reflection negates every orientation, and reversing three indices is an odd permutation).
- **Severity:** incomplete.

**I10. Section 3, y-flip unit.**
- **Problem:** the text does not say why X(1,2,3) may be assumed.
- **Source:** `results/H3/README.md` §2: "Complementing σ keeps the signotope axioms, the mirror symmetry and gon-freeness", and it swaps the two interior clauses.
- **Severity:** incomplete.

**I11. Section 2, D_3 count.**
- **Problem:** "a mirror line carries at most 2 points, so b ≤ 2" skips steps:
  - each 3-orbit puts one point on each axis;
  - c = 0 by the C_3 case;
  - 33 = 6a + 3b forces b to be odd.
- The conclusion (a = 5, b = 1) is correct.
- **Severity:** incomplete.

**I12. Section 5, description of the waves.**
- **Text:** "march_cu top cubes (`march_cu CASE -d 7`, 128 cubes per top file in WAVE1)".
- **Source:** `verify/README.md` "Wave 1". Only the six hardest 4-gon cases were split by top cube; the other cases went whole to the driver. `results/V3Z/covers.jsonl` shows that 138 cases have the empty cube as their only leaf.
- **Severity:** incomplete.

**I13. Section 3, base CNF.**
- **Text:** "`gen_etv.py … --mirror`, Lean `ETV.etvClauses`, soundness proved in `results/H`".
- **Source:** `results/H3/README.md` §3. `mirClauses` is `ETV.etvClauses` (the option-free generator, proved in H) plus hull units plus the identification clauses. H does not prove the `--mirror` output itself.
- **Severity:** incomplete.

### Unclear

**U1. Section 5 and NUMBERS.tsv, pass2 timings.**
- **Problem:** "443 s CaDiCaL and 331 s cake_lpr in total" is the sum over the 172 verified records only. Over all 174 records the CaDiCaL time is 563 s; the two extra records are U_L2-3 and U_L2-4, result UNKNOWN (`results/Mii-S/pass2_lrat.jsonl`).
- **Severity:** unclear.

**U2. Section 7 and NUMBERS.tsv, V3 compute sums.**
- **Problem:**
  - `accepted_final.tsv` counts one VERIFIED record per leaf (not all 75,459 records), and adds the cover proofs (`results/V3Z/scripts/aggregate_final.py`, lines 110–116).
  - The real V3 compute is therefore larger.
  - The sums themselves are correct: 1,353,233.41 s and 301,295.45 s.
- **Severity:** unclear.

**U3. Section 1.** In "if the H3 tail is mild", H3 is a 3-fold top case in `results/C3-S/README.md`, not the directory `results/H3` that the text cites throughout. **Severity:** unclear.

**U4. Section 3, interior clauses.**
- **Text:** "some chord P_i P_{34−i} has c above it and some has c below it".
- **Source:** the clauses range over all X(i,17,k) with i < 17 < k (`mirgen.py --interior`, `AxisInterior`). The mirror chords are only the witnesses in the proof.
- **Severity:** unclear.

**U5. Section 2.**
- **Text:** "two independent constructions" of the D_3 class.
- **Source:** `results/E/README.md`. `n33k7d3direct` is the same generator `d3cnf.py` with the direct K-gon encoding. Only `n33k7m3refl` shares just the label rule with `d3cnf.py`.
- **Severity:** unclear.

**U6. Section 4.**
- **Text:** "satisfies exactly the cube of its own case".
- **Source:** `results/Mii-S/soundness.md` proves only that a configuration satisfies the cube of its own case. Uniqueness is only tested, and it is not needed.
- **Severity:** unclear.

**U7. Section 5.**
- **Text:** "5,589 cake_lpr-verified leaves from the C2 tree".
- **Source:** `results/H3/README.md`. These are C2's closed cubes plus C2's 1,048 open cubes refuted by H3, the last one after a split into 4 sub-cubes.
- **Severity:** unclear.

**U8. Whole text, repository jargon used without definition.**
- **Terms:**
  - wave, V3, V3T/V3A–E/V3Z, Zf, shard, Mi-0..3, Mii-S, Haudit, H/H3, C/C2, E/E2, V2F/V2G;
  - CNF/cube/leaf/cover, LRAT, cake_lpr, cube-and-conquer;
  - the case names U4_L, U_L7, U_L2;
  - "S-directories".
- **Notation** used without definition: reflX and orient (section 3), and "free orbits" (section 3).
- **Severity:** unclear.

**U9. Section 2.**
- **Problem:** "G is finite … so G is cyclic or dihedral" is stated without a reason, and the text does not say that the point reflection is the rotation of order 2.
- **Severity:** unclear.

**U10. Section 9.** "39 WAVE2 S-directories" is undefined. These are the directories of machines S1–S5 (`results/V2-L/README.md` §7a). **Severity:** unclear.

### Cosmetic

**C1. Section 1.** The Lean block was H3 README's abbreviation (`∀ S a u, …`), not the definition in `results/H3/MirrorEncoding/Line.lean`. **Severity:** cosmetic.

**C2. Section 6.** The path `logs/tree_grep_forbidden.log` lacks its `results/V2-L/` prefix. **Severity:** cosmetic.

**C3. Section 4.** The sha256 equality of the 122 CNFs is in `results/Haudit/AUDIT.md` task 3, not task 2. Task 2 is the independent construction. **Severity:** cosmetic.

**C4. Section 7, commands.**
- **Problem:** one `v3_check.py` command was given for both leaves and covers, with `--cap 1800`.
- **Source:**
  - Leaves: `--skip-covers --work W --cap 1800` (`results/V3B/TASK.md` step 4).
  - Covers: `--skip-leaves --jobs 4 --cap 3600` (`results/V3Z/README.md`).
- **Severity:** cosmetic.

**C5. Section 4.**
- **Problem:** `casesOf_length_sum` alone only says that the lengths sum to 450. With `upSets_nodup` and `caseSpecs_upper_mem` it gives a partition.
- **Source:** `results/V2-L/README.md` §4 adds: "Only the nonzero facts are used by the proofs".
- **Severity:** cosmetic.

**C6. Section 3.** `results/C/scripts/make_cnfs.sh` was called a "Python generator". It is a shell script that drives `gen_etv.py` and `mirgen.py`. **Severity:** cosmetic.

**C7. Section 2.** The quote "this is not a theorem" is from a later paragraph of `results/E/README.md`. The opening statement is "Nothing in this directory is a theorem", and that is now quoted. **Severity:** cosmetic.

**C8. Section 5 (not applied).** The REJECTED V3A record (`results/V3A/V07/out.jsonl`) has an empty `cake_lpr` field and rc 20. This could be added; the change was left out as optional. **Severity:** cosmetic.

## Checked and found correct

### Numbers

- **Mii-S cases:** 450 cases (30 with a 4-gon hull, 420 with a 6-gon hull); by |U|, 120 / 225 / 105; 121 = 1 + 15 + 105; 172 UNSAT_VERIFIED and 278 OPEN; cube lengths 61–535.
- **122 obligations:** 503 s / 222 s (Mii-S) and 515 s / 313 s (Haudit), with sha256 equal between the two runs.
- **172 direct cases (Haudit):** 699 s / 445 s, with sha256 equal to `cases.jsonl`.
- **READY.json:** Zf 14447d0d → 06c1f798, dated 2026-10-20T16:20:17Z; 278 wave cases, 0 open cubes; 73,880 leaves; manifest sha256 e01af167….
- **V3Z:**
  - covers 278 = 140 + 138;
  - 278 cases ACCEPTED;
  - 78 input files;
  - 75,459 leaf VERIFIED and 1 REJECTED records, and 377 cover VERIFIED and 9 NOT_COVERED, recounted;
  - the REJECTED leaf;
  - per leaf, median and max 10.9 / 730.0 s solve and 3.0 / 52.0 s check;
  - no SAT record.
- **V1-L:** 300 + 300 + 299 + 299 = 1,198 leaves; 26,142 s and 4,608 s; `hull_leaves.icnf` sha256.
- **V2-L:**
  - 74,000; 310; 140; 73,690; 910; 1,050; 220; 2,230 / 694 s; 2.98 GB; 52 (U_L7); 22,529; 411 / 74,031; 450 / 74,052; 517;
  - the sums 73,690 + 52 + 138 = 73,880, 172 + 138 + 73,690 = 74,000, and 73,880 + 172 = 74,052.
- **H3:** 47,002 / 515,121 / 535,454, both sha256 values, 5,589, 29 pinned axiom sets, the 84/84 grid, 1,340 open cubes.
- **Other runs:** C: 2,736. Haudit: 15,900 and 394. Mii-S: 279 and 1,480 s. C3-S: 1,956. C3WAVE2: 1,349 of 1,630. C3WAVE1: C00–C23.
- **Machines:** waves 36 / 12 / 26 / 75 (149); acceptance 1 / 9 / 16 / 16 / 24 / 8 / 1 (75).

### Hashes

All old → new translations agree with COMMIT_MAP:
- 14447d0d → 06c1f798
- bdf319c → 92746acb
- ff29bc68 → 569b763f
- e1d13c7b → 6ba4e377
- 6a44b5f → fef1a241
- a3e5d17 → a89d6de7
- f3b07a7 → 6664466f

Also confirmed:
- 3a04d94 is unchanged by the rewrite.
- 45bce6a0 is the V3Z summary commit.
- 852bee7 is the commit of `TASK.md`.
- The tool commits (CnC, CaDiCaL, cake_lpr) match `results/V3Z/tools.txt`.

### Lean

- The statements of `V2L.mirrorExclusionLine_final`, `axisInteriorLine_final`, `RootCertificate`, `UpCertificates`, `CTree` and `V1L.hullVertexLine_of_leaves` match the source.
- The axioms are as stated: `[propext, Classical.choice, Quot.sound]` for the main theorems, and `[propext]` for `treeOf_check`.
- The hypothesis count 1 + 121 + 1,198 + 74,000 is correct.
- The cake_lpr hash and trusted remainder are as in V2-L §6.
- The sections cited from V2-L (§3, §5, §6, §9.1–§9.6) say what the text claims.

### Mathematics

- The rotation orders: s ≥ 7, s even (through the half-turn), s = 5 (33 ≡ 3 mod 5), and s = 3 with the centre not in S.
- The D_3 orbit structure (a = 5, b = 1).
- Exactly one point on the axis.
- The + sign of the mirror identification.
- The AxisInterior identity (0 − x)(y − y) − (c.y − y)(−2x) = 2x(c.y − y).
- |V| ∈ {4, 6}, and the certificate argument for the 122 obligations.

### Commands and V3 behaviour

- The commands for F and for the manifest.
- `v3_check.py` `leaf_job` behaves as described: it drops cube literals, sorts by |literal|, and records a contradicting leaf as VERIFIED.
- The cover rule.
- V3T's two bugs and the 2,655 records.

## Changes applied

### MIRROR.md
- **Header:** new "Terms" paragraph, defining CNF/UNSAT/cube/`cubeCnf`/LRAT/cake_lpr/leaf/cover, the case names, every run directory and Zf (sources cited there; U8). The one-line LRAT gloss is a standard definition, not taken from a repository file.
- **Section 1:**
  - Lean block replaced by the definition from `Line.lean` (C1).
  - F defined at first use (U8).
  - "H3 tail" clarified (U3).
  - SAT sentence limited to what Mii-S and V3Z state (I7).
  - Related-work bullet rewritten from `results/LIT/RELATED.md` and the 14 Oct survey, still "We did not find prior work" and "No priority is claimed" (I8).
- **Section 2:**
  - Finiteness reason and the half-turn added (U9). The finiteness argument is elementary and not from a source.
  - D_3 count completed (I11).
  - Description of the two D_3 constructions corrected (U5).
  - E quote corrected (C7).
- **Section 3:**
  - Base CNF / `mirClauses` (I13).
  - Sub-case (i) identification and the sign argument (I9).
  - Sub-case (i) normal form rewritten from `Frame.lean` (W2).
  - reflX and orient defined; interior clauses corrected (U4, U8).
  - y-flip justification (I10).
  - `make_cnfs.sh` (C6).
- **Section 4:**
  - "exactly" removed (U6).
  - `casesOf_length_sum` (C5).
  - task 3 / task 2 (C3).
  - Vacuous-case rule corrected and the NOTE-3 discrepancy noted (W1).
- **Section 5:**
  - The 5,589 leaves (U7).
  - pass2 records and timings (U1).
  - Wave description (I12).
  - RISK-3 scope (I5).
  - No final contradicting leaf (I6).
- **Section 6:**
  - Forbidden-word grep scope (I1).
  - Trust base items 1, 2 and 4 (I2, I3, I4).
  - No final contradicting leaf (I6).
  - Log path (C2).
- **Section 7:**
  - V2-L tree commit (W3).
  - Leaf and cover commands (C4).
  - Meaning of the V3 compute sums (U2).
- **Section 8:** vacuous-case row (W1).
- **Section 9:**
  - S-directories (U10).
  - New items: the vacuous-case rule (W1), `rotB` in `results/H3/README.md` (W2), and Koshelev–Koshka (I8).

### NUMBERS.tsv
- Row "manifest leaf lines" relabelled (W4).
- V3 seconds rows relabelled (U2).
- Mii-S direct-case seconds row relabelled (U1).
- Vacuous-case row: rule stated and `t4_summary.txt` added (W1).

### README.md
- Note that no final leaf took V3's no-solver path (I6).
- Pointer to this report.

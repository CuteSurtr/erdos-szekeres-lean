# VERIFY_N66: independent adversarial check of "N66 ≤ 59" (the 18:11 certificate, data/cert59)

Phase-2 verifier, 13 November 2026, 20:21–21:00 KST. Scratch directory `/home/jay/research/data/verify-N66-20261113`
(abbreviated V; not in Git). Units `nov13c-vfy-N66-{pb,rows,real,recert,rtest,recert2,sub,final,e2e}`, one thread at a
time, MemoryMax 1.0–1.5 GB each (largest peaks: cake_lpr 1.03 GB with a 1,000 MB heap; Python 0.73 GB); none was
stopped by the memory guard. No git state was changed; this file is the only file written in the repository.

**Verdict: CONFIRMED.** Every component of the 18:11 certificate was re-checked with my own code and re-run through
cake_lpr: the PB step (with my own encoder and with the record's CNF), all 3,052 row justifications (with my own
tables), all 281 template CNFs and all 68 core CNFs (hash, a clause-by-clause recognizer, cake_lpr), and a real-set
test (5,524 sets, 0 violations). No mathematical error was found. The problems found are about the record and its
tooling (§5), not about the bound.

## 1. Method

I read the README line by line before testing (198 lines, version of 20:26; A2 rewrote it at 20:43 and added
§3–§9, which I read for §4.1 and §7). My code was written from the README's definitions, not copied from the
track: `V/vmodel.py` (states, cells, τ, refined domains, triple table), `V/pbmine.py` (PB encoder),
`V/gen66.cpp` (real sets, exact `__int128` determinants), `V/realtest.py`, `V/verify_rows.py`, `V/recert.py` +
`V/recert_sub.py` (clause recognizer and re-certification), `V/e2e.py`. I used the track's code in two places only:
(a) `coupled5.py` / `bigcore.py` regenerate the text of each template/core CNF from its recorded parameters, so that
the text can be compared with the recorded SHA-256 and then checked clause by clause by my recognizer, and
`coupled5.CNF` is evaluated against real geometry in `e2e.py`; (b) one comparison of its cached triple table and
state order with mine. None of the record's checker scripts (`final_verify66.py`, `pb_consistency.py`,
`check_bigtemplate.py`, `realcheck66.py`, `soundness_test2.py`) was used as evidence.

## 2. Verdicts per claim

| Claim (README) | Verdict | Basis |
|---|---|---|
| §2.1–2.4: labels in [1..4]², growth with ceilings, 70 states, state separation, fixed states (0,0,0,0), (1,0,0,0) | confirmed | Arguments re-derived (state separation: if d(t,u) ≥ d(u,v) componentwise, the triple (t,u,v) is neither a cap nor a cup). 70 = C(8,4) nonincreasing 4-tuples. Real sets: owners always have distinct states, both fixed states always occupied (§3.3). |
| §2.5 Lemma R and refined domains D′ | confirmed | Proof re-derived (predecessor on an attaining chain; a 2-point chain gives label 1). My D′ equals the record's for all 70² pairs. |
| §2.6 cycle rows; triple table 29,436 forced, none both ways, cyclic | confirmed | My table from the definition (impossible orders skipped): 29,436 entries, 0 differences from the record's, 0 triples with both orientations, cyclically invariant. "All triples in list order positive" implies convex position in that order, so at most 7 occupied. All 51 cycle rows of the subset are 8-lists with demand 1; 51/51 orders pass my table. |
| §2.7 coupled CNF families | confirmed | Every clause of all 349 certified CNFs is an instance of a valid family (§4). Signotope property and the convex_four formula checked on 18,730 random integer quadruples (the formula in an arbitrary labelling). End-to-end: `coupled5.CNF` on 1,302 real supports, 58,714,759 clause evaluations with my own assignment, 0 violations (§3.5). |
| §2.8 mirror lemma (τ = transposition) | confirmed | Proof checked (ρ keeps the x-order, negates determinants, swaps caps and cups, keeps convexity; the class is ρ-closed). τ recomputed: 16 fixed states including both fixed states, capH∘τ = cupH, D′ transposes, TT[τa,τb,τc] = TT[a,c,b]. On real sets Occ(ρS) = τ Occ(S) (ETV set; and for the x-flip/rotation pair). All 1,487 mirror rows equal τ of a verified core/transported support. |
| §2.9 big-template format, transport | confirmed | For each of the 281 templates, every state-dependent clause of the regenerated CNF is valid for the template's own core and for each of the 2,866 σ uses in the justification file (my tables; the record's test lists were not relied on). The static part of each CNF is byte-identical to a static file whose every clause my recognizer accepts; the counts equal the complete families (no-octagon family absent in the 198 + 60 "noct" CNFs, which add 8,717 listed octagon clauses). |
| §2.10 no block rows (COMPUTED, negative) | not checked | Not used by the certificate (the subset has no block rows). |
| PB certificate "≤ 10 holes" over 3,052 rows (CNF `92048925…`, LRAT `9272dfbc…`, cake_lpr) | confirmed | Own encoding: cake_lpr `s VERIFIED UNSAT`. Record CNF: hash equal, CaDiCaL reproduced the LRAT bit for bit, cake_lpr `s VERIFIED UNSAT` (§3.1). |
| 281/281 templates and 68/68 cores cake_lpr-verified | confirmed | 349/349 regenerated CNFs hash-equal to the record. 223 re-verified directly by cake_lpr; 126 via a sub-CNF (the original clauses used by CaDiCaL's proof on the full CNF, re-proved, cake_lpr `s VERIFIED UNSAT`). Each sub-CNF clause is a line of the validated full CNF, so its UNSAT certifies the row. The record's own LRAT for these 126 full CNFs was not re-checked (my heap cap was 1.5 GB). |
| **N66 ≤ 59 CERTIFIED** | **confirmed** | The components above; the label CERTIFIED is justified. |
| Later claims (A2, read 20:46): N66 ≤ 58 (trimmed monolithic CNF cake_lpr-accepted at 20:39, rows and clause check pending); level 12 searches; driver | not verified (noted only) | Outside this task. The README itself labels N66 ≤ 58 as not yet CERTIFIED. |
| Novelty | no overstatement found | The N66 record makes no novelty claim. NOVELTY20261113B §3 (C8) and §2: nothing below cup-cap 70 was found for N(8; 6, 6) for general point sets; 50 is the ETV/Baek–Balko lower value. |

## 3. Checks run (commands and outputs)

### 3.1 PB certificate (unit nov13c-vfy-N66-pb; log V/pb/pb.log)

- Row file `data/cert59/subset11_rows.json`, SHA-256 `7a175cbf8b1e4f7cbce720d9a266718d41ab3f0c9e4e6823cd1494821ce31b91`
  (equals the justification file's rows_sha256 and `W/final11/subset_rows.json`). All 3,052 rows have demand 1;
  supports are sorted and distinct; 415 contain a fixed state (it is dropped from the clause, since it is never a hole).
- My encoding (`python -I V/pbmine.py subset11_rows.json 10 mine10.cnf`): h_s = "state s is a hole", unit ¬h for
  (0,0,0,0) and (1,0,0,0), a Sinz sequential counter (my code) for Σh ≤ 10 over the 68 others, one clause ∨h per row.
  750 vars, 4,462 clauses, SHA-256 `489f24fb6c1b8d58892a30e9f164bbf4b0e73f2e4e018821b38c0606c47b5afd`.
  `cadical -q --lrat=true --binary=false` exit 20 (11 s), LRAT 146,083,542 bytes, SHA-256
  `5515eb7b6cf513db271e2d69523aaaf014caf5bc24068db4c6e1d83ba65db344`;
  `cake_lpr --CML_HEAP_SIZE=1000 --CML_STACK_SIZE=100` → `s VERIFIED UNSAT`.
  The encoding is sound in the needed direction: a hole vector with ≤ 10 holes, none on the fixed states and one
  in every row extends to a model (counter variables = true prefix counts).
- Record CNF `W/final11/pb_sub/pb.cnf`: SHA-256 `920489253e49d2b8527ff32771b08afa05cc2956f149d3c20711657b5b4f4ab0`;
  CaDiCaL 2.1.3 gives an LRAT of 162,152,215 bytes with SHA-256
  `9272dfbc3364eff199dd1713e054d1879931e6dab2f0b301a0bb4e79b472a244` (bit-identical to the record);
  cake_lpr → `s VERIFIED UNSAT`.
- Sanity: my encoding with the first 2,000 rows at budget 10 → SAT; all 3,052 rows at budget 11 → SAT. These
  rows give exactly "at least 11 holes", hence |S| ≤ 70 − 11 = 59 for |S| ≥ 2.

### 3.2 Tables and row justifications (unit nov13c-vfy-N66-rows; V/verify_rows.out, V/ttprops.out)

- State order (Σf, f) equals the record's; my refined domains equal the record's; my plain triple table equals
  the record's cache entry for entry (29,436 true, 0 differences); no triple is forced both ways; cyclically
  invariant; TT[τa,τb,τc] = TT[a,c,b].
- `justification11.json.gz`: (support, demand) multiset equal to the 3,052 rows; kinds 51 cycle,
  1,447 transported, 67 core, 1,487 mirror. With my tables: cycle orders 51/51; transported rows (and the
  transported preimages of mirror rows): σ injective, sorted(σ) = support, |σ| = |core|, every recorded test holds,
  template id = hash of (core, tests, octs); mirror rows: support = sorted τ(preimage). **0 bad rows**; 281 templates
  and 68 cores used; every template's tests also hold on its own core.

### 3.3 Real-set test (units nov13c-vfy-N66-real, nov13c-vfy-N66-recert; V/realtest.out)

- `V/gen66.cpp`: class check = distinct x, no collinear triple, longest cap ≤ 5, longest cup ≤ 5, largest convex
  polygon ≤ 7 (exact DP over left/right endpoints); profiles from the exact labels. Greedy random sets: pure random
  multi-scale insertions, and random subsets of the ETV set and its reflections grown by random insertions
  (690 seeds × 2 modes × 4 sets, 300 s; every generated set was in the class).
- ETV 50-point set from `R/ETVTHY20261113/tools/etvcon.py` (`etv(8,6,6)`) and its images under (x,−y), (−x,y),
  (−x,−y): all four in the class (cap 5, cup 5, convex 7), 50 distinct states each. The ETV holes are exactly the
  20 states with f₁ = 4 and f₄ ≥ 1.
- 5,524 in-class sets (42 with 50 points, 1,405 with 40–49, 2,615 with 30–39, 1,462 with 20–29); all 70 states
  occur as owners. **0 violations of the 3,052 certificate rows; 0 violations of the 12,906 rows of
  `W/final11/rows_all.json`.** 3,324 sets have a certificate row with exactly one hole (the rows are tight).

### 3.4 Template and core CNFs (units nov13c-vfy-N66-recert2 and nov13c-vfy-N66-sub; V/recert.jsonl, V/recert_sub.jsonl)

For each of the 349 records (281 templates, 68 cores; sizes 9–29 states):
1. Regenerated the CNF text from (core, tests, octs) or (support, octs) with the track's generator. **SHA-256 equal
   to the recorded `cnf_sha256`: 349/349.**
2. Decoded the variables with my own numbering (pairs: before, cap_ge 2..4, cup_ge 2..4; then triples; then
   quadruples). The variable count equals the header in all 349.
3. Recognizer: each clause must be an exact instance of threshold, transitivity, growth with the ceiling 4 (both
   types, k = 1..4), signotope (forbidden pattern with more than one sign change in x-order), convex_four definition,
   no-octagon on an 8-set (all 70 quadruples), or a state-dependent clause (empty / domain / positive). The 25
   distinct static blocks (n = 9…29, with and without the octagon family) were checked once each: all clauses are
   recognized and the counts equal the complete families, e.g. n = 29: threshold 1,624, transitivity 21,924, growth
   175,392, signotope 4,560,192, convex 380,016 (5,139,148 clauses). The non-static clauses (220,871 domain,
   19,408 empty, 56,430 positive, 8,717 octagon) are all recognized. **0 unrecognized clauses.**
4. Each state-dependent clause is valid (my D′ and TT) for the core's own states and for every σ that uses the
   template (2,866 σ in total). **0 invalid.**
5. cake_lpr. First pass: CaDiCaL LRAT + cake_lpr on the full CNF, 223/223 `s VERIFIED UNSAT` (18 further runs
   only failed with "CakeML heap space exhausted" because I set the heap too small). Second pass, for the other 126
   (n = 17…29): the original clauses used by CaDiCaL's proof on the full CNF were extracted (for example n = 29:
   7,638 of 5,140,022), re-proved by CaDiCaL and checked by cake_lpr (heap 900 MB): 126/126 `s VERIFIED UNSAT`.
   **349/349 ALL_OK.**

### 3.5 End-to-end semantics of the generator (unit nov13c-vfy-N66-e2e; V/e2e.out)

434 real sets (the ETV set and its three images, and 430 random sets with 25–50 points), 3 random supports of 8–11
occupied states each: `coupled5.CNF(support)` (with the complete no-octagon family and all state-dependent clauses),
evaluated on my assignment (x-order, exact labels, determinant signs, brute-force convex position): 1,302 CNFs,
58,714,759 clauses (963,433 state-dependent), **0 violations**. The C++ profiles equal a Python recomputation on all
434 sets.

## 4. What the certificate establishes

Under the written arguments of §2 (which I re-derived) and the trusted checker cake_lpr: every planar set with
distinct x-coordinates, in general position, with no 6-cap, no 6-cup and no convex octagon has at least 11 holes
among the 70 states, so N66 ≤ 59. The 3,052 rows do not give 12 holes (budget 11 is satisfiable over them).

## 5. Problems found (none affects the bound)

1. **Record incomplete when phase 1 ended.** The README version I read at 20:21 (modified 18:39) cited "§4.1" (the
   certificate) and "§5" (the ETV set). Neither section existed; the certificate was described only in the 18:11
   log entry. The 20:26 version also cited a nonexistent "§7". A2's rewrite of 20:43 added §3–§9, and §4.1 now
   matches what I verified.
2. **Not reproducible from the repository alone.** `tools/` in the record was still empty at 20:53, although
   README §1 and §7.1 say the tools are copied there. The code (`coupled5.py`, `bigcore.py`, …) and the static clause cache (`W/static`, 1.2 GB) are
   only in W. The template/core CNFs and all LRAT proofs were deleted, and only their hashes are kept. They are
   deterministic: I regenerated all 349 CNFs and the PB LRAT bit for bit. The justification file names its row file
   by a path relative to W (`final11/subset_rows.json`).
3. **The record's own final checker does not tie the template certificates to their content.** `final_verify66.py`
   accepts a transported/core row when the cert list says `s VERIFIED UNSAT`. It does not regenerate the template CNF
   or compare its hash, and it does not check that the certified CNF contains only valid clauses. The construction
   in `template_cert66.py` gives this, and `check_bigtemplate.py` controls only 6 random supports of ≤ 14 states.
   I closed the gap independently (§3.4: hashes, recognizer on every clause, validity for every σ).
4. **Template tests are under-described.** For the soundness of a transported row, what counts is that every
   state-dependent clause of the template CNF is valid for σ. The recorded test list is the tool's way of ensuring
   this. I checked the clauses themselves, so this is a documentation point only.
5. Labels: §2.10 (no block rows) is COMPUTED and not needed. The README's phase-1 controls (§5: 459 sets /
   1,836 CNFs; 14,914 rows against real sets) are the track's own and were not re-run as such; §3.3 and §3.5 above
   replace them.

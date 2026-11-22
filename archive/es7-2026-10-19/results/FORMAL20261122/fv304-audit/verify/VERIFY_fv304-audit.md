# VERIFY_fv304-audit: independent review of the FV304 closing audit (lens: statement fidelity, Lean)

Reviewer slot rv4, 22 Nov 2026, 18:02–18:50 KST. Work directory, the only place written:
`/home/jay/research/data/formalize-20261122/fv304-audit/verify` (3.7 MB). Default when unsure: not confirmed.
Own code throughout (`tools/`); the audit's scripts were read, not used.

## 1. Headline

**DONE. All five claims CONFIRMED, each at its stated label.** Nothing is running.
- I ran ONE compile, `src/RV.lean`, with no olean written. It re-printed the statements and axioms from the FV304 and
  audit oleans, and it checked every theorem type against my own transcription of the claimed signature.
- It also re-derived the combined theorem in my own file, kernel-checked: **ES(8) ≤ 304 is Lean-checked modulo
  `N66Bound 55`, the four `BlockValid` and the six `ResSliceExcludes`**, with only `propext`, `Classical.choice`
  and `Quot.sound`.
- No new bound, and no label changes. The hypotheses stay outside Lean and were not re-checked:
  - N66 ≤ 55: CERTIFIED plus a written model;
  - the six slices: EXACT TREE;
  - the 2,021 rows: CERTIFIED plus the written encoder argument.
- Statement fidelity: the conclusion unfolds to the standard Erdős–Szekeres statement.
  - N66Bound matches N66N §1's definition of N66.
  - Each slice hypothesis's (B, T) and row data match its tree artefact (packet master or `verify_stream.out`, and the
    row file). The remaining tree semantics and the base-row binding are taken from res118 (§5 R7).
  - The literal data inside the hypotheses, read from the kernel terms, equal the six hash-identified slice row files.
  - The meaning of both final statements depends on no E304Z, CompactChecker or chain311 tree module. The 8,217
    E304Z oleans, whose hashes are first recorded by the audit, matter only for the proof.
- My own re-hash of both import closures (13,199 and 13,382 modules) agrees with the audit's TSVs in every row and
  with every earlier pin.

## 2. Claims under review

| key | label claimed | verdict |
|---|---|---|
| `fv304-final-reprinted` | Lean-checked (re-confirmed from FV304's oleans) | **confirmed** |
| `fv304-mangled-axiom-logs` | Lean-checked re-print; log diagnosis COMPUTED | **confirmed** |
| `fv304-import-closure` | COMPUTED | **confirmed** |
| `combined-304-modulo` | Lean-checked modulo N66Bound 55 + 4 BlockValid + 6 ResSliceExcludes | **confirmed** |
| `res118-and-support-rebuilds` | COMPUTED | **confirmed** (own hashes; compile provenance from the audit's logs and systemd's journal; not recompiled by me) |

## 3. What the review checks, and why that suffices

- An import does not re-check an olean, so the kernel check of the E304Z chunks happened in FV304's compiles. A
  re-print from the same olean bytes confirms what those bytes state and which axioms they use. It does not re-run the
  kernel on them.
- My own theorems `RV.forces_304` and `RV.forces_304_alt` are kernel-checked in my compile. They re-check the
  composition step, not the imported proofs.
- Statement fidelity has three parts:
  - the types equal my transcription of the claims, up to alpha-equivalence (`Expr ==`);
  - the definitions unfold, by defeq, to explicit statements I wrote in Mathlib terms;
  - the literal data in the hypotheses equal the evidence files, which are identified by sha256.
- Non-vacuity:
  - `ErdosSzekeres.not_forcesConvexNGon_64_8` (library, standard axioms) shows the conclusion's predicate is not
    trivially true;
  - no unit row is empty, out of range, has a repeated state, or lies inside {0, 1}.
    - State 0 is occupied in every nonempty residual configuration (`zero_mem_residualOccupied`), so a row inside {0}
      would make `BlockValid` false.
    - The {0, 1} test is only a heuristic guard. "State 1 fixed for n ≥ 2" is shown for the 70-state N66 catalog
      (N66N §2.4), not for the 154-state residual catalog;
  - N66Bound 55 is consistent with the known 50-point Erdős–Tuza–Valtr set (N66N §1);
  - truth of the hypotheses is outside this review.

## 4. Method

- **A. Hashes.** My own sha256sum of the 45 artefacts named in the claims. Logs, run.tsv, driver.log and the sources
  were read directly.
- **B. Two-roots walk** (`tools/shadow.py`): `.olean`, `.olean.server` and `.olean.private` over FV304's 14 roots, the
  same with the audit's `olean/` appended, and the negative control with `res118/olean`.
- **C. The ONE compile**, unit `esr-ag-rv4-fv304s` (18:22:15–18:38:49).
  - Settings: 1 thread, MemoryMax 4000M, MemorySwapMax 0, RuntimeMaxSec 3600, nice 10.
  - Command: `lean -j1 -R src src/RV.lean` with the bare v4.24.0 binary, no `-o`.
  - LEAN_PATH: FV304's `lean_path.txt` plus the audit's `olean/`, both read only.
  - Pre-registered stop: anon+shmem ≥ 3,200 MB.
  - Contents: `#check`, `#print axioms` and `#print` lines; the two own theorems; meta checks inside try/catch, so a
    transcription slip could not change lean_rc; a decoder that reads the row data from the kernel terms; and a dump of
    every module's direct imports.
- **D. Closure re-hash** (`tools/closure.py`), unit `esr-ag-rv4-fv304h` (18:41:41–18:42:48, 1 thread, MemoryMax 4000M).
  - The closures come from my own import dump.
  - Each module is resolved against the 15 roots; exactly one may provide it.
  - Each `.olean` is hashed and compared with the audit TSVs and with library.json (root and hash), the last ok row
    of chain311 `build.tsv`, the 311 route record (`chain.inputs`, with the symlink target), LemmaZ (ES305 README),
    BalancedBudgetsZ (comp-audit), the FcatZ/BridgeZ rebuilds, res118's oleans and the claimed Combined hash.
  - Companions are recomputed in comp-audit's own digest format. The 8,207 chunk sources are checked against the
    context manifests. The mtime order is checked as compile start = olean mtime − wall.
- **E. Row binding** (`tools/rows_bind.py`, own parser, self-tested): Rows.lean, LemmaA.lean and the kernel-decoded
  data against the six slice row files.

## 5. Results

- **R1 Hashes.** All 45 claimed sha256 values equal my sha256sum (`data/claimed_artefacts_sha256.txt`). They
  include:
  - `src/Audit.lean` `908f9e9d…`, Final.olean `ef479c06…`, Root.olean `ab5be7fb…`, the lean binary `8fadc3ed…`
    and `lean_path.txt` `65463fd5…`;
  - the four chunk oleans, `src/FV4A/Combined.lean` `ada157ef…` and `olean/FV4A/Combined.olean` `9e71de87…`;
  - all data/log files named.
- **R2 Statements re-printed** (my `#check`, the same text as the audit's):
  - `E304Z.Final.excludes_67 : OmissionBalancedZ.ExcludesHoleBudgetZ 67`;
  - `E304Z.Final.forces_304_of_n66_res (n66 : OmissionZRow.N66Bound 55) (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) : ErdosSzekeres.ForcesConvexNGon 304 8`;
  - `E304Z.root : ¬∃ holes, CompactChecker.FFeas CompactChecker.fcatZ 3132 252 67 (CompactChecker.pmask (CompactChecker.zerosF 252) []) holes`;
  - `FV4A.forces_304_of_slices_rows_n66`, with the 11 hypotheses of the claim.
- **R3 Axioms.** Each of the following prints exactly `[propext, Classical.choice, Quot.sound]`; `rows_lengths`
  uses none:
  - excludes_67, forces_304_of_n66_res and E304Z.root;
  - E304Z.{C260801, C311801, C325201, C634501}.ex0;
  - FV4A.forces_304_of_slices_rows_n66, RV.forces_304 and RV.forces_304_alt;
  - Res118.forces_304_of_slices, Res118.residual_bound_118_of_slices and composition_304_z;
  - BridgeZ.balanced_z_of_root, Res118.F_eq, Res118.Lo_eq and not_forcesConvexNGon_64_8.
- **R4 Own transcription.** Every type above is alpha-equivalent and defeq to my transcription of the claimed
  signature, including Res118.forces_304_of_slices with the tree hypothesis first.
  - `RV.forces_304 := Res118.forces_304_of_slices E304Z.Final.excludes_67 …` and
    `RV.forces_304_alt := E304Z.Final.forces_304_of_n66_res n66 (Res118.residual_bound_118_of_slices n66 …)` are
    kernel-checked.
  - Both have exactly the type of FV4A.forces_304_of_slices_rows_n66. That type has no ExcludesHoleBudgetZ.
- **R5 Unfolding** (defeq to my explicit statements):
  - `ForcesConvexNGon 304 8` = for every `s : Finset (Fin 2 → ℝ)` with no three distinct points `Collinear ℝ` and
    304 ≤ |s|, there is t ⊆ s with |t| = 8 and `ConvexIndependent ℝ`. That is ES(8) ≤ 304.
  - `N66Bound 55` = every `Configuration n` (strictly increasing x, every increasing triple with `orient ≠ 0`) with
    no 6-cap, no 6-cup and no 8 points in convex position has n ≤ 55. This is N66N20261113 §1's N66 ("distinct
    x-coordinates, general position, no 6-cap, no 6-cup, no convex octagon").
  - `HasCap`/`HasCup` = all increasing triples have negative / positive `orient`, and
    `orient a b c = (b0−a0)(c1−a1) − (b1−a1)(c0−a0)`.
  - `ResidualBound 118`: as in Partition.lean and LEAN_STATUS §2.
  - The definitions printed from the oleans equal the source texts. These are the library's Definitions,
    Orientation, Realization, Partition and Subsets, LemmaZ, BalancedBudgetsZ, Res118 Glue/LemmaA, Transfer and the
    2650 Catalog.
- **R6 What fixes the meaning** (a walk over types, definition bodies and inductives; proofs skipped):
  - `forces_304_of_n66_res`: 2,313 constants in 179 modules: Mathlib 139, Init 28, ErdosSzekeres 9, Batteries 2,
    LemmaZ 1.
  - The combined theorem: 2,552 constants in 205 modules, adding Res118.{Glue, LemmaA, Rows}, Transfer,
    Residual32Bridge2650.Catalog and the library's ResidualCatalog modules.
  - Neither statement depends on any E304Z, CompactChecker or chain311 tree module.
  - Opaque constants reached:
    - Mathlib `irreducible_def` wrappers (Real operations, Finsupp, rank);
    - in the combined and excludes_67 statements, the core `String.Internal.append`. It is most likely reached through
      the panic branch of `!`-indexing in the catalog arrays; not traced.
- **R7 Hypothesis data.** Decoded from the kernel terms: rowsP/Q/U/A have 812/208/35/970 rows, 0 undecoded, equal to
  Rows.lean in order; fIndices (84) and loIndices (70) equal LemmaA.lean.
  - Hence each of the six slice row files has capacity rows exactly (fIndices, T) and (loIndices, B − T), and unit
    rows exactly the stated block concatenation in file order, all with rhs 1. The file sha256 values equal res118
    README §4: `1d6141af…`, `1b72eb93…`, `770d276d…`, `c9c922c0…`, `1257c4a1…`, `de4bcceb…`.
  - There are 2,021 distinct rows (U ∩ A = 4). F_eq and Lo_eq bind Res118.F and Res118.Lo to the two lists.
  - **Budgets come from the tree artefacts themselves**, not only from res118's table.
    - The five es308 packet masters (`runs/{s18,s19,b35s18,b35s19}/bb/master.json`, `runs/b35s20/bb-s1/master.json`;
      sha256 prefixes `72c5a954…`, `1e956e2b…`, `e1f3cfb9…`, `249497e8…`, `71993a47…` = res118 README §4) record
      `budget` 34, 34, 35, 35, 35. They also record `extra` = exactly the row file bound above, `source` =
      `source-2650.json.gz` and `root` 0.
    - LO33N's `verify_stream.out` (`7b88742c…`) records budget 33, capacity pair (66, 55) = (84 − 18, 70 − 15), 1,908
      leaves, 1 pending and minimum margin 1.
    - So (B, T) in each `ResSliceExcludes` hypothesis matches its tree.
  - Not re-checked here: the remaining tree semantics (0/1 holes; state 0 occupied as the only pending leaf; base rows
    = `source-2650.json.gz` = `support2650`/`demand2650`). They are taken from res118 README §2/§4 and res118's
    COMPUTED `check_base_rows`.
- **R8 Logs (claim 2).** My regex is the full line `'E304Z.<m>.<name>' depends on axioms: [propext, Classical.choice,
  Quot.sound]`.
  - Of the 8,207 chunk logs, exactly four have no such line: C260801, C311801, C325201 and C634501.
  - No log has a non-standard axiom line.
  - C634501's log contains the substring 0 times, and its run.tsv row is `… 6571 0 2:16.43 0 0 718`.
  - FV304's driver.log has ALERTs only for C260801 (06:36:31) and C325201 (07:37:19).
  - `drive_es304z.verdict` counts the substring, so ax = std = 0 raised no alert.
- **R9 Closure (claim 3)**, `data/closure_rv.json`; `problems: []`:
  - **E304Z.Final** has 13,199 modules, equal to `modules_audit.txt` and the TSV module set.
    - By class: 4,883 library.json, 87 chain311 build.tsv, 8 route inputs (symlinks into `build/CompactChecker`),
      LemmaZ `ef249ba1…`, BalancedBudgetsZ `38d8f8ae…`, FcatZ and BridgeZ equal to the rebuilds, and 8,217 E304Z
      without an earlier pin (8,207 chunks, 8 S3, Root, Final).
    - Each module is provided by exactly one root, my sha256 equals the TSV row, and every pin matches.
  - **FV4A.Combined** has 13,382 modules: 4,952 library.json (all of library.json), 195 chain311, 8 route, 10 fixed
    pins and 8,217 E304Z. All are equal and pinned. `modules_combined.txt` lists 13,381, because the environment of
    Combined.lean lacks FV4A.Combined itself.
  - **Digests** recomputed from my own hashes: audit `84fdbbe9…`, its E304Z part `fa02576e…`, combined `a8c70049…`.
    All three equal the claim.
  - **Two roots:** none on the 14 roots or with `olean/` appended. The res118 control names exactly BalancedBudgetsZ
    and CompactChecker/{Fast, Fast2, Packed, Path, Split, WordPack}.
  - **Companions:** 3,464, all in the toolchain root. In comp-audit's format the digest is `9b3b8546…` = its
    06:05 value, and the set is equal.
  - **E304Z support:**
    - all 8,207 chunk sources equal their manifest sha256, none corrupted;
    - Final.lean equals git HEAD `drive_es304z.FINAL` (`1fcaabf0…`);
    - the S3 and Root source hashes are recorded in `closure_rv.json`;
    - all 8,217 logs end `lean_rc=0` with no error line; C075301 and C334201 are under the pilot2 names `c-<m>.log`;
    - 0 mtime-order violations.
- **R10 Rebuilds (claim 5).**
  - The five Res118 oleans in the audit's root equal res118's (`7d8fa1d2…`, `135216d0…`, `64b1888f…`, `0d325186…`,
    `64af03ba…`).
  - The FcatZ (`7aba4aa7…`) and BridgeZ (`4481a28c…`) rebuilds equal FV304's, from sources equal to git HEAD
    (`da544bd9…`, `382bf3bc…`).
  - The C000001, C634501 and S3_7 rebuilds equal FV304's. `recompile/pilotname/C751401.olean` equals FV304's
    `586c1dd1…`, while `recompile/E304Z/C751401.olean` is `35822323…`.
  - Each rebuild log records a real compile (`lean -j1 -R … -o ….tmp`, lean_rc 0, 3–141 s).
  - systemd's own journal, independent of the audit's files, records each unit consuming CPU time that matches the
    logged wall time:
    - `esr-ag-fv4a-res-{Rows,LemmaA,Glue,Final,Compose304}`: 8.7, 7.9, 12.4, 3.9 and 3.0 s;
    - `sup-FcatZ` / `sup-BridgeZ`: 2.5 / 2.9 s;
    - `smp-C000001`, `smp-C751401`, `smp-C634501`, `smp-S3_7`, `smp-pilotname`: 8.6 s, 18.4 s, 2 min 20.6 s,
      24.8 s, 18.1 s.
    - So these were compiles, not copies.
  - FV304's own C751401 log shows `lean -j1 -o … src/E304Z/C751401.lean` with no `-R`. Exactly 7 FV304 logs use
    `src/E304Z/` paths, and they are the 7 pilot.tsv modules.
- **R11 Memory of the one compile:** anon+shmem peak 516 MB. memory.peak was 4,197 MB, with 161,291 `high` events;
  that is page cache of the mapped chunk oleans. lean_rc 0, 16:34 wall, no oom.
- **R12 Read only:** `find -L … -newer` over the 14 roots, `build/CompactChecker` and `res118/olean` gives 0 files newer
  than the audit's start marker (16:39) and 0 newer than mine (18:02). FV304's newest olean is Final.olean, 12:19:18.

## 6. Controls

- **rows_bind.py self-test:** the in-order comparison rejects a one-entry mutation, a dropped row and a swap (asserted).
- **Two-roots negative control:** appending `res118/olean` is refused, naming the expected 7 files.
- **Cross-checks against the audit's own records** serve as controls for my code: the closure module sets, the 13,199
  and 13,382 TSV rows, three digests, and comp-audit's companion digest. All agree. A wrong closure walk or a wrong
  hash would have shown up as a difference.
- **No negative Lean control was run**, because only one compile was allowed. The meta checks report `alpha=true` and
  `defeq=true`; there was no deliberately wrong transcription to show that they can report false.

## 7. Files and hashes (sha256; `data/verify_sha256.txt`)

| file | sha256 |
|---|---|
| `src/RV.lean` | `36c7d00658fd21125a88f0c62235a2257cbffb3e4d4569262f494b023cc06774` |
| `logs/rv.log` | `1e4a93d5a0479f28646681ec4be41668e56a6f66bb85e5f9fc9cb9b426ce9516` |
| `data/lean_path_rv.txt` | `39b8d782c7857137ebb0300e15a077cb551a8638b6dba86a1a156dfadcfe865b` |
| `data/shadow.json` | `6c93f25ccdaa0dd39dba2001fdefff141d10838292929411de731f0000b3b6a4` |
| `data/rows_bind_source.json` | `8719485656f8fc94274bcd1aac96bf95c8d5523d526875ae21661b78f148fc77` |
| `data/rows_bind_kernel.json` | `49b0fb7305f5574a6636ec6f92523e5ad8bb51ceeaebe3ac1cc29342c245d5b8` |
| `data/closure_rv.json` | `456f3a2e42543bcaaa1cffda4eea2221a165df276dd6cd85ca2e2559f7dd3473` |
| `data/closure_rv_hashes.tsv` (13,382 files) | `3d4eb98bd49024f1b3ffe11dfdbaa2d9e537712e1ce2666867fceb47480c516a` |
| `data/claimed_artefacts_sha256.txt` | `1b6bb3332e62a1b9981c0494362e3645130e1a0b860934a4210b727f7a7a7063` |
| `tools/closure.py` | `4934735c3ac8e3a209a5658b6b9a635d5de9470aa2e7f72885fa2c4c0a51aca4` |
| `tools/rows_bind.py` | `7aef49f05b76f8bcbb9b15ddbfed5e9dab6a06d16725554355cac7067a75a596` |
| `tools/shadow.py` | `323fbb64c5c81bf6e141dd29386851d221824271fda25e3572fa00ede9b51e06` |
| `tools/unit_rv.sh` / `tools/launch.sh` | `99984dd6…` / `1bf0e0fc…` |

## 8. What remains, and findings

1. **Not re-checked here:** the truth of the hypotheses.
   - N66Bound 55 is CERTIFIED (132 cubes) plus the written model. The certified N66 ≤ 54 (cubes20261120 §8) implies
     it.
   - The six ResSliceExcludes are EXACT TREE.
   - The 2,021 rows are CERTIFIED plus the written encoder soundness.
   - The base-row binding (support2650 and demand2650 equal source-2650.json) is res118's COMPUTED check.
   - The binding of the row files to the certified CNFs (pool812.json etc.) is in the records.
2. **Not rebuilt by me.** No E304Z, Res118 or support module was recompiled, because only one compile was allowed.
   - Byte-identity of fresh rebuilds rests on the audit's logs and files: 5 Res118, 2 support and 4 E304Z modules.
   - The other 8,213 E304Z oleans rest on FV304's compile logs, the mtime order, source = manifest, and hashes first
     recorded by the audit, which my re-hash reproduces. This is short of the 310 standard of pre-recorded olean
     hashes, as the claim itself says.
3. **The audit's `check_pins_es304z.py` was not re-run**; this review uses its own code.
   - Own code covers all 4,952 library.json pins (root and hash), the 195 chain311 pins and the 8 route inputs in the
     closures.
   - Not covered here: the toolchain/manifest file hashes and the build/ext catalogs that check_pins also checks.
4. **Extra import.** My compile also imported `ErdosSzekeres.LowerBound.Construction`, which adds 6 library modules
   that are not in library.json's pins, built 4 Nov 23:40. They serve only the non-vacuity check `¬ ForcesConvexNGon 64
   8`. They are not in the closures above, and the two-roots walk covers them.
5. **Finding (the audit already reported it):** FV304's per-module axiom gate counts a substring. A profiler-spliced
   line (C634501) is invisible to it.
   - The transitive `#print axioms excludes_67` covers every chunk theorem the Root uses, so the result is unaffected.
   - The 303/302 runs should parse one well-formed line per `#print axioms`, or drop `set_option profiler true`.

## 9. Resume

Nothing to resume; both units finished. To repeat the review from this directory:
```bash
V=/home/jay/research/data/formalize-20261122/fv304-audit/verify
python3 -I -B $V/tools/shadow.py $V/data/shadow.json                   # seconds
python3 -I -B $V/tools/rows_bind.py $V/data/rows_bind_source.json      # seconds
$V/tools/launch.sh esr-ag-rv4-fv304s 600 3600 /bin/bash $V/tools/unit_rv.sh                 # the one compile, ~17 min
python3 -I -B $V/tools/rows_bind.py $V/data/rows_bind_kernel.json $V/logs/rv.log
$V/tools/launch.sh esr-ag-rv4-fv304h 300 3600 /usr/bin/python3 -I -B $V/tools/closure.py $V/logs/rv.log $V/data/closure_rv.json   # ~1 min, reads ~48 GB
```

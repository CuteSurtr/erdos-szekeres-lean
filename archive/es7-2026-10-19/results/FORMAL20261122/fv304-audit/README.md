# fv304-audit: closing import audit of FV304 and the combined 304 theorem (22 Nov 2026)

## 1. Headline

Status: **DONE**. The driver finished at 17:29 KST, the re-check at 17:32 and the sample rebuild at 17:47. Verdict in
`result.json`: **audit passed**, with findings (§8). Nothing is running. Work directory, the only place written:
`/home/jay/research/data/formalize-20261122/fv304-audit` (73 MB). Start marker `MARKER_START` (16:39:46 KST).

1. **FV304 closing audit: passed.**
   - A fresh `src/Audit.lean`, compiled here against the FV304 oleans (read-only, no olean written), re-prints both
     results with axioms `[propext, Classical.choice, Quot.sound]`:
     - `E304Z.Final.excludes_67 : OmissionBalancedZ.ExcludesHoleBudgetZ 67`;
     - `E304Z.Final.forces_304_of_n66_res (n66 : OmissionZRow.N66Bound 55) (hR : …ResidualBound 118) : ErdosSzekeres.ForcesConvexNGon 304 8`.
   - The import closure of `E304Z.Final` has **13,199 modules**, each provided by exactly one LEAN_PATH root
     (COMPUTED: `data/closure_audit.tsv`, own code, independent re-check). The evidence differs by class:
     - **4,980 match a hash recorded before this audit**: 4,883 library.json, 87 chain311 `build.tsv`, 8 311-route
       inputs, LemmaZ (ES305 §7) and BalancedBudgetsZ (comp-audit).
     - **2 are byte-identical rebuilds** from their git-HEAD sources: FcatZ and BridgeZ.
     - **8,217 E304Z modules have no earlier hash.** Their sha256 are first recorded here.
       - Support: the 8,207 chunk sources equal their context manifests and Final.lean equals the tracked template.
         The 8 S3 sources and Root have no earlier reference: their hashes are recorded only.
       - Every log ends `lean_rc=0`, and the mtime order holds.
       - A sample of 4 (3 chunks and S3_7) was rebuilt off-path byte-identically, each under the main-module name it
         was compiled with (§5).
     - The 3,464 `.olean.server` and `.olean.private` companions, all in the toolchain root, equal comp-audit's set and
       digest from 06:05.
   - `check_pins_es304z.py` re-ran clean. An independent re-check (coreutils sha256sum, own code) found 0 problems.
2. **Combined theorem: Lean-checked.** `FV4A.forces_304_of_slices_rows_n66`, with standard axioms:
   **ES(8) ≤ 304 is Lean-checked modulo `N66Bound 55`, `BlockValid rowsP/Q/U/A` and the six `ResSliceExcludes`**.
   - The budget-67 tree is no longer a hypothesis: it is the Lean theorem `E304Z.Final.excludes_67`.
   - **No new bound, and no label changes.** N66 ≤ 55 stays CERTIFIED with a written model, the six slices stay
     EXACT TREE, and the 2,021 extra rows stay CERTIFIED with a written encoder argument (res118 README §4, [R]).
3. **Main finding.** FV304's per-module axiom check (`drive_es304z.verdict`) silently passed **C634501**, whose axiom
   line was split by profiler output (run.tsv: 0 axiom lines, 0 standard).
   - Four logs in all lack a well-formed axiom line: C260801, C325201, C311801 and C634501.
   - All four were re-printed here from their oleans with the standard axioms.
   - The two driver ALERTs of 06:36 and 07:37 were this interleaving, not non-standard axioms.

## 2. Statement

1. FV304 (`/home/jay/research/data/fv304-20261120`) finished at 12:19.
   - **Re-run the pin check.** Run `check_pins_es304z.py` read-only (as `python3 -I -B`, so no .pyc lands in the
     repo), plus comp-audit's pin checks.
   - **Record the full import closure of `E304Z.Final`.** For every module: the providing LEAN_PATH root, the resolved
     file, the olean sha256, the pin class and its status. Refuse any module that two roots provide.
   - **Re-print `#check` and `#print axioms`** of both Final theorems in a fresh `Audit.lean` compiled here.
2. **Combined theorem** `FV4A.forces_304_of_slices_rows_n66`, from `E304Z.Final.excludes_67` and
   `Res118.forces_304_of_slices`, with no tree hypothesis and standard axioms. Both olean stores must be on one
   LEAN_PATH with no duplicate module.

## 3. Model and soundness

- **What the kernel checked.** Lean's kernel checked every declaration when its module compiled. An import trusts the
  .olean bytes and does not re-check them against a source. The audit therefore fixes which bytes were imported, from
  which root, and whether each matches a recorded pin. It also checks that nothing could have bypassed the kernel:
  - no forbidden tokens in the sources;
  - axiom audits;
  - the import order.
- **Why the tree statement needs no binding to the tree files.** `E304Z.Final.excludes_67` is a closed statement
  about `ExcludesHoleBudgetZ 67`, and `E304Z.root` is stated at the empty path, so it covers both sides of state 0.
  Its truth does not depend on how the chunk sources were generated: the exporter, the tree files and the replay are
  outside the trust base. They matter only for provenance.
- **Pin classes** (column `pin` of `data/closure_*.tsv`):

  | class | source of the pin |
  |---|---|
  | library.json | `build/chain311/library.json` (4,952 oleans, 11 roots) |
  | chain311 build.tsv | last ok row |
  | 311 route record | `logs/es311/final311-compact.json` chain.inputs. The symlink must resolve into `build/CompactChecker` |
  | ES305 pin = comp-audit rebuild | LemmaZ `ef249ba1…` |
  | comp-audit rebuild | BalancedBudgetsZ `38d8f8ae…` |
  | rebuilt here from git HEAD source | FcatZ, BridgeZ: byte-identical off-path rebuild |
  | first recorded here (FV304 run.tsv has no hash) | E304Z/*: see below |
  | this build | Res118.*, FV4A.Combined |

  - E304Z/* rows are "ok" only when all of the following hold:
    - the source sha256 equals the context manifest (chunks) or the git-tracked template (`E304Z.Final`);
    - the log ends `lean_rc=0` with no error;
    - every `#print axioms` of the source appears standard, in the log or in a re-print;
    - every import is older than the module's compile start, where compile start = olean mtime − wall.
  - **This is short of the 310 standard**, where run.tsv carried every olean hash before the assembly. Here the
    hashes were recorded only after the fact (§8).
- **Memory rule** (pre-registered, §4): anon+shmem sampled every 0.2 s must stay below 3,200 MB (80 % of
  MemoryMax 4000M).

## 4. Method

- **Driver.** `tools/fv4a.py`, resumable (`data/step_<name>.json`; status in `status.json`, log in `driver.log`).
  - It ran as unit `esr-ag-fv4a-drv` (1 thread, MemoryMax 4000M, MemorySwapMax 0, RuntimeMaxSec 14400, nice 10).
  - It launches one child compile at a time, `esr-ag-fv4a-<job>` (1 thread, MemoryMax 4000M), with body
    `tools/unit_lean.sh`.
  - Every compile uses the bare `/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean -j1 -R src`
    (sha256 `8fadc3ed…`) and an explicit read-only LEAN_PATH:
    - FV304's `lean_path.txt` verbatim (14 roots, sha256 `65463fd5…`);
    - for Res118 and Combined, that list plus this directory's `olean/`.
  - No lake, no lean-lsp, no git writes (only `git show`).
- **Gates before every child and every step**: no YIELD file; Tctl < 86 °C (poll 60 s, up to 45 min); `cpu_free.sh
  esr,esv` ≥ 1; ag-track and esr-total use (anon+shmem+swap) each at least 1,000 MB below their budgets.
- **Memory rule** (written in this README before the first compile):
  - The guard counts anon+shmem+swap and turns MemoryMax into `memory.high`.
  - About 25 GB of chunk oleans are mapped by an `import E304Z.Final`, so `memory.peak` ≈ 4,000 MB and `high` events
    are page cache. They are reported, not a stop.
  - Binding measure: anon+shmem sampled every 0.2 s. At 3,200 MB the sampler sends SIGTERM to lean and the driver
    stops. Any oom or oom_kill event also stops it.
  - "Measure first": FV304's Root and Final compiles peaked at 429 and 451 MB anon. The Audit compile measured
    453 MB before the Combined compile started.
- **Steps**:

  | step | what it does |
  |---|---|
  | pins | `check_pins_es304z.py`; lake roots = library.json = chain311 `lake-lean-path.txt`; 0 lake oleans newer than the 4 Nov freeze; 196 chain311 oleans = build.tsv; LemmaZ/BalancedBudgetsZ pins; 12 tracked files = git HEAD (and = record pins for the two ES305 sources) |
  | shadow | two-roots check (.olean/.server/.private) on both LEAN_PATHs; negative control with `res118/olean` |
  | support | FcatZ, BridgeZ rebuilt off-path |
  | res118 | 5 modules rebuilt |
  | audit | `src/Audit.lean` |
  | combined | `src/FV4A/Combined.lean` |
  | records | 8,192 manifests; sha256 of all 8,217 E304Z sources (20.7 GB); structural scan; logs; run.tsv; mtimes |
  | reprint | `src/Reprint.lean` |
  | closure | closure TSVs |
  | readonly | `find -newer MARKER_START` |

  - Structural scan: forbidden tokens, first token of every line, set_option/import/open/#print lines, tactic forms.
  - After the driver: `tools/recheck.py` (unit `esr-ag-fv4a-recheck`), an independent re-check of both closure TSVs.

## 5. Results

| step (KST) | result |
|---|---|
| pins 16:51:02 | passed (detail below) |
| shadow 16:51:02 | no module file provided by two roots, on FV304's 14 roots or with `olean/` appended; negative control refused |
| support 16:51:08 | FcatZ `7aba4aa7…` and BridgeZ `4481a28c…` byte-identical to FV304's; 3 s each, anon ≤ 289 MB; fcatZ_wf [propext], BridgeZ theorems standard |
| res118 16:53:46 | the 5 copied sources = res118 README §7; 5 rebuilt oleans byte-identical to res118's; all axiom lines standard; largest anon 1,322 MB (Glue) |
| audit 16:53:46–17:04:30 | lean_rc 0, 643.8 s (251 s user, 74 s sys); anon 453 MB; cgroup 4,002 MB = page cache (172,838 `high` events); max RSS 14.3 GB; no oom |
| combined 17:07:28–17:12:50 | lean_rc 0, 321.7 s; anon 464 MB; page cache as above (91,822 `high`); max RSS 17.8 GB; no oom |
| records 17:16:59–17:20:33 | passed with 4 findings (detail below) |
| reprint 17:27:34 | `src/Reprint.lean` imports the 4 modules; all 4 `ex0` print `[propext, Classical.choice, Quot.sound]`; 3.7 s, anon 219 MB |
| closure 17:27:38–17:29:32 | every row ok (table below) |
| readonly 17:29:35 | 0 files newer than the marker in every read-only store; 3 new repo files outside them (below) |
| recheck 17:32 | `data/recheck.json`: 0 problems |

**pins** in detail:
- `check_pins_es304z.py` (git HEAD `b484b16e…`):
  - rc 0;
  - 4,952 library oleans as pinned (digest `39bc4023…`, pinned 2026-11-06T00:11:21Z);
  - 13 route inputs = the 311 record;
  - build/ext catalogs = chain311;
  - symlinks inside build/CompactChecker.
- 196/196 chain311 oleans equal build.tsv.
- 0 lake oleans newer than the freeze.
- LemmaZ.olean `ef249ba1…` and fv304 BalancedBudgetsZ.olean `38d8f8ae…`.
- 12/12 tracked files equal git HEAD.

**shadow**: the negative-control refusal names exactly BalancedBudgetsZ.olean and
CompactChecker/{Packed,Fast,WordPack,Split,Fast2,Path}.olean.

**records** in detail:
- Context manifests: 8,192 contexts (0..8191), 8,207 chunk modules, none corrupted.
- Sources:
  - all 8,207 chunk sources equal their manifest sha256;
  - Final.lean equals `drive_es304z.FINAL` (git HEAD) byte for byte;
  - the 8 S3 and Root sources were hashed and recorded.
- Structural scan of the 8,216 generated sources:
  - 0 forbidden tokens (sorry, admit, native_decide, ofReduceBool, skipKernelTC, implemented_by, extern, unsafe,
    `axiom `, `debug.`, run_cmd/elab/meta, #eval, elab, macro, syntax, `@[`, attribute, instance, opaque, partial);
  - first tokens only theorem/noncomputable/checkF2_feas/split_pm/set_option/--/import/open/namespace/end/#print;
  - set_option only maxRecDepth 100000, Elab.async false, linter.all false and profiler true;
  - non-E304Z imports only CompactChecker.FcatZ, CompactChecker.Path, CompactChecker.BridgeZ and BalancedBudgetsZ;
  - all 261,918 `by ` are `by decide +kernel`.
- Every log has lean_rc=0 and no error.
- Every import is older than its importer's compile start.
- `E304Z.Final` has the newest olean.

| closure | modules | pin classes (all status ok) | TSV sha256 | digest (all) | digest (E304Z part) |
|---|---|---|---|---|---|
| `E304Z.Final` (Audit) | 13,199 | library.json 4,883; chain311 87; route 8; LemmaZ 1; BalancedBudgetsZ 1; rebuilt-here 2; E304Z first-recorded 8,217 | `fa81fcce…` | `84fdbbe9…` | `fa02576e…` |
| `FV4A.Combined` | 13,382 | library.json 4,952; chain311 195; route 8; LemmaZ 1; BalancedBudgetsZ 1; rebuilt-here 2; E304Z 8,217; this build 6 | `c49920ad…` | `a8c70049…` | `fa02576e…` |

- The combined closure contains the whole audit closure. Its 183 extra modules are the residual chain that
  `Res118.Glue` imports through `Residual32Bridge2650.Rows`, plus Res118.* and FV4A.Combined. That means 108 more
  chain311 modules, including ResidualCoverCutsV2 and RankCore*, and 69 more library modules, all pinned.
- The E304Z set of both closures equals the expected 8,217 modules: 8,207 chunks, 8 S3, Root and Final. The pilot
  oleans `S12_1671`, `S12_376` and `FinalTest` exist in `fv304/olean/E304Z` but are not imported.

**readonly**: the 3 new repo files are `.git/objects` ce/b5b881…, cb/dc11f0… and 55/d09e74… (2 blobs, 1 tree),
written at 17:04:19.
- Read with `git cat-file`:
  - the tree is the ES303N20261120 record directory;
  - blob 55d09e74 is that record's README ("ES(8) ≤ 303 ESTABLISHED");
  - blob ceb5b881 is the N66 level-15 campaign README.
- These are other writers' record files. The writer was not identified.
- No command of this audit writes to git: its only git commands are `git show` (pins step, 16:51) and
  `git cat-file`/`git log` (read only, 17:30). At 17:04 the driver was blocked waiting on the Audit lean unit.
- At 17:48, a final `find` again gave 0 newer files in every read-only store. In the repo outside `.git`, one file is
  newer: `archive/…/STATUS20261121_1930/README.md`, the status handoff that another writer edits. This audit never
  writes to the repo.

**companions** (`data/companions_{audit,combined}.tsv`, sha256 `3f0c1c7f…`; both closures identical):
- 3,464 `.olean.server` and `.olean.private` files exist for closure modules, all under the toolchain root
  (Init/Std/Lean). The list digest in this audit's format is `81fbc1d0…`.
- In comp-audit's format, recomputed now over comp-audit's `closure.tsv`, the digest is `9b3b8546…`. That equals
  comp-audit's recorded value from 06:05, and the set equals this closure's.
- So the toolchain companions are unchanged since then. library.json pins only `.olean` files, so comp-audit's record
  is the only earlier reference for them.

**sample rebuild** (after the driver; `tools/sample_rebuild.py`, `data/sample_rebuild.json`):
- Four E304Z modules were rebuilt off-path into `recompile/`: C000001, C751401, C634501 and S3_7.
  - Sources were copied, with sha256 equal to `data/e304z_modules.json`.
  - Each compiled in a gated unit with FV304's LEAN_PATH: lean_rc 0, anon ≤ 759 MB.
- Byte-identical to FV304's oleans as `E304Z.<m>`: C000001 `c3222df2…`, C634501 `5c7da916…` and S3_7 `7fca1bcf…`.
- **C751401 differed** (`35822323…` against `586c1dd1…`).
  - Cause: its FV304 olean was built by the first pilot, whose log shows `lean -j1 -o … src/E304Z/C751401.lean` run
    from `export/`. The main-module name was therefore `src.E304Z.C751401`.
  - Rebuilt with that module name (`-R` = work dir; `logs/smp-pilotname-C751401.log`), it is **byte-identical**
    (`586c1dd1…`).
- So all four reproduce byte for byte from their recorded sources under their compile-time module names.
- Per their logs, the 7 pilot.tsv modules carry the main-module name `src.E304Z.<m>`: C334301, C751401, C420801 and
  C075201–04. The public theorem names come from `namespace E304Z.<m>`, so imports are unaffected. This is provenance
  only.
- The C634501 rebuild log again has its axiom line split by profiler output, at the same place. Its axioms come from
  `step_reprint.json`, on the identical bytes.

**Statements and axioms** (`data/statements_*.txt`, `data/axioms_*.txt`; whitespace-normalised `#check`):
- `E304Z.Final.excludes_67 : OmissionBalancedZ.ExcludesHoleBudgetZ 67`
- `E304Z.Final.forces_304_of_n66_res (n66 : OmissionZRow.N66Bound 55) (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) : ErdosSzekeres.ForcesConvexNGon 304 8`
- `E304Z.root : ¬∃ holes, CompactChecker.FFeas CompactChecker.fcatZ 3132 252 67 (CompactChecker.pmask (CompactChecker.zerosF 252) []) holes`
- `FV4A.forces_304_of_slices_rows_n66 (n66 : OmissionZRow.N66Bound 55) (vP : Res118.BlockValid Res118.rowsP)
  (vQ : Res118.BlockValid Res118.rowsQ) (vU : Res118.BlockValid Res118.rowsU) (vA : Res118.BlockValid Res118.rowsA)
  (s33_18 : Res118.ResSliceExcludes [] 33 18) (s34_18 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 34 18)
  (s34_19 : Res118.ResSliceExcludes Res118.rowsP 34 19) (s35_18 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 35 18)
  (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
  (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) : ErdosSzekeres.ForcesConvexNGon 304 8`
- Every one of the following depends on exactly `[propext, Classical.choice, Quot.sound]`:
  - from the Audit: excludes_67, forces_304_of_n66_res, E304Z.root, C260801.ex0 and C325201.ex0;
  - from the reprint: C260801.ex0, C311801.ex0, C325201.ex0 and C634501.ex0;
  - from the Combined: FV4A.forces_304_of_slices_rows_n66, Res118.forces_304_of_slices and
    Res118.residual_bound_118_of_slices.
- The definitions in the statements were printed from the oleans (`data/defs_audit.txt`, `data/defs_combined.txt`):
  - ExcludesHoleBudgetZ, N66Bound, ResidualBound and ForcesConvexNGon, as in LEAN_STATUS §2;
  - BlockValid, ValidUnitRow (with the `0 < n` premise, res118 §8.5), ResSliceExcludes, lsupp, F, Lo, InLo and
    loProfile.

## 6. Controls

- **Two-roots refusal (negative control)**: appending `res118/olean` to FV304's LEAN_PATH is refused (`data/step_shadow.json`).
  That is why Res118 was rebuilt into this directory's own root and not used in place.
- **Reproduction controls**: these rebuilds are byte-identical to the oleans that FV304, res118 and this build import:
  - FcatZ and BridgeZ, from the git-HEAD sources;
  - the five Res118 modules.
- **Parser self-tests** (`fv4a.selftest`) run at every driver start. They include a spliced axiom line from the
  C260801 log, which must parse as "garbled".
- **Independent re-check** (`tools/recheck.py`, separate code; `data/recheck.json`):
  - coreutils `sha256sum` of all 13,382 distinct closure files equals the TSV rows;
  - root uniqueness by a direct existence test per root;
  - resolved paths match;
  - library/chain311 pins match on fresh parses of library.json and build.tsv;
  - the E304Z set of the audit closure equals {Root, Final} ∪ the import lines of the Root and S3 sources (8,217).
  - Result: 0 problems; 26 s, 1 thread. The unit's memory peak of 3.9 GB is page cache from reading the files; its
    anon was not sampled (it holds only the two TSVs).

## 7. Files and hashes (sha256)

| file | sha256 |
|---|---|
| `src/Audit.lean` | `908f9e9d4075d84c58b0badc693b9940382c7dda373b23060b0710fdabeddbf9` |
| `src/FV4A/Combined.lean` | `ada157eff6de74be4578e03498d015f06e39071bd4dddb96df04c393d53dc2e1` |
| `src/Reprint.lean` (generated by the driver) | `654fdc50913d7cb0e08441ba749848285e6ebe80bd1389a1003a93ce2b53bf12` |
| `src/Res118/*.lean` (copies) | = res118 README §7 |
| `src/CompactChecker/{FcatZ,BridgeZ}.lean` (copies) | = git HEAD `da544bd9…`, `382bf3bc…` |
| `olean/FV4A/Combined.olean` | `9e71de8761341db1afaadce264c9b4e60c206b8d7d70ebf636db650ac6a19ca8` |
| `olean/Res118/{Rows,LemmaA,Glue,Final,Compose304}.olean` | `7d8fa1d2…`, `135216d0…`, `64b1888f…`, `0d325186…`, `64af03ba…` (= res118's) |
| `tools/fv4a.py` (final) | `f553c915c891ab230fde0c24754f01b8a86bc61e3ba5ce1b815863b414cf9bd7` |
| `tools/unit_lean.sh` | `10d31245fc45943e7a57ad236afe7974204ff026a7207a35ad93587124cb83dd` |
| `tools/recheck.py` | `05e569b56bb2c4ca0ab2357810a8b6f76efd25cd13ee6c6d9ea9bf3a7e4e2c09` |
| `data/closure_audit.tsv` | `fa81fcce0eb56d16a1f0bb9bfa5d7d213bd9588dbc5580c7072a1050736eae53` |
| `data/closure_combined.tsv` | `c49920ad97ff3c7e9f340c204ddecea8250f714a0abaa37d4d3abc7b8adbd7a5` |
| `data/modules_audit.txt` / `modules_combined.txt` | `f29645db…` / `6d92cebe…` |
| `data/e304z_modules.tsv` (per module: source sha256, check, log, rc, axioms, re-print, mtimes) | `595465a8fa3aae3591be91dcf90d7692e7d789ec45edc2cded2a567644c8acaa` |
| `data/axioms_audit.txt` / `axioms_combined.txt` | `84df8844…` / `fa417ccf…` |
| `data/statements_audit.txt` / `statements_combined.txt` | `91526aee…` / `b46b44fe…` |
| `logs/audit.log` / `combined.log` / `reprint.log` | `8a828977…` / `e97fb505…` / `f715d3eb…` |
| `result.json` | `46657f1f7df513f8f69596d4d70a648bf8cb38a7438f89133944f51015f2a3b6` |
| `data/recheck.json` | `eae21f9cfe940d52d3276e7e479720672f418d7a1c2340ab2f7596341ca26e41` |
| `data/companions_audit.tsv` (= `companions_combined.tsv`) | `3f0c1c7f5a125593cf2ce160f1d188bab2b0e14b7ba79d9001315c7fc8d16e56` |
| `tools/sample_rebuild.py` | `9c54edb4c969e8da3ee25fd1fe84692f33cb4d3e50c3c8e2525f09629d029c2f` |
| `data/sample_rebuild.json` | `b2e014bea91e14d5c9f748363f59271c0e6795738e31f5f7e245ff309dbd9846` |
| `recompile/E304Z/{C000001,C634501,S3_7}.olean` (= FV304's) | `c3222df2…`, `5c7da916…`, `7fca1bcf…` |
| `recompile/E304Z/C751401.olean` (as `E304Z.C751401`) | `35822323c3273336df36cdd86c4afbb355ac4ea4cba1ac14a0214a331f790190` |
| `recompile/pilotname/C751401.olean` (as `src.E304Z.C751401`; = FV304's) | `586c1dd1c0f2e806b5ae3da52af74012c7ff98baee227aa88014becd1e3d8143` |

- Closure digests are sha256 over the sorted lines "module\tsha256\n":

  | closure | digest (all) | digest (E304Z part) |
  |---|---|---|
  | audit | `84fdbbe978f877083d56c93f813d78d488a9a12919f0369094b64cc30e0f2fee` | `fa02576ef5752c7fa509ea9f74b95feb46e4fdce9de26292b6df19c654b36c76` |
  | combined | `a8c7004950cc601e13006e777f284627c6842281afb8e872aeb0e8a39470bea6` | same as audit |

- Inputs, read-only:
  - FV304 `lean_path.txt` `65463fd5…`;
  - the 311 route record `logs/es311/final311-compact.json`;
  - library.json, digest `39bc4023…`;
  - the per-step JSONs, which hold every other hash: `data/step_*.json`.

## 8. What remains, findings

1. **Hypotheses outside Lean, unchanged.**
   - `N66Bound 55`: CERTIFIED (132 cubes) plus a written model.
   - Six `ResSliceExcludes`: EXACT TREE.
   - Four `BlockValid` (2,021 distinct rows): CERTIFIED plus the written encoder soundness.
   - The Lean ↔ JSON binding of rowsP/Q/U/A, F and Lo is COMPUTED (res118's and its reviewer's own checks).
   - None of these was re-checked here.
2. **FV304 driver finding.** `drive_es304z.verdict` counts the substring "depends on axioms".
   - C634501's axiom line was split inside "depends", so the driver counted 0 = 0 standard: no ALERT, run.tsv
     `0 0`. C311801's split line still contained the counted substring.
   - The four affected modules were re-printed standard here, and the transitive axioms of `excludes_67` cover every
     chunk theorem that the Root uses.
   - Suggested fix for the 303/302 FV runs: drop `set_option profiler true` from the generated sources, or parse one
     well-formed line per `#print axioms` name.
3. **E304Z olean hashes first recorded here** (`data/closure_audit.tsv`).
   - FV304's run.tsv has no hash column, so there was nothing to compare them against.
   - Support: sources = manifests or template; logs rc 0; mtime order; byte-identical rebuilds of the support modules.
   - A sample of 4 of the 8,217 was rebuilt byte-identically (§5). The other 8,213, and Root and Final, were not
     rebuilt.
   - This is short of the 310 standard.
4. **Provenance notes, not soundness.**
   - The six pilot contexts (752, 753, 3342, 3343, 4208, 7514; 9 modules) were exported by a pilot exporter
     (`9fbce4ce…`, not in git). The other 8,186 used git HEAD `eee1151c…`.
   - 26 modules have no run.tsv row (pilot compiles and driver restarts); their per-module logs were used.
   - 7 pilot modules were compiled under the main-module name `src.E304Z.<m>` (§5, sample rebuild).
   - My own `lean_ok` accepts a log with no parseable axiom line, the same blind spot as FV304's driver. None of the
     results relies on it:
     - Audit, Combined and Reprint check the expected names explicitly;
     - the support and Res118 logs parsed fully;
     - the sample's C634501 axioms come from the reprint.
   - No shapes or coverage gate ran for FV304; the empty-path Root makes the coverage kernel-checked.
5. **Driver history, own tools.**
   - The first audit parse failed in my statement parser: Lean wraps `#check` signatures despite `format.width`. The
     fix joins continuation lines, and the rerun reused the same compile and log, verified equal to the unit record.
   - The driver was stopped by hand at 17:05 while idle at the gate, to add a thermal gate before every step. It was
     restarted at 17:07 at Tctl 85.8 °C.
   - Its first restart had been launched at Tctl 87.1 °C; it only waited at a child gate. The old records code
     refused C634501 as designed (17:16). At 17:27 the driver's own CPUQuota was lowered to 20 % at runtime, because
     the 28-thread cap was full and the driver only waits and hashes.
6. **For the owner (repo, not written here).** LEAN_STATUS §5 and §9 finding 6 ("no closing audit") can now point to
   this directory. Before a record is written, the combined theorem's Lean file should be copied into the res118 /
   ES304 record by the main session.
7. **Disk.** These remain regenerable per LEAN_STATUS §5; this audit gives no deletion verdict:
   - `fv304-20261120/export/src` (20.7 GB) and the chunk oleans (25 GB);
   - their hashes are now in `data/e304z_modules.tsv` and `data/closure_audit.tsv`.
   - This directory holds 73 MB.

## 9. Resume

The driver is resumable: a step whose `data/step_<name>.json` says `"ok": true` is skipped, and a failed compile's
log is re-parsed rather than recompiled when it still matches its unit record. It pauses while YIELD exists and waits
while Tctl ≥ 86 °C (45 min, then it stops with "refused").

```bash
W=/home/jay/research/data/formalize-20261122/fv304-audit
systemctl --user reset-failed esr-ag-fv4a-drv 2>/dev/null   # only if an earlier run of this unit failed
systemd-run --user --unit=esr-ag-fv4a-drv -p CPUQuota=100% -p MemoryMax=4000M -p MemorySwapMax=0 \
  -p RuntimeMaxSec=14400 --nice=10 --working-directory=$W /usr/bin/python3 -I -B $W/tools/fv4a.py
# independent re-check of the closure TSVs:
systemd-run --user --unit=esr-ag-fv4a-recheck -p CPUQuota=100% -p MemoryMax=4000M -p MemorySwapMax=0 \
  -p RuntimeMaxSec=3600 --nice=10 --working-directory=$W /bin/sh -c 'python3 -I -B tools/recheck.py > data/recheck.json'
```

- To redo a step, delete its `data/step_<name>.json` (in this directory only). A full redo deletes all of them plus
  `data/units.jsonl`.
- The heavy steps (audit, combined) each re-import about 25 GB of chunk oleans: about 5–11 min each, anon about
  450 MB.

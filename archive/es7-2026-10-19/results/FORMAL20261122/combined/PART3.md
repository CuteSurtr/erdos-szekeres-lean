# combined part 3: FV302's tree and the slice s35_20 discharged (PRE-REGISTRATION, written 25 Nov 2026 16:02 KST)

Written before `E302ZZ.Final` (FV302) and `RS.Final3520` (res-slices-fv) exist: at 16:02 FV302 had 29,905 chunk
modules and 29 of 32 sub-roots compiled, s35_20 20,855 modules (no Root, no Final). Nothing here has been compiled.
No bound and no research label changes before §6 holds and an AI model has been consulted for review (not a person; es-research §7).

## 1. Gates (all must hold before the first compile)

1. **FV302 accepted**: `fv302-20261124/PLAN.md` acceptance items 1-4 pass and are logged there (item 3 via
   `tools/axiom_audit.py` over every module log).
2. **s35_20 accepted** by the res-slices-fv §9 finish recipe with tag 3520: `RS.s35_20` and `RS.residual_bound_118_fv`
   print [propext, Classical.choice, Quot.sound] with `lean_rc=0`; `audit.py 3520` reports `"problems": []` apart
   from split axiom lines, which `axlines.py 3520 --reprint` settles (`"n_problems": 0`); every unit manifest has
   `min_margin` 1 and `lean_test_failures` 0; the leaf sum is **119,054,033** (corrected 25 Nov 16:35, see §7: the tree's 119,054,034 leaves minus the
   pending "state 0 missing" leaf that Lean discharges; s3520-gate README §2 and LAUNCH_PLAN l.165-166); the six-slice specialisation is snapshotted in `data/spec-snapshots/`.
3. Both drivers (`esr-fv2-drv`, `esr-fvr-drv`) have exited; no YIELD file; Tctl < 86 C; `cpu_free.sh esr` >= 1.

## 2. Source and statement

- `src/Combined/ES302Final.lean`, sha256 `950be9327271e9799b1233d17a176805c2a8d8f9b5adc0e2a293c13d75acfee1`:
  `Combined.es302_verdicts`, `Combined.es304_verdicts`, `Combined.residual_bound_118_verdicts`, each the `_s3519`
  form of part 2 applied to `E302ZZ.Final.excludes_69` (302 only) and `RS.s35_20`.
- Expected `#check` of the end theorem (6 explicit hypotheses, all cake_lpr verdict props):
  `Combined.es302_verdicts (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
  (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
  (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA) : ForcesConvexNGon 302 8`.
- Four `example`s pin the types mechanically: `excludes_69 : ExcludesHoleBudgetZZsN 16 69`,
  `forces_302_of_n54_res : N66Bound 54 → ResidualBound 118 → ForcesConvexNGon 302 8` (closes the 25 Nov review
  finding that FV302's acceptance checked axioms but not the elaborated statement), `RS.s35_20` with Res118's own
  arguments, and `es302_verdicts` as a plain implication.
- Three `#guard_msgs` axiom guards: exactly [propext, Classical.choice, Quot.sound].

## 3. LEAN_PATH

`tools/env2.sh` unchanged, plus two roots appended: `/home/jay/research/data/fv302-20261124/olean` (E302ZZ/*,
CompactChecker/FcatZZs16, BridgeZZs16) and `links3/` (file-level symlinks to res-slices-fv's `RS/Final3520`,
`RS/Bridge3520`, `RS/Cat3520*`, `RS3520/*` and the updated `RS/Res118FV` only if needed), built by a copy of
`tools/mklinks.py` for tag 3520 with the pins of `res-slices-fv/data/audit-3520.json`. The two-providers check over
the whole path must report no module file with two providers.

## 4. Control

`controls/Bad302.lean` (sha256 `2466006c9318b64261b99b5947ba56ff6fd1466e0aef365420271419c2124a03`) states
`ForcesConvexNGon 301 8` from the same proof term. It MUST fail with a type mismatch (compiled without `-o`).

## 5. Units and memory (HEURISTIC estimates marked)

- Units `esr-vfy-lcb3-<job>` (memguard track vfy, 20,000 MB), CPUQuota 100 %, MemorySwapMax 0, nice 10, one at a time,
  through `tools/unit_lean.sh` (anon+shmem sampler, SIGTERM at 80 % of MemoryMax).
- `ES302Final`: MemoryMax 12G (stop at 9,830 MB), RuntimeMaxSec 10800. HEURISTIC: anon+shmem 1-3 GB (FV304's Root and
  Final over 8,192 contexts used 429/451 MB; FV302 sub-roots 615-742 MB); wall 30-90 min (the axiom walks cover both
  trees' proof DAGs).
- `Bad302` control: MemoryMax 12G, RuntimeMaxSec 10800 (it imports the same closure).
- Import audit `audit3` (copy of `tools/audit2.py` with the two new roots and pins: FV302 olean sha256 recorded at
  FV302 acceptance, RS3520 oleans from `audit-3520.json`): MemoryMax 2G, O_DIRECT hashing.

## 6. Acceptance (all must hold)

1. `ES302Final` lean_rc 0; the three guards pass; the four `example`s elaborate; the `#check` lines equal §2.
2. `Bad302` fails with a type mismatch at `bad301` (and with nothing else).
3. `audit3` reports `"problems": []` (every closure module from exactly one root, every file hash equal to its pin).
4. The label then reads: **ES(8) ≤ 302, Lean-checked modulo the cake_lpr verdict propositions H-N66C (105), H-N66R
   (629) and H-ROWS (2,025), trust items E1-E6 (E3 tested, not proved)**. Stated in REMAINS.md and the records only
   after the AI model review (not a person). Known limits to state with it: the 105 N66 cube proofs were deleted on 24 Nov (two
   recorded acceptances; a re-run needs a re-solve); no external review.

## 7. Corrections (dated; the original text is in git, commit 7311d7e66)

- 25 Nov 2026 16:35 KST, before either driver ended: gate 2 first said the leaf sum is 119,054,034, the tree's
  leaf count (238,116,145 nodes). The Lean-side sum pre-registered for s35_20 is 119,054,033 = 119,054,034 minus
  the "state 0 missing" leaf (`zero_mem_residualOccupied`), as for s35_19 (7,763,207 tree leaves, Lean sum
  7,763,206). Found by the AI model review (not a person); no result was known when it was corrected.
- 25 Nov 2026 ~19:40 KST, before any part-3 compile: §5's estimate (anon+shmem 1-3 GB, MemoryMax 12G) is contradicted
  by the s35_20 Root: the flat `RS3520/Root.lean` (21,495 imports, 23,485 join theorems) held 7.0 GB anonymous for the
  s35_20 closure alone, reached 23.9 GB maximum RSS, and aborted twice with "Stack overflow detected" (lean_rc 134;
  logs/RS3520_Root.try2-20261125.log). Gate 2 cannot hold until the Root is rebuilt as sub-roots (res-slices-fv
  deviation of 25 Nov). New rule: the MemoryMax of `ES302Final`, `Bad302` and `Audit3` is set from the measured peak of
  the new s35_20 Root plus FV302 Final's 1,437 MB, with the 80 % stop level, and every compile that imports a whole
  closure runs alone. Part 3 is therefore not a result of 25 Nov.
- 26 Nov 2026 00:38 KST, before any part-3 compile: the 25 Nov 19:40 rule (MemoryMax from the measured peaks: 2,645 +
  1,437 + 533 = 4,615 MB, so 7G with the stop at 5,734 MB) is withdrawn for the compiles: with memguard's memory.high at
  the unit limit it would leave about 2.5 GB of page cache for a closure of about 245 GB of oleans. ES302Final, Bad302
  and Audit3 run at §5's first registration, MemoryMax 12G (stop at 9,830 MB), RuntimeMaxSec 21600 (§5 said 10800;
  page-cache bound). Unit logs are `logs/p3_<job>.out` (`links.out` and `audit3.out` belong to parts 1-2). Chain:
  `tools/run_part3c.sh` (unit esr-vfy-p3chain); its finish-recipe step re-ran axlines after RP3520 (lean_rc 0, 671 lines).
- 26 Nov 2026 01:26 KST, before any part-3 compile: the two-providers check (§3) failed in mklinks3.py on 23 module
  files (CompactChecker/*) that both the FV304 and the FV302 olean roots provide; all 23 resolve to the same physical
  file (both roots link the shared CompactChecker build; checked: 23 same real path, 0 different bytes). As FV302's
  fv2a item 4 decided on 25 Nov, roots that resolve to the same file count as one provider: mklinks3.py and audit3.py
  (closure modules and companions) now flag only providers that resolve to different files. The negative control
  (adding res118/olean, real copies) must still be refused. Chain resumed as `tools/run_part3d.sh` from §3.
  Negative control under that rule: adding res118/olean must still be refused; it is, through its real copies
  (BalancedBudgetsZ.olean, a regular file there), while its CompactChecker/* entries, links to the shared build, are no
  longer duplicates; the control now requires exactly that (BalancedBudgetsZ in, CompactChecker/Fast2 out).
- 26 Nov 2026 01:35 KST, before any part-3 compile had run: ES302Final stopped after 5 s with "object file
  .../fv304-20261120/olean/CompactChecker/FcatZZs16.olean ... does not exist": Lean resolves a module through the FIRST
  LEAN_PATH root that holds its package directory, and env3.sh had appended the FV302 root after the FV304 root (both
  have CompactChecker/) and links3 after links (both have RS/). env3.sh now inserts the FV302 root right before the
  FV304 root (its CompactChecker/ = the same 23 files + FcatZZs16, BridgeZZs16) and links3 right before links;
  mklinks3.py adds to links3/RS a link for every links/RS entry (same targets; pins from part 2's data/links.json), so
  each package resolves to a directory that holds all of its modules. Nothing else changed. Chain resumed from §3.
- 26 Nov 2026 10:34 KST, after ES302Final (lean_rc 0), Bad302 (failed as required: one error, the type mismatch
  `ForcesConvexNGon 302 8` / `301 8` at `bad301`, line 9) and Audit3 (lean_rc 0, the three STMT lines): audit3.py
  stopped after 1 s with an IndexError before checking anything (no data/audit3.json). Its default log list (Audit3,
  ES302Final) was carried over from audit2.py, whose two end modules each printed a module list; in part 3 only
  `src/Audit3.lean` prints one (§5: it imports Combined.ES302Final alone, so its list is that module's import closure
  plus the module itself), and ES302Final.lean prints only `=== CHECK`. audit3.py now gets `logs/Audit3.log` as its
  one argument (script unchanged). Chain resumed as `tools/run_part3f.sh` (unit esr-vfy-p3chain) with only that step,
  RuntimeMaxSec 10800 for the unit (3600 before; the closure is about 245 GB of oleans). run_part3e.sh's last step
  (restart the N66 re-solve driver) is dropped: the re-solve ended at 06:13 with 105/105 CERTIFIED and its driver has
  ended (n66-resolve-20261125/PLAN.md).
- 26 Nov 2026 (owner's wrap-up request), wording only: "advisor" was replaced by "AI model review (not a person)" in
  lines 5, 64 and 72; nothing else changed. `data/manifest4.sha256` pins the version accepted at 10:50 (git 54908d4ad).

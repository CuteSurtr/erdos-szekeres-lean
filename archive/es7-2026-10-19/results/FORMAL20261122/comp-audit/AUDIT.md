# AUDIT: one-build audit of the 30x composition Lean files (22 Nov 2026, 06:03-06:06 KST)

Work dir `/home/jay/research/data/formalize-20261122/comp-audit`, slot `lcmp`. Driver `comp_audit.py`, run 3,
2026-11-21T21:03:29Z to 2026-11-21T21:05:51Z (06:03:29 to 06:05:51 KST). Verdict in `result.json`: **audit passed**.

## 1. Verdict and labels

- **Passed.** The nine 30x files and Composition306 compiled in ONE fresh olean directory (`out/olean`) with the
  pinned v4.24.0 compiler. All 31 audited theorems print exactly `[propext, Classical.choice, Quot.sound]`; no
  other axiom appeared anywhere. The import closure of the audit file has 4,980 modules. Each has exactly one
  providing LEAN_PATH root and matches its pin: 4,883 against library.json, 87 against chain311 build.tsv, and
  10 against this build.
- **Labels.** Each theorem is **Lean-checked** as the implication it states (statements in section 8).
  - ES(8) <= 304 is **Lean-checked modulo** `ExcludesHoleBudgetZ 67`, `N66Bound 55` and `ResidualBound 118`
    (`composition_304_z`), and modulo `BalancedBound 184` and `ResidualBound 118` (`composition_304`).
  - The 303/302/301/300 statements are Lean-checked implications. Their balanced hypotheses have no complete
    evidence today: `ExcludesHoleBudgetZZsF 68` and `ExcludesHoleBudgetZF 68` are pending checks, the larger
    budgets and `ExcludesHoleBudgetZZsN 16 69` have no tree, and nothing supports `BalancedBound 183`. For
    `composition_302_n54` and `composition_301_n53`, `N66Bound 54` and `N66Bound 53` are also incomplete. This
    is per LEAN_STATUS sections 4.5-4.6 [R] and was not re-checked here. **No claim** for 303 or below.
  - This audit adds no evidence for any hypothesis and states no new bound.
- **Memory flag (details in section 6).** `time -v` max RSS was above 2,800 MiB in every unit (3,094-3,776 MiB).
  Under the rule pre-registered before any compile (cgroup memory.peak plus memory.events), every unit passed.
  The largest cgroup peak was 1,053 MiB and the largest sampled anon peak 909 MiB; there was no memory event.
  The orchestrator may overrule that reading of the 2,800 MB rule.

## 2. What it settles (findings of `/home/jay/research/data/ledger-20261122/lean/LEAN_STATUS.md`)

- **Finding 2.** `composition_303_zzsf` now has a Linux `#print axioms` line, with the standard axioms.
  `Composition303.lean` has a Linux compile record (rc 0, standard axioms).
- **Finding 3.** The nine files, plus Composition306, now have one build with a recorded import audit and pin
  checks, replacing compiles across three olean directories.
- **Earlier oleans reproduced.** The fresh oleans are byte-identical to the older copies:
  - LemmaZ = `zrow/leanz` (the ES305 section 7 value `ef249ba1...`);
  - FixedStatesZ, LemmaZStar and BalancedBudgetsZZs = `zrow/leanzs`;
  - BalancedBudgetsZ = `fv304-20261120/olean`.
  So the earlier multi-directory compiles produced the same oleans.
- **Finding 6, partly.** FV304 compiles against `fv304-20261120/olean/BalancedBudgetsZ.olean` and
  `zrow/leanz/olean/LemmaZ.olean`. That is from LEAN_STATUS sections 1 and 5 [R] and from FV304's
  `lean_path.txt`, which lists both directories. Checked here: both files equal this audited build byte for
  byte. FV304's own closing audit, after `E304Z.Final`, is still missing.

## 3. Tools, sources and pins

- **Compiler.** Lean 4.24.0 (commit 797c613eb9b6d4ec95db23e3e00af9ac6657f24b, Release),
  `/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean`, sha256 `8fadc3ed92cc9decb94c96ee9c0876e91e03a3a5e69138f32114f02789e2766c`.
  It is called by absolute path as `lean -j1 -R . -o <out>.olean.tmp <M>.lean` from the flat `src/` dir, and
  the output is renamed on rc 0.
- **Other tools.** Python 3.14.4 (driver run as `python3 -I -B`), systemd 259, kernel 7.0.0-43-generic,
  GNU time (`/usr/bin/time -v`).
- **Toolchain pins.** `lean-toolchain` sha256 `42779d67b81608af8a12aa4328d2ab47ca201925b3b2bd68369587b5340bb434` and `lake-manifest.json` sha256
  `bc21802066bdf7c94b0eb1e7bd3d3389ae0d416c2ed69c6e5dae03e74945c8e7` equal both `build/chain311/library.json` and `closure.json`.
- **Library and Mathlib.** All 4,952 `.olean` files pinned by library.json have their pinned
  sha256 (2.32 GiB). library.json was written 2026-11-06T00:11:21Z, digest `39bc40235acc18c3046a9fe2a68cf5f2560fc5c0b25ae96861ee4496645c44c0`.
  A second, separate script confirmed the result.
  - No lake `.olean` is newer than the freeze, 2026-11-04T14:46:00Z (count: 0).
- **chain311.** 196 of 196 `.olean` files have the sha256 of their
  last `build.tsv` row, and every last row is `ok`.
- **Roots.** The 11 roots of library.json, which equal `chain311/lake-lean-path.txt`.
  - Lake was **not** re-queried: no lake command was run in the repo, per the build discipline.
  - The `Cli` root does not exist; that package was never built. library.json pins 0 modules there, as when it
    was written.
- **LEAN_PATH.** The 11 roots, then `experiments/omission-compact-checker-2026-11-05/build/chain311/olean`,
  then this audit's `out/olean` (wiped at the start). `zrow/leanz`, `zrow/leanzs` and `fv304-20261120/olean`
  were **not** on it.
- **Two-roots check.** It covers `.olean`, `.olean.server` and `.olean.private` files, and found nothing before
  or after the compiles.
  - Negative control: with `zrow/leanz/olean` added, it refuses with
    `LemmaZ.olean: [comp-audit/out/olean, zrow/leanz/olean]`.
- **Sources.** The ten copies in `src/` (read-only) were checked as follows:
  - each equals its record sha256 and the blob at git HEAD `b01f0acd9`, read with `git show`;
  - HEAD was committed at 05:47:37 KST, before this audit;
  - all ten files are identical at `2d1cb6baa`;
  - each copy was re-hashed right before its compile.

| copy | record file | sha256 | pin |
|---|---|---|---|
| LemmaZ.lean | `ES305N20261119/LemmaZ.lean` | `e6b28efaa80cb2158180daf12dd4ce76cf2b86cc833ae9d79b1c08ffca005d65` | record = git HEAD |
| BalancedBudgetsZ.lean | `ES305N20261119/BalancedBudgetsZ.lean` | `3e0651a023a58df5a9a0fff4c7d0fc1c5859dfe40b67e9a4e17cdc313224ab1a` | record = git HEAD |
| FixedStatesZ.lean | `ES305N20261119/FixedStatesZ.lean` | `20945f03e3c2ea7623f8cebcfd92622a3b13cf49c01bb20c863d71d2a2818988` | record = git HEAD |
| LemmaZStar.lean | `ES303N20261120/LemmaZStar.lean` | `47bd1f5618ee515b4f9f5c398bd6239b1c650a16dc6aa1ae687b7dafd49fd61c` | record = git HEAD |
| BalancedBudgetsZZs.lean | `ES303N20261120/BalancedBudgetsZZs.lean` | `7684a1deb0297c7444b1719d0403d1e814ddbab3623ec5c13320294f03278a8e` | record = git HEAD |
| BalancedBudgetsZZsN.lean | `ES303N20261120/BalancedBudgetsZZsN.lean` | `4cfface86e87798e34e60c98228a757505f13ea491c763a2caa67b73b41203f7` | record = git HEAD |
| Composition305.lean | `ES305N20261119/Composition305.lean` | `d7d1b2c30d6986ab5104630054e663bb5639e0f67fb3fa03ab1ef5c82b05eeae` | record = git HEAD |
| Composition304.lean | `ES304N20261119/Composition304.lean` | `a58df4a713d6c37247f9930accbf46d7f9dd31db351bf463b21ff8150f34fe96` | record = git HEAD |
| Composition303.lean | `ES303N20261120/Composition303.lean` | `bbecd6cf67b12cfa377f7f252923a0b910e27f20ea10e4174d131d358cfe426e` | record = git HEAD |
| Composition306.lean | `ES306N20261119/Composition306.lean` | `c87f171a235e1009fd2e5e2a7faf26c3fcaf3daa2a9a72108e54bb4ea93ad23d` | no record hash; = git HEAD |

## 4. Compiles

| unit | wall | user s | time -v max RSS MiB | cgroup memory.peak MiB | anon peak MiB (0.2 s samples) | memory.events | Tctl at start (C) | .olean sha256 | older copy |
|---|---|---|---|---|---|---|---|---|---|
| LemmaZ | 0:09.49 | 8.1 | 3,767 | 1,053 | 909 | all 0 | 85.6 | `ef249ba167372ac31f995027299efa1eeddac251ff73e4ef093a990ab02c353c` | equal: leanz/olean |
| BalancedBudgetsZ | 0:04.45 | 3.88 | 3,164 | 327 | 238 | all 0 | 85.0 | `38d8f8aed92e5e2fefbd86bf46607f920eea28dc5b757a5a30e26734b0cbe71a` | equal: fv304-20261120/olean |
| FixedStatesZ | 0:08.76 | 8.04 | 3,592 | 767 | 683 | all 0 | 85.2 | `fdd1900d9118cab5b013f1957178c160fe938bdc6873000a62755ca33c6e390c` | equal: leanzs/olean |
| LemmaZStar | 0:09.55 | 8.09 | 3,776 | 1,050 | 909 | all 0 | 85.9 | `1a741fa05068b4c1f0e09465fe218df793d3e30bbb27e2b99a7ca9a32b555102` | equal: leanzs/olean |
| BalancedBudgetsZZs | 0:03.93 | 3.24 | 3,156 | 327 | 230 | all 0 | 85.5 | `c53030beac0b3238982b3b15fd4e11d5f0fa7e8486a870adb848d58e52f01791` | equal: leanzs/olean |
| BalancedBudgetsZZsN | 0:05.40 | 4.3 | 3,156 | 329 | 237 | all 0 | 84.5 | `b11c8bd8a0cd19b87e04b8e815bab75402116a77b9acf1bfb5d3eca7d55e4fef` | no older copy |
| Composition305 | 0:03.86 | 2.79 | 3,094 | 320 | 231 | all 0 | 84.8 | `94e5257e170ec2cde931402abfe2d618793834218df044d126398a4ad8f7b2f8` | no older copy |
| Composition304 | 0:03.69 | 2.77 | 3,101 | 316 | 226 | all 0 | 85.0 | `88029bb32ed86adf5801b7a06e3bf4626ac59c5a4008569af11224d81606f6ce` | no older copy |
| Composition303 | 0:03.88 | 3.24 | 3,101 | 313 | 226 | all 0 | 85.0 | `ae3961f3c767ae83744b9ee3dd9a144f3556a3b658e5bdd3eb825fe155017c20` | no older copy |
| Composition306 | 0:03.21 | 2.62 | 3,100 | 313 | 225 | all 0 | 84.6 | `1cc3daf27a8c670dfdb0bdcfd45623ab90eee5ae24b4ea085226e2e2934fd1e3` | no older copy |
| audit | 0:17.77 | 16.77 | 3,152 | 321 | 233 | all 0 | 84.4 | `3a3c815bb0943579aa5162df3322c7ab04334ac0adcbc05fb41864740d6ffd86` | no older copy |

- **Units.** One unit per compile, one at a time: `esr-ag-lcmp-<module>`, with CPUQuota=100%, MemoryMax=3500M,
  MemorySwapMax=0, RuntimeMaxSec=7200 and nice 10. Each was started with `systemd-run --user --wait --collect`.
- **Gates before each start.** No YIELD file, Tctl below 86 C, and ag-track and esr-total guard use each at least
  1,500 MB below budget. One wait happened: at 21:03:54Z (Tctl 86.6 C); the run resumed after 60 s.
- **Time.** 2 min 22 s wall for the whole run, including that 60 s wait and the pin checks (1.7 s); 63.8 s of user
  time over the 11 units.
- **Every unit.** lean_rc 0, `Exit status: 0`, no signal, and no error, sorry or warning message. Every
  `#print axioms` line in the ten files' own logs is standard (section 7b).

## 5. Import closure

- **`closure.tsv`** (sha256 `ea90547ab2d20e9e867b4ded2d4ed397908a08d0e43bf637ab01d87dc6416cf6`): the 4,980 modules of Audit.lean's
  `header.moduleNames`. Each row gives the module's one providing root, its `.olean` sha256 and its pin source,
  and every row is `ok`.
- **Count by root:** <repo>/.lake/packages/Cli/.lake/build/lib/lean 0, <repo>/.lake/packages/batteries/.lake/build/lib/lean 84, <repo>/.lake/packages/Qq/.lake/build/lib/lean 13, <repo>/.lake/packages/aesop/.lake/build/lib/lean 130, <repo>/.lake/packages/proofwidgets/.lake/build/lib/lean 12, <repo>/.lake/packages/importGraph/.lake/build/lib/lean 2, <repo>/.lake/packages/LeanSearchClient/.lake/build/lib/lean 4, <repo>/.lake/packages/plausible/.lake/build/lib/lean 9, <repo>/.lake/packages/mathlib/.lake/build/lib/lean 2825, <repo>/.lake/build/lib/lean 72, /home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/lib/lean 1732, <repo>/experiments/omission-compact-checker-2026-11-05/build/chain311/olean 87, /home/jay/research/data/formalize-20261122/comp-audit/out/olean 10.
- **The 87 chain311 modules:** BalancedRows, BalancedCoverCutsV2, BalancedProof.Catalog and Geometry00000 ...
  Geometry02656 (84 modules). This is the 87-module closure that LEAN_STATUS section 1 describes.
- **Core companions.** These are the `.olean.server` and `.olean.private` files of the toolchain's core modules,
  which library.json does not pin. There are 3,464 of them.
  - Digest `9b3b8546f02fcd8759d39caf99923d4d49b6b343505105d6f7641fe50ea3b6c4`: the sha256 of the lines `<module><.server|.private><TAB><sha256>`, in
    closure order.
  - Recorded only.
- **Independent re-check** (separate code: re-hash each row, compare with library.json, build.tsv and this
  build, require exactly one provider): 4,980 rows, 0 bad.

## 6. Memory

All memory figures are MiB (2^20 bytes): `/usr/bin/time` reports KiB, the cgroup files count bytes, and
systemd's `MemoryMax=3500M` is MiB, so the 2,800 limit is 2,800 MiB.

- **FLAG.** `time -v` max RSS was above 2,800 MiB (80 % of MemoryMax) in all 11 units: 3,094-3,776 MiB. The same
  compiles reported 3,087-3,709 MiB in the earlier records (`ES303N20261120/data/build_zsn.log`,
  `fv304-20261120/logs/lean/bbz.log`).
- **Pre-registered rule** (README, written before the first driver run at 06:02:06 KST): stop if a unit's cgroup
  memory.peak is at least 2,800 MiB, or if memory.events shows any high, max, oom or oom_kill event.
  - Result: cgroup peaks 313-1,053 MiB; every event counter 0; swap peak 0; sampled anon peaks 225-909 MiB.
  - The memory guard counts anon + shmem + swap; at no point did a unit come near its limit.
- **Why RSS is higher (HEURISTIC).** In every unit, RSS minus the anon peak is 2,858-2,926 MiB (2.79-2.86 GiB).
  That is about the
  size of the mapped olean closure: 2,367 MiB of `.olean` plus up to 922 MiB of core companions. This is
  consistent with the RSS being mostly file-backed mappings, which the guard does not count and the kernel can
  reclaim.
  - The pin hashing ran in the launcher, outside the units, so the oleans were already in page cache when the
    units started. The cgroup peaks therefore mostly exclude mapped olean pages. The anon figure does not depend
    on that.

## 7. Axioms, verbatim

### 7a. Audit.lean, 31 theorems (`axioms.txt`, sha256 `52e6c7cc6c90d8d14c49101c685dd10e5bc1f315864037c5cfcd67d8d189ee24`)

```
'OmissionBalancedZ.composition_304_z' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZ.composition_305_z' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZF.composition_304_zf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZF.composition_303_zf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsF.composition_303_zzsf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsF.composition_302_zzsf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsF.composition_301_zzsf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsF.composition_300_zzsf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsN.composition_302_n54' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsN.composition_301_n53' depends on axioms: [propext, Classical.choice, Quot.sound]
'composition_304' depends on axioms: [propext, Classical.choice, Quot.sound]
'composition_303' depends on axioms: [propext, Classical.choice, Quot.sound]
'composition_305' depends on axioms: [propext, Classical.choice, Quot.sound]
'composition_306' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionZRow.z_row' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionZStarRow.zs_row' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsN.z_row_of' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsN.zs_row_of' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZ.balanced_bound_of_hole_budget_z' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsF.balanced_bound_of_hole_budget_zzsf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsN.balanced_bound_of_hole_budget_zzsn' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionZRow.Z_eq' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionZStarRow.Zs_eq' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZ.feasible_holes_z' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZF.feasible_holes_zf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZF.balanced_bound_of_hole_budget_zf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsN.zzsn_55_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
'avoiding_302' depends on axioms: [propext, Classical.choice, Quot.sound]
'avoiding_303' depends on axioms: [propext, Classical.choice, Quot.sound]
'avoiding_304' depends on axioms: [propext, Classical.choice, Quot.sound]
'avoiding_305' depends on axioms: [propext, Classical.choice, Quot.sound]
```

### 7b. The files' own `#print axioms` lines (from `logs/<module>.log`)

```
-- LemmaZ.lean
'OmissionZRow.Z_eq' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionZRow.z_row' depends on axioms: [propext, Classical.choice, Quot.sound]
-- BalancedBudgetsZ.lean
'OmissionBalancedZ.feasible_holes_z' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZ.composition_305_z' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZ.composition_304_z' depends on axioms: [propext, Classical.choice, Quot.sound]
-- FixedStatesZ.lean
'OmissionBalancedZF.feasible_holes_zf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZF.composition_304_zf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZF.composition_303_zf' depends on axioms: [propext, Classical.choice, Quot.sound]
-- LemmaZStar.lean
'OmissionZStarRow.Zs_eq' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionZStarRow.zs_row' depends on axioms: [propext, Classical.choice, Quot.sound]
-- BalancedBudgetsZZs.lean
'OmissionBalancedZZsF.balanced_bound_of_hole_budget_zzsf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsF.composition_301_zzsf' depends on axioms: [propext, Classical.choice, Quot.sound]
-- BalancedBudgetsZZsN.lean
'OmissionBalancedZZsN.balanced_bound_of_hole_budget_zzsn' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsN.composition_302_n54' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsN.composition_301_n53' depends on axioms: [propext, Classical.choice, Quot.sound]
-- Composition305.lean
'composition_305' depends on axioms: [propext, Classical.choice, Quot.sound]
'avoiding_304' depends on axioms: [propext, Classical.choice, Quot.sound]
-- Composition304.lean
'composition_304' depends on axioms: [propext, Classical.choice, Quot.sound]
'avoiding_303' depends on axioms: [propext, Classical.choice, Quot.sound]
-- Composition303.lean
'composition_303' depends on axioms: [propext, Classical.choice, Quot.sound]
'avoiding_302' depends on axioms: [propext, Classical.choice, Quot.sound]
-- Composition306.lean
'composition_306' depends on axioms: [propext, Classical.choice, Quot.sound]
'avoiding_305' depends on axioms: [propext, Classical.choice, Quot.sound]
```

## 8. Statements as Lean printed them (`#check`; `checks.txt`, sha256 `a7c13359efb90f422ff687c984af6b65aaa6b317c4fa106d6b62818d11c45978`)

Lean wrapped long statements at its default width. `set_option format.width 1000` in Audit.lean had no visible
effect on the CLI messages, so the driver joins the indented continuation lines. `theorems.json` gives each
statement on one line, with its file and explicit hypotheses.

```
OmissionBalancedZ.composition_304_z (trees : OmissionBalancedZ.ExcludesHoleBudgetZ 67) (n66 : OmissionZRow.N66Bound 55)
  (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) : ErdosSzekeres.ForcesConvexNGon 304 8
OmissionBalancedZ.composition_305_z (trees : OmissionBalancedZ.ExcludesHoleBudgetZ 66) (n66 : OmissionZRow.N66Bound 55)
  (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) : ErdosSzekeres.ForcesConvexNGon 305 8
OmissionBalancedZF.composition_304_zf (trees : OmissionBalancedZF.ExcludesHoleBudgetZF 67)
  (n66 : OmissionZRow.N66Bound 55) (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) :
  ErdosSzekeres.ForcesConvexNGon 304 8
OmissionBalancedZF.composition_303_zf (trees : OmissionBalancedZF.ExcludesHoleBudgetZF 68)
  (n66 : OmissionZRow.N66Bound 55) (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) :
  ErdosSzekeres.ForcesConvexNGon 303 8
OmissionBalancedZZsF.composition_303_zzsf (trees : OmissionBalancedZZsF.ExcludesHoleBudgetZZsF 68)
  (n66 : OmissionZRow.N66Bound 55) (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) :
  ErdosSzekeres.ForcesConvexNGon 303 8
OmissionBalancedZZsF.composition_302_zzsf (trees : OmissionBalancedZZsF.ExcludesHoleBudgetZZsF 69)
  (n66 : OmissionZRow.N66Bound 55) (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) :
  ErdosSzekeres.ForcesConvexNGon 302 8
OmissionBalancedZZsF.composition_301_zzsf (trees : OmissionBalancedZZsF.ExcludesHoleBudgetZZsF 70)
  (n66 : OmissionZRow.N66Bound 55) (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) :
  ErdosSzekeres.ForcesConvexNGon 301 8
OmissionBalancedZZsF.composition_300_zzsf (trees : OmissionBalancedZZsF.ExcludesHoleBudgetZZsF 71)
  (n66 : OmissionZRow.N66Bound 55) (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) :
  ErdosSzekeres.ForcesConvexNGon 300 8
OmissionBalancedZZsN.composition_302_n54 (trees : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69)
  (n66 : OmissionZRow.N66Bound 54) (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) :
  ErdosSzekeres.ForcesConvexNGon 302 8
OmissionBalancedZZsN.composition_301_n53 (trees : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 17 70)
  (n66 : OmissionZRow.N66Bound 53) (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) :
  ErdosSzekeres.ForcesConvexNGon 301 8
composition_304 (hB : ErdosSzekeres.Omission.Partition.BalancedBound 184)
  (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) : ErdosSzekeres.ForcesConvexNGon 304 8
composition_303 (hB : ErdosSzekeres.Omission.Partition.BalancedBound 183)
  (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) : ErdosSzekeres.ForcesConvexNGon 303 8
composition_305 (hB : ErdosSzekeres.Omission.Partition.BalancedBound 185)
  (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) : ErdosSzekeres.ForcesConvexNGon 305 8
composition_306 (hB : ErdosSzekeres.Omission.Partition.BalancedBound 186)
  (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) : ErdosSzekeres.ForcesConvexNGon 306 8
OmissionZRow.z_row {n : ℕ} (n66 : OmissionZRow.N66Bound 55) (c : ErdosSzekeres.Omission.Configuration n)
  (noCap : ¬c.HasCap 7) (noCup : ¬c.HasCup 7)
  (noOctagon : ¬ErdosSzekeres.HasConvexNGon 8 (Finset.image c.point Finset.univ)) :
  15 ≤ (OmissionZRow.Z \ c.occupied noCap noCup).card
OmissionZStarRow.zs_row {n : ℕ} (n66 : OmissionZRow.N66Bound 55) (c : ErdosSzekeres.Omission.Configuration n)
  (noCap : ¬c.HasCap 7) (noCup : ¬c.HasCup 7)
  (noOctagon : ¬ErdosSzekeres.HasConvexNGon 8 (Finset.image c.point Finset.univ)) :
  15 ≤ (OmissionZStarRow.Zs \ c.occupied noCap noCup).card
OmissionBalancedZZsN.z_row_of {B n : ℕ} (n66 : OmissionZRow.N66Bound B) (c : ErdosSzekeres.Omission.Configuration n)
  (noCap : ¬c.HasCap 7) (noCup : ¬c.HasCup 7)
  (noOctagon : ¬ErdosSzekeres.HasConvexNGon 8 (Finset.image c.point Finset.univ)) :
  70 - B ≤ (OmissionZRow.Z \ c.occupied noCap noCup).card
OmissionBalancedZZsN.zs_row_of {B n : ℕ} (n66 : OmissionZRow.N66Bound B) (c : ErdosSzekeres.Omission.Configuration n)
  (noCap : ¬c.HasCap 7) (noCup : ¬c.HasCup 7)
  (noOctagon : ¬ErdosSzekeres.HasConvexNGon 8 (Finset.image c.point Finset.univ)) :
  70 - B ≤ (OmissionZStarRow.Zs \ c.occupied noCap noCup).card
OmissionBalancedZ.balanced_bound_of_hole_budget_z {budget : ℕ} (n66 : OmissionZRow.N66Bound 55)
  (verified : OmissionBalancedZ.ExcludesHoleBudgetZ budget) :
  ErdosSzekeres.Omission.Partition.BalancedBound (251 - budget)
OmissionBalancedZZsF.balanced_bound_of_hole_budget_zzsf {budget : ℕ} (small : budget ≤ 249)
  (n66 : OmissionZRow.N66Bound 55) (verified : OmissionBalancedZZsF.ExcludesHoleBudgetZZsF budget) :
  ErdosSzekeres.Omission.Partition.BalancedBound (251 - budget)
OmissionBalancedZZsN.balanced_bound_of_hole_budget_zzsn {B budget : ℕ} (small : budget ≤ 249)
  (n66 : OmissionZRow.N66Bound B) (verified : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN (70 - B) budget) :
  ErdosSzekeres.Omission.Partition.BalancedBound (251 - budget)
OmissionZRow.Z_eq (i : Fin 252) : i ∈ OmissionZRow.Z ↔ ↑i ∈ OmissionZRow.zIndices
OmissionZStarRow.Zs_eq (i : Fin 252) : i ∈ OmissionZStarRow.Zs ↔ ↑i ∈ OmissionZStarRow.zsIndices
OmissionBalancedZ.feasible_holes_z (n66 : OmissionZRow.N66Bound 55) {n : ℕ} (c : ErdosSzekeres.Omission.Configuration n)
  (noCap : ¬c.HasCap 7) (noCup : ¬c.HasCup 7)
  (noOctagon : ¬ErdosSzekeres.HasConvexNGon 8 (Finset.image c.point Finset.univ)) :
  ∃ holes,
    (∀ (i : Fin 252), holes i ≤ 1) ∧
      (∀ (r : Fin 2685), OmissionBalanced.demand r ≤ ∑ i ∈ OmissionBalanced.support r, holes i) ∧
        (∀ (r : Fin 446), BalancedCoverCutsV2.demand r ≤ ∑ i ∈ BalancedCoverCutsV2.support r, holes i) ∧
          15 ≤ ∑ i ∈ OmissionZRow.Z, holes i ∧ ∑ i, holes i + n = 252
OmissionBalancedZF.feasible_holes_zf (n66 : OmissionZRow.N66Bound 55) {n : ℕ}
  (c : ErdosSzekeres.Omission.Configuration n) (noCap : ¬c.HasCap 7) (noCup : ¬c.HasCup 7)
  (noOctagon : ¬ErdosSzekeres.HasConvexNGon 8 (Finset.image c.point Finset.univ)) (hn : 2 ≤ n) :
  ∃ holes,
    holes 0 = 0 ∧
      holes 1 = 0 ∧
        (∀ (i : Fin 252), holes i ≤ 1) ∧
          (∀ (r : Fin 2685), OmissionBalanced.demand r ≤ ∑ i ∈ OmissionBalanced.support r, holes i) ∧
            (∀ (r : Fin 446), BalancedCoverCutsV2.demand r ≤ ∑ i ∈ BalancedCoverCutsV2.support r, holes i) ∧
              15 ≤ ∑ i ∈ OmissionZRow.Z, holes i ∧ ∑ i, holes i + n = 252
OmissionBalancedZF.balanced_bound_of_hole_budget_zf {budget : ℕ} (small : budget ≤ 249) (n66 : OmissionZRow.N66Bound 55)
  (verified : OmissionBalancedZF.ExcludesHoleBudgetZF budget) :
  ErdosSzekeres.Omission.Partition.BalancedBound (251 - budget)
OmissionBalancedZZsN.zzsn_55_iff (b : ℕ) :
  OmissionBalancedZZsN.ExcludesHoleBudgetZZsN (70 - 55) b ↔ OmissionBalancedZZsF.ExcludesHoleBudgetZZsF b
avoiding_302 (hB : ErdosSzekeres.Omission.Partition.BalancedBound 183)
  (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) (S : Finset ErdosSzekeres.Point)
  (gp : ErdosSzekeres.GeneralPosition S) (avoid : ¬ErdosSzekeres.HasConvexNGon 8 S) : S.card ≤ 302
avoiding_303 (hB : ErdosSzekeres.Omission.Partition.BalancedBound 184)
  (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) (S : Finset ErdosSzekeres.Point)
  (gp : ErdosSzekeres.GeneralPosition S) (avoid : ¬ErdosSzekeres.HasConvexNGon 8 S) : S.card ≤ 303
avoiding_304 (hB : ErdosSzekeres.Omission.Partition.BalancedBound 185)
  (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) (S : Finset ErdosSzekeres.Point)
  (gp : ErdosSzekeres.GeneralPosition S) (avoid : ¬ErdosSzekeres.HasConvexNGon 8 S) : S.card ≤ 304
avoiding_305 (hB : ErdosSzekeres.Omission.Partition.BalancedBound 186)
  (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) (S : Finset ErdosSzekeres.Point)
  (gp : ErdosSzekeres.GeneralPosition S) (avoid : ¬ErdosSzekeres.HasConvexNGon 8 S) : S.card ≤ 305
```

## 9. Notes and deviations

- **Run 1 refused.** My missing-root test was stricter than `drive_es310.check_library`. It now refuses only
  when a missing root has pinned modules.
- **Run 2.** It compiled LemmaZ, with the same figures as run 3, then crashed on a JSON bug (axiom sets) before
  the second unit. Fixed.
- **Run 3** is the one recorded here. It wiped `src/`, `out/olean/` and `audit/`, and rebuilt everything.
- **No writes outside the work dir.** No lake command was run, and nothing was written into the repo or into
  any existing olean store.
  - Git was used read-only: `git show`, `git log`, `git rev-parse`, and, during orientation,
    `git ls-files --error-unmatch <file>` and `git diff --quiet HEAD -- <file>`.
  - `.git/index` was last modified at 05:47:37 KST, which is commit `b01f0acd9`'s time and before this session's
    first git command.
- **The memory-rule reading is mine.** It was reviewed by the advisor and pre-registered in the README before
  any compile.

## 10. Files

| file | sha256 |
|---|---|
| `comp_audit.py` | `2d8213f97b353d89fef3a396fa9c91daee50d545b00dea0e01d591db84bdb239` |
| `unit_compile.sh` | `cd6ba893114ba804cd4020e8f580dbd179cd567528c631d401864525afa9dad9` |
| `audit/Audit.lean` | `c2f27fa172955b1b8f7559249a0037b7a719454c8875cbfed0a6eb19deb2c0ee` |
| `closure.tsv` | `ea90547ab2d20e9e867b4ded2d4ed397908a08d0e43bf637ab01d87dc6416cf6` |
| `axioms.txt` | `52e6c7cc6c90d8d14c49101c685dd10e5bc1f315864037c5cfcd67d8d189ee24` |
| `checks.txt` | `a7c13359efb90f422ff687c984af6b65aaa6b317c4fa106d6b62818d11c45978` |
| `theorems.json` | `d7c0692c9514da15a7f85054301ede35c4fe202a4a951e3ccd384ee0ac4c5cf2` |

Fresh oleans (`out/olean`):

| file | sha256 |
|---|---|
| `out/olean/LemmaZ.olean` | `ef249ba167372ac31f995027299efa1eeddac251ff73e4ef093a990ab02c353c` |
| `out/olean/BalancedBudgetsZ.olean` | `38d8f8aed92e5e2fefbd86bf46607f920eea28dc5b757a5a30e26734b0cbe71a` |
| `out/olean/FixedStatesZ.olean` | `fdd1900d9118cab5b013f1957178c160fe938bdc6873000a62755ca33c6e390c` |
| `out/olean/LemmaZStar.olean` | `1a741fa05068b4c1f0e09465fe218df793d3e30bbb27e2b99a7ca9a32b555102` |
| `out/olean/BalancedBudgetsZZs.olean` | `c53030beac0b3238982b3b15fd4e11d5f0fa7e8486a870adb848d58e52f01791` |
| `out/olean/BalancedBudgetsZZsN.olean` | `b11c8bd8a0cd19b87e04b8e815bab75402116a77b9acf1bfb5d3eca7d55e4fef` |
| `out/olean/Composition305.olean` | `94e5257e170ec2cde931402abfe2d618793834218df044d126398a4ad8f7b2f8` |
| `out/olean/Composition304.olean` | `88029bb32ed86adf5801b7a06e3bf4626ac59c5a4008569af11224d81606f6ce` |
| `out/olean/Composition303.olean` | `ae3961f3c767ae83744b9ee3dd9a144f3556a3b658e5bdd3eb825fe155017c20` |
| `out/olean/Composition306.olean` | `1cc3daf27a8c670dfdb0bdcfd45623ab90eee5ae24b4ea085226e2e2934fd1e3` |

Also here: `result.json` (all checks and figures), `driver.log`, `logs/*.log` (each unit's Lean output,
`time -v` report and cgroup figures), `src/` (the ten read-only copies), `README.md`.

## 11. Re-run

```
cd /home/jay/research/data/formalize-20261122/comp-audit && python3 -I -B comp_audit.py
```

This takes about 2.5 min. It wipes `src/`, `out/olean/` and `audit/`, and rewrites `result.json`,
`closure.tsv`, `axioms.txt`, `checks.txt` and `logs/`. It refuses or stops on any failed check.

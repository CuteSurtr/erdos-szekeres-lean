# s3520-gate: launch gate for the last Res118 slice, s35_20 (22 Nov 2026)

## 1. Headline (status; updated after every milestone)

- **22:47 KST: GATE PASSED (with the axiom-line caveat below); all milestones M0–M8 done. The campaign is NOT
  launched** (`LAUNCH_PLAN.md`).
- **What Lean checked here** (lean v4.24.0, bare `lean -j1`, read-only LEAN_PATH, the campaign's catalog `RS.Cat3520`
  and checker): all **57 chunk modules of ctx-4274** (unit 2080, the largest context, 320,422 leaves) and the
  context-level theorem
  `RS3520.U2080.root : ¬ ∃ holes : Fin 154 → ℕ, FFeas fcatS3520 4642 154 35 (pmask (zerosF 154) [(109, 2), (75, 2),
  (133, 1), (33, 2), (25, 2), (17, 2), (20, 1), (56, 1), (45, 2), (36, 2), (54, 2), (98, 2), (44, 1), (0, 2)]) holes`
  with axioms `[propext, Classical.choice, Quot.sound]` (`logs/RS3520_U2080.log`, lean_rc 0); plus the 11 chunk
  modules of units 161 and 1793. That is 3 of the 3,212 units (387,322 of 119,054,033 leaves). **Nothing about
  `s35_20` as a whole is claimed**; `RS.s35_20` does not exist yet.
- Gate results:
  - pre-pass (streamed, all 8,080 contexts) equal to the independent T7 record for every context (gz sha256, leaves,
    nodes); `total_leaves` **119,054,033** = the pre-registered count (COMPUTED);
  - the lean exporter v3 is **byte-identical** to the reference on 3318 and on two real 3520 units (56 MB of source);
  - ctx-4274 exported at **705 MB** anon + shmem in a fresh one-unit process (the reference would need about
    5.4 GB), and at 1,189 MB as the last of 21 units in one process (identical output); drive v3 therefore restarts
    the exporter hourly with MemoryMax 3000M;
  - axiom lines: 73 of the 75 `#print axioms` lines of the 68 modules are whole and standard in their own logs; 2
    (C208014, C208053) were split by profiler output, so **pre-registered acceptance item 3 was not met literally** for
    them; both were re-printed from their oleans (`logs/RP3520.log`): standard, lean_rc 0;
  - negative control: the corrupted chunk is **rejected** by Lean;
  - calibration (HEURISTIC): 0.0116–0.0126 s per leaf, 821 + 1,108 B per leaf, compile peak ≤ 748 MB; campaign
    383–417 CPU-h (370–470 at the per-module extremes), 5.3–5.8 days at 3 compiles, 2.7–2.9 at 6, 1.3–1.4 at 12;
    228–239 GB of disk with sources kept.
- Item `s35_20-gate` of the Lean wave (owner: "lean verify everything"). Label of the unit theorem: Lean-checked
  (standard axioms, no hypotheses); trust items as res-slices-fv §3 (imported oleans pinned, not re-checked).
- 21:16 KST: plan and pre-registration written (§2, §3) before any 3520 command (README sha256 at that time in
  `data/prereg-readme.sha256`).
- Item `s35_20-gate` of the Lean wave (owner: "lean verify everything"). This is a **gate**, not the campaign: the
  campaign (about 119 M leaves) is **not** launched here. Track `s20`, slot `g`, units `esr-s20-g-<job>`.
- Work directory (the only place written): `/home/jay/research/data/formalize-20261122/s3520-gate`.
  `res-slices-fv` (driver `esr-fvr-drv` running s35_19) is read-only for this item.

## 2. Plan (milestones)

| # | milestone | state |
|---|---|---|
| M0 | README with plan and the s35_20 pre-registration (§3) | done 21:16 |
| M1 | patched tools as new files in `tools/` with diffs in `diffs/`: `slice_export_v3.py` (context-id fix, streamed pre-pass, streamed compact context loader, lean unit export writing each module as it is built), `slice_export_w13fix.py` (reference: `slice_export_w13.py` + the id fix only), `compile.sh` (own `D`), `drive_v3.py` | done 21:30 (§5) |
| M2 | byte-identity controls: v3 vs reference on 3318 unit 0 and on one small real 3520 unit (module sha256 and manifest stats); tool hashes frozen afterwards | **byte-identical**: 3318 (21:29), 3520 units 1793 and 161 (21:41); hashes frozen 21:41:55 (`data/tools-frozen.sha256`) |
| M3 | streamed pre-pass of s35_20 (all 8,080 contexts): acceptance in §3 | **accepted** 21:39 (§4) |
| M4 | memory ladder: export a 40,000–60,000-leaf context, extrapolate, then export ctx-4274 (largest, 320,422 leaves) under MemoryMax ≤ 6G; anon + shmem sampled from the unit's own memory.stat | done 21:43: 166 MB at 47,865 leaves, **705 MB** at 320,422 (§4) |
| M5 | compile every chunk module of the ctx-4274 unit (one or two at a time, gated loop units), same checker, catalog and parameters as the campaign (unit 40,000, chunk 8,000, block 64, 16 entries per word, profiler on) | **done** 22:24: 57/57 lean_rc 0 (plus units 1793 and 161: 11/11) |
| M6 | context-level sub-root theorem for the ctx-4274 unit; axiom lines checked with `res-slices-fv/tools/axlines.py` (unmodified, through a view directory) | **done** 22:25 / 22:33: `RS3520.U2080.root` standard; axlines: only the expected Root/Final problems |
| M7 | negative control: one corrupted chunk (separate `--out` and olean dir) rejected by Lean | **rejected** 21:48 (§6) |
| M8 | `LAUNCH_PLAN.md`: re-calibrated cost (HEURISTIC), wall time at 3/6/12 compiles, disk, swap-in commands for drive v3, pre-launch checks | **done** 22:40 |

## 3. PRE-REGISTRATION of s35_20 (tag 3520), written 21:16 KST before any 3520 file was generated

- **Lean statement**, Res118's hypothesis copied verbatim from
  `/home/jay/research/data/formalize-20261122/res118/lean/Res118/Final.lean` (sha256
  `7f9198b7660c2ff6329fe5ac3a640b1efa0e09d68f60b65c263cb3cc2713d83b`, namespace `Res118`):
  `(s35_20 : ResSliceExcludes (rowsP ++ rowsQ ++ rowsA) 35 20)`.
  The campaign's theorem will be
  `theorem s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20`, proved as
  `Res118.slice_of_root RS.cat3520_ok`, then
  `rw [List.length_append, List.length_append, Res118.rows_lengths.1, Res118.rows_lengths.2.1, Res118.rows_lengths.2.2.2]`
  (copied from `res-slices-fv/lean/RS/FinalTest3520.lean`, which compiled with lean_rc 0 at 20:07), then
  `exact RS3520.root`, where
  `RS3520.root : ¬ ∃ holes : Fin 154 → ℕ, FFeas fcatS3520 4642 154 35 (pmask (zerosF 154) [(0, 2)]) holes`.
  The Res118 specialisation then takes `RS.s35_20` as its argument `s35_20` (Lean checks the match).
- **Tree** (read-only): `/home/jay/research/data/es308-20261114/runs/b35s20/bb-s1`, `master.json` sha256
  `71993a47f134ff06afa1d0029f39b7f6feceaf23bfee17b945e32329498e9dea` (hashed 21:16; equals the T7 fresh replay
  summary `LO33N20261113/budget34/audit/fresh-b35s20-v169-bbs1/summary.json` and res118 README); budget 35, root 0,
  16,347 master nodes (8,173 branch, 8,080 context placeholders, 94 weighted leaves), `contexts: 8080`; context ids
  0..8080 with **4782 absent** (read 21:16).
- **Expected leaf count: 119,054,033** = T7's 119,054,034 (fresh_replay_v3) minus the pending "state 0 missing" leaf,
  which the mask `[(0, 2)]` excludes; it equals the T5/T6 count (tcheck_b35 + pycheck_b35, ES307 README T6:
  238,116,145 nodes, 119,054,033 leaves, minimum margin 1). The exporter's `skeleton.json` `total_leaves` must equal it.
- **Rows**: `/home/jay/research/data/es308-20261114/inputs/b35s20-v169/extra.json` sha256
  `de4bcceba6d0c80ce6f63cbef15822cac8300780607c738569999a7d94b81916`: 1,992 rows, row 0 = (F, 20), row 1 = (Lo, 15),
  1,990 unit rows of demand 1. Catalog rows m = 2,650 + 1,992 = 4,642 (13 bits: the w13 exporter, J = K << 13).
- **Catalog and bridge** (built by res-slices-fv at 20:06–20:08; used read-only): `RS.Cat3520` chain
  `Cat3520_p0..p5`, `Cat3520` (olean sha256 `f7904232…`, `53624fc2…`, `1e4d334e…`, `d5b3ddc3…`, `5ce3953c…`,
  `c66baffd…`, `247855f5…`), `RS.Bridge3520` olean `11dfffa7d302b60e32700d9c1a6eb5492d9499a9c82bb6f247a0704a3da93193`
  (= res-slices-fv README §7), `RS.cat3520_ok : Res118.SliceCatalog fcatS3520 (rowsP ++ rowsQ ++ rowsA) 35 20`.
- **Gate unit**: context 4274, the largest (T7 `contexts.jsonl`: 640,843 nodes, 320,422 leaves, minimum margin 1,
  max used row 4520). A placeholder is never split, so it is one unit by itself, and its unit-top theorem is the
  context-level theorem
  `¬ ∃ holes : Fin 154 → ℕ, FFeas fcatS3520 4642 154 35 (pmask (zerosF 154) P) holes`, with P = the context's master
  path (innermost first) followed by `(0, 2)`.
- **Gate acceptance** (all required; not accepted on any Python output alone):
  1. pre-pass: 8,080 contexts, id 4782 absent; leaves = branches + 1 in every context; every context's leaf count
     (and gz sha256, if the T7 field is the gz hash) equals T7 `contexts.jsonl`; `total_leaves` = 119,054,033;
  2. export of the ctx-4274 unit: manifest leaves 320,422, minimum margin ≥ 1, 0 leaf-test failures, exporter anon
     peak well under 4 GB;
  3. every chunk module of the unit: log ends `lean_rc=0` and has a whole line
     `'<module>.ex<s>' depends on axioms: [propext, Classical.choice, Quot.sound]` for each subtree root (axlines);
  4. the sub-root theorem compiles with lean_rc 0 and the standard axiom line;
  5. the corrupted chunk is rejected ("decide proved that the proposition … is false"), rc ≠ 0, no olean.

## 4. Progress log (KST)

- 21:16 orientation; master read (ids, 4782 gap); memory guard `esr-memguard-1122f` active with track `s20=8000`.
- 21:29 M2a: control `controls/ctl3318.sh` in unit `esr-s20-g-ctl3318`: slice 3318 (110 contexts, 1,907 leaves) exported
  by the reference and by v3 with the driver's parameters: `cmp_export.py` **identical** (skeleton, pre-pass digest,
  manifest without tool hashes/seconds, the chunk source 1,871,340 bytes); the v3 chunk is also byte-identical to
  res-slices-fv's w13 control chunk `controls/w13/3318-C/src/RS3318/C000001.lean` (made by slice_export_w13.py 20:01).
- 21:31 M3 started: unit `esr-s20-g-pre3520` (MemoryMax 1500M, RuntimeMaxSec 7200), `slice_export_v3.py 3520 ...
  --unit-leaves 40000 --chunk-leaves 8000 --prepass-only` (tool hashes at start in `data/tools-at-prepass.sha256`).
  500 contexts after 62.5 s, anon 72 MB.

- 21:38:59 M3 done: 453.5 s wall (404 s user), anon + shmem peak 155 MB (RSS 161 MB; the cgroup peak of 1,501 MB is page
  cache held at the 1500M brake). `logs/pre3520.out`: 8,080 contexts, `total_leaves` **119,054,033**, 3,212 units.
  `tools/check_prepass.py` (`logs/check_prepass.out`): **ok, 0 problems**: ids 0..8080 without 4782; for every
  context gz sha256, leaves and nodes (leaves + branches) equal T7 `contexts.jsonl`, and leaves = branches + 1;
  context leaves 119,053,939 + 94 master leaves = 119,054,033; contexts digest `b3fd865d…`; master and extra hashes as
  pre-registered. Unit sizes: median 30,982 leaves; 863 units above 40,000 (single contexts) hold 59,237,580 leaves;
  ctx-4274 is unit **2080** (master node 12473, a context placeholder).
- 21:41 M2b: `controls/ctl3520.sh 1793 161` in unit `esr-s20-g-ctl3520`: unit 1793 (19,035 leaves: 7 contexts + 1
  master leaf, 3 modules) and unit 161 (ctx-169, 47,865 leaves, 8 modules), exported by the reference (into
  `controls/ref3520`, reusing the v3 pre-pass) and by v3 (into the gate export `export/3520`): `cmp_export.py`
  **identical** (11 modules, 56,324,233 bytes; manifests equal without tool hashes/seconds). Memory (anon + shmem
  peak, sampled) and time: unit 1793 reference 398 MB / 6.2 s, v3 103 MB / 6.7 s; unit 161 reference **903 MB** /
  16.5 s, v3 **166 MB** / 15.6 s. Linear projection to 320,422 leaves: v3 about 710 MB, reference about 5.4 GB.
- 21:41:55 tool hashes frozen (`data/tools-frozen-2141.sha256`; v3 unchanged since the pre-pass). The final list
  `data/tools-frozen.sha256` (22:38) has the same exporter hashes; `drive_v3.py` changed after the freeze (the join_*
  keys, 21:58) and both of its tests were re-run on the final file.
- 21:43 M4: unit `esr-s20-g-exp4274` (MemoryMax 3000M): `slice_export_v3.py ... --units 2080:2081`: unit 2080 =
  ctx-4274: **57 modules, 320,422 leaves**, 640,843 nodes, minimum margin 1, 0 leaf-test failures, K = 2^24 (max
  weight 10,000,000), J = 2^37, 21,083,566 entries (65.8 per leaf), 261,586,357 bytes of source (816 B per leaf);
  100.8 s (0.000315 s per leaf); anon + shmem peak **705 MB** (maxrss 719 MB, cgroup peak 1,028 MB). So the driver's
  exporter MemoryMax 2000M suffices for the largest context (705 < 1,600 = 80 %).
- 21:44 first 3520 chunk compile (unit 1793's C179301, 7,401 leaves): lean_rc 0, axiom line standard, 85.5 s CPU
  (0.0116 s per leaf), anon + shmem peak 654 MB (RSS 3.68 GB, mostly mapped oleans), 872 B source + 1,168 B olean per
  leaf.
- 21:43 M5 started: loop unit `esr-s20-g-c2080a` (modules 1, 3, 5, … of unit 2080); `esr-s20-g-c2080b` (2, 4, …) from
  21:49, after the negative control (M7, §6).
- 22:24:47 M5 done: **57 of 57 modules of unit 2080 lean_rc 0** (`logs/loop_c2080{a,b}.out`, `logs/RS3520_C2080*.log`);
  4,037.9 s CPU, 0.0126 s per leaf (per module 0.0112–0.0142), anon + shmem peaks 425–748 MB, RSS ≤ 3.76 GB.
- 22:19–22:29 unit 161 (8 modules, loop `esr-s20-g-c0161`): 8 of 8 lean_rc 0, 0.0125 s per leaf (third calibration
  point; unit 1793: 0.0116). All 68: `logs/calib_gate.out`, derived numbers `logs/plan_numbers.out` (HEURISTIC).
- 22:25 M6: `tools/subroot.py export/3520 2080` wrote `RS3520.U2080` (57 imports, 61 `split_pm` joins through the
  unit's skeleton, root_slice's unit_root logic; shape check kind "root" passed; stated path = `skeleton.json`
  `tops[2080].path` = the manifest's base path). Unit `esr-s20-g-rootmem`: lean_rc 0 in 5.7 s, the whole line
  `'RS3520.U2080.root' depends on axioms: [propext, Classical.choice, Quot.sound]`, anon + shmem 272 MB.
- 22:28 import-memory measurements (`controls/rootmem/`, units `esr-s20-g-rootmem`, `-rootmem2`): baseline
  (RS.Cat3520 + CompactChecker.Path) 229, 213, 227 MB; the 57 modules of unit 2080 imported, nothing else: 236, 233
  MB; 387 chunk modules (320 finished RS3519 oleans of res-slices-fv, read-only, and 67 gate modules; 2.43 GB of
  oleans) 255 MB. Used in LAUNCH_PLAN §3 with FV304's Root (429 MB, 25 GB of chunk oleans).
- 22:30–22:33 axiom lines: `tools/axlines_view.py axview export/3520 3520 2080 161 1793` runs the unmodified
  `res-slices-fv/tools/axlines.py` (sha256 `193253216b76…`) on a view directory. First run: 75 lines expected, 73
  whole, 2 missing: `C208014 ex148045` and `C208053 ex584381`, whose lines the profiler split
  (`…[propext, Classical.choice.olean serialization took 135ms` / `, Quot.sound]`; axlines files them under "missing",
  not "split_logs", because the split falls inside the standard text). `--reprint` wrote `axview/reprint/RP3520.lean`;
  compiled in unit `esr-s20-g-rp3520`: both `[propext, Classical.choice, Quot.sound]`, lean_rc 0 (`logs/RP3520.log`).
  Second run (`logs/axlines_view.out`): 73 ok + **2 re-printed, 0 missing**; the only problems are the two expected
  ones, `Root: …RS3520.root` and `Final: …RS.s35_20` (the gate has neither).
- 22:38 final hashes (`data/tools-frozen.sha256`, `data/gate-files.sha256`), diffs regenerated, `LAUNCH_PLAN.md`
  written.
- 22:38–22:46 after the advisor's final review:
  - sandbox scenario E (`tools/test_drive_v3_sandbox.py`): with the plan's environment the driver launches the
    exporter plus exactly 3 chunk compiles, estimates 450 + leaves // 20 (800 MB at 7,000 leaves in `driver.log`),
    `compile.sh` arguments as v2; all 5 scenarios OK (`logs/test_drive_v3_sandbox.out`);
  - `--stop-after` control (`controls/ctl_stopafter.sh`, unit `esr-s20-g-stopafter`): 3318 with `--stop-after 0`
    printed `stopped_before_unit: 0`, exit 0, no manifest and no source; the rerun gave the chunk of `controls/v3-3318`
    byte for byte;
  - 21 units in one exporter process (unit `esr-s20-g-multi`, units 2060–2080, 1,075,337 leaves, 5:42): maxrss 124 →
    618 MB over the first 20 units, then **1,189 MB anon + shmem** at ctx-4274 (705 MB fresh); every unit minimum
    margin 1; unit 2080's manifest and module hashes equal the gate export (`logs/multi3520.*`;
    `scratch/multi3520/src` deleted afterwards, 0.9 GB in this directory; manifests kept). Consequence: drive v3's
    exporter defaults changed to an hourly restart (`FVR_EXPSTOP=3600`, `FVR_EXPRT=7200`) and MemoryMax 3000M
    (`FVR_EXPMEM`, `FVR_EXPEST=1500`); both driver tests re-run OK.

## 5. Tools (M1; all new files in `tools/`, diffs in `diffs/`)

| file | what | diff |
|---|---|---|
| `slice_export_v3.py` | the exporter for s35_20: context-id fix (sorted placeholder ids), streamed pre-pass (header parsed from the text before `"nodes"`, leaves/branches counted as `"type":"weighted"`/`"over_budget"`/`"branch"`, every `"type":` one of the three, leaves = branches + 1, text ends `]}`), contexts read node by node (JSON scanner on a sliding window of the inflated text) into flat arrays, unit grafted into a `CUnit`, each module written (hidden `.tmp` name) as soon as it passes its checks, renamed after the unit's last check, manifest LAST; `--stop-after S` (no new unit after S seconds), `--prepass-only` | `diffs/slice_export_w13fix_to_v3.diff` |
| `export_es310_w13l.py` | `export_es310_w13.py` (05c41a58…) + `CUnit` + `export_compact` (export_context on flat arrays: the same texts, checks and refusals; per-leaf data in typed arrays, raw weights dropped after the leaf replay, one module text at a time) | `diffs/export_es310_w13_to_w13l.diff` (additions only) |
| `slice_export_w13fix.py` | reference for the byte-identity controls: `slice_export_w13.py` + the id fix only (3 code lines) | `diffs/slice_export_w13_to_w13fix.diff` |
| `export_es310_w13.py`, `slice_export_w13.py`, `drive.py` | unchanged copies (05c41a58…, 35b059de…, 6259c258…) for the reference and the diffs | – |
| `drive_v3.py` | drive.py v2 + the 3520 SLICES entry + per-slice exporter keys (`exporter`, `exp_args`, `exp_rt`, `exp_tries`, `exp_mem`, `exp_est`; for 3520 from env `FVR_EXPSTOP` (3,600 s), `FVR_EXPRT` (7,200 s), `FVR_EXPMEM` (3000), `FVR_EXPEST` (1500)) + per-slice `join_mem`/`join_est`/`join_rt` for the units that import a slice's whole chunk closure (its Root and Final, and the specialisation once it is done; env `FVR_JOINMEM`, `FVR_JOINEST`, `FVR_JOINRT`) + `start()` with MemoryMax/RuntimeMaxSec + `FVR_CEST` (compile estimate a + leaves // b) + a manifest cache + `-I -B` | `diffs/drive_v2_to_v3.diff`. Tests: `tools/test_drive_v3.py` (import only: the v2 slices unchanged, the 3520 entry, the Final text against the compiled `FinalTest3520.lean`, the six-slice specialisation text; `logs/test_drive_v3.out` OK) and `tools/test_drive_v3_sandbox.py` (main() on a fake res-slices-fv tree under `scratch/drvtest` with start/tctl/threads faked and the loop stopped after one pass; scenarios: exporter launch with v3, `--stop-after 3600`, 3000M/7,200 s; Root, Final and specialisation launches with the join resources; E: the plan's environment gives the exporter plus exactly 3 chunk compiles with estimate 450 + leaves // 20; `logs/test_drive_v3_sandbox.out` OK). Never run live: launching is the campaign. |
| `compile.sh` | res-slices-fv's compile.sh with this directory's `olean/` added LAST to LEAN_PATH and writes only under this directory | `diffs/compile_sh.diff` |
| `compile_loop.sh`, `gate_start.sh`, `sampled.sh` | gated compile loop (YIELD and Tctl checked before each module), gated unit start (YIELD, Tctl < 86, cpu_free ≥ 1, ≤ 2 s20 units, track anon + estimate ≤ 6,800 MB), in-unit anon + shmem sampler (0.5 s) | – |
| `subroot.py`, `axlines_view.py`, `cmp_export.py`, `check_prepass.py` | unit sub-root module (`RS3520.U<uuuu>.root`; root_slice's unit_root), unmodified axlines.py through a view directory, byte-identity check, pre-pass vs T7 | – |

## 6. Controls

- 3318 byte identity (21:29) and 3520 units 1793 and 161 (21:41): see §4.
- **Negative control** (21:48, unit `esr-s20-g-neg2080`, `controls/neg2080.sh`): unit 2080 re-exported by v3 with
  `--corrupt 2080:21` into the separate directory `controls/neg2080` (the exporter changed row 20's weight 2266 → 2265
  in leaf 231893, the module's minimum-margin leaf: exact margin 1 → 0, and its own leaf test failed on that leaf
  only); modules 01, 20 and 22 stayed byte-identical to the gate export. Only the corrupted `C208021` was compiled,
  into `controls/olean-neg`: **rejected** (lean_rc 1, one error, `C208021.lean:14:367: error: Tactic `decide` proved
  that the proposition … is false` at `chk231858`, the block holding leaf 231893), no olean written.
- Unit 1793 (21:43–21:46, loop `esr-s20-g-c1793`): all 3 modules lean_rc 0 with standard axiom lines (the second
  calibration point).
- Unit 161 (22:19–22:29): 8 of 8 lean_rc 0.

## 7. Files and hashes

- `README.md` (this file), `LAUNCH_PLAN.md`; `data/prereg-readme.sha256` (the README at pre-registration, 21:16:56,
  `1aaae17c…`).
- Tools: `tools/` (hashes in `data/tools-frozen.sha256`; the three files to swap in: `slice_export_v3.py`
  `4b5c5092…`, `export_es310_w13l.py` `9bff505e…`, `drive_v3.py` as listed there); diffs in `diffs/`.
- Gate export `export/3520/`: `prepass.json` `669bb305…`, `skeleton.json` `28f0146c…` (8,080 contexts, digest
  `b3fd865d…`, 3,212 units), manifests `ctx/ctx-{0161,1793,2080}.json`, sources `src/RS3520/C{0161,1793,2080}*.lean`
  and the sub-root `U2080.lean`; oleans `olean/RS3520/` (68 chunks + `U2080.olean` `7bf5abff…`). All hashed in
  `data/gate-files.sha256` (144 files, including the corrupted `controls/neg2080/src/RS3520/C208021.lean`).
- Logs: `logs/RS3520_<stem>.{log,mem}` per module, `logs/loop_*.out`, `logs/pre3520.*`, `logs/exp4274.*`,
  `logs/check_prepass.out`, `logs/calib_gate.out`, `logs/plan_numbers.out`, `logs/axlines_view.out`, `logs/RP3520.log`,
  `logs/test_drive_v3*.out`.
- Controls: `controls/ctl3318.*`, `controls/ctl3520.*` (+ `ref3318/`, `v3-3318/`, `ref3520/`), `controls/neg2080*`,
  `controls/rootmem/`.
- Inputs (read-only, hashes in §3): master `71993a47…`, extra `de4bcceb…`, the 8,080 context gz files (sha256 = T7
  `contexts.jsonl`), source-2650 raw `e800d5f8…` (asserted by the exporter), catalog/bridge oleans of res-slices-fv.
- Size: about 1.1 GB (chunk sources 318 MB, oleans 430 MB, reference export and controls the rest).

## 8. What remains

- **The campaign** (not launched): `LAUNCH_PLAN.md` (swap in drive v3 after s35_19; owner decisions for N > 3,
  join memory if the s35_19 Root says so, and deleting sources).
- The join units' memory (Root, Final, specialisation) is projected, not measured at scale (1.3–2.1 GB, HEURISTIC);
  the s35_19 Root measurement is the check (LAUNCH_PLAN §3).
- Not re-checked here: the imported oleans against their sources (res-slices-fv §3 trust items, pins only). The gate's
  chunk oleans were built with this directory's `olean/` appended LAST to LEAN_PATH; chunk modules import only
  `RS.Cat3520` and `CompactChecker.Path`, both from res-slices-fv's store.
- Disclosures:
  - The two compile loops `esr-s20-g-c2080a` and `-c2080b` ran at the same time (21:49–22:17) with no exporter
    running. I read the track line "up to 2 units at a time (exporter 1 + compile 1)" together with step (3) "units one
    or two at a time"; if only one compile unit was meant, this was a second compile unit beyond it.
  - At orientation (21:10–21:15) I read res-slices-fv's live `status.json` and `tries.json` once (read-only); not
    `run.tsv` or `export/3519`.
  - The pre-registration hash in `data/prereg-readme.sha256` has no snapshot copy of the README of 21:16:56, so it
    cannot be re-verified now; I did not edit §3 after it (my later edits touched §1, §2 and §4 onwards).
  - The gate checks (YIELD, Tctl, free thread, track room) ran at each unit start and before each module inside the
    compile loops; the memory guard covered every `esr-s20-*` unit. Units used: `esr-s20-g-{ctl3318,pre3520,
  ctl3520,exp4274,c1793,c2080a,neg2080,c2080b,c0161,rootmem,rootmem2,rp3520,stopafter,multi}`, at most 2 at a time. Foreground
  commands: Python checks of a few seconds (`check_prepass.py`, `cmp_export.py` inside units, `subroot.py`,
  `calib_gate.py`, `axlines_view.py`, the driver tests) and hashing (0.4 s). The import test read 320 finished RS3519
  oleans of res-slices-fv (read-only; a finished olean is not written again).

## 9. Resume

```bash
G=/home/jay/research/data/formalize-20261122/s3520-gate; PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
S=/home/jay/research/data/es308-20261114
(cd $G && grep -v '^#' data/tools-frozen.sha256 | sha256sum -c --quiet) && echo tools ok
# re-export one unit (deterministic; compare with data/gate-files.sha256):
$G/tools/gate_start.sh exp<U> 3000 3600 1000 90 $PY -I -B $G/tools/slice_export_v3.py 3520 --budget 35 \
  --master $S/runs/b35s20/bb-s1/master.json --ctxdir $S/runs/b35s20/bb-s1 --extra $S/inputs/b35s20-v169/extra.json \
  --out $G/export/3520 --unit-leaves 40000 --chunk-leaves 8000 --units <U>:<U+1>
# compile a unit's modules (skips existing oleans), then its sub-root:
$G/tools/gate_start.sh c<U> 2000 14400 800 90 $G/tools/compile_loop.sh $G/export/3520 3520 <U> 0 1
$PY -I -B $G/tools/subroot.py $G/export/3520 <U>    # then compile.sh export/3520/src/RS3520/U<UUUU>.lean in a unit
$PY -I -B $G/tools/axlines_view.py $G/axview $G/export/3520 3520 2080 161 1793      # expect only Root/Final problems
```

# VERIFY_s35_20-gate: independent review of the s35_20 launch gate (22 Nov 2026, 22:50–23:25 KST)

Reviewer's work directory: `/home/jay/research/data/formalize-20261122/s3520-gate/review`, the only place this review
wrote (one exception, §6). Every check uses my own scripts in `review/tools/`, not only the worker's.

Units, one at a time, each started after the gate check (YIELD absent, Tctl 75–83 °C, cpu_free 3–4, s20 track empty):
- `esr-s20-rv5-gzhash` and `-gzhash2`: Python, about 1 min each;
- `esr-s20-rv5-ax`: the ONE Lean compile;
- `esr-s20-rv5-reexp`: one exporter run, 6 s.

## 1. Verdict

**Gate: CONFIRMED except for the literal pre-registered axiom-line criterion and the launch command.** The campaign was
not launched. Nothing about `s35_20` as a whole is claimed, and `RS.s35_20` does not exist.

1. **Acceptance item 3 holds only through re-print.** It was pre-registered as "all required": a whole standard axiom
   line in each chunk log. For C208014 and C208053 it was **not met literally**, because profiler output split those
   two lines. The worker re-printed them from their oleans, and my own compile without the profiler re-printed all 75
   lines whole and standard. The axioms themselves are therefore confirmed; the literal criterion is not. The worker
   says the same.
2. **LAUNCH_PLAN §5 needs a fix.** The command it gives (`FVR_JOBS=4`) runs 4 compiles once the export ends. The plan's
   own rule (§6.5) makes more than 3 an owner decision (§4).

**Theorem `RS3520.U2080.root`** (the context-level fact for ctx-4274, unit 2080 of 3,212):
`¬ ∃ holes : Fin 154 → ℕ, CompactChecker.FFeas CompactChecker.fcatS3520 4642 154 35 (CompactChecker.pmask
(CompactChecker.zerosF 154) [(109, 2), (75, 2), (133, 1), (33, 2), (25, 2), (17, 2), (20, 1), (56, 1), (45, 2), (36, 2),
(54, 2), (98, 2), (44, 1), (0, 2)]) holes`.
- **Label: Lean-checked (standard axioms, no hypotheses).** The trust items are those of res-slices-fv §3: imported
  oleans are pinned by hash and not re-checked against their sources.
- What it is not: a statement about the slice. It covers 320,422 of 119,054,033 leaves. With units 161 and 1793
  (11 chunk modules, no sub-root), Lean has checked 387,322 leaves.

## 2. Checks and results

| key | verdict | check (my own code) and result |
|---|---|---|
| prereg | **confirmed** | **Method.** I rebuilt the README as of 21:16:56 from the worker's session transcript: its `Write` at 21:16:44, then the `sed -i` at 21:16:53 that changed "21:20" to "21:16" (`tools/prereg_replay.py`; snapshot `logs/README_at_prereg_sed.md`). **Hash.** sha256 **1aaae17c…** equals `data/prereg-readme.sha256`, so the worker's "cannot be re-verified" issue is closed. §3 today is byte-identical to §3 at 21:16:56. **Timing.** Before 21:16:44 the worker only read files. The first 3520 output is born at 21:31:15. **Inputs.** Res118 `Final.lean` (`7f9198b7…`) states `(s35_20 : ResSliceExcludes (rowsP ++ rowsQ ++ rowsA) 35 20)` verbatim. Master `71993a47…` and extra `de4bcceb…` re-hashed. Expected leaves 119,054,033 = the ES307 T6 count = T7's 119,054,034 minus the pending leaf. |
| statement | **confirmed** | **Walker.** My own master walker (`tools/rv_master.py`): 16,347 nodes (8,173 branch, 94 weighted, 8,080 placeholders), each reached once. Ids are 0..8080 with only **4782** absent, and node 12473 is context 4274. The zero child maps to 2 (occupied, hole 0) and the one child to 1 (missing, hole 1). **Path.** It equals the theorem's mask, `skeleton.json` `tops[2080].path`, the manifest `base_path`, the ctx-4274 header and all 8,080 `contexts.json` headers. **Lean.** It accepted my own fully qualified `theorem rv_stmt : <statement> := RS3520.U2080.root`. |
| catalog / glue | **confirmed** | Same compile, all three accepted: `rv_cat : Res118.SliceCatalog CompactChecker.fcatS3520 (P ++ Q ++ A) 35 20 := RS.cat3520_ok`; `rv_rows` (2652 + length = 4642); `rv_glue` (mask `[(0, 2)]` gives `Res118.ResSliceExcludes (rowsP ++ rowsQ ++ rowsA) 35 20`). I called drive_v3's own `final_text` and `spec_text` (`logs/rv_drive_texts.out`): the 3520 Final states the pre-registered statement and ends `exact RS3520.root`, and the six-slice specialisation has no slice hypothesis left. |
| binding (no CNF verdicts) | **confirmed** | **Context files.** In a unit, sha256 of all 8,080 `ctx-*.json.gz` against T7: **0 mismatches**. **Digest.** The contexts digest computed from T7's hashes (`b3fd865d…`) equals the skeleton's, the pre-pass's and the one in every chunk header. **At export time.** The exporter re-hashes each gz against the pre-pass when it loads it. |
| one provider per module | **confirmed** | 5,151-module closure from my compile, under the same LEAN_PATH; none missing. **Duplicates.** 6 `CompactChecker` modules sit in 2 directories, but both entries are symlinks to the same pinned file. **Origins.** All 69 `RS3520.*` modules come from the gate's `olean/`. **Pins.** `CompactChecker` olean hashes appear in `logs/es311/final311-compact.json`. `RS.Cat3520_p0..p5`, `RS.Cat3520` and `RS.Bridge3520` equal the pre-registered hashes. |
| axioms | **confirmed** | **ONE compile**, `esr-s20-rv5-ax`: lean v4.24.0 `-j1`, read-only LEAN_PATH, no profiler; lean_rc 0, 34 s, 277 MB anon. **Results.** `[propext, Classical.choice, Quot.sound]` for `RS3520.U2080.root`, `RS.cat3520_ok`, `rv_stmt`, `rv_cat` and `rv_glue`; `[propext]` for `rv_rows`, `rv_pos` and both negatives. All **75** chunk axiom targets print whole standard lines. **Sources.** None of the 69 sources contains `sorry`, `axiom`, `native_decide`, `implemented_by`, `extern`, `unsafe` or `ofReduceBool`. |
| acceptance item 3 (literal) | **not_confirmed** | The 2 profiler-split lines (C208014, C208053) are whole only in re-prints: the worker's `RP3520` and my compile. |
| non-vacuity | **confirmed** | Kernel proofs by `decide +kernel` that `checkF2 … = false`: the worker's corrupted block `b231858`, and the genuine block at budget 36 instead of 35 (my own perturbation). `rv_pos` = `chk231858` at budget 35. The theorem has no hypotheses. |
| prepass | **confirmed** | **All contexts.** For all 8,080, `prepass.json` (leaves, gz sha256, nodes, leaves = branches + 1) equals T7: 0 mismatches. **Total.** 119,053,939 + 94 master leaves = **119,054,033** = skeleton `total_leaves` = the sum of the 3,212 unit leaves. **Streamed counts.** My own counts equal T7 for contexts 4274, 4781, 4783, 0, 8080 and 169. **Unit statistics.** 863 units above 40,000 leaves hold 59,237,580 leaves; the largest unit is 2080. |
| export binding | **confirmed** | **Leaves.** For all 3 manifests the leaves add up (2080 = T7 ctx-4274; 161 = T7 ctx-169). **Modules.** All 68 sources hash to the manifest values and have oleans. Every module has min_margin 1, 0 leaf-test failures and 0 over_budget leaves. Every module's axiom targets are its subtree roots. All import exactly `RS.Cat3520` and `CompactChecker.Path`. **Hash list.** `data/gate-files.sha256` checks 144/144. |
| measurements | **confirmed** | **CPU per leaf** (user + sys): 2080 **0.01260**, 161 0.01246, 1793 0.01158, all 0.01253; per module 0.0112–0.0142. **Bytes per leaf:** 821 source + 1,108 olean. **Compiles:** anon peak 748 MB (C208024), RSS at most 3,757 MB. **Exporter:** 705 MB on ctx-4274 (maxrss 720 MiB) and 1,189 MB in the 21-unit run (maxrss 1,195 MiB); the pre-pass used 155 MB. |
| byte identity | **confirmed** | **Re-hashed.** 3318: reference = v3 = res-slices-fv w13 chunk. 3520 units 161 and 1793: all 11 modules identical. **Regenerated.** The frozen v3 exporter (`4b5c5092…`), re-run on unit 1793 into `review/reexp` in 5.8 s and 134 MB, reproduces C179301–03 and `skeleton.json` byte for byte. |
| negative control | **confirmed** | **Diff.** My token diff finds exactly one packed word changed in `C208021`: row 20, weight 2266 → 2265. **Rejection.** lean_rc 1 with "decide proved … is false" at `chk231858`, and no olean. **Locality.** Modules 01, 20 and 22 of the control export equal the gate's. **`--stop-after 0`:** rc 0, no output, and the rerun is identical. |
| tools | **confirmed** | **Diffs and hashes.** All 5 diffs regenerate identically, and `tools-frozen.sha256` passes. The exporter hashes are the same in all three freeze files and in the manifests. `export_es310_w13l.py` only adds lines. **id fix.** It iterates the sorted placeholder ids. **drive_v3.** The diff does what it states. Its tests ran after its last edit. The sandbox did not touch the live driver: `res-slices-fv/driver.log` has 0 lines with "3520". drive_v3 does no I/O at import time. |
| worker stayed in its directory | **confirmed** | **Writes.** In the worker's transcript there is no Write or Edit outside `s3520-gate`. All 25 Bash commands with write operators and outside paths write inside `$G`. **res-slices-fv tools.** All files have mtimes before 20:05. `audit.py` (`62623f9f…`, mtime 18:00:58) predates the worker, and the `ea311f5b…` in res-slices-fv README §7 is stale. That is res-slices-fv's matter, not this item's. |
| launch plan numbers | **confirmed** | **Recomputed.** 383.6–416.7 CPU-h (370–470 at the per-module extremes). Wall time: 5.33–5.79 / 2.66–2.89 / 1.33–1.45 days at 3 / 6 / 12 compiles. Export 10.4–11.6 h. Disk 97.7–101.9 + 131.3–137.3 GB. `FVR_MEM` 4,050 / 6,600 / 11,700. All HEURISTIC. **Root/Final memory.** FV304's 429 / 451 MB was found in fv304-audit; the "8:53 wall" was not re-checked. |
| launch plan commands | **not_confirmed** | §5 runs 4 compiles after the export, against §6.5 (fix 1 in §4). Otherwise correct: the hash check passes, `cp -n` plus the re-hash is safe, and the unit parameters match the code. `audit.py` and `root_slice.py` are tag-generic and read v3 manifests. |

## 3. What the gate establishes, and what it does not

**Established:**
- the patched exporter reproduces the reference byte for byte, and its frozen copy regenerates the gate's unit 1793;
- it exports the largest context at 705 MB (the reference would need about 5.4 GB);
- the campaign's checker and catalog accept all 57 chunks of ctx-4274 and its sub-root, with standard axioms;
- a corrupted chunk is rejected;
- the pre-pass equals T7 for every context.

**Not established (the worker discloses all of these):**
- drive_v3 has never run live.
- The memory and time of the Root, the Final and the specialisation at about 20,900 modules are projected, not measured. That closure is about 131–137 GB of oleans, more than the 60.9 GB of RAM.
- A one-file Root with about 20,900 direct imports has no precedent. FV304's Root was built over 8 S3 sub-roots (fv304-audit: "8,207 chunks, 8 S3, Root and Final").
- Exporter heap growth beyond 21 units per process is unmeasured; the hourly restart bounds it.

## 4. Required fixes

1. **LAUNCH_PLAN §5 against §6.5.** drive_v3 counts every active `esr-fvr-*` unit, the exporter included, toward
   `FVR_JOBS`. So `--setenv=FVR_JOBS=4` gives 3 compiles while the exporter runs and **4 once the export ends (about
   11 h in)**. That contradicts §6.5 and the worker's resume note ("above 3 needs the owner's OK"). Choose one:
   - add an explicit step: restart the driver with `FVR_JOBS=3` when `status.json` shows `units_exported` = 3,212;
   - start with `FVR_JOBS=3` (2 compiles while the export runs);
   - get the owner's OK for 4 (the old res-slices-fv §4 maximum).
2. **Wording nits (never round up):**
   - "FVR_CEST=450,20 … above every measured module by ≥ 100 MB": the minimum is **97 MB** (C208057: 4,541 leaves,
     estimate 677 MB, measured 580 MB).
   - "levels off after about 12" units: maxrss is a high-water mark and still rises 546 → 618 MB over units 13–20.
   - "≤ 37 %" is 37.4 %.
3. **Acceptance recipe (§8).** `audit.py 3520` re-hashes and shape-checks about 100 GB of sources and hashes about
   135 GB of oleans. The 3,600 s deadline in res-slices-fv §9 (sized for 3519, about 16 GB) would be far too short. Give
   the audit unit a deadline of several hours (HEURISTIC).

## 5. Not checked

- I did not recompile any chunk from source: the oleans are trusted as pins, as for every project.
- I did not run drive_v3's `main()`.
- I did not read export_compact line by line beyond its refusals and replays. Byte identity on 4 units, and Lean as the
  checker, cover it.
- FV304's Root wall time.

## 6. Disclosures

**Reviewer:**
- **Reads of files the running driver `esr-fvr-drv` writes** (all read-only): res-slices-fv `run.tsv`, once (grep for
  the Root rows), and `driver.log`, once (`grep -c 3520`, to show the sandbox did not write there).
- **One write outside my directory:** a temporary diff file under `/tmp/claude-1000/`, deleted at once.
- **First gz unit:** it printed a wrong equality flag (bytes against str keys; the counts were right). Its output is
  kept as `logs/rv_prepass_gz.run1-flagbug.out`, and the run was repeated as `-gzhash2`.
- **Transcript:** I read the worker's session transcript (read-only, local) to rebuild the pre-registered README.

**Worker (accepted):**
- two s20 compile units ran at once, which the item allows ("units one or two at a time", "up to 2 units");
- one read-only read each of res-slices-fv's live `status.json` and `tries.json`, the same class as my reads above;
- the import test read 320 finished RS3519 oleans.

## 7. Files (sha256 prefixes)

**Tools** (`tools/`):
- `prereg_replay.py` `86034651…`
- `rv_master.py` `0a7d766d…`
- `rv_prepass.py` `4a184512…`
- `rv_files.py` `f2646f9f…`
- `gen_rv.py` `b254ac5d…`
- `rv_compile.sh` `53df185d…`
- `rv_providers.py` `f4b82910…`
- `rv_gate.sh` `d90d3b31…`
- `rv_worker_writes.py` 6cacc06e…

**Lean:**
- `lean/RV3520.lean` `33cb677f…`
- `olean/RV3520.olean` `2067998e…`
- `logs/RV3520.log` `1dbdcfcc…` (lean_rc 0), with `.mem` and `rv_lean_path.txt`

**Outputs** (`logs/`):
- `README_at_prereg_sed.md` `1aaae17c…`: the pre-registration snapshot
- `rv_master.out`, `path4274.txt`
- `rv_prepass_json.out`, `rv_prepass_gz.out`
- `rv_files.out`, `axtargets.json`
- `rv_providers.out`
- `rv_drive_texts.out`
- `rv_worker_writes.out`
- `rv_reexp.out`, with `reexp/3520/`

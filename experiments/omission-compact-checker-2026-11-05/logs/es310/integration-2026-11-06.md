# ES(8) <= 310 compact check: integration log (6 Nov 2026)

ES(8) <= 310 is NOT proved. These are tests of the pipeline only (prefixes E310BT, E310BX, E310BK; outputs in
build/es310/test-*). Nothing was written under the campaign directory C, no 311 build directory was touched,
no lake build was run. Times are KST (UTC+9) unless marked Z.

D = /path/to/repo/experiments/omission-compact-checker-2026-11-05
C = /path/to/data/es8-b64-pilot-20261105

## 0. Start state (13:30 KST)
- Tctl 70.2 C, MemAvailable 50 GiB, load 33.9; es8-b64-campaign and c6upper-noty12 active (not touched);
  no lean process running; campaign STATUS: closed 422 of 4096, running 28.
- sha256 of every es310 file and of the 311 files it reuses: logs/es310/integration-shas-start.txt.

## 1. E1 (Python only)
- `bash test_export_es310.sh` (13:30-13:31): rc 0, **111 passed, 0 failed** (log logs/es310/test_export_es310.log).
- `bash test_coverage_es310.sh` (13:31-13:32): rc 0, **50 passed, 0 failed**
  (log logs/es310/test_coverage_es310-20261106-133114.log).

## 2. E3 end to end on real closed ctx 2406 + 2407 (OUT = build/es310/test-e2e)
Commands (cwd D; C read only; SRC = ../omission-cover-certificates-2026-10-10/balanced-v2-source.json):
```
nice -n 10 python3 export_es310.py --campaign $C --source $SRC --ctx 2406,2407 --chunk-leaves 500 \
    --block-leaves 64 --per-word 8 --prefix E310BT --out build/es310/test-e2e
nice -n 10 python3 merge_es310.py build/es310/test-e2e --subtree 11:1203 --prefix E310BT
nice -n 10 python3 coverage_es310.py build/es310/test-e2e --subtree 11:1203 --prefix E310BT --campaign $C \
    --exporter-sha256 5aa0f571... --report build/es310/test-e2e/coverage-subtree.json
nice -n 10 python3 shapes_es311.py build/es310/test-e2e
python3 drive_es310.py build/es310/test-e2e --jobs 2 --nice 10 --no-final      # no --reuse needed
```
- export: exit 0, 2.2 s wall, 125 MB RSS. ctx 2406: 921 leaves, 3 modules, internal skeleton 2 nodes;
  ctx 2407: 1,781 leaves, 5 modules, internal skeleton 4 nodes; K 131072 both; min margin 1; 0 Lean-test failures;
  counts equal the results' (leaves 921/1781, nodes 1841/3561).
- merge --subtree 11:1203: exit 0; export_root 1000003251 (= 10^9 + 2^11 + 1203); 7 skeleton theorems
  (6 context-internal: ex2407000xx, ex2408000xx; 1 top: ex1000003251); root at the depth-11 path (11 decisions).
- coverage --subtree 11:1203: **PASS** (exit 0), 48 checks, 2 contexts deep-checked, 2,702 leaves, 0 warnings, 0.5 s.
- shapes_es311.py: PASS (9 files).
- driver (13:33:44-13:34:34 KST, 54 s wall, Tctl 71 C at start, at most 2 Lean jobs, MemoryMax 12G, nice 10):
  **9/9 ok** (8 chunks + E310BT.Root), every expected theorem `[propext, Classical.choice, Quot.sound]`.

| module | leaves | kernel s | wall s | RSS KB | cgroup peak KB | .olean bytes |
|---|---|---|---|---|---|---|
| C240701 | 425 | 7.94 | 10.85 | 3317016 | 561496 | 1628640 |
| C240705 | 412 | 7.69 | 10.63 | 3318288 | 564480 | 1558912 |
| C240603 | 392 | 9.27 | 12.55 | 3309384 | 560688 | 1523448 |
| C240702 | 335 | 6.26 | 8.91 | 3306128 | 547092 | 1305880 |
| C240704 | 324 | 5.93 | 8.62 | 3262136 | 502420 | 1266096 |
| C240601 | 293 | 5.71 | 8.37 | 3252576 | 497108 | 1155176 |
| C240703 | 285 | 5.25 | 7.85 | 3284064 | 525520 | 1094792 |
| C240602 | 236 | 4.28 | 6.79 | 3272972 | 514356 | 933584 |
| Root | 2702 | 0.002 | 2.19 | 3073352 | 303564 | 53360 |

  Totals: 52.3 s kernel for 2,702 leaves (19.4 ms/leaf), 10.47 MB of chunk .olean (3.87 KB/leaf at k = 8).
- **E3: PASS.**

## 3. E4 path enforcement (same pair; hand-edited copies of test-e2e)
New test-only helper `make_pathflip_es310.py` (writes only build/es310/test-*; refuses /tmp: checked). It copies
test-e2e and replaces ctx 2407's 12-decision base path B, as the exact tail of every path literal, by B'. All
edited files' sha256 are re-recorded (context manifest, merged manifest modules/root, ctx_manifests pins), so the
checkers must catch the edit semantically. Copied .olean files of edited modules and of the sub-Root are deleted.
Read-only pre-scan (scratchpad flip_scan.py): flipping any one of the 12 base decisions of ctx 2407 makes
1,732-1,781 of its 1,781 leaves fail the full-load margin (min margin -99,360 to -267,635), so a flipped chunk
can never compile; the Root-level test therefore keeps the true chunks.

| copy | edit | coverage --subtree 11:1203 | Lean |
|---|---|---|---|
| test-e4-flipall | decision 1 (87,1)->(87,2) in all 5 ctx-2407 modules (151 path literals), ctx-2407.json base_path and the 6 ctx-2407 Root theorems | **FAIL** (exit 1): ctx_manifest_fields, root_paths, statement_paths | 5/5 ctx-2407 chunks **rejected**: 9+7+6+8+9 = 39 of 39 blocks "`decide` proved that the proposition ... is false", sorryAx in axioms, no .olean; driver: "blocked: a prerequisite failed", sub-Root never started |
| test-e4-fliproot | same flip, sub-Root only (chunks true, their .olean reused from E3) | **FAIL**: root_paths | sub-Root **rejected**: 4 "Application type mismatch" (Root.lean lines 22, 24, 26 = ctx-2407 internal split_pm vs chunk ex at the true path; line 30 = top skeleton ex1000003251 vs ex240800000 at the flipped path), sorryAx, no Root.olean |
| test-e4-swaproot | decisions 1 and 2 swapped ((87,1),(71,1)) = same mask (crit1 item 3), sub-Root only | **FAIL**: root_paths | sub-Root **accepted** (ok, standard axioms, wall 2.5 s): Lean identifies the permuted path by defeq, as crit1 item 3 predicted. Literal-path equality is enforced only by coverage_es310.py. |

shapes_es311.py passes all three copies (the edit keeps every line shape). **E4: PASS** (coverage fails on all three;
Lean rejects the flipped mask both at chunk and at Root level; the same-mask swap is caught by coverage only).

## 4. E2 rejection (OUT = build/es310/test-e2-reject, prefix E310BX)
```
nice -n 10 python3 export_es310.py --campaign $C --source $SRC --ctx 2406 --chunk-leaves 500 --block-leaves 64 \
    --per-word 8 --prefix E310BX --corrupt 1 --out build/es310/test-e2-reject
nice -n 10 python3 merge_es310.py build/es310/test-e2-reject --subtree 12:2406 --prefix E310BX
python3 drive_es310.py build/es310/test-e2-reject --only E310BX.C240601 --bench 1 --jobs 1 --nice 10 --no-final
```
- export: exit 0; corruption {module E310BX.C240601, leaf_node 48, row 3, weight 46 -> 45, margin 1 -> 0};
  stats.lean_test_failures = 1. The exporter refuses unless the Lean-test transcription fails exactly at the
  corrupted leaf (export_es310.py:536-540, :573-574), so "exactly that leaf" is enforced, not just counted.
- merge --subtree 12:2406: exit 0, corrupted_modules ['E310BX.C240601'] flagged in the merged manifest.
- coverage --subtree 12:2406: FAIL as it should (block_terms at b37 node 48; module_not_corrupted).
- Lean (13:41:29, Tctl 73.6 C, 1 job): verdict **fail**, wall 9.8 s, cgroup peak 491 MB; the log has exactly one
  "error: Tactic `decide` proved that the proposition\n  checkF2 fcat62 3131 252 64 1048576 131072 536870912 8 b37 ..."
  (b37 holds leaf 48), `E310BX.C240601.ex1` depends on [propext, sorryAx, Classical.choice, Quot.sound];
  `find build/es310/test-e2-reject -name '*.olean*'` finds nothing. **E2: PASS.**
- Bug found and fixed (cosmetic, diagnostics only): coverage_es310.py `diagnose()` (leaf branch, now lines
  745-746) returned "leaf entries differ" for the FIRST leaf of a mismatching block, without comparing it, so it
  named node 41 (an intact leaf; "subset: True"). It now skips leaves whose term equals the expected one and
  names node 48 ("subset: False"), matching the exporter. Verdicts are unchanged (block_terms failed before and
  after).

## 5. E5 calibration of the per-word k (ctx 2407, 1,781 leaves, one module at --chunk-leaves 12000)
New script `calibrate_k_es310.sh 3` (log logs/es310/calibrate_k_es310-20261106-134404.log). Exports
build/es310/test-calib-k{4,8,16}-a (export_es310.py --ctx 2407 --chunk-leaves 12000 --block-leaves 64
--per-word k --prefix E310BT; merge --partial; coverage --partial PASS for all three), each copied to -b.
Two lanes, each compiling E310BT.C240701 by drive_es310.py --only ... --bench 1 (MemoryMax 12G, nice 10,
driver gate Tctl < 80): lane a k = 4,8,16 x 3 rounds on the -a copies, lane b k = 8,16,4 x 3 rounds on the -b
copies; so at most 2 Lean jobs, k interleaved in time, 6 runs per k (13:44-13:52 KST, load 34-38, Tctl 76-78 C).
All 18 compiles ok with standard axioms.

| k | source bytes | words | .olean bytes (same every run) | KB/leaf | kernel s, 6 runs (sorted) | min | median | x k=4 (median) | elab median | user median | RSS max | cgroup max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 2,923,784 | 77,512 | 11,493,216 | 6.45 | 34.8 35.8 38.0 38.6 41.0 44.1 | 34.8 | 38.30 | 1.00 | 2.27 | 43.80 | 3.45 GB | 732 MB |
| 8 | 2,861,609 | 39,201 | 6,606,800 | 3.71 | 34.7 35.5 36.8 42.9 43.6 43.9 | 34.7 | 39.85 | 1.04 | 2.58 | 45.66 | 3.41 GB | 678 MB |
| 16 | 2,828,535 | 19,973 | 4,150,688 | 2.33 | 35.1 37.1 38.8 43.0 43.0 43.6 | 35.1 | 40.90 | 1.07 | 2.77 | 46.73 | 3.38 GB | 660 MB |

- Kernel times are bimodal (34.7-38.8 s or 42.9-44.1 s) in every k, which is co-scheduling noise, not k: the minima
  are equal within 1% (34.7-35.1 s). The medians (1.04x, 1.07x of k = 4) are within the design's 1.15x rule, but
  6 runs cannot resolve a 4-7% difference. Elaboration grows slightly with k (2.27 -> 2.77 s per module).
- Projection at 7.0-7.3M leaves (linear, unverified): .olean 45-47 GB (k=4), 26-27 GB (k=8), 16-17 GB (k=16).
  Kernel ~ 21.5 ms/leaf median at any k on this context (E3 at k=8, L=500: 19.4 ms/leaf).
- **Recommendation: k = 16.** By the design's rule (smallest .olean whose kernel time stays within 1.15x of k=4)
  it is k = 16: 36% of the k=4 .olean and 63% of k=8, at a median kernel cost of +7% (within noise); the whole
  E310B set (~17 GB) then fits in the page cache beside the campaign, which matters most for the Root, E310.Final
  and the assembly, each of which walks every imported .olean. If the reviewer prefers the cheaper CPU side,
  k = 8 is the conservative choice (+4%, ~27 GB). Either way the choice must be frozen before the real export
  (design G.3).

## 6. E6 import probe (new script `probe_import_es310.sh CAP`; logs logs/es310/probe_import_es310-*.log)
Steps: posix_fadvise(POSIX_FADV_DONTNEED) on the 352 .olean files of build/es311/full/olean (6.46 GB), each
opened O_RDONLY; then `lean -j1 build/es310/test-e6-probe/ProbeE311.lean` (`import E311.Final`, `#print axioms`
of E311.balanced_excludes_63 and E311.residual_excludes_32), WITHOUT -o (no .olean written), in a transient scope
MemoryMax=CAP, MemorySwapMax=0, nice 10, /usr/bin/time -v; LEAN_PATH = lake's : build : build/ext :
build/es311/full/olean. build/es311/full/olean checked unchanged (paths, sizes, mtimes of all 352 files) after each run.

| cap | start | lean exit | oom_kill | memory.events max | cgroup memory.peak | RSS | wall | axioms |
|---|---|---|---|---|---|---|---|---|
| **4G** (the design's probe) | 13:55:39, Tctl 76.6 C, MemAvailable 42.4 GiB | 0 | 0 | 5,662 | 4,294,967,296 (= the cap) | 6.91 GB | 42.3 s | both standard |
| 12G (comparison, cold cache) | 13:56:32, Tctl 76.1 C, MemAvailable 50.1 GiB | 0 | 0 | 0 | 6,800,404,480 | 9.38 GB | 36.6 s | both standard |

- **E6: PASS** at 4G. With a cold page cache the imported .olean pages ARE charged to the compiling cgroup (6.8 GB
  at 12G; the 311 run's 0.35 GB peak for E311.Final was a warm cache charged elsewhere), but they are file-backed
  and reclaimable: under the 4G cap the cgroup sat at its limit (5,662 reclaim events) and finished with no OOM,
  16% slower than without reclaim (42.3 vs 36.6 s).
- Consequence for the plan (design F): a Root / E310.Final / assembly cap does not need to exceed the total
  imported .olean; 24G is enough on memory grounds at any k, and at k = 16 (~17 GB) the whole set also fits under
  24G without reclaim. Not shown: behaviour at ~4,100 modules and 17-48 GB (crit1 item 6: re-probe with a partial
  E310B import after the campaign).
- Machine note: MemAvailable was 42.4 GiB at 13:55 (another process, not from this workflow, was using ~8 GB;
  50.1 GiB again at 13:56).

## 7. E7 driver and assembly tests
### test_driver_es310.sh build/es310/test-driver (all cases G H I J K L M T A B C D E F)
- Run 1 (13:57:48-14:02:52, script sha 2a78f675 as delivered; log logs/es310/test_driver_es310-integration-20261106.log):
  **79 passed, 1 failed**. Compile cases T, A-F (never run by builder 3) all PASS: T ok + .olean with the recorded
  sha256 + restart runs nothing; TX fail with "`decide` proved that the proposition", no .olean; A (kill -9 of
  /usr/bin/time) and B (kill -9 of sh): verdict fail, no lean left, no .olean 25 s later; C (kill -9 of the driver
  with 2 compiles running): restart "cleaned up: 2 leftover scopes stopped", no stray tmp, all three modules ok;
  D: to_run 0 / already_done 3; E (SIGTERM): exit 130, no process, no tmp, no row; F: corrupted chunk fail.
  The failure: "H: while drive_es310 runs with --reuse, drive_es311.py's exclusive lock on build/es311/full is
  refused" - H.lock2.out said "exclusive lock GRANTED".
- **Bug 1 (test race, fixed):** the test starts the driver with `> H.lock.out &` and polls that file with wait_for;
  the background job truncates the file only when it starts, so wait_for matched the stale "waiting: Tctl" line of
  the builder's earlier run, the flock probe ran (13:58:01) before the new driver had taken its shared lock, and the
  driver then stopped at once on STOP (its output has no "waiting:" line). The same race could make J's
  "--max-tctl 1: the driver waits" and "fresh PAUSE line" checks pass on stale text. Fix: test_driver_es310.sh:225-227
  (`rm -f H.lock.out H.lock2.out` before the launch), :339 and :352 (`rm -f J.t.out J.p.out`). Not a driver bug: the
  driver takes the shared lock (drive_es310.py:607-612) before anything else.
- Re-run of H and J after the fix (14:07; log ...-integration-HJ-20261106.log): **31 passed, 0 failed**, including
  "exclusive lock refused" and "waiting: Tctl 79.2 C >= 1 C".
- **Bug 2 (test hang, fixed):** a second full run (log ...-integration-rerun-hung-20261106.log) hung in case A: R
  was left fully compiled by run 1 (`[ -d R ] || mk_R`), so the driver had nothing to run (to_run 0, exit at
  14:12:52) and `wait_lean` waited forever for a lean process. I stopped that test script (my own process, pid
  1188938; no Lean was running). Fix: case A now makes R afresh (test_driver_es310.sh:496-498), and `wait_lean`
  takes the driver pid and returns 1 when the driver has exited or after 60 min (:86-93; callers :507, :525, :550).

### test_assemble_final310.sh (14:07:52-14:09:58, 2 min 6 s; summary logs/es310/assemble-tests.txt)
Script sha256 c1c4727a (unchanged), assemble_final310.sh e22b4885 (unchanged), drive_es310.py 868d6be9 (unchanged).
Every Lean job ran one at a time in a MemoryMax=12G / MemorySwapMax=0 / nice 10 scope (its own gate: Tctl < 85 C,
< 2 lean processes). Result: **every case as expected; 57 of 57 "exit N (M expected)" lines have N = M**:
- 0: Final310Compact.lean sha256 = pin 7a91d397; FINAL_TEMPLATE = design D outside comments; variants (budget 63,
  `import E311.Final`, hidden `axiom cheat`) rejected.
- 1-2: stub E310.Final (sorry) compiles; `--test-stub`: Lean exit 0 on both compiles (cgroup peak 0.34/0.33 GB),
  statement `ErdosSzekeres.ForcesConvexNGon 310 8`, rejected ONLY for sorryAx (main and audit); route same, 13 inputs
  equal to the 311 pins, 7,551 .lake .olean under the freeze (newest 2026-11-04T14:45:15Z), 5,160 imported modules.
- 3: synthetic 4,096-context export accepted; 14 perturbations each refused for the right reason; gates pass case
  accepted and 7 gate failures refused; --dry-run on the synthetic and on the real (absent) export refused with the
  reasons (campaign not finished, unit active, exporter pin empty); a process named like the driver refused.
- 4-5: shadowed BalancedBudgets.olean and build/ext on LEAN_PATH refused. 6: audit probe exit 0, 4,969 modules.
- 7: report on synthetic logs: signal, OOM, statement 311, fake second axiom line, axiom line of another name, two
  statement lines, an E311B module, audit without axiom line: all rejected.
- 8: test switches outside test mode and A310_MEM=45G refused; 44G passes the guard.
- 9-10: pins on a fake tree and the .lake freeze: unchanged passes; every change refused.
- 11-12: a fake `#print axioms` line via #eval and a `ForcesConvexNGon 311 8` variant: both rejected.
**E7 assembly: PASS.**

### test_driver_es310.sh, final full run with both fixes (14:22:06-14:32:42; script sha 993ea4a4)
Log logs/es310/test_driver_es310-integration-final-20261106.log: **80 passed, 0 failed** (all 14 cases, including H's
lock check and A-F on a fresh R; the compile cases waited several minutes at the driver's Tctl < 80 C gate, Tctl
79.6-81.4 C from the campaign plus 4 cadical processes of another job). Afterwards: 0 lean processes, 0 es310-*
scopes. **E7 driver: PASS.**

## 8. After the tests (14:35 KST)
- Hard rules: no file under C other than the campaign's own (logs/, runs/, campaign/) changed since 13:29; 0 files in
  build/es311, build/CompactChecker, build/ext, build/chain311 newer than 13:29; 0 .lake .olean newer than the
  freeze 2026-11-04T14:46:00Z; the 311 scripts (export/drive/coverage/shapes_es311, assemble_final311.sh) have their
  start sha256; no lake build; every Lean job capped (MemoryMax 4G-12G, MemorySwapMax 0, nice 10), at most 2 at once,
  each started below Tctl 80 C (driver) or 85 C (probe and assembly tests). Both units active and untouched; the only
  signals sent were to this workflow's own test processes. Nothing committed. build/es310 holds 739 MB of test output.
- Changed es310 files: coverage_es310.py f2c53dc4 -> e6e7cc31 (diagnostic message only); test_driver_es310.sh
  2a78f675 -> 993ea4a4 (two test bugs). New: make_pathflip_es310.py 9443032d, calibrate_k_es310.sh 3fb3e636,
  probe_import_es310.sh ebe314a4. Unchanged: export_es310.py 5aa0f571, merge_es310.py 1449177d, drive_es310.py
  868d6be9, assemble_final310.sh e22b4885, Final310Compact.lean 7a91d397, the other test scripts
  (logs/es310/integration-shas-end.txt). After the coverage change, test_coverage_es310.sh was re-run: 50/50
  (logs/es310/test_coverage_es310-20261106-135805.log).
- Open, for the user / reviewer: freeze k (recommend 16) and the exporter, then fill EXPORTER_SHA256 in
  assemble_final310.sh (empty, so real mode and --dry-run refuse); a permuted base path is accepted by Lean (E4
  swap) and caught only by coverage_es310.py; the real export and any compile in build/es310/full were not run.
  ES(8) <= 310 is NOT proved.

## 9. Fixer pass after the soundness and operations reviews (15:05-15:31 KST)
ES(8) <= 310 is still NOT proved. Every review finding was checked against the code; all were real except where
noted. Fixes are in es310 files only (no 311 file changed; `git diff` of tracked files is empty). Start/end
sha256: logs/es310/fixer-shas-start.txt, logs/es310/fixer-shas-end.txt.

| review item | verified in code | fix (file) | test |
|---|---|---|---|
| S1 Final310Compact pin checked only at step 0 | yes: compile of FINAL_SRC in place, report never compared | the source is copied to WORK/final-src, the copy's sha256 is checked right before the compile, the copy (read-only) is compiled; the report fails unless the compiled source has the pin (assemble_final310.sh) | assembly 2 (compiled source = pinned copy), 7m, 12 |
| S2 report compares only library .olean | yes (inherited from 311) | every non-library .olean in the environment is compared: E310B/E311R/E310.Final with the last run.tsv rows, CompactChecker with the 13 route pins, chain311 with build.tsv, Final310Compact with the .olean just written; unrecorded ones fail (only the test-mode stub E310.Final is exempt) | assembly 7j (88 compared), 7k, 7l |
| S3 driver never recompiles a stale Root / Final | yes: stamps exclude the imports | a Root (E310.Final) is done only if all its chunks (both Roots) are done and ended <= 2 s after it started, the assembly's rule (drive_es310.py, fix 10) | driver S (3 cases), N unit tests |
| S4 coverage exporter pin is a substring test | yes | exact equality with the export_es310 field; non-64-hex pins are a usage error (exit 2) (coverage_es310.py) | coverage: 311 hash FAIL, prefix / 63 digits / "export_es310" / upper case exit 2 |
| S5 test modes print VERIFIED | yes | verified only in mode real; test modes print "TEST ONLY" and record test_only, checks_passed (assemble_final310.sh) | assembly 2, 7j |
| S6 other scripts unpinned | yes | MERGE/DRIVER/COVERAGE_SHA256 (empty until frozen) and SHAPES_SHA256 (set): check-run refuses unless the files, the manifest's merger_sha256 and the coverage gate's checker_sha256 equal them; new freeze_es310.sh fills the 4 empty pins once | assembly 3 (6 new refusals, gate cov-checker-sha), 14 (freeze on a copy) |
| S7 / O1 campaign-code edit stalls the export | yes | run_context.py / pbb_strong.py changes are recorded warnings (code_changed) in exporter, merge and coverage; contexts.jsonl and the source still ALERT | export 5b (5 checks), coverage D |
| O3a driver exit 0 after STOP | yes | exit 3 when work is left; 1 failures; 5 WITNESS (drive_es310.py, fix 12) | driver J (2), N |
| O3b exporter exit 0 with stale / permanently broken contexts | yes | exit 5 on stale_exporter; a missing / broken gz behind a result.json > 600 s old is refused as damage (export_es310.py) | export 2b (4), 3 (exit 5) |
| O3c one refused context stops the run | yes | per-context refusals go to refused_ctx, the others are exported, exit 1 at the end; WITNESS, contexts.jsonl / source changes stay global (RefuseAll) | export 2c (5) |
| O3d exit 4 means retry | documentation | OPERATOR.md exit-code table | - |
| O4 driver has no WITNESS check | yes (0 matches) | --campaign-dir: WITNESS refuses the start and, when it appears, stops new starts; exit 5 | driver N (6) |
| O5 44G root cap can never start | yes (waits forever) | --root-memory default 24G (was the 12G fallback); --mem-wait-max (1800 s): nothing running and memory blocked that long gives exit 3 | driver M, N |
| O6 start gap 5 s too fast | yes (default) | default --start-gap 60 | E3 used 20 |
| O7 cool() counts editor lean servers | yes (pgrep -xc lean) | helper lean-jobs: lean processes without --server/--worker | assembly 13 |
| O8 coverage takes no lock | yes | shared flock on OUT/.export.lock when it exists (opened read-only); held: exit 4 | coverage (exit 4) |
| O9 mkdir / empty EXPORTER_SHA256 | documentation | OPERATOR.md A1 (mkdir, freeze_es310.sh, rerun test_assemble) | - |
| O10 import walk at 17 GB untested | not a code defect | optional probe in OPERATOR.md A2 (needs approval) | - |
| O1/O2 freeze window, temperature gate | operational | OPERATOR.md "Never during the run", driver settings | - |

Final test runs (all on the final script sha256s of logs/es310/fixer-shas-end.txt, except test_export: rerun at 15:30
after a log-only edit of the test script, sha 7c46abe1):
- `bash test_export_es310.sh`: **128 passed, 0 failed** (logs/es310/test_export_es310.log; was 111).
- `bash test_coverage_es310.sh`: **58 passed, 0 failed** (logs/es310/test_coverage_es310-20261106-151709.log; was 50).
- `bash test_driver_es310.sh build/es310/test-driver` (all cases G H I J K L M N S T A B C D E F, 15:18-15:24):
  **94 passed, 0 failed** (logs/es310/test_driver_es310-fixer-20261106.log; was 80). Lean jobs: T/TX tiny, A/B killed,
  C three 935-1,000-leaf modules (2 at once), E killed, F corrupted; each started under the driver's Tctl < 80 C gate
  (Tctl 72-75 C), MemoryMax 12G, MemorySwapMax 0, nice 10.
- `bash test_assemble_final310.sh` (15:24-15:26): **69 of 69 "exit N (M expected)" lines match, 0 UNEXPECTED**
  (logs/es310/assemble-tests.txt, logs/es310/test_assemble_final310-fixer-20261106.out). The stub run: Lean exit 0 on
  both compiles, compiled source = WORK/final-src copy with sha256 7a91d397 (the pin), rejected only for sorryAx,
  test_only true, no VERIFIED line. 7 Lean jobs, one at a time, Tctl < 85 C, MemoryMax 12G.
- E3 end to end (`build/es310/test-e2e2`, fresh, ctx 2406+2407, L 500, B 64, **per-word 16**; log
  logs/es310/e3-e2e2-fixer-20261106.log, side outputs logs/es310/e3-e2e2/): export exit 0 (2.15 s, 120 MB RSS;
  921 + 1,781 leaves, 3 + 5 modules, internal skeletons 2 + 4, K 131072, min margin 1); merge --subtree 11:1203
  exit 0 (root 1000003251, 7 skeleton theorems); coverage --subtree with the exact exporter pin 29854a37: PASS (47
  checks, 0 warnings); shapes_es311: PASS; driver (--jobs 2, nice 10, Tctl < 80, start gap 20, 12G / 24G):
  **9/9 ok**, every expected theorem [propext, Classical.choice, Quot.sound], exit 0; restart dry-run to_run 0,
  stale_after_imports {}. Chunks: 57.1 s kernel for 2,702 leaves (21.1 ms/leaf), .olean 6.73 MB (2.49 KB/leaf;
  k=8 in section 2 gave 3.87 KB/leaf).

Hard rules (read-only checks, 15:31): 0 files newer than the start in build/es311, build/CompactChecker, build/ext,
build/chain311; 0 .lake .olean newer than the freeze; 0 files under C outside its own logs/runs/campaign changed;
export_es311.py, drive_es311.py, coverage_es311.py, shapes_es311.py, assemble_final311.sh, lean_make.sh unchanged;
es8-b64-campaign and c6upper-noty12 active and untouched; no lake build; nothing committed; 0 lean processes and 0
es310-/assemble310- scopes left. build/es310 now 757 MB of test output.

New: freeze_es310.sh (sha 8a0b1f49; not run on the real script: its 4 pins are still empty), logs/es310/OPERATOR.md.
Still open: the freeze itself (k, exporter and script pins: user decision); the swapped-base-path case is caught by
coverage only (unchanged, by design); the full-scale import walk (about 17 GB at k = 16) is still untested.
